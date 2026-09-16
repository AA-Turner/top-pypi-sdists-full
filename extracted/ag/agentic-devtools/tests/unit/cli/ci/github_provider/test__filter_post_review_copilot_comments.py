"""Tests for filtering post-review Copilot comments."""

from agentic_devtools.cli.ci.github_provider import _filter_post_review_copilot_comments
from agentic_devtools.cli.ci.models import IssueCommentInfo


def test_filters_human_and_pre_review_comments_and_sorts() -> None:
    comments = [
        IssueCommentInfo(3, "copilot-swe-agent[bot]", "later", "2026-01-03T00:00:00Z"),
        IssueCommentInfo(1, "copilot-swe-agent[bot]", "before", "2025-12-31T00:00:00Z"),
        IssueCommentInfo(2, "reviewer", "human", "2026-01-02T00:00:00Z"),
        IssueCommentInfo(4, "COPILOT-SWE-AGENT[BOT]", "earlier", "2026-01-02T12:00:00Z"),
    ]

    result = _filter_post_review_copilot_comments(comments, "2026-01-01T00:00:00Z")

    assert [comment.body for comment in result] == ["earlier", "later"]


def test_excludes_comments_with_invalid_timestamps() -> None:
    comments = [IssueCommentInfo(1, "Copilot", "invalid", "not-a-timestamp")]

    assert _filter_post_review_copilot_comments(comments, "2026-01-01T00:00:00Z") == ()


def test_invalid_review_timestamp_returns_empty() -> None:
    comments = [IssueCommentInfo(1, "Copilot", "comment", "2026-01-02T00:00:00Z")]

    assert _filter_post_review_copilot_comments(comments, "not-a-timestamp") == ()


def test_normalizes_naive_timestamps_to_utc() -> None:
    comments = [IssueCommentInfo(1, "Copilot", "comment", "2026-01-02T00:00:00")]

    result = _filter_post_review_copilot_comments(comments, "2026-01-01T00:00:00")

    assert [comment.body for comment in result] == ["comment"]
