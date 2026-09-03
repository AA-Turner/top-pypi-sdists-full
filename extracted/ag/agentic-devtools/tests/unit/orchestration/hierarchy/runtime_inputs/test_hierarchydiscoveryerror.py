"""Unit tests for provider-verified hierarchy discovery and runtime input generation."""

from __future__ import annotations

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


def test_duplicate_parent_claim_on_ancestor_fails_discovery() -> None:
    relationships = {
        "3": _rel("3", "2"),
        "2": _rel("2", "1"),
        "2-duplicate": _rel("2", "9"),
        "1": _rel("1", None),
        "9": _rel("9", None),
    }
    with pytest.raises(HierarchyDiscoveryError, match="Conflicting parent claims"):
        discover_hierarchy_chain("3", relationships)


def test_duplicate_parent_claim_on_terminal_ancestor_fails_discovery() -> None:
    relationships = {
        "2": _rel("2", "1"),
        "1": _rel("1", None),
        "1-duplicate": _rel("1", "9"),
        "9": _rel("9", None),
    }
    with pytest.raises(HierarchyDiscoveryError, match="Conflicting parent claims"):
        discover_hierarchy_chain("2", relationships)


def test_unresolved_subtask_raises() -> None:
    with pytest.raises(HierarchyDiscoveryError) as exc_info:
        discover_hierarchy_chain("missing", {})
    assert exc_info.value.reason == "unresolved_issue"


def test_unresolved_parent_raises() -> None:
    relationships = {"2": _rel("2", "1")}  # parent "1" absent
    with pytest.raises(HierarchyDiscoveryError) as exc_info:
        discover_hierarchy_chain("2", relationships)
    assert exc_info.value.reason == "unresolved_issue"


def test_cycle_detection_raises() -> None:
    relationships = {"1": _rel("1", "2"), "2": _rel("2", "1")}
    with pytest.raises(HierarchyDiscoveryError) as exc_info:
        discover_hierarchy_chain("1", relationships)
    assert exc_info.value.reason == "cycle_detected"


def test_unresolvable_subtask_flag_raises() -> None:
    relationships = {"1": _rel("1", None, resolvable=False)}
    with pytest.raises(HierarchyDiscoveryError) as exc_info:
        discover_hierarchy_chain("1", relationships)
    assert exc_info.value.reason == "unresolved_issue"


def test_ancestor_chain_exceeding_max_depth_raises_cycle_detected() -> None:
    # A valid chain with depth 2 and max_depth=1 exceeds the bound — the error
    # is cycle_detected (not ValueError, which is reserved for invalid max_depth).
    relationships = {"3": _rel("3", "2"), "2": _rel("2", "1"), "1": _rel("1", None)}
    with pytest.raises(HierarchyDiscoveryError) as exc_info:
        discover_hierarchy_chain("3", relationships, max_depth=1)
    assert exc_info.value.reason == "cycle_detected"
    assert "max_depth" in str(exc_info.value)


def test_ambiguous_depth_raises() -> None:
    relationships = {"4": _rel("4", "3"), "3": _rel("3", "2"), "2": _rel("2", "1"), "1": _rel("1", None)}
    with pytest.raises(HierarchyDiscoveryError) as exc_info:
        discover_hierarchy_chain("4", relationships)
    assert exc_info.value.reason == "ambiguous_depth"
