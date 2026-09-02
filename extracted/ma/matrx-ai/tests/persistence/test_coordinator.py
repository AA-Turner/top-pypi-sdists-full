"""Coordinator (Phase G consolidated) — verifies the matrx-ai façade
over ``matrx_orm.Session``.

The legacy WriteCoordinator and SessionCoordinator are gone. There is
one ``Coordinator`` class now (with a back-compat ``WriteCoordinator``
alias). These tests pin its behavior: queue translation, idempotent
flush, error path, late-write auto-elevation, registry interaction.

We register fake Models in the matrx-ai persistence registry and
intercept the matrx-orm session flush executor so no real DB is
touched.
"""

from __future__ import annotations

import asyncio
import contextlib
from collections.abc import Sequence

import pytest

from matrx_ai.persistence.coordinator import (
    Coordinator,
    CoordinatorPhase,
    PersistenceBarrierError,
    WriteCoordinator,  # back-compat alias
)
from matrx_ai.persistence.registry import register_table


class _FakeFK:
    def __init__(self, related_model):
        self.related_model = related_model


class _FakeMetaA:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "cx_fake_a"
    db_schema = "public"


class _FakeMetaB:
    primary_keys = ["id"]
    foreign_keys: dict = {}  # set below after both classes defined
    table_name = "cx_fake_b"
    db_schema = "public"


class _FakeModelA:
    _meta = _FakeMetaA()

    @classmethod
    async def bulk_create(cls, objects_data):
        return [cls(**d) for d in objects_data]

    @classmethod
    async def bulk_update(cls, instances, fields=None):
        return len(instances)

    @classmethod
    async def bulk_delete(cls, instances):
        return len(instances)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class _FakeModelB:
    _meta = _FakeMetaB()

    @classmethod
    async def bulk_create(cls, objects_data):
        return [cls(**d) for d in objects_data]

    @classmethod
    async def bulk_update(cls, instances, fields=None):
        return len(instances)

    @classmethod
    async def bulk_delete(cls, instances):
        return len(instances)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


_FakeMetaB.foreign_keys = {"a_id": _FakeFK(_FakeModelA)}

register_table("public.cx_fake_a", _FakeModelA)
register_table("public.cx_fake_b", _FakeModelB)


@contextlib.asynccontextmanager
async def _fake_transaction(*args, **kwargs):
    yield


@pytest.fixture(autouse=True)
def _patch_transaction(monkeypatch):
    import matrx_orm.core.transaction as txn_mod

    monkeypatch.setattr(txn_mod, "transaction", _fake_transaction)
    yield


@pytest.fixture(autouse=True)
def _reset_inflight_commits():
    """The background-commit in-flight counter is process-global (backpressure
    cap). Reset it around each test so done-callback timing can't drift it across
    tests and trip a false backpressure error."""
    import matrx_ai.persistence.coordinator as _coord_mod

    _coord_mod._inflight_commits = 0
    yield
    _coord_mod._inflight_commits = 0


@pytest.fixture
def captured_tiers(monkeypatch):
    captured: list[list[list]] = []

    async def fake_execute_tiers(tiers: Sequence[Sequence]) -> int:
        snapshot = [list(t) for t in tiers]
        captured.append(snapshot)
        return sum(len(t) for t in snapshot)

    monkeypatch.setattr(
        "matrx_orm.session.flush.execute_tiers",
        fake_execute_tiers,
    )
    monkeypatch.setattr(
        "matrx_orm.session.session.execute_tiers",
        fake_execute_tiers,
    )
    return captured


async def _let_captures_run() -> None:
    """The Coordinator captures dropped ops on a DETACHED task (queue() is sync,
    capture is async). Yield enough scheduler turns for it to complete."""
    for _ in range(20):
        await asyncio.sleep(0)


# ---------------------------------------------------------------------------
# Queue + flush
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_queue_then_flush_writes_all_ops(captured_tiers):
    coord = Coordinator()
    op_id_a = coord.queue("public.cx_fake_a", {"id": "a1", "name": "alice"})
    op_id_b = coord.queue(
        "public.cx_fake_b",
        {"id": "b1", "a_id": "a1", "label": "hi"},
    )
    assert op_id_a and op_id_b

    report = await coord.flush(reason="stream_end")

    assert report.ops_queued == 2
    assert report.ops_written == 2
    assert coord.phase is CoordinatorPhase.FLUSHED
    # FK-inferred DAG: A before B → 2 tiers.
    assert len(captured_tiers[0]) == 2


@pytest.mark.asyncio
async def test_update_op_coalesces_with_insert(captured_tiers):
    coord = Coordinator()
    coord.queue("public.cx_fake_a", {"id": "a1", "name": "alice"})
    coord.queue(
        "public.cx_fake_a",
        {"name": "alice2"},
        op_type="update",
        primary_key=("id", "a1"),
    )
    report = await coord.flush(reason="stream_end")
    # Coalescer merges INSERT + UPDATE → 1 INSERT.
    assert report.ops_queued == 2
    assert report.ops_after_coalesce == 1


@pytest.mark.asyncio
async def test_flush_is_idempotent(captured_tiers):
    coord = Coordinator()
    coord.queue("public.cx_fake_a", {"id": "a1"})
    r1 = await coord.flush(reason="stream_end")
    r2 = await coord.flush(reason="stream_end")
    assert r1 is r2
    assert len(captured_tiers) == 1


@pytest.mark.asyncio
async def test_standalone_coordinator_isolated_and_restores_context(
    captured_tiers, monkeypatch
):
    from matrx_orm.session.managed import _has_coordinator_authority
    from matrx_orm.session.session import _session_stack

    from matrx_ai.persistence import queue_helpers

    monkeypatch.setattr(queue_helpers, "_ensure_cx_registered", lambda: None)
    parent = Coordinator()
    parent_token = queue_helpers._coordinator_cv.set(parent)
    stack_before = _session_stack.get()
    scoped = None
    try:
        async with queue_helpers.standalone_coordinator(
            reason="background_test",
            request_id="request-1",
        ) as coordinator:
            scoped = coordinator
            assert coordinator is not parent
            assert queue_helpers.get_coordinator() is coordinator
            assert _has_coordinator_authority(_session_stack.get()[-1])
            coordinator.queue("public.cx_fake_a", {"id": "a-standalone"})

        assert parent.ops_count == 0
        assert scoped is not None
        assert scoped.phase is CoordinatorPhase.FLUSHED
        assert _session_stack.get() == stack_before
    finally:
        queue_helpers._coordinator_cv.reset(parent_token)


@pytest.mark.asyncio
async def test_flush_with_no_ops_succeeds(captured_tiers):
    coord = Coordinator()
    report = await coord.flush(reason="stream_end")
    assert report.ops_queued == 0
    assert coord.phase is CoordinatorPhase.FLUSHED
    assert len(captured_tiers) == 0


@pytest.mark.asyncio
async def test_queue_with_no_pk_captures_to_system_error(capture_sink, captured_tiers):
    """No pk → not cleanly replayable, but the loss is STILL durable (system_error),
    never a silent drop. Still poisons ops_lost accounting."""
    failures, errors = capture_sink
    coord = Coordinator(request_id="r-1")
    op_id = coord.queue("public.cx_fake_a", {"name": "no-id"})
    assert op_id == ""
    await _let_captures_run()
    assert not failures
    assert len(errors) == 1
    assert errors[0]["kwargs"].get("error_type") == "coordinator_drop_malformed"
    report = await coord.flush(reason="stream_end")
    assert report.ops_lost == 1


@pytest.mark.asyncio
async def test_queue_with_unregistered_table_captures(capture_sink, captured_tiers):
    """An unregistered table can't build a replayable op (get_model fails) but is
    captured to system_error so the loss is durable, not silent."""
    failures, errors = capture_sink
    coord = Coordinator()
    op_id = coord.queue("public.not_registered_anywhere", {"id": "x"})
    assert op_id == ""
    await _let_captures_run()
    assert len(errors) == 1


@pytest.mark.asyncio
async def test_bare_table_key_is_reconciled_not_dropped(capture_sink, captured_tiers):
    """THE 2026-08-15 INCIDENT. A call site passing a bare relation name must
    still write — the op lands, nothing is captured, and no barrier fails.

    Before this, ``get_model`` raised, the op was dropped at queue time, and
    ``commit_async`` killed the live request with a PersistenceBarrierError.
    """
    failures, errors = capture_sink
    coord = Coordinator(request_id="r-1", conversation_id="c-1")

    op_id = coord.queue("cx_fake_a", {"id": "a1", "name": "alice"})

    assert op_id != "", "a bare-but-unambiguous key must NOT be dropped"
    assert coord._dropped_ops_count == 0
    coord.commit_async(reason="turn_1_commit")  # must not raise
    await coord.check_pending()
    await _let_captures_run()
    assert failures == [] and errors == []
    assert captured_tiers, "the reconciled op actually committed"


@pytest.mark.asyncio
async def test_late_one_shot_for_unknown_table_is_captured(
    capture_sink, captured_tiers
):
    """A LATE write for a table we cannot resolve must still be captured.

    This path used to print one red console line and return — the only drop
    path in the Coordinator with no durable sink at all.
    """
    _failures, errors = capture_sink
    coord = Coordinator(request_id="r-1", conversation_id="c-1")
    coord.queue("public.cx_fake_a", {"id": "a1"})
    await coord.flush(reason="stream_end")
    assert coord.phase is CoordinatorPhase.FLUSHED

    assert coord.queue("nothing.ever_registered_this", {"id": "late-1"}) == ""
    await _let_captures_run()

    assert len(errors) == 1, "late write for an unknown table must not vanish"
    assert (errors[0]["kwargs"].get("context") or {}).get("reason") == (
        "one_shot_unregistered_table"
    )


@pytest.mark.asyncio
async def test_uncaptured_drop_records_primary_key_and_op_type(
    capture_sink, captured_tiers
):
    """An op the Coordinator cannot rebuild still records WHICH row it was.

    2026-08-15: 51 uncaptured drops landed carrying only ``table`` + ``reason``,
    so the rows they belonged to could not be named from the record at all —
    the diagnostic was durable but unactionable.
    """
    _failures, errors = capture_sink
    coord = Coordinator(request_id="r-1", conversation_id="c-1")

    coord.queue(
        "nothing.ever_registered_this",
        {"status": "completed"},
        op_type="update",
        primary_key=("id", "row-42"),
    )
    await _let_captures_run()

    assert len(errors) == 1
    ctx = errors[0]["kwargs"].get("context") or {}
    assert ctx.get("op_type") == "update"
    assert ctx.get("primary_key") == ["id", "row-42"]


@pytest.mark.asyncio
async def test_queue_in_errored_phase_captures_for_replay(capture_sink, captured_tiers):
    """The user's exact 'latch onto the group, group is gone, silently ignored'
    scenario. A registered op queued into an ERRORED coordinator is now CAPTURED
    to system_write_failure (replayable), not dropped on the floor."""
    failures, errors = capture_sink
    coord = Coordinator(request_id="r-1", conversation_id="c-1")
    coord._phase = CoordinatorPhase.ERRORED
    op_id = coord.queue("public.cx_fake_a", {"id": "a1", "name": "alice"})
    assert op_id == ""
    await _let_captures_run()
    assert len(failures) == 1, "ERRORED-phase write must be captured for replay"
    assert failures[0]["kwargs"].get("conversation_id") == "c-1"
    assert len(failures[0]["ops"]) == 1


@pytest.mark.asyncio
async def test_failed_late_one_shot_is_captured(capture_sink, captured_tiers, monkeypatch):
    """A late write that one-shots and then FAILS outside Session (the exact gap
    that left research_web's cx_tool_call stuck 'running' until the watchdog)
    must be captured to system_write_failure, not just logged."""
    failures, _errors = capture_sink
    structured = []

    async def fake_capture_error(exc, **kwargs):
        structured.append({"exc": exc, "kwargs": kwargs})

    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error", fake_capture_error
    )
    coord = Coordinator(request_id="r-1", conversation_id="c-1")
    coord.queue("public.cx_fake_a", {"id": "a1"})
    await coord.flush(reason="stream_end")
    assert coord.phase is CoordinatorPhase.FLUSHED

    class _BoomSession:
        def __init__(self, *a, **k):
            pass

        async def __aenter__(self):
            raise RuntimeError("one-shot session boom")

        async def __aexit__(self, *a):
            return False

    monkeypatch.setattr("matrx_orm.session.session.Session", _BoomSession)

    op_id = coord.queue(
        "public.cx_fake_a", {"name": "late"}, op_type="update", primary_key=("id", "a1")
    )
    assert op_id  # the one-shot was scheduled
    await _let_captures_run()
    assert len(failures) == 1, "failed late one-shot must be captured for replay"
    assert failures[0]["kwargs"].get("conversation_id") == "c-1"
    assert len(structured) == 1
    assert structured[0]["kwargs"]["kind"] == "late_persistence_write_failed"
    assert structured[0]["kwargs"]["context"] == {
        "table": "public.cx_fake_a",
        "op_type": "update",
    }


@pytest.mark.asyncio
async def test_late_one_shots_preserve_fk_queue_order(monkeypatch, captured_tiers):
    """A late parent INSERT must finish before its FK-dependent UPDATE starts."""
    coord = Coordinator(request_id="r-1", conversation_id="c-1")
    coord.queue("public.cx_fake_a", {"id": "seed"})
    await coord.flush(reason="stream_end")

    order: list[str] = []
    first_may_finish = asyncio.Event()

    class _OrderedSession:
        def __init__(self, *args, **kwargs):
            self.label = ""

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            order.append(f"finish:{self.label}")
            if self.label == "parent":
                first_may_finish.set()
            return False

        def defer_insert(self, model, payload, *, pk_value):
            self.label = "parent"
            order.append("start:parent")

        def defer_update(self, model, pk_value, payload):
            assert first_may_finish.is_set(), "dependent update raced parent insert"
            self.label = "child"
            order.append("start:child")

    monkeypatch.setattr(
        "matrx_orm.session.managed._coordinator_session", _OrderedSession
    )

    coord.queue("public.cx_fake_a", {"id": "parent"})
    coord.queue(
        "public.cx_fake_b",
        {"a_id": "parent"},
        op_type="update",
        primary_key=("id", "child"),
    )
    await coord._late_one_shot_tail

    assert order == ["start:parent", "finish:parent", "start:child", "finish:child"]


# ---------------------------------------------------------------------------
# Cross-coordinator pending visibility (the duplicate-cx_user_request fix)
#
# Each sub-agent gets its OWN Coordinator (own Session), pushed onto the
# matrx-orm session stack on top of the parent request's Session. A read
# inside the child must see the ancestor row the parent already queued —
# otherwise the child's ``ensure_*_exists`` gate misses it and re-queues a
# duplicate INSERT → ``*_pkey`` unique violation when both coordinators
# flush. This pins the stack-walk visibility the gate depends on.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_child_coordinator_sees_parent_pending_ancestor(captured_tiers):
    from matrx_orm.session import (
        current_session,
        has_pending_in_stack,
        pending_ops_across_stack,
    )

    # Parent request coordinator queues the ancestor row (e.g. cx_user_request).
    parent = Coordinator(request_id="r-shared")
    parent.queue("public.cx_fake_a", {"id": "a1", "name": "ancestor"})

    # A sub-agent opens its OWN coordinator → its own Session pushed on top.
    child = Coordinator(request_id="r-shared")

    # The innermost (child) Session has nothing pending for this Model — this is
    # exactly what made the old current_session()-only read blind to the parent.
    assert current_session() is child._session
    assert child._session.has_pending_for(_FakeModelA) is False

    # The stack-walk DOES see the parent's queued ancestor row, so a pending-aware
    # read returns it and the child's gate short-circuits instead of duplicating.
    assert has_pending_in_stack(_FakeModelA) is True
    ops = pending_ops_across_stack(_FakeModelA)
    assert [o.pk_value for o in ops] == ["a1"]


@pytest.mark.asyncio
async def test_flush_failure_surfaces_in_report(monkeypatch, captured_tiers):
    async def boom(tiers):
        raise RuntimeError("simulated flush failure")

    monkeypatch.setattr(
        "matrx_orm.session.flush.execute_tiers",
        boom,
    )
    monkeypatch.setattr(
        "matrx_orm.session.session.execute_tiers",
        boom,
    )

    async def fake_fallback(ops, exc, **kwargs):
        pass

    monkeypatch.setattr(
        "matrx_orm.session.fallback.record_failures",
        fake_fallback,
    )

    coord = Coordinator(request_id="r-1", user_id="u-1")
    coord.queue("public.cx_fake_a", {"id": "a1"})
    report = await coord.flush(reason="error")
    assert coord.phase is CoordinatorPhase.ERRORED
    assert report.error is not None
    assert "simulated flush failure" in report.error


@pytest.mark.asyncio
async def test_queue_after_flush_auto_elevates(captured_tiers):
    coord = Coordinator()
    coord.queue("public.cx_fake_a", {"id": "a1"})
    await coord.flush(reason="stream_end")
    assert len(captured_tiers) == 1

    op_id = coord.queue("public.cx_fake_a", {"id": "a2"})
    assert op_id != ""

    # Let the detached one-shot task run.
    for _ in range(4):
        await asyncio.sleep(0)

    assert len(captured_tiers) == 2


# ---------------------------------------------------------------------------
# Per-turn commit barrier (finalize) — the durability checkpoint
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_finalize_commits_turn_and_rolls_open(captured_tiers):
    """The per-turn barrier commits this turn, keeps the coordinator OPEN, and
    rolls a fresh Session so the next turn batches into its own transaction."""
    coord = Coordinator()
    coord.queue("public.cx_fake_a", {"id": "a1", "name": "alice"})

    sess_before = coord._session
    report1 = await coord.finalize(reason="turn_commit")

    assert report1.ops_written == 1
    assert len(captured_tiers) == 1
    # Unlike terminal flush(), finalize keeps the coordinator OPEN across turns.
    assert coord.phase is CoordinatorPhase.OPEN
    # A fresh Session was installed for the next turn.
    assert coord._session is not sess_before

    # Next turn: independent batch → its own separate transaction.
    coord.queue("public.cx_fake_a", {"id": "a2", "name": "bob"})
    report2 = await coord.finalize(reason="turn_commit")
    assert report2.ops_written == 1
    assert len(captured_tiers) == 2
    assert coord.phase is CoordinatorPhase.OPEN


@pytest.mark.asyncio
async def test_finalize_empty_turn_is_noop(captured_tiers):
    """An empty turn commits nothing and keeps the same open Session — no
    wasted transaction, no churn."""
    coord = Coordinator()
    sess_before = coord._session
    report = await coord.finalize(reason="turn_commit")
    assert report.ops_queued == 0
    assert len(captured_tiers) == 0
    assert coord.phase is CoordinatorPhase.OPEN
    assert coord._session is sess_before


@pytest.mark.asyncio
async def test_finalize_raises_on_commit_failure(monkeypatch, captured_tiers):
    """A failed barrier BLOWS UP — raises PersistenceBarrierError and the
    coordinator goes ERRORED. No silent continue, per the CLAUDE.md contract."""

    async def boom(tiers):
        raise RuntimeError("simulated commit failure")

    monkeypatch.setattr("matrx_orm.session.flush.execute_tiers", boom)
    monkeypatch.setattr("matrx_orm.session.session.execute_tiers", boom)

    async def fake_fallback(ops, exc, **kwargs):
        pass

    monkeypatch.setattr("matrx_orm.session.fallback.record_failures", fake_fallback)

    coord = Coordinator(request_id="r-1", user_id="u-1", conversation_id="c-1")
    coord.queue("public.cx_fake_a", {"id": "a1"})

    with pytest.raises(PersistenceBarrierError) as exc_info:
        await coord.finalize(reason="turn_commit")

    assert coord.phase is CoordinatorPhase.ERRORED
    err = exc_info.value
    assert err.conversation_id == "c-1"
    assert err.request_id == "r-1"
    assert err.report.error is not None
    assert "simulated commit failure" in err.report.error
    assert err.error_info.error_type == "persistence_commit_failed"
    assert err.error_info.is_retryable is False
    assert err.error_info.details["barrier"] == "turn_commit"
    assert err.error_info.details["operations_lost"] == 1
    assert "not a problem with your prompt" in err.error_info.user_message


@pytest.mark.asyncio
async def test_finalize_blows_up_on_dropped_op(captured_tiers):
    """A write dropped at queue time (no pk) is a lost write — the barrier must
    blow up rather than swallow it."""
    coord = Coordinator()
    assert coord.queue("public.cx_fake_a", {"name": "no-id"}) == ""  # dropped: no pk
    with pytest.raises(PersistenceBarrierError):
        await coord.finalize(reason="turn_commit")
    assert coord.phase is CoordinatorPhase.ERRORED


# ---------------------------------------------------------------------------
# Fire-and-forget + accountability (the hot path)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_commit_async_fires_nonblocking_and_check_confirms(captured_tiers):
    """commit_async rolls the session synchronously and fires the flush in the
    background (non-blocking); check_pending confirms it landed."""
    coord = Coordinator()
    coord.queue("public.cx_fake_a", {"id": "a1", "name": "alice"})
    sess_before = coord._session

    coord.commit_async(reason="turn_1")  # fire — sync, non-blocking
    assert coord._session is not sess_before  # rolled immediately
    assert len(coord._pending_commits) == 1

    await coord.check_pending()  # accountability
    assert coord._pending_commits == []
    assert len(captured_tiers) == 1  # actually committed
    assert coord.phase is CoordinatorPhase.OPEN


@pytest.mark.asyncio
async def test_fire_two_turns_then_verify_both(captured_tiers):
    coord = Coordinator()
    coord.queue("public.cx_fake_a", {"id": "a1"})
    coord.commit_async(reason="turn_1")
    coord.queue("public.cx_fake_a", {"id": "a2"})
    coord.commit_async(reason="turn_2")
    assert len(coord._pending_commits) == 2

    await coord.check_pending()
    assert not coord._pending_commits
    assert len(captured_tiers) == 2


@pytest.mark.asyncio
async def test_check_pending_blows_up_on_failed_commit(monkeypatch, captured_tiers):
    """A fired commit that fails surfaces at the NEXT check_pending → blow up."""

    async def boom(tiers):
        raise RuntimeError("background commit failure")

    monkeypatch.setattr("matrx_orm.session.flush.execute_tiers", boom)
    monkeypatch.setattr("matrx_orm.session.session.execute_tiers", boom)

    async def noop(*a, **k):
        return None

    monkeypatch.setattr("matrx_orm.session.fallback.record_failures", noop)

    coord = Coordinator(conversation_id="c-1", request_id="r-1")
    coord.queue("public.cx_fake_a", {"id": "a1"})
    coord.commit_async(reason="turn_1")  # fire (won't land)
    with pytest.raises(PersistenceBarrierError):
        await coord.check_pending()
    assert coord.phase is CoordinatorPhase.ERRORED


@pytest.mark.asyncio
async def test_check_pending_blows_up_on_overdue_commit(monkeypatch, captured_tiers):
    """A commit that never finishes is OVERDUE → bounded wait → blow up (no
    indefinite hang — the exact failure we are eliminating)."""

    async def hang(tiers):
        await asyncio.sleep(3600)  # never completes within grace

    monkeypatch.setattr("matrx_orm.session.flush.execute_tiers", hang)
    monkeypatch.setattr("matrx_orm.session.session.execute_tiers", hang)

    coord = Coordinator()
    coord.queue("public.cx_fake_a", {"id": "a1"})
    coord.commit_async(reason="turn_1")
    hang_task = coord._pending_commits[0].task
    try:
        with pytest.raises(PersistenceBarrierError):
            await coord.check_pending(grace_seconds=0.05)
        assert coord.phase is CoordinatorPhase.ERRORED
    finally:
        hang_task.cancel()


@pytest.mark.asyncio
async def test_commit_async_blows_up_on_dropped_op(captured_tiers):
    """A queue-time drop is a lost write — commit_async refuses to fire past it."""
    coord = Coordinator()
    assert coord.queue("public.cx_fake_a", {"name": "no-id"}) == ""  # dropped: no pk
    with pytest.raises(PersistenceBarrierError):
        coord.commit_async(reason="turn_1")  # sync raise
    assert coord.phase is CoordinatorPhase.ERRORED


@pytest.mark.asyncio
async def test_commit_async_backpressure_blows_up_at_cap(monkeypatch, captured_tiers):
    """When too many bg commits are stuck in flight process-wide, commit_async
    refuses to fire (backpressure) and blows up rather than pile up and starve
    the connection pool."""
    import matrx_ai.persistence.coordinator as _c

    monkeypatch.setattr(_c, "_inflight_commits", _c._MAX_INFLIGHT_COMMITS)
    coord = Coordinator()
    coord.queue("public.cx_fake_a", {"id": "a1"})
    with pytest.raises(PersistenceBarrierError):
        coord.commit_async(reason="turn_1")
    assert coord.phase is CoordinatorPhase.ERRORED


# ---------------------------------------------------------------------------
# Degrade-to-synchronous (panic drain) — data first, never raises
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_drain_and_confirm_secures_cache_and_in_flight(captured_tiers):
    """DEGRADE: flushes the current cache AND awaits in-flight commits, then
    reports clean."""
    coord = Coordinator()
    coord.queue("public.cx_fake_a", {"id": "a1"})
    coord.commit_async(reason="turn_1")  # in-flight
    coord.queue("public.cx_fake_a", {"id": "a2"})  # cached (not yet fired)

    failures = await coord.drain_and_confirm(reason="degrade")
    assert failures == []
    assert len(captured_tiers) == 2  # both secured


@pytest.mark.asyncio
async def test_drain_and_confirm_reports_failure_without_raising(monkeypatch, captured_tiers):
    """The panic drain must NEVER raise — it captures + reports so the unwind
    can't be derailed (failures already in system_write_failure)."""

    async def boom(tiers):
        raise RuntimeError("drain-time failure")

    monkeypatch.setattr("matrx_orm.session.flush.execute_tiers", boom)
    monkeypatch.setattr("matrx_orm.session.session.execute_tiers", boom)

    async def noop(*a, **k):
        return None

    monkeypatch.setattr("matrx_orm.session.fallback.record_failures", noop)

    coord = Coordinator()
    coord.queue("public.cx_fake_a", {"id": "a1"})
    failures = await coord.drain_and_confirm(reason="degrade")  # must not raise
    assert failures
    assert coord.phase is CoordinatorPhase.ERRORED


def test_writecoordinator_alias_is_coordinator():
    """Back-compat: WriteCoordinator must still resolve to the new class."""
    assert WriteCoordinator is Coordinator


def test_set_correlation_updates_ids(captured_tiers):
    coord = Coordinator()
    coord.set_correlation(request_id="r-1", user_id="u-1", conversation_id="c-1")
    assert coord._request_id == "r-1"
    assert coord._user_id == "u-1"
    assert coord._conversation_id == "c-1"


# ---------------------------------------------------------------------------
# Sub-agent fork/join — the FORK-SIDE pre-fan-out parent commit
# ---------------------------------------------------------------------------
# Main already does the JOIN half (flush the child on exit). These pin the FORK
# half: forcing the parent's pending ancestor rows durable BEFORE the child fans
# out, so a child opened after the parent crossed a turn barrier can't miss a
# detached-but-not-yet-landed ancestor INSERT and re-queue a duplicate.


@pytest.mark.asyncio
async def test_child_scope_finalizes_parent_before_fan_out(captured_tiers):
    """Entering a sub-agent scope forces the PARENT's pending ancestor rows
    durable FIRST, so the child's FK-dependent writes can never miss them."""
    from matrx_ai.persistence.queue_helpers import (
        _child_coordinator_scope,
        _coordinator_cv,
    )

    parent = Coordinator()
    parent.queue("public.cx_fake_a", {"id": "a1", "name": "ancestor"})
    token = _coordinator_cv.set(parent)
    try:
        assert len(captured_tiers) == 0  # nothing committed before fan-out
        async with _child_coordinator_scope("child", object()):
            # Ancestor row is on disk the instant the child enters.
            assert len(captured_tiers) == 1
            # finalize keeps the parent OPEN so it resumes writing after join.
            assert parent.phase is CoordinatorPhase.OPEN
    finally:
        _coordinator_cv.reset(token)


@pytest.mark.asyncio
async def test_child_scope_empty_parent_is_noop(captured_tiers):
    """No pending parent work → the fork-side commit is a cheap no-op and the
    child still forks normally (the common nested-fan-out path stays fast)."""
    from matrx_ai.persistence.queue_helpers import (
        _child_coordinator_scope,
        _coordinator_cv,
    )

    parent = Coordinator()
    token = _coordinator_cv.set(parent)
    try:
        async with _child_coordinator_scope("child", object()):
            pass
        assert len(captured_tiers) == 0
        assert parent.phase is CoordinatorPhase.OPEN
    finally:
        _coordinator_cv.reset(token)


@pytest.mark.asyncio
async def test_child_scope_pins_owner_before_delayed_task_inherits(monkeypatch):
    """A child-created task cannot first bind persistence after lane close."""
    import asyncio
    from types import SimpleNamespace

    from matrx_ai.persistence import queue_helpers

    lane = SimpleNamespace(phase="active")
    finalizers = []
    late_boundaries = []
    release = asyncio.Event()
    monkeypatch.setattr(queue_helpers, "get_current_lane", lambda: lane)
    monkeypatch.setattr(queue_helpers, "_resolve_app_context", lambda: None)
    monkeypatch.setattr(queue_helpers, "_ensure_cx_registered", lambda: None)
    monkeypatch.setattr(
        queue_helpers,
        "_register_lane_finalizer",
        lambda coordinator, got_lane: finalizers.append((coordinator, got_lane)),
    )
    monkeypatch.setattr(
        queue_helpers,
        "_capture_late_lane_boundary",
        lambda got_lane, _ctx, **_identity: late_boundaries.append(got_lane.phase),
    )

    async def delayed_first_touch():
        await release.wait()
        return queue_helpers.get_coordinator()

    token = queue_helpers._coordinator_cv.set(None)
    try:
        async with queue_helpers._child_coordinator_scope("child", object()):
            owner = queue_helpers._coordinator_cv.get(None)
            assert owner is not None
            task = asyncio.create_task(delayed_first_touch())

        lane.phase = "closed"
        release.set()
        inherited = await task
        assert inherited is owner
        assert finalizers == [(owner, lane)]
        assert late_boundaries == []
    finally:
        queue_helpers._coordinator_cv.reset(token)


@pytest.mark.asyncio
async def test_child_scope_after_parent_lane_uses_standalone_owner(monkeypatch):
    """A child beginning after request close gets an independent commit scope."""
    from contextlib import asynccontextmanager
    from types import SimpleNamespace

    from matrx_ai.persistence import queue_helpers

    lane = SimpleNamespace(phase="closed")
    owner = object()
    entered = []

    monkeypatch.setattr(queue_helpers, "get_current_lane", lambda: lane)

    @asynccontextmanager
    async def fake_standalone(**kwargs):
        entered.append(kwargs)
        token = queue_helpers._coordinator_cv.set(owner)
        try:
            yield owner
        finally:
            queue_helpers._coordinator_cv.reset(token)

    monkeypatch.setattr(queue_helpers, "standalone_coordinator", fake_standalone)
    monkeypatch.setattr(
        queue_helpers,
        "get_coordinator",
        lambda: pytest.fail("terminal request lane must not mint a request coordinator"),
    )

    child = SimpleNamespace(request_id="r-child", user_id="u-child", conversation_id="c-child")
    async with queue_helpers._child_coordinator_scope("child", child):
        assert queue_helpers._coordinator_cv.get(None) is owner

    assert entered == [
        {
            "reason": "child_agent_after_parent_lane",
            "request_id": "r-child",
            "user_id": "u-child",
            "conversation_id": "c-child",
        }
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize("lane_phase", ["draining", "closed"])
async def test_first_write_after_lane_drain_uses_one_shot_and_captures(
    monkeypatch, lane_phase
):
    """A late first write cannot enter an OPEN Session with no finalizer."""
    from types import SimpleNamespace

    from matrx_ai.persistence import queue_helpers
    from matrx_ai.persistence.coordinator import CoordinatorPhase

    lane = SimpleNamespace(phase=lane_phase)
    captures = []
    one_shots = []

    monkeypatch.setattr(queue_helpers, "get_current_lane", lambda: lane)
    monkeypatch.setattr(queue_helpers, "_resolve_app_context", lambda: None)
    monkeypatch.setattr(queue_helpers, "_ensure_cx_registered", lambda: None)
    monkeypatch.setattr(
        queue_helpers,
        "_capture_late_lane_boundary",
        lambda got_lane, ctx, **identity: captures.append(
            (got_lane.phase, ctx, identity)
        ),
    )
    monkeypatch.setattr(
        queue_helpers.Coordinator,
        "_fire_one_shot",
        lambda self, table, payload, op_type, primary_key: one_shots.append(
            (table, op_type, primary_key)
        )
        or "late-op",
    )

    token = queue_helpers._coordinator_cv.set(None)
    try:
        coord = queue_helpers.get_coordinator()
        assert coord is not None
        assert coord.phase is CoordinatorPhase.FLUSHED
        assert captures == []
        assert (
            queue_helpers.queue_message_create(id="m-1", conversation_id="c-1")
            == "late-op"
        )
        assert captures == [
            (
                lane_phase,
                None,
                {
                    "table": "chat.message",
                    "op_type": "insert",
                    "primary_key": ("id", "m-1"),
                },
            )
        ]
        assert queue_helpers.queue_message_update("m-1", role="assistant") == "late-op"
        assert len(captures) == 1
        assert one_shots == [
            ("chat.message", "insert", ("id", "m-1")),
            ("chat.message", "update", ("id", "m-1")),
        ]
    finally:
        queue_helpers._coordinator_cv.reset(token)


@pytest.mark.asyncio
async def test_late_lane_boundary_forces_structured_system_error(monkeypatch):
    """The log-only lifecycle family is promoted into the repair queue."""
    from types import SimpleNamespace

    from matrx_ai.persistence import queue_helpers

    captured = []
    tasks = []

    async def fake_capture_error(exc, **kwargs):
        captured.append((exc, kwargs))

    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error", fake_capture_error
    )
    monkeypatch.setattr(
        queue_helpers,
        "detached_task",
        lambda coro, *, name: tasks.append(__import__("asyncio").create_task(coro)),
    )

    ctx = SimpleNamespace(request_id="r-1", user_id="u-1", conversation_id="c-1")
    queue_helpers._capture_late_lane_boundary(
        SimpleNamespace(phase="closed"),
        ctx,
        table="chat.message",
        op_type="update",
        primary_key=("id", "m-1"),
    )
    await tasks[0]

    assert len(captured) == 1
    _, kwargs = captured[0]
    assert kwargs["kind"] == "persistence_after_lane_drain"
    assert kwargs["error_type"] == "LatePersistenceBoundary"
    assert kwargs["request_id"] == "r-1"
    assert kwargs["context"] == {
        "lane_phase": "closed",
        "table": "chat.message",
        "op_type": "update",
        "primary_key_field": "id",
        "primary_key": "m-1",
    }


@pytest.mark.asyncio
async def test_child_scope_fails_fast_on_parent_commit_failure(monkeypatch, captured_tiers):
    """FAIL FAST: if the parent flush errors at fork time, we do NOT fork a child
    whose FK-dependent writes are already doomed — entering the scope raises and
    the failure is already on the parent's ERRORED verdict / system_write_failure."""

    async def boom(tiers):
        raise RuntimeError("simulated parent flush failure")

    monkeypatch.setattr("matrx_orm.session.flush.execute_tiers", boom)
    monkeypatch.setattr("matrx_orm.session.session.execute_tiers", boom)

    async def noop(*a, **k):
        return None

    monkeypatch.setattr("matrx_orm.session.fallback.record_failures", noop)

    from matrx_ai.persistence.queue_helpers import (
        _child_coordinator_scope,
        _coordinator_cv,
    )

    parent = Coordinator(request_id="r-1", conversation_id="c-1")
    parent.queue("public.cx_fake_a", {"id": "a1"})
    token = _coordinator_cv.set(parent)
    entered = False
    try:
        with pytest.raises(PersistenceBarrierError):
            async with _child_coordinator_scope("child", object()):
                entered = True
        assert entered is False  # body never ran — the fork was aborted
        assert parent.phase is CoordinatorPhase.ERRORED
    finally:
        _coordinator_cv.reset(token)


@pytest.mark.asyncio
async def test_tool_completion_update_survives_child_agent_fork(captured_tiers):
    """End-to-end ``agent_call`` regression (2026-06-20).

    A tool that runs a child agent forks the coordinator. Timeline:

      1. ``log_started`` queues the ``cx_tool_call`` INSERT (status='running')
         on the PARENT coordinator.
      2. The tool dispatches a child agent → ``child_agent_context`` runs the
         ``pre_fan_out`` finalize, flushing that INSERT in its OWN cycle (so the
         row's INSERT and its later completion UPDATE are now in SEPARATE flush
         cycles — the split that does NOT happen for an ordinary tool, whose
         INSERT+UPDATE coalesce in one barrier).
      3. ``log_completed`` queues the completion UPDATE SYNCHRONOUSLY onto the
         restored, still-OPEN parent coordinator (the fix). Pre-fix this was a
         fire-and-forget ``detached_task`` that raced the request's drain+seal
         and landed too late (after seal, as a one-shot that teardown never ran)
         — so it was DROPPED.
      4. The final barrier flushes the UPDATE.

    The completion UPDATE MUST land. Pre-fix it was lost, the row stayed
    ``status='running'`` until the watchdog flipped it to ``error``, and the
    resulting orphaned/empty tool_result produced a duplicate ``tool_result``
    block → Anthropic 400 ``each tool_use must have a single result``.
    """
    from matrx_ai.persistence.queue_helpers import (
        _child_coordinator_scope,
        _coordinator_cv,
    )

    parent = Coordinator(request_id="r-1", conversation_id="c-1")
    token = _coordinator_cv.set(parent)
    try:
        # 1. log_started → INSERT queued on the parent (status='running').
        parent.queue("public.cx_fake_a", {"id": "call-row", "name": "running"})

        # 2. tool dispatch forks a child agent. Entering the scope finalizes the
        #    parent (pre_fan_out), flushing the INSERT in its own cycle.
        async with _child_coordinator_scope("child", object()):
            pass
        assert _coordinator_cv.get(None) is parent  # parent restored on exit
        assert len(captured_tiers) >= 1, "pre_fan_out finalize must flush the INSERT"

        # 3. log_completed → completion UPDATE queued SYNCHRONOUSLY on the still-
        #    OPEN parent coordinator. A drop here (queue() returning "") is the
        #    exact regression — the OPEN coordinator must accept it.
        op = parent.queue(
            "public.cx_fake_a",
            {"name": "completed"},
            op_type="update",
            primary_key=("id", "call-row"),
        )
        assert op, "completion UPDATE must be accepted by the OPEN parent coordinator"

        # 4. final barrier flushes the UPDATE — it must NOT have been lost across
        #    the pre_fan_out split.
        report = await parent.finalize(reason="request_final_commit")
        assert report.ops_written >= 1, (
            "the completion UPDATE was LOST across the child-agent fork — the "
            "agent_call stuck-'running' → watchdog-'error' → duplicate "
            "tool_result → Anthropic 400 regression"
        )
    finally:
        _coordinator_cv.reset(token)


# ---------------------------------------------------------------------------
# Fan-out saturation — the shape that broke production run
# 6266cb1b-f7f9-44f7-a951-15da231de9ef (a Masterwork fanning 25 concurrent
# auditor agent runs; 22 committed, 3 were refused at the 8-commit cap).
# ---------------------------------------------------------------------------


async def _turn_barrier(coord: Coordinator, iteration: int) -> None:
    """Exactly what the orchestrator does at a turn boundary."""
    await coord.check_pending()
    await coord.acquire_commit_slot()
    coord.commit_async(reason=f"turn_{iteration}_commit")


@pytest.mark.asyncio
async def test_wide_fanout_waits_for_a_slot_instead_of_failing(monkeypatch):
    """25 concurrent agent runs (each its own Coordinator) all commit their
    turns while the process-wide cap is 8. Every one must COMPLETE: saturation
    of a pool budget by HEALTHY commits is backpressure to wait on, not a
    durability incident. Nothing commits unconfirmed — each run still crosses
    check_pending and finalize."""
    committed: list[int] = []

    async def slow_execute_tiers(tiers: Sequence[Sequence]) -> int:
        # Real commits take real time; that is what lets 25 concurrent firers
        # collide on 8 slots.
        await asyncio.sleep(0.02)
        n = sum(len(t) for t in tiers)
        committed.append(n)
        return n

    monkeypatch.setattr("matrx_orm.session.flush.execute_tiers", slow_execute_tiers)
    monkeypatch.setattr("matrx_orm.session.session.execute_tiers", slow_execute_tiers)

    fanout = 25

    async def one_agent_run(i: int) -> None:
        coord = Coordinator(request_id=f"req-{i}", conversation_id=f"conv-{i}")
        for turn in (1, 2):
            coord.queue("public.cx_fake_a", {"id": f"a{i}-{turn}"})
            await _turn_barrier(coord, turn)
        await coord.finalize(reason="stream_end")

    # No PersistenceBarrierError anywhere — that is the regression.
    await asyncio.gather(*(one_agent_run(i) for i in range(fanout)))

    # Two fired turns per run, all confirmed.
    assert len(committed) == fanout * 2
    assert sum(committed) == fanout * 2

    import matrx_ai.persistence.coordinator as _c

    assert _c._inflight_commits == 0  # every slot given back


@pytest.mark.asyncio
async def test_slot_wait_is_bounded_and_still_blows_up_when_not_draining(monkeypatch):
    """The wait must NEVER become a way to proceed unconfirmed or hang forever.
    When commits genuinely do not drain, the bounded wait expires and the
    barrier raises exactly as before."""
    import matrx_ai.persistence.coordinator as _c

    async def hang(tiers):
        await asyncio.sleep(3600)

    monkeypatch.setattr("matrx_orm.session.flush.execute_tiers", hang)
    monkeypatch.setattr("matrx_orm.session.session.execute_tiers", hang)
    monkeypatch.setattr(_c, "_inflight_commits", _c._MAX_INFLIGHT_COMMITS)

    coord = Coordinator()
    coord.queue("public.cx_fake_a", {"id": "a1"})
    acquired = await coord.acquire_commit_slot(wait_seconds=0.05)
    assert acquired is False
    with pytest.raises(PersistenceBarrierError) as exc:
        coord.commit_async(reason="turn_1_commit")
    assert "not draining" in str(exc.value)
    assert coord.phase is CoordinatorPhase.ERRORED


@pytest.mark.asyncio
async def test_acquire_slot_never_holds_a_slot_it_does_not_need(captured_tiers):
    """An empty turn (nothing queued) must not consume a slot — otherwise idle
    coordinators would starve real commits."""
    import matrx_ai.persistence.coordinator as _c

    coord = Coordinator()
    assert await coord.acquire_commit_slot() is False
    assert _c._inflight_commits == 0
    coord.commit_async(reason="turn_1_commit")  # no-op, no leak
    assert _c._inflight_commits == 0

    # And a reserved slot that never fires (phase already flushed) is returned.
    coord.queue("public.cx_fake_a", {"id": "a1"})
    assert await coord.acquire_commit_slot() is True
    assert _c._inflight_commits == 1
    await coord.finalize(reason="stream_end")
    assert _c._inflight_commits == 0
