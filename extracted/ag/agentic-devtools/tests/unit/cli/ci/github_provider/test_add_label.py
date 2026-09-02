"""Tests for GitHubActionsProvider.add_label() method."""

import json
from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _mock_run_safe_response(data):
    class _Result:
        returncode = 0
        stdout = json.dumps(data) if isinstance(data, (dict, list)) else data
        stderr = ""

    return _Result()


class TestAddLabel:
    """Tests for GitHubActionsProvider.add_label()."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_adds_label(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response([{"name": "audited"}])

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.add_label(pr_number=42, label="audited")

        mock_run_safe.assert_called_once()
        kwargs = mock_run_safe.call_args[1]
        body = json.loads(kwargs["input"])
        assert body == {"labels": ["audited"]}

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_sends_post_method(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response([])

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.add_label(pr_number=1, label="test")

        args = mock_run_safe.call_args[0][0]
        assert "--method" in args
        method_idx = args.index("--method") + 1
        assert args[method_idx] == "POST"
