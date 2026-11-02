"""Bare-venv tests for the shared rows -> markdown table primitive."""

from __future__ import annotations

from matrx_files.specific_handlers.table_markdown import md_escape, rows_to_markdown


def test_empty_rows_returns_empty():
    assert rows_to_markdown([]) == ""
    assert rows_to_markdown([[]]) == ""  # single zero-width row


def test_single_row_header_emits_separator():
    out = rows_to_markdown([["A", "B"]], header=True)
    assert out == "| A | B |\n| --- | --- |"


def test_basic_header_table():
    out = rows_to_markdown([["Region", "Rev"], ["North", "100"], ["South", "80"]])
    assert out == (
        "| Region | Rev |\n"
        "| --- | --- |\n"
        "| North | 100 |\n"
        "| South | 80 |"
    )


def test_header_false_has_no_separator():
    out = rows_to_markdown([["a", "b"], ["c", "d"]], header=False)
    assert out == "| a | b |\n| c | d |"
    assert "---" not in out


def test_ragged_rows_padded_to_max_width():
    out = rows_to_markdown([["h1", "h2", "h3"], ["only"], ["a", "b"]])
    lines = out.split("\n")
    # separator sized to the widest row (3 cols)
    assert lines[1] == "| --- | --- | --- |"
    # short body rows padded with empty cells to full width
    assert lines[2] == "| only |  |  |"
    assert lines[3] == "| a | b |  |"


def test_escaping_pipe_and_newline():
    out = rows_to_markdown([["a|b", "c\nd"]], header=True)
    assert out.splitlines()[0] == r"| a\|b | c d |"


def test_md_escape_tolerates_none_and_trims():
    assert md_escape(None) == ""  # type: ignore[arg-type]
    assert md_escape("  x  ") == "x"
    assert md_escape("a|b") == r"a\|b"
    assert md_escape("line1\nline2") == "line1 line2"
