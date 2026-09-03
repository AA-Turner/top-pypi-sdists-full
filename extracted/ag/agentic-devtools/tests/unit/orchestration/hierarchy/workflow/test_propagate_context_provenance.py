"""Unit tests for orchestration-workflow enforcement, handoffs, and provenance propagation."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.context import (
    ContextInjectionRecord,
    ContextProvenance,
    InjectedField,
)
from agentic_devtools.orchestration.hierarchy.scopes import (
    FileBoundary,
    make_subtask_scope,
)
from agentic_devtools.orchestration.hierarchy.workflow import (
    ReviewDecision,
    propagate_context_provenance,
)


def _subtask(paths=("a.py",)):
    return make_subtask_scope(
        agent_id="subtask-1", issue_key="3", file_boundary=FileBoundary(paths=paths), specialization=None
    )


def test_propagate_context_provenance_preserves_unavailable_status() -> None:
    record = ContextInjectionRecord(
        agent_id="feature-1",
        fields=(
            InjectedField(
                name="plan_md",
                content="",
                provenance=ContextProvenance.UNAVAILABLE,
                snapshot_ref="unavailable:no-content-retained",
            ),
        ),
    )
    decision = ReviewDecision(agent_id="feature-1", verdict="approved")
    propagated = propagate_context_provenance([record], decision)
    assert propagated.provenance == ContextProvenance.UNAVAILABLE


def test_propagate_context_provenance_stays_verified_when_all_verified() -> None:
    record = ContextInjectionRecord(
        agent_id="feature-1",
        fields=(
            InjectedField(
                name="spec_md",
                content="hello",
                provenance=ContextProvenance.VERIFIED,
                locator=None,
                snapshot_ref="sha256:2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
            ),
        ),
    )
    decision = ReviewDecision(agent_id="feature-1", verdict="approved")
    propagated = propagate_context_provenance([record], decision)
    assert propagated.provenance == ContextProvenance.VERIFIED


def test_propagate_context_provenance_ignores_records_for_other_agents() -> None:
    target = ContextInjectionRecord(
        agent_id="feature-1",
        fields=(
            InjectedField(
                name="spec_md",
                content="ok",
                provenance=ContextProvenance.VERIFIED,
                snapshot_ref="sha256:2689367b205c16ce32ed4200942b8b8b1e262dfc70d9bc9fbc77c49699a4f1df",
            ),
        ),
    )
    other = ContextInjectionRecord(
        agent_id="epic-1",
        fields=(
            InjectedField(
                name="plan_md",
                content="",
                provenance=ContextProvenance.UNAVAILABLE,
                snapshot_ref="unavailable:no-content-retained",
            ),
        ),
    )
    decision = ReviewDecision(agent_id="feature-1", verdict="approved")
    propagated = propagate_context_provenance([target, other], decision)
    assert propagated.provenance == ContextProvenance.VERIFIED
