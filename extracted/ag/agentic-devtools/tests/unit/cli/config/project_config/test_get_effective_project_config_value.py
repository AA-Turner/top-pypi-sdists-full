"""Tests for get_effective_project_config_value()."""

from unittest.mock import patch

from agentic_devtools.cli.config.project_config import get_effective_project_config_value


class TestGetEffectiveProjectConfigValue:
    """Tests for get_effective_project_config_value function."""

    def test_auto_mode_returns_value(self) -> None:
        """Auto mode returns value from project.json."""
        with patch(
            "agentic_devtools.cli.config.project_config.load_effective_project_config",
            return_value={"default_copilot_model": "gpt-4o"},
        ):
            assert get_effective_project_config_value("default_copilot_model") == "gpt-4o"

    def test_auto_mode_returns_none_for_missing_key(self) -> None:
        """Auto mode returns None for missing key."""
        with patch(
            "agentic_devtools.cli.config.project_config.load_effective_project_config",
            return_value={"other_key": "value"},
        ):
            assert get_effective_project_config_value("default_copilot_model") is None

    def test_manual_mode_returns_none(self) -> None:
        """Manual mode always returns None."""
        with patch(
            "agentic_devtools.cli.config.project_config.load_effective_project_config",
            return_value={},
        ):
            assert get_effective_project_config_value("default_copilot_model") is None

    def test_stringifies_non_string_values(self) -> None:
        """Non-string values are converted to string."""
        with patch(
            "agentic_devtools.cli.config.project_config.load_effective_project_config",
            return_value={"count": 42},
        ):
            assert get_effective_project_config_value("count") == "42"
