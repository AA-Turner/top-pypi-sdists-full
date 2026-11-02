"""Unit tests for workflow.py trace-recording helpers, completion wiring, and status messages."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.orchestration.hierarchy.retry import (
    AgentFailureEvent,
    AttemptOutcome,
    FailurePhase,
)
from agentic_devtools.orchestration.hierarchy.trace import read_events
from agentic_devtools.orchestration.hierarchy.workflow import (
    record_agent_failure,
)


def test_record_agent_failure_writes_event(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.ndjson"
    failure = AgentFailureEvent(
        agent_id="subtask-1",
        failure_reason="boom",
        retry_attempt=0,
        failure_phase=FailurePhase.INITIAL,
        attempt_outcome=AttemptOutcome.FAILED,
        recovery_mode=None,
        recovered=False,
        terminal_cleanup=None,
        disposition="retry_pending",
    )
    record_agent_failure(trace_path, "subtask", failure)
    events = read_events(trace_path)
    assert events[0]["event_type"] == "agent_failure"
    assert events[0]["event_detail"]["failure_reason"] == "boom"
