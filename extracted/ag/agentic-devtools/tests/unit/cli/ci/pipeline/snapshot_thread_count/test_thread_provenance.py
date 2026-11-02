"""Focused tests for prior review-thread counting."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot_thread_count import count_unresolved_prior_threads


class TestCountUnresolvedPriorThreads:
    """Tests for count_unresolved_prior_threads()."""

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
