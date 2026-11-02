"""Tests for build_pr_state_snapshot."""

from agentic_devtools.cli.ci.models import (
    PRMetadata,
    ReviewCommentInfo,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _current_review_provider, _make_provider


class TestBuildPrStateSnapshot:
    """Tests for count_effective_review_comments()."""

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

    def test_effective_review_comment_count_is_unknown_for_non_mapping_thread_state(self) -> None:
        provider = _current_review_provider([], [])

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
