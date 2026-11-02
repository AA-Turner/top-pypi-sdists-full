"""Engine fail-soft contract (audit P0-1 / P0-5).

The product's central promise — "a minor failure PARKS the run, never
kills it" — previously held only for exceptions raised inside a node
executor. Two whole classes escaped it:

  * ChannelError from a reducer during ``channels.commit`` → propagated
    uncaught past ``except ExecutionError`` (sibling classes) → terminal
    FAILED with no node attribution and no run_errored event.
  * EdgeRoutingError-class failures (conditional predicate, explicit
    mapping miss) in ``_route_outputs`` → terminal FAILED; mapping
    misses were worse — silently swallowed (``except: pass``).

And every exception exit out of ``scheduler.run()`` lost the partial
``last_outputs`` (the host persisted ``wf_run.output = null``).

These tests pin the NEW contract:
  1. Reducer failure parks as ERRORED, attributed to the writing node,
     recoverable via skip + resume.
  2. Explicit edge-mapping miss parks as ERRORED (never silent).
  3. Framework failures (max_steps) return RunResult(FAILED) with
     partial last_outputs — ``run()`` does not raise.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeCategory,
    NodeRegistry,
    NodeSpec,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.checkpoint.protocol import NodeOutcome
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.result import NodeResult, success

from tests._fixtures import FakeEmitter, make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


class _BadWriteOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ok: bool


class _BadWriteExec:
    """Succeeds as a node but writes a NON-DICT to a merge-reducer channel —
    the reducer rejects it at commit time, after the node already recorded
    a successful outcome."""

    spec = NodeSpec(
        type="test.bad_channel_write",
        category=NodeCategory.CUSTOM,
        display_name="Bad channel write",
        output_schema=_BadWriteOut,
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
    )

    async def execute(self, ctx: NodeExecutionContext, inputs, config) -> NodeResult[_BadWriteOut]:
        ctx.channels.write("merged", "not-a-dict")  # merge reducer → ChannelError
        return success(_BadWriteOut(ok=True))


def _bad_write_definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "writer",
                    "type": "test.bad_channel_write",
                    "position": {"x": 0, "y": 0},
                    "data": {},
                }
            ],
            "edges": [],
            "channels": [{"name": "merged", "reducer": "merge"}],
        }
    )


async def test_channel_reducer_failure_parks_recoverable():
    registry = _registry()
    registry.register(_BadWriteExec())
    graph = compile_graph(_bad_write_definition(), registry=registry)
    emitter = FakeEmitter()
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(emitter), registry=registry)

    result = await scheduler.run(run_id="reducer-park")

    # Parked, not killed.
    assert result.status is RunStatus.ERRORED
    assert "merge reducer" in (result.error or "")
    # The node itself succeeded — its output is preserved.
    assert result.last_outputs["writer"] == {"ok": True}

    errored = [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == "run_errored"
    ]
    assert len(errored) == 1
    assert errored[0]["node_id"] == "writer"  # attributed
    assert errored[0]["error_type"] == "ChannelError"
    cp_id = errored[0]["checkpoint_id"]
    assert cp_id

    # RECOVERY: the user's lever for a reducer-rejected output is skip /
    # manual-result on the writing node. Simulate skip: overwrite the
    # outcome with an empty output and NO channel writes, then resume.
    await checkpointer.record_outcome(
        NodeOutcome(
            run_id="reducer-park",
            step=0,
            node_id="writer",
            attempt=1,
            output={"ok": False},
            channel_writes=[],
        )
    )
    resumed = await scheduler.resume(run_id="reducer-park", checkpoint_id=cp_id)
    assert resumed.status is RunStatus.COMPLETED


async def test_edge_mapping_miss_parks_not_silent():
    """An EXPLICITLY mapped field that can't resolve must park the run
    (attributed to the source node) — never silently drop the field."""
    registry = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "a",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "{'score': 0.7}"}},
                },
                {
                    "id": "b",
                    "type": "data.transform",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {"expression": "inputs"}},
                },
            ],
            "edges": [
                {
                    "id": "e_map",
                    "source": "a",
                    "target": "b",
                    "data": {"mappings": {"x": "does.not.exist"}},
                }
            ],
        }
    )
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)

    result = await scheduler.run(run_id="map-miss")

    assert result.status is RunStatus.ERRORED
    assert "does.not.exist" in (result.error or "")
    # a's output survived the park.
    assert result.last_outputs["a"]["score"] == 0.7

    errored = [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == "run_errored"
    ]
    assert len(errored) == 1
    assert errored[0]["node_id"] == "a"
    assert errored[0]["error_type"] == "EdgeRoutingError"


async def test_edge_mapping_dotted_target_key_rejected():
    """A dotted TARGET key ('variables.count') would be written verbatim into
    the downstream node's inputs — a literally-dotted key, not a nested field —
    and silently do nothing. The scheduler must park the run with an actionable
    error instead (FOUND_DEFECTS agent-node #5)."""
    registry = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "a",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "{'count': 3}"}},
                },
                {
                    "id": "b",
                    "type": "data.transform",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {"expression": "inputs"}},
                },
            ],
            "edges": [
                {
                    "id": "e_dotted",
                    "source": "a",
                    "target": "b",
                    "data": {"mappings": {"variables.count": "count"}},
                }
            ],
        }
    )
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)

    result = await scheduler.run(run_id="dotted-target")

    assert result.status is RunStatus.ERRORED
    # The error names the offending key and says what IS allowed.
    assert "variables.count" in (result.error or "")
    assert "TARGET" in (result.error or "")
    assert "'count'" in (result.error or "")  # the suggested plain key
    # a's output survived the park.
    assert result.last_outputs["a"]["count"] == 3

    errored = [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == "run_errored"
    ]
    assert len(errored) == 1
    assert errored[0]["node_id"] == "a"
    assert errored[0]["error_type"] == "EdgeRoutingError"


async def test_max_steps_returns_failed_result_with_outputs():
    """Framework-level failures are terminal FAILED but never RAISE —
    the RunResult carries partial last_outputs so the host persists what
    completed instead of nulling wf_run.output (audit P0-5)."""
    registry = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "t1",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "{'v': 1}"}},
                },
                {
                    "id": "t2",
                    "type": "data.transform",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {"expression": "{'v': inputs['v'] + 1}"}},
                },
            ],
            "edges": [
                {"id": "e1", "source": "t1", "target": "t2", "data": {}},
            ],
        }
    )
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)

    # max_steps=1: t1 runs in step 0, then the step-1 boundary trips the cap.
    result = await scheduler.run(run_id="max-steps", max_steps=1)

    assert result.status is RunStatus.FAILED
    assert "max_steps" in (result.error or "")
    # t1's completed output is preserved on the result.
    assert result.last_outputs["t1"]["v"] == 1

    failed = [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == "run_failed"
    ]
    assert len(failed) == 1


class _TrackerOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ok: bool


_CONCURRENCY_TRACKER = {"current": 0, "peak": 0}


class _AnyIn(BaseModel):
    model_config = ConfigDict(extra="allow")


class _SlowTrackedExec:
    """Records peak concurrent executions — proves the step semaphore."""

    spec = NodeSpec(
        type="test.slow_tracked",
        category=NodeCategory.CUSTOM,
        display_name="Slow tracked",
        input_schema=_AnyIn,
        output_schema=_TrackerOut,
        handles=(HandleSpec(id="in", direction=HandleDirection.INPUT),),
    )

    async def execute(self, ctx, inputs, config) -> NodeResult[_TrackerOut]:
        import asyncio

        _CONCURRENCY_TRACKER["current"] += 1
        _CONCURRENCY_TRACKER["peak"] = max(
            _CONCURRENCY_TRACKER["peak"], _CONCURRENCY_TRACKER["current"]
        )
        await asyncio.sleep(0.02)
        _CONCURRENCY_TRACKER["current"] -= 1
        return success(_TrackerOut(ok=True))


class _Fanout6Exec:
    spec = NodeSpec(
        type="test.fanout6",
        category=NodeCategory.CUSTOM,
        display_name="Fanout 6",
        launches_nodes=True,  # ctx.send to a run-time target
        output_schema=_TrackerOut,
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
    )

    async def execute(self, ctx, inputs, config) -> NodeResult[_TrackerOut]:
        for i in range(6):
            ctx.send("worker", {"i": i})
        return success(_TrackerOut(ok=True))


async def test_step_concurrency_bounds_parallel_invocations():
    """BS-6: step_concurrency=2 → a 6-way fan-out never runs more than 2
    invocations at once."""
    _CONCURRENCY_TRACKER["current"] = 0
    _CONCURRENCY_TRACKER["peak"] = 0

    registry = _registry()
    registry.register(_Fanout6Exec())
    registry.register(_SlowTrackedExec())
    definition = Definition.model_validate(
        {
            "nodes": [
                {"id": "fan", "type": "test.fanout6", "position": {"x": 0, "y": 0}, "data": {}},
                {
                    "id": "worker",
                    "type": "test.slow_tracked",
                    "position": {"x": 200, "y": 0},
                    "data": {},
                },
            ],
            "edges": [],
            "entry_nodes": ["fan"],
        }
    )
    graph = compile_graph(definition, registry=registry)
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
        step_concurrency=2,
    )
    result = await scheduler.run(run_id="bounded-fanout")
    assert result.status is RunStatus.COMPLETED
    assert _CONCURRENCY_TRACKER["peak"] <= 2


async def test_map_max_dispatches_caps_fanout():
    """P2-7: a data-driven list beyond max_dispatches PARKS the run with a
    clear error instead of fanning out unbounded."""
    registry = _registry()
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "m",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {
                            "target_node_id": "t",
                            "max_dispatches": 3,
                        },
                    },
                },
                {
                    "id": "t",
                    "type": "data.transform",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {"expression": "inputs"}},
                },
            ],
            "edges": [],
            "entry_nodes": ["m"],
        }
    )
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id="map-cap", inputs={"items": [1, 2, 3, 4, 5]})
    assert result.status is RunStatus.ERRORED  # parked, recoverable
    assert "max_dispatches" in (result.error or "")
