"""Unit tests for orchestration-workflow enforcement, handoffs, and provenance propagation."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.hierarchy.scopes import (
    FileBoundary,
    make_subtask_scope,
)
from agentic_devtools.orchestration.hierarchy.workflow import (
    ReviewDecision,
)


def _subtask(paths=("a.py",)):
    return make_subtask_scope(
        agent_id="subtask-1", issue_key="3", file_boundary=FileBoundary(paths=paths), specialization=None
    )


def test_review_decision_requires_violation_and_corrective_action_for_rejection() -> None:
    with pytest.raises(ValueError):
        ReviewDecision(agent_id="feature-1", verdict="rejected")


def test_review_decision_approved_needs_no_violation_details() -> None:
    decision = ReviewDecision(agent_id="feature-1", verdict="approved")
    detail = decision.to_event_detail()
    assert detail["verdict"] == "approved"
    assert detail["context_provenance"] == "verified"


def test_review_decision_rejects_invalid_verdict() -> None:
    with pytest.raises(ValueError, match="Invalid verdict"):
        ReviewDecision(agent_id="feature-1", verdict="bogus")


def test_review_decision_rejected_with_violation_details_is_valid() -> None:
    decision = ReviewDecision(
        agent_id="feature-1", verdict="rejected", violation_ref="FR-006", corrective_action="fix it"
    )
    assert decision.violation_ref == "FR-006"
