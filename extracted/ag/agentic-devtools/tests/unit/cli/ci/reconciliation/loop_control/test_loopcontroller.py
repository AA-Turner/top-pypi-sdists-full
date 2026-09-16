"""Unit tests for the offline controller's explicit safety boundary."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.reconciliation.loop_control import AdmissionBlockedError, LoopController
from agentic_devtools.cli.ci.reconciliation.models import (
    AdmissionRequestStatus,
    AttemptKind,
    AttemptStatus,
    PermitStatus,
    ProviderCapacityObservation,
    QuarantineRecord,
    QueueState,
    WorkItem,
    WorkItemStatus,
    _history_digest,
    _legacy_digest,
    validate_queue_state,
)


def test_controller_requires_verifier_and_clock():
    with pytest.raises(ValueError, match="verifier and clock"):
        LoopController(None, None)


def test_unknown_legacy_history_is_not_bootstrap_authority():
    controller = LoopController(lambda proof: True, lambda: datetime.now(UTC))
    state = QueueState("owner/repo", 0, {}, [], [])
    with pytest.raises(AdmissionBlockedError, match="migration/activation"):
        controller.register_obligation(state, "problem", 42)


def test_shared_admission_lifecycle_and_rejections(foundation):
    f = foundation()
    c = controller(f)
    state = f.state
    observation = ProviderCapacityObservation(
        "github",
        f.now,
        f.now + timedelta(minutes=5),
        2,
        0,
        0,
        "capacity",
    )
    with pytest.raises(AdmissionBlockedError, match="missing"):
        c.observe_provider_capacity(state, replace(observation, complete=False))
    state = c.observe_provider_capacity(state, observation)
    with pytest.raises(AdmissionBlockedError, match="reordered"):
        c.observe_provider_capacity(state, replace(observation, observed_at=f.now - timedelta(seconds=1)))
    with pytest.raises(ValueError, match="identities"):
        c.request_worker_admission(
            state,
            request_id="",
            pr_number=42,
            obligation_id="problem",
            batch_id="batch",
            worker_id="worker",
            provider="github",
        )
    with pytest.raises(AdmissionBlockedError, match="unsupported"):
        c.request_worker_admission(
            state,
            request_id="bad-model",
            pr_number=42,
            obligation_id="problem",
            batch_id="batch",
            worker_id="worker",
            provider="github",
            model="other",
        )
    with pytest.raises(AdmissionBlockedError, match="historical budget"):
        c.request_worker_admission(
            state,
            request_id="unknown-pr",
            pr_number=43,
            obligation_id="problem",
            batch_id="batch",
            worker_id="worker",
            provider="github",
        )
    with pytest.raises(AdmissionBlockedError, match="stale controller"):
        c.request_worker_admission(
            replace(state, global_epoch=2),
            request_id="stale-epoch",
            pr_number=42,
            obligation_id="problem",
            batch_id="batch",
            worker_id="worker",
            provider="github",
        )
    with pytest.raises(ValueError, match="aware"):
        LoopController(lambda proof: True, lambda: datetime(2026, 1, 1)).request_worker_admission(
            state,
            request_id="naive-clock",
            pr_number=42,
            obligation_id="problem",
            batch_id="batch",
            worker_id="worker",
            provider="github",
        )
    with pytest.raises(AdmissionBlockedError, match="lineage"):
        c.request_worker_admission(
            state,
            request_id="bad-lineage",
            pr_number=42,
            obligation_id="problem",
            batch_id="wrong",
            worker_id="worker",
            provider="github",
        )
    with pytest.raises(ValueError, match="future"):
        c.request_worker_admission(
            state,
            request_id="expired",
            pr_number=42,
            obligation_id="problem",
            batch_id="batch",
            worker_id="worker",
            provider="github",
            deadline_at=f.now,
        )
    state, request = c.request_worker_admission(
        state,
        request_id="request",
        pr_number=42,
        obligation_id="problem",
        batch_id="batch",
        worker_id="worker",
        provider="github",
    )
    replayed, same_request = c.request_worker_admission(
        state,
        request_id="request",
        pr_number=42,
        obligation_id="problem",
        batch_id="batch",
        worker_id="worker",
        provider="github",
    )
    assert replayed == state and same_request == request
    with pytest.raises(AdmissionBlockedError, match="replay differs"):
        c.request_worker_admission(
            state,
            request_id="request",
            pr_number=42,
            obligation_id="problem",
            batch_id="batch",
            worker_id="other-worker",
            provider="github",
        )
    state, decision = c.admit_worker(state, "request")
    assert decision.admitted
    state, decision = c.admit_worker(state, "request")
    assert decision.reason == "already admitted"
    with pytest.raises(AdmissionBlockedError, match="unknown admission"):
        c.admit_worker(state, "missing")
    with pytest.raises(AdmissionBlockedError, match="reserved"):
        c.mark_worker_dispatch_unknown(state, "missing")
    state = c.mark_worker_dispatch_unknown(state, "request")
    state = c.mark_worker_dispatch_unknown(state, "request")
    with pytest.raises(AdmissionBlockedError, match="nonacceptance"):
        c.release_worker_admission(
            state,
            "request",
            f.proof(
                kind="failure",
                subject="request",
                before="running",
                after="unresolved",
                related_id="permit:request",
            ),
        )
    with pytest.raises(AdmissionBlockedError, match="bound"):
        c.bind_accepted_worker(
            state,
            "request",
            remote_task_id="task",
            remote_session_id="session",
            model="gpt-6-astra",
        )
    with pytest.raises(AdmissionBlockedError, match="bound"):
        c.bind_accepted_worker(
            state,
            "request",
            remote_task_id="task",
            remote_session_id="session",
            model="gpt-6-astra",
        )
    state = c.bind_accepted_worker(
        state,
        "request",
        remote_task_id="task",
        remote_session_id="session",
        model="gpt-5.6-luna",
    )
    with pytest.raises(AdmissionBlockedError, match="terminal evidence"):
        c.release_worker_admission(
            state,
            "request",
            f.proof(
                kind="success",
                subject="request",
                before="running",
                after="satisfied",
                related_id="permit:request",
            ),
        )
    with pytest.raises(AdmissionBlockedError, match="not reserved"):
        c.mark_worker_dispatch_unknown(state, "request")
    proof = f.proof(
        kind="success",
        subject="request",
        before="terminal",
        after="satisfied",
        related_id="permit:request",
    )
    state = c.release_worker_admission(state, "request", proof)
    assert state.active_permits["permit:request"].status == PermitStatus.RELEASED
    assert state.permit_requests["request"].status == AdmissionRequestStatus.RELEASED
    state, _ = c.request_worker_admission(
        state,
        request_id="unknown-release",
        pr_number=42,
        obligation_id="problem",
        batch_id="batch",
        worker_id="unknown-release",
        provider="github",
    )
    state, _ = c.admit_worker(state, "unknown-release")
    state = c.mark_worker_dispatch_unknown(state, "unknown-release")
    state = c.release_worker_admission(
        state,
        "unknown-release",
        f.proof(
            kind="absence",
            subject="unknown-release",
            after="not_accepted",
            related_id="permit:unknown-release",
        ),
    )
    with pytest.raises(AdmissionBlockedError, match="never-issued"):
        c.cancel_worker_admission(state, "unknown-release")
    with pytest.raises(AdmissionBlockedError, match="unknown admission"):
        c.cancel_worker_admission(state, "missing")


def test_shared_admission_capacity_fairness_cancellation_and_unknown_release(foundation):
    f = foundation()
    c = controller(f)
    state = c.observe_provider_capacity(
        f.state,
        ProviderCapacityObservation("github", f.now, f.now + timedelta(minutes=5), 1, 0, 0, "capacity"),
    )
    state, _ = c.request_worker_admission(
        state,
        request_id="first",
        pr_number=42,
        obligation_id="problem",
        batch_id="batch",
        worker_id="first",
        provider="github",
    )
    state, _ = c.request_worker_admission(
        state,
        request_id="second",
        pr_number=42,
        obligation_id="problem",
        batch_id="batch",
        worker_id="second",
        provider="github",
    )
    state, decision = c.admit_worker(state, "second")
    assert not decision.admitted and decision.reason == "fairness wait"
    state, _ = c.admit_worker(state, "first")
    state, decision = c.admit_worker(state, "second")
    assert not decision.admitted and decision.reason == "provider capacity exhausted"
    state, _ = c.request_worker_admission(
        state,
        request_id="azure",
        pr_number=42,
        obligation_id="problem",
        batch_id="batch",
        worker_id="azure",
        provider="azure",
    )
    _, decision = c.admit_worker(state, "azure")
    assert not decision.admitted and decision.reason == "provider capacity unavailable"
    held_state = replace(
        state,
        pr_envelopes={42: replace(state.pr_envelopes[42], hold="held")},
    )
    _, decision = c.admit_worker(held_state, "second")
    assert not decision.admitted and decision.reason == "held"
    permit = state.active_permits["permit:first"]
    full_state = replace(
        state,
        active_permits={
            f"permit-{index}": replace(permit, permit_id=f"permit-{index}", request_id=f"request-{index}")
            for index in range(100)
        },
    )
    _, decision = c.admit_worker(full_state, "second")
    assert not decision.admitted and decision.reason == "global capacity exhausted"
    with pytest.raises(AdmissionBlockedError, match="reserved permit"):
        c.bind_accepted_worker(
            state,
            "missing",
            remote_task_id="task",
            remote_session_id="session",
            model="gpt-5.6-luna",
        )
    with pytest.raises(AdmissionBlockedError, match="unknown admission"):
        c.release_worker_admission(state, "missing", f.proof(subject="missing", related_id="permit:missing"))
    state = c.cancel_worker_admission(state, "first")
    state, decision = c.admit_worker(state, "second")
    assert decision.admitted
    with pytest.raises(AdmissionBlockedError, match="bound"):
        c.release_worker_admission(
            state,
            "second",
            f.proof(subject="second", related_id="forged"),
        )
    with pytest.raises(AdmissionBlockedError, match="occupied"):
        c.release_worker_admission(
            state,
            "second",
            f.proof(subject="second", related_id="permit:second"),
        )
    _, decision = c.admit_worker(state, "first")
    assert not decision.admitted and decision.reason == "request is terminal"
    projection = c._controller_projection(state, 42, request_id="first", permit_id="permit:first")
    assert projection.request_ids and projection.permit_ids


def test_admission_receipts_are_rejected_without_independent_verification(foundation):
    f = foundation()
    c = controller(f, verifier=lambda _proof: False)
    observation = ProviderCapacityObservation(
        "github",
        f.now,
        f.now + timedelta(minutes=5),
        1,
        0,
        0,
        "capacity",
    )
    with pytest.raises(AdmissionBlockedError, match="capacity verification"):
        c.observe_provider_capacity(f.state, observation)


def test_capacity_observation_reuses_bound_receipt(foundation):
    f = foundation()
    receipt = f.add(
        "observation",
        "github",
        pr_number=0,
        related_id="capacity:github:epoch:1",
    )
    observation = ProviderCapacityObservation(
        "github",
        f.now,
        f.now + timedelta(minutes=5),
        1,
        0,
        0,
        "capacity",
        receipt_evidence_id=receipt,
    )
    state = controller(f).observe_provider_capacity(f.state, observation)
    assert state.provider_capacity["github"].receipt_evidence_id == receipt
    assert state.evidence == f.state.evidence


@pytest.mark.parametrize(
    "changes",
    [
        {"kind": "history"},
        {"pr_number": 42},
        {"subject": "other-provider"},
        {"related_id": "capacity:github:epoch:2"},
        {"observed_at": datetime(2026, 9, 14, 11, tzinfo=UTC)},
        {"valid_until": datetime(2026, 9, 14, 12, 10, tzinfo=UTC)},
    ],
)
def test_capacity_observation_rejects_misbound_receipt(foundation, changes):
    f = foundation()
    values = dict(kind="observation", subject="github", pr_number=0, related_id="capacity:github:epoch:1")
    values.update(changes)
    receipt = f.add(**values)
    observation = ProviderCapacityObservation(
        "github",
        f.now,
        f.now + timedelta(minutes=5),
        1,
        0,
        0,
        "capacity",
        receipt_evidence_id=receipt,
    )
    with pytest.raises(AdmissionBlockedError, match="capacity receipt is not bound"):
        controller(f).observe_provider_capacity(f.state, observation)
    assert f.state.provider_capacity == {}


def test_expired_queued_request_is_terminal_and_does_not_block_next_request(foundation):
    f = foundation()
    c = controller(f)
    state = c.observe_provider_capacity(
        f.state,
        ProviderCapacityObservation("github", f.now, f.now + timedelta(minutes=5), 1, 0, 0, "capacity"),
    )
    state, _ = c.request_worker_admission(
        state,
        request_id="expired",
        pr_number=42,
        obligation_id="problem",
        batch_id="batch",
        worker_id="expired",
        provider="github",
        deadline_at=f.now + timedelta(seconds=1),
    )
    state, _ = c.request_worker_admission(
        state,
        request_id="next",
        pr_number=42,
        obligation_id="problem",
        batch_id="batch",
        worker_id="next",
        provider="github",
    )
    c._clock = lambda: f.now + timedelta(seconds=2)
    state, decision = c.admit_worker(state, "expired")
    assert not decision.admitted and decision.reason == "expired"
    assert c.cancel_worker_admission(state, "expired") == state
    state, decision = c.admit_worker(state, "next")
    assert decision.admitted and state.permit_requests["expired"].status == AdmissionRequestStatus.CANCELLED


def test_admission_rechecks_epoch_and_current_authority(foundation):
    f = foundation()
    c = controller(f)
    observation = ProviderCapacityObservation(
        "github",
        f.now,
        f.now + timedelta(minutes=5),
        1,
        0,
        0,
        "capacity",
    )
    with pytest.raises(AdmissionBlockedError, match="stale"):
        c.observe_provider_capacity(replace(f.state, global_epoch=2), observation)
    state = c.observe_provider_capacity(f.state, observation)
    state, _ = c.request_worker_admission(
        state,
        request_id="request",
        pr_number=42,
        obligation_id="problem",
        batch_id="batch",
        worker_id="worker",
        provider="github",
    )
    c._input_current = lambda *_args: False
    _, decision = c.admit_worker(state, "request")
    assert not decision.admitted and decision.reason == "stale authority"


def test_dispatch_unknown_is_fenced_by_hold(foundation):
    f = foundation()
    c = controller(f)
    state = c.observe_provider_capacity(
        f.state,
        ProviderCapacityObservation("github", f.now, f.now + timedelta(minutes=5), 1, 0, 0, "capacity"),
    )
    state, _ = c.request_worker_admission(
        state,
        request_id="request",
        pr_number=42,
        obligation_id="problem",
        batch_id="batch",
        worker_id="worker",
        provider="github",
    )
    state, _ = c.admit_worker(state, "request")
    held = replace(state, pr_envelopes={42: replace(state.pr_envelopes[42], hold="held")})
    with pytest.raises(AdmissionBlockedError, match="current PR authority"):
        c.mark_worker_dispatch_unknown(held, "request")


def test_queued_cancellation_is_idempotent_and_terminal_requests_are_blocked(foundation):
    f = foundation()
    c = controller(f)
    state, _ = c.request_worker_admission(
        f.state,
        request_id="queued",
        pr_number=42,
        obligation_id="problem",
        batch_id="batch",
        worker_id="worker",
        provider="github",
    )
    state = c.cancel_worker_admission(state, "queued")
    assert c.cancel_worker_admission(state, "queued") == state
    with pytest.raises(AdmissionBlockedError, match="terminal"):
        c.cancel_worker_admission(
            replace(
                state,
                permit_requests={
                    "queued": replace(state.permit_requests["queued"], status=AdmissionRequestStatus.RELEASED)
                },
            ),
            "queued",
        )


def controller(f, verifier=lambda proof: True):
    return LoopController(verifier, lambda: f.now)


def test_epoch_advancement_fences_prior_admission(foundation):
    f = foundation()
    c = controller(f)
    state, _ = c.request_worker_admission(
        f.state,
        request_id="request",
        pr_number=42,
        obligation_id="problem",
        batch_id="batch",
        worker_id="worker",
        provider="github",
    )
    updated = c.advance_epoch(state)
    assert updated.global_epoch == f.state.global_epoch + 1
    assert updated.pr_envelopes[42].control_epoch == f.state.pr_envelopes[42].control_epoch
    with pytest.raises(AdmissionBlockedError, match="stale"):
        c.admit_worker(updated, "request")
    updated.permit_requests["request"] = replace(updated.permit_requests["request"], permit_id="permit")
    with pytest.raises(AdmissionBlockedError, match="stale"):
        c.mark_worker_dispatch_unknown(updated, "request")


def test_effect_intent_settlement_is_idempotent_and_bound(foundation):
    f = foundation()
    c = controller(f)
    state = c.intent_effect(f.state, "effect-1", 42, "comment", "digest")
    with pytest.raises(ValueError, match="identity"):
        c.intent_effect(state, "", 42, "comment", "digest")
    with pytest.raises(AdmissionBlockedError, match="unknown"):
        c.settle_effect(state, "missing", f.proof("effect", "effect", related_id="missing"))
    with pytest.raises(AdmissionBlockedError, match="bound"):
        c.settle_effect(state, "effect-1", f.proof("effect", "effect", related_id="other"))
    assert c.intent_effect(state, "effect-1", 42, "comment", "digest") is state
    with pytest.raises(AdmissionBlockedError, match="payload"):
        c.intent_effect(state, "effect-1", 42, "comment", "other")
    proof = f.proof("effect", "effect", before="pending", after="settled", related_id="effect-1")
    settled = c.settle_effect(state, "effect-1", proof)
    assert settled.effects["effect-1"].status.value == "settled"
    assert c.settle_effect(settled, "effect-1", proof) == settled
    with pytest.raises(AdmissionBlockedError, match="immutable"):
        c.settle_effect(settled, "effect-1", f.proof("effect", "effect", after="failed", related_id="effect-1"))


def test_eligibility_predicates_report_failed_requirements(foundation):
    f = foundation()
    c = controller(f)
    observation = f.proof()
    approval = c.approval_eligible(f.state, 42, observation)
    assert not approval.eligible
    assert approval.reason == "actionable_findings_addressed"
    merge = c.merge_eligible(f.state, 42, observation)
    assert not merge.eligible
    assert merge.reason == "actionable_findings_addressed"


@pytest.mark.parametrize("clock", [None, datetime(2026, 1, 1), "not-a-clock"])
def test_fresh_rejects_invalid_clock(foundation, clock):
    f = foundation()
    with pytest.raises(ValueError, match="aware datetime"):
        LoopController(lambda p: True, lambda: clock)._fresh(f.proof())


@pytest.mark.parametrize("offset", [-1, 300])
def test_fresh_rejects_future_and_expired(foundation, offset):
    f = foundation()
    f.now += timedelta(seconds=offset)
    with pytest.raises(AdmissionBlockedError, match="stale or from"):
        controller(f)._fresh(f.proof())


@pytest.mark.parametrize("proof", [None, "worker says success"])
def test_scoped_rejects_untyped_evidence(foundation, proof):
    f = foundation()
    with pytest.raises(AdmissionBlockedError, match="typed"):
        controller(f)._scoped(f.state, proof, "finding", 42)


@pytest.mark.parametrize("field,value", [("head_sha", "d" * 40), ("base_sha", "e" * 40), ("policy_version", "new")])
def test_scoped_rejects_changed_scope(foundation, field, value):
    f = foundation()
    with pytest.raises(AdmissionBlockedError, match="stale head"):
        controller(f)._scoped(f.state, f.proof(**{field: value}), "observation", 42)


@pytest.mark.parametrize("kind,pr", [("failure", 42), ("observation", 43)])
def test_verify_rejects_wrong_binding(foundation, kind, pr):
    f = foundation()
    with pytest.raises(AdmissionBlockedError, match="wrong evidence"):
        controller(f)._verify(f.state, f.proof(), kind, pr)


@pytest.mark.parametrize("verdict", [False, None, 1])
def test_verify_requires_literal_independent_approval(foundation, verdict):
    f = foundation()
    with pytest.raises(AdmissionBlockedError, match="independent"):
        controller(f, lambda p: verdict)._verify(f.state, f.proof(), "observation", 42)


def test_verify_rejects_content_collision_without_mutation(foundation):
    f = foundation()
    proof = f.proof()
    f.state.evidence[proof.evidence_id] = replace(proof, source_revision="tampered")
    with pytest.raises(AdmissionBlockedError, match="immutable"):
        controller(f)._verify(f.state, proof, "observation", 42)
    assert f.state.evidence[proof.evidence_id].source_revision == "tampered"


def test_gate_rejects_quarantine_and_unknown_pr(foundation):
    f = foundation()
    with pytest.raises(AdmissionBlockedError, match="historical budget"):
        controller(f)._gate(f.state, 43)
    f.state.quarantines = [QuarantineRecord("q", f.state.repo, "blocked", "digest", "proof", f.now)]
    with pytest.raises(AdmissionBlockedError, match="quarantined"):
        controller(f)._gate(f.state)


@pytest.mark.parametrize("hold", ["held", "ignored"])
def test_gate_honors_current_hold(foundation, hold):
    f = foundation()
    observation = f.add(before=hold)
    f.state.pr_envelopes[42] = replace(f.state.pr_envelopes[42], hold=hold, observation_id=observation)
    with pytest.raises(AdmissionBlockedError, match="held or ignored"):
        controller(f)._gate(f.state, 42)


@pytest.mark.parametrize("invalid", [None, "", " "])
def test_register_obligation_rejects_empty_identity(foundation, invalid):
    f = foundation()
    with pytest.raises(ValueError, match="canonical"):
        controller(f).register_obligation(f.state, invalid, 42)


def test_register_obligation_is_copy_on_write_and_idempotent(foundation):
    f = foundation()
    c = controller(f)
    updated, identity = c.register_obligation(f.state, "independent", 42)
    assert set(updated.obligations) == {"problem", identity}
    assert identity not in f.state.obligations
    assert c.register_obligation(updated, "independent", 42) == (updated, identity)


def test_register_finding_retains_lineage_and_rejects_disposition_change(foundation):
    f = foundation()
    c = controller(f)
    proof = f.proof("finding", "second-comment", related_id="problem")
    updated = c.register_finding(f.state, "problem", proof, "implement_better_fix")
    assert len(updated.findings) == 2
    assert len(f.state.findings) == 1
    assert c.register_finding(updated, "problem", proof, "implement_better_fix") is updated
    with pytest.raises(AdmissionBlockedError, match="lineage"):
        c.register_finding(updated, "problem", proof, "reject_with_evidence")


@pytest.mark.parametrize(
    "change",
    [
        {"after": "complete"},
        {"subject": "43"},
        {"inventory": ("unknown",)},
    ],
)
def test_enroll_requires_empty_history(foundation, change):
    f = foundation()
    f.state.pr_envelopes = {}
    f.state.obligations = {}
    f.state.findings = {}
    f.state.attempts = {}
    f.state.rounds = {}
    with pytest.raises(AdmissionBlockedError, match="empty lifetime"):
        controller(f).enroll_pr(f.state, f.proof(), f.proof("history", **{"after": "empty", "inventory": (), **change}))


def test_enroll_new_pr_and_reject_bad_inputs(foundation):
    f = foundation()
    c = controller(f)
    observation = f.proof(subject="43", pr_number=43)
    history = f.proof("history", "43", pr_number=43, after="empty", inventory=())
    updated = c.enroll_pr(f.state, observation, history)
    assert updated.pr_envelopes[43].round_ids == ()
    assert 43 not in f.state.pr_envelopes
    with pytest.raises(AdmissionBlockedError, match="already enrolled"):
        c.enroll_pr(updated, observation, history)
    with pytest.raises(AdmissionBlockedError, match="typed observation"):
        c.enroll_pr(f.state, None, history)
    with pytest.raises(AdmissionBlockedError, match="hold state"):
        c.enroll_pr(f.state, f.proof(subject="not-43", pr_number=43), history)


@pytest.mark.parametrize("change", [{"subject": "43"}, {"before": "unknown"}, {"pr_number": 43}])
def test_observe_rejects_wrong_pr_or_hold(foundation, change):
    f = foundation()
    with pytest.raises(AdmissionBlockedError, match="invalid PR"):
        controller(f).observe_pr(f.state, f.proof(**change))


def test_observe_rejects_untyped_and_reordered_input(foundation):
    f = foundation()
    with pytest.raises(AdmissionBlockedError, match="typed"):
        controller(f).observe_pr(f.state, None)
    with pytest.raises(AdmissionBlockedError, match="reordered"):
        controller(f).observe_pr(f.state, f.proof(observed_at=f.now - timedelta(seconds=1)))


@pytest.mark.parametrize("phase", ["prepublication", "published", "reviewed"])
def test_observe_changed_head_keeps_history_and_invalidates_only_unreviewed(foundation, phase):
    f = foundation((AttemptStatus.FAILED,), phase)
    updated = controller(f).observe_pr(f.state, f.proof(head_sha="d" * 40))
    assert updated.pr_envelopes[42].head_sha == "d" * 40
    assert updated.rounds["batch"].phase == ("reviewed" if phase == "reviewed" else "invalidated")
    assert updated.attempts == f.state.attempts
    assert f.state.pr_envelopes[42].head_sha == "a" * 40


def test_observe_expected_publication_does_not_invalidate(foundation):
    f = foundation((AttemptStatus.FAILED,), "published")
    batch = f.state.rounds["batch"]
    publication = f.state.evidence[batch.publication_id]
    identity = f.add("publication", "batch", related_id=batch.observation_id, after="d" * 40)
    f.state.rounds["batch"] = replace(batch, publication_id=identity)
    updated = controller(f).observe_pr(f.state, f.proof(head_sha="d" * 40))
    assert updated.rounds["batch"].phase == "published"
    assert publication.evidence_id in updated.evidence


@pytest.mark.parametrize("kind", ["progress_gate", "progress_finding"])
def test_progress_persists_once_and_rejects_logical_remint(foundation, kind):
    f = foundation((AttemptStatus.FAILED,), "reviewed")
    subject = "finding" if kind == "progress_finding" else "required-check"
    proof = f.proof(kind, subject, before="failing", after="satisfied", related_id="batch")
    c = controller(f)
    updated = c.record_progress(f.state, proof)
    assert proof.evidence_id in updated.evidence
    assert c.record_progress(updated, proof).evidence == updated.evidence
    with pytest.raises(AdmissionBlockedError, match="reminted"):
        c.record_progress(
            updated,
            f.proof(
                kind, subject, before="failing", after="satisfied", related_id="batch", source_revision="duplicate"
            ),
        )


@pytest.mark.parametrize(
    "change,message",
    [
        ({"before": "passing"}, "failing-to-satisfied"),
        ({"related_id": "missing"}, "review boundary"),
        ({"kind": "progress_finding", "subject": "missing"}, "finding is unknown"),
    ],
)
def test_progress_rejects_unsubstantiated_claim(foundation, change, message):
    f = foundation((AttemptStatus.FAILED,), "reviewed")
    values = dict(kind="progress_gate", subject="check", before="failing", after="satisfied", related_id="batch")
    values.update(change)
    with pytest.raises(AdmissionBlockedError, match=message):
        controller(f).record_progress(f.state, f.proof(**values))


def test_begin_round_bootstrap_and_replay(foundation):
    f = foundation(())
    f.state.rounds = {}
    f.state.pr_envelopes[42] = replace(f.state.pr_envelopes[42], rounds_used=0, round_ids=(), active_batch_id=None)
    c = controller(f)
    updated, batch = c.begin_round(f.state, "problem", "first")
    assert batch.round_number == 1
    assert c.begin_round(updated, "problem", "first") == (updated, batch)
    with pytest.raises(AdmissionBlockedError, match="replay differs"):
        c.begin_round(updated, "problem", "first", "another")
    with pytest.raises(AdmissionBlockedError, match="bootstrap cannot"):
        c.begin_round(f.state, "problem", "first", "unexpected")
    assert f.state.rounds == {}


@pytest.mark.parametrize("identity", ["", " ", None])
def test_begin_round_requires_stable_identity(foundation, identity):
    f = foundation()
    with pytest.raises(ValueError, match="stable batch"):
        controller(f).begin_round(f.state, "problem", identity)


def test_begin_round_needs_review_boundary_and_authority(foundation):
    f = foundation()
    with pytest.raises(AdmissionBlockedError, match="review boundary"):
        controller(f).begin_round(f.state, "problem", "new")
    f = foundation((AttemptStatus.FAILED,), "reviewed")
    with pytest.raises(AdmissionBlockedError, match="requires progress"):
        controller(f).begin_round(f.state, "problem", "new")
    failure = f.state.attempts["attempt-0"].outcome_id
    updated, batch = controller(f).begin_round(f.state, "problem", "new", failure)
    assert batch.reason == "recovery"
    assert updated.pr_envelopes[42].rounds_used == 2
    assert f.state.pr_envelopes[42].rounds_used == 1


@pytest.mark.parametrize("status", ["isolated", "verified"])
def test_begin_round_rejects_nonactionable_problem(foundation, status):
    f = foundation((AttemptStatus.FAILED,), "reviewed")
    f.state.obligations["problem"] = replace(f.state.obligations["problem"], status=status)
    with pytest.raises(AdmissionBlockedError, match="no actionable"):
        controller(f).begin_round(f.state, "problem", "new")


def test_begin_round_requires_current_finding_inventory(foundation):
    f = foundation((AttemptStatus.FAILED,), "reviewed")
    observation = f.add(inventory=("unrelated",))
    f.state.pr_envelopes[42] = replace(f.state.pr_envelopes[42], observation_id=observation)
    with pytest.raises(AdmissionBlockedError, match="no actionable findings"):
        controller(f).begin_round(f.state, "problem", "new")


def test_begin_progress_round_consumes_verified_progress(foundation):
    f = foundation((AttemptStatus.FAILED,), "reviewed")
    proof = f.add("progress_gate", "check", before="failing", after="satisfied", related_id="batch")
    updated, batch = controller(f).begin_round(f.state, "problem", "new", proof)
    assert batch.reason == "progress"
    assert updated.pr_envelopes[42].round_ids == ("batch", "new")
    updated.rounds["new"] = replace(batch, phase="invalidated")
    with pytest.raises(AdmissionBlockedError, match="already consumed"):
        controller(f).begin_round(updated, "problem", "third", proof)


@pytest.mark.parametrize("count", [0, 1, 2, 3, 4])
def test_next_kind_enforces_order_and_budget(foundation, count):
    f = foundation((AttemptStatus.FAILED,) * count)
    c = controller(f)
    obligation = f.state.obligations["problem"]
    authorization = None if count == 0 else f.state.attempts[f"attempt-{count - 1}"].outcome_id
    if count == 3:
        remediation = f.add("remediation", "problem", before="broken", after="fixed")
        obligation = replace(obligation, remediation_id=remediation)
        authorization = f.add("verification", "problem", related_id=remediation, after="repair_required")
    if count == 4:
        with pytest.raises(AdmissionBlockedError, match="budget exhausted"):
            c._next_kind(f.state, obligation, authorization)
    else:
        assert c._next_kind(f.state, obligation, authorization) == tuple(AttemptKind)[count]


@pytest.mark.parametrize(
    "statuses,auth,message",
    [
        ((), "unexpected", "initial Luna"),
        ((AttemptStatus.AUTHORIZED,), None, "not independently failed"),
        ((AttemptStatus.FAILED,), None, "preceding verified failure"),
        ((AttemptStatus.FAILED,) * 3, None, "verify distinct remediation"),
    ],
)
def test_next_kind_cannot_mint_recovery(foundation, statuses, auth, message):
    f = foundation(statuses)
    with pytest.raises(AdmissionBlockedError, match=message):
        controller(f)._next_kind(f.state, f.state.obligations["problem"], auth)


def test_revalidate_failure_keeps_accepted_history(foundation):
    f = foundation((AttemptStatus.FAILED,))
    attempt = f.state.attempts["attempt-0"]
    proof = f.proof(
        "failure",
        attempt.attempt_id,
        before="terminal",
        after="unresolved",
        related_id=attempt.acceptance_id,
        source_revision="new-read",
    )
    updated = controller(f).revalidate_failure(f.state, attempt.attempt_id, proof)
    assert updated.attempts == f.state.attempts
    assert updated.evidence[proof.evidence_id] == proof
    with pytest.raises(AdmissionBlockedError, match="bind failed"):
        controller(f).revalidate_failure(f.state, attempt.attempt_id, f.proof("failure", "wrong"))


def test_authorize_attempt_does_not_account_acceptance_and_replays(foundation):
    f = foundation(())
    c = controller(f)
    updated, attempt = c.authorize_attempt(f.state, "problem", "batch", "initial")
    assert attempt.status == AttemptStatus.AUTHORIZED
    assert attempt.acceptance_id is None
    assert updated.obligations["problem"].attempt_ids == ("initial",)
    assert c.authorize_attempt(updated, "problem", "batch", "initial") == (updated, attempt)
    with pytest.raises(AdmissionBlockedError, match="replay differs"):
        c.authorize_attempt(updated, "problem", "wrong", "initial")


@pytest.mark.parametrize("batch", ["missing", "batch"])
def test_authorize_requires_current_prepublication_batch(foundation, batch):
    f = foundation((AttemptStatus.FAILED,), "reviewed")
    with pytest.raises(AdmissionBlockedError, match="prepublication"):
        controller(f).authorize_attempt(f.state, "problem", batch, "new")


def test_authorize_retry_preserves_previous_acceptance(foundation):
    f = foundation((AttemptStatus.FAILED,))
    previous = f.state.attempts["attempt-0"]
    updated, attempt = controller(f).authorize_attempt(f.state, "problem", "batch", "retry", previous.outcome_id)
    assert attempt.kind == AttemptKind.RETRY_LUNA
    assert updated.attempts["attempt-0"] == previous
    with pytest.raises(ValueError, match="stable attempt"):
        controller(f).authorize_attempt(f.state, "problem", "batch", "", previous.outcome_id)


@pytest.mark.parametrize(
    "status", [AttemptStatus.UNKNOWN, AttemptStatus.ACCEPTED, AttemptStatus.FAILED, AttemptStatus.SUCCEEDED]
)
@pytest.mark.parametrize("method", ["renew_authorized_attempt", "replan_authorized_attempt"])
def test_refresh_rejects_unknown_and_accepted_work(foundation, status, method):
    f = foundation((status,))
    args = ("attempt-0", "new") if method.startswith("replan") else ("attempt-0",)
    with pytest.raises(AdmissionBlockedError, match="authorized, unaccepted"):
        getattr(controller(f), method)(f.state, *args)


def test_renew_preserves_admitted_and_accepted_inputs(foundation):
    f = foundation((AttemptStatus.FAILED, AttemptStatus.AUTHORIZED))
    f.now += timedelta(minutes=6)
    observation = f.add(observed_at=f.now, valid_until=f.now + timedelta(minutes=5))
    f.state.pr_envelopes[42] = replace(f.state.pr_envelopes[42], observation_id=observation)
    updated = controller(f).renew_authorized_attempt(f.state, "attempt-1")
    assert updated.attempts["attempt-0"] == f.state.attempts["attempt-0"]
    assert updated.rounds == f.state.rounds
    assert updated.attempts["attempt-1"].observation_id == observation
    assert updated.obligations == f.state.obligations
    assert controller(f).renew_authorized_attempt(updated, "attempt-1") == updated


def test_renew_requires_active_unchanged_input(foundation):
    f = foundation(phase="invalidated")
    with pytest.raises(AdmissionBlockedError, match="active prepublication"):
        controller(f).renew_authorized_attempt(f.state, "attempt-0")
    f = foundation()
    observation = f.add(head_sha="d" * 40)
    f.state.pr_envelopes[42] = replace(f.state.pr_envelopes[42], observation_id=observation, head_sha="d" * 40)
    with pytest.raises(AdmissionBlockedError, match="explicit replan"):
        controller(f).renew_authorized_attempt(f.state, "attempt-0")


def test_replan_retains_history_and_has_idempotent_replay(foundation):
    f = foundation((AttemptStatus.FAILED, AttemptStatus.AUTHORIZED), "invalidated")
    observation = f.add(head_sha="d" * 40)
    f.state.pr_envelopes[42] = replace(f.state.pr_envelopes[42], observation_id=observation, head_sha="d" * 40)
    c = controller(f)
    updated = c.replan_authorized_attempt(f.state, "attempt-1", "new")
    assert updated.attempts["attempt-0"] == f.state.attempts["attempt-0"]
    assert updated.rounds["batch"] == f.state.rounds["batch"]
    assert updated.rounds["new"].authorization_id == "batch"
    assert updated.pr_envelopes[42].round_ids == ("batch", "new")
    assert c.replan_authorized_attempt(updated, "attempt-1", "new") is updated


@pytest.mark.parametrize("batch", ["batch", "", " ", None])
def test_replan_rejects_used_or_empty_batch_identity(foundation, batch):
    f = foundation(phase="invalidated")
    observation = f.add(head_sha="d" * 40)
    f.state.pr_envelopes[42] = replace(f.state.pr_envelopes[42], observation_id=observation, head_sha="d" * 40)
    with pytest.raises(AdmissionBlockedError, match="already used"):
        controller(f).replan_authorized_attempt(f.state, "attempt-0", batch)


def test_replan_requires_invalidated_and_changed_input(foundation):
    f = foundation()
    with pytest.raises(AdmissionBlockedError, match="invalidated active"):
        controller(f).replan_authorized_attempt(f.state, "attempt-0", "new")
    f.state.rounds["batch"] = replace(f.state.rounds["batch"], phase="invalidated")
    with pytest.raises(AdmissionBlockedError, match="use renewal"):
        controller(f).replan_authorized_attempt(f.state, "attempt-0", "new")


@pytest.mark.parametrize("status", [AttemptStatus.AUTHORIZED, AttemptStatus.UNKNOWN, AttemptStatus.ACCEPTED])
def test_dispatch_status_is_persistable_and_idempotent(foundation, status):
    f = foundation((status,))
    c = controller(f)
    if status == AttemptStatus.ACCEPTED:
        with pytest.raises(AdmissionBlockedError, match="not authorized"):
            c.mark_dispatch_unknown(f.state, "attempt-0")
    else:
        updated = c.mark_dispatch_unknown(f.state, "attempt-0")
        assert updated.attempts["attempt-0"].status == AttemptStatus.UNKNOWN
        assert updated.obligations == f.state.obligations


def test_dispatch_rejects_stale_input(foundation):
    f = foundation()
    observation = f.add(head_sha="d" * 40)
    f.state.pr_envelopes[42] = replace(f.state.pr_envelopes[42], observation_id=observation, head_sha="d" * 40)
    with pytest.raises(AdmissionBlockedError, match="stale attempt"):
        controller(f).mark_dispatch_unknown(f.state, "attempt-0")


def test_nonacceptance_reopens_only_same_slot(foundation):
    f = foundation((AttemptStatus.UNKNOWN,))
    attempt = f.state.attempts["attempt-0"]
    proof = f.proof("absence", attempt.attempt_id, related_id=attempt.observation_id, after="not_accepted")
    updated = controller(f).record_nonacceptance(f.state, attempt.attempt_id, proof)
    assert updated.attempts[attempt.attempt_id].status == AttemptStatus.AUTHORIZED
    assert updated.obligations == f.state.obligations
    with pytest.raises(AdmissionBlockedError, match="absence evidence"):
        controller(f).record_nonacceptance(f.state, attempt.attempt_id, f.proof("absence", "wrong"))


def test_acceptance_binds_model_and_is_idempotent(foundation):
    f = foundation((AttemptStatus.UNKNOWN,))
    attempt = f.state.attempts["attempt-0"]
    proof = f.proof(
        "acceptance",
        attempt.attempt_id,
        related_id=attempt.observation_id,
        before="provider:task",
        after="gpt-5.6-luna",
    )
    c = controller(f)
    updated = c.record_acceptance(f.state, attempt.attempt_id, proof)
    assert updated.attempts[attempt.attempt_id].acceptance_id == proof.evidence_id
    assert c.record_acceptance(updated, attempt.attempt_id, proof) is updated
    with pytest.raises(AdmissionBlockedError, match="immutable"):
        c.record_acceptance(updated, attempt.attempt_id, f.proof("acceptance", attempt.attempt_id, before="other"))
    with pytest.raises(AdmissionBlockedError, match="persisted dispatch"):
        c.record_acceptance(foundation().state, attempt.attempt_id, proof)


@pytest.mark.parametrize("kind", ["failure", "success"])
@pytest.mark.parametrize("count", [1, 3, 4])
def test_outcome_records_terminal_and_isolation_without_budget_reset(foundation, kind, count):
    f = foundation((AttemptStatus.FAILED,) * (count - 1) + (AttemptStatus.ACCEPTED,))
    attempt = f.state.attempts[f"attempt-{count - 1}"]
    proof = f.proof(
        kind,
        attempt.attempt_id,
        related_id=attempt.acceptance_id,
        before="terminal",
        after="unresolved" if kind == "failure" else "satisfied",
    )
    c = controller(f)
    updated = c.record_outcome(f.state, attempt.attempt_id, proof)
    assert updated.attempts[attempt.attempt_id].outcome_id == proof.evidence_id
    assert updated.obligations["problem"].status == ("isolated" if kind == "failure" and count >= 3 else "in_progress")
    assert c.record_outcome(updated, attempt.attempt_id, proof) is updated
    with pytest.raises(AdmissionBlockedError, match="immutable"):
        c.record_outcome(updated, attempt.attempt_id, f.proof(kind, attempt.attempt_id, source_revision="other"))


def test_outcome_rejects_polling_and_unaccepted_work(foundation):
    f = foundation()
    c = controller(f)
    with pytest.raises(AdmissionBlockedError, match="terminal evidence"):
        c.record_outcome(f.state, "attempt-0", f.proof())
    with pytest.raises(AdmissionBlockedError, match="only accepted"):
        c.record_outcome(f.state, "attempt-0", f.proof("failure", "attempt-0"))


def test_publication_and_review_receipts_are_immutable(foundation):
    f = foundation((AttemptStatus.FAILED,))
    c = controller(f)
    proof = f.proof("publication", "batch", related_id=f.state.rounds["batch"].observation_id, after="a" * 40)
    updated = c.record_publication(f.state, "batch", proof)
    assert updated.rounds["batch"].phase == "published"
    assert c.record_publication(updated, "batch", proof) is updated
    with pytest.raises(AdmissionBlockedError, match="immutable"):
        c.record_publication(updated, "batch", f.proof("publication", "batch", source_revision="other"))
    review = f.proof("review", "batch", related_id=proof.evidence_id)
    reviewed = c.record_batch_review(updated, "batch", review)
    assert reviewed.rounds["batch"].phase == "reviewed"
    assert c.record_batch_review(reviewed, "batch", review) is reviewed
    with pytest.raises(AdmissionBlockedError, match="immutable"):
        c.record_batch_review(reviewed, "batch", f.proof("review", "batch", source_revision="other"))
    with pytest.raises(AdmissionBlockedError, match="unpublished"):
        c.record_batch_review(f.state, "batch", review)


@pytest.mark.parametrize(
    "statuses", [(), (AttemptStatus.AUTHORIZED,), (AttemptStatus.UNKNOWN,), (AttemptStatus.ACCEPTED,)]
)
def test_publication_requires_all_terminal_work(foundation, statuses):
    f = foundation(statuses)
    with pytest.raises(AdmissionBlockedError, match="terminal accepted"):
        controller(f).record_publication(f.state, "batch", f.proof("publication", "batch"))


def test_remediation_grant_is_one_use_and_requires_isolation(foundation):
    f = foundation((AttemptStatus.FAILED,) * 3)
    proof = f.proof("remediation", "problem", before="broken", after="fixed")
    c = controller(f)
    with pytest.raises(AdmissionBlockedError, match="isolated"):
        c.record_remediation(f.state, "problem", proof)
    f.state.obligations["problem"] = replace(f.state.obligations["problem"], status="isolated")
    updated = c.record_remediation(f.state, "problem", proof)
    assert updated.obligations["problem"].remediation_id == proof.evidence_id
    assert c.record_remediation(updated, "problem", proof) is updated
    with pytest.raises(AdmissionBlockedError, match="only one"):
        c.record_remediation(updated, "problem", f.proof("remediation", "problem", source_revision="other"))


@pytest.mark.parametrize("after,status", [("satisfied", "verified"), ("repair_required", "pending")])
def test_remediation_verification_cannot_be_reminted(foundation, after, status):
    f = foundation((AttemptStatus.FAILED,) * 3)
    remediation = f.add("remediation", "problem", before="broken", after="fixed")
    f.state.obligations["problem"] = replace(f.state.obligations["problem"], remediation_id=remediation)
    proof = f.proof("verification", "problem", related_id=remediation, after=after)
    c = controller(f)
    updated = c.verify_remediation(f.state, "problem", proof)
    assert updated.obligations["problem"].status == status
    assert c.verify_remediation(updated, "problem", proof) is updated
    with pytest.raises(AdmissionBlockedError, match="reminted"):
        c.verify_remediation(
            updated,
            "problem",
            f.proof("verification", "problem", related_id=remediation, after=after, source_revision="other"),
        )
    with pytest.raises(AdmissionBlockedError, match="bind the distinct"):
        c.verify_remediation(f.state, "problem", f.proof("verification", "unknown"))


def test_migration_preparation_is_source_bound_and_activation_separate(foundation):
    f = foundation(())
    source = QueueState("owner/repo", 0, {}, [], [])
    history = QueueState("owner/repo", 0, {}, [], [])
    proof = f.proof(
        "migration",
        "inventory",
        pr_number=0,
        inventory=(),
        before=_legacy_digest(source),
        after=_history_digest(history),
        source_revision="0",
    )
    c = controller(f)
    prepared = c.prepare_legacy_migration(source, history, proof)
    assert prepared.migration_status == "prepared"
    assert source.migration is None
    with pytest.raises(AdmissionBlockedError, match="source or historical"):
        c.activate_migration(prepared, proof.evidence_id)
    persisted = replace(prepared, revision=1)
    active = c.activate_migration(persisted, proof.evidence_id)
    assert active.migration_status == "active"
    validate_queue_state(active)
    with pytest.raises(AdmissionBlockedError, match="not been prepared"):
        c.activate_migration(source, proof.evidence_id)
    with pytest.raises(AdmissionBlockedError, match="no longer valid"):
        controller(f, lambda p: False).activate_migration(persisted, proof.evidence_id)


def test_migration_rejects_foreign_or_nonterminal_history(foundation):
    f = foundation()
    source = QueueState("owner/repo", 0, {}, [], [])
    c = controller(f)
    with pytest.raises(AdmissionBlockedError, match="matching preactivation"):
        c.prepare_legacy_migration(source, replace(f.state, repo="other/repo"), f.proof())
    with pytest.raises(AdmissionBlockedError, match="independently terminal"):
        c.prepare_legacy_migration(source, f.state, f.proof())
    f = foundation((AttemptStatus.FAILED,))
    with pytest.raises(AdmissionBlockedError, match="boundary is incomplete"):
        c.prepare_legacy_migration(source, f.state, f.proof())
    f = foundation((AttemptStatus.FAILED,), "reviewed")
    with pytest.raises(AdmissionBlockedError, match="complete inventory"):
        c.prepare_legacy_migration(source, f.state, f.proof())
    proof = f.proof(
        "migration",
        "inventory",
        pr_number=0,
        inventory=("42",),
        before=_legacy_digest(source),
        after=_history_digest(f.state),
        source_revision="0",
    )
    with pytest.raises(AdmissionBlockedError, match="provenance"):
        controller(f, lambda p: False).prepare_legacy_migration(source, f.state, proof)
    prepared = controller(f).prepare_legacy_migration(source, f.state, proof)
    assert prepared.attempts == f.state.attempts


@pytest.mark.parametrize(
    "status,message",
    [
        (WorkItemStatus.UNKNOWN, "may still be running"),
        (WorkItemStatus.QUEUED, "omitted a legacy PR"),
    ],
)
def test_migration_requires_complete_legacy_inventory(foundation, status, message):
    f = foundation(())
    source = QueueState(
        "owner/repo",
        0,
        {
            43: WorkItem(43, "owner/repo", "change", "eligible", None, status),
        },
        [],
        [],
    )
    with pytest.raises(AdmissionBlockedError, match=message):
        controller(f).prepare_legacy_migration(source, f.state, f.proof())


def test_observe_without_active_batch_and_unchanged_observation(foundation):
    f = foundation()
    c = controller(f)
    assert c.observe_pr(f.state, f.proof()).rounds == f.state.rounds
    f.state.pr_envelopes[42] = replace(f.state.pr_envelopes[42], active_batch_id=None)
    updated = c.observe_pr(f.state, f.proof(head_sha="d" * 40))
    assert updated.rounds == f.state.rounds
    assert updated.pr_envelopes[42].stage == "planning"


def test_fifty_round_ceiling_blocks_round_retry_and_replan(foundation):
    f = foundation((AttemptStatus.FAILED,), round_count=50)
    c = controller(f)
    with pytest.raises(AdmissionBlockedError, match="50-round"):
        c.begin_round(f.state, "problem", "round-51")
    f.state.attempts["attempt-0"] = replace(f.state.attempts["attempt-0"], batch_id="batch-50")
    with pytest.raises(AdmissionBlockedError, match="already-authorized"):
        c.authorize_attempt(f.state, "problem", "batch-50", "retry", f.state.attempts["attempt-0"].outcome_id)
    f = foundation(round_count=50)
    f.state.attempts["attempt-0"] = replace(f.state.attempts["attempt-0"], batch_id="batch-50")
    f.state.rounds["batch-50"] = replace(f.state.rounds["batch-50"], phase="invalidated")
    observation = f.add(head_sha="d" * 40)
    f.state.pr_envelopes[42] = replace(f.state.pr_envelopes[42], head_sha="d" * 40, observation_id=observation)
    with pytest.raises(AdmissionBlockedError, match="50-round"):
        controller(f).replan_authorized_attempt(f.state, "attempt-0", "round-51")
