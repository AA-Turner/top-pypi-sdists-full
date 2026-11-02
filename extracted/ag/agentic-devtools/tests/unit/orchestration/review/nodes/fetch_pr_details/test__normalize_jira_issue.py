"""Tests for _normalize_jira_issue helper."""

from __future__ import annotations

import os
from typing import Any
from unittest.mock import patch

from agentic_devtools.orchestration.review.nodes.fetch_pr_details import _normalize_jira_issue


class TestNormalizeJiraIssue:
    """Tests for the _normalize_jira_issue helper function."""

    def test_happy_path_with_all_fields(self) -> None:
        """All fields are extracted from a well-formed Jira issue."""
        raw = {
            "key": "PROJ-123",
            "fields": {
                "summary": "Fix the bug",
                "description": "Detailed description here",
                "status": {"name": "In Progress"},
                "issuetype": {"name": "Story"},
                "priority": {"name": "High"},
                "labels": ["backend", "urgent"],
                "customfield_10014": "User can login successfully",
            },
        }
        result = _normalize_jira_issue(raw)
        assert result == {
            "key": "PROJ-123",
            "summary": "Fix the bug",
            "description": "Detailed description here",
            "status": "In Progress",
            "issue_type": "Story",
            "labels": ["backend", "urgent"],
            "acceptance_criteria": "User can login successfully",
            "priority": "High",
        }

    def test_missing_fields_key(self) -> None:
        """Missing 'fields' key produces safe defaults."""
        raw = {"key": "PROJ-456"}
        result = _normalize_jira_issue(raw)
        assert result["key"] == "PROJ-456"
        assert result["summary"] == ""
        assert result["description"] is None
        assert result["status"] is None
        assert result["issue_type"] is None
        assert result["labels"] == []
        assert result["acceptance_criteria"] is None
        assert result["priority"] is None

    def test_none_status_issuetype_priority(self) -> None:
        """None values for nested dicts produce None outputs."""
        raw = {
            "key": "PROJ-789",
            "fields": {
                "status": None,
                "issuetype": None,
                "priority": None,
            },
        }
        result = _normalize_jira_issue(raw)
        assert result["status"] is None
        assert result["issue_type"] is None
        assert result["priority"] is None

    def test_empty_labels(self) -> None:
        """Empty labels list is preserved."""
        raw = {"key": "PROJ-1", "fields": {"labels": []}}
        result = _normalize_jira_issue(raw)
        assert result["labels"] == []

    def test_non_list_labels(self) -> None:
        """Non-list labels value defaults to empty list."""
        raw = {"key": "PROJ-1", "fields": {"labels": "not-a-list"}}
        result = _normalize_jira_issue(raw)
        assert result["labels"] == []

    def test_acceptance_criteria_from_env_var(self) -> None:
        """Custom acceptance criteria field name from environment."""
        raw = {
            "key": "PROJ-1",
            "fields": {
                "customfield_99999": "Custom AC value",
            },
        }
        with patch.dict(os.environ, {"JIRA_ACCEPTANCE_CRITERIA_FIELD": "customfield_99999"}):
            result = _normalize_jira_issue(raw)
        assert result["acceptance_criteria"] == "Custom AC value"

    def test_acceptance_criteria_defaults_to_customfield_10014(self) -> None:
        """Default acceptance criteria field is customfield_10014."""
        raw = {
            "key": "PROJ-1",
            "fields": {
                "customfield_10014": "Default AC value",
            },
        }
        with patch.dict(os.environ, {}, clear=False):
            # Ensure env var is not set
            os.environ.pop("JIRA_ACCEPTANCE_CRITERIA_FIELD", None)
            result = _normalize_jira_issue(raw)
        assert result["acceptance_criteria"] == "Default AC value"

    def test_acceptance_criteria_none_when_field_missing(self) -> None:
        """Acceptance criteria is None when custom field is absent."""
        raw = {"key": "PROJ-1", "fields": {}}
        result = _normalize_jira_issue(raw)
        assert result["acceptance_criteria"] is None

    def test_acceptance_criteria_none_when_value_is_empty_string(self) -> None:
        """Empty string acceptance criteria is treated as None."""
        raw = {"key": "PROJ-1", "fields": {"customfield_10014": ""}}
        result = _normalize_jira_issue(raw)
        assert result["acceptance_criteria"] is None

    def test_blank_env_var_falls_back_to_default_ac_field(self) -> None:
        """A blank/whitespace JIRA_ACCEPTANCE_CRITERIA_FIELD env-var is ignored."""
        raw = {
            "key": "PROJ-1",
            "fields": {
                "customfield_10014": "AC from default field",
            },
        }
        with patch.dict(os.environ, {"JIRA_ACCEPTANCE_CRITERIA_FIELD": "   "}):
            result = _normalize_jira_issue(raw)
        assert result["acceptance_criteria"] == "AC from default field"

    def test_none_key_normalizes_to_empty_string(self) -> None:
        """A None 'key' value in the raw issue dict is normalized to empty string."""
        raw: dict[str, Any] = {"key": None, "fields": {}}
        result = _normalize_jira_issue(raw)
        assert result["key"] == ""

    def test_none_summary_normalizes_to_empty_string(self) -> None:
        """A None 'summary' value in the fields dict is normalized to empty string."""
        raw: dict[str, Any] = {"key": "PROJ-1", "fields": {"summary": None}}
        result = _normalize_jira_issue(raw)
        assert result["summary"] == ""

    def test_non_string_label_entries_are_dropped(self) -> None:
        """Non-string entries in the labels list are filtered out."""
        raw: dict[str, Any] = {
            "key": "PROJ-1",
            "fields": {"labels": ["backend", 123, None, "urgent", {"x": 1}]},
        }
        result = _normalize_jira_issue(raw)
        assert result["labels"] == ["backend", "urgent"]

    def test_acceptance_criteria_none_when_whitespace_only(self) -> None:
        """Whitespace-only acceptance criteria is treated as None."""
        raw: dict[str, Any] = {"key": "PROJ-1", "fields": {"customfield_10014": "   \n\t"}}
        result = _normalize_jira_issue(raw)
        assert result["acceptance_criteria"] is None

    def test_acceptance_criteria_none_when_non_string(self) -> None:
        """A non-string acceptance criteria value (e.g. ADF dict) is normalized to None."""
        raw: dict[str, Any] = {
            "key": "PROJ-1",
            "fields": {"customfield_10014": {"type": "doc", "content": []}},
        }
        result = _normalize_jira_issue(raw)
        assert result["acceptance_criteria"] is None

    def test_acceptance_criteria_is_stripped(self) -> None:
        """Surrounding whitespace on acceptance criteria is stripped."""
        raw: dict[str, Any] = {"key": "PROJ-1", "fields": {"customfield_10014": "  Login works  "}}
        result = _normalize_jira_issue(raw)
        assert result["acceptance_criteria"] == "Login works"

    def test_non_string_description_normalizes_to_none(self) -> None:
        """A non-string 'description' (e.g. ADF dict) is normalized to None."""
        raw: dict[str, Any] = {
            "key": "PROJ-1",
            "fields": {
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [],
                }
            },
        }
        result = _normalize_jira_issue(raw)
        assert result["description"] is None
