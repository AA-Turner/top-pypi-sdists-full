"""Tests for the _is_table_delimiter_or_header helper."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.mapping_validation import _is_table_delimiter_or_header


def _flags(lines: list[str]) -> list[bool]:
    return [False] * len(lines)


def test_non_table_line_returns_false() -> None:
    lines = ["plain {{created_at}} text"]
    assert _is_table_delimiter_or_header(lines, 0, _flags(lines)) is False


def test_delimiter_row_returns_true() -> None:
    lines = ["| --- | --- |"]
    assert _is_table_delimiter_or_header(lines, 0, _flags(lines)) is True


def test_placeholder_bearing_delimiter_candidate_returns_true() -> None:
    lines = ["| Field | Value |", "| --- | {{created_at}} |"]
    assert _is_table_delimiter_or_header(lines, 1, _flags(lines)) is True


def test_header_row_followed_by_delimiter_returns_true() -> None:
    lines = ["| A | B |", "| --- | --- |"]
    assert _is_table_delimiter_or_header(lines, 0, _flags(lines)) is True


def test_header_row_not_followed_by_delimiter_returns_false() -> None:
    lines = ["| A | B |", "| data | data |"]
    assert _is_table_delimiter_or_header(lines, 0, _flags(lines)) is False


def test_three_column_row_returns_false() -> None:
    lines = ["| A | B | C |", "| --- | --- | --- |"]
    assert _is_table_delimiter_or_header(lines, 0, _flags(lines)) is False


def test_fenced_line_returns_false() -> None:
    lines = ["| --- | --- |"]
    assert _is_table_delimiter_or_header(lines, 0, [True]) is False
