"""Tests for the FenceLineCandidate record."""

from dataclasses import FrozenInstanceError, fields

import pytest

from agentic_devtools.cli.ci.pipeline.markdown_fences import FenceLineCandidate


def test_stores_exact_fields_and_is_immutable() -> None:
    candidate = FenceLineCandidate(12, "`", 3, True, False)

    assert tuple(field.name for field in fields(candidate)) == (
        "line_number",
        "marker",
        "run_length",
        "can_open",
        "can_close",
    )
    assert FenceLineCandidate.__annotations__ == {
        "line_number": int,
        "marker": str,
        "run_length": int,
        "can_open": bool,
        "can_close": bool,
    }
    assert candidate.line_number == 12
    assert candidate.marker == "`"
    assert candidate.run_length == 3
    assert candidate.can_open is True
    assert candidate.can_close is False
    with pytest.raises(FrozenInstanceError):
        setattr(candidate, "line_number", 13)
