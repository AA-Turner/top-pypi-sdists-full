"""Tests for find_stalled_unaddressed_reviews()."""

from datetime import UTC, datetime
from types import SimpleNamespace
from typing import cast
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.reconciliation.models import WorkflowRun
from agentic_devtools.cli.ci.retry import ProviderRateLimitError
from agentic_devtools.cli.ci.scheduler import EligiblePR
from agentic_devtools.cli.ci.watchdog_command import find_stalled_unaddressed_reviews

NOW = datetime(2026, 9, 16, 15, tzinfo=UTC)
OLD = "2026-09-16T14:00:00Z"
RECENT = "2026-09-16T14:55:00Z"


class TestFindStalledUnaddressedReviews:
    """Tests for stalled review detection."""

    @pytest.mark.parametrize("exhausted", [True, False])
    def test_skips_only_unchanged_exhausted_work(self, exhausted) -> None:
        provider = MagicMock()
        provider.list_eligible_prs.return_value = [EligiblePR(42, "")]
        provider.list_reviews.return_value = [ReviewInfo(10, "Copilot", "CHANGES_REQUESTED", submitted_at=OLD)]
        provider.list_workflow_runs.return_value = []
        provider.get_pr_metadata.return_value = SimpleNamespace(head_sha="head", head_branch="branch", pr_id=42)
        with (
            patch("agentic_devtools.cli.ci.repair_accounting.exhausted_repair_is_unchanged", return_value=exhausted),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=NOW),
            patch(
                "agentic_devtools.cli.ci.watchdog_command.is_copilot_session_active_via_agent_task", return_value=False
            ),
        ):
            assert find_stalled_unaddressed_reviews(provider, "o/r", "token") == ([] if exhausted else [42])

    def test_exhaustion_lookup_preserves_rate_limit_pause(self) -> None:
        provider = MagicMock()
        provider.list_eligible_prs.return_value = [EligiblePR(42, "")]
        provider.list_reviews.return_value = [ReviewInfo(10, "Copilot", "CHANGES_REQUESTED", submitted_at=OLD)]
        provider.list_workflow_runs.return_value = []
        with (
            patch(
                "agentic_devtools.cli.ci.repair_accounting.exhausted_repair_is_unchanged",
                side_effect=ProviderRateLimitError(provider="github"),
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=NOW),
            pytest.raises(ProviderRateLimitError),
        ):
            find_stalled_unaddressed_reviews(provider, "o/r", "token")

    def test_rejects_negative_age(self) -> None:
        with pytest.raises(ValueError, match="max_age_minutes"):
            find_stalled_unaddressed_reviews(cast(GitHubActionsProvider, object()), "o/r", "token", max_age_minutes=-1)

    def test_returns_empty_when_eligible_pr_lookup_fails(self, caplog) -> None:
        class _Provider:
            def list_eligible_prs(self, max_prs=None):
                raise RuntimeError("eligible PR lookup failed")

        assert find_stalled_unaddressed_reviews(cast(GitHubActionsProvider, _Provider()), "o/r", "token") == []
        assert "Could not inspect eligible PRs" in caplog.text

    def test_returns_empty_when_no_actionable_old_reviews_exist(self) -> None:
        class _Provider:
            def list_eligible_prs(self, max_prs=None):
                return [
                    EligiblePR(number=0, created_at=""),
                    EligiblePR(number=True, created_at=""),
                    EligiblePR(number=1, created_at=""),
                    EligiblePR(number=2, created_at=""),
                    EligiblePR(number=3, created_at=""),
                    EligiblePR(number=4, created_at=""),
                ]

            def list_reviews(self, pr_number):
                return {
                    1: [ReviewInfo(7, "reviewer", "APPROVED", submitted_at=OLD)],
                    2: [ReviewInfo(8, "reviewer", "CHANGES_REQUESTED", submitted_at="bad")],
                    3: [ReviewInfo(9, "reviewer", "CHANGES_REQUESTED", submitted_at=RECENT)],
                    4: [ReviewInfo(10, "reviewer", "COMMENTED", body="", submitted_at=OLD)],
                }[pr_number]

            def list_review_comments(self, pr_number, review_id):
                return []

        with patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=NOW):
            assert find_stalled_unaddressed_reviews(cast(GitHubActionsProvider, _Provider()), "o/r", "token") == []

    def test_skips_prs_whose_review_lookup_fails(self, caplog) -> None:
        class _Provider:
            def list_eligible_prs(self, max_prs=None):
                return [EligiblePR(number=42, created_at="")]

            def list_reviews(self, pr_number):
                raise RuntimeError("review lookup failed")

        with patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=NOW):
            assert find_stalled_unaddressed_reviews(cast(GitHubActionsProvider, _Provider()), "o/r", "token") == []
        assert "Could not inspect reviews for PR #42" in caplog.text

    def test_returns_empty_when_active_workflow_inventory_is_unavailable(self) -> None:
        class _Provider:
            def list_eligible_prs(self, max_prs=None):
                return [EligiblePR(number=42, created_at="")]

            def list_reviews(self, pr_number):
                return [ReviewInfo(7, "reviewer", "CHANGES_REQUESTED", submitted_at=OLD)]

            def list_workflow_runs(self, workflow_id, **kwargs):
                raise RuntimeError("workflow lookup failed")

        with (
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=NOW),
            patch(
                "agentic_devtools.cli.ci.watchdog_command.is_copilot_session_active_via_agent_task",
                return_value=False,
            ),
        ):
            assert find_stalled_unaddressed_reviews(cast(GitHubActionsProvider, _Provider()), "o/r", "token") == []

    def test_returns_only_reviews_without_active_processing(self, caplog) -> None:
        class _Provider:
            def list_eligible_prs(self, max_prs=None):
                return [
                    EligiblePR(number=42, created_at=""),
                    EligiblePR(number=43, created_at=""),
                    EligiblePR(number=44, created_at=""),
                    EligiblePR(number=45, created_at=""),
                    EligiblePR(number=46, created_at=""),
                ]

            def list_reviews(self, pr_number):
                return {
                    42: [ReviewInfo(7, "reviewer", "CHANGES_REQUESTED", submitted_at=OLD)],
                    43: [ReviewInfo(8, "reviewer", "COMMENTED", body="fix", submitted_at=OLD)],
                    44: [ReviewInfo(9, "reviewer", "CHANGES_REQUESTED", submitted_at=OLD)],
                    45: [ReviewInfo(10, "reviewer", "CHANGES_REQUESTED", submitted_at=OLD)],
                    46: [ReviewInfo(11, "reviewer", "CHANGES_REQUESTED", submitted_at=OLD)],
                }[pr_number]

            def list_review_comments(self, pr_number, review_id):
                return []

            def get_pr_metadata(self, pr_number):
                if pr_number == 45:
                    raise RuntimeError("metadata lookup failed")
                return type(
                    "Metadata",
                    (),
                    {"head_branch": f"feature/{pr_number}", "head_sha": "a" * 40, "pr_id": pr_number + 1000},
                )()

            def list_workflow_runs(self, workflow_id, **kwargs):
                return [
                    WorkflowRun(
                        id=99,
                        name="AI PR Loop",
                        conclusion="",
                        run_attempt=1,
                        created_at="2026-09-16T14:30:00Z",
                        event="workflow_dispatch",
                        head_branch="feature",
                        pr_number=44,
                    )
                ]

        def active_task(repo, pr_number, *, head_branch, head_sha, pr_id, provider):
            if pr_number == 43:
                return True
            if pr_number == 45:
                return False
            if pr_number == 46:
                raise RuntimeError("task lookup failed")
            assert head_branch == f"feature/{pr_number}"
            assert head_sha == "a" * 40
            assert pr_id == pr_number + 1000
            return False

        with (
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=NOW),
            patch(
                "agentic_devtools.cli.ci.watchdog_command.is_copilot_session_active_via_agent_task",
                side_effect=active_task,
            ),
        ):
            assert find_stalled_unaddressed_reviews(cast(GitHubActionsProvider, _Provider()), "o/r", "token") == [42]
        assert "Could not inspect metadata for PR #45" in caplog.text
        assert "Could not inspect active agent task for PR #46" in caplog.text
