"""Tests for load_epic_tree_config function."""

import json

import pytest

from agentic_devtools.epic_tree.config import EpicTreeConfig, load_epic_tree_config
from agentic_devtools.epic_tree.errors import ConfigError


class TestLoadEpicTreeConfigDefaults:
    """Tests for default config when no config file present."""

    def test_returns_defaults_when_no_repo_path(self):
        """Returns default config when repo_path is None."""
        config = load_epic_tree_config(None)
        assert config.max_depth == 3
        assert config.default_issue_types == {0: "Epic", 1: "Feature", 2: "Subtask"}
        assert config.default_labels == {0: ["epic"], 1: ["feature"], 2: ["subtask"]}

    def test_provider_override_without_repo_path(self):
        """An explicit provider is honored even when repo_path is None."""
        config = load_epic_tree_config(None, provider="GitHub")
        assert config.provider == "github"

    def test_provider_override_ignored_when_blank_without_repo_path(self):
        """A blank provider falls back to defaults when repo_path is None."""
        config = load_epic_tree_config(None, provider="   ")
        assert isinstance(config, EpicTreeConfig)

    def test_non_string_provider_raises_config_error_without_repo_path(self):
        """A non-string provider raises ConfigError before any strip call."""
        with pytest.raises(ConfigError, match="must be a string"):
            load_epic_tree_config(None, provider=123)  # type: ignore[arg-type]

    def test_non_string_provider_raises_config_error_with_repo_path(self, tmp_path):
        """A non-string provider raises ConfigError when repo_path is provided."""
        with pytest.raises(ConfigError, match="must be a string"):
            load_epic_tree_config(tmp_path, provider=123)  # type: ignore[arg-type]

    def test_unsupported_provider_raises_config_error_without_repo_path(self):
        """An unsupported provider name raises ConfigError when repo_path is None."""
        with pytest.raises(ConfigError, match="unsupported provider"):
            load_epic_tree_config(None, provider="gitlab")

    def test_unsupported_provider_raises_config_error_with_repo_path(self, tmp_path):
        """An unsupported provider name raises ConfigError when repo_path is provided."""
        with pytest.raises(ConfigError, match="unsupported provider"):
            load_epic_tree_config(tmp_path, provider="gitlab")

    def test_provider_override_with_repo_path(self, tmp_path):
        """An explicit provider is normalized and honored with a repo_path."""
        config = load_epic_tree_config(tmp_path, provider="JIRA")
        assert config.provider == "jira"

    def test_returns_defaults_when_no_config_file(self, tmp_path):
        """Returns default config when agdt-config.json doesn't exist."""
        config = load_epic_tree_config(tmp_path)
        assert config.max_depth == 3
        assert isinstance(config, EpicTreeConfig)

    def test_returns_defaults_when_no_epic_tree_section(self, tmp_path):
        """Returns default config when epicTree section is absent."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text(json.dumps({"other": "data"}), encoding="utf-8")
        config = load_epic_tree_config(tmp_path)
        assert config.max_depth == 3

    def test_default_labels_are_isolated_between_instances(self):
        """Default label lists are copied per config instance."""
        config_a = EpicTreeConfig()
        config_b = EpicTreeConfig()

        config_a.default_labels[0].append("custom")

        assert config_b.default_labels == {0: ["epic"], 1: ["feature"], 2: ["subtask"]}


class TestLoadEpicTreeConfigParsing:
    """Tests for config file parsing."""

    def _write_config(self, tmp_path, epic_tree_section):
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text(json.dumps({"epicTree": epic_tree_section}), encoding="utf-8")

    def test_parses_max_depth(self, tmp_path):
        """Parses maxDepth from config."""
        self._write_config(tmp_path, {"maxDepth": 2})
        config = load_epic_tree_config(tmp_path)
        assert config.max_depth == 2

    def test_parses_allowed_labels(self, tmp_path):
        """Parses allowedLabels from config."""
        self._write_config(tmp_path, {"allowedLabels": {"0": ["epic"], "1": ["feature", "enhancement"]}})
        config = load_epic_tree_config(tmp_path)
        assert config.allowed_labels == {0: ["epic"], 1: ["feature", "enhancement"]}

    def test_parses_allowed_issue_types(self, tmp_path):
        """Parses allowedIssueTypes from config."""
        self._write_config(tmp_path, {"allowedIssueTypes": {"0": ["Epic"], "1": ["Feature", "Story"]}})
        config = load_epic_tree_config(tmp_path)
        assert config.allowed_issue_types == {0: ["Epic"], 1: ["Feature", "Story"]}

    def test_parses_required_body_sections(self, tmp_path):
        """Parses requiredBodySections from config."""
        self._write_config(tmp_path, {"requiredBodySections": {"0": ["Summary", "Goals"]}})
        config = load_epic_tree_config(tmp_path)
        assert config.required_body_sections == {0: ["Summary", "Goals"]}

    def test_parses_default_issue_types(self, tmp_path):
        """Parses defaultIssueTypes from config."""
        self._write_config(tmp_path, {"defaultIssueTypes": {"0": "Initiative", "1": "Story", "2": "Task"}})
        config = load_epic_tree_config(tmp_path)
        assert config.default_issue_types == {0: "Initiative", 1: "Story", 2: "Task"}

    def test_parses_default_labels(self, tmp_path):
        """Parses defaultLabels from config."""
        self._write_config(tmp_path, {"defaultLabels": {"0": ["initiative"], "1": ["story"]}})
        config = load_epic_tree_config(tmp_path)
        assert config.default_labels == {0: ["initiative"], 1: ["story"]}

    def test_missing_default_labels_returns_fresh_default_lists(self, tmp_path):
        """Missing defaultLabels uses non-shared default lists."""
        self._write_config(tmp_path, {"maxDepth": 3})

        config_a = load_epic_tree_config(tmp_path)
        config_b = load_epic_tree_config(tmp_path)
        config_a.default_labels[0].append("custom")

        assert config_b.default_labels == {0: ["epic"], 1: ["feature"], 2: ["subtask"]}


class TestLoadEpicTreeConfigErrors:
    """Tests for config validation errors."""

    def _write_config(self, tmp_path, epic_tree_section):
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        config_file = config_dir / "agdt-config.json"
        config_file.write_text(json.dumps({"epicTree": epic_tree_section}), encoding="utf-8")

    def test_max_depth_exceeds_limit(self, tmp_path):
        """maxDepth > 3 raises ConfigError."""
        self._write_config(tmp_path, {"maxDepth": 4})
        with pytest.raises(ConfigError) as exc_info:
            load_epic_tree_config(tmp_path)
        assert "maxDepth" in str(exc_info.value)

    def test_max_depth_non_positive(self, tmp_path):
        """maxDepth < 1 raises ConfigError."""
        self._write_config(tmp_path, {"maxDepth": 0})
        with pytest.raises(ConfigError) as exc_info:
            load_epic_tree_config(tmp_path)
        assert "maxDepth" in str(exc_info.value)

    def test_default_issue_types_non_string_value(self, tmp_path):
        """Non-string values in defaultIssueTypes raises ConfigError."""
        self._write_config(tmp_path, {"defaultIssueTypes": {"0": 123}})
        with pytest.raises(ConfigError) as exc_info:
            load_epic_tree_config(tmp_path)
        assert "defaultIssueTypes" in str(exc_info.value)

    def test_non_numeric_depth_key(self, tmp_path):
        """Non-numeric depth key raises ConfigError."""
        self._write_config(tmp_path, {"allowedLabels": {"abc": ["label"]}})
        with pytest.raises(ConfigError) as exc_info:
            load_epic_tree_config(tmp_path)
        assert "allowedLabels" in str(exc_info.value)

    def test_allowed_labels_negative_depth_key_rejected(self, tmp_path):
        """Negative depth key in allowedLabels raises ConfigError."""
        self._write_config(tmp_path, {"allowedLabels": {"-1": ["label"]}})
        with pytest.raises(ConfigError) as exc_info:
            load_epic_tree_config(tmp_path)
        assert "allowedLabels" in str(exc_info.value)
        assert "out of range" in str(exc_info.value)

    def test_allowed_labels_depth_key_too_large_rejected(self, tmp_path):
        """Depth key >= 3 in allowedLabels raises ConfigError."""
        self._write_config(tmp_path, {"allowedLabels": {"3": ["label"]}})
        with pytest.raises(ConfigError) as exc_info:
            load_epic_tree_config(tmp_path)
        assert "allowedLabels" in str(exc_info.value)
        assert "out of range" in str(exc_info.value)

    def test_allowed_issue_types_negative_depth_key_rejected(self, tmp_path):
        """Negative depth key in allowedIssueTypes raises ConfigError."""
        self._write_config(tmp_path, {"allowedIssueTypes": {"-1": ["Epic"]}})
        with pytest.raises(ConfigError) as exc_info:
            load_epic_tree_config(tmp_path)
        assert "allowedIssueTypes" in str(exc_info.value)
        assert "out of range" in str(exc_info.value)

    def test_allowed_issue_types_depth_key_too_large_rejected(self, tmp_path):
        """Depth key >= 3 in allowedIssueTypes raises ConfigError."""
        self._write_config(tmp_path, {"allowedIssueTypes": {"3": ["Epic"]}})
        with pytest.raises(ConfigError) as exc_info:
            load_epic_tree_config(tmp_path)
        assert "allowedIssueTypes" in str(exc_info.value)
        assert "out of range" in str(exc_info.value)

    def test_default_issue_types_negative_depth_key_rejected(self, tmp_path):
        """Negative depth key in defaultIssueTypes raises ConfigError."""
        self._write_config(tmp_path, {"defaultIssueTypes": {"-1": "Epic"}})
        with pytest.raises(ConfigError) as exc_info:
            load_epic_tree_config(tmp_path)
        assert "defaultIssueTypes" in str(exc_info.value)
        assert "out of range" in str(exc_info.value)

    def test_default_issue_types_depth_key_too_large_rejected(self, tmp_path):
        """Depth key >= 3 in defaultIssueTypes raises ConfigError."""
        self._write_config(tmp_path, {"defaultIssueTypes": {"3": "Epic"}})
        with pytest.raises(ConfigError) as exc_info:
            load_epic_tree_config(tmp_path)
        assert "defaultIssueTypes" in str(exc_info.value)
        assert "out of range" in str(exc_info.value)

    def test_allowed_labels_non_dict_value_ignored(self, tmp_path):
        """Non-dict allowedLabels returns empty (treated as no config)."""
        self._write_config(tmp_path, {"allowedLabels": "not-a-dict"})
        config = load_epic_tree_config(tmp_path)
        assert config.allowed_labels == {}

    def test_allowed_labels_non_string_list_values(self, tmp_path):
        """Non-string items in allowedLabels list raises ConfigError."""
        self._write_config(tmp_path, {"allowedLabels": {"0": [123, 456]}})
        with pytest.raises(ConfigError) as exc_info:
            load_epic_tree_config(tmp_path)
        assert "allowedLabels" in str(exc_info.value)
        assert "list of strings" in str(exc_info.value)

    def test_default_issue_types_non_dict_value_ignored(self, tmp_path):
        """Non-dict defaultIssueTypes returns defaults."""
        self._write_config(tmp_path, {"defaultIssueTypes": "not-a-dict"})
        config = load_epic_tree_config(tmp_path)
        assert config.default_issue_types == {0: "Epic", 1: "Feature", 2: "Subtask"}

    def test_default_issue_types_non_numeric_key(self, tmp_path):
        """Non-numeric depth key in defaultIssueTypes raises ConfigError."""
        self._write_config(tmp_path, {"defaultIssueTypes": {"abc": "Epic"}})
        with pytest.raises(ConfigError) as exc_info:
            load_epic_tree_config(tmp_path)
        assert "defaultIssueTypes" in str(exc_info.value)
        assert "numeric string" in str(exc_info.value)


class TestLoadEpicTreeConfigProvider:
    """Tests for provider resolution in load_epic_tree_config."""

    def _write_config(self, tmp_path, config_data):
        config_dir = tmp_path / ".github"
        config_dir.mkdir(exist_ok=True)
        config_file = config_dir / "agdt-config.json"
        config_file.write_text(json.dumps(config_data), encoding="utf-8")

    def test_provider_defaults_to_jira_when_no_platform(self, tmp_path):
        """Provider defaults to 'jira' when no platform section."""
        self._write_config(tmp_path, {"epicTree": {"maxDepth": 2}})
        config = load_epic_tree_config(tmp_path)
        assert config.provider == "jira"

    def test_provider_from_platform_issue_adapter_github(self, tmp_path):
        """Provider reflects platform.issue_adapter = github."""
        self._write_config(tmp_path, {"platform": {"issue_adapter": "github"}, "epicTree": {"maxDepth": 2}})
        config = load_epic_tree_config(tmp_path)
        assert config.provider == "github"

    def test_provider_from_platform_issue_adapter_markdown(self, tmp_path):
        """Provider reflects platform.issue_adapter = markdown."""
        self._write_config(tmp_path, {"platform": {"issue_adapter": "markdown"}, "epicTree": {"maxDepth": 2}})
        config = load_epic_tree_config(tmp_path)
        assert config.provider == "markdown"

    def test_provider_default_when_invalid_adapter(self, tmp_path):
        """Provider defaults to jira when adapter is invalid."""
        self._write_config(tmp_path, {"platform": {"issue_adapter": "unknown"}, "epicTree": {"maxDepth": 2}})
        config = load_epic_tree_config(tmp_path)
        assert config.provider == "jira"

    def test_provider_set_even_without_epic_tree_section(self, tmp_path):
        """Provider is set even when no epicTree section."""
        self._write_config(tmp_path, {"platform": {"issue_adapter": "github"}})
        config = load_epic_tree_config(tmp_path)
        assert config.provider == "github"

    def test_provider_set_when_no_matching_issue_management_block(self, tmp_path):
        """Provider reflects adapter even when issueManagement block doesn't match."""
        self._write_config(
            tmp_path,
            {
                "platform": {"issue_adapter": "github"},
                "issueManagement": {"jira": {"maxDepth": 2}},
            },
        )
        config = load_epic_tree_config(tmp_path)
        assert config.provider == "github"


class TestLoadEpicTreeConfigIssueManagement:
    """Tests for issueManagement section integration in load_epic_tree_config."""

    def _write_config(self, tmp_path, config_data):
        config_dir = tmp_path / ".github"
        config_dir.mkdir(exist_ok=True)
        config_file = config_dir / "agdt-config.json"
        config_file.write_text(json.dumps(config_data), encoding="utf-8")

    def test_issue_management_allowed_labels_resolved(self, tmp_path):
        """issueManagement.github.allowedLabels is resolved for github provider."""
        self._write_config(
            tmp_path,
            {
                "platform": {"issue_adapter": "github"},
                "issueManagement": {
                    "github": {
                        "allowedLabels": {"0": ["epic", "initiative"], "1": ["feature"]},
                    }
                },
            },
        )
        config = load_epic_tree_config(tmp_path)
        assert config.allowed_labels == {0: ["epic", "initiative"], 1: ["feature"]}
        assert config.provider == "github"

    def test_issue_management_merges_with_epic_tree(self, tmp_path):
        """issueManagement overrides epicTree per depth key."""
        self._write_config(
            tmp_path,
            {
                "platform": {"issue_adapter": "github"},
                "epicTree": {
                    "allowedLabels": {"0": ["epic"], "1": ["feature"], "2": ["subtask"]},
                },
                "issueManagement": {
                    "github": {
                        "allowedLabels": {"0": ["initiative"]},
                    }
                },
            },
        )
        config = load_epic_tree_config(tmp_path)
        # Depth 0 overridden by issueManagement, depths 1 and 2 from epicTree
        assert config.allowed_labels == {0: ["initiative"], 1: ["feature"], 2: ["subtask"]}

    def test_issue_management_max_depth_overrides_epic_tree(self, tmp_path):
        """issueManagement maxDepth overrides epicTree maxDepth."""
        self._write_config(
            tmp_path,
            {
                "platform": {"issue_adapter": "jira"},
                "epicTree": {"maxDepth": 3},
                "issueManagement": {
                    "jira": {"maxDepth": 2},
                },
            },
        )
        config = load_epic_tree_config(tmp_path)
        assert config.max_depth == 2

    def test_issue_management_boolean_max_depth_rejected(self, tmp_path):
        """Boolean issueManagement maxDepth raises ConfigError."""
        self._write_config(
            tmp_path,
            {
                "platform": {"issue_adapter": "jira"},
                "issueManagement": {
                    "jira": {"maxDepth": True},
                },
            },
        )
        with pytest.raises(ConfigError) as exc_info:
            load_epic_tree_config(tmp_path)
        assert "issueManagement.jira.maxDepth" in str(exc_info.value)

    def test_issue_management_default_issue_types_merged(self, tmp_path):
        """issueManagement defaultIssueTypes merged with epicTree."""
        self._write_config(
            tmp_path,
            {
                "platform": {"issue_adapter": "jira"},
                "epicTree": {
                    "defaultIssueTypes": {"0": "Epic", "1": "Story", "2": "Task"},
                },
                "issueManagement": {
                    "jira": {
                        "maxDepth": 3,
                        "defaultIssueTypes": {"0": "Initiative"},
                    }
                },
            },
        )
        config = load_epic_tree_config(tmp_path)
        assert config.default_issue_types == {0: "Initiative", 1: "Story", 2: "Task"}

    def test_backward_compat_no_issue_management(self, tmp_path):
        """Config with no issueManagement uses epicTree unchanged."""
        self._write_config(
            tmp_path,
            {
                "epicTree": {
                    "maxDepth": 2,
                    "allowedLabels": {"0": ["epic"], "1": ["feature"]},
                },
            },
        )
        config = load_epic_tree_config(tmp_path)
        assert config.max_depth == 2
        assert config.allowed_labels == {0: ["epic"], 1: ["feature"]}

    def test_backward_compat_no_epic_tree_no_issue_management(self, tmp_path):
        """Config with neither section uses defaults."""
        self._write_config(tmp_path, {"platform": {"issue_adapter": "github"}})
        config = load_epic_tree_config(tmp_path)
        assert config.max_depth == 3
        assert config.allowed_labels == {}
        assert config.default_labels == {0: ["epic"], 1: ["feature"], 2: ["subtask"]}
        assert config.default_issue_types == {0: "Epic", 1: "Feature", 2: "Subtask"}

    def test_partial_overlap_preserves_lower_precedence_keys(self, tmp_path):
        """Non-overlapping depth keys from epicTree are preserved."""
        self._write_config(
            tmp_path,
            {
                "platform": {"issue_adapter": "github"},
                "epicTree": {
                    "allowedLabels": {"0": ["epic"], "1": ["feature"], "2": ["subtask"]},
                },
                "issueManagement": {
                    "github": {
                        "allowedLabels": {"0": ["initiative"], "1": ["story"]},
                    }
                },
            },
        )
        config = load_epic_tree_config(tmp_path)
        # Depth 2 preserved from epicTree
        assert config.allowed_labels[2] == ["subtask"]

    def test_depth_key_exceeding_effective_max_depth_raises(self, tmp_path):
        """issueManagement depth key >= effective maxDepth raises ConfigError."""
        self._write_config(
            tmp_path,
            {
                "platform": {"issue_adapter": "github"},
                "issueManagement": {
                    "github": {
                        "maxDepth": 2,
                        "allowedLabels": {"0": ["epic"], "1": ["feature"], "2": ["subtask"]},
                    }
                },
            },
        )
        with pytest.raises(ConfigError) as exc_info:
            load_epic_tree_config(tmp_path)
        assert "exceeds effective maxDepth" in str(exc_info.value)

    def test_depth_key_exceeding_effective_max_depth_default_issue_types_raises(self, tmp_path):
        """issueManagement defaultIssueTypes depth key >= effective maxDepth raises ConfigError."""
        self._write_config(
            tmp_path,
            {
                "platform": {"issue_adapter": "github"},
                "issueManagement": {
                    "github": {
                        "maxDepth": 2,
                        "defaultIssueTypes": {"0": "Epic", "1": "Feature", "2": "Subtask"},
                    }
                },
            },
        )
        with pytest.raises(ConfigError) as exc_info:
            load_epic_tree_config(tmp_path)
        assert "exceeds effective maxDepth" in str(exc_info.value)
        assert "defaultIssueTypes" in str(exc_info.value)

    def test_issue_management_non_dict_ignored(self, tmp_path):
        """Non-dict issueManagement section is ignored (falls back to epicTree)."""
        self._write_config(
            tmp_path,
            {
                "platform": {"issue_adapter": "github"},
                "issueManagement": "not-a-dict",
                "epicTree": {"maxDepth": 2},
            },
        )
        config = load_epic_tree_config(tmp_path)
        assert config.max_depth == 2
        assert config.provider == "github"

    def test_issue_management_provider_block_non_dict_ignored(self, tmp_path):
        """Non-dict provider block within issueManagement is ignored."""
        self._write_config(
            tmp_path,
            {
                "platform": {"issue_adapter": "github"},
                "issueManagement": {"github": "not-a-dict"},
                "epicTree": {"maxDepth": 2},
            },
        )
        config = load_epic_tree_config(tmp_path)
        assert config.max_depth == 2
        assert config.provider == "github"

    def test_resolved_config_exposes_all_fields(self, tmp_path):
        """Full precedence merge exposes all resolved fields."""
        self._write_config(
            tmp_path,
            {
                "platform": {"issue_adapter": "github"},
                "epicTree": {
                    "maxDepth": 3,
                    "defaultLabels": {"0": ["epic"], "1": ["feature"], "2": ["subtask"]},
                    "defaultIssueTypes": {"0": "Epic", "1": "Feature", "2": "Subtask"},
                },
                "issueManagement": {
                    "github": {
                        "allowedLabels": {"0": ["epic", "initiative"]},
                        "allowedIssueTypes": {"0": ["Epic"]},
                        "requiredBodySections": {"0": ["Summary"]},
                    }
                },
            },
        )
        config = load_epic_tree_config(tmp_path)
        assert config.provider == "github"
        assert config.max_depth == 3
        assert config.allowed_labels == {0: ["epic", "initiative"]}
        assert config.allowed_issue_types == {0: ["Epic"]}
        assert config.required_body_sections == {0: ["Summary"]}
        assert config.default_labels == {0: ["epic"], 1: ["feature"], 2: ["subtask"]}
        assert config.default_issue_types == {0: "Epic", 1: "Feature", 2: "Subtask"}
