"""Tests for parse_table in derive_customization_disposition."""

from __future__ import annotations

import pytest

from tests.scripts.derive_customization_disposition import REPO_ROOT, derive

PUBLISHED = REPO_ROOT / derive.PUBLISHED_PATH


def test_round_trips_the_published_table() -> None:
    """`--verify-partition` must read the table the way a later issue would."""
    rows = derive.parse_table(PUBLISHED.read_text(encoding="utf-8"))
    derived = derive.derive_rows(REPO_ROOT)
    assert [(r.path, r.disposition, r.group, r.target, r.batch) for r in rows] == [
        (r.path, r.disposition, r.group, r.target, r.batch) for r in derived
    ]


def test_summary_tables_above_the_rows_are_ignored() -> None:
    """Only the table under the rows heading is parsed."""
    text = (
        "| `.github/agents/agdt.a.agent.md` | delete | a reason |\n"
        f"\n{derive.ROWS_HEADING}\n"
        "| `.github/agents/agdt.a.agent.md` | `agdt.a` | delete | - | - | wrappers |\n"
    )
    rows = derive.parse_table(text)
    assert len(rows) == 1
    assert rows[0].batch == "wrappers"


def test_document_without_a_rows_section_raises() -> None:
    """A document with no rows heading cannot be verified."""
    with pytest.raises(ValueError, match="no '## Rows' section"):
        derive.parse_table("# Title\n")


def test_malformed_row_raises() -> None:
    """A row with the wrong column count is an error, not a silent skip."""
    text = f"\n{derive.ROWS_HEADING}\n| `.github/agents/agdt.a.agent.md` | `agdt.a` | delete |\n"
    with pytest.raises(ValueError, match="malformed row"):
        derive.parse_table(text)


def test_document_with_no_rows_raises() -> None:
    """An empty rows section carries no map."""
    with pytest.raises(ValueError, match="no rows found"):
        derive.parse_table(f"\n{derive.ROWS_HEADING}\n\nNothing here.\n")
