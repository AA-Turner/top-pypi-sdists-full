"""Tests for GitHubIssuesAdapter._exec timeout parameter."""

from __future__ import annotations

import subprocess
from unittest.mock import MagicMock

import pytest

from agentic_devtools.adapters.github_adapter import GitHubIssuesAdapter


def _mock_run(stdout: str = "", stderr: str = "", returncode: int = 0) -> MagicMock:
    """Build a mock run_command callable returning a CompletedProcess."""
    mock = MagicMock()
    mock.return_value = subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr=stderr)
    return mock


class TestExec:
    """Tests for _exec timeout handling."""

    def test_timeout_forwarded_to_run(self) -> None:
        """Timeout parameter is forwarded to the run command."""
        run = _mock_run(stdout="ok")
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)
        adapter._exec(["gh", "api", "test"], timeout=5.0)
        _, kwargs = run.call_args
        assert kwargs["timeout"] == 5.0

    def test_timeout_expired_raises_runtime_error(self) -> None:
        """TimeoutExpired from subprocess raises RuntimeError with actual timeout from exception."""
        run = MagicMock()
        run.side_effect = subprocess.TimeoutExpired(cmd="gh", timeout=3.0)
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)
        with pytest.raises(RuntimeError, match="3.0s"):
            adapter._exec(["gh", "api", "test"], timeout=3.0)

    def test_timeout_expired_uses_exc_timeout_not_param(self) -> None:
        """TimeoutExpired uses exc.timeout (not local param) so None param still gives a readable message."""
        run = MagicMock()
        run.side_effect = subprocess.TimeoutExpired(cmd="gh", timeout=5.0)
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)
        with pytest.raises(RuntimeError, match="5.0s"):
            adapter._exec(["gh", "api", "test"], timeout=None)

    def test_non_positive_timeout_raises_runtime_error(self) -> None:
        """Non-positive timeout raises RuntimeError before calling run."""
        run = _mock_run()
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)
        with pytest.raises(RuntimeError, match="positive"):
            adapter._exec(["gh", "api", "test"], timeout=0.0)
        run.assert_not_called()

    def test_negative_timeout_raises_runtime_error(self) -> None:
        """Negative timeout raises RuntimeError before calling run."""
        run = _mock_run()
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)
        with pytest.raises(RuntimeError, match="positive"):
            adapter._exec(["gh", "api", "test"], timeout=-1.0)
        run.assert_not_called()

    def test_none_timeout_does_not_forward(self) -> None:
        """None timeout is not forwarded to the run command."""
        run = _mock_run(stdout="ok")
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)
        adapter._exec(["gh", "api", "test"], timeout=None)
        _, kwargs = run.call_args
        assert "timeout" not in kwargs
