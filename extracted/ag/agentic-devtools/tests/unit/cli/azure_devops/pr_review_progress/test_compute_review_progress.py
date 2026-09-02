"""Tests for compute_review_progress."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.pr_review_progress import compute_review_progress

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_progress"


def _run(total: int, reviewed: int) -> dict:
    with (
        patch(f"{_MODULE}.count_in_scope_files", return_value=total),
        patch(f"{_MODULE}.ledger_reviewed_count", return_value=reviewed),
    ):
        return compute_review_progress(99)


class TestComputeReviewProgress:
    def test_total_correct_before_any_answers(self):
        # Acceptance: total equals in-scope file count (not 0) before answers.
        assert _run(3, 0) == {
            "total_count": 3,
            "completed_count": 0,
            "pending_count": 3,
            "all_complete": False,
        }

    def test_partial_progress_does_not_complete(self):
        assert _run(3, 1) == {
            "total_count": 3,
            "completed_count": 1,
            "pending_count": 2,
            "all_complete": False,
        }

    def test_all_complete_when_every_file_answered(self):
        assert _run(3, 3) == {
            "total_count": 3,
            "completed_count": 3,
            "pending_count": 0,
            "all_complete": True,
        }

    def test_stale_ledger_more_than_total_does_not_advance(self):
        # reviewed > total (stale accepted entries for files no longer in manifest):
        # fall back to the baseline so we never advance prematurely.
        assert _run(3, 4) == {
            "total_count": 3,
            "completed_count": 0,
            "pending_count": 3,
            "all_complete": False,
        }

    def test_zero_total_never_completes(self):
        # Guards against a missing manifest spuriously reading total=0 and
        # auto-advancing delegate -> consolidate-and-submit with no review.
        assert _run(0, 0) == {
            "total_count": 0,
            "completed_count": 0,
            "pending_count": 0,
            "all_complete": False,
        }
