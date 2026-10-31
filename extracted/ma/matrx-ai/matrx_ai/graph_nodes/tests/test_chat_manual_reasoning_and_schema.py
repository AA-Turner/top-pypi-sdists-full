"""Custom AI Call (``ai.chat.manual``) is the complete raw-model step.

Use case: a workflow author who used to pick "Agent with Tools" or "Agent with
Visible Reasoning" now builds the same step on Custom AI Call — a model, tools,
an iteration cap — and also sets how hard the model thinks and the exact JSON it
must return. Both settings must reach the provider request; neither may be
invented when the author left it unset (our reasoning default is LOWER than the
provider's, so the step must not send one of its own).

The provider call (``execute_ai_request``) is the only stand-in; the node, the
Holder resolution and ``UnifiedConfig`` are the real code.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_graph.actions.decorator import resolve_action_executor
from matrx_graph.types.node_spec import EmptyConfig
from matrx_graph.types.result import Success
from pydantic import ValidationError

from matrx_ai.graph_nodes.chat_action import ChatManualInput
from matrx_ai.graph_nodes.tests.test_node_handlers_execute import _ctx, _FakeCompleted

SCHEMA = {
    "type": "object",
    "properties": {"verdict": {"type": "string"}, "confidence": {"type": "number"}},
    "required": ["verdict", "confidence"],
}


def _record_config(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    from matrx_ai.orchestrator import executor as executor_module

    seen: dict[str, Any] = {}

    async def _fake(config: Any, **kwargs: Any) -> Any:
        seen["config"] = config
        seen["max_iterations"] = kwargs.get("max_iterations")
        return _FakeCompleted()

    monkeypatch.setattr(executor_module, "execute_ai_request", _fake)
    return seen


async def _run(inputs: ChatManualInput) -> Any:
    return await resolve_action_executor("ai.chat.manual").execute(_ctx(), inputs, EmptyConfig())


@pytest.mark.asyncio
async def test_reasoning_and_output_schema_reach_the_provider_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = _record_config(monkeypatch)
    inputs = ChatManualInput(
        model="gpt-5",
        user_input="Is this invoice a duplicate?",
        tools=["table"],
        max_iterations=6,
        reasoning_effort="low",
        output_schema=SCHEMA,
    )

    result = await _run(inputs)

    assert isinstance(result, Success)
    config = seen["config"]
    assert config.reasoning_effort == "low"
    rf = config.response_format
    rf = rf.model_dump(mode="json", by_alias=True) if hasattr(rf, "model_dump") else rf
    assert rf["type"] == "json_schema"
    assert rf["json_schema"]["strict"] is True
    assert set(rf["json_schema"]["schema"]["properties"]) == {"verdict", "confidence"}
    assert seen["max_iterations"] == 6


@pytest.mark.asyncio
async def test_unset_reasoning_and_schema_send_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    seen = _record_config(monkeypatch)

    await _run(ChatManualInput(model="gpt-5", user_input="hello"))

    config = seen["config"]
    assert config.reasoning_effort is None, "the step invented a reasoning level"
    assert config.response_format is None


def test_reasoning_uses_the_platform_vocabulary() -> None:
    assert ChatManualInput(model="gpt-5", reasoning_effort="none").reasoning_effort == "none"
    with pytest.raises(ValidationError):
        ChatManualInput(model="gpt-5", reasoning_effort="extreme")


@pytest.mark.asyncio
async def test_an_empty_output_schema_fails_loudly(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_graph.errors import ExecutionError

    _record_config(monkeypatch)
    with pytest.raises(ExecutionError, match="empty") as refused:
        await _run(ChatManualInput(model="gpt-5", user_input="hi", output_schema={}))
    message = str(refused.value)
    assert message.startswith("ai.chat.manual:"), "the refusal must name Custom AI Call"
    assert "ai.llm.chat" not in message
