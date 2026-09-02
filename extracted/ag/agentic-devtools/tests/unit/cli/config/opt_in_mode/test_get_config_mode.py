"""Tests for get_config_mode()."""

from unittest.mock import patch

from agentic_devtools.cli.config.opt_in_mode import get_config_mode


class TestGetConfigMode:
    """Tests for get_config_mode function."""

    def test_returns_auto_when_key_absent(self) -> None:
        """Absent config_mode defaults to 'auto'."""
        with patch("agentic_devtools.state.get_value", return_value=None):
            assert get_config_mode() == "auto"

    def test_returns_auto_when_value_is_auto(self) -> None:
        """Explicit 'auto' value is returned."""
        with patch("agentic_devtools.state.get_value", return_value="auto"):
            assert get_config_mode() == "auto"

    def test_returns_manual_when_value_is_manual(self) -> None:
        """Explicit 'manual' value is returned."""
        with patch("agentic_devtools.state.get_value", return_value="manual"):
            assert get_config_mode() == "manual"

    def test_returns_auto_when_value_is_empty_string(self) -> None:
        """Empty string defaults to 'auto'."""
        with patch("agentic_devtools.state.get_value", return_value=""):
            assert get_config_mode() == "auto"

    def test_returns_auto_when_value_is_whitespace(self) -> None:
        """Whitespace-only string defaults to 'auto'."""
        with patch("agentic_devtools.state.get_value", return_value="   "):
            assert get_config_mode() == "auto"

    def test_strips_whitespace(self) -> None:
        """Leading/trailing whitespace is stripped."""
        with patch("agentic_devtools.state.get_value", return_value="  manual  "):
            assert get_config_mode() == "manual"

    def test_returns_invalid_value_as_is(self) -> None:
        """Invalid values are returned as-is (validation is separate)."""
        with patch("agentic_devtools.state.get_value", return_value="invalid"):
            assert get_config_mode() == "invalid"

    def test_non_string_value_returned_as_string(self) -> None:
        """Non-string values are stringified so validate_config_mode() can reject them."""
        with patch("agentic_devtools.state.get_value", return_value=0):
            assert get_config_mode() == "0"

    def test_non_string_bool_returned_as_string(self) -> None:
        """Boolean stored values are stringified rather than silently becoming 'auto'."""
        with patch("agentic_devtools.state.get_value", return_value=False):
            assert get_config_mode() == "False"
