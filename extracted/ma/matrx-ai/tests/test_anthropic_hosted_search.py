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

    # Carried as provider state — never a ToolCallContent the local executor
    # would try to dispatch, and never dropped (see the round-trip test below).
    assert [type(block).__name__ for block in message.content] == [
        "HostedToolContent",
        "HostedToolContent",
        "TextContent",
    ]
    from matrx_ai.config import ToolCallContent

    assert not any(isinstance(block, ToolCallContent) for block in message.content)


_INTERLEAVED_TURN = [
    {"type": "thinking", "thinking": "look it up", "signature": "sig-1"},
    {
        "type": "server_tool_use",
        "id": "srvtoolu_1",
        "name": "web_search",
        "input": {"query": "MX Master 4 810-010674"},
        "cache_control": None,
    },
    {
        "type": "web_search_tool_result",
        "tool_use_id": "srvtoolu_1",
        "content": [
            {
                "type": "web_search_result",
                "url": "https://example.test/spec",
                "title": "Spec",
                "encrypted_content": "enc",
                "page_age": None,
            }
        ],
    },
    {"type": "thinking", "thinking": "the 810 prefix differs", "signature": "sig-2"},
    {"type": "tool_use", "id": "toolu_1", "name": "web", "input": {"action": "read", "url": "u"}},
]


def test_interleaved_hosted_search_turn_replays_block_for_block():
    """The 2026-09-14 class: hosted search + extended thinking + a LOCAL tool call
    in one turn. Anthropic requires the latest assistant message back exactly as
    produced once a tool result follows it; dropping the hosted blocks turned
    ``[thinking, server_tool_use, web_search_tool_result, thinking, tool_use]``
    into ``[thinking, thinking, tool_use]`` and Anthropic refused the resend
    ("`thinking` or `redacted_thinking` blocks ... cannot be modified")."""
    message = Message.from_anthropic_content("assistant", _INTERLEAVED_TURN)
    replayed = message.to_anthropic_blocks()

    assert [b["type"] for b in replayed] == [b["type"] for b in _INTERLEAVED_TURN]
    assert replayed[0] == {"type": "thinking", "thinking": "look it up", "signature": "sig-1"}
    # Verbatim, minus the SDK's null-valued optional fields.
    assert replayed[1] == {
        "type": "server_tool_use",
        "id": "srvtoolu_1",
        "name": "web_search",
        "input": {"query": "MX Master 4 810-010674"},
    }
    assert replayed[2]["content"][0] == {
        "type": "web_search_result",
        "url": "https://example.test/spec",
        "title": "Spec",
        "encrypted_content": "enc",
    }
    assert replayed[4]["id"] == "toolu_1"


def test_hosted_blocks_survive_storage_and_reload():
    from matrx_ai.config.unified_content import reconstruct_content

    message = Message.from_anthropic_content("assistant", _INTERLEAVED_TURN)
    stored = [block.to_storage_dict() for block in message.content]
    assert stored[1]["type"] == "hosted_tool"
    assert stored[1]["provider"] == "anthropic"

    rebuilt = [reconstruct_content(item) for item in stored]
    assert [type(b).__name__ for b in rebuilt] == [type(b).__name__ for b in message.content]
    assert rebuilt[2].to_anthropic() == message.content[2].to_anthropic()


def test_hosted_blocks_are_dropped_for_other_providers():
    message = Message.from_anthropic_content("assistant", _INTERLEAVED_TURN)
    hosted = [b for b in message.content if type(b).__name__ == "HostedToolContent"]
    assert hosted and all(b.to_openai() is None and b.to_google() is None for b in hosted)


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
