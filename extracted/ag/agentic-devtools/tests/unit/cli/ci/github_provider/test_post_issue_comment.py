"""Tests for GitHubActionsProvider.post_issue_comment()."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import _MAX_COMMENT_BODY_CHARS, GitHubActionsProvider
from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.retry import RetryableError


class TestPostIssueComment:
    """Tests for the issue-comment write used when reaping a no-change PR."""

    def test_returns_the_created_comment_id(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            return_value=json.dumps({"id": 999}),
        ) as mock_api:
            assert provider.post_issue_comment(1240, "verdict") == 999

        assert mock_api.call_args.args[0].endswith("/issues/1240/comments")
        assert mock_api.call_args.kwargs["method"] == "POST"
        assert mock_api.call_args.kwargs["body"] == {"body": "verdict\n\n🤖 AI PR Loop ·"}

    def test_bookkeeping_issue_comment_uses_verified_bot_identity(self, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        provider = GitHubActionsProvider(repo="o/r")
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", lambda: "github-actions[bot]")
        with (
            patch(
                "agentic_devtools.cli.ci.github_provider.require_ai_pr_loop_bookkeeping_token",
                return_value="bot-token",
            ),
            patch(
                "agentic_devtools.cli.ci.github_provider._gh_api",
                return_value=json.dumps({"id": 999}),
            ) as mock_api,
            patch.object(provider, "list_issue_comments", return_value=[]),
        ):
            assert provider.post_issue_comment_as_bookkeeping_token(1240, "verdict") == 999

        assert mock_api.call_args.kwargs["token"] == "bot-token"
        assert mock_api.call_args.kwargs["credential_identity"] == "AI_PR_LOOP_BOOKKEEPING_TOKEN"
        assert mock_api.call_args.kwargs["body"] == {"body": "verdict\n\n🤖 AI PR Loop ·"}

    def test_bookkeeping_issue_comment_retry_reuses_accepted_comment(self, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        provider = GitHubActionsProvider(repo="o/r")
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", lambda: "github-actions[bot]")
        comments: list[IssueCommentInfo] = []

        def post_comment(endpoint, *, method="GET", body=None, **_kwargs):
            assert endpoint.endswith("/issues/1240/comments")
            assert method == "POST"
            assert body is not None
            comments.append(IssueCommentInfo(id=100, author="github-actions[bot]", body=body["body"]))
            if len(comments) == 1:
                raise RetryableError("GitHub API server error (HTTP 502)")
            return json.dumps({"id": 101})

        with (
            patch.object(
                provider,
                "list_issue_comments",
                side_effect=lambda _issue: list(comments),
            ) as list_comments,
            patch(
                "agentic_devtools.cli.ci.github_provider.require_ai_pr_loop_bookkeeping_token",
                return_value="bot-token",
            ),
            patch(
                "agentic_devtools.cli.ci.github_provider._gh_api",
                side_effect=post_comment,
            ) as mock_api,
            patch("agentic_devtools.cli.ci.retry.time.sleep"),
        ):
            assert provider.post_issue_comment_as_bookkeeping_token(1240, "verdict") == 100

        assert list_comments.call_count == 2
        mock_api.assert_called_once()

    def test_bookkeeping_issue_comment_scans_past_nonmatching_copy(self, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        provider = GitHubActionsProvider(repo="o/r")
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", lambda: "github-actions[bot]")
        with (
            patch(
                "agentic_devtools.cli.ci.github_provider.require_ai_pr_loop_bookkeeping_token",
                return_value="bot-token",
            ),
            patch(
                "agentic_devtools.cli.ci.github_provider._gh_api",
            ) as mock_api,
            patch.object(
                provider,
                "list_issue_comments",
                return_value=[
                    IssueCommentInfo(100, "github-actions[bot]", "older state\n\n🤖 AI PR Loop ·"),
                    IssueCommentInfo(101, "github-actions[bot]", "verdict\n\n🤖 AI PR Loop ·"),
                ],
            ),
        ):
            assert provider.post_issue_comment_as_bookkeeping_token(1240, "verdict") == 101

        mock_api.assert_not_called()

    def test_bookkeeping_issue_comment_rejects_unexpected_verified_identity(self, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        provider = GitHubActionsProvider(repo="o/r")
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", lambda: "unexpected[bot]")
        with (
            patch(
                "agentic_devtools.cli.ci.github_provider.require_ai_pr_loop_bookkeeping_token",
                return_value="bot-token",
            ),
            patch("agentic_devtools.cli.ci.github_provider._gh_api") as mock_api,
            pytest.raises(RuntimeError, match="github-actions\\[bot\\]"),
        ):
            provider.post_issue_comment_as_bookkeeping_token(1240, "verdict")
        mock_api.assert_not_called()

    def test_raises_when_the_response_carries_no_id(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=json.dumps({})):
            with pytest.raises(RuntimeError, match="response carried no comment ID"):
                provider.post_issue_comment(1240, "verdict")

    def test_raises_when_body_exceeds_size_limit(self) -> None:
        """An oversized body raises ValueError rather than posting a truncated audit record."""
        provider = GitHubActionsProvider(repo="o/r")
        oversized = "x" * (_MAX_COMMENT_BODY_CHARS - len("\n\n🤖 AI PR Loop ·") + 1)
        with pytest.raises(ValueError, match="exceeds the.*-character limit"):
            provider.post_issue_comment(1240, oversized)

    def test_body_at_exact_limit_is_accepted(self) -> None:
        """A body equal to the limit is posted without error."""
        provider = GitHubActionsProvider(repo="o/r")
        at_limit = "x" * (_MAX_COMMENT_BODY_CHARS - len("\n\n🤖 AI PR Loop ·"))
        with patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            return_value=json.dumps({"id": 1}),
        ):
            assert provider.post_issue_comment(1240, at_limit) == 1

    def test_bookkeeping_issue_comment_uses_default_writer_outside_actions(self, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        provider = GitHubActionsProvider(repo="o/r")
        with patch.object(provider, "post_issue_comment", return_value=999) as post_comment:
            assert provider.post_issue_comment_as_bookkeeping_token(1240, "verdict") == 999

        post_comment.assert_called_once_with(1240, "verdict")

    def test_bookkeeping_issue_comment_rejects_oversized_body(self, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        provider = GitHubActionsProvider(repo="o/r")
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", lambda: "github-actions[bot]")
        oversized = "x" * (_MAX_COMMENT_BODY_CHARS - len("\n\n🤖 AI PR Loop ·") + 1)

        with (
            patch(
                "agentic_devtools.cli.ci.github_provider.require_ai_pr_loop_bookkeeping_token",
                return_value="bot-token",
            ),
            pytest.raises(ValueError, match="exceeds the.*-character limit"),
        ):
            provider.post_issue_comment_as_bookkeeping_token(1240, oversized)

    def test_bookkeeping_issue_comment_requires_response_id(self, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        provider = GitHubActionsProvider(repo="o/r")
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", lambda: "github-actions[bot]")

        with (
            patch(
                "agentic_devtools.cli.ci.github_provider.require_ai_pr_loop_bookkeeping_token",
                return_value="bot-token",
            ),
            patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=json.dumps({})),
            patch.object(provider, "list_issue_comments", return_value=[]),
            pytest.raises(RuntimeError, match="response carried no comment ID"),
        ):
            provider.post_issue_comment_as_bookkeeping_token(1240, "verdict")
