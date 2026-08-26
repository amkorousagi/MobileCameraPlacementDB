#!/usr/bin/env python3
"""Build output artifacts (SQLite / JSON / XML / CSV) from schema.sql.

schema.sql is the single source of truth. Every value in it, including
updated_at, is a literal, so re-running this script on the same schema.sql
produces byte-identical outputs. Standard library only.
"""
import csv
import json
import os
import sqlite3
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(ROOT, "schema.sql")
OUTPUT_DIR = os.path.join(ROOT, "output")

COLUMNS = ["id", "model_id", "market_name", "platform",
           "camera_position_portrait", "updated_at"]


def build_db(schema_sql, db_path):
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    conn.executescript(schema_sql)
    conn.commit()
    return conn


def write_json(rows, path):
    devices = [dict(zip(COLUMNS, row)) for row in rows]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(devices, f, indent=2, ensure_ascii=False)
        f.write("\n")


def write_csv(rows, path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
        writer.writerows(rows)


def write_min_csv(rows, path):
    """Minimal lookup table for memory-constrained apps.

    No header; two columns: model_id, camera_position_portrait as a single
    uppercase letter (T=TOP, R=RIGHT, L=LEFT). Row order matches the other
    outputs (ORDER BY id).
    """
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow([row[1], row[4][0]])


def write_xml(rows, path):
    root = ET.Element("devices", {"count": str(len(rows))})
    for row in rows:
        device = ET.SubElement(root, "device")
        for col, value in zip(COLUMNS, row):
            ET.SubElement(device, col).text = str(value)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True)
    with open(path, "ab") as f:
        f.write(b"\n")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema_sql = f.read()

    conn = build_db(schema_sql, os.path.join(OUTPUT_DIR, "devices.db"))
    rows = conn.execute(
        "SELECT id, model_id, market_name, platform,"
        " camera_position_portrait, updated_at FROM devices ORDER BY id"
    ).fetchall()
    conn.close()

    write_json(rows, os.path.join(OUTPUT_DIR, "devices.json"))
    write_csv(rows, os.path.join(OUTPUT_DIR, "devices.csv"))
    write_min_csv(rows, os.path.join(OUTPUT_DIR, "devices.min.csv"))
    write_xml(rows, os.path.join(OUTPUT_DIR, "devices.xml"))

    print(f"built {len(rows)} devices -> "
          f"output/devices.{{db,json,csv,min.csv,xml}}")


if __name__ == "__main__":
    main()
