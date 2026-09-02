"""Tests for load_github_type_mapping config loader (FR-002)."""

from __future__ import annotations

from agentic_devtools.adapters.issue_type_mapping import (
    GITHUB_DEFAULT_LABELS,
    load_github_type_mapping,
)


class TestLoadGitHubTypeMapping:
    def test_empty_config_returns_defaults(self) -> None:
        result = load_github_type_mapping({})
        assert result == GITHUB_DEFAULT_LABELS

    def test_partial_override_merges_over_defaults(self) -> None:
        config = {"github": {"issue_type_labels": {"epic": "EPIC"}}}
        result = load_github_type_mapping(config)
        assert result["epic"] == "EPIC"
        assert result["bug"] == GITHUB_DEFAULT_LABELS["bug"]

    def test_override_values_are_trimmed(self) -> None:
        config = {"github": {"issue_type_labels": {"epic": "  EPIC  "}}}
        result = load_github_type_mapping(config)
        assert result["epic"] == "EPIC"

    def test_full_override(self) -> None:
        overrides = {k: f"Custom-{k}" for k in GITHUB_DEFAULT_LABELS}
        config = {"github": {"issue_type_labels": overrides}}
        result = load_github_type_mapping(config)
        for key in GITHUB_DEFAULT_LABELS:
            assert result[key] == f"Custom-{key}"

    def test_absent_github_section_uses_defaults(self) -> None:
        result = load_github_type_mapping({"jira": {}})
        assert result == GITHUB_DEFAULT_LABELS

    def test_absent_issue_type_labels_uses_defaults(self) -> None:
        result = load_github_type_mapping({"github": {}})
        assert result == GITHUB_DEFAULT_LABELS

    def test_non_dict_github_section_uses_defaults(self) -> None:
        result = load_github_type_mapping({"github": "not-a-dict"})
        assert result == GITHUB_DEFAULT_LABELS
