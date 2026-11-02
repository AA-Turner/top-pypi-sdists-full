"""Shared provider fixtures for pipeline snapshot capability tests."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import PRMetadata, ReviewCommentInfo, ReviewInfo


def _make_provider() -> MagicMock:
    provider = MagicMock()
    provider.count_commits_behind.return_value = 0
    provider.get_approver_login.return_value = ""
    provider.compute_diff_files = None
    return provider


def _current_review_provider(
    comments: list[ReviewCommentInfo],
    thread_states: object,
    *,
    body: str = "",
    provider: MagicMock | None = None,
) -> MagicMock:
    provider = provider or _make_provider()
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


class _PromotionProvider(MagicMock):
    def promote_ccr_findings(self, **kwargs: object) -> list[ReviewCommentInfo]:
        calls = self.__dict__.setdefault("promotion_calls", [])
        calls.append(kwargs)
        error = self.__dict__.get("promotion_error", "")
        if error:
            raise RuntimeError(error)
        return []


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


def _provider_for_review(review: ReviewInfo) -> MagicMock:
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
    provider.list_reviews.return_value = [review]
    provider.list_review_threads_by_thread_id.return_value = {}
    provider.count_commits_above_merge_base.return_value = 1
    return provider
