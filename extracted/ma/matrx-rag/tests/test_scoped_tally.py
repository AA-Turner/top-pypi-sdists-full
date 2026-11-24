"""A run's cost is its own calls only — never a concurrent run's.

SUT: ``matrx_rag._observability.scoped_tally``. The content-processing orchestrator used to diff the
process-wide tally before/after a run, so seven files processed together each reported every other
file's page cleanups (2026-11-12, ~4x real spend). Two overlapping runs here must each see exactly
their own buckets, while the process tally still sees both.
"""

from __future__ import annotations

import asyncio

from matrx_rag import _observability as obs


def _chat(cost: float) -> None:
    obs._tally.record(
        provider="openai",
        kind="chat",
        purpose="pdf_cleanup",
        model="m",
        input_chars=1,
        output_chars=1,
        elapsed_ms=1,
        cost_usd=cost,
        cost_is_exact=True,
    )


def _cost(snapshot: dict) -> float:
    return round(sum(b["estimated_cost_usd"] for b in snapshot["buckets"]), 6)


def test_overlapping_runs_each_count_only_their_own_calls() -> None:
    before = _cost(obs.tally_snapshot())
    results: dict[str, float] = {}

    async def run(name: str, costs: list[float]) -> None:
        with obs.scoped_tally() as tally:
            for c in costs:
                _chat(c)
                await asyncio.sleep(0)  # interleave with the other run
            results[name] = _cost(tally.snapshot())

    async def both() -> None:
        await asyncio.gather(run("a", [0.1, 0.2, 0.3]), run("b", [1.0, 2.0]))

    asyncio.run(both())
    assert results == {"a": 0.6, "b": 3.0}
    assert round(_cost(obs.tally_snapshot()) - before, 6) == 3.6


def test_cache_hits_land_in_the_run_scope_without_cost() -> None:
    with obs.scoped_tally() as tally:
        obs._tally.record_cache_served(
            provider="openai", kind="embedding", purpose="embedding", model="m",
            hits=4, input_chars=10, cost_saved_usd=0.02,
        )
        snap = tally.snapshot()
    (bucket,) = snap["buckets"]
    assert bucket["cache_hits"] == 4 and bucket["estimated_cost_usd"] == 0.0


def test_calls_outside_a_scope_are_not_counted_in_it() -> None:
    _chat(5.0)
    with obs.scoped_tally() as tally:
        _chat(0.5)
    _chat(7.0)
    assert _cost(tally.snapshot()) == 0.5
