"""A system message kept in place in the history reaches EVERY provider, in order, unfilled.

Carried history keeps a later system message in place as data (``UnifiedConfig.from_dict``
with ``authored_message_count``). OpenAI-shaped wires take a mid-list system role; Anthropic
and Google have none. Before the fix, Anthropic DROPPED it (a red log line only) and Google
raised ``Unknown role 'system'``. Each provider now receives it in place, as a marked note in
the user channel (``matrx_ai.providers.system_notes``), with its text never filled or unescaped.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.testing.profile_factory import make_profile

NOTE = "Remember {{name}} and {{!kept}} exactly"


def _messages() -> list[UnifiedMessage]:
    return [
        UnifiedMessage(role="user", content=[TextContent(text="first question")]),
        UnifiedMessage(role="assistant", content=[TextContent(text="first answer")]),
        UnifiedMessage(role="system", content=[TextContent(text=NOTE)]),
        UnifiedMessage(role="user", content=[TextContent(text="second question")]),
    ]


def _config(model: str) -> UnifiedConfig:
    return UnifiedConfig(
        model=model,
        system_instruction="You are helpful.",
        messages=MessageList(_messages=_messages()),
    )


def _wire_text(request: Any) -> str:
    return json.dumps(request, default=str)


def _assert_in_order(wire: str) -> None:
    first = wire.index("first answer")
    note = wire.index(NOTE)
    second = wire.index("second question")
    assert first < note < second, wire


def test_anthropic_delivers_history_system_note_in_place() -> None:
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    request = AnthropicTranslator().build_request(
        _config("claude-sonnet"), make_profile(model_name="claude-sonnet", wire_format="anthropic_chat")
    )
    wire = _wire_text(request["messages"])
    assert NOTE in wire, "the history system message never reached Anthropic"
    _assert_in_order(wire)
    roles = [m["role"] for m in request["messages"]]
    assert roles == ["user", "assistant", "user"], roles
    texts = [b.get("text") for b in request["messages"][-1]["content"]]
    assert texts[0] == f"<system_note>\n{NOTE}\n</system_note>"
    assert texts[-1] == "second question"
    assert NOTE not in json.dumps(request.get("system"), default=str)


def test_google_delivers_history_system_note_in_place() -> None:
    from matrx_ai.providers.google.translator import GoogleTranslator

    result = GoogleTranslator().build_request(
        _config("gemini-test"), make_profile(model_name="gemini-test", wire_format="google_chat")
    )
    wire = _wire_text(result["contents"])
    assert NOTE in wire
    _assert_in_order(wire)
    roles = [c["role"] for c in result["contents"]]
    assert roles == ["user", "model", "user"], roles


def test_openai_responses_keeps_history_system_in_place() -> None:
    from matrx_ai.providers.openai.translator import OpenAITranslator

    request = OpenAITranslator().build_request(
        _config("gpt-test"), make_profile(model_name="gpt-test", wire_format="openai_responses")
    )
    wire = _wire_text(request.get("input"))
    assert NOTE in wire
    _assert_in_order(wire)


@pytest.mark.parametrize(
    ("module", "cls", "wire_format"),
    [
        ("matrx_ai.providers.groq.translator", "GroqTranslator", "groq_chat"),
        ("matrx_ai.providers.cerebras.translator", "CerebrasTranslator", "cerebras_chat"),
        ("matrx_ai.providers.together.translator", "TogetherTranslator", "together_chat"),
        ("matrx_ai.providers.generic_openai.translator", "GenericOpenAITranslator", "openai_chat"),
    ],
)
def test_chat_completions_keep_history_system_in_place(module: str, cls: str, wire_format: str) -> None:
    import importlib

    translator = getattr(importlib.import_module(module), cls)()
    request = translator.build_request(_config("m"), make_profile(model_name="m", wire_format=wire_format))
    wire = _wire_text(request["messages"])
    assert NOTE in wire
    _assert_in_order(wire)


def test_note_before_tool_results_waits_until_after_them() -> None:
    """Anthropic needs tool_result blocks FIRST in their user turn; a note between a tool call
    and its result is delivered right after the results, never in front of them."""
    from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    messages = [
        UnifiedMessage(role="user", content=[TextContent(text="go")]),
        UnifiedMessage(
            role="assistant",
            content=[ToolCallContent(id="call_1", name="lookup", arguments={})],
        ),
        UnifiedMessage(role="system", content=[TextContent(text=NOTE)]),
        UnifiedMessage(
            role="tool",
            content=[ToolResultContent(tool_use_id="call_1", call_id="call_1", name="lookup", content=[{"type": "text", "text": "ok"}])],
        ),
    ]
    config = UnifiedConfig(model="claude-sonnet", messages=MessageList(_messages=messages))
    request = AnthropicTranslator().build_request(
        config, make_profile(model_name="claude-sonnet", wire_format="anthropic_chat")
    )
    last = request["messages"][-1]
    assert last["role"] == "user"
    assert last["content"][0]["type"] == "tool_result"
    assert NOTE in last["content"][-1]["text"]


def test_conversion_is_announced_in_a_capture() -> None:
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator
    from matrx_ai.providers.request_capture import capturing_provider_request

    with capturing_provider_request() as slot:
        AnthropicTranslator().build_request(
            _config("claude-sonnet"), make_profile(model_name="claude-sonnet", wire_format="anthropic_chat")
        )
    assert any("system_note" in note for note in slot.notes), slot.notes


def test_stored_config_messages_are_never_rewritten() -> None:
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    config = _config("claude-sonnet")
    AnthropicTranslator().build_request(
        config, make_profile(model_name="claude-sonnet", wire_format="anthropic_chat")
    )
    assert [m.role for m in config.messages] == ["user", "assistant", "system", "user"]
    assert config.messages[2].content[0].text == NOTE


def _two_notes_before_a_result(result_role: str) -> list[UnifiedMessage]:
    from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent

    return [
        UnifiedMessage(role="user", content=[TextContent(text="go")]),
        UnifiedMessage(role="assistant", content=[ToolCallContent(id="call_1", name="lookup", arguments={})]),
        UnifiedMessage(role="system", content=[TextContent(text="N1")]),
        UnifiedMessage(role="system", content=[TextContent(text="N2")]),
        UnifiedMessage(
            role=result_role,
            content=[ToolResultContent(tool_use_id="call_1", call_id="call_1", name="lookup", content=[{"type": "text", "text": "ok"}])],
        ),
        UnifiedMessage(role="user", content=[TextContent(text="next")]),
    ]


@pytest.mark.parametrize("result_role", ["tool", "user"])
def test_two_notes_before_a_tool_result_both_wait_for_it(result_role: str) -> None:
    from matrx_ai.providers.system_notes import history_system_messages_as_notes

    out = history_system_messages_as_notes(_two_notes_before_a_result(result_role), provider="anthropic")
    kinds = [
        "result" if type(c).__name__ == "ToolResultContent" else (c.text if hasattr(c, "text") else type(c).__name__)
        for m in out
        for c in m.content
    ]
    assert kinds.index("result") < min(i for i, k in enumerate(kinds) if "N1" in k or "N2" in k), kinds


def test_anthropic_gets_the_result_first_with_two_notes_before_it() -> None:
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    config = UnifiedConfig(
        model="claude-sonnet", messages=MessageList(_messages=_two_notes_before_a_result("tool"))
    )
    request = AnthropicTranslator().build_request(
        config, make_profile(model_name="claude-sonnet", wire_format="anthropic_chat")
    )
    result_turn = request["messages"][2]
    assert result_turn["role"] == "user"
    assert result_turn["content"][0]["type"] == "tool_result", result_turn
    texts = [b.get("text", "") for b in result_turn["content"][1:]]
    assert "N1" in texts[0] and "N2" in texts[1], texts


def test_google_gets_the_result_first_with_two_notes_before_it() -> None:
    from matrx_ai.providers.google.translator import GoogleTranslator

    config = UnifiedConfig(
        model="gemini-test", messages=MessageList(_messages=_two_notes_before_a_result("tool"))
    )
    result = GoogleTranslator().build_request(
        config, make_profile(model_name="gemini-test", wire_format="google_chat")
    )
    parts = result["contents"][2]["parts"]
    assert "function_response" in parts[0] or "functionResponse" in parts[0], parts
