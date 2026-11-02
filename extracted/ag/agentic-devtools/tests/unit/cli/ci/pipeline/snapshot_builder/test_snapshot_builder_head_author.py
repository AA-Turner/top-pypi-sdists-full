"""Tests for build_pr_state_snapshot."""

import pytest

from agentic_devtools.cli.ci.models import (
    PRMetadata,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from agentic_devtools.cli.ci.retry import ProviderRateLimitError
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _make_provider


class TestBuildPrStateSnapshot:
    """Tests for build_pr_state_snapshot behavior."""

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
