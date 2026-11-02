"""Tests for _validate_github_auth."""

from __future__ import annotations

import subprocess

import pytest

from agentic_devtools.adapters.factory import _validate_github_auth
from agentic_devtools.epic_tree.errors import ConfigError


class TestValidateGithubAuth:
    """Verify GitHub CLI auth status validation."""

    def test_gh_auth_status_success(self, monkeypatch):
        """No error when gh auth status returns 0."""
        monkeypatch.setattr(
            "agentic_devtools.adapters.factory.run_safe",
            lambda *args, **kwargs: subprocess.CompletedProcess(
                args=["gh", "auth", "status"], returncode=0, stdout="", stderr=""
            ),
        )
        _validate_github_auth()  # Should not raise

    def test_gh_auth_status_failure(self, monkeypatch):
        """Non-zero exit raises ConfigError with exit code, output, and auth login hint."""
        monkeypatch.setattr(
            "agentic_devtools.adapters.factory.run_safe",
            lambda *args, **kwargs: subprocess.CompletedProcess(
                args=["gh", "auth", "status"], returncode=1, stdout="", stderr="not logged in"
            ),
        )
        with pytest.raises(ConfigError) as exc_info:
            _validate_github_auth()
        msg = str(exc_info.value)
        assert "gh auth login" in msg
        assert "exit code 1" in msg
        assert "not logged in" in msg

    def test_gh_auth_status_failure_no_output(self, monkeypatch):
        """Non-zero exit with empty stdout/stderr includes only exit code in detail."""
        monkeypatch.setattr(
            "agentic_devtools.adapters.factory.run_safe",
            lambda *args, **kwargs: subprocess.CompletedProcess(
                args=["gh", "auth", "status"], returncode=2, stdout="", stderr=""
            ),
        )
        with pytest.raises(ConfigError) as exc_info:
            _validate_github_auth()
        msg = str(exc_info.value)
        assert "exit code 2" in msg
        assert "gh auth login" in msg

    def test_gh_not_installed(self, monkeypatch):
        """FileNotFoundError raises ConfigError with install hint."""

        def _raise_fnf(*args, **kwargs):
            raise FileNotFoundError("gh not found")

        monkeypatch.setattr("agentic_devtools.adapters.factory.run_safe", _raise_fnf)
        with pytest.raises(ConfigError) as exc_info:
            _validate_github_auth()
        assert "Install the GitHub CLI" in str(exc_info.value)

    def test_gh_auth_timeout(self, monkeypatch):
        """TimeoutExpired raises ConfigError with timeout hint."""

        def _raise_timeout(*args, **kwargs):
            raise subprocess.TimeoutExpired(cmd="gh", timeout=10)

        monkeypatch.setattr("agentic_devtools.adapters.factory.run_safe", _raise_timeout)
        with pytest.raises(ConfigError) as exc_info:
            _validate_github_auth()
        assert "timed out" in str(exc_info.value)
