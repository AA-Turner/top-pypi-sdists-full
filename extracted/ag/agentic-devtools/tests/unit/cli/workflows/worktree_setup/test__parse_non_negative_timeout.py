"""Tests for _parse_non_negative_timeout."""

import pytest

from agentic_devtools.cli.workflows.worktree_setup import _parse_non_negative_timeout


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        (" +1200 ", 1200),
        ("１２", 12),
    ],
)
def test_parses_valid_non_negative_timeout(value, expected):
    """Valid non-negative integer values are parsed."""
    assert _parse_non_negative_timeout(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        None,
        True,
        -1,
        "-1",
        1.5,
        "1.5",
        "",
        "²",
        "9" * 5000,
        [],
    ],
)
def test_rejects_invalid_timeout(value):
    """Unsupported values return no timeout."""
    assert _parse_non_negative_timeout(value) is None
