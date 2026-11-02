"""Tests for GitHubActionsProvider.add_label() method."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _mock_run_safe_response(data, *, returncode=0, stderr=""):
    class _Result:
        pass

    result = _Result()
    result.returncode = returncode
    result.stdout = json.dumps(data) if isinstance(data, (dict, list)) else data
    result.stderr = stderr
    return result


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

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_creates_missing_label_then_retries_attach(self, mock_run_safe) -> None:
        mock_run_safe.side_effect = [
            _mock_run_safe_response("", returncode=1, stderr="HTTP 404: Not Found (label does not exist)"),
            _mock_run_safe_response([{"name": "ai-pr-loop:agent-failed"}]),
            _mock_run_safe_response([{"name": "ai-pr-loop:agent-failed"}]),
        ]

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.add_label(pr_number=1, label="ai-pr-loop:agent-failed")

        assert mock_run_safe.call_count == 3
        create_args = mock_run_safe.call_args_list[1][0][0]
        assert "/repos/owner/repo/labels" in create_args
        create_method_idx = create_args.index("--method") + 1
        assert create_args[create_method_idx] == "POST"
        attach_args = mock_run_safe.call_args_list[2][0][0]
        assert "/repos/owner/repo/issues/1/labels" in attach_args

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_tolerates_concurrent_label_creation(self, mock_run_safe) -> None:
        mock_run_safe.side_effect = [
            _mock_run_safe_response("", returncode=1, stderr="HTTP 404: Not Found (label does not exist)"),
            _mock_run_safe_response("", returncode=1, stderr="HTTP 422: Unprocessable (already_exists)"),
            _mock_run_safe_response([{"name": "ai-pr-loop:agent-failed"}]),
        ]

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.add_label(pr_number=1, label="ai-pr-loop:agent-failed")

        assert mock_run_safe.call_count == 3

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_reraises_non_404_attach_error(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response(
            "", returncode=1, stderr="HTTP 403: Forbidden (insufficient scope)"
        )

        provider = GitHubActionsProvider(repo="owner/repo")
        with pytest.raises(RuntimeError, match="403"):
            provider.add_label(pr_number=1, label="audited")

        mock_run_safe.assert_called_once()

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_reraises_non_422_create_label_error(self, mock_run_safe) -> None:
        mock_run_safe.side_effect = [
            _mock_run_safe_response("", returncode=1, stderr="HTTP 404: Not Found (label does not exist)"),
            _mock_run_safe_response("", returncode=1, stderr="HTTP 403: Forbidden (insufficient scope)"),
        ]

        provider = GitHubActionsProvider(repo="owner/repo")
        with pytest.raises(RuntimeError, match="403"):
            provider.add_label(pr_number=1, label="audited")

        assert mock_run_safe.call_count == 2
