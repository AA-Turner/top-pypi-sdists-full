"""Tests for delete_review_comments_command._print_result output."""

from __future__ import annotations

from agentic_devtools.cli.ci.delete_review_comments_command import _print_result
from agentic_devtools.cli.ci.models import ReviewCommentDeletionResult, ReviewCommentTarget


def _target(**overrides: object) -> ReviewCommentTarget:
    base: dict[str, object] = {
        "thread_id": 1,
        "comment_id": 2,
        "comment_type": "text",
        "marker_type": "file-summary",
        "snippet": "summary",
    }
    base.update(overrides)
    return ReviewCommentTarget(**base)  # type: ignore[arg-type]


class TestPrintResult:
    """Tests for the human-readable summary printer."""

    def test_empty_dry_run(self, capsys) -> None:
        _print_result(ReviewCommentDeletionResult(executed=False, targets=()), 5)
        out = capsys.readouterr().out
        assert "[DRY-RUN] PR #5: 0 comment(s) selected for deletion." in out
        assert "Nothing to delete." in out

    def test_dry_run_with_marker_and_author_targets(self, capsys) -> None:
        targets = (_target(marker_type="file-summary"), _target(comment_id=3, marker_type=None))
        _print_result(ReviewCommentDeletionResult(executed=False, targets=targets), 5)
        out = capsys.readouterr().out
        assert "[marker:file-summary]" in out
        assert "[author]" in out
        assert "Dry-run only. Re-run with --execute" in out

    def test_execute_with_deleted_and_failed(self, capsys) -> None:
        targets = (
            _target(deleted=True),
            _target(comment_id=3, deleted=False, error="HTTP 500"),
        )
        _print_result(ReviewCommentDeletionResult(executed=True, targets=targets), 9)
        out = capsys.readouterr().out
        assert "[EXECUTE] PR #9" in out
        assert "-> deleted" in out
        assert "-> FAILED (HTTP 500)" in out
        assert "Done: 1 deleted, 1 failed." in out
