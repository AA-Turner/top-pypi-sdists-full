"""Tests for GitHubActionsProvider post-comment helpers."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _mock_run_safe_response(data):
    class _Result:
        returncode = 0
        stdout = json.dumps(data)
        stderr = ""

    return _Result()


class TestPostComment:
    """Tests for GitHubActionsProvider comment posting methods."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_comment_id(self, mock_run_safe, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        mock_run_safe.return_value = _mock_run_safe_response({"id": 12345, "body": "hello"})

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.post_comment(42, "hello")

        assert result == 12345

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_sends_body_in_request(self, mock_run_safe, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        mock_run_safe.return_value = _mock_run_safe_response({"id": 1})

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.post_comment(1, "test body")

        kwargs = mock_run_safe.call_args[1]
        assert kwargs.get("input") is not None
        body = json.loads(kwargs["input"])
        assert body == {"body": "test body\n\n🤖 AI PR Loop ·"}

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    @patch("agentic_devtools.cli.ci.github_provider.require_ai_pr_loop_bookkeeping_token")
    def test_actions_post_uses_verified_bookkeeping_role(self, require_token, gh_api, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        require_token.return_value = "bot-token"
        gh_api.return_value = json.dumps({"id": 9})
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", lambda: "github-actions[bot]")

        result = provider.post_comment(42, "tracking state")

        assert result == 9
        assert gh_api.call_args.kwargs["token"] == "bot-token"
        assert gh_api.call_args.kwargs["credential_identity"] == "AI_PR_LOOP_BOOKKEEPING_TOKEN"
        assert gh_api.call_args.kwargs["body"] == {"body": "tracking state\n\n🤖 AI PR Loop ·"}

    @patch("agentic_devtools.cli.ci.github_provider.require_ai_pr_loop_bookkeeping_token", return_value="bot-token")
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_actions_post_rejects_unverified_bookkeeping_identity(self, gh_api, _require_token, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", lambda: "")

        with pytest.raises(RuntimeError, match="identity could not be verified"):
            provider.post_comment(42, "tracking state")

        gh_api.assert_not_called()
