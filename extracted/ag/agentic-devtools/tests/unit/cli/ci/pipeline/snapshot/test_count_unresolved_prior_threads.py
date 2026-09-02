"""Tests for count_unresolved_prior_threads."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot import count_unresolved_prior_threads


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

    def test_effective_verdict_review_id_is_used(self) -> None:
        """The verdict parameter acts as the thread owner when provided, superseding verdict_review_id."""
        from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_CLEAN, CopilotGateVerdict

        provider = MagicMock()

        # When review 10 is considered the verdict thread owner, it won't be counted as prior.
        # But if the fallback fails and review 10 is NOT the owner, it will be counted.
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="mapped comment", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101,)),
        }

        # First verify it is counted when verdict_review_id=0 and no verdict is provided
        result_without_verdict = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")],
            verdict_review_id=0,
        )
        assert result_without_verdict == (1, 1, False, True)

        # Then verify it is skipped when verdict is provided and identifies review 10 as the owner
        verdict = CopilotGateVerdict(passed=True, reason=REASON_CLEAN, review_id=10)
        result_with_verdict = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")],
            verdict_review_id=0,
            verdict=verdict,
        )
        assert result_with_verdict == (0, 1, False, False)

    def test_unknown_provenance_counts_all_but_is_not_degraded(self) -> None:
        """Unknown provenance counts all reviews and sets unknown_provenance=True; degraded stays False."""
        from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_AWAITING_FRESH, CopilotGateVerdict

        provider = MagicMock()
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="mapped comment", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}

        verdict = CopilotGateVerdict(passed=False, reason=REASON_AWAITING_FRESH, review_id=0)
        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")],
            verdict_review_id=0,
            verdict=verdict,
        )

        assert result == (1, 1, False, True)

    def test_unknown_verdict_does_not_fallback_to_legacy_owner_id(self) -> None:
        """A present verdict with review_id=0 is authoritative unknown provenance."""
        from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_AWAITING_FRESH, CopilotGateVerdict

        provider = MagicMock()
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="mapped comment", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}

        result_without_verdict = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")],
            verdict_review_id=10,
        )
        assert result_without_verdict == (0, 1, False, False)

        verdict = CopilotGateVerdict(passed=False, reason=REASON_AWAITING_FRESH, review_id=0)
        result = count_unresolved_prior_threads(
            provider,
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha")],
            verdict_review_id=10,
            verdict=verdict,
        )

        assert result == (1, 1, False, True)
