"""Tests for build_pr_state_snapshot."""

import logging
from typing import cast
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.guards import REPAIR_SATISFIED_MARKER
from agentic_devtools.cli.ci.models import (
    CheckRunStatus,
    IssueCommentInfo,
    PRMetadata,
    ReviewCommentInfo,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.deferral import SUPPRESSED_DEFERRAL_SENTINEL
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_API_ERROR,
    REASON_AWAITING_FRESH,
    REASON_HAS_COMMENTS,
    REASON_SUPPRESSED_COMMENTS,
    SYNTHETIC_MARKER,
    TRUSTED_SYNTHETIC_USERS,
    CopilotGateVerdict,
)
from agentic_devtools.cli.ci.pipeline.snapshot import (
    PRStateSnapshot,
    _evaluate_ci_status,
    build_pr_state_snapshot,
    has_non_copilot_changes_requested_on_head,
)
from agentic_devtools.cli.ci.retry import ProviderRateLimitError


def _make_provider() -> MagicMock:
    provider = MagicMock()
    provider.count_commits_behind.return_value = 0
    provider.get_approver_login.return_value = ""
    return provider


def _current_review_provider(
    comments: list[ReviewCommentInfo],
    thread_states: object,
    *,
    body: str = "",
) -> MagicMock:
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
            id=12,
            user="Copilot",
            state="CHANGES_REQUESTED",
            body=body,
            commit_sha="head-sha",
        ),
    ]
    provider.list_review_comments.return_value = comments
    provider.list_review_threads_by_thread_id.return_value = thread_states
    provider.list_pr_issue_events.return_value = []
    provider.count_commits_above_merge_base.return_value = 1
    return provider


class TestBuildPrStateSnapshot:
    """Tests for build_pr_state_snapshot behavior."""

    def test_ci_status_unknown_for_non_success_non_failure_completed_checks(self) -> None:
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
        provider.list_check_runs.return_value = [
            CheckRunStatus(
                id=101,
                name="Run Targeted Checks",
                status="completed",
                conclusion="cancelled",
            )
        ]
        provider.list_reviews.return_value = []
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.ci_status == "unknown"
        assert snapshot.ci_failed_checks == []

    def test_uses_explicit_actionable_check_names_when_provided(self) -> None:
        """Explicit actionable set should be used without defaulting."""
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
        provider.list_check_runs.return_value = [
            CheckRunStatus(id=101, name="Custom Check", status="completed", conclusion="success"),
        ]
        provider.list_reviews.return_value = []
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1, actionable_check_names=frozenset({"Custom Check"}))

        assert snapshot.ci_status == "passing"

    def test_head_author_login_populated_from_provider(self) -> None:
        """head_author_login captures the HEAD commit author login."""
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=1, title="t", head_branch="feature", head_sha="head-sha", base_branch="main", requested_reviewers=[]
        )
        provider.list_pr_files.return_value = ["a.py"]
        provider.list_check_runs.return_value = []
        provider.list_reviews.return_value = []
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_commit_author_login.return_value = "Copilot"

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_author_login == "Copilot"
        provider.get_commit_author_login.assert_called_once_with("head-sha")

    def test_head_author_login_coerced_to_empty_when_non_string(self) -> None:
        """A non-string author value is coerced to an empty string."""
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=1, title="t", head_branch="feature", head_sha="head-sha", base_branch="main", requested_reviewers=[]
        )
        provider.list_pr_files.return_value = ["a.py"]
        provider.list_check_runs.return_value = []
        provider.list_reviews.return_value = []
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_commit_author_login.return_value = object()

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_author_login == ""

    def test_head_author_login_empty_when_provider_raises(self) -> None:
        """A provider error resolving the author fails open to an empty string."""
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=1, title="t", head_branch="feature", head_sha="head-sha", base_branch="main", requested_reviewers=[]
        )
        provider.list_pr_files.return_value = ["a.py"]
        provider.list_check_runs.return_value = []
        provider.list_reviews.return_value = []
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_commit_author_login.side_effect = RuntimeError("boom")

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_author_login == ""

    def test_head_author_rate_limit_error_is_propagated(self) -> None:
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=1, title="t", head_branch="feature", head_sha="head-sha", base_branch="main", requested_reviewers=[]
        )
        provider.list_pr_files.return_value = ["a.py"]
        provider.list_check_runs.return_value = []
        provider.list_reviews.return_value = []
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_commit_author_login.side_effect = ProviderRateLimitError(is_rate_limit=True)

        with pytest.raises(ProviderRateLimitError):
            build_pr_state_snapshot(provider, 1)

    def test_unresolved_threads_fails_closed_when_review_comments_fetch_fails(self) -> None:
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
            ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha"),
        ]
        provider.list_review_comments.side_effect = RuntimeError("boom")
        provider.list_review_threads_by_thread_id.side_effect = RuntimeError("boom")
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1

    def test_unresolved_threads_counts_across_all_prior_copilot_reviews(self) -> None:
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
            ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha-1"),
            ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha-2"),
        ]
        provider.list_review_comments.side_effect = [
            [
                ReviewCommentInfo(id=101, path="a.py", body="a", html_url=""),
                ReviewCommentInfo(id=102, path="a.py", body="b", html_url=""),
            ],
            [
                ReviewCommentInfo(id=201, path="a.py", body="c", html_url=""),
                ReviewCommentInfo(id=202, path="a.py", body="d", html_url=""),
                ReviewCommentInfo(id=203, path="a.py", body="e", html_url=""),
            ],
        ]
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101, 102)),
            "thread-2": (False, (201, 202, 203)),
        }
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 2
        assert provider.list_review_comments.call_count == 2

    def test_unresolved_threads_counts_prior_trusted_synthetic_reviews(self) -> None:
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
                user="AMARSNIK_swica",
                state="COMMENTED",
                body=f"{SYNTHETIC_MARKER}\nsynthetic review",
                commit_sha="old-sha",
            ),
        ]
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="a", html_url=""),
            ReviewCommentInfo(id=102, path="a.py", body="b", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101, 102))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        provider.list_review_comments.assert_called_once_with(1, 10)

    def test_unresolved_threads_fails_closed_after_partial_aggregation(self) -> None:
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
            ReviewInfo(id=10, user="Copilot", state="COMMENTED", commit_sha="old-sha-1"),
            ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha-2"),
        ]
        provider.list_review_comments.side_effect = [
            [
                ReviewCommentInfo(id=101, path="a.py", body="a", html_url=""),
                ReviewCommentInfo(id=102, path="a.py", body="b", html_url=""),
            ],
            RuntimeError("boom"),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101, 102))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1

    def test_unresolved_threads_excludes_resolved_threads(self) -> None:
        """Only unresolved threads should be counted."""
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
            ReviewCommentInfo(id=102, path="a.py", body="also this", html_url=""),
            ReviewCommentInfo(id=103, path="a.py", body="and this", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101, 103)),
            "thread-2": (True, (102,)),
        }
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1

    def test_unresolved_threads_counts_a_single_thread_with_multiple_comments_once(self) -> None:
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
            ReviewCommentInfo(id=102, path="a.py", body="also this", html_url=""),
            ReviewCommentInfo(id=103, path="a.py", body="and this", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101, 102, 103))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1

    def test_unresolved_threads_fails_closed_when_thread_state_lookup_is_not_implemented(self) -> None:
        """A NotImplemented thread-state lookup degrades to the blocking floor."""
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
            ReviewCommentInfo(id=101, path="a.py", body="fix", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.side_effect = NotImplementedError()
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True

    def test_unresolved_threads_fails_closed_when_thread_state_mapping_is_invalid(self) -> None:
        """An invalid thread-state mapping degrades to the blocking floor."""
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
            ReviewCommentInfo(id=101, path="a.py", body="fix", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False,)}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True

    def test_unresolved_threads_fails_closed_when_thread_key_is_none(self) -> None:
        """A None thread key is malformed; the mapping is rejected and the snapshot fails closed."""
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
            ReviewCommentInfo(id=101, path="a.py", body="fix", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {None: (False, (101,))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True

    def test_unresolved_threads_fails_closed_when_thread_key_is_empty_string(self) -> None:
        """An empty-string thread key is malformed; the mapping is rejected and the snapshot fails closed."""
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
            ReviewCommentInfo(id=101, path="a.py", body="fix", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"": (False, (101,))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True

    def test_unresolved_threads_fails_closed_when_thread_comment_ids_shape_is_invalid(self) -> None:
        """A non-tuple thread comment-id collection is treated as invalid and fail-closed."""
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
            ReviewCommentInfo(id=101, path="a.py", body="fix", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, ["101"])}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True

    def test_unresolved_threads_fails_closed_when_thread_comment_id_is_not_int(self) -> None:
        """A non-integer thread comment ID is treated as invalid thread-state data."""
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
            ReviewCommentInfo(id=101, path="a.py", body="fix", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, ("101",))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True

    def test_unresolved_threads_fails_closed_when_thread_comment_ids_mix_int_and_non_int(self) -> None:
        """Mixed-type thread comment IDs are malformed, even if one id maps cleanly."""
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
            ReviewCommentInfo(id=101, path="a.py", body="fix", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (True, (101, "bad"))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True

    def test_unresolved_threads_fails_closed_when_same_comment_maps_to_two_threads(self) -> None:
        """A comment ID that appears in two different threads is a conflicting mapping; fail closed."""
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
            ReviewCommentInfo(id=101, path="a.py", body="fix", html_url=""),
        ]
        # comment 101 appears in both thread-1 and thread-2 — conflicting mapping
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (101,)),
            "thread-2": (True, (101,)),
        }
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True

    def test_unresolved_threads_skips_negative_comment_ids(self) -> None:
        """Synthetic review-body entries are ignored when counting unresolved threads."""
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
            ReviewCommentInfo(id=-1, path="a.py", body="synthetic", html_url=""),
            ReviewCommentInfo(id=101, path="a.py", body="fix", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is False

    def test_unresolved_threads_skips_repeated_comment_after_missing_thread_state(self) -> None:
        """A comment already counted as missing-thread-state is not double-counted on later reviews."""
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
            ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha-1"),
            ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha-2"),
        ]
        provider.list_review_comments.side_effect = [
            [ReviewCommentInfo(id=101, path="a.py", body="fix", html_url="")],
            [ReviewCommentInfo(id=101, path="a.py", body="fix", html_url="")],
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (True, (102,))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True

    def test_unresolved_threads_falls_back_when_thread_states_unavailable(self) -> None:
        """When review-thread state lookup fails, degrade and count the blocking floor."""
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
            ReviewCommentInfo(id=101, path="a.py", body="fix", html_url=""),
            ReviewCommentInfo(id=102, path="a.py", body="fix2", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.side_effect = RuntimeError("API error")
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True

    def test_unresolved_threads_falls_back_without_thread_state_method(self) -> None:
        """Without the thread-state capability, the count degrades to a blocking fallback."""
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
            ReviewCommentInfo(id=-1, path="a.py", body="review body", html_url=""),
            ReviewCommentInfo(id=101, path="a.py", body="fix", html_url=""),
        ]
        provider.list_review_threads_by_thread_id = None
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True

    def test_unresolved_threads_never_zero_without_thread_state_capability(self) -> None:
        """A capability-less provider yields a degraded, blocking count — never 0."""
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
            ReviewCommentInfo(id=-1, path="a.py", body="review body", html_url=""),
        ]
        del provider.list_review_threads_by_thread_id
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads_degraded is True
        assert snapshot.unresolved_threads >= 1

    def test_unresolved_threads_not_degraded_without_prior_reviews(self) -> None:
        """No prior reviews needs no capability, so the zero count is not degraded."""
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
        provider.list_reviews.return_value = []
        provider.list_review_comments.return_value = []
        del provider.list_review_threads_by_thread_id
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 0
        assert snapshot.unresolved_threads_degraded is False

    def test_unresolved_threads_deduplicates_same_thread_across_reviews(self) -> None:
        """The same unresolved thread appearing in multiple prior reviews is only counted once."""
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
            ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha-1"),
            ReviewInfo(id=11, user="Copilot", state="COMMENTED", commit_sha="old-sha-2"),
        ]
        provider.list_review_comments.side_effect = [
            [ReviewCommentInfo(id=101, path="a.py", body="fix this", html_url="")],
            [ReviewCommentInfo(id=101, path="a.py", body="fix this", html_url="")],
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1

    def test_unresolved_threads_fails_closed_when_thread_statuses_omit_comments(self) -> None:
        """Incomplete thread-state data degrades without inflating by comment count."""
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
            ReviewCommentInfo(id=101, path="a.py", body="unresolved", html_url=""),
            ReviewCommentInfo(id=102, path="a.py", body="not in thread data", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True

    def test_unresolved_threads_logs_when_thread_statuses_omit_a_comment(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A comment absent from thread-state data emits a diagnostic warning."""
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
            ReviewCommentInfo(id=102, path="a.py", body="not in thread data", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (True, (101,))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        with caplog.at_level(logging.WARNING, logger="agentic_devtools.cli.ci.pipeline.snapshot"):
            snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads_degraded is True
        assert "review-thread state omitted comment 102" in caplog.text

    def test_unresolved_threads_degrades_and_logs_when_comments_fetch_fails(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A review whose comments cannot be listed degrades the count and logs it."""
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
        provider.list_review_comments.side_effect = RuntimeError("comments unavailable")
        provider.list_review_threads_by_thread_id.return_value = {}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        with caplog.at_level(logging.WARNING, logger="agentic_devtools.cli.ci.pipeline.snapshot"):
            snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True
        assert "failed to list review comments for review 10" in caplog.text

    def test_unresolved_threads_combined_fail_and_omitted_entry_is_not_inflated(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Two-review mixed case: one fetch fails and another has an omitted thread-state entry.

        The failed fetch contributes no fabricated thread, so the total is the single
        candidate thread whose state was omitted — blocking (non-zero) and degraded,
        but never inflated beyond what was actually observed.
        """
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
            ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old-sha"),
        ]
        provider.list_review_comments.side_effect = [
            RuntimeError("network error"),
            [ReviewCommentInfo(id=200, path="a.py", body="needs work", html_url="")],
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (True, (101,))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        with caplog.at_level(logging.WARNING, logger="agentic_devtools.cli.ci.pipeline.snapshot"):
            snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.unresolved_threads == 1
        assert snapshot.unresolved_threads_degraded is True

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
        # The Copilot review targets "old-sha", not HEAD, so no HEAD Copilot review is found.
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
        # The Copilot review targets an old SHA; the verdict fails closed (no fresh HEAD review).
        assert snapshot.copilot_gate_verdict is not None
        assert snapshot.copilot_gate_verdict.passed is False
        assert snapshot.copilot_gate_verdict.reason == REASON_AWAITING_FRESH
        assert snapshot.copilot_gate_verdict.review_id == 0
        assert snapshot.head_changed_since_review is True
        assert snapshot.repair_satisfied_review_id is None
        assert snapshot.suppressed_deferral_review_id is None
        assert snapshot.suppressed_deferral_issue_number is None

    def test_count_commits_error_propagates_as_metadata_failure(self) -> None:
        """When count_commits_above_merge_base raises, build_pr_state_snapshot raises too.

        This ensures the caller (run_ai_pr_loop_v2) exits with EXIT_METADATA_FAILED
        rather than proceeding with an assumed commit count of 1.
        """
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
        provider.list_reviews.return_value = []
        provider.list_review_comments.return_value = []
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.side_effect = RuntimeError("git failure")

        with pytest.raises(RuntimeError, match="git failure"):
            build_pr_state_snapshot(provider, 1)

    def test_count_commits_behind_error_propagates_as_metadata_failure(self) -> None:
        """When count_commits_behind raises, build_pr_state_snapshot raises too."""
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
        provider.list_reviews.return_value = []
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.count_commits_behind.side_effect = RuntimeError("compare failed")

        with pytest.raises(RuntimeError, match="compare failed"):
            build_pr_state_snapshot(provider, 1)

    def test_count_commits_provider_without_support_defaults_to_1(self) -> None:
        """When the provider lacks count_commits_above_merge_base, default to 1."""
        provider = MagicMock(
            spec=[
                "get_pr_metadata",
                "list_pr_files",
                "list_check_runs",
                "list_reviews",
                "list_review_comments",
                "list_pr_issue_events",
            ]
        )
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
        provider.list_reviews.return_value = []
        provider.list_pr_issue_events.return_value = []

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.commit_count == 1

    def test_list_check_runs_error_propagates_as_metadata_failure(self) -> None:
        """When list_check_runs raises, build_pr_state_snapshot raises too.

        This ensures the caller (run_ai_pr_loop_v2) exits with EXIT_METADATA_FAILED
        rather than proceeding with an empty check list that silently drives
        ci_status to 'pending' and allows readiness evaluation against stale data.
        """
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
        provider.list_check_runs.side_effect = RuntimeError("API outage")

        with pytest.raises(RuntimeError, match="API outage"):
            build_pr_state_snapshot(provider, 1)

    def test_list_pr_files_error_propagates_as_metadata_failure(self) -> None:
        """When list_pr_files raises, build_pr_state_snapshot raises too.

        This ensures the caller (run_ai_pr_loop_v2) exits with EXIT_METADATA_FAILED
        rather than proceeding with an empty file list that bypasses guard checks
        (privileged-path / Dockerfile checks rely on snapshot.files).
        """
        provider = _make_provider()
        provider.get_pr_metadata.return_value = PRMetadata(
            number=1,
            title="Test PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
            requested_reviewers=[],
        )
        provider.list_pr_files.side_effect = RuntimeError("network failure")

        with pytest.raises(RuntimeError, match="network failure"):
            build_pr_state_snapshot(provider, 1)

    def test_list_reviews_error_propagates_as_metadata_failure(self) -> None:
        """When list_reviews raises, build_pr_state_snapshot raises too."""
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
        provider.list_reviews.side_effect = RuntimeError("reviews unavailable")

        with pytest.raises(RuntimeError, match="reviews unavailable"):
            build_pr_state_snapshot(provider, 1)

    def test_has_approval_on_head_uses_effective_latest_review_per_reviewer(self) -> None:
        """A superseded approval should not count as current approval on HEAD.

        Copilot's approval sets the generic ``has_approval_on_head`` flag; the only
        non-Copilot reviewer (alice) has a superseding CHANGES_REQUESTED so their
        earlier approval is not effective on HEAD.
        """
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
            ReviewInfo(id=10, user="alice", state="APPROVED", commit_sha="head-sha"),
            ReviewInfo(id=11, user="alice", state="CHANGES_REQUESTED", commit_sha="head-sha"),
            ReviewInfo(id=12, user="Copilot", state="APPROVED", commit_sha="head-sha"),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.has_approval_on_head is True
        assert snapshot.review_state == "APPROVED"
        assert snapshot.copilot_review_id == 12

    def test_copilot_review_fields_populated_for_synthetic_review_on_head(self) -> None:
        """Trusted synthetic Copilot reviews on HEAD populate the review id/state fields."""
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
                id=12,
                user="AMARSNIK_swica",
                state="COMMENTED",
                commit_sha="head-sha",
                body="<!-- synthetic-copilot-review -->",
            ),
        ]
        provider.list_review_comments.return_value = []
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.review_state == "COMMENTED"
        assert snapshot.copilot_review_id == 12
        assert snapshot.copilot_review_inline_count == 0

    def test_effective_review_comment_count_excludes_resolved_comments(self) -> None:
        """Resolved current-review comments do not remain effective repair work."""
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
                id=12,
                user="Copilot",
                state="CHANGES_REQUESTED",
                body="Review reports 1 comment(s) posted",
                commit_sha="head-sha",
            ),
        ]
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="fix", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (True, (101,))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count == 0
        assert snapshot.effective_review_comment_count_review_id == 12
        assert snapshot.effective_review_comment_filter_applied is True

    def test_effective_review_comment_count_excludes_answered_cloud_agent_comments(self) -> None:
        """A non-empty Cloud Coding Agent reply consumes its parent finding."""
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
                id=12,
                user="Copilot",
                state="CHANGES_REQUESTED",
                body="Review reports 1 comment(s) posted",
                commit_sha="head-sha",
            ),
        ]
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(
                id=101,
                path="a.py",
                body="fix",
                html_url="",
                author_login="copilot-pull-request-reviewer[bot]",
            ),
            ReviewCommentInfo(
                id=102,
                path="a.py",
                body="Implemented.",
                html_url="",
                author_login="copilot-swe-agent[bot]",
                in_reply_to_id=101,
            ),
        ]
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101, 102))}
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count == 0
        assert snapshot.effective_review_comment_count_review_id == 12
        assert snapshot.effective_review_comment_filter_applied is True

    def test_effective_review_comment_count_includes_unresolved_comments(self) -> None:
        """An unresolved current-review comment remains effective repair work."""
        provider = _current_review_provider(
            [ReviewCommentInfo(id=101, path="a.py", body="fix", html_url="")],
            {"thread-1": (False, (101,))},
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count == 1
        assert snapshot.effective_review_comment_count_review_id == 12
        assert snapshot.effective_review_comment_filter_applied is False

    def test_effective_review_comment_count_is_unknown_when_thread_state_fetch_fails(self) -> None:
        """Thread-state failures preserve fail-open repair dispatch behavior."""
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
            ReviewInfo(id=12, user="Copilot", state="CHANGES_REQUESTED", commit_sha="head-sha"),
        ]
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="fix", html_url=""),
        ]
        provider.list_review_threads_by_thread_id.side_effect = RuntimeError("threads unavailable")
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count is None

    def test_effective_review_comment_count_is_unknown_without_thread_state_support(self) -> None:
        """Providers without thread-state support preserve fail-open behavior."""
        provider = _current_review_provider(
            [ReviewCommentInfo(id=101, path="a.py", body="fix", html_url="")],
            {},
        )
        provider.list_review_threads_by_thread_id = None

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count is None

    def test_effective_review_comment_count_is_unknown_for_invalid_thread_state(self) -> None:
        """Malformed thread-state data must not be treated as an empty inventory."""
        provider = _current_review_provider(
            [ReviewCommentInfo(id=101, path="a.py", body="fix", html_url="")],
            {"thread-1": (False,)},
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count is None

    def test_effective_review_comment_count_is_unknown_for_conflicting_thread_resolution(self) -> None:
        """Conflicting duplicate comment resolution must preserve fail-open behavior."""
        provider = _current_review_provider(
            [ReviewCommentInfo(id=101, path="a.py", body="fix", html_url="")],
            {
                "thread-1": (True, (101,)),
                "thread-2": (False, (101,)),
            },
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count is None
        assert snapshot.effective_review_comment_filter_applied is None

    def test_effective_review_comment_count_is_unknown_for_unmapped_comment(self) -> None:
        """A positive comment missing from thread state keeps dispatch fail-open."""
        provider = _current_review_provider(
            [ReviewCommentInfo(id=101, path="a.py", body="fix", html_url="")],
            {"thread-1": (False, (102,))},
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count is None

    def test_effective_review_comment_count_is_unknown_for_non_integer_comment_id(self) -> None:
        """Malformed comment identifiers keep the effective inventory unknown."""
        provider = _current_review_provider(
            [ReviewCommentInfo(id=cast(int, "bad"), path="a.py", body="fix", html_url="")],
            {},
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count is None

    def test_effective_review_comment_count_counts_synthetic_entries(self) -> None:
        """Recovered synthetic entries count as effective review work."""
        provider = _current_review_provider(
            [ReviewCommentInfo(id=-1, path="a.py", body="suppressed", html_url="")],
            {},
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count == 1

    def test_effective_review_comment_count_is_unknown_for_zero_comment_id(self) -> None:
        """A zero comment identifier is malformed and cannot prove no work remains."""
        provider = _current_review_provider(
            [ReviewCommentInfo(id=0, path="a.py", body="fix", html_url="")],
            {},
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count is None

    def test_effective_review_comment_count_is_unknown_for_unrecovered_suppressed_comments(self) -> None:
        """A declared suppressed count without recovered entries is incomplete."""
        provider = _current_review_provider(
            [ReviewCommentInfo(id=101, path="a.py", body="fix", html_url="")],
            {"thread-1": (False, (101,))},
            body="### Comments suppressed due to low confidence (1)",
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count is None

    def test_effective_review_comment_count_skips_non_actionable_review_states(self) -> None:
        """Reviews outside repair-triggering states do not require comment retrieval."""
        provider = _current_review_provider([], {})
        provider.list_reviews.return_value[0] = ReviewInfo(
            id=12,
            user="Copilot",
            state="DISMISSED",
            commit_sha="head-sha",
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count is None

    def test_effective_review_comment_count_handles_non_commented_fetch_failure(self) -> None:
        """A failed fetch for an approved review remains fail-open."""
        provider = _current_review_provider([], {})
        provider.list_reviews.return_value[0] = ReviewInfo(
            id=12,
            user="Copilot",
            state="APPROVED",
            commit_sha="head-sha",
        )
        provider.list_review_comments.side_effect = RuntimeError("comments unavailable")

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.effective_review_comment_count is None

    def test_copilot_review_selection_tolerates_missing_submitted_at(self) -> None:
        """Missing synthetic-review timestamps must not break latest-review selection."""
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
                id=12,
                user="AMARSNIK_swica",
                state="COMMENTED",
                commit_sha="head-sha",
                body="<!-- synthetic-copilot-review -->",
                submitted_at=cast(str, None),
            ),
            ReviewInfo(
                id=13,
                user="Copilot",
                state="APPROVED",
                commit_sha="head-sha",
                submitted_at="2026-08-07T07:00:00Z",
            ),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.review_state == "APPROVED"
        assert snapshot.copilot_review_id == 13

    def test_has_approver_approval_on_head_true_when_approver_login_matches(self) -> None:
        """Precise approver-identity check: approver login resolves and matches reviewer."""
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
            ReviewInfo(id=13, user="loop-bot", state="APPROVED", commit_sha="head-sha"),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_approver_login.return_value = "loop-bot"

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.approver_login == "loop-bot"
        assert snapshot.has_approver_approval_on_head is True

    def test_has_approver_approval_on_head_true_case_insensitive(self) -> None:
        """Approver login comparison is case-insensitive."""
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
            ReviewInfo(id=13, user="Loop-Bot", state="APPROVED", commit_sha="head-sha"),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_approver_login.return_value = "loop-bot"

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.has_approver_approval_on_head is True

    def test_has_approver_approval_on_head_false_when_login_empty(self) -> None:
        """When approver login cannot be resolved, flag stays False."""
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
            ReviewInfo(id=13, user="some-human", state="APPROVED", commit_sha="head-sha"),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_approver_login.return_value = ""  # PAT not configured

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.approver_login == ""
        assert snapshot.has_approver_approval_on_head is False

    def test_has_approver_approval_on_head_false_when_approver_has_not_approved(self) -> None:
        """Known approver login but no matching APPROVED review ⇒ flag stays False."""
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
            ReviewInfo(id=12, user="Copilot", state="APPROVED", commit_sha="head-sha"),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_approver_login.return_value = "loop-bot"

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.approver_login == "loop-bot"
        assert snapshot.has_approver_approval_on_head is False

    def test_has_approver_approval_on_head_false_when_review_has_empty_commit_sha(self) -> None:
        """Approver APPROVED review with empty commit_sha fails closed and is not treated as HEAD approval."""
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
            ReviewInfo(id=13, user="loop-bot", state="APPROVED", commit_sha=""),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_approver_login.return_value = "loop-bot"

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.approver_login == "loop-bot"
        assert snapshot.has_approver_approval_on_head is False

    def test_has_approver_approval_on_head_false_when_login_resolution_fails(self) -> None:
        """When get_approver_login raises an exception, flag stays False (fail-open)."""
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
            ReviewInfo(id=13, user="loop-bot", state="APPROVED", commit_sha="head-sha"),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_approver_login.side_effect = RuntimeError("API unavailable")

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.approver_login == ""
        assert snapshot.has_approver_approval_on_head is False

    def test_logs_debug_when_approver_login_resolution_fails(self, caplog: pytest.LogCaptureFixture) -> None:
        """Approver-login resolution failures are logged for operational debugging."""
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
        provider.list_reviews.return_value = []
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_approver_login.side_effect = RuntimeError("API unavailable")

        with caplog.at_level(logging.DEBUG, logger="agentic_devtools.cli.ci.pipeline.snapshot"):
            snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.approver_login == ""
        assert snapshot.has_approver_approval_on_head is False
        assert "Failed to resolve approver login for PR 1" in caplog.text

    def test_has_approver_approval_on_head_false_when_login_returns_non_string(self) -> None:
        """When get_approver_login returns a non-string, approver_login is coerced to ''."""
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
            ReviewInfo(id=14, user="loop-bot", state="APPROVED", commit_sha="head-sha"),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1
        provider.get_approver_login.return_value = None  # type: ignore[assignment]

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.approver_login == ""
        assert snapshot.has_approver_approval_on_head is False

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

    def test_has_approval_on_head_false_when_latest_effective_review_is_changes_requested(self) -> None:
        """If latest effective HEAD review is CHANGES_REQUESTED, approval should be false."""
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
            ReviewInfo(id=10, user="alice", state="APPROVED", commit_sha="head-sha"),
            ReviewInfo(id=11, user="alice", state="CHANGES_REQUESTED", commit_sha="head-sha"),
        ]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.has_approval_on_head is False

    def test_inline_count_unknown_when_head_commented_review_comments_fetch_fails(self) -> None:
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
            ReviewInfo(id=12, user="Copilot", state="COMMENTED", commit_sha="head-sha"),
        ]
        provider.list_review_comments.side_effect = RuntimeError("comments unavailable")
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.review_state == "COMMENTED"
        assert snapshot.copilot_review_id == 12
        assert snapshot.copilot_review_inline_count == -1

    def test_evaluate_ci_status_pending_when_actionable_pending(self) -> None:
        status, failed = _evaluate_ci_status(
            [
                CheckRunStatus(id=1, name="Targeted Checks ✅", status="in_progress", conclusion=""),
            ],
            frozenset({"Targeted Checks ✅"}),
        )
        assert status == "pending"
        assert failed == []

    def test_evaluate_ci_status_failing_with_actionable_failed_checks(self) -> None:
        status, failed = _evaluate_ci_status(
            [
                CheckRunStatus(id=1, name="Targeted Checks ✅", status="completed", conclusion="failure"),
            ],
            frozenset({"Targeted Checks ✅"}),
        )
        assert status == "failing"
        assert failed == ["Targeted Checks ✅"]

    def test_evaluate_ci_status_pending_takes_priority_over_failed(self) -> None:
        status, failed = _evaluate_ci_status(
            [
                CheckRunStatus(id=1, name="Targeted Checks ✅", status="completed", conclusion="failure"),
                CheckRunStatus(id=2, name="Smart Module Tests ✅", status="queued", conclusion=""),
            ],
            frozenset({"Targeted Checks ✅", "Smart Module Tests ✅"}),
        )
        assert status == "pending"
        assert failed == ["Targeted Checks ✅"]

    def test_evaluate_ci_status_passing_when_actionable_checks_succeed(self) -> None:
        status, failed = _evaluate_ci_status(
            [
                CheckRunStatus(id=1, name="Targeted Checks ✅", status="completed", conclusion="success"),
                CheckRunStatus(id=2, name="non-actionable", status="completed", conclusion="failure"),
            ],
            frozenset({"Targeted Checks ✅"}),
        )
        assert status == "passing"
        assert failed == []

    def test_head_commented_review_inline_count_is_comment_count(self) -> None:
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
            ReviewInfo(id=12, user="Copilot", state="COMMENTED", commit_sha="head-sha"),
        ]
        provider.list_review_comments.return_value = [MagicMock(), MagicMock(), MagicMock()]
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.copilot_review_inline_count == 3

    def test_has_non_copilot_changes_requested_on_head_false_when_none(self) -> None:
        assert has_non_copilot_changes_requested_on_head([], "head-sha") is False

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_gate_verdict_exception_results_in_failed_closed_verdict(self, mock_gate) -> None:
        """When evaluate_copilot_gate_verdict raises, gate verdict is failed-closed."""
        mock_gate.side_effect = RuntimeError("unexpected gate error")
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
        provider.list_reviews.return_value = []
        provider.list_pr_issue_events.return_value = []
        provider.count_commits_above_merge_base.return_value = 1

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.copilot_gate_verdict is not None
        assert snapshot.copilot_gate_verdict.passed is False
        assert snapshot.copilot_gate_verdict.reason == REASON_API_ERROR


def _suppressed_marker_provider(
    *,
    review_commit_sha: str = "head-sha",
    head_sha: str = "head-sha",
) -> MagicMock:
    """Provider with one Copilot review; caller patches the gate verdict."""
    provider = _make_provider()
    provider.get_pr_metadata.return_value = PRMetadata(
        number=1,
        title="Test PR",
        head_branch="feature",
        head_sha=head_sha,
        base_branch="main",
        requested_reviewers=[],
    )
    provider.list_pr_files.return_value = ["a.py"]
    provider.list_check_runs.return_value = []
    provider.list_reviews.return_value = [
        ReviewInfo(id=42, user="Copilot", state="COMMENTED", commit_sha=review_commit_sha),
    ]
    provider.list_review_comments.return_value = []
    provider.list_pr_issue_events.return_value = []
    provider.count_commits_above_merge_base.return_value = 1
    return provider


class TestBuildPrStateSnapshotSuppressedMarker:
    """Tests for head_changed_since_review and repair_satisfied_review_id fields."""

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_head_changed_true_when_latest_review_on_other_commit(self, mock_gate) -> None:
        mock_gate.return_value = CopilotGateVerdict(passed=True, reason="clean", review_id=42)
        provider = _suppressed_marker_provider(review_commit_sha="old-sha", head_sha="head-sha")

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is True
        # Passed verdict → marker branch skipped.
        assert snapshot.repair_satisfied_review_id is None

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_head_changed_false_when_latest_review_on_head(self, mock_gate) -> None:
        mock_gate.return_value = CopilotGateVerdict(passed=True, reason="clean", review_id=42)
        provider = _suppressed_marker_provider(review_commit_sha="head-sha", head_sha="head-sha")

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is False

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_head_changed_false_when_effective_synthetic_review_matches_head(self, mock_gate) -> None:
        """Trusted synthetic effective review on HEAD should not fail closed."""
        mock_gate.return_value = CopilotGateVerdict(passed=True, reason="clean", review_id=41, synthetic=True)
        provider = _suppressed_marker_provider(head_sha="head-sha")
        provider.list_reviews.return_value = [
            ReviewInfo(
                id=41,
                user="AMARSNIK_swica",
                state="COMMENTED",
                body="<!-- synthetic-copilot-review -->",
                commit_sha="head-sha",
            ),
        ]

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is False

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_head_changed_uses_effective_gate_review_instead_of_latest_review(self, mock_gate) -> None:
        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=41,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider(head_sha="head-sha")
        provider.list_reviews.return_value = [
            ReviewInfo(id=41, user="Copilot", state="COMMENTED", commit_sha="head-sha"),
            ReviewInfo(id=42, user="Copilot", state="COMMENTED", commit_sha="older-sha"),
        ]
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="copilot-swe-agent[bot]",
                body=f"{REPAIR_SATISFIED_MARKER}\n<!-- review-id:41 -->",
            ),
        ]

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is False
        assert snapshot.repair_satisfied_review_id == 41
        provider.list_issue_comments.assert_called_once_with(1)

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_head_changed_fails_closed_when_effective_review_commit_sha_missing(self, mock_gate) -> None:
        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider(review_commit_sha="")

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is True
        assert snapshot.repair_satisfied_review_id is None
        provider.list_issue_comments.assert_not_called()

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_repair_satisfied_review_id_populated_for_suppressed_only_block(self, mock_gate) -> None:
        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="copilot-swe-agent[bot]",
                body=f"{REPAIR_SATISFIED_MARKER}\n<!-- review-id:42 -->",
            ),
        ]

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is False
        assert snapshot.repair_satisfied_review_id == 42
        provider.list_issue_comments.assert_called_once_with(1)

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_repair_satisfied_review_id_none_when_no_marker(self, mock_gate) -> None:
        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider()
        provider.list_issue_comments.return_value = []

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.repair_satisfied_review_id is None

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_repair_satisfied_review_id_none_when_issue_comments_raise(self, mock_gate) -> None:
        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider()
        provider.list_issue_comments.side_effect = RuntimeError("boom")

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.repair_satisfied_review_id is None

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_repair_satisfied_review_id_none_when_provider_lacks_method(self, mock_gate) -> None:
        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider()
        provider.list_issue_comments = None  # not callable → branch skipped

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.repair_satisfied_review_id is None

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_repair_satisfied_review_id_none_when_not_suppressed_only(self, mock_gate) -> None:
        """A non-suppressed-only block does not fetch issue comments."""
        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_HAS_COMMENTS,
            review_id=42,
            body_comment_count=3,
            suppressed_count=0,
        )
        provider = _suppressed_marker_provider()

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.repair_satisfied_review_id is None
        provider.list_issue_comments.assert_not_called()

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_head_changed_fails_closed_when_no_copilot_reviews_in_fallback(self, mock_gate) -> None:
        """Fallback branch returns True (fail-closed) when no Copilot reviews exist."""
        mock_gate.return_value = CopilotGateVerdict(passed=True, reason="clean", review_id=0)
        provider = _suppressed_marker_provider()
        provider.list_reviews.return_value = []

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is True

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_head_changed_fails_closed_when_fallback_review_has_no_commit_sha(self, mock_gate) -> None:
        """Fallback branch returns True (fail-closed) when the latest Copilot review has no commit SHA."""
        mock_gate.return_value = CopilotGateVerdict(passed=True, reason="clean", review_id=0)
        provider = _suppressed_marker_provider()
        provider.list_reviews.return_value = [
            ReviewInfo(id=42, user="Copilot", state="COMMENTED", commit_sha=""),
        ]

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is True

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_head_changed_false_when_fallback_review_matches_head(self, mock_gate) -> None:
        """Fallback branch returns False when the latest Copilot review matches HEAD."""
        mock_gate.return_value = CopilotGateVerdict(passed=True, reason="clean", review_id=0)
        provider = _suppressed_marker_provider(review_commit_sha="head-sha", head_sha="head-sha")

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is False

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_head_changed_true_when_fallback_review_on_other_commit(self, mock_gate) -> None:
        """Fallback branch returns True when the latest Copilot review targets a non-HEAD commit."""
        mock_gate.return_value = CopilotGateVerdict(passed=True, reason="clean", review_id=0)
        provider = _suppressed_marker_provider(review_commit_sha="old-sha", head_sha="head-sha")

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.head_changed_since_review is True

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_suppressed_deferral_review_id_populated_from_marker(self, mock_gate) -> None:
        """suppressed_deferral_review_id is populated when a deferral marker exists."""
        import json

        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider()
        payload = json.dumps({"review_id": "42", "issue": 99, "active": True})
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="copilot",
                body=f"{SUPPRESSED_DEFERRAL_SENTINEL}{payload} -->",
            ),
        ]

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.suppressed_deferral_review_id == 42
        assert snapshot.suppressed_deferral_issue_number == 99

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_pr_token_login_exception_is_silenced(self, mock_gate) -> None:
        """get_pr_token_login raising falls back to static allowed set (fail-open)."""
        import json

        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider()
        provider.get_pr_token_login.side_effect = RuntimeError("token not set")
        payload = json.dumps({"review_id": "42", "issue": 99, "active": True})
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="copilot",
                body=f"{SUPPRESSED_DEFERRAL_SENTINEL}{payload} -->",
            ),
        ]

        # Exception from get_pr_token_login must not propagate; marker still found
        # via the static allowed set (author "copilot" is always trusted).
        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.suppressed_deferral_review_id == 42

    @patch("agentic_devtools.cli.ci.pipeline.snapshot.evaluate_copilot_gate_verdict")
    def test_pr_token_login_not_callable_is_skipped(self, mock_gate) -> None:
        """When get_pr_token_login is not callable, skip token resolution gracefully."""
        import json

        mock_gate.return_value = CopilotGateVerdict(
            passed=False,
            reason=REASON_SUPPRESSED_COMMENTS,
            review_id=42,
            body_comment_count=0,
            suppressed_count=2,
        )
        provider = _suppressed_marker_provider()
        provider.get_pr_token_login = None  # not callable → branch skipped
        payload = json.dumps({"review_id": "42", "issue": 99, "active": True})
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=1,
                author="copilot",
                body=f"{SUPPRESSED_DEFERRAL_SENTINEL}{payload} -->",
            ),
        ]

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.suppressed_deferral_review_id == 42
