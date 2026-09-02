"""Tests for :func:`agentic_devtools.cli.setup.provider_connectivity._check_jira_connectivity`."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.provider_connectivity import _check_jira_connectivity


class TestCheckJiraConnectivity:
    """Exercise Jira provider pre-flight checks."""

    def test_success_on_http_200(self, tmp_path: Path) -> None:
        """Jira returns 200 → connectivity is reported as healthy."""
        with (
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._resolve_jira_probe_config",
                return_value=(
                    "https://jira.example.com",
                    {"Authorization": "******", "Content-Type": "application/json", "Accept": "application/json"},
                    True,
                ),
            ),
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._run_jira_probe_with_deadline",
                return_value=(200, "{}", None),
            ) as mock_probe,
        ):
            assert _check_jira_connectivity(tmp_path, timeout=5.0) == (True, None)

        mock_probe.assert_called_once_with(
            "https://jira.example.com/rest/api/2/myself",
            {"Authorization": "******", "Content-Type": "application/json", "Accept": "application/json"},
            timeout=5.0,
            verify=True,
        )

    def test_timeout_returns_false(self, tmp_path: Path) -> None:
        """Jira timeout → connectivity is reported as failed."""
        with (
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._resolve_jira_probe_config",
                return_value=(
                    "https://jira.example.com",
                    {"Authorization": "******", "Content-Type": "application/json", "Accept": "application/json"},
                    False,
                ),
            ),
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._run_jira_probe_with_deadline",
                return_value=(None, None, "Jira connectivity check timed out after 5.0s"),
            ),
        ):
            is_connected, error = _check_jira_connectivity(tmp_path, timeout=5.0)

        assert is_connected is False
        assert "timed out" in (error or "")

    def test_missing_base_url_returns_false(self, tmp_path: Path) -> None:
        """No Jira base URL configured → connectivity is treated as failed."""
        with patch(
            "agentic_devtools.cli.setup.provider_connectivity._resolve_jira_probe_config",
            return_value=("", {"Content-Type": "application/json", "Accept": "application/json"}, True),
        ):
            is_connected, error = _check_jira_connectivity(tmp_path, timeout=5.0)

        assert is_connected is False
        assert "Invalid Jira base URL" in (error or "")

    def test_invalid_base_url_returns_false(self, tmp_path: Path) -> None:
        """Malformatted Jira URL is rejected before any HTTP attempt."""
        with patch(
            "agentic_devtools.cli.setup.provider_connectivity._resolve_jira_probe_config",
            return_value=(
                "not-a-valid-url",
                {"Authorization": "******", "Content-Type": "application/json", "Accept": "application/json"},
                True,
            ),
        ):
            is_connected, error = _check_jira_connectivity(tmp_path, timeout=5.0)

        assert is_connected is False
        assert "Invalid Jira base URL" in (error or "")

    def test_request_exception_returns_false(self, tmp_path: Path) -> None:
        """Jira request exceptions are surfaced as non-fatal connection failures."""
        with (
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._resolve_jira_probe_config",
                return_value=(
                    "https://jira.example.com",
                    {"Authorization": "******", "Content-Type": "application/json", "Accept": "application/json"},
                    "/etc/custom.pem",
                ),
            ),
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._run_jira_probe_with_deadline",
                return_value=(None, None, "Jira connectivity check failed: offline"),
            ),
        ):
            is_connected, error = _check_jira_connectivity(tmp_path, timeout=5.0)

        assert is_connected is False
        assert "offline" in (error or "")

    def test_http_500_returns_false(self, tmp_path: Path) -> None:
        """Unexpected Jira HTTP status codes are reported clearly with the response details."""
        with (
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._resolve_jira_probe_config",
                return_value=(
                    "https://jira.example.com",
                    {"Authorization": "******", "Content-Type": "application/json", "Accept": "application/json"},
                    True,
                ),
            ),
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._run_jira_probe_with_deadline",
                return_value=(500, "server error", None),
            ),
        ):
            is_connected, error = _check_jira_connectivity(tmp_path, timeout=5.0)

        assert is_connected is False
        assert "500" in (error or "")
        assert "server error" in (error or "")

    def test_auth_error_returns_false(self, tmp_path: Path) -> None:
        """Jira 401/403 response → auth failure is surfaced distinctly."""
        with (
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._resolve_jira_probe_config",
                return_value=(
                    "https://jira.example.com",
                    {"Authorization": "******", "Content-Type": "application/json", "Accept": "application/json"},
                    True,
                ),
            ),
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._run_jira_probe_with_deadline",
                return_value=(401, "Unauthorized", None),
            ),
        ):
            is_connected, error = _check_jira_connectivity(tmp_path, timeout=5.0)

        assert is_connected is False
        assert "401" in (error or "")

    def test_redirect_response_returns_false(self, tmp_path: Path) -> None:
        """Redirect responses are rejected so SSO/login redirects cannot be treated as healthy auth."""
        with (
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._resolve_jira_probe_config",
                return_value=(
                    "https://jira.example.com",
                    {"Authorization": "******", "Content-Type": "application/json", "Accept": "application/json"},
                    True,
                ),
            ),
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._run_jira_probe_with_deadline",
                return_value=(302, "<html>login</html>", None),
            ),
        ):
            is_connected, error = _check_jira_connectivity(tmp_path, timeout=5.0)

        assert is_connected is False
        assert "302" in (error or "")
