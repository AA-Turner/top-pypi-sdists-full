"""Unit tests for the FR-017 exactly-one-lifetime-retry policy."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.retry import (
    FailurePhase,
    RetryState,
)


def test_initial_failure_is_retry_pending() -> None:
    state = RetryState(agent_id="subtask-1")
    event = state.initial_failure("boom")
    assert event.retry_attempt == 0
    assert event.failure_phase == FailurePhase.INITIAL
    assert event.recovered is False
    assert event.disposition == "retry_pending"
    assert not state.retry_used
