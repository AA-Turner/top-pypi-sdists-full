"""Tests for cooldown probe state machine."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

import pytest

import agentic_devtools.cli.ci.reconciliation.config as cfg
from agentic_devtools.cli.ci.reconciliation.models import (
    CooldownProbe,
    CooldownState,
    ProbeStatus,
)
from agentic_devtools.cli.ci.reconciliation.probes import CooldownProbeAdapter


def _make_state(
    resume_at: datetime,
    retry_count: int = 0,
    max_retries: int = 3,
    gen_id: str = "gen1",
) -> CooldownState:
    return CooldownState(
        provider_identity="gh",
        credential_identity="cred1",
        cooldown_generation_id=gen_id,
        resume_at=resume_at,
        retry_count=retry_count,
        max_retries=max_retries,
    )


def _make_probe(
    scheduled_at: datetime,
    status: ProbeStatus = ProbeStatus.PENDING,
    retry_count: int = 0,
    *,
    provider_identity: str = "gh",
    credential_identity: str = "cred1",
    gen_id: str = "gen1",
) -> CooldownProbe:
    return CooldownProbe(
        probe_id=str(uuid.uuid4()),
        provider_identity=provider_identity,
        credential_identity=credential_identity,
        cooldown_generation_id=gen_id,
        status=status,
        scheduled_at=scheduled_at,
        retry_count=retry_count,
    )


def test_probe_suppressed_before_resume_at() -> None:
    now = datetime.now(UTC)
    adapter = CooldownProbeAdapter()
    assert adapter.should_suppress(_make_state(now + timedelta(minutes=10)), now) is True


def test_initial_probe_exactly_once() -> None:
    now = datetime.now(UTC)
    adapter = CooldownProbeAdapter()
    assert adapter.should_suppress(_make_state(now - timedelta(minutes=1)), now) is False


def test_failed_probe_schedules_retry() -> None:
    now = datetime.now(UTC)
    resume_at = now - timedelta(minutes=1)
    state = _make_state(resume_at)
    probe = _make_probe(scheduled_at=now)
    adapter = CooldownProbeAdapter()
    new_state, new_probe = adapter.execute_probe(state, probe, False, None, now=now)
    assert new_state.retry_count == 1
    assert new_probe.next_probe_at is not None
    assert new_probe.next_probe_at > resume_at + timedelta(minutes=5)


def test_retry_retains_generation() -> None:
    now = datetime.now(UTC)
    gen_id = str(uuid.uuid4())
    state = CooldownState(
        provider_identity="gh",
        credential_identity="cred1",
        cooldown_generation_id=gen_id,
        resume_at=now - timedelta(minutes=1),
        retry_count=0,
        max_retries=3,
    )
    probe = _make_probe(scheduled_at=now, gen_id=gen_id)
    adapter = CooldownProbeAdapter()
    new_state, new_probe = adapter.execute_probe(state, probe, False, None, now=now)
    assert new_state.cooldown_generation_id == gen_id
    assert new_probe.cooldown_generation_id == gen_id


def test_new_resume_at_starts_new_generation() -> None:
    now = datetime.now(UTC)
    old_gen = str(uuid.uuid4())
    state = CooldownState(
        provider_identity="gh",
        credential_identity="cred1",
        cooldown_generation_id=old_gen,
        resume_at=now - timedelta(minutes=1),
        retry_count=0,
        max_retries=3,
    )
    probe = _make_probe(scheduled_at=now, gen_id=old_gen)
    new_resume_at = now + timedelta(hours=1)
    adapter = CooldownProbeAdapter()
    new_state, new_probe = adapter.execute_probe(
        state,
        probe,
        False,
        new_resume_at,
        now=now,
    )
    assert new_state.cooldown_generation_id != old_gen
    assert new_state.probe_status == ProbeStatus.PENDING
    assert new_state.retry_count == 0
    assert new_state.next_probe_at is None
    assert new_probe.cooldown_generation_id == new_state.cooldown_generation_id
    assert new_probe.status == ProbeStatus.PENDING
    assert new_probe.retry_count == 0
    assert new_probe.scheduled_at == new_resume_at
    assert new_probe.resume_at == new_resume_at
    assert new_probe.probe_id != probe.probe_id


def test_successful_probe_ends_generation() -> None:
    now = datetime.now(UTC)
    state = _make_state(now - timedelta(minutes=1))
    probe = _make_probe(scheduled_at=now)
    adapter = CooldownProbeAdapter()
    new_state, new_probe = adapter.execute_probe(state, probe, True, None, now=now)
    assert new_state.probe_status == ProbeStatus.SUCCEEDED
    assert new_probe.status == ProbeStatus.SUCCEEDED


def test_probe_retry_bounded() -> None:
    now = datetime.now(UTC)
    state = _make_state(now - timedelta(minutes=1), retry_count=2, max_retries=3)
    probe = _make_probe(scheduled_at=now, retry_count=2)
    adapter = CooldownProbeAdapter()
    new_state, new_probe = adapter.execute_probe(state, probe, False, None, now=now)
    assert new_state.retry_count == 3
    assert new_probe.status == ProbeStatus.ALERTABLE


def test_failed_probe_retry_anchor_uses_late_execution_time() -> None:
    now = datetime.now(UTC)
    resume_at = now - timedelta(minutes=30)
    state = _make_state(resume_at)
    probe = _make_probe(scheduled_at=resume_at)
    adapter = CooldownProbeAdapter()
    new_state, new_probe = adapter.execute_probe(state, probe, False, None, now=now)
    expected_next_probe_at = now + timedelta(minutes=5)
    assert new_state.next_probe_at == expected_next_probe_at
    assert new_probe.next_probe_at == expected_next_probe_at


def test_failed_probe_becomes_alertable_when_retry_exceeds_max_failure_duration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = datetime.now(UTC)
    resume_at = now - timedelta(minutes=1)
    state = _make_state(resume_at, max_retries=99)
    probe = _make_probe(scheduled_at=resume_at)
    adapter = CooldownProbeAdapter()
    monkeypatch.setattr(cfg, "MAX_PROVIDER_FAILURE_DURATION", 60)

    new_state, new_probe = adapter.execute_probe(state, probe, False, None, now=now)

    assert new_state.probe_status == ProbeStatus.ALERTABLE
    assert new_state.next_probe_at is None
    assert new_probe.status == ProbeStatus.ALERTABLE
    assert new_probe.next_probe_at is None


def test_is_due_naive_now_raises() -> None:
    adapter = CooldownProbeAdapter()
    now = datetime.now(UTC)
    probe = _make_probe(scheduled_at=now)
    with pytest.raises(ValueError, match="timezone"):
        adapter.is_due(probe, datetime(2024, 1, 1))


def test_should_suppress_naive_now_raises() -> None:
    adapter = CooldownProbeAdapter()
    now = datetime.now(UTC)
    state = _make_state(resume_at=now)
    with pytest.raises(ValueError, match="timezone"):
        adapter.should_suppress(state, datetime(2024, 1, 1))


def test_generate_probe_id_returns_string() -> None:
    adapter = CooldownProbeAdapter()
    probe_id = adapter.generate_probe_id()
    assert isinstance(probe_id, str)
    assert len(probe_id) > 0


def test_generate_generation_id_returns_string() -> None:
    adapter = CooldownProbeAdapter()
    gen_id = adapter.generate_generation_id()
    assert isinstance(gen_id, str)
    assert len(gen_id) > 0


def test_is_due_returns_true_when_scheduled_in_past() -> None:
    adapter = CooldownProbeAdapter()
    now = datetime.now(UTC)
    probe = _make_probe(scheduled_at=now - timedelta(minutes=1))
    assert adapter.is_due(probe, now) is True


def test_is_due_returns_false_when_scheduled_in_future() -> None:
    adapter = CooldownProbeAdapter()
    now = datetime.now(UTC)
    probe = _make_probe(scheduled_at=now + timedelta(minutes=1))
    assert adapter.is_due(probe, now) is False


def test_is_due_failed_probe_uses_next_probe_at() -> None:
    adapter = CooldownProbeAdapter()
    now = datetime.now(UTC)
    probe = _make_probe(
        scheduled_at=now - timedelta(hours=1),
        status=ProbeStatus.FAILED,
    )
    probe = CooldownProbe(
        probe_id=probe.probe_id,
        provider_identity=probe.provider_identity,
        credential_identity=probe.credential_identity,
        cooldown_generation_id=probe.cooldown_generation_id,
        status=probe.status,
        scheduled_at=probe.scheduled_at,
        next_probe_at=now + timedelta(minutes=1),
    )
    assert adapter.is_due(probe, now) is False
    assert adapter.is_due(probe, now + timedelta(minutes=2)) is True


def test_is_due_non_pending_probe_statuses_return_false() -> None:
    adapter = CooldownProbeAdapter()
    now = datetime.now(UTC)
    in_progress_probe = _make_probe(
        scheduled_at=now - timedelta(minutes=10),
        status=ProbeStatus.IN_PROGRESS,
    )
    alertable_probe = _make_probe(
        scheduled_at=now - timedelta(minutes=10),
        status=ProbeStatus.ALERTABLE,
    )
    succeeded_probe = _make_probe(
        scheduled_at=now - timedelta(minutes=10),
        status=ProbeStatus.SUCCEEDED,
    )
    assert adapter.is_due(in_progress_probe, now) is False
    assert adapter.is_due(alertable_probe, now) is False
    assert adapter.is_due(succeeded_probe, now) is False


def test_execute_probe_default_now() -> None:
    """execute_probe with now=None uses datetime.now(UTC)."""
    resume_at = datetime.now(UTC) - timedelta(minutes=1)
    state = _make_state(resume_at)
    probe = _make_probe(scheduled_at=datetime.now(UTC) - timedelta(minutes=1))
    adapter = CooldownProbeAdapter()
    new_state, new_probe = adapter.execute_probe(state, probe, True, None)
    assert new_probe.status == ProbeStatus.SUCCEEDED


def test_execute_probe_naive_now_raises() -> None:
    resume_at = datetime.now(UTC) - timedelta(minutes=1)
    state = _make_state(resume_at)
    probe = _make_probe(scheduled_at=datetime.now(UTC))
    adapter = CooldownProbeAdapter()
    with pytest.raises(ValueError, match="timezone"):
        adapter.execute_probe(state, probe, True, None, now=datetime(2024, 1, 1))


def test_execute_probe_naive_renewed_resume_at_raises() -> None:
    now = datetime.now(UTC)
    state = _make_state(now - timedelta(minutes=1))
    probe = _make_probe(scheduled_at=now)
    adapter = CooldownProbeAdapter()
    with pytest.raises(ValueError, match="timezone"):
        adapter.execute_probe(state, probe, True, datetime(2024, 2, 1), now=now)


def test_execute_probe_rejects_provider_identity_mismatch() -> None:
    now = datetime.now(UTC)
    state = _make_state(now - timedelta(minutes=1))
    probe = _make_probe(provider_identity="other-provider", scheduled_at=now)
    adapter = CooldownProbeAdapter()
    with pytest.raises(ValueError, match="provider_identity"):
        adapter.execute_probe(state, probe, True, None, now=now)


def test_execute_probe_rejects_credential_identity_mismatch() -> None:
    now = datetime.now(UTC)
    state = _make_state(now - timedelta(minutes=1))
    probe = _make_probe(credential_identity="other-credential", scheduled_at=now)
    adapter = CooldownProbeAdapter()
    with pytest.raises(ValueError, match="credential_identity"):
        adapter.execute_probe(state, probe, True, None, now=now)


def test_execute_probe_rejects_generation_mismatch() -> None:
    now = datetime.now(UTC)
    state = _make_state(now - timedelta(minutes=1))
    probe = _make_probe(gen_id="older-generation", scheduled_at=now)
    adapter = CooldownProbeAdapter()
    with pytest.raises(ValueError, match="cooldown_generation_id"):
        adapter.execute_probe(state, probe, True, None, now=now)
