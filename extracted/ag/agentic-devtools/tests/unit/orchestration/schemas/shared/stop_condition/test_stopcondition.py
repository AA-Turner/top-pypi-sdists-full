"""Tests for StopCondition model."""

import json

from agentic_devtools.orchestration.schemas.shared.stop_condition import StopCondition


class TestStopCondition:
    """Tests for StopCondition construction and serialization."""

    def test_construction(self):
        condition = StopCondition(reason="Budget exceeded")
        assert condition.reason == "Budget exceeded"
        assert condition.is_recoverable is False
        assert condition.details == ""

    def test_full_construction(self):
        condition = StopCondition(
            reason="Token limit reached",
            is_recoverable=True,
            details="Used 50k of 40k budget",
        )
        assert condition.is_recoverable is True
        assert condition.details == "Used 50k of 40k budget"

    def test_model_dump(self):
        condition = StopCondition(reason="Blocked", is_recoverable=True)
        data = condition.model_dump()
        assert data["reason"] == "Blocked"
        assert data["is_recoverable"] is True

    def test_model_validate_json(self):
        raw = json.dumps({"reason": "Halted", "is_recoverable": False})
        condition = StopCondition.model_validate_json(raw)
        assert condition.reason == "Halted"

    def test_round_trip(self):
        original = StopCondition(reason="Test", is_recoverable=True, details="d")
        raw = original.model_dump_json()
        restored = StopCondition.model_validate_json(raw)
        assert original == restored
