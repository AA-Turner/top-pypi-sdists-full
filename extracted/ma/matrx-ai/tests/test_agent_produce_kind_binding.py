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

    async def _passthrough(supplied: dict[str, Any]) -> dict[str, Any]:
        return dict(supplied)

    async def _resolver(mandate_key: str) -> mandates.MandateResolution:
        return mandates.MandateResolution(
            source=AgentRecordSource(agent_id=_HOLDER, is_version=False),
            output_kind=_KIND,
            materialize=_passthrough,
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
        sent["app_metadata"] = dict(getattr(_app, "metadata", None) or {})
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
        agent_produce_action, "normalize_completed_result", lambda _c, **_kwargs: success(result)
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
    assert outcome.result.model_dump() == {"__kind": _KIND, **_ANSWER}

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


def _bind_kind(monkeypatch) -> None:
    from matrx_ai.config.response_format import OutputSchemaEnvelope, ResponseFormatJsonSchema
    from matrx_ai.graph_nodes import agent_produce_action

    async def _binding(slug: str):
        return ResponseFormatJsonSchema(
            type="json_schema",
            json_schema=OutputSchemaEnvelope.model_validate(
                {"name": slug, "schema": {"type": "object"}, "strict": True}
            ),
        )

    monkeypatch.setattr(agent_produce_action, "response_format_for_kind", _binding)


@pytest.mark.asyncio
async def test_a_mandate_step_runs_its_values_through_the_BINDING_and_is_RECORDED(
    monkeypatch, agent_host
):
    """Runner plan step 1 (2026-10-20): the produce step sent its variables to the
    doer BY NAME (no binding, no gate) and passed no mandate_key / run_stamp, so no
    run record was written. Now the step's variables are the offer, the binding's
    answer is what the doer gets, and the step carries the run stamp like Run
    Mandate. RED before: the doer got the raw names and no stamp reached the host."""
    seen: dict[str, Any] = {}
    stamp = {"mandate_key": "education.x", "rung": "system", "holder_type": "agent"}

    async def _binding_map(supplied: dict[str, Any]) -> dict[str, Any]:
        seen["offer"] = dict(supplied)
        return {"source_material": supplied["topic"]}

    async def _resolver(mandate_key: str) -> mandates.MandateResolution:
        return mandates.MandateResolution(
            source=AgentRecordSource(agent_id=_HOLDER, is_version=False),
            output_kind=_KIND,
            materialize=_binding_map,
            run_stamp=stamp,
        )

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver)
    _bind_kind(monkeypatch)
    _stub_completion(monkeypatch, structured_output=_ANSWER)

    sent, _ = agent_host
    outcome = await agent_produce(
        _ctx(_KIND), AgentProduceInput(mandate_key="education.x", topic="Photosynthesis")
    )

    assert outcome.status == "success"
    assert seen["offer"] == {"topic": "Photosynthesis"}
    assert sent["request"].variables == {"source_material": "Photosynthesis"}, (
        "the doer received the step's raw names instead of what the binding gave it"
    )
    assert sent["app_metadata"].get("mandate_key") == "education.x"
    assert sent["app_metadata"].get("mandate_resolution", {}).get("rung") == "system", (
        "no run stamp reached the host — the step's mandate run is never recorded"
    )


@pytest.mark.asyncio
async def test_a_mandate_step_on_a_host_with_no_pipeline_refuses(monkeypatch, agent_host):
    async def _resolver(mandate_key: str) -> mandates.MandateResolution:
        return mandates.MandateResolution(
            source=AgentRecordSource(agent_id=_HOLDER, is_version=False), output_kind=_KIND
        )

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver)
    _bind_kind(monkeypatch)
    sent, _ = agent_host
    with pytest.raises(ExecutionError, match="does not run unbound"):
        await agent_produce(_ctx(_KIND), AgentProduceInput(mandate_key="education.x", topic="t"))
    assert "request" not in sent, "a paid call ran unbound"


# ── Run Typed Agent: the step's GOAL is graded (Arman, 2026-10-27) ──────────


def _bind_any_kind(monkeypatch):
    from matrx_ai.config.response_format import OutputSchemaEnvelope, ResponseFormatJsonSchema
    from matrx_ai.graph_nodes import agent_produce_action

    async def _binding(slug: str):
        return ResponseFormatJsonSchema(
            type="json_schema",
            json_schema=OutputSchemaEnvelope.model_validate(
                {"name": slug, "schema": {"type": "object", "properties": {}}, "strict": True}
            ),
        )

    monkeypatch.setattr(agent_produce_action, "response_format_for_kind", _binding)


async def _settle() -> None:
    import asyncio

    for _ in range(20):
        await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_a_typed_step_hands_its_answer_and_GOAL_to_the_hosts_judge(monkeypatch, agent_host):
    from matrx_ai import _ext
    from matrx_ai.graph_nodes.agent_produce_action import TYPED_STEP_JUDGE_EXT, TypedAgentConfig

    _bind_any_kind(monkeypatch)
    _stub_completion(monkeypatch, structured_output=_ANSWER)
    graded: list[dict[str, Any]] = []

    async def _judge(**kw: Any) -> None:
        graded.append(kw)

    monkeypatch.setitem(_ext._registry, TYPED_STEP_JUDGE_EXT, _judge)
    ctx = _ctx(_KIND)
    outcome = await agent_produce(
        ctx,
        AgentProduceInput(agent_id=_HOLDER, source_feature="education.flashcards"),
        TypedAgentConfig(goal="Cards a student can drill from.", goal_grounding="V", required_output_keys=["title"]),
    )
    await _settle()
    assert outcome.status == "success" and outcome.result.model_dump() == {"__kind": _KIND, **_ANSWER}
    [call] = graded
    assert call["goal"] == "Cards a student can drill from." and call["goal_grounding"] == "V"
    assert call["required_output_keys"] == ["title"]
    assert call["output_kind"] == _KIND and call["artifact"] == {"__kind": _KIND, **_ANSWER}
    assert call["node_id"] == "flashcards" and call["run_id"] == "run-produce" and call["agent_id"] == _HOLDER
    # Cost attribution rides on the step's own source_feature.
    sent, _ = agent_host
    assert sent["request"].source_feature == "education.flashcards"


@pytest.mark.asyncio
async def test_the_step_never_waits_for_a_slow_judge(monkeypatch, agent_host):
    import asyncio
    import time

    from matrx_ai import _ext
    from matrx_ai.graph_nodes.agent_produce_action import TYPED_STEP_JUDGE_EXT, TypedAgentConfig

    _bind_any_kind(monkeypatch)
    _stub_completion(monkeypatch, structured_output=_ANSWER)
    finished: list[int] = []

    async def _slow(**_kw: Any) -> None:
        await asyncio.sleep(3)
        finished.append(1)

    monkeypatch.setitem(_ext._registry, TYPED_STEP_JUDGE_EXT, _slow)
    started = time.monotonic()
    outcome = await agent_produce(_ctx(_KIND), AgentProduceInput(agent_id=_HOLDER), TypedAgentConfig(goal="g"))
    assert outcome.status == "success" and time.monotonic() - started < 1.0 and finished == []


@pytest.mark.asyncio
async def test_a_goal_less_step_still_reaches_the_judge_and_a_broken_judge_never_sinks_it(monkeypatch, agent_host):
    from matrx_ai import _ext
    from matrx_ai.graph_nodes.agent_produce_action import TYPED_STEP_JUDGE_EXT, TypedAgentConfig

    _bind_any_kind(monkeypatch)
    _stub_completion(monkeypatch, structured_output=_ANSWER)
    calls: list[dict[str, Any]] = []

    async def _broken(**kw: Any) -> None:
        calls.append(kw)
        raise RuntimeError("judge down")

    monkeypatch.setitem(_ext._registry, TYPED_STEP_JUDGE_EXT, _broken)
    no_goal = await agent_produce(_ctx(_KIND), AgentProduceInput(agent_id=_HOLDER), TypedAgentConfig())
    await _settle()
    assert no_goal.status == "success" and calls[0]["goal"] == "" and calls[0]["goal_grounding"] == "A"


@pytest.mark.asyncio
async def test_a_TEXT_step_answers_in_the_text_kind(monkeypatch, agent_host):
    from matrx_ai.graph_nodes.agent_produce_action import TypedAgentConfig

    result = _stub_completion(monkeypatch, structured_output=None)
    result.final_text = "A two-host script about tides."
    sent, _ = agent_host
    outcome = await agent_produce(_ctx("text"), AgentProduceInput(agent_id=_HOLDER), TypedAgentConfig())
    assert outcome.status == "success"
    assert outcome.result.model_dump() == {"__kind": "text", "text": "A two-host script about tides."}
    assert "response_format" not in (getattr(sent["request"], "config_overrides", None) or {})


@pytest.mark.asyncio
async def test_a_step_with_no_node_kind_takes_the_kind_from_its_SETTING_and_marks_the_answer(
    monkeypatch, agent_host
):
    """A reusable workflow names the agent, the kind and the goal as run inputs: the kind arrives
    as the step setting ``output_kind`` (``{'$input': 'output_kind'}``), the model is bound to it,
    and the answer carries ``__kind`` so the scheduler validates it against that kind."""
    from matrx_ai.graph_nodes import agent_produce_action
    from matrx_ai.graph_nodes.agent_produce_action import TypedAgentConfig

    seen: list[str] = []

    async def _binding(slug: str):
        from matrx_ai.config.response_format import OutputSchemaEnvelope, ResponseFormatJsonSchema

        seen.append(slug)
        return ResponseFormatJsonSchema(
            type="json_schema",
            json_schema=OutputSchemaEnvelope.model_validate(
                {"name": slug, "schema": {"type": "object", "properties": {}}, "strict": True}
            ),
        )

    monkeypatch.setattr(agent_produce_action, "response_format_for_kind", _binding)
    _stub_completion(monkeypatch, structured_output=_ANSWER)
    sent, _ = agent_host
    outcome = await agent_produce(
        _ctx(None), AgentProduceInput(agent_id=_HOLDER), TypedAgentConfig(output_kind=_KIND)
    )
    assert seen == [_KIND]
    assert sent["request"].config_overrides["response_format"]["json_schema"]["name"] == _KIND
    assert outcome.status == "success"
    assert outcome.result.model_dump() == {"__kind": _KIND, **_ANSWER}


@pytest.mark.asyncio
async def test_a_step_with_neither_a_node_kind_nor_a_kind_setting_still_refuses(agent_host):
    from matrx_ai.graph_nodes.agent_produce_action import TypedAgentConfig

    with pytest.raises(ExecutionError, match="declares no output"):
        await agent_produce(_ctx(None), AgentProduceInput(agent_id=_HOLDER), TypedAgentConfig(output_kind=""))
