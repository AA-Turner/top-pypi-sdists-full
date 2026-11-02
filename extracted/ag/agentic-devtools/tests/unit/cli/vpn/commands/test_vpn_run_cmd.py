"""Tests for vpn_run_cmd function."""

import shlex
import subprocess
import sys
from unittest.mock import patch

import pytest

from agentic_devtools.cli.vpn.commands import vpn_run_cmd
from agentic_devtools.cli.vpn.runner import VpnRequirement


class TestVpnRunCmd:
    """Tests for vpn_run_cmd function."""

    def test_function_exists(self):
        """Verify vpn_run_cmd is importable and callable."""
        assert callable(vpn_run_cmd)

    def test_default_smart_requirement(self):
        """Test that no explicit requirement defaults to SMART."""
        with patch(
            "agentic_devtools.cli.vpn.commands.run_with_vpn_context",
            return_value=(0, "", ""),
        ) as mock_run:
            with patch("sys.argv", ["agdt-vpn-run", "echo", "hello"]):
                with pytest.raises(SystemExit) as exc_info:
                    vpn_run_cmd()
                assert exc_info.value.code == 0

        mock_run.assert_called_once_with("echo hello", VpnRequirement.SMART)

    def test_require_vpn_flag(self):
        """Test --require-vpn sets VPN requirement."""
        with patch(
            "agentic_devtools.cli.vpn.commands.run_with_vpn_context",
            return_value=(0, "", ""),
        ) as mock_run:
            with patch("sys.argv", ["agdt-vpn-run", "--require-vpn", "curl", "https://internal"]):
                with pytest.raises(SystemExit) as exc_info:
                    vpn_run_cmd()
                assert exc_info.value.code == 0

        mock_run.assert_called_once_with("curl https://internal", VpnRequirement.REQUIRE_VPN)

    def test_require_public_flag(self):
        """Test --require-public sets public requirement."""
        with patch(
            "agentic_devtools.cli.vpn.commands.run_with_vpn_context",
            return_value=(0, "", ""),
        ) as mock_run:
            with patch("sys.argv", ["agdt-vpn-run", "--require-public", "npm", "install"]):
                with pytest.raises(SystemExit) as exc_info:
                    vpn_run_cmd()
                assert exc_info.value.code == 0

        mock_run.assert_called_once_with("npm install", VpnRequirement.REQUIRE_PUBLIC)

    def test_smart_flag(self):
        """Test --smart explicitly sets SMART requirement."""
        with patch(
            "agentic_devtools.cli.vpn.commands.run_with_vpn_context",
            return_value=(0, "", ""),
        ) as mock_run:
            with patch("sys.argv", ["agdt-vpn-run", "--smart", "some", "command"]):
                with pytest.raises(SystemExit) as exc_info:
                    vpn_run_cmd()
                assert exc_info.value.code == 0

        mock_run.assert_called_once_with("some command", VpnRequirement.SMART)

    def test_nonzero_exit_code_propagated(self):
        """Test that non-zero return code from command is propagated."""
        with patch(
            "agentic_devtools.cli.vpn.commands.run_with_vpn_context",
            return_value=(42, "", "error"),
        ):
            with patch("sys.argv", ["agdt-vpn-run", "failing-command"]):
                with pytest.raises(SystemExit) as exc_info:
                    vpn_run_cmd()
                assert exc_info.value.code == 42

    def test_command_args_shell_joined_preserving_spaces(self):
        """Test that command args are shell-joined without losing spaced arguments."""

        command_parts = ["echo", "a b"]

        with patch(
            "agentic_devtools.cli.vpn.commands.run_with_vpn_context",
            return_value=(0, "", ""),
        ) as mock_run:
            with patch("sys.argv", ["agdt-vpn-run", *command_parts]):
                with pytest.raises(SystemExit) as exc_info:
                    vpn_run_cmd()
                assert exc_info.value.code == 0
                mock_run.assert_called_once_with(
                    shlex.join(command_parts),
                    VpnRequirement.SMART,
                )

    def test_command_args_use_windows_quoting_on_win32(self):
        """Test that Windows command reconstruction uses cmd.exe-compatible quoting."""
        command_parts = ["echo", "a b"]

        with patch(
            "agentic_devtools.cli.vpn.commands.run_with_vpn_context",
            return_value=(0, "", ""),
        ) as mock_run:
            with patch.object(sys, "platform", "win32"):
                with patch("sys.argv", ["agdt-vpn-run", *command_parts]):
                    with pytest.raises(SystemExit) as exc_info:
                        vpn_run_cmd()
                    assert exc_info.value.code == 0
                    mock_run.assert_called_once_with(
                        subprocess.list2cmdline(command_parts),
                        VpnRequirement.SMART,
                    )
