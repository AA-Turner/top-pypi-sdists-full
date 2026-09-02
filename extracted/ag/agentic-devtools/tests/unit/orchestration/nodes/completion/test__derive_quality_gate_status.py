"""Tests for _derive_quality_gate_status."""

from __future__ import annotations

from typing import Any, cast

from agentic_devtools.orchestration.nodes.completion import _derive_quality_gate_status
from agentic_devtools.orchestration.state_schema import WorkOnIssueState


class TestDeriveQualityGateStatus:
    """Tests for gate status derivation from recorded verification events."""

    def _state(self, **kwargs: Any) -> WorkOnIssueState:
        return cast(WorkOnIssueState, kwargs)

    def test_returns_fail_when_no_events_key(self) -> None:
        result = _derive_quality_gate_status(self._state())
        assert result == "fail"

    def test_returns_fail_when_events_is_not_list(self) -> None:
        result = _derive_quality_gate_status(self._state(events="not a list"))
        assert result == "fail"

    def test_returns_fail_when_events_list_is_empty(self) -> None:
        result = _derive_quality_gate_status(self._state(events=[]))
        assert result == "fail"

    def test_returns_pass_for_verification_passed_event(self) -> None:
        state = self._state(events=[{"event": "verification_passed"}])
        result = _derive_quality_gate_status(state)
        assert result == "pass"

    def test_returns_fail_for_verification_failed_event(self) -> None:
        state = self._state(events=[{"event": "verification_failed"}])
        result = _derive_quality_gate_status(state)
        assert result == "fail"

    def test_uses_last_event_when_multiple_verification_events(self) -> None:
        state = self._state(
            events=[
                {"event": "verification_passed"},
                {"event": "verification_failed"},
            ]
        )
        # The last event in reversed order is the first in list; "failed" wins
        result = _derive_quality_gate_status(state)
        assert result == "fail"

    def test_last_pass_event_wins_over_earlier_failure(self) -> None:
        state = self._state(
            events=[
                {"event": "verification_failed"},
                {"event": "verification_passed"},
            ]
        )
        result = _derive_quality_gate_status(state)
        assert result == "pass"

    def test_ignores_non_dict_events(self) -> None:
        state = self._state(events=["bad", None, {"event": "verification_passed"}])
        result = _derive_quality_gate_status(state)
        assert result == "pass"
