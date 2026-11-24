"""A request never inherits the previous request's Coordinator (system_error 72139ca5, 2026-11-11).

THE DEFECT. The request Coordinator lives in a ContextVar (``_coordinator_cv``) that
``get_coordinator()`` sets and nothing resets: the lane ContextVar is released at the
end of a response, the Coordinator one is not. A new request task created from inside a
finished one copies that context (uvicorn starts a pipelined keep-alive request from the
previous request's ``on_response_complete``; CPython 140947 leaks context between tasks
too). The new request then found the OLD Coordinator, owned by the OLD request's lane,
already drained and closed. Live, request afb72b61 (a ``/ai/agents`` start): the
conversation create saw a terminal owner and took the out-of-lane write, the
``last_request_context`` patch from ``track_request_context`` filed
``persistence_after_lane_drain`` with ``lane_phase=closed`` 130 ms into prep (the cancel
came 1.2 s later and played no part), and every later write of the run was a late
one-shot outside the run's own write order.

THE CONTRACT. A Coordinator whose owner lane has closed is not the Coordinator of a
different, active lane. The current request mints its own, registered on its own lane;
nothing is captured as a late write, and its writes commit when its lane drains.
"""

from __future__ import annotations

import asyncio
import contextlib
import contextvars
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.persistence.registry import register_table

_TABLE = "public.cx_inherited_coord_rows"
_ORG = "77777777-7777-4777-8777-777777777777"
_WRITTEN: list[tuple[str, str]] = []


class _Meta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "cx_inherited_coord_rows"
    db_schema = "public"


class _Row:
    _meta = _Meta()

    @classmethod
    async def bulk_create(cls, objects_data):
        for d in objects_data:
            _WRITTEN.append(("insert", str(d["id"])))
        return [cls(**d) for d in objects_data]

    @classmethod
    async def bulk_update(cls, instances, fields=None):
        for inst in instances:
            _WRITTEN.append(("update", str(inst.id)))
        return len(instances)

    @classmethod
    async def bulk_delete(cls, instances):
        return len(instances)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


register_table(_TABLE, _Row)


class _Lane:
    def __init__(self, name: str) -> None:
        self.name = name
        self.phase = "active"
        self.finalizers: list[Any] = []

    def add_finalizer(self, fn, *, name: str) -> None:
        assert self.phase == "active", "a finalizer cannot join a draining lane"
        self.finalizers.append((name, fn))

    async def drain(self) -> None:
        self.phase = "draining"
        for _name, fn in self.finalizers:
            await fn(SimpleNamespace(outcome="stream_end"))
        self.phase = "closed"


@contextlib.asynccontextmanager
async def _fake_transaction(*args, **kwargs):
    yield


@pytest.fixture
def harness(monkeypatch):
    import matrx_orm.core.transaction as txn_mod

    from matrx_ai.persistence import queue_helpers
    from matrx_ai.persistence.coordinator import Coordinator

    _WRITTEN.clear()
    monkeypatch.setattr(txn_mod, "transaction", _fake_transaction)
    current: dict[str, Any] = {"lane": None, "request_id": None}
    late: list[dict[str, Any]] = []
    one_shots: list[str] = []
    capture_tasks: list[asyncio.Future] = []

    async def fake_capture_error(exc, **kwargs):
        late.append(kwargs)

    real_one_shot = Coordinator._fire_one_shot

    def recording_one_shot(self, table, payload, op_type, primary_key):
        one_shots.append(f"{op_type}:{primary_key[1]}")
        return real_one_shot(self, table, payload, op_type, primary_key)

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", fake_capture_error)
    monkeypatch.setattr(
        queue_helpers,
        "detached_task",
        lambda coro, *, name: capture_tasks.append(asyncio.ensure_future(coro)),
    )
    monkeypatch.setattr(queue_helpers, "get_current_lane", lambda: current["lane"])
    monkeypatch.setattr(queue_helpers, "_ensure_cx_registered", lambda: None)
    monkeypatch.setattr(
        queue_helpers,
        "_resolve_app_context",
        lambda: SimpleNamespace(
            organization_id=_ORG,
            request_id=current["request_id"],
            user_id="u-1",
            conversation_id="c-1",
        ),
    )
    monkeypatch.setattr(Coordinator, "_fire_one_shot", recording_one_shot)
    token = queue_helpers._coordinator_cv.set(None)
    try:
        yield SimpleNamespace(
            qh=queue_helpers,
            current=current,
            late=late,
            one_shots=one_shots,
            capture_tasks=capture_tasks,
        )
    finally:
        queue_helpers._coordinator_cv.reset(token)


async def _settle(h) -> None:
    for _ in range(5):
        await asyncio.sleep(0)
    if h.capture_tasks:
        await asyncio.gather(*h.capture_tasks)


def _write(qh, row_id: str) -> None:
    qh._queue_or_drop(_TABLE, {"id": row_id}, op_type="insert", primary_key=("id", row_id))


@pytest.mark.asyncio
async def test_a_request_started_from_a_finished_one_owns_a_fresh_coordinator(harness):
    h = harness
    qh = h.qh

    # Request 1 runs to completion on its lane; its Coordinator stays in the context.
    lane_1 = _Lane("request-1")
    h.current.update(lane=lane_1, request_id="r-1")
    first = qh.get_coordinator()
    assert first is not None
    _write(qh, "request-1-row")
    await lane_1.drain()
    assert lane_1.phase == "closed"

    # Request 2's task is created from inside request 1's context (a pipelined
    # keep-alive request), so it copies request 1's ContextVars. It opens its own lane.
    lane_2 = _Lane("request-2")
    seen: dict[str, Any] = {}

    async def request_2() -> None:
        h.current.update(lane=lane_2, request_id="r-2")
        seen["terminal_owner"] = qh.live_owner_is_terminal()
        coord = qh.get_coordinator()
        seen["coord"] = coord
        _write(qh, "request-2-conversation-metadata")
        _write(qh, "request-2-message")
        await lane_2.drain()

    await asyncio.get_running_loop().create_task(
        request_2(), context=contextvars.copy_context()
    )
    await _settle(h)

    assert seen["terminal_owner"] is False, (
        "request 2 judged its write owner terminal: it read request 1's drained Coordinator"
    )
    assert seen["coord"] is not first, "request 2 reused request 1's sealed Coordinator"
    assert [name for name, _ in lane_2.finalizers] == ["coordinator.commit"], (
        "request 2's Coordinator was not registered on request 2's own lane"
    )
    assert h.late == [], (
        "request 2 filed persistence_after_lane_drain against request 1's closed lane: "
        f"{[k.get('context') for k in h.late]}"
    )
    assert h.one_shots == [], f"request 2's writes took late one-shots: {h.one_shots}"
    assert ("insert", "request-2-conversation-metadata") in _WRITTEN, _WRITTEN
    assert ("insert", "request-2-message") in _WRITTEN, _WRITTEN


@pytest.mark.asyncio
async def test_a_write_after_its_own_lane_closed_is_still_captured(harness):
    """The guard is about a DIFFERENT lane: a write that reaches a Coordinator after its
    own lane drained (the ambient lane is that same closed lane) is still the defect, and
    is still captured — never hidden by the fix above."""
    h = harness
    qh = h.qh

    lane = _Lane("request")
    h.current.update(lane=lane, request_id="r-1")
    qh.get_coordinator()
    await lane.drain()

    _write(qh, "late-row")
    await _settle(h)

    assert [k.get("kind") for k in h.late] == ["persistence_after_lane_drain"]
    assert h.one_shots == ["insert:late-row"]


@pytest.mark.asyncio
async def test_work_after_its_lane_scope_exited_never_writes_into_that_lane(harness):
    """system_error b54f8102 + 66483317 (2026-11-17, ``agent_tests_judge``): an agent-tests
    step ran its agent under ``async with RequestLane.open(...)``; the lane closed and its
    ContextVar was reset (no lane is current), but ``_coordinator_cv`` still held the
    lane's Coordinator. The judge ran next in the same task, saw no lane, so kept its
    lifecycle untouched — and its first ``chat.conversation`` write reached the drained
    Coordinator and filed ``persistence_after_lane_drain`` (lane_phase=closed).

    Left behind by a lane scope that has exited, a Coordinator owns nothing: with no lane
    current, the write goes out through the out-of-lane path, never captured as late."""
    h = harness
    qh = h.qh

    lane = _Lane("agent-call")
    h.current.update(lane=lane, request_id="r-1")
    first = qh.get_coordinator()
    assert first is not None
    await lane.drain()
    h.current.update(lane=None, request_id="r-judge")  # the `async with` exited: no lane is current

    assert qh.live_owner_is_terminal() is False, "the exited lane's drained Coordinator still claims ownership"
    assert qh.get_coordinator() is None, "a write outside any lane reused the exited lane's Coordinator"
    out_of_lane: list[str] = []
    qh_mod = qh

    def fake_without(table, payload, **kw):
        out_of_lane.append(str(payload["id"]))
        return None

    import pytest as _pytest

    mp = _pytest.MonkeyPatch()
    mp.setattr(qh_mod, "_write_without_coordinator", fake_without)
    try:
        _write(qh, "judge-conversation")
    finally:
        mp.undo()
    await _settle(h)

    assert h.late == [], f"filed persistence_after_lane_drain: {[k.get('context') for k in h.late]}"
    assert out_of_lane == ["judge-conversation"]
