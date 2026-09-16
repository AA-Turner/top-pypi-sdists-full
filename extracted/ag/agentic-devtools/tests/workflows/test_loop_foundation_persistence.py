"""Offline contract tests across the controller, codec and QueueStore CAS."""

from dataclasses import asdict, replace
from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.reconciliation.loop_control import AdmissionBlockedError, LoopController
from agentic_devtools.cli.ci.reconciliation.models import (
    AttemptKind,
    AttemptStatus,
    Evidence,
    ProviderCapacityObservation,
    QueueState,
    WorkItem,
    WorkItemStatus,
    _history_digest,
    _legacy_digest,
    queue_state_from_dict,
)
from agentic_devtools.cli.ci.reconciliation.queue_store import (
    ConcurrentModificationError,
    InMemoryBackingStore,
    QueueStore,
    _decode_queue_document,
    _state_to_dict,
)
from agentic_devtools.state import serialize_queue_document

NOW = datetime(2026, 9, 14, 12, tzinfo=UTC)
REPO = "owner/repo"
HEAD = "a" * 40
BASE = "b" * 40


class WireBacking(InMemoryBackingStore):
    """Exercise the real JSON codec at every offline persistence boundary."""

    def save_entry(self, key, expected_revision, updated):
        decoded = queue_state_from_dict(_decode_queue_document(serialize_queue_document(_state_to_dict(updated))))
        super().save_entry(key, expected_revision, decoded)


def test_preactivation_cannot_bootstrap_or_be_promoted_by_replacing_a_status():
    store = QueueStore(REPO, backing=WireBacking())
    state = store.save(store.load(), 0)
    controller = LoopController(lambda evidence: True, lambda: NOW)
    with pytest.raises(AdmissionBlockedError):
        controller.register_obligation(state, "problem", 42)
    with pytest.raises(ValueError):
        store.save(replace(state, migration_status="native"), state.revision)


def test_schema_three_omission_does_not_default_to_empty_history():
    raw = asdict(QueueState(REPO, 0, {}, [], []))
    del raw["attempts"]
    with pytest.raises(ValueError):
        queue_state_from_dict(raw)


class Harness:
    """Independent fake evidence authority and restarting JSON-backed controller."""

    def __init__(self):
        self.verified = set()
        self.now = NOW
        self.controller = LoopController(lambda proof: proof.evidence_id in self.verified, lambda: self.now)
        self.backing = WireBacking()
        self.store = QueueStore(REPO, backing=self.backing)
        self.state = self.store.load()

    def proof(self, kind, subject, pr=42, **kwargs):
        envelope = self.state.pr_envelopes.get(pr)
        values = dict(
            evidence_id="",
            repo=REPO,
            pr_number=pr,
            head_sha=envelope.head_sha if envelope else HEAD,
            base_sha=envelope.base_sha if envelope else BASE,
            policy_version=envelope.policy_version if envelope else "policy-1",
            kind=kind,
            subject=subject,
            before="none",
            after="actionable",
            source_digest="c" * 64,
            source_revision="provider-revision-1",
            issuer="independent-verifier",
            producer="worker",
            observed_at=self.now,
            valid_until=self.now + timedelta(minutes=5),
            complete=True,
        )
        values.update(kwargs)
        if kind == "observation" and "inventory" not in kwargs:
            values["inventory"] = tuple(
                finding.comment_key for finding in self.state.findings.values() if finding.pr_number == pr
            ) or (f"{pr}:canonical-problem",)
        proof = Evidence(**values)
        proof = replace(proof, evidence_id=proof.digest())
        self.verified.add(proof.evidence_id)
        return proof

    def save(self, state):
        self.store.save(state, self.state.revision)
        self.store = QueueStore(REPO, backing=self.backing)
        self.state = self.store.load()
        return self.state

    def apply(self, method, *args, **kwargs):
        if method == "observe_provider_capacity":
            observation = args[0]
            receipt = self.proof(
                "observation",
                observation.provider,
                pr=0,
                before=f"capacity:{observation.capacity}",
                after=f"occupied:{observation.occupied}:reservations:{observation.reservation_count}",
                related_id=f"capacity:{observation.provider}:epoch:{self.state.global_epoch}",
            )
            self.state = replace(self.state, evidence={**self.state.evidence, receipt.evidence_id: receipt})
            args = (replace(observation, receipt_evidence_id=receipt.evidence_id), *args[1:])
        elif method == "bind_accepted_worker":
            request = self.state.permit_requests[args[0]]
            receipt = self.controller._admission_receipt(
                self.state,
                kind="acceptance",
                request=request,
                subject=args[0],
                before=kwargs["remote_task_id"],
                after=kwargs["model"],
                related_id=request.permit_id,
            )
            self.verified.add(receipt.evidence_id)
            self.state = replace(self.state, evidence={**self.state.evidence, receipt.evidence_id: receipt})
        result = getattr(self.controller, method)(self.state, *args, **kwargs)
        state, value = result if isinstance(result, tuple) else (result, None)
        self.save(state)
        return value

    def activate(self):
        history = QueueState(REPO, 0, {}, [], [])
        proof = self.proof(
            "migration",
            "repository-inventory",
            pr=0,
            before=_legacy_digest(self.state),
            after=_history_digest(history),
            source_revision=str(self.state.revision),
        )
        self.apply("prepare_legacy_migration", history, proof)
        self.apply("activate_migration", proof.evidence_id)

    def enroll(self, pr=42, problem="canonical-problem"):
        if self.state.migration_status != "active":
            self.activate()
        if pr not in self.state.pr_envelopes:
            self.apply(
                "enroll_pr",
                self.proof("observation", str(pr), pr=pr, inventory=(f"{pr}:{problem}",)),
                self.proof("history", str(pr), pr=pr, before="unknown", after="empty"),
            )
        else:
            inventory = tuple(
                finding.comment_key for finding in self.state.findings.values() if finding.pr_number == pr
            )
            inventory = tuple(dict.fromkeys((*inventory, f"{pr}:{problem}")))
            self.apply("observe_pr", self.proof("observation", str(pr), pr=pr, inventory=inventory))
        obligation = self.apply("register_obligation", problem, pr)
        self.apply(
            "register_finding", obligation, self.proof("finding", f"{pr}:{problem}", pr=pr, related_id=obligation)
        )
        return obligation

    def start(self, obligation, batch="batch-1", attempt="attempt-1", auth=None):
        self.apply("begin_round", obligation, batch, auth)
        attempt_auth = auth if self.state.obligations[obligation].attempt_ids else None
        self.apply("authorize_attempt", obligation, batch, attempt, attempt_auth)

    def fail(self, attempt_id):
        attempt = self.state.attempts[attempt_id]
        pr = attempt.pr_number
        self.apply("mark_dispatch_unknown", attempt_id)
        acceptance = self.proof(
            "acceptance",
            attempt_id,
            pr=pr,
            before=f"provider-task:{attempt_id}",
            after="gpt-6-astra" if attempt.kind == AttemptKind.ASTRA else "gpt-5.6-luna",
            related_id=attempt.observation_id,
        )
        self.apply("record_acceptance", attempt_id, acceptance)
        failure = self.proof(
            "failure", attempt_id, pr=pr, before="terminal", after="unresolved", related_id=acceptance.evidence_id
        )
        self.apply("record_outcome", attempt_id, failure)
        return failure.evidence_id

    def review(self, batch_id):
        batch = self.state.rounds[batch_id]
        publication = self.proof(
            "publication",
            batch_id,
            pr=batch.pr_number,
            after=self.state.pr_envelopes[batch.pr_number].head_sha,
            related_id=batch.observation_id,
        )
        self.apply("record_publication", batch_id, publication)
        self.apply(
            "record_batch_review",
            batch_id,
            self.proof("review", batch_id, pr=batch.pr_number, related_id=publication.evidence_id),
        )


def test_empty_complete_inventory_activation_survives_restart():
    h = Harness()
    h.activate()
    assert h.state.migration_status == "active"
    assert h.state.migration is not None
    assert h.state.pr_envelopes == {}
    assert h.state.evidence[h.state.migration.evidence_id].inventory == ()


def test_shared_admission_is_fair_durable_and_releases_only_on_terminal_evidence():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.apply(
        "observe_provider_capacity",
        ProviderCapacityObservation(
            provider="github",
            observed_at=NOW,
            valid_until=NOW + timedelta(minutes=5),
            capacity=1,
            occupied=0,
            reservation_count=0,
            evidence_id="capacity-1",
        ),
    )
    _, request = h.controller.request_worker_admission(
        h.state,
        request_id="request-1",
        pr_number=42,
        obligation_id=obligation,
        batch_id="batch-1",
        worker_id="worker-1",
        provider="github",
    )
    h.save(
        h.controller.request_worker_admission(
            h.state,
            request_id="request-1",
            pr_number=42,
            obligation_id=obligation,
            batch_id="batch-1",
            worker_id="worker-1",
            provider="github",
        )[0]
    )
    decision = h.apply("admit_worker", "request-1")
    assert decision.admitted and decision.permit_id == "permit:request-1"
    h.apply("mark_worker_dispatch_unknown", "request-1")
    h.apply(
        "bind_accepted_worker",
        "request-1",
        remote_task_id="task-1",
        remote_session_id="session-1",
        model="gpt-5.6-luna",
    )
    proof = h.proof(
        "success",
        "request-1",
        before="terminal",
        after="satisfied",
        related_id="permit:request-1",
    )
    h.apply("release_worker_admission", "request-1", proof)
    assert h.state.active_permits["permit:request-1"].status.value == "released"
    assert h.state.permit_requests["request-1"].status.value == "released"


def test_shared_pool_ceiling_and_cas_contention_survive_restart():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.apply(
        "observe_provider_capacity",
        ProviderCapacityObservation(
            provider="github",
            observed_at=NOW,
            valid_until=NOW + timedelta(minutes=5),
            capacity=100,
            occupied=0,
            reservation_count=0,
            evidence_id="capacity-100",
        ),
    )
    state = h.state
    for index in range(101):
        state, _ = h.controller.request_worker_admission(
            state,
            request_id=f"request-{index}",
            pr_number=42,
            obligation_id=obligation,
            batch_id="batch-1",
            worker_id=f"worker-{index}",
            provider="github",
            parent_request_id="request-0" if index else None,
        )
    h.save(state)
    for index in range(100):
        state, decision = h.controller.admit_worker(h.state, f"request-{index}")
        assert decision.admitted
        h.save(state)
    decision = h.apply("admit_worker", "request-100")
    assert not decision.admitted
    assert decision.reason == "global capacity exhausted"
    assert len(h.state.active_permits) == 100

    stale = h.store.load()
    admitted, _ = h.controller.admit_worker(stale, "request-100")
    with pytest.raises(ConcurrentModificationError):
        h.store.save(admitted, stale.revision - 1)
    assert len(h.store.load().active_permits) == 100


def test_unavailable_provider_does_not_block_another_fair_candidate():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.apply(
        "observe_provider_capacity",
        ProviderCapacityObservation(
            provider="github",
            observed_at=NOW,
            valid_until=NOW + timedelta(minutes=5),
            capacity=1,
            occupied=0,
            reservation_count=0,
            evidence_id="capacity-github",
        ),
    )
    for request_id, provider in (("request-unavailable", "azure"), ("request-ready", "github")):
        h.apply(
            "request_worker_admission",
            request_id=request_id,
            pr_number=42,
            obligation_id=obligation,
            batch_id="batch-1",
            worker_id=request_id,
            provider=provider,
        )
    decision = h.apply("admit_worker", "request-ready")
    assert decision.admitted
    blocked = h.apply("admit_worker", "request-unavailable")
    assert not blocked.admitted
    assert blocked.reason == "provider capacity unavailable"


def test_unknown_worker_requires_exact_nonacceptance_and_retains_capacity_after_expiry():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.apply(
        "observe_provider_capacity",
        ProviderCapacityObservation(
            provider="github",
            observed_at=NOW,
            valid_until=NOW + timedelta(minutes=5),
            capacity=1,
            occupied=0,
            reservation_count=0,
            evidence_id="capacity-unknown",
        ),
    )
    h.apply(
        "request_worker_admission",
        request_id="request-unknown",
        pr_number=42,
        obligation_id=obligation,
        batch_id="batch-1",
        worker_id="worker-unknown",
        provider="github",
        deadline_at=NOW + timedelta(minutes=1),
    )
    h.apply("admit_worker", "request-unknown")
    h.apply("mark_worker_dispatch_unknown", "request-unknown")
    h.now += timedelta(minutes=2)
    with pytest.raises(AdmissionBlockedError, match="nonacceptance"):
        h.apply(
            "release_worker_admission",
            "request-unknown",
            h.proof(
                "failure",
                "request-unknown",
                after="not_accepted",
                related_id="permit:request-unknown",
            ),
        )
    with pytest.raises(AdmissionBlockedError, match="bound"):
        h.apply(
            "release_worker_admission",
            "request-unknown",
            h.proof(
                "absence",
                "request-unknown",
                after="not_accepted",
                related_id="forged-permit",
            ),
        )
    h.apply(
        "release_worker_admission",
        "request-unknown",
        h.proof(
            "absence",
            "request-unknown",
            after="not_accepted",
            related_id="permit:request-unknown",
        ),
    )
    assert h.state.active_permits["permit:request-unknown"].status.value == "released"


def test_two_prs_share_cas_but_not_bootstrap_or_problem_authority():
    h = Harness()
    first, second = h.enroll(42), h.enroll(43)
    h.start(first, "42", "a42")
    h.start(second, "43", "a43")
    assert first != second
    assert h.state.pr_envelopes[42].rounds_used == h.state.pr_envelopes[43].rounds_used == 1
    assert set(h.state.rounds) == {"42", "43"}
    h.fail("a42")
    h.review("42")
    third = h.enroll(42, "independent-problem")
    with pytest.raises(AdmissionBlockedError, match="requires progress"):
        h.apply("begin_round", third, "cannot-renew-bootstrap")
    assert h.state.pr_envelopes[42].rounds_used == 1


def test_cas_stale_controller_and_duplicate_replay_preserve_one_batch():
    h = Harness()
    obligation = h.enroll()
    stale = h.store.load()
    planned, _ = h.controller.begin_round(stale, obligation, "one")
    h.save(planned)
    with pytest.raises(ConcurrentModificationError):
        h.store.save(planned, stale.revision)
    h.apply("begin_round", obligation, "one")
    assert h.state.pr_envelopes[42].rounds_used == 1
    other = h.enroll(43)
    with pytest.raises(AdmissionBlockedError, match="replay differs"):
        h.apply("begin_round", other, "one")


def test_initial_retry_astra_accepted_accounting_survives_every_save():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    assert h.state.attempts["attempt-1"].status == AttemptStatus.AUTHORIZED
    with pytest.raises(AdmissionBlockedError, match="not independently failed"):
        h.apply("authorize_attempt", obligation, "batch-1", "early-astra", "fake-failure")
    first = h.fail("attempt-1")
    h.apply("authorize_attempt", obligation, "batch-1", "retry", first)
    assert h.state.attempts["retry"].kind == AttemptKind.RETRY_LUNA
    second = h.fail("retry")
    h.apply("authorize_attempt", obligation, "batch-1", "astra", second)
    assert h.state.attempts["astra"].kind == AttemptKind.ASTRA
    assert h.state.attempts["astra"].sequence == 3
    h.fail("astra")
    assert h.state.obligations[obligation].status == "isolated"
    with pytest.raises(AdmissionBlockedError, match="remediation"):
        h.apply("authorize_attempt", obligation, "batch-1", "another-astra", second)
    assert len(h.state.attempts) == 3
    assert h.state.pr_envelopes[42].rounds_used == 1


def test_published_recovery_batch_consumes_another_round_before_attempt_acceptance():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    failure = h.fail("attempt-1")
    h.review("batch-1")
    h.start(obligation, "retry-batch", "retry", failure)
    assert h.state.pr_envelopes[42].rounds_used == 2
    assert h.state.attempts["retry"].status == AttemptStatus.AUTHORIZED
    assert h.state.rounds["batch-1"].phase == "reviewed"
    with pytest.raises(AdmissionBlockedError):
        h.apply("begin_round", obligation, "replayed-failure", failure)


def test_polling_429_and_ambiguous_dispatch_do_not_consume_retry_or_allow_replacement():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.apply("mark_dispatch_unknown", "attempt-1")
    h.apply("mark_dispatch_unknown", "attempt-1")
    with pytest.raises(AdmissionBlockedError):
        h.apply("record_outcome", "attempt-1", h.proof("failure", "attempt-1", before="429", after="unresolved"))
    with pytest.raises(AdmissionBlockedError):
        h.apply("authorize_attempt", obligation, "batch-1", "duplicate-task")
    attempt = h.state.attempts["attempt-1"]
    h.apply(
        "record_nonacceptance",
        "attempt-1",
        h.proof("absence", "attempt-1", after="not_accepted", related_id=attempt.observation_id),
    )
    assert h.state.attempts["attempt-1"].status == AttemptStatus.AUTHORIZED
    assert len(h.state.attempts) == 1
    h.fail("attempt-1")
    assert len(h.state.attempts) == 1


def test_acceptance_model_and_provider_task_identity_cannot_be_forged_or_reused():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.apply("mark_dispatch_unknown", "attempt-1")
    proof = h.proof(
        "acceptance",
        "attempt-1",
        before="task",
        after="gpt-6-astra",
        related_id=h.state.attempts["attempt-1"].observation_id,
    )
    with pytest.raises(ValueError, match="model"):
        h.apply("record_acceptance", "attempt-1", proof)
    assert h.state.attempts["attempt-1"].acceptance_id is None


def test_independent_verifier_rejects_well_formed_worker_evidence():
    h = Harness()
    h.enroll()
    proof = h.proof("observation", "42")
    h.verified.remove(proof.evidence_id)
    with pytest.raises(AdmissionBlockedError, match="independent"):
        h.apply("observe_pr", proof)


@pytest.mark.parametrize("hold", ["held", "ignored"])
def test_authoritative_holds_veto_round_attempt_and_dispatch(hold):
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.apply("observe_pr", h.proof("observation", "42", before=hold))
    with pytest.raises(AdmissionBlockedError, match="held or ignored"):
        h.apply("mark_dispatch_unknown", "attempt-1")
    with pytest.raises(AdmissionBlockedError):
        h.apply("authorize_attempt", obligation, "batch-1", "retry")
    assert h.state.attempts["attempt-1"].status == AttemptStatus.AUTHORIZED


@pytest.mark.parametrize(
    "field,value",
    [
        ("head_sha", "d" * 40),
        ("base_sha", "e" * 40),
        ("policy_version", "policy-2"),
    ],
)
def test_human_scope_changes_invalidate_draft_not_problem_or_round_history(field, value):
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.apply("observe_pr", h.proof("observation", "42", **{field: value}))
    assert h.state.rounds["batch-1"].phase == "invalidated"
    assert h.state.pr_envelopes[42].stage == "planning"
    assert h.apply("register_obligation", "canonical-problem", 42) == obligation
    with pytest.raises(AdmissionBlockedError, match="stale"):
        h.apply("mark_dispatch_unknown", "attempt-1")
    assert len(h.state.attempts) == 1


def test_authorized_attempt_renews_fresh_unchanged_observation_after_queue_delay():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.now += timedelta(minutes=6)
    h.apply("observe_pr", h.proof("observation", "42", source_revision="fresh-poll"))
    h.apply("renew_authorized_attempt", "attempt-1")
    assert h.state.pr_envelopes[42].rounds_used == 1
    assert h.state.attempts["attempt-1"].status == AttemptStatus.AUTHORIZED
    h.apply("mark_dispatch_unknown", "attempt-1")
    assert h.state.attempts["attempt-1"].status == AttemptStatus.UNKNOWN
    assert h.state.attempts["attempt-1"].observation_id == h.state.pr_envelopes[42].observation_id


def test_changed_scope_replans_unaccepted_attempt_on_new_head_without_duplicate_attempt():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.now += timedelta(seconds=1)
    h.apply("observe_pr", h.proof("observation", "42", head_sha="d" * 40))
    assert h.state.rounds["batch-1"].phase == "invalidated"
    h.apply("replan_authorized_attempt", "attempt-1", "batch-2")
    assert h.state.pr_envelopes[42].rounds_used == 2
    assert h.state.attempts["attempt-1"].batch_id == "batch-2"
    assert h.state.attempts["attempt-1"].status == AttemptStatus.AUTHORIZED
    h.apply("mark_dispatch_unknown", "attempt-1")
    assert h.state.attempts["attempt-1"].status == AttemptStatus.UNKNOWN


def test_unknown_attempt_cannot_be_renewed_or_replanned_from_clock_expiry():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.apply("mark_dispatch_unknown", "attempt-1")
    h.now += timedelta(minutes=6)
    h.apply("observe_pr", h.proof("observation", "42", source_revision="later-poll"))
    with pytest.raises(AdmissionBlockedError, match="authorized"):
        h.apply("renew_authorized_attempt", "attempt-1")
    with pytest.raises(AdmissionBlockedError, match="authorized"):
        h.apply("replan_authorized_attempt", "attempt-1", "batch-2")


@pytest.mark.parametrize("replan", [False, True])
def test_refresh_retains_other_pr_obligations_and_accepted_history(replan):
    h = Harness()
    first = h.enroll()
    other = h.enroll(43)
    h.start(other, "other-batch", "other-attempt")
    h.start(first)
    failure = h.fail("attempt-1")
    h.apply("authorize_attempt", first, "batch-1", "retry", failure)
    pending = h.enroll(42, "independent-pending")
    retained = {key: value for key, value in h.state.attempts.items() if key != "retry"}
    admitted = h.state.rounds["batch-1"].observation_id
    h.now += timedelta(minutes=6)
    h.apply("observe_pr", h.proof("observation", "42", head_sha="d" * 40 if replan else HEAD))
    if replan:
        h.apply("replan_authorized_attempt", "retry", "fresh-batch")
    else:
        h.apply("renew_authorized_attempt", "retry")
    assert all(h.state.attempts[key] == value for key, value in retained.items())
    assert pending in h.state.pr_envelopes[42].obligation_ids
    assert h.state.obligations[first].attempt_ids == ("attempt-1", "retry")
    assert h.state.rounds["batch-1"].observation_id == admitted
    assert h.state.pr_envelopes[42].rounds_used == (2 if replan else 1)
    h.apply("mark_dispatch_unknown", "retry")
    attempt = h.state.attempts["retry"]
    h.apply(
        "record_acceptance",
        "retry",
        h.proof(
            "acceptance", "retry", before="provider:retry", after="gpt-5.6-luna", related_id=attempt.observation_id
        ),
    )
    assert h.state.attempts["retry"].status == AttemptStatus.ACCEPTED
    assert h.state.attempts["other-attempt"] == retained["other-attempt"]


def test_save_rejects_rebinding_invalidated_batch_after_replan():
    h = Harness()
    h.start(h.enroll())
    h.apply("observe_pr", h.proof("observation", "42", head_sha="d" * 40))
    h.apply("replan_authorized_attempt", "attempt-1", "batch-2")
    original = h.state.rounds["batch-1"]
    forged = replace(
        h.state,
        rounds={
            **h.state.rounds,
            "batch-1": replace(original, observation_id=h.state.rounds["batch-2"].observation_id),
        },
    )
    with pytest.raises(ValueError, match="immutable batch"):
        h.store.save(forged, h.state.revision)
    assert h.store.load().rounds["batch-1"] == original


@pytest.mark.parametrize("replan", [False, True])
def test_refresh_with_another_completed_obligation_retains_all_attempts(replan):
    h = Harness()
    first = h.enroll()
    h.start(first)
    failure = h.fail("attempt-1")
    h.review("batch-1")
    progress = h.proof("progress_gate", "check", before="failing", after="satisfied", related_id="batch-1")
    h.apply("record_progress", progress)
    independent = h.enroll(42, "independent")
    h.start(independent, "independent-batch", "independent-attempt", progress.evidence_id)
    h.fail("independent-attempt")
    h.review("independent-batch")
    h.start(first, "retry-batch", "retry", failure)
    original = h.state
    h.now += timedelta(minutes=6)
    h.apply("observe_pr", h.proof("observation", "42", head_sha="d" * 40 if replan else HEAD))
    if replan:
        h.apply("replan_authorized_attempt", "retry", "replanned-batch")
    else:
        h.apply("renew_authorized_attempt", "retry")
    assert h.state.obligations == original.obligations
    for identity in ("attempt-1", "independent-attempt"):
        assert h.state.attempts[identity] == original.attempts[identity]
    h.apply("mark_dispatch_unknown", "retry")
    attempt = h.state.attempts["retry"]
    h.apply(
        "record_acceptance",
        "retry",
        h.proof(
            "acceptance",
            "retry",
            before="provider:retry",
            after="gpt-5.6-luna",
            related_id=attempt.observation_id,
        ),
    )
    assert h.state.attempts["retry"].status == AttemptStatus.ACCEPTED
    assert h.state.pr_envelopes[42].rounds_used == (4 if replan else 3)


def test_progress_requires_before_after_independent_review_and_is_consumed_once():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.fail("attempt-1")
    with pytest.raises(AdmissionBlockedError, match="unpublished"):
        h.apply("record_batch_review", "batch-1", h.proof("review", "batch-1"))
    h.review("batch-1")
    for before, after in [("head-1", "head-2"), ("failing", "failing"), ("comment", "reply")]:
        with pytest.raises(AdmissionBlockedError, match="failing-to-satisfied"):
            h.apply(
                "record_progress",
                h.proof("progress_gate", "required-check", before=before, after=after, related_id="batch-1"),
            )
    proof = h.proof("progress_gate", "required-check", before="failing", after="satisfied", related_id="batch-1")
    h.apply("record_progress", proof)
    duplicate = h.proof(
        "progress_gate",
        "required-check",
        before="failing",
        after="satisfied",
        related_id="batch-1",
        source_revision="another-event",
    )
    with pytest.raises(AdmissionBlockedError, match="reminted"):
        h.apply("record_progress", duplicate)
    next_obligation = h.enroll(42, "independent")
    h.apply("begin_round", next_obligation, "two", proof.evidence_id)
    assert h.state.rounds["two"].authorization_id == proof.evidence_id
    with pytest.raises(AdmissionBlockedError):
        h.apply("begin_round", next_obligation, "three", proof.evidence_id)


def test_remediation_verifies_first_grants_one_extra_luna_and_never_resets():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    auth = h.fail("attempt-1")
    h.apply("authorize_attempt", obligation, "batch-1", "retry", auth)
    auth = h.fail("retry")
    h.apply("authorize_attempt", obligation, "batch-1", "astra", auth)
    h.fail("astra")
    remediation = h.proof("remediation", obligation, before="defect-present", after="distinct-fix")
    h.apply("record_remediation", obligation, remediation)
    h.apply("record_remediation", obligation, remediation)
    with pytest.raises(AdmissionBlockedError):
        h.apply("authorize_attempt", obligation, "batch-1", "extra", remediation.evidence_id)
    verification = h.proof("verification", obligation, after="repair_required", related_id=remediation.evidence_id)
    h.apply("verify_remediation", obligation, verification)
    assert len(h.state.attempts) == 3
    h.apply("authorize_attempt", obligation, "batch-1", "extra", verification.evidence_id)
    assert h.state.attempts["extra"].kind == AttemptKind.REMEDIATION
    h.fail("extra")
    with pytest.raises(AdmissionBlockedError):
        h.apply(
            "record_remediation",
            obligation,
            h.proof("remediation", obligation, before="defect-present", after="yet-another-fix"),
        )
    with pytest.raises(AdmissionBlockedError):
        h.apply("authorize_attempt", obligation, "batch-1", "fifth", verification.evidence_id)
    assert len(h.state.attempts) == 4


def test_legacy_real_work_item_updates_remain_available_but_unknown_history_cannot_activate():
    h = Harness()
    item = WorkItem(42, REPO, "legacy-sha", "eligible", NOW, WorkItemStatus.QUEUED, retry_count=2)
    h.save(replace(h.state, items={42: item}))
    h.save(replace(h.state, items={42: replace(item, retry_count=3)}))
    assert h.state.items[42].retry_count == 3
    history = QueueState(REPO, 0, {}, [], [])
    proof = h.proof(
        "migration",
        "inventory",
        pr=0,
        before=_legacy_digest(h.state),
        after=_history_digest(history),
        source_revision=str(h.state.revision),
    )
    with pytest.raises(AdmissionBlockedError, match="omitted"):
        h.apply("prepare_legacy_migration", history, proof)
    with pytest.raises(AdmissionBlockedError):
        h.apply("register_obligation", "legacy-problem", 42)


def test_activation_rejects_intervening_legacy_save_even_if_it_changes_no_work():
    h = Harness()
    history = QueueState(REPO, 0, {}, [], [])
    proof = h.proof(
        "migration",
        "inventory",
        pr=0,
        before=_legacy_digest(h.state),
        after=_history_digest(history),
        source_revision=str(h.state.revision),
    )
    h.apply("prepare_legacy_migration", history, proof)
    h.save(h.state)
    with pytest.raises(AdmissionBlockedError, match="changed"):
        h.apply("activate_migration", proof.evidence_id)
    with pytest.raises(Exception):
        h.store.save(replace(h.state, migration_status="active"), h.state.revision)


def test_schema3_rejects_corrupted_records_and_budget_reset_after_restart():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    raw = _state_to_dict(h.state)
    raw["attempts"]["attempt-1"]["sequence"] = 0
    with pytest.raises(ValueError, match="order"):
        queue_state_from_dict(raw)
    raw = _state_to_dict(h.state)
    raw["obligations"][obligation]["extra"] = "ignored?"
    with pytest.raises(ValueError, match="declared fields"):
        queue_state_from_dict(raw)
    raw = _state_to_dict(h.state)
    raw["pr_envelopes"][42]["rounds_used"] = 0
    with pytest.raises(ValueError, match="ledger"):
        queue_state_from_dict(raw)
    raw = _state_to_dict(h.state)
    raw["attempts"]["attempt-1"]["sequence"] = True
    with pytest.raises(ValueError, match="type"):
        queue_state_from_dict(raw)


@pytest.mark.parametrize(
    "disposition",
    [
        "implement_suggestion",
        "implement_better_fix",
        "reject_with_evidence",
        "defer_with_followup",
    ],
)
def test_four_dispositions_persist_as_proposals_not_fake_terminal_receipts(disposition):
    h = Harness()
    obligation = h.enroll()
    h.apply(
        "register_finding", obligation, h.proof("finding", f"second:{disposition}", related_id=obligation), disposition
    )
    assert any(finding.disposition == disposition for finding in h.state.findings.values())
    assert not hasattr(h.controller, "record_finding_receipt")


def test_lifetime_rounds_49_50_51_and_already_authorized_completion():
    h = Harness()
    previous_batch = None
    for number in range(1, 51):
        obligation = h.enroll(42, f"independent-{number}")
        authorization = None
        if previous_batch is not None:
            proof = h.proof(
                "progress_gate", f"gate-{number}", before="failing", after="satisfied", related_id=previous_batch
            )
            h.apply("record_progress", proof)
            authorization = proof.evidence_id
        batch, attempt = f"batch-{number}", f"attempt-{number}"
        h.start(obligation, batch, attempt, authorization)
        assert h.state.pr_envelopes[42].rounds_used == number
        failure = h.fail(attempt)
        if number == 50:
            with pytest.raises(AdmissionBlockedError, match="already-authorized"):
                h.apply("authorize_attempt", obligation, batch, "hidden-retry-51", failure)
        h.review(batch)
        previous_batch = batch
    independent = h.enroll(42, "independent-51")
    proof = h.proof("progress_gate", "gate-51", before="failing", after="satisfied", related_id="batch-50")
    h.apply("record_progress", proof)
    with pytest.raises(AdmissionBlockedError, match="50-round"):
        h.apply("begin_round", independent, "batch-51", proof.evidence_id)
    assert len(h.state.rounds) == 50
    assert h.state.rounds["batch-50"].phase == "reviewed"


def test_migration_preserves_nonempty_round_and_accepted_attempt_history():
    original = Harness()
    obligation = original.enroll()
    original.start(obligation)
    failure = original.fail("attempt-1")
    original.apply("authorize_attempt", obligation, "batch-1", "retry", failure)
    original.fail("retry")
    original.review("batch-1")
    h = Harness()
    h.verified.update(original.verified)
    h.save(replace(h.state, items={42: WorkItem(42, REPO, HEAD, "eligible", NOW, WorkItemStatus.QUEUED)}))
    history = original.state
    proof = h.proof(
        "migration",
        "complete-inventory",
        pr=0,
        before=_legacy_digest(h.state),
        after=_history_digest(history),
        source_revision=str(h.state.revision),
        inventory=("42",),
    )
    h.apply("prepare_legacy_migration", history, proof)
    h.apply("activate_migration", proof.evidence_id)
    assert h.state.obligations[obligation].attempt_ids == ("attempt-1", "retry")
    assert h.state.pr_envelopes[42].rounds_used == 1
    assert h.state.attempts["retry"].status == AttemptStatus.FAILED


def test_migration_cannot_mark_accepted_or_possibly_running_work_known_from_counts():
    original = Harness()
    obligation = original.enroll()
    original.start(obligation)
    original.apply("mark_dispatch_unknown", "attempt-1")
    h = Harness()
    h.verified.update(original.verified)
    history = original.state
    proof = h.proof(
        "migration",
        "inventory",
        pr=0,
        before=_legacy_digest(h.state),
        after=_history_digest(history),
        source_revision="0",
        inventory=("42",),
    )
    with pytest.raises(AdmissionBlockedError, match="terminal"):
        h.apply("prepare_legacy_migration", history, proof)
    h.save(replace(h.state, items={42: WorkItem(42, REPO, HEAD, "eligible", NOW, WorkItemStatus.UNKNOWN)}))
    with pytest.raises(AdmissionBlockedError, match="running or unknown"):
        h.apply("prepare_legacy_migration", history, proof)


@pytest.mark.parametrize(
    "mutator",
    [
        lambda raw, oid: raw["obligations"][oid].update(pr_number=43),
        lambda raw, oid: raw["obligations"][oid].update(budget_known=False),
        lambda raw, oid: raw["obligations"][oid].update(attempt_ids=[]),
        lambda raw, oid: raw["pr_envelopes"][42].update(active_batch_id="foreign"),
        lambda raw, oid: raw["pr_envelopes"][42].update(round_limit=51),
        lambda raw, oid: raw["pr_envelopes"][42].update(rounds_used=51),
        lambda raw, oid: raw["rounds"]["batch-1"].update(pr_number=43),
        lambda raw, oid: raw["rounds"]["batch-1"].update(batch_id="another-key"),
        lambda raw, oid: raw["attempts"]["attempt-1"].update(status="failed"),
        lambda raw, oid: raw["attempts"]["attempt-1"].update(kind="astra"),
        lambda raw, oid: raw["attempts"]["attempt-1"].pop("status"),
        lambda raw, oid: raw["evidence"].pop(next(iter(raw["evidence"]))),
        lambda raw, oid: raw["findings"][next(iter(raw["findings"]))].update(disposition="no_code"),
    ],
)
def test_malformed_persisted_cross_references_and_histories_fail_closed(mutator):
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    raw = _state_to_dict(h.state)
    mutator(raw, obligation)
    with pytest.raises(ValueError):
        queue_state_from_dict(raw)


def test_missing_schema_cannot_disguise_new_or_unknown_history_as_legacy():
    raw = {"repo": REPO, "attempts": {}}
    with pytest.raises(ValueError):
        queue_state_from_dict(raw)
    with pytest.raises(ValueError):
        queue_state_from_dict({"repo": REPO, "active_permits": {"lost-worker": {}}})


def test_identical_provider_receipt_replay_is_idempotent_after_restart():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.fail("attempt-1")
    attempt = h.state.attempts["attempt-1"]
    h.apply("record_acceptance", "attempt-1", h.state.evidence[attempt.acceptance_id])
    h.apply("record_outcome", "attempt-1", h.state.evidence[attempt.outcome_id])
    assert len(h.state.attempts) == 1
    assert h.state.attempts["attempt-1"].sequence == 1


def test_changed_evidence_or_forged_status_cannot_clear_prepared_activation():
    h = Harness()
    history = QueueState(REPO, 0, {}, [], [])
    proof = h.proof(
        "migration",
        "inventory",
        pr=0,
        before=_legacy_digest(h.state),
        after=_history_digest(history),
        source_revision="0",
    )
    h.apply("prepare_legacy_migration", history, proof)
    with pytest.raises(AdmissionBlockedError):
        h.apply("activate_migration", "different-proof")
    changed = replace(proof, source_digest="d" * 64)
    with pytest.raises(ValueError, match="digest"):
        h.save(replace(h.state, evidence={proof.evidence_id: changed}))
    with pytest.raises(ValueError):
        h.save(replace(h.state, migration_status="native"))


def test_timeout_after_cas_apply_reloads_same_admission_without_double_charge():
    class AmbiguousBacking(WireBacking):
        fail_after_apply = False

        def save_entry(self, key, expected_revision, updated):
            super().save_entry(key, expected_revision, updated)
            if self.fail_after_apply:
                self.fail_after_apply = False
                raise RuntimeError("simulated timeout after apply")

    h = Harness()
    h.backing = AmbiguousBacking()
    h.store = QueueStore(REPO, backing=h.backing)
    obligation = h.enroll()
    admitted, _ = h.controller.begin_round(h.state, obligation, "stable-admission")
    h.backing.fail_after_apply = True
    with pytest.raises(RuntimeError, match="after apply"):
        h.store.save(admitted, h.state.revision)
    h.state = h.store.load()
    h.apply("begin_round", obligation, "stable-admission")
    assert h.state.pr_envelopes[42].rounds_used == 1
    assert list(h.state.rounds) == ["stable-admission"]


def test_unchanged_fresh_observation_does_not_invalidate_authorized_input():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.now += timedelta(seconds=1)
    h.apply("observe_pr", h.proof("observation", "42", source_revision="new-poll"))
    h.apply("mark_dispatch_unknown", "attempt-1")
    assert h.state.attempts["attempt-1"].status == AttemptStatus.UNKNOWN


def test_publication_new_head_requires_bound_review_and_keeps_original_input():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    failure = h.fail("attempt-1")
    batch = h.state.rounds["batch-1"]
    publication = h.proof("publication", "batch-1", after="d" * 40, related_id=batch.observation_id)
    h.apply("record_publication", "batch-1", publication)
    h.apply("observe_pr", h.proof("observation", "42", head_sha="d" * 40))
    assert h.state.rounds["batch-1"].phase == "published"
    h.apply("record_batch_review", "batch-1", h.proof("review", "batch-1", related_id=publication.evidence_id))
    with pytest.raises(AdmissionBlockedError, match="stale"):
        h.apply("begin_round", obligation, "stale-recovery", failure)
    revalidated = h.proof(
        "failure",
        "attempt-1",
        before="terminal",
        after="unresolved",
        related_id=h.state.attempts["attempt-1"].acceptance_id,
    )
    h.apply("revalidate_failure", "attempt-1", revalidated)
    h.start(obligation, "recovery-current", "retry-current", revalidated.evidence_id)
    assert h.state.attempts["retry-current"].kind == AttemptKind.RETRY_LUNA
    assert h.state.rounds["batch-1"].observation_id == batch.observation_id


def test_recurring_problem_after_verified_success_keeps_luna_retry_not_fresh_initial():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.apply("mark_dispatch_unknown", "attempt-1")
    attempt = h.state.attempts["attempt-1"]
    acceptance = h.proof(
        "acceptance", "attempt-1", before="accepted-task", after="gpt-5.6-luna", related_id=attempt.observation_id
    )
    h.apply("record_acceptance", "attempt-1", acceptance)
    h.apply(
        "record_outcome",
        "attempt-1",
        h.proof("success", "attempt-1", before="terminal", after="satisfied", related_id=acceptance.evidence_id),
    )
    h.review("batch-1")
    recurring = h.proof(
        "failure",
        "attempt-1",
        before="terminal",
        after="unresolved",
        related_id=acceptance.evidence_id,
        source_revision="later-review",
    )
    h.apply("revalidate_failure", "attempt-1", recurring)
    h.start(obligation, "recurrence", "retry", recurring.evidence_id)
    assert h.state.attempts["attempt-1"].status == AttemptStatus.SUCCEEDED
    assert h.state.attempts["retry"].kind == AttemptKind.RETRY_LUNA


def test_mutating_uncertainty_or_history_directly_through_save_is_rejected():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.apply("mark_dispatch_unknown", "attempt-1")
    attempt = h.state.attempts["attempt-1"]
    with pytest.raises(ValueError, match="absence"):
        h.save(replace(h.state, attempts={"attempt-1": replace(attempt, status=AttemptStatus.AUTHORIZED)}))
    fresh = QueueState(REPO, h.state.revision, {}, [], [])
    with pytest.raises(Exception, match="erase"):
        h.store.save_recovery(fresh, h.store.recovery_token())


def test_no_publication_with_one_failed_and_another_possibly_running_attempt():
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    failure = h.fail("attempt-1")
    h.apply("authorize_attempt", obligation, "batch-1", "retry", failure)
    h.apply("mark_dispatch_unknown", "retry")
    batch = h.state.rounds["batch-1"]
    proof = h.proof("publication", "batch-1", after=HEAD, related_id=batch.observation_id)
    with pytest.raises(AdmissionBlockedError, match="terminal accepted work"):
        h.apply("record_publication", "batch-1", proof)


def test_stale_partial_and_unknown_observation_cannot_be_bootstrap_authority():
    h = Harness()
    obligation = h.enroll()
    partial = h.proof("observation", "42", complete=False)
    with pytest.raises(ValueError, match="incomplete"):
        h.apply("observe_pr", partial)
    h.now += timedelta(minutes=6)
    with pytest.raises(AdmissionBlockedError, match="stale"):
        h.apply("begin_round", obligation, "stale-bootstrap")


def test_unrelated_actionable_inventory_cannot_bootstrap_this_problem():
    h = Harness()
    obligation = h.enroll()
    h.apply("observe_pr", h.proof("observation", "42", inventory=("unrelated-comment",)))
    with pytest.raises(AdmissionBlockedError, match="no actionable"):
        h.apply("begin_round", obligation, "not-observed")


def test_semantic_finding_linkage_requires_independent_evidence_not_new_problem_text():
    h = Harness()
    original = h.enroll()
    other = h.apply("register_obligation", "renamed-problem", 42)
    proof = h.proof("finding", "same-problem-new-review-comment", related_id=original)
    with pytest.raises(ValueError, match="finding evidence mismatch"):
        h.apply("register_finding", other, proof)


def test_duplicate_json_keys_and_missing_published_attempts_are_not_clean_state():
    with pytest.raises(ValueError):
        _decode_queue_document(b'{"repo":"owner/repo","repo":"foreign/repo"}')
    h = Harness()
    obligation = h.enroll()
    h.start(obligation)
    h.fail("attempt-1")
    h.review("batch-1")
    raw = _state_to_dict(h.state)
    raw["attempts"] = {}
    raw["obligations"][obligation]["attempt_ids"] = ()
    with pytest.raises(ValueError, match="terminal attempt history"):
        queue_state_from_dict(raw)
