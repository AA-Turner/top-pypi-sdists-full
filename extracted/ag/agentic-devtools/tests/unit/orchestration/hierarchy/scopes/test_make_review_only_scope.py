"""Unit tests for ScopeAgent, FileBoundary immutability and enforcement (FR-010)."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.hierarchy.scopes import (
    AgentScopeLevel,
    make_review_only_scope,
)


def test_make_review_only_scope_rejects_subtask_level() -> None:
    with pytest.raises(ValueError, match="requires EPIC or FEATURE"):
        make_review_only_scope(agent_id="x", scope_level=AgentScopeLevel.SUBTASK, issue_key="1")


def test_make_review_only_scope_constructs_feature() -> None:
    """A feature review scope has review authority and no writable boundary."""
    agent = make_review_only_scope(agent_id="feature", scope_level=AgentScopeLevel.FEATURE, issue_key="1")
    assert agent.review_authority.can_review
    assert agent.file_boundary.is_empty
