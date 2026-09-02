"""Tests for recovery-command argument quoting."""

from unittest.mock import patch

from agentic_devtools.cli.workflows.worktree_setup import _quote_recovery_argument


class TestQuoteRecoveryArgument:
    """Tests for _quote_recovery_argument."""

    def test_quotes_windows_arguments_and_doubles_apostrophes(self):
        """Windows recovery arguments use PowerShell single-quote escaping."""
        with patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Windows"):
            result = _quote_recovery_argument("model with 'quote'")

        assert result == "'model with ''quote'''"

    def test_quotes_posix_arguments_with_shell_quote(self):
        """POSIX recovery arguments use shlex quoting."""
        with patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Linux"):
            result = _quote_recovery_argument("model with spaces")

        assert result == "'model with spaces'"

    def test_normalizes_line_separators(self):
        """Recovery arguments remain single-line when input contains line breaks."""
        with patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Windows"):
            result = _quote_recovery_argument("model\r\nwith\nlines")

        assert result == "'model with lines'"
