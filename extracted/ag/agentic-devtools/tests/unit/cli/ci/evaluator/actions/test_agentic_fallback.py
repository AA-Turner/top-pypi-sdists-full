"""Tests for agentic_fallback action handler."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.evaluator.actions import agentic_fallback
from agentic_devtools.cli.ci.evaluator.models import (
    PostAgentAction,
    PostAgentClassification,
    PostAgentSnapshot,
    ThreadInfo,
)
from agentic_devtools.cli.ci.models import ReviewCommentInfo
from agentic_devtools.cli.ci.provider import (
    RepairDispatchBookkeepingRateLimitError,
    RepairDispatchNotAttemptedError,
)
from agentic_devtools.cli.ci.repair_accounting import repair_work_key
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class TestAgenticFallback:
    """Tests for agentic_fallback action."""

    def test_dry_run(self):
        """Dry run reports success without dispatching."""
        snap = PostAgentSnapshot(pr_number=42, current_head_sha="abc", review_id=100)
        provider = MagicMock()

        result = agentic_fallback(provider, snap, dry_run=True)

        assert result.dry_run is True
        assert result.action_taken == PostAgentAction.agentic_fallback
        assert result.success is True
        provider.dispatch_repair.assert_not_called()

    def test_dispatches_repair(self):
        """Dispatches repair with correct parameters."""
        snap = PostAgentSnapshot(pr_number=42, current_head_sha="abc123", review_id=100)
        provider = MagicMock()
        provider.dispatch_repair.return_value = "task:confirmed"

        with (
            patch(
                "agentic_devtools.cli.ci.evaluator.actions.check_deduplication",
                return_value=(False, 0),
            ) as check_deduplication,
            patch("agentic_devtools.cli.ci.evaluator.actions.RepairDispatchLedger") as ledger_class,
        ):
            result = agentic_fallback(provider, snap, dry_run=False)

        assert result.success is True
        provider.dispatch_repair.assert_called_once_with(
            pr_number=42,
            head_sha="abc123",
            repair_type="review",
            failed_checks=[],
            review_comments=[],
            review_id=100,
        )
        check_deduplication.assert_called_once_with(
            provider,
            42,
            "abc123",
            max_dispatches=3,
            review_id=100,
            work_key=repair_work_key(100, [], []),
        )
        ledger = ledger_class.return_value
        ledger.reconcile.assert_called_once_with()
        ledger.begin.assert_called_once_with()
        ledger.record.assert_called_once_with("task:confirmed")

    def test_scopes_and_dispatches_only_unresolved_root_findings(self):
        """Uses the same unresolved root findings for accounting and dispatch."""
        unresolved = ReviewCommentInfo(
            id=11,
            path="src/app.py",
            body="Fix this finding",
            html_url="https://example.test/comments/11",
            source_review_id=70,
        )
        reply = ReviewCommentInfo(
            id=12,
            path="src/app.py",
            body="Reply",
            html_url="https://example.test/comments/12",
            source_review_id=70,
            in_reply_to_id=11,
        )
        resolved = ReviewCommentInfo(
            id=22,
            path="src/other.py",
            body="Already resolved",
            html_url="https://example.test/comments/22",
            source_review_id=80,
        )
        snap = PostAgentSnapshot(
            pr_number=42,
            current_head_sha="abc123",
            review_id=100,
            threads=(
                ThreadInfo(comment_id=11),
                ThreadInfo(comment_id=12),
                ThreadInfo(comment_id=22, is_resolved=True),
            ),
        )
        provider = MagicMock()
        provider.list_review_comments.return_value = [unresolved, reply, resolved]
        provider.dispatch_repair.return_value = "task:confirmed"

        with (
            patch(
                "agentic_devtools.cli.ci.evaluator.actions.check_deduplication",
                return_value=(False, 0),
            ) as check_deduplication,
            patch("agentic_devtools.cli.ci.evaluator.actions.RepairDispatchLedger"),
        ):
            result = agentic_fallback(provider, snap)

        assert result.success is True
        provider.list_review_comments.assert_called_once_with(42, 100)
        provider.dispatch_repair.assert_called_once_with(
            pr_number=42,
            head_sha="abc123",
            repair_type="review",
            failed_checks=[],
            review_comments=[unresolved],
            review_id=100,
        )
        check_deduplication.assert_called_once_with(
            provider,
            42,
            "abc123",
            max_dispatches=3,
            review_id=100,
            work_key=repair_work_key(100, [unresolved], []),
        )

    def test_loads_reply_parent_from_an_older_review(self):
        """Uses the PR-wide inventory to recover a reply's root from another review."""
        root = ReviewCommentInfo(
            id=11,
            path="src/app.py",
            body="Original finding",
            html_url="https://example.test/comments/11",
            source_review_id=70,
        )
        reply = ReviewCommentInfo(
            id=22,
            path="src/app.py",
            body="Follow-up",
            html_url="https://example.test/comments/22",
            source_review_id=100,
            in_reply_to_id=11,
        )
        snap = PostAgentSnapshot(
            pr_number=42,
            current_head_sha="abc123",
            review_id=100,
            threads=(ThreadInfo(comment_id=22),),
        )
        provider = MagicMock()
        provider.list_all_review_comments.return_value = [root, reply]
        provider.list_review_comments.return_value = [reply]
        provider.dispatch_repair.return_value = "task:confirmed"

        with (
            patch(
                "agentic_devtools.cli.ci.evaluator.actions.check_deduplication",
                return_value=(False, 0),
            ),
            patch("agentic_devtools.cli.ci.evaluator.actions.RepairDispatchLedger"),
        ):
            result = agentic_fallback(provider, snap)

        assert result.success is True
        provider.list_all_review_comments.assert_called_once_with(42)
        provider.list_review_comments.assert_called_once_with(42, 100)
        assert provider.dispatch_repair.call_args.kwargs["review_comments"] == [root]

    def test_fails_closed_when_unresolved_finding_inventory_cannot_be_loaded(self):
        """Does not dispatch when unresolved findings cannot be fingerprinted."""
        snap = PostAgentSnapshot(
            pr_number=42,
            current_head_sha="abc123",
            review_id=100,
            threads=(ThreadInfo(comment_id=11),),
        )
        provider = MagicMock()
        provider.list_review_comments.side_effect = RuntimeError("inventory unavailable")

        with patch("agentic_devtools.cli.ci.evaluator.actions.RepairDispatchLedger"):
            result = agentic_fallback(provider, snap)

        assert result.success is False
        assert "inventory unavailable" in result.error_details
        provider.dispatch_repair.assert_not_called()

    def test_handles_dispatch_failure(self):
        """Reports failure when dispatch_repair raises."""
        snap = PostAgentSnapshot(pr_number=42, current_head_sha="abc", review_id=1)
        provider = MagicMock()
        provider.dispatch_repair.side_effect = RuntimeError("dispatch failed")

        with (
            patch(
                "agentic_devtools.cli.ci.evaluator.actions.check_deduplication",
                return_value=(False, 0),
            ),
            patch("agentic_devtools.cli.ci.evaluator.actions.RepairDispatchLedger") as ledger_class,
        ):
            result = agentic_fallback(provider, snap, dry_run=False)

        assert result.success is False
        assert "dispatch failed" in result.error_details
        ledger = ledger_class.return_value
        ledger.begin.assert_called_once_with()
        ledger.retire_pending.assert_not_called()

    def test_records_confirmed_receipt_before_reporting_bookkeeping_quota_error(self):
        snap = PostAgentSnapshot(pr_number=42, current_head_sha="abc", review_id=1)
        provider = MagicMock()
        rate_limit = ProviderRateLimitError(provider="github", is_rate_limit=True)
        provider.dispatch_repair.side_effect = RepairDispatchBookkeepingRateLimitError("task:confirmed", rate_limit)

        with (
            patch(
                "agentic_devtools.cli.ci.evaluator.actions.check_deduplication",
                return_value=(False, 0),
            ),
            patch("agentic_devtools.cli.ci.evaluator.actions.RepairDispatchLedger") as ledger_class,
        ):
            result = agentic_fallback(provider, snap, dry_run=False)

        assert result.success is False
        assert "Provider rate limit exhausted" in result.error_details
        ledger_class.return_value.record.assert_called_once_with("task:confirmed")

    def test_reports_quota_and_unresolved_receipt_when_both_writes_fail(self):
        snap = PostAgentSnapshot(pr_number=42, current_head_sha="abc", review_id=1)
        provider = MagicMock()
        quota_error = ProviderRateLimitError(provider="github", is_rate_limit=True)
        provider.dispatch_repair.side_effect = RepairDispatchBookkeepingRateLimitError("task:confirmed", quota_error)

        with (
            patch(
                "agentic_devtools.cli.ci.evaluator.actions.check_deduplication",
                return_value=(False, 0),
            ),
            patch("agentic_devtools.cli.ci.evaluator.actions.RepairDispatchLedger") as ledger_class,
        ):
            ledger_class.return_value.record.side_effect = RuntimeError("receipt write failed")
            result = agentic_fallback(provider, snap, dry_run=False)

        assert result.success is False
        assert "Provider rate limit exhausted" in result.error_details
        assert "task:confirmed" in result.error_details
        assert "accounting unresolved" in result.error_details
        assert "receipt write failed" in result.error_details
        ledger_class.return_value.record.assert_called_once_with("task:confirmed")

    def test_retires_intent_when_provider_confirms_no_creation_attempt(self):
        """Retires intent only when the provider confirms dispatch never started."""
        snap = PostAgentSnapshot(pr_number=42, current_head_sha="abc", review_id=1)
        provider = MagicMock()
        provider.dispatch_repair.side_effect = RepairDispatchNotAttemptedError("missing token")

        with (
            patch(
                "agentic_devtools.cli.ci.evaluator.actions.check_deduplication",
                return_value=(False, 0),
            ),
            patch("agentic_devtools.cli.ci.evaluator.actions.RepairDispatchLedger") as ledger_class,
        ):
            result = agentic_fallback(provider, snap, dry_run=False)

        assert result.success is False
        assert "missing token" in result.error_details
        ledger_class.return_value.retire_pending.assert_called_once_with()

    def test_skips_dispatch_when_scoped_budget_is_exhausted(self):
        """Does not create another repair after the scoped receipt cap is reached."""
        snap = PostAgentSnapshot(pr_number=42, current_head_sha="abc", review_id=100)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.evaluator.actions.check_deduplication",
                return_value=(True, 3),
            ),
            patch("agentic_devtools.cli.ci.evaluator.actions.RepairDispatchLedger") as ledger_class,
        ):
            result = agentic_fallback(provider, snap, dry_run=False)

        assert result.success is False
        assert "budget exhausted" in result.error_details
        provider.dispatch_repair.assert_not_called()
        ledger_class.return_value.reconcile.assert_called_once_with()
        ledger_class.return_value.begin.assert_not_called()

    def test_uses_single_dispatch_cap_without_a_review_id(self):
        """Uses the CI-only dispatch cap when the evaluator has no review identity."""
        snap = PostAgentSnapshot(pr_number=42, current_head_sha="abc", review_id=0)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.evaluator.actions.check_deduplication",
                return_value=(True, 1),
            ) as check_deduplication,
            patch("agentic_devtools.cli.ci.evaluator.actions.RepairDispatchLedger"),
        ):
            result = agentic_fallback(provider, snap, dry_run=False)

        assert result.success is False
        assert "1/1" in result.error_details
        assert check_deduplication.call_args.kwargs["max_dispatches"] == 1
        provider.dispatch_repair.assert_not_called()

    def test_fails_closed_when_prior_accounting_cannot_be_reconciled(self):
        """Does not dispatch when unresolved accounting prevents safe retry."""
        snap = PostAgentSnapshot(pr_number=42, current_head_sha="abc", review_id=1)
        provider = MagicMock()

        with patch("agentic_devtools.cli.ci.evaluator.actions.RepairDispatchLedger") as ledger_class:
            ledger_class.return_value.reconcile.side_effect = RuntimeError("pending receipt")
            result = agentic_fallback(provider, snap, dry_run=False)

        assert result.success is False
        assert "pending receipt" in result.error_details
        provider.dispatch_repair.assert_not_called()

    def test_propagates_rate_limit_while_reconciling_prior_accounting(self):
        snap = PostAgentSnapshot(pr_number=42, current_head_sha="abc", review_id=1)
        provider = MagicMock()
        quota = ProviderRateLimitError(
            retry_after_seconds=45,
            provider="github",
            credential_identity="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
        )

        with (
            patch("agentic_devtools.cli.ci.evaluator.actions.RepairDispatchLedger") as ledger_class,
            pytest.raises(ProviderRateLimitError) as exc_info,
        ):
            ledger_class.return_value.reconcile.side_effect = quota
            agentic_fallback(provider, snap, dry_run=False)

        assert exc_info.value is quota
        provider.dispatch_repair.assert_not_called()

    def test_does_not_clear_existing_intent_when_begin_fails(self):
        """Preserves possible earlier intent when begin cannot confirm its write."""
        snap = PostAgentSnapshot(pr_number=42, current_head_sha="abc", review_id=1)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.evaluator.actions.check_deduplication",
                return_value=(False, 0),
            ),
            patch("agentic_devtools.cli.ci.evaluator.actions.RepairDispatchLedger") as ledger_class,
        ):
            ledger_class.return_value.begin.side_effect = RuntimeError("intent not confirmed")
            result = agentic_fallback(provider, snap, dry_run=False)

        assert result.success is False
        assert "intent not confirmed" in result.error_details
        ledger_class.return_value.retire_pending.assert_not_called()
        provider.dispatch_repair.assert_not_called()

    def test_reports_confirmed_dispatch_when_receipt_recording_fails(self):
        """Does not report success when confirmed creation accounting is unresolved."""
        snap = PostAgentSnapshot(pr_number=42, current_head_sha="abc", review_id=1)
        provider = MagicMock()
        provider.dispatch_repair.return_value = "task:confirmed"

        with (
            patch(
                "agentic_devtools.cli.ci.evaluator.actions.check_deduplication",
                return_value=(False, 0),
            ),
            patch("agentic_devtools.cli.ci.evaluator.actions.RepairDispatchLedger") as ledger_class,
        ):
            ledger_class.return_value.record.side_effect = RuntimeError("record failed")
            result = agentic_fallback(provider, snap, dry_run=False)

        assert result.success is False
        assert "accounting unresolved" in result.error_details
        provider.dispatch_repair.assert_called_once()
        ledger_class.return_value.record.assert_called_once_with("task:confirmed")

    def test_reports_when_precreation_intent_cannot_be_retired(self):
        """Keeps the accounting failure visible after a confirmed no-request failure."""
        snap = PostAgentSnapshot(pr_number=42, current_head_sha="abc", review_id=1)
        provider = MagicMock()
        provider.dispatch_repair.side_effect = RepairDispatchNotAttemptedError("missing token")

        with (
            patch(
                "agentic_devtools.cli.ci.evaluator.actions.check_deduplication",
                return_value=(False, 0),
            ),
            patch("agentic_devtools.cli.ci.evaluator.actions.RepairDispatchLedger") as ledger_class,
        ):
            ledger_class.return_value.retire_pending.side_effect = RuntimeError("retire failed")
            result = agentic_fallback(provider, snap, dry_run=False)

        assert result.success is False
        assert "intent retirement failed" in result.error_details

    def test_classification_in_result(self):
        """Result has agent_silent classification."""
        snap = PostAgentSnapshot(pr_number=42)
        provider = MagicMock()

        result = agentic_fallback(provider, snap, dry_run=True)

        assert result.classification == PostAgentClassification.agent_silent
