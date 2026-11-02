"""Tests for DispatchRepairAction."""

from collections.abc import Iterator
from dataclasses import replace
from unittest.mock import ANY, MagicMock, patch

import pytest

from agentic_devtools.cli.ci.models import CheckRunStatus, IssueCommentInfo, ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions.dispatch_repair import DispatchRepairAction
from agentic_devtools.cli.ci.pipeline.exclusion import ExclusionContext
from agentic_devtools.cli.ci.pipeline.gate_verdict import (
    REASON_AWAITING_FRESH,
    REASON_CLEAN,
    REASON_CONTENT_CHANGED,
    REASON_HAS_COMMENTS,
    REASON_NEW_CCR_NOT_APPROVED,
    REASON_SUPPRESSED_COMMENTS,
    REASON_UNPARSED_SUPPRESSION,
    CopilotGateVerdict,
)
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.repair_attempts import RepairAttemptTracker
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.provider import (
    RepairDispatchBookkeepingRateLimitError,
    RepairDispatchNotAttemptedError,
)
from agentic_devtools.cli.ci.repair_accounting import repair_work_key
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


@pytest.fixture(autouse=True)
def _mock_inactive_session_detector() -> Iterator[None]:
    """Default all tests to known-inactive session inventory."""
    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
            return_value=False,
        ),
        patch("agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.begin"),
        patch("agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.record"),
        patch("agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.reconcile"),
    ):
        yield


@pytest.fixture(autouse=True)
def _valid_provider_evidence() -> Iterator[None]:
    """Old action tests default to successful empty provider evidence, not mocks."""
    mock_type = MagicMock

    def configured_mock(*args, **kwargs):
        if "id" in kwargs:
            return ReviewCommentInfo(
                id=kwargs["id"],
                path=kwargs.get("path", ""),
                body=kwargs.get("body", ""),
                html_url=kwargs.get("html_url", ""),
                source_review_id=kwargs.get("source_review_id", 0),
                author_login=kwargs.get("author_login", ""),
                in_reply_to_id=kwargs.get("in_reply_to_id"),
            )
        provider = mock_type(*args, **kwargs)
        stored: dict[int, str] = {}

        def find_comment(pr_number: int, marker: str):
            return next(((key, body) for key, body in stored.items() if marker in body), None)

        def list_issue_comments(pr_number: int) -> list[IssueCommentInfo]:
            return [
                IssueCommentInfo(id=comment_id, author="github-actions[bot]", body=body)
                for comment_id, body in stored.items()
            ]

        def post_comment(pr_number: int, body: str) -> int:
            key = len(stored) + 1
            stored[key] = body
            return key

        def update_comment(comment_id: int, body: str) -> None:
            stored[comment_id] = body

        provider.find_comment.side_effect = find_comment
        provider.get_pr_token_login.return_value = "github-actions[bot]"
        provider.list_issue_comments.side_effect = list_issue_comments
        provider.list_review_comments.return_value = []
        provider.list_review_thread_states.return_value = {}
        provider.post_comment.side_effect = post_comment
        provider.post_comment_as_pr_token.side_effect = post_comment
        provider.update_comment.side_effect = update_comment
        return provider

    with patch(__name__ + ".MagicMock", side_effect=configured_mock):
        yield


class TestDispatchRepairAction:
    """Tests for dispatch repair action evaluation."""

    def test_confirmed_task_receipt_is_recorded_before_quota_pause(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="head", ci_status="failing")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        rate_limit = ProviderRateLimitError(provider="github", is_rate_limit=True)
        error = RepairDispatchBookkeepingRateLimitError("task:owner/repo:9999", rate_limit)
        provider.dispatch_repair.side_effect = error
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch("agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.record") as record,
            pytest.raises(ProviderRateLimitError) as exc_info,
        ):
            DispatchRepairAction().execute(provider, snapshot, derived)

        assert exc_info.value is error
        assert record.call_args.args[0] == "task:owner/repo:9999"
        assert derived.repair_dispatched is True

    def test_receipt_write_failure_does_not_replace_dispatch_quota_error(self, caplog) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="head", ci_status="failing")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        quota_error = ProviderRateLimitError(provider="github", is_rate_limit=True)
        dispatch_error = RepairDispatchBookkeepingRateLimitError("task:confirmed", quota_error)
        provider.dispatch_repair.side_effect = dispatch_error
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.record",
                side_effect=RuntimeError("receipt write failed"),
            ) as record,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.retire_pending"
            ) as retire,
            pytest.raises(ProviderRateLimitError) as exc_info,
        ):
            DispatchRepairAction().execute(provider, snapshot, derived)

        assert exc_info.value is dispatch_error
        record.assert_called_once_with("task:confirmed")
        retire.assert_not_called()
        assert "task:confirmed" in caplog.text
        assert "receipt write failed" in caplog.text

    def test_filtered_review_work_does_not_apply_stale_trigger_to_ci_only_repair(self):
        root = ReviewCommentInfo(101, "x.py", "finding", "", source_review_id=10)
        reply = replace(root, id=102, in_reply_to_id=101, author_login="copilot-swe-agent[bot]", body="Fixed")
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="head",
            ci_status="failing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=10,
        )
        provider = MagicMock()
        provider.list_review_comments.return_value = [root, reply]
        provider.list_review_thread_states.return_value = {}
        provider.dispatch_repair.return_value = 77
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger", return_value=True
            ) as trigger,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit", return_value=(False, 0)
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication", return_value=(False, 0)
            ) as dedup,
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))
        assert result.decision is ActionDecision.EXECUTE
        trigger.assert_not_called()
        assert dedup.call_args.kwargs["review_id"] == 0
        assert dedup.call_args.kwargs["max_dispatches"] == 1
        assert provider.dispatch_repair.call_args.kwargs["repair_type"] == "ci"

    def test_failed_intent_write_does_not_consume_first_repair_attempt(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="head", ci_status="failing")
        provider = MagicMock()
        provider.dispatch_repair.return_value = 77
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.begin",
                side_effect=[RuntimeError("intent write failed"), None],
            ) as begin,
        ):
            action = DispatchRepairAction()
            first_result = action.execute(provider, snapshot, DerivedState(snapshot))
            provider.post_comment.assert_not_called()
            second_result = action.execute(provider, snapshot, DerivedState(snapshot))

        assert first_result.decision is ActionDecision.FAILED
        assert second_result.decision is ActionDecision.EXECUTE
        assert begin.call_count == 2
        provider.dispatch_repair.assert_called_once()
        assert provider.post_comment.call_count == 1

    @pytest.mark.parametrize("retirement_error", [None, RuntimeError("retirement failed")])
    def test_reservation_failure_retires_intent_before_returning(self, retirement_error) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="head", ci_status="failing")
        provider = MagicMock()
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairAttemptTracker.reserve",
                side_effect=RuntimeError("reservation failed"),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.retire_pending",
                side_effect=retirement_error,
            ) as retire_pending,
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.FAILED
        assert "reservation failed" in result.error
        if retirement_error is not None:
            assert "intent retirement failed: retirement failed" in result.error
        retire_pending.assert_called_once()
        provider.dispatch_repair.assert_not_called()

    def test_review_only_work_key_excludes_already_reserved_ci_checks(self) -> None:
        failed_check = CheckRunStatus(id=1, name="Build", status="completed", conclusion="failure")
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="head",
            ci_status="failing",
            ci_failed_checks=["Build"],
            check_runs=[failed_check],
            review_state="CHANGES_REQUESTED",
            copilot_review_id=10,
        )
        provider = MagicMock()
        provider.post_comment(
            42,
            '<!-- repair-dispatch-findings:42:head:v1 -->\n{"attempted": ["ci"]}',
        )
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="x.py", body="Fix", html_url="", source_review_id=10)
        ]
        provider.list_review_thread_states.return_value = {}

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.repair_work_key",
                return_value="review-scope",
            ) as work_key,
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.EXECUTE
        assert work_key.call_args.args[2] == []
        assert provider.dispatch_repair.call_args.kwargs["repair_type"] == "review"

    def test_ci_only_exhaustion_scope_keeps_failed_checks_in_work_key(self) -> None:
        failed_check = CheckRunStatus(id=1, name="Build", status="completed", conclusion="failure")
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="head",
            ci_status="failing",
            ci_failed_checks=["Build"],
            check_runs=[failed_check],
        )
        provider = MagicMock()
        provider.post_comment(
            42,
            '<!-- repair-dispatch-findings:42:head:v1 -->\n{"attempted": ["ci"]}',
        )

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.repair_work_key",
                return_value="ci-scope",
            ) as work_key,
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.SKIP
        assert work_key.call_args.args[2] == [failed_check]

    @pytest.mark.parametrize("failure", ["begin", "record"])
    def test_accounting_failure_preserves_external_creation_outcome(self, failure) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="head", ci_status="failing")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 77
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                f"agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.{failure}",
                side_effect=RuntimeError("persistence failed"),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)
        if failure == "record":
            assert result.decision is ActionDecision.EXECUTE
            assert derived.repair_dispatched is True
            assert result.definitive_no_mutation is False
            assert "accounting unresolved" in result.details
        else:
            assert result.decision is ActionDecision.FAILED
            provider.dispatch_repair.assert_not_called()

    def test_exhaustion_has_scope_status_and_watchdog_marker(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="head", ci_status="failing")
        provider = MagicMock()
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(True, 1),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.repair_observation_key",
                return_value="a" * 64,
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))
        assert result.repair_exhaustion_marker == f"<!-- repair-dispatch:exhausted:head:{'a' * 64} -->"
        assert "confirmed=1/1" in result.details
        assert "review=0" in result.details
        assert "remaining work" in result.details

    def test_reserved_ci_work_reports_exhaustion_when_ledger_cap_is_reached(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="head", ci_status="failing")
        provider = MagicMock()
        attempts = MagicMock()
        attempts.attempted = {"ci"}
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairAttemptTracker",
                return_value=attempts,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(True, 1),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.repair_observation_key",
                return_value="a" * 64,
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.SKIP
        assert result.dedup_limit_reached
        assert result.repair_exhaustion_marker == f"<!-- repair-dispatch:exhausted:head:{'a' * 64} -->"

    def test_reserved_unresolved_review_work_uses_capped_review_ledger(self) -> None:
        root = ReviewCommentInfo(id=101, path="a.py", body="Fix", html_url="")
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="head",
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
        )
        provider = MagicMock()
        provider.list_review_comments.return_value = [root]
        provider.list_review_thread_states.return_value = {101: (False, False)}
        attempts = MagicMock()
        attempts.attempted = {"root:101"}
        attempts.resolved_ids.return_value = set()
        attempts.finding_key.side_effect = RepairAttemptTracker.finding_key
        attempts.filter_review.return_value = []

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairAttemptTracker",
                return_value=attempts,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(True, 3),
            ) as check_deduplication,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.repair_observation_key",
                return_value="a" * 64,
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        assert result.dedup_limit_reached
        assert result.repair_exhaustion_marker == f"<!-- repair-dispatch:exhausted:head:{'a' * 64} -->"
        assert "review=100" in result.details
        check_deduplication.assert_called_once_with(
            provider,
            42,
            "head",
            max_dispatches=3,
            review_id=100,
            work_key=repair_work_key(100, [root], []),
        )
        provider.dispatch_repair.assert_not_called()

    def test_fails_when_pending_accounting_cannot_be_reconciled_before_skipping(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="head", ci_status="failing")
        provider = MagicMock()
        provider.post_comment(
            42,
            '<!-- repair-dispatch-findings:42:head:v1 -->\n{"attempted": ["ci"]}',
        )
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.reconcile",
            side_effect=RuntimeError("pending intent is unresolved"),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))
        assert result.decision is ActionDecision.FAILED
        assert result.error == "pending intent is unresolved"
        provider.dispatch_repair.assert_not_called()

    def test_exhaustion_without_observation_key_still_blocks_dispatch(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="head", ci_status="failing")
        provider = MagicMock()
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(True, 1),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.repair_observation_key",
                side_effect=RuntimeError("thread inventory unavailable"),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.repair_hold_observation_key",
                return_value="b" * 64,
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))
        assert result.decision is ActionDecision.SKIP
        assert result.dedup_limit_reached
        assert result.repair_exhaustion_marker == f"<!-- repair-dispatch:exhausted-hold:head:{'b' * 64} -->"

    def test_exhaustion_uses_head_hold_when_work_fingerprinting_also_fails(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="head", ci_status="failing")
        provider = MagicMock()
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(True, 1),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.repair_observation_key",
                side_effect=RuntimeError("thread inventory unavailable"),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.repair_hold_observation_key",
                side_effect=RuntimeError("review inventory unavailable"),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))
        assert result.decision is ActionDecision.SKIP
        assert result.repair_exhaustion_marker == "<!-- repair-dispatch:exhausted-hold:head:unavailable -->"

    def test_reports_when_failed_intent_cannot_be_retired(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, head_sha="head", ci_status="failing")
        provider = MagicMock()
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.begin",
                side_effect=RuntimeError("intent persistence failed"),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.retire_pending",
                side_effect=RuntimeError("intent retirement failed"),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))
        assert result.decision is ActionDecision.FAILED
        assert result.definitive_no_mutation
        assert result.error == "intent persistence failed; intent retirement failed: intent retirement failed"

    def test_reports_bookkeeping_skips_in_action_summary_details(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
        )
        provider = MagicMock()
        provider._bookkeeping_audit = []
        provider.list_review_comments.return_value = [ReviewCommentInfo(id=101, path="", body="Fix", html_url="")]

        def dispatch_with_skipped_tracking(**_kwargs: object) -> int:
            provider._bookkeeping_audit.append("Task tracking replies skipped: bookkeeping bot identity unavailable")
            return 77

        provider.dispatch_repair.side_effect = dispatch_with_skipped_tracking

        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.EXECUTE
        assert "bookkeeping audit: Task tracking replies skipped" in result.details

    @pytest.mark.parametrize("label_error", [RuntimeError("missing label"), ProviderRateLimitError()])
    def test_label_failure_does_not_block_unrelated_dispatch(self, label_error) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
        )
        provider = MagicMock()
        root = ReviewCommentInfo(id=101, path="", body="Fix", html_url="")
        new_root = replace(root, id=102)
        provider.list_review_comments.return_value = [root]
        provider.dispatch_repair.return_value = 77
        action = DispatchRepairAction()
        assert action.execute(provider, snapshot, DerivedState(snapshot)).decision == ActionDecision.EXECUTE
        provider.list_review_comments.return_value = [root, new_root]
        provider.add_label.side_effect = label_error

        assert action.execute(provider, snapshot, DerivedState(snapshot)).decision == ActionDecision.EXECUTE
        assert provider.dispatch_repair.call_args.kwargs["review_comments"] == [new_root]
        assert sum("Human intervention" in c.args[1] for c in provider.post_comment.call_args_list) == 1

    @pytest.mark.parametrize("state", ["open", "resolved", "auto_applied", "answered", "attempted"])
    def test_promoted_suppression_does_not_create_body_fallback(self, state) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot[bot]",
                    state="CHANGES_REQUESTED",
                    body="### Comments suppressed due to low confidence (1)",
                )
            ],
        )
        root = ReviewCommentInfo(
            id=101,
            path="a.py",
            body="Fix\n<!-- ccr-promoted:100:suppressed:1 -->",
            html_url="https://example/101",
            source_review_id=100,
        )
        provider = MagicMock()
        provider.list_review_comments.return_value = [root]
        provider.list_review_thread_states.return_value = {101: (state == "resolved", False)}
        provider.dispatch_repair.return_value = 77
        derived = DerivedState(snapshot)
        if state == "auto_applied":
            derived.set("exclusion_context", ExclusionContext(resolved_comment_ids={101}))
        if state == "answered":
            provider.list_review_comments.return_value = [
                root,
                replace(root, id=102, body="Fixed", in_reply_to_id=101, author_login="copilot-swe-agent[bot]"),
            ]
        if state == "attempted":
            provider.post_comment(42, '<!-- repair-dispatch-findings:42:abc123:v1 -->\n{"attempted": ["root:101"]}')
        result = DispatchRepairAction().execute(provider, snapshot, derived)

        if state != "open":
            assert result.decision == ActionDecision.SKIP
            provider.dispatch_repair.assert_not_called()
            if state != "attempted":
                provider.post_comment.assert_not_called()
            else:
                assert sum("Human intervention" in c.args[1] for c in provider.post_comment.call_args_list) == 1
        else:
            assert result.decision == ActionDecision.EXECUTE
            assert provider.dispatch_repair.call_args.kwargs["declared_author_comment_count"] == 0
            reservation = provider.find_comment(42, "<!-- repair-dispatch-findings:")
            assert '"root:101"' in reservation[1]
            assert '"review:100"' not in reservation[1]

    def test_explicitly_resolved_suppression_with_no_comments_has_no_fallback(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot[bot]",
                    state="CHANGES_REQUESTED",
                    body=(
                        "<details><summary>Suppressed comments (1)</summary>\n"
                        "**a.py:8**\n* Resolved since the previous review.\n</details>"
                    ),
                ),
            ],
        )
        provider = MagicMock()
        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        provider.dispatch_repair.assert_not_called()
        provider.post_comment.assert_not_called()

    def test_ordinary_native_root_does_not_satisfy_suppression_declaration(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot[bot]",
                    state="CHANGES_REQUESTED",
                    body="### Comments suppressed due to low confidence (1)",
                )
            ],
        )
        provider = MagicMock()
        provider.list_review_comments.return_value = [
            ReviewCommentInfo(id=101, path="a.py", body="Ordinary root", html_url="https://example/101"),
        ]
        provider.dispatch_repair.return_value = 77

        assert (
            DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot)).decision
            == ActionDecision.EXECUTE
        )
        assert provider.dispatch_repair.call_args.kwargs["declared_author_comment_counts_by_review"] == {100: 1}
        assert '"review:100"' in provider.find_comment(42, "<!-- repair-dispatch-findings:")[1]

    def test_promoted_and_resolved_suppressions_leave_only_real_author_shortfall(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="copilot[bot]",
                    state="CHANGES_REQUESTED",
                    body="### Comments suppressed due to low confidence (4)",
                )
            ],
        )
        promoted = ReviewCommentInfo(
            id=101,
            path="a.py",
            body="Fix\n<!-- ccr-promoted:100:suppressed:1 -->",
            html_url="https://example/101",
            source_review_id=100,
        )
        resolved = replace(promoted, id=102, body="Fixed\n<!-- ccr-promoted:100:suppressed:2 -->")
        synthetic = ReviewCommentInfo(
            id=-3,
            path="b.py",
            body="Fix",
            html_url="",
            is_suppressed=True,
            source_review_id=100,
        )
        provider = MagicMock()
        provider.list_review_comments.return_value = [promoted, resolved, synthetic]
        provider.list_review_thread_states.return_value = {102: (True, True)}
        provider.dispatch_repair.return_value = 77
        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.EXECUTE
        assert provider.dispatch_repair.call_args.kwargs["review_comments"] == [promoted, synthetic]
        assert provider.dispatch_repair.call_args.kwargs["declared_author_comment_counts_by_review"] == {100: 2}

    def test_evaluate_skips_known_dispatched_work(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, ci_status="failing", head_sha="abc123")
        derived = DerivedState(snapshot)
        derived.set("repair_dispatched", True)
        assert DispatchRepairAction().evaluate(snapshot, derived).decision == ActionDecision.SKIP

    @pytest.mark.parametrize("marker", [False, (), (1,), ("1", ""), (0, ""), (1, None), (1, "malformed")])
    def test_malformed_global_marker_fails_closed(self, marker) -> None:
        snapshot = PRStateSnapshot(pr_number=42, ci_status="failing", head_sha="abc123")
        provider = MagicMock()
        provider.find_comment.side_effect = lambda pr, prefix: marker if prefix == "<!-- repair-dispatch:" else None
        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.FAILED
        provider.dispatch_repair.assert_not_called()

    def test_new_findings_head_and_ci_remain_independently_eligible(self) -> None:
        """Only exhausted findings leave the payload; a failed dispatch stays spent."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
        )
        provider = MagicMock()
        root = ReviewCommentInfo(id=101, path="a.py", body="Fix", html_url="")
        new_root = ReviewCommentInfo(id=102, path="b.py", body="Also fix", html_url="")
        provider.list_review_comments.return_value = [root]
        provider.dispatch_repair.return_value = 77
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=True,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 1),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            assert action.execute(provider, snapshot, DerivedState(snapshot)).decision == ActionDecision.EXECUTE
            provider.list_review_comments.return_value = [root, new_root]
            assert action.execute(provider, snapshot, DerivedState(snapshot)).decision == ActionDecision.EXECUTE
            assert provider.dispatch_repair.call_args.kwargs["review_comments"] == [new_root]

            failing = replace(snapshot, ci_status="failing")
            assert action.execute(provider, failing, DerivedState(failing)).decision == ActionDecision.EXECUTE
            assert provider.dispatch_repair.call_args.kwargs["repair_type"] == "ci"
            assert provider.dispatch_repair.call_args.kwargs["review_id"] == 0
            assert provider.dispatch_repair.call_args.kwargs["review_comments"] == []
            count = provider.dispatch_repair.call_count
            assert action.execute(provider, failing, DerivedState(failing)).decision == ActionDecision.SKIP
            assert provider.dispatch_repair.call_count == count

            next_head = replace(snapshot, head_sha="def456")
            provider.dispatch_repair.side_effect = RuntimeError("uncertain dispatch")
            assert action.execute(provider, next_head, DerivedState(next_head)).decision == ActionDecision.FAILED
            count = provider.dispatch_repair.call_count
            assert action.execute(provider, next_head, DerivedState(next_head)).decision == ActionDecision.SKIP
            assert provider.dispatch_repair.call_count == count

    def test_body_only_attempt_escalates_without_redispatch(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
        )
        provider = MagicMock()
        provider.dispatch_repair.return_value = 77
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 1),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            assert action.execute(provider, snapshot, DerivedState(snapshot)).decision == ActionDecision.EXECUTE
            assert action.execute(provider, snapshot, DerivedState(snapshot)).decision == ActionDecision.SKIP
        provider.dispatch_repair.assert_called_once()
        provider.add_label.assert_called_once_with(42, "ai-pr-loop:agent-failed")

    def test_legacy_review_read_failure_blocks_opaque_work(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
        )
        provider = MagicMock()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
            side_effect=RuntimeError("missing legacy evidence"),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.FAILED
        provider.dispatch_repair.assert_not_called()

    @pytest.mark.parametrize("method", ["find_comment", "list_review_thread_states", "post_comment"])
    def test_new_evidence_and_reservation_rate_limits_propagate(self, method) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="abc123",
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
        )
        provider = MagicMock()
        provider.list_review_comments.return_value = [ReviewCommentInfo(id=101, path="", body="Fix", html_url="")]
        getattr(provider, method).side_effect = ProviderRateLimitError(provider="github", credential_identity="test")
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 1),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
            pytest.raises(ProviderRateLimitError),
        ):
            DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))
        provider.dispatch_repair.assert_not_called()

    def test_new_findings_get_independent_scoped_budgets(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="abc123",
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
        )
        provider = MagicMock()
        provider.dispatch_repair.return_value = 77
        action = DispatchRepairAction()
        provider.list_review_comments.return_value = [ReviewCommentInfo(id=101, path="", body="First", html_url="")]
        assert action.execute(provider, snapshot, DerivedState(snapshot)).decision == ActionDecision.EXECUTE
        provider.list_review_comments.return_value = [ReviewCommentInfo(id=102, path="", body="Second", html_url="")]
        assert action.execute(provider, snapshot, DerivedState(snapshot)).decision == ActionDecision.EXECUTE
        provider.list_review_comments.return_value = [ReviewCommentInfo(id=103, path="", body="Third", html_url="")]
        assert action.execute(provider, snapshot, DerivedState(snapshot)).decision == ActionDecision.EXECUTE
        provider.list_review_comments.return_value = [ReviewCommentInfo(id=104, path="", body="Fourth", html_url="")]
        result = action.execute(provider, snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE
        assert provider.dispatch_repair.call_count == 4

    def test_finding_attempt_is_durable_and_escalates_once(self) -> None:
        """A new finding bypasses legacy review dedup; its next visit escalates."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
        )
        provider = MagicMock()
        stored: dict[str, tuple[int, str]] = {}

        def find_comment(pr_number: int, marker: str):
            return next((value for value in stored.values() if marker in value[1]), None)

        def list_issue_comments(pr_number: int) -> list[IssueCommentInfo]:
            return [
                IssueCommentInfo(id=comment_id, author="github-actions[bot]", body=body)
                for comment_id, body in stored.values()
            ]

        def post_comment(pr_number: int, body: str) -> int:
            stored[str(len(stored))] = (len(stored) + 1, body)
            return len(stored)

        def update_comment(comment_id: int, body: str) -> None:
            key = next(key for key, value in stored.items() if value[0] == comment_id)
            stored[key] = (comment_id, body)

        provider.find_comment.side_effect = find_comment
        provider.get_pr_token_login.return_value = "github-actions[bot]"
        provider.list_issue_comments.side_effect = list_issue_comments
        provider.post_comment.side_effect = post_comment
        provider.update_comment.side_effect = update_comment
        provider.list_review_comments.return_value = [ReviewCommentInfo(id=101, path="a.py", body="Fix", html_url="")]
        provider.list_review_thread_states.return_value = {101: (False, False)}
        provider.dispatch_repair.return_value = 77
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=True,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 1),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            first = action.execute(provider, snapshot, DerivedState(snapshot))
            provider.list_review_comments.return_value.append(
                ReviewCommentInfo(
                    id=202,
                    path="a.py",
                    body="Fixed",
                    html_url="",
                    author_login="copilot-swe-agent[bot]",
                    in_reply_to_id=101,
                )
            )
            second = action.execute(provider, snapshot, DerivedState(snapshot))
            third = action.execute(provider, snapshot, DerivedState(snapshot))

        assert first.decision == ActionDecision.EXECUTE
        assert second.decision == third.decision == ActionDecision.SKIP
        provider.dispatch_repair.assert_called_once()
        provider.add_label.assert_called_with(42, "ai-pr-loop:agent-failed")
        assert sum("Human intervention" in call.args[1] for call in provider.post_comment.call_args_list) == 1

    def test_marker_persistence_failure_prevents_dispatch(self) -> None:
        """A failed reservation must not result in an untracked repair."""
        snapshot = PRStateSnapshot(pr_number=42, ci_status="failing", head_sha="abc123")
        provider = MagicMock()
        provider.post_comment.side_effect = RuntimeError("write failed")
        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 1),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.FAILED
        provider.dispatch_repair.assert_not_called()

    def _execute_review_dispatch(
        self,
        provider: MagicMock,
        comments: list[ReviewCommentInfo],
        thread_states: dict[int, tuple[bool, bool]] | None = None,
    ) -> list[ReviewCommentInfo]:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider.list_review_comments.return_value = comments
        provider.list_review_thread_states.return_value = thread_states if thread_states is not None else {}
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        return provider.dispatch_repair.call_args.kwargs["review_comments"]

    def test_excludes_answered_cloud_coding_agent_root_and_reply(self) -> None:
        root = ReviewCommentInfo(
            id=101,
            path="src/foo.py",
            body="Fix this",
            html_url="https://example.test/root",
            author_login="copilot-pull-request-reviewer[bot]",
        )
        reply = ReviewCommentInfo(
            id=202,
            path="src/foo.py",
            body="Implemented.",
            html_url="https://example.test/reply",
            author_login="copilot-swe-agent[bot]",
            in_reply_to_id=101,
        )
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = [root, reply]
        provider.list_review_thread_states.return_value = {101: (False, True), 202: (False, True)}
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        # All comments were filtered (root suppressed, reply dropped) and CI is
        # passing with no declared suppressed findings — repair must be skipped.
        assert result.decision == ActionDecision.SKIP
        provider.dispatch_repair.assert_not_called()

    def test_keeps_unresolved_root_without_cloud_coding_agent_response(self) -> None:
        root = ReviewCommentInfo(
            id=101,
            path="src/foo.py",
            body="Fix this",
            html_url="https://example.test/root",
            author_login="copilot-pull-request-reviewer[bot]",
        )
        provider = MagicMock()

        comments = self._execute_review_dispatch(provider, [root], {101: (False, False)})

        assert comments == [root]

    def test_drops_resolved_root_without_response(self) -> None:
        root = ReviewCommentInfo(id=101, path="src/foo.py", body="Fix this", html_url="")
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = [root]
        provider.list_review_thread_states.return_value = {101: (True, False)}
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        # The root is resolved so it is filtered out; CI is passing and there are
        # no declared suppressed findings — repair must be skipped.
        assert result.decision == ActionDecision.SKIP
        provider.dispatch_repair.assert_not_called()

    def test_invalid_cloud_reply_does_not_suppress_root(self) -> None:
        root = ReviewCommentInfo(id=101, path="src/foo.py", body="Fix this", html_url="")
        empty_reply = ReviewCommentInfo(
            id=202,
            path="src/foo.py",
            body=" ",
            html_url="",
            author_login="copilot-swe-agent[bot]",
            in_reply_to_id=101,
        )
        provider = MagicMock()

        comments = self._execute_review_dispatch(
            provider,
            [root, empty_reply],
            {101: (False, True), 202: (False, True)},
        )

        # The empty reply is a Cloud Coding Agent reply with a valid parent and is
        # always dropped regardless of body content. The root is not suppressed
        # because the reply body is empty, so it is retained as a repair candidate.
        assert comments == [root]

    def test_stuck_prior_threads_skips_when_owner_reviews_are_fully_filtered(self) -> None:
        """Stuck-thread dispatch is skipped when ownership filtering leaves no owner reviews."""
        root = ReviewCommentInfo(
            id=101,
            path="src/foo.py",
            body="Fix this",
            html_url="https://example.test/root",
            author_login="copilot-pull-request-reviewer[bot]",
        )
        reply = ReviewCommentInfo(
            id=202,
            path="src/foo.py",
            body="Implemented.",
            html_url="https://example.test/reply",
            author_login="copilot-swe-agent[bot]",
            in_reply_to_id=101,
        )
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            copilot_review_id=0,
            unresolved_threads=1,
            repairable_threads=1,
            reviews=[
                ReviewInfo(
                    id=12,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    commit_sha="old111",
                    submitted_at="2024-01-01T11:00:00Z",
                )
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101, 202))}
        provider.list_review_comments.return_value = [root, reply]
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        provider.dispatch_repair.assert_not_called()
        provider.list_review_comments.assert_called_once_with(42, 12)

    def test_stuck_fully_filtered_reviews_use_review_context_for_shortfall_dispatch(self) -> None:
        """Shortfall dispatches retain a review ID when all stuck reviews are filtered."""
        root = ReviewCommentInfo(
            id=101,
            path="src/foo.py",
            body="Fix this",
            html_url="https://example.test/root",
            author_login="copilot-pull-request-reviewer[bot]",
        )
        reply = ReviewCommentInfo(
            id=202,
            path="src/foo.py",
            body="Implemented.",
            html_url="https://example.test/reply",
            author_login="copilot-swe-agent[bot]",
            in_reply_to_id=101,
        )
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            copilot_review_id=0,
            unresolved_threads=1,
            repairable_threads=1,
            reviews=[
                ReviewInfo(
                    id=12,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    commit_sha="old111",
                    submitted_at="2024-01-01T11:00:00Z",
                    body="### Comments suppressed due to low confidence (2)\n\nreview body",
                )
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101, 202))}
        provider.list_review_comments.return_value = [root, reply]
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ) as mock_is_duplicate_trigger,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert provider.dispatch_repair.call_args.kwargs["review_id"] == 12
        mock_is_duplicate_trigger.assert_not_called()

    def test_keeps_synthetic_entry_when_thread_is_answered(self) -> None:
        root = ReviewCommentInfo(id=101, path="src/foo.py", body="Fix this", html_url="")
        reply = ReviewCommentInfo(
            id=202,
            path="src/foo.py",
            body="Implemented.",
            html_url="",
            author_login="copilot-swe-agent",
            in_reply_to_id=101,
        )
        synthetic = ReviewCommentInfo(
            id=-1, path="README.md", body="Suppressed finding", html_url="", is_suppressed=True
        )
        provider = MagicMock()

        comments = self._execute_review_dispatch(
            provider,
            [root, reply, synthetic],
            {101: (False, True), 202: (False, True)},
        )

        assert comments == [synthetic]

    def test_human_reply_does_not_suppress_root(self) -> None:
        root = ReviewCommentInfo(id=101, path="src/foo.py", body="Fix this", html_url="")
        human_reply = ReviewCommentInfo(
            id=202,
            path="src/foo.py",
            body="Can you clarify?",
            html_url="",
            author_login="octocat",
            in_reply_to_id=101,
        )
        provider = MagicMock()

        comments = self._execute_review_dispatch(
            provider,
            [root, human_reply],
            {101: (False, True), 202: (False, True)},
        )

        assert comments == [root, human_reply]

    def test_thread_state_failure_blocks_dispatch(self) -> None:
        root = ReviewCommentInfo(id=101, path="src/foo.py", body="Fix this", html_url="")
        provider = MagicMock()
        provider.list_review_thread_states.side_effect = RuntimeError("unavailable")

        provider.list_review_comments.return_value = [root]
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="abc123",
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
        )
        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.FAILED
        provider.dispatch_repair.assert_not_called()

    def test_fetch_failure_disables_filtered_skip(self) -> None:
        """Missing comment evidence cannot safely authorize a dispatch."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.side_effect = RuntimeError("network error")
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED
        provider.dispatch_repair.assert_not_called()

    def test_declared_suppressed_findings_prevent_filtered_skip(self) -> None:
        """Declared suppressed findings must still dispatch even when all inline comments are filtered."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            check_runs=[],
            reviews=[
                ReviewInfo(
                    id=100,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    body="### Comments suppressed due to low confidence (2)\n\nsome prose",
                )
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        # All inline comments are filtered (e.g., all resolved)
        provider.list_review_comments.return_value = []
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        # Declared suppressed count > 0 — repair must run so the agent receives
        # a shortfall notice for the unrecovered author comments.
        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_repair.assert_called_once()

    def test_empty_review_collection_is_not_skipped(self) -> None:
        """A review that was empty from the start (not filtered empty) must still dispatch.

        An empty-from-the-start collection is not evidence of all-replied work;
        the review may still carry context that the agent needs (body, link).
        """
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = []
        provider.list_review_thread_states.return_value = {}
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        # Review was empty from the start — not made empty by filtering — so
        # the guard must not suppress dispatch.
        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_repair.assert_called_once()

    def test_skip_when_ci_failing_with_active_session(self) -> None:
        """Fail closed when session inventory shows an active Copilot session."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            pr_id=123456,
            ci_status="failing",
            base_repo_full_name="owner/repo",
            head_branch="copilot/issue-1-fix",
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        derived.set("provider", provider)
        action = DispatchRepairAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
            return_value=True,
        ) as mock_detector:
            result = action.evaluate(snapshot, derived)
        mock_detector.assert_called_once_with(
            "owner/repo",
            1,
            head_branch="copilot/issue-1-fix",
            pr_id=123456,
            head_sha=snapshot.head_sha,
            provider=provider,
        )
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions.get("no_active_session") is False

    def test_skip_when_ci_failing_with_unknown_session_inventory(self) -> None:
        """Fail closed when session inventory is unavailable/unknown."""
        snapshot = PRStateSnapshot(pr_number=1, ci_status="failing")
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
            return_value=None,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions.get("no_active_session") is False
        assert "inventory unavailable" in result.details.lower()

    def test_skip_when_review_actionable_with_active_session(self) -> None:
        """Actionable review still blocks dispatch while a session is active."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
            return_value=True,
        ):
            result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions.get("no_active_session") is False

    def test_skip_when_ci_passing_and_no_review(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=1,
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "no actionable" in result.details.lower() or "passing" in result.details.lower()

    def test_skip_when_effective_review_work_is_empty(self) -> None:
        """A stale review with no effective comments does not trigger repair."""
        snapshot = PRStateSnapshot(
            pr_number=3993,
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=5409561506,
            copilot_review_inline_count=-1,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=5409561506,
        )
        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["review_actionable"] is True
        assert result.preconditions["effective_review_work"] is False
        assert "effective review work" in result.details.lower()

    def test_execute_skips_when_effective_review_work_is_empty(self) -> None:
        """Direct execution also skips stale review work before posting a repair."""
        snapshot = PRStateSnapshot(
            pr_number=3993,
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=5409561506,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=5409561506,
        )
        provider = MagicMock()

        result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        assert "effective review work" in result.details.lower()
        provider.dispatch_repair.assert_not_called()

    def test_failing_ci_dispatches_when_effective_review_work_is_empty(self) -> None:
        """CI failure remains an independent repair reason when review work is stale."""
        snapshot = PRStateSnapshot(
            pr_number=3993,
            ci_status="failing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=5409561506,
            copilot_review_inline_count=-1,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=5409561506,
        )
        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["ci_failing"] is True
        assert result.preconditions["effective_review_work"] is False

    def test_dispatches_when_effective_current_review_work_remains(self) -> None:
        """A current review with effective comments still triggers repair."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=-1,
            effective_review_comment_count=1,
            effective_review_comment_count_review_id=100,
        )
        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True
        assert result.preconditions["effective_review_work"] is True

    def test_skips_new_ccr_review_when_reported_comments_are_all_filtered(self) -> None:
        """A new-CCR review with no remaining reported comments does not dispatch."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=100,
            effective_review_comment_filter_applied=True,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_NEW_CCR_NOT_APPROVED,
                review_id=100,
                body_comment_count=3,
            ),
        )
        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["review_actionable"] is True
        assert result.preconditions["effective_review_work"] is False

    def test_dispatches_new_ccr_body_only_work_when_effective_inventory_is_empty(self) -> None:
        """Unknown inline work in a new-CCR body remains fail-open."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=100,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_NEW_CCR_NOT_APPROVED,
                review_id=100,
                body_comment_count=0,
            ),
        )
        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["effective_review_work"] is True

    def test_dispatches_new_ccr_when_body_count_positive_without_filter_evidence(self) -> None:
        """A positive body count with no recorded filtering remains fail-open."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=100,
            effective_review_comment_filter_applied=False,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_NEW_CCR_NOT_APPROVED,
                review_id=100,
                body_comment_count=3,
            ),
        )

        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["effective_review_work"] is True

    def test_dispatches_when_effective_count_source_review_differs_from_actionable_review(self) -> None:
        """Count data from a different review id must not suppress actionable work."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=100,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_HAS_COMMENTS,
                review_id=200,
                body_comment_count=1,
            ),
        )

        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True
        assert result.preconditions["effective_review_work"] is True

    def test_skip_message_includes_non_failing_ci_status(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="pending",
            review_state="APPROVED",
            copilot_review_id=1,
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "ci_status=pending" in result.details.lower()

    def test_execute_when_ci_failing(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="failing",
            active_session=False,
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_execute_when_review_actionable(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            active_session=False,
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_execute_when_prior_review_threads_are_stuck(self) -> None:
        """Action executes when repairable threads exist, even if blocking thread count is 0."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=0,  # Zero blocking threads
            repairable_threads=2,  # But repairable threads exist
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions.get("stuck_prior_threads") is True

    def test_evaluate_when_only_verdict_owned_repairable_threads_exist(self) -> None:
        """A verdict-owned unresolved thread should still trigger the stuck-thread repair path."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=0,
            repairable_threads=1,
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_CONTENT_CHANGED,
                review_id=100,
            ),
            reviews=[
                ReviewInfo(id=100, user="Copilot", state="COMMENTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions.get("stuck_prior_threads") is True

    def test_execute_when_approved_review_has_promoted_repairable_threads(self) -> None:
        """Promoted threads from an otherwise clean approved review still trigger repair."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            head_sha="head123",
            review_state="APPROVED",
            copilot_review_id=100,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=100,
            unresolved_threads=0,
            repairable_threads=1,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="Copilot",
                    state="APPROVED",
                    commit_sha="head123",
                    body="0 open findings",
                ),
            ],
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()

        result = action.evaluate(snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions.get("stuck_prior_threads") is True

    def test_skip_when_threads_exist_but_no_prior_copilot_review(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(id=10, user="alice", state="CHANGES_REQUESTED", commit_sha="old123"),
            ],
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions.get("stuck_prior_threads") is False

    def test_execute_when_prior_synthetic_review_threads_are_stuck(self) -> None:
        """Trusted synthetic review on a prior commit contributes to stuck_prior_threads."""
        from agentic_devtools.cli.ci.pipeline.gate_verdict import SYNTHETIC_MARKER, TRUSTED_SYNTHETIC_USERS

        synthetic_user = next(iter(TRUSTED_SYNTHETIC_USERS))
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(
                    id=10,
                    user=synthetic_user,
                    state="CHANGES_REQUESTED",
                    commit_sha="old123",
                    body=f"Review feedback. {SYNTHETIC_MARKER}",
                ),
            ],
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions.get("stuck_prior_threads") is True

    def test_execute_when_commented_review_inline_count_unknown(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            active_session=False,
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=-1,
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.EXECUTE

    def test_skip_when_ci_pending_even_if_review_actionable(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="pending",
            active_session=False,
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=1,
        )
        derived = DerivedState(snapshot)
        action = DispatchRepairAction()
        result = action.evaluate(snapshot, derived)
        assert result.decision == ActionDecision.SKIP
        assert "pending" in result.details.lower()

    def test_execute_dispatches_repair(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            copilot_review_id=0,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)
            assert result.decision == ActionDecision.EXECUTE
            provider.dispatch_repair.assert_called_once()

    def test_execute_uses_global_ceiling_with_separate_ci_reservation(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            copilot_review_id=0,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ) as mock_check_deduplication,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        mock_check_deduplication.assert_called_once_with(
            provider, 42, "abc123", max_dispatches=1, review_id=0, work_key=ANY
        )

    def test_execute_uses_default_dedup_limit_when_review_actionable(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=12,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = [MagicMock(id=1)]
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ) as mock_check_deduplication,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        mock_check_deduplication.assert_called_once_with(
            provider, 42, "abc123", max_dispatches=3, review_id=12, work_key=ANY
        )

    def test_skip_when_dedup_limit_reached(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, ci_status="failing", head_sha="abc123")
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(True, 3),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)
            assert result.decision == ActionDecision.SKIP
            assert "budget exhausted" in result.details.lower()
            assert result.limit_reached is True
            assert result.dedup_limit_reached is True
            assert result.cycle_limit_reached is False

    def test_skip_when_cycle_limit_reached(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, ci_status="failing", head_sha="abc123")
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(True, 5),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)
            assert result.decision == ActionDecision.SKIP
            assert "cycle" in result.details.lower()
            assert result.limit_reached is True
            assert result.dedup_limit_reached is False
            assert result.cycle_limit_reached is True

    def test_failed_checks_uses_actionable_subset_only(self) -> None:
        """execute() passes only actionable failed checks to dispatch_repair."""
        from agentic_devtools.cli.ci.models import CheckRunStatus

        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            ci_failed_checks=["Targeted Checks ✅"],
            head_sha="abc123",
            check_runs=[
                CheckRunStatus(id=1, name="Targeted Checks ✅", status="completed", conclusion="failure"),
                CheckRunStatus(id=2, name="flaky-optional", status="completed", conclusion="failure"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 1

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            action.execute(provider, snapshot, derived)

        call_kwargs = provider.dispatch_repair.call_args
        passed_checks = call_kwargs.kwargs.get("failed_checks") or call_kwargs.args[3]
        check_names = [cr.name for cr in passed_checks]
        assert "Targeted Checks ✅" in check_names
        assert "flaky-optional" not in check_names

    def test_execute_sets_repair_dispatched_on_derived(self) -> None:
        """execute() must set derived.repair_dispatched after successful dispatch."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            copilot_review_id=0,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)
            assert result.decision == ActionDecision.EXECUTE
            assert derived.repair_dispatched is True

    def test_failed_when_deduplication_check_raises(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, ci_status="failing", head_sha="abc123")
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                side_effect=RuntimeError("dedup boom"),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED
        assert "Deduplication check failed" in result.details

    def test_failed_when_cycle_limit_check_raises(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, ci_status="failing", head_sha="abc123")
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                side_effect=RuntimeError("cycle boom"),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED
        assert "Cycle limit check failed" in result.details

    def test_execute_dispatches_review_only_and_fetches_review_comments(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=12,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = [MagicMock(id=1)]
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs["repair_type"] == "review"
        assert call_kwargs["review_comments"] == [provider.list_review_comments.return_value[0]]

    def test_execute_dispatches_review_for_stuck_prior_threads(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(
                    id=11, user="Copilot", state="COMMENTED", commit_sha="old111", submitted_at="2024-01-01T10:00:00Z"
                ),
                ReviewInfo(
                    id=12,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    commit_sha="old222",
                    submitted_at="2024-01-01T11:00:00Z",
                ),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        review_comment_a = MagicMock(id=101)
        review_comment_b = MagicMock(id=102)
        review_comment_b_duplicate = MagicMock(id=102)
        review_comment_suppressed_a = MagicMock(id=-1)
        review_comment_suppressed_b = MagicMock(id=-1)
        provider.list_review_comments.side_effect = [
            [review_comment_b, review_comment_suppressed_a],
            [review_comment_a, review_comment_b_duplicate, review_comment_suppressed_b],
        ]
        provider.dispatch_repair.return_value = 88

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs["repair_type"] == "review"
        assert call_kwargs["review_id"] == 12
        assert call_kwargs["review_comments"] == [
            review_comment_b,
            review_comment_suppressed_a,
            review_comment_a,
            review_comment_suppressed_b,
        ]
        provider.list_review_comments.assert_any_call(42, 12)
        provider.list_review_comments.assert_any_call(42, 11)

    def test_execute_dispatches_verdict_review_when_it_is_the_only_repairable_provenance(self) -> None:
        verdict = CopilotGateVerdict(passed=False, reason=REASON_CONTENT_CHANGED, review_id=99)
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=0,
            repairable_threads=1,
            copilot_gate_verdict=verdict,
            reviews=[
                ReviewInfo(
                    id=99,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old333",
                    submitted_at="2024-01-01T12:00:00Z",
                ),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        verdict_comment = MagicMock(id=203)
        provider.list_review_comments.return_value = [verdict_comment]
        provider.dispatch_repair.return_value = 88

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs["repair_type"] == "review"
        assert call_kwargs["review_id"] == 99
        assert call_kwargs["review_comments"] == [verdict_comment]
        provider.list_review_comments.assert_called_once_with(42, 99)

    def test_execute_includes_verdict_review_comments_when_both_actionable_and_stuck_prior(self) -> None:
        """When review_actionable and stuck_prior_threads are both true, the verdict-owned review's
        comments must appear in the repair payload alongside the prior-review comments."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_HAS_COMMENTS, review_id=99)
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=3,
            repairable_threads=3,
            copilot_gate_verdict=verdict,
            reviews=[
                ReviewInfo(
                    id=11, user="Copilot", state="COMMENTED", commit_sha="old111", submitted_at="2024-01-01T10:00:00Z"
                ),
                ReviewInfo(
                    id=12,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    commit_sha="old222",
                    submitted_at="2024-01-01T11:00:00Z",
                ),
                ReviewInfo(
                    id=99,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old333",
                    submitted_at="2024-01-01T12:00:00Z",
                ),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        prior_comment_11 = MagicMock(id=201)
        prior_comment_12 = MagicMock(id=202)
        verdict_comment_99 = MagicMock(id=203)
        provider.list_review_comments.side_effect = [
            [prior_comment_12],
            [prior_comment_11],
            [verdict_comment_99],
        ]
        provider.dispatch_repair.return_value = 88

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs["repair_type"] == "review"
        # review_context_id is the verdict review (99)
        assert call_kwargs["review_id"] == 99
        # All three reviews' comments must be present
        assert prior_comment_11 in call_kwargs["review_comments"]
        assert prior_comment_12 in call_kwargs["review_comments"]
        assert verdict_comment_99 in call_kwargs["review_comments"]
        provider.list_review_comments.assert_any_call(42, 11)
        provider.list_review_comments.assert_any_call(42, 12)
        provider.list_review_comments.assert_any_call(42, 99)

    def test_execute_stuck_prior_threads_uses_stable_order_for_missing_or_invalid_timestamps(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(id=11, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old111", submitted_at=""),
                ReviewInfo(
                    id=12,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    commit_sha="old222",
                    submitted_at=None,  # type: ignore[arg-type]
                ),
                ReviewInfo(
                    id=13,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    commit_sha="old333",
                    submitted_at=123,  # type: ignore[arg-type]
                ),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = []
        provider.dispatch_repair.return_value = 89

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs["review_id"] == 13

    def test_execute_skips_stuck_threads_when_review_id_dedup_matches_prior_review(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(id=12, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old222"),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
            return_value=True,
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "No unattempted findings" in result.details
        provider.dispatch_repair.assert_not_called()

    def test_execute_stuck_prior_threads_uses_unresolved_thread_owner_for_dedup_and_context(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=0,
            repairable_threads=1,
            reviews=[
                ReviewInfo(
                    id=10,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old111",
                    submitted_at="2024-01-01T10:00:00Z",
                ),
                ReviewInfo(
                    id=11,
                    user="Copilot",
                    state="APPROVED",
                    commit_sha="old222",
                    submitted_at="2024-01-01T11:00:00Z",
                ),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        owner_comment = ReviewCommentInfo(id=101, path="a.py", body="owner unresolved", html_url="")
        provider.list_review_threads_by_thread_id.return_value = {"thread-1": (False, (101,))}
        provider.list_review_thread_states.return_value = {101: (False, False)}
        provider.list_review_comments.side_effect = [
            [],  # review 11 has no findings; it must not gain opaque body work.
            [owner_comment],  # review 10
        ]
        provider.dispatch_repair.return_value = 123

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                side_effect=lambda _provider, _pr, review_id: review_id == 11,
            ) as duplicate_mock,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        duplicate_mock.assert_not_called()
        dispatch_kwargs = provider.dispatch_repair.call_args.kwargs
        assert dispatch_kwargs["review_id"] == 10
        assert dispatch_kwargs["review_comments"] == [owner_comment]

    def test_execute_stuck_prior_threads_ignores_old_review_markers_for_new_findings(self) -> None:
        """Both unattempted roots remain eligible despite a legacy review marker."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=0,
            repairable_threads=2,
            reviews=[
                ReviewInfo(
                    id=10,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old111",
                    submitted_at="2024-01-01T10:00:00Z",
                ),
                ReviewInfo(
                    id=20,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old222",
                    submitted_at="2024-01-01T12:00:00Z",
                ),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        comment_20 = ReviewCommentInfo(id=201, path="a.py", body="review 20 comment", html_url="")
        comment_10 = ReviewCommentInfo(id=101, path="b.py", body="review 10 comment", html_url="")
        # Both reviews own separate unresolved threads.
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (201,)),
            "thread-2": (False, (101,)),
        }
        # Reviews are sorted newest-first (20 then 10), so list_review_comments is called in that order.
        provider.list_review_comments.side_effect = [
            [comment_20],  # review 20
            [comment_10],  # review 10
        ]
        provider.dispatch_repair.return_value = 123

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                side_effect=lambda _provider, _pr, review_id: review_id == 20,
            ) as duplicate_mock,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        duplicate_mock.assert_not_called()
        dispatch_kwargs = provider.dispatch_repair.call_args.kwargs
        assert dispatch_kwargs["review_id"] == 20
        assert dispatch_kwargs["review_comments"] == [comment_20, comment_10]

    def test_execute_stuck_prior_threads_new_findings_ignore_all_legacy_review_markers(self) -> None:
        """Legacy markers cannot attribute an attempt to either new root."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=0,
            repairable_threads=2,
            reviews=[
                ReviewInfo(
                    id=10,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old111",
                    submitted_at="2024-01-01T10:00:00Z",
                ),
                ReviewInfo(
                    id=20,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old222",
                    submitted_at="2024-01-01T12:00:00Z",
                ),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        comment_20 = ReviewCommentInfo(id=201, path="a.py", body="review 20 comment", html_url="")
        comment_10 = ReviewCommentInfo(id=101, path="b.py", body="review 10 comment", html_url="")
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (201,)),
            "thread-2": (False, (101,)),
        }
        provider.list_review_comments.side_effect = [
            [comment_20],  # review 20
            [comment_10],  # review 10
        ]

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=True,
            ) as duplicate_mock,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        duplicate_mock.assert_not_called()
        provider.dispatch_repair.assert_called_once()

    def test_execute_stuck_prior_threads_does_not_read_legacy_guard_for_known_findings(self) -> None:
        """The finding ledger supersedes the old review-level lookup."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=0,
            repairable_threads=2,
            reviews=[
                ReviewInfo(
                    id=10,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old111",
                    submitted_at="2024-01-01T10:00:00Z",
                ),
                ReviewInfo(
                    id=20,
                    user="Copilot",
                    state="COMMENTED",
                    commit_sha="old222",
                    submitted_at="2024-01-01T12:00:00Z",
                ),
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        comment_20 = ReviewCommentInfo(id=201, path="a.py", body="review 20 comment", html_url="")
        comment_10 = ReviewCommentInfo(id=101, path="b.py", body="review 10 comment", html_url="")
        provider.list_review_threads_by_thread_id.return_value = {
            "thread-1": (False, (201,)),
            "thread-2": (False, (101,)),
        }
        provider.list_review_comments.side_effect = [
            [comment_20],  # review 20
            [comment_10],  # review 10
        ]
        provider.dispatch_repair.return_value = 123

        def _dedup_raises_for_20(_provider: object, _pr: int, review_id: int) -> bool:
            if review_id == 20:
                raise RuntimeError("API error")
            return False

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                side_effect=_dedup_raises_for_20,
            ) as duplicate_mock,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        duplicate_mock.assert_not_called()
        dispatch_kwargs = provider.dispatch_repair.call_args.kwargs
        assert dispatch_kwargs["review_id"] == 20

    def test_execute_fails_closed_when_review_comments_fetch_fails(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=12,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.side_effect = RuntimeError("comments boom")
        provider.dispatch_repair.return_value = 88

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED
        provider.dispatch_repair.assert_not_called()

    def test_failed_when_dispatch_repair_raises(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.side_effect = RuntimeError("dispatch boom")

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.FAILED
        assert "dispatch_repair call failed" in result.details

    def test_retires_intent_when_dispatch_failed_before_creation(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, ci_status="failing", head_sha="abc123")
        provider = MagicMock()
        provider.dispatch_repair.side_effect = RepairDispatchNotAttemptedError("missing token")
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
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.retire_pending"
            ) as retire,
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.FAILED
        assert result.definitive_no_mutation is True
        retire.assert_called_once()
        assert RepairAttemptTracker(provider, 42, "abc123").attempted == set()

    def test_reports_when_pre_creation_intent_retirement_fails(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, ci_status="failing", head_sha="abc123")
        provider = MagicMock()
        provider.dispatch_repair.side_effect = RepairDispatchNotAttemptedError("missing token")
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
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.retire_pending",
                side_effect=RuntimeError("ledger unavailable"),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision is ActionDecision.FAILED
        assert "intent retirement failed" in result.error

    def test_reraises_rate_limit_after_retiring_pre_creation_intent(self) -> None:
        snapshot = PRStateSnapshot(pr_number=42, ci_status="failing", head_sha="abc123")
        provider = MagicMock()
        rate_limit = ProviderRateLimitError(provider="github")
        pre_creation_error = RepairDispatchNotAttemptedError("preflight rate limit")
        pre_creation_error.__cause__ = rate_limit
        provider.dispatch_repair.side_effect = pre_creation_error
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
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.retire_pending"
            ) as retire,
            pytest.raises(ProviderRateLimitError),
        ):
            DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        retire.assert_called_once()

    def test_reraises_rate_limit_when_dispatch_repair_raises(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
        )

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.RepairDispatchLedger.retire_pending"
            ) as retire,
        ):
            action = DispatchRepairAction()
            with pytest.raises(ProviderRateLimitError):
                action.execute(provider, snapshot, derived)

        retire.assert_not_called()

    def test_reraises_rate_limit_when_fetching_review_comments(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=12,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.side_effect = ProviderRateLimitError(
            provider="github",
            credential_identity="SPECKIT_PR_TOKEN",
            source="x-ratelimit-reset",
        )

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            with pytest.raises(ProviderRateLimitError):
                action.execute(provider, snapshot, derived)

    def test_execute_dispatches_both_when_ci_failing_and_review_actionable(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=12,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = [MagicMock(id=1)]
        provider.dispatch_repair.return_value = 99

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        assert provider.dispatch_repair.call_args.kwargs["repair_type"] == "both"

    def test_execute_ci_failing_stale_review_not_blocked_by_review_id_dedup(self) -> None:
        """CI-failing repair is not blocked by stale-review dedup when effective review work is empty."""
        # The stale review (copilot_review_id=9000) already has a trigger marker, but
        # CI is failing.  Because effective review work is 0, review_context_id must be
        # cleared so the review-ID dedup path is bypassed and the CI repair proceeds.
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=9000,
            copilot_review_inline_count=-1,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=9000,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 99

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=True,  # stale review already has a trigger marker
            ) as mock_dedup,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        # review_context_id is 0 (cleared), so is_duplicate_trigger is never called
        assert result.decision == ActionDecision.EXECUTE
        mock_dedup.assert_not_called()

    def test_execute_ci_failing_stale_review_dispatches_without_review_id(self) -> None:
        """CI-only dispatch does not attach a stale review ID when effective review work is empty."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="sha999",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=7777,
            copilot_review_inline_count=-1,
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=7777,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 55

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ) as mock_dedup,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        # review_context_id=0 → review-ID dedup is never invoked
        mock_dedup.assert_not_called()
        # dispatch_repair should be called with repair_type="ci" and review_id=0 (no stale review)
        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs.get("review_id", 0) == 0

    def test_execute_when_duplicate_trigger_exists_for_review_id(self) -> None:
        """FR-012: Duplicate trigger for same review_id is treated as already dispatched."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=4401589029,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
            return_value=True,
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "No unattempted findings" in result.details
        assert getattr(derived, "repair_dispatched", False) is False
        provider.dispatch_repair.assert_not_called()

    def test_known_finding_does_not_use_review_id_dedup(self) -> None:
        """Finding-aware work never reads the superseded review-level guard."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = [MagicMock(id=101)]
        provider.dispatch_repair.return_value = 200

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                side_effect=RuntimeError("API error"),
            ) as duplicate_trigger,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        duplicate_trigger.assert_not_called()
        provider.dispatch_repair.assert_called_once()

    def test_exclusion_context_filters_review_comments(self) -> None:
        """ExclusionContext filters out already-applied comments from dispatch."""
        from agentic_devtools.cli.ci.pipeline.exclusion import ExclusionContext

        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="failing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=3,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        exclusion_ctx = ExclusionContext(resolved_comment_ids={101, 102})
        derived.set("exclusion_context", exclusion_ctx)

        provider = MagicMock()
        provider.list_review_comments.return_value = [
            MagicMock(id=101),
            MagicMock(id=102),
            MagicMock(id=103),
        ]
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        call_kwargs = provider.dispatch_repair.call_args
        review_comments = call_kwargs.kwargs.get("review_comments") or call_kwargs[0][4]
        assert len(review_comments) == 1

    def test_exclusion_context_skips_repair_when_all_excluded_ci_passing(self) -> None:
        """SKIP when all review comments excluded and CI is passing."""
        from agentic_devtools.cli.ci.pipeline.exclusion import ExclusionContext

        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=2,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        exclusion_ctx = ExclusionContext(resolved_comment_ids={101, 102})
        derived.set("exclusion_context", exclusion_ctx)

        provider = MagicMock()
        provider.list_review_comments.return_value = [
            MagicMock(id=101),
            MagicMock(id=102),
        ]

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "No unattempted findings" in result.details

    def test_exclusion_context_does_not_skip_declared_shortfall_when_all_inline_comments_are_excluded(self) -> None:
        """Declared suppressed findings must still dispatch a shortfall notice."""
        from agentic_devtools.cli.ci.pipeline.exclusion import ExclusionContext

        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=2,
            reviews=[
                ReviewInfo(
                    id=100,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    body="### Comments suppressed due to low confidence (2)\n\nreview body",
                )
            ],
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        exclusion_ctx = ExclusionContext(resolved_comment_ids={101, 102})
        derived.set("exclusion_context", exclusion_ctx)

        provider = MagicMock()
        provider.list_review_comments.return_value = [
            MagicMock(id=101),
            MagicMock(id=102),
        ]
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs["review_comments"] == []
        assert call_kwargs["declared_author_comment_count"] == 2
        assert call_kwargs["declared_author_comment_counts_by_review"] == {100: 2}

    def test_exclusion_context_no_matching_ids_still_dispatches(self) -> None:
        """Dispatch when exclusion context IDs don't match any review comments."""
        from agentic_devtools.cli.ci.pipeline.exclusion import ExclusionContext

        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=2,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        # Exclusion context has IDs that don't match actual review comments
        exclusion_ctx = ExclusionContext(resolved_comment_ids={999, 998})
        derived.set("exclusion_context", exclusion_ctx)

        provider = MagicMock()
        provider.list_review_comments.return_value = [
            MagicMock(id=101),
            MagicMock(id=102),
        ]
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE

    def test_exclusion_context_skips_without_any_remaining_work(self) -> None:
        """Unknown CI does not justify retrying already auto-applied findings."""
        from agentic_devtools.cli.ci.pipeline.exclusion import ExclusionContext

        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="unknown",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            copilot_review_inline_count=2,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        exclusion_ctx = ExclusionContext(resolved_comment_ids={101, 102})
        derived.set("exclusion_context", exclusion_ctx)

        provider = MagicMock()
        provider.list_review_comments.return_value = [
            MagicMock(id=101),
            MagicMock(id=102),
        ]
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        provider.dispatch_repair.assert_not_called()


class TestDispatchRepairDedupEscalation:
    """Tests for escalation when a repair scope is exhausted."""

    @pytest.mark.parametrize("threads_degraded", [False, True])
    def test_dedup_limit_escalates_body_only_unresolved_findings(self, threads_degraded: bool) -> None:
        review = ReviewInfo(
            id=100,
            user="copilot-pull-request-reviewer[bot]",
            state="CHANGES_REQUESTED",
            commit_sha="abc123",
            body="### Comments suppressed due to low confidence (1)",
        )
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="abc123",
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            repairable_threads=0,
            unresolved_threads_degraded=threads_degraded,
            reviews=[review],
        )
        provider = MagicMock()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
            return_value=(True, 8),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        assert result.dedup_limit_reached is True
        assert result.escalation_needed is (not threads_degraded)
        if threads_degraded:
            provider.add_label.assert_not_called()
            provider.post_comment.assert_not_called()
        else:
            provider.add_label.assert_called_once_with(42, "ai-pr-loop:agent-failed")
            comment = provider.post_comment.call_args.args[1]
            assert "repair-dispatch-escalation:v1:42:abc123:review:100" in comment
        provider.dispatch_repair.assert_not_called()

    def test_dedup_limit_escalates_remaining_unresolved_finding(self) -> None:
        review = ReviewInfo(
            id=100,
            user="copilot-pull-request-reviewer[bot]",
            state="CHANGES_REQUESTED",
            commit_sha="abc123",
        )
        root = ReviewCommentInfo(id=101, path="a.py", body="Fix this", html_url="https://example/101")
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="abc123",
            ci_status="passing",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=100,
            repairable_threads=1,
            reviews=[review],
        )
        provider = MagicMock()
        provider.list_review_comments.return_value = [root]
        provider.list_review_thread_states.return_value = {}
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
            return_value=(True, 8),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        assert result.dedup_limit_reached is True
        assert result.escalation_needed is True
        provider.add_label.assert_called_once_with(42, "ai-pr-loop:agent-failed")
        provider.dispatch_repair.assert_not_called()
        comment = provider.post_comment.call_args.args[1]
        assert "repair-dispatch-escalation:v1:42:abc123:root:101" in comment
        assert "actionable repair remains" in comment
        assert "deduplication limit is exhausted" in comment
        assert "Human attention is required" in comment

    def test_dedup_limit_without_unresolved_review_findings_does_not_escalate(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="abc123",
            ci_status="failing",
            repairable_threads=0,
        )
        provider = MagicMock()
        with patch(
            "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
            return_value=(True, 8),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.SKIP
        assert result.escalation_needed is False
        provider.add_label.assert_not_called()
        provider.post_comment.assert_not_called()


class TestDispatchRepairDeferralCheck:
    """Tests for deferral marker check in execute."""

    def test_skips_dispatch_when_active_deferral_marker(self) -> None:
        """Lines 138-147: active deferral marker causes skip."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="failing",
            copilot_review_id=100,
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value={"review_id": "100", "active": True},
            ),
            patch("agentic_devtools.cli.ci.pipeline.deferral.deactivate_deferral_marker") as mock_deactivate,
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "Deferred" in result.details
        mock_deactivate.assert_called_once_with(provider, 1, 100)

    def test_proceeds_when_no_active_deferral_marker(self) -> None:
        """Branch 138->162: no active deferral, falls through to normal flow."""
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="failing",
            copilot_review_id=100,
            review_state="CHANGES_REQUESTED",
            reviews=[
                ReviewInfo(id=100, user="Copilot", state="CHANGES_REQUESTED"),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with patch(
            "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
            return_value=None,
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        # Should proceed past deferral check (not SKIP due to deferral)
        assert "Deferred" not in result.details

    def test_proceeds_when_deferral_marker_cannot_be_deactivated(self) -> None:
        """Failed deferral consumption must not stall repair dispatch."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            copilot_review_id=100,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value={"review_id": "100", "active": True},
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.deactivate_deferral_marker",
                return_value=False,
            ),
            patch("agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.logger.warning") as mock_warning,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_repair.assert_called_once()
        mock_warning.assert_called_once()

    def test_proceeds_when_deferral_check_raises(self) -> None:
        """Deferral lookup failures log a warning and do not block dispatch."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="failing",
            head_sha="abc123",
            copilot_review_id=100,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 999

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                side_effect=RuntimeError("boom"),
            ),
            patch("agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.logger.warning") as mock_warning,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            result = action.execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        provider.dispatch_repair.assert_called_once()
        mock_warning.assert_called_once()


class TestDispatchRepairNewCcrActionability:
    """A content-blocking gate verdict makes a 0-inline COMMENTED review actionable.

    Guards the new-CCR-format gap: a "Not ready to approve" verdict heading or
    body-only suppressed comments block the gate while exposing no inline
    comments through the API. Such a PR must still trigger repair (otherwise it
    is blocked forever), while freshness reasons must NOT trigger repair.
    """

    def _snapshot(self, verdict: CopilotGateVerdict | None) -> PRStateSnapshot:
        return PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            active_session=False,
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            copilot_gate_verdict=verdict,
        )

    def _evaluate(self, verdict: CopilotGateVerdict | None):
        snapshot = self._snapshot(verdict)
        return DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

    def test_execute_new_ccr_not_approved_zero_inline(self) -> None:
        """'Not ready to approve' with 0 inline comments is actionable."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_NEW_CCR_NOT_APPROVED, review_id=100)
        result = self._evaluate(verdict)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True

    def test_execute_suppressed_comments_zero_inline(self) -> None:
        """Body-only suppressed comments (0 inline) are actionable."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_SUPPRESSED_COMMENTS, review_id=100, suppressed_count=8)
        result = self._evaluate(verdict)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True

    def test_execute_has_comments_zero_inline(self) -> None:
        """A body reporting posted comments (0 inline via API) is actionable."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_HAS_COMMENTS, review_id=100, body_comment_count=3)
        result = self._evaluate(verdict)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True

    def test_execute_has_comments_when_empty_inventory_has_no_filter_evidence(self) -> None:
        """A positive body count with an unfiltered empty inventory remains actionable."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_HAS_COMMENTS, review_id=100, body_comment_count=3)
        snapshot = replace(
            self._snapshot(verdict),
            effective_review_comment_count=0,
            effective_review_comment_count_review_id=100,
            effective_review_comment_filter_applied=False,
        )

        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))

        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["effective_review_work"] is True

    def test_skip_when_gate_verdict_passed(self) -> None:
        """A clean (passed) verdict is not actionable."""
        verdict = CopilotGateVerdict(passed=True, reason=REASON_CLEAN, review_id=100)
        result = self._evaluate(verdict)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["review_actionable"] is False

    def test_skip_when_freshness_reason_content_changed(self) -> None:
        """Content-changed is a freshness reason — needs a new review, not repair."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_CONTENT_CHANGED, review_id=100)
        result = self._evaluate(verdict)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["review_actionable"] is False

    def test_skip_when_freshness_reason_awaiting_fresh(self) -> None:
        """Awaiting-fresh is a freshness reason — needs a new review, not repair."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_AWAITING_FRESH, review_id=100)
        result = self._evaluate(verdict)
        assert result.decision == ActionDecision.SKIP
        assert result.preconditions["review_actionable"] is False

    def test_execute_when_review_id_differs_from_head(self) -> None:
        """A blocking verdict whose review id differs from copilot_review_id is actionable.

        The effective review the gate evaluated may be a prior-commit review selected
        by diff-hash freshness (whose id differs from ``copilot_review_id``), so the
        widened, identity-agnostic actionability must still dispatch a repair.
        """
        verdict = CopilotGateVerdict(passed=False, reason=REASON_NEW_CCR_NOT_APPROVED, review_id=999)
        result = self._evaluate(verdict)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True

    def test_execute_suppressed_only_approved_state_is_actionable(self) -> None:
        """A suppressed-only review submitted as APPROVED is actionable (state-agnostic)."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_SUPPRESSED_COMMENTS, review_id=100, suppressed_count=2)
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            copilot_gate_verdict=verdict,
        )
        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True

    def test_execute_new_ccr_not_approved_approved_state_is_actionable(self) -> None:
        """A new-CCR 'Not ready to approve' submitted as APPROVED is actionable (state-agnostic)."""
        verdict = CopilotGateVerdict(
            passed=False,
            reason=REASON_NEW_CCR_NOT_APPROVED,
            review_id=100,
            body_comment_count=0,
            suppressed_count=1,
        )
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            copilot_gate_verdict=verdict,
        )
        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True

    def test_execute_unparsed_suppression_is_actionable(self) -> None:
        """A REASON_UNPARSED_SUPPRESSION gate verdict (zero recovered entries) is actionable.

        Without this, a body-only COMMENTED review that declares suppressed
        comments but whose entries could not be parsed would never trigger
        repair — preserving the exact permanent stall this PR is intended to fix.
        """
        verdict = CopilotGateVerdict(
            passed=False, reason=REASON_UNPARSED_SUPPRESSION, review_id=100, suppressed_count=0
        )
        snapshot = PRStateSnapshot(
            pr_number=1,
            ci_status="passing",
            review_state="COMMENTED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            copilot_gate_verdict=verdict,
        )
        result = DispatchRepairAction().evaluate(snapshot, DerivedState(snapshot))
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True

    def test_execute_dispatches_review_repair_for_effective_review_id(self) -> None:
        """A suppressed-only APPROVED review with a mismatching id dispatches a 'review' repair.

        The repair (and its review-comment fetch) must target the gate's effective
        review id (999), not ``copilot_review_id`` (100).
        """
        verdict = CopilotGateVerdict(passed=False, reason=REASON_SUPPRESSED_COMMENTS, review_id=999, suppressed_count=3)
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            copilot_gate_verdict=verdict,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = [MagicMock(id=-1)]
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs["repair_type"] == "review"
        assert call_kwargs["review_id"] == 999
        provider.list_review_comments.assert_called_once_with(42, 999)

    def test_skip_when_duplicate_trigger_for_effective_review_id(self) -> None:
        """The per-review-id dedup guard still prevents repeated dispatch on the widened path."""
        verdict = CopilotGateVerdict(passed=False, reason=REASON_SUPPRESSED_COMMENTS, review_id=999, suppressed_count=3)
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="APPROVED",
            copilot_review_id=100,
            copilot_review_inline_count=0,
            copilot_gate_verdict=verdict,
            check_runs=[],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=True,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "No unattempted findings" in result.details
        provider.dispatch_repair.assert_not_called()

    def test_execute_new_ccr_not_approved_positive_body_comment_count(self) -> None:
        """New CCR not-approve with body_comment_count > 0 is still actionable via content-blocking path."""
        verdict = CopilotGateVerdict(
            passed=False, reason=REASON_NEW_CCR_NOT_APPROVED, review_id=100, body_comment_count=3
        )
        result = self._evaluate(verdict)
        assert result.decision == ActionDecision.EXECUTE
        assert result.preconditions["review_actionable"] is True


class TestDispatchRepairSuppressedDeferralCheck:
    """Tests for the read-only suppressed-comment deferral check in execute."""

    @staticmethod
    def _suppressed_snapshot(
        *,
        ci_status: str = "passing",
        copilot_review_id: int = 0,
        head_sha: str = "abc123",
        unresolved_threads: int = 0,
        repairable_threads: int = 0,
        reviews: list[ReviewInfo] | None = None,
    ) -> PRStateSnapshot:
        return PRStateSnapshot(
            pr_number=1,
            ci_status=ci_status,
            head_sha=head_sha,
            copilot_review_id=copilot_review_id,
            unresolved_threads=unresolved_threads,
            repairable_threads=repairable_threads,
            reviews=reviews or [],
            copilot_gate_verdict=CopilotGateVerdict(
                passed=False,
                reason=REASON_SUPPRESSED_COMMENTS,
                review_id=100,
                body_comment_count=0,
                suppressed_count=2,
            ),
        )

    def test_skips_dispatch_when_suppressed_deferral_is_recorded(self) -> None:
        snapshot = self._suppressed_snapshot()
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.read_active_suppressed_deferral",
                return_value={"review_id": "100", "issue": 4242, "active": True},
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        assert "triage issue" in result.details
        provider.dispatch_repair.assert_not_called()

    def test_does_not_skip_ci_repair_when_suppressed_deferral_is_recorded(self) -> None:
        snapshot = self._suppressed_snapshot(ci_status="failing")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "dispatch-bot"
        provider.dispatch_repair.return_value = 777

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.read_active_suppressed_deferral",
                return_value={"review_id": "100", "issue": 4242, "active": True},
            ) as mock_read,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        mock_read.assert_not_called()
        provider.dispatch_repair.assert_called_once()

    def test_does_not_skip_stuck_prior_threads_when_suppressed_deferral_is_recorded(self) -> None:
        snapshot = self._suppressed_snapshot(
            copilot_review_id=0,
            unresolved_threads=2,
            repairable_threads=2,
            head_sha="head123",
            reviews=[ReviewInfo(id=10, user="Copilot", state="CHANGES_REQUESTED", commit_sha="old123")],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "dispatch-bot"
        provider.dispatch_repair.return_value = 888

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.read_active_suppressed_deferral",
                return_value={"review_id": "100", "issue": 4242, "active": True},
            ) as mock_read,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.EXECUTE
        mock_read.assert_not_called()
        provider.dispatch_repair.assert_called_once()

    def test_marker_is_never_consumed(self) -> None:
        """The suppressed marker is durable evidence — it must not be deactivated."""
        snapshot = self._suppressed_snapshot()
        derived = DerivedState(snapshot)

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.read_active_suppressed_deferral",
                return_value={"review_id": "100", "active": True},
            ),
            patch("agentic_devtools.cli.ci.pipeline.deferral.deactivate_deferral_marker") as mock_deactivate,
        ):
            DispatchRepairAction().execute(MagicMock(), snapshot, derived)

        mock_deactivate.assert_not_called()

    def test_autofix_marker_is_still_consumed_when_deferral_exists(self) -> None:
        snapshot = self._suppressed_snapshot(copilot_review_id=100)
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value={"review_id": "100", "active": True},
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.deactivate_deferral_marker",
                return_value=True,
            ) as mock_deactivate,
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.read_active_suppressed_deferral",
                return_value={"review_id": "100", "active": True},
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert result.decision == ActionDecision.SKIP
        mock_deactivate.assert_called_once_with(provider, 1, 100)

    def test_proceeds_when_deferral_check_raises(self) -> None:
        """Fail-open: an unreadable marker must not stall repair dispatch."""
        snapshot = self._suppressed_snapshot()
        derived = DerivedState(snapshot)
        provider = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.read_active_suppressed_deferral",
                side_effect=RuntimeError("API down"),
            ),
        ):
            result = DispatchRepairAction().execute(provider, snapshot, derived)

        assert "triage issue" not in result.details

    def test_no_deferral_check_without_actionable_review(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, ci_status="failing")
        derived = DerivedState(snapshot)

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.deferral.read_active_deferral",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.read_active_suppressed_deferral",
            ) as mock_read,
        ):
            DispatchRepairAction().execute(MagicMock(), snapshot, derived)

        mock_read.assert_not_called()

    def test_declared_suppressed_count_is_passed_to_the_dispatch(self) -> None:
        """The gate blocks on the declared count, so the dispatch must carry it."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="abc123",
            review_state="CHANGES_REQUESTED",
            copilot_review_id=12,
            reviews=[
                ReviewInfo(
                    id=12,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    body="### Comments suppressed due to low confidence (4)\n\nprose",
                )
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = []
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            action.execute(provider, snapshot, derived)

        assert provider.dispatch_repair.call_args.kwargs["declared_author_comment_count"] == 4
        assert provider.dispatch_repair.call_args.kwargs["declared_author_comment_counts_by_review"] == {12: 4}

    def test_declared_suppressed_counts_are_preserved_per_prior_review(self) -> None:
        """Stuck prior threads must carry a per-review shortfall map, not just an aggregate total."""
        snapshot = PRStateSnapshot(
            pr_number=42,
            ci_status="passing",
            head_sha="head123",
            copilot_review_id=0,
            unresolved_threads=2,
            repairable_threads=2,
            reviews=[
                ReviewInfo(
                    id=11,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    commit_sha="old111",
                    submitted_at="2024-01-01T10:00:00Z",
                    body="### Comments suppressed due to low confidence (1)\n\nolder review",
                ),
                ReviewInfo(
                    id=12,
                    user="Copilot",
                    state="CHANGES_REQUESTED",
                    commit_sha="old222",
                    submitted_at="2024-01-01T11:00:00Z",
                    body="### Comments suppressed due to low confidence (2)\n\nnewer review",
                ),
            ],
        )
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.list_review_comments.return_value = []
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            action.execute(provider, snapshot, derived)

        call_kwargs = provider.dispatch_repair.call_args.kwargs
        assert call_kwargs["declared_author_comment_count"] == 3
        assert call_kwargs["declared_author_comment_counts_by_review"] == {12: 2, 11: 1}

    def test_declared_suppressed_count_is_zero_for_a_ci_only_dispatch(self) -> None:
        """No review context means no declared count to plumb."""
        snapshot = PRStateSnapshot(pr_number=42, ci_status="failing", head_sha="abc123")
        derived = DerivedState(snapshot)
        provider = MagicMock()
        provider.dispatch_repair.return_value = 77

        with (
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_deduplication",
                return_value=(False, 0),
            ),
            patch(
                "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.check_cycle_limit",
                return_value=(False, 1),
            ),
        ):
            action = DispatchRepairAction()
            action.execute(provider, snapshot, derived)

        assert provider.dispatch_repair.call_args.kwargs["declared_author_comment_count"] == 0
        assert provider.dispatch_repair.call_args.kwargs["declared_author_comment_counts_by_review"] == {}
