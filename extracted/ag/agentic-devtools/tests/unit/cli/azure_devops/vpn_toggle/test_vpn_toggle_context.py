"""Tests for VpnToggleContext class."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.vpn_toggle import VpnToggleContext


class TestVpnToggleContextInit:
    """Tests for VpnToggleContext initialization."""

    def test_default_state(self):
        """Verify initial attribute defaults."""
        ctx = VpnToggleContext(auto_toggle=True, vpn_url="https://vpn.example.com")
        assert ctx.auto_toggle is True
        assert ctx.vpn_url == "https://vpn.example.com"
        assert ctx.verbose is True
        assert ctx.was_connected is False
        assert ctx.disconnected is False


class TestVpnToggleContextEnter:
    """Tests for VpnToggleContext __enter__."""

    def test_auto_toggle_disabled(self):
        """No-op when auto_toggle is False."""
        ctx = VpnToggleContext(auto_toggle=False, vpn_url="https://vpn.example.com")
        result = ctx.__enter__()
        assert result is ctx
        assert ctx.disconnected is False

    def test_vpn_url_none(self, capsys):
        """Skips when vpn_url is None."""
        ctx = VpnToggleContext(auto_toggle=True, vpn_url=None, verbose=True)
        result = ctx.__enter__()
        assert result is ctx
        captured = capsys.readouterr()
        assert "VPN URL not configured" in captured.out

    def test_vpn_url_none_not_verbose(self, capsys):
        """Skips silently when vpn_url is None and verbose is False."""
        ctx = VpnToggleContext(auto_toggle=True, vpn_url=None, verbose=False)
        result = ctx.__enter__()
        assert result is ctx
        captured = capsys.readouterr()
        assert captured.out == ""

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=False)
    def test_pulse_not_installed(self, _mock, capsys):
        """Skips when Pulse Secure is not installed."""
        ctx = VpnToggleContext(auto_toggle=True, vpn_url="https://vpn.example.com", verbose=True)
        result = ctx.__enter__()
        assert result is ctx
        captured = capsys.readouterr()
        assert "not installed" in captured.out

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=False)
    def test_pulse_not_installed_not_verbose(self, _mock, capsys):
        """Skips silently when Pulse not installed and verbose=False."""
        ctx = VpnToggleContext(auto_toggle=True, vpn_url="https://vpn.example.com", verbose=False)
        result = ctx.__enter__()
        assert result is ctx
        captured = capsys.readouterr()
        assert captured.out == ""

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_vpn_connected", return_value=False)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=True)
    def test_vpn_not_connected(self, _mock_pulse, _mock_vpn):
        """No action when VPN is not connected."""
        ctx = VpnToggleContext(auto_toggle=True, vpn_url="https://vpn.example.com")
        ctx.__enter__()
        assert ctx.was_connected is False
        assert ctx.disconnected is False

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.disconnect_vpn", return_value=(True, "Disconnected"))
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_vpn_connected", return_value=True)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=True)
    def test_vpn_connected_disconnect_success(self, _mock_pulse, _mock_vpn, _mock_disconnect):
        """Disconnects when VPN is connected."""
        ctx = VpnToggleContext(auto_toggle=True, vpn_url="https://vpn.example.com", verbose=False)
        ctx.__enter__()
        assert ctx.was_connected is True
        assert ctx.disconnected is True

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.disconnect_vpn", return_value=(False, "Failed"))
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_vpn_connected", return_value=True)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=True)
    def test_vpn_connected_disconnect_failure(self, _mock_pulse, _mock_vpn, _mock_disconnect):
        """Handles disconnect failure gracefully."""
        ctx = VpnToggleContext(auto_toggle=True, vpn_url="https://vpn.example.com", verbose=False)
        ctx.__enter__()
        assert ctx.was_connected is True
        assert ctx.disconnected is False


class TestVpnToggleContextExit:
    """Tests for VpnToggleContext __exit__."""

    def test_auto_toggle_disabled(self):
        """No-op on exit when auto_toggle is False."""
        ctx = VpnToggleContext(auto_toggle=False, vpn_url="https://vpn.example.com")
        result = ctx.__exit__(None, None, None)
        assert result is False

    def test_not_disconnected(self):
        """No reconnect when never disconnected."""
        ctx = VpnToggleContext(auto_toggle=True, vpn_url="https://vpn.example.com")
        ctx.disconnected = False
        result = ctx.__exit__(None, None, None)
        assert result is False

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.reconnect_vpn", return_value=(True, "Connected"))
    def test_reconnects_on_exit(self, _mock_reconnect):
        """Reconnects VPN on exit when it was disconnected."""
        ctx = VpnToggleContext(auto_toggle=True, vpn_url="https://vpn.example.com", verbose=False)
        ctx.disconnected = True
        result = ctx.__exit__(None, None, None)
        assert result is False
        _mock_reconnect.assert_called_once_with("https://vpn.example.com")
