"""Tests for _advance_column()."""

import pytest

from agentic_devtools.cli.ci.evaluator.snapshot_markdown_blocks import _advance_column


@pytest.mark.parametrize(
    ("char", "expected"),
    [
        ("\t", 4),
        (" ", 2),
        ("x", 1),
    ],
)
def test_advance_column(char: str, expected: int) -> None:
    """Whitespace advances the visual column, while other characters do not."""
    assert _advance_column(1, char) == expected
