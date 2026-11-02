"""Tests for _get_copilot_review."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot_builder import _get_copilot_review


def test_selects_latest_head_copilot_review_and_counts_comments() -> None:
    """The newest Copilot review on HEAD supplies its state and inline count."""
    provider = MagicMock()
    provider.list_review_comments.return_value = [ReviewCommentInfo(id=21, path="a.py", body="fix", html_url="")]
    reviews = [
        ReviewInfo(id=1, user="Copilot", state="COMMENTED", commit_sha="old", submitted_at="2025-01-01"),
        ReviewInfo(id=2, user="Copilot", state="COMMENTED", commit_sha="head", submitted_at="2025-02-01"),
    ]

    result = _get_copilot_review(provider, 7, reviews, "head")

    assert result == (reviews[1], "COMMENTED", 2, 1, provider.list_review_comments.return_value)
    provider.list_review_comments.assert_called_once_with(7, 2)


def test_missing_copilot_review_returns_empty_state() -> None:
    """No eligible review produces the documented empty tuple."""
    assert _get_copilot_review(MagicMock(), 7, [], "head") == (None, "", 0, 0, None)


def test_failed_comment_fetch_marks_commented_review_count_unknown() -> None:
    """A comment-fetch failure is represented by an unknown inline count."""
    provider = MagicMock()
    provider.list_review_comments.side_effect = RuntimeError("comments unavailable")
    review = ReviewInfo(id=2, user="Copilot", state="COMMENTED", commit_sha="head")

    assert _get_copilot_review(provider, 7, [review], "head") == (review, "COMMENTED", 2, -1, None)
