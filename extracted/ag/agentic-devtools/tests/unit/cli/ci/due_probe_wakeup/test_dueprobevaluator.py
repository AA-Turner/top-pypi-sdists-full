"""Tests for DueProbeEvaluator."""

from __future__ import annotations

import uuid
from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.due_probe_wakeup import DueProbeEvaluator, _build_availability_checker
from agentic_devtools.cli.ci.reconciliation.models import CooldownProbe, ProbeStatus
from agentic_devtools.cli.ci.reconciliation.probes import CooldownProbeAdapter
from agentic_devtools.cli.ci.reconciliation.queue_store import (
    ConcurrentModificationError,
    InMemoryBackingStore,
    QueueStore,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


def _make_store(repo: str = "owner/repo") -> QueueStore:
    return QueueStore(repo=repo, backing=InMemoryBackingStore())


def _make_probe(
    *,
    scheduled_at: datetime,
    status: ProbeStatus = ProbeStatus.PENDING,
    provider_identity: str = "gh",
    credential_identity: str = "cred1",
    resume_at: datetime | None = None,
    next_probe_at: datetime | None = None,
) -> CooldownProbe:
    return CooldownProbe(
        probe_id=str(uuid.uuid4()),
        provider_identity=provider_identity,
        credential_identity=credential_identity,
        cooldown_generation_id="gen1",
        status=status,
        scheduled_at=scheduled_at,
        resume_at=resume_at,
        next_probe_at=next_probe_at,
    )


def _save_probes(store: QueueStore, probes: list[CooldownProbe]) -> None:
    state = store.load()
    state.probes = probes
    store.save(state, expected_revision=state.revision)


def test_evaluate_due_probes_returns_empty_list() -> None:
    store = _make_store()
    evaluator = DueProbeEvaluator(store=store, adapter=CooldownProbeAdapter())

    assert evaluator.evaluate_due_probes("owner/repo") == []


def test_evaluate_due_probes_naive_now_raises() -> None:
    store = _make_store()
    evaluator = DueProbeEvaluator(store=store, adapter=CooldownProbeAdapter())

    with pytest.raises(ValueError, match="timezone"):
        evaluator.evaluate_due_probes("owner/repo", now=datetime(2024, 1, 1))


def test_evaluate_due_probes_repo_mismatch_logs(caplog: pytest.LogCaptureFixture) -> None:
    store = _make_store("repo-a")
    evaluator = DueProbeEvaluator(store=store, adapter=CooldownProbeAdapter())

    with caplog.at_level("WARNING"):
        probes = evaluator.evaluate_due_probes("repo-b")

    assert probes == []
    assert "Loaded queue state" in caplog.text


def test_evaluate_due_probes_skips_missing_probe_after_reload(monkeypatch: pytest.MonkeyPatch) -> None:
    store = _make_store()
    now = datetime.now(UTC)
    probe = _make_probe(scheduled_at=now - timedelta(minutes=1))
    _save_probes(store, [probe])
    evaluator = DueProbeEvaluator(store=store, adapter=CooldownProbeAdapter())
    monkeypatch.setattr(
        evaluator,
        "claim_and_execute_probe",
        lambda *_args: (_ for _ in ()).throw(ConcurrentModificationError("missing")),
    )

    assert evaluator.evaluate_due_probes("owner/repo", now=now) == []


def test_claim_and_execute_probe_raises_when_probe_missing() -> None:
    evaluator = DueProbeEvaluator(store=_make_store(), adapter=CooldownProbeAdapter())
    probe = _make_probe(scheduled_at=datetime.now(UTC) - timedelta(minutes=1))
    with pytest.raises(ConcurrentModificationError, match="was not found"):
        evaluator.claim_and_execute_probe("owner/repo", probe, datetime.now(UTC))


def test_claim_and_execute_probe_raises_when_requested_probe_is_not_in_state() -> None:
    store = _make_store()
    now = datetime.now(UTC)
    stored_probe = _make_probe(scheduled_at=now - timedelta(minutes=1))
    requested_probe = _make_probe(scheduled_at=now - timedelta(minutes=1))
    _save_probes(store, [stored_probe])
    evaluator = DueProbeEvaluator(store=store, adapter=CooldownProbeAdapter())

    with pytest.raises(ConcurrentModificationError, match="was not found"):
        evaluator.claim_and_execute_probe("owner/repo", requested_probe, now)


def test_evaluate_due_probes_executes_pending_probe_and_persists_success() -> None:
    store = _make_store()
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    _save_probes(store, [_make_probe(scheduled_at=now - timedelta(minutes=1))])
    evaluator = DueProbeEvaluator(store=store, adapter=CooldownProbeAdapter())

    probes = evaluator.evaluate_due_probes("owner/repo", now=now)

    assert len(probes) == 1
    assert probes[0].status == ProbeStatus.SUCCEEDED
    reloaded = store.load()
    assert reloaded.probes[0].status == ProbeStatus.SUCCEEDED
    assert reloaded.revision == 3


def test_claim_and_execute_probe_uses_availability_checker_and_persists_failure() -> None:
    store = _make_store()
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    resume_at = now - timedelta(minutes=10)
    probe = _make_probe(scheduled_at=now - timedelta(minutes=1), resume_at=resume_at)
    _save_probes(store, [probe])
    evaluator = DueProbeEvaluator(
        store=store,
        adapter=CooldownProbeAdapter(),
        availability_checker=lambda _probe: False,
    )

    result = evaluator.claim_and_execute_probe("owner/repo", probe, now)

    assert result.status == ProbeStatus.FAILED
    assert result.attempted_at == now
    assert result.retry_count == 1
    assert result.next_probe_at is not None
    assert store.load().probes[0] == result


def test_claim_and_execute_probe_accepts_renewed_cooldown_metadata() -> None:
    store = _make_store()
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    probe = _make_probe(scheduled_at=now - timedelta(minutes=1), resume_at=now - timedelta(minutes=10))
    _save_probes(store, [probe])
    renewed_resume_at = now + timedelta(minutes=10)
    evaluator = DueProbeEvaluator(
        store=store,
        adapter=CooldownProbeAdapter(),
        availability_checker=lambda _probe: (False, renewed_resume_at),
    )

    result = evaluator.claim_and_execute_probe("owner/repo", probe, now)

    assert result.status == ProbeStatus.PENDING
    assert result.resume_at == renewed_resume_at


def test_claim_and_execute_probe_falls_back_to_failure_when_checker_raises() -> None:
    store = _make_store()
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    probe = _make_probe(scheduled_at=now - timedelta(minutes=1), resume_at=now - timedelta(minutes=10))
    _save_probes(store, [probe])
    evaluator = DueProbeEvaluator(
        store=store,
        adapter=CooldownProbeAdapter(),
        availability_checker=lambda _probe: (_ for _ in ()).throw(RuntimeError("provider down")),
    )

    result = evaluator.claim_and_execute_probe("owner/repo", probe, now)

    assert result.status == ProbeStatus.FAILED
    assert result.retry_count == 1
    assert result.next_probe_at is not None
    assert store.load().probes[0] == result


def test_claim_and_execute_probe_persists_failed_probe_when_adapter_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    store = _make_store()
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    probe = _make_probe(scheduled_at=now - timedelta(minutes=1), resume_at=now - timedelta(minutes=10))
    _save_probes(store, [probe])
    adapter = CooldownProbeAdapter()
    evaluator = DueProbeEvaluator(store=store, adapter=adapter, availability_checker=lambda _probe: True)
    monkeypatch.setattr(adapter, "execute_probe", lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("boom")))

    result = evaluator.claim_and_execute_probe("owner/repo", probe, now)

    assert result.status == ProbeStatus.FAILED
    assert result.alert_reason.startswith("probe_execution_failed:")
    assert "boom" in result.alert_reason
    assert store.load().probes[0] == result


def test_claim_and_execute_probe_reclaims_stale_claim() -> None:
    store = _make_store()
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    probe = _make_probe(
        scheduled_at=now - timedelta(minutes=1),
        status=ProbeStatus.IN_PROGRESS,
    )
    probe = replace(probe, claim_expires_at=now - timedelta(seconds=1))
    _save_probes(store, [probe])
    evaluator = DueProbeEvaluator(store=store, adapter=CooldownProbeAdapter(), availability_checker=lambda _: True)

    result = evaluator.claim_and_execute_probe("owner/repo", probe, now)

    assert result.status == ProbeStatus.SUCCEEDED
    assert result.claim_expires_at is None


def test_claim_and_execute_probe_raises_for_unexpired_active_claim() -> None:
    store = _make_store()
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    probe = _make_probe(
        scheduled_at=now - timedelta(minutes=1),
        status=ProbeStatus.IN_PROGRESS,
    )
    probe = replace(probe, claim_expires_at=now + timedelta(minutes=3))
    _save_probes(store, [probe])
    evaluator = DueProbeEvaluator(store=store, adapter=CooldownProbeAdapter(), availability_checker=lambda _: True)

    with pytest.raises(ConcurrentModificationError, match="unexpired active claim"):
        evaluator.claim_and_execute_probe("owner/repo", probe, now)


def test_claim_and_execute_probe_uses_type_only_when_adapter_error_message_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = _make_store()
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    probe = _make_probe(scheduled_at=now - timedelta(minutes=1), resume_at=now - timedelta(minutes=10))
    _save_probes(store, [probe])
    adapter = CooldownProbeAdapter()
    evaluator = DueProbeEvaluator(store=store, adapter=adapter, availability_checker=lambda _probe: True)
    monkeypatch.setattr(adapter, "execute_probe", lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError()))

    result = evaluator.claim_and_execute_probe("owner/repo", probe, now)

    assert result.status == ProbeStatus.FAILED
    assert result.alert_reason == "probe_execution_failed:RuntimeError"


def test_claim_and_execute_probe_rejects_probe_that_is_no_longer_due() -> None:
    store = _make_store()
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    probe = _make_probe(scheduled_at=now + timedelta(minutes=1))
    _save_probes(store, [probe])
    evaluator = DueProbeEvaluator(store=store, adapter=CooldownProbeAdapter())

    with pytest.raises(ConcurrentModificationError, match="no longer due"):
        evaluator.claim_and_execute_probe("owner/repo", probe, now)


def test_claim_and_execute_probe_rejects_repo_mismatch() -> None:
    store = _make_store("repo-a")
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    probe = _make_probe(scheduled_at=now - timedelta(minutes=1))
    _save_probes(store, [probe])
    evaluator = DueProbeEvaluator(store=store, adapter=CooldownProbeAdapter())

    with pytest.raises(ConcurrentModificationError, match="repo-a"):
        evaluator.claim_and_execute_probe("repo-b", probe, now)


def test_evaluate_due_probes_skips_concurrent_modification(monkeypatch: pytest.MonkeyPatch) -> None:
    store = _make_store()
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    _save_probes(store, [_make_probe(scheduled_at=now - timedelta(minutes=1))])
    evaluator = DueProbeEvaluator(store=store, adapter=CooldownProbeAdapter())

    def _claim_and_execute(_repo: str, _probe: CooldownProbe, _current: datetime) -> CooldownProbe:
        raise ConcurrentModificationError("claimed elsewhere")

    monkeypatch.setattr(evaluator, "claim_and_execute_probe", _claim_and_execute)

    assert evaluator.evaluate_due_probes("owner/repo", now=now) == []


def test_evaluate_due_probes_skips_failed_probe_without_next_probe_at() -> None:
    store = _make_store()
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    _save_probes(store, [_make_probe(scheduled_at=now - timedelta(days=1), status=ProbeStatus.FAILED)])
    evaluator = DueProbeEvaluator(store=store, adapter=CooldownProbeAdapter())

    assert evaluator.evaluate_due_probes("owner/repo", now=now) == []


def test_evaluate_due_probes_executes_failed_probe_when_next_probe_is_due() -> None:
    store = _make_store()
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    probe = _make_probe(
        scheduled_at=now - timedelta(days=1),
        status=ProbeStatus.FAILED,
        resume_at=now - timedelta(minutes=10),
        next_probe_at=now - timedelta(minutes=1),
    )
    _save_probes(store, [probe])
    evaluator = DueProbeEvaluator(store=store, adapter=CooldownProbeAdapter())

    probes = evaluator.evaluate_due_probes("owner/repo", now=now)

    assert len(probes) == 1
    assert probes[0].status == ProbeStatus.SUCCEEDED


def test_build_availability_checker_caches_true_result(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = {"count": 0}
    monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "token")

    def _fake_gh_api(_endpoint: str, token: str | None = None) -> str:
        calls["count"] += 1
        return "[]"

    monkeypatch.setattr(
        "agentic_devtools.cli.ci.due_probe_wakeup._gh_api",
        _fake_gh_api,
    )
    checker = _build_availability_checker("owner/repo")
    probe = _make_probe(scheduled_at=datetime.now(UTC), credential_identity="COPILOT_GITHUB_TOKEN")

    assert checker(probe) is True
    assert checker(probe) is True
    assert calls["count"] == 1


def test_build_availability_checker_retries_after_provider_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = {"count": 0}
    monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "token")

    def _fake_gh_api(_endpoint: str, token: str | None = None) -> str:
        assert token == "token"
        calls["count"] += 1
        if calls["count"] == 1:
            raise RuntimeError("offline")
        return "[]"

    monkeypatch.setattr("agentic_devtools.cli.ci.due_probe_wakeup._gh_api", _fake_gh_api)
    checker = _build_availability_checker("owner/repo")
    probe = _make_probe(scheduled_at=datetime.now(UTC), credential_identity="COPILOT_GITHUB_TOKEN")

    assert checker(probe) is False
    assert checker(probe) is True
    assert calls["count"] == 2


def test_build_availability_checker_preserves_rate_limit_resume_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "token")
    reset_timestamp = datetime.now(UTC).timestamp() + 120

    def _fake_gh_api(_endpoint: str, token: str | None = None) -> str:
        assert token == "token"
        raise ProviderRateLimitError(reset_timestamp=reset_timestamp)

    monkeypatch.setattr("agentic_devtools.cli.ci.due_probe_wakeup._gh_api", _fake_gh_api)
    checker = _build_availability_checker("owner/repo")
    probe = _make_probe(scheduled_at=datetime.now(UTC), credential_identity="COPILOT_GITHUB_TOKEN")

    result = checker(probe)

    assert isinstance(result, tuple)
    available, renewed_resume_at = result
    assert available is False
    assert renewed_resume_at is not None
    assert renewed_resume_at.timestamp() >= reset_timestamp


def test_build_availability_checker_rejects_unsupported_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    called = {"value": False}

    def _fake_gh_api(_endpoint: str, token: str | None = None) -> str:
        called["value"] = True
        return "[]"

    monkeypatch.setattr(
        "agentic_devtools.cli.ci.due_probe_wakeup._gh_api",
        _fake_gh_api,
    )
    checker = _build_availability_checker("owner/repo")
    probe = _make_probe(
        scheduled_at=datetime.now(UTC),
        provider_identity="ado",
        credential_identity="COPILOT_GITHUB_TOKEN",
    )

    assert checker(probe) is False
    assert called["value"] is False


def test_build_availability_checker_rejects_missing_credential_env(monkeypatch: pytest.MonkeyPatch) -> None:
    called = {"value": False}

    def _fake_gh_api(_endpoint: str, token: str | None = None) -> str:
        called["value"] = True
        return "[]"

    monkeypatch.setattr(
        "agentic_devtools.cli.ci.due_probe_wakeup._gh_api",
        _fake_gh_api,
    )
    checker = _build_availability_checker("owner/repo")
    probe = _make_probe(
        scheduled_at=datetime.now(UTC),
        provider_identity="gh",
        credential_identity="COPILOT_GITHUB_TOKEN",
    )

    assert checker(probe) is False
    assert called["value"] is False


def test_build_availability_checker_uses_gh_token_alias_for_configured_identity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = {"count": 0}
    monkeypatch.setenv("AI_PR_LOOP_CREDENTIAL_IDENTITY", "SPECKIT_PR_TOKEN")
    monkeypatch.setenv("GH_TOKEN", "gh-token")

    def _fake_gh_api(_endpoint: str, token: str | None = None) -> str:
        calls["count"] += 1
        assert token == "gh-token"
        return "[]"

    monkeypatch.setattr("agentic_devtools.cli.ci.due_probe_wakeup._gh_api", _fake_gh_api)
    checker = _build_availability_checker("owner/repo")
    probe = _make_probe(scheduled_at=datetime.now(UTC), credential_identity="SPECKIT_PR_TOKEN")

    assert checker(probe) is True
    assert calls["count"] == 1


def test_build_availability_checker_preserves_rate_limit_metadata_from_retryable_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "token")
    reset_timestamp = datetime.now(UTC).timestamp() + 90

    def _fake_gh_api(_endpoint: str, token: str | None = None) -> str:
        assert token == "token"
        raise RetryableError(
            "rate limited",
            reset_timestamp=reset_timestamp,
            provider="github",
            credential_identity="COPILOT_GITHUB_TOKEN",
            is_rate_limit=True,
        )

    monkeypatch.setattr("agentic_devtools.cli.ci.due_probe_wakeup._gh_api", _fake_gh_api)
    checker = _build_availability_checker("owner/repo")
    probe = _make_probe(scheduled_at=datetime.now(UTC), credential_identity="COPILOT_GITHUB_TOKEN")

    result = checker(probe)

    assert isinstance(result, tuple)
    available, renewed_resume_at = result
    assert available is False
    assert renewed_resume_at is not None
    assert renewed_resume_at.timestamp() >= reset_timestamp


def test_build_availability_checker_handles_non_rate_limit_retryable_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "token")

    def _fake_gh_api(_endpoint: str, token: str | None = None) -> str:
        assert token == "token"
        raise RetryableError("transient outage", is_rate_limit=False)

    monkeypatch.setattr("agentic_devtools.cli.ci.due_probe_wakeup._gh_api", _fake_gh_api)
    checker = _build_availability_checker("owner/repo")
    probe = _make_probe(scheduled_at=datetime.now(UTC), credential_identity="COPILOT_GITHUB_TOKEN")

    assert checker(probe) is False
