"""Tests for ``RoundAssignments``."""

import pytest

from agentic_devtools.orchestration.trio_config import RoundAssignments


def test_roundassignments_tracks_effective_phase_and_validates_mapping() -> None:
    result = RoundAssignments(
        "standard",
        "heavyweight_checkpoint",
        {"doer": "mai-code-1.1-flash", "heavyweightDuckA": "claude-opus-4.8"},
    )
    assert result.escalated
    assert len(result) == 2
    assert result["doer"] == "mai-code-1.1-flash"
    assert dict(result.items()) == {"doer": "mai-code-1.1-flash", "heavyweightDuckA": "claude-opus-4.8"}
    with pytest.raises(ValueError):
        RoundAssignments("other", "standard", {"doer": "mai-code-1.1-flash"})  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        RoundAssignments("standard", "other", {"doer": "mai-code-1.1-flash"})  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        RoundAssignments("standard", "standard", {})  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        RoundAssignments("standard", "standard", ["mai-code-1.1-flash"])  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        RoundAssignments("standard", "standard", {"other": "mai-code-1.1-flash"})
    with pytest.raises(ValueError):
        RoundAssignments("standard", "standard", {"doer": None})  # type: ignore[dict-item]
