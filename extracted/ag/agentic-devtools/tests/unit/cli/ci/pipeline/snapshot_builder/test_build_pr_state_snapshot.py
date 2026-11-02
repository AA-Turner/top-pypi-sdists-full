"""Tests for build_pr_state_snapshot."""

from dataclasses import replace
from unittest.mock import Mock

from agentic_devtools.cli.ci.approver_preflight import (
    ApproverPreflightResult,
    CapabilityEvidence,
    EvidenceStatus,
)
from agentic_devtools.cli.ci.models import (
    CheckRunStatus,
    PRMetadata,
    ReviewInfo,
)
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_API_ERROR,
)
from agentic_devtools.cli.ci.pipeline.snapshot_builder import build_pr_state_snapshot
from tests.unit.cli.ci.pipeline._snapshot_fixtures import _current_review_provider, _make_provider, _PromotionProvider


class TestBuildPrStateSnapshot:
    """Tests for build_pr_state_snapshot behavior."""

    def test_optional_preflight_uses_actual_base_and_retains_existing_head_approval(self) -> None:
        provider = _current_review_provider([], {})
        provider.get_pr_metadata.return_value = replace(
            provider.get_pr_metadata.return_value,
            base_repo_full_name="actual/base",
        )
        preflight = ApproverPreflightResult(identity=CapabilityEvidence(EvidenceStatus.VERIFIED, "bot"))
        provider.get_approver_preflight = Mock(return_value=preflight)
        provider.list_reviews.return_value = [
            ReviewInfo(id=1, user="bot", state="APPROVED", commit_sha="head-sha"),
        ]
        snapshot = build_pr_state_snapshot(provider, 1)
        provider.get_approver_preflight.assert_called_once_with("actual/base")
        provider.get_approver_login.assert_not_called()
        assert snapshot.approver_preflight is preflight
        assert preflight.blocking_capability == "repository_visibility"
        assert snapshot.has_approver_approval_on_head is True
        assert snapshot.has_approval_on_head is True
        assert snapshot.approver_login == "bot"

    def test_missing_preflight_identity_never_uses_legacy_empty_login_bypass(self) -> None:
        provider = _current_review_provider([], {})
        provider.get_approver_preflight = Mock(return_value=ApproverPreflightResult())
        provider.get_approver_login.return_value = "bot"
        snapshot = build_pr_state_snapshot(provider, 1)
        assert snapshot.approver_preflight is not None
        assert snapshot.approver_login == ""
        assert snapshot.has_approver_approval_on_head is False
        provider.get_approver_login.assert_not_called()

    def test_provider_without_preflight_keeps_legacy_login_behavior(self) -> None:
        provider = _current_review_provider([], {})
        provider.get_approver_login.return_value = "legacy-bot"
        snapshot = build_pr_state_snapshot(provider, 1)
        assert snapshot.approver_preflight is None
        assert snapshot.approver_login == "legacy-bot"
        provider.get_approver_login.assert_called_once_with()

    def test_promotion_runs_during_snapshot_collection(self) -> None:
        provider = _current_review_provider([], {}, provider=_PromotionProvider())

        snapshot = build_pr_state_snapshot(provider, 1)

        assert len(provider.promotion_calls) == 1
        assert snapshot.copilot_gate_verdict is not None

    def test_snapshot_can_skip_finding_promotion(self) -> None:
        provider = _current_review_provider([], {}, provider=_PromotionProvider())

        snapshot = build_pr_state_snapshot(provider, 1, promote_findings=False)

        assert provider.__dict__.get("promotion_calls") is None
        assert snapshot.copilot_gate_verdict is not None

    def test_promotion_failure_forces_api_error_gate_verdict(self) -> None:
        provider = _current_review_provider([], {}, provider=_PromotionProvider())
        provider.promotion_error = "no diff anchor"

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.copilot_gate_verdict is not None
        assert snapshot.copilot_gate_verdict.passed is False
        assert snapshot.copilot_gate_verdict.reason == REASON_API_ERROR
        assert "no diff anchor" in snapshot.copilot_gate_verdict.details

    def test_codeql_configuration_is_required_for_snapshot_ci_status(self) -> None:
        provider = _current_review_provider([], {})
        provider.list_check_runs.return_value = [
            CheckRunStatus(
                id=1,
                name="Run Targeted Checks",
                status="completed",
                conclusion="success",
            )
        ]
        provider.is_codeql_configured.return_value = True

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.ci_status == "pending"
        provider.is_codeql_configured.assert_called_once_with(base_branch="main")

    def test_copies_pr_database_id_from_metadata(self) -> None:
        """The snapshot preserves the provider's PR database id for task correlation."""
        provider = _current_review_provider([], {})
        provider.get_pr_metadata.return_value = PRMetadata(
            number=1,
            pr_id=123456,
            title="Test PR",
            head_branch="feature",
            head_sha="head-sha",
            base_branch="main",
            requested_reviewers=[],
        )

        snapshot = build_pr_state_snapshot(provider, 1)

        assert snapshot.pr_id == 123456

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
