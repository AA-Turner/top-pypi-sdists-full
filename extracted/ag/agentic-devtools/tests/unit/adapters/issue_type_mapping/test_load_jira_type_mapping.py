"""Tests for load_jira_type_mapping config loader (FR-002)."""

from __future__ import annotations

from agentic_devtools.adapters.issue_type_mapping import (
    JIRA_DEFAULT_TYPE_NAMES,
    load_jira_type_mapping,
)


class TestLoadJiraTypeMapping:
    def test_empty_config_returns_defaults(self) -> None:
        result = load_jira_type_mapping({})
        assert result == JIRA_DEFAULT_TYPE_NAMES

    def test_partial_override_merges_over_defaults(self) -> None:
        config = {"jira": {"issue_type_names": {"subtask": "Unteraufgabe"}}}
        result = load_jira_type_mapping(config)
        assert result["subtask"] == "Unteraufgabe"
        assert result["epic"] == JIRA_DEFAULT_TYPE_NAMES["epic"]

    def test_override_values_are_trimmed(self) -> None:
        config = {"jira": {"issue_type_names": {"feature": "  Story  "}}}
        result = load_jira_type_mapping(config)
        assert result["feature"] == "Story"

    def test_full_override(self) -> None:
        overrides = {k: f"Custom-{k}" for k in JIRA_DEFAULT_TYPE_NAMES}
        config = {"jira": {"issue_type_names": overrides}}
        result = load_jira_type_mapping(config)
        for key in JIRA_DEFAULT_TYPE_NAMES:
            assert result[key] == f"Custom-{key}"

    def test_absent_jira_section_uses_defaults(self) -> None:
        result = load_jira_type_mapping({"github": {}})
        assert result == JIRA_DEFAULT_TYPE_NAMES

    def test_absent_issue_type_names_uses_defaults(self) -> None:
        result = load_jira_type_mapping({"jira": {}})
        assert result == JIRA_DEFAULT_TYPE_NAMES

    def test_non_dict_jira_section_uses_defaults(self) -> None:
        result = load_jira_type_mapping({"jira": "not-a-dict"})
        assert result == JIRA_DEFAULT_TYPE_NAMES
