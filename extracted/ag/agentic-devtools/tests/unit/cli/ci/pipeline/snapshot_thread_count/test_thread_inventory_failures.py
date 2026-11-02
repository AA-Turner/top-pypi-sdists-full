"""Focused tests for prior review-thread counting."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot_thread_count import count_unresolved_prior_threads


class TestCountUnresolvedPriorThreads:
    """Tests for count_unresolved_prior_threads()."""

    def test_returns_degraded_when_review_comments_fetch_fails(self) -> None:
        provider = MagicMock()
        provider.list_review_comments.side_effect = RuntimeError("comments unavailable")
        provider.list_review_threads_by_thread_id.side_effect = RuntimeError("thread state unavailable")

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")],
            verdict_review_id=0,
        )

        assert result == (1, 1, True, True)

    def test_multiple_failing_reviews_yield_the_blocking_floor(self) -> None:
        """Two failing fetches must not fabricate two unresolved threads."""
        provider = MagicMock()
        provider.list_review_comments.side_effect = RuntimeError("comments unavailable")
        provider.list_review_threads_by_thread_id.side_effect = RuntimeError("thread state unavailable")

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha"),
                ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha-2"),
            ],
            verdict_review_id=0,
        )

        assert result == (1, 1, True, True)

    def test_approved_only_unknown_inventory_sets_repairable_floor_without_blocking_floor(self) -> None:
        """Unknown inventory for non-blocking-only reviews should not force blocking floor."""
        provider = MagicMock()
        provider.list_review_threads_by_thread_id.side_effect = RuntimeError("thread state unavailable")

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="APPROVED", commit_sha="old-sha")],
            verdict_review_id=0,
        )

        assert result == (0, 1, True, True)

    def test_non_blocking_comment_fetch_failure_does_not_apply_blocking_floor(self) -> None:
        provider = MagicMock()
        provider.list_review_comments.side_effect = RuntimeError("comments unavailable")
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="APPROVED", commit_sha="old-sha")],
            verdict_review_id=0,
        )

        assert result == (0, 1, True, True)

    def test_blocking_review_fetch_failure_still_processes_remaining_reviews(self) -> None:
        provider = MagicMock()
        provider.list_review_comments.side_effect = [
            RuntimeError("blocking comments unavailable"),
            [ReviewCommentInfo(id=201, path="a.py", body="approved unresolved", html_url="")],
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (201,))}

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha"),
                ReviewInfo(id=11, user="Copilot", state="APPROVED", commit_sha="old-sha-2"),
            ],
            verdict_review_id=0,
        )

        assert result == (1, 1, True, True)

    def test_blocking_floor_applied_when_repairable_nonzero_but_blocking_zero_and_degraded(self) -> None:
        """Degraded partial-measurement floors blocking at 1 even when measured blocking count is 0.

        Scenario: an APPROVED verdict review has an unresolved thread (measured, repairable but not
        blocking), and a prior CHANGES_REQUESTED review fails to load its comments (degraded).
        Before the fix, this returned (0, 1, True) — blocking count zero in a degraded state — which
        could allow squash/approval guards to proceed. After the fix, blocking is floored at 1.
        """
        provider = MagicMock()
        provider.list_review_comments.side_effect = [
            [ReviewCommentInfo(id=101, path="a.py", body="approved thread", html_url="")],
            RuntimeError("comments unavailable"),
        ]
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101,)),
        }

        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="APPROVED", commit_sha="old-sha"),
                ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha-2"),
            ],
            verdict_review_id=0,
        )

        # total_blocking == 0 (APPROVED is not blocking), total_repairable == 1,
        # comments_unavailable == True — blocking must be floored at 1.
        assert result == (1, 1, True, True)
