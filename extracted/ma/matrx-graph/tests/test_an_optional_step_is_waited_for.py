"""The step an optional step feeds WAITS for it, and hears "absent" when it fails.

THE USE CASE (Smart Add Identify parent d6d9891e, 2026-10-28): every unit of work is a
``subgraph.call`` (slow, seconds) whose answer an adapter (``data.transform``) reshapes for the
screen. The adapter is fed by the unit (``s``) AND by the fast ``intake`` step (``excl``). With the
unit marked ``data.optional`` (Smart Add's code is fail-soft per side step), a unit failure
PRUNED its connection like a branch not taken, so the adapter fired on ``excl`` alone and its
``inputs['s']`` raised ``KeyError: 's'`` — the round failed anyway, inside the adapter, with a
sentence that names nothing. The parent had to make every unit call required, so ONE unit failure
failed the whole round.

THE RULE: an optional step's normal connections DELIVER when it fails — ``None`` under each
mapped field (the step is absent) — so the step it feeds waits for it, fires once with every
input key present, and can test ``inputs['s'] is None``. Unchanged: a required step's failure
(caught by its ERROR connection) still stops what depends on it; an optional step that SUCCEEDS
delivers its answer; an optional step skipped by 'Only when' delivers its 'If skipped' value;
a fanned item's failure is still its For Each's hole.

THE BREAKS: the scheduler prunes an optional failure's connections again (the adapter runs on
its other inputs and raises), or delivers before the slow optional step finished.
"""

from __future__ import annotations

import asyncio
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

SLOW_S = 0.3


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: str = ""


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: str = ""


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")

    seconds: float = 0.0
    fail: bool = False


class _SlowUnit:
    """A slow unit of work: sleeps, then answers ``value`` or fails."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.slow_unit",
        category=NodeCategory.DATA,
        display_name="Slow unit",
        description="Sleeps, then answers or fails.",
        input_schema=_In,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        await asyncio.sleep(config.seconds)
        if config.fail:
            raise RuntimeError("the unit failed on purpose")
        return success(_Out(value=f"answer:{inputs.value}"))


def _node(nid: str, type_: str, config: dict[str, Any], **data: Any) -> dict[str, Any]:
    return {"id": nid, "type": type_, "position": {"x": 0, "y": 0}, "data": {"config": config, **data}}


def _edge(eid: str, source: str, target: str, mappings: dict[str, str] | None, **data: Any) -> dict[str, Any]:
    return {"id": eid, "source": source, "target": target, "data": {"kind": "data", "mappings": mappings, **data}}


#: The adapter the parent writes: absent unit -> an empty list, never a KeyError.
ADAPTER = "{'rows': [] if inputs['s'] is None else [inputs['s']['value']], 'excl': inputs['excl']}"


def _definition(*, fail: bool, optional: bool = True, when: str | None = None) -> Definition:
    """intake -> unit (slow, optional) -> adapter ; intake -> adapter (fast) ; adapter -> result."""
    unit_data: dict[str, Any] = {"optional": True} if optional else {}
    if when is not None:
        unit_data.update({"when": when, "if_skipped": "{'value': 'skipped'}"})
    nodes = [
        _node("intake", "data.transform", {"expression": "{'url': 'x', 'excl': ['k'], 'go': True}"}),
        _node("unit", "test.slow_unit", {"seconds": SLOW_S, "fail": fail}, **unit_data),
        _node("adapter", "data.transform", {"expression": ADAPTER}),
        _node("other", "data.transform", {"expression": "'OTHER'"}),
        _node("result", "data.transform", {"expression": "{'a': inputs['a'], 'o': inputs['o']}"}),
    ]
    edges = [
        _edge("i_u", "intake", "unit", {"value": "url", **({"go": "go"} if when else {})}),
        _edge("u_a", "unit", "adapter", {"s": "$FULL_PAYLOAD"}),
        _edge("i_a", "intake", "adapter", {"excl": "excl"}),
        _edge("i_o", "intake", "other", None),
        _edge("a_r", "adapter", "result", {"a": "$FULL_PAYLOAD"}),
        _edge("o_r", "other", "result", {"o": "$FULL_PAYLOAD"}),
    ]
    return Definition.model_validate({"nodes": nodes, "edges": edges, "entry_nodes": ["intake"]})


async def _run(definition: Definition, run_id: str):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_SlowUnit())
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    return await scheduler.run(run_id=run_id), emitter


def _completed(emitter: FakeEmitter) -> list[str]:
    return [
        e["node_id"]
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == "node_completed"
    ]


async def test_an_optional_step_that_succeeds_is_waited_for():
    result, emitter = await _run(_definition(fail=False), "opt-ok")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["result"]["a"] == {"rows": ["answer:x"], "excl": ["k"]}
    done = _completed(emitter)
    assert done.index("unit") < done.index("adapter"), done


async def test_an_optional_step_that_fails_delivers_absent_and_the_round_goes_on():
    result, emitter = await _run(_definition(fail=True), "opt-fail")
    assert result.status is RunStatus.COMPLETED, result.error
    done = _completed(emitter)
    assert "adapter" in done, "the adapter never ran after the optional unit failed"
    # The adapter WAITED for the unit and heard it was absent: no KeyError, every key present.
    assert result.last_outputs["result"]["a"] == {"rows": [], "excl": ["k"]}
    assert result.last_outputs["result"]["o"] == {"result": "OTHER"}


async def test_an_optional_step_skipped_by_only_when_delivers_its_if_skipped_value():
    result, _ = await _run(_definition(fail=True, when="inputs['go'] is False"), "opt-skip")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["result"]["a"] == {"rows": ["skipped"], "excl": ["k"]}


async def test_an_optional_step_with_only_when_that_runs_and_fails_delivers_absent():
    result, _ = await _run(_definition(fail=True, when="inputs['go'] is True"), "opt-when-fail")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["result"]["a"] == {"rows": [], "excl": ["k"]}


async def test_a_required_step_that_fails_still_fails_the_run():
    result, _ = await _run(_definition(fail=True, optional=False), "req-fail")
    assert result.status is not RunStatus.COMPLETED
