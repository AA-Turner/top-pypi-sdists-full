"""Tests for agentic_devtools.config.load_platform_config."""

import json
import logging

from agentic_devtools.config import (
    DEFAULT_CODE_HOSTING,
    DEFAULT_ISSUE_ADAPTER,
    load_platform_config,
)


class TestLoadPlatformConfig:
    """Tests for load_platform_config function."""

    def test_returns_full_defaults_when_config_file_missing(self, tmp_path):
        """Return dict with all default values when .github/agdt-config.json does not exist."""
        result = load_platform_config(str(tmp_path))

        assert result["issue_adapter"] == DEFAULT_ISSUE_ADAPTER
        assert result["code_hosting"] == DEFAULT_CODE_HOSTING
        assert result["jira"] == {}
        assert result["github"] == {}
        assert result["azure_devops"] == {}

    def test_returns_full_defaults_when_platform_section_missing(self, tmp_path):
        """Return dict with all default values when config has no 'platform' key."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        (github_dir / "agdt-config.json").write_text(json.dumps({}), encoding="utf-8")

        result = load_platform_config(str(tmp_path))

        assert result["issue_adapter"] == DEFAULT_ISSUE_ADAPTER
        assert result["code_hosting"] == DEFAULT_CODE_HOSTING
        assert result["jira"] == {}
        assert result["github"] == {}
        assert result["azure_devops"] == {}

    def test_returns_parsed_platform_config_when_all_fields_valid(self, tmp_path):
        """Return parsed platform config when all fields are present and valid."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        config = {
            "platform": {
                "issue_adapter": "github",
                "code_hosting": "github",
                "jira": {"base_url": "https://jira.example.com"},
                "github": {"repo_owner": "org", "repo_name": "repo"},
                "azure_devops": {"org_url": "https://dev.azure.com/org"},
            }
        }
        (github_dir / "agdt-config.json").write_text(json.dumps(config), encoding="utf-8")

        result = load_platform_config(str(tmp_path))

        assert result["issue_adapter"] == "github"
        assert result["code_hosting"] == "github"
        assert result["jira"] == {"base_url": "https://jira.example.com"}
        assert result["github"] == {"repo_owner": "org", "repo_name": "repo"}
        assert result["azure_devops"] == {"org_url": "https://dev.azure.com/org"}

    def test_uses_default_issue_adapter_when_missing(self, tmp_path):
        """Use DEFAULT_ISSUE_ADAPTER when issue_adapter is absent from platform section."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        config = {"platform": {"code_hosting": "github"}}
        (github_dir / "agdt-config.json").write_text(json.dumps(config), encoding="utf-8")

        result = load_platform_config(str(tmp_path))

        assert result["issue_adapter"] == DEFAULT_ISSUE_ADAPTER

    def test_uses_default_code_hosting_when_missing(self, tmp_path):
        """Use DEFAULT_CODE_HOSTING when code_hosting is absent from platform section."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        config = {"platform": {"issue_adapter": "github"}}
        (github_dir / "agdt-config.json").write_text(json.dumps(config), encoding="utf-8")

        result = load_platform_config(str(tmp_path))

        assert result["code_hosting"] == DEFAULT_CODE_HOSTING

    def test_defaults_sub_dicts_to_empty_when_missing(self, tmp_path):
        """Default jira, github, azure_devops sub-dicts to {} when absent."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        config = {"platform": {"issue_adapter": "jira"}}
        (github_dir / "agdt-config.json").write_text(json.dumps(config), encoding="utf-8")

        result = load_platform_config(str(tmp_path))

        assert result["jira"] == {}
        assert result["github"] == {}
        assert result["azure_devops"] == {}

    def test_normalizes_null_sub_dicts_to_empty(self, tmp_path, caplog):
        """Normalize JSON null sub-dicts to {} without logging a warning."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        config = {"platform": {"jira": None, "github": None, "azure_devops": None}}
        (github_dir / "agdt-config.json").write_text(json.dumps(config), encoding="utf-8")

        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = load_platform_config(str(tmp_path))

        assert result["jira"] == {}
        assert result["github"] == {}
        assert result["azure_devops"] == {}
        assert not any(
            record.levelno >= logging.WARNING and record.name == "agentic_devtools.config" for record in caplog.records
        )

    def test_warns_and_uses_defaults_when_platform_is_not_a_dict(self, tmp_path, caplog):
        """Log warning and use defaults when 'platform' value is not an object."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        config = {"platform": "not-a-dict"}
        (github_dir / "agdt-config.json").write_text(json.dumps(config), encoding="utf-8")

        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = load_platform_config(str(tmp_path))

        assert result["issue_adapter"] == DEFAULT_ISSUE_ADAPTER
        assert result["code_hosting"] == DEFAULT_CODE_HOSTING
        assert any("Expected 'platform' section" in record.message for record in caplog.records)

    def test_warns_and_uses_default_for_invalid_issue_adapter(self, tmp_path, caplog):
        """Log warning and use default when issue_adapter has an invalid enum value."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        config = {"platform": {"issue_adapter": "trello"}}
        (github_dir / "agdt-config.json").write_text(json.dumps(config), encoding="utf-8")

        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = load_platform_config(str(tmp_path))

        assert result["issue_adapter"] == DEFAULT_ISSUE_ADAPTER
        assert any("Invalid issue_adapter" in record.message for record in caplog.records)

    def test_warns_and_uses_default_for_invalid_code_hosting(self, tmp_path, caplog):
        """Log warning and use default when code_hosting has an invalid enum value."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        config = {"platform": {"code_hosting": "bitbucket"}}
        (github_dir / "agdt-config.json").write_text(json.dumps(config), encoding="utf-8")

        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = load_platform_config(str(tmp_path))

        assert result["code_hosting"] == DEFAULT_CODE_HOSTING
        assert any("Invalid code_hosting" in record.message for record in caplog.records)

    def test_warns_and_uses_default_for_non_string_issue_adapter(self, tmp_path, caplog):
        """Log warning and use default when issue_adapter is a non-string type."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        config = {"platform": {"issue_adapter": {"nested": "dict"}}}
        (github_dir / "agdt-config.json").write_text(json.dumps(config), encoding="utf-8")

        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = load_platform_config(str(tmp_path))

        assert result["issue_adapter"] == DEFAULT_ISSUE_ADAPTER
        assert any("Invalid issue_adapter" in record.message for record in caplog.records)

    def test_warns_and_uses_default_for_non_string_code_hosting(self, tmp_path, caplog):
        """Log warning and use default when code_hosting is a non-string type."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        config = {"platform": {"code_hosting": ["github", "other"]}}
        (github_dir / "agdt-config.json").write_text(json.dumps(config), encoding="utf-8")

        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = load_platform_config(str(tmp_path))

        assert result["code_hosting"] == DEFAULT_CODE_HOSTING
        assert any("Invalid code_hosting" in record.message for record in caplog.records)

    def test_warns_and_uses_empty_dict_when_sub_dict_is_not_a_dict(self, tmp_path, caplog):
        """Log warning and use {} when a platform sub-dict is not a dict."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        config = {"platform": {"jira": "invalid", "github": 42, "azure_devops": ["list"]}}
        (github_dir / "agdt-config.json").write_text(json.dumps(config), encoding="utf-8")

        with caplog.at_level(logging.WARNING, logger="agentic_devtools.config"):
            result = load_platform_config(str(tmp_path))

        assert result["jira"] == {}
        assert result["github"] == {}
        assert result["azure_devops"] == {}
        warning_messages = [r.message for r in caplog.records if r.levelno == logging.WARNING]
        assert any("platform.jira" in m for m in warning_messages)
        assert any("platform.github" in m for m in warning_messages)
        assert any("platform.azure_devops" in m for m in warning_messages)

    def test_preserves_unknown_keys_in_platform_section(self, tmp_path):
        """Silently preserve unknown keys in platform section for forward-compatibility."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        config = {"platform": {"issue_adapter": "jira", "custom_key": "custom_value", "future_setting": 123}}
        (github_dir / "agdt-config.json").write_text(json.dumps(config), encoding="utf-8")

        result = load_platform_config(str(tmp_path))

        assert result["custom_key"] == "custom_value"
        assert result["future_setting"] == 123

    def test_preserves_other_top_level_sections(self, tmp_path):
        """Other top-level sections (e.g., 'review') are not affected by platform loading."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        config = {
            "review": {"focus-areas-file": ".github/focus.md"},
            "platform": {"issue_adapter": "github"},
        }
        (github_dir / "agdt-config.json").write_text(json.dumps(config), encoding="utf-8")

        # load_platform_config only reads the platform section — verify it doesn't
        # interfere with other sections by calling load_repo_config separately.
        from agentic_devtools.config import load_repo_config

        full_config = load_repo_config(str(tmp_path))
        assert full_config["review"] == {"focus-areas-file": ".github/focus.md"}

        result = load_platform_config(str(tmp_path))
        assert result["issue_adapter"] == "github"

    def test_phase_0_defaults_when_config_file_missing(self, tmp_path):
        """phase_0 defaults present when config file does not exist."""
        result = load_platform_config(str(tmp_path))

        assert result["phase_0"] == {
            "enabled": False,
            "sync_back_on_merge": False,
            "sync_back_fields": ["comment"],
        }

    def test_phase_0_defaults_when_platform_section_missing(self, tmp_path):
        """phase_0 defaults present when platform section is missing."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        (github_dir / "agdt-config.json").write_text(json.dumps({}), encoding="utf-8")

        result = load_platform_config(str(tmp_path))

        assert result["phase_0"] == {
            "enabled": False,
            "sync_back_on_merge": False,
            "sync_back_fields": ["comment"],
        }

    def test_phase_0_defaults_when_phase_0_key_absent(self, tmp_path):
        """phase_0 defaults present when phase_0 key is absent from platform."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        config = {"platform": {"issue_adapter": "github"}}
        (github_dir / "agdt-config.json").write_text(json.dumps(config), encoding="utf-8")

        result = load_platform_config(str(tmp_path))

        assert result["phase_0"] == {
            "enabled": False,
            "sync_back_on_merge": False,
            "sync_back_fields": ["comment"],
        }

    def test_explicit_phase_0_values_flow_through(self, tmp_path):
        """Explicit phase_0 values flow through full load_platform_config() path."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        config = {
            "platform": {
                "issue_adapter": "github",
                "phase_0": {
                    "enabled": True,
                    "sync_back_on_merge": True,
                    "sync_back_fields": ["comment", "label"],
                },
            }
        }
        (github_dir / "agdt-config.json").write_text(json.dumps(config), encoding="utf-8")

        result = load_platform_config(str(tmp_path))

        assert result["phase_0"]["enabled"] is True
        assert result["phase_0"]["sync_back_on_merge"] is True
        assert result["phase_0"]["sync_back_fields"] == ["comment", "label"]

    def test_phase_0_sync_back_fields_is_fresh_list_per_call(self, tmp_path):
        """Returned sync_back_fields is a fresh mutable list copy per call."""
        result1 = load_platform_config(str(tmp_path))
        result2 = load_platform_config(str(tmp_path))

        assert result1["phase_0"]["sync_back_fields"] == result2["phase_0"]["sync_back_fields"]
        assert result1["phase_0"]["sync_back_fields"] is not result2["phase_0"]["sync_back_fields"]
