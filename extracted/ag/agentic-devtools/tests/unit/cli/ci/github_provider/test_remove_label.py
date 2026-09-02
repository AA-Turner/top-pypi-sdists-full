"""Tests for GitHubActionsProvider.remove_label() method."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _mock_run_safe_response(data=""):
    class _Result:
        returncode = 0
        stdout = json.dumps(data) if isinstance(data, (dict, list)) else data
        stderr = ""

    return _Result()


def _mock_run_safe_error(stderr_text):
    class _Result:
        returncode = 1
        stdout = ""
        stderr = stderr_text

    return _Result()


class TestRemoveLabel:
    """Tests for GitHubActionsProvider.remove_label()."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_removes_label(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response()

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.remove_label(pr_number=42, label="audit-in-progress")

        mock_run_safe.assert_called_once()
        args = mock_run_safe.call_args[0][0]
        assert "--method" in args
        method_idx = args.index("--method") + 1
        assert args[method_idx] == "DELETE"

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_swallows_404_error(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_error("404 Not Found")

        provider = GitHubActionsProvider(repo="owner/repo")
        # Should not raise
        provider.remove_label(pr_number=42, label="nonexistent")

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_non_404_errors(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_error("422 Validation Failed")

        provider = GitHubActionsProvider(repo="owner/repo")
        with pytest.raises(RuntimeError, match="422"):
            provider.remove_label(pr_number=42, label="audited")
