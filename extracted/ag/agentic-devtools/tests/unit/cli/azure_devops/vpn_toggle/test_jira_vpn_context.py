"""Tests for JiraVpnContext class."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.vpn_toggle import JiraVpnContext


class TestJiraVpnContextInit:
    """Tests for JiraVpnContext initialization."""

    def test_default_state(self):
        """Verify initial attribute defaults."""
        ctx = JiraVpnContext(vpn_url="https://vpn.example.com")
        assert ctx.vpn_url == "https://vpn.example.com"
        assert ctx.verbose is True
        assert ctx.on_corporate_network is False
        assert ctx.vpn_was_off is False
        assert ctx.connected_vpn is False


class TestJiraVpnContextEnter:
    """Tests for JiraVpnContext __enter__."""

    def test_vpn_url_none(self, capsys):
        """Skips when vpn_url is None."""
        ctx = JiraVpnContext(vpn_url=None, verbose=True)
        result = ctx.__enter__()
        assert result is ctx
        captured = capsys.readouterr()
        assert "VPN URL not configured" in captured.out

    def test_vpn_url_none_not_verbose(self, capsys):
        """Skips silently when vpn_url is None and verbose is False."""
        ctx = JiraVpnContext(vpn_url=None, verbose=False)
        result = ctx.__enter__()
        assert result is ctx
        captured = capsys.readouterr()
        assert captured.out == ""

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_on_corporate_network", return_value=True)
    def test_on_corporate_network(self, _mock, capsys):
        """Sets on_corporate_network when in office."""
        ctx = JiraVpnContext(vpn_url="https://vpn.example.com", verbose=True)
        result = ctx.__enter__()
        assert result is ctx
        assert ctx.on_corporate_network is True
        captured = capsys.readouterr()
        assert "corporate network" in captured.out

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_on_corporate_network", return_value=True)
    def test_on_corporate_network_not_verbose(self, _mock, capsys):
        """Sets on_corporate_network silently when verbose=False."""
        ctx = JiraVpnContext(vpn_url="https://vpn.example.com", verbose=False)
        ctx.__enter__()
        assert ctx.on_corporate_network is True
        captured = capsys.readouterr()
        assert captured.out == ""

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=False)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_on_corporate_network", return_value=False)
    def test_pulse_not_installed(self, _mock_corp, _mock_pulse, capsys):
        """Proceeds without VPN management when Pulse not installed."""
        ctx = JiraVpnContext(vpn_url="https://vpn.example.com", verbose=True)
        result = ctx.__enter__()
        assert result is ctx
        captured = capsys.readouterr()
        assert "not installed" in captured.out

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=False)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_on_corporate_network", return_value=False)
    def test_pulse_not_installed_not_verbose(self, _mock_corp, _mock_pulse, capsys):
        """Skips silently when Pulse not installed and verbose=False."""
        ctx = JiraVpnContext(vpn_url="https://vpn.example.com", verbose=False)
        ctx.__enter__()
        captured = capsys.readouterr()
        assert captured.out == ""

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_vpn_connected", return_value=True)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=True)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_on_corporate_network", return_value=False)
    def test_vpn_already_connected(self, _mock_corp, _mock_pulse, _mock_vpn, capsys):
        """No action when VPN already connected."""
        ctx = JiraVpnContext(vpn_url="https://vpn.example.com", verbose=True)
        ctx.__enter__()
        assert ctx.vpn_was_off is False
        captured = capsys.readouterr()
        assert "already connected" in captured.out

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_vpn_connected", return_value=True)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=True)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_on_corporate_network", return_value=False)
    def test_vpn_already_connected_not_verbose(self, _mock_corp, _mock_pulse, _mock_vpn, capsys):
        """Silent when VPN already connected and verbose=False."""
        ctx = JiraVpnContext(vpn_url="https://vpn.example.com", verbose=False)
        ctx.__enter__()
        captured = capsys.readouterr()
        assert captured.out == ""

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.smart_connect_vpn", return_value=(True, "Connected"))
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_vpn_connected", return_value=False)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=True)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_on_corporate_network", return_value=False)
    def test_connects_vpn_success(self, _corp, _pulse, _vpn, _connect, capsys):
        """Connects VPN when it's off and needed."""
        ctx = JiraVpnContext(vpn_url="https://vpn.example.com", verbose=True)
        ctx.__enter__()
        assert ctx.vpn_was_off is True
        assert ctx.connected_vpn is True
        captured = capsys.readouterr()
        assert "Connected" in captured.out

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.smart_connect_vpn", return_value=(True, "OK"))
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_vpn_connected", return_value=False)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=True)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_on_corporate_network", return_value=False)
    def test_connects_vpn_success_not_verbose(self, _corp, _pulse, _vpn, _connect, capsys):
        """Connects VPN silently when verbose=False."""
        ctx = JiraVpnContext(vpn_url="https://vpn.example.com", verbose=False)
        ctx.__enter__()
        assert ctx.connected_vpn is True
        captured = capsys.readouterr()
        assert captured.out == ""

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.smart_connect_vpn", return_value=(False, "Timeout"))
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_vpn_connected", return_value=False)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=True)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_on_corporate_network", return_value=False)
    def test_connects_vpn_failure(self, _corp, _pulse, _vpn, _connect, capsys):
        """Handles VPN connect failure gracefully."""
        ctx = JiraVpnContext(vpn_url="https://vpn.example.com", verbose=True)
        ctx.__enter__()
        assert ctx.vpn_was_off is True
        assert ctx.connected_vpn is False
        captured = capsys.readouterr()
        assert "Timeout" in captured.out

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.smart_connect_vpn", return_value=(False, "Err"))
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_vpn_connected", return_value=False)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_pulse_secure_installed", return_value=True)
    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.is_on_corporate_network", return_value=False)
    def test_connects_vpn_failure_not_verbose(self, _corp, _pulse, _vpn, _connect, capsys):
        """Silent on failure when verbose=False."""
        ctx = JiraVpnContext(vpn_url="https://vpn.example.com", verbose=False)
        ctx.__enter__()
        assert ctx.connected_vpn is False
        captured = capsys.readouterr()
        assert captured.out == ""


class TestJiraVpnContextExit:
    """Tests for JiraVpnContext __exit__."""

    def test_on_corporate_network(self):
        """No VPN action when on corporate network."""
        ctx = JiraVpnContext(vpn_url="https://vpn.example.com")
        ctx.on_corporate_network = True
        result = ctx.__exit__(None, None, None)
        assert result is False

    def test_not_connected_vpn(self):
        """No action when VPN wasn't connected by context."""
        ctx = JiraVpnContext(vpn_url="https://vpn.example.com")
        ctx.connected_vpn = False
        ctx.vpn_was_off = True
        result = ctx.__exit__(None, None, None)
        assert result is False

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.disconnect_vpn", return_value=(True, "Suspended"))
    def test_suspends_vpn_on_exit(self, _mock_disconnect, capsys):
        """Suspends VPN on exit when it was connected by context."""
        ctx = JiraVpnContext(vpn_url="https://vpn.example.com", verbose=True)
        ctx.connected_vpn = True
        ctx.vpn_was_off = True
        result = ctx.__exit__(None, None, None)
        assert result is False
        captured = capsys.readouterr()
        assert "Suspended" in captured.out

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.disconnect_vpn", return_value=(True, "Done"))
    def test_suspends_vpn_on_exit_not_verbose(self, _mock_disconnect, capsys):
        """Suspends VPN silently when verbose=False."""
        ctx = JiraVpnContext(vpn_url="https://vpn.example.com", verbose=False)
        ctx.connected_vpn = True
        ctx.vpn_was_off = True
        ctx.__exit__(None, None, None)
        captured = capsys.readouterr()
        assert captured.out == ""
