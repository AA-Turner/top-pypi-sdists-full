"""A run whose result is tens of megabytes COMPLETES, and its result reads back whole.

2026-10-27: child run 61b8404f (pages.plan_reading) finished all 59 steps and ended failed with
``final_write_failed``: the engine wrote every step's output into ``workflow.run.output`` and the one
21.7 MB row (one step 11 MB) timed out. 2026-10-05: an 11 MB row did the same (run 70601b15).

The rule now: a step output over the ``workflow.run_output.inline_value_max_bytes`` knob goes by
reference into the run's value store (``workflow.checkpoint_value``); the row keeps the step id and
small references; ``RunStore.load`` — what every server reader of a run uses — resolves them.

The fake run table below times out on a large output write exactly like the live one, so these tests
are red on the old engine (the 20 MB write raised and the run ended ``final_write_failed``).
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from matrx_graph.checkpoint import value_store
from matrx_graph.types.primitives import RunStatus

RUN = "7a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d"
TIMEOUT_BYTES = 2_000_000  # a write carrying more output than this "times out", like the live row did


def _row(run_id: str) -> dict[str, Any]:
    keys = (
        "thread_id", "parent_run_id", "definition_id", "definition_version_id", "definition_hash", "input",
        "output", "error", "interrupt_payload", "last_checkpoint_id", "created_by", "organization_id",
        "project_id", "task_id", "conversation_id", "agent_id", "agent_version_id", "created_at",
        "started_at", "completed_at", "metadata",
    )
    row: dict[str, Any] = dict.fromkeys(keys)
    row.update(id=run_id, thread_id=run_id, definition_id=run_id, status="running", steps_executed=0)
    return row


class FakeRunTable:
    """``workflow.run`` for ``RunStore``: guarded updates, jsonb merge, and a statement timeout."""

    def __init__(self) -> None:
        self.rows: dict[str, dict[str, Any]] = {}
        self.output_writes: list[int] = []

    def model(self) -> Any:
        table = self

        class _Result:
            def __init__(self, n: int) -> None:
                self.rows_affected = n
                self.updated_rows: list[Any] = []

        class _Query:
            def __init__(self, run_id: str) -> None:
                self.run_id = run_id

            async def values(self, *fields: str) -> list[dict[str, Any]]:
                row = table.rows.get(self.run_id)
                if row is None:
                    return []
                return [json.loads(json.dumps(row, default=str))]

        class _Model:
            @staticmethod
            async def update_where(filters: dict[str, Any], **values: Any) -> Any:
                row = table.rows.get(filters["id"])
                if row is None:
                    return _Result(0)
                if row["status"] in filters.get("status__not_in", ()):
                    return _Result(0)
                if "status__in" in filters and row["status"] not in filters["status__in"]:
                    return _Result(0)
                out = values.get("output")
                if out is not None:
                    sent = len(json.dumps(getattr(out, "value", out), default=str))
                    table.output_writes.append(sent)
                    if sent > TIMEOUT_BYTES:
                        raise TimeoutError(f"QueryTimeoutError: query timed out during execute_query ({sent} bytes)")
                for key, value in values.items():
                    if type(value).__name__ == "JsonbMerge":
                        value = {**(row.get(key) or {}), **value.value}
                    row[key] = value
                return _Result(1)

            @staticmethod
            def filter(**kw: Any) -> Any:
                return _Query(kw["id"])

        return _Model


@pytest.fixture
def wired(monkeypatch: pytest.MonkeyPatch) -> tuple[FakeRunTable, dict[str, Any]]:
    from matrx_graph import knobs
    from matrx_graph.db import run_store as module
    from matrx_graph.workers import queue

    table = FakeRunTable()
    model = table.model()
    monkeypatch.setattr(module, "get_model", lambda _name: model)

    async def _no_jobs(_run_id: str) -> None:
        return None

    monkeypatch.setattr(queue, "discard_for_run", _no_jobs)

    stored: dict[str, Any] = {}

    async def _store(run_id: str, values: dict[str, Any], *, organization_id: str | None = None) -> None:
        stored.update(json.loads(json.dumps(values)))

    async def _load(run_id: str, hashes: Any) -> dict[str, Any]:
        from matrx_graph.checkpoint.values import resolve_values

        return {h: resolve_values(stored[h], stored) for h in hashes if h in stored}

    async def _knob() -> int:
        return 1_048_576

    monkeypatch.setattr(value_store, "store_run_values", _store)
    monkeypatch.setattr(value_store, "load_run_values", _load)
    monkeypatch.setattr(value_store, "_store_available", lambda: True)
    monkeypatch.setattr(knobs, "run_output_inline_value_max_bytes", _knob, raising=False)
    table.rows[RUN] = _row(RUN)
    return table, stored


def _big_output() -> dict[str, Any]:
    pages = [{"url": f"https://example.com/p{i}", "text": f"page {i} " + "x" * 20_000} for i in range(1000)]
    return {
        "plan": {"__kind": "page_plan", "pages": pages, "count": len(pages)},  # ~20 MB
        "brief": {"title": "Small step", "count": 3},
    }


async def test_a_20_mb_result_completes_and_reads_back_whole(wired) -> None:
    from matrx_graph.db.run_store import RunStore

    table, stored = wired
    output = _big_output()
    assert len(json.dumps(output)) > 20_000_000

    applied = await RunStore().apply_result(
        RUN, status=RunStatus.COMPLETED, steps_executed=59, output=output,
        interrupt=None, error=None, last_checkpoint_id=None,
    )

    assert applied is True
    assert table.rows[RUN]["status"] == "completed", table.rows[RUN].get("error")
    assert max(table.output_writes) <= 1_048_576, table.output_writes
    row_output = table.rows[RUN]["output"]
    assert row_output["brief"] == output["brief"], "a small step stays inline"
    assert set(row_output["plan"]) == {"__kind", "pages", "count"}, "the large step keeps its keys"
    assert row_output["plan"]["__kind"] == "page_plan" and row_output["plan"]["count"] == 1000
    assert stored, "the large values went to the run's value store"

    loaded = await RunStore().load(RUN)
    assert loaded is not None
    assert loaded["output"] == output, "every reader of the run gets exactly what the run produced"


async def test_a_resumed_leg_merges_by_reference_without_losing_the_first_leg(wired) -> None:
    from matrx_graph.db.run_store import RunStore

    table, _ = wired
    first = {"plan": _big_output()["plan"]}
    await RunStore().mark_paused(RUN, steps_executed=10, output=first)
    table.rows[RUN]["status"] = "running"
    await RunStore().mark_completed(RUN, output={"brief": {"count": 1}}, steps_executed=20)

    loaded = await RunStore().load(RUN)
    assert loaded is not None
    assert loaded["output"]["plan"] == first["plan"] and loaded["output"]["brief"] == {"count": 1}


async def test_a_reference_whose_value_is_gone_raises_for_every_reader_that_hands_it_on(wired) -> None:
    """A missing value never flows on as data: the default read raises a named error; only the display read
    (GET /runs/{id}) asks for the honest marker."""
    from matrx_graph.checkpoint.values import REF_KEY
    from matrx_graph.db.run_store import RunOutputValueMissingError, RunStore

    table, _ = wired
    table.rows[RUN]["output"] = {"plan": {REF_KEY: "f" * 64}, "brief": {"count": 1}}
    with pytest.raises(RunOutputValueMissingError) as raised:
        await RunStore().load(RUN)
    assert raised.value.run_id == RUN and raised.value.missing == ["f" * 64]
    assert "run_output_value_missing" in str(raised.value)

    shown = await RunStore().load(RUN, missing="mark")
    assert shown is not None
    assert shown["output"]["brief"] == {"count": 1}
    marker = shown["output"]["plan"]
    assert marker["output_elided"] is True and marker["missing"] is True, marker
    assert REF_KEY not in json.dumps(shown["output"]), "a raw reference never reaches a reader"


async def test_an_owner_or_status_read_never_touches_the_value_store(wired, monkeypatch) -> None:
    from matrx_graph.db.run_store import RunStore

    table, _ = wired
    await RunStore().apply_result(
        RUN, status=RunStatus.COMPLETED, steps_executed=59, output=_big_output(),
        interrupt=None, error=None, last_checkpoint_id=None,
    )
    reads: list[Any] = []

    async def _counted(run_id: str, hashes: Any) -> dict[str, Any]:
        reads.append(hashes)
        return {}

    monkeypatch.setattr(value_store, "load_run_values", _counted)
    row = await RunStore().load(RUN, resolve_output=False)
    assert row is not None and row["status"] == "completed" and row["created_by"] is None
    assert reads == [], "an owner/status read loads no stored values"
    assert len(json.dumps(row["output"])) <= 1_048_576


async def test_many_resumed_legs_never_rebuild_a_row_over_the_knob(wired) -> None:
    """Each leg's step is under the knob alone, but the row MERGES legs: sized alone, five 600 KB legs built a
    3 MB row. Sized against the row it merges into, earlier large steps move by reference too."""
    from matrx_graph.db.run_store import RunStore

    table, _ = wired
    legs = {f"leg_{i}": {"__kind": "notes", "text": f"{i} " + "z" * 600_000} for i in range(5)}
    for i, (step, out) in enumerate(legs.items()):
        if i % 2:
            await RunStore().mark_paused(RUN, steps_executed=i + 1, output={step: out})
        else:
            await RunStore().mark_interrupted(
                RUN, steps_executed=i + 1, output={step: out}, interrupt_payload={"prompt": f"q{i}"}
            )
        table.rows[RUN]["status"] = "running"
        size = len(json.dumps(table.rows[RUN]["output"]))
        assert size <= 1_048_576, f"after leg {i + 1} the row is {size} bytes"
    table.rows[RUN]["status"] = "running"
    await RunStore().mark_completed(RUN, output={"brief": {"count": 1}}, steps_executed=9)
    assert len(json.dumps(table.rows[RUN]["output"])) <= 1_048_576

    loaded = await RunStore().load(RUN)
    assert loaded is not None
    assert loaded["output"] == {**legs, "brief": {"count": 1}}, "every leg reads back whole"


async def test_a_missing_value_among_many_is_found_in_batched_reads(wired, monkeypatch) -> None:
    """The missing-value path reads in batches: 60 references, one gone, is ONE read (not 61), and a value
    whose NESTED value is gone is isolated by halving (a handful of reads), never one read per hash."""
    from matrx_graph.checkpoint.values import REF_KEY, RunOutputValueMissingError

    _, stored = wired
    digests = [f"{i:064x}" for i in range(60)]
    for d in digests[1:]:
        stored[d] = {"v": d}
    output = {f"s{i}": {REF_KEY: d} for i, d in enumerate(digests)}
    calls: list[int] = []
    real = value_store.load_run_values

    async def _counted(run_id: str, hashes: Any) -> dict[str, Any]:
        calls.append(len(list(hashes)))
        return await real(run_id, hashes)

    monkeypatch.setattr(value_store, "load_run_values", _counted)
    shown = await value_store.resolve_run_output(RUN, output, missing="mark")
    assert shown["s0"]["missing"] is True and shown["s1"] == {"v": digests[1]}
    assert len(calls) == 1, calls

    # A stored value that references a value which is gone: the batch read raises; halving isolates it.
    stored[digests[0]] = {"inner": {REF_KEY: "e" * 64}}
    calls.clear()
    shown = await value_store.resolve_run_output(RUN, output, missing="mark")
    assert shown["s0"]["missing"] is True and shown["s59"] == {"v": digests[59]}
    assert len(calls) <= 15, calls
    with pytest.raises(RunOutputValueMissingError):
        await value_store.resolve_run_output(RUN, output)


def test_the_row_stays_under_the_knob_when_many_mid_size_steps_add_up() -> None:
    from matrx_graph.checkpoint.value_store import run_output_row

    output = {f"step_{i}": {"text": "y" * 300_000} for i in range(10)}  # 3 MB, no step over 1 MB
    row, values = run_output_row(output, 1_048_576, 4096)
    assert len(json.dumps(row)) <= 1_048_576
    assert set(row) == set(output) and values


def test_knob_zero_keeps_every_output_inline() -> None:
    from matrx_graph.checkpoint.value_store import run_output_row

    output = _big_output()
    row, values = run_output_row(output, 0, 4096)
    assert row is output and not values
