"""Tests for ResolveThreadsAction."""

from unittest.mock import MagicMock, call

import pytest

from agentic_devtools.cli.ci.models import FinalizationResult, ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions.resolve_threads import ResolveThreadsAction
from agentic_devtools.cli.ci.pipeline.gate_verdict import CopilotGateVerdict
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.retry import ProviderRateLimitError


class TestResolveThreadsAction:
    """Tests for resolve threads action."""

    def test_runs_after_invalidation(self) -> None:
        """ResolveThreadsAction opts in to run after snapshot invalidation."""
        action = ResolveThreadsAction()
        assert action.runs_after_invalidation is True

    def test_proceeds_when_active_session(self) -> None:
        """Active session no longer blocks thread resolution."""
        snapshot = PRStateSnapshot(
            pr_number=1, active_session=True, ci_status="passing", unresolved_threads=5, repairable_threads=5
        )
        derived = DerivedState(snapshot)
        action = ResolveThreadsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_proceeds_when_copilot_review_pending(self) -> None:
        """Pending review no longer blocks thread resolution (FR-002)."""
        snapshot = PRStateSnapshot(
            pr_number=1, ci_status="passing", copilot_review_pending=True, unresolved_threads=3, repairable_threads=3
        )
        derived = DerivedState(snapshot)
        action = ResolveThreadsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert "no_pending_review" not in result.preconditions

    def test_proceeds_when_ci_not_passing(self) -> None:
        """CI status no longer blocks thread resolution (FR-002)."""
        snapshot = PRStateSnapshot(pr_number=1, ci_status="failing", unresolved_threads=3, repairable_threads=3)
        derived = DerivedState(snapshot)
        action = ResolveThreadsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert "ci_passing" not in result.preconditions

    def test_skip_when_no_threads(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, ci_status="passing", unresolved_threads=0, repairable_threads=0)
        derived = DerivedState(snapshot)
        action = ResolveThreadsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "no unresolved" in result.details.lower()

    def test_skip_when_autofix_applied_without_repair(self) -> None:
        """Skip SDK evaluation when autofix just ran but no repair dispatched."""
        snapshot = PRStateSnapshot(pr_number=1, ci_status="passing", unresolved_threads=3, repairable_threads=3)
        derived = DerivedState(snapshot)
        derived.set("autofix_applied_this_iteration", True)
        action = ResolveThreadsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "autofix_without_repair" in result.preconditions
        assert "autofix just applied" in result.details

    def test_skip_when_ci_pending_without_repair(self) -> None:
        """Skip SDK evaluation when CI is pending and no repair dispatched."""
        snapshot = PRStateSnapshot(pr_number=1, ci_status="pending", unresolved_threads=3, repairable_threads=3)
        derived = DerivedState(snapshot)
        action = ResolveThreadsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "ci_not_actionable" in result.preconditions
        assert "pending" in result.details

    def test_execute_when_threads_exist(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            active_session=False,
            ci_status="passing",
            copilot_review_pending=False,
            unresolved_threads=3,
            repairable_threads=3,
        )
        derived = DerivedState(snapshot)
        action = ResolveThreadsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_only_has_unresolved_threads_precondition(self) -> None:
        """Only has_unresolved_threads remains as a precondition (FR-002, FR-003)."""
        snapshot = PRStateSnapshot(
            pr_number=1, ci_status="failing", copilot_review_pending=True, unresolved_threads=5, repairable_threads=5
        )
        derived = DerivedState(snapshot)
        derived.set("copilot_review_pending", True)
        action = ResolveThreadsAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert "has_unresolved_threads" in result.preconditions
        assert "ci_passing" not in result.preconditions
        assert "no_pending_review" not in result.preconditions

    def test_execute_calls_finalize(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.return_value = FinalizationResult(resolved_count=2, unresolved_count=0)
        action = ResolveThreadsAction()
        result = action.execute(provider, snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert "2" in result.details
        provider.finalize_post_repair.assert_called_once()

    def test_execute_calls_finalize_for_all_prior_reviews(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=4,
            repairable_threads=4,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
                ReviewInfo(id=12, user="Copilot", state="COMMENTED", commit_sha="old456"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.side_effect = [
            FinalizationResult(resolved_count=1, unresolved_count=1),
            FinalizationResult(resolved_count=2, unresolved_count=0),
        ]
        action = ResolveThreadsAction()

        result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert result.details == "Resolved 3 thread(s), 1 left open"
        assert derived.unresolved_threads == 1
        provider.finalize_post_repair.assert_has_calls(
            [
                call(
                    pr_number=1,
                    base_branch="main",
                    head_branch="feature",
                    head_sha="head123",
                    review_id=12,
                ),
                call(
                    pr_number=1,
                    base_branch="main",
                    head_branch="feature",
                    head_sha="head123",
                    review_id=10,
                ),
            ]
        )

    def test_execute_sets_derived_unresolved_threads(self) -> None:
        """execute() writes post-resolution unresolved count to derived state."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=3,
            repairable_threads=3,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.return_value = FinalizationResult(resolved_count=2, unresolved_count=1)
        action = ResolveThreadsAction()
        action.execute(provider, snapshot, derived)
        # Derived state must reflect the post-resolution count, not the snapshot count.
        assert derived.unresolved_threads == 1

    def test_execute_uses_requeried_count_instead_of_snapshot_floor(self) -> None:
        """execute() reports the authoritative re-queried count, not a snapshot floor."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=3,
            repairable_threads=3,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.return_value = FinalizationResult(resolved_count=1, unresolved_count=0)
        # Authoritative post-resolution state: every prior-review comment resolved.
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="x", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (True, (101,))}
        action = ResolveThreadsAction()

        result = action.execute(provider, snapshot, derived)

        assert result.details == "Resolved 1 thread(s), 0 left open"
        assert derived.unresolved_threads == 0

    def test_execute_ignores_suppressed_synthetic_inflation(self) -> None:
        """Suppressed synthetic counts from finalize no longer inflate the total."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=1,
            repairable_threads=1,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old123"),
                ReviewInfo(id=11, user="Copilot", state="COMMENTED", commit_sha="old456"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        # finalize_post_repair reports large per-review unresolved counts that
        # include suppressed synthetics and are summed without de-duplication.
        provider.finalize_post_repair.side_effect = [
            FinalizationResult(resolved_count=0, unresolved_count=40),
            FinalizationResult(resolved_count=0, unresolved_count=31),
        ]
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="x", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}
        action = ResolveThreadsAction()

        result = action.execute(provider, snapshot, derived)

        assert result.details == "Resolved 0 thread(s), 1 left open"
        assert derived.unresolved_threads == 1

    def test_execute_reports_suppressed_comments_separately(self) -> None:
        """Suppressed synthetics are surfaced in the summary but never block."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=1,
            repairable_threads=1,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.return_value = FinalizationResult(
            resolved_count=1, unresolved_count=0, suppressed_count=3
        )
        provider.list_review_comments.return_value = []
        provider.list_review_threads_by_thread_id.return_value = {}
        action = ResolveThreadsAction()

        result = action.execute(provider, snapshot, derived)

        assert result.details == "Resolved 1 thread(s), 0 left open; 3 suppressed comment(s) not counted"
        assert derived.unresolved_threads == 0

    def test_execute_falls_back_when_thread_state_degraded(self) -> None:
        """A degraded re-query keeps the conservative pre-re-query estimate."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=3,
            repairable_threads=3,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.return_value = FinalizationResult(resolved_count=1, unresolved_count=0)
        provider.list_review_threads_by_thread_id.side_effect = NotImplementedError()
        action = ResolveThreadsAction()

        result = action.execute(provider, snapshot, derived)

        assert result.details == "Resolved 1 thread(s), 2 left open"
        assert derived.unresolved_threads == 2
        assert derived.unresolved_threads_degraded is True

    def test_execute_degraded_fallback_keeps_fail_closed_sentinel(self) -> None:
        """Degraded fallback must not drop to zero when state is unknown."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=1,
            repairable_threads=1,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.return_value = FinalizationResult(resolved_count=1, unresolved_count=0)
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="x", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.side_effect = NotImplementedError()
        action = ResolveThreadsAction()

        result = action.execute(provider, snapshot, derived)

        assert result.details == "Resolved 1 thread(s), 1 left open"
        assert derived.unresolved_threads == 1
        assert derived.unresolved_threads_degraded is True

    def test_execute_marks_comment_fetch_failure_as_degraded(self) -> None:
        """A re-query comment-fetch failure must mark thread state as degraded."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=1,
            repairable_threads=1,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.return_value = FinalizationResult(resolved_count=1, unresolved_count=0)
        provider.list_review_comments.side_effect = RuntimeError("comments unavailable")
        provider.list_review_threads_by_thread_id.return_value = {}
        action = ResolveThreadsAction()

        result = action.execute(provider, snapshot, derived)

        assert result.details == "Resolved 1 thread(s), 1 left open"
        assert derived.unresolved_threads == 1
        assert derived.unresolved_threads_degraded is True

    def test_execute_degraded_requery_preserves_prior_repairable_count_when_resolved_is_duplicated(self) -> None:
        """A degraded re-query must not over-subtract repairable count with per-review resolved totals."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=1,
            repairable_threads=1,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
                ReviewInfo(id=11, user="Copilot", state="COMMENTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.side_effect = [
            FinalizationResult(resolved_count=1, unresolved_count=0),
            FinalizationResult(resolved_count=1, unresolved_count=0),
        ]
        provider.list_review_threads_by_thread_id.side_effect = NotImplementedError()
        action = ResolveThreadsAction()

        result = action.execute(provider, snapshot, derived)

        assert result.details == "Resolved 2 thread(s), 1 left open"
        assert derived.unresolved_threads == 1
        assert derived.repairable_threads == 1
        assert derived.unresolved_threads_degraded is True

    def test_execute_clears_degraded_when_requery_succeeds_after_degraded_snapshot(self) -> None:
        """A successful re-query clears the degraded sentinel when concrete provenance is known again."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=3,
            repairable_threads=3,
            unresolved_threads_degraded=True,
            copilot_gate_verdict=CopilotGateVerdict(passed=False, reason="reviewed", review_id=10),
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
                ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old456"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.return_value = FinalizationResult(resolved_count=1, unresolved_count=0)
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="x", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (True, (101,))}
        action = ResolveThreadsAction()

        action.execute(provider, snapshot, derived)

        assert derived.unresolved_threads == 0
        assert derived.unresolved_threads_degraded is False

    def test_execute_reports_skipped_prior_reviews(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
                ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old456"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.side_effect = [
            FinalizationResult(skipped=True, reason="no_new_commit"),
            FinalizationResult(resolved_count=2, unresolved_count=0),
        ]
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="x", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (True, (101,))}
        action = ResolveThreadsAction()

        result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert result.details == "Resolved 2 thread(s), 0 left open; skipped 1 prior review(s): #11:no_new_commit"

    def test_execute_records_skipped_review_metrics_by_reason(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=3,
            repairable_threads=3,
            reviews=[
                ReviewInfo(id=12, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
                ReviewInfo(id=11, user="Copilot", state="COMMENTED", commit_sha="old456"),
                ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old789"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.side_effect = [
            FinalizationResult(skipped=True, reason="already_finalized"),
            FinalizationResult(skipped=True, reason="no_new_commit"),
            FinalizationResult(resolved_count=1, unresolved_count=0),
        ]
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="x", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (True, (101,))}
        action = ResolveThreadsAction()

        action.execute(provider, snapshot, derived)

        assert derived.get("finalization_skipped_reviews_count") == 2
        assert derived.get("finalization_skipped_reviews_by_reason") == {
            "already_finalized": 1,
            "no_new_commit": 1,
        }

    def test_execute_reports_unknown_reason_for_skipped_review_without_reason(self) -> None:
        """A skipped review with no reason renders 'unknown' rather than vanishing."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.return_value = FinalizationResult(skipped=True)
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="x", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (True, (101,))}
        action = ResolveThreadsAction()

        result = action.execute(provider, snapshot, derived)

        assert "#11:unknown" in result.details

    def test_execute_reports_no_comments_reason_for_semantic_no_op_review(self) -> None:
        """A no-comments finalization still renders its reason in the summary details."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.return_value = FinalizationResult(reason="no_comments")
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="x", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (True, (101,))}
        action = ResolveThreadsAction()

        result = action.execute(provider, snapshot, derived)

        assert result.details == "Resolved 0 thread(s), 0 left open; skipped 1 prior review(s): #11:no_comments"

    def test_execute_reports_finalization_errors(self) -> None:
        """Finalization errors reach the rendered details so failures are diagnosable."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=1,
            repairable_threads=1,
            reviews=[
                ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.return_value = FinalizationResult(
            reason="verified_with_resolution_errors",
            resolved_count=1,
            unresolved_count=0,
            errors=("thread_resolution_unverified", "comment_101:boom"),
        )
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="x", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (True, (101,))}
        action = ResolveThreadsAction()

        result = action.execute(provider, snapshot, derived)

        assert result.details == (
            "Resolved 1 thread(s), 0 left open; finalization errors: thread_resolution_unverified, comment_101:boom"
        )

    def test_execute_skips_when_no_prior_copilot_reviews(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[ReviewInfo(id=11, user="alice", state="COMMENTED", commit_sha="old123")],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        action = ResolveThreadsAction()

        result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "No prior Copilot or synthetic reviews found" in result.details

    def test_execute_calls_finalize_for_trusted_synthetic_review(self) -> None:
        """Trusted synthetic prior review triggers thread resolution."""
        from agentic_devtools.cli.ci.pipeline.gate_verdict import SYNTHETIC_MARKER, TRUSTED_SYNTHETIC_USERS

        synthetic_user = next(iter(TRUSTED_SYNTHETIC_USERS))
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(
                    id=10,
                    user=synthetic_user,
                    state="CHANGES_REQUESTED",
                    commit_sha="old123",
                    body=f"Review feedback. {SYNTHETIC_MARKER}",
                ),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.return_value = FinalizationResult(resolved_count=2, unresolved_count=0)
        action = ResolveThreadsAction()

        result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.finalize_post_repair.assert_called_once_with(
            pr_number=1,
            base_branch="main",
            head_branch="feature",
            head_sha="head123",
            review_id=10,
        )

    def test_execute_failed_when_finalize_post_repair_raises(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123")],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.finalize_post_repair.side_effect = RuntimeError("finalize boom")
        action = ResolveThreadsAction()

        result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED
        assert "All 1 prior reviews failed finalization: #10: finalize boom" in result.details

    def test_execute_partial_success_when_some_finalize_calls_raise(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=4,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
                ReviewInfo(id=12, user="Copilot", state="COMMENTED", commit_sha="old456"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()

        def mock_finalize(
            pr_number: int, base_branch: str, head_branch: str, head_sha: str, review_id: int
        ) -> FinalizationResult:
            if review_id == 10:
                return FinalizationResult(resolved_count=2, unresolved_count=0)
            raise RuntimeError("finalize boom")

        provider.finalize_post_repair.side_effect = mock_finalize
        action = ResolveThreadsAction()

        result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert "Resolved 2 thread(s), 2 left open" in result.details
        assert "hard failures: #12: finalize boom" in result.details
        # Degraded fallback calculates max(1, 0, 4 - 2, 0) = 2
        assert derived.unresolved_threads == 2

    def test_execute_re_raises_rate_limit_error(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            head_sha="head123",
            base_branch="main",
            head_branch="feature",
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123")],
        )
        provider = MagicMock()
        provider.finalize_post_repair.side_effect = ProviderRateLimitError(is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError):
            ResolveThreadsAction().execute(provider, snapshot, DerivedState(snapshot))
