"""Calls that arrive together share ONE batch call; each caller keeps its own answer.

Workflow lane B (2026-11-12): three ``records.read`` steps of one wave were three statements.
``matrx_graph.actions.Coalescer`` is the engine's DataLoader: same group + same window = one batch.
"""

from __future__ import annotations

import asyncio

import pytest

from matrx_graph.actions import Coalescer


@pytest.mark.asyncio
async def test_siblings_share_one_batch_and_keep_their_own_answers():
    calls: list[list[str]] = []

    async def batch(keys):
        calls.append(list(keys))
        return {k: (ValueError(f"no {k}") if k == "bad" else k.upper()) for k in keys}

    co: Coalescer[str, str] = Coalescer()
    results = await asyncio.gather(
        co.load("run-1", "a", batch), co.load("run-1", "b", batch), co.load("run-1", "a", batch),
        co.load("run-1", "bad", batch), return_exceptions=True,
    )
    assert results[:3] == ["A", "B", "A"]
    assert isinstance(results[3], ValueError) and "bad" in str(results[3])
    assert calls == [["a", "b", "bad"]], "one trip for the whole wave, a repeated key asked once"


@pytest.mark.asyncio
async def test_groups_never_share_and_a_missing_key_is_named():
    calls: list[list[str]] = []

    async def batch(keys):
        calls.append(list(keys))
        return {k: k for k in keys if k != "gone"}

    co: Coalescer[str, str] = Coalescer()
    a, b, gone = await asyncio.gather(
        co.load("person-1", "x", batch), co.load("person-2", "y", batch), co.load("person-1", "gone", batch),
        return_exceptions=True,
    )
    assert (a, b) == ("x", "y")
    assert isinstance(gone, KeyError) and "gone" in str(gone)
    assert sorted(map(sorted, calls)) == [["gone", "x"], ["y"]]


@pytest.mark.asyncio
async def test_a_failed_batch_fails_every_caller_and_a_full_batch_goes_at_once():
    async def boom(keys):
        raise RuntimeError("store down")

    co: Coalescer[str, str] = Coalescer(window_s=10, max_batch=2)
    out = await asyncio.wait_for(
        asyncio.gather(co.load("g", "1", boom), co.load("g", "2", boom), return_exceptions=True), timeout=1
    )
    assert all(isinstance(o, RuntimeError) for o in out)
    assert co.batches == 1
