"""Guards (2026-10-27, run b0e3f868 of wrap-up workflow f3ff47f8): ``wu_state`` had DATA inputs
from ``done`` and ``start`` and ERROR connections from ``record`` and ``notes`` — both of which
lead to ``done`` on success. Both succeeded, both error connections pruned, the error-handler gate
dropped ``wu_state`` and its whole subtree, and the run read "completed".

* An error connection whose source's SUCCESS path reaches the step (directly or through later
  steps) is a convergence: an input alternative, never a gate. The step runs on success (through
  the normal path) and on failure (through the error connection).
* A pure handler — the source's success path goes elsewhere — still runs only on an error.
* RUN-END INVARIANT: a join left with a connection that never resolved raises an
  ``engine.join_never_resolved`` review flag naming the step; never silent.
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
from matrx_graph.checkpoint.protocol import PendingBinding, PendingEdgeBinding
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
        description="error-join test node",
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
    spec: ClassVar[NodeSpec] = _spec("test.ej_ok")

    def __init__(self) -> None:
        self.seen: dict[str, dict[str, Any]] = {}

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Out]:
        self.seen[ctx.node_id] = inputs.model_dump()
        return success(_Out(text="ok"))


class _Boom:
    spec: ClassVar[NodeSpec] = _spec("test.ej_boom")

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Out]:
        raise RuntimeError("the recording could not be fetched")


def _registry(*executors: Any) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    for ex in executors:
        reg.register(ex, overwrite=True)
    return reg


def _node(node_id: str, node_type: str = "test.ej_ok") -> dict:
    return {"id": node_id, "type": node_type, "position": {"x": 0, "y": 0}, "data": {"config": {}}}


def _data(eid: str, src: str, tgt: str, key: str = "a") -> dict:
    return {"id": eid, "source": src, "target": tgt, "data": {"kind": "data", "mappings": {key: "text"}}}


def _error(eid: str, src: str, tgt: str) -> dict:
    return {"id": eid, "source": src, "target": tgt, "data": {"kind": "error", "mappings": {"failure": "$FULL_PAYLOAD"}}}


def _scheduler(definition: dict, registry: NodeRegistry) -> Scheduler:
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    return Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry)


def _wrap_up(record_type: str = "test.ej_ok") -> dict:
    """The run b0e3f868 shape: start → record → job → notes → done → wu_state → wu_next;
    start → wu_state; record --error--> wu_state; notes --error--> wu_state."""
    return {
        "nodes": [
            _node("start"),
            _node("record", record_type),
            _node("job"),
            _node("notes"),
            _node("done"),
            _node("wu_state"),
            _node("wu_next"),
        ],
        "edges": [
            _data("p1", "start", "record"),
            _data("p2", "record", "job"),
            _data("p3", "job", "notes"),
            _data("p4", "notes", "done"),
            _data("w15a", "done", "wu_state", "done"),
            _data("w15b", "start", "wu_state", "start"),
            _error("w15c", "record", "wu_state"),
            _error("w15d", "notes", "wu_state"),
            _data("w15e", "wu_state", "wu_next"),
        ],
    }


async def test_a_join_with_error_connections_from_upstream_steps_runs_when_they_succeed():
    ok = _Ok()
    result = await _scheduler(_wrap_up(), _registry(ok)).run(run_id="wrapup-ok")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "wu_state" in result.last_outputs, "the error gate dropped wu_state although its data arrived"
    assert "wu_next" in result.last_outputs, "wu_state's subtree never ran"
    assert ok.seen["wu_state"].get("done") == "ok"


async def test_a_join_with_error_connections_from_upstream_steps_runs_when_one_fails():
    ok = _Ok()
    result = await _scheduler(_wrap_up("test.ej_boom"), _registry(ok, _Boom())).run(run_id="wrapup-boom")
    assert "wu_state" in result.last_outputs, "the failure's error connection did not reach wu_state"
    assert "failure" in ok.seen["wu_state"], ok.seen["wu_state"]
    assert "wu_next" in result.last_outputs


async def test_a_pure_error_handler_still_runs_only_on_an_error():
    """A --error--> H, B --data--> H, and A's success path goes elsewhere: H is a handler."""
    definition = {
        "nodes": [_node("b"), _node("a"), _node("elsewhere"), _node("handler")],
        "edges": [
            _data("e1", "b", "a"),
            _data("e2", "a", "elsewhere"),
            _data("e3", "b", "handler", "ctx"),
            _error("e4", "a", "handler"),
        ],
    }
    ok = _Ok()
    result = await _scheduler(definition, _registry(ok)).run(run_id="handler-ok")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "elsewhere" in result.last_outputs
    assert "handler" not in result.last_outputs, "a pure error handler fired on success"


async def test_a_join_left_with_a_connection_that_never_resolved_raises_a_named_review_flag():
    """RUN-END INVARIANT: no-data residue (a required connection never resolved) is never a
    silent drop — it raises ``engine.join_never_resolved`` naming the step and its sources."""
    definition = {
        "nodes": [_node("left"), _node("right"), _node("join")],
        "edges": [_data("l", "left", "join", "l"), _data("r", "right", "join", "r")],
    }
    scheduler = _scheduler(definition, _registry(_Ok()))
    scheduler._pending_bindings["join"] = PendingBinding(
        firing=1, edges={"l": PendingEdgeBinding(state="pruned", source_node_id="left", source_step=1)}
    )
    raised: list[Any] = []

    async def _capture(run_id: str, flag: Any) -> bool:
        raised.append(flag)
        return True

    scheduler._review.raise_flag = _capture  # type: ignore[method-assign]
    assert scheduler._blocked_join_leftovers("residue-run") is None  # no data → not a deadlock park
    await scheduler._flag_never_resolved_joins("residue-run", 3)
    assert [f.label for f in raised] == ["engine.join_never_resolved"]
    flag = raised[0]
    assert flag.node_id == "join" and flag.severity == "error"
    assert flag.payload == {"unresolved_connections": ["r"], "waits_on": ["right"]}
    assert "'right'" in flag.message
    assert "join" not in scheduler._pending_bindings
