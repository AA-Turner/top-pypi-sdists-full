"""Tests for JIRA_DEFAULT_TYPE_NAMES constant (SC-001)."""

from __future__ import annotations

from agentic_devtools.adapters.issue_provider import VALID_ISSUE_TYPES
from agentic_devtools.adapters.issue_type_mapping import JIRA_DEFAULT_TYPE_NAMES


class TestJiraDefaultTypeNames:
    def test_covers_all_valid_issue_types(self) -> None:
        assert set(JIRA_DEFAULT_TYPE_NAMES.keys()) == VALID_ISSUE_TYPES

    def test_exact_values(self) -> None:
        assert JIRA_DEFAULT_TYPE_NAMES["epic"] == "Epic"
        assert JIRA_DEFAULT_TYPE_NAMES["feature"] == "Story"
        assert JIRA_DEFAULT_TYPE_NAMES["subtask"] == "Sub-task"
        assert JIRA_DEFAULT_TYPE_NAMES["task"] == "Task"
        assert JIRA_DEFAULT_TYPE_NAMES["bug"] == "Bug"

    def test_has_five_entries(self) -> None:
        assert len(JIRA_DEFAULT_TYPE_NAMES) == 5
