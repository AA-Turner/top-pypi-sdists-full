"""Tests for _is_backslash_escaped()."""

import pytest

from agentic_devtools.cli.ci.evaluator.snapshot_comment_sanitization import _is_backslash_escaped


@pytest.mark.parametrize(
    ("body", "idx", "expected"),
    [
        (r"\<!--", 1, True),
        (r"\\<!--", 2, False),
        ("<!--", 0, False),
    ],
)
def test_is_backslash_escaped(body: str, idx: int, expected: bool) -> None:
    """Odd backslash runs escape the marker, while even runs do not."""
    assert _is_backslash_escaped(body, idx) is expected
