"""A called workflow with ``runs_as: "inline"`` runs inside its caller's step (L-SPEED 6d, 2026-11-09).

What each test proves (red first, then green):
- a For each over an inline child: every item runs its own child, the For each's at-once setting holds, and no two
  items share an identity (dispatch id, request conversation) — red with ``invocation_namespace`` ignored;
- a crash mid-child, then the caller's step again: the child's side-effect step is REPLAYED, never run twice — red
  when the inline store records nothing;
- the child's steps reach the caller's stream under the calling step (``call/side``), never its run-level events;
- the child's paid launch asks the spend gate for the CALLER's run.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any, ClassVar

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph, register_builtin_nodes
from matrx_graph import knobs as graph_knobs
from matrx_graph.nodes.subgraph.call import set_subgraph_resolver
from matrx_graph.nodes.subgraph.inline import run_inline_child, runs_inline
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")
    value: str = ""


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: str = ""


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")
    seconds: float = 0.0


def _spec(type_: str, tier: ActionTier, category: NodeCategory = NodeCategory.DATA) -> NodeSpec:
    return NodeSpec(
        type=type_, category=category, display_name=type_, description=type_,
        input_schema=_In, output_schema=_Out, config_schema=_Cfg,
        handles=(HandleSpec(id="in", direction=HandleDirection.INPUT),
                 HandleSpec(id="out", direction=HandleDirection.OUTPUT)),
        determinism=tier,
    )


class _Side:
    """A step with a real effect (a write): it must never run twice for one call."""

    spec: ClassVar[NodeSpec] = _spec("test.inline_side", ActionTier.SIDE_EFFECT)

    def __init__(self) -> None:
        self.writes: list[str] = []
        self.identities: list[tuple[str, str]] = []

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        self.writes.append(inputs.value)
        self.identities.append((ctx.dispatch_id, str(ctx.app.conversation_id)))
        return success(_Out(value=f"{inputs.value}+side"))


class _Slow:
    spec: ClassVar[NodeSpec] = _spec("test.inline_slow", ActionTier.PURE)

    def __init__(self) -> None:
        self.live = 0
        self.peak = 0
        self.runs = 0

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        self.runs += 1
        self.live += 1
        self.peak = max(self.peak, self.live)
        try:
            await asyncio.sleep(config.seconds)
        finally:
            self.live -= 1
        return success(_Out(value=f"{inputs.value}+slow"))


def _child(seconds: float = 0.0) -> Definition:
    return Definition.model_validate({
        "nodes": [
            {"id": "side", "type": "test.inline_side", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
            {"id": "slow", "type": "test.inline_slow", "position": {"x": 0, "y": 0},
             "data": {"config": {"seconds": seconds}}},
        ],
        "edges": [{"id": "e1", "source": "side", "target": "slow",
                   "data": {"kind": "data", "mappings": {"value": "value"}}}],
        "entry_nodes": ["side"],
        "metadata": {"runs_as": "inline"},
    })


def _registry(*steps: Any) -> NodeRegistry:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    for step in steps:
        registry.register(step, overwrite=True)
    return registry


@pytest.fixture(autouse=True)
def _clean():
    set_subgraph_resolver(None)
    yield
    set_subgraph_resolver(None)


@pytest.fixture
def policy(monkeypatch):
    async def _policy() -> graph_knobs.FanOutPolicy:
        return graph_knobs.FanOutPolicy(default_item_concurrency=4, max_item_concurrency=8)

    monkeypatch.setattr(graph_knobs, "fan_out_policy", _policy)


def test_only_a_workflow_that_asks_runs_inline():
    assert runs_inline({"runs_as": "inline"})
    assert not runs_inline({"runs_as": "step"}) and not runs_inline({}) and not runs_inline(None)


async def test_a_for_each_over_an_inline_child_runs_one_child_per_item_at_the_callers_pace(policy):
    side, slow = _Side(), _Slow()
    registry = _registry(side, slow)
    child = compile_graph(_child(seconds=0.05), registry=registry)
    checkpointer = MemoryCheckpointer()

    async def resolver(ctx: Any, _config: Any, inputs: Any) -> dict[str, Any]:
        result = await run_inline_child(ctx, child, checkpointer=checkpointer, registry=registry,
                                        inputs={"value": inputs.model_extra.get("value", "")})
        assert result.status is RunStatus.COMPLETED, result.error
        return {"run_id": ctx.run_id, "last_outputs": result.last_outputs}

    set_subgraph_resolver(resolver)
    parent = compile_graph(Definition.model_validate({
        "nodes": [
            {"id": "each", "type": "control.map", "position": {"x": 0, "y": 0},
             "data": {"config": {"target_node_id": "call", "payload_key": "value"},
                      "input": {"items": [f"item{i}" for i in range(6)]}}},
            {"id": "call", "type": "subgraph.call", "position": {"x": 0, "y": 0},
             "data": {"config": {"definition_id": "child"}, "concurrency": 2}},
        ],
        "edges": [], "entry_nodes": ["each"],
    }), registry=registry)
    emitter = FakeEmitter()
    result = await Scheduler(parent, checkpointer, make_app_context(emitter), registry=registry).run(run_id="parent-1")

    assert result.status is RunStatus.COMPLETED, result.error
    assert sorted(side.writes) == [f"item{i}" for i in range(6)]
    assert slow.runs == 6
    assert slow.peak <= 2, slow.peak  # the For each's at-once setting holds for inline children
    dispatches = [d for d, _ in side.identities]
    conversations = [c for _, c in side.identities]
    assert len(set(dispatches)) == 6, dispatches
    assert len(set(conversations)) == 6, conversations
    # The child's side effect is recorded under the CALLER's run, under the calling step's path.
    recorded = [k for k in checkpointer._outcomes if k[2] == "call/side"]
    assert {k[0] for k in recorded} == {"parent-1"} and len(recorded) == 6
    # Its pure step records nothing durable (a re-run rebuilds it).
    assert not [k for k in checkpointer._outcomes if k[2] == "call/slow"]
    # The child's steps reach the caller's stream under the calling step; its run events never do.
    def _pair(p: Any) -> tuple[Any, Any]:
        p = p if isinstance(p, dict) else (p.model_dump() if hasattr(p, "model_dump") else {})
        return p.get("event"), p.get("node_id")

    names = [_pair(p) for m, p in emitter.events if m == "data"]
    assert ("node_completed", "call/slow") in names
    assert sum(1 for e, _ in names if e == "run_completed") == 1  # the parent's own


def _ctx(app: Any) -> Any:
    return SimpleNamespace(run_id="parent-2", node_id="call", dispatch_id="d-1", item_index=0, firing=0,
                           app=app, thread_id="parent-2")


async def test_a_crash_mid_child_then_the_callers_step_again_never_writes_twice():
    side, slow = _Side(), _Slow()
    registry = _registry(side, slow)
    child = compile_graph(_child(seconds=5), registry=registry)
    checkpointer = MemoryCheckpointer()
    app = make_app_context(FakeEmitter())

    crashed = asyncio.ensure_future(run_inline_child(_ctx(app), child, checkpointer=checkpointer,
                                                     registry=registry, inputs={"value": "x"}))
    for _ in range(200):
        await asyncio.sleep(0.01)
        if slow.live:
            break
    assert side.writes == ["x"] and slow.live == 1
    crashed.cancel()  # the process dies mid-child
    with pytest.raises(asyncio.CancelledError):
        await crashed

    fast = compile_graph(_child(seconds=0), registry=registry)
    again = await run_inline_child(_ctx(app), fast, checkpointer=checkpointer, registry=registry, inputs={"value": "x"})
    assert again.status is RunStatus.COMPLETED, again.error
    assert side.writes == ["x"], side.writes  # replayed, never written twice
    assert again.last_outputs["slow"]["value"] == "x+side+slow"


async def test_the_childs_paid_launch_asks_the_spend_gate_for_the_callers_run():
    from matrx_graph import spend_gate as gate_mod

    asked: list[str] = []

    async def gate(query: Any) -> None:
        asked.append(query.run_id)
        return None

    class _Paid(_Side):
        spec: ClassVar[NodeSpec] = _spec("test.inline_paid", ActionTier.SIDE_EFFECT, NodeCategory.LLM)

    paid = _Paid()
    registry = _registry(paid)
    child = compile_graph(Definition.model_validate({
        "nodes": [{"id": "ask", "type": "test.inline_paid", "position": {"x": 0, "y": 0}, "data": {"config": {}}}],
        "edges": [], "entry_nodes": ["ask"], "metadata": {"runs_as": "inline"},
    }), registry=registry)
    gate_mod.configure_spend_gate(gate)
    try:
        result = await run_inline_child(_ctx(make_app_context(FakeEmitter())), child, checkpointer=MemoryCheckpointer(),
                                        registry=registry, inputs={"value": "q"})
    finally:
        gate_mod.configure_spend_gate(None)
    assert result.status is RunStatus.COMPLETED, result.error
    assert asked == ["parent-2"], asked


async def test_an_inline_child_inside_an_inline_child_nests_its_path_and_identity():
    side, slow = _Side(), _Slow()
    registry = _registry(side, slow)
    grandchild = compile_graph(_child(), registry=registry)
    middle = compile_graph(Definition.model_validate({
        "nodes": [{"id": "inner", "type": "subgraph.call", "position": {"x": 0, "y": 0},
                   "data": {"config": {"definition_id": "grandchild"}}}],
        "edges": [], "entry_nodes": ["inner"], "metadata": {"runs_as": "inline"},
    }), registry=registry)
    checkpointer = MemoryCheckpointer()

    async def resolver(ctx: Any, config: Any, inputs: Any) -> dict[str, Any]:
        graph = grandchild if config.definition_id == "grandchild" else middle
        result = await run_inline_child(ctx, graph, checkpointer=checkpointer, registry=registry, inputs={"value": "v"})
        assert result.status is RunStatus.COMPLETED, result.error
        return {"run_id": ctx.run_id, "last_outputs": result.last_outputs}

    set_subgraph_resolver(resolver)
    emitter = FakeEmitter()
    for item in (0, 1):
        ctx = SimpleNamespace(run_id="parent-3", node_id="outer", dispatch_id="d", item_index=item, firing=0,
                              app=make_app_context(emitter), thread_id="parent-3")
        assert (await run_inline_child(ctx, middle, checkpointer=checkpointer, registry=registry,
                                       inputs={})).status is RunStatus.COMPLETED
    assert side.writes == ["v", "v"]
    assert len({d for d, _ in side.identities}) == 2  # two outer items never share the grandchild's identity
    recorded = sorted(k[2] for k in checkpointer._outcomes if k[0] == "parent-3")
    # the grandchild's write and the middle's call step (a finished call replays whole on a re-run)
    assert recorded == ["outer/inner", "outer/inner", "outer/inner/side", "outer/inner/side"], recorded


def _loop_child(seconds: float) -> Definition:
    return Definition.model_validate({
        "nodes": [
            {"id": "start", "type": "data.transform", "position": {"x": 0, "y": 0}, "data": {"config": {"expression": "0"}}},
            {"id": "loop", "type": "control.loop", "position": {"x": 0, "y": 0},
             "data": {"config": {"target_node_id": "side", "max_iterations": 3, "exit_expression": "1 > 2"}}},
            {"id": "side", "type": "test.inline_side", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
            {"id": "slow", "type": "test.inline_slow", "position": {"x": 0, "y": 0},
             "data": {"config": {"seconds": seconds}}},
        ],
        "edges": [
            {"id": "e1", "source": "start", "target": "loop"},
            {"id": "e2", "source": "side", "target": "loop"},
            {"id": "e3", "source": "loop", "sourceHandle": "done", "target": "slow"},
        ],
        "entry_nodes": ["start"],
        "metadata": {"runs_as": "inline"},
    })


async def test_a_loop_inside_an_inline_child_never_repeats_its_work_on_a_re_run():
    """Review C1 (2026-11-10): a PURE loop is safe to run again, but its sends carry a fresh dispatch id per
    execution — unrecorded, the re-run orphaned the body's recorded writes and wrote 3 more (3 -> 6)."""
    side, slow = _Side(), _Slow()
    registry = _registry(side, slow)
    checkpointer = MemoryCheckpointer()
    app = make_app_context(FakeEmitter())
    crashed = asyncio.ensure_future(run_inline_child(_ctx(app), compile_graph(_loop_child(5), registry=registry),
                                                     checkpointer=checkpointer, registry=registry, inputs={}))
    for _ in range(500):
        await asyncio.sleep(0.01)
        if slow.live:
            break
    first = len(side.writes)
    assert first == 3 and slow.live == 1
    crashed.cancel()
    with pytest.raises(asyncio.CancelledError):
        await crashed
    again = await run_inline_child(_ctx(app), compile_graph(_loop_child(0), registry=registry),
                                   checkpointer=checkpointer, registry=registry, inputs={})
    assert again.status is RunStatus.COMPLETED, again.error
    assert len(side.writes) == first, side.writes


def test_a_child_that_can_wait_is_refused_before_it_runs_inline():
    """Review M1: a question or a timer needs a run to wait in — refused before the first step, never after."""
    from matrx_graph.nodes.subgraph.inline import inline_refusal

    side = _Side()
    registry = _registry(side, _Slow())
    waits = compile_graph(Definition.model_validate({
        "nodes": [
            {"id": "side", "type": "test.inline_side", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
            {"id": "nap", "type": "flow.sleep", "position": {"x": 0, "y": 0}, "data": {"config": {"duration_seconds": 5}}},
        ],
        "edges": [{"id": "e1", "source": "side", "target": "nap"}],
        "entry_nodes": ["side"], "metadata": {"runs_as": "inline"},
    }), registry=registry)
    why = inline_refusal(waits, registry)
    assert why and "nap" in why
    assert inline_refusal(compile_graph(_child(), registry=registry), registry) is None


async def test_a_show_on_screen_step_never_shows_twice_on_a_re_run():
    """Review M4: Show on Screen re-runs safely for its data, but a re-run showed it again."""
    side, slow = _Side(), _Slow()
    registry = _registry(side, slow)
    definition = Definition.model_validate({
        "nodes": [
            {"id": "side", "type": "test.inline_side", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
            {"id": "show", "type": "output.to_frontend", "position": {"x": 0, "y": 0}, "data": {}},
        ],
        "edges": [{"id": "e1", "source": "side", "target": "show"}],
        "entry_nodes": ["side"], "metadata": {"runs_as": "inline"},
    })
    child = compile_graph(definition, registry=registry)
    checkpointer = MemoryCheckpointer()

    def shown(emitter: FakeEmitter) -> int:
        def ev(p: Any) -> Any:
            return p.get("event") if isinstance(p, dict) else getattr(p, "event", None)

        return sum(1 for m, p in emitter.events if m == "data" and ev(p) == "node_emitted")

    first, second = FakeEmitter(), FakeEmitter()
    for emitter in (first, second):
        result = await run_inline_child(_ctx(make_app_context(emitter)), child, checkpointer=checkpointer,
                                        registry=registry, inputs={"value": "x"})
        assert result.status is RunStatus.COMPLETED, result.error
    assert shown(first) == 1 and shown(second) == 0
    assert side.writes == ["x"]
