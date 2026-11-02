"""Tests for find_repair_satisfied_review_id in the guards module."""

from __future__ import annotations

from agentic_devtools.cli.ci.guards import (
    REPAIR_SATISFIED_MARKER,
    REVIEW_ID_MARKER_RE,
    find_repair_satisfied_review_id,
)
from agentic_devtools.cli.ci.models import IssueCommentInfo

COPILOT_AUTHOR = "copilot-swe-agent[bot]"


def _marker_body(review_id: int) -> str:
    return f"{REPAIR_SATISFIED_MARKER}\n<!-- review-id:{review_id} -->\nNo changes needed."


class TestFindRepairSatisfiedReviewId:
    """Tests for find_repair_satisfied_review_id."""

    def test_empty_list_returns_none(self) -> None:
        assert find_repair_satisfied_review_id([]) is None

    def test_no_marker_returns_none(self) -> None:
        comments = [IssueCommentInfo(id=1, author=COPILOT_AUTHOR, body="Just a normal comment")]
        assert find_repair_satisfied_review_id(comments) is None

    def test_single_marker_returns_review_id(self) -> None:
        comments = [IssueCommentInfo(id=1, author=COPILOT_AUTHOR, body=_marker_body(555))]
        assert find_repair_satisfied_review_id(comments) == 555

    def test_marker_without_review_id_ignored(self) -> None:
        """A repair-satisfied marker with no review-id marker is not matched."""
        comments = [
            IssueCommentInfo(id=1, author=COPILOT_AUTHOR, body=f"{REPAIR_SATISFIED_MARKER}\nNo review id here"),
        ]
        assert find_repair_satisfied_review_id(comments) is None

    def test_non_copilot_author_ignored(self) -> None:
        """A marker posted by a non-Copilot author must not be trusted."""
        comments = [IssueCommentInfo(id=1, author="someuser", body=_marker_body(777))]
        assert find_repair_satisfied_review_id(comments) is None

    def test_multiple_markers_returns_latest_by_created_at(self) -> None:
        comments = [
            IssueCommentInfo(id=1, author=COPILOT_AUTHOR, body=_marker_body(100), created_at="2024-01-01T00:00:00Z"),
            IssueCommentInfo(id=2, author=COPILOT_AUTHOR, body=_marker_body(200), created_at="2024-06-01T00:00:00Z"),
        ]
        assert find_repair_satisfied_review_id(comments) == 200

    def test_ties_broken_by_comment_id(self) -> None:
        """When created_at is equal, the highest comment id wins."""
        comments = [
            IssueCommentInfo(id=5, author=COPILOT_AUTHOR, body=_marker_body(100), created_at="2024-01-01T00:00:00Z"),
            IssueCommentInfo(id=9, author=COPILOT_AUTHOR, body=_marker_body(200), created_at="2024-01-01T00:00:00Z"),
        ]
        assert find_repair_satisfied_review_id(comments) == 200

    def test_review_id_regex_extracts_from_marker_body(self) -> None:
        """Sanity: the review-id regex extracts the id embedded by _marker_body."""
        match = REVIEW_ID_MARKER_RE.search(_marker_body(42))
        assert match is not None
        assert match.group(1) == "42"
