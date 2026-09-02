"""Tests for config_mode_cmd()."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.config.opt_in_mode import config_mode_cmd


class TestConfigModeCmd:
    """Tests for config_mode_cmd CLI entry point."""

    def test_displays_current_mode_when_no_args(self, capsys) -> None:
        """Prints the current config_mode when called without arguments."""
        with (
            patch("sys.argv", ["agdt-config-mode"]),
            patch("agentic_devtools.cli.config.opt_in_mode.get_config_mode", return_value="auto"),
        ):
            config_mode_cmd()

        captured = capsys.readouterr()
        assert "config_mode: auto" in captured.out

    def test_displays_manual_mode(self, capsys) -> None:
        """Prints 'manual' when that is the current config_mode."""
        with (
            patch("sys.argv", ["agdt-config-mode"]),
            patch("agentic_devtools.cli.config.opt_in_mode.get_config_mode", return_value="manual"),
        ):
            config_mode_cmd()

        captured = capsys.readouterr()
        assert "config_mode: manual" in captured.out

    def test_sets_valid_mode(self, capsys) -> None:
        """Sets config_mode when a valid value is provided."""
        with (
            patch("sys.argv", ["agdt-config-mode", "manual"]),
            patch("agentic_devtools.state.set_value") as mock_set,
        ):
            config_mode_cmd()

        mock_set.assert_called_once_with("config_mode", "manual")
        captured = capsys.readouterr()
        assert "config_mode set to: manual" in captured.out

    def test_sets_auto_mode(self, capsys) -> None:
        """Sets config_mode to 'auto' when specified."""
        with (
            patch("sys.argv", ["agdt-config-mode", "auto"]),
            patch("agentic_devtools.state.set_value") as mock_set,
        ):
            config_mode_cmd()

        mock_set.assert_called_once_with("config_mode", "auto")
        captured = capsys.readouterr()
        assert "config_mode set to: auto" in captured.out

    def test_rejects_invalid_mode(self, capsys) -> None:
        """Exits with error when an invalid mode is provided."""
        with (
            patch("sys.argv", ["agdt-config-mode", "bogus"]),
            pytest.raises(SystemExit, match="1"),
        ):
            config_mode_cmd()

        captured = capsys.readouterr()
        assert "Invalid config_mode" in captured.err
        assert "'bogus'" in captured.err

    def test_strips_whitespace_from_mode_arg(self, capsys) -> None:
        """Whitespace around mode arg is stripped before validation and storage."""
        with (
            patch("sys.argv", ["agdt-config-mode", " manual "]),
            patch("agentic_devtools.state.set_value") as mock_set,
        ):
            config_mode_cmd()

        mock_set.assert_called_once_with("config_mode", "manual")
        captured = capsys.readouterr()
        assert "config_mode set to: manual" in captured.out

    def test_whitespace_padded_invalid_mode_rejected(self, capsys) -> None:
        """Whitespace-padded invalid mode is rejected after stripping."""
        with (
            patch("sys.argv", ["agdt-config-mode", " bogus "]),
            pytest.raises(SystemExit, match="1"),
        ):
            config_mode_cmd()

        captured = capsys.readouterr()
        assert "Invalid config_mode" in captured.err
        assert "'bogus'" in captured.err
