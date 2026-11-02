"""Tests for GitHubActionsProvider.delete_review_comments stub."""

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


class TestDeleteReviewComments:
    """The GitHub provider stub always raises NotImplementedError."""

    def test_raises_not_implemented(self) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")
        with pytest.raises(NotImplementedError, match="delete_review_comments"):
            provider.delete_review_comments(1)

    def test_error_message_is_actionable(self) -> None:
        provider = GitHubActionsProvider()
        with pytest.raises(NotImplementedError) as exc_info:
            provider.delete_review_comments(1, execute=True, author_substring="bot")
        message = str(exc_info.value)
        assert "Azure DevOps" in message
        assert "agdt-delete-pr-review-comments" in message
