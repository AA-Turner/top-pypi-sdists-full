"""control.loop at scale — high iteration counts, the 1000 cap, park/resume.

The loop contract suite (test_scheduler_loop_contract.py) proves 1-3
iterations; nothing exercised the machinery at real width: 200+ engine-carried
iterations, the le=1000 config ceiling (both sides of it), and a park/resume
in the MIDDLE of a long loop. The body is a cheap in-memory recorder — the
LOOP machinery (LoopFrame push/pop, engine-injected iteration, return-edge
re-fire) is the system under test, and the recorder's exact call count +
strictly-sequential iteration payloads are only producible by that machinery
running every single pass.
"""

from __future__ import annotations

from typing import Any, ClassVar

import pytest
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
from matrx_graph.errors import CompilationError
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success

from tests._fixtures import FakeEmitter, make_app_context


class _BodyInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _BodyOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    runs: int = 0


class _NoConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _EchoBody:
    """Trivial loop body: records the engine-delivered iteration, echoes
    nothing loop-related back (the engine owns the counter)."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.echo_body",
        category=NodeCategory.DATA,
        display_name="Echo body",
        description="Cheap in-memory loop body.",
        input_schema=_BodyInput,
        output_schema=_BodyOutput,
        config_schema=_NoConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    def __init__(self) -> None:
        self.iterations_seen: list[int] = []

    async def execute(
        self, _ctx: NodeExecutionContext, inputs: _BodyInput, _config: _NoConfig
    ) -> NodeResult[_BodyOutput]:
        self.iterations_seen.append(int(inputs.model_dump().get("iteration", -1)))
        return success(_BodyOutput(runs=len(self.iterations_seen)))


def _registry() -> tuple[NodeRegistry, _EchoBody]:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    body = _EchoBody()
    reg.register(body)
    return reg, body


def _loop_definition(max_iterations: int) -> dict[str, Any]:
    """start → loop ⇄ body (ctx.send out, bare DATA return edge), loop --done--> final."""
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
                "data": {
                    "config": {
                        "target_node_id": "body",
                        "max_iterations": max_iterations,
                        # Never true — the run must terminate on the cap.
                        "exit_expression": "1 > 2",
                    }
                },
            },
            {
                "id": "body",
                "type": "test.echo_body",
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
            {"id": "e_body_loop", "source": "body", "target": "loop"},
            {
                "id": "e_loop_final",
                "source": "loop",
                "sourceHandle": "done",
                "target": "final",
            },
        ],
    }


def _steps_for(iterations: int) -> int:
    # Each iteration costs ~2 super-steps (body fires, loop re-fires) plus
    # setup/teardown — generous headroom without masking non-termination.
    return iterations * 2 + 20


async def test_loop_runs_200_iterations_with_engine_carried_state() -> None:
    registry, body = _registry()
    graph = compile_graph(Definition.model_validate(_loop_definition(200)), registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )

    result = await scheduler.run(run_id="run-loop-200", max_steps=_steps_for(200))

    assert result.status is RunStatus.COMPLETED, result.error
    # The body ran EVERY iteration, in strict engine order — no drops, no
    # repeats, no reordering across 200 LoopFrame push/pop round trips.
    assert body.iterations_seen == list(range(1, 201))
    assert result.last_outputs["loop"]["iteration"] == 200
    assert result.last_outputs["loop"]["done"] is True
    # The final accumulator is the LAST body output, round-tripped.
    assert result.last_outputs["loop"]["accumulator"] == {"runs": 200}
    assert result.last_outputs["final"]["result"] == "DONE"


async def test_loop_runs_at_the_1000_iteration_cap() -> None:
    """The le=1000 ceiling is a REAL operating point, not a theoretical
    bound: a loop configured at the cap executes all 1000 passes and
    terminates COMPLETED within the run's step budget."""
    registry, body = _registry()
    graph = compile_graph(Definition.model_validate(_loop_definition(1000)), registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )

    result = await scheduler.run(run_id="run-loop-1000", max_steps=_steps_for(1000))

    assert result.status is RunStatus.COMPLETED, result.error
    assert len(body.iterations_seen) == 1000
    assert body.iterations_seen[0] == 1
    assert body.iterations_seen[-1] == 1000
    assert sorted(set(body.iterations_seen)) == body.iterations_seen  # unique + ordered
    assert result.last_outputs["loop"]["iteration"] == 1000


def test_max_iterations_above_1000_fails_compilation() -> None:
    """The config ceiling itself: 1001 must be rejected at COMPILE time by
    the le=1000 bound — never accepted and left to run away."""
    registry, _ = _registry()
    with pytest.raises(CompilationError, match="less than or equal to 1000"):
        compile_graph(Definition.model_validate(_loop_definition(1001)), registry=registry)


def test_max_iterations_zero_fails_compilation() -> None:
    registry, _ = _registry()
    with pytest.raises(CompilationError, match="greater than or equal to 1"):
        compile_graph(Definition.model_validate(_loop_definition(0)), registry=registry)


async def test_long_loop_parks_mid_flight_and_resumes_to_completion() -> None:
    """Park a 250-iteration loop ~halfway via the pause poll, then resume
    on a FRESH scheduler from the durable checkpoint. Iteration integrity
    is the forcing function: the combined body call sequence must still be
    exactly 1..250 with no gap and no repeat at the seam, and the resumed
    half must have run from checkpoint state (not restarted)."""
    iterations = 250
    registry, body = _registry()
    graph = compile_graph(
        Definition.model_validate(_loop_definition(iterations)), registry=registry
    )
    checkpointer = MemoryCheckpointer()

    # The pause poll runs before every super-step; pausing at poll ~260
    # lands us mid-loop (each iteration is ~2 polls).
    polls = {"n": 0}

    async def _pause() -> bool:
        polls["n"] += 1
        return polls["n"] == 260

    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(FakeEmitter()),
        registry=registry,
        pause_check=_pause,
    )
    parked = await scheduler.run(run_id="run-loop-park", max_steps=_steps_for(iterations))
    assert parked.status is RunStatus.PAUSED
    ran_before_park = len(body.iterations_seen)
    assert 50 < ran_before_park < iterations  # genuinely mid-flight

    latest = await checkpointer.latest_checkpoint("run-loop-park")
    assert latest is not None

    fresh = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    resumed = await fresh.resume(
        run_id="run-loop-park",
        checkpoint_id=latest.checkpoint_id,
        max_steps=_steps_for(iterations),
    )

    assert resumed.status is RunStatus.COMPLETED, resumed.error
    # Seam integrity: one continuous engine-carried sequence across the park.
    assert body.iterations_seen == list(range(1, iterations + 1))
    assert resumed.last_outputs["loop"]["iteration"] == iterations
    assert resumed.last_outputs["final"]["result"] == "DONE"
