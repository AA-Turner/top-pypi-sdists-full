"""Focused tests for prior review-thread counting."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot_thread_count import count_unresolved_prior_threads


class TestCountUnresolvedPriorThreads:
    """Tests for count_unresolved_prior_threads()."""

    def test_counts_only_unresolved_threads_from_thread_state(self) -> None:
        provider = MagicMock()
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="resolved", html_url=""),
            ReviewCommentInfo(id=102, path="a.py", body="unresolved", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (True, (101,)),
            "thread-2": (False, (102,)),
        }

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")],
            verdict_review_id=0,
        )

        assert result == (1, 1, False, True)

    def test_measured_count_is_not_inflated_by_a_failing_review(self) -> None:
        """A failed fetch keeps the measured count instead of adding to it."""
        provider = MagicMock()
        provider.list_review_comments.side_effect = [
            [
                ReviewCommentInfo(id=101, path="a.py", body="a", html_url=""),
                ReviewCommentInfo(id=102, path="a.py", body="b", html_url=""),
            ],
            RuntimeError("comments unavailable"),
        ]
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101,)),
            "thread-2": (False, (102,)),
        }

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha"),
                ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha-2"),
            ],
            verdict_review_id=0,
        )

        assert result == (2, 2, True, True)

    def test_verdict_review_threads_count_as_repairable_but_not_blocking(self) -> None:
        """A thread from the verdict review is repairable but not blocking."""
        provider = MagicMock()
        provider.list_review_comments.side_effect = [
            [ReviewCommentInfo(id=101, path="a.py", body="verdict thread", html_url="")],
            [ReviewCommentInfo(id=102, path="a.py", body="prior thread", html_url="")],
        ]
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101,)),
            "thread-2": (False, (102,)),
        }

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha"),
                ReviewInfo(id=11, user="Copilot", state="COMMENTED", commit_sha="old-sha"),
            ],
            verdict_review_id=10,
        )

        assert result == (1, 2, False, False)

    def test_thread_with_comments_in_verdict_and_prior_review_is_blocking(self) -> None:
        """A thread with comments in both the verdict review and a prior review is blocking."""
        provider = MagicMock()
        provider.list_review_comments.side_effect = [
            [ReviewCommentInfo(id=101, path="a.py", body="verdict comment", html_url="")],
            [ReviewCommentInfo(id=102, path="a.py", body="prior comment", html_url="")],
        ]
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101, 102)),
        }

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha"),
                ReviewInfo(id=11, user="Copilot", state="COMMENTED", commit_sha="old-sha"),
            ],
            verdict_review_id=10,
        )

        # thread-1 has comment 101 from verdict (repairable but not blocking)
        # and comment 102 from prior review (is blocking).
        # It should count as 1 repairable and 1 blocking.
        assert result == (1, 1, False, False)

    def test_approved_review_threads_count_as_repairable_but_not_blocking(self) -> None:
        """An APPROVED Copilot review's unresolved threads are repairable but not blocking."""
        provider = MagicMock()
        provider.list_review_comments.side_effect = [
            [ReviewCommentInfo(id=101, path="a.py", body="approved thread", html_url="")],
        ]
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101,)),
        }

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="APPROVED", commit_sha="old-sha")],
            verdict_review_id=0,
        )

        # APPROVED reviews are repairable but excluded from blocking classification.
        assert result == (0, 1, False, True)

    def test_dismissed_review_is_excluded_from_repairable_inventory(self) -> None:
        """DISMISSED reviews must not contribute to repairable inventory or degradation state."""
        provider = MagicMock()
        provider.list_review_comments.side_effect = RuntimeError("should not be called for dismissed review")
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101,)),
        }

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="DISMISSED", commit_sha="old-sha")],
            verdict_review_id=0,
        )

        assert result == (0, 0, False, True)
        provider.list_review_comments.assert_not_called()
