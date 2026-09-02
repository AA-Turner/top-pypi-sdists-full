"""Tests for Jira-specific MockAdapter fixture wiring."""

from __future__ import annotations

from tests.unit.adapters.mock_adapter import MockAdapter


def test_jira_mock_adapter_type_properties_match_types(jira_mock_adapter: MockAdapter) -> None:
    """jira_mock_adapter returns properties for every configured Jira issue type."""
    for issue_type in jira_mock_adapter.get_issue_types():
        assert jira_mock_adapter.get_type_properties(issue_type["name"]) != []
