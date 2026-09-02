"""Tests for agentic_devtools.cli.azure_devops.helpers._escape_for_cmd."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.azure_devops.helpers import _escape_for_cmd


class TestEscapeForCmd:
    """Tests for the helpers._escape_for_cmd function."""

    def test_doubles_percent_signs_on_windows(self):
        """Percent signs are doubled to prevent cmd.exe variable expansion on Windows."""
        with patch("agentic_devtools.cli.azure_devops.helpers.sys") as mock_sys:
            mock_sys.platform = "win32"
            assert _escape_for_cmd("feat(%ISSUE%): title") == "feat(%%ISSUE%%): title"

    def test_no_op_on_non_windows(self):
        """Value is returned unchanged on non-Windows platforms."""
        with patch("agentic_devtools.cli.azure_devops.helpers.sys") as mock_sys:
            mock_sys.platform = "linux"
            assert _escape_for_cmd("feat(%ISSUE%): title") == "feat(%ISSUE%): title"

    def test_plain_text_unchanged_on_windows(self):
        """Values without percent signs are unchanged even on Windows."""
        with patch("agentic_devtools.cli.azure_devops.helpers.sys") as mock_sys:
            mock_sys.platform = "win32"
            assert _escape_for_cmd("normal text") == "normal text"

    def test_empty_string(self):
        """Empty string returns empty string on all platforms."""
        with patch("agentic_devtools.cli.azure_devops.helpers.sys") as mock_sys:
            mock_sys.platform = "win32"
            assert _escape_for_cmd("") == ""

    @pytest.mark.parametrize("platform", ["linux", "darwin"])
    def test_no_op_on_posix_platforms(self, platform: str):
        """No-op on both Linux and macOS."""
        with patch("agentic_devtools.cli.azure_devops.helpers.sys") as mock_sys:
            mock_sys.platform = platform
            assert _escape_for_cmd("%A% and %B%") == "%A% and %B%"

    def test_escapes_shell_operators_on_windows(self):
        """Shell operators &, |, <, > are caret-escaped on Windows."""
        with patch("agentic_devtools.cli.azure_devops.helpers.sys") as mock_sys:
            mock_sys.platform = "win32"
            assert _escape_for_cmd("a&b|c<d>e") == "a^&b^|c^<d^>e"

    def test_escapes_caret_on_windows(self):
        """Caret is doubled on Windows to prevent cmd.exe interpretation."""
        with patch("agentic_devtools.cli.azure_devops.helpers.sys") as mock_sys:
            mock_sys.platform = "win32"
            assert _escape_for_cmd("a^b") == "a^^b"

    def test_escapes_double_quote_on_windows(self):
        """Double quote is caret-escaped on Windows."""
        with patch("agentic_devtools.cli.azure_devops.helpers.sys") as mock_sys:
            mock_sys.platform = "win32"
            assert _escape_for_cmd('say "hello"') == 'say ^"hello^"'
