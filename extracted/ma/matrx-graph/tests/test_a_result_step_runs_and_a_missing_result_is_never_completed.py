"""Guards (2026-10-27, run f2735de2 of workflow 84da90c2): the result step had a DATA and an
ERROR connection from one optional side step. The side step succeeded, its error connection
pruned, the error-handler gate dropped the result step — and the run read "completed" with no
result. Now:

* an error connection whose source also feeds the step normally is an input alternative, never
  a gate; any error connection into a declared deliverable is an input, never a gate;
* a pure error handler (error connection only from its source) still runs only on an error;
* a run whose declared deliverables ALL never ran ends FAILED with ``deliverable_never_ran``;
* a For Each's body step is never an entry step (it is reached only through the dispatch).
"""

from __future__ import annotations

from typing import Any, ClassVar

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
    model_config = ConfigDict(extra="forbid")

    text: str = "ok"


def _spec(node_type: str) -> NodeSpec:
    return NodeSpec(
        type=node_type,
        category=NodeCategory.DATA,
        display_name=node_type,
        description="result-step test node",
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


class _Ok:
    spec: ClassVar[NodeSpec] = _spec("test.res_ok")

    def __init__(self) -> None:
        self.seen: dict[str, dict[str, Any]] = {}

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Out]:
        self.seen[ctx.node_id] = inputs.model_dump()
        return success(_Out(text="ok"))


class _Boom:
    spec: ClassVar[NodeSpec] = _spec("test.res_boom")

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Out]:
        raise RuntimeError("the side step could not read the page")


def _registry(*executors: Any) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    for ex in executors:
        reg.register(ex, overwrite=True)
    return reg


def _node(node_id: str, node_type: str, **data: Any) -> dict:
    return {"id": node_id, "type": node_type, "position": {"x": 0, "y": 0}, "data": {"config": {}, **data}}


def _data(eid: str, src: str, tgt: str, **mappings: str) -> dict:
    return {"id": eid, "source": src, "target": tgt, "data": {"kind": "data", "mappings": mappings or {"a": "text"}}}


def _error(eid: str, src: str, tgt: str) -> dict:
    return {"id": eid, "source": src, "target": tgt, "data": {"kind": "error", "mappings": {"side_error": "$FULL_PAYLOAD"}}}


async def _run(definition: dict, registry: NodeRegistry, run_id: str):
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry)
    return await scheduler.run(run_id=run_id)


def _paired(side_type: str, *, deliverable: bool | None = None) -> dict:
    """start → side (optional) → result by DATA and by ERROR; start → result by DATA."""
    extra = {} if deliverable is None else {"deliverable": deliverable}
    return {
        "nodes": [
            _node("start", "test.res_ok"),
            _node("side", side_type, optional=True),
            _node("result", "test.res_ok", **extra),
        ],
        "edges": [
            _data("e1", "start", "side"),
            _data("e2", "start", "result", main="text"),
            _data("e3", "side", "result", side="text"),
            _error("e4", "side", "result"),
        ],
    }


async def test_a_result_step_with_data_and_error_from_one_side_step_runs_when_the_side_step_succeeds():
    ok = _Ok()
    result = await _run(_paired("test.res_ok"), _registry(ok), "paired-ok")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "result" in result.last_outputs, "the result step was dropped by the error gate"
    assert ok.seen["result"].get("side") == "ok"


async def test_a_result_step_with_data_and_error_from_one_side_step_runs_when_the_side_step_fails():
    ok = _Ok()
    result = await _run(_paired("test.res_boom"), _registry(ok, _Boom()), "paired-boom")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "result" in result.last_outputs
    assert "side_error" in ok.seen["result"], ok.seen["result"]


async def test_an_error_connection_into_a_declared_deliverable_is_an_input_never_a_gate():
    ok = _Ok()
    definition = {
        "nodes": [
            _node("start", "test.res_ok"),
            _node("side", "test.res_ok", optional=True),
            _node("result", "test.res_ok", deliverable=True),
        ],
        "edges": [_data("e1", "start", "side"), _data("e2", "start", "result"), _error("e3", "side", "result")],
    }
    result = await _run(definition, _registry(ok), "deliverable-error-input")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "result" in result.last_outputs


async def test_a_pure_error_handler_still_runs_only_on_an_error():
    ok = _Ok()
    definition = {
        "nodes": [_node("a", "test.res_ok"), _node("b", "test.res_ok"), _node("handler", "test.res_ok")],
        "edges": [_error("e1", "a", "handler"), _data("e2", "b", "handler")],
    }
    result = await _run(definition, _registry(ok), "pure-handler")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "handler" not in result.last_outputs


async def test_a_run_whose_declared_result_never_ran_ends_failed_with_a_named_cause():
    definition = {
        "nodes": [
            _node("start", "test.res_ok"),
            _node("side", "test.res_boom", optional=True),
            _node("result", "test.res_ok", deliverable=True),
        ],
        "edges": [_data("e1", "start", "side"), _data("e2", "side", "result")],
    }
    result = await _run(definition, _registry(_Ok(), _Boom()), "never-ran")
    assert result.status is RunStatus.FAILED, result.status
    assert result.stopped and result.stopped["reason"] == "deliverable_never_ran"
    assert result.failure is not None and result.failure.step_id == "side", result.failure
    assert "'result' never ran because 'side' failed" in (result.error or ""), result.error


async def test_a_run_without_a_declared_deliverable_is_unchanged():
    definition = {
        "nodes": [_node("start", "test.res_ok"), _node("side", "test.res_boom", optional=True), _node("after", "test.res_ok")],
        "edges": [_data("e1", "start", "side"), _data("e2", "side", "after")],
    }
    result = await _run(definition, _registry(_Ok(), _Boom()), "no-deliverable")
    assert result.status is RunStatus.COMPLETED, result.error


def test_a_for_each_body_is_never_an_entry_step():
    definition = {
        "nodes": [
            _node("start", "test.res_ok"),
            {"id": "each", "type": "control.map", "position": {"x": 0, "y": 0},
             "data": {"config": {"target_node_id": "body"}}},
            _node("body", "test.res_ok"),
        ],
        "edges": [_data("e1", "start", "each", items="text")],
    }
    graph = compile_graph(Definition.model_validate(definition), registry=_registry(_Ok()))
    assert graph.entry_node_ids == ("start",), graph.entry_node_ids


# --- 2026-10-27 review round: only a FAULT fails a run; a branch not taken never does ------------


def _branch(node_id: str, predicate: str) -> dict:
    return {"id": node_id, "type": "control.branch", "position": {"x": 0, "y": 0},
            "data": {"config": {"predicate": predicate}}}


def _handle(eid: str, src: str, handle: str, tgt: str) -> dict:
    return {"id": eid, "source": src, "sourceHandle": handle, "target": tgt,
            "data": {"kind": "data", "mappings": {"a": "text"}}}


def _show(node_id: str, **data: Any) -> dict:
    return {"id": node_id, "type": "output.to_frontend", "position": {"x": 0, "y": 0},
            "data": {"config": {}, **data}}


async def test_a_branch_not_taken_before_the_result_step_completes_the_run():
    """Agent build (f49a418d) ends at 'stopped' / 'needs a model' and never reaches its result
    steps BY DESIGN — that is a finish, never deliverable_never_ran."""
    definition = {
        "nodes": [_node("start", "test.res_ok"), _branch("decide", "False"),
                  _node("result", "test.res_ok", deliverable=True)],
        "edges": [{"id": "e1", "source": "start", "target": "decide",
                   "data": {"kind": "data", "mappings": {"text": "text"}}},
                  _handle("e2", "decide", "true", "result")],
    }
    result = await _run(definition, _registry(_Ok()), "branch-not-taken")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "result" not in result.last_outputs


async def test_an_end_step_reached_instead_of_the_show_on_screen_steps_completes_the_run():
    definition = {
        "nodes": [_node("start", "test.res_ok"), _branch("decide", "True"),
                  _node("end_stopped", "test.res_ok"), _show("show_result")],
        "edges": [{"id": "e1", "source": "start", "target": "decide",
                   "data": {"kind": "data", "mappings": {"text": "text"}}},
                  _handle("e2", "decide", "true", "end_stopped"),
                  _handle("e3", "decide", "false", "show_result")],
    }
    result = await _run(definition, _registry(_Ok()), "end-step")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "end_stopped" in result.last_outputs and "show_result" not in result.last_outputs


async def test_a_show_on_screen_step_is_a_deliverable_by_default_so_an_error_connection_never_gates_it():
    """``output.*`` steps are deliverables with no ``data.deliverable`` flag (THE deliverable
    rule): data from one step + an error connection from another successful step is an input,
    not a gate, so the step runs."""
    definition = {
        "nodes": [_node("start", "test.res_ok"), _node("side", "test.res_ok", optional=True),
                  _show("show_result")],
        "edges": [_data("e1", "start", "side"), _data("e2", "start", "show_result"),
                  _error("e3", "side", "show_result")],
    }
    result = await _run(definition, _registry(_Ok()), "output-default")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "show_result" in result.last_outputs


async def test_an_optional_result_step_that_fails_is_fail_soft():
    definition = {
        "nodes": [_node("start", "test.res_ok"),
                  _node("result", "test.res_boom", optional=True, deliverable=True)],
        "edges": [_data("e1", "start", "result")],
    }
    result = await _run(definition, _registry(_Ok(), _Boom()), "optional-deliverable")
    assert result.status is RunStatus.COMPLETED, (result.status, result.error)
    assert not (result.stopped or {}).get("reason") == "deliverable_never_ran"


async def test_a_resumed_run_is_judged_on_its_whole_history():
    """The side step failed in the FIRST leg (before the pause); the resumed leg ran only the
    pause. The result step never ran because of that failure, so the run is not completed."""
    definition = {
        "nodes": [
            _node("start", "test.res_ok"),
            _node("side", "test.res_boom", optional=True),
            _node("result", "test.res_ok", deliverable=True),
            {"id": "pause", "type": "control.human_input", "position": {"x": 0, "y": 0},
             "data": {"config": {"title": "One question", "preset": "free_text", "prompt": "Why?"}}},
            _node("after", "test.res_ok"),
        ],
        "edges": [_data("e1", "start", "side"), _data("e2", "side", "result"),
                  {"id": "e3", "source": "start", "target": "pause",
                   "data": {"kind": "data", "mappings": {"context": "text"}}},
                  _data("e4", "pause", "after", answer="answer")],
    }
    registry = _registry(_Ok(), _Boom())
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    first = await scheduler.run(run_id="resumed")
    assert first.status is RunStatus.INTERRUPTED, (first.status, first.error)
    parked = await checkpointer.latest_checkpoint("resumed")
    resumed_scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    result = await resumed_scheduler.resume(
        run_id="resumed", checkpoint_id=parked.checkpoint_id, resume_value={"answer": "because"}
    )
    assert result.status is RunStatus.FAILED, (result.status, result.error)
    assert result.stopped and result.stopped["reason"] == "deliverable_never_ran"
    assert "'result' never ran because 'side' failed" in (result.error or ""), result.error
