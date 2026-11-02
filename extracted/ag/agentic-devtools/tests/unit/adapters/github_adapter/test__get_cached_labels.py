"""Tests for GitHubIssuesAdapter._get_cached_labels."""

from __future__ import annotations

import subprocess
import time
from unittest.mock import MagicMock

import pytest

from agentic_devtools.adapters.github_adapter import GitHubIssuesAdapter


def _mock_run(stdout: str = "", stderr: str = "", returncode: int = 0) -> MagicMock:
    """Build a mock run_command callable returning a CompletedProcess."""
    mock = MagicMock()
    mock.return_value = subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr=stderr)
    return mock


class TestGetCachedLabels:
    """Tests for the _get_cached_labels helper."""

    def test_returns_none_when_unpopulated(self) -> None:
        """Returns None when labels have not been fetched."""
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=_mock_run())
        assert adapter._get_cached_labels() is None

    def test_returns_cached_value(self) -> None:
        """Returns stored value after cache is populated."""
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=_mock_run())
        adapter._labels_cache = ["bug", "feature"]
        assert adapter._get_cached_labels() == ["bug", "feature"]

    def test_fetch_failure_leaves_cache_unpopulated(self) -> None:
        """_fetch_labels raising leaves _labels_cache as None."""
        run = MagicMock()
        run.return_value = subprocess.CompletedProcess(
            args=[], returncode=1, stdout="", stderr="HTTP 500 Internal Server Error"
        )
        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=run)
        deadline = time.monotonic() + 30.0
        with pytest.raises(RuntimeError):
            adapter._fetch_labels(deadline)
        assert adapter._labels_cache is None
