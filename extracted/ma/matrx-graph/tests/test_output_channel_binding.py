"""Per-node output_channel binding — reducer-based fan-in for generic nodes.

NodeDef.data.output_channel = "<name>" surfaces as CompiledNode.output_channel;
after the node succeeds (or is mocked) the scheduler appends its full output
dump to that channel through the channel's reducer. This is the only
aggregation path that survives send-driven fan-out: edge routing groups
results per target node and merges them last-writer-wins, so N parallel
worker results routed over edges collapse to ONE payload.

Verifies:
    1. compile: data.output_channel lands on CompiledNode + writes_channels;
       invalid values fail compilation loudly.
    2. The canonical fan-in wiring end-to-end: control.map fans out N items
       to a worker bound to an append channel; a worker→gather edge triggers
       gather exactly once, one super-step later, and gather drains all N
       outputs from the channel.
    3. A mocked worker honors the binding identically (writes recorded on
       the NodeOutcome so crash-replay reproduces them).
"""

from __future__ import annotations

from typing import ClassVar

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
from matrx_graph.errors import CompilationError
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context


class _WorkerInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _WorkerOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    got: str


class _WorkerConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _WorkerExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.channel_worker",
        category=NodeCategory.DATA,
        display_name="Channel worker",
        description="Echoes the sent item; output aggregates via output_channel.",
        input_schema=_WorkerInput,
        output_schema=_WorkerOutput,
        config_schema=_WorkerConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(
        self,
        _ctx: NodeExecutionContext,
        inputs: _WorkerInput,
        _config: _WorkerConfig,
    ) -> NodeResult[_WorkerOutput]:
        return success(_WorkerOutput(got=str(inputs.model_dump().get("value"))))


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(_WorkerExecutor(), overwrite=True)
    return reg


def _fanout_definition(worker_data_extra: dict | None = None) -> Definition:
    """map(items) → worker(output_channel=results) → gather(channel=results)."""
    worker_data: dict = {"config": {}, "output_channel": "results"}
    if worker_data_extra:
        worker_data.update(worker_data_extra)
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "fanout",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"target_node_id": "worker"},
                        "input": {"items": ["a", "b", "c"]},
                    },
                },
                {
                    "id": "worker",
                    "type": "test.channel_worker",
                    "position": {"x": 200, "y": 0},
                    "data": worker_data,
                },
                {
                    "id": "collect",
                    "type": "control.gather",
                    "position": {"x": 400, "y": 0},
                    "data": {"config": {"channel": "results"}},
                },
            ],
            "edges": [
                {"id": "e__worker__collect", "source": "worker", "target": "collect"},
            ],
            "channels": [{"name": "results", "reducer": "append"}],
            "entry_nodes": ["fanout"],
        }
    )


def test_compile_surfaces_output_channel():
    registry = _registry()
    graph = compile_graph(_fanout_definition(), registry=registry)
    worker = graph.nodes["worker"]
    assert worker.output_channel == "results"
    assert "results" in worker.writes_channels
    assert graph.channels["results"].reducer == "append"
    # Nodes without the binding are untouched.
    assert graph.nodes["fanout"].output_channel is None


@pytest.mark.parametrize("bad", ["", "   ", 123, {"name": "results"}])
def test_compile_rejects_invalid_output_channel(bad):
    definition = _fanout_definition()
    definition.nodes[1].data["output_channel"] = bad
    with pytest.raises(CompilationError, match="output_channel"):
        compile_graph(definition, registry=_registry())


async def test_map_worker_channel_gather_fan_in():
    """The canonical fan-in proof: N parallel worker outputs all reach gather."""
    registry = _registry()
    graph = compile_graph(_fanout_definition(), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(emitter),
        registry=registry,
    )
    result = await scheduler.run(run_id="chan-bind-real")
    assert result.status is RunStatus.COMPLETED

    gathered = result.last_outputs["collect"]
    assert gathered["count"] == 3
    assert {v["got"] for v in gathered["values"]} == {"a", "b", "c"}

    # Gather fired exactly once: the three worker→collect edge firings in one
    # super-step collapse to a single invocation (grouped per target node).
    completed = [
        e
        for k, e in emitter.events
        if k == "data"
        and isinstance(e, dict)
        and e.get("event") == "node_completed"
        and e.get("node_id") == "collect"
    ]
    assert len(completed) == 1


async def test_mocked_worker_honors_output_channel():
    """Mock path writes the channel AND records it on the NodeOutcome."""
    registry = _registry()
    graph = compile_graph(
        _fanout_definition({"mock_response": {"enabled": True, "output": {"got": "mocked"}}}),
        registry=registry,
    )
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(FakeEmitter()),
        registry=registry,
    )
    result = await scheduler.run(run_id="chan-bind-mock")
    assert result.status is RunStatus.COMPLETED

    gathered = result.last_outputs["collect"]
    assert gathered["count"] == 3
    assert [v["got"] for v in gathered["values"]] == ["mocked"] * 3

    # The channel write is on the recorded outcome — crash-replay reproduces
    # it. Send-driven workers are keyed by their fan-out correlation
    # (ENGINE_SPEC §4.2): read the dispatcher's recorded Sends for the minted
    # (dispatch_id, item_index) instead of the pre-§4 attempt-numbered key.
    map_outcome = await checkpointer.get_outcome(
        run_id="chan-bind-mock", step=0, node_id="fanout", attempt=1
    )
    assert map_outcome is not None and map_outcome.sends
    first_send = map_outcome.sends[0]
    outcome = await checkpointer.get_outcome(
        run_id="chan-bind-mock",
        step=1,
        node_id="worker",
        attempt=1,
        dispatch_id=first_send.dispatch_id,
        item_index=first_send.item_index,
    )
    assert outcome is not None
    assert outcome.source == "mocked"
    assert len(outcome.channel_writes) == 1
    channel_name, payload = outcome.channel_writes[0]
    assert channel_name == "results"
    assert payload == {"got": "mocked"}


async def test_gather_explicit_channel_wins_over_engine_shaped_trigger():
    """🚨 Regression (found live 2026-08-19): a gather TRIGGERED by a
    multi-fire source (a work-queue's 'done' handle) receives its trigger in
    the §4.4 aggregated-dispatch shape, which matches _is_engine_items — and
    the old order made gather return the TRIGGER payload while the channel it
    was explicitly configured to drain sat unread (two rendered images lost).
    An explicit config.channel must always win."""
    from types import SimpleNamespace

    from matrx_graph.nodes.control.gather import (
        GatherConfig,
        GatherExecutor,
        GatherInput,
    )

    channel_contents = [{"final_text": "https://cdn/u1"}, {"final_text": "https://cdn/u2"}]
    ctx = SimpleNamespace(
        channels=SimpleNamespace(
            get=lambda name, default=None: channel_contents if name == "results" else default
        )
    )
    trigger = GatherInput.model_validate(
        {"items": [{"item_index": 0, "status": "succeeded", "value": {"succeeded": 2}}]}
    )
    result = await GatherExecutor().execute(ctx, trigger, GatherConfig(channel="results"))
    assert result.result.values == channel_contents
    # And without a configured channel the engine path still works unchanged.
    result2 = await GatherExecutor().execute(ctx, trigger, GatherConfig(channel=None))
    assert result2.result.values == [{"succeeded": 2}]
