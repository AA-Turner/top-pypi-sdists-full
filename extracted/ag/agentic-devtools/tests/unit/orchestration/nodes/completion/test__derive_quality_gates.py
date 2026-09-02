"""Tests for _derive_quality_gates."""

from __future__ import annotations

from typing import Any, cast

from agentic_devtools.orchestration.nodes.completion import _derive_quality_gates
from agentic_devtools.orchestration.state_schema import WorkOnIssueState


class TestDeriveQualityGates:
    """Tests for quality gate derivation from verification output and events."""

    def _state(self, **kwargs: Any) -> WorkOnIssueState:
        return cast(WorkOnIssueState, kwargs)

    def test_returns_empty_list_when_no_output_and_no_events(self) -> None:
        result = _derive_quality_gates(self._state())
        assert result == []

    def test_returns_gate_when_verification_passed_event_no_output(self) -> None:
        state = self._state(events=[{"event": "verification_passed"}])
        result = _derive_quality_gates(state)
        assert len(result) == 1
        assert result[0]["name"] == "Targeted checks"
        assert result[0]["status"] == "pass"
        assert result[0]["details"] == ""

    def test_returns_gate_when_verification_failed_event_no_output(self) -> None:
        state = self._state(events=[{"event": "verification_failed"}])
        result = _derive_quality_gates(state)
        assert len(result) == 1
        assert result[0]["status"] == "fail"

    def test_returns_gate_with_text_when_output_present(self) -> None:
        state = self._state(verification_output="All checks passed successfully")
        result = _derive_quality_gates(state)
        assert len(result) == 1
        assert "All checks passed successfully" in result[0]["details"]

    def test_truncates_details_at_200_chars(self) -> None:
        long_output = "x " * 150
        state = self._state(verification_output=long_output)
        result = _derive_quality_gates(state)
        assert len(result[0]["details"]) <= 200

    def test_truncated_details_end_with_ellipsis(self) -> None:
        long_output = "word " * 200
        state = self._state(verification_output=long_output)
        result = _derive_quality_gates(state)
        assert result[0]["details"].endswith("...")

    def test_status_pass_when_verification_passed_event_with_output(self) -> None:
        state = self._state(
            verification_output="Tests OK",
            events=[{"event": "verification_passed"}],
        )
        result = _derive_quality_gates(state)
        assert result[0]["status"] == "pass"

    def test_status_fail_when_no_events_but_has_output(self) -> None:
        state = self._state(verification_output="Some output", events=[])
        result = _derive_quality_gates(state)
        assert result[0]["status"] == "fail"
