"""Tests for ReviewCommentTarget dataclass."""

import dataclasses

import pytest

from agentic_devtools.cli.ci.models import ReviewCommentTarget


class TestReviewCommentTarget:
    """Tests for the ReviewCommentTarget frozen dataclass."""

    def test_required_fields(self) -> None:
        target = ReviewCommentTarget(
            thread_id=10,
            comment_id=20,
            comment_type="text",
            marker_type="file-summary",
            snippet="## File Review: src/app.ts",
        )
        assert target.thread_id == 10
        assert target.comment_id == 20
        assert target.comment_type == "text"
        assert target.marker_type == "file-summary"
        assert target.snippet == "## File Review: src/app.ts"

    def test_default_outcome_fields(self) -> None:
        target = ReviewCommentTarget(
            thread_id=1,
            comment_id=1,
            comment_type="text",
            marker_type=None,
            snippet="x",
        )
        assert target.deleted is False
        assert target.error is None

    def test_marker_type_can_be_none(self) -> None:
        target = ReviewCommentTarget(
            thread_id=1,
            comment_id=1,
            comment_type="text",
            marker_type=None,
            snippet="x",
        )
        assert target.marker_type is None

    def test_outcome_fields_settable_at_construction(self) -> None:
        target = ReviewCommentTarget(
            thread_id=1,
            comment_id=1,
            comment_type="text",
            marker_type="overall-summary",
            snippet="x",
            deleted=True,
            error=None,
        )
        assert target.deleted is True

    def test_replace_records_outcome(self) -> None:
        target = ReviewCommentTarget(
            thread_id=1,
            comment_id=1,
            comment_type="text",
            marker_type="activity-log",
            snippet="x",
        )
        deleted = dataclasses.replace(target, deleted=True)
        failed = dataclasses.replace(target, error="HTTP 500")
        assert deleted.deleted is True
        assert deleted.error is None
        assert failed.error == "HTTP 500"
        assert failed.deleted is False

    def test_frozen(self) -> None:
        target = ReviewCommentTarget(
            thread_id=1,
            comment_id=1,
            comment_type="text",
            marker_type=None,
            snippet="x",
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            target.deleted = True  # type: ignore[misc]
