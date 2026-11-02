"""Cross-component repair eligibility, receipt persistence and recovery regressions."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.guards import check_deduplication, is_duplicate_trigger
from agentic_devtools.cli.ci.models import CheckRunStatus, IssueCommentInfo, ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions import ApproveAction, DispatchRepairAction, MergeAction
from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_HAS_COMMENTS, CopilotGateVerdict
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.repair_attempts import RepairAttemptTracker
from agentic_devtools.cli.ci.pipeline.runner import run_pipeline
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.ci.pipeline.summary import SUMMARY_SENTINEL
from agentic_devtools.cli.ci.provider import RepairDispatchBookkeepingRateLimitError, RepairDispatchNotAttemptedError
from agentic_devtools.cli.ci.repair_accounting import (
    RepairDispatchLedger,
    exhausted_repair_is_unchanged,
    repair_work_key,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


@pytest.fixture
def provider():
    """A serialized provider with durable in-memory comments and real accounting."""
    provider = MagicMock()
    provider.get_pr_token_login.return_value = "dispatch-bot"
    provider.comments = []
    provider.inventory = {
        10: [ReviewCommentInfo(101, "x.py", "Fix this", "", source_review_id=10)],
        11: [ReviewCommentInfo(102, "x.py", "New finding", "", source_review_id=11)],
    }
    provider.list_issue_comments.side_effect = lambda _: list(provider.comments)
    provider.list_review_comments.side_effect = lambda _, review: list(provider.inventory.get(review, []))
    provider.list_review_thread_states.return_value = {}
    provider.list_review_threads_by_thread_id.return_value = {}

    def post(pr_number, body):
        comment_id = len(provider.comments) + 1
        provider.comments.append(IssueCommentInfo(comment_id, "dispatch-bot", body))
        return comment_id

    def update(comment_id, body):
        index = next(index for index, item in enumerate(provider.comments) if item.id == comment_id)
        provider.comments[index] = replace(provider.comments[index], body=body)

    def find(pr_number, marker):
        matches = [item for item in provider.comments if marker in item.body]
        return (matches[-1].id, matches[-1].body) if matches else None

    def dispatch(**kwargs):
        key = repair_work_key(
            kwargs["review_id"],
            kwargs["review_comments"],
            kwargs["failed_checks"],
            kwargs["declared_author_comment_counts_by_review"],
        )
        ledger = RepairDispatchLedger(provider, kwargs["pr_number"], kwargs["head_sha"], kwargs["review_id"], key)
        trigger = f"<!-- copilot-trigger:{kwargs['review_id']}:{datetime.now(UTC).isoformat()} -->"
        return post(kwargs["pr_number"], f"@copilot repair\n{trigger}\n{ledger.evidence_marker}")

    provider.post_comment_as_pr_token.side_effect = post
    provider.post_comment.side_effect = post
    provider.update_comment.side_effect = update
    provider.update_comment_as_pr_token.side_effect = update
    provider.find_comment.side_effect = find
    provider.dispatch_repair.side_effect = dispatch
    return provider


@pytest.fixture(autouse=True)
def inactive_session():
    with patch(
        "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_copilot_session_active_via_agent_task",
        return_value=False,
    ):
        yield


def test_new_review_on_same_head_ignores_legacy_inflation_and_immediate_repeat(provider):
    provider.post_comment(42, "<!-- repair-dispatch:abc123:8 -->")
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="abc123",
        ci_status="passing",
        review_state="CHANGES_REQUESTED",
        copilot_review_id=10,
    )
    action = DispatchRepairAction()
    first = action.execute(provider, snapshot, DerivedState(snapshot))
    repeat = action.execute(provider, snapshot, DerivedState(snapshot))
    new_review = replace(snapshot, copilot_review_id=11)
    second = action.execute(provider, new_review, DerivedState(new_review))

    assert first.decision is ActionDecision.EXECUTE
    assert repeat.decision is ActionDecision.SKIP
    assert second.decision is ActionDecision.EXECUTE
    assert provider.dispatch_repair.call_count == 2
    key = repair_work_key(11, provider.inventory[11], [])
    assert check_deduplication(provider, 42, "abc123", review_id=11, work_key=key) == (False, 1)


def test_effective_selected_review_owns_the_budget_not_latest_review(provider):
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="abc123",
        ci_status="passing",
        review_state="APPROVED",
        copilot_review_id=11,
        copilot_gate_verdict=CopilotGateVerdict(passed=False, reason=REASON_HAS_COMMENTS, review_id=10),
    )
    result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))
    assert result.decision is ActionDecision.EXECUTE
    assert provider.dispatch_repair.call_args.kwargs["review_id"] == 10
    key = repair_work_key(10, provider.inventory[10], [])
    assert check_deduplication(provider, 42, "abc123", review_id=10, work_key=key) == (False, 1)
    assert check_deduplication(provider, 42, "abc123", review_id=11, work_key=key) == (False, 0)


def test_changed_finding_scope_on_same_review_recovers_after_existing_trigger_ttl(provider):
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="abc123",
        ci_status="passing",
        review_state="CHANGES_REQUESTED",
        copilot_review_id=10,
    )
    action = DispatchRepairAction()
    assert action.execute(provider, snapshot, DerivedState(snapshot)).decision is ActionDecision.EXECUTE
    provider.inventory[10] = [ReviewCommentInfo(-1, "x.py", "new", "", source_review_id=10)]
    future = datetime.now(UTC) + timedelta(days=2)
    with patch(
        "agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.is_duplicate_trigger",
        side_effect=lambda provider, number, review: is_duplicate_trigger(provider, number, review, now=future),
    ):
        assert action.execute(provider, snapshot, DerivedState(snapshot)).decision is ActionDecision.EXECUTE
    assert provider.dispatch_repair.call_count == 2
    key = repair_work_key(10, provider.inventory[10], [], {10: 1})
    assert check_deduplication(provider, 42, "abc123", review_id=10, work_key=key) == (False, 1)


def test_ci_attempt_reservation_blocks_repeat_and_changed_checks_on_same_head(provider):
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="abc123",
        ci_status="failing",
        ci_failed_checks=["lint"],
        check_runs=[CheckRunStatus(1, "lint", "completed", "failure")],
    )
    action = DispatchRepairAction()
    assert action.execute(provider, snapshot, DerivedState(snapshot)).decision is ActionDecision.EXECUTE
    reordered_run = replace(snapshot, check_runs=[replace(snapshot.check_runs[0], id=999)])
    repeated = action.execute(provider, reordered_run, DerivedState(reordered_run))
    assert repeated.decision is ActionDecision.SKIP
    assert repeated.dedup_limit_reached
    assert repeated.repair_exhaustion_marker.startswith("<!-- repair-dispatch:exhausted:abc123:")
    provider.comments.append(
        IssueCommentInfo(
            99,
            "github-actions[bot]",
            f"{SUMMARY_SENTINEL}\n{repeated.repair_exhaustion_marker}",
        )
    )
    with patch(
        "agentic_devtools.cli.ci.pipeline.snapshot_builder.build_pr_state_snapshot",
        return_value=reordered_run,
    ):
        assert exhausted_repair_is_unchanged(provider, 42, "abc123") is True
    changed = replace(
        snapshot, ci_failed_checks=["test"], check_runs=[CheckRunStatus(2, "test", "completed", "failure")]
    )
    assert action.execute(provider, changed, DerivedState(changed)).decision is ActionDecision.SKIP
    assert provider.dispatch_repair.call_count == 1


def test_uncertain_creation_remains_pending_without_success_or_replacement(provider):
    snapshot = PRStateSnapshot(pr_number=42, head_sha="abc123", ci_status="failing")
    provider.dispatch_repair.side_effect = RuntimeError("connection lost after POST")
    action = DispatchRepairAction()
    first = action.execute(provider, snapshot, DerivedState(snapshot))
    repeat = action.execute(provider, snapshot, DerivedState(snapshot))
    assert first.decision is ActionDecision.FAILED
    assert first.definitive_no_mutation is False
    assert repeat.decision is ActionDecision.FAILED
    assert provider.dispatch_repair.call_count == 1
    ledger = RepairDispatchLedger(provider, 42, "abc123", 0, repair_work_key(0, [], []))
    assert ledger.read()[1] is True
    key = repair_work_key(0, [], [])
    assert check_deduplication(provider, 42, "abc123", max_dispatches=1, review_id=0, work_key=key) == (False, 0)


def test_confirmed_quota_rejection_releases_repair_intent_and_finding_reservation(provider):
    snapshot = PRStateSnapshot(pr_number=42, head_sha="abc123", ci_status="failing")
    quota = ProviderRateLimitError(
        retry_after_seconds=30,
        provider="github",
        credential_identity="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
    )

    def reject_dispatch(**_kwargs):
        raise RepairDispatchNotAttemptedError("Agent Tasks POST rejected by quota") from quota

    provider.dispatch_repair.side_effect = reject_dispatch

    with pytest.raises(ProviderRateLimitError) as exc_info:
        DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

    assert exc_info.value is quota
    ledger = RepairDispatchLedger(provider, 42, "abc123", 0, repair_work_key(0, [], []))
    assert ledger.read()[:2] == (set(), False)
    assert RepairAttemptTracker(provider, 42, "abc123").attempted == set()
    assert not any(comment.body.startswith("@copilot") for comment in provider.comments)


def test_retries_confirmed_quota_rejection_after_ledger_cleanup_rate_limit(provider):
    snapshot = PRStateSnapshot(pr_number=42, head_sha="abc123", ci_status="failing")
    quota = ProviderRateLimitError(retry_after_seconds=30, provider="github")
    original_dispatch = provider.dispatch_repair.side_effect
    original_update = provider.update_comment_as_pr_token.side_effect
    fail_ledger_retirement = True

    def reject_once(**kwargs):
        if provider.dispatch_repair.call_count == 1:
            raise RepairDispatchNotAttemptedError("Agent Tasks POST rejected by quota") from quota
        return original_dispatch(**kwargs)

    def rate_limit_ledger_retirement(comment_id, body):
        nonlocal fail_ledger_retirement
        if comment_id == 1 and fail_ledger_retirement:
            fail_ledger_retirement = False
            raise ProviderRateLimitError(retry_after_seconds=30, provider="github")
        original_update(comment_id, body)

    provider.dispatch_repair.side_effect = reject_once
    provider.update_comment_as_pr_token.side_effect = rate_limit_ledger_retirement

    with pytest.raises(ProviderRateLimitError):
        DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

    ledger = RepairDispatchLedger(provider, 42, "abc123", 0, repair_work_key(0, [], []))
    assert ledger.read()[1] is True
    assert RepairAttemptTracker(provider, 42, "abc123").attempted == set()

    resumed = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

    assert resumed.decision is ActionDecision.EXECUTE
    assert ledger.read()[:2] == ({"comment-4"}, False)
    assert provider.dispatch_repair.call_count == 2


def test_review_dispatch_reconciles_evidence_without_already_reserved_ci_checks(provider):
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="abc123",
        ci_status="failing",
        ci_failed_checks=["lint"],
        check_runs=[CheckRunStatus(1, "lint", "completed", "failure")],
        review_state="CHANGES_REQUESTED",
        copilot_review_id=10,
    )
    provider.post_comment(
        42,
        '<!-- repair-dispatch-findings:42:abc123:v1 -->\n{"attempted": ["ci"]}',
    )
    first_dispatch = True

    def dispatch(**kwargs):
        nonlocal first_dispatch
        key = repair_work_key(
            kwargs["review_id"],
            kwargs["review_comments"],
            kwargs["failed_checks"],
            kwargs["declared_author_comment_counts_by_review"],
        )
        ledger = RepairDispatchLedger(provider, 42, "abc123", kwargs["review_id"], key)
        comment_id = provider.post_comment(
            42,
            f"@copilot repair\n{ledger.evidence_marker}",
        )
        if first_dispatch:
            first_dispatch = False
            raise RuntimeError("dispatch response lost")
        return comment_id

    provider.dispatch_repair.side_effect = dispatch
    action = DispatchRepairAction()

    failed = action.execute(provider, snapshot, DerivedState(snapshot))
    recovered = action.execute(provider, snapshot, DerivedState(snapshot))

    assert failed.decision is ActionDecision.FAILED
    assert recovered.decision is ActionDecision.SKIP
    assert provider.dispatch_repair.call_count == 1
    assert provider.dispatch_repair.call_args.kwargs["failed_checks"] == []
    key = repair_work_key(10, provider.inventory[10], [])
    ledger = RepairDispatchLedger(provider, 42, "abc123", 10, key)
    assert ledger.read()[:2] == ({"comment-3"}, False)


def test_review_only_provider_evidence_recovers_against_ledger_without_checks(provider):
    root = provider.inventory[10][0]
    expected_key = repair_work_key(10, [root], [])
    github_provider = GitHubActionsProvider(repo="owner/repo")
    ledger = RepairDispatchLedger(github_provider, 42, "abc123", 10, expected_key)
    comments: list[IssueCommentInfo] = []

    def post_comment(_pr_number, body):
        comment_id = len(comments) + 1
        comments.append(IssueCommentInfo(comment_id, "dispatch-bot", body))
        return comment_id

    def post_repair_comment(*, pr_number, body, token, classify_quota_rejection=False):
        assert classify_quota_rejection is True
        post_comment(pr_number, body)
        return f'{{"id": {comments[-1].id}}}'

    def update_comment(comment_id, body):
        comments[comment_id - 1] = IssueCommentInfo(comment_id, "dispatch-bot", body)

    with (
        patch.dict("os.environ", {"AGDT_USE_AGENT_TASKS_API": ""}),
        patch("agentic_devtools.cli.ci.github_provider._require_default_workflow_token", return_value="token"),
        patch("agentic_devtools.cli.ci.github_provider._build_repair_comment", return_value="@copilot repair"),
        patch.object(github_provider, "list_issue_comments", side_effect=lambda _: list(comments)),
        patch.object(github_provider, "get_pr_token_login", return_value="dispatch-bot"),
        patch.object(github_provider, "post_comment_as_pr_token", side_effect=post_comment),
        patch.object(github_provider, "update_comment_as_pr_token", side_effect=update_comment),
        patch.object(github_provider, "_post_repair_comment", side_effect=post_repair_comment),
    ):
        ledger.begin()
        github_provider.dispatch_repair(
            pr_number=42,
            head_sha="abc123",
            repair_type="review",
            failed_checks=[CheckRunStatus(9, "stale CI check", "completed", "failure")],
            review_comments=[root],
            review_id=10,
        )
        ledger.reconcile()
        assert ledger.read()[:2] == ({"comment-2"}, False)


def test_attempted_review_root_still_checks_capped_scope_and_suppresses_watchdog(provider):
    root = provider.inventory[10][0]
    key = repair_work_key(10, [root], [])
    ledger = RepairDispatchLedger(provider, 42, "abc123", 10, key)
    for receipt in ("task:one", "task:two", "task:three"):
        ledger.record(receipt)
    provider.post_comment(
        42,
        '<!-- repair-dispatch-findings:42:abc123:v1 -->\n{"attempted": ["root:101"]}',
    )
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="abc123",
        ci_status="passing",
        review_state="CHANGES_REQUESTED",
        copilot_review_id=10,
        unresolved_threads=1,
        repairable_threads=1,
        reviews=[ReviewInfo(10, "copilot[bot]", "CHANGES_REQUESTED", "abc123")],
    )

    result = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

    assert result.decision is ActionDecision.SKIP
    assert result.dedup_limit_reached
    assert "review=10" in result.details
    provider.dispatch_repair.assert_not_called()
    provider.post_comment(42, f"{SUMMARY_SENTINEL}\n{result.repair_exhaustion_marker}")
    with patch(
        "agentic_devtools.cli.ci.pipeline.snapshot_builder.build_pr_state_snapshot",
        return_value=snapshot,
    ):
        assert exhausted_repair_is_unchanged(provider, 42, "abc123") is True


def test_task_receipt_is_recorded_before_bookkeeping_quota_pause(provider):
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="abc123",
        ci_status="passing",
        review_state="CHANGES_REQUESTED",
        copilot_review_id=10,
    )
    rate_limit = ProviderRateLimitError(provider="github", is_rate_limit=True)
    provider.dispatch_repair.side_effect = RepairDispatchBookkeepingRateLimitError("task:owner/repo:9999", rate_limit)
    key = repair_work_key(10, provider.inventory[10], [])
    ledger = RepairDispatchLedger(provider, 42, "abc123", 10, key)

    with pytest.raises(ProviderRateLimitError):
        DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))

    assert ledger.read()[:2] == ({"task:owner/repo:9999"}, False)


def test_real_creation_with_failed_accounting_is_not_a_no_mutation_failure(provider):
    snapshot = PRStateSnapshot(pr_number=42, head_sha="abc123", ci_status="failing")
    original_update = provider.update_comment_as_pr_token.side_effect
    provider.update_comment_as_pr_token.side_effect = RuntimeError("receipt write failed")
    derived = DerivedState(snapshot)
    result = DispatchRepairAction().execute(provider, snapshot, derived)
    assert result.decision is ActionDecision.EXECUTE
    assert result.definitive_no_mutation is False
    assert derived.repair_dispatched
    assert "accounting unresolved" in result.details

    provider.update_comment_as_pr_token.side_effect = original_update
    again = DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot))
    assert again.decision is ActionDecision.SKIP
    assert again.dedup_limit_reached
    assert again.repair_exhaustion_marker.startswith("<!-- repair-dispatch:exhausted:abc123:")
    assert provider.dispatch_repair.call_count == 1
    ledger = RepairDispatchLedger(provider, 42, "abc123", 0, repair_work_key(0, [], []))
    assert ledger.read()[:2] == ({"comment-3"}, False)


def test_exhausted_runner_keeps_findings_blocking_approval_and_merge(provider):
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="abc123",
        ci_status="passing",
        review_state="CHANGES_REQUESTED",
        copilot_review_id=10,
        reviews=[ReviewInfo(10, "Copilot", "CHANGES_REQUESTED")],
        unresolved_threads=1,
        repairable_threads=1,
        labels=["ai-auto-merge-allowed"],
    )
    ledger = RepairDispatchLedger(provider, 42, "abc123", 10, repair_work_key(10, provider.inventory[10], []))
    ledger.record(77)
    ledger.record(78)
    ledger.record(79)
    old = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    provider.comments[0] = replace(
        provider.comments[0], body=provider.comments[0].body.rsplit("\n", 1)[0] + f"\n<!-- copilot-trigger:10:{old} -->"
    )
    results = run_pipeline(provider, snapshot, actions=[DispatchRepairAction(), ApproveAction(), MergeAction()]).results
    dispatch = next(result for result in results if result.name == "dispatch_repair")
    assert dispatch.dedup_limit_reached
    assert all(result.decision is not ActionDecision.EXECUTE for result in results)
    provider.approve_pr.assert_not_called()
    provider.merge_pr.assert_not_called()


def test_spoofed_trigger_or_receipt_does_not_invent_success(provider):
    key = repair_work_key(10, provider.inventory[10], [])
    ledger = RepairDispatchLedger(provider, 42, "abc123", 10, key)
    provider.comments.append(
        IssueCommentInfo(1, "stranger", f"@copilot\n<!-- copilot-trigger:10 -->\n{ledger.evidence_marker}")
    )
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="abc123",
        ci_status="passing",
        review_state="CHANGES_REQUESTED",
        copilot_review_id=10,
    )
    assert ledger.read()[0] == set()
    assert DispatchRepairAction().execute(provider, snapshot, DerivedState(snapshot)).decision is ActionDecision.EXECUTE
