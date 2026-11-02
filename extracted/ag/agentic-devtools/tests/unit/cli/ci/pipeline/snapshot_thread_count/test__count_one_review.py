"""Tests for _count_one_review."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot_thread_count import _count_one_review


def test_ignores_synthetic_negative_comment_ids() -> None:
    """Synthetic comment IDs do not count or degrade a real thread inventory."""
    provider = MagicMock()
    provider.list_review_comments.return_value = [
        ReviewCommentInfo(id=-1, path="a.py", body="synthetic", html_url=""),
    ]

    result = _count_one_review(
        provider,
        pr_number=7,
        review=ReviewInfo(id=10, user="Copilot", state="COMMENTED"),
        is_blocking=True,
        thread_states={},
        comment_to_thread={},
        counted_blocking=set(),
        counted_repairable=set(),
    )

    assert result == (0, 0, False, False)
