"""A run interns each large value ONCE per limit, though its events, outcome rows, checkpoints and output all name it.

2026-11-09 (L-SPEED round 3, research pick): every large step output was walked and hashed ~7 times a run — its
node_completed event, the next step's node_started event, its outcome row, every checkpoint (4 KB grain), the run
output (4 KB grain) and the run_completed event's ``last_outputs`` — each interned on its own. The process now
remembers a large value it interned (live object + limit → digest); a later write of the SAME object whose run has
COMMITTED that digest uses the reference with no walk (``checkpoint.values`` § ONE INTERNING PER VALUE).

Red before: with nothing remembered (``INTERNED_CACHE_MAX_BYTES = 0``) the run's life below hashes every output
once per write. Green: once per limit (32 KB events/outcomes, 4 KB checkpoints/run output), and every row still
resolves to exactly the value it names.

The soundness guard (a delivered value is never edited in place) is proven here too: a cached value that changed
size is a miss (re-interned, its new digest); a same-size edit raises under ``VERIFY_INTERNED_VALUES`` (on for this
whole suite, conftest); a step that edits its delivered inputs fails its run, naming itself.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_graph import (
    ActionRegistry,
    ActionTier,
    Definition,
    MemoryCheckpointer,
    NodeCategory,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_node,
)
from matrx_graph.checkpoint import values as values_module
from matrx_graph.checkpoint.value_store import run_output_row
from matrx_graph.checkpoint.values import (
    DeliveredValueChangedInPlaceError,
    InternMemo,
    checkpoint_row,
    clear_interned_cache,
    event_payload_row,
    outcome_input_row,
    referenced_hashes,
    resolve_values,
)
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import make_app_context

EVENT = 32768
PIECE = 4096
STEPS = 4


class _HashedBytes:
    def __init__(self) -> None:
        self.total = 0

    def sha256(self, data: bytes = b"") -> Any:
        self.total += len(data)
        return hashlib.sha256(data)


def _rows(step: int) -> list[dict[str, Any]]:
    return [{"source": f"s{step}_{i}", "body": "x" * 3000, "score": i} for i in range(80)]


def _json(value: Any) -> Any:
    return json.loads(json.dumps(value, default=str))


def _a_runs_life(committed: set[str], store: dict[str, Any]) -> list[tuple[Any, Any]]:
    """Every write a run of STEPS chained steps makes, in order, each 'committed' as it lands.

    Returns (row form, the value it must resolve to) for each write."""
    written: list[tuple[Any, Any]] = []

    def commit(values: dict[str, Any]) -> None:
        store.update(values)
        committed.update(values)

    outputs: dict[str, Any] = {}
    previous: Any = None
    for step in range(STEPS):
        output = {"rows": _rows(step)}
        if previous is not None:
            started, values = event_payload_row({"event": "node_started", "inputs": {"rows": previous["rows"]}}, EVENT, committed)
            commit(values)
            written.append((started["inputs"], {"rows": previous["rows"]}))
        done, values = event_payload_row({"event": "node_completed", "output": output}, EVENT, committed)
        commit(values)
        written.append((done["output"], output))
        row, values = outcome_input_row(output, EVENT, InternMemo(committed))
        commit(values)
        written.append((row, output))
        outputs[f"n{step}"] = output
        memo = InternMemo(committed)
        columns, values = checkpoint_row(
            channel_values=dict(outputs), pending_bindings={}, next_invocations=[], interrupt_payload=None,
            max_inline_bytes=PIECE, memo=memo,
        )
        commit(values)
        written.append((columns["channel_values"], dict(outputs)))
        previous = output
    final, values = event_payload_row({"event": "run_completed", "last_outputs": outputs}, EVENT, committed)
    commit(values)
    written.append((final["last_outputs"], outputs))
    row, values = run_output_row(outputs, EVENT, PIECE, committed)
    commit(values)
    written.append((row, outputs))
    return written


def _hashed_by_a_run(monkeypatch) -> tuple[int, list[tuple[Any, Any]], dict[str, Any]]:
    # Counted as production runs it: the suite's proof switch re-hashes every hit on purpose.
    monkeypatch.setattr(values_module, "VERIFY_INTERNED_VALUES", False)
    clear_interned_cache()
    hashed = _HashedBytes()
    monkeypatch.setattr(values_module, "hashlib", hashed)
    store: dict[str, Any] = {}
    written = _a_runs_life(set(), store)
    return hashed.total, written, store


def test_a_run_hashes_each_large_value_once_per_limit(monkeypatch) -> None:
    total, written, store = _hashed_by_a_run(monkeypatch)
    one = len(json.dumps(_rows(0), sort_keys=True, separators=(",", ":")).encode())
    # Each output is hashed at most once at 32 KB and once at 4 KB (plus the small 4 KB pieces' own text);
    # the run's ~7 writes of it add nothing more.
    assert total < one * STEPS * 3, (
        f"the run hashed {total:,} bytes for {STEPS} outputs of {one:,} — each large value must be interned once "
        "per limit, not again by every event, outcome, checkpoint and the run output"
    )
    stored = _json(store)
    for row, value in written:
        assert referenced_hashes(_json(row)) <= set(stored)
        assert resolve_values(_json(row), stored) == _json(value)


def test_with_nothing_remembered_every_write_hashes_again(monkeypatch) -> None:
    """The red side: the same life with the cache unable to hold anything."""
    monkeypatch.setattr(values_module, "INTERNED_CACHE_MAX_BYTES", 0)
    total, written, store = _hashed_by_a_run(monkeypatch)
    one = len(json.dumps(_rows(0), sort_keys=True, separators=(",", ":")).encode())
    assert total > one * STEPS * 5, total
    stored = _json(store)
    for row, value in written:
        assert resolve_values(_json(row), stored) == _json(value)


def test_a_reference_is_used_only_once_the_run_committed_it() -> None:
    clear_interned_cache()
    rows = _rows(9)
    first, store = outcome_input_row({"rows": rows}, EVENT, InternMemo(frozenset()))
    digest = next(iter(referenced_hashes(first)))
    # Not committed: walked again, and the value comes back in the store to be written.
    again, again_store = outcome_input_row({"rows": rows}, EVENT, InternMemo(frozenset()))
    assert again == first and digest in again_store
    # Committed: the reference, and nothing to write.
    hit, hit_store = outcome_input_row({"rows": rows}, EVENT, InternMemo({digest}))
    assert hit == first and hit_store == {}


def test_a_value_grown_in_place_is_interned_again() -> None:
    """Production's cheap check: a cached list that changed length is a miss, re-interned under its new digest."""
    clear_interned_cache()
    rows = _rows(3)
    first, store = outcome_input_row({"rows": rows}, EVENT, InternMemo(frozenset()))
    committed = set(store)
    rows.append({"source": "late", "body": "y", "score": -1})
    second, second_store = outcome_input_row({"rows": rows}, EVENT, InternMemo(committed))
    assert second != first
    assert resolve_values(_json(second), _json({**store, **second_store})) == _json({"rows": rows})


def test_a_same_size_edit_in_place_is_caught_by_the_proof_switch(monkeypatch) -> None:
    monkeypatch.setattr(values_module, "VERIFY_INTERNED_VALUES", True)
    clear_interned_cache()
    rows = _rows(4)
    _first, store = outcome_input_row({"rows": rows}, EVENT, InternMemo(frozenset()))
    rows[0] = {**rows[0], "score": 999}
    with pytest.raises(DeliveredValueChangedInPlaceError):
        outcome_input_row({"rows": rows}, EVENT, InternMemo(set(store)))


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _RowsIn(BaseModel):
    rows: Any = None  # Any: the step is handed the delivered object itself


class _Rows(BaseModel):
    rows: list[dict[str, Any]] = []


def _graph_with_an_editing_step() -> tuple[Any, NodeRegistry]:
    nreg, areg = NodeRegistry(), ActionRegistry()

    @register_node(name="test.makes_rows", category=NodeCategory.DATA, determinism=ActionTier.PURE,
                   input_schema=_In, output_schema=_Rows, node_registry=nreg, action_registry=areg)
    async def _make(_ctx, inputs: _In) -> NodeResult[_Rows]:
        return success(_Rows(rows=_rows(0)))

    @register_node(name="test.edits_its_input", category=NodeCategory.DATA, determinism=ActionTier.PURE,
                   input_schema=_RowsIn, output_schema=_Rows, node_registry=nreg, action_registry=areg)
    async def _edit(_ctx, inputs: _RowsIn) -> NodeResult[_Rows]:
        delivered = inputs.rows
        delivered[0]["score"] = 999  # edits the value it was handed, in place
        return success(_Rows(rows=delivered))

    definition = Definition.model_validate({
        "nodes": [
            {"id": "a", "type": "test.makes_rows", "position": {"x": 0, "y": 0}, "data": {}},
            {"id": "b", "type": "test.edits_its_input", "position": {"x": 100, "y": 0}, "data": {}},
        ],
        "edges": [{"id": "e", "source": "a", "target": "b", "data": {"kind": "data"}}],
    })
    return compile_graph(definition, registry=nreg), nreg


async def test_a_step_that_edits_its_arguments_never_changes_the_delivered_value() -> None:
    """The engine hands every step a rebuilt copy of its arguments (``_gate_step_inputs``): the step's edit
    stays in its own copy, the delivered output of ``a`` is untouched, and the proof switch sees no change."""
    graph, nreg = _graph_with_an_editing_step()
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=nreg).run(
        run_id="edits-a-copy", inputs={}
    )
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["a"]["rows"][0]["score"] == 0
    assert result.last_outputs["b"]["rows"][0]["score"] == 999


async def test_without_the_argument_copy_the_proof_switch_fails_the_run(monkeypatch) -> None:
    """Red side of the guard: with the copy removed, the same step edits the delivered value, and the run fails
    naming the step instead of storing a value under a stale reference."""
    from matrx_graph.executor import scheduler as scheduler_module

    monkeypatch.setattr(scheduler_module, "_gate_step_inputs", lambda merged, _schema: (merged, []))
    graph, nreg = _graph_with_an_editing_step()
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=nreg).run(
        run_id="edits-in-place", inputs={}
    )
    assert result.status in (RunStatus.FAILED, RunStatus.ERRORED), result.status
    assert "edited its delivered inputs in place" in json.dumps(_json(result.error)), result.error
