"""A chat that switches models mid-way (cloud -> this computer -> cloud) sends a wire each side accepts.

One-chat plan C2 (common-docs/systems/chat/conversations/projects/one-chat-local-and-cloud/PLAN.md):
a device pick keeps the conversation, so the SAME history — tool turns, reasoning and all — is
replayed to llama-server (OpenAI Chat Completions) and then back to the cloud model. What either
side rejects, and what this asserts never reaches its wire:

* on the device (Chat Completions): an assistant ``tool_calls`` entry with no ``role: tool`` answer
  right after it, a ``tool`` message answering no call, or provider signature material;
* on the cloud (Anthropic Messages): a ``tool_use`` without its ``tool_result`` in the very next user
  message, an id outside ``^[a-zA-Z0-9_-]+$``, foreign (unsigned) thinking sent as a thinking block,
  or two messages in a row with the same role.

The history is built from the shapes each provider's parser stores (Anthropic thinking carries its
signature; llama-server's ``reasoning_content`` is stored as ``generic_openai`` thinking with no
signature; llama-server mints its own short call ids). The translators are the real ones the
device route (``DeviceChat``) and the Claude route (``AnthropicTranslator``) send through.
"""

from __future__ import annotations

import json
import re
from typing import Any

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.served_via import ServedVia
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_content import ThinkingContent
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.device.device_api import DeviceChat
from matrx_ai.testing.profile_factory import make_profile

DEVICE = "506e6752-13b3-4616-b99e-dab6f0e436ab"
DEVICE_MODEL = "qwen-3-4b"
CLOUD_MODEL = "claude-sonnet-5"
CLOUD_CALL = "toolu_01AbCdEfGh"
DEVICE_CALL = "Q7xk2Lp9mN3vR1sT"
_ANTHROPIC_ID = re.compile(r"^[a-zA-Z0-9_-]+$")
_CAPS = {
    "input": ["text"],
    "output": ["text"],
    "features": ["function_calling", "reasoning"],
    "interaction": "turn",
}


def _call(call_id: str, city: str) -> ToolCallContent:
    return ToolCallContent(id=call_id, name="get_weather", arguments={"city": city})


def _result(call_id: str, text: str) -> UnifiedMessage:
    return UnifiedMessage(
        role="tool",
        content=[ToolResultContent(tool_use_id=call_id, name="get_weather", content=[{"type": "text", "text": text}])],
    )


def _cloud_turn() -> list[UnifiedMessage]:
    return [
        UnifiedMessage(role="user", content=[TextContent(text="What is the weather in Paris?")]),
        UnifiedMessage(
            role="assistant",
            content=[
                ThinkingContent(text="Look it up.", provider="anthropic", signature="sig-anthropic-123"),
                TextContent(text="Checking."),
                _call(CLOUD_CALL, "Paris"),
            ],
        ),
        _result(CLOUD_CALL, "12C, cloudy"),
        UnifiedMessage(role="assistant", content=[TextContent(text="Paris is 12C and cloudy.")]),
    ]


def _device_turn() -> list[UnifiedMessage]:
    return [
        UnifiedMessage(role="user", content=[TextContent(text="And Rome?")]),
        UnifiedMessage(
            role="assistant",
            content=[ThinkingContent(text="Same tool, Rome.", provider="generic_openai"), _call(DEVICE_CALL, "Rome")],
        ),
        _result(DEVICE_CALL, "18C, sunny"),
        UnifiedMessage(role="assistant", content=[TextContent(text="Rome is 18C and sunny.")]),
    ]


def _config(model: str, messages: list[UnifiedMessage]) -> UnifiedConfig:
    return UnifiedConfig(model=model, messages=MessageList(_messages=messages))


def _device_wire(messages: list[UnifiedMessage]) -> list[dict[str, Any]]:
    profile = make_profile(
        model_name=DEVICE_MODEL, wire_format="device_chat", vendor="device", provider_model_id=DEVICE_MODEL, capabilities=_CAPS,
    ).model_copy(update={"route_kind": "device", "served_via": ServedVia.model_validate(
        {"provider": "device", "app_instance_id": DEVICE, "local_model_id": DEVICE_MODEL})})
    return DeviceChat().to_provider_config(_config(DEVICE_MODEL, messages), profile)["messages"]


def _cloud_wire(messages: list[UnifiedMessage]) -> list[dict[str, Any]]:
    profile = make_profile(model_name=CLOUD_MODEL, wire_format="anthropic_chat", capabilities=_CAPS)
    return AnthropicTranslator().to_anthropic(_config(CLOUD_MODEL, messages), profile)["messages"]


def _assert_chat_completions_pairing(wire: list[dict[str, Any]], expected_calls: set[str]) -> None:
    """Every assistant tool call is answered by ``role: tool`` messages right after it, and every
    tool message answers a call that is still open."""
    open_calls: list[str] = []
    seen: set[str] = set()
    for index, message in enumerate(wire):
        role = message["role"]
        if role == "tool":
            assert message.get("tool_call_id") in open_calls, f"#{index} answers no open call: {message}"
            open_calls.remove(message["tool_call_id"])
            continue
        assert not open_calls, f"#{index} ({role}) arrived while calls {open_calls} were unanswered"
        for call in message.get("tool_calls") or []:
            assert call["id"], f"#{index} has a call with no id"
            assert call["function"]["name"] == "get_weather"
            json.loads(call["function"]["arguments"])
            open_calls.append(call["id"])
            seen.add(call["id"])
    assert not open_calls, f"calls never answered: {open_calls}"
    assert seen == expected_calls, f"tool calls lost on the device wire: sent {seen}, expected {expected_calls}"


def _assert_no_signature_material(wire: list[dict[str, Any]]) -> None:
    blob = json.dumps(wire, default=repr)
    assert "sig-anthropic-123" not in blob, "a Claude thinking signature reached the device"
    assert "signature" not in blob


def test_the_device_turn_after_a_cloud_tool_turn_sends_valid_pairing() -> None:
    history = _cloud_turn() + [UnifiedMessage(role="user", content=[TextContent(text="And Rome?")])]
    wire = _device_wire(history)
    _assert_chat_completions_pairing(wire, {CLOUD_CALL})
    _assert_no_signature_material(wire)
    assert wire[-1] == {"role": "user", "content": "And Rome?"}


def test_the_device_loop_after_its_own_tool_call_sends_valid_pairing() -> None:
    history = _cloud_turn() + _device_turn()[:3]
    wire = _device_wire(history)
    _assert_chat_completions_pairing(wire, {CLOUD_CALL, DEVICE_CALL})
    _assert_no_signature_material(wire)
    assert wire[-1]["role"] == "tool" and wire[-1]["tool_call_id"] == DEVICE_CALL


def test_back_on_the_cloud_every_tool_use_is_answered_next_with_a_legal_id() -> None:
    history = _cloud_turn() + _device_turn() + [
        UnifiedMessage(role="user", content=[TextContent(text="And Berlin?")]),
    ]
    wire = _cloud_wire(history)
    tool_uses: set[str] = set()
    for index, message in enumerate(wire):
        for block in message["content"]:
            if not (isinstance(block, dict) and block.get("type") == "tool_use"):
                continue
            tool_uses.add(block["id"])
            assert _ANTHROPIC_ID.match(block["id"]), block["id"]
            nxt = wire[index + 1]
            assert nxt["role"] == "user"
            answered = {b.get("tool_use_id") for b in nxt["content"] if isinstance(b, dict)}
            assert block["id"] in answered, f"tool_use {block['id']} has no tool_result next"
    assert tool_uses == {CLOUD_CALL, DEVICE_CALL}, f"tool calls lost on the cloud wire: {tool_uses}"


def test_back_on_the_cloud_the_devices_thinking_is_never_an_unsigned_thinking_block() -> None:
    history = _cloud_turn() + _device_turn() + [
        UnifiedMessage(role="user", content=[TextContent(text="And Berlin?")]),
    ]
    for message in _cloud_wire(history):
        for block in message["content"]:
            if isinstance(block, dict) and block.get("type") in {"thinking", "redacted_thinking"}:
                assert block.get("signature"), f"foreign thinking sent as {block['type']}: {block}"


def test_back_on_the_cloud_roles_alternate_and_the_new_question_is_last() -> None:
    history = _cloud_turn() + _device_turn() + [
        UnifiedMessage(role="user", content=[TextContent(text="And Berlin?")]),
    ]
    wire = _cloud_wire(history)
    assert wire[0]["role"] == "user"
    for prev, cur in zip(wire, wire[1:]):
        assert prev["role"] != cur["role"], (prev["role"], cur["role"])
    texts = [b.get("text") for b in wire[-1]["content"] if isinstance(b, dict)]
    assert "And Berlin?" in texts
