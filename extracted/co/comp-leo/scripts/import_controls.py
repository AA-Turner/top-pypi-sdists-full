#!/usr/bin/env python3
"""
Bulk import PCI controls into controls_catalog.json

Usage:
  python scripts/import_controls.py --input controls.csv [--format csv|tsv|json] \
      [--catalog comp_leo/policies/controls_catalog.json]

CSV/TSV must contain headers:
  Control_ID,Standard_Name,Section_Title,Requirement_Ref,Requirement_Description,
  Requirement_Type,Version,Domain,Scope
"""
import argparse
import csv
import json
import os
from typing import List, Dict

DEFAULT_CATALOG = os.path.join(os.path.dirname(__file__), "..", "comp_leo", "policies", "controls_catalog.json")

REQUIRED_FIELDS = [
    "Control_ID",
    "Standard_Name",
    "Section_Title",
    "Requirement_Ref",
    "Requirement_Description",
    "Requirement_Type",
    "Version",
    "Domain",
    "Scope",
]

def load_catalog(path: str) -> Dict:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"schema_version": "1.0.0", "source": "PCI multi-standard controls catalog", "controls": []}


def save_catalog(path: str, catalog: Dict):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)


def import_rows(rows: List[Dict[str, str]], catalog: Dict) -> int:
    existing = {c.get("Control_ID"): i for i, c in enumerate(catalog.get("controls", [])) if c.get("Control_ID")}
    added = 0
    for row in rows:
        # normalize keys
        item = {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items() if k}
        if not item.get("Control_ID"):
            continue
        # ensure required fields present
        for f in REQUIRED_FIELDS:
            item.setdefault(f, "")
        if item["Control_ID"] in existing:
            catalog["controls"][existing[item["Control_ID"]]] = item
        else:
            catalog.setdefault("controls", []).append(item)
            added += 1
    return added


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Path to controls file (csv/tsv/json)")
    p.add_argument("--format", choices=["csv", "tsv", "json"], default=None, help="Input format; inferred from extension if omitted")
    p.add_argument("--catalog", default=DEFAULT_CATALOG, help="Path to controls_catalog.json")
    return p.parse_args()


def main():
    args = parse_args()
    fmt = args.format or os.path.splitext(args.input)[1].lstrip(".").lower()
    cat = load_catalog(args.catalog)

    rows: List[Dict[str, str]] = []
    if fmt == "json":
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "controls" in data:
                rows = data["controls"]
            elif isinstance(data, list):
                rows = data
            else:
                raise SystemExit("Unsupported JSON structure; expected list or {controls: [...]}.")
    else:
        delimiter = "," if fmt == "csv" else "\t"
        with open(args.input, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            rows = list(reader)

    added = import_rows(rows, cat)
    save_catalog(args.catalog, cat)
    print(f"Imported {len(rows)} rows; added/updated {added} new controls. Catalog now has {len(cat.get('controls', []))} entries.")


if __name__ == "__main__":
    main()
