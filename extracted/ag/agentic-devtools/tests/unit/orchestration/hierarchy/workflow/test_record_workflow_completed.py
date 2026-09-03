"""Unit tests for orchestration-workflow enforcement, handoffs, and provenance propagation."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.orchestration.hierarchy.scopes import (
    FileBoundary,
    make_subtask_scope,
)
from agentic_devtools.orchestration.hierarchy.trace import read_events
from agentic_devtools.orchestration.hierarchy.workflow import (
    WorkflowCompletion,
    record_workflow_completed,
)


def _subtask(paths=("a.py",)):
    return make_subtask_scope(
        agent_id="subtask-1", issue_key="3", file_boundary=FileBoundary(paths=paths), specialization=None
    )


def test_record_workflow_completed_writes_terminal_event(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.ndjson"
    completion = WorkflowCompletion(
        outcome="success",
        agents_completed=("epic-1", "feature-1", "subtask-1"),
        agents_skipped=(),
        final_disposition="success",
    )
    record_workflow_completed(trace_path, completion)
    events = read_events(trace_path)
    assert events[0]["event_type"] == "workflow_completed"
    assert events[0]["event_detail"]["outcome"] == "success"
