"""Tests for _format_degraded_setup_message."""

import shlex
from unittest.mock import patch

from agentic_devtools.cli.workflows import commands
from agentic_devtools.cli.workflows.commands import _format_degraded_setup_message


class TestFormatDegradedSetupMessage:
    """Tests for _format_degraded_setup_message helper function."""

    def test_includes_issue_key(self):
        """Test that the message includes the issue key."""
        result = _format_degraded_setup_message(
            "PROJECT-1234",
            ["agdt-initiate-update-jira-issue-workflow", "--issue-key", "PROJECT-1234"],
        )
        assert "PROJECT-1234" in result

    def test_includes_manual_command(self):
        """Test that the message includes the shell-joined manual command."""
        # Pin the platform so the POSIX space-joined form is asserted
        # deterministically regardless of host OS (matches the pattern used by
        # test_uses_posix_command_quoting_on_non_windows). Without this, the
        # test fails on Windows, where the command is PowerShell single-quoted.
        with patch.object(commands.sys, "platform", "linux"):
            result = _format_degraded_setup_message(
                "PROJECT-1234",
                ["agdt-initiate-update-jira-issue-workflow", "--issue-key", "PROJECT-1234"],
            )
        assert "agdt-initiate-update-jira-issue-workflow --issue-key PROJECT-1234" in result

    def test_includes_failure_notice(self):
        """Test that the message includes a failure notice."""
        result = _format_degraded_setup_message(
            "PROJECT-5678",
            ["agdt-initiate-create-jira-issue-workflow", "--issue-key", "PROJECT-5678"],
        )
        assert "Auto-setup failed" in result
        assert "could not be started automatically" in result
        assert "The issue was created" not in result

    def test_includes_visual_separator(self):
        """Test that the message includes visual separators."""
        result = _format_degraded_setup_message(
            "PROJECT-1234",
            ["agdt-initiate-update-jira-issue-workflow", "--issue-key", "PROJECT-1234"],
        )
        assert "=" * 80 in result

    def test_returns_string(self):
        """Test that the function returns a string."""
        result = _format_degraded_setup_message(
            "PROJECT-999",
            ["agdt-initiate-update-jira-issue-workflow", "--issue-key", "PROJECT-999"],
        )
        assert isinstance(result, str)

    def test_handles_command_with_spaces_in_args(self):
        """Test that arguments with spaces are properly shell-quoted."""
        result = _format_degraded_setup_message(
            "PROJECT-1234",
            ["agdt-initiate-update-jira-issue-workflow", "--user-request", "I need a story to cover this"],
        )
        assert "I need a story to cover this" in result

    def test_includes_manual_instructions(self):
        """Test that the message includes instructions to run manually."""
        result = _format_degraded_setup_message(
            "PROJECT-1234",
            ["agdt-initiate-update-jira-issue-workflow", "--issue-key", "PROJECT-1234"],
        )
        assert "manually" in result.lower()

    def test_different_issue_keys_produce_different_messages(self):
        """Test that different issue keys produce different messages."""
        cmd1 = ["agdt-initiate-update-jira-issue-workflow", "--issue-key", "PROJECT-1111"]
        cmd2 = ["agdt-initiate-update-jira-issue-workflow", "--issue-key", "PROJECT-2222"]
        msg1 = _format_degraded_setup_message("PROJECT-1111", cmd1)
        msg2 = _format_degraded_setup_message("PROJECT-2222", cmd2)
        assert msg1 != msg2
        assert "PROJECT-1111" in msg1
        assert "PROJECT-2222" in msg2

    def test_uses_windows_command_quoting_on_win32(self):
        """Test that Windows uses PowerShell single-quote quoting and note."""
        manual_command = [
            "agdt-initiate-update-jira-issue-workflow",
            "--user-request",
            'needs "quotes" and spaces',
            "--token",
            "%TEMP%",
        ]

        with patch.object(commands.sys, "platform", "win32"):
            result = _format_degraded_setup_message("PROJECT-1234", manual_command)

        # Must use PowerShell single-quote quoting (& 'cmd' 'arg' ...) so the
        # copy-paste command is actually safe in PowerShell.  list2cmdline is
        # NOT PowerShell-safe when args contain double quotes.
        assert "& 'agdt-initiate-update-jira-issue-workflow'" in result
        assert "'needs \"quotes\" and spaces'" in result
        assert "PowerShell" in result
        assert "Git Bash" not in result
        assert "cmd.exe" not in result

    def test_uses_posix_command_quoting_on_non_windows(self):
        """Test that non-Windows platforms use POSIX shell quoting and no shell note."""
        manual_command = [
            "agdt-initiate-update-jira-issue-workflow",
            "--user-request",
            'needs "quotes" and spaces',
        ]

        with patch.object(commands.sys, "platform", "linux"):
            result = _format_degraded_setup_message("PROJECT-1234", manual_command)

        assert shlex.join(manual_command) in result
        assert "PowerShell" not in result

    def test_windows_escapes_single_quotes_in_args(self):
        """Test that embedded single quotes in args are escaped by doubling on Windows."""
        manual_command = [
            "agdt-initiate-update-jira-issue-workflow",
            "--user-request",
            "it's a test",
        ]

        with patch.object(commands.sys, "platform", "win32"):
            result = _format_degraded_setup_message("PROJECT-1234", manual_command)

        # Embedded single quote is escaped by doubling: it's → it''s
        expected_cmd = "& 'agdt-initiate-update-jira-issue-workflow' '--user-request' 'it''s a test'"
        assert expected_cmd in result
