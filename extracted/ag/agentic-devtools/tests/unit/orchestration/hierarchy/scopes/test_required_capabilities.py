"""Unit tests for canonical capability provisioning (FR-016)."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.scopes import (
    BASELINE_CAPABILITIES,
    AgentScopeLevel,
    required_capabilities,
)


def test_required_capabilities_orchestrator_scope_is_baseline_only() -> None:
    caps = required_capabilities(AgentScopeLevel.ORCHESTRATOR)
    assert set(caps) == set(BASELINE_CAPABILITIES)


def test_required_capabilities_subtask_without_specialization_includes_write_tools() -> None:
    """An unclassified subtask receives write capabilities but no language extension."""
    caps = required_capabilities(AgentScopeLevel.SUBTASK)
    assert "write_files" in caps
    assert "version_control" in caps
    assert "python_language" not in caps


def test_required_capabilities_review_scope_includes_review_tools() -> None:
    """Epic and feature scopes receive review capabilities in addition to baseline tools."""
    caps = required_capabilities(AgentScopeLevel.FEATURE)
    assert "evaluate_requirements" in caps
