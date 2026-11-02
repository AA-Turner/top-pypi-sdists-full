"""Tests for critique-specific dispatch gates."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.critique_adjudicator import build_critique_task_comment
from agentic_devtools.cli.ci.models import IssueCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions.dispatch_repair import DispatchRepairAction
from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_NEW_CCR_NOT_APPROVED, CopilotGateVerdict
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.provider import RepairDispatchBookkeepingRateLimitError
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def _zero_findings_headline_snapshot(headline: str, classification: str) -> PRStateSnapshot:
    body = f"<!-- ccr-overview-v2 -->\n### Needs a closer look\n\n{headline}\n\n0 open findings"
    return PRStateSnapshot(
        pr_number=42,
        head_sha="head",
        base_repo_full_name="owner/repo",
        ci_status="passing",
        review_state="COMMENTED",
        effective_review_comment_count=0,
        effective_review_comment_count_review_id=100,
        effective_review_comment_filter_applied=False,
        reviews=[ReviewInfo(100, "copilot[bot]", "COMMENTED", body, "head")],
        copilot_gate_verdict=CopilotGateVerdict(False, REASON_NEW_CCR_NOT_APPROVED, 100, body_comment_count=0),
        critique_headline_classification=classification,
    )


def _critique_dispatch_provider(receipt: int | str) -> MagicMock:
    provider = MagicMock()
    comments: dict[int, str] = {}

    def find_comment(_pr_number: int, marker: str):
        return next(((comment_id, body) for comment_id, body in comments.items() if marker in body), None)

    def list_issue_comments(_pr_number: int) -> list[IssueCommentInfo]:
        return [IssueCommentInfo(comment_id, "github-actions[bot]", body) for comment_id, body in comments.items()]

    def post_comment(_pr_number: int, body: str) -> int:
        comment_id = len(comments) + 1
        comments[comment_id] = body
        return comment_id

    def update_comment(comment_id: int, body: str) -> None:
        comments[comment_id] = body

    provider.get_pr_token_login.return_value = "github-actions[bot]"
    provider.get_trusted_loop_comment_logins.return_value = {"github-actions[bot]"}
    provider.find_comment.side_effect = find_comment
    provider.list_issue_comments.side_effect = list_issue_comments
    provider.list_review_comments.return_value = []
    provider.list_review_thread_states.return_value = {}
    provider.post_comment.side_effect = post_comment
    provider.post_comment_as_pr_token.side_effect = post_comment
    provider.update_comment.side_effect = update_comment
    provider.update_comment_as_pr_token.side_effect = update_comment
    provider.dispatch_repair.return_value = receipt
    return provider


def test_execute_returns_at_approval_worthy_skip_gate() -> None:
    snapshot = _zero_findings_headline_snapshot(
        "Broad modernization and limited baseline verification require final human review.",
        "approval_worthy",
    )
    provider = MagicMock()

    result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

    assert result.decision is ActionDecision.SKIP
    provider.dispatch_repair.assert_not_called()


def test_critique_task_receipt_is_bound_when_ledger_write_fails() -> None:
    snapshot = _zero_findings_headline_snapshot("A concrete parser regression remains.", "critique")
    provider = _critique_dispatch_provider("task:owner/repo:task-123")

    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
            return_value=(False, 0),
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
            return_value=(False, 0),
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.record",
            side_effect=RuntimeError("receipt write failed"),
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.bind_dispatched_critique_task",
            return_value=None,
        ) as bind,
    ):
        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

    assert result.decision is ActionDecision.EXECUTE
    assert bind.call_args.args[0] is provider
    assert bind.call_args.args[3] == "task:owner/repo:task-123"


def test_critique_task_receipt_is_bound_on_bookkeeping_rate_limit() -> None:
    snapshot = _zero_findings_headline_snapshot("A concrete parser regression remains.", "critique")
    quota_error = ProviderRateLimitError(provider="github", is_rate_limit=True)
    dispatch_error = RepairDispatchBookkeepingRateLimitError("task:owner/repo:task-123", quota_error)
    provider = _critique_dispatch_provider(dispatch_error.receipt)
    provider.dispatch_repair.side_effect = dispatch_error

    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
            return_value=(False, 0),
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
            return_value=(False, 0),
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.bind_dispatched_critique_task",
            return_value=None,
        ) as bind,
        pytest.raises(ProviderRateLimitError) as exc_info,
    ):
        DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

    assert exc_info.value is dispatch_error
    assert bind.call_args.args[0] is provider
    assert bind.call_args.args[3] == dispatch_error.receipt


def test_binding_reconciliation_failure_stops_another_dispatch() -> None:
    snapshot = _zero_findings_headline_snapshot("A concrete parser regression remains.", "critique")
    provider = _critique_dispatch_provider("task:owner/repo:task-123")
    failure = ActionResult(name="dispatch_repair", decision=ActionDecision.FAILED, error="binding unresolved")

    with patch(
        "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.reconcile_existing_critique_task_binding",
        return_value=failure,
    ):
        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

    assert result is failure
    provider.dispatch_repair.assert_not_called()


def test_reconciles_existing_critique_task_before_no_pending_work_skip() -> None:
    snapshot = _zero_findings_headline_snapshot("A concrete parser regression remains.", "critique")
    provider = _critique_dispatch_provider("task:owner/repo:task-123")
    attempts = MagicMock()
    attempts.attempted = {"critique:100:1"}
    attempts.resolved_ids.return_value = set()
    attempts.filter_review.return_value = []
    failure = ActionResult(name="dispatch_repair", decision=ActionDecision.FAILED, error="binding unresolved")

    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairAttemptTracker",
            return_value=attempts,
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.reconcile_existing_critique_task_binding",
            return_value=failure,
        ) as reconcile,
    ):
        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

    assert result is failure
    reconcile.assert_called_once()
    provider.dispatch_repair.assert_not_called()


def test_reconciles_existing_critique_task_before_attempt_cap_skip() -> None:
    snapshot = _zero_findings_headline_snapshot("A concrete parser regression remains.", "critique")
    provider = _critique_dispatch_provider("task:owner/repo:task-123")
    attempts = MagicMock()
    attempts.attempted = {"critique:100:1", "critique:100:2"}
    attempts.resolved_ids.return_value = set()
    failure = ActionResult(name="dispatch_repair", decision=ActionDecision.FAILED, error="binding unresolved")

    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairAttemptTracker",
            return_value=attempts,
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.critique_dispatch.register_review_attempt",
            return_value=(ActionResult(name="dispatch_repair", decision=ActionDecision.SKIP, details="attempt cap"), 0),
        ),
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.reconcile_existing_critique_task_binding",
            return_value=failure,
        ) as reconcile,
    ):
        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

    assert result is failure
    reconcile.assert_called_once()
    provider.dispatch_repair.assert_not_called()


def test_unbound_critique_task_is_reconciled_before_attempt_cap() -> None:
    snapshot = _zero_findings_headline_snapshot("A concrete parser regression remains.", "critique")
    provider = _critique_dispatch_provider("task:owner/repo:task-123")
    provider.post_comment(
        42,
        '<!-- repair-dispatch-findings:42:head:v1 -->\n{"attempted": ["critique:100:1", "critique:100:2"]}',
    )
    provider.post_comment_as_pr_token(42, build_critique_task_comment(42, "head", 100, 1))

    with patch(
        "agentic_devtools.cli.ci.repair_accounting.RepairDispatchLedger.read",
        return_value=({"task:owner/repo:task-123"}, False, 3),
    ):
        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

    assert result.decision is ActionDecision.SKIP
    assert "Critique repair task cap reached" in result.details
    assert "critique-task-id task=task-123" in provider.find_comment(42, "critique-task")[1]
    provider.dispatch_repair.assert_not_called()


def test_registered_attempt_result_stops_repair_dispatch() -> None:
    snapshot = _zero_findings_headline_snapshot(
        "Previously reported parser regressions remain unresolved and can lose findings or block promotion.",
        "critique",
    )
    provider = MagicMock()
    provider.list_issue_comments.return_value = []
    provider.list_review_comments.return_value = []
    provider.list_review_thread_states.return_value = {}
    attempt_result = ActionResult(name="dispatch_repair", decision=ActionDecision.SKIP, details="attempt cap")

    with patch(
        "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.critique_dispatch.register_review_attempt",
        return_value=(attempt_result, 0),
    ) as register:
        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

    assert result is attempt_result
    register.assert_called_once()
    provider.dispatch_repair.assert_not_called()
