"""Unit tests for cleanup_collapsed_summaries."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import IssueCommentInfo
from scripts.cleanup_pr_summary_comments import cleanup_collapsed_summaries


def test_cleanup_collapsed_summaries_deletes_matching_comments() -> None:
    provider = MagicMock()
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(id=1, author="bot", body="<!-- agdt:ai-pr-loop-summary-collapsed -->\n\nOld run 1"),
        IssueCommentInfo(id=2, author="bot", body="<!-- agdt:ai-pr-loop-summary -->\n\nActive run"),
        IssueCommentInfo(id=3, author="bot", body="<!-- agdt:ai-pr-loop-summary-collapsed -->\n\nOld run 2"),
        IssueCommentInfo(id=4, author="user", body="LGTM!"),
    ]

    deleted = cleanup_collapsed_summaries(provider, 42)

    assert deleted == 2
    provider.delete_comment.assert_any_call(1)
    provider.delete_comment.assert_any_call(3)
    assert provider.delete_comment.call_count == 2


def test_cleanup_collapsed_summaries_dry_run_does_not_delete() -> None:
    provider = MagicMock()
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(id=1, author="bot", body="<!-- agdt:ai-pr-loop-summary-collapsed -->\n\nOld run"),
    ]

    deleted = cleanup_collapsed_summaries(provider, 42, dry_run=True)

    assert deleted == 1
    provider.delete_comment.assert_not_called()


def test_cleanup_collapsed_summaries_unsupported_provider() -> None:
    provider = MagicMock(spec=[])

    deleted = cleanup_collapsed_summaries(provider, 42)

    assert deleted == 0


def test_cleanup_collapsed_summaries_handles_delete_error() -> None:
    provider = MagicMock()
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(id=10, author="bot", body="<!-- agdt:ai-pr-loop-summary-collapsed -->\n\nOld"),
    ]
    provider.delete_comment.side_effect = RuntimeError("API error")

    deleted = cleanup_collapsed_summaries(provider, 42)

    assert deleted == 0
    provider.delete_comment.assert_called_once_with(10)
