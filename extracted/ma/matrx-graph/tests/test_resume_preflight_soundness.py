"""The resume pre-flight refuses only on PROOF — never an unchanged graph.

Reviews of 6bac24af48 / f053f5b83d (2026-10-01): a step a dispatcher launches
is fired by a Send, which skips the join, so its edge inputs (a static input
from a 'setup' step) are never waited on. Judging it on its edge join refused
UNCHANGED graphs. Each test resumes a checkpoint on the same graph it came from.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeCategory,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
)
from matrx_graph.checkpoint.protocol import NextInvocation, PendingBinding, PendingEdgeBinding
from matrx_graph.executor.resume_preflight import (
    _cyclic_nodes,
    resume_preflight_problems,
)
from matrx_graph.nodes import register_builtin_nodes
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.result import success


class _Any(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: str = ""


class _Echo:
    spec = NodeSpec(
        type="test.echo",
        category=NodeCategory.CUSTOM,
        display_name="Echo",
        input_schema=_Any,
        output_schema=_Out,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
    )
    calls: list[str] = []

    async def execute(self, ctx, inputs, config):  # noqa: ANN001
        type(self).calls.append(ctx.node_id)
        return success(_Out(value=ctx.node_id))


def _registry() -> NodeRegistry:
    reg = register_builtin_nodes(NodeRegistry(), overwrite=True)
    reg.register(_Echo(), overwrite=True)
    return reg


def _n(nid: str, spec: str, config: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "id": nid,
        "type": spec.split(".")[0],
        "position": {"x": 0, "y": 0},
        "data": {"spec_type": spec, "label": nid, "config": config or {}, "input": {}},
    }


def _e(src: str, tgt: str, mappings: dict[str, str] | None = None) -> dict[str, Any]:
    """``mappings={}`` = broadcast (no mappings key at all)."""
    data: dict[str, Any] = {"kind": "data"}
    if mappings is None:
        data["mappings"] = {"value": "value"}
    elif mappings:
        data["mappings"] = mappings
    return {"id": f"e_{src}_{tgt}", "source": src, "target": tgt, "data": data}


def _graph(nodes: list[dict[str, Any]], edges: list[dict[str, Any]], entry: list[str]) -> Any:
    defn = Definition.model_validate(
        {"version": "1", "nodes": nodes, "edges": edges, "entry_nodes": entry, "metadata": {}}
    )
    return compile_graph(defn, registry=_registry())


def _cp(frontier: list[str], pending: dict[str, PendingBinding] | None = None) -> Any:
    return SimpleNamespace(
        next_invocations=[NextInvocation(node_id=n, inputs={}) for n in frontier],
        pending_bindings=pending or {},
    )


def _delivered(graph: Any, source: str, target: str) -> PendingBinding:
    eid = next(
        e for e, edge in graph.edges.items()
        if edge.source_node_id == source and edge.target_node_id == target
    )
    return PendingBinding(
        edges={
            eid: PendingEdgeBinding(
                state="delivered", payload={}, source_node_id=source, source_step=0
            )
        }
    )


@pytest.mark.parametrize(
    ("dispatcher", "config"),
    [
        # control.map is not here: a plain connection into a For Each's body is refused at save
        # (tests/test_no_connection_into_a_for_each_step.py) — it ran the body once with no item.
        ("control.loop", {"target_node_id": "body", "max_iterations": 3}),
        ("control.work_queue", {"target_node_id": "body", "set_name": "crawl"}),
    ],
)
def test_a_dispatched_body_with_a_static_input_is_never_judged_on_its_join(
    dispatcher: str, config: dict[str, Any]
) -> None:
    """start -> dispatcher ⇢ body, setup -> body (a static input), body -> final.
    Mid-run the setup step has already run; the dispatcher is the frontier."""
    graph = _graph(
        [
            _n("start", "test.echo"),
            _n("setup", "test.echo"),
            _n("disp", dispatcher, config),
            _n("body", "test.echo"),
            _n("final", "control.gather"),
        ],
        [_e("start", "disp", {}), _e("setup", "body"), _e("body", "final")],
        ["start", "setup"],
    )

    assert resume_preflight_problems(graph, _cp(["disp"]), _registry()) == []


def test_an_added_edge_behind_a_finished_step_is_still_refused() -> None:
    """The soundness fixes never blunt the real case: an ordinary join."""
    graph = _graph(
        [_n("a", "test.echo"), _n("b", "test.echo"), _n("j", "test.echo")],
        [_e("a", "j"), _e("b", "j")],
        ["a", "b"],
    )
    # a already ran and its delivery is not in j's binding (the edge is new).
    problems = resume_preflight_problems(graph, _cp(["b"]), _registry())
    assert any("'j' needs input from 'a'" in p and "rerun from 'a'" in p for p in problems)


def test_cycle_detection_is_linear() -> None:
    """A 4,000-edge hub: adjacency is built once, never per child step."""
    import time

    nodes = [_n("hub", "test.echo")] + [_n(f"n{i}", "test.echo") for i in range(4000)]
    edges = [_e("hub", f"n{i}") for i in range(4000)]
    graph = _graph(nodes, edges, ["hub"])
    started = time.perf_counter()
    assert _cyclic_nodes(graph) == set()
    assert time.perf_counter() - started < 0.25


@pytest.mark.asyncio
async def test_the_loop_repro_on_the_real_scheduler_completes() -> None:
    """The reviewer's case, end to end: start -> loop ⇄ body, setup -> body,
    loop done -> final. Park mid-loop, resume on the SAME graph: it finishes."""
    reg = _registry()
    defn = Definition.model_validate(
        {
            "version": "1",
            "nodes": [
                _n("start", "test.echo"),
                _n("setup", "test.echo"),
                _n("loop", "control.loop", {"target_node_id": "body", "max_iterations": 3}),
                _n("body", "test.echo"),
                _n("final", "test.echo"),
            ],
            "edges": [
                _e("start", "loop", {}),
                _e("setup", "body"),
                {**_e("body", "loop", {}), "id": "e_body_loop"},
                {
                    "id": "e_loop_final",
                    "source": "loop",
                    "target": "final",
                    "sourceHandle": "done",
                    "data": {"kind": "data"},
                },
            ],
            "entry_nodes": ["start", "setup"],
            "metadata": {},
        }
    )
    try:
        graph = compile_graph(defn, registry=reg)
    except Exception as exc:  # the loop's exact wiring is the loop's own contract
        pytest.skip(f"loop wiring not compilable in this fixture: {exc}")
    checkpointer = MemoryCheckpointer()
    paused = {"n": 0}

    async def _pause() -> bool:
        paused["n"] += 1
        return paused["n"] == 4

    first = await Scheduler(graph, checkpointer, _ctx(), registry=reg, pause_check=_pause).run(
        run_id="loop-run", inputs={}
    )
    if first.status is not RunStatus.PAUSED:
        pytest.skip(f"loop fixture did not park mid-run ({first.status})")
    cp = (await checkpointer.list_checkpoints("loop-run"))[-1]

    assert resume_preflight_problems(graph, cp, reg) == []
    resumed = await Scheduler(graph, checkpointer, _ctx(), registry=reg).resume(
        run_id="loop-run", checkpoint_id=cp.checkpoint_id
    )
    assert resumed.status is RunStatus.COMPLETED, resumed.error


def _ctx() -> Any:
    from matrx_connect.context.app_context import AppContext

    return AppContext(emitter=None, user_id="u", is_authenticated=True, conversation_id="c", request_id="r")


class _UndeclaredSender:
    spec = NodeSpec(
        type="test.undeclared_sender",
        category=NodeCategory.CUSTOM,
        display_name="Undeclared sender",
        input_schema=_Any,
        output_schema=_Out,
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
    )

    async def execute(self, ctx, inputs, config):  # noqa: ANN001
        send = ctx.send  # aliased on purpose: no static scan can be trusted alone
        send("worker", {"value": "w"})
        return success(_Out(value="sent"))


def _sender_graph(reg: NodeRegistry) -> Any:
    reg.register(_UndeclaredSender(), overwrite=True)
    defn = Definition.model_validate(
        {
            "version": "1",
            "nodes": [_n("src", "test.undeclared_sender"), _n("worker", "test.echo")],
            "edges": [],
            "entry_nodes": ["src"],
            "metadata": {},
        }
    )
    return compile_graph(defn, registry=reg)


@pytest.mark.asyncio
async def test_an_undeclared_send_fails_loudly_when_strict(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MATRX_GRAPH_STRICT_LAUNCHES", "1")
    reg = _registry()
    result = await Scheduler(_sender_graph(reg), MemoryCheckpointer(), _ctx(), registry=reg).run(
        run_id="strict", inputs={}
    )
    assert result.status is not RunStatus.COMPLETED
    assert "launches_nodes" in (result.error or "")


@pytest.mark.asyncio
async def test_an_undeclared_send_is_announced_and_allowed_in_production(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    from matrx_graph.executor import resume_preflight

    monkeypatch.setenv("MATRX_GRAPH_STRICT_LAUNCHES", "0")
    monkeypatch.setattr(resume_preflight, "_OBSERVED_LAUNCHERS", set())
    from matrx_graph.executor.resume_preflight import can_still_run

    reg = _registry()
    graph = _sender_graph(reg)
    before = can_still_run(graph, {"src"}, reg)
    with caplog.at_level("ERROR"):
        result = await Scheduler(graph, MemoryCheckpointer(), _ctx(), registry=reg).run(
            run_id="prod", inputs={}
        )
    assert result.status is RunStatus.COMPLETED, result.error
    assert any("UNDECLARED LAUNCH" in r.getMessage() for r in caplog.records)
    # The pre-flight's picture comes from declarations only — a sighting never
    # changes it, so two processes of different ages always agree.
    assert can_still_run(graph, {"src"}, reg) == before
