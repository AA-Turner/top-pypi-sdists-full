"""Unit tests for workflow.py trace-recording helpers, completion wiring, and status messages."""

from __future__ import annotations

from pathlib import Path


def test_run_review_sequence_raises_on_mismatched_decision_agent(tmp_path: Path) -> None:
    """run_review_sequence must raise ValueError when a callback returns a decision for the wrong agent."""
    import pytest

    from agentic_devtools.orchestration.hierarchy.assignment import HierarchyAssignment
    from agentic_devtools.orchestration.hierarchy.runtime_inputs import HierarchyChain
    from agentic_devtools.orchestration.hierarchy.scopes import AgentScopeLevel, make_review_only_scope
    from agentic_devtools.orchestration.hierarchy.workflow import ReviewDecision, run_review_sequence

    feature = make_review_only_scope(
        agent_id="feature-agent",
        scope_level=AgentScopeLevel.FEATURE,
        issue_key="F-1",
    )
    assignment = HierarchyAssignment(
        outcome="success",
        chain=HierarchyChain(subtask_key="T-1", feature_key="F-1"),
        feature_agent=feature,
    )

    trace_path = tmp_path / "trace.ndjson"

    def bad_callback(reviewer):  # type: ignore[no-untyped-def]
        # Returns a decision attributed to the wrong agent.
        return ReviewDecision(agent_id="wrong-agent", verdict="approved")

    with pytest.raises(ValueError, match="does not match"):
        run_review_sequence(assignment, ["sub-1"], trace_path=trace_path, render_review=bad_callback)


def test_run_review_sequence_records_handoffs_and_reviews(tmp_path: Path) -> None:
    """Review sequence records subtask-to-feature handoffs and reviewer decisions."""
    from agentic_devtools.orchestration.hierarchy.assignment import HierarchyAssignment
    from agentic_devtools.orchestration.hierarchy.runtime_inputs import HierarchyChain
    from agentic_devtools.orchestration.hierarchy.scopes import AgentScopeLevel, make_review_only_scope
    from agentic_devtools.orchestration.hierarchy.workflow import ReviewDecision, run_review_sequence

    feature = make_review_only_scope(agent_id="feature-agent", scope_level=AgentScopeLevel.FEATURE, issue_key="F-1")
    epic = make_review_only_scope(agent_id="epic-agent", scope_level=AgentScopeLevel.EPIC, issue_key="E-1")
    assignment = HierarchyAssignment(
        outcome="success",
        chain=HierarchyChain(subtask_key="T-1", feature_key="F-1", epic_key="E-1"),
        feature_agent=feature,
        epic_agent=epic,
    )
    decisions = run_review_sequence(
        assignment,
        ["sub-1"],
        trace_path=tmp_path / "trace.ndjson",
        render_review=lambda reviewer: ReviewDecision(agent_id=reviewer.agent_id, verdict="approved"),
    )
    assert [decision.agent_id for decision in decisions] == ["feature-agent", "epic-agent"]


def test_run_review_sequence_stops_after_feature_revision_request(tmp_path: Path) -> None:
    """A non-approved feature decision must stop the sequence before epic review."""
    from agentic_devtools.orchestration.hierarchy.assignment import HierarchyAssignment
    from agentic_devtools.orchestration.hierarchy.runtime_inputs import HierarchyChain
    from agentic_devtools.orchestration.hierarchy.scopes import AgentScopeLevel, make_review_only_scope
    from agentic_devtools.orchestration.hierarchy.workflow import ReviewDecision, run_review_sequence

    feature = make_review_only_scope(agent_id="feature-agent", scope_level=AgentScopeLevel.FEATURE, issue_key="F-1")
    epic = make_review_only_scope(agent_id="epic-agent", scope_level=AgentScopeLevel.EPIC, issue_key="E-1")
    assignment = HierarchyAssignment(
        outcome="success",
        chain=HierarchyChain(subtask_key="T-1", feature_key="F-1", epic_key="E-1"),
        feature_agent=feature,
        epic_agent=epic,
    )
    decisions = run_review_sequence(
        assignment,
        ["sub-1"],
        trace_path=tmp_path / "trace.ndjson",
        render_review=lambda reviewer: (
            ReviewDecision(
                agent_id=reviewer.agent_id,
                verdict="revision_requested",
                violation_ref="FR-006",
                corrective_action="add missing feature artifacts",
            )
            if reviewer.agent_id == "feature-agent"
            else ReviewDecision(agent_id=reviewer.agent_id, verdict="approved")
        ),
    )
    assert [decision.agent_id for decision in decisions] == ["feature-agent"]
    assert decisions[0].verdict == "revision_requested"
