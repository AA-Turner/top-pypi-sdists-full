from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.config import TextContent, TokenUsage, UnifiedConfig, UnifiedMessage
from matrx_ai.config.message_config import UnifiedMessage as Message
from matrx_ai.providers.anthropic.anthropic_api import AnthropicChat
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.testing.profile_factory import make_profile


def _profile():
    return make_profile(
        model_name="claude-opus-4-5-20250929",
        wire_format="anthropic_chat",
        capabilities={
            "input": ["text"],
            "output": ["text"],
            "features": ["function_calling", "structured_output", "web_search"],
            "interaction": "turn",
        },
    )


def _config(*, search: bool) -> UnifiedConfig:
    return UnifiedConfig(
        model="claude-opus-4-5-20250929",
        messages=[UnifiedMessage(role="user", content=[TextContent(text="verify this")])],
        internal_web_search=search,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "Verdict",
                "schema": {
                    "type": "object",
                    "properties": {"passed": {"type": "boolean"}},
                    "required": ["passed"],
                    "additionalProperties": False,
                },
            },
        },
    )


def test_anthropic_native_search_coexists_with_structured_output():
    request = AnthropicTranslator().to_anthropic(_config(search=True), _profile())

    search_tools = [tool for tool in request["tools"] if tool.get("type") == "web_search_20250305"]
    assert len(search_tools) == 1
    assert search_tools[0]["name"] == "web_search"
    assert search_tools[0]["max_uses"] == 5
    assert request["output_config"]["format"]["type"] == "json_schema"


def test_anthropic_native_search_absent_when_disabled():
    request = AnthropicTranslator().to_anthropic(_config(search=False), _profile())
    assert not any(
        tool.get("type") == "web_search_20250305" for tool in request.get("tools", [])
    )


def test_hosted_search_blocks_never_become_local_tool_calls():
    message = Message.from_anthropic_content(
        "assistant",
        [
            {"type": "server_tool_use", "id": "srv_1", "name": "web_search", "input": {}},
            {"type": "web_search_tool_result", "tool_use_id": "srv_1", "content": []},
            {"type": "text", "text": '{"passed":true}'},
        ],
    )

    assert [type(block).__name__ for block in message.content] == ["TextContent"]


async def test_nonstreaming_pause_turn_continues_and_aggregates_usage():
    responses = [
        SimpleNamespace(stop_reason="pause_turn", content=[{"type": "server_tool_use"}]),
        SimpleNamespace(stop_reason="end_turn", content=[{"type": "text", "text": "done"}]),
    ]
    requests: list[dict] = []

    class _Messages:
        async def create(self, **kwargs):
            requests.append(kwargs)
            return responses.pop(0)

    class _Emitter:
        async def send_chunk(self, text):
            return None

    chat = AnthropicChat()
    chat.client = SimpleNamespace(messages=_Messages())

    def convert(response, model):
        count = 1 if response.stop_reason == "pause_turn" else 2
        return SimpleNamespace(
            usage=TokenUsage(
                input_tokens=10,
                output_tokens=5,
                matrx_model_name=model,
                api="anthropic",
                billing_components={"service.web_search": count},
            )
        )

    chat.to_unified_response = convert  # type: ignore[method-assign]
    result = await chat._execute_non_streaming(
        {"messages": [{"role": "user", "content": "search"}]},
        _Emitter(),  # type: ignore[arg-type]
        "claude-test",
    )

    assert len(requests) == 2
    assert requests[1]["messages"][-1]["role"] == "assistant"
    assert result.usage.input_tokens == 20
    assert result.usage.billing_components == {"service.web_search": 3}
