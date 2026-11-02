"""A caller can set how many items of a For Each run at once (``data.concurrency: {"$input": name}``).

2026-10-27: a step's "how many at once" was fixed in the definition, so a shared unit
(``mandate.ask_and_check``) could not be told "at most 2 at a time" by the workflow calling it
(the Brand foundation Curator retries at most 2 at a time; a rate-limited provider; a person's
"go slow" on a large run). The cap may now read a run input, bound once per run, and the
``workflow.fan_out`` ceiling still holds it (min(requested, ceiling)).

The breaks each test names:
- the ref not resolved (the cap ignored)            → peak == the knob default, not 2 / 3
- the ceiling not applied to a run-supplied cap     → peak above max_item_concurrency
- an invalid value accepted (0, "fast", yes/no)     → the step runs instead of failing in words
- a literal or absent cap changed                   → the default-unchanged test fails

Real ``Scheduler`` + ``MemoryCheckpointer``; the only double is the work step (a live counter).
"""

from __future__ import annotations

import asyncio
from typing import Any, ClassVar

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
from matrx_graph import knobs as graph_knobs
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.validation import validate_definition
from pydantic import BaseModel, ConfigDict

from tests._fixtures import make_app_context


class _Item(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Out(BaseModel):
    model_config = ConfigDict(extra="allow")


class _CheckOneBrand:
    """One retry of the Curator's check — counts how many are live at once."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.check_one_brand",
        category=NodeCategory.DATA,
        display_name="Check one brand",
        description="concurrency test step",
        input_schema=_Item,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
    )

    def __init__(self) -> None:
        self.live = 0
        self.peak = 0
        self.calls = 0

    async def execute(self, ctx: NodeExecutionContext, inputs: _Item, config: _Cfg) -> NodeResult[_Out]:
        self.calls += 1
        self.live += 1
        self.peak = max(self.peak, self.live)
        try:
            await asyncio.sleep(0.05)
            return success(_Out(checked=getattr(inputs, "value", None)))
        finally:
            self.live -= 1


def _definition(concurrency: Any, *, items: int = 16, default: Any = 3) -> dict[str, Any]:
    check: dict[str, Any] = {"config": {}, "label": "Check one brand"}
    if concurrency is not None:
        check["concurrency"] = concurrency
    return {
        "variables": [{"name": "at_once", "default": default}],
        "nodes": [
            {
                "id": "each_brand",
                "type": "control.map",
                "position": {"x": 0, "y": 0},
                "data": {
                    "config": {"target_node_id": "check", "payload_key": "value", "max_dispatches": 100},
                    "input": {"items": [f"Acme Outdoor {i}" for i in range(items)]},
                },
            },
            {"id": "check", "type": "test.check_one_brand", "position": {"x": 0, "y": 0}, "data": check},
        ],
        "edges": [],
        "entry_nodes": ["each_brand"],
    }


@pytest.fixture
def policy(monkeypatch):
    holder = {"policy": graph_knobs.FanOutPolicy(default_item_concurrency=4, max_item_concurrency=8)}

    async def _policy() -> graph_knobs.FanOutPolicy:
        return holder["policy"]

    monkeypatch.setattr(graph_knobs, "fan_out_policy", _policy)
    return holder


async def _run(definition: dict[str, Any], inputs: dict[str, Any] | None = None):
    step = _CheckOneBrand()
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(step, overwrite=True)
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    result = await Scheduler(
        graph, MemoryCheckpointer(), make_app_context(), registry=registry, surface_inputs=inputs or {}
    ).run(run_id=f"at-once-{id(step)}")
    return result, step


async def test_the_callers_value_sets_how_many_run_at_once(policy):
    result, step = await _run(_definition({"$input": "at_once"}), {"at_once": 2})
    assert result.status is RunStatus.COMPLETED, result.error
    assert step.calls == 16
    assert step.peak == 2, step.peak

    # The same unit, another caller: its value, not the first one's.
    result, step = await _run(_definition({"$input": "at_once"}), {"at_once": 5})
    assert result.status is RunStatus.COMPLETED, result.error
    assert step.peak == 5, step.peak

    # No value from the caller: the input's declared default.
    result, step = await _run(_definition({"$input": "at_once"}))
    assert result.status is RunStatus.COMPLETED, result.error
    assert step.peak == 3, step.peak


async def test_the_platform_ceiling_still_holds_a_callers_value(policy):
    policy["policy"] = graph_knobs.FanOutPolicy(default_item_concurrency=2, max_item_concurrency=3)
    result, step = await _run(_definition({"$input": "at_once"}), {"at_once": 12})
    assert result.status is RunStatus.COMPLETED, result.error
    assert step.peak == 3, step.peak


@pytest.mark.parametrize("bad", [0, -1, "fast", True, 2.5, "²"])
async def test_a_value_that_is_not_a_whole_number_of_one_or_more_is_refused(policy, bad):
    result, step = await _run(_definition({"$input": "at_once"}), {"at_once": bad})
    assert result.status is RunStatus.ERRORED
    assert step.calls == 0, "the step ran with a cap it should have refused"
    assert "must be a whole number of 1 or more" in str(result.error), result.error


def test_a_bad_cap_is_refused_when_the_workflow_is_saved() -> None:
    registry = register_builtin_nodes(NodeRegistry())
    registry.register(_CheckOneBrand(), overwrite=True)
    unknown = validate_definition(_definition({"$input": "nope"}), registry=registry)
    assert any("'nope', which is not on this workflow's input surface" in i.message for i in unknown.issues)
    zero = validate_definition(_definition({"$input": "at_once", "default": 0}), registry=registry)
    assert any("whole number of 1 or more" in i.message for i in zero.issues)
    superscript = validate_definition(_definition({"$input": "at_once", "default": "²"}), registry=registry)
    assert any("whole number of 1 or more" in i.message for i in superscript.issues)
    ok = validate_definition(_definition({"$input": "at_once"}), registry=registry)
    assert not [i for i in ok.issues if "concurrency" in i.path], ok.issues


async def test_a_written_or_absent_cap_is_unchanged(policy):
    result, step = await _run(_definition(None))
    assert result.status is RunStatus.COMPLETED, result.error
    assert step.peak == 4, step.peak  # the knob's default
    result, step = await _run(_definition(2))
    assert result.status is RunStatus.COMPLETED, result.error
    assert step.peak == 2, step.peak
    result, step = await _run(_definition(20))
    assert result.status is RunStatus.COMPLETED, result.error
    assert step.peak == 8, step.peak  # a written cap is still held by the ceiling


@pytest.mark.parametrize("run_ahead", [True, False])
async def test_a_fault_that_escapes_a_step_stops_the_run_in_words(policy, monkeypatch, run_ahead):
    # The class behind the "²" probe (review of d4fccf78): an exception raised outside the step's
    # own error capture was dropped with the task — the run said COMPLETED with every item unrun.
    from matrx_graph.executor import scheduler as scheduler_module

    monkeypatch.setattr(scheduler_module, "RUN_AHEAD_ENABLED", run_ahead)
    real = scheduler_module.Scheduler._run_invocation

    async def _faulty(self, **kwargs):
        if kwargs["result"].invocation.node_id == "check":
            raise ValueError("the pool handed back a closed connection")
        return await real(self, **kwargs)

    monkeypatch.setattr(scheduler_module.Scheduler, "_run_invocation", _faulty)
    result, step = await _run(_definition(None, items=3))
    assert result.status is RunStatus.ERRORED, result.status
    assert step.calls == 0
    assert "the pool handed back a closed connection" in str(result.error), result.error


async def test_a_gate_fault_that_is_not_an_execution_error_fails_the_step_in_words(policy, monkeypatch):
    from matrx_graph.executor import scheduler as scheduler_module

    async def _broken_gate(self, inv):
        raise KeyError("fan_out policy row")

    monkeypatch.setattr(scheduler_module.Scheduler, "_node_gate", _broken_gate)
    result, step = await _run(_definition(None, items=3))
    assert result.status is RunStatus.ERRORED, result.status
    assert step.calls == 0
    assert "could not start" in str(result.error) and "fan_out policy row" in str(result.error), result.error


class _CancelsItself(_CheckOneBrand):
    """A step whose own code raises CancelledError (a library that cancels its inner wait wrongly)."""

    async def execute(self, ctx: NodeExecutionContext, inputs: _Item, config: _Cfg) -> NodeResult[_Out]:
        self.calls += 1
        raise asyncio.CancelledError("the provider client cancelled its own request")


async def _run_with(step: _CheckOneBrand, definition: dict[str, Any], **scheduler_kwargs: Any):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(step, overwrite=True)
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    return await Scheduler(
        graph, MemoryCheckpointer(), make_app_context(), registry=registry, **scheduler_kwargs
    ).run(run_id=f"stop-{id(step)}")


@pytest.mark.parametrize("run_ahead", [True, False])
async def test_a_step_that_cancels_itself_stops_the_run_in_words(policy, monkeypatch, run_ahead):
    from matrx_graph.executor import scheduler as scheduler_module

    monkeypatch.setattr(scheduler_module, "RUN_AHEAD_ENABLED", run_ahead)
    step = _CancelsItself()
    result = await _run_with(step, _definition(None, items=3))
    assert step.calls >= 1
    assert result.status is RunStatus.ERRORED, result.status
    assert "stopped itself with a cancellation" in str(result.error), result.error


@pytest.mark.parametrize("run_ahead", [True, False])
async def test_a_run_cancel_still_ends_cancelled(policy, monkeypatch, run_ahead):
    from matrx_graph.executor import scheduler as scheduler_module

    monkeypatch.setattr(scheduler_module, "RUN_AHEAD_ENABLED", run_ahead)
    step = _CheckOneBrand()

    async def cancel_once_started() -> bool:
        return step.calls > 0

    two_steps = {
        "nodes": [
            {
                "id": "first",
                "type": "test.check_one_brand",
                "position": {"x": 0, "y": 0},
                "data": {"config": {}, "input": {"value": "Acme Outdoor"}},
            },
            {"id": "second", "type": "test.check_one_brand", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
        ],
        "edges": [
            {"id": "e1", "source": "first", "target": "second", "data": {"kind": "data", "mappings": {"value": "checked"}}}
        ],
        "entry_nodes": ["first"],
    }
    result = await _run_with(step, two_steps, cancel_check=cancel_once_started)
    assert result.status is RunStatus.CANCELLED, (result.status, result.error)
    assert step.calls == 1, "the step after the cancel ran"


class _SignalsStart(_CheckOneBrand):
    """Says when its first item has started, so the drain lands mid-run."""

    def __init__(self) -> None:
        super().__init__()
        self.started = asyncio.Event()

    async def execute(self, ctx: NodeExecutionContext, inputs: _Item, config: _Cfg) -> NodeResult[_Out]:
        self.started.set()
        return await super().execute(ctx, inputs, config)


@pytest.mark.parametrize("run_ahead", [True, False])
async def test_a_drained_run_still_stops_as_a_cancellation(policy, monkeypatch, run_ahead):
    from matrx_graph.executor import scheduler as scheduler_module

    monkeypatch.setattr(scheduler_module, "RUN_AHEAD_ENABLED", run_ahead)
    step = _SignalsStart()
    drive = asyncio.create_task(_run_with(step, _definition(None, items=12)))
    await asyncio.wait_for(step.started.wait(), timeout=5)
    drive.cancel()
    with pytest.raises(asyncio.CancelledError):
        await drive
    assert step.calls < 12, "the drain did not stop the run"
