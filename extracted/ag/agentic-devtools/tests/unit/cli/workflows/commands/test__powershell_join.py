"""Tests for _powershell_join."""

from agentic_devtools.cli.workflows.commands import _powershell_join


class TestPowershellJoin:
    """Tests for the _powershell_join helper."""

    def test_empty_args_returns_empty_string(self):
        """Test that an empty args list returns an empty string."""
        assert _powershell_join([]) == ""

    def test_single_arg(self):
        """Test formatting of a single argument."""
        result = _powershell_join(["agdt-initiate-update-jira-issue-workflow"])
        assert result == "& 'agdt-initiate-update-jira-issue-workflow'"

    def test_multiple_args(self):
        """Test formatting of multiple arguments."""
        result = _powershell_join(["cmd", "--key", "value"])
        assert result == "& 'cmd' '--key' 'value'"

    def test_arg_with_spaces(self):
        """Test that args with spaces are single-quoted."""
        result = _powershell_join(["cmd", "hello world"])
        assert result == "& 'cmd' 'hello world'"

    def test_arg_with_double_quotes(self):
        """Test that args with double quotes pass through without escaping."""
        result = _powershell_join(["cmd", 'needs "quotes"'])
        assert result == "& 'cmd' 'needs \"quotes\"'"

    def test_arg_with_percent_tokens(self):
        """Test that %VAR% tokens are passed through literally."""
        result = _powershell_join(["cmd", "%TEMP%"])
        assert result == "& 'cmd' '%TEMP%'"

    def test_arg_with_single_quote_is_escaped_by_doubling(self):
        """Test that embedded single quotes are escaped by doubling."""
        result = _powershell_join(["cmd", "it's a test"])
        assert result == "& 'cmd' 'it''s a test'"

    def test_arg_with_multiple_single_quotes(self):
        """Test that multiple single quotes are all escaped."""
        result = _powershell_join(["cmd", "it's don't"])
        assert result == "& 'cmd' 'it''s don''t'"
