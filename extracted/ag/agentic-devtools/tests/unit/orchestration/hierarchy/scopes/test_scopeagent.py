"""Unit tests for ScopeAgent, FileBoundary immutability and enforcement (FR-010)."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.hierarchy.scopes import (
    AgentScopeLevel,
    FileBoundary,
    ScopeAgent,
    make_subtask_scope,
)


def test_scope_agent_is_frozen() -> None:
    agent = make_subtask_scope(
        agent_id="subtask-1",
        issue_key="1",
        file_boundary=FileBoundary(),
        specialization=None,
    )
    with pytest.raises(Exception):  # noqa: B017 - frozen dataclass raises FrozenInstanceError
        agent.agent_id = "other"  # type: ignore[misc]


def test_scope_agent_rejects_invalid_discovery_scope_combinations() -> None:
    """Discovery-only subtasks cannot carry boundaries or specializations."""
    from agentic_devtools.orchestration.hierarchy.scopes import SpecializationCategory

    with pytest.raises(ValueError, match="Review-only"):
        ScopeAgent("epic", AgentScopeLevel.EPIC, "1", discovery_only=True)
    with pytest.raises(ValueError, match="must not declare a file boundary"):
        ScopeAgent("epic", AgentScopeLevel.EPIC, "1", file_boundary=FileBoundary(("x.py",)))
    with pytest.raises(ValueError, match="ORCHESTRATOR"):
        ScopeAgent("orch", AgentScopeLevel.ORCHESTRATOR, "1")
    with pytest.raises(ValueError, match="empty file boundary"):
        ScopeAgent("sub", AgentScopeLevel.SUBTASK, "1", file_boundary=FileBoundary(("x.py",)), discovery_only=True)
    with pytest.raises(ValueError, match="must not declare a specialization"):
        ScopeAgent(
            "sub",
            AgentScopeLevel.SUBTASK,
            "1",
            specialization=SpecializationCategory.PYTHON,
            discovery_only=True,
        )


def test_scope_agent_serializes_artifacts_and_specialization() -> None:
    """Scope serialization includes artifact, authority, specialization, and sibling details."""
    from agentic_devtools.orchestration.hierarchy.scopes import ArtifactReference, SpecializationCategory

    agent = ScopeAgent(
        "sub",
        AgentScopeLevel.SUBTASK,
        "1",
        artifacts=(ArtifactReference("spec.md", "1"),),
        file_boundary=FileBoundary(("x.py",)),
        specialization=SpecializationCategory.PYTHON,
        capabilities=("write_files",),
        sibling_ids=("other",),
    )
    payload = agent.to_dict()
    assert payload["artifacts"] == [{"path": "spec.md", "issue_key": "1", "available": True}]
    assert payload["specialization"] == "python"
