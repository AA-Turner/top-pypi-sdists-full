"""The screen and full views walk payloads that reach megabytes; they never run that walk on the event loop.

2026-11-10: ``GET /runs/{id}/events`` measured each withheld value by serializing it ON the loop and froze the
whole API for 1-3 s at a time (event_loop_stall aidream-api:9ab9718b5356cd2c, 4 times in one afternoon)."""

from __future__ import annotations

import threading

from matrx_graph.checkpoint import value_store
from matrx_graph.checkpoint.values import REF_KEY


async def test_screen_views_fill_runs_off_the_loop_thread(monkeypatch):
    loop_thread = threading.get_ident()
    seen_threads: list[int] = []
    real_fill = value_store._fill_event

    def spy(item, store):
        seen_threads.append(threading.get_ident())
        return real_fill(item, store)

    async def fake_load(run_id, hashes):
        return {h: {"page": "x" * 50_000} for h in hashes}

    monkeypatch.setattr(value_store, "_fill_event", spy)
    monkeypatch.setattr(value_store, "load_run_values", fake_load)
    ref = "a" * 64
    events = [{"event": "node_completed", "node_id": "n", "output": {"pages": {REF_KEY: ref}}}]
    views = await value_store.screen_views("r", events)
    assert seen_threads and all(t != loop_thread for t in seen_threads)
    assert views[0]["withheld"][0]["ref"] == ref


async def test_full_views_resolve_runs_off_the_loop_thread(monkeypatch):
    loop_thread = threading.get_ident()
    seen_threads: list[int] = []
    real = value_store._resolve_everything

    def spy(value, store):
        seen_threads.append(threading.get_ident())
        return real(value, store)

    async def fake_load(run_id, hashes):
        return {h: {"page": "x"} for h in hashes}

    monkeypatch.setattr(value_store, "_resolve_everything", spy)
    monkeypatch.setattr(value_store, "_load_all", fake_load)
    views = await value_store.full_views("r", [{"output": {REF_KEY: "b" * 64}}])
    assert seen_threads and all(t != loop_thread for t in seen_threads)
    assert views[0]["output"] == {"page": "x"}
