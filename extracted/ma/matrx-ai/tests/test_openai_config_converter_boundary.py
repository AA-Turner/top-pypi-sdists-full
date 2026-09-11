"""The config layer consumes response-shaped values without importing an SDK."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, get_type_hints

from openai.types.responses import (
    ResponseFunctionToolCall,
    ResponseFunctionWebSearch,
    ResponseOutputMessage,
    ResponseOutputText,
    ResponseReasoningItem,
    ResponseUsage,
)

from matrx_ai.config.extra_config import WebSearchCallContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent
from matrx_ai.config.unified_content import TextContent, ThinkingContent
from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.providers.openai.translator import OpenAITranslator


class Shape(SimpleNamespace):
    """Minimal response-shaped input for the provider-neutral config boundary."""

    def model_dump(self, *, exclude: set[str] | None = None, **_: Any) -> dict[str, Any]:
        return {key: value for key, value in vars(self).items() if key not in (exclude or set())}


def _sdk_usage() -> ResponseUsage:
    return ResponseUsage(
        input_tokens=7,
        output_tokens=3,
        total_tokens=10,
        input_tokens_details={"cached_tokens": 2, "cache_write_tokens": 0},
        output_tokens_details={"reasoning_tokens": 0},
    )


def _sdk_text() -> ResponseOutputText:
    return ResponseOutputText(type="output_text", text="hello", annotations=[])


def _sdk_reasoning() -> ResponseReasoningItem:
    return ResponseReasoningItem(id="rs_1", type="reasoning", summary=[], encrypted_content="enc")


def _sdk_tool_call() -> ResponseFunctionToolCall:
    return ResponseFunctionToolCall(
        id="fc_1", call_id="call_1", name="lookup", arguments='{"q":"x"}', type="function_call"
    )


def _sdk_web_search() -> ResponseFunctionWebSearch:
    return ResponseFunctionWebSearch(
        id="ws_1", type="web_search_call", status="completed", action={"type": "search", "query": "x"}
    )


def test_openai_config_converters_accept_sdk_objects_and_neutral_shapes() -> None:
    sdk_usage = TokenUsage.from_openai(_sdk_usage(), "m", "provider")
    neutral_usage = TokenUsage.from_openai(
        Shape(
            input_tokens=7,
            output_tokens=3,
            input_tokens_details=Shape(cached_tokens=2),
            model_dump=lambda **_: {"input_tokens": 7, "output_tokens": 3},
        ),
        "m",
        "provider",
    )
    assert (sdk_usage.input_tokens, sdk_usage.cached_input_tokens) == (5, 2)
    assert (neutral_usage.input_tokens, neutral_usage.cached_input_tokens) == (5, 2)

    for value in (_sdk_text(), Shape(text="hello", annotations=[])):
        assert TextContent.from_openai(value, "msg_1").text == "hello"
    for value in (_sdk_reasoning(), Shape(id="rs_1", encrypted_content="enc", summary=[])):
        assert ThinkingContent.from_openai(value).signature == "enc"
    for value in (_sdk_tool_call(), Shape(id="fc_1", call_id="call_1", name="lookup", arguments="{}")):
        assert ToolCallContent.from_openai(value).id == "call_1"
    for value in (_sdk_web_search(), Shape(id="ws_1", status="completed", action={"query": "x"})):
        assert WebSearchCallContent.from_openai(value).id == "ws_1"

    sdk_message = ResponseOutputMessage(
        id="msg_1", type="message", role="assistant", status="completed", content=[_sdk_text()]
    )
    neutral_message = Shape(
        id="msg_1", type="message", role="assistant", status="completed", content=[Shape(type="output_text", text="hello", annotations=[])]
    )
    for value in (sdk_message, neutral_message):
        assert UnifiedMessage.from_openai_item(value).content[0].text == "hello"


def test_config_converter_reflection_declares_neutral_inputs() -> None:
    converters = (
        (TokenUsage.from_openai, "usage"),
        (TextContent.from_openai, "content_item"),
        (ThinkingContent.from_openai, "item"),
        (ToolCallContent.from_openai, "item"),
        (UnifiedMessage.from_openai_item, "item"),
        (WebSearchCallContent.from_openai, "content_item"),
    )
    for converter, parameter in converters:
        assert get_type_hints(converter)[parameter] is Any


def test_openai_translator_still_consumes_real_sdk_items() -> None:
    response = OpenAITranslator()._build_unified_messages([_sdk_reasoning(), _sdk_tool_call()])
    assert [type(block) for message in response for block in message.content] == [
        ThinkingContent,
        ToolCallContent,
    ]
