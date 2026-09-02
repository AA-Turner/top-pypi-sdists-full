"""Determinism tests — 1000 consecutive invocations produce identical output (SC-005)."""

from __future__ import annotations

from agentic_devtools.adapters.issue_type_mapping import (
    map_issue_type_to_github_labels,
    map_issue_type_to_jira,
)


class TestDeterminism:
    def test_github_mapping_deterministic(self) -> None:
        labels = ["docs", "backend", "Epic"]
        first = map_issue_type_to_github_labels("epic", declared_labels=labels)
        for _ in range(999):
            result = map_issue_type_to_github_labels("epic", declared_labels=labels)
            assert result == first

    def test_jira_mapping_deterministic(self) -> None:
        labels = ["backend", "frontend"]
        first = map_issue_type_to_jira("subtask", parent_issue_type="epic", declared_labels=labels)
        for _ in range(999):
            result = map_issue_type_to_jira("subtask", parent_issue_type="epic", declared_labels=labels)
            assert result == first
