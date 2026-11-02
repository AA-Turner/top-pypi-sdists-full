"""ENGINE_SPEC §6.2 (interrupt keeps siblings — fixes audit E5) + §12 criterion 5.

On ``GraphInterrupt`` in a step with parallel siblings, the engine runs the
step's normal completion phases for every NON-interrupted result first:

  1. Completed siblings' channel writes COMMIT (an interrupt is not a failure
     — resume never re-runs completed siblings).
  2. Completed siblings' outputs/emissions/sends ROUTE through the §3 join
     accumulator.
  3. The interrupt checkpoint carries the FULL remaining frontier: the
     interrupted invocation(s) — the surfaced one explicitly marked
     ``NextInvocation.is_interrupted`` — plus every invocation made Ready by
     sibling routing, plus errored siblings, plus step-mode deferred siblings.

Resume records ``resume_value`` at the MARKED invocation's correlation key
(never blindly ``next_invocations[0]``) and drives on: the sibling's
downstream subtree executes exactly once, sibling outputs stay visible, and
partial join bindings delivered by the sibling survive the round-trip.
Temporal precedent: completed activity results are never discarded while the
workflow awaits a signal.
"""

from __future__ import annotations

from typing import Any, ClassVar

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context


class _SinkInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _SinkOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    result: str = ""
    runs: int = 0


class _SinkConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _CountingSink:
    """Spy executor — proves how many times the engine REALLY ran a node."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.counting_sink",
        category=NodeCategory.DATA,
        display_name="Counting sink",
        description="Records every execution payload.",
        input_schema=_SinkInput,
        output_schema=_SinkOutput,
        config_schema=_SinkConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _SinkInput, _config: _SinkConfig
    ) -> NodeResult[_SinkOutput]:
        self.calls.append(inputs.model_dump())
        return success(_SinkOutput(result="SINK", runs=len(self.calls)))


def _registry_with_sink() -> tuple[NodeRegistry, _CountingSink]:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    sink = _CountingSink()
    reg.register(sink)
    return reg, sink


def _sibling_graph_data() -> dict[str, Any]:
    """seed → (ask: human_input | double: transform→channel) ; double → sink ;
    ask → echo. The interrupt (ask) and the sibling (double) run in the SAME
    super-step."""
    return {
        "nodes": [
            {
                "id": "seed",
                "type": "data.transform",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"expression": "1"}},
            },
            {
                "id": "ask",
                "type": "control.human_input",
                "position": {"x": 200, "y": -50},
                "data": {"config": {"prompt": "continue?"}},
            },
            {
                "id": "double",
                "type": "data.transform",
                "position": {"x": 200, "y": 50},
                "data": {
                    "config": {"expression": "inputs['result'] * 2"},
                    "output_channel": "side",
                },
            },
            {
                "id": "sink",
                "type": "test.counting_sink",
                "position": {"x": 400, "y": 50},
                "data": {},
            },
            {
                "id": "echo",
                "type": "data.transform",
                "position": {"x": 400, "y": -50},
                "data": {"config": {"expression": "'You said ' + inputs['answer']"}},
            },
        ],
        "edges": [
            {"id": "e_seed_ask", "source": "seed", "target": "ask"},
            {"id": "e_seed_double", "source": "seed", "target": "double"},
            {"id": "e_double_sink", "source": "double", "target": "sink"},
            {"id": "e_ask_echo", "source": "ask", "target": "echo"},
        ],
    }


async def test_interrupt_commits_and_routes_completed_siblings() -> None:
    """§12 criterion 5: after resume, the sibling's output is committed,
    routed, and its downstream subtree executes exactly once."""
    registry, sink = _registry_with_sink()
    graph = compile_graph(Definition.model_validate(_sibling_graph_data()), registry=registry)
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)

    result = await scheduler.run(run_id="run-int-sib-1")
    assert result.status is RunStatus.INTERRUPTED
    assert result.interrupt is not None
    assert result.interrupt["node_id"] == "ask"

    checkpoints = await checkpointer.list_checkpoints("run-int-sib-1")
    interrupt_cp = next(cp for cp in checkpoints if cp.interrupt_payload)

    # The checkpoint carries the FULL remaining frontier: the interrupted
    # invocation (explicitly marked) AND the sibling-routed downstream.
    by_node = {ni.node_id: ni for ni in interrupt_cp.next_invocations}
    assert "ask" in by_node and "sink" in by_node
    assert by_node["ask"].is_interrupted is True
    assert by_node["sink"].is_interrupted is False
    # Sibling channel write committed BEFORE the interrupt checkpoint.
    assert interrupt_cp.channel_values.get("side") == {"result": 2}

    resume_result = await scheduler.resume(
        run_id="run-int-sib-1",
        checkpoint_id=interrupt_cp.checkpoint_id,
        resume_value={"answer": "blue"},
    )
    assert resume_result.status is RunStatus.COMPLETED
    # Sibling downstream executed EXACTLY once — nothing amputated, nothing doubled.
    assert len(sink.calls) == 1
    assert resume_result.last_outputs["sink"]["result"] == "SINK"
    # Sibling output stays visible post-resume (channel + interrupted branch).
    assert resume_result.channel_values.get("side") == {"result": 2}
    assert resume_result.last_outputs["echo"]["result"] == "You said blue"


async def test_interrupt_sibling_crash_replay_resume_from_latest() -> None:
    """Crash variant: process dies after the interrupt park; a FRESH scheduler
    resumes from the latest durable checkpoint — same guarantees."""
    registry, sink = _registry_with_sink()
    graph = compile_graph(Definition.model_validate(_sibling_graph_data()), registry=registry)
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)

    result = await scheduler.run(run_id="run-int-sib-2")
    assert result.status is RunStatus.INTERRUPTED

    latest = await checkpointer.latest_checkpoint("run-int-sib-2")
    assert latest is not None and latest.interrupt_payload

    # "Crash": new scheduler instance, no in-memory state carried over.
    fresh = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    resume_result = await fresh.resume(
        run_id="run-int-sib-2",
        checkpoint_id=latest.checkpoint_id,
        resume_value={"answer": "green"},
    )
    assert resume_result.status is RunStatus.COMPLETED
    assert len(sink.calls) == 1
    assert resume_result.channel_values.get("side") == {"result": 2}
    assert resume_result.last_outputs["echo"]["result"] == "You said green"


async def test_interrupt_preserves_sibling_join_binding() -> None:
    """A sibling's delivery into a join that ALSO waits on the interrupted
    node must survive the interrupt round-trip: J fires exactly once, with
    BOTH arguments, after resume."""
    registry, joined = _registry_with_sink()
    data = {
        "nodes": [
            {
                "id": "seed",
                "type": "data.transform",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"expression": "1"}},
            },
            {
                "id": "ask",
                "type": "control.human_input",
                "position": {"x": 200, "y": -50},
                "data": {"config": {"prompt": "value?"}},
            },
            {
                "id": "double",
                "type": "data.transform",
                "position": {"x": 200, "y": 50},
                "data": {"config": {"expression": "inputs['result'] * 2"}},
            },
            {
                "id": "j",
                "type": "test.counting_sink",
                "position": {"x": 400, "y": 0},
                "data": {},
            },
        ],
        "edges": [
            {"id": "e_seed_ask", "source": "seed", "target": "ask"},
            {"id": "e_seed_double", "source": "seed", "target": "double"},
            {
                "id": "e_double_j",
                "source": "double",
                "target": "j",
                "data": {"mappings": {"a": "result"}},
            },
            {
                "id": "e_ask_j",
                "source": "ask",
                "target": "j",
                "data": {"mappings": {"b": "answer"}},
            },
        ],
    }
    graph = compile_graph(Definition.model_validate(data), registry=registry)
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)

    result = await scheduler.run(run_id="run-int-join-1")
    assert result.status is RunStatus.INTERRUPTED

    checkpoints = await checkpointer.list_checkpoints("run-int-join-1")
    interrupt_cp = next(cp for cp in checkpoints if cp.interrupt_payload)
    # The sibling's partial delivery into J is durable on the interrupt
    # checkpoint — the buffered fragment IS the proof nothing was amputated.
    j_binding = interrupt_cp.pending_bindings.get("j")
    assert j_binding is not None
    assert j_binding.edges["e_double_j"].state == "delivered"
    assert j_binding.edges["e_double_j"].payload == {"a": 2}

    resume_result = await scheduler.resume(
        run_id="run-int-join-1",
        checkpoint_id=interrupt_cp.checkpoint_id,
        resume_value={"answer": 40},
    )
    assert resume_result.status is RunStatus.COMPLETED
    # J fired exactly ONCE, with BOTH arguments present.
    assert len(joined.calls) == 1
    assert joined.calls[0]["a"] == 2
    assert joined.calls[0]["b"] == 40
