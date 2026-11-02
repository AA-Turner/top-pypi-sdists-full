"""Unit tests for workflow.py trace-recording helpers, completion wiring, and status messages."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.orchestration.hierarchy.conflicts import ConflictDetection
from agentic_devtools.orchestration.hierarchy.trace import read_events
from agentic_devtools.orchestration.hierarchy.workflow import record_conflict_detected


def test_record_conflict_detected(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.ndjson"
    detection = ConflictDetection(
        conflicting_agent_ids=("a", "b"), contested_paths=("x.py",), proposed_edit_summaries={}
    )
    record_conflict_detected(trace_path, detection)
    events = read_events(trace_path)
    assert events[0]["event_type"] == "conflict_detected"
