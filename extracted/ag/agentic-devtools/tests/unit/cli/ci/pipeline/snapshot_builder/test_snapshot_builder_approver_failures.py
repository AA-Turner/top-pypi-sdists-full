"""Tests for build_pr_state_snapshot."""

import logging

import pytest

from agentic_devtools.cli.ci.models import (
    PRMetadata,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _make_provider


class TestBuildPrStateSnapshot:
    """Tests for build_pr_state_snapshot behavior."""

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

        with caplog.at_level(logging.DEBUG, logger="agentic_devtools.cli.ci.pipeline.snapshot_builder"):
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
