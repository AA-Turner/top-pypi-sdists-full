"""Unit tests for AgentFailureEvent."""

from agentic_devtools.orchestration.hierarchy.retry import RetryState


def test_agent_failure_event_to_event_detail_shape() -> None:
    state = RetryState(agent_id="subtask-1")
    detail = state.initial_failure("boom").to_event_detail()
    assert detail["agent_id"] == "subtask-1"
    assert detail["failure_reason"] == "boom"
    assert detail["retry_attempt"] == 0
    assert detail["failure_phase"] == "initial"
    assert detail["attempt_outcome"] == "failed"
    assert detail["recovery_mode"] is None
    assert detail["recovered"] is False
    assert detail["terminal_cleanup"] is None
    assert detail["disposition"] == "retry_pending"
