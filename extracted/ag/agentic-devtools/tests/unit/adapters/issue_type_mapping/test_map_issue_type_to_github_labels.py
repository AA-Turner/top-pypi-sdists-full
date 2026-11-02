"""Tests for map_issue_type_to_github_labels (FR-001, FR-003, FR-005, FR-009)."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_provider import IssueTypeMappingError
from agentic_devtools.adapters.issue_type_mapping import (
    GITHUB_DEFAULT_LABELS,
    map_issue_type_to_github_labels,
)


class TestMapIssueTypeToGitHubLabels:
    @pytest.mark.parametrize("issue_type", ["epic", "feature", "subtask", "task", "bug"])
    def test_all_types_with_defaults(self, issue_type: str) -> None:
        result = map_issue_type_to_github_labels(issue_type)
        assert result.merged_labels == [GITHUB_DEFAULT_LABELS[issue_type]]

    def test_custom_mapping_override(self) -> None:
        custom = {"epic": "EPIC-LABEL", "feature": "Feature", "subtask": "Subtask", "task": "Task", "bug": "Bug"}
        result = map_issue_type_to_github_labels("epic", type_mapping=custom)
        assert result.merged_labels == ["EPIC-LABEL"]

    def test_labels_merge_with_dedup(self) -> None:
        result = map_issue_type_to_github_labels("epic", declared_labels=["Epic", "docs"])
        assert result.merged_labels == ["epic", "docs"]

    def test_invalid_type_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Unsupported issue_type"):
            map_issue_type_to_github_labels("story")

    def test_missing_mapping_raises_mapping_error(self) -> None:
        with pytest.raises(IssueTypeMappingError, match="Cannot resolve"):
            map_issue_type_to_github_labels("epic", type_mapping={"bug": "Bug"})

    def test_declared_labels_preserved(self) -> None:
        result = map_issue_type_to_github_labels("subtask", declared_labels=["documentation"])
        assert result.merged_labels == ["Subtask", "documentation"]
