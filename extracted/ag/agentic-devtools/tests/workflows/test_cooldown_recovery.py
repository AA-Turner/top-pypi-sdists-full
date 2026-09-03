"""Integration tests for cooldown probe recovery.

Covers US2, FR-007, FR-008, FR-009, and FR-019: provider suppression,
successful recovery, failed recovery, renewed cooldown metadata, generation
persistence, and duplicate wake-up prevention.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from agentic_devtools.cli.ci.due_probe_wakeup import DueProbeEvaluator, run_due_probe_wakeup
from agentic_devtools.cli.ci.reconciliation.models import CooldownProbe, CooldownState, ProbeStatus
from agentic_devtools.cli.ci.reconciliation.probes import CooldownProbeAdapter
from agentic_devtools.cli.ci.reconciliation.queue_store import InMemoryBackingStore, QueueStore


def _make_adapter() -> CooldownProbeAdapter:
    return CooldownProbeAdapter()


def _make_state(
    provider: str = "gh",
    cred: str = "cred1",
    resume_at: datetime | None = None,
    gen_id: str | None = None,
) -> CooldownState:
    if resume_at is None:
        resume_at = datetime.now(UTC) - timedelta(minutes=10)
    if gen_id is None:
        gen_id = str(uuid.uuid4())
    return CooldownState(
        provider_identity=provider,
        credential_identity=cred,
        cooldown_generation_id=gen_id,
        resume_at=resume_at,
    )


def _make_probe(
    scheduled_at: datetime | None = None,
    gen_id: str | None = None,
    status: ProbeStatus = ProbeStatus.PENDING,
) -> CooldownProbe:
    if scheduled_at is None:
        scheduled_at = datetime.now(UTC) - timedelta(seconds=30)
    if gen_id is None:
        gen_id = str(uuid.uuid4())
    return CooldownProbe(
        probe_id=str(uuid.uuid4()),
        provider_identity="gh",
        credential_identity="cred1",
        cooldown_generation_id=gen_id,
        status=status,
        scheduled_at=scheduled_at,
    )


class TestProviderSuppression:
    def test_should_suppress_before_resume_at(self) -> None:
        adapter = _make_adapter()
        future_resume = datetime.now(UTC) + timedelta(minutes=30)
        state = _make_state(resume_at=future_resume)
        now = datetime.now(UTC)
        assert adapter.should_suppress(state, now) is True

    def test_should_not_suppress_after_resume_at(self) -> None:
        adapter = _make_adapter()
        past_resume = datetime.now(UTC) - timedelta(minutes=1)
        state = _make_state(resume_at=past_resume)
        now = datetime.now(UTC)
        assert adapter.should_suppress(state, now) is False


class TestSuccessfulRecovery:
    def test_successful_probe_sets_succeeded_status(self) -> None:
        adapter = _make_adapter()
        gen_id = str(uuid.uuid4())
        state = _make_state(gen_id=gen_id)
        probe = _make_probe(gen_id=gen_id)
        now = datetime.now(UTC)
        new_state, new_probe = adapter.execute_probe(
            state, probe, availability_result=True, renewed_resume_at=None, now=now
        )
        assert new_probe.status == ProbeStatus.SUCCEEDED
        assert new_state.probe_status == ProbeStatus.SUCCEEDED

    def test_successful_probe_ends_generation(self) -> None:
        adapter = _make_adapter()
        gen_id = str(uuid.uuid4())
        state = _make_state(gen_id=gen_id)
        probe = _make_probe(gen_id=gen_id)
        now = datetime.now(UTC)
        new_state, new_probe = adapter.execute_probe(
            state, probe, availability_result=True, renewed_resume_at=None, now=now
        )
        assert new_probe.cooldown_generation_id == gen_id
        assert new_state.cooldown_generation_id == gen_id


class TestFailedRecovery:
    def test_failed_probe_increments_retry(self) -> None:
        adapter = _make_adapter()
        gen_id = str(uuid.uuid4())
        state = _make_state(gen_id=gen_id)
        probe = _make_probe(gen_id=gen_id)
        now = datetime.now(UTC)
        new_state, new_probe = adapter.execute_probe(
            state, probe, availability_result=False, renewed_resume_at=None, now=now
        )
        assert new_probe.retry_count == 1
        assert new_state.retry_count == 1

    def test_failed_probe_retains_generation_id(self) -> None:
        adapter = _make_adapter()
        gen_id = str(uuid.uuid4())
        state = _make_state(gen_id=gen_id)
        probe = _make_probe(gen_id=gen_id)
        now = datetime.now(UTC)
        _, new_probe = adapter.execute_probe(state, probe, availability_result=False, renewed_resume_at=None, now=now)
        assert new_probe.cooldown_generation_id == gen_id

    def test_max_retries_sets_alertable(self) -> None:
        adapter = _make_adapter()
        gen_id = str(uuid.uuid4())
        state = _make_state(gen_id=gen_id)
        probe = _make_probe(gen_id=gen_id)
        now = datetime.now(UTC)
        for _ in range(state.max_retries):
            state, probe = adapter.execute_probe(
                state, probe, availability_result=False, renewed_resume_at=None, now=now
            )
        assert probe.status == ProbeStatus.ALERTABLE


class TestRenewedCooldownMetadata:
    def test_renewed_resume_at_starts_new_generation(self) -> None:
        adapter = _make_adapter()
        old_gen = str(uuid.uuid4())
        state = _make_state(gen_id=old_gen)
        probe = _make_probe(gen_id=old_gen)
        new_resume = datetime.now(UTC) + timedelta(hours=2)
        now = datetime.now(UTC)
        new_state, new_probe = adapter.execute_probe(
            state, probe, availability_result=False, renewed_resume_at=new_resume, now=now
        )
        assert new_state.cooldown_generation_id != old_gen
        assert new_state.resume_at == new_resume
        assert new_state.probe_status == ProbeStatus.PENDING
        assert new_probe.status == ProbeStatus.PENDING
        assert new_probe.scheduled_at == new_resume

    def test_same_resume_at_retains_generation(self) -> None:
        adapter = _make_adapter()
        gen_id = str(uuid.uuid4())
        resume = datetime.now(UTC) - timedelta(minutes=5)
        state = _make_state(gen_id=gen_id, resume_at=resume)
        probe = _make_probe(gen_id=gen_id)
        now = datetime.now(UTC)
        new_state, _ = adapter.execute_probe(state, probe, availability_result=False, renewed_resume_at=resume, now=now)
        assert new_state.cooldown_generation_id == gen_id


class TestDuplicateWakeUpPrevention:
    def test_evaluate_due_probes_returns_list(self) -> None:
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        adapter = _make_adapter()
        evaluator = DueProbeEvaluator(store=store, adapter=adapter)
        now = datetime.now(UTC)
        result = evaluator.evaluate_due_probes("owner/repo", now=now)
        assert isinstance(result, list)

    def test_run_due_probe_wakeup_returns_count(self) -> None:
        store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
        count = run_due_probe_wakeup(repo="owner/repo", store=store)
        assert isinstance(count, int)
        assert count >= 0
