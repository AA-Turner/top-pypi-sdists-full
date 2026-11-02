"""Tests for GitHubActionsProvider.dispatch_agent_retry."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.github_provider import _MAX_COMMENT_BODY_CHARS, GitHubActionsProvider
from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError


def test_retry_comment_starts_with_at_copilot_and_keeps_marker_in_same_comment() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    provider._post_comment_as_pr_token_once = MagicMock(return_value=123)  # type: ignore[method-assign]
    prompt = (
        "retry context <!-- agdt:agent-retry:task-1:2 -->\n\n@copilot continue task\n\nMore context mentions @copilot."
    )
    assert provider.dispatch_agent_retry(5, prompt, "task-1") == 123
    posted = provider._post_comment_as_pr_token_once.call_args.args[1]
    assert posted.startswith("@copilot\n\n<!-- agdt:agent-retry:task-1:2 -->")
    assert posted.count("@copilot") == 1
    assert "More context" in posted


def test_retry_comment_keeps_failure_alias_in_the_same_comment() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    provider._post_comment_as_pr_token_once = MagicMock(return_value=123)  # type: ignore[method-assign]
    prompt = (
        "<!-- agdt:agent-retry:task-1:2 -->\n"
        "<!-- agdt:agent-retry-alias:42 -->\n"
        "<!-- agdt:agent-retry-identity:task:task-1 -->\n"
        "<!-- agdt:agent-retry-identity:event:42 -->\n"
        "\n@copilot continue task"
    )

    provider.dispatch_agent_retry(5, prompt, "task-1")

    posted = provider._post_comment_as_pr_token_once.call_args.args[1]
    assert posted.startswith("@copilot\n\n<!-- agdt:agent-retry:task-1:2 -->")
    assert posted.splitlines()[3] == "<!-- agdt:agent-retry-alias:42 -->"
    assert posted.splitlines()[4] == "<!-- agdt:agent-retry-identity:task:task-1 -->"
    assert posted.splitlines()[5] == "<!-- agdt:agent-retry-identity:event:42 -->"
    assert "<!-- agdt:agent-retry-alias:42 -->" in posted


def test_retry_dispatch_does_not_promote_or_remove_quoted_retry_markers() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    provider._post_comment_as_pr_token_once = MagicMock(return_value=123)  # type: ignore[method-assign]
    prompt = (
        "<!-- agdt:agent-retry:task-1:2 -->\n"
        "\n@copilot continue task\n\n"
        "## Previous repair task context\n\n"
        "```text\n"
        "<!-- agdt:agent-retry-alias:99 -->\n"
        "<!-- agdt:agent-retry:99:1 -->\n"
        "```"
    )

    provider.dispatch_agent_retry(5, prompt, "task-1")
    posted = provider._post_comment_as_pr_token_once.call_args.args[1]
    _, _, metadata_and_context = posted.partition("\n\n")
    metadata, _, context = metadata_and_context.partition("\n\n")
    assert metadata == "<!-- agdt:agent-retry:task-1:2 -->"
    assert "<!-- agdt:agent-retry-alias:99 -->" in context
    assert "<!-- agdt:agent-retry:99:1 -->" in context


def test_retry_requires_failure_marker() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    with pytest.raises(ValueError, match="missing its failure marker"):
        provider.dispatch_agent_retry(5, "@copilot retry", "task-1")


def test_retry_body_is_capped_without_truncating_marker() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    provider._post_comment_as_pr_token_once = MagicMock(return_value=123)  # type: ignore[method-assign]
    prompt = "<!-- agdt:agent-retry:task-1:1 -->\n\n" + ("context " * _MAX_COMMENT_BODY_CHARS)
    provider.dispatch_agent_retry(5, prompt, "task-1")
    posted = provider._post_comment_as_pr_token_once.call_args.args[1]
    assert len(posted) <= _MAX_COMMENT_BODY_CHARS
    assert posted.startswith("@copilot\n\n<!-- agdt:agent-retry:task-1:1 -->")
    assert posted.count("@copilot") == 1


def test_retry_body_truncates_if_comment_size_helper_exceeds_limit() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    provider._post_comment_as_pr_token_once = MagicMock(return_value=123)  # type: ignore[method-assign]
    prompt = "<!-- agdt:agent-retry:task-1:1 -->\n\nretry context"
    with patch(
        "agentic_devtools.cli.ci.github_provider._enforce_comment_size_limit",
        return_value="x" * (_MAX_COMMENT_BODY_CHARS + 1),
    ):
        provider.dispatch_agent_retry(5, prompt, "task-1")
    posted = provider._post_comment_as_pr_token_once.call_args.args[1]
    assert len(posted) <= _MAX_COMMENT_BODY_CHARS
    assert posted.startswith("@copilot\n\n<!-- agdt:agent-retry:task-1:1 -->")
    assert posted.endswith("[Retry context truncated to fit GitHub's comment limit.]")


def test_retry_body_preserves_previous_repair_findings_before_large_linked_issue_context() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    provider._post_comment_as_pr_token_once = MagicMock(return_value=123)  # type: ignore[method-assign]
    repair_context = (
        "## Previous repair task context\n\n"
        "The exact finding is in this fenced section:\n\n"
        "```text\n"
        "Critical repair finding\n" + ("repair detail " * 2_000) + "\n```\n\n"
    )
    prompt = (
        "<!-- agdt:agent-retry:task-1:1 -->\n\n@copilot Resume the task.\n\n"
        + repair_context
        + "## Linked issue #42\n\n"
        + ("Long refined specification. " * 2_000)
    )

    provider.dispatch_agent_retry(5, prompt, "task-1")

    posted = provider._post_comment_as_pr_token_once.call_args.args[1]
    assert len(posted) <= _MAX_COMMENT_BODY_CHARS
    assert "Critical repair finding" in posted


def test_retry_dispatch_reconciles_an_accepted_comment_after_timeout() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    provider._post_comment_as_pr_token_once = MagicMock(side_effect=RetryableError("request timed out"))  # type: ignore[method-assign]
    provider.get_dispatch_login = MagicMock(return_value="workflow-bot")  # type: ignore[method-assign]
    provider.list_issue_comments = MagicMock(  # type: ignore[method-assign]
        return_value=[IssueCommentInfo(456, "workflow-bot", "@copilot\n\n<!-- agdt:agent-retry:task-1:2 -->")]
    )
    prompt = "<!-- agdt:agent-retry:task-1:2 -->\n\n@copilot resume"

    assert provider.dispatch_agent_retry(5, prompt, "task-1") == 456
    provider._post_comment_as_pr_token_once.assert_called_once()


@pytest.mark.parametrize(
    "comments",
    [
        [],
        [IssueCommentInfo(456, "untrusted-user", "<!-- agdt:agent-retry:task-1:2 -->")],
    ],
    ids=["marker-not-found", "marker-from-untrusted-author"],
)
def test_retry_dispatch_does_not_resend_when_acceptance_cannot_be_verified(
    comments: list[IssueCommentInfo],
) -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    provider._post_comment_as_pr_token_once = MagicMock(side_effect=RetryableError("request timed out"))  # type: ignore[method-assign]
    provider.get_dispatch_login = MagicMock(return_value="workflow-bot")  # type: ignore[method-assign]
    provider.list_issue_comments = MagicMock(return_value=comments)  # type: ignore[method-assign]
    prompt = "<!-- agdt:agent-retry:task-1:2 -->\n\n@copilot resume"

    with pytest.raises(RetryableError, match="timed out"):
        provider.dispatch_agent_retry(5, prompt, "task-1")

    provider._post_comment_as_pr_token_once.assert_called_once()


def test_retry_dispatch_propagates_rate_limit_without_reconciliation() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    provider._post_comment_as_pr_token_once = MagicMock(  # type: ignore[method-assign]
        side_effect=RetryableError(
            "rate limited",
            retry_after=45,
            reset_timestamp=1_700_000_000,
            remaining=0,
            provider="github",
            credential_identity="workflow-token",
            source="response",
            is_rate_limit=True,
        )
    )
    provider.get_dispatch_login = MagicMock(return_value="workflow-bot")  # type: ignore[method-assign]
    provider.list_issue_comments = MagicMock()  # type: ignore[method-assign]
    prompt = "<!-- agdt:agent-retry:task-1:2 -->\n\n@copilot resume"

    with pytest.raises(ProviderRateLimitError) as exc_info:
        provider.dispatch_agent_retry(5, prompt, "task-1")

    assert exc_info.value.retry_after_seconds == 45
    assert exc_info.value.reset_timestamp == 1_700_000_000
    assert exc_info.value.remaining == 0
    assert exc_info.value.provider == "github"
    assert exc_info.value.credential_identity == "workflow-token"
    assert exc_info.value.source == "response"
    provider.get_dispatch_login.assert_not_called()
    provider.list_issue_comments.assert_not_called()


def test_retry_dispatch_does_not_reconcile_a_marker_quoted_in_findings() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    provider._post_comment_as_pr_token_once = MagicMock(  # type: ignore[method-assign]
        side_effect=RetryableError("request timed out")
    )
    provider.get_dispatch_login = MagicMock(return_value="workflow-bot")  # type: ignore[method-assign]
    provider.list_issue_comments = MagicMock(  # type: ignore[method-assign]
        return_value=[
            IssueCommentInfo(
                456,
                "workflow-bot",
                "A prior finding quotes this marker:\n\n```text\n<!-- agdt:agent-retry:task-1:2 -->\n```",
            )
        ]
    )

    with pytest.raises(RetryableError, match="timed out"):
        provider.dispatch_agent_retry(5, "<!-- agdt:agent-retry:task-1:2 -->\n\n@copilot resume", "task-1")

    provider._post_comment_as_pr_token_once.assert_called_once()


def test_retry_dispatch_does_not_resend_when_reconciliation_fails() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    provider._post_comment_as_pr_token_once = MagicMock(side_effect=RetryableError("request timed out"))  # type: ignore[method-assign]
    provider.get_dispatch_login = MagicMock(return_value="workflow-bot")  # type: ignore[method-assign]
    provider.list_issue_comments = MagicMock(side_effect=RuntimeError("comments unavailable"))  # type: ignore[method-assign]
    prompt = "<!-- agdt:agent-retry:task-1:2 -->\n\n@copilot resume"

    with pytest.raises(RetryableError, match="Could not verify"):
        provider.dispatch_agent_retry(5, prompt, "task-1")

    provider._post_comment_as_pr_token_once.assert_called_once()


def test_retry_dispatch_propagates_reconciliation_rate_limit() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    provider._post_comment_as_pr_token_once = MagicMock(side_effect=RetryableError("request timed out"))  # type: ignore[method-assign]
    provider.get_dispatch_login = MagicMock(return_value="workflow-bot")  # type: ignore[method-assign]
    provider.list_issue_comments = MagicMock(  # type: ignore[method-assign]
        side_effect=ProviderRateLimitError(provider="github", is_rate_limit=True)
    )
    prompt = "<!-- agdt:agent-retry:task-1:2 -->\n\n@copilot resume"

    with pytest.raises(ProviderRateLimitError):
        provider.dispatch_agent_retry(5, prompt, "task-1")


def test_public_dispatch_rejects_initial_delivery_marker_without_posting() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    prompt = "<!-- agdt:initial-delivery-retry:original:1 -->\n\nResume initial delivery"
    with patch.object(provider, "_post_comment_as_pr_token_once") as post:
        with pytest.raises(ValueError, match="missing its failure marker"):
            provider.dispatch_agent_retry(5, prompt, "original")
    post.assert_not_called()
