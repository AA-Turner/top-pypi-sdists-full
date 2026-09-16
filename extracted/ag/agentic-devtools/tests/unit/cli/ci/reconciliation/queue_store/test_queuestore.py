"""Tests for QueueStore."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, replace
from datetime import UTC, datetime, timedelta

import pytest

import agentic_devtools.cli.ci.reconciliation.config as cfg
from agentic_devtools.cli.ci.reconciliation.metrics import MetricEventType, create_metric_event
from agentic_devtools.cli.ci.reconciliation.models import (
    AdmissionController,
    AdmissionRequestStatus,
    AttemptStatus,
    EffectRecord,
    EffectStatus,
    MigrationRecord,
    PermitRequest,
    PermitStatus,
    QueueState,
    RepairRound,
    WorkerPermit,
    WorkItem,
    WorkItemStatus,
    _history_digest,
    _legacy_digest,
)
from agentic_devtools.cli.ci.reconciliation.queue_store import (
    ConcurrentModificationError,
    GitHubVariableBackingStore,
    InMemoryBackingStore,
    MigrationRequiredError,
    QuarantineActiveError,
    QueueStore,
    StateDecodeError,
    StateTooLargeError,
)
from agentic_devtools.state import serialize_queue_document


def _make_store() -> QueueStore:
    return QueueStore(repo="owner/repo", backing=InMemoryBackingStore())


def test_load_empty_state() -> None:
    store = _make_store()
    state = store.load()
    assert state.revision == 0
    assert state.items == {}
    assert state.records == []
    assert state.quarantines == []


def test_save_increments_revision() -> None:
    store = _make_store()
    state = store.load()
    saved = store.save(state, expected_revision=0)
    assert saved.revision == 1


def test_concurrent_modification_raises() -> None:
    store = _make_store()
    state = store.load()
    store.save(state, expected_revision=0)
    with pytest.raises(ConcurrentModificationError):
        store.save(state, expected_revision=0)


def test_quarantine_blocks_save() -> None:
    store = _make_store()
    state = store.load()
    store.quarantine(state, reason="test", evidence="bad data")
    quarantined = store.load()
    with pytest.raises(QuarantineActiveError):
        store.save(quarantined, expected_revision=quarantined.revision)


def test_quarantine_raises_on_stale_revision() -> None:
    store = _make_store()
    state = store.load()
    store.save(state, expected_revision=0)
    with pytest.raises(ConcurrentModificationError):
        store.quarantine(state, reason="test", evidence="bad data")


def test_quarantine_increments_revision() -> None:
    store = _make_store()
    state = store.load()

    store.quarantine(state, reason="test", evidence="bad data")

    quarantined = store.load()
    assert quarantined.revision == 1
    assert len(quarantined.quarantines) == 1


def test_state_too_large_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cfg, "MAX_STATE_SIZE_BYTES", 1)
    store = _make_store()
    state = store.load()
    with pytest.raises(StateTooLargeError):
        store.save(state, expected_revision=0)


def test_save_rechecks_updated_payload_size(monkeypatch: pytest.MonkeyPatch) -> None:
    store = _make_store()
    state = store.load()
    payload = serialize_queue_document(asdict(state))
    monkeypatch.setattr(cfg, "MAX_STATE_SIZE_BYTES", len(payload))
    with pytest.raises(StateTooLargeError):
        store.save(state, expected_revision=0)


def test_save_returns_queuestate() -> None:
    store = _make_store()
    saved = store.save(store.load(), expected_revision=0)
    assert isinstance(saved, QueueState)


def test_transact_applies_transition_through_cas_boundary() -> None:
    store = _make_store()

    saved = store.transact(lambda state: state)

    assert saved.revision == 1


def test_transact_rejects_stale_expected_revision() -> None:
    store = _make_store()
    store.save(store.load(), expected_revision=0)

    with pytest.raises(ConcurrentModificationError):
        store.transact(lambda state: state, expected_revision=0)


def test_transact_rejects_non_queue_state_transition() -> None:
    store = _make_store()

    with pytest.raises(TypeError, match="must return QueueState"):
        store.transact(lambda _state: object())  # type: ignore[arg-type,return-value]


def test_save_thaws_nested_metric_attributes() -> None:
    store = _make_store()
    state = store.load()
    state.metric_events.append(
        create_metric_event(
            MetricEventType.DISCOVERY,
            "owner/repo",
            {"nested": {"values": [1, 2]}},
        )
    )

    saved = store.save(state, expected_revision=0)

    nested = saved.metric_events[0].attributes["nested"]
    assert isinstance(nested, Mapping)
    assert nested["values"] == (1, 2)


def test_save_rejects_foreign_repo_state() -> None:
    store = _make_store()
    state = store.load()
    state.repo = "other/repo"
    with pytest.raises(ValueError, match="expected repo"):
        store.save(state, expected_revision=0)


def test_save_rejects_leased_item_without_expiry() -> None:
    store = _make_store()
    state = store.load()
    state.items[1] = WorkItem(
        repo="owner/repo",
        pr_number=1,
        change_id="change-1",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.LEASED,
        claim_id="claim-1",
        lease_id="lease-1",
        operation_id="operation-1",
    )
    with pytest.raises(ValueError, match="lease_expires_at"):
        store.save(state, expected_revision=0)


def test_state_too_stale_is_available_for_recovery(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cfg, "MAX_STATE_AGE_SECONDS", 1)
    store = _make_store()
    state = store.load()
    saved = store.save(state, expected_revision=0)
    stale_time = datetime.now(UTC) - timedelta(seconds=100)
    saved.last_updated_at = stale_time
    store._store[("owner/repo", "ai-pr-loop-state")] = (saved.revision, saved)
    assert store.load().revision == saved.revision


def test_load_after_save_returns_state() -> None:
    """Load after save returns the saved state."""
    store = _make_store()
    state = store.load()
    saved = store.save(state, expected_revision=0)
    loaded = store.load()
    assert loaded.revision == saved.revision


def test_load_state_with_null_updated_at() -> None:
    """Load a stored state with last_updated_at=None returns it without error."""
    store = _make_store()
    state = store.load()
    saved = store.save(state, expected_revision=0)
    saved.last_updated_at = None
    store._store[("owner/repo", "ai-pr-loop-state")] = (saved.revision, saved)
    loaded = store.load()
    assert loaded.revision == saved.revision
    assert loaded.last_updated_at is None


def test_legacy_state_remains_mutable_without_new_mode_authority() -> None:
    store = _make_store()
    legacy = store.load()
    legacy.items[1] = WorkItem(
        repo="owner/repo",
        pr_number=1,
        change_id="change-1",
        eligibility="eligible",
        due_at=None,
        status=WorkItemStatus.QUEUED,
    )
    store._store[("owner/repo", "ai-pr-loop-state")] = (
        0,
        QueueState(
            repo="owner/repo",
            revision=0,
            items=legacy.items,
            records=[],
            quarantines=[],
            schema_version=3,
            migration_status="preactivation",
        ),
    )
    saved = store.save(store.load(), expected_revision=0)
    assert saved.revision == 1
    assert saved.migration_status == "preactivation"
    assert saved.pr_envelopes == {}


def test_load_invalid_entry_raises_state_decode_error() -> None:
    class _InvalidBacking:
        def load_entry(self, _key: tuple[str, str]) -> tuple[int, QueueState]:
            return (1, QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[]))

        def save_entry(self, _key: tuple[str, str], _expected_revision: int, _updated: QueueState) -> None:
            raise AssertionError("save_entry should not be called")

        def recovery_token(self, _key: tuple[str, str]) -> str | None:
            return None

        def save_recovery_entry(self, _key, _expected_token, _updated) -> None:
            raise AssertionError("save_recovery_entry should not be called")

    store = QueueStore(repo="owner/repo", backing=_InvalidBacking())

    with pytest.raises(StateDecodeError, match="Persisted revision 1"):
        store.load()


@pytest.mark.parametrize(
    ("revision", "state", "message"),
    [
        (True, QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[]), "must be an int"),
        (0, object(), "must be a QueueState"),
    ],
)
def test_load_rejects_invalid_entry_types(revision, state, message) -> None:
    class _InvalidBacking:
        def load_entry(self, _key):
            return revision, state

        def save_entry(self, _key, _expected_revision, _updated):
            raise AssertionError("save_entry should not be called")

        def recovery_token(self, _key):
            return None

        def save_recovery_entry(self, _key, _expected_token, _updated):
            raise AssertionError("save_recovery_entry should not be called")

    store = QueueStore(repo="owner/repo", backing=_InvalidBacking())

    with pytest.raises(StateDecodeError, match=message):
        store.load()


def test_load_rejects_invalid_state() -> None:
    class _InvalidBacking:
        def load_entry(self, _key):
            return 0, QueueState(repo="other/repo", revision=0, items={}, records=[], quarantines=[])

        def save_entry(self, _key, _expected_revision, _updated):
            raise AssertionError("save_entry should not be called")

        def recovery_token(self, _key):
            return None

        def save_recovery_entry(self, _key, _expected_token, _updated):
            raise AssertionError("save_recovery_entry should not be called")

    store = QueueStore(repo="owner/repo", backing=_InvalidBacking())

    with pytest.raises(StateDecodeError, match="Loaded queue state is invalid"):
        store.load()


def test_store_property_returns_empty_mapping_for_non_inmemory_backing() -> None:
    store = QueueStore(repo="owner/repo", backing=GitHubVariableBackingStore(repo="owner/repo"))

    assert store._store == {}


def test_ensure_state_ref_delegates_to_github_backing(monkeypatch: pytest.MonkeyPatch) -> None:
    backing = GitHubVariableBackingStore(repo="owner/repo")
    store = QueueStore(repo="owner/repo", backing=backing)
    calls: list[tuple[str, str]] = []

    def _create_ref(repo: str, state_ref: str) -> None:
        calls.append((repo, state_ref))

    monkeypatch.setattr(backing, "_create_state_ref", _create_ref)

    store.ensure_state_ref()

    assert calls == [("owner/repo", "ai-pr-loop-state")]


def test_ensure_state_ref_is_noop_for_inmemory_backing() -> None:
    _make_store().ensure_state_ref()


def test_recovery_save_uses_opaque_token() -> None:
    store = _make_store()
    state = store.save(store.load(), expected_revision=0)

    assert store.recovery_token() == "1"
    recovered = store.save_recovery(state, "1")

    assert recovered.revision == state.revision


def seeded_store(state):
    store = _make_store()
    store._store[(state.repo, state.state_ref)] = (state.revision, state)
    return store


def test_active_save_retains_all_history_and_cas(foundation):
    f = foundation((AttemptStatus.FAILED,) * 3 + (AttemptStatus.SUCCEEDED,), "reviewed")
    store = seeded_store(f.state)
    saved = store.save(f.state, f.state.revision)
    assert store.load() == saved
    assert saved.attempts == f.state.attempts
    assert saved.rounds == f.state.rounds
    with pytest.raises(ConcurrentModificationError):
        store.save(f.state, f.state.revision)


@pytest.mark.parametrize("field", ["evidence", "findings", "pr_envelopes", "obligations", "rounds", "attempts"])
def test_transition_rejects_history_deletion(foundation, field):
    f = foundation()
    updated = replace(f.state, **{field: {}})
    with pytest.raises(ValueError, match="history|identity"):
        QueueStore._validate_transition(f.state, updated)


@pytest.mark.parametrize(
    "field,value", [("migration_status", "prepared"), ("control_epoch", 2), ("inventory_invalidated", False)]
)
def test_active_transition_cannot_revert_epoch_or_write_legacy_state(foundation, field, value):
    f = foundation()
    with pytest.raises(MigrationRequiredError):
        QueueStore._validate_transition(f.state, replace(f.state, **{field: value}))


def test_migration_provenance_cannot_change(foundation):
    f = foundation()
    with pytest.raises(MigrationRequiredError, match="provenance"):
        QueueStore._validate_transition(f.state, replace(f.state, migration=None))


def test_preparation_binds_exact_source_and_activation(foundation):
    f = foundation(())
    current = QueueState("owner/repo", 0, {}, [], [])
    history = QueueState("owner/repo", 0, {}, [], [])
    source, historical = _legacy_digest(current), _history_digest(history)
    proof = f.proof(
        "migration", "inventory", pr_number=0, before=source, after=historical, source_revision="0", inventory=()
    )
    prepared = replace(
        current,
        migration_status="prepared",
        evidence={proof.evidence_id: proof},
        migration=MigrationRecord(0, 1, source, historical, proof.evidence_id),
    )
    store = _make_store()
    saved = store.save(prepared, 0)
    active = store.save(replace(saved, migration_status="active"), 1)
    assert active.migration_status == "active"
    assert active.migration == prepared.migration
    with pytest.raises(MigrationRequiredError, match="exact legacy source"):
        QueueStore._validate_transition(current, replace(prepared, migration=None))
    with pytest.raises(MigrationRequiredError, match="exact legacy source"):
        QueueStore._validate_transition(current, replace(prepared, migration_status="active"))


def test_prepared_legacy_save_allowed_but_activation_becomes_stale(foundation):
    f = foundation(())
    current = replace(f.state, migration_status="prepared")
    assert QueueStore._validate_transition(current, replace(current, inventory_invalidated=False)) is None
    with pytest.raises(MigrationRequiredError, match="history is immutable"):
        QueueStore._validate_transition(current, replace(current, findings={}))
    with pytest.raises(MigrationRequiredError, match="unchanged persisted"):
        QueueStore._validate_transition(current, replace(current, migration_status="active"))


@pytest.mark.parametrize("phase", ["prepublication", "invalidated", "published", "reviewed"])
def test_save_rejects_rewriting_every_admitted_batch_observation(foundation, phase):
    f = foundation((AttemptStatus.FAILED,), phase)
    observation = f.add(source_revision="new")
    batch = f.state.rounds["batch"]
    store = seeded_store(f.state)
    updated = replace(f.state, rounds={"batch": replace(batch, observation_id=observation)})
    with pytest.raises(ValueError):
        store.save(updated, f.state.revision)
    assert store.load().rounds["batch"].observation_id == batch.observation_id


@pytest.fixture
def admission_state(foundation):
    def build(status):
        f = foundation()
        request = PermitRequest(
            "request",
            f.state.repo,
            42,
            "problem",
            "batch",
            "worker",
            "github",
            "gpt-6-astra",
            1,
            f.now,
            f.now + timedelta(minutes=5),
            0,
            status=AdmissionRequestStatus(status),
            permit_id="permit",
        )
        acceptance = f.add("acceptance", "request", after=request.model, related_id="permit")
        permit = WorkerPermit(
            "permit",
            "request",
            f.state.repo,
            42,
            "problem",
            "batch",
            "worker",
            "github",
            request.model,
            1,
            f.now,
            request.deadline_at,
            status=PermitStatus(status),
            remote_task_id="task" if status == "accepted" else None,
            remote_session_id="session" if status == "accepted" else None,
            acceptance_evidence_id=acceptance if status == "accepted" else None,
        )
        f.state.permit_requests["request"] = request
        f.state.active_permits["permit"] = permit
        return f

    return build


@pytest.mark.parametrize("status", ["unknown", "accepted"])
@pytest.mark.parametrize("evidence_field", ["observation_id", "history_evidence_id"])
def test_direct_save_rejects_unrelated_release_evidence(admission_state, status, evidence_field):
    f = admission_state(status)
    store = seeded_store(f.state)
    evidence_id = getattr(f.state.pr_envelopes[42], evidence_field)
    updated = replace(
        f.state,
        permit_requests={
            "request": replace(
                f.state.permit_requests["request"],
                status=AdmissionRequestStatus.RELEASED,
                terminal_evidence_id=evidence_id,
            )
        },
        active_permits={
            "permit": replace(
                f.state.active_permits["permit"],
                status=PermitStatus.RELEASED,
                terminal_evidence_id=evidence_id,
            )
        },
    )
    with pytest.raises(ValueError, match="terminal evidence"):
        store.save(updated, f.state.revision)
    assert store.load() == f.state


@pytest.mark.parametrize("status", ["unknown", "accepted"])
@pytest.mark.parametrize("invalid", ["subject", "related_id", "kind", "outcome", "request_receipt"])
def test_direct_save_rejects_misbound_terminal_receipts(admission_state, status, invalid):
    f = admission_state(status)
    changes = dict(
        kind="absence" if status == "unknown" else "success",
        subject="request",
        related_id="permit",
        before="terminal",
        after="not_accepted",
    )
    changes.update(
        {
            "subject": {"subject": "other-request"},
            "related_id": {"related_id": "other-permit"},
            "kind": {"kind": "observation"},
            "outcome": {"after": "accepted"} if status == "unknown" else {"before": "running"},
            "request_receipt": {},
        }[invalid]
    )
    terminal = f.add(**changes)
    request_receipt = f.state.pr_envelopes[42].history_evidence_id if invalid == "request_receipt" else terminal
    store = seeded_store(f.state)
    updated = replace(
        f.state,
        permit_requests={
            "request": replace(
                f.state.permit_requests["request"],
                status=AdmissionRequestStatus.RELEASED,
                terminal_evidence_id=request_receipt,
            )
        },
        active_permits={
            "permit": replace(
                f.state.active_permits["permit"],
                status=PermitStatus.RELEASED,
                terminal_evidence_id=terminal,
            )
        },
    )
    with pytest.raises(ValueError, match="terminal evidence"):
        store.save(updated, f.state.revision)
    assert store.load() == f.state


@pytest.mark.parametrize("status,kind", [("unknown", "absence"), ("accepted", "success"), ("accepted", "failure")])
def test_direct_save_persists_bound_release_and_replay(admission_state, status, kind):
    f = admission_state(status)
    terminal = f.add(kind, "request", related_id="permit", before="terminal", after="not_accepted")
    store = seeded_store(f.state)
    updated = replace(
        f.state,
        permit_requests={
            "request": replace(
                f.state.permit_requests["request"],
                status=AdmissionRequestStatus.RELEASED,
                terminal_evidence_id=terminal,
            )
        },
        active_permits={
            "permit": replace(
                f.state.active_permits["permit"],
                status=PermitStatus.RELEASED,
                terminal_evidence_id=terminal,
            )
        },
    )
    saved = store.save(updated, f.state.revision)
    assert store.load() == saved
    assert store.save(saved, saved.revision).active_permits == saved.active_permits


@pytest.mark.parametrize("kind,model", [("observation", "gpt-6-astra"), ("acceptance", "other-model")])
def test_direct_save_rejects_wrong_acceptance_receipt(admission_state, kind, model):
    f = admission_state("unknown")
    receipt = f.add(kind, "request", after=model, related_id="permit")
    store = seeded_store(f.state)
    updated = replace(
        f.state,
        permit_requests={
            "request": replace(f.state.permit_requests["request"], status=AdmissionRequestStatus.ACCEPTED)
        },
        active_permits={
            "permit": replace(
                f.state.active_permits["permit"],
                status=PermitStatus.ACCEPTED,
                acceptance_evidence_id=receipt,
                remote_task_id="task",
                remote_session_id="session",
            )
        },
    )
    with pytest.raises(ValueError, match="acceptance evidence"):
        store.save(updated, f.state.revision)
    assert store.load() == f.state


def test_direct_save_persists_valid_acceptance_and_replay(admission_state):
    f = admission_state("unknown")
    receipt = f.add("acceptance", "request", after="gpt-6-astra", related_id="permit")
    store = seeded_store(f.state)
    updated = replace(
        f.state,
        permit_requests={
            "request": replace(f.state.permit_requests["request"], status=AdmissionRequestStatus.ACCEPTED)
        },
        active_permits={
            "permit": replace(
                f.state.active_permits["permit"],
                status=PermitStatus.ACCEPTED,
                acceptance_evidence_id=receipt,
                remote_task_id="task",
                remote_session_id="session",
            )
        },
    )
    saved = store.save(updated, f.state.revision)
    assert store.load() == saved
    assert store.save(saved, saved.revision).active_permits == saved.active_permits


@pytest.mark.parametrize("terminal", [None, "missing"])
def test_release_transition_rejects_missing_permit_evidence(admission_state, terminal):
    f = admission_state("unknown")
    updated = replace(
        f.state,
        active_permits={
            "permit": replace(
                f.state.active_permits["permit"],
                status=PermitStatus.RELEASED,
                terminal_evidence_id=terminal,
            )
        },
    )
    with pytest.raises(ValueError, match="released permit requires authoritative terminal evidence"):
        QueueStore._validate_transition(f.state, updated)


def test_transition_guards_shared_admission_identity_and_lifecycle(foundation):
    f = foundation()
    now = datetime.now(UTC)
    request = PermitRequest(
        "request",
        "owner/repo",
        42,
        "obligation",
        "batch",
        "worker",
        "github",
        "gpt-5.6-luna",
        1,
        now,
        now + timedelta(minutes=5),
        0,
        AdmissionRequestStatus.RESERVED,
        "permit",
    )
    permit = WorkerPermit(
        "permit",
        "request",
        "owner/repo",
        42,
        "obligation",
        "batch",
        "worker",
        "github",
        "gpt-5.6-luna",
        1,
        now,
        now + timedelta(minutes=5),
    )
    current = replace(f.state, permit_requests={"request": request}, active_permits={"permit": permit})
    with pytest.raises(ValueError, match="global admission epoch"):
        QueueStore._validate_transition(current, replace(current, global_epoch=2))
    with pytest.raises(ValueError, match="permit request history"):
        QueueStore._validate_transition(current, replace(current, permit_requests={}))
    with pytest.raises(ValueError, match="identity changed"):
        QueueStore._validate_transition(
            current,
            replace(current, permit_requests={"request": replace(request, worker_id="other-worker")}),
        )
    with pytest.raises(ValueError, match="permit request cannot rewind"):
        QueueStore._validate_transition(
            current,
            replace(current, permit_requests={"request": replace(request, status=AdmissionRequestStatus.QUEUED)}),
        )
    with pytest.raises(ValueError, match="released request requires"):
        QueueStore._validate_transition(
            replace(
                current,
                permit_requests={"request": replace(request, status=AdmissionRequestStatus.UNKNOWN)},
                active_permits={"permit": replace(permit, status=PermitStatus.UNKNOWN)},
            ),
            replace(
                current,
                permit_requests={"request": replace(request, status=AdmissionRequestStatus.RELEASED)},
            ),
        )
    with pytest.raises(ValueError, match="must be queued"):
        QueueStore._validate_transition(
            current,
            replace(
                current,
                permit_requests={
                    **current.permit_requests,
                    "new-request": replace(
                        request,
                        request_id="new-request",
                        status=AdmissionRequestStatus.RESERVED,
                    ),
                },
            ),
        )
    with pytest.raises(ValueError, match="permit identity"):
        QueueStore._validate_transition(current, replace(current, active_permits={}))
    with pytest.raises(ValueError, match="permit identity"):
        QueueStore._validate_transition(
            current,
            replace(current, active_permits={"permit": replace(permit, worker_id="other-worker")}),
        )
    with pytest.raises(ValueError, match="permit cannot rewind"):
        QueueStore._validate_transition(
            replace(current, active_permits={"permit": replace(permit, status=PermitStatus.UNKNOWN)}),
            replace(current, active_permits={"permit": replace(permit, status=PermitStatus.CANCELLED)}),
        )
    accepted = replace(permit, status=PermitStatus.ACCEPTED, remote_task_id="task", remote_session_id="session")
    accepted_state = replace(
        current,
        permit_requests={"request": replace(request, status=AdmissionRequestStatus.ACCEPTED)},
        active_permits={"permit": accepted},
    )
    with pytest.raises(ValueError, match="remote task"):
        QueueStore._validate_transition(
            accepted_state,
            replace(accepted_state, active_permits={"permit": replace(accepted, remote_task_id="other-task")}),
        )
    with pytest.raises(ValueError, match="accepted permit requires"):
        QueueStore._validate_transition(
            replace(
                current,
                permit_requests={"request": replace(request, status=AdmissionRequestStatus.UNKNOWN)},
                active_permits={"permit": replace(permit, status=PermitStatus.UNKNOWN)},
            ),
            replace(
                current,
                permit_requests={"request": replace(request, status=AdmissionRequestStatus.ACCEPTED)},
                active_permits={"permit": replace(permit, status=PermitStatus.ACCEPTED)},
            ),
        )
    with pytest.raises(ValueError, match="released request requires"):
        terminal_evidence = next(iter(current.evidence))
        QueueStore._validate_transition(
            replace(
                current,
                permit_requests={"request": replace(request, status=AdmissionRequestStatus.UNKNOWN)},
                active_permits={"permit": replace(permit, status=PermitStatus.UNKNOWN)},
            ),
            replace(
                current,
                permit_requests={
                    "request": replace(
                        request,
                        status=AdmissionRequestStatus.RELEASED,
                        terminal_evidence_id=terminal_evidence,
                    )
                },
                active_permits={"permit": replace(permit, status=PermitStatus.RELEASED)},
            ),
        )
    receipt_id = next(iter(current.evidence))
    with pytest.raises(ValueError, match="request terminal evidence"):
        QueueStore._validate_transition(
            replace(
                current,
                permit_requests={
                    "request": replace(
                        request,
                        status=AdmissionRequestStatus.UNKNOWN,
                        terminal_evidence_id=receipt_id,
                    )
                },
                active_permits={"permit": replace(permit, status=PermitStatus.UNKNOWN)},
            ),
            replace(
                current,
                permit_requests={"request": replace(request, status=AdmissionRequestStatus.UNKNOWN)},
                active_permits={"permit": replace(permit, status=PermitStatus.UNKNOWN)},
            ),
        )
    with pytest.raises(ValueError, match="acceptance evidence is immutable"):
        QueueStore._validate_transition(
            replace(
                current,
                permit_requests={"request": replace(request, status=AdmissionRequestStatus.UNKNOWN)},
                active_permits={
                    "permit": replace(
                        permit,
                        status=PermitStatus.UNKNOWN,
                        acceptance_evidence_id=receipt_id,
                    )
                },
            ),
            replace(
                current,
                permit_requests={"request": replace(request, status=AdmissionRequestStatus.UNKNOWN)},
                active_permits={
                    "permit": replace(
                        permit,
                        status=PermitStatus.UNKNOWN,
                        acceptance_evidence_id="other",
                    )
                },
            ),
        )
    with pytest.raises(ValueError, match="permit terminal evidence is immutable"):
        QueueStore._validate_transition(
            replace(
                current,
                permit_requests={"request": replace(request, status=AdmissionRequestStatus.UNKNOWN)},
                active_permits={
                    "permit": replace(
                        permit,
                        status=PermitStatus.UNKNOWN,
                        terminal_evidence_id=receipt_id,
                    )
                },
            ),
            replace(
                current,
                permit_requests={"request": replace(request, status=AdmissionRequestStatus.UNKNOWN)},
                active_permits={
                    "permit": replace(
                        permit,
                        status=PermitStatus.UNKNOWN,
                        terminal_evidence_id="other",
                    )
                },
            ),
        )
    with pytest.raises(ValueError, match="remote session"):
        QueueStore._validate_transition(
            accepted_state,
            replace(accepted_state, active_permits={"permit": replace(accepted, remote_session_id="other-session")}),
        )
    with pytest.raises(ValueError, match="persist reservation"):
        QueueStore._validate_transition(
            current,
            replace(
                current,
                active_permits={
                    **current.active_permits,
                    "new-permit": replace(
                        permit,
                        permit_id="new-permit",
                        request_id="new-request",
                        status=PermitStatus.ACCEPTED,
                    ),
                },
            ),
        )


@pytest.mark.parametrize(
    "old_phase,new_phase",
    [
        ("prepublication", "published"),
        ("prepublication", "invalidated"),
        ("published", "reviewed"),
        ("published", "invalidated"),
    ],
)
def test_batch_boundaries_are_forward_only(foundation, old_phase, new_phase):
    f = foundation((AttemptStatus.FAILED,), old_phase)
    batch = f.state.rounds["batch"]
    updated = replace(f.state, rounds={"batch": replace(batch, phase=new_phase)})
    assert QueueStore._validate_transition(f.state, updated) is None
    with pytest.raises(ValueError, match="cannot rewind"):
        QueueStore._validate_transition(updated, f.state)


@pytest.mark.parametrize(
    "status", [AttemptStatus.UNKNOWN, AttemptStatus.ACCEPTED, AttemptStatus.FAILED, AttemptStatus.SUCCEEDED]
)
def test_save_rejects_rebinding_unknown_or_accepted_authority(foundation, status):
    f = foundation((status,))
    observation = f.add(source_revision="new")
    f.state.pr_envelopes[42] = replace(f.state.pr_envelopes[42], observation_id=observation)
    attempt = f.state.attempts["attempt-0"]
    store = seeded_store(f.state)
    updated = replace(f.state, attempts={"attempt-0": replace(attempt, observation_id=observation)})
    with pytest.raises(ValueError):
        store.save(updated, f.state.revision)
    assert store.load().attempts["attempt-0"] == attempt


def test_save_renews_only_active_known_unaccepted_authority(foundation):
    f = foundation((AttemptStatus.FAILED, AttemptStatus.AUTHORIZED))
    observation = f.add(source_revision="new")
    f.state.pr_envelopes[42] = replace(f.state.pr_envelopes[42], observation_id=observation)
    store = seeded_store(f.state)
    updated = replace(
        f.state,
        attempts={
            **f.state.attempts,
            "attempt-1": replace(f.state.attempts["attempt-1"], observation_id=observation),
        },
    )
    saved = store.save(updated, f.state.revision)
    assert store.load() == saved
    assert saved.rounds == f.state.rounds
    assert saved.attempts["attempt-0"] == f.state.attempts["attempt-0"]
    assert saved.obligations == f.state.obligations


@pytest.mark.parametrize("invalid", ["inactive", "historical", "unpersisted_observation", "invalidated"])
def test_renewal_cannot_rebind_inactive_or_unpersisted_authority(foundation, invalid):
    f = foundation()
    observation = f.add(source_revision="new")
    if invalid != "unpersisted_observation":
        f.state.pr_envelopes[42] = replace(f.state.pr_envelopes[42], observation_id=observation)
    if invalid == "inactive":
        f.state.pr_envelopes[42] = replace(f.state.pr_envelopes[42], active_batch_id=None)
    if invalid == "historical":
        f.state.pr_envelopes[42] = replace(f.state.pr_envelopes[42], active_batch_id="other")
    if invalid == "invalidated":
        f.state.rounds["batch"] = replace(f.state.rounds["batch"], phase="invalidated")
    updated = replace(
        f.state,
        attempts={
            "attempt-0": replace(f.state.attempts["attempt-0"], observation_id=observation),
        },
    )
    with pytest.raises(ValueError, match="authorized work|renewal requires"):
        QueueStore._validate_transition(f.state, updated)


def test_replan_save_retains_original_batch_and_attempt_history(foundation):
    f = foundation((AttemptStatus.FAILED, AttemptStatus.AUTHORIZED), "invalidated")
    observation = f.add(head_sha="d" * 40)
    envelope = replace(f.state.pr_envelopes[42], observation_id=observation, head_sha="d" * 40)
    f.state.pr_envelopes[42] = envelope
    batch = RepairRound("new", 42, 2, "problem", observation, "replan", "batch")
    updated = replace(
        f.state,
        rounds={**f.state.rounds, "new": batch},
        attempts={
            **f.state.attempts,
            "attempt-1": replace(f.state.attempts["attempt-1"], batch_id="new", observation_id=observation),
        },
        pr_envelopes={42: replace(envelope, rounds_used=2, round_ids=("batch", "new"), active_batch_id="new")},
    )
    store = seeded_store(f.state)
    saved = store.save(updated, f.state.revision)
    assert store.load() == saved
    assert saved.attempts["attempt-0"] == f.state.attempts["attempt-0"]
    assert saved.rounds["batch"] == f.state.rounds["batch"]
    with pytest.raises(ValueError, match="admitted batch"):
        store.save(
            replace(
                saved, rounds={**saved.rounds, "batch": replace(saved.rounds["batch"], observation_id=observation)}
            ),
            saved.revision,
        )
    assert store.load().rounds["batch"] == f.state.rounds["batch"]


def test_rebinding_to_existing_or_unjustified_batch_is_rejected(foundation):
    f = foundation(phase="invalidated", round_count=2)
    observation = f.add(head_sha="d" * 40)
    f.state.pr_envelopes[42] = replace(
        f.state.pr_envelopes[42], active_batch_id="batch", observation_id=observation, head_sha="d" * 40
    )
    updated = replace(
        f.state,
        attempts={
            "attempt-0": replace(f.state.attempts["attempt-0"], batch_id="batch-2", observation_id=observation),
        },
        pr_envelopes={42: replace(f.state.pr_envelopes[42], active_batch_id="batch-2")},
    )
    with pytest.raises(ValueError, match="new bounded batch"):
        QueueStore._validate_transition(f.state, updated)
    f = foundation(phase="invalidated")
    updated = replace(
        f.state,
        rounds={
            **f.state.rounds,
            "new": RepairRound(
                "new",
                42,
                2,
                "problem",
                f.state.rounds["batch"].observation_id,
                "replan",
                "batch",
            ),
        },
    )
    with pytest.raises(ValueError, match="retained known-unaccepted"):
        QueueStore._validate_transition(f.state, updated)


def test_unknown_reopening_requires_new_absence_not_timeout_or_replay(foundation):
    f = foundation((AttemptStatus.UNKNOWN,))
    attempt = f.state.attempts["attempt-0"]
    reopened = replace(f.state, attempts={"attempt-0": replace(attempt, status=AttemptStatus.AUTHORIZED)})
    with pytest.raises(ValueError, match="independently verified absence"):
        QueueStore._validate_transition(f.state, reopened)
    proof = f.proof("absence", "attempt-0", related_id=attempt.observation_id, after="not_accepted")
    updated = replace(reopened, evidence={**f.state.evidence, proof.evidence_id: proof})
    store = seeded_store(f.state)
    assert store.save(updated, f.state.revision).attempts["attempt-0"].status == AttemptStatus.AUTHORIZED
    f.state.evidence[proof.evidence_id] = proof
    with pytest.raises(ValueError, match="independently verified absence"):
        QueueStore._validate_transition(f.state, updated)


def test_attempt_status_and_receipts_cannot_rewind(foundation):
    f = foundation((AttemptStatus.FAILED,))
    attempt = f.state.attempts["attempt-0"]
    with pytest.raises(ValueError, match="cannot rewind"):
        QueueStore._validate_transition(
            f.state,
            replace(
                f.state,
                attempts={
                    "attempt-0": replace(attempt, status=AttemptStatus.ACCEPTED),
                },
            ),
        )
    with pytest.raises(ValueError, match="persist attempt authorization"):
        QueueStore._validate_transition(
            f.state,
            replace(
                f.state,
                attempts={
                    **f.state.attempts,
                    "new": replace(attempt, attempt_id="new"),
                },
            ),
        )
    with pytest.raises(ValueError, match="persist round admission"):
        QueueStore._validate_transition(
            f.state,
            replace(
                f.state,
                rounds={
                    **f.state.rounds,
                    "new": replace(f.state.rounds["batch"], batch_id="new", phase="published"),
                },
            ),
        )


def test_recovery_cannot_erase_readable_foundation(foundation):
    f = foundation()
    store = seeded_store(f.state)
    with pytest.raises(MigrationRequiredError, match="cannot assert"):
        store.save_recovery(f.state, str(f.state.revision))
    legacy = QueueState("owner/repo", f.state.revision, {}, [], [])
    with pytest.raises(MigrationRequiredError, match="cannot erase"):
        store.save_recovery(legacy, str(f.state.revision))


def test_recovery_of_corrupt_source_uses_backing_token(monkeypatch):
    store = _make_store()
    legacy = QueueState("owner/repo", 0, {}, [], [])
    store._store[("owner/repo", "ai-pr-loop-state")] = (0, legacy)

    def corrupt(_key):
        raise StateDecodeError("corrupt")

    monkeypatch.setattr(store._backing, "load_entry", corrupt)
    saved = store.save_recovery(legacy, "0")
    assert saved.migration_status == "preactivation"
    assert saved.last_updated_at is not None


def test_renewal_transition_rejects_changed_scope_even_before_structural_validation(foundation):
    f = foundation()
    observation = f.add(head_sha="d" * 40)
    f.state.pr_envelopes[42] = replace(f.state.pr_envelopes[42], head_sha="d" * 40, observation_id=observation)
    updated = replace(
        f.state,
        attempts={
            "attempt-0": replace(f.state.attempts["attempt-0"], observation_id=observation),
        },
    )
    with pytest.raises(ValueError, match="renewal requires"):
        QueueStore._validate_transition(f.state, updated)


def test_wp1c_epoch_and_effect_transition_guards(foundation):
    f = foundation()
    with pytest.raises(ValueError, match="revert or skip"):
        QueueStore._validate_transition(f.state, replace(f.state, global_epoch=3))
    with pytest.raises(ValueError, match="requires advance_epoch"):
        QueueStore._validate_transition(f.state, replace(f.state, global_epoch=2))
    controller = AdmissionController(42, f.state.repo, 1)
    epoch_state = replace(f.state, controllers={42: controller})
    with pytest.raises(ValueError, match="refresh controller"):
        QueueStore._validate_transition(
            epoch_state,
            replace(epoch_state, global_epoch=2, audit_refs=("epoch:2",)),
        )
    QueueStore._validate_transition(
        epoch_state,
        replace(
            epoch_state, global_epoch=2, audit_refs=("epoch:2",), controllers={42: replace(controller, global_epoch=2)}
        ),
    )
    effect = EffectRecord("effect", f.state.repo, 42, "comment", "digest")
    current = replace(f.state, effects={"effect": effect})
    QueueStore._validate_transition(current, current)
    with pytest.raises(ValueError, match="cannot be deleted"):
        QueueStore._validate_transition(current, f.state)
    with pytest.raises(ValueError, match="intent changed"):
        QueueStore._validate_transition(current, replace(current, effects={"effect": replace(effect, kind="other")}))
    settled = replace(effect, status=EffectStatus.SETTLED)
    with pytest.raises(ValueError, match="cannot rewind"):
        QueueStore._validate_transition(
            replace(current, effects={"effect": settled}),
            current,
        )
    with pytest.raises(ValueError, match="before settlement"):
        QueueStore._validate_transition(f.state, replace(f.state, effects={"effect": settled}))
