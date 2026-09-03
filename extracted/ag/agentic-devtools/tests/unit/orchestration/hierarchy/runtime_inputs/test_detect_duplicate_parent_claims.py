"""Unit tests for provider-verified hierarchy discovery and runtime input generation."""

from __future__ import annotations

from agentic_devtools.hierarchy.models import HierarchyLevel
from agentic_devtools.orchestration.hierarchy.runtime_inputs import (
    ProviderIssueRelationship,
    detect_duplicate_parent_claims,
)


def _rel(
    key: str,
    parent: str | None = None,
    resolvable: bool = True,
    level: HierarchyLevel | None = None,
) -> ProviderIssueRelationship:
    return ProviderIssueRelationship(issue_key=key, parent_key=parent, resolvable=resolvable, level=level)


def test_duplicate_parent_claims_detected() -> None:
    records = [_rel("1", "10"), _rel("1", "20")]  # same issue key, conflicting parents
    assert detect_duplicate_parent_claims(records) == ["1"]


def test_duplicate_parent_claims_reported_once_for_repeated_conflicts() -> None:
    records = [_rel("1", "10"), _rel("1", "20"), _rel("1", "30")]
    assert detect_duplicate_parent_claims(records) == ["1"]


def test_no_duplicate_parent_claims_for_consistent_records() -> None:
    records = [_rel("1", "10"), _rel("2", "10")]
    assert detect_duplicate_parent_claims(records) == []
