"""Tests for build_pr_state_snapshot."""

from agentic_devtools.cli.ci.models import (
    PRMetadata,
    ReviewCommentInfo,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _make_provider


class TestBuildPrStateSnapshot:
    """Tests for build_pr_state_snapshot behavior."""

    def test_unresolved_threads_stable_across_head_move_alone(self) -> None:
        """A HEAD move alone (e.g. squash/takeover) must not change the unresolved count.

        Reproduces the squash/takeover scenario: the Copilot review the gate verdict
        already owns keeps its provenance across a HEAD-SHA-only move (via the
        content-hash freshness carry-over), so it is excluded from the count both
        before and after the move, while a genuinely different prior review is
        counted identically both times.
        """
        head_sha_before = "1" * 40
        head_sha_after = "2" * 40
        owned_review = ReviewInfo(
            id=10,
            user="Copilot",
            state="CHANGES_REQUESTED",
            body="Copilot generated 1 comment.",
            commit_sha=head_sha_before,
            submitted_at="2024-02-01T00:00:00Z",
        )
        other_prior_review = ReviewInfo(
            id=20,
            user="Copilot",
            state="COMMENTED",
            commit_sha="c" * 40,
            submitted_at="2024-01-01T00:00:00Z",
        )

        def _list_review_comments(pr_number: int, review_id: int) -> list[ReviewCommentInfo]:
            if review_id == 20:
                return [ReviewCommentInfo(id=201, path="a.py", body="fix this", html_url="")]
            return []

        def _build(head_sha: str) -> PRStateSnapshot:
            provider = _make_provider()
            provider.get_pr_metadata.return_value = PRMetadata(
                number=1,
                title="Test",
                head_branch="feature",
                head_sha=head_sha,
                base_branch="main",
                requested_reviewers=[],
            )
            provider.list_pr_files.return_value = ["a.py"]
            provider.list_check_runs.return_value = []
            provider.list_reviews.return_value = [owned_review, other_prior_review]
            provider.list_review_comments.side_effect = _list_review_comments
            provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (201,))}
            provider.compute_diff_hash.return_value = "same-hash"
            provider.list_pr_issue_events.return_value = []
            provider.count_commits_above_merge_base.return_value = 1
            return build_pr_state_snapshot(provider, 1)

        snapshot_before = _build(head_sha_before)
        snapshot_after = _build(head_sha_after)

        assert snapshot_before.copilot_gate_verdict is not None
        assert snapshot_after.copilot_gate_verdict is not None
        assert snapshot_before.copilot_gate_verdict.review_id == 10
        assert snapshot_after.copilot_gate_verdict.review_id == 10
        assert snapshot_before.unresolved_threads == 1
        assert snapshot_after.unresolved_threads == 1
        assert snapshot_before.unresolved_threads == snapshot_after.unresolved_threads

    def test_unresolved_threads_counts_all_when_verdict_review_id_is_zero(self) -> None:
        """review_id <= 0 (no verdict review resolved) degenerates to count-all."""
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=1,
            title="Test",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
            requested_reviewers=[],
        )
        provider.list_pr_files.return_value = ["a.py"]
        provider.list_check_runs.return_value = []
        provider.list_reviews.return_value = [
            ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha"),
        ]
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="fix this", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        # No review targets HEAD and no diff-hash capability is configured, so
        # the gate verdict fails closed with review_id == 0 (AWAITING_FRESH).
        # Provenance is unknown so count-all is used, but the query succeeded —
        # the count is authoritative and degraded is False.
        assert snapshot.copilot_gate_verdict is not None
        assert snapshot.copilot_gate_verdict.review_id == 0
        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is False
