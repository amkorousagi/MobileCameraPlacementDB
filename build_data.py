#!/usr/bin/env python3
"""Build SQLite, JSON, XML, and CSV exports from schema.sql.

Standard library only: sqlite3, json, csv, xml.etree.ElementTree, os.
"""

from __future__ import annotations

import csv
import json
import os
import sqlite3
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(ROOT, "schema.sql")
OUTPUT_DIR = os.path.join(ROOT, "output")
DB_PATH = os.path.join(OUTPUT_DIR, "devices.db")
JSON_PATH = os.path.join(OUTPUT_DIR, "devices.json")
CSV_PATH = os.path.join(OUTPUT_DIR, "devices.csv")
XML_PATH = os.path.join(OUTPUT_DIR, "devices.xml")

COLUMNS = (
    "id",
    "model_id",
    "market_name",
    "platform",
    "camera_position_portrait",
    "updated_at",
)


def read_schema() -> str:
    if not os.path.isfile(SCHEMA_PATH):
        raise FileNotFoundError("schema.sql not found next to build_data.py")
    with open(SCHEMA_PATH, "r", encoding="utf-8") as handle:
        return handle.read()


def build_sqlite(schema_sql: str) -> list[dict]:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if os.path.isfile(DB_PATH):
        os.remove(DB_PATH)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        connection.executescript(schema_sql)
        rows = connection.execute(
            """
            SELECT id, model_id, market_name, platform,
                   camera_position_portrait, updated_at
            FROM devices
            ORDER BY id
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def export_json(rows: list[dict]) -> None:
    with open(JSON_PATH, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(rows, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def export_csv(rows: list[dict]) -> None:
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(COLUMNS))
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row[column] for column in COLUMNS})


def export_xml(rows: list[dict]) -> None:
    root = ET.Element("devices")
    for row in rows:
        device = ET.SubElement(root, "device")
        for column in COLUMNS:
            child = ET.SubElement(device, column)
            value = row[column]
            child.text = "" if value is None else str(value)
    ET.indent(root, space="  ")
    xml_body = ET.tostring(root, encoding="unicode")
    with open(XML_PATH, "w", encoding="utf-8", newline="\n") as handle:
        handle.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        handle.write(xml_body)
        handle.write("\n")


def main() -> int:
    schema_sql = read_schema()
    rows = build_sqlite(schema_sql)
    export_json(rows)
    export_csv(rows)
    export_xml(rows)
    print("Built {count} devices:".format(count=len(rows)))
    print("  {path}".format(path=os.path.relpath(DB_PATH, ROOT)))
    print("  {path}".format(path=os.path.relpath(JSON_PATH, ROOT)))
    print("  {path}".format(path=os.path.relpath(CSV_PATH, ROOT)))
    print("  {path}".format(path=os.path.relpath(XML_PATH, ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
