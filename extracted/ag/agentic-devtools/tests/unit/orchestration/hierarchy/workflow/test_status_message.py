"""Unit tests for orchestration-workflow enforcement, handoffs, and provenance propagation."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.scopes import (
    FileBoundary,
    make_subtask_scope,
)
from agentic_devtools.orchestration.hierarchy.workflow import (
    status_message,
)


def _subtask(paths=("a.py",)):
    return make_subtask_scope(
        agent_id="subtask-1", issue_key="3", file_boundary=FileBoundary(paths=paths), specialization=None
    )


def test_status_message_identifies_scope_stage_and_reason() -> None:
    message = status_message(scope="feature", stage="review", reason="requirement FR-006 violated")
    assert "feature" in message
    assert "review" in message
    assert "FR-006" in message
