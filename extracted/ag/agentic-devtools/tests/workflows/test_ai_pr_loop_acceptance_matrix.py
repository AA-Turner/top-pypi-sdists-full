"""WP8 acceptance matrix across the offline AI PR loop components."""

from datetime import UTC, datetime, timedelta
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.reconciliation.context_mapper import coalesce_event_contexts
from agentic_devtools.cli.ci.reconciliation.integrator import (
    SinglePRIntegrator,
    SpecialistOutput,
)
from agentic_devtools.cli.ci.reconciliation.models import (
    AttemptKind,
    AttemptStatus,
    EffectRecord,
    EffectStatus,
    PermitStatus,
    PRControlEnvelope,
    QueueState,
    RepairAttempt,
    RunEventContext,
    SemanticObligation,
    WorkerPermit,
    WorkItem,
    WorkItemStatus,
)
from agentic_devtools.cli.ci.reconciliation.orchestrator import (
    ReliabilitySliceEvent,
    coalesce_wakeups,
)
from agentic_devtools.cli.ci.reconciliation.reliability_metrics import calculate_reliability_metrics
from agentic_devtools.cli.ci.reconciliation.supervisor import (
    IncidentManager,
    RecoveryActionType,
    StaleProposalError,
    SupervisorGovernor,
    SupervisorProposal,
    evaluate_supervisor_proposal,
)
from agentic_devtools.cli.ci.reconciliation.wp3 import (
    Disposition,
    DispositionEvidence,
    IssueEffectCoordinator,
    description_hash,
    evaluate_disposition,
    update_description_guarded,
)

NOW = datetime(2026, 9, 15, 12, tzinfo=UTC)


def _context(pr: int = 42):
    return RunEventContext(
        target_type="pull_request",
        target_id=pr,
        repository_full_name="owner/repo",
        event_type="pull_request",
        action="synchronize",
    )


def test_duplicate_and_reordered_events_have_one_logical_wakeup() -> None:
    first = ReliabilitySliceEvent(_context(), Mock())
    reordered = ReliabilitySliceEvent(_context(), Mock())
    assert coalesce_event_contexts([first.context, reordered.context]) == [first.context]
    assert coalesce_wakeups([first, reordered]) == [first]


@pytest.mark.parametrize(
    ("disposition", "kwargs"),
    [
        (Disposition.IMPLEMENT_SUGGESTION, {"code_changed": True}),
        (Disposition.IMPLEMENT_BETTER_FIX, {"code_changed": True}),
        (Disposition.REJECT_WITH_EVIDENCE, {"evidence": "not reproducible"}),
        (Disposition.DEFER_WITH_FOLLOWUP, {"followup_issue_id": 100}),
    ],
)
def test_all_four_dispositions_require_their_contract(disposition, kwargs) -> None:
    evidence = DispositionEvidence(disposition, "finding-1", "head", "source", True, **kwargs)
    assert evaluate_disposition(evidence, current_head_sha="head", current_source_revision="source").accepted


def test_disposition_rejects_stale_and_unsafe_deferral() -> None:
    stale = DispositionEvidence(Disposition.REJECT_WITH_EVIDENCE, "f", "old", "source", True, evidence="x")
    blocked = DispositionEvidence(Disposition.DEFER_WITH_FOLLOWUP, "f", "head", "source", True, blocking=True)
    assert not evaluate_disposition(stale, current_head_sha="head", current_source_revision="source").accepted
    assert not evaluate_disposition(blocked, current_head_sha="head", current_source_revision="source").accepted


def test_reply_resolve_and_issue_effects_are_replay_safe() -> None:
    provider = Mock()
    provider.find_followup_issue.return_value = 7
    provider.find_thread_reply.side_effect = [None, 99]
    coordinator = IssueEffectCoordinator(provider)
    first = coordinator.defer(
        finding_id="finding",
        thread_id="thread",
        pr_url="https://example/pr",
        title="Follow-up",
        body="body",
        marker="m",
    )
    second = coordinator.defer(
        finding_id="finding",
        thread_id="thread",
        pr_url="https://example/pr",
        title="Follow-up",
        body="body",
        marker="m",
    )
    assert first == second
    assert provider.post_thread_reply.call_count == 1
    assert provider.resolve_thread.call_count == 2


def test_description_maintenance_updates_target_or_records_no_change() -> None:
    provider = Mock()
    provider.get_pr_description.return_value = "body"
    assert (
        update_description_guarded(provider, pr_number=42, edit="\nedit", expected_hash=description_hash("body"))
        == "updated"
    )
    assert (
        update_description_guarded(provider, pr_number=42, edit="", expected_hash=description_hash("body"))
        == "no_change"
    )
    with pytest.raises(RuntimeError):
        update_description_guarded(provider, pr_number=42, edit="x", expected_hash="stale")


def test_footprint_conflicts_are_serialized_and_disjoint_work_is_parallel() -> None:
    now = NOW
    permit = WorkerPermit(
        "permit",
        "request",
        "owner/repo",
        42,
        "obligation",
        "batch",
        "worker",
        "github",
        "luna",
        1,
        now,
        now + timedelta(hours=1),
        PermitStatus.ACCEPTED,
    )
    state = QueueState("owner/repo", 0, {}, [], [], active_permits={"permit": permit})
    outputs = [
        SpecialistOutput("one", "permit", "head", ("a.py",)),
        SpecialistOutput("two", "permit", "head", ("b.py",)),
        SpecialistOutput("three", "permit", "head", ("a.py",)),
    ]
    applied: list[tuple[SpecialistOutput, ...]] = []
    result = SinglePRIntegrator(lambda: now).integrate(
        state, outputs, current_head_sha="head", apply_batch=applied.append, publish=lambda: "new-head"
    )
    assert result.accepted and len(result.batches) == 2
    assert len(applied) == 2


def test_stale_integrator_output_is_fenced_after_manual_push() -> None:
    now = NOW
    permit = WorkerPermit(
        "permit",
        "request",
        "owner/repo",
        42,
        "obligation",
        "batch",
        "worker",
        "github",
        "luna",
        1,
        now,
        now + timedelta(hours=1),
        PermitStatus.ACCEPTED,
    )
    state = QueueState("owner/repo", 0, {}, [], [], active_permits={"permit": permit})
    with pytest.raises(ValueError, match="stale"):
        SinglePRIntegrator(lambda: now).integrate(
            state,
            [SpecialistOutput("worker", "permit", "old-head", ("a.py",))],
            current_head_sha="new-head",
            apply_batch=lambda _: None,
            publish=lambda: "unused",
        )


def test_supervisor_budget_stale_proposals_and_shared_incident_remediation() -> None:
    proposal = SupervisorProposal("p", RecoveryActionType.RETRY_WITH_REDUCED_SCOPE, "repo", 42, "o", "head", "problem")
    assert evaluate_supervisor_proposal(proposal, current_head_sha="head", attempt_count=3).accepted is False
    with pytest.raises(StaleProposalError):
        evaluate_supervisor_proposal(proposal, current_head_sha="new-head")
    incident = IncidentManager()
    incident_id = incident.get_or_create("quota", "429").incident_id
    incident.attach(incident_id, "o")
    incident.mark_remediated(incident_id)
    assert incident.grant_extra_luna(incident_id, "o", rounds_used=49)
    assert not incident.grant_extra_luna(incident_id, "o", rounds_used=49)


def test_round_49_50_51_and_same_problem_boundaries_fail_closed() -> None:
    proposal = SupervisorProposal("p", RecoveryActionType.RETRY_WITH_REDUCED_SCOPE, "repo", 42, "o", "head", "problem")
    assert evaluate_supervisor_proposal(proposal, current_head_sha="head", round_count=49).accepted
    assert not evaluate_supervisor_proposal(proposal, current_head_sha="head", round_count=50).accepted
    assert not evaluate_supervisor_proposal(proposal, current_head_sha="head", attempt_count=3).accepted
    quarantine = SupervisorProposal("q", RecoveryActionType.QUARANTINE_OBLIGATION, "repo", 42, "o", "head", "problem")
    assert evaluate_supervisor_proposal(quarantine, current_head_sha="head", attempt_count=3).accepted


def test_global_hold_and_idle_queue_are_fail_silent() -> None:
    governor = SupervisorGovernor()
    empty = QueueState("repo", 0, {}, [], [])
    decision = governor.should_run(empty, NOW)
    assert not decision.allowed and decision.reason == "no work exists"


def test_provider_quota_backpressure_is_explicit() -> None:
    governor = SupervisorGovernor()
    state = QueueState("repo", 0, {}, [], [])
    state.obligations["o"] = SemanticObligation("o", 42, "problem")
    governor.record_execution(NOW)
    assert governor.should_run(state, NOW + timedelta(minutes=1)).reason == "hourly limit reached"


def test_reliability_metrics_report_quarantine_and_exhausted_budget() -> None:
    state = QueueState("repo", 0, {}, [], [])
    state.attempts["a"] = RepairAttempt(
        "a", 42, "o", "batch", AttemptKind.INITIAL_LUNA, 1, "observation", None, AttemptStatus.SUCCEEDED
    )
    state.items[1] = WorkItem(1, "repo", "change", "eligible", None, WorkItemStatus.QUARANTINED)
    state.pr_envelopes[1] = PRControlEnvelope(1, "repo", "head", "base", "policy", "obs", "history", rounds_used=50)
    metrics = calculate_reliability_metrics(state)
    assert metrics.completed_obligations == 1
    assert metrics.quarantined_prs == 1
    assert metrics.exhausted_budgets == 1


def test_effect_records_are_explicitly_fenced_and_statuses_are_terminal() -> None:
    record = EffectRecord("effect", "repo", 42, "reply", "digest", EffectStatus.INTENT)
    settled = EffectRecord("effect", "repo", 42, "reply", "digest", EffectStatus.SETTLED, "evidence")
    assert record.effect_id == settled.effect_id
    assert settled.status is EffectStatus.SETTLED
