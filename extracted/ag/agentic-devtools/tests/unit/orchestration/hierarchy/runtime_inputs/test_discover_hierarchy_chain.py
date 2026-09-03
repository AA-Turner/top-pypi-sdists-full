"""Unit tests for provider-verified hierarchy discovery and runtime input generation."""

from __future__ import annotations

from typing import cast

import pytest

from agentic_devtools.hierarchy.models import HierarchyLevel
from agentic_devtools.orchestration.hierarchy.runtime_inputs import (
    HierarchyDiscoveryError,
    ProviderIssueRelationship,
    discover_hierarchy_chain,
)


def _rel(
    key: str,
    parent: str | None = None,
    resolvable: bool = True,
    level: HierarchyLevel | None = None,
) -> ProviderIssueRelationship:
    return ProviderIssueRelationship(issue_key=key, parent_key=parent, resolvable=resolvable, level=level)


def test_full_epic_feature_subtask_chain() -> None:
    relationships = {"3": _rel("3", "2"), "2": _rel("2", "1"), "1": _rel("1", None)}
    chain = discover_hierarchy_chain("3", relationships)
    assert chain.subtask_key == "3"
    assert chain.feature_key == "2"
    assert chain.epic_key == "1"
    assert chain.levels_found == ["subtask", "feature", "epic"]


def test_feature_only_chain() -> None:
    relationships = {"2": _rel("2", "1"), "1": _rel("1", None)}
    chain = discover_hierarchy_chain("2", relationships)
    assert chain.feature_key == "1"
    assert chain.epic_key is None
    assert chain.levels_found == ["subtask", "feature"]


def test_direct_epic_parent_is_identified_from_provider_level() -> None:
    relationships = {
        "2": _rel("2", "1", level=HierarchyLevel.TASK),
        "1": _rel("1", None, level=HierarchyLevel.EPIC),
    }

    chain = discover_hierarchy_chain("2", relationships)

    assert chain.feature_key is None
    assert chain.epic_key == "1"
    assert chain.levels_found == ["subtask", "epic"]


@pytest.mark.parametrize(
    ("relationships", "message"),
    [
        (
            {
                "3": _rel("3", "2", level=HierarchyLevel.FEATURE),
                "2": _rel("2", "1", level=HierarchyLevel.FEATURE),
                "1": _rel("1", None, level=HierarchyLevel.EPIC),
            },
            "Issue '3' declares level 'feature'; expected 'task'",
        ),
        (
            {
                "3": _rel("3", "2", level=HierarchyLevel.TASK),
                "2": _rel("2", "1", level=HierarchyLevel.EPIC),
                "1": _rel("1", None, level=HierarchyLevel.FEATURE),
            },
            "Issue '2' declares level 'epic'; expected 'feature'",
        ),
    ],
)
def test_rejects_inconsistent_declared_levels(
    relationships: dict[str, ProviderIssueRelationship], message: str
) -> None:
    with pytest.raises(HierarchyDiscoveryError, match=message):
        discover_hierarchy_chain("3" if "3" in relationships else "2", relationships)


def test_standalone_chain() -> None:
    relationships = {"1": _rel("1", None)}
    chain = discover_hierarchy_chain("1", relationships)
    assert chain.is_standalone


def test_max_depth_zero_raises_value_error() -> None:
    relationships = {"2": _rel("2", "1"), "1": _rel("1", None)}
    with pytest.raises(ValueError, match="max_depth must be a positive integer"):
        discover_hierarchy_chain("2", relationships, max_depth=0)


@pytest.mark.parametrize("invalid_max_depth", ["2", 1.5, None, True])
def test_max_depth_requires_integer_type(invalid_max_depth: object) -> None:
    relationships = {"2": _rel("2", "1"), "1": _rel("1", None)}
    with pytest.raises(ValueError, match="max_depth must be a positive integer"):
        discover_hierarchy_chain("2", relationships, max_depth=cast(int, invalid_max_depth))
