"""Domain label sets are DATA (label_presets/*.json), never customer-specific code in the shared catalog."""

from __future__ import annotations

import json
from pathlib import Path

import matrx_files.analysis.label_catalog as catalog

SOURCE = Path(catalog.__file__).read_text(encoding="utf-8")


def test_the_code_carries_no_trade_specific_labels() -> None:
    for word in ("workers_comp", "Workers'", "impairment", "wcab", "WPI"):
        assert word.lower() not in SOURCE.lower(), word


def test_presets_are_merged_in_from_data_files() -> None:
    folder = Path(catalog.__file__).parent / "label_presets"
    files = sorted(folder.glob("*.json"))
    assert files, "the domain presets moved to data files"
    ids = {e["id"] for e in catalog.get_label_catalog()}
    cats = catalog.get_categories()
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        assert cats[data["category"]] == data["display_name"]
        assert {e["id"] for e in data["labels"]} <= ids
    assert catalog.get_label("claim_number") is not None
