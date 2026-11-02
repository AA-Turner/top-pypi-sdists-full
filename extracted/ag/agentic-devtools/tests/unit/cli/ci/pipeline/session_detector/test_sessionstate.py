"""Tests for SessionState."""

from dataclasses import FrozenInstanceError

import pytest

from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState


def test_session_state_is_immutable() -> None:
    state = SessionState(outcome=SessionOutcome.FAILED, failure_event_id=42, task_id=None)
    assert state.failure_event_id == 42
    with pytest.raises(FrozenInstanceError):
        state.outcome = SessionOutcome.FINISHED  # type: ignore[misc]


def test_session_state_defaults_preserve_legacy_construction() -> None:
    state = SessionState(SessionOutcome.NONE)
    assert state.inventory_availability.value == "complete"
    assert state.failure_category is None
    assert state.http_status is None
    assert state.failure_source is None
