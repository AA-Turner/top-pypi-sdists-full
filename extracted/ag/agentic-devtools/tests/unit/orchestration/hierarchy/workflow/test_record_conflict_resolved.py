"""Unit tests for record_conflict_resolved."""

from pathlib import Path

from agentic_devtools.orchestration.hierarchy.conflicts import ConflictResolution
from agentic_devtools.orchestration.hierarchy.trace import read_events
from agentic_devtools.orchestration.hierarchy.workflow import record_conflict_resolved


def test_record_conflict_resolved(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.ndjson"
    resolution = ConflictResolution(
        resolution_authority="feature-1",
        contested_paths=("x.py",),
        granted_paths={"a": ("x.py",)},
        resolution_decision="grant to a",
    )
    record_conflict_resolved(trace_path, resolution)
    assert read_events(trace_path)[0]["event_type"] == "conflict_resolved"
