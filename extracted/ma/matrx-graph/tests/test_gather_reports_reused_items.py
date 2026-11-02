"""A For Each says which items reused a saved result — ``control.gather.reused_indexes``.

Run once per key (``data.once``) lets a fanned step answer an item from a stored success
(outcome ``source="reused"``). The gather closing the For Each used to report values,
item indexes and holes but not which items were reused, so no workflow could count them
(``mandate.run_each`` returned ``reused: null``). Driven through the real Scheduler and the
real in-memory step-result store; the step counts its real executions.
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from typing import Any

import pytest

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    RunStatus,
    Scheduler,
    compile_graph,
)
from matrx_graph import knobs
from matrx_graph.nodes.control.gather import GatherConfig, GatherExecutor, GatherInput
from matrx_graph.once import MemoryStepResultStore, configure_step_result_store
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.result import NodeResult, failure, success
from tests._fixtures import FakeEmitter
from tests.test_once_per_key import ORG_A, WF, _Cfg, _ctx, _In, _Out, _registry, _Step


class _Item(_Step):
    """A paid per-item step that refuses the item ``"bad"`` (a failed item → a hole)."""

    def __init__(self) -> None:
        super().__init__("test.item")

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        data = inputs.model_dump(mode="json")
        if "value" in data:
            self.calls += 1
            self.seen.append(data)
        if data.get("value") == "bad":
            return failure(code="Boom", message="the provider refused this item")
        return success(_Out(answer=f"done:{data.get('value')}"))


@pytest.fixture
def store() -> Iterator[MemoryStepResultStore]:
    s = MemoryStepResultStore()
    configure_step_result_store(s)
    knobs._cache[knobs.ONCE_FEATURE] = (
        time.monotonic() + 10**9,
        {"lease_seconds": 5, "wait_poll_seconds": 1, "keep_days_default": 30},
    )
    try:
        yield s
    finally:
        configure_step_result_store(None)
        knobs._cache.pop(knobs.ONCE_FEATURE, None)


def _for_each(items: list[str]) -> dict[str, Any]:
    return {
        "entry_nodes": ["fan"],
        "nodes": [
            {"id": "fan", "type": "control.map", "position": {"x": 0, "y": 0},
             "data": {"config": {"target_node_id": "work", "payload_key": "value"},
                      "input": {"items": items}}},
            {"id": "work", "type": "test.item", "position": {"x": 1, "y": 0},
             "data": {"once": {"key": ["value"], "scope": "workflow"}, "on_item_failure": "hole"}},
            {"id": "gather", "type": "control.gather", "position": {"x": 2, "y": 0}, "data": {}},
        ],
        "edges": [{"id": "e_wg", "source": "work", "target": "gather", "data": {"kind": "data"}}],
    }


async def _gather(items: list[str], step: _Item, run_id: str) -> dict[str, Any]:
    registry = _registry(step)
    graph = compile_graph(Definition.model_validate(_for_each(items)), registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), _ctx(FakeEmitter(), ORG_A),
                          registry=registry, definition_id=WF)
    result = await scheduler.run(run_id=run_id, max_steps=20)
    assert result.status is RunStatus.COMPLETED, result.error
    return (result.last_outputs or {})["gather"]


async def test_the_reused_item_is_named_by_its_index(store):
    step = _Item()
    await _gather(["b"], step, "run-1")
    assert step.calls == 1
    out = await _gather(["a", "b", "c"], step, "run-2")
    assert step.calls == 3, "item 1 must not run again"
    assert out["item_indexes"] == [0, 1, 2]
    assert out["reused_indexes"] == [1]
    assert [v["answer"] for v in out["values"]] == ["done:a", "done:b", "done:c"]


async def test_nothing_reused_reports_an_empty_list(store):
    step = _Item()
    out = await _gather(["a", "b", "c"], step, "run-1")
    assert step.calls == 3
    assert out["reused_indexes"] == []
    assert out["count"] == 3


async def test_holes_and_reused_items_are_reported_together(store):
    step = _Item()
    await _gather(["b"], step, "run-1")
    out = await _gather(["bad", "b", "c"], step, "run-2")
    assert [h["item_index"] for h in out["holes"]] == [0]
    assert out["holes"][0]["status"] == "failed"
    assert out["item_indexes"] == [1, 2]
    assert out["reused_indexes"] == [1]


async def test_gather_reads_the_reused_mark_off_succeeded_items_only():
    items = [
        {"item_index": 0, "status": "skipped", "value": {}, "error": None, "reused": False},
        {"item_index": 1, "status": "succeeded", "value": {"v": 1}, "error": None, "reused": True},
        {"item_index": 2, "status": "succeeded", "value": {"v": 2}, "error": None, "reused": False},
        # an aggregated delivery recorded before the mark existed carries no key: not reused
        {"item_index": 3, "status": "succeeded", "value": {"v": 3}, "error": None},
    ]
    result = await GatherExecutor().execute(None, GatherInput.model_validate({"items": items}), GatherConfig())
    assert result.result.reused_indexes == [1]
    assert result.result.skipped_indexes == [0]
    assert result.result.item_indexes == [1, 2, 3]
