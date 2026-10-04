"""A hung commit can never hang the run (live 2026-10-03, conversation 93ea4aed).

During a DB outage a background group-chat turn sat in its final synchronous
commit (``Coordinator.finalize``) for 7+ minutes: the current-cache flush was a
bare ``await session.flush()`` with no bound, while the lease heartbeat kept the
conversation locked. These guards simulate that wedged commit — including one
that also ignores cancellation, which defeats ``asyncio.wait_for`` — and require
every synchronous commit point to come back BOUNDED, with a real failure
(``PersistenceBarrierError``) and the ops captured to system_write_failure.

Each test runs under an outer timeout: on the old code it hangs and fails there.
"""

from __future__ import annotations

import asyncio
import contextlib

import pytest

import matrx_ai.persistence.coordinator as coord_mod
from matrx_ai.persistence.coordinator import (
    Coordinator,
    CoordinatorPhase,
    PersistenceBarrierError,
)
from matrx_ai.persistence.liveness import (
    RunLiveness,
    bind_run_liveness,
    unbind_run_liveness,
)
from matrx_ai.persistence.registry import register_table

# The outer bound the old code cannot meet (it hangs until cancelled).
_OUTER = 5.0


class _Meta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "cx_hung_commit"
    db_schema = "public"


class _Model:
    _meta = _Meta()

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


register_table("public.cx_hung_commit", _Model)


@contextlib.asynccontextmanager
async def _fake_transaction(*args, **kwargs):
    yield


@pytest.fixture(autouse=True)
def _short_bounds(monkeypatch):
    import matrx_orm.core.transaction as txn_mod

    monkeypatch.setattr(txn_mod, "transaction", _fake_transaction)
    monkeypatch.setattr(coord_mod, "_COMMIT_HARD_DEADLINE_SECONDS", 0.2)
    monkeypatch.setattr(coord_mod, "_CANCEL_SETTLE_SECONDS", 0.05)
    monkeypatch.setattr(coord_mod, "_CAPTURE_DEADLINE_SECONDS", 0.2)
    monkeypatch.setattr(coord_mod, "_DRAIN_TIMEOUT_SECONDS", 0.3)
    coord_mod._inflight_commits = 0
    yield
    coord_mod._inflight_commits = 0


_released = {"value": False}


def _wedge(monkeypatch, *, ignore_cancel: bool) -> None:
    """Make every flush hang like a black-holed DB socket."""

    async def hang(tiers):
        swallowed = 0
        while True:
            try:
                await asyncio.sleep(3600)
            except asyncio.CancelledError:
                # The FIRST cancel (the deadline's) is swallowed when ignore_cancel;
                # a later one (loop teardown) is honoured so the test can finish.
                if not ignore_cancel or swallowed or _released["value"]:
                    raise
                swallowed += 1
                # asyncpg cleanup on a dead connection: the cancel is not honoured

    monkeypatch.setattr("matrx_orm.session.flush.execute_tiers", hang)
    monkeypatch.setattr("matrx_orm.session.session.execute_tiers", hang)


@pytest.fixture(autouse=True)
def _release_wedged_fakes():
    _released["value"] = False
    yield
    # Loop teardown cancels leftovers; let the cancel-ignoring fakes honour it.
    _released["value"] = True


@pytest.mark.asyncio
@pytest.mark.parametrize("ignore_cancel", [False, True])
async def test_finalize_on_a_wedged_commit_raises_within_its_bound(
    monkeypatch, capture_sink, ignore_cancel
):
    _wedge(monkeypatch, ignore_cancel=ignore_cancel)
    coord = Coordinator(request_id="r-hung", conversation_id="93ea4aed-test")
    coord.queue("public.cx_hung_commit", {"id": "m1", "status": "active"})

    with pytest.raises(PersistenceBarrierError) as info:
        await asyncio.wait_for(coord.finalize(reason="request_final_commit"), _OUTER)

    assert coord.phase is CoordinatorPhase.ERRORED
    assert "hard_deadline" in (info.value.report.error or "")
    assert info.value.report.ops_lost == 1
    failures, _ = capture_sink
    captured_ids = [op.pk_value for f in failures for op in f["ops"]]
    assert captured_ids == ["m1"], "the wedged ops must reach system_write_failure"


@pytest.mark.asyncio
async def test_degrade_drain_on_a_wedged_commit_returns_within_its_bound(monkeypatch):
    _wedge(monkeypatch, ignore_cancel=True)
    coord = Coordinator()
    coord.queue("public.cx_hung_commit", {"id": "m2"})

    failures = await asyncio.wait_for(coord.drain_and_confirm(reason="cancel"), _OUTER)

    assert any("hard_deadline" in f for f in failures)
    assert coord.phase is CoordinatorPhase.ERRORED


@pytest.mark.asyncio
async def test_background_commit_that_ignores_cancel_still_settles(monkeypatch, capture_sink):
    """asyncio.wait_for waits for the cancelled flush to finish cancelling — a
    flush that never does would wedge the 'hard deadline' itself."""
    _wedge(monkeypatch, ignore_cancel=True)
    coord = Coordinator()
    coord.queue("public.cx_hung_commit", {"id": "m3"})
    coord.commit_async(reason="turn_1")
    task = coord._pending_commits[0].task

    done, _ = await asyncio.wait({task}, timeout=_OUTER)

    assert task in done, "the background commit outlived its hard deadline"
    assert isinstance(task.exception(), PersistenceBarrierError)
    failures, _ = capture_sink
    assert [op.pk_value for f in failures for op in f["ops"]] == ["m3"]


@pytest.mark.asyncio
async def test_finalize_declares_itself_to_the_run_liveness_tracker(monkeypatch):
    """The lease heartbeat can only refuse to renew a wedged run if the run
    declares its blocking waits — finalize must be one of them."""
    _wedge(monkeypatch, ignore_cancel=False)
    liveness = RunLiveness("test")
    token = bind_run_liveness(liveness)
    try:
        coord = Coordinator()
        coord.queue("public.cx_hung_commit", {"id": "m4"})
        task = asyncio.ensure_future(coord.finalize(reason="request_final_commit"))
        await asyncio.sleep(0.05)
        assert liveness.open_sections == ["coordinator.finalize:request_final_commit"]
        with pytest.raises(PersistenceBarrierError):
            await asyncio.wait_for(task, _OUTER)
        assert liveness.open_sections == []
    finally:
        unbind_run_liveness(token)


def test_a_section_past_its_bound_is_an_overrun():
    liveness = RunLiveness("test")
    with liveness.section("coordinator.finalize:x", 10.0):
        start = next(iter(liveness._open.values()))[2]
        assert liveness.overrun(now=start + 10.0, grace_seconds=5.0) is None
        stalled = liveness.overrun(now=start + 420.0, grace_seconds=5.0)
        assert stalled is not None and stalled.section == "coordinator.finalize:x"
    assert liveness.overrun(now=start + 9999.0) is None


@pytest.mark.asyncio
async def test_a_wedged_late_one_shot_settles_within_its_bound(monkeypatch, capture_sink):
    """A late write (queued after the request sealed) rides its own Session-of-one.
    That flush was unbounded: on a wedged DB it held its pool connection for as
    long as the DB stayed down. It now settles at the hard deadline and its op
    is captured for replay."""
    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error",
        lambda *a, **k: asyncio.sleep(0),
    )
    coord = Coordinator(request_id="r-late", conversation_id="c-late")
    await coord.flush(reason="stream_end")  # sealed: later writes one-shot
    _wedge(monkeypatch, ignore_cancel=True)

    coord.queue(
        "public.cx_hung_commit", {"status": "done"}, op_type="update", primary_key=("id", "m5")
    )
    late = [t for t in coord._late_one_shots if not t.done()]
    assert late, "the late write was not scheduled as a one-shot"

    done, _ = await asyncio.wait(set(late), timeout=_OUTER)

    assert set(late) <= done, "a late one-shot outlived its hard deadline"
    failures, _ = capture_sink
    assert [op.pk_value for f in failures for op in f["ops"]] == ["m5"]
