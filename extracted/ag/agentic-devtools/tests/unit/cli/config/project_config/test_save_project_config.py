"""Tests for save_project_config function."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.config.project_config import save_project_config


class TestSaveProjectConfig:
    """Tests for save_project_config function."""

    def test_creates_file_and_dirs(self, tmp_path):
        """Should create directories and write config file."""
        config_file = tmp_path / "config" / "project.json"
        with patch("agentic_devtools.cli.config.project_config._get_config_path", return_value=config_file):
            result = save_project_config({"jira_project_keys": "PROJ"})
        assert result == config_file
        assert config_file.exists()
        data = json.loads(config_file.read_text(encoding="utf-8"))
        assert data == {"jira_project_keys": "PROJ"}

    def test_overwrites_existing(self, tmp_path):
        """Should overwrite existing config file."""
        config_file = tmp_path / "project.json"
        config_file.write_text('{"old": true}', encoding="utf-8")
        with patch("agentic_devtools.cli.config.project_config._get_config_path", return_value=config_file):
            save_project_config({"new": True})
        data = json.loads(config_file.read_text(encoding="utf-8"))
        assert data == {"new": True}

    def test_raises_when_no_git_root(self):
        """Should raise RuntimeError when git root cannot be determined."""
        with patch("agentic_devtools.cli.config.project_config._get_config_path", return_value=None):
            with pytest.raises(RuntimeError, match="Cannot determine git repository root"):
                save_project_config({"key": "value"})

    def test_preserves_empty_string_values(self, tmp_path):
        """Should faithfully store empty string values without stripping them."""
        config_file = tmp_path / "config" / "project.json"
        with patch("agentic_devtools.cli.config.project_config._get_config_path", return_value=config_file):
            save_project_config({"jira_project_keys": "", "vpn_url": ""})
        data = json.loads(config_file.read_text(encoding="utf-8"))
        assert data["jira_project_keys"] == ""
        assert data["vpn_url"] == ""

    def test_explicit_git_root_writes_to_that_path(self, tmp_path):
        """When git_root is passed, writes config under that path directly."""
        result = save_project_config({"agdt_version": "0.2.69"}, git_root=tmp_path)

        expected = tmp_path / ".agdt" / "config" / "project.json"
        assert result == expected
        assert expected.exists()
        data = json.loads(expected.read_text(encoding="utf-8"))
        assert data == {"agdt_version": "0.2.69"}

    def test_validates_issue_types_metadata_before_writing(self, tmp_path):
        """Should call validate_issue_types_metadata on all entries before writing."""
        invalid_config = {
            "issue_types_metadata": {
                "PROJ": {"provider": "jira"}  # missing required fields
            }
        }
        with pytest.raises(ValueError, match="issue_types_metadata"):
            save_project_config(invalid_config, git_root=tmp_path)
        # File should not be written
        config_file = tmp_path / ".agdt" / "config" / "project.json"
        assert not config_file.exists()

    def test_raises_when_issue_types_metadata_is_not_a_dict(self, tmp_path):
        """Should reject non-dict issue_types_metadata before writing."""
        invalid_config = {"issue_types_metadata": ["not", "a", "dict"]}
        with pytest.raises(ValueError, match="issue_types_metadata must be a dict"):
            save_project_config(invalid_config, git_root=tmp_path)
        config_file = tmp_path / ".agdt" / "config" / "project.json"
        assert not config_file.exists()

    def test_raises_when_issue_types_metadata_is_explicitly_none(self, tmp_path):
        """Should reject a present issue_types_metadata key with a null value."""
        invalid_config = {"issue_types_metadata": None}
        with pytest.raises(ValueError, match="issue_types_metadata must be a dict"):
            save_project_config(invalid_config, git_root=tmp_path)
        config_file = tmp_path / ".agdt" / "config" / "project.json"
        assert not config_file.exists()

    def test_raises_valueerror_with_project_key_in_message(self, tmp_path):
        """ValueError should identify the failing project key."""
        invalid_config = {
            "issue_types_metadata": {
                "BAD_PROJ": {"provider": ""}  # missing fields
            }
        }
        with pytest.raises(ValueError, match="BAD_PROJ"):
            save_project_config(invalid_config, git_root=tmp_path)

    def test_writes_valid_issue_types_metadata(self, tmp_path):
        """Should write successfully when issue_types_metadata entries are valid."""
        valid_config = {
            "issue_types_metadata": {
                "PROJ": {
                    "lastDiscovered": "2026-07-12T10:00:00+00:00",
                    "lastRefreshed": "2026-07-12T10:00:00+00:00",
                    "provider": "jira",
                    "issue_types": [],
                }
            }
        }
        result = save_project_config(valid_config, git_root=tmp_path)
        assert result.exists()
        data = json.loads(result.read_text(encoding="utf-8"))
        assert data["issue_types_metadata"]["PROJ"]["provider"] == "jira"

    def test_skips_validation_without_issue_types_metadata(self, tmp_path):
        """Should write without validation when issue_types_metadata is absent."""
        config = {"some_key": "some_value"}
        result = save_project_config(config, git_root=tmp_path)
        assert result.exists()

    def test_preserves_other_project_keys_on_round_trip(self, tmp_path):
        """Valid metadata write preserves existing entries for other project keys."""
        valid_config = {
            "other_setting": "preserved",
            "issue_types_metadata": {
                "PROJ_A": {
                    "lastDiscovered": "2026-07-12T10:00:00+00:00",
                    "lastRefreshed": "2026-07-12T10:00:00+00:00",
                    "provider": "jira",
                    "issue_types": [],
                },
                "PROJ_B": {
                    "lastDiscovered": "2026-07-13T10:00:00+00:00",
                    "lastRefreshed": "2026-07-13T10:00:00+00:00",
                    "provider": "github",
                    "issue_types": [],
                },
            },
        }
        result = save_project_config(valid_config, git_root=tmp_path)
        data = json.loads(result.read_text(encoding="utf-8"))
        assert data["other_setting"] == "preserved"
        assert "PROJ_A" in data["issue_types_metadata"]
        assert "PROJ_B" in data["issue_types_metadata"]

    def test_file_unchanged_after_validation_failure(self, tmp_path):
        """File should remain unchanged when validation fails."""
        config_file = tmp_path / ".agdt" / "config" / "project.json"
        config_file.parent.mkdir(parents=True)
        original = '{"existing": true}\n'
        config_file.write_text(original, encoding="utf-8")

        invalid_config = {
            "issue_types_metadata": {
                "PROJ": {"provider": ""}  # invalid
            }
        }
        with pytest.raises(ValueError):
            save_project_config(invalid_config, git_root=tmp_path)
        assert config_file.read_text(encoding="utf-8") == original
