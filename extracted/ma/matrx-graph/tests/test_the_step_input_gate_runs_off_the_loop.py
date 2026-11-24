"""A step's input gate (reduce, parse, node_started dump) runs OFF the event loop for a large value,
and still hands the step a COPY, so a step that mutates its arguments cannot change stored values.

Live 2026-11-07 (event_loop_stall 347cbb62, aidream-api, worst 4.1 s on
``workflow_step:scoring_rows``): ``_execute_invocation_body`` ran ``reduce_for_ingestion``,
``model_validate`` and the node_started ``model_dump_json`` directly on the loop; on a large
argument the whole process froze. The reduce is ALSO the copy that keeps a mutating step away from
the producer's stored output, so it cannot be skipped, only moved. RED before: every spy below saw
the loop thread.
"""

from __future__ import annotations

import asyncio
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, model_validator

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.content_ir import markers
from matrx_graph.executor import json_dump
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context

ENTRIES = 2000  # ~4000+ containers: over values.OFF_LOOP_MIN_NODES, so "large"
ORIGINAL = "x" * 40


def _on_loop_thread() -> bool:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return False
    return True


PARSE_THREADS: list[bool] = []


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entries: int = 0


class _Out(BaseModel):
    model_config = ConfigDict(extra="allow")

    ledger: Any = None
    first_raw: str = ""
    count: int = 0


class _MakeIn(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Make:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.gate_make",
        category=NodeCategory.DATA,
        display_name="Make",
        description="Emits a large ledger.",
        input_schema=_MakeIn,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(self, ctx: NodeExecutionContext, inputs: _MakeIn, config: _Cfg) -> NodeResult[_Out]:
        ledger = [{"n": i, "raw": ORIGINAL} for i in range(config.entries)]
        return success(_Out(ledger=ledger, count=len(ledger)))


class _TakeIn(BaseModel):
    """``ledger: Any`` — pydantic keeps the very object it was handed, so only the gate's copy
    stands between the step and the producer's stored output."""

    model_config = ConfigDict(extra="allow")

    ledger: Any = None
    after: Any = None

    @model_validator(mode="before")
    @classmethod
    def _record_thread(cls, data: Any) -> Any:
        PARSE_THREADS.append(_on_loop_thread())
        return data


class _Mutate:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.gate_mutate",
        category=NodeCategory.DATA,
        display_name="Mutate",
        description="Mutates its input ledger in place.",
        input_schema=_TakeIn,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(self, ctx: NodeExecutionContext, inputs: _TakeIn, config: _Cfg) -> NodeResult[_Out]:
        inputs.ledger[0]["raw"] = "MUTATED"
        inputs.ledger.append({"n": -1, "raw": "EXTRA"})
        return success(_Out(first_raw=inputs.ledger[0]["raw"], count=len(inputs.ledger)))


class _Read:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.gate_read",
        category=NodeCategory.DATA,
        display_name="Read",
        description="Reports what it received.",
        input_schema=_TakeIn,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(self, ctx: NodeExecutionContext, inputs: _TakeIn, config: _Cfg) -> NodeResult[_Out]:
        return success(_Out(first_raw=inputs.ledger[0]["raw"], count=len(inputs.ledger)))


def _definition() -> Definition:
    def node(node_id: str, kind: str, entries: int = 0) -> dict[str, Any]:
        return {"id": node_id, "type": kind, "position": {"x": 0, "y": 0}, "data": {"config": {"entries": entries}}}

    def edge(src: str, tgt: str, mappings: dict[str, str]) -> dict[str, Any]:
        return {"id": f"e_{src}_{tgt}", "source": src, "target": tgt, "data": {"kind": "data", "mappings": mappings}}

    return Definition.model_validate(
        {
            "nodes": [
                node("make", "test.gate_make", ENTRIES),
                node("mutate", "test.gate_mutate"),
                node("read", "test.gate_read"),
            ],
            "edges": [
                edge("make", "mutate", {"ledger": "ledger"}),
                # read waits for mutate, then reads make's ledger: what mutate did must not show.
                edge("make", "read", {"ledger": "ledger"}),
                edge("mutate", "read", {"after": "count"}),
            ],
            "entry_nodes": ["make"],
        }
    )


async def _run(run_id: str):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    for node in (_Make(), _Mutate(), _Read()):
        registry.register(node)
    scheduler = Scheduler(
        compile_graph(_definition(), registry=registry),
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    return await scheduler.run(run_id=run_id)


async def test_the_step_input_gate_never_runs_on_the_loop_for_a_large_value(monkeypatch) -> None:
    PARSE_THREADS.clear()
    reduce_threads: list[bool] = []
    dump_threads: list[bool] = []
    real_reduce = markers.reduce_for_ingestion
    real_dump = json_dump.model_dump_json

    def spy_reduce(value: Any, schema: Any = None) -> Any:
        if isinstance(value, dict) and isinstance(value.get("ledger"), list):
            reduce_threads.append(_on_loop_thread())
        return real_reduce(value, schema)

    def spy_dump(model: BaseModel, *, context: str = "") -> dict[str, Any]:
        if "node_started inputs" in context and isinstance(model, _TakeIn):
            dump_threads.append(_on_loop_thread())
        return real_dump(model, context=context)

    monkeypatch.setattr(markers, "reduce_for_ingestion", spy_reduce)
    monkeypatch.setattr(json_dump, "model_dump_json", spy_dump)
    from matrx_graph.executor import scheduler as scheduler_module

    monkeypatch.setattr(scheduler_module, "model_dump_json", spy_dump)

    result = await _run("gate-off-loop")

    assert result.status is RunStatus.COMPLETED, result.error
    assert reduce_threads and not any(reduce_threads), f"reduce_for_ingestion ran on the loop: {reduce_threads}"
    assert PARSE_THREADS and not any(PARSE_THREADS), f"model_validate ran on the loop: {PARSE_THREADS}"
    # An argument delivered unchanged is recorded as the delivered object and never dumped (L-SPEED 6e part 2,
    # _started_dump); any dump that does run is off the loop.
    assert not any(dump_threads), f"node_started dump ran on the loop: {dump_threads}"


async def test_a_step_that_mutates_its_input_cannot_change_the_stored_value() -> None:
    result = await _run("gate-copy-holds")

    assert result.status is RunStatus.COMPLETED, result.error
    outputs = result.last_outputs
    # The mutating step really mutated what it was handed...
    assert outputs["mutate"]["first_raw"] == "MUTATED"
    assert outputs["mutate"]["count"] == ENTRIES + 1
    # ...yet the producer's stored output and the next reader see the original.
    assert outputs["make"]["ledger"][0]["raw"] == ORIGINAL
    assert len(outputs["make"]["ledger"]) == ENTRIES
    assert outputs["read"]["first_raw"] == ORIGINAL
    assert outputs["read"]["count"] == ENTRIES
