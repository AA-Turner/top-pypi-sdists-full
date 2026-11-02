"""Tests for build_pr_state_snapshot."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.models import (
    PRMetadata,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _make_provider


class TestBuildPrStateSnapshot:
    """Tests for build_pr_state_snapshot behavior."""

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
