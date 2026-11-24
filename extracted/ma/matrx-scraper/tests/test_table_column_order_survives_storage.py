"""A table's column order is data, not dict key order (L7i, 2026-11-09).

A parse held between workflow steps is stored as Postgres ``jsonb``, which re-sorts every
object's keys (shortest first). The read step's landing then rendered kunetictech.com's price
table with "Cost per kWh" moved to the second column, so the workflow wrote a different text
(and a second processed document) than the code path did for the same page. The table's data
form now names its columns in a list, and the portion walk reads that list.
"""

from __future__ import annotations

import json

from matrx_scraper.portions import from_organized_data

COLUMNS = ["System Size", "Typical Application", "Installed Cost (Total)", "Cost per kWh"]
ROW = {"System Size": "30 kW", "Typical Application": "Retail", "Installed Cost (Total)": "$39,000", "Cost per kWh": "$650"}


def _jsonb_order(row: dict[str, str]) -> dict[str, str]:
    """Postgres jsonb key order: shorter keys first, then bytewise."""
    return {k: row[k] for k in sorted(row, key=lambda k: (len(k.encode()), k.encode()))}


def test_a_stored_table_portions_in_the_page_column_order() -> None:
    fresh = [{"type": "table", "columns": COLUMNS, "rows": [ROW]}]
    stored = json.loads(json.dumps([{"type": "table", "columns": COLUMNS, "rows": [_jsonb_order(ROW)]}]))
    assert list(stored[0]["rows"][0]) != COLUMNS  # the storage really re-ordered the keys
    assert from_organized_data(stored)[0]["text"] == from_organized_data(fresh)[0]["text"]
    assert from_organized_data(stored)[0]["text"].split("\n")[:4] == COLUMNS


def test_the_parser_names_its_table_columns() -> None:
    from matrx_scraper.parser.data_types import ExtractionSettings, Table, TextContent  # noqa: PLC0415

    table = Table(content=[{col: [TextContent(content=ROW[col])] for col in COLUMNS}])
    data = table.to_data(ExtractionSettings(["text", "table"], ["data"]))
    assert data["columns"] == COLUMNS
    assert from_organized_data([data])[0]["text"].split("\n")[:4] == COLUMNS
