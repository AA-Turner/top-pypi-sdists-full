"""Tests for the matrx-ai graph node pack.

Focus: pure Pydantic I/O contract + output-normalization.

Actual action call-paths import ``matrx_ai.orchestrator.executor`` which
transitively triggers matrx-ai's DB DI registry. Exercising that here would
require re-producing aidream's ``configure_db()`` wiring in the test scope —
a brittle moving target. Instead, the E2E run against the real stack in
aidream's Phase 4 validation workflow covers the call path.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest
from pydantic import ValidationError

from matrx_ai.graph_nodes.shared import (
    AiExecutionResult,
    AiMessage,
    AiUsage,
    normalize_completed,
)

# ---------------------------------------------------------------------------
# Fakes for CompletedRequest — matrx-ai ships dataclasses we can stub minimally
# ---------------------------------------------------------------------------


@dataclass
class _FakeUnifiedResponse:
    text: str = ""
    finish_reason: str | None = "stop"


@dataclass
class _FakeConfig:
    messages: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _FakeRequest:
    conversation_id: str = "conv-1"
    request_id: str = "req-1"
    config: _FakeConfig = field(default_factory=_FakeConfig)


@dataclass
class _FakeTotals:
    input_tokens: int = 10
    output_tokens: int = 20
    total_tokens: int = 30
    cost_usd: float = 0.01


@dataclass
class _FakeUsage:
    totals: _FakeTotals = field(default_factory=_FakeTotals)


@dataclass
class _FakeCompleted:
    request: _FakeRequest
    iterations: int
    final_response: _FakeUnifiedResponse
    total_usage: _FakeUsage
    timing_stats: dict[str, Any] = field(default_factory=dict)
    tool_call_stats: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


def _make_completed(
    text: str = "hello world",
    iterations: int = 1,
    conversation_id: str = "conv-1",
    messages: list[dict[str, Any]] | None = None,
) -> _FakeCompleted:
    return _FakeCompleted(
        request=_FakeRequest(
            conversation_id=conversation_id,
            config=_FakeConfig(messages=messages or [{"role": "user", "content": "hi"}]),
        ),
        iterations=iterations,
        final_response=_FakeUnifiedResponse(text=text),
        total_usage=_FakeUsage(),
        timing_stats={"total_duration_ms": 123},
        tool_call_stats={"total_calls": 0},
        metadata={},
    )


# ---------------------------------------------------------------------------
# normalize_completed
# ---------------------------------------------------------------------------


def test_normalize_completed_reads_the_orchestrator_s_seconds_timing():
    """The orchestrator reports SECONDS under ``total_duration``.

    ``TimingUsage.aggregate`` has never emitted a ``total_duration_ms`` key,
    so reading only that name silently reported ``duration_ms: 0`` on every
    real run of every matrx-ai graph node (found 2026-08-20 distilling
    ``agent_react_result``; a live 7-second agent turn reported 0). The replay
    harness DOES emit milliseconds directly, so both names must work.
    """
    completed = _make_completed()
    completed.timing_stats = {"total_duration": 6.9741, "api_duration": 6.5}
    assert normalize_completed(completed).duration_ms == 6974

    completed.timing_stats = {}
    assert normalize_completed(completed).duration_ms == 0


def test_normalize_completed_extracts_core_fields():
    completed = _make_completed(text="final answer", iterations=3)
    result = normalize_completed(completed)

    assert isinstance(result, AiExecutionResult)
    assert result.conversation_id == "conv-1"
    assert result.request_id == "req-1"
    assert result.iterations == 3
    assert result.final_text == "final answer"
    assert result.finish_reason == "stop"
    assert result.duration_ms == 123
    assert result.tool_calls_made == 0

    assert result.usage.input_tokens == 10
    assert result.usage.output_tokens == 20
    assert result.usage.total_tokens == 30


def test_normalize_completed_with_missing_fields_returns_defaults():
    @dataclass
    class _Minimal:
        request: None = None
        iterations: int = 0
        final_response: None = None

    result = normalize_completed(_Minimal())  # type: ignore[arg-type]
    assert result.conversation_id == ""
    assert result.final_text == ""
    assert result.iterations == 0
    assert result.usage.total_tokens == 0


def test_normalize_completed_wraps_final_message():
    completed = _make_completed(text="reply")
    result = normalize_completed(completed)
    assert result.final_message is not None
    assert result.final_message.role == "assistant"
    assert result.final_message.content == "reply"


def test_normalize_completed_round_trips_messages():
    msgs = [
        {"role": "system", "content": "you are helpful"},
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi!"},
    ]
    completed = _make_completed(messages=msgs)
    result = normalize_completed(completed)
    assert [m.role for m in result.messages] == ["system", "user", "assistant"]


# ---------------------------------------------------------------------------
# Pydantic input validation
# ---------------------------------------------------------------------------


def test_chat_manual_input_requires_model():
    from matrx_ai.graph_nodes.chat_action import ChatManualInput

    with pytest.raises(ValidationError):
        ChatManualInput(model="")  # min_length=1


def test_chat_manual_input_accepts_minimal_payload():
    from matrx_ai.graph_nodes.chat_action import ChatManualInput

    inputs = ChatManualInput(model="claude-opus-4-7")
    assert inputs.max_iterations == 100
    assert inputs.messages == []


def test_llm_chat_input_requires_prompt_and_model():
    from matrx_ai.graph_nodes.llm_action import LlmChatInput

    with pytest.raises(ValidationError):
        LlmChatInput(model="gpt-5", prompt="")

    inputs = LlmChatInput(model="gpt-5", prompt="hi there")
    assert inputs.max_tokens is None


@pytest.mark.asyncio
async def test_agent_start_step_must_name_an_agent_or_a_mandate():
    """A step names the JOB (mandate_key) or an agent id — naming neither is
    refused. The check moved OFF the Pydantic layer when `agent_id` became
    optional for the mandate migration: `AgentStartInput(agent_id="")` stopped
    raising, and this test asserted the old layer rather than the contract.
    `resolve_step_agent` is where the refusal actually lives."""
    from matrx_ai.graph_nodes.agent_action import AgentStartInput, resolve_step_agent

    with pytest.raises(ValueError, match="names no agent"):
        await resolve_step_agent(AgentStartInput(), consumer="ai.agent.start:test")

    # A pinned id alone still resolves — mandate_key is preferred, not required.
    agent_id, is_version, overrides = await resolve_step_agent(
        AgentStartInput(agent_id="agent-1"), consumer="ai.agent.start:test"
    )
    assert (agent_id, is_version, overrides) == ("agent-1", False, None)


def test_agent_assignment_input_is_strict_and_coordinates_rows():
    from matrx_ai.graph_nodes.agent_assignment_action import AgentAssignmentBatchInput

    payload = {
        "agent": {"agent_id": "agent-1", "variables": {"tone": "formal"}},
        "plan": {
            "strategy": "coordinated_rows",
            "rows": [
                {
                    "key": "topic-one",
                    "values": {"topic": "One", "research": "Source one"},
                }
            ],
        },
    }
    parsed = AgentAssignmentBatchInput.model_validate(payload)
    assert parsed.plan.strategy == "coordinated_rows"

    with pytest.raises(ValidationError):
        AgentAssignmentBatchInput.model_validate({**payload, "unknown": True})

    with pytest.raises(ValidationError):
        AgentAssignmentBatchInput.model_validate(
            {**payload, "agent": {"agent_id": "agent-1", "conversation_id": "existing"}}
        )


def test_conversation_continue_input_requires_conversation_id_but_not_user_input():
    """``user_input`` is OPTIONAL — ``retry=true`` expresses "re-run the last
    turn" by omitting it (mirrors ``ConversationContinueRequest.user_input``
    on the host, aidream/services/conversation_context/continue_conversation.py).
    ``conversation_id`` is still mandatory and non-empty."""
    from matrx_ai.graph_nodes.conversation_action import ConversationContinueInput

    with pytest.raises(ValidationError):
        ConversationContinueInput(conversation_id="", user_input="hi")  # empty id

    # No user_input, retry unset — valid at the INPUT layer (the host request
    # validates the retry-or-input contract; the node input just mirrors the
    # host's optionality).
    parsed = ConversationContinueInput.model_validate({"conversation_id": "c1"})
    assert parsed.user_input is None
    assert parsed.retry is False

    retry_parsed = ConversationContinueInput.model_validate(
        {"conversation_id": "c1", "retry": True}
    )
    assert retry_parsed.retry is True
    assert retry_parsed.user_input is None


class _FakeContinueRequest:
    """Stands in for the host's ``ConversationContinueRequest`` — records
    exactly what payload the node built, the same way a real pydantic model
    would validate it, without needing aidream's DB-backed model."""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    @classmethod
    def model_validate(cls, payload: dict[str, Any]) -> "_FakeContinueRequest":
        return cls(**payload)


@pytest.mark.asyncio
async def test_conversation_continue_executes_through_the_host_seam():
    """Finding Zero, closed: the node must EXECUTE the handler, not merely
    register it. ``conversation_action.py:80`` used to do
    ``config = resolution.config`` on a ``UnifiedConfig`` (no such attribute)
    — every call raised ``AttributeError``, and the only test in this suite
    asserted registration. This test calls the REGISTERED node function and
    asserts on what it actually did: it built a real host request (not a
    hand-rolled resolver call), ran it through the injected
    ``conversation_continuer`` seam (mirroring ``ai.agent.start``'s
    ``agent_runner``), and normalized the result.
    """
    import matrx_ai
    from matrx_ai._ext import _registry
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
    from matrx_ai.graph_nodes.conversation_action import (
        ConversationContinueInput,
        conversation_continue,
    )

    calls: dict[str, Any] = {}

    async def _fake_continuer(conversation_id, request, ctx):
        calls["conversation_id"] = conversation_id
        calls["request"] = request
        calls["ctx"] = ctx
        return _make_completed(text="hello from continue", conversation_id=conversation_id)

    matrx_ai.configure(
        conversation_continuer=_fake_continuer,
        ConversationContinueRequest=_FakeContinueRequest,
    )
    try:
        inputs = ConversationContinueInput(
            conversation_id="conv-1",
            user_input="hi again",
            context={"topic": "widgets"},
            tools=[{"kind": "registered", "name": "web_search"}],
            retry=False,
        )

        class _StepContext:
            def __init__(self) -> None:
                self.app = AppContext(user_id="u1", request_id="r1", emitter=None)
                self.node_id = "node-1"

        step_ctx = _StepContext()
        token = set_app_context(step_ctx.app)
        try:
            result = await conversation_continue(step_ctx, inputs)
        finally:
            clear_app_context(token)
    finally:
        # Leave no residue for other tests in this module.
        _registry.pop("conversation_continuer", None)
        _registry.pop("ConversationContinueRequest", None)

    # The seam was actually called — not skipped, not raised past.
    assert calls["conversation_id"] == "conv-1"
    # A real host request was built (conversation_id excluded — it's a
    # separate positional argument, never a body field).
    assert "conversation_id" not in calls["request"].kwargs
    assert calls["request"].kwargs["user_input"] == "hi again"
    assert calls["request"].kwargs["context"] == {"topic": "widgets"}
    assert calls["request"].kwargs["tools"] == [{"kind": "registered", "name": "web_search"}]

    assert result.status == "success"
    assert result.result.final_text == "hello from continue"


@pytest.mark.asyncio
async def test_conversation_continue_requires_the_host_seam():
    """Without the host wiring, the node fails LOUDLY (RuntimeError naming the
    missing extensions) instead of the old silent AttributeError deep inside
    a package."""
    from matrx_ai._ext import _registry
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
    from matrx_ai.graph_nodes.conversation_action import (
        ConversationContinueInput,
        conversation_continue,
    )

    _registry.pop("conversation_continuer", None)
    _registry.pop("ConversationContinueRequest", None)

    class _StepContext:
        def __init__(self) -> None:
            self.app = AppContext(user_id="u1", request_id="r1", emitter=None)
            self.node_id = "node-1"

    step_ctx = _StepContext()
    token = set_app_context(step_ctx.app)
    try:
        with pytest.raises(RuntimeError, match="conversation_continuer"):
            await conversation_continue(
                step_ctx, ConversationContinueInput(conversation_id="conv-1", retry=True)
            )
    finally:
        clear_app_context(token)


# ---------------------------------------------------------------------------
# Registration smoke test
# ---------------------------------------------------------------------------


def test_register_with_graph_populates_default_registry():
    from matrx_graph.actions import default_action_registry
    from matrx_graph.executor.registry import default_registry

    from matrx_ai.graph_nodes import register_with_graph

    register_with_graph()  # idempotent

    action_names = {a.name for a in default_action_registry().all()}
    for expected in (
        "ai.llm.chat",
        "ai.chat.manual",
        "ai.agent.start",
        "ai.agent.assignment_batch",
        "ai.conversation.continue",
    ):
        assert expected in action_names, f"Missing action: {expected}"

    # Each is also registered as a node type
    for expected in (
        "ai.llm.chat",
        "ai.chat.manual",
        "ai.agent.start",
        "ai.agent.assignment_batch",
        "ai.conversation.continue",
    ):
        assert default_registry().has(expected), f"Missing node type: {expected}"


def test_shared_models_are_frozen_json():
    """AiExecutionResult must round-trip through JSON so checkpoints work."""
    msg = AiMessage(role="user", content="hi")
    result = AiExecutionResult(
        conversation_id="c1",
        request_id="r1",
        iterations=1,
        final_text="ok",
        final_message=msg,
        messages=[msg],
        usage=AiUsage(total_tokens=15),
    )
    dumped = result.model_dump(mode="json")
    re_parsed = AiExecutionResult.model_validate(dumped)
    assert re_parsed.conversation_id == "c1"
    assert re_parsed.messages[0].content == "hi"


def test_ai_execution_result_json_dumps_google_thinking_signature_bytes():
    """Google thought_signature is binary; workflow checkpoints must base64 it."""
    from matrx_ai.config import ThinkingContent, UnifiedMessage
    from matrx_ai.graph_nodes.shared import _message_to_model

    invalid_utf8_sig = b"\x00\xe3\x81\xff\xfe"
    unified = UnifiedMessage(
        role="assistant",
        content=[
            ThinkingContent(
                text="plan the flashcards",
                provider="google",
                signature=invalid_utf8_sig,
            )
        ],
    )
    msg = _message_to_model(unified)
    result = AiExecutionResult(
        conversation_id="c1",
        request_id="r1",
        iterations=1,
        messages=[msg],
    )
    dumped = result.model_dump(mode="json")
    thinking = dumped["messages"][0]["content"][0]
    assert thinking["signature_encoding"] == "base64"
    assert isinstance(thinking["signature"], str)
    assert thinking["type"] == "thinking"
