"""Tests for extracting authenticated suppression-promotion markers."""

from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot_review_comments import _promoted_suppression_markers


def test_ignores_a_promoted_root_with_an_empty_normalized_body() -> None:
    review = ReviewInfo(id=12, user="Copilot", state="COMMENTED", commit_sha="head-sha")
    comment = ReviewCommentInfo(
        id=101,
        path="a.py",
        body="\n\n🤖 AI PR Loop ·",
        html_url="",
        source_review_id=12,
    )

    assert _promoted_suppression_markers(review, [comment]) == set()
