"""The checkpoint written beside the next step (task ``wf-checkpoint:<run>:<step>``) never holds the loop.

Live 2026-11-14 (event_loop_stall d1a3e7a2cabc8ef3, aidream-api): the watchdog named the task holding a
1.2 s stall ``wf-checkpoint:f2ece685:1``. That checkpoint was 1,160 bytes, and the stack the same report
captured was a step's own work (``web.read_identity`` spawning a child process), so the name was not the
culprit. This test pins what the name claimed: a LARGE checkpoint, saved with its step's outcomes through
the same path the beside-write task runs (``save_checkpoint_with_outcomes``), lets a heartbeat on the loop
tick at every ``BOUND_S`` — the interning, JSON checks and sizing go to a worker thread
(``run_pure_off_loop``). The red half runs the same save with that door forced inline and shows the
heartbeat stalls past the bound, so the bound is one this test can see broken.

The collector is off while the heartbeat is measured: a full collection stops every thread for a time set
by the whole process heap (96-138 ms alone, 240-322 ms inside the full suite, measured 2026-11-14), which
no thread door changes and which is not this save's work. Both halves run the same way, so the red half
still proves the bound can break.
"""

from __future__ import annotations

import asyncio
import gc
import time
from typing import Any

from matrx_graph.checkpoint import postgres as pg
from matrx_graph.checkpoint.protocol import Checkpoint, NextInvocation, NodeOutcome
from matrx_graph.knobs import CheckpointWritePolicy

#: The longest the loop may go without running the heartbeat while a large checkpoint is saved.
BOUND_S = 0.15
GRAIN = 32768
POLICY = CheckpointWritePolicy(statement_timeout_ms=5000, max_retries=0, retry_backoff_ms=0, warn_bytes=10**9)


def _rows(tag: str, n: int = 24000) -> list[dict[str, Any]]:
    return [{"source": f"{tag}-{i}", "body": f"word {i} " * 12, "score": i, "tags": [tag, str(i)]} for i in range(n)]


def _large_save() -> tuple[Checkpoint, list[NodeOutcome]]:
    pages = {"rows": _rows("page")}
    found = {"rows": _rows("found")}
    checkpoint = Checkpoint(
        checkpoint_id="cp-large",
        run_id="run-large",
        thread_id="t",
        step=1,
        channel_values={"pages": pages, "found": found},
        next_invocations=[
            NextInvocation(node_id="compose", inputs={"pages": pages, "found": found}, step=2),
            NextInvocation(node_id="score", inputs={"rows": _rows("score")}, step=2),
        ],
    )
    outcomes = [
        NodeOutcome(run_id="run-large", step=1, node_id="read", attempt=1, output=pages, inputs={"found": found}),
    ]
    return checkpoint, outcomes


async def _save_and_measure(monkeypatch) -> tuple[float, list[dict[str, Any]]]:
    async def org(_run_id: str) -> str:
        return "org-1"

    async def policy() -> CheckpointWritePolicy:
        return POLICY

    async def grain() -> int:
        return GRAIN

    written: list[dict[str, Any]] = []

    async def write_once(self, checkpoint, *, columns, values, policy, outcomes=(), earlier=()):  # noqa: ANN001
        # The database round trip itself (asyncpg) is not under test: only what the save does on the loop.
        written.append({"columns": columns, "values": values, "outcomes": list(outcomes)})

    monkeypatch.setattr(pg, "_organization_for_run", org)
    monkeypatch.setattr(pg, "checkpoint_write_policy", policy)
    monkeypatch.setattr("matrx_graph.knobs.interning_grain", grain)
    monkeypatch.setattr("matrx_graph.knobs.event_inline_value_max_bytes", grain)
    monkeypatch.setattr(pg, "_value_store_available", lambda: True)
    monkeypatch.setattr(pg, "_available_versioned_kind_columns", lambda: ())
    monkeypatch.setattr(pg, "_available_input_envelope_columns", lambda: ("input",))
    monkeypatch.setattr(pg.PostgresCheckpointer, "_write_checkpoint_once", write_once)

    checkpoint, outcomes = _large_save()
    collecting = gc.isenabled()
    gc.collect()  # before the heartbeat starts: a collection here is not a stall of the save
    gc.disable()
    worst = 0.0
    done = asyncio.Event()
    beat = None
    try:
        async def heartbeat() -> None:
            nonlocal worst
            last = time.perf_counter()
            while not done.is_set():
                await asyncio.sleep(0.002)
                now = time.perf_counter()
                worst = max(worst, now - last)
                last = now

        beat = asyncio.create_task(heartbeat())
        await asyncio.sleep(0.01)  # the heartbeat is ticking before the save starts
        # The scheduler's beside-write task runs exactly this call (Scheduler._write_one).
        save = asyncio.create_task(
            pg.PostgresCheckpointer().save_checkpoint_with_outcomes(checkpoint, outcomes),
            name="wf-checkpoint:run-larg:1",
        )
        await save
    finally:
        if collecting:
            gc.enable()
        done.set()
        if beat is not None:
            await beat
    return worst, written


async def test_a_large_checkpoint_save_never_holds_the_loop_past_the_bound(monkeypatch) -> None:
    worst, written = await _save_and_measure(monkeypatch)

    assert written, "the save never reached its write"
    assert worst < BOUND_S, f"the loop went {worst * 1000:.0f} ms without the heartbeat (bound {BOUND_S * 1000:.0f} ms)"
    # It saved what it was given: the large values went by reference, the row stays small.
    [row] = written
    assert row["values"], "no value went by reference — the checkpoint was not large"
    assert len(str(row["columns"]["channel_values"])) < GRAIN


async def test_the_same_save_on_the_loop_breaks_the_bound(monkeypatch) -> None:
    async def inline(fn, *args, values=None):  # noqa: ANN001, ANN202 — the off-loop door, forced on the loop
        return fn(*args)

    monkeypatch.setattr(pg, "run_pure_off_loop", inline)
    worst, written = await _save_and_measure(monkeypatch)

    assert written
    assert worst > BOUND_S, (
        f"inline the save held the loop only {worst * 1000:.0f} ms — the checkpoint is too small to prove the bound"
    )
