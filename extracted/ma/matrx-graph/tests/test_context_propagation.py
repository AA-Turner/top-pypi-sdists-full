"""The per-invocation AppContext fork MUST become the ambient context.

Regression guard for the 2026-06-12 Study Pack outage: an LLM node read
``get_app_context()`` (matrx-ai does this internally) and saw the RUN-LEVEL
context — whose ``conversation_id`` was ""  — instead of the per-invocation
fork the scheduler built. Its cx_* persistence then crashed with
``invalid input syntax for type uuid: ""`` and parked the whole run.

The scheduler forks a context per invocation for isolation; this test pins
that the fork is actually INSTALLED on the ContextVar so any code the node
calls (LLM requests, tools, sub-agents) sees it.
"""

from __future__ import annotations

import uuid

from matrx_connect.context.app_context import get_app_context
from matrx_graph import Scheduler, compile_graph
from matrx_graph.actions import ActionRegistry, register_node
from matrx_graph.checkpoint import MemoryCheckpointer
from matrx_graph.executor.registry import NodeRegistry
from matrx_graph.types.definition import Definition
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel

from tests._fixtures import make_app_context


class _In(BaseModel):
    pass


class _Out(BaseModel):
    seen_conversation_id: str | None = None


async def test_node_sees_per_invocation_context_conversation_id():
    nreg = NodeRegistry()
    areg = ActionRegistry()

    @register_node(
        name="test.read_ambient_ctx",
        category=NodeCategory.DATA,
        determinism=ActionTier.NON_DETERMINISTIC,
        input_schema=_In,
        output_schema=_Out,
        node_registry=nreg,
        action_registry=areg,
    )
    async def _read(_ctx, _inputs: _In) -> NodeResult[_Out]:
        # matrx-ai's execute_ai_request reads identity off get_app_context(),
        # NOT off the ctx.app handed to the executor. This must see the fork.
        return success(_Out(seen_conversation_id=get_app_context().conversation_id))

    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "r",
                    "type": "test.read_ambient_ctx",
                    "position": {"x": 0, "y": 0},
                    "data": {},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(definition, registry=nreg)

    # Run-level context with an EMPTY conversation_id (the exact failure
    # input: the detached workflow ctx whose override was never installed).
    app_ctx = make_app_context()
    app_ctx = app_ctx.with_overrides(conversation_id="")
    run_id = str(uuid.uuid4())

    scheduler = Scheduler(graph, MemoryCheckpointer(), app_ctx, registry=nreg)
    result = await scheduler.run(run_id=run_id, inputs={}, max_steps=5)

    assert result.status.value == "completed"
    seen = (result.last_outputs.get("r") or {}).get("seen_conversation_id")
    # The invocation fork derives its own durable UUID from the full invocation
    # coordinates, and — crucially — that fork is INSTALLED so the node
    # observes it rather than the empty run-level value.
    expected = str(
        uuid.uuid5(
            uuid.NAMESPACE_URL,
            f"matrx-workflow-invocation:{run_id}:0:r:root:0:0",
        )
    )
    assert seen == expected, (
        f"node saw conversation_id={seen!r}; expected the per-invocation "
        f"fork's value (expected={expected!r}). The fork was not installed on "
        f"the ContextVar — matrx-ai would see '' and crash cx_* persistence."
    )
