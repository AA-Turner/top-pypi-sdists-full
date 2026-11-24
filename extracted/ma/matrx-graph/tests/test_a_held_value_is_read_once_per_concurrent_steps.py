"""Steps that start together and read the same held value share ONE read and ONE decoded copy (lane M2, 2026-11-19).

The research read held a ~3 MB page that a landing step and a gallery step each loaded and decoded on their own: two
copies of the page per read in memory at once. ``resolve_step_inputs`` now single-flights the load per (run, ref);
the scheduler's ingestion gate still copies every argument, so a step never mutates the shared value.
"""

from __future__ import annotations

import asyncio
import contextlib
from contextlib import asynccontextmanager
from typing import Any

import pytest

from matrx_graph.checkpoint import value_store
from matrx_graph.checkpoint.value_store import HELD_KEY


@pytest.mark.asyncio
async def test_concurrent_steps_reading_one_held_value_share_one_read(monkeypatch: pytest.MonkeyPatch) -> None:
    reads: list[set[str]] = []

    async def fake_fetch(run_id: str, hashes: Any) -> dict[str, Any]:
        reads.append(set(hashes))
        await asyncio.sleep(0.05)  # the DB read takes a moment: the second step starts while the first waits
        return {h: {"raw_html": "x" * 1000, "title": "page"} for h in hashes}

    monkeypatch.setattr(value_store, "fetch_stored_values", fake_fetch)
    ref = "a" * 64
    land, gallery = await asyncio.gather(
        value_store.resolve_step_inputs("run-1", {"page": {HELD_KEY: ref}}),
        value_store.resolve_step_inputs("run-1", {"page": {HELD_KEY: ref}}),
    )
    assert len(reads) == 1, f"one read for both steps, got {len(reads)}"
    assert land["page"] is gallery["page"], "both steps get the one decoded copy"
    assert value_store._HELD_LOADS == {}, "nothing kept once the steps have it"

    # A later step reads it again (nothing is cached past the steps that asked), and a different run never shares.
    await value_store.resolve_step_inputs("run-1", {"page": {HELD_KEY: ref}})
    await value_store.resolve_step_inputs("run-2", {"page": {HELD_KEY: ref}})
    assert len(reads) == 3


@pytest.mark.asyncio
async def test_a_missing_held_value_still_fails_every_reader(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_fetch(run_id: str, hashes: Any) -> dict[str, Any]:
        await asyncio.sleep(0.01)
        return {}

    monkeypatch.setattr(value_store, "fetch_stored_values", fake_fetch)
    from matrx_graph.checkpoint.values import MissingCheckpointValueError

    results = await asyncio.gather(
        value_store.resolve_step_inputs("run-1", {"page": {HELD_KEY: "b" * 64}}),
        value_store.resolve_step_inputs("run-1", {"page": {HELD_KEY: "b" * 64}}),
        return_exceptions=True,
    )
    assert all(isinstance(r, MissingCheckpointValueError) for r in results)


async def test_guarded_held_read_bypasses_an_existing_shared_future_and_closes_after_missing_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Break: a recording-admitted read consumes a prior shared task or validates the missing value after rollback."""
    from matrx_graph.checkpoint.values import MissingCheckpointValueError

    events: list[str] = []
    waiting = asyncio.Event()

    async def stale_shared_read() -> dict[str, Any]:
        await waiting.wait()
        return {"c" * 64: {"source": "wrong-admission"}}

    ref = "c" * 64
    key = (id(asyncio.get_running_loop()), "recording-run", ref)
    stale = asyncio.create_task(stale_shared_read())
    value_store._HELD_LOADS[key] = stale

    @asynccontextmanager
    async def admission(unit: str, run_id: str | None, checkpoint_id: str | None):
        assert (unit, run_id, checkpoint_id) == ("resolve_held_values", "recording-run", None)
        events.append("enter")
        try:
            yield
        except MissingCheckpointValueError:
            events.append("rollback")
            raise
        finally:
            events.append("exit")

    async def guarded_load(run_id: str, hashes: Any) -> dict[str, Any]:
        events.append("load")
        return {}

    monkeypatch.setattr(value_store, "load_run_values", guarded_load)
    try:
        with pytest.raises(MissingCheckpointValueError, match="not stored"):
            await value_store.resolve_step_inputs(
                "recording-run", {"provision": {HELD_KEY: ref}}, read_scope=admission
            )
        assert not stale.done(), "guarded admission consumed a cached read from another context"
        assert events == ["enter", "load", "rollback", "exit"]
    finally:
        value_store._HELD_LOADS.pop(key, None)
        stale.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await stale


async def test_guarded_held_read_batches_nested_values_and_closes_on_cancellation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Break: guarded reads use concurrent loads, truncate a large set, or leave the admission open when cancelled."""
    from matrx_graph.checkpoint.values import REF_KEY

    refs = [f"{n:064x}" for n in range(value_store.MAX_HASHES_PER_READ + 1)]
    nested = "f" * 64
    batches: list[set[str]] = []
    events: list[str] = []

    @asynccontextmanager
    async def admission(unit: str, run_id: str | None, checkpoint_id: str | None):
        events.append("enter")
        try:
            yield
        finally:
            events.append("exit")

    async def fetch(run_id: str, hashes: Any) -> dict[str, Any]:
        batch = set(hashes)
        batches.append(batch)
        return {
            digest: ({REF_KEY: nested} if digest == refs[0] else {"stored": digest})
            for digest in batch
            if digest in refs
        } | ({nested: {"nested": "value"}} if nested in batch else {})

    monkeypatch.setattr(value_store, "fetch_stored_values", fetch)
    resolved = await value_store.resolve_step_inputs(
        "recording-run",
        {f"input_{n}": {HELD_KEY: ref} for n, ref in enumerate(refs)},
        read_scope=admission,
    )
    assert resolved["input_0"] == {"nested": "value"}
    assert resolved[f"input_{len(refs) - 1}"] == {"stored": refs[-1]}
    assert all(len(batch) <= value_store.MAX_HASHES_PER_READ for batch in batches)
    assert events == ["enter", "exit"]

    started = asyncio.Event()
    release = asyncio.Event()

    async def blocked_load(run_id: str, hashes: Any) -> dict[str, Any]:
        started.set()
        await release.wait()
        return {}

    monkeypatch.setattr(value_store, "load_run_values", blocked_load)
    task = asyncio.create_task(
        value_store.resolve_step_inputs(
            "recording-run", {"provision": {HELD_KEY: refs[0]}}, read_scope=admission
        )
    )
    await started.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert events[-2:] == ["enter", "exit"]


async def test_empty_and_malformed_held_inputs_do_not_open_a_read_scope(monkeypatch: pytest.MonkeyPatch) -> None:
    """Break: an empty read opens an admission, or malformed markers stop raising their historical error."""
    from matrx_graph.checkpoint.values import MissingCheckpointValueError

    calls: list[str] = []

    @asynccontextmanager
    async def admission(unit: str, run_id: str | None, checkpoint_id: str | None):
        calls.append("scope")
        yield

    async def unexpected_load(run_id: str, hashes: Any) -> dict[str, Any]:
        calls.append("load")
        return {}

    monkeypatch.setattr(value_store, "load_run_values", unexpected_load)
    assert await value_store.resolve_step_inputs("recording-run", {}, read_scope=admission) == {}
    with pytest.raises(MissingCheckpointValueError, match="not stored"):
        await value_store.resolve_step_inputs("recording-run", {"bad": {}}, read_scope=admission)
    assert calls == []
