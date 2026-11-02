"""An identity input never binds from an edge BROADCAST (2026-09-12 defect).

THE LIVE FAILURE this guards. Workflow run 51524ca9 of "Watson Parenting
Adviser": step 1 (``ai.agent.start``, "Watson Case Reader") succeeded, its
``agent_result`` — which carries ``conversation_id`` — flowed down three
plain pass-through edges with NO field mappings and landed whole on step 5,
another ``ai.agent.start``. That step therefore ran with the FIRST agent's
``conversation_id``, tried to CONTINUE that conversation with its own
variables, and the conversation binding guard refused it (HTTP 409
``conversation_binding_mismatch``). The run died; the parent got nothing.

The class: a field naming a durable resource somebody else owns binds only
from something the AUTHOR declared for that step — never because an upstream
payload happened to carry a key with that name.

Both directions are pinned:
  * broadcast (no mappings) → the identity field is WITHHELD;
  * explicit mapping → it still arrives (the author asked for it by name).
"""

from __future__ import annotations

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
from matrx_graph.types.identity_inputs import identity_input, identity_input_fields
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from tests._fixtures import FakeEmitter, make_app_context

#: The live id: the CASE READER's conversation, which the Prescriber inherited.
UPSTREAM_CONVERSATION_ID = "95cce75d-e755-4a2e-a27a-ab806730f3d4"


class _EmptyConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _PassthroughInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _AgentResultLike(BaseModel):
    """The live ``agent_result`` shape, trimmed to what matters here."""

    model_config = ConfigDict(extra="allow")

    conversation_id: str = ""
    final_text: str = ""
    structured_output: dict[str, JsonValue] = Field(default_factory=dict)


class _UpstreamAgent:
    """Stands in for ``ai.agent.start`` step 1 — emits an agent_result."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.identity_source",
        category=NodeCategory.DATA,
        display_name="Upstream agent",
        description="Emits an agent-result-shaped payload.",
        input_schema=_PassthroughInput,
        output_schema=_AgentResultLike,
        config_schema=_EmptyConfig,
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
        determinism=ActionTier.PURE,
    )

    async def execute(
        self, _ctx: NodeExecutionContext, _inputs: _PassthroughInput, _config: _EmptyConfig
    ) -> NodeResult[_AgentResultLike]:
        return success(
            _AgentResultLike(
                conversation_id=UPSTREAM_CONVERSATION_ID,
                final_text="the case, read",
                structured_output={"age_band": "toddler"},
            )
        )


class _DownstreamAgentInput(BaseModel):
    """Stands in for a second agent step: a conversation identity + variables."""

    model_config = ConfigDict(extra="allow")

    conversation_id: str | None = Field(default=None, json_schema_extra=identity_input())
    final_text: str = ""


class _DownstreamOutput(BaseModel):
    model_config = ConfigDict(extra="allow")

    ran_in: str | None = None


class _DownstreamAgent:
    """Records exactly what conversation identity it was handed."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.identity_target",
        category=NodeCategory.DATA,
        display_name="Downstream agent",
        description="Records the conversation identity it received.",
        input_schema=_DownstreamAgentInput,
        output_schema=_DownstreamOutput,
        config_schema=_EmptyConfig,
        handles=(HandleSpec(id="in", direction=HandleDirection.INPUT),),
        determinism=ActionTier.PURE,
    )

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def execute(
        self, _ctx: NodeExecutionContext, inputs: _DownstreamAgentInput, _config: _EmptyConfig
    ) -> NodeResult[_DownstreamOutput]:
        self.calls.append(inputs.model_dump())
        return success(_DownstreamOutput(ran_in=inputs.conversation_id))


def _registry() -> tuple[NodeRegistry, _DownstreamAgent]:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    target = _DownstreamAgent()
    reg.register(_UpstreamAgent(), overwrite=True)
    reg.register(target, overwrite=True)
    return reg, target


def _definition(edge_data: dict[str, Any], *, target_inputs: dict[str, Any] | None = None):
    """source → passthrough (data.transform) → target, exactly like the live graph."""
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "source",
                    "type": "test.identity_source",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                },
                {
                    "id": "target",
                    "type": "test.identity_target",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {}, "inputs": target_inputs or {}},
                },
            ],
            "edges": [
                {"id": "e1", "source": "source", "target": "target", "data": edge_data}
            ],
        }
    )


async def _run(definition, registry: NodeRegistry, run_id: str):
    graph = compile_graph(definition, registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    return await scheduler.run(run_id=run_id)


def test_the_mark_is_readable_from_the_schema() -> None:
    assert identity_input_fields(_DownstreamAgentInput) == frozenset({"conversation_id"})
    assert identity_input_fields(_AgentResultLike) == frozenset()


async def test_a_broadcast_edge_does_not_hand_over_the_conversation_identity() -> None:
    """THE GUARD. Without the fix the target runs in 95cce75d… — the 409."""
    registry, target = _registry()
    result = await _run(_definition({"kind": "data"}), registry, "identity-broadcast")

    assert result.status is RunStatus.COMPLETED
    assert len(target.calls) == 1
    call = target.calls[0]
    # The identity was withheld: this step starts its OWN conversation.
    assert call["conversation_id"] is None
    # Ordinary data still rides the broadcast — only identity is special.
    assert call["final_text"] == "the case, read"
    assert call["structured_output"] == {"age_band": "toddler"}


async def test_an_explicit_mapping_still_continues_the_named_conversation() -> None:
    """The author asking for it BY NAME is the one lawful way in."""
    registry, target = _registry()
    result = await _run(
        _definition({"kind": "data", "mappings": {"conversation_id": "conversation_id"}}),
        registry,
        "identity-mapped",
    )

    assert result.status is RunStatus.COMPLETED
    assert target.calls[0]["conversation_id"] == UPSTREAM_CONVERSATION_ID


async def test_an_authored_static_input_survives_a_broadcast() -> None:
    """A step the author pinned to a conversation keeps it, broadcast or not."""
    authored = "11111111-2222-3333-4444-555555555555"
    registry, target = _registry()
    result = await _run(
        _definition({"kind": "data"}, target_inputs={"conversation_id": authored}),
        registry,
        "identity-authored",
    )

    assert result.status is RunStatus.COMPLETED
    assert target.calls[0]["conversation_id"] == authored
