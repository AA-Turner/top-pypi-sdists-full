"""One fanned item's own write refused by a busy database never ends the run (run 188426a6).

Live 2026-11-01: "Knowledge buckets" drained ~5,000 sources through ``rag.ingest_source`` under
``on_item_failure='hole'``. Hundreds of item failures became holes and the run went on — until one
item (step 45, item 38) FINISHED its work and the engine's own write of its success outcome was
canceled by Postgres (``LockContentionError``, 55P03 lock timeout, inside the declared write's
transaction, so matrx-orm never re-ran it). That exception escaped the attempt's failure ladder,
became the step's parking error, and the whole run went ``errored`` — reading "ran past its time
limit", because the class was lost under the note wrap and the prose said "lock timeout".

Three guards, each red before the fix:
* an escaped database-busy fault on a hole item becomes that item's hole and the run completes;
* the same fault on a step that is NOT a hole still parks (nothing is hidden);
* the parking error under the step's note wrap reads ``database_busy``, never ``timed_out``.
"""

from __future__ import annotations

import asyncio
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.checkpoint.protocol import NodeOutcome
from matrx_graph.executor.scheduler import append_failure_notes
from matrx_graph.failure import Cause, failure_from_exception, failure_from_text
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context

LOCK_SENTENCE = (
    "Postgres canceled this statement to break a lock collision (55P03) inside a caller-managed "
    "transaction, so nothing was re-run: canceling statement due to lock timeout"
)


class LockContentionError(Exception):
    """Stands in for matrx-orm's class of the same name (classified by class name, no ORM needed)."""


class _Open(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Out(BaseModel):
    model_config = ConfigDict(extra="allow")
    text: str = ""


class _Ingest:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.ingest_source",
        category=NodeCategory.DATA,
        display_name="Ingest",
        description="busy-database test node",
        input_schema=_Open,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        # Not PURE: its outcome is written at once (never deferred to the checkpoint),
        # exactly like the live ingest step.
        determinism=ActionTier.NON_DETERMINISTIC,
        retry=RetryPolicy(max_attempts=1),
    )

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Out]:
        return success(_Out(text=f"read {(inputs.model_extra or {}).get('value')}"))


class _BusyCheckpointer(MemoryCheckpointer):
    """Refuses the SUCCESS outcome of the item that read ``busy`` — the database was busy."""

    async def record_outcome(self, outcome: NodeOutcome) -> None:
        if outcome.error is None and (outcome.inputs or {}).get("value") == "busy":
            raise LockContentionError(LOCK_SENTENCE)
        await super().record_outcome(outcome)


def _definition(*, hole: bool) -> dict[str, Any]:
    ingest_data: dict[str, Any] = {"config": {}}
    if hole:
        ingest_data["on_item_failure"] = "hole"
    return {
        "nodes": [
            {
                "id": "each_source",
                "type": "control.map",
                "position": {"x": 0, "y": 0},
                "data": {
                    "config": {"target_node_id": "ingest", "payload_key": "value"},
                    "input": {"items": ["notes.pdf", "busy", "minutes.txt"]},
                },
            },
            {"id": "ingest", "type": "test.ingest_source", "position": {"x": 0, "y": 0}, "data": ingest_data},
            {"id": "gather", "type": "control.gather", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
        ],
        "edges": [{"id": "e_g", "source": "ingest", "target": "gather", "data": {"mappings": {"value": "text"}}}],
        "entry_nodes": ["each_source"],
    }


async def _run(*, hole: bool, run_id: str):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_Ingest(), overwrite=True)
    graph = compile_graph(Definition.model_validate(_definition(hole=hole)), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, _BusyCheckpointer(), make_app_context(emitter), registry=registry)
    result = await asyncio.wait_for(scheduler.run(run_id=run_id), timeout=20)
    return result, emitter


async def test_a_busy_database_refusing_one_items_own_write_is_that_items_hole():
    result, emitter = await _run(hole=True, run_id="busy-db-hole")

    assert result.status is RunStatus.COMPLETED, (
        f"one item's refused outcome write ended the whole run: {result.error}"
    )
    gathered = result.last_outputs["gather"]
    assert sorted(gathered["values"]) == ["read minutes.txt", "read notes.pdf"]
    (hole,) = gathered["holes"]
    assert hole["error"]["code"] == "LockContentionError"
    assert hole["error"]["cause"] == Cause.DATABASE_BUSY
    failed = [
        e for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == "node_failed"
    ]
    assert [f["error_type"] for f in failed] == ["LockContentionError"]


async def test_the_same_fault_on_a_step_that_is_not_a_hole_still_parks_the_run():
    result, _ = await _run(hole=False, run_id="busy-db-no-hole")

    assert result.status is RunStatus.ERRORED
    assert result.failure is not None
    assert result.failure.cause == Cause.DATABASE_BUSY, result.failure


def test_a_lock_timeout_under_the_steps_note_wrap_reads_database_busy():
    wrapped = append_failure_notes(
        LockContentionError(LOCK_SENTENCE),
        ["[99 of 100 invocations in this step completed and are preserved; retry re-runs only the failed one(s)]"],
    )
    failure = failure_from_exception(wrapped, step_id="ingest", step_label="Read what is new")
    assert failure.cause == Cause.DATABASE_BUSY, failure
    assert failure.error_type == "LockContentionError"

    # The same failure when all that is left is its stored text.
    stored = failure_from_text(f"ExecutionError: LockContentionError:\n{LOCK_SENTENCE}", error_type="ExecutionError")
    assert stored.cause == Cause.DATABASE_BUSY, stored
