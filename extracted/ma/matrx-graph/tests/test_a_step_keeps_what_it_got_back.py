"""Watch AI RAW tier, engine side: every node invocation runs inside its own
``matrx_utils.raw_capture`` scope, and what the step's outside calls returned is
delivered to the host's sink with the step's identity (run, step, node, attempt).

The node here does what Smart Add's ``socials`` step does through matrx-social's
response observer: it records one vendor answer (a recorded ScrapeCreators body)
while it runs. A step that records nothing delivers nothing (no row write).
"""

from __future__ import annotations

from typing import ClassVar

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
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_utils import raw_capture
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context

VENDOR_BODY = (
    b'{"success": true, "credits_remaining": 24898, "credits_charged": 1, "handle": "shredit", '
    b'"userId": null, "error": "not_found", "errorStatus": 404, "message": "Profile is private"}'
)


class _Any(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


def _spec(node_type: str) -> NodeSpec:
    return NodeSpec(
        type=node_type,
        category=NodeCategory.DATA,
        display_name=node_type,
        description="test step",
        input_schema=_Any,
        output_schema=_Any,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.IDEMPOTENT,
    )


class LookupExecutor:
    spec: ClassVar[NodeSpec] = _spec("test.social_lookup")

    async def execute(self, ctx: NodeExecutionContext, inputs: _Any, config: _Cfg) -> NodeResult[_Any]:
        raw_capture.record_raw(label="GET /v1/instagram/profile", data=VENDOR_BODY, source="scrapecreators",
                               status_code=404, content_type="application/json")
        return success(_Any(found=False))


class QuietExecutor:
    spec: ClassVar[NodeSpec] = _spec("test.quiet")

    async def execute(self, ctx: NodeExecutionContext, inputs: _Any, config: _Cfg) -> NodeResult[_Any]:
        return success(_Any(ok=True))


@pytest.fixture
def delivered():
    got: list[raw_capture.CaptureScope] = []
    raw_capture.register_raw_capture_sink(got.append)
    yield got
    raw_capture.clear_raw_capture_sink()


async def _run(executor: object, node_type: str, run_id: str):
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(executor, overwrite=True)
    definition = Definition.model_validate(
        {"nodes": [{"id": "socials", "type": node_type, "position": {"x": 0, "y": 0}, "data": {"config": {}}}],
         "edges": []}
    )
    graph = compile_graph(definition, registry=reg)
    return await Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=reg).run(
        run_id=run_id
    )


async def test_a_steps_vendor_answer_reaches_the_sink_with_the_steps_identity(delivered) -> None:
    result = await _run(LookupExecutor(), "test.social_lookup", "raw-capture-run")
    assert result.status is RunStatus.COMPLETED
    (scope,) = delivered
    assert scope.target["target"] == "node_outcome"
    assert scope.target["run_id"] == "raw-capture-run" and scope.target["node_id"] == "socials"
    assert scope.target["attempt"] >= 1 and isinstance(scope.target["step"], int)
    (item,) = scope.items
    assert item.data == VENDOR_BODY and item.status_code == 404


async def test_a_step_that_got_nothing_back_delivers_nothing(delivered) -> None:
    result = await _run(QuietExecutor(), "test.quiet", "raw-capture-quiet")
    assert result.status is RunStatus.COMPLETED
    assert delivered == []
    assert raw_capture.current_scope() is None
