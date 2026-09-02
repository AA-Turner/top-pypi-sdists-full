"""Tests for GitHubActionsProvider.post_issue_comment()."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import _MAX_COMMENT_BODY_CHARS, GitHubActionsProvider


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
        assert mock_api.call_args.kwargs["body"] == {"body": "verdict"}

    def test_raises_when_the_response_carries_no_id(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value=json.dumps({})):
            with pytest.raises(RuntimeError, match="response carried no comment ID"):
                provider.post_issue_comment(1240, "verdict")

    def test_raises_when_body_exceeds_size_limit(self) -> None:
        """An oversized body raises ValueError rather than posting a truncated audit record."""
        provider = GitHubActionsProvider(repo="o/r")
        oversized = "x" * (_MAX_COMMENT_BODY_CHARS + 1)
        with pytest.raises(ValueError, match="exceeds the.*-character limit"):
            provider.post_issue_comment(1240, oversized)

    def test_body_at_exact_limit_is_accepted(self) -> None:
        """A body equal to the limit is posted without error."""
        provider = GitHubActionsProvider(repo="o/r")
        at_limit = "x" * _MAX_COMMENT_BODY_CHARS
        with patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            return_value=json.dumps({"id": 1}),
        ):
            assert provider.post_issue_comment(1240, at_limit) == 1
