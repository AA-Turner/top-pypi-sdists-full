"""Behavior of the admitted initial-delivery recovery consumer."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.guards import AGENT_FAILED_LABEL
from agentic_devtools.cli.ci.models import AgentTaskInventoryAvailability, IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.actions.initial_delivery_recovery import InitialDeliveryRecovery
from agentic_devtools.cli.ci.pipeline.actions.retry_failed_session import RetryFailedSessionAction
from agentic_devtools.cli.ci.pipeline.delivery import InitialDeliveryEvidence, InitialDeliveryOutcome
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState
from agentic_devtools.cli.ci.pipeline.snapshot_models import DerivedState, PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

MODULE = "agentic_devtools.cli.ci.pipeline.actions.initial_delivery_recovery"
RETRY = "agentic_devtools.cli.ci.pipeline.actions.retry_failed_session"
HEAD = "a" * 40
NEW_HEAD = "b" * 40
HANDOFF = dict(head=NEW_HEAD, initial_task_id="initial-task", initial_plan_sha=HEAD, task_id="recovery-task")


@pytest.fixture
def recovery():
    evidence = InitialDeliveryEvidence(InitialDeliveryOutcome.NO_DELIVERY, "initial-task", HEAD, HEAD)
    snapshot = PRStateSnapshot(
        pr_number=12,
        head_sha=HEAD,
        head_branch="copilot/feature",
        head_repo_full_name="org/repo",
        base_repo_full_name="org/repo",
        initial_delivery=evidence,
    )
    provider = MagicMock()
    provider.get_dispatch_login.return_value = "workflow-bot"
    provider.list_issue_comments.return_value = []
    provider.get_agent_task_prompt.return_value = "Implement the linked issue"
    provider.list_closing_issues.return_value = []
    provider.get_pr_body.return_value = ""
    provider.get_pr_metadata.return_value = snapshot
    provider._dispatch_agent_retry.return_value = 99
    provider.dispatch_agent_retry.side_effect = AssertionError("Recovery must not use public FAILED dispatch")
    claims = provider._get_initial_delivery_claims.return_value
    claims.read.return_value = None
    claims.claim.return_value = True
    claims._reserve_escalation.return_value = True
    claims._transition_escalation.return_value = True
    no_delivery = (HEAD, InitialDeliveryOutcome.NO_DELIVERY)
    with (
        patch(
            f"{RETRY}.get_latest_session_state",
            return_value=SessionState(SessionOutcome.FINISHED, task_id="initial-task"),
        ) as state,
        patch(f"{MODULE}.get_latest_session_state", side_effect=lambda *a, **kw: state.return_value),
        patch(f"{MODULE}.is_copilot_session_active_via_agent_task", return_value=False) as active,
        patch(f"{MODULE}.classify_initial_delivery_with_head", return_value=no_delivery) as classify,
    ):
        yield provider, claims, snapshot, state, active, classify


def _run(provider, snapshot):
    action = RetryFailedSessionAction(provider, retry_limit=0)
    derived = DerivedState(snapshot)
    result = action.evaluate(snapshot, derived)
    if result.decision is ActionDecision.EXECUTE:
        result = action.execute(provider, snapshot, derived)
    return result


def _delivered_snapshot(snapshot):
    return replace(
        snapshot,
        head_sha=NEW_HEAD,
        initial_delivery=replace(
            snapshot.initial_delivery,
            outcome=InitialDeliveryOutcome.DELIVERED,
            head_sha=NEW_HEAD,
        ),
    )


def test_claim_precedes_single_dispatch_and_uses_separate_budget(recovery):
    provider, claims, snapshot, *_ = recovery
    provider._dispatch_agent_retry.side_effect = lambda *a, **kw: claims.claim.assert_called_once() or 99
    result = _run(provider, snapshot)
    assert result.preconditions["retry_dispatched"] is True
    provider._dispatch_agent_retry.assert_called_once()
    assert provider._dispatch_agent_retry.call_args.kwargs["initial_delivery"] is True
    assert "NO_DELIVERY" in provider._dispatch_agent_retry.call_args.args[1]
    provider.dispatch_agent_retry.assert_not_called()


@pytest.mark.parametrize("outcome", [InitialDeliveryOutcome.UNKNOWN, "NO_DELIVERY", None])
def test_untyped_or_unknown_admission_never_dispatches(recovery, outcome):
    provider, _, snapshot, *_ = recovery
    snapshot = replace(snapshot, initial_delivery=replace(snapshot.initial_delivery, outcome=outcome))
    assert _run(provider, snapshot).decision is ActionDecision.BLOCKED
    provider._dispatch_agent_retry.assert_not_called()


@pytest.mark.parametrize("active", [True, None])
def test_active_or_unknown_inventory_never_claims_or_escalates(recovery, active):
    provider, claims, snapshot, _, activity, _ = recovery
    activity.return_value = active
    assert _run(provider, snapshot).decision is ActionDecision.BLOCKED
    claims.claim.assert_not_called()
    provider.add_label.assert_not_called()


def test_incomplete_inventory_never_claims(recovery):
    provider, claims, snapshot, state, *_ = recovery
    state.return_value = SessionState(
        SessionOutcome.FINISHED,
        task_id="initial-task",
        inventory_availability=AgentTaskInventoryAvailability.PARTIAL,
    )
    assert _run(provider, snapshot).decision is ActionDecision.BLOCKED
    claims.claim.assert_not_called()


@pytest.mark.parametrize("mutation", ["head", "active", "unknown_diff", "task"])
def test_revalidates_immediately_before_claim_and_dispatch(recovery, mutation):
    provider, claims, snapshot, state, active, classify = recovery
    action = RetryFailedSessionAction(provider)
    derived = DerivedState(snapshot)
    assert action.evaluate(snapshot, derived).decision is ActionDecision.EXECUTE
    if mutation == "head":
        provider.get_pr_metadata.return_value = replace(snapshot, head_sha=NEW_HEAD)
    elif mutation == "active":
        active.return_value = True
    elif mutation == "task":
        state.return_value = SessionState(SessionOutcome.FINISHED, task_id="different-task")
    else:
        classify.return_value = (HEAD, InitialDeliveryOutcome.UNKNOWN)
    assert action.execute(provider, snapshot, derived).decision is ActionDecision.BLOCKED
    claims.claim.assert_not_called()
    provider._dispatch_agent_retry.assert_not_called()


def test_lost_claim_race_never_dispatches_or_prematurely_escalates(recovery):
    provider, claims, snapshot, *_ = recovery
    claims.claim.return_value = False
    assert _run(provider, snapshot).decision is ActionDecision.BLOCKED
    provider._dispatch_agent_retry.assert_not_called()
    provider.add_label.assert_not_called()


@pytest.mark.parametrize("receipt", [None, 0, True])
def test_uncertain_dispatch_receipt_escalates_without_second_attempt(recovery, receipt):
    provider, claims, snapshot, *_ = recovery
    provider._dispatch_agent_retry.return_value = receipt
    _run(provider, snapshot)
    assert provider._dispatch_agent_retry.call_count == 1
    provider.add_label.assert_called_once_with(12, AGENT_FAILED_LABEL)
    assert "uncertain" in provider.post_comment_as_pr_token.call_args.args[1].lower()


def test_dispatch_exception_escalates_with_unknown_cause_and_observed_evidence(recovery):
    provider, _, snapshot, *_ = recovery
    provider._dispatch_agent_retry.side_effect = TimeoutError("response lost")
    _run(provider, snapshot)
    body = provider.post_comment_as_pr_token.call_args.args[1]
    assert HEAD in body and "ZERO_DIFF" in body
    assert "unknown" in body.lower()
    assert "validator" not in body.lower()


def test_persisted_claim_survives_restart_and_terminal_event_changes(recovery):
    provider, claims, snapshot, state, *_ = recovery
    claims.read.return_value = {"created_at": (datetime.now(UTC) - timedelta(hours=2)).isoformat()}
    state.return_value = SessionState(SessionOutcome.FINISHED, task_id="initial-task", failure_event_id=765)
    _run(provider, snapshot)
    provider._dispatch_agent_retry.assert_not_called()
    provider.add_label.assert_called_once_with(12, AGENT_FAILED_LABEL)


def test_fresh_claim_waits_for_confirmation_not_immediate_escalation(recovery):
    provider, claims, snapshot, *_ = recovery
    claims.read.return_value = {"created_at": datetime.now(UTC).isoformat()}
    assert _run(provider, snapshot).decision is ActionDecision.BLOCKED
    provider._dispatch_agent_retry.assert_not_called()
    provider.add_label.assert_not_called()


def test_finished_recovery_without_delivery_exhausts_budget(recovery):
    provider, claims, snapshot, state, *_ = recovery
    claims.read.return_value = {"created_at": datetime.now(UTC).isoformat()}
    state.return_value = SessionState(SessionOutcome.FINISHED, task_id="recovery-task")
    _run(provider, snapshot)
    provider._dispatch_agent_retry.assert_not_called()
    provider.add_label.assert_called_once_with(12, AGENT_FAILED_LABEL)


def test_fresh_nonempty_recovery_returns_to_normal_pipeline(recovery):
    provider, claims, snapshot, state, _, classify = recovery
    snapshot = _delivered_snapshot(snapshot)
    provider.get_pr_metadata.return_value = snapshot
    claims.read.return_value = {"created_at": datetime.now(UTC).isoformat()}
    state.return_value = SessionState(SessionOutcome.FINISHED, task_id="recovery-task")
    classify.return_value = (NEW_HEAD, InitialDeliveryOutcome.DELIVERED)
    assert _run(provider, snapshot).decision is ActionDecision.SKIP
    provider._dispatch_agent_retry.assert_not_called()
    provider.request_copilot_review.assert_not_called()
    state.return_value = SessionState(SessionOutcome.FAILED, task_id="later-task")
    assert _run(provider, snapshot).decision is ActionDecision.BLOCKED
    classify.return_value = ("", InitialDeliveryOutcome.UNKNOWN)
    with patch.object(InitialDeliveryRecovery, "_should_defer_failed_task", side_effect=[None, True]):
        state.return_value = SessionState(SessionOutcome.FAILED, task_id="recovery-task")
        assert _run(provider, snapshot).decision is ActionDecision.BLOCKED
        state.return_value = SessionState(SessionOutcome.FAILED, task_id="later-task")
        assert _run(provider, snapshot).decision is ActionDecision.EXECUTE


@pytest.mark.parametrize(
    ("existing", "task_id", "expected"),
    [
        (None, "recovery-task", ActionDecision.BLOCKED),
        (HANDOFF, "recovery-task", ActionDecision.SKIP),
        (HANDOFF, "bad/task", ActionDecision.BLOCKED),
        (dict(HANDOFF, head=HEAD, initial_task_id="different-task"), "recovery-task", ActionDecision.BLOCKED),
    ],
)
def test_delivered_handoff_reconciles_create_conflicts(recovery, existing, task_id, expected):
    provider, claims, snapshot, state, _, classify = recovery
    snapshot = _delivered_snapshot(snapshot)
    provider.get_pr_metadata.return_value = snapshot
    recovery_claim = {"created_at": datetime.now(UTC).isoformat()}
    claims.read.side_effect = lambda _pr, _key, purpose: recovery_claim if purpose == "recovery" else existing
    claims.claim.return_value = False
    state.return_value = SessionState(SessionOutcome.FINISHED, task_id=task_id)
    classify.return_value = (NEW_HEAD, InitialDeliveryOutcome.DELIVERED)
    assert _run(provider, snapshot).decision is expected
    provider._dispatch_agent_retry.assert_not_called()
    if expected is ActionDecision.SKIP and task_id == "recovery-task":
        state.return_value = SessionState(SessionOutcome.FINISHED, task_id="t2")
        claims.claim.side_effect = [False, True, False, False]
        claims.read.side_effect = [recovery_claim, existing] * 2 + [dict(existing, task_id="t2")]
        assert all(_run(provider, snapshot).decision is ActionDecision.SKIP for _ in range(2))


@pytest.mark.parametrize(
    ("task_id", "has_evidence", "claim", "expected"),
    [
        ("later-task", True, None, True),
        ("later-task", True, {}, True),
        ("recovery-task", True, {}, None),
        ("t2", True, {}, None),
        ("bad/task", True, {}, None),
        (None, True, {}, None),
        ("later-task", False, None, False),
    ],
)
def test_only_unrelated_failed_task_uses_the_delivered_handoff(recovery, task_id, has_evidence, claim, expected):
    provider, _, snapshot, *_ = recovery
    if not has_evidence:
        snapshot = replace(snapshot, initial_delivery=None)
    store = MagicMock()
    store.read.return_value = {
        "head": HEAD,
        "initial_task_id": "initial-task",
        "initial_plan_sha": HEAD,
        "task_id": "recovery-task",
    }
    if task_id == "t2":
        store.read.side_effect = [store.read.return_value, {**store.read.return_value, "task_id": task_id}]
    action = InitialDeliveryRecovery(RetryFailedSessionAction(provider))
    outcome = SessionOutcome.FAILED if has_evidence else SessionOutcome.FINISHED
    state = SessionState(outcome, task_id=task_id)
    assert action._should_defer_failed_task(store, claim, snapshot, "a" * 64, state) is expected


@pytest.mark.parametrize("scenario", ["duplicate", "existing", "unrelated"])
def test_escalation_notice_identity_and_label_reconciliation(recovery, scenario):
    provider, claims, snapshot, *_ = recovery
    claims.read.return_value = {"created_at": (datetime.now(UTC) - timedelta(hours=2)).isoformat()}
    if scenario == "duplicate":
        claims._reserve_escalation.return_value = False
    else:
        key = InitialDeliveryRecovery._identity(snapshot.initial_delivery)
        comment = (
            f"<!-- agdt:agent-retry-escalation:{key} -->\n\nEscalation"
            if scenario == "existing"
            else "<!-- agdt:agent-retry-escalation:old -->\n<!-- agdt:agent-retry-escalation-pr:12 -->\n\nOld failure"
        )
        provider.list_issue_comments.return_value = [IssueCommentInfo(1, "workflow-bot", comment)]
    result = _run(provider, snapshot)
    if scenario == "duplicate":
        assert result.decision is ActionDecision.FAILED
        provider.post_comment_as_pr_token.assert_not_called()
        provider.add_label.assert_not_called()
    elif scenario == "existing":
        provider.post_comment_as_pr_token.assert_not_called()
        provider.add_label.assert_called_once_with(12, AGENT_FAILED_LABEL)
    else:
        body = provider.post_comment_as_pr_token.call_args.args[1]
        assert HEAD in body and "ZERO_DIFF" in body


@pytest.mark.parametrize(
    ("activity", "transition", "expected", "stage"),
    [
        ([False, True], True, ActionDecision.BLOCKED, None),
        ([False, False, True], True, ActionDecision.BLOCKED, "retryable"),
        ([False, False, True], False, ActionDecision.FAILED, "retryable"),
        ([False, False, False], False, ActionDecision.FAILED, "attempted"),
    ],
)
def test_escalation_checks_lifecycle_at_each_reservation_boundary(recovery, activity, transition, expected, stage):
    provider, claims, snapshot, _, active, _ = recovery
    active.side_effect = activity
    claims._transition_escalation.return_value = transition
    derived = DerivedState(snapshot)
    derived.set("initial_delivery_mode", True)
    derived.set("initial_delivery_key", InitialDeliveryRecovery._identity(snapshot.initial_delivery))
    action = InitialDeliveryRecovery(RetryFailedSessionAction(provider))
    result = action._escalate(provider, snapshot, derived, "Recovery failed")
    assert result.decision is expected
    provider.post_comment_as_pr_token.assert_not_called()
    provider.add_label.assert_not_called()
    if stage is None:
        claims._reserve_escalation.assert_not_called()
    else:
        claims._transition_escalation.assert_called_once()
        assert claims._transition_escalation.call_args.args[3:] == ("reserved", stage)


def test_head_moves_during_diff_observation_never_hands_off_stale_snapshot(recovery):
    provider, claims, snapshot, _, _, classify = recovery
    for observed_head, after in ((HEAD, NEW_HEAD), (NEW_HEAD, HEAD)):
        classify.return_value = (observed_head, InitialDeliveryOutcome.DELIVERED)
        provider.get_pr_metadata.side_effect = [snapshot, replace(snapshot, head_sha=after)]
        assert _run(provider, snapshot).decision is ActionDecision.BLOCKED and claims.claim.call_count == 0


def test_after_claim_activity_change_consumes_budget_without_dispatch(recovery):
    provider, claims, snapshot, _, active, _ = recovery
    claims.claim.side_effect = lambda *a, **kw: setattr(active, "return_value", True) or True
    assert _run(provider, snapshot).decision is ActionDecision.BLOCKED
    provider._dispatch_agent_retry.assert_not_called()
    provider.add_label.assert_not_called()


def test_dispatch_timeout_does_not_escalate_a_now_active_recovery(recovery):
    provider, _, snapshot, state, *_ = recovery

    def dispatch(*args, **kwargs):
        state.return_value = SessionState(SessionOutcome.ACTIVE, task_id="recovery-task")
        raise TimeoutError("response lost")

    provider._dispatch_agent_retry.side_effect = dispatch
    assert _run(provider, snapshot).decision is ActionDecision.BLOCKED
    provider.add_label.assert_not_called()


def test_bounded_existing_diagnostics_are_reported_without_retriggering_copilot(recovery):
    provider, claims, snapshot, *_ = recovery
    snapshot = replace(
        snapshot,
        initial_delivery=replace(
            snapshot.initial_delivery,
            push_diagnostics="guard rejected commit. @copilot\n" + "x" * 3000,
        ),
    )
    claims.read.return_value = {"created_at": (datetime.now(UTC) - timedelta(hours=2)).isoformat()}
    _run(provider, snapshot)
    body = provider.post_comment_as_pr_token.call_args.args[1]
    assert "guard rejected commit" in body
    assert "@copilot" not in body
    assert "x" * 2001 not in body


def test_failed_recovery_escalates_even_when_diff_is_unknown(recovery):
    provider, claims, snapshot, state, _, classify = recovery
    claims.read.return_value = {"created_at": datetime.now(UTC).isoformat()}
    state.return_value = SessionState(SessionOutcome.FAILED, task_id="recovery-task")
    classify.return_value = (HEAD, InitialDeliveryOutcome.UNKNOWN)
    _run(provider, snapshot)
    provider._dispatch_agent_retry.assert_not_called()
    assert "diff: `UNKNOWN`" in provider.post_comment_as_pr_token.call_args.args[1]
    assert classify.call_args.kwargs["completion_confirmed"] is False


def test_true_failed_session_without_recovery_claim_keeps_original_policy(recovery):
    provider, _, snapshot, state, *_ = recovery
    state.return_value = SessionState(SessionOutcome.FAILED, task_id="initial-task")
    result = _run(provider, snapshot)
    assert result.decision is ActionDecision.EXECUTE
    assert "retry budget" in provider.post_comment_as_pr_token.call_args.args[1].lower()


@pytest.mark.parametrize("error", [RuntimeError("unavailable"), ProviderRateLimitError(is_rate_limit=False)])
def test_unavailable_claim_evidence_blocks_mutation(recovery, error):
    provider, claims, snapshot, *_ = recovery
    claims.read.side_effect = error
    assert _run(provider, snapshot).decision is ActionDecision.BLOCKED
    provider._dispatch_agent_retry.assert_not_called()


def test_rate_limit_during_evaluation_propagates(recovery):
    provider, claims, snapshot, *_ = recovery
    claims.read.side_effect = ProviderRateLimitError(is_rate_limit=True)
    with pytest.raises(ProviderRateLimitError):
        _run(provider, snapshot)


@pytest.mark.parametrize("error", [TimeoutError("claim response lost"), ProviderRateLimitError(is_rate_limit=True)])
def test_claim_failure_never_dispatches(recovery, error):
    provider, claims, snapshot, *_ = recovery
    claims.claim.side_effect = error
    if isinstance(error, ProviderRateLimitError):
        with pytest.raises(ProviderRateLimitError):
            _run(provider, snapshot)
    else:
        assert _run(provider, snapshot).decision is ActionDecision.FAILED
    provider._dispatch_agent_retry.assert_not_called()


def test_escalation_identity_unknown_retains_claim_without_posting(recovery):
    provider, claims, snapshot, *_ = recovery
    claims.read.return_value = {"created_at": (datetime.now(UTC) - timedelta(hours=2)).isoformat()}
    provider.get_dispatch_login.return_value = ""
    assert _run(provider, snapshot).decision is ActionDecision.FAILED
    provider.post_comment_as_pr_token.assert_not_called()


@pytest.mark.parametrize(
    "evidence",
    [
        None,
        {},
        InitialDeliveryEvidence(
            InitialDeliveryOutcome.NO_DELIVERY,
            "bad\n@copilot",
            HEAD,
            HEAD,
        ),
    ],
)
def test_malformed_handoff_has_no_identity(recovery, evidence):
    from agentic_devtools.cli.ci.pipeline.actions.initial_delivery_recovery import InitialDeliveryRecovery

    assert InitialDeliveryRecovery._identity(evidence) == ""


@pytest.mark.parametrize("field,value", [("head_sha", "old"), ("initial_plan_sha", None), ("initial_task_id", None)])
def test_malformed_fields_never_dispatch(recovery, field, value):
    provider, _, snapshot, *_ = recovery
    snapshot = replace(snapshot, initial_delivery=replace(snapshot.initial_delivery, **{field: value}))
    assert _run(provider, snapshot).decision is ActionDecision.BLOCKED
    provider._dispatch_agent_retry.assert_not_called()


@pytest.mark.parametrize(
    ("admission", "classified", "expected"),
    [
        (InitialDeliveryOutcome.DELIVERED, InitialDeliveryOutcome.NO_DELIVERY, ActionDecision.BLOCKED),
        (InitialDeliveryOutcome.DELIVERED, InitialDeliveryOutcome.DELIVERED, ActionDecision.SKIP),
        (InitialDeliveryOutcome.UNKNOWN, InitialDeliveryOutcome.NO_DELIVERY, ActionDecision.BLOCKED),
    ],
)
def test_admission_requires_and_honors_fresh_delivery_result(recovery, admission, classified, expected):
    provider, claims, snapshot, state, _, classify = recovery
    snapshot = replace(snapshot, initial_delivery=replace(snapshot.initial_delivery, outcome=admission))
    classify.return_value = (HEAD, classified)
    assert _run(provider, snapshot).decision is expected
    claims.claim.assert_not_called()
    provider._dispatch_agent_retry.assert_not_called()


@pytest.mark.parametrize("outcome", list(SessionOutcome))
def test_unadmitted_session_guards_preserve_legacy_behavior(recovery, outcome):
    provider, _, snapshot, state, *_ = recovery
    snapshot = replace(snapshot, initial_delivery=None)
    state.return_value = SessionState(outcome, task_id="task")
    result = RetryFailedSessionAction(provider).evaluate(snapshot, DerivedState(snapshot))
    expected = (
        ActionDecision.BLOCKED
        if outcome in {SessionOutcome.ACTIVE, SessionOutcome.UNKNOWN}
        else ActionDecision.EXECUTE
        if outcome is SessionOutcome.FAILED
        else ActionDecision.SKIP
    )
    assert result.decision is expected


def test_escalation_rechecks_activity_after_comment_and_before_exclusion(recovery):
    provider, claims, snapshot, state, *_ = recovery
    claims.read.return_value = {"created_at": (datetime.now(UTC) - timedelta(hours=2)).isoformat()}

    def start_recovery(*args, **kwargs):
        state.return_value = SessionState(SessionOutcome.ACTIVE, task_id="recovery-task")
        return True

    provider.post_comment_as_pr_token.side_effect = start_recovery
    assert _run(provider, snapshot).decision is ActionDecision.FAILED
    provider.post_comment_as_pr_token.assert_called_once()
    provider.add_label.assert_not_called()
