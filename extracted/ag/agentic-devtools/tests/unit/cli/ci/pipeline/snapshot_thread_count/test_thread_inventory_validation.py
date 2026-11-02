"""Focused tests for prior review-thread counting."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot_thread_count import count_unresolved_prior_threads


class TestCountUnresolvedPriorThreads:
    """Tests for count_unresolved_prior_threads()."""

    def test_returns_degraded_when_thread_state_is_not_a_mapping(self) -> None:
        provider = MagicMock()
        provider.list_review_threads_by_thread_id.return_value = []

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")],
            verdict_review_id=0,
        )

        assert result == (1, 1, True, True)

    def test_omitted_thread_state_degrades_without_counting_per_comment(self) -> None:
        provider = MagicMock()
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="mapped unresolved", html_url=""),
            ReviewCommentInfo(id=102, path="a.py", body="omitted from state", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")],
            verdict_review_id=0,
        )

        assert result == (1, 1, True, True)

    def test_non_int_thread_comment_ids_fail_closed_even_with_one_valid_comment(self) -> None:
        provider = MagicMock()
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="mapped comment", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101, "bad"))}

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")],
            verdict_review_id=0,
        )

        assert result == (1, 1, True, True)

    def test_duplicate_comment_id_across_threads_fails_closed(self) -> None:
        provider = MagicMock()
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="mapped comment", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101,)),
            "thread-2": (True, (101,)),
        }

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")],
            verdict_review_id=0,
        )

        assert result == (1, 1, True, True)

    def test_missing_thread_state_on_non_blocking_review_keeps_blocking_at_zero(self) -> None:
        provider = MagicMock()
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=102, path="a.py", body="omitted-1", html_url=""),
            ReviewCommentInfo(id=103, path="a.py", body="omitted-2", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="APPROVED", commit_sha="old-sha")],
            verdict_review_id=0,
        )

        assert result == (0, 1, True, True)

    def test_missing_thread_state_on_blocking_review_marks_blocking_unknown(self) -> None:
        provider = MagicMock()
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=102, path="a.py", body="omitted", html_url=""),
            ReviewCommentInfo(id=101, path="a.py", body="mapped", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")],
            verdict_review_id=0,
        )

        assert result == (1, 1, True, True)
