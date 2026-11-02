"""Tests for _parse_issue_management_section function."""

import pytest

from agentic_devtools.epic_tree.config import _parse_issue_management_section
from agentic_devtools.epic_tree.errors import ConfigError


class TestParseIssueManagementSectionHappyPath:
    """Happy-path tests for _parse_issue_management_section."""

    def test_empty_section_returns_empty_dict(self):
        """Empty section returns empty result dict."""
        result = _parse_issue_management_section({}, "config.json", "github")
        assert result == {}

    def test_parses_max_depth(self):
        """Parses maxDepth from provider block."""
        result = _parse_issue_management_section({"maxDepth": 2}, "config.json", "github")
        assert result["max_depth"] == 2

    def test_parses_allowed_labels(self):
        """Parses allowedLabels from provider block."""
        result = _parse_issue_management_section(
            {"allowedLabels": {"0": ["epic"], "1": ["feature", "enhancement"]}},
            "config.json",
            "github",
        )
        assert result["allowed_labels"] == {0: ["epic"], 1: ["feature", "enhancement"]}

    def test_parses_allowed_issue_types(self):
        """Parses allowedIssueTypes from provider block."""
        result = _parse_issue_management_section(
            {"allowedIssueTypes": {"0": ["Epic"], "1": ["Story"]}},
            "config.json",
            "jira",
        )
        assert result["allowed_issue_types"] == {0: ["Epic"], 1: ["Story"]}

    def test_parses_required_body_sections(self):
        """Parses requiredBodySections from provider block."""
        result = _parse_issue_management_section(
            {"requiredBodySections": {"0": ["Summary", "Goals"]}},
            "config.json",
            "github",
        )
        assert result["required_body_sections"] == {0: ["Summary", "Goals"]}

    def test_parses_default_labels(self):
        """Parses defaultLabels from provider block."""
        result = _parse_issue_management_section(
            {"defaultLabels": {"0": ["initiative"], "1": ["story"]}},
            "config.json",
            "github",
        )
        assert result["default_labels"] == {0: ["initiative"], 1: ["story"]}

    def test_parses_default_issue_types(self):
        """Parses defaultIssueTypes from provider block."""
        result = _parse_issue_management_section(
            {"defaultIssueTypes": {"0": "Initiative", "1": "Story"}},
            "config.json",
            "jira",
        )
        assert result["default_issue_types"] == {0: "Initiative", 1: "Story"}

    def test_unknown_keys_silently_ignored(self):
        """Unknown keys in the section are silently ignored."""
        result = _parse_issue_management_section(
            {"unknownKey": "value", "anotherKey": [1, 2, 3]},
            "config.json",
            "github",
        )
        assert result == {}


class TestParseIssueManagementSectionErrors:
    """Error scenarios for _parse_issue_management_section (FR-008/SC-004)."""

    def test_non_numeric_depth_key_in_allowed_labels(self):
        """Non-numeric depth key raises ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _parse_issue_management_section({"allowedLabels": {"abc": ["label"]}}, "config.json", "github")
        assert "issueManagement.github.allowedLabels" in str(exc_info.value)

    def test_negative_depth_key_in_allowed_labels(self):
        """Negative depth key raises ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _parse_issue_management_section({"allowedLabels": {"-1": ["label"]}}, "config.json", "github")
        assert "out of range" in str(exc_info.value)

    def test_out_of_range_depth_key_in_allowed_labels(self):
        """Depth key >= 3 raises ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _parse_issue_management_section({"allowedLabels": {"3": ["label"]}}, "config.json", "github")
        assert "out of range" in str(exc_info.value)

    def test_non_list_allowlist_values(self):
        """Non-list values for per-depth entries raise ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _parse_issue_management_section({"allowedLabels": {"0": "not-a-list"}}, "config.json", "github")
        assert "list of strings" in str(exc_info.value)

    def test_non_string_list_elements(self):
        """Non-string elements in per-depth list raise ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _parse_issue_management_section({"allowedLabels": {"0": [123, 456]}}, "config.json", "github")
        assert "list of strings" in str(exc_info.value)

    def test_non_string_default_issue_types_values(self):
        """Non-string per-depth values for defaultIssueTypes raise ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _parse_issue_management_section({"defaultIssueTypes": {"0": 123}}, "config.json", "jira")
        assert "defaultIssueTypes" in str(exc_info.value)

    def test_invalid_max_depth_type(self):
        """Non-integer maxDepth raises ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _parse_issue_management_section({"maxDepth": "two"}, "config.json", "github")
        assert "maxDepth" in str(exc_info.value)

    def test_invalid_max_depth_too_large(self):
        """maxDepth > 3 raises ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _parse_issue_management_section({"maxDepth": 4}, "config.json", "github")
        assert "maxDepth" in str(exc_info.value)

    def test_invalid_max_depth_zero(self):
        """maxDepth < 1 raises ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _parse_issue_management_section({"maxDepth": 0}, "config.json", "github")
        assert "maxDepth" in str(exc_info.value)

    def test_non_dict_allowed_labels_raises(self):
        """Non-dict allowedLabels raises ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _parse_issue_management_section({"allowedLabels": "not-a-dict"}, "config.json", "github")
        assert "must be an object" in str(exc_info.value)

    def test_non_dict_default_issue_types_raises(self):
        """Non-dict defaultIssueTypes raises ConfigError."""
        with pytest.raises(ConfigError) as exc_info:
            _parse_issue_management_section({"defaultIssueTypes": [1, 2]}, "config.json", "jira")
        assert "must be an object" in str(exc_info.value)
