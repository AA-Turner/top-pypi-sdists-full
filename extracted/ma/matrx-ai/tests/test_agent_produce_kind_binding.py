"""``ai.agent.produce`` — the declaration reaches the model, or the step refuses.

Arman's ruling, 2026-08-20. Before it, an agent step returned the run ENVELOPE
with the real answer buried in ``final_text`` as a JSON string, and downstream
projection nodes rebuilt the platform kind by hand. These tests hold the four
refusals that keep the new node honest, and the one happy path that proves the
node's payload IS the kind — plus that spend still settles when the payload has
nowhere to carry a usage block.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_graph.errors import ExecutionError

from matrx_ai import mandates
from matrx_ai.agents.named import AgentRecordSource
from matrx_ai.graph_nodes.agent_produce_action import AgentProduceInput, agent_produce

_HOLDER = "11111111-2222-3333-4444-555555555555"
_KIND = "flashcard_set"
_ANSWER = {"title": "Photosynthesis", "cards": [{"front": "q", "back": "a"}]}


def _ctx(output_kind: str | None):
    """A NodeExecutionContext carrying only what this node reads."""
    from matrx_connect.context.app_context import AppContext
    from matrx_graph.types.context import ChannelView, NodeExecutionContext

    class _Emitter:
        async def send_data(self, *_a: Any, **_k: Any) -> None: ...

    return NodeExecutionContext(
        app=AppContext(
            emitter=_Emitter(),
            user_id="test-user",
            is_authenticated=True,
            conversation_id="test-conv",
            request_id="test-req",
            organization_id="test-org",
        ),
        run_id="run-produce",
        thread_id="run-produce",
        node_id="flashcards",
        step=0,
        attempt=1,
        channels=ChannelView(_values={}, _pending_writes=[]),
        checkpointer=None,
        output_kind=output_kind,
    )


@pytest.fixture
def bound_mandate(monkeypatch):
    """A mandate whose declared output kind agrees with the node's."""

    async def _resolver(mandate_key: str) -> mandates.MandateResolution:
        return mandates.MandateResolution(
            source=AgentRecordSource(agent_id=_HOLDER, is_version=False),
            output_kind=_KIND,
        )

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver)


@pytest.fixture
def agent_host(monkeypatch):
    """Stand in for the host's agent_runner + AgentStartRequest.

    Records the request so a test can assert WHAT was sent to the provider —
    the whole point of this node is the response_format it carries.
    """
    from pydantic import BaseModel, ConfigDict

    from matrx_ai import _ext
    from matrx_ai.graph_nodes import shared

    class _Request(BaseModel):
        model_config = ConfigDict(extra="allow")

        _mandate_key: str | None = None

    sent: dict[str, Any] = {}

    async def _runner(agent_id: str, request: Any, _app: Any) -> Any:
        sent["agent_id"] = agent_id
        sent["request"] = request
        return object()  # normalize_completed_result is stubbed below

    monkeypatch.setitem(_ext._registry, "agent_runner", _runner)
    monkeypatch.setitem(_ext._registry, "AgentStartRequest", _Request)
    return sent, shared


def _stub_completion(monkeypatch, *, structured_output: Any, cost_usd: float = 0.5):
    """Make normalize_completed_result answer with a fixed AiExecutionResult."""
    from matrx_graph.types.result import success

    from matrx_ai.graph_nodes import agent_produce_action, shared

    result = shared.AiExecutionResult(
        conversation_id="conv-1",
        request_id="req-1",
        iterations=1,
        final_text="ignored — the payload is the structured output",
        usage=shared.AiUsage(input_tokens=10, output_tokens=20, cost_usd=cost_usd),
        structured_output=structured_output,
    )
    monkeypatch.setattr(
        agent_produce_action, "normalize_completed_result", lambda _c: success(result)
    )
    return result


@pytest.mark.asyncio
async def test_a_step_with_NO_declared_kind_refuses_before_any_paid_call(
    bound_mandate, agent_host
):
    """This node's whole contract is 'produce X'. Not saying which X is not a step."""
    sent, _ = agent_host
    with pytest.raises(ExecutionError) as excinfo:
        await agent_produce(_ctx(None), AgentProduceInput(mandate_key="education.x"))
    assert "declares no output kind" in str(excinfo.value)
    assert not sent, "the agent must not run when the step cannot say what it produces"


@pytest.mark.asyncio
async def test_a_GENERIC_kind_refuses_because_there_is_nothing_to_bind(bound_mandate, agent_host):
    """`text` / `json` name a FORMAT. Binding to one is not enforcement."""
    sent, _ = agent_host
    with pytest.raises(ExecutionError) as excinfo:
        await agent_produce(_ctx("json"), AgentProduceInput(mandate_key="education.x"))
    assert "a FORMAT, not a structure" in str(excinfo.value)
    assert not sent


@pytest.mark.asyncio
async def test_a_graph_declaration_CONTRADICTING_the_mandate_refuses(monkeypatch, agent_host):
    """Two statements about what a paid run produces cannot both be true."""

    async def _resolver(_key: str) -> mandates.MandateResolution:
        return mandates.MandateResolution(
            source=AgentRecordSource(agent_id=_HOLDER, is_version=False),
            output_kind="quiz_set",
        )

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver)
    sent, _ = agent_host
    with pytest.raises(ExecutionError) as excinfo:
        await agent_produce(_ctx(_KIND), AgentProduceInput(mandate_key="education.x"))
    message = str(excinfo.value)
    assert _KIND in message and "quiz_set" in message
    assert not sent


@pytest.mark.asyncio
async def test_an_UNBINDABLE_kind_refuses_rather_than_degrading_to_prose(
    monkeypatch, bound_mandate, agent_host
):
    """A response_format that cannot be enforced is worse than no binding."""
    from matrx_ai.graph_nodes import agent_produce_action

    async def _no_binding(_slug: str):
        return None

    monkeypatch.setattr(agent_produce_action, "response_format_for_kind", _no_binding)
    sent, _ = agent_host
    with pytest.raises(ExecutionError) as excinfo:
        await agent_produce(_ctx(_KIND), AgentProduceInput(mandate_key="education.x"))
    assert "does not run unbound" in str(excinfo.value)
    assert not sent


@pytest.mark.asyncio
async def test_the_bound_step_sends_the_kinds_schema_and_returns_the_KIND_as_its_payload(
    monkeypatch, bound_mandate, agent_host
):
    from matrx_ai.config.response_format import (
        OutputSchemaEnvelope,
        ResponseFormatJsonSchema,
    )
    from matrx_ai.graph_nodes import agent_produce_action

    schema = {"type": "object", "properties": {"title": {"type": "string"}}}

    async def _binding(slug: str):
        assert slug == _KIND
        return ResponseFormatJsonSchema(
            type="json_schema",
            json_schema=OutputSchemaEnvelope.model_validate(
                {"name": slug, "schema": schema, "strict": True}
            ),
        )

    monkeypatch.setattr(agent_produce_action, "response_format_for_kind", _binding)
    _stub_completion(monkeypatch, structured_output=_ANSWER, cost_usd=0.5)

    sent, _ = agent_host
    ctx = _ctx(_KIND)
    outcome = await agent_produce(
        ctx,
        # An authored config_overrides must NOT be able to unbind the kind.
        AgentProduceInput(mandate_key="education.x", config_overrides={"temperature": 0.1}),
    )

    # 1. The kind's schema actually reached the provider request, and the
    #    authored override rode along beside it rather than replacing it.
    overrides = sent["request"].config_overrides
    assert overrides["temperature"] == 0.1
    assert overrides["response_format"]["json_schema"]["name"] == _KIND
    assert overrides["response_format"]["json_schema"]["schema"] == schema

    # 2. The node's payload IS the kind — not the run envelope.
    assert outcome.status == "success"
    assert outcome.result.model_dump() == _ANSWER

    # 3. Spend is declared on the engine plane, because a strict kind has
    #    nowhere to carry a usage block.
    billed = ctx.drain_billed_usage()
    assert billed["usage"]["cost_usd"] == 0.5
    assert billed["conversation_id"] == "conv-1"
    assert ctx.drain_billed_usage() is None, "draining must clear it"


@pytest.mark.asyncio
async def test_a_turn_that_produced_NO_structured_output_fails_the_node(
    monkeypatch, bound_mandate, agent_host
):
    """A kind-bound step has nothing to hand downstream without one."""
    from matrx_ai.config.response_format import (
        OutputSchemaEnvelope,
        ResponseFormatJsonSchema,
    )
    from matrx_ai.graph_nodes import agent_produce_action

    async def _binding(slug: str):
        return ResponseFormatJsonSchema(
            type="json_schema",
            json_schema=OutputSchemaEnvelope.model_validate(
                {"name": slug, "schema": {"type": "object"}, "strict": True}
            ),
        )

    monkeypatch.setattr(agent_produce_action, "response_format_for_kind", _binding)
    _stub_completion(monkeypatch, structured_output=None)

    outcome = await agent_produce(_ctx(_KIND), AgentProduceInput(mandate_key="education.x"))
    assert outcome.status == "error"
    assert outcome.error.code == "kind_output_missing"
    # The paid turn's usage still travels, so cost settlement survives failure.
    assert outcome.error.details["usage"]["cost_usd"] == 0.5
