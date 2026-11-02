"""A time limit on any step (``data.step_clock``) and where the stopped step goes.

Arman, 2026-10-26: profile lookups, scraping, web searches and agent calls each need
a per-step limit, and a step stopped by it must take that step's NORMAL failure path
— the error edge, ``data.optional``, a For Each hole — never a different one.

The break this catches: a timed-out step that skips its failure routing (e.g. the
timeout raised outside the attempt's failure ladder, or cancelling the run) parks
the whole run instead of continuing down the route the author drew.
"""

from __future__ import annotations

import asyncio
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
from matrx_graph import knobs as graph_knobs
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context


class _Open(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Out(BaseModel):
    model_config = ConfigDict(extra="allow")
    text: str = ""


def _spec(node_type: str) -> NodeSpec:
    return NodeSpec(
        type=node_type,
        category=NodeCategory.DATA,
        display_name=node_type,
        description="time-limit test node",
        input_schema=_Open,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        retry=RetryPolicy(max_attempts=1),
    )


class _ProfileLookup:
    """Answers at once for most handles; the stalled one never answers."""

    spec: ClassVar[NodeSpec] = _spec("test.profile_lookup")

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Out]:
        handle = (inputs.model_extra or {}).get("value", "@stalled")
        if handle == "@stalled":
            await asyncio.sleep(30)
        return success(_Out(text=f"profile of {handle}"))


class _Recorder:
    spec: ClassVar[NodeSpec] = _spec("test.record_error")

    def __init__(self) -> None:
        self.seen: list[dict[str, Any]] = []

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Out]:
        self.seen.append(dict(inputs.model_extra or {}))
        return success(_Out(text="recorded"))


@pytest.fixture(autouse=True)
def _one_second_floor(monkeypatch: pytest.MonkeyPatch):
    # The engine floors every limit at MIN_STEP_SECONDS (5s); scale it to 1s so
    # a 1-second limit really is 1 second in this test.
    monkeypatch.setattr(graph_knobs, "MIN_STEP_SECONDS", 1)


def _node(node_id: str, node_type: str, **data: Any) -> dict:
    return {"id": node_id, "type": node_type, "position": {"x": 0, "y": 0}, "data": {"config": {}, **data}}


async def _run(definition: dict, *extra: Any, run_id: str):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    for ex in (_ProfileLookup(), *extra):
        registry.register(ex, overwrite=True)
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    try:
        result = await asyncio.wait_for(scheduler.run(run_id=run_id), timeout=20)
    except TimeoutError:
        raise AssertionError(
            "the stalled step was never stopped at its own 1s data.step_clock limit"
        ) from None
    return result, emitter


def _failed(emitter: FakeEmitter) -> list[dict]:
    return [
        e for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == "node_failed"
    ]


async def test_an_optional_step_past_its_limit_is_recorded_failed_and_the_run_completes():
    result, emitter = await _run(
        {"nodes": [_node("lookup", "test.profile_lookup", optional=True, step_clock={"seconds": 1})], "edges": []},
        run_id="limit-optional",
    )
    assert result.status is RunStatus.COMPLETED, result.error
    (failed,) = _failed(emitter)
    assert failed["error_type"] == "NodeTimeoutError"
    assert "stopped after 1s" in failed["error_message"]


async def test_a_step_past_its_limit_takes_its_error_edge():
    recorder = _Recorder()
    result, _ = await _run(
        {
            "nodes": [
                _node("lookup", "test.profile_lookup", step_clock={"seconds": 1}),
                _node("on_timeout", "test.record_error"),
            ],
            "edges": [{"id": "e_err", "source": "lookup", "target": "on_timeout", "data": {"kind": "error"}}],
        },
        recorder,
        run_id="limit-error-edge",
    )
    assert result.status is RunStatus.COMPLETED, result.error
    (delivered,) = recorder.seen
    assert delivered["code"] == "NodeTimeoutError"


async def test_a_for_each_item_past_its_limit_becomes_a_hole_and_the_others_arrive():
    result, _ = await _run(
        {
            "nodes": [
                {
                    "id": "each_handle",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"target_node_id": "lookup", "payload_key": "value"},
                        "input": {"items": ["@harborwatch", "@stalled", "@ferrytimes"]},
                    },
                },
                _node("lookup", "test.profile_lookup", step_clock={"seconds": 1}, on_item_failure="hole"),
                _node("gather", "control.gather"),
            ],
            "edges": [{"id": "e_g", "source": "lookup", "target": "gather", "data": {"mappings": {"value": "text"}}}],
            "entry_nodes": ["each_handle"],
        },
        run_id="limit-hole",
    )
    assert result.status is RunStatus.COMPLETED, result.error
    gathered = result.last_outputs["gather"]
    assert sorted(gathered["values"]) == ["profile of @ferrytimes", "profile of @harborwatch"]
    (hole,) = gathered["holes"]
    assert hole["error"]["code"] == "NodeTimeoutError"
