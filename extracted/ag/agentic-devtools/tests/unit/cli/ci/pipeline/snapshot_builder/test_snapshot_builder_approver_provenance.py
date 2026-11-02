"""Tests for build_pr_state_snapshot."""

from agentic_devtools.cli.ci.models import (
    PRMetadata,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    SYNTHETIC_MARKER,
    TRUSTED_SYNTHETIC_USERS,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _make_provider


class TestBuildPrStateSnapshot:
    """Tests for build_pr_state_snapshot behavior."""

    def test_has_approver_approval_on_head_false_when_synthetic_review_matches_approver_login(self) -> None:
        """A trusted synthetic review matching the approver login must NOT count as approver approval."""
        synthetic_user = next(iter(TRUSTED_SYNTHETIC_USERS))
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=1,
            title="Test PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
            requested_reviewers=[],
        )
        provider.list_pr_files.return_value = ["a.py"]
        provider.list_check_runs.return_value = []
        provider.list_reviews.return_value = [
            ReviewInfo(
                id=15,
                user=synthetic_user,
                state="APPROVED",
                commit_sha="head-sha",
                body=f"{SYNTHETIC_MARKER}\nsynthetic review",
            ),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_approver_login.return_value = synthetic_user

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.approver_login == synthetic_user
        assert snapshot.has_approver_approval_on_head is False

    def test_copilot_review_id_preserved_when_synthetic_user_also_submits_plain_approval(self) -> None:
        """Synthetic-marker review must not be lost when the same user later submits a plain approval.

        When the trusted synthetic user submits both a synthetic-marker review (lower ID) and a
        later plain APPROVED review (higher ID), the per-user de-duplication in
        get_effective_head_reviews retains only the plain APPROVED review, losing the marker.
        copilot_review selection must use the raw reviews list so the synthetic-marker review is
        still found and copilot_review_id is set correctly.
        """
        synthetic_user = next(iter(TRUSTED_SYNTHETIC_USERS))
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=1,
            title="Test PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
            requested_reviewers=[],
        )
        provider.list_pr_files.return_value = ["a.py"]
        provider.list_check_runs.return_value = []
        provider.list_reviews.return_value = [
            ReviewInfo(
                id=10,
                user=synthetic_user,
                state="COMMENTED",
                commit_sha="head-sha",
                body=f"{SYNTHETIC_MARKER}\ncopilot gate feedback",
                submitted_at="2026-08-08T01:00:00Z",
            ),
            # Later plain approval from the same user without the marker body.
            ReviewInfo(
                id=20,
                user=synthetic_user,
                state="APPROVED",
                commit_sha="head-sha",
                body="",
                submitted_at="2026-08-08T02:00:00Z",
            ),
        ]
        provider.list_review_comments.return_value = []
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        # The synthetic-marker review (ID=10) must be found even though the later plain
        # APPROVED review (ID=20) from the same user has a higher ID.
        assert snapshot.copilot_review_id == 10
        assert snapshot.review_state == "COMMENTED"
