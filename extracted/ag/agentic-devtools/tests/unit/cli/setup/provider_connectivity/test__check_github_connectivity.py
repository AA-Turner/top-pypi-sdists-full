"""Tests for :func:`agentic_devtools.cli.setup.provider_connectivity._check_github_connectivity`."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.provider_connectivity import _check_github_connectivity


class TestCheckGitHubConnectivity:
    """Exercise GitHub provider pre-flight checks."""

    def test_success_when_repo_access_succeeds(self, tmp_path: Path) -> None:
        """GitHub repo probe returning 0 means connectivity is healthy."""
        result = subprocess.CompletedProcess(
            args=["gh", "repo", "view", "owner/repo", "--json", "nameWithOwner"],
            returncode=0,
            stdout='{"nameWithOwner":"owner/repo"}',
        )
        with (
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._resolve_github_repo_slug",
                return_value=("owner/repo", None),
            ),
            patch("agentic_devtools.cli.setup.provider_connectivity.run_safe", return_value=result) as mock_run,
        ):
            assert _check_github_connectivity(tmp_path, timeout=5.0) == (True, None)

        mock_run.assert_called_once_with(
            ["gh", "repo", "view", "owner/repo", "--json", "nameWithOwner"],
            capture_output=True,
            text=True,
            shell=False,
            timeout=5.0,
        )

    def test_missing_repo_config_returns_false(self, tmp_path: Path) -> None:
        """Resolver failures propagate as non-fatal connectivity failures."""
        with patch(
            "agentic_devtools.cli.setup.provider_connectivity._resolve_github_repo_slug",
            return_value=(None, "GitHub repository is not configured"),
        ):
            is_connected, error = _check_github_connectivity(tmp_path, timeout=5.0)

        assert is_connected is False
        assert error == "GitHub repository is not configured"

    def test_missing_gh_cli_returns_false(self, tmp_path: Path) -> None:
        """Missing gh binary is treated as provider-unreachable."""
        with (
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._resolve_github_repo_slug",
                return_value=("owner/repo", None),
            ),
            patch("agentic_devtools.cli.setup.provider_connectivity.run_safe", side_effect=FileNotFoundError),
        ):
            is_connected, error = _check_github_connectivity(tmp_path, timeout=5.0)

        assert is_connected is False
        assert "gh CLI" in (error or "")

    def test_timeout_returns_false(self, tmp_path: Path) -> None:
        """TimeoutExpired on gh repo view is mapped to a non-fatal connection failure."""
        with (
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._resolve_github_repo_slug",
                return_value=("owner/repo", None),
            ),
            patch(
                "agentic_devtools.cli.setup.provider_connectivity.run_safe",
                side_effect=subprocess.TimeoutExpired(
                    cmd=["gh", "repo", "view", "owner/repo", "--json", "nameWithOwner"], timeout=5.0
                ),
            ),
        ):
            is_connected, error = _check_github_connectivity(tmp_path, timeout=5.0)

        assert is_connected is False
        assert "timed out" in (error or "")

    def test_oserror_returns_false(self, tmp_path: Path) -> None:
        """OSError in gh execution is surfaced as provider-unreachable."""
        with (
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._resolve_github_repo_slug",
                return_value=("owner/repo", None),
            ),
            patch("agentic_devtools.cli.setup.provider_connectivity.run_safe", side_effect=OSError("os error")),
        ):
            is_connected, error = _check_github_connectivity(tmp_path, timeout=5.0)

        assert is_connected is False
        assert "os error" in (error or "")

    def test_failed_probe_message_uses_stderr(self, tmp_path: Path) -> None:
        """GitHub repo failures return the CLI stderr output when no stdout text is present."""
        result = subprocess.CompletedProcess(
            args=["gh", "repo", "view", "owner/repo", "--json", "nameWithOwner"],
            returncode=1,
            stderr="not found",
        )
        with (
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._resolve_github_repo_slug",
                return_value=("owner/repo", None),
            ),
            patch("agentic_devtools.cli.setup.provider_connectivity.run_safe", return_value=result),
        ):
            is_connected, error = _check_github_connectivity(tmp_path, timeout=5.0)

        assert is_connected is False
        assert "not found" in (error or "")

    def test_failed_probe_message_uses_exit_code_when_output_is_empty(self, tmp_path: Path) -> None:
        """GitHub failures without output fall back to the exit-code summary."""
        result = subprocess.CompletedProcess(
            args=["gh", "repo", "view", "owner/repo", "--json", "nameWithOwner"],
            returncode=1,
            stderr="",
            stdout="",
        )
        with (
            patch(
                "agentic_devtools.cli.setup.provider_connectivity._resolve_github_repo_slug",
                return_value=("owner/repo", None),
            ),
            patch("agentic_devtools.cli.setup.provider_connectivity.run_safe", return_value=result),
        ):
            is_connected, error = _check_github_connectivity(tmp_path, timeout=5.0)

        assert is_connected is False
        assert "gh repo view owner/repo failed with exit code 1" == error
