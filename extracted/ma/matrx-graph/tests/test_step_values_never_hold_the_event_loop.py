"""A large step value never freezes the event loop (PF-WF, 2026-11-02).

Live, 7 days on aidream-api: the step loop's own CPU — the output fingerprint, value
interning, event screening — froze the event loop 240+ times, up to 66 s, and every other
run on the server waited. Each of those passes now runs in a worker thread for a large
value. A thread spy proves the heavy pass ran off the loop thread (red before: it ran on
the loop); a 10 ms ticker adds a loose wall bound.
"""

from __future__ import annotations

import asyncio
import threading
import time
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

import pytest

from matrx_graph.checkpoint.values import event_payload_row, outcome_input_row, run_pure_off_loop
from matrx_graph.content_ir.envelope import (
    ir_metadata_for_verified_output,
    ir_metadata_for_verified_output_async,
)
from matrx_graph.content_ir.fingerprint import fingerprint_text, fingerprint_text_off_loop

# A loose wall bound only (shared CI runners are noisy): the exact proof is the thread spy.
# The sync passes below hold the loop for hundreds of ms to seconds.
_LOOSE_GAP_S = 0.5


def _big_value(n: int = 9_000) -> dict[str, Any]:
    """~3 MB, many leaves: the shape of a search/scrape step output."""
    return {
        "results": [
            {"i": i, "title": f"Result {i} — ünïcödé", "snippet": "word " * 40, "tags": ["a", "b", str(i)]}
            for i in range(n)
        ]
    }


async def _max_loop_gap(work: Callable[[], Awaitable[Any]]) -> tuple[float, Any]:
    gaps: list[float] = []
    done = asyncio.Event()

    async def ticker() -> None:
        last = time.perf_counter()
        while not done.is_set():
            await asyncio.sleep(0.01)
            now = time.perf_counter()
            gaps.append(now - last - 0.01)
            last = now

    tick = asyncio.create_task(ticker())
    await asyncio.sleep(0.03)
    try:
        result = await work()
    finally:
        await asyncio.sleep(0.03)
        done.set()
        await tick
    return max(gaps), result


def _thread_spy(monkeypatch: pytest.MonkeyPatch, module: Any, name: str) -> list[int]:
    """Record the thread every call of ``module.name`` runs on."""
    seen: list[int] = []
    real = getattr(module, name)

    def spy(*args: Any, **kwargs: Any) -> Any:
        seen.append(threading.get_ident())
        return real(*args, **kwargs)

    monkeypatch.setattr(module, name, spy)
    return seen


@pytest.mark.asyncio
async def test_the_fingerprint_of_a_large_output_is_hashed_off_the_loop(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_graph.content_ir import fingerprint as fp

    value = _big_value()
    expected = ir_metadata_for_verified_output(value, "x_kind")
    hashed_on = _thread_spy(monkeypatch, fp, "fingerprint_text")
    gap, meta = await _max_loop_gap(lambda: ir_metadata_for_verified_output_async(value, "x_kind"))
    assert meta == expected  # byte-identical envelope
    assert hashed_on and threading.get_ident() not in hashed_on, "a large output was fingerprinted on the loop"
    assert gap < _LOOSE_GAP_S, f"the loop froze {gap:.3f}s while a step output was fingerprinted"


@pytest.mark.asyncio
async def test_interning_and_screening_a_large_value_run_off_the_loop(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_graph.checkpoint import values as values_mod

    value = _big_value(40_000)
    expected_row = outcome_input_row(value, 1024)
    event = {"event": "node_completed", "output": value}
    expected_event = event_payload_row(event, 1024)
    walked_on = _thread_spy(monkeypatch, values_mod, "_intern")
    gap, row = await _max_loop_gap(lambda: run_pure_off_loop(outcome_input_row, value, 1024))
    assert row == expected_row
    assert walked_on and threading.get_ident() not in walked_on, "a large value was interned on the loop"
    assert gap < _LOOSE_GAP_S, f"the loop froze {gap:.3f}s while a step value was interned"
    walked_on.clear()
    ev_row = await run_pure_off_loop(event_payload_row, event, 1024)
    assert ev_row == expected_event
    assert walked_on and threading.get_ident() not in walked_on, "a large event was screened on the loop"


def test_the_step_value_passes_are_called_through_the_off_loop_door() -> None:
    """Every production site that interns, screens or sizes a step value goes through
    ``run_pure_off_loop`` (a direct call puts the walk back on the event loop)."""
    root = Path(__file__).resolve().parents[1] / "matrx_graph"
    sites = {
        "checkpoint/postgres.py": ("run_pure_off_loop(outcome_input_row", "_columns_and_size,"),
        "checkpoint/value_store.py": ("run_pure_off_loop(event_payload_row",),
        "once.py": ("run_pure_off_loop(outcome_input_row",),
        "db/run_store.py": ("run_pure_off_loop(outcome_input_row",),
    }
    for rel, needles in sites.items():
        text = (root / rel).read_text()
        for needle in needles:
            assert needle in text, f"{rel}: {needle!r} missing"
        direct = text.count("outcome_input_row(") + text.count("event_payload_row(")
        assert direct == 0, f"{rel} calls a value pass directly on the loop"
    postgres = (root / "checkpoint/postgres.py").read_text()
    passes = ("_columns_and_size", "_earlier_columns")  # the current checkpoint; a chain's earlier ones
    for name in passes:
        body = postgres.split(f"def {name}", 1)[1].split("run_pure_off_loop(", 1)[0]
        assert "checkpoint_columns(" in body, f"{name} no longer builds the columns"
        assert f"run_pure_off_loop(\n                {name}" in postgres or f"run_pure_off_loop(\n            {name}" in postgres, name
    assert postgres.count("checkpoint_columns(") == len(passes), (
        "the checkpoint's columns are interned outside the off-loop passes"
    )


@pytest.mark.asyncio
async def test_a_small_value_stays_inline_and_the_fingerprint_matches_either_way() -> None:
    assert await run_pure_off_loop(outcome_input_row, {"a": 1}, 1024) == ({"a": 1}, {})
    for text in ("short", "x" * 70_000 + "🎉"):
        assert await fingerprint_text_off_loop(text) == fingerprint_text(text)


@pytest.mark.asyncio
async def test_a_value_changed_under_the_thread_is_answered_on_the_loop_and_other_errors_raise() -> None:
    big = _big_value()
    calls: list[int] = []

    def changed_once(value: Any) -> int:
        calls.append(threading.get_ident())
        if len(calls) == 1:
            raise RuntimeError("dictionary changed size during iteration")
        return len(value["results"])

    assert await run_pure_off_loop(changed_once, big) == 9_000
    assert calls[0] != threading.get_ident() and calls[1] == threading.get_ident()

    def deep(_value: Any) -> int:
        raise RecursionError("maximum recursion depth exceeded")

    with pytest.raises(RecursionError):
        await run_pure_off_loop(deep, big)


def test_models_count_by_their_fields() -> None:
    """A checkpoint's next_invocations / pending_bindings are models: a fan-out of many large
    inputs must read as large (review of 118310e66: a model counted as one node)."""
    from pydantic import BaseModel

    from matrx_graph.checkpoint.values import is_large_value

    class Inv(BaseModel):
        node_id: str
        inputs: dict[str, Any]

    many = [Inv(node_id=f"n{i}", inputs={"text": "y" * 500}) for i in range(500)]
    assert is_large_value(many)
    assert not is_large_value([Inv(node_id="n", inputs={"a": 1})])


def test_the_step_loop_calls_only_the_off_loop_envelope() -> None:
    """The scheduler and the frontend output step must use the awaitable form."""
    root = Path(__file__).resolve().parents[1] / "matrx_graph"
    for rel in ("executor/scheduler.py", "nodes/output/to_frontend.py"):
        text = (root / rel).read_text()
        assert "ir_metadata_for_verified_output(" not in text, f"{rel} calls the sync envelope on the loop"
        assert "ir_metadata_for_verified_output_async(" in text, rel


@pytest.mark.asyncio
async def test_a_resumed_legs_settled_outputs_are_decoded_off_the_loop(monkeypatch: pytest.MonkeyPatch) -> None:
    """event_loop_stall cdbb1070 (2026-11-17): ``settled_outputs`` decoded and walked every earlier
    step's output on the loop for 1.14 s when a workflow resumed."""
    from matrx_graph.checkpoint import postgres as pg

    big = _big_value()

    class _Query:
        def __init__(self, filters: dict[str, Any]) -> None:
            self.filters = filters

        async def values(self, *fields: str) -> list[dict[str, Any]]:
            if "output" in fields:
                return [{"node_id": "a", "output": big}]
            return [{"id": "row-a", "node_id": "a", "step": 1, "dispatch_id": "", "item_index": 0, "attempt": 0, "error": None}]

    class _Outcome:
        @staticmethod
        def filter(**filters: Any) -> _Query:
            return _Query(filters)

    monkeypatch.setattr(pg, "get_model", lambda _name: _Outcome)
    walked_on = _thread_spy(monkeypatch, pg, "referenced_hashes")
    got = await pg.PostgresCheckpointer().settled_outputs("run-1", {"a"})
    assert got == {"a": big}
    assert walked_on and threading.get_ident() not in walked_on, "a large settled output was walked on the loop"
