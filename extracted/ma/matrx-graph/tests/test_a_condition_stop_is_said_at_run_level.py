"""A run a condition stopped says so at run level — never a bare ``completed`` (lane 11, 2026-10-02).

THE USE CASE: "When a Job's Stage changes, if Stage is Done, set Invoice Status to Ready".
Most changes are not "Done", so most runs end at the condition. Before, such a run was just
``completed`` — indistinguishable from one that set the invoice — and Runs could never show
"Condition not met". Now the condition step's output declares ``run_stop``; when the engine
prunes its conditional edge and nothing it feeds runs, ``RunResult.stopped`` carries
``{reason, says, step}`` and the run store writes it to ``workflow.run.metadata.stopped`` in
the completion statement.

THE BREAKS:
* the scheduler stops computing ``stopped`` (``test_a_pruned_condition_stops_the_run_with_its_reason``);
* it claims a stop when the next step DID run — through the edge, or because it was wired
  unconditionally (the second and third cases, a different expected value: None);
* the run store drops it on the way to the row (``test_the_completion_writes_the_reason``).
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)

from tests._fixtures import FakeEmitter, make_app_context

NOT_MET = {"reason": "condition_not_met", "says": "Condition not met"}


def _definition(passed: bool, edge: dict[str, Any]) -> Definition:
    expression = repr({"passed": passed, "run_stop": None if passed else NOT_MET})
    return Definition.model_validate(
        {
            "nodes": [
                {"id": "stage_is_done", "type": "data.transform", "position": {"x": 0, "y": 0},
                 "data": {"config": {"expression": expression}}},
                {"id": "set_invoice_ready", "type": "data.transform",
                 "position": {"x": 200, "y": 0},
                 "data": {"config": {"expression": "'INVOICE_READY'"}}},
            ],
            "edges": [{"id": "then", "source": "stage_is_done", "target": "set_invoice_ready",
                       "data": edge}],
        }
    )


CONDITIONAL = {"kind": "conditional", "condition": "inputs['passed']"}


@pytest.mark.parametrize(
    ("label", "passed", "edge", "expected"),
    [
        ("condition not met, edge pruned", False, CONDITIONAL,
         {**NOT_MET, "step": "stage_is_done"}),
        ("condition met, next step ran", True, CONDITIONAL, None),
        ("a stop declared but the next step wired unconditionally", False, {}, None),
    ],
)
async def test_a_pruned_condition_stops_the_run_with_its_reason(label, passed, edge, expected):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(_definition(passed, edge), registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    result = await scheduler.run(run_id=f"stop-{label}")
    assert result.status is RunStatus.COMPLETED, (label, result.error)
    assert result.stopped == expected, label


def _parallel_definition() -> Definition:
    """start → (condition → set_invoice_ready) AND start → notify_office (a parallel branch)."""
    expression = repr({"passed": False, "run_stop": NOT_MET})
    node = lambda nid, x, expr: {"id": nid, "type": "data.transform",  # noqa: E731
                                 "position": {"x": x, "y": 0},
                                 "data": {"config": {"expression": expr}}}
    return Definition.model_validate(
        {
            "nodes": [node("start", 0, "{'job': 1042}"), node("stage_is_done", 200, expression),
                      node("set_invoice_ready", 400, "'INVOICE_READY'"),
                      node("notify_office", 200, "'OFFICE_TOLD'")],
            "edges": [
                {"id": "a", "source": "start", "target": "stage_is_done", "data": {}},
                {"id": "then", "source": "stage_is_done", "target": "set_invoice_ready",
                 "data": CONDITIONAL},
                {"id": "b", "source": "start", "target": "notify_office", "data": {}},
            ],
        }
    )


async def test_a_parallel_branch_that_ran_keeps_the_stop_on_the_step():
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(_parallel_definition(), registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    result = await scheduler.run(run_id="stop-parallel")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "notify_office" in result.last_outputs
    assert result.stopped is None
    assert result.last_outputs["stage_is_done"]["run_stop"] == NOT_MET


async def test_the_completion_writes_the_reason(monkeypatch):
    from matrx_graph.db import run_store as module
    from matrx_graph.db.run_store import RunStore

    writes: list[dict[str, Any]] = []

    class _Result:
        rows_affected = 1
        updated_rows: list = []

    class _Model:
        @staticmethod
        async def update_where(filters, **values):
            writes.append(values)
            return _Result()

    async def _discard(_run_id):
        return None

    monkeypatch.setattr(module, "get_model", lambda _name: _Model)
    import matrx_graph.workers.queue as queue

    monkeypatch.setattr(queue, "discard_for_run", _discard)
    stop = {**NOT_MET, "step": "stage_is_done"}
    applied = await RunStore().apply_result(
        "6f1e2d3c-4b5a-4968-8776-655443322110",
        status=RunStatus.COMPLETED,
        steps_executed=1,
        output={"stage_is_done": {"passed": False}},
        interrupt=None,
        error=None,
        last_checkpoint_id=None,
        stopped=stop,
    )
    assert applied is True
    merged = writes[0]["metadata"]
    assert merged.args == ("metadata",) and merged.value == {"stopped": stop}, vars(merged)
    assert writes[0]["status"] == "completed"

    # A later finish with no stop REPLACES the earlier reason (null), never keeps it.
    await RunStore().apply_result(
        "6f1e2d3c-4b5a-4968-8776-655443322110",
        status=RunStatus.COMPLETED,
        steps_executed=2,
        output={"set_invoice_ready": "INVOICE_READY"},
        interrupt=None,
        error=None,
        last_checkpoint_id=None,
    )
    assert writes[1]["metadata"].value == {"stopped": None}, vars(writes[1]["metadata"])
