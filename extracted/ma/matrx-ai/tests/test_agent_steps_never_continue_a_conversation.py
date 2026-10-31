"""A step that STARTS an agent never continues a conversation; Continue Conversation covers it.

The ruling (workflow node-library cleanup, 2026-10-29): Agent = start a run of a saved agent;
Chat = act on an existing conversation. Run Agent, Run Mandate, Run Typed Agent and Run Agent in
Batches lost ``conversation_id`` / ``is_new``; ``ai.conversation.continue`` is the one way to add a
turn, and it carries every knob a continuing turn had on Run Agent.

Each test fails on the old shape: the fields were declared (so offered in Studio's form and accepted
silently), and Continue Conversation had no per-run config layer, no money guards, and shared the
workflow root's request id.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, get_app_context
from matrx_graph.types.identity_inputs import identity_input_fields
from pydantic import BaseModel, ConfigDict, ValidationError

from matrx_ai import _ext
from matrx_ai.graph_nodes import conversation_action
from matrx_ai.graph_nodes.agent_action import AgentStartInput
from matrx_ai.graph_nodes.agent_assignment_action import AgentAssignmentBatchInput
from matrx_ai.graph_nodes.agent_produce_action import AgentProduceInput
from matrx_ai.graph_nodes.conversation_action import (
    ConversationContinueInput,
    ConversationForkAndRunInput,
    build_continue_request,
    build_fork_request,
    run_step_conversation_continue,
)
from matrx_ai.graph_nodes.mandate_action import MandateStartInput
from matrx_ai.providers.guardrail_gate import current_call_spend_cap

AGENT_ID = "6f1c2b7e-4a0d-4d7e-9a51-0c2f3e8b9a10"
UPSTREAM_CONVERSATION = "2b8f6c1d-93a4-4f0e-8e57-5d1a7c9e0b42"

STARTING_STEPS: dict[str, tuple[type[BaseModel], dict[str, Any]]] = {
    "ai.agent.start": (AgentStartInput, {"agent_id": AGENT_ID}),
    "ai.mandate.start": (MandateStartInput, {"mandate_key": "support.triage"}),
    "ai.agent.produce": (AgentProduceInput, {"agent_id": AGENT_ID}),
}


@pytest.mark.parametrize("node_type", sorted(STARTING_STEPS))
def test_a_starting_step_does_not_offer_continuation(node_type: str) -> None:
    model, _ = STARTING_STEPS[node_type]
    offered = set(model.model_json_schema().get("properties", {}))
    assert not {"conversation_id", "is_new"} & offered, f"{node_type} still offers {offered & {'conversation_id', 'is_new'}}"


def test_the_batch_template_does_not_offer_continuation() -> None:
    template = AgentAssignmentBatchInput.model_json_schema()["$defs"]["AssignmentAgentInput"]
    assert not {"conversation_id", "is_new"} & set(template["properties"])


@pytest.mark.parametrize("node_type", sorted(STARTING_STEPS))
def test_a_starting_step_refuses_a_conversation_to_continue_by_name(node_type: str) -> None:
    model, base = STARTING_STEPS[node_type]
    with pytest.raises(ValidationError) as caught:
        model.model_validate({**base, "conversation_id": UPSTREAM_CONVERSATION, "is_new": False})
    message = str(caught.value)
    assert "ai.conversation.continue" in message
    assert UPSTREAM_CONVERSATION in message


def test_the_batch_template_refuses_a_conversation_to_continue() -> None:
    with pytest.raises(ValidationError, match="ai.conversation.continue"):
        AgentAssignmentBatchInput.model_validate(
            {
                "agent": {"agent_id": AGENT_ID, "conversation_id": UPSTREAM_CONVERSATION},
                "plan": {"strategy": "coordinated_rows", "rows": [{"key": "a", "values": {"topic": "A"}}]},
            }
        )


@pytest.mark.parametrize("node_type", sorted(STARTING_STEPS))
def test_empty_old_form_keys_are_dropped_never_bound_as_variables(node_type: str) -> None:
    model, base = STARTING_STEPS[node_type]
    parsed = model.model_validate({**base, "conversation_id": None, "is_new": True})
    assert not {"conversation_id", "is_new"} & set(parsed.model_extra or {})


@pytest.mark.parametrize(
    "model", [AgentStartInput, MandateStartInput, AgentProduceInput], ids=lambda m: m.__name__
)
def test_the_engine_still_withholds_a_broadcast_conversation_id(model: type[BaseModel]) -> None:
    """Without the identity declaration an upstream agent_result's conversation_id would reach the
    step on an unmapped edge — and now be REFUSED, killing every agent→agent chain."""
    assert {"conversation_id", "is_new"} <= identity_input_fields(model)


# ── Continue Conversation carries what a continuing Run Agent turn had ────────────────


class _HostBody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    user_input: str | None = None
    config_overrides: dict[str, Any] = {}
    model_this_turn_only: bool = False
    tools: list[dict[str, Any]] = []
    retry: bool = False
    store: bool = True
    debug: bool = False
    block_mode: bool = False
    allow_context_create: bool = False
    context: dict[str, Any] = {}
    writable_variables: list[str] = []
    memory_scope: str = "thread"
    max_retries_per_iteration: int = 2
    max_iterations: int | None = None
    # fork-only
    exclusive: bool = False
    keep_whole: bool = True
    host_turn: dict[str, Any] | None = None


@pytest.fixture
def host_body(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(_ext._registry, "ConversationContinueRequest", _HostBody)
    monkeypatch.setitem(_ext._registry, "ForkAndRunRequest", _HostBody)


def _continue_inputs(**extra: Any) -> ConversationContinueInput:
    return ConversationContinueInput(
        conversation_id=UPSTREAM_CONVERSATION,
        user_input="And the second chapter?",
        config_overrides={"temperature": 0.2, "max_output_tokens": 9000},
        runtime_config_overrides={"temperature": 0.7},
        max_output_tokens=1200,
        model_this_turn_only=True,
        max_call_cost_usd=0.5,
        **extra,
    )


def test_continue_layers_the_run_config_and_the_answer_ceiling(host_body: None) -> None:
    request = build_continue_request(_continue_inputs())
    # Authored temperature lost to the edge-fed per-run layer; the step's ceiling sits on top.
    assert request.config_overrides["temperature"] == 0.7
    assert request.config_overrides["max_output_tokens"] == 1200
    assert request.model_this_turn_only is True


def test_fork_and_ask_shares_the_same_layering(host_body: None) -> None:
    request = build_fork_request(
        ConversationForkAndRunInput(
            conversation_id=UPSTREAM_CONVERSATION,
            question="What went wrong?",
            runtime_config_overrides={"temperature": 0.9},
            max_output_tokens=800,
        )
    )
    assert request.config_overrides == {"temperature": 0.9, "max_output_tokens": 800}


@pytest.mark.asyncio
async def test_continue_runs_as_its_own_request_under_the_spend_cap(
    host_body: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    seen: dict[str, Any] = {}

    async def fake_continuer(conversation_id: str, request: Any, app: Any) -> str:
        seen["conversation_id"] = conversation_id
        seen["request_id"] = get_app_context().request_id
        seen["cap"] = current_call_spend_cap()
        return "completed"

    async def no_pricing() -> None:
        return None

    monkeypatch.setitem(_ext._registry, "conversation_continuer", fake_continuer)
    monkeypatch.setattr("matrx_ai.config.usage_config.ensure_pricing_lookup", no_pricing)
    root = AppContext(emitter=None, user_id="u-1", conversation_id="root-conv", request_id="root-request", organization_id="org-1")

    class _Ctx:
        app = root
        node_id = "continue-1"

    inputs = _continue_inputs()
    await run_step_conversation_continue(_Ctx(), inputs.conversation_id, build_continue_request(inputs), inputs)

    assert seen["conversation_id"] == UPSTREAM_CONVERSATION
    assert seen["request_id"] and seen["request_id"] != "root-request"
    assert seen["cap"] is not None and seen["cap"].max_usd == 0.5
    assert current_call_spend_cap() is None
    assert conversation_action.STEP_ONLY_INPUTS >= {"runtime_config_overrides", "max_output_tokens", "max_call_cost_usd"}
