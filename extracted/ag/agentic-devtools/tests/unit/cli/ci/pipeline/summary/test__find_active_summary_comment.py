"""Tests for _find_active_summary_comment."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.summary import (
    SUMMARY_COLLAPSED_SENTINEL,
    SUMMARY_SENTINEL,
    _find_active_summary_comment,
)


def _comment_body(sentinel: str, suffix: str = "") -> str:
    return f"{sentinel}\n\n#### 🤖 AI PR Loop Run — stable content{suffix}"


def test_newer_collapsed_copy_suppresses_older_active_summary() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            id=10,
            author="github-actions[bot]",
            body=_comment_body(SUMMARY_SENTINEL),
        ),
        IssueCommentInfo(
            id=11,
            author="github-actions[bot]",
            body=_comment_body(SUMMARY_COLLAPSED_SENTINEL),
        ),
    ]

    assert _find_active_summary_comment(provider, 42) is None


def test_malformed_collapsed_copy_does_not_suppress_active_summary() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            id=10,
            author="github-actions[bot]",
            body=_comment_body(SUMMARY_SENTINEL),
        ),
        IssueCommentInfo(
            id=11,
            author="github-actions[bot]",
            body=_comment_body(SUMMARY_COLLAPSED_SENTINEL, "\n🤖 AI PR Loop ·"),
        ),
    ]

    result = _find_active_summary_comment(provider, 42)

    assert result is not None
    assert result[0] == 10


def test_newer_collapsed_copy_can_be_resolved_from_unsorted_comments() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            id=11,
            author="github-actions[bot]",
            body=_comment_body(SUMMARY_COLLAPSED_SENTINEL),
        ),
        IssueCommentInfo(
            id=10,
            author="github-actions[bot]",
            body=_comment_body(SUMMARY_SENTINEL),
        ),
    ]

    assert _find_active_summary_comment(provider, 42) is None


def test_selected_summary_body_removes_only_its_exact_terminal_label() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    body = (
        f"{SUMMARY_SENTINEL}\n\n#### 🤖 AI PR Loop Run — stable content\n"
        "> quoted text: 🤖 AI PR Loop ·\n\n🤖 AI PR Loop ·"
    )
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(id=12, author="github-actions[bot]", body=body),
    ]

    result = _find_active_summary_comment(provider, 42)

    assert result == (
        12,
        f"{SUMMARY_SENTINEL}\n\n#### 🤖 AI PR Loop Run — stable content\n> quoted text: 🤖 AI PR Loop ·",
    )


def test_skips_active_summary_with_malformed_terminal_label() -> None:
    provider = MagicMock()
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    provider.list_issue_comments.return_value = [
        IssueCommentInfo(
            id=13,
            author="github-actions[bot]",
            body=_comment_body(SUMMARY_SENTINEL, "\n🤖 AI PR Loop ·"),
        ),
    ]

    assert _find_active_summary_comment(provider, 42) is None


def test_fallback_skips_malformed_terminal_label() -> None:
    provider = MagicMock()
    provider.list_issue_comments = None
    provider.find_comment.return_value = (
        14,
        _comment_body(SUMMARY_SENTINEL, "\n🤖 AI PR Loop ·"),
    )

    assert _find_active_summary_comment(provider, 42) is None
