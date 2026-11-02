"""Tests for _is_promoted_root."""

from typing import cast

import pytest

from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot_thread_count import _is_promoted_root


def test_recognizes_a_valid_promoted_root_owned_by_review() -> None:
    """A positive-ID root with matching provenance and marker belongs to its review."""
    review = ReviewInfo(id=42, user="Copilot", state="COMMENTED")
    comment = ReviewCommentInfo(
        id=101,
        path="a.py",
        body="Finding\n<!-- ccr-promoted:42:review_finding:1 -->",
        html_url="",
        source_review_id=42,
    )

    assert _is_promoted_root(review, comment) is True


@pytest.mark.parametrize(
    "comment",
    [
        ReviewCommentInfo(
            id=101,
            path="a.py",
            body="Finding\n<!-- ccr-promoted:43:review_finding:1 -->",
            html_url="",
            source_review_id=42,
        ),
        ReviewCommentInfo(
            id=101,
            path="a.py",
            body="Finding\n<!-- ccr-promoted:42:review_finding:1 -->",
            html_url="",
            source_review_id=42,
            in_reply_to_id=100,
        ),
        ReviewCommentInfo(
            id=-1,
            path="a.py",
            body="Finding\n<!-- ccr-promoted:42:review_finding:1 -->",
            html_url="",
            source_review_id=42,
        ),
        ReviewCommentInfo(
            id=101,
            path="a.py",
            body=cast(str, None),
            html_url="",
            source_review_id=42,
        ),
        ReviewCommentInfo(
            id=101,
            path="a.py",
            body="Finding\n<!-- ccr-promoted:42:Review-Finding:1 -->",
            html_url="",
            source_review_id=42,
        ),
    ],
)
def test_rejects_invalid_promoted_root_provenance_or_marker(comment: ReviewCommentInfo) -> None:
    """Wrong review ownership, replies, synthetic IDs, body types, or marker syntax are rejected."""
    review = ReviewInfo(id=42, user="Copilot", state="COMMENTED")

    assert _is_promoted_root(review, comment) is False
