"""Tests for ensure_jira_vpn_access decorator."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.vpn_toggle import ensure_jira_vpn_access


class TestEnsureJiraVpnAccess:
    """Tests for ensure_jira_vpn_access function."""

    def test_function_exists(self):
        """Verify ensure_jira_vpn_access is importable and callable."""
        assert callable(ensure_jira_vpn_access)

    def test_decorated_function_is_callable(self):
        """Decorated functions should remain callable."""

        @ensure_jira_vpn_access
        def my_jira_func():
            return "result"

        assert callable(my_jira_func)

    @patch("agentic_devtools.cli.azure_devops.vpn_toggle.get_vpn_url_from_state", return_value=None)
    def test_decorated_function_executes_with_vpn_context(self, _mock_url, temp_state_dir):
        """Decorated function executes inside JiraVpnContext and returns result."""

        @ensure_jira_vpn_access
        def my_jira_func(x, y=10):
            return x + y

        result = my_jira_func(5, y=20)
        assert result == 25
