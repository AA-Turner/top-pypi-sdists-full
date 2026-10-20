"""A background helper owns its own persistence lane (L25c, 2026-10-18).

THE DEFECT. A background helper (the ``agent`` tool handed off, a wake-up, a
steer that continues a helper) is a child agent run that keeps going after the
request that started it has ended. Its child scope used to mint a Coordinator
and register that Coordinator's flush on the PARENT request's lane. When the
parent finished first, the parent's lane drained and SEALED the helper's
Coordinator mid-run; every later helper write (its assistant message, its
conversation's status/message_count update, its request snapshot) then took a
late one-shot and filed a ``persistence_after_lane_drain`` system_error — three
per PB-08 turn 2 (local conversation 23d0b11f…, request 43113960…). The writes
landed late, one by one, outside the helper's own write order.

THE CONTRACT. A child agent run owns its Coordinator outright: it is never a
finalizer on the parent's lane, it commits synchronously at the child's own
exit, and the parent's lane drains only the parent's writes. So a helper that
finishes after its parent persists every write through its own Coordinator,
in order, with zero ``persistence_after_lane_drain``.
"""

from __future__ import annotations

import asyncio
import contextlib
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.persistence.registry import register_table

_TABLE = "public.cx_l25c_helper_rows"
_ORG = "88888888-8888-4888-8888-888888888888"

_WRITTEN: list[tuple[str, str, dict[str, Any]]] = []


class _Meta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "cx_l25c_helper_rows"
    db_schema = "public"


class _Row:
    _meta = _Meta()

    @classmethod
    async def bulk_create(cls, objects_data):
        for d in objects_data:
            _WRITTEN.append(("insert", str(d["id"]), dict(d)))
        return [cls(**d) for d in objects_data]

    @classmethod
    async def bulk_update(cls, instances, fields=None):
        for inst in instances:
            _WRITTEN.append(("update", str(inst.id), dict(vars(inst))))
        return len(instances)

    @classmethod
    async def bulk_delete(cls, instances):
        return len(instances)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


register_table(_TABLE, _Row)


class _Lane:
    """The parent request's lane: finalizers run once, when it drains."""

    def __init__(self) -> None:
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
    lane = _Lane()
    late_kinds: list[str] = []
    one_shots: list[str] = []
    capture_tasks: list[asyncio.Task] = []

    async def fake_capture_error(exc, **kwargs):
        late_kinds.append(kwargs.get("kind"))

    real_one_shot = Coordinator._fire_one_shot

    def recording_one_shot(self, table, payload, op_type, primary_key):
        one_shots.append(f"{op_type}:{primary_key[1]}")
        return real_one_shot(self, table, payload, op_type, primary_key)

    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error", fake_capture_error
    )
    monkeypatch.setattr(
        queue_helpers,
        "detached_task",
        lambda coro, *, name: capture_tasks.append(asyncio.ensure_future(coro)),
    )
    monkeypatch.setattr(queue_helpers, "get_current_lane", lambda: lane)
    monkeypatch.setattr(queue_helpers, "_ensure_cx_registered", lambda: None)
    monkeypatch.setattr(
        queue_helpers,
        "_resolve_app_context",
        lambda: SimpleNamespace(
            organization_id=_ORG,
            request_id="r-parent",
            user_id="u-1",
            conversation_id="c-parent",
        ),
    )
    monkeypatch.setattr(Coordinator, "_fire_one_shot", recording_one_shot)
    token = queue_helpers._coordinator_cv.set(None)
    try:
        yield SimpleNamespace(
            qh=queue_helpers,
            lane=lane,
            late_kinds=late_kinds,
            one_shots=one_shots,
            capture_tasks=capture_tasks,
        )
    finally:
        queue_helpers._coordinator_cv.reset(token)


def _write(qh, row_id: str, op_type: str = "insert", **fields: Any) -> None:
    qh._queue_or_drop(
        _TABLE,
        {"id": row_id, **fields},
        op_type=op_type,
        primary_key=("id", row_id),
    )


async def _settle(h) -> None:
    for _ in range(5):
        await asyncio.sleep(0)
    if h.capture_tasks:
        await asyncio.gather(*h.capture_tasks)


@pytest.mark.asyncio
async def test_a_helper_finishing_after_its_parent_persists_every_write(harness):
    h = harness
    qh = h.qh

    # The parent request owns its lane's Coordinator.
    parent = qh.get_coordinator()
    assert parent is not None
    _write(qh, "parent-tool-row")

    helper_started = asyncio.Event()
    parent_done = asyncio.Event()
    live_owner: list[bool] = []
    helper_ctx = SimpleNamespace(request_id="r-parent", user_id="u-1", conversation_id="c-helper")

    async def background_helper() -> None:
        async with qh._child_coordinator_scope("helper", helper_ctx):
            _write(qh, "helper-user-msg")
            helper_started.set()
            await parent_done.wait()
            # Every "who owns this write?" door answers with the helper's OWN
            # Coordinator, not a side scope — the parent's lane is closed but
            # the helper's owner is not (persist_completed_request, the
            # conversation gate and the cache-state update ask this).
            own = qh._coordinator_cv.get(None)
            live_owner.append(qh.get_live_coordinator() is own and own is not None)
            # The helper keeps working after its parent request has ended.
            _write(qh, "helper-assistant-msg")
            _write(qh, "helper-conversation", status="completed", message_count=2)
            _write(qh, "helper-user-msg", op_type="update", status="answered")

    task = asyncio.create_task(background_helper())
    await helper_started.wait()

    # The parent request finishes FIRST and drains its lane.
    await h.lane.drain()
    parent_done.set()
    await task
    await _settle(h)

    assert h.late_kinds == [], (
        "a background helper's writes reached a Coordinator after the parent "
        f"lane drained: system_error kinds {h.late_kinds}"
    )
    assert h.one_shots == [], (
        "a helper's writes took late one-shots instead of its own Coordinator's "
        f"ordered commit: {h.one_shots}"
    )
    assert live_owner == [True], (
        "after the parent closed, get_live_coordinator() did not answer with the "
        "helper's own Coordinator"
    )
    finalizer_owners = [name for name, _ in h.lane.finalizers]
    assert finalizer_owners == ["coordinator.commit"], (
        "the parent's lane must drain only the parent's own Coordinator; "
        f"it held {len(finalizer_owners)} coordinator finalizers"
    )
    written = [(op, row_id) for op, row_id, _ in _WRITTEN]
    for expected in (
        ("insert", "parent-tool-row"),
        ("insert", "helper-user-msg"),
        ("insert", "helper-assistant-msg"),
        ("insert", "helper-conversation"),
    ):
        assert expected in written, f"{expected} never persisted; wrote {written}"
    # The helper's later UPDATE is applied in its own write order: either
    # coalesced into its still-pending INSERT or written after it.
    final = {}
    for _op, row_id, data in _WRITTEN:
        final.setdefault(row_id, {}).update(data)
    assert final["helper-user-msg"].get("status") == "answered", _WRITTEN
    assert final["helper-conversation"].get("status") == "completed", _WRITTEN


@pytest.mark.asyncio
async def test_a_helper_starting_after_its_parent_closed_writes_without_a_boundary_error(
    harness,
):
    """A wake-up or continued helper that begins after the parent lane closed
    commits through its own Coordinator — no late boundary is manufactured."""
    h = harness
    qh = h.qh

    qh.get_coordinator()
    await h.lane.drain()

    helper_ctx = SimpleNamespace(request_id="r-parent", user_id="u-1", conversation_id="c-helper")
    async with qh._child_coordinator_scope("helper", helper_ctx):
        _write(qh, "woken-helper-msg")
        _write(qh, "woken-helper-conversation", status="completed")
    await _settle(h)

    assert h.late_kinds == [], f"system_error kinds {h.late_kinds}"
    assert h.one_shots == [], f"late one-shots {h.one_shots}"
    written = [(op, row_id) for op, row_id, _ in _WRITTEN]
    assert ("insert", "woken-helper-msg") in written
    assert ("insert", "woken-helper-conversation") in written


@pytest.mark.asyncio
async def test_a_drained_lane_with_no_owned_coordinator_is_never_minted_into(harness):
    """The other half: work with NO owner of its own under a drained lane gets
    None from get_live_coordinator (its caller takes a standalone scope)."""
    h = harness
    qh = h.qh
    qh.get_coordinator()
    await h.lane.drain()
    qh._coordinator_cv.set(None)
    assert qh.live_owner_is_terminal() is True
    assert qh.get_live_coordinator() is None
