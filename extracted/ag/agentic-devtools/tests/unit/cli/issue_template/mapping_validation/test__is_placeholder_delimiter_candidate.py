"""Tests for the _is_placeholder_delimiter_candidate helper."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.mapping_validation import _is_placeholder_delimiter_candidate


def _flags(lines: list[str]) -> list[bool]:
    return [False] * len(lines)


def test_placeholder_bearing_delimiter_candidate_returns_true() -> None:
    lines = ["| Property | Value |", "| --- | {{created_at}} |"]
    assert _is_placeholder_delimiter_candidate(lines, 1, _flags(lines)) is True


def test_three_column_placeholder_bearing_delimiter_candidate_returns_true() -> None:
    lines = ["| A | B | C |", "| --- | {{created_at}} | Extra |"]
    assert _is_placeholder_delimiter_candidate(lines, 1, _flags(lines)) is True


def test_non_candidate_row_returns_false() -> None:
    lines = ["| Field | Value |"]
    assert _is_placeholder_delimiter_candidate(lines, 0, _flags(lines)) is False


def test_fenced_row_returns_false() -> None:
    lines = ["| --- | {{created_at}} |"]
    assert _is_placeholder_delimiter_candidate(lines, 0, [True]) is False


def test_selected_table_data_row_returns_false() -> None:
    lines = [
        "| Property | Value |",
        "| --- | --- |",
        "| --- | {{created_at}} |",
    ]
    assert _is_placeholder_delimiter_candidate(lines, 2, _flags(lines)) is False


def test_standalone_placeholder_bearing_delimiter_row_returns_false() -> None:
    lines = ["| --- | {{created_at}} |"]
    assert _is_placeholder_delimiter_candidate(lines, 0, _flags(lines)) is False


def test_already_delimited_table_data_row_returns_false() -> None:
    lines = [
        "| Property | Value |",
        "| --- | --- |",
        "| Alpha | beta |",
        "| --- | {{created_at}} |",
    ]
    assert _is_placeholder_delimiter_candidate(lines, 3, _flags(lines)) is False


def test_candidate_with_non_delimiter_row_two_lines_back_returns_true() -> None:
    lines = [
        "| Earlier | Row |",
        "| Property | Value |",
        "| --- | {{created_at}} |",
    ]
    assert _is_placeholder_delimiter_candidate(lines, 2, _flags(lines)) is True
