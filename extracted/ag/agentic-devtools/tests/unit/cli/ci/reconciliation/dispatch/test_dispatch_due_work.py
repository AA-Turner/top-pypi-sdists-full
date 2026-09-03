"""Tests for dispatch_due_work()."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.reconciliation import dispatch as dispatch_module
from agentic_devtools.cli.ci.reconciliation.dispatch import (
    DispatchConflictError,
    dispatch_due_work,
)
from agentic_devtools.cli.ci.reconciliation.models import DispatchEligibility, QueueState, WorkItem, WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.queue_store import InMemoryBackingStore, QueueStore
from agentic_devtools.orchestration.safety.operation_id import compute_operation_id
from agentic_devtools.orchestration.safety.operation_log import OperationLog, OperationLogRecord


def _make_item(pr_number: int, *, now: datetime) -> WorkItem:
    return WorkItem(pr_number, "o/r", f"c-{pr_number}", "eligible", now - timedelta(seconds=1), WorkItemStatus.QUEUED)


def test_dispatch_due_work_claims_and_leases_after_live_preflight() -> None:
    now = datetime.now(UTC)
    item = _make_item(1, now=now)
    state = QueueState("o/r", 0, {1: item}, [], [])
    result = dispatch_due_work(state, eligibility_checker=lambda _: True, preflight_checker=lambda _: True, now=now)
    assert result.lease is not None
    assert result.state is not None
    assert result.state.items[1].status == WorkItemStatus.LEASED


def test_dispatch_due_work_rejects_failed_preflight() -> None:
    now = datetime.now(UTC)
    item = WorkItem(1, "o/r", "c", "eligible", now, WorkItemStatus.QUEUED)
    result = dispatch_due_work(
        QueueState("o/r", 0, {1: item}, [], []),
        eligibility_checker=lambda _: True,
        preflight_checker=lambda _: False,
        now=now,
    )
    assert result.lease is None
    assert result.eligibility.eligibility_reason == "no_due_work"
    assert result.state is not None
    assert result.state.items[1].due_at is not None
    assert result.state.items[1].due_at > now


def test_dispatch_due_work_skips_failed_preflight_and_dispatches_next() -> None:
    now = datetime.now(UTC)
    item1 = _make_item(1, now=now)
    item2 = _make_item(2, now=now)
    state = QueueState("o/r", 0, {1: item1, 2: item2}, [], [])
    result = dispatch_due_work(
        state,
        eligibility_checker=lambda _: True,
        preflight_checker=lambda item: item.pr_number != 1,
        now=now,
    )
    assert result.lease is not None
    assert result.lease.pr_number == 2


def test_dispatch_due_work_returns_unknown_when_live_eligibility_is_unknown() -> None:
    now = datetime.now(UTC)
    item = _make_item(1, now=now)
    state = QueueState("o/r", 0, {1: item}, [], [])

    result = dispatch_due_work(
        state,
        eligibility_checker=lambda _: None,
        preflight_checker=lambda _: True,
        now=now,
    )

    assert result.lease is None
    assert result.eligibility.eligibility_reason == "live_eligibility_unknown"
    assert result.eligibility.pr_number == 1


def test_dispatch_due_work_returns_unknown_when_preflight_is_unknown() -> None:
    now = datetime.now(UTC)
    item = _make_item(1, now=now)
    state = QueueState("o/r", 0, {1: item}, [], [])

    result = dispatch_due_work(
        state,
        eligibility_checker=lambda _: True,
        preflight_checker=lambda _: None,
        now=now,
    )

    assert result.lease is None
    assert result.eligibility.eligibility_reason == "preflight_unknown"
    assert result.eligibility.pr_number == 1


def test_dispatch_due_work_skips_unknown_preflight_and_dispatches_next() -> None:
    now = datetime.now(UTC)
    state = QueueState("o/r", 0, {1: _make_item(1, now=now), 2: _make_item(2, now=now)}, [], [])

    result = dispatch_due_work(
        state,
        eligibility_checker=lambda _: True,
        preflight_checker=lambda item: None if item.pr_number == 1 else True,
        now=now,
    )

    assert result.lease is not None
    assert result.lease.pr_number == 2


def test_dispatch_due_work_skips_failed_eligibility_and_dispatches_next() -> None:
    now = datetime.now(UTC)
    item1 = _make_item(1, now=now)
    item2 = _make_item(2, now=now)
    state = QueueState("o/r", 0, {1: item1, 2: item2}, [], [])
    result = dispatch_due_work(
        state,
        eligibility_checker=lambda item: item.pr_number != 1,
        preflight_checker=lambda _: True,
        now=now,
    )
    assert result.lease is not None
    assert result.lease.pr_number == 2


def test_dispatch_due_work_defers_failed_eligibility_with_store() -> None:
    now = datetime.now(UTC)
    backing = InMemoryBackingStore()
    store = QueueStore(repo="o/r", backing=backing)
    state = store.load()
    state.items[1] = _make_item(1, now=now)
    persisted = store.save(state, expected_revision=state.revision)

    result = dispatch_due_work(
        persisted,
        eligibility_checker=lambda _: False,
        preflight_checker=lambda _: True,
        now=now,
        store=store,
    )

    assert result.lease is None
    reloaded = store.load()
    assert reloaded.items[1].due_at is not None
    assert reloaded.items[1].due_at > now


def test_dispatch_due_work_reloads_on_defer_save_conflict_for_eligibility(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = datetime.now(UTC)
    backing = InMemoryBackingStore()
    store = QueueStore(repo="o/r", backing=backing)
    state = store.load()
    state.items[1] = _make_item(1, now=now)
    persisted = store.save(state, expected_revision=state.revision)

    def _save(_state: QueueState, *, expected_revision: int) -> QueueState:
        _ = expected_revision
        raise dispatch_module.ConcurrentModificationError("conflict")

    monkeypatch.setattr(store, "save", _save)

    result = dispatch_due_work(
        persisted,
        eligibility_checker=lambda _: False,
        preflight_checker=lambda _: True,
        now=now,
        store=store,
    )

    assert result.lease is None
    assert result.state is not None


def test_dispatch_due_work_reloads_on_defer_save_conflict_for_preflight(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = datetime.now(UTC)
    backing = InMemoryBackingStore()
    store = QueueStore(repo="o/r", backing=backing)
    state = store.load()
    state.items[1] = _make_item(1, now=now)
    persisted = store.save(state, expected_revision=state.revision)

    def _save(_state: QueueState, *, expected_revision: int) -> QueueState:
        _ = expected_revision
        raise dispatch_module.ConcurrentModificationError("conflict")

    monkeypatch.setattr(store, "save", _save)

    result = dispatch_due_work(
        persisted,
        eligibility_checker=lambda _: True,
        preflight_checker=lambda _: False,
        now=now,
        store=store,
    )

    assert result.lease is None
    assert result.state is not None


def test_dispatch_due_work_rejects_missing_live_checks() -> None:
    now = datetime.now(UTC)
    item = _make_item(1, now=now)
    state = QueueState("o/r", 0, {1: item}, [], [])
    result = dispatch_due_work(state, now=now)
    assert result.lease is None
    assert result.eligibility.eligibility_reason == "live_checks_unavailable"
    assert result.state is state


def test_dispatch_due_work_returns_no_due_work_before_live_checks() -> None:
    now = datetime.now(UTC)
    state = QueueState("o/r", 0, {}, [], [])

    result = dispatch_due_work(state, now=now)

    assert result.lease is None
    assert result.eligibility.eligibility_reason == "no_due_work"
    assert result.state is state


def test_dispatch_due_work_rejects_naive_now() -> None:
    state = QueueState("o/r", 0, {}, [], [])
    with pytest.raises(ValueError, match="timezone"):
        dispatch_due_work(state, now=datetime(2026, 1, 1))


def test_dispatch_due_work_skips_candidate_missing_from_current_state(monkeypatch: pytest.MonkeyPatch) -> None:
    now = datetime.now(UTC)
    item = _make_item(1, now=now)
    state = QueueState("o/r", 0, {1: item}, [], [])
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.reconciliation.dispatch.select_due_work",
        lambda *_args: [item],
    )
    state.items.clear()
    result = dispatch_due_work(state, eligibility_checker=lambda _: True, preflight_checker=lambda _: True, now=now)
    assert result.lease is None


def test_dispatch_due_work_continues_when_static_eligibility_check_turns_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = datetime.now(UTC)
    item1 = _make_item(1, now=now)
    item2 = _make_item(2, now=now)
    state = QueueState("o/r", 0, {1: item1, 2: item2}, [], [])

    def _evaluate(item: WorkItem, _now: datetime) -> DispatchEligibility:
        return DispatchEligibility(
            pr_number=item.pr_number,
            repo=item.repo,
            is_eligible=item.pr_number == 2,
            eligibility_reason="" if item.pr_number == 2 else "ineligible",
            evaluated_at=_now,
            is_due=True,
            due_reason="due",
        )

    monkeypatch.setattr("agentic_devtools.cli.ci.reconciliation.dispatch.evaluate_dispatch_eligibility", _evaluate)
    result = dispatch_due_work(
        state,
        eligibility_checker=lambda _: True,
        preflight_checker=lambda _: True,
        now=now,
    )
    assert result.lease is not None
    assert result.lease.pr_number == 2


def test_dispatch_due_work_retries_next_item_after_claim_conflict(monkeypatch: pytest.MonkeyPatch) -> None:
    now = datetime.now(UTC)
    item1 = _make_item(1, now=now)
    item2 = _make_item(2, now=now)
    state = QueueState("o/r", 0, {1: item1, 2: item2}, [], [])
    seen: list[int] = []
    original = dispatch_module.acquire_dispatch_claim

    def _claim(current_state: QueueState, pr_number: int, operation_id: str):
        seen.append(pr_number)
        if pr_number == 1:
            raise DispatchConflictError("claimed elsewhere")
        return original(current_state, pr_number, operation_id)

    monkeypatch.setattr("agentic_devtools.cli.ci.reconciliation.dispatch.acquire_dispatch_claim", _claim)
    result = dispatch_due_work(
        state,
        eligibility_checker=lambda _: True,
        preflight_checker=lambda _: True,
        now=now,
    )
    assert seen == [1, 2]
    assert result.lease is not None
    assert result.lease.pr_number == 2


def test_dispatch_due_work_reloads_store_after_claim_conflict(monkeypatch: pytest.MonkeyPatch) -> None:
    now = datetime.now(UTC)
    item = _make_item(1, now=now)
    backing = InMemoryBackingStore()
    store = QueueStore(repo="o/r", backing=backing)
    state = store.load()
    state.items[1] = item
    persisted = store.save(state, expected_revision=0)
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.reconciliation.dispatch.acquire_dispatch_claim",
        lambda *_args: (_ for _ in ()).throw(DispatchConflictError("claimed elsewhere")),
    )

    result = dispatch_due_work(
        persisted,
        eligibility_checker=lambda _: True,
        preflight_checker=lambda _: True,
        now=now,
        store=store,
    )
    assert result.lease is None
    assert result.state is not None


def test_dispatch_due_work_persists_leased_state_when_store_is_provided() -> None:
    now = datetime.now(UTC)
    backing = InMemoryBackingStore()
    store = QueueStore(repo="o/r", backing=backing)
    state = store.load()
    state.items[1] = _make_item(1, now=now)
    persisted = store.save(state, expected_revision=state.revision)

    result = dispatch_due_work(
        persisted,
        eligibility_checker=lambda _: True,
        preflight_checker=lambda _: True,
        now=now,
        store=store,
    )

    assert result.lease is not None
    assert result.state is not None
    assert result.state.revision == persisted.revision + 1
    assert store.load().items[1].status == WorkItemStatus.LEASED


def test_dispatch_due_work_continues_after_save_conflict(monkeypatch: pytest.MonkeyPatch) -> None:
    now = datetime.now(UTC)
    backing = InMemoryBackingStore()
    store = QueueStore(repo="o/r", backing=backing)
    state = store.load()
    state.items[1] = _make_item(1, now=now)
    state.items[2] = _make_item(2, now=now)
    persisted = store.save(state, expected_revision=state.revision)
    competing_store = QueueStore(repo="o/r", backing=backing)
    real_save = store.save
    calls = 0

    def _save(current_state: QueueState, expected_revision: int) -> QueueState:
        nonlocal calls
        calls += 1
        if calls == 1:
            competing_state = competing_store.load()
            competing_state.items[99] = WorkItem(
                99,
                "o/r",
                str(uuid.uuid4()),
                "eligible",
                now + timedelta(minutes=1),
                WorkItemStatus.QUEUED,
            )
            competing_store.save(competing_state, expected_revision=competing_state.revision)
        return real_save(current_state, expected_revision)

    monkeypatch.setattr(store, "save", _save)

    result = dispatch_due_work(
        persisted,
        eligibility_checker=lambda _: True,
        preflight_checker=lambda _: True,
        now=now,
        store=store,
    )

    assert result.lease is not None
    assert result.lease.pr_number == 2
    assert result.state is not None
    assert result.state.revision == 3


def test_dispatch_due_work_records_operation_with_operation_log(tmp_path) -> None:
    now = datetime.now(UTC)
    item = _make_item(1, now=now)
    store = QueueStore(repo="o/r", backing=InMemoryBackingStore())
    state = store.save(QueueState("o/r", 0, {1: item}, [], []), expected_revision=0)
    operation_log = OperationLog(tmp_path, "run-1")
    operation_log.append(
        OperationLogRecord(
            operation_id="unrelated",
            run_id="run-1",
            tool_name="other",
            status="pending",
        )
    )

    result = dispatch_due_work(
        state,
        eligibility_checker=lambda _: True,
        preflight_checker=lambda _: True,
        now=now,
        store=store,
        operation_log=operation_log,
    )

    assert result.lease is not None
    assert operation_log.all_records()


def test_dispatch_due_work_uses_supplied_operation_id(tmp_path) -> None:
    now = datetime.now(UTC)
    item = _make_item(1, now=now)
    operation_log = OperationLog(tmp_path, "run-1")
    operation_log.log_path.touch()

    result = dispatch_due_work(
        QueueState("o/r", 0, {1: item}, [], []),
        eligibility_checker=lambda _: True,
        preflight_checker=lambda _: True,
        now=now,
        operation_log=operation_log,
        operation_id="supplied-operation",
    )

    assert result.operation_id == "supplied-operation"
    assert result.lease is not None


def test_dispatch_due_work_skips_completed_operation(tmp_path) -> None:
    now = datetime.now(UTC)
    item = _make_item(1, now=now)
    operation_log = OperationLog(tmp_path, "run-1")
    operation_id = compute_operation_id(
        "dispatch_due_work",
        "reconciliation.dispatch",
        {
            "repo": item.repo,
            "pr_number": item.pr_number,
            "change_id": item.change_id,
            "observation_watermark": item.observation_watermark,
        },
    )
    operation_log.append(
        OperationLogRecord(
            operation_id=operation_id,
            run_id="run-1",
            tool_name="reconciliation.dispatch",
            status="completed",
        )
    )
    result = dispatch_due_work(
        QueueState("o/r", 0, {1: item}, [], []),
        eligibility_checker=lambda _: True,
        preflight_checker=lambda _: True,
        now=now,
        operation_log=operation_log,
    )

    assert result.lease is None
