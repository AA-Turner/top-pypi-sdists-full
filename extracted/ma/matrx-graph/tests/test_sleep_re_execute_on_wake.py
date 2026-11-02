"""A polling park (``re_execute`` in the sleep marker) is RE-RUN on every wake, never answered by a value.

The node under test asks a mutable world "are we done?" and parks with ``re_execute`` while not.
Each resume — whatever value it carries, from the same or a FRESH scheduler (the crash / recovery
leg) — must execute the node again; the downstream step runs exactly once, after the world is done.

Red without the scheduler's ``re_executes_on_wake`` branch: the first resume records the resume
value as the poller's output, the poller never re-runs, and the run completes with the stale value.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
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
from matrx_graph.nodes.flow.sleep import RE_EXECUTE_ON_WAKE, SLEEP_MARKER, re_executes_on_wake
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")

    done: int = 0
    polls: int = 0


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Poller:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.poller",
        category=NodeCategory.CONTROL,
        display_name="Poller",
        description="Parks until the world says done.",
        input_schema=_In,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        can_interrupt=True,
    )

    def __init__(self, world: dict[str, Any], re_execute: bool = True) -> None:
        self.world = world
        self.polls = 0
        self.re_execute = re_execute

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, _c: _Cfg) -> NodeResult[_Out]:
        self.polls += 1
        if self.world["done"]:
            return success(_Out(done=self.world["done"], polls=self.polls))
        wake = datetime.now(UTC) + timedelta(hours=1)
        marker: dict[str, Any] = {"wake_at": wake.isoformat(), "duration_seconds": 3600.0, "node_id": ctx.node_id}
        if self.re_execute:
            marker[RE_EXECUTE_ON_WAKE] = True
        ctx.interrupt({"prompt": "waiting", SLEEP_MARKER: marker, "resume_output": {"stale": True}})
        raise AssertionError("unreachable")


class _Sink:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.after_poll",
        category=NodeCategory.DATA,
        display_name="After",
        description="Records what it got.",
        input_schema=_In,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, _c: _Cfg) -> NodeResult[_Out]:
        self.calls.append(inputs.model_dump())
        return success(_Out(done=int(inputs.model_dump().get("done") or 0)))


def _graph(poller: _Poller) -> tuple[Any, NodeRegistry, _Sink]:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    sink = _Sink()
    reg.register(poller)
    reg.register(sink)
    definition = Definition.model_validate({
        "nodes": [
            {"id": "poll", "type": "test.poller", "position": {"x": 0, "y": 0}, "data": {}},
            {"id": "after", "type": "test.after_poll", "position": {"x": 200, "y": 0}, "data": {}},
        ],
        "edges": [{"id": "e1", "source": "poll", "target": "after"}],
    })
    return compile_graph(definition, registry=reg), reg, sink


def _scheduler(graph: Any, cp: MemoryCheckpointer, reg: NodeRegistry) -> Scheduler:
    return Scheduler(graph, cp, make_app_context(FakeEmitter()), registry=reg)


async def test_every_wake_re_runs_the_poll_and_the_run_moves_on_once() -> None:
    world = {"done": 0}
    poller = _Poller(world)
    graph, reg, sink = _graph(poller)
    cp = MemoryCheckpointer()

    first = await _scheduler(graph, cp, reg).run(run_id="poll-1")
    assert first.status is RunStatus.INTERRUPTED and poller.polls == 1
    park1 = await cp.latest_checkpoint("poll-1")
    assert park1 is not None and re_executes_on_wake(park1.interrupt_payload)

    # Wake 1 (a value is passed and must be IGNORED): still not done → parks again on a NEW checkpoint.
    again = await _scheduler(graph, cp, reg).resume(run_id="poll-1", checkpoint_id=park1.checkpoint_id,
                                                    resume_value={"stale": True})
    assert again.status is RunStatus.INTERRUPTED, again.status
    assert poller.polls == 2 and sink.calls == []
    park2 = await cp.latest_checkpoint("poll-1")
    assert park2 is not None and park2.checkpoint_id != park1.checkpoint_id

    # The world finishes; a FRESH scheduler (the restarted worker) resumes with an empty value.
    world["done"] = 7
    final = await _scheduler(graph, cp, reg).resume(run_id="poll-1", checkpoint_id=park2.checkpoint_id,
                                                    resume_value={})
    assert final.status is RunStatus.COMPLETED, final.status
    assert poller.polls == 3
    assert len(sink.calls) == 1 and sink.calls[0].get("done") == 7, sink.calls
    assert final.last_outputs["poll"]["done"] == 7


async def test_a_plain_sleep_park_still_takes_its_resume_value() -> None:
    """Without the flag nothing changes: the resume value IS the parked step's output."""
    world = {"done": 0}
    poller = _Poller(world, re_execute=False)
    graph, reg, sink = _graph(poller)
    cp = MemoryCheckpointer()
    await _scheduler(graph, cp, reg).run(run_id="poll-2")
    park = await cp.latest_checkpoint("poll-2")
    assert park is not None and not re_executes_on_wake(park.interrupt_payload)
    final = await _scheduler(graph, cp, reg).resume(run_id="poll-2", checkpoint_id=park.checkpoint_id,
                                                    resume_value={"done": 3})
    assert final.status is RunStatus.COMPLETED
    assert poller.polls == 1 and sink.calls and sink.calls[0].get("done") == 3


def test_the_flag_is_read_from_either_interrupt_shape() -> None:
    payload = {SLEEP_MARKER: {"wake_at": "x", RE_EXECUTE_ON_WAKE: True}}
    assert re_executes_on_wake(payload)
    assert re_executes_on_wake({"node_id": "n", "payload": payload})
    assert not re_executes_on_wake({SLEEP_MARKER: {"wake_at": "x"}})
    assert not re_executes_on_wake({SLEEP_MARKER: {RE_EXECUTE_ON_WAKE: "yes"}})
    assert not re_executes_on_wake(None)
