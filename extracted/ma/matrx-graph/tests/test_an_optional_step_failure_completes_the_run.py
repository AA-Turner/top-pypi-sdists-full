"""Guard (2026-10-14): a fail-soft side step (``data.optional: true``) that fails is recorded
FAILED with its reason and the run COMPLETES; a required step that fails still parks the run
ERRORED. Before this, one off-critical-path leaf (Smart Add's key_people refusing a binding the
live server did not offer yet) errored every round between ~22:00 and 23:19 UTC.
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
        description="optional-step test node",
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
    spec: ClassVar[NodeSpec] = _spec("test.opt_ok")

    def __init__(self) -> None:
        self.calls = 0

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Out]:
        self.calls += 1
        return success(_Out(text="ok"))


class _Boom:
    spec: ClassVar[NodeSpec] = _spec("test.opt_boom")

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: _Cfg) -> NodeResult[_Out]:
        raise RuntimeError("MandateResolutionError: binding names a value the server does not offer")


def _registry(*executors: Any) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    for ex in executors:
        reg.register(ex, overwrite=True)
    return reg


def _node(node_id: str, node_type: str, **data: Any) -> dict:
    return {"id": node_id, "type": node_type, "position": {"x": 0, "y": 0}, "data": {"config": {}, **data}}


def _definition(*, optional: bool, with_dependent: bool = False) -> dict:
    side = {"optional": True} if optional else {}
    nodes = [_node("start", "test.opt_ok"), _node("main", "test.opt_ok"), _node("side", "test.opt_boom", **side)]
    edges = [
        {"id": "e1", "source": "start", "target": "main", "data": {"kind": "data", "mappings": {"a": "text"}}},
        {"id": "e2", "source": "start", "target": "side", "data": {"kind": "data", "mappings": {"a": "text"}}},
    ]
    if with_dependent:
        nodes.append(_node("after_side", "test.opt_ok"))
        edges.append(
            {"id": "e3", "source": "side", "target": "after_side", "data": {"kind": "data", "mappings": {"a": "text"}}}
        )
    return {"nodes": nodes, "edges": edges}


async def _run(definition: dict, registry: NodeRegistry, run_id: str):
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    return await scheduler.run(run_id=run_id), emitter


def _events(emitter: FakeEmitter, name: str) -> list[dict]:
    return [e for k, e in emitter.events if k == "data" and isinstance(e, dict) and e.get("event") == name]


async def test_an_optional_leaf_failure_completes_the_run_and_records_the_step_failed():
    ok = _Ok()
    result, emitter = await _run(_definition(optional=True), _registry(ok, _Boom()), "opt-leaf")
    assert result.status is RunStatus.COMPLETED, result.error
    failed = _events(emitter, "node_failed")
    assert [f["node_id"] for f in failed] == ["side"], failed
    assert "does not offer" in failed[0]["error_message"]
    assert ok.calls == 2, "start and main both ran"


async def test_an_optional_step_failure_prunes_its_dependents_like_a_branch_not_taken():
    ok = _Ok()
    result, _ = await _run(
        _definition(optional=True, with_dependent=True), _registry(ok, _Boom()), "opt-branch"
    )
    assert result.status is RunStatus.COMPLETED, result.error
    assert ok.calls == 2, "after_side never ran: its only input was pruned"


async def test_a_required_step_failure_still_errors_the_run():
    result, _ = await _run(_definition(optional=False), _registry(_Ok(), _Boom()), "req-leaf")
    assert result.status is RunStatus.ERRORED


def test_optional_must_be_a_boolean():
    from matrx_graph.validation import validate_definition

    bad = _definition(optional=False)
    bad["nodes"][2]["data"]["optional"] = "yes"
    report = validate_definition(Definition.model_validate(bad), registry=_registry(_Ok(), _Boom()))
    assert not report.valid
    assert any(i.path.endswith(".data.optional") for i in report.issues), report.issues
