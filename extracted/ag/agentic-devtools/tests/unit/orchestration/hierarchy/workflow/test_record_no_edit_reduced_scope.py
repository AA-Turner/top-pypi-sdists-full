"""Unit tests for workflow.py trace-recording helpers, completion wiring, and status messages."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.orchestration.hierarchy.trace import read_events
from agentic_devtools.orchestration.hierarchy.workflow import (
    record_no_edit_reduced_scope,
)


def test_record_no_edit_reduced_scope_writes_degradation(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.ndjson"
    record_no_edit_reduced_scope(trace_path, agent_id="subtask-1")
    events = read_events(trace_path)
    assert events[0]["event_detail"]["reason"] == "no_candidate_file_list_established"
    assert events[0]["event_detail"]["agent_id"] == "subtask-1"
