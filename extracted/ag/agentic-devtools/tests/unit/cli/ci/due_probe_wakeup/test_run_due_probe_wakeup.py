"""Tests for run_due_probe_wakeup()."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

import pytest

import agentic_devtools.cli.ci.reconciliation.config as cfg
from agentic_devtools.cli.ci.due_probe_wakeup import run_due_probe_wakeup
from agentic_devtools.cli.ci.reconciliation.models import CooldownProbe, CooldownState, ProbeStatus
from agentic_devtools.cli.ci.reconciliation.queue_store import InMemoryBackingStore, QueueStore


def _make_probe(*, scheduled_at: datetime, status: ProbeStatus = ProbeStatus.PENDING) -> CooldownProbe:
    return CooldownProbe(
        probe_id=str(uuid.uuid4()),
        provider_identity="gh",
        credential_identity="cred1",
        cooldown_generation_id="gen1",
        status=status,
        scheduled_at=scheduled_at,
        resume_at=scheduled_at,
        next_probe_at=scheduled_at if status == ProbeStatus.FAILED else None,
    )


def _make_store(repo: str = "owner/repo") -> QueueStore:
    return QueueStore(repo=repo, backing=InMemoryBackingStore())


def _save_probe(store: QueueStore, probe: CooldownProbe) -> None:
    state = store.load()
    state.probes.append(probe)
    store.save(state, expected_revision=state.revision)


def test_returns_int() -> None:
    count = run_due_probe_wakeup("owner/repo", store=QueueStore(repo="owner/repo", backing=InMemoryBackingStore()))
    assert isinstance(count, int)
    assert count == 0


def test_returns_zero_with_explicit_store() -> None:
    store = _make_store()
    count = run_due_probe_wakeup("owner/repo", store=store)
    assert count == 0


def test_creates_default_store_when_not_provided(monkeypatch: pytest.MonkeyPatch) -> None:
    store = _make_store()
    monkeypatch.setattr("agentic_devtools.cli.ci.due_probe_wakeup.QueueStore", lambda repo: store)
    assert run_due_probe_wakeup("owner/repo") == 0


def test_repo_mismatch_does_not_mutate_foreign_probes() -> None:
    past = datetime(2024, 1, 1, tzinfo=UTC)
    probe = _make_probe(scheduled_at=past)
    store = QueueStore(repo="repo-a", backing=InMemoryBackingStore())
    _save_probe(store, probe)

    count = run_due_probe_wakeup("repo-b", store=store)

    assert count == 0
    assert store.load().probes[0].status == ProbeStatus.PENDING


def test_returns_due_count_and_persists_probe_success() -> None:
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    probe = _make_probe(scheduled_at=now - timedelta(minutes=1))
    store = _make_store()
    _save_probe(store, probe)
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(
            "agentic_devtools.cli.ci.due_probe_wakeup._build_availability_checker",
            lambda _repo: lambda _probe: True,
        )
        count = run_due_probe_wakeup(repo="owner/repo", store=store)

    assert count == 1
    reloaded = store.load()
    assert reloaded.probes[0].status == ProbeStatus.SUCCEEDED
    assert reloaded.probes[0].attempted_at is not None


def test_returns_due_count_for_failed_probe_with_due_retry() -> None:
    now = datetime.now(UTC)
    probe = _make_probe(scheduled_at=now - timedelta(minutes=2), status=ProbeStatus.FAILED)
    store = _make_store()
    _save_probe(store, probe)
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(
            "agentic_devtools.cli.ci.due_probe_wakeup._build_availability_checker",
            lambda _repo: lambda _probe: True,
        )
        assert run_due_probe_wakeup(repo="owner/repo", store=store) == 1


def test_persists_initial_probe_for_cooldown_state() -> None:
    resume_at = datetime.now(UTC) + timedelta(minutes=5)
    store = _make_store()
    cooldown = CooldownState("gh", "cred1", "generation-1", resume_at)

    assert run_due_probe_wakeup("owner/repo", store=store, cooldown_state=cooldown) == 0

    probes = store.load().probes
    assert len(probes) == 1
    assert probes[0].cooldown_generation_id == "generation-1"
    assert probes[0].scheduled_at == resume_at
    assert run_due_probe_wakeup("owner/repo", store=store, cooldown_state=cooldown) == 0


def test_disabled_feature_flag_returns_zero(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cfg, "ENABLE_DUE_PROBE_WAKEUP", False)
    store = _make_store()
    assert run_due_probe_wakeup("owner/repo", store=store) == 0
