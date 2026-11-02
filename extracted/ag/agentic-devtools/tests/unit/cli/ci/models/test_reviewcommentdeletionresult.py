"""Tests for ReviewCommentDeletionResult dataclass."""

import dataclasses

import pytest

from agentic_devtools.cli.ci.models import ReviewCommentDeletionResult, ReviewCommentTarget


def _target(**overrides: object) -> ReviewCommentTarget:
    base: dict[str, object] = {
        "thread_id": 1,
        "comment_id": 1,
        "comment_type": "text",
        "marker_type": "file-summary",
        "snippet": "x",
    }
    base.update(overrides)
    return ReviewCommentTarget(**base)  # type: ignore[arg-type]


class TestReviewCommentDeletionResult:
    """Tests for the ReviewCommentDeletionResult frozen dataclass."""

    def test_default_targets_empty(self) -> None:
        result = ReviewCommentDeletionResult(executed=False)
        assert result.executed is False
        assert result.targets == ()
        assert result.selected_count == 0
        assert result.deleted_count == 0
        assert result.failed_count == 0

    def test_selected_count(self) -> None:
        result = ReviewCommentDeletionResult(
            executed=False,
            targets=(_target(), _target(comment_id=2)),
        )
        assert result.selected_count == 2

    def test_deleted_and_failed_counts(self) -> None:
        result = ReviewCommentDeletionResult(
            executed=True,
            targets=(
                _target(comment_id=1, deleted=True),
                _target(comment_id=2, deleted=True),
                _target(comment_id=3, error="HTTP 500"),
            ),
        )
        assert result.deleted_count == 2
        assert result.failed_count == 1
        assert result.selected_count == 3

    def test_dry_run_counts_zero(self) -> None:
        result = ReviewCommentDeletionResult(
            executed=False,
            targets=(_target(), _target(comment_id=2)),
        )
        assert result.deleted_count == 0
        assert result.failed_count == 0

    def test_frozen(self) -> None:
        result = ReviewCommentDeletionResult(executed=False)
        with pytest.raises(dataclasses.FrozenInstanceError):
            result.executed = True  # type: ignore[misc]

    def test_targets_are_immutable_tuple(self) -> None:
        result = ReviewCommentDeletionResult(executed=False, targets=(_target(),))
        with pytest.raises(AttributeError):
            result.targets.append(_target(comment_id=2))  # type: ignore[attr-defined]
