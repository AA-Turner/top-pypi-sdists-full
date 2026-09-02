"""Tests for load_effective_project_config()."""

from unittest.mock import patch

from agentic_devtools.cli.config.project_config import load_effective_project_config


class TestLoadEffectiveProjectConfig:
    """Tests for load_effective_project_config function."""

    def test_auto_mode_returns_full_config(self) -> None:
        """Auto mode delegates to load_project_config."""
        config_data = {"default_copilot_model": "gpt-4o", "jira_base_url": "http://jira.example.com"}
        with (
            patch(
                "agentic_devtools.state.get_value",
                return_value="auto",
            ),
            patch(
                "agentic_devtools.cli.config.project_config.load_project_config",
                return_value=config_data,
            ),
        ):
            result = load_effective_project_config()
            assert result == config_data

    def test_manual_mode_returns_empty_dict(self) -> None:
        """Manual mode returns empty dict regardless of project.json content."""
        with patch(
            "agentic_devtools.state.get_value",
            return_value="manual",
        ):
            result = load_effective_project_config()
            assert result == {}

    def test_absent_mode_defaults_to_auto(self) -> None:
        """Absent config_mode defaults to auto (backward compat)."""
        config_data = {"key": "value"}
        with (
            patch(
                "agentic_devtools.state.get_value",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.config.project_config.load_project_config",
                return_value=config_data,
            ),
        ):
            result = load_effective_project_config()
            assert result == config_data

    def test_raises_valueerror_on_invalid_mode(self) -> None:
        """Invalid config_mode raises ValueError."""
        import pytest

        with (
            patch(
                "agentic_devtools.state.get_value",
                return_value="bogus",
            ),
            pytest.raises(ValueError, match="Invalid config_mode"),
        ):
            load_effective_project_config()
