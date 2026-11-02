"""Every park and un-park passes through ONE hook (``configure_run_waiting``).

The host keeps a record of what a run waits on (a Request). It can only be right if
the engine tells it at every place a run starts or stops waiting: each test fails
without the hook in that writer.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

from matrx_graph.db import run_store as rs

RUN = "44444444-4444-4444-8444-444444444444"


def _store(monkeypatch, applied: dict) -> rs.RunStore:
    class _Model:
        async def update_where(self, filters, **kw):
            return SimpleNamespace(rows_affected=applied["n"])

    monkeypatch.setattr(rs, "get_model", lambda name: _Model())
    return rs.RunStore.__new__(rs.RunStore)


def test_every_park_and_unpark_is_announced(monkeypatch):
    heard: list[tuple] = []

    async def hook(run_id, event, status, interrupt):
        heard.append((event, status, (interrupt or {}).get("node_id")))

    applied = {"n": 1}
    store = _store(monkeypatch, applied)

    async def transition(run_id, *, from_statuses, to_status, **kw):
        return applied["n"] == 1

    monkeypatch.setattr(store, "transition", transition, raising=False)
    rs.configure_run_waiting(hook)
    try:
        asyncio.run(store.mark_interrupted(RUN, interrupt_payload={"node_id": "ask", "payload": {}}))
        asyncio.run(store.mark_awaiting_input(RUN, interrupt_payload={"kind": "awaiting_input"}))
        asyncio.run(store.claim_for_resume(RUN, from_statuses=("interrupted",)))
        asyncio.run(store.mark_completed(RUN, output={}, steps_executed=1))
        asyncio.run(store.mark_paused(RUN))  # a person-free park is not announced
        applied["n"] = 0
        asyncio.run(store.mark_awaiting_input(RUN, interrupt_payload={}))  # guard refused: nothing
        asyncio.run(store.claim_for_resume(RUN))  # lost the race: nothing
    finally:
        rs.configure_run_waiting(None)
    assert heard == [
        ("waiting", "interrupted", "ask"),
        ("waiting", "awaiting_input", None),
        ("resumed", "running", None),
        ("settled", "completed", None),
    ]


def test_a_failing_hook_never_reaches_the_run(monkeypatch):
    async def hook(*a):
        raise RuntimeError("host is down")

    store = _store(monkeypatch, {"n": 1})
    rs.configure_run_waiting(hook)
    try:
        asyncio.run(store.mark_interrupted(RUN, interrupt_payload={"node_id": "ask"}))
    finally:
        rs.configure_run_waiting(None)
