"""Unit tests for orchestration-workflow enforcement, handoffs, and provenance propagation."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.orchestration.hierarchy.scopes import (
    FileBoundary,
    make_subtask_scope,
)
from agentic_devtools.orchestration.hierarchy.trace import read_events
from agentic_devtools.orchestration.hierarchy.workflow import (
    enforce_file_boundary,
)


def _subtask(paths=("a.py",)):
    return make_subtask_scope(
        agent_id="subtask-1", issue_key="3", file_boundary=FileBoundary(paths=paths), specialization=None
    )


def test_enforce_file_boundary_allows_in_boundary_write(tmp_path: Path) -> None:
    agent = _subtask(("a.py", "b.py"))
    trace_path = tmp_path / "trace.ndjson"
    result = enforce_file_boundary(agent, "a.py", trace_path=trace_path)
    assert result.allowed is True
    assert read_events(trace_path) == []


def test_enforce_file_boundary_blocks_out_of_boundary_write_and_records_violation(tmp_path: Path) -> None:
    agent = _subtask(("a.py",))
    trace_path = tmp_path / "trace.ndjson"
    result = enforce_file_boundary(agent, "unauthorized.py", trace_path=trace_path)
    assert result.allowed is False
    events = read_events(trace_path)
    assert len(events) == 1
    assert events[0]["event_type"] == "scope_violation"
    assert events[0]["event_detail"]["attempted_path"] == "unauthorized.py"
    assert events[0]["event_detail"]["enforcement"] == "blocked"
