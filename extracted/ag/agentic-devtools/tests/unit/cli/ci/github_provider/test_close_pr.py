"""Tests for GitHubActionsProvider.close_pr()."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.retry import RetryableError


class TestClosePr:
    """Tests for the pull-request close used when reaping a no-change PR."""

    def test_patches_the_pull_request_state(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="{}") as mock_api:
            provider.close_pr(12)

        assert mock_api.call_args.args[0].endswith("/pulls/12")
        assert mock_api.call_args.kwargs["method"] == "PATCH"
        assert mock_api.call_args.kwargs["body"] == {"state": "closed"}

    def test_posts_the_optional_comment_before_closing(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with (
            patch.object(GitHubActionsProvider, "post_issue_comment") as mock_comment,
            patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="{}"),
        ):
            provider.close_pr(12, comment="closing")

        mock_comment.assert_called_once_with(12, "closing")

    def test_skips_an_empty_comment(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with (
            patch.object(GitHubActionsProvider, "post_issue_comment") as mock_comment,
            patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="{}"),
        ):
            provider.close_pr(12, comment="")

        mock_comment.assert_not_called()

    def test_a_transient_close_failure_does_not_repost_the_comment(self) -> None:
        """The comment carries its own retry, so retrying the close must not duplicate it."""
        provider = GitHubActionsProvider(repo="o/r")
        with (
            patch.object(GitHubActionsProvider, "post_issue_comment") as mock_comment,
            patch("agentic_devtools.cli.ci.retry.time.sleep"),
            patch(
                "agentic_devtools.cli.ci.github_provider._gh_api",
                side_effect=[RetryableError("rate limit"), "{}"],
            ) as mock_api,
        ):
            provider.close_pr(12, comment="closing")

        mock_comment.assert_called_once_with(12, "closing")
        assert mock_api.call_count == 2
