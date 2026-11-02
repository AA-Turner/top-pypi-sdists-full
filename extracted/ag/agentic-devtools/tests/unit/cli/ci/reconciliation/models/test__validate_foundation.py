"""Foundation invariants over directly constructed, independent record fixtures."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.reconciliation.models import (
    AdmissionController,
    AdmissionFence,
    AdmissionRequestStatus,
    AttemptStatus,
    EffectRecord,
    EffectStatus,
    PermitRequest,
    PermitStatus,
    ProviderCapacityObservation,
    RepairRound,
    WorkerPermit,
    _validate_foundation,
)


@pytest.mark.parametrize(
    "statuses,phase",
    [
        ((), "prepublication"),
        ((AttemptStatus.AUTHORIZED,), "prepublication"),
        ((AttemptStatus.UNKNOWN,), "invalidated"),
        ((AttemptStatus.ACCEPTED,), "prepublication"),
        ((AttemptStatus.SUCCEEDED,), "published"),
        ((AttemptStatus.FAILED,), "reviewed"),
        ((AttemptStatus.FAILED,) * 2, "reviewed"),
        ((AttemptStatus.FAILED,) * 3, "reviewed"),
        ((AttemptStatus.FAILED,) * 3 + (AttemptStatus.SUCCEEDED,), "reviewed"),
    ],
)
def test_accepts_complete_retained_typed_history(foundation, statuses, phase):
    f = foundation(statuses, phase)
    assert _validate_foundation(f.state) is None
    assert _validate_foundation(f.state, history_only=True) is None


def test_accepts_complete_shared_admission_records(foundation):
    f = foundation()
    now = datetime.now(UTC)
    request = PermitRequest(
        "request",
        f.state.repo,
        42,
        "problem",
        "batch",
        "worker",
        "github",
        "gpt-5.6-luna",
        1,
        now,
        now + timedelta(minutes=5),
        0,
        AdmissionRequestStatus.ACCEPTED,
        "permit",
    )
    permit = WorkerPermit(
        "permit",
        "request",
        f.state.repo,
        42,
        "problem",
        "batch",
        "worker",
        "github",
        "gpt-5.6-luna",
        1,
        now,
        now + timedelta(minutes=5),
        PermitStatus.ACCEPTED,
        "task",
        "session",
    )
    state = replace(
        f.state,
        permit_requests={
            "request": request,
            "queued": replace(
                request, request_id="queued", status=AdmissionRequestStatus.QUEUED, permit_id=None, queue_position=1
            ),
        },
        active_permits={"permit": permit},
        controllers={42: AdmissionController(42, f.state.repo, 1, ("permit",), ("request",), f.state.revision)},
        provider_capacity={
            "github": ProviderCapacityObservation(
                "github",
                now,
                now + timedelta(minutes=5),
                10,
                1,
                0,
                "capacity",
            )
        },
        effect_fences={"fence:request": AdmissionFence("fence:request", "request", 1, 1, "github", "gpt-5.6-luna")},
    )
    assert _validate_foundation(state) is None


def test_rejects_unbound_admission_receipts(foundation):
    f = foundation()
    now = datetime.now(UTC)
    request = PermitRequest(
        "request",
        f.state.repo,
        42,
        "problem",
        "batch",
        "worker",
        "github",
        "gpt-5.6-luna",
        1,
        now,
        now + timedelta(minutes=5),
        0,
        AdmissionRequestStatus.ACCEPTED,
        "permit",
    )
    permit = WorkerPermit(
        "permit",
        "request",
        f.state.repo,
        42,
        "problem",
        "batch",
        "worker",
        "github",
        "gpt-5.6-luna",
        1,
        now,
        now + timedelta(minutes=5),
        PermitStatus.ACCEPTED,
        "task",
        "session",
        "missing-acceptance",
    )
    state = replace(
        f.state,
        permit_requests={"request": request},
        active_permits={"permit": permit},
        provider_capacity={
            "github": ProviderCapacityObservation(
                "github", now, now + timedelta(minutes=5), 1, 0, 0, "capacity", source_revision="source"
            )
        },
    )
    with pytest.raises(ValueError, match="dangling acceptance"):
        _validate_foundation(state)


def test_rejects_missing_release_and_capacity_provenance(foundation):
    f = foundation()
    now = datetime.now(UTC)
    released = PermitRequest(
        "released",
        f.state.repo,
        42,
        "problem",
        "batch",
        "worker",
        "github",
        "gpt-5.6-luna",
        1,
        now,
        now + timedelta(minutes=5),
        0,
        AdmissionRequestStatus.RELEASED,
    )
    with pytest.raises(ValueError, match="released request"):
        _validate_foundation(replace(f.state, permit_requests={"released": released}))
    dangling = replace(
        released,
        request_id="dangling",
        status=AdmissionRequestStatus.QUEUED,
        terminal_evidence_id="missing",
    )
    with pytest.raises(ValueError, match="dangling request terminal"):
        _validate_foundation(replace(f.state, permit_requests={"dangling": dangling}))
    reserved = replace(released, request_id="reserved", status=AdmissionRequestStatus.RESERVED, permit_id="permit")
    permit = WorkerPermit(
        "permit",
        "reserved",
        f.state.repo,
        42,
        "problem",
        "batch",
        "worker",
        "github",
        "gpt-5.6-luna",
        1,
        now,
        now + timedelta(minutes=5),
        PermitStatus.RESERVED,
        terminal_evidence_id="missing",
    )
    with pytest.raises(ValueError, match="dangling permit terminal"):
        _validate_foundation(
            replace(f.state, permit_requests={"reserved": reserved}, active_permits={"permit": permit})
        )
    capacity = ProviderCapacityObservation(
        "github",
        now,
        now + timedelta(minutes=5),
        1,
        0,
        0,
        "capacity",
        source_revision="source",
        receipt_evidence_id=f.add("observation", "github", pr_number=0, related_id="wrong"),
    )
    with pytest.raises(ValueError, match="capacity receipt"):
        _validate_foundation(replace(f.state, provider_capacity={"github": capacity}))


@pytest.mark.parametrize("kind", ["progress_gate", "progress_finding", "failure", "verification", "replan"])
def test_round_authorizations_bind_retained_history(foundation, kind):
    f = foundation((AttemptStatus.FAILED,) * 3, "reviewed")
    if kind == "verification":
        remediation = f.add("remediation", "problem", before="broken", after="fixed")
        f.state.obligations["problem"] = replace(f.state.obligations["problem"], remediation_id=remediation)
        authorization = f.add(kind, "problem", after="repair_required", related_id=remediation)
        reason = "recovery"
    elif kind == "failure":
        authorization = f.state.attempts["attempt-2"].outcome_id
        reason = "recovery"
    elif kind == "replan":
        f.state.rounds["batch"] = replace(f.state.rounds["batch"], phase="invalidated")
        authorization, reason = "batch", "replan"
    else:
        authorization = f.add(
            kind,
            "finding" if kind == "progress_finding" else "check",
            before="failing",
            after="satisfied",
            related_id="batch",
        )
        reason = "progress"
    f.state.rounds["second"] = RepairRound(
        "second",
        42,
        2,
        "problem",
        f.state.rounds["batch"].observation_id,
        reason,
        authorization,
    )
    f.state.pr_envelopes[42] = replace(
        f.state.pr_envelopes[42],
        rounds_used=2,
        round_ids=("batch", "second"),
        active_batch_id="second",
    )
    assert _validate_foundation(f.state) is None
    f.state.rounds["second"] = replace(f.state.rounds["second"], authorization_id="missing")
    with pytest.raises(ValueError):
        _validate_foundation(f.state)


@pytest.mark.parametrize(
    "map_name,key,changes,message",
    [
        ("pr_envelopes", 42, {"rounds_used": 0}, "round count"),
        ("pr_envelopes", 42, {"budget_known": False}, "unknown PR"),
        ("pr_envelopes", 42, {"round_limit": 51}, "lifetime budget"),
        ("pr_envelopes", 42, {"hold": "held"}, "authority mismatch"),
        ("pr_envelopes", 42, {"head_sha": "d" * 40}, "scope mismatch"),
        ("obligations", "problem", {"attempt_ids": ()}, "attempt ownership"),
        ("obligations", "problem", {"finding_ids": ()}, "finding ownership"),
        ("obligations", "problem", {"budget_known": False}, "unknown problem"),
        ("findings", "finding", {"disposition": "resolve"}, "disposition"),
        ("findings", "finding", {"observed_heads": ("invalid",)}, "finding evidence"),
        ("rounds", "batch", {"reason": "unknown"}, "round reason"),
        ("rounds", "batch", {"phase": "published"}, "missing publication"),
        ("rounds", "batch", {"phase": "reviewed"}, "missing review"),
        ("rounds", "batch", {"authorization_id": "forged"}, "bootstrap renewed"),
        ("attempts", "attempt-0", {"acceptance_id": "forged"}, "accepted accounting"),
        ("attempts", "attempt-0", {"outcome_id": "forged"}, "terminal accounting"),
    ],
)
def test_rejects_invalid_ownership_accounting_and_authority(foundation, map_name, key, changes, message):
    f = foundation()
    mapping = getattr(f.state, map_name)
    mapping[key] = replace(mapping[key], **changes)
    with pytest.raises(ValueError, match=message):
        _validate_foundation(f.state)


def test_renewed_authority_preserves_original_input(foundation):
    f = foundation()
    identity = f.add(source_revision="fresh")
    f.state.attempts["attempt-0"] = replace(f.state.attempts["attempt-0"], observation_id=identity)
    assert _validate_foundation(f.state) is None
    identity = f.add(head_sha="d" * 40)
    f.state.attempts["attempt-0"] = replace(f.state.attempts["attempt-0"], observation_id=identity)
    with pytest.raises(ValueError, match="admitted batch"):
        _validate_foundation(f.state)


def test_evidence_provenance_and_scope(foundation):
    f = foundation()
    identity = f.add(complete=False)
    with pytest.raises(ValueError, match="incomplete"):
        _validate_foundation(f.state)
    del f.state.evidence[identity]
    identity = f.add(head_sha="not-a-sha")
    with pytest.raises(ValueError, match="evidence scope"):
        _validate_foundation(f.state)


def test_validates_effect_evidence_binding(foundation):
    f = foundation()
    ev_id = f.add(pr_number=42, related_id="eff-1")
    eff = EffectRecord("eff-1", f.state.repo, 42, "reply", "payload-dig", EffectStatus.SETTLED, ev_id)
    eff_none = EffectRecord("eff-none", f.state.repo, 42, "reply", "payload-dig", EffectStatus.INTENT, None)
    f.state.effects["eff-1"] = eff
    f.state.effects["eff-none"] = eff_none
    assert _validate_foundation(f.state) is None

    # Missing evidence
    del f.state.effects["eff-none"]
    del f.state.evidence[ev_id]
    with pytest.raises(ValueError, match="effect evidence is not bound"):
        _validate_foundation(f.state)

    # Mismatched PR number
    ev_wrong_pr = f.proof(pr_number=99, related_id="eff-1")
    f.state.effects["eff-1"] = replace(eff, evidence_id=ev_wrong_pr.evidence_id)
    f.state.evidence[ev_wrong_pr.evidence_id] = ev_wrong_pr
    with pytest.raises(ValueError, match="effect evidence is not bound"):
        _validate_foundation(f.state)

    # Mismatched related ID
    ev_wrong_rel = f.proof(pr_number=42, related_id="wrong-id")
    f.state.effects["eff-1"] = replace(eff, evidence_id=ev_wrong_rel.evidence_id)
    f.state.evidence[ev_wrong_rel.evidence_id] = ev_wrong_rel
    with pytest.raises(ValueError, match="effect evidence is not bound"):
        _validate_foundation(f.state)
