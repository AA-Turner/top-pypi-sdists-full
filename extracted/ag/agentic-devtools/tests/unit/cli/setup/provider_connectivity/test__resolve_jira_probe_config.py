"""Tests for :func:`agentic_devtools.cli.setup.provider_connectivity._resolve_jira_probe_config`."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.setup.provider_connectivity import _resolve_jira_probe_config


class TestResolveJiraProbeConfig:
    """Ensure Jira probe config uses the same shared adapter resolver as the Jira adapter."""

    def test_returns_url_headers_and_ssl_from_shared_resolver(self) -> None:
        """Probe config is assembled from the shared resolve_jira_config() path."""
        git_root = Path("/tmp/repo")
        mock_config = MagicMock()
        mock_config.base_url = "https://jira.example.com"
        mock_config.headers = {"Authorization": "******", "Content-Type": "application/json"}
        mock_config.ssl_verify = "/tmp/ca.pem"

        with patch("agentic_devtools.adapters.resolve_jira_config", return_value=mock_config) as mock_resolve:
            base_url, headers, ssl_verify = _resolve_jira_probe_config(git_root)

        assert base_url == "https://jira.example.com"
        assert ssl_verify == "/tmp/ca.pem"
        assert headers == {
            "Authorization": "******",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        mock_resolve.assert_called_once_with(git_root)

    def test_accept_header_is_added_when_absent(self) -> None:
        """Accept header is injected even when not present in the adapter config headers."""
        git_root = Path("/tmp/repo")
        mock_config = MagicMock()
        mock_config.base_url = "https://jira.example.com"
        mock_config.headers = {"Content-Type": "application/json"}
        mock_config.ssl_verify = True

        with patch("agentic_devtools.adapters.resolve_jira_config", return_value=mock_config):
            _, headers, _ = _resolve_jira_probe_config(git_root)

        assert headers.get("Accept") == "application/json"
