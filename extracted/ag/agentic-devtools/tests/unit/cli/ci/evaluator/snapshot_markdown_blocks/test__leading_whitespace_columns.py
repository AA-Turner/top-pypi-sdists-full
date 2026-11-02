"""Tests for _leading_whitespace_columns()."""

import pytest

from agentic_devtools.cli.ci.evaluator.snapshot_markdown_blocks import _leading_whitespace_columns


@pytest.mark.parametrize(
    ("text", "start_column", "expected"),
    [
        ("", 0, 0),
        ("  text", 0, 2),
        ("\ttext", 1, 3),
        (" \ttext", 1, 3),
    ],
)
def test_leading_whitespace_columns(text: str, start_column: int, expected: int) -> None:
    """Returns indentation width with tabs measured from the current column."""
    assert _leading_whitespace_columns(text, start_column=start_column) == expected
