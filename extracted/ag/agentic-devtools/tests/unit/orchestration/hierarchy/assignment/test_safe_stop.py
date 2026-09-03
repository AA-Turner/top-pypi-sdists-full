"""Unit tests for hierarchy chain -> ScopeAgent team composition (FR-001-FR-004, FR-014, FR-015)."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.assignment import (
    AssignmentOutcome,
    safe_stop,
)
from agentic_devtools.orchestration.hierarchy.scopes import (
    FileBoundary,
    ScopeAgent,
    make_subtask_scope,
)


def _subtask(issue_key: str = "3") -> ScopeAgent:
    return make_subtask_scope(
        agent_id=f"subtask-{issue_key}-python",
        issue_key=issue_key,
        file_boundary=FileBoundary(("src/app.py",)),
        specialization=None,
    )


def test_safe_stop_spawns_no_agents() -> None:
    assignment = safe_stop("cycle_detected")
    assert assignment.outcome == AssignmentOutcome.SAFE_STOPPED
    assert assignment.epic_agent is None
    assert assignment.feature_agent is None
    assert assignment.review_order == ()
