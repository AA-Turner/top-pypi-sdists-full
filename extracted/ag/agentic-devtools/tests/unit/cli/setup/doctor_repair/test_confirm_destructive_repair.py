"""Tests for confirm_destructive_repair."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup.doctor_repair import (
    UserDeclinedRepairError,
    confirm_destructive_repair,
)


class TestConfirmDestructiveRepair:
    """Tests for confirm_destructive_repair function."""

    def test_non_interactive_raises(self, capsys: pytest.CaptureFixture[str]) -> None:
        artifacts = [Path("/site-packages/~gentic-devtools")]
        with patch.object(sys.stdin, "isatty", return_value=False):
            with pytest.raises(UserDeclinedRepairError, match="Non-interactive"):
                confirm_destructive_repair(artifacts)
        captured = capsys.readouterr()
        assert "DESTRUCTIVE REPAIR" in captured.err
        assert "~gentic-devtools" in captured.err

    def test_user_declines_with_n(self, capsys: pytest.CaptureFixture[str]) -> None:
        artifacts = [Path("/site-packages/~gentic-devtools")]
        with patch.object(sys.stdin, "isatty", return_value=True):
            with patch("builtins.input", return_value="n"):
                with pytest.raises(UserDeclinedRepairError, match="User declined"):
                    confirm_destructive_repair(artifacts)

    def test_user_declines_with_empty(self, capsys: pytest.CaptureFixture[str]) -> None:
        artifacts = [Path("/site-packages/~gentic-devtools")]
        with patch.object(sys.stdin, "isatty", return_value=True):
            with patch("builtins.input", return_value=""):
                with pytest.raises(UserDeclinedRepairError, match="User declined"):
                    confirm_destructive_repair(artifacts)

    def test_user_accepts_with_y(self, capsys: pytest.CaptureFixture[str]) -> None:
        artifacts = [Path("/site-packages/~gentic-devtools")]
        with patch.object(sys.stdin, "isatty", return_value=True):
            with patch("builtins.input", return_value="y"):
                confirm_destructive_repair(artifacts)  # Should not raise

    def test_user_accepts_with_yes(self, capsys: pytest.CaptureFixture[str]) -> None:
        artifacts = [Path("/site-packages/~gentic-devtools")]
        with patch.object(sys.stdin, "isatty", return_value=True):
            with patch("builtins.input", return_value="yes"):
                confirm_destructive_repair(artifacts)  # Should not raise

    def test_grouped_output(self, capsys: pytest.CaptureFixture[str]) -> None:
        artifacts = [
            Path("/lib/python3.10/site-packages/~gentic-devtools"),
            Path("/lib/python3.10/site-packages/bad.dist-info"),
            Path("/other/site-packages/~gentic_devtools"),
        ]
        with patch.object(sys.stdin, "isatty", return_value=True):
            with patch("builtins.input", return_value="y"):
                confirm_destructive_repair(artifacts)
        captured = capsys.readouterr()
        assert "/lib/python3.10/site-packages/" in captured.err
        assert "/other/site-packages/" in captured.err
        assert "~gentic-devtools" in captured.err
        assert "bad.dist-info" in captured.err

    def test_eof_error_treated_as_decline(self) -> None:
        artifacts = [Path("/site-packages/foo")]
        with patch.object(sys.stdin, "isatty", return_value=True):
            with patch("builtins.input", side_effect=EOFError):
                with pytest.raises(UserDeclinedRepairError, match="User declined"):
                    confirm_destructive_repair(artifacts)

    @patch("sys.platform", "linux")
    def test_platform_pinned_linux(self, capsys: pytest.CaptureFixture[str]) -> None:
        artifacts = [Path("/site-packages/~gentic-devtools")]
        with patch.object(sys.stdin, "isatty", return_value=False):
            with pytest.raises(UserDeclinedRepairError):
                confirm_destructive_repair(artifacts)

    @patch("sys.platform", "win32")
    def test_platform_pinned_windows(self, capsys: pytest.CaptureFixture[str]) -> None:
        artifacts = [Path("C:\\Python\\site-packages\\~gentic-devtools")]
        with patch.object(sys.stdin, "isatty", return_value=False):
            with pytest.raises(UserDeclinedRepairError):
                confirm_destructive_repair(artifacts)

    def test_multiple_site_packages_single_prompt(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Multiple site-packages directories shown in a single grouped prompt."""
        artifacts = [
            Path("/sp1/~gentic-devtools"),
            Path("/sp2/bad.dist-info"),
        ]
        with patch.object(sys.stdin, "isatty", return_value=True):
            with patch("builtins.input", return_value="y") as mock_input:
                confirm_destructive_repair(artifacts)
        # Only one input call (single prompt).
        mock_input.assert_called_once()
        captured = capsys.readouterr()
        assert "/sp1/" in captured.err
        assert "/sp2/" in captured.err
