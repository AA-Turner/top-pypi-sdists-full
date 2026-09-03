"""Unit tests for hierarchy chain -> ScopeAgent team composition (FR-001-FR-004, FR-014, FR-015)."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.hierarchy.assignment import (
    AssignmentOutcome,
    compose_assignment,
)
from agentic_devtools.orchestration.hierarchy.runtime_inputs import HierarchyChain
from agentic_devtools.orchestration.hierarchy.scopes import (
    AgentScopeLevel,
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


def test_complete_hierarchy_composes_epic_feature() -> None:
    chain = HierarchyChain(subtask_key="3", feature_key="2", epic_key="1")
    assignment = compose_assignment(chain, subtask_agents=(_subtask("3"),))
    assert assignment.outcome == AssignmentOutcome.COMPLETE
    assert assignment.epic_agent is not None
    assert assignment.feature_agent is not None
    assert assignment.epic_agent.scope_level == AgentScopeLevel.EPIC
    assert assignment.feature_agent.scope_level == AgentScopeLevel.FEATURE
    assert assignment.degradation is None


def test_feature_only_composes_without_epic() -> None:
    chain = HierarchyChain(subtask_key="2", feature_key="1", epic_key=None)
    assignment = compose_assignment(chain, subtask_agents=(_subtask("2"),))
    assert assignment.outcome == AssignmentOutcome.FEATURE_ONLY
    assert assignment.epic_agent is None
    assert assignment.feature_agent is not None
    assert assignment.degradation is not None
    assert assignment.degradation.missing_level == "epic"


def test_epic_subtask_topology_records_absent_feature_level() -> None:
    chain = HierarchyChain(subtask_key="2", feature_key=None, epic_key="1")
    assignment = compose_assignment(chain, subtask_agents=(_subtask("2"),))
    assert assignment.outcome == AssignmentOutcome.EPIC_SUBTASK
    assert assignment.epic_agent is not None
    assert assignment.feature_agent is None
    assert assignment.degradation is not None
    assert assignment.degradation.missing_level == "feature"
    assert assignment.degradation.resulting_topology == ("epic", "subtask")


def test_standalone_preserves_single_agent_behavior() -> None:
    chain = HierarchyChain(subtask_key="1", feature_key=None, epic_key=None)
    assignment = compose_assignment(chain)
    assert assignment.outcome == AssignmentOutcome.STANDALONE
    assert assignment.epic_agent is None
    assert assignment.feature_agent is None
    assert assignment.degradation is None


def test_review_order_is_feature_before_epic() -> None:
    chain = HierarchyChain(subtask_key="3", feature_key="2", epic_key="1")
    assignment = compose_assignment(chain, subtask_agents=(_subtask("3"),))
    order = assignment.review_order
    assert [a.scope_level for a in order] == [AgentScopeLevel.FEATURE, AgentScopeLevel.EPIC]


def test_review_order_epic_only_when_feature_absent() -> None:
    chain = HierarchyChain(subtask_key="2", feature_key=None, epic_key="1")
    assignment = compose_assignment(chain, subtask_agents=(_subtask("2"),))
    order = assignment.review_order
    assert [a.scope_level for a in order] == [AgentScopeLevel.EPIC]


def test_assignment_exposes_subtask_agents_and_all_agents() -> None:
    subtask = _subtask("3")
    assignment = compose_assignment(
        HierarchyChain(subtask_key="3", feature_key="2", epic_key="1"),
        subtask_agents=(subtask,),
    )

    assert assignment.subtask_agents == (subtask,)
    assert assignment.all_agents == (assignment.epic_agent, assignment.feature_agent, subtask)


def test_requires_epic_and_requires_feature_properties() -> None:
    complete = compose_assignment(
        HierarchyChain(subtask_key="3", feature_key="2", epic_key="1"), subtask_agents=(_subtask("3"),)
    )
    assert complete.requires_epic is True
    assert complete.requires_feature is True

    standalone = compose_assignment(HierarchyChain(subtask_key="1"))
    assert standalone.requires_epic is False
    assert standalone.requires_feature is False


def test_non_standalone_assignment_requires_subtask_agents() -> None:
    with pytest.raises(ValueError, match="at least one Subtask Agent"):
        compose_assignment(HierarchyChain(subtask_key="3", feature_key="2", epic_key="1"))


def test_compose_assignment_rejects_wrong_scope_level() -> None:
    from agentic_devtools.orchestration.hierarchy.scopes import make_review_only_scope

    chain = HierarchyChain(subtask_key="3", feature_key="2", epic_key="1")
    feature_agent = make_review_only_scope(
        agent_id="feature-3",
        scope_level=AgentScopeLevel.FEATURE,
        issue_key="3",
        artifacts=(),
        can_resolve_conflicts=False,
    )
    with pytest.raises(ValueError, match="non-Subtask agent"):
        compose_assignment(chain, subtask_agents=(feature_agent,))


def test_compose_assignment_rejects_mismatched_issue_key() -> None:
    chain = HierarchyChain(subtask_key="3", feature_key="2", epic_key="1")
    wrong_agent = _subtask("99")
    with pytest.raises(ValueError, match="subtask_key is '3'"):
        compose_assignment(chain, subtask_agents=(wrong_agent,))
