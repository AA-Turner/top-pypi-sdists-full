"""Parallel steps' events intern a value they share ONCE, not once each.

L-SPEED 6e (2026-11-10): the production Brand pick child spent 1.8 s interning 36 events (~50 ms each) although
the process remembers every value it interned. The leg line's new cache counters, run locally on the same child,
said why: ``uncommitted`` misses. Steps that start together (four parallel steps handed the same 1.4 MB input)
emit their ``node_started`` events at once; each event found the value remembered by the event next to it, but
that event's store write had not landed yet, so the digest was not committed for the run — and every one walked
and hashed the whole value again (and sent it to the database again). Production's store write is a real round
trip, so the window covered nearly every event.

Green: a run's large events intern one at a time, so the second waits for the first's store write and hits.
Red with the per-run turn removed: every concurrent event walks the value.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_graph.checkpoint import postgres as pg
from matrx_graph.checkpoint import value_store
from matrx_graph.checkpoint import values as values_module
from matrx_graph.checkpoint.values import INTERN_CACHE_TOTALS, clear_interned_cache, referenced_hashes

LIMIT = 32768


def _big() -> dict[str, Any]:
    return {"rows": [{"source": f"s{i}", "body": "x" * 3000, "score": i} for i in range(200)]}


@pytest.fixture
def store(monkeypatch) -> dict[str, Any]:
    monkeypatch.setattr(values_module, "VERIFY_INTERNED_VALUES", False)
    clear_interned_cache()
    written: dict[str, Any] = {}

    async def limit() -> int:
        return LIMIT

    async def slow_store(run_id: str, values: dict[str, Any], **_: Any) -> set[str]:
        fresh = {h: v for h, v in values.items() if h not in pg._stored_value_hashes.get(run_id, set())}
        await asyncio.sleep(0.05)  # a database round trip
        written.update(fresh)
        value_store.remember_stored_values(run_id, fresh)
        return set(fresh)

    monkeypatch.setattr(pg, "_value_store_available", lambda: True)
    monkeypatch.setattr("matrx_graph.knobs.event_inline_value_max_bytes", limit)
    monkeypatch.setattr(value_store, "store_run_values", slow_store)
    return written


async def test_events_that_start_together_walk_their_shared_input_once(store: dict[str, Any]) -> None:
    run_id = "6e000000-0000-4000-8000-000000000001"
    shared = _big()
    before = list(INTERN_CACHE_TOTALS)
    events = [{"event": "node_started", "node_id": f"n{i}", "inputs": {"provision": shared}} for i in range(4)]
    outs = await asyncio.gather(*(value_store.intern_event_payload(run_id, e) for e in events))
    walked = INTERN_CACHE_TOTALS[1] - before[1]
    hits = INTERN_CACHE_TOTALS[0] - before[0]
    assert walked == 1 and hits == 3, (
        f"4 parallel events of one shared value walked it {walked}x (hits {hits}) — the value must be interned "
        "once per run, the other events waiting for its store write instead of hashing it again"
    )
    refs = [referenced_hashes(out["inputs"]) for out in outs]
    assert refs[0] and all(r == refs[0] for r in refs) and refs[0] <= set(store), "every event names the one stored value"


async def test_a_failed_store_write_leaves_the_next_event_to_store_it_itself(store: dict[str, Any], monkeypatch) -> None:
    """The turn is never a promise: an event whose store write failed goes out whole, and the next walks again."""
    run_id = "6e000000-0000-4000-8000-000000000002"
    shared = _big()
    calls = {"n": 0}
    good = value_store.store_run_values

    async def flaky(run_id_: str, values: dict[str, Any], **kw: Any) -> set[str]:
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("database away")
        return await good(run_id_, values, **kw)

    monkeypatch.setattr(value_store, "store_run_values", flaky)
    first, second = await asyncio.gather(
        value_store.intern_event_payload(run_id, {"event": "node_started", "inputs": {"p": shared}}),
        value_store.intern_event_payload(run_id, {"event": "node_started", "inputs": {"p": shared}}),
    )
    assert first["inputs"]["p"] is shared  # stored inline, loud
    named = referenced_hashes(second["inputs"])
    assert named and named <= set(store)


async def test_events_of_different_values_intern_in_parallel(store: dict[str, Any], monkeypatch) -> None:
    """The turn is per VALUE, never per run (review 6h, I1): a For each over large items emits one large event per
    item, each a different value. A per-run turn made them strictly serial (32 events: 1.2 s instead of 0.12 s at a
    30 ms store write). Each must start its store write without waiting for another event's."""
    run_id = "6e000000-0000-4000-8000-000000000003"
    inside = {"now": 0, "most": 0}
    good = value_store.store_run_values

    async def counting(run_id_: str, values: dict[str, Any], **kw: Any) -> set[str]:
        inside["now"] += 1
        inside["most"] = max(inside["most"], inside["now"])
        try:
            return await good(run_id_, values, **kw)
        finally:
            inside["now"] -= 1

    monkeypatch.setattr(value_store, "store_run_values", counting)
    events = [{"event": "node_started", "node_id": f"n{i}", "inputs": {"item": _big()}} for i in range(4)]
    await asyncio.gather(*(value_store.intern_event_payload(run_id, e) for e in events))
    assert inside["most"] == 4, (
        f"4 events of 4 different large values wrote at most {inside['most']} at a time — events that share no "
        "value must never wait for each other's store write"
    )
