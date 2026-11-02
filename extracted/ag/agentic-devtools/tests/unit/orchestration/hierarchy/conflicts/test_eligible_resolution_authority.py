"""Unit tests for FR-018 conflict detection and resolution."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.conflicts import (
    eligible_resolution_authority,
)
from agentic_devtools.orchestration.hierarchy.scopes import (
    AgentScopeLevel,
    FileBoundary,
    make_review_only_scope,
    make_subtask_scope,
)


def _subtask(agent_id: str, paths: tuple[str, ...]):
    return make_subtask_scope(
        agent_id=agent_id, issue_key="1", file_boundary=FileBoundary(paths=paths), specialization=None
    )


def test_eligible_resolution_authority_prefers_feature() -> None:
    feature = make_review_only_scope(
        agent_id="feature-1", scope_level=AgentScopeLevel.FEATURE, issue_key="1", can_resolve_conflicts=True
    )
    epic = make_review_only_scope(
        agent_id="epic-1", scope_level=AgentScopeLevel.EPIC, issue_key="1", can_resolve_conflicts=True
    )
    authority = eligible_resolution_authority(
        feature_agent=feature, feature_failed=False, epic_agent=epic, epic_review_independent=True
    )
    assert authority is feature


def test_eligible_resolution_authority_falls_back_to_independent_epic() -> None:
    epic = make_review_only_scope(
        agent_id="epic-1", scope_level=AgentScopeLevel.EPIC, issue_key="1", can_resolve_conflicts=True
    )
    authority = eligible_resolution_authority(
        feature_agent=None, feature_failed=False, epic_agent=epic, epic_review_independent=True
    )
    assert authority is epic


def test_eligible_resolution_authority_skips_feature_without_conflict_authority() -> None:
    feature = make_review_only_scope(
        agent_id="feature-1",
        scope_level=AgentScopeLevel.FEATURE,
        issue_key="1",
        can_resolve_conflicts=False,
    )
    epic = make_review_only_scope(
        agent_id="epic-1",
        scope_level=AgentScopeLevel.EPIC,
        issue_key="1",
        can_resolve_conflicts=True,
    )
    authority = eligible_resolution_authority(
        feature_agent=feature,
        feature_failed=False,
        epic_agent=epic,
        epic_review_independent=True,
    )
    assert authority is epic


def test_eligible_resolution_authority_none_when_neither_eligible() -> None:
    authority = eligible_resolution_authority(
        feature_agent=None, feature_failed=False, epic_agent=None, epic_review_independent=False
    )
    assert authority is None
