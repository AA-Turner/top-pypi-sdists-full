"""Tests for build_pr_state_snapshot."""

from agentic_devtools.cli.ci.models import (
    CheckRunStatus,
    PRMetadata,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_AWAITING_FRESH,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _make_provider


def _assert_snapshot_fields(snapshot: PRStateSnapshot) -> None:
    """Assert unrelated snapshot fields remain unchanged by the thread-count ordering."""
    assert snapshot.pr_number == 7
    assert snapshot.head_sha == "head-sha"
    assert snapshot.base_branch == "main"
    assert snapshot.head_branch == "feature"
    assert snapshot.ci_status == "passing"
    assert snapshot.ci_failed_checks == []
    assert snapshot.commit_count == 3
    assert snapshot.commits_behind == 2
    assert snapshot.has_approval_on_head is True
    assert snapshot.head_author_login == "someone"
    assert snapshot.title == "Reorder PR"
    assert snapshot.head_repo_full_name == "org/repo"
    assert snapshot.base_repo_full_name == "org/repo"
    assert snapshot.has_changes is True
    assert snapshot.copilot_review_pending is False
    assert snapshot.review_state == ""
    assert snapshot.copilot_review_id == 0
    assert snapshot.copilot_review_inline_count == 0
    assert snapshot.active_session is False
    assert snapshot.unresolved_threads == 0
    assert snapshot.unresolved_threads_degraded is False
    assert snapshot.is_draft is False
    assert snapshot.mergeable is None
    assert snapshot.mergeable_state == ""
    assert snapshot.requested_reviewers == []
    assert snapshot.approver_login == ""
    assert snapshot.has_approver_approval_on_head is False
    assert snapshot.files == ["a.py", "b.py"]
    assert snapshot.check_runs == [
        CheckRunStatus(id=1, name="Run Targeted Checks", status="completed", conclusion="success"),
    ]
    assert snapshot.reviews == [
        ReviewInfo(id=10, user="alice", state="APPROVED", commit_sha="head-sha"),
        ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha"),
    ]
    assert snapshot.copilot_gate_verdict is not None
    assert snapshot.copilot_gate_verdict.passed is False
    assert snapshot.copilot_gate_verdict.reason == REASON_AWAITING_FRESH
    assert snapshot.copilot_gate_verdict.review_id == 0
    assert snapshot.head_changed_since_review is True
    assert snapshot.repair_satisfied_review_id is None
    assert snapshot.suppressed_deferral_review_id is None
    assert snapshot.suppressed_deferral_issue_number is None


class TestBuildPrStateSnapshot:
    """Tests for build_pr_state_snapshot behavior."""

    def test_reorder_does_not_change_other_snapshot_fields(self) -> None:
        """Moving the thread count below the gate verdict must not disturb other fields."""
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=7,
            title="Reorder PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
            head_repo_full_name="org/repo",
            base_repo_full_name="org/repo",
            requested_reviewers=[],
        )
        provider.list_pr_files.return_value = ["a.py", "b.py"]
        provider.list_check_runs.return_value = [
            CheckRunStatus(id=1, name="Run Targeted Checks", status="completed", conclusion="success"),
        ]
        provider.list_reviews.return_value = [
            ReviewInfo(id=10, user="alice", state="APPROVED", commit_sha="head-sha"),
            ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha"),
        ]
        provider.list_review_comments.return_value = []
        provider.list_review_threads_by_thread_id.return_value = {}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 3
        provider.count_commits_behind.return_value = 2
        provider.get_commit_author_login.return_value = "someone"

        snapshot = build_pr_state_snapshot(provider, 7)
        # The Copilot review targets "old-sha", not HEAD, so no HEAD Copilot review is found.
        # The verdict fails closed because no fresh HEAD review exists.
        _assert_snapshot_fields(snapshot)
