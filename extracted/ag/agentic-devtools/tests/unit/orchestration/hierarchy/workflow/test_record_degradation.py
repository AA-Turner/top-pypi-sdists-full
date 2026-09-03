"""Unit tests for the record_degradation helper (workflow.py)."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.orchestration.hierarchy.trace import read_events
from agentic_devtools.orchestration.hierarchy.workflow import (
    record_degradation,
)


def test_record_degradation_writes_event(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.ndjson"
    record_degradation(
        trace_path, reason="epic_not_found", missing_level="epic", resulting_topology=("feature", "subtask")
    )
    events = read_events(trace_path)
    assert events[0]["event_type"] == "degradation"
    assert events[0]["event_detail"]["missing_level"] == "epic"
