#!/usr/bin/env python3
"""Monthly sync of device identifier sources into schema.sql.

Sources (primary -> fallback):
  iOS:     AppleDB main.json.gz  -> DeviceKit Device.generated.swift
  Android: Google Play certified devices by_model.json -> official Play CSV

Rules:
  * Only NEW model_ids are inserted. camera_position_portrait of existing
    rows is never overwritten.
  * market_name may be updated when the primary source is more accurate.
  * schema.sql is rewritten canonically (INSERTs in chunks of 200) only when
    the catalog actually changed. updated_at is written as a literal ISO-8601
    UTC timestamp so build_data.py stays deterministic.

Standard library only.
"""
import csv
import gzip
import io
import json
import os
import re
import sqlite3
import sys
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(ROOT, "schema.sql")
OUTPUT_DIR = os.path.join(ROOT, "output")
STATS_PATH = os.path.join(OUTPUT_DIR, "stats.json")

APPLEDB_URL = "https://api.appledb.dev/device/main.json.gz"
DEVICEKIT_URL = ("https://raw.githubusercontent.com/devicekit/DeviceKit/"
                 "master/Source/Device.generated.swift")
PLAY_JSON_URL = ("https://raw.githubusercontent.com/androidtrackers/"
                 "certified-android-devices/master/by_model.json")
PLAY_CSV_URL = "https://storage.googleapis.com/play_public/supported_devices.csv"

INSERT_CHUNK = 200
MOBILE_IDENT_RE = re.compile(r"^(iPhone|iPad|iPod)\d+,\d+$")

SCHEMA_HEADER = """\
-- MobileCameraPlacementDB — source of truth
-- Front camera position of mobile devices, portrait orientation.
--   RIGHT: long edge (right side in portrait, top in landscape video call)
--   TOP:   short edge (phones, older tablets, iPad mini)
--   LEFT:  opposite long edge (reserved)
-- Rows are maintained by sync_sources.py. camera_position_portrait of an
-- existing row is never overwritten by sync; only market_name may be updated.
-- updated_at is an explicit ISO-8601 UTC literal so rebuilds are deterministic.

CREATE TABLE IF NOT EXISTS devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id TEXT UNIQUE NOT NULL,
    market_name TEXT NOT NULL,
    platform TEXT NOT NULL CHECK (platform IN ('iOS','Android')),
    camera_position_portrait TEXT NOT NULL CHECK (camera_position_portrait IN ('RIGHT','TOP','LEFT')),
    updated_at DATETIME
);
"""


def fetch(url, timeout=120):
    req = urllib.request.Request(
        url, headers={"User-Agent": "MobileCameraPlacementDB-sync/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


# ---------------------------------------------------------------- iOS rules

def classify_ios(ident, name, soc=""):
    """Front camera edge for an Apple mobile identifier (portrait)."""
    if not ident.startswith("iPad"):
        return "TOP"  # every iPhone / iPod touch
    low = name.lower()
    if "mini" in low:
        return "TOP"  # all iPad mini, incl. A17 Pro
    m = re.search(r"\bM(\d+)\b", soc or "") or re.search(r"\(M(\d+)\)", name)
    m_gen = int(m.group(1)) if m else None
    if "pro" in low:
        return "RIGHT" if m_gen is not None and m_gen >= 4 else "TOP"
    if "air" in low:
        return "RIGHT" if m_gen is not None and m_gen >= 2 else "TOP"
    gen = re.search(r"\((\d+)(?:st|nd|rd|th) generation\)", name)
    if gen:
        return "RIGHT" if int(gen.group(1)) >= 10 else "TOP"
    a = re.search(r"\bA(\d+)", soc or "") or re.search(r"\(A(\d+)\)", name)
    if a:
        return "RIGHT" if int(a.group(1)) >= 16 else "TOP"
    return "TOP"


def load_appledb():
    entries = json.loads(gzip.decompress(fetch(APPLEDB_URL)))
    devices = {}
    stats = {
        "source": "AppleDB (api.appledb.dev/device/main.json.gz)",
        "skipped_unreleased": 0,
        "skipped_watch": 0,
        "skipped_apple_tv": 0,
        "skipped_vision": 0,
    }
    for entry in entries:
        etype = entry.get("type", "")
        if etype == "Apple Watch":
            stats["skipped_watch"] += 1
            continue
        if etype == "Apple TV":
            stats["skipped_apple_tv"] += 1
            continue
        if etype in ("Headset", "RealityDevice", "Vision"):
            stats["skipped_vision"] += 1
            continue
        idents = [i for i in entry.get("identifier", [])
                  if MOBILE_IDENT_RE.match(i)]
        if not idents:
            continue  # accessories, Macs, software, ...
        released = entry.get("released")
        if not released:
            stats["skipped_unreleased"] += len(idents)
            continue
        if isinstance(released, str):
            released = [released]
        year = min(int(r[:4]) for r in released if r[:4].isdigit())
        for ident in idents:
            devices.setdefault(ident, {
                "name": entry.get("name", ident),
                "soc": entry.get("soc", ""),
                "year": year,
            })
    stats["mapped_iphone"] = sum(1 for i in devices if i.startswith("iPhone"))
    stats["mapped_ipad"] = sum(1 for i in devices if i.startswith("iPad"))
    stats["mapped_ipod"] = sum(1 for i in devices if i.startswith("iPod"))
    stats["mapped_total"] = len(devices)
    return devices, stats


def load_devicekit():
    """Fallback only: merges Wi-Fi/Cellular under one name, fewer iPads."""
    text = fetch(DEVICEKIT_URL).decode("utf-8")
    # e.g.  case "iPad16,3", "iPad16,4": return iPadPro11M4
    ident_cases = re.findall(
        r'case ((?:"(?:iPhone|iPad|iPod)\d+,\d+"(?:,\s*)?)+):\s*return (\w+)',
        text)
    # e.g.  case .iPadPro11M4: return "iPad Pro (11-inch) (M4)"
    case_to_name = dict(re.findall(r'case \.(\w+):\s*return "([^"]+)"', text))
    devices = {}
    for idents_blob, case in ident_cases:
        for ident in re.findall(r'"([^"]+)"', idents_blob):
            devices.setdefault(ident, {
                "name": case_to_name.get(case, case),
                "soc": "",
                "year": None,
            })
    stats = {
        "source": "DeviceKit Device.generated.swift (fallback)",
        "mapped_iphone": sum(1 for i in devices if i.startswith("iPhone")),
        "mapped_ipad": sum(1 for i in devices if i.startswith("iPad")),
        "mapped_ipod": sum(1 for i in devices if i.startswith("iPod")),
        "mapped_total": len(devices),
    }
    return devices, stats


# ------------------------------------------------------------ Android rules

NON_MOBILE_RE = re.compile(
    r"\btv\b|set[\s-]?top|chromebook|galaxy book|laptop|watch|\bwear\b|"
    r"\bcamera\b", re.IGNORECASE)
GALAXY_TAB_S_RE = re.compile(r"galaxy tab s(\d{1,2})\b", re.IGNORECASE)
TABLET_HINT_RE = re.compile(r"tab(?![a-z])|tablet|pad(?![a-z])", re.IGNORECASE)


def classify_android(brand, name):
    """Front camera edge for an Android device (portrait).

    Phones are TOP (foldable inner cameras vary, but per Build.MODEL the
    convention here is TOP). Only specific landscape-first tablet families
    are RIGHT.
    """
    low = name.lower()
    blow = brand.lower()
    # verified short-edge exceptions inside otherwise landscape-first
    # families (see docs/camera-position-references.md)
    if re.search(r"\bpad mini\b", low):
        return "TOP"  # Oppo Pad Mini, Xiaomi Pad Mini (~8.x", portrait camera)
    if re.search(r"xiaomi pad 5\b", low):
        return "TOP"  # Pad 5 family is short-edge; long edge starts with Pad 6
                      # (existing 22081281AC = Pad 5 Pro 12.4 RIGHT is preserved)
    if re.search(r"redmi pad se (8\.7|4g)", low):
        return "TOP"  # 8.7" SE line is phone-style (4G = SE 8.7 in India)
    if "honor pad x7" in low:
        return "TOP"  # 8.7" phone-style
    m = GALAXY_TAB_S_RE.search(low)
    if m and int(m.group(1)) >= 7:
        return "RIGHT"  # Tab S7+ era incl. +/Ultra/FE/Lite
    if "pixel tablet" in low:
        return "RIGHT"
    if "oneplus pad" in low or "oppo pad" in low:
        return "RIGHT"
    if re.search(r"\b(xiaomi|redmi|poco) pad\b", low):
        return "RIGHT"
    if "honor pad" in low or "magicpad" in low or "magic pad" in low:
        return "RIGHT"
    if "matepad pro" in low and "huawei" in (blow + " " + low):
        return "RIGHT"
    if re.search(r"tab p1[12]\b", low) and "lenovo" in (blow + " " + low):
        return "RIGHT"
    return "TOP"


def pick_android_name(entries):
    """Deterministic marketing name: prefer branded entries, then sort."""
    candidates = []
    for entry in entries:
        name = (entry.get("name") or "").strip()
        if not name:
            continue
        brand = (entry.get("brand") or "").strip()
        if brand and not name.lower().startswith(brand.lower()):
            full = f"{brand} {name}"
        else:
            full = name
        candidates.append((0 if brand else 1, full, brand, name))
    if not candidates:
        return None
    candidates.sort()
    _, full, brand, name = candidates[0]
    return full, brand, name


def load_play_json():
    models = json.loads(fetch(PLAY_JSON_URL))
    source = ("Google Play certified devices "
              "(androidtrackers by_model.json, daily mirror of official CSV)")
    return models, source


def load_play_csv():
    text = fetch(PLAY_CSV_URL).decode("utf-16")
    reader = csv.reader(io.StringIO(text))
    next(reader, None)  # Retail Branding, Marketing Name, Device, Model
    models = {}
    for row in reader:
        if len(row) < 4:
            continue
        brand, marketing, device, model = (c.strip() for c in row[:4])
        if not model:
            continue
        models.setdefault(model, []).append(
            {"brand": brand, "name": marketing, "device": device})
    return models, "Google Play supported_devices.csv (official, fallback)"


def load_android():
    try:
        return load_play_json()
    except Exception as exc:  # noqa: BLE001 - any fetch/parse error -> fallback
        print(f"WARN: Play by_model.json failed ({exc}); "
              f"falling back to official CSV", file=sys.stderr)
        return load_play_csv()


def load_ios():
    try:
        return load_appledb(), True
    except Exception as exc:  # noqa: BLE001
        print(f"WARN: AppleDB failed ({exc}); falling back to DeviceKit",
              file=sys.stderr)
        return load_devicekit(), False


# ----------------------------------------------------------- schema rewrite

def load_existing():
    conn = sqlite3.connect(":memory:")
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        conn.executescript(f.read())
    rows = conn.execute(
        "SELECT model_id, market_name, platform, camera_position_portrait,"
        " updated_at FROM devices ORDER BY id").fetchall()
    conn.close()
    return [list(r) for r in rows]


def sql_quote(value):
    return "'" + str(value).replace("'", "''") + "'"


def render_schema(rows):
    parts = [SCHEMA_HEADER]
    for start in range(0, len(rows), INSERT_CHUNK):
        chunk = rows[start:start + INSERT_CHUNK]
        values = ",\n".join(
            "({},{},{},{},{})".format(*(sql_quote(v) for v in row))
            for row in chunk)
        parts.append(
            "INSERT INTO devices (model_id, market_name, platform,"
            " camera_position_portrait, updated_at) VALUES\n" + values + ";")
    return "\n".join(parts) + "\n"


# ------------------------------------------------------------------- stats

def pct(part, total):
    return round(100.0 * part / total, 2) if total else 0.0


def build_stats(rows, ios_devices, ios_stats, ios_primary,
                android_source_keys, android_stats):
    by_platform, by_position = {}, {"TOP": 0, "RIGHT": 0, "LEFT": 0}
    by_platform_position = {}
    for _, _, platform, position, _ in rows:
        by_platform[platform] = by_platform.get(platform, 0) + 1
        by_position[position] = by_position.get(position, 0) + 1
        by_platform_position.setdefault(platform, {})
        by_platform_position[platform][position] = \
            by_platform_position[platform].get(position, 0) + 1
    total = len(rows)

    ipad_by_year = {}
    if ios_primary:
        pos_by_ident = {r[0]: r[3] for r in rows if r[2] == "iOS"}
        for ident, info in ios_devices.items():
            if not ident.startswith("iPad") or info["year"] is None:
                continue
            year = str(info["year"])
            bucket = ipad_by_year.setdefault(
                year, {"total": 0, "RIGHT": 0, "TOP": 0})
            bucket["total"] += 1
            position = pos_by_ident.get(ident)
            if position in bucket:
                bucket[position] += 1
        ipad_by_year = dict(sorted(ipad_by_year.items()))
    else:
        ipad_by_year = {
            "note": "unavailable (DeviceKit fallback has no release dates)"}

    return {
        "catalog_total": total,
        "by_platform": by_platform,
        "by_position": by_position,
        "by_position_pct": {k: pct(v, total) for k, v in by_position.items()},
        "by_platform_position": by_platform_position,
        "sources": {
            "ios": ios_stats,
            "android": {**android_stats, "source_keys": android_source_keys},
        },
        "ipad_by_release_year": ipad_by_year,
    }


# -------------------------------------------------------------------- main

def main():
    existing = load_existing()
    index = {row[0]: row for row in existing}
    today = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00Z")

    (ios_devices, ios_stats), ios_primary = load_ios()
    android_models, android_source = load_android()

    added_ios = added_android = renamed = 0

    for ident in sorted(ios_devices):
        info = ios_devices[ident]
        if ident in index:
            row = index[ident]
            # primary source names are canonical (Wi-Fi vs Cellular split);
            # never let the coarser DeviceKit fallback rename rows
            if ios_primary and info["name"] and row[1] != info["name"]:
                row[1] = info["name"]
                row[4] = today
                renamed += 1
        else:
            position = classify_ios(ident, info["name"], info["soc"])
            row = [ident, info["name"], "iOS", position, today]
            existing.append(row)
            index[ident] = row
            added_ios += 1

    android_stats = {
        "source": android_source,
        "skipped_empty_name": 0,
        "skipped_non_mobile": 0,
        "mapped": 0,
        "mapped_phones": 0,
        "mapped_tablets": 0,
    }
    for model in sorted(android_models):
        if not model.strip():
            android_stats["skipped_empty_name"] += 1
            continue
        picked = pick_android_name(android_models[model])
        if picked is None:
            android_stats["skipped_empty_name"] += 1
            continue
        full, brand, name = picked
        if NON_MOBILE_RE.search(full):
            android_stats["skipped_non_mobile"] += 1
            continue
        android_stats["mapped"] += 1
        if TABLET_HINT_RE.search(full):
            android_stats["mapped_tablets"] += 1
        else:
            android_stats["mapped_phones"] += 1
        if model in index:
            row = index[model]
            if row[1] != full:
                row[1] = full
                row[4] = today
                renamed += 1
        else:
            position = classify_android(brand, full)
            row = [model, full, "Android", position, today]
            existing.append(row)
            index[model] = row
            added_android += 1
    android_stats["mapped_pct"] = pct(
        android_stats["mapped"], len(android_models))

    rendered = render_schema(existing)
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        changed = f.read() != rendered
    if changed:
        with open(SCHEMA_PATH, "w", encoding="utf-8", newline="\n") as f:
            f.write(rendered)

    stats = build_stats(existing, ios_devices, ios_stats, ios_primary,
                        len(android_models), android_stats)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(STATS_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(json.dumps(stats, indent=2, ensure_ascii=False))
    if android_stats["mapped_pct"] < 90:
        print(f"WARN: Android mapped_pct={android_stats['mapped_pct']} "
              f"is unusually low — check the source", file=sys.stderr)
    if added_ios or added_android or renamed:
        print(f"sync: +{added_ios} iOS, +{added_android} Android, "
              f"{renamed} names updated -> schema.sql "
              f"({'rewritten' if changed else 'unchanged'})")
    else:
        print("sync: no catalog changes")


if __name__ == "__main__":
    main()
