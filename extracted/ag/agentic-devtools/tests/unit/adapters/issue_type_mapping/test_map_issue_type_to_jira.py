"""Tests for map_issue_type_to_jira (FR-001, FR-004, FR-005, FR-009)."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.issue_provider import IssueTypeMappingError
from agentic_devtools.adapters.issue_type_mapping import (
    JIRA_DEFAULT_TYPE_NAMES,
    map_issue_type_to_jira,
)


class TestMapIssueTypeToJira:
    @pytest.mark.parametrize("issue_type", ["epic", "feature", "subtask", "task", "bug"])
    def test_all_types_with_defaults(self, issue_type: str) -> None:
        result = map_issue_type_to_jira(issue_type)
        assert result.type_name == JIRA_DEFAULT_TYPE_NAMES[issue_type]

    def test_subtask_with_epic_parent_routes_to_parent(self) -> None:
        result = map_issue_type_to_jira("subtask", parent_issue_type="epic")
        assert result.route == "parent"

    def test_feature_with_epic_parent_routes_to_epic_link(self) -> None:
        result = map_issue_type_to_jira("feature", parent_issue_type="epic")
        assert result.route == "epic-link"

    def test_task_with_task_parent_routes_to_none(self) -> None:
        result = map_issue_type_to_jira("task", parent_issue_type="task")
        assert result.route is None

    def test_subtask_with_no_parent_routes_to_none(self) -> None:
        result = map_issue_type_to_jira("subtask", parent_issue_type=None)
        assert result.route is None

    def test_epic_with_any_parent_routes_to_none(self) -> None:
        result = map_issue_type_to_jira("epic", parent_issue_type="epic")
        assert result.route is None

    def test_bug_with_epic_parent_routes_to_epic_link(self) -> None:
        result = map_issue_type_to_jira("bug", parent_issue_type="epic")
        assert result.route == "epic-link"

    def test_feature_with_no_parent_routes_to_none(self) -> None:
        result = map_issue_type_to_jira("feature", parent_issue_type=None)
        assert result.route is None

    def test_labels_normalization(self) -> None:
        result = map_issue_type_to_jira("task", declared_labels=["  backend  ", "", "frontend"])
        assert result.labels == ["backend", "frontend"]

    def test_invalid_type_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Unsupported issue_type"):
            map_issue_type_to_jira("story")

    def test_missing_mapping_raises_mapping_error(self) -> None:
        with pytest.raises(IssueTypeMappingError, match="Cannot resolve"):
            map_issue_type_to_jira("epic", type_mapping={"bug": "Bug"})

    def test_custom_mapping(self) -> None:
        custom = {"epic": "Epic", "feature": "Feature", "subtask": "CustomSub", "task": "Task", "bug": "Bug"}
        result = map_issue_type_to_jira("subtask", type_mapping=custom)
        assert result.type_name == "CustomSub"

    def test_task_with_feature_parent_routes_to_none(self) -> None:
        result = map_issue_type_to_jira("task", parent_issue_type="feature")
        assert result.route is None

    def test_whitespace_parent_type_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="parent_issue_type must be None or a non-empty string"):
            map_issue_type_to_jira("subtask", parent_issue_type="   ")

    def test_unsupported_parent_type_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="unsupported parent_issue_type"):
            map_issue_type_to_jira("subtask", parent_issue_type="story")
