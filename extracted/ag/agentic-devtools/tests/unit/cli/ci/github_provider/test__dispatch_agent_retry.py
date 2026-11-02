"""Internal initial-delivery dispatch preserves its separate marker and uncertainty fence."""

from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.guards import get_agent_retry_markers
from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.retry import RetryableError


def test_initial_delivery_dispatch_is_not_a_failed_session_budget_marker() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    prompt = "<!-- agdt:initial-delivery-retry:original:1 -->\n\nResume initial delivery"
    with patch.object(provider, "_post_comment_as_pr_token_once", return_value=123) as post:
        assert provider._dispatch_agent_retry(5, prompt, "original", initial_delivery=True) == 123
    body = post.call_args.args[1]
    assert body.startswith("@copilot\n\n<!-- agdt:initial-delivery-retry:original:1 -->")
    assert get_agent_retry_markers([IssueCommentInfo(123, "workflow-bot", body)], "workflow-bot") == {}


def test_initial_delivery_dispatch_reconciles_timeout_without_resending() -> None:
    provider = GitHubActionsProvider(repo="owner/repo")
    marker = "<!-- agdt:initial-delivery-retry:original:1 -->"
    with (
        patch.object(provider, "_post_comment_as_pr_token_once", side_effect=RetryableError("response lost")) as post,
        patch.object(provider, "get_dispatch_login", return_value="workflow-bot"),
        patch.object(
            provider,
            "list_issue_comments",
            return_value=[IssueCommentInfo(123, "workflow-bot", f"@copilot\n\n{marker}")],
        ),
    ):
        assert provider._dispatch_agent_retry(5, f"{marker}\n\nResume", "original", initial_delivery=True) == 123
    post.assert_called_once()
