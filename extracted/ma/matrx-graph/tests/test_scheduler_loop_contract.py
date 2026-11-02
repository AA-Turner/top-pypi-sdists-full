"""ENGINE_SPEC §9 (loop contract — fixes audit E7-loop) + §12 criterion 6.

The iteration round-trip MUST NOT depend on the loop body echoing
``iteration``. The ENGINE carries loop state:

  * ``control.loop``'s body ``Send`` pushes a ``LoopFrame``
    ``{origin_node_id, iteration}`` onto the child invocation's
    ``loop_stack`` (nested loops compose — it's a stack).
  * The stack propagates through the body chain by correlation inheritance
    (§4.3): Send children inherit; join-accumulator firings inherit via the
    buffered ``PendingBinding.loop_stack``.
  * When a routed delivery targets the top frame's ``origin_node_id``, the
    engine POPS the frame and INJECTS ``iteration`` into the delivered
    payload; a return edge with no explicit mappings wraps the body output
    as ``{"accumulator": <full payload>}``. The body never needs to know it
    is in a loop.
  * ``exit_expression`` / ``max_iterations`` therefore evaluate against
    ENGINE truth — a non-echoing body terminates correctly, never the old
    non-recoverable ``max_steps`` FAILED death.

Temporal precedent: iteration count lives in workflow state; activities
never carry orchestration counters.
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


class _BodyInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _BodyOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    note: str = ""
    runs: int = 0


class _BodyConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _NonEchoingBody:
    """A loop body that deliberately does NOT echo ``iteration`` (audit E7).

    Records every payload it was invoked with so tests can prove the engine
    — not the body — advanced the counter.
    """

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.non_echoing_body",
        category=NodeCategory.DATA,
        display_name="Non-echoing loop body",
        description="Returns only its own fields; never echoes iteration.",
        input_schema=_BodyInput,
        output_schema=_BodyOutput,
        config_schema=_BodyConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _BodyInput, _config: _BodyConfig
    ) -> NodeResult[_BodyOutput]:
        self.calls.append(inputs.model_dump())
        return success(_BodyOutput(note="worked", runs=len(self.calls)))


def _registry_with_body() -> tuple[NodeRegistry, _NonEchoingBody]:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    body = _NonEchoingBody()
    reg.register(body)
    return reg, body


def _loop_graph_data(
    *, exit_expression: str | None = None, max_iterations: int = 5
) -> dict[str, Any]:
    """start → loop ⇄ body (dispatch via ctx.send, return via a plain DATA
    edge with NO mappings) ; loop --done--> final. ``body`` has no inbound
    edges (it is Send-driven), so entry_nodes is declared explicitly."""
    config: dict[str, Any] = {
        "target_node_id": "body",
        "max_iterations": max_iterations,
    }
    if exit_expression is not None:
        config["exit_expression"] = exit_expression
    return {
        "entry_nodes": ["start"],
        "nodes": [
            {
                "id": "start",
                "type": "data.transform",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"expression": "0"}},
            },
            {
                "id": "loop",
                "type": "control.loop",
                "position": {"x": 200, "y": 0},
                "data": {"config": config},
            },
            {
                "id": "body",
                "type": "test.non_echoing_body",
                "position": {"x": 200, "y": 150},
                "data": {},
            },
            {
                "id": "final",
                "type": "data.transform",
                "position": {"x": 400, "y": 0},
                "data": {"config": {"expression": "'DONE'"}},
            },
        ],
        "edges": [
            {"id": "e_start_loop", "source": "start", "target": "loop"},
            # The return edge: NO mappings — §9 wraps the body output as
            # {"accumulator": <full payload>} and injects engine iteration.
            {"id": "e_body_loop", "source": "body", "target": "loop"},
            {
                "id": "e_loop_final",
                "source": "loop",
                "sourceHandle": "done",
                "target": "final",
            },
        ],
    }


async def test_loop_without_echo_terminates_via_default_exit() -> None:
    """Default exit_expression (iteration >= 1) against ENGINE-carried truth:
    one body pass, then done — never max_steps FAILED (§12 criterion 6)."""
    registry, body = _registry_with_body()
    graph = compile_graph(Definition.model_validate(_loop_graph_data()), registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )

    result = await scheduler.run(run_id="run-loop-1", max_steps=25)

    assert result.status is RunStatus.COMPLETED, result.error
    assert len(body.calls) == 1
    # Engine truth reached the loop: exit_expression saw iteration == 1.
    assert result.last_outputs["loop"]["iteration"] == 1
    assert result.last_outputs["loop"]["done"] is True
    # The wrapped accumulator carried the body's FULL output back.
    assert result.last_outputs["loop"]["accumulator"] == {"note": "worked", "runs": 1}
    # done-handle edge routed downstream.
    assert result.last_outputs["final"]["result"] == "DONE"


async def test_loop_without_echo_terminates_via_max_iterations() -> None:
    """An exit_expression that never holds still terminates at the
    max_iterations safety bound — engine-side counting, no body echo, and
    NEVER the old terminal max_steps FAILED death."""
    registry, body = _registry_with_body()
    graph = compile_graph(
        Definition.model_validate(_loop_graph_data(exit_expression="1 > 2", max_iterations=3)),
        registry=registry,
    )
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )

    result = await scheduler.run(run_id="run-loop-2", max_steps=50)

    assert result.status is RunStatus.COMPLETED, result.error
    # Iterations 1, 2, 3 each ran the body once; iteration 3 hit the cap.
    assert len(body.calls) == 3
    assert result.last_outputs["loop"]["iteration"] == 3
    assert result.last_outputs["loop"]["done"] is True
    assert result.last_outputs["final"]["result"] == "DONE"


async def test_loop_stack_survives_park_and_resume() -> None:
    """The engine-carried loop state is DURABLE: park (pause) while the body
    invocation sits on the frontier, resume from the checkpoint — the loop
    still terminates with engine-injected iteration."""
    registry, body = _registry_with_body()
    graph = compile_graph(Definition.model_validate(_loop_graph_data()), registry=registry)
    checkpointer = MemoryCheckpointer()

    # Pause polls happen BEFORE each super-step: step0=start, step1=loop,
    # step2=body(iteration 1). Pausing on the 3rd poll parks the frontier
    # that carries the body's Send invocation — and its loop_stack.
    polls = {"n": 0}

    async def _pause() -> bool:
        polls["n"] += 1
        return polls["n"] == 3

    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(FakeEmitter()),
        registry=registry,
        pause_check=_pause,
    )
    result = await scheduler.run(run_id="run-loop-3", max_steps=25)
    assert result.status is RunStatus.PAUSED
    assert len(body.calls) == 0  # parked BEFORE the body ran

    latest = await checkpointer.latest_checkpoint("run-loop-3")
    assert latest is not None
    frontier = {ni.node_id: ni for ni in latest.next_invocations}
    assert "body" in frontier
    # The durable frontier invocation carries the engine's loop frame.
    assert frontier["body"].loop_stack == [{"origin_node_id": "loop", "iteration": 1}]

    fresh = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    resumed = await fresh.resume(
        run_id="run-loop-3", checkpoint_id=latest.checkpoint_id, max_steps=25
    )
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert len(body.calls) == 1
    assert resumed.last_outputs["loop"]["iteration"] == 1
    assert resumed.last_outputs["final"]["result"] == "DONE"
