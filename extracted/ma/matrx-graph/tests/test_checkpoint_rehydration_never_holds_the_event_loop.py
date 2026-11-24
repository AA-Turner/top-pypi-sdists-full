"""Rehydrating a run's checkpoints never freezes the event loop.

Live 2026-11-07 (event_loop_stall 8fa91a5b, workflow-worker): a resume's ``list_checkpoints``
decoded every checkpoint row and resolved every by-reference value with ``resolve_values`` on
the loop, holding the worker 3 s (no other job, heartbeat or pool checkout ran). A thread spy
proves the walk now runs off the loop thread for a large checkpoint (red before: on the loop).
"""

from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime
from typing import Any

import pytest

from matrx_graph.checkpoint import postgres
from matrx_graph.checkpoint.values import REF_KEY

DIGEST = "a" * 64


def _big_value(n: int = 9_000) -> dict[str, Any]:
    return {"results": [{"i": i, "snippet": "word " * 40, "tags": ["a", str(i)]} for i in range(n)]}


def _row() -> dict[str, Any]:
    return {
        "id": "00000000-0000-4000-8000-000000000001",
        "run_id": "00000000-0000-4000-8000-000000000002",
        "thread_id": "t1",
        "parent_checkpoint_id": None,
        "step": 3,
        "channel_values": json.dumps({"search": {REF_KEY: DIGEST}, "note": "x"}),
        "pending_bindings": json.dumps({}),
        "next_invocations": json.dumps([]),
        "interrupt_payload": None,
        "metadata": None,
        "created_at": datetime.now(UTC),
    }


def _on_loop_thread() -> bool:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return False
    return True


@pytest.mark.asyncio
async def test_resolving_a_large_checkpoint_runs_off_the_loop(monkeypatch: pytest.MonkeyPatch) -> None:
    big = _big_value()

    async def fake_fetch(run_id: str, hashes: Any) -> dict[str, Any]:
        return {DIGEST: big} if DIGEST in set(hashes) else {}

    from matrx_graph.checkpoint import value_store

    monkeypatch.setattr(value_store, "fetch_stored_values", fake_fetch)
    seen: list[bool] = []
    real_resolve = postgres.resolve_values

    def spy_resolve(value: Any, store: dict[str, Any]) -> Any:
        seen.append(_on_loop_thread())
        return real_resolve(value, store)

    monkeypatch.setattr(postgres, "resolve_values", spy_resolve)

    [checkpoint] = await postgres._rows_to_checkpoints([_row()])

    assert seen, "resolve_values never ran"
    assert not any(seen), "resolve_values ran on the event loop thread"
    # The answer is unchanged: the reference resolved to its stored value.
    assert checkpoint.channel_values["search"] == big
    assert checkpoint.channel_values["note"] == "x"
    assert checkpoint.step == 3
