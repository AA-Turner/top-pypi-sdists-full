"""Tests for _run_pulse_command function."""

import subprocess
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.vpn_toggle import _run_pulse_command


class TestRunPulseCommand:
    """Tests for _run_pulse_command internal function."""

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=False)
    def test_pulse_not_installed(self, _mock_installed):
        """Returns error when Pulse Secure is not installed."""
        success, msg, code = _run_pulse_command(["-suspend"])
        assert success is False
        assert "not installed" in msg
        assert code == -1

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=True)
    @patch("subprocess.run")
    def test_successful_command(self, mock_run, _mock_installed):
        """Returns success when command exits with code 0."""
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="Connected", stderr="")
        success, msg, code = _run_pulse_command(["-resume", "-url", "https://vpn.example.com"])
        assert success is True
        assert msg == "Connected"
        assert code == 0

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=True)
    @patch("subprocess.run")
    def test_timeout(self, mock_run, _mock_installed):
        """Returns error on timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="pulse", timeout=30)
        success, msg, code = _run_pulse_command(["-suspend"], timeout=30)
        assert success is False
        assert "timed out" in msg
        assert code == -1

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=True)
    @patch("subprocess.run")
    def test_generic_exception(self, mock_run, _mock_installed):
        """Returns error on unexpected exception."""
        mock_run.side_effect = OSError("Permission denied")
        success, msg, code = _run_pulse_command(["-suspend"])
        assert success is False
        assert "Permission denied" in msg
        assert code == -1
