"""A reply after a made picture never sends the picture inside an assistant turn.

Live 2026-11-10 (CGU-10 AND-V IMG4, chat bd194318…): an image model made a picture, then one
Claude turn in the same chat failed with *"Anthropic rejected the request: messages.1.content:
'image' blocks are not permitted within assistant turns."* The made picture is stored on the
assistant message that answered with it, and every translator but Gemini's put it inside that
assistant turn. The OpenAI Responses API (assistant content is ``output_text``/``refusal``) and
Chat Completions (``image_url`` on a user message only) refuse the same shape.

Two layers, each tested alone (``config/assistant_turn_media.py``):

1. the send boundary carries the picture to a host-written user turn after the assistant turn
   (the model still SEES what it made);
2. a translator handed the raw history (no boundary) names it instead of sending a 400 shape.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.send_boundary import _carry_assistant_media, order_for_wire
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.groq.translator import GroqTranslator
from matrx_ai.providers.openai.translator import OpenAITranslator
from matrx_ai.testing.profile_factory import make_profile

_PNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
_FILE_ID = "5d64da50-0000-4000-8000-000000000001"


def _made_picture() -> ImageContent:
    return ImageContent(base64_data=_PNG, mime_type="image/png", file_id=_FILE_ID)


def _conversation() -> list[UnifiedMessage]:
    return [
        UnifiedMessage(role="user", content=[TextContent(text="Make a red square.")]),
        UnifiedMessage(role="assistant", content=[TextContent(text="Here it is."), _made_picture()]),
        UnifiedMessage(role="user", content=[TextContent(text="Describe what you made.")]),
    ]


def _send(translator: Any, wire_format: str, *, boundary: bool) -> Any:
    config = UnifiedConfig(model="m-x", messages=MessageList(_messages=_conversation()))
    profile = make_profile(model_name="m-x", wire_format=wire_format)
    wire = config
    if boundary:
        prep = order_for_wire(config, profile)
        _carry_assistant_media(prep, config, profile)
        wire = prep.wire_config if prep.wire_config is not None else config
    request = translator.build_request(wire, profile)
    return request if isinstance(request, dict) else dict(request)


def _blocks(message: dict[str, Any]) -> list[dict[str, Any]]:
    content = message.get("content")
    return content if isinstance(content, list) else [{"type": "text", "text": content}]


_IMAGE_TYPES = {"image", "input_image", "image_url"}

_CASES = [
    pytest.param(AnthropicTranslator, "anthropic_chat", "messages", id="anthropic"),
    pytest.param(OpenAITranslator, "openai_chat", "input", id="openai-responses"),
    pytest.param(GroqTranslator, "groq_chat", "messages", id="chat-completions"),
]


def _messages(request: dict[str, Any], key: str) -> list[dict[str, Any]]:
    return [m for m in request[key] if isinstance(m, dict) and m.get("role") in ("user", "assistant")]


@pytest.mark.parametrize("boundary", [True, False], ids=["with-boundary", "translator-alone"])
@pytest.mark.parametrize(("translator", "wire_format", "key"), _CASES)
def test_no_assistant_turn_carries_a_picture(translator: Any, wire_format: str, key: str, boundary: bool) -> None:
    for message in _messages(_send(translator(), wire_format, boundary=boundary), key):
        if message["role"] == "assistant":
            assert all(b.get("type") not in _IMAGE_TYPES for b in _blocks(message)), message


@pytest.mark.parametrize(("translator", "wire_format", "key"), _CASES)
def test_the_model_still_sees_the_picture_it_made(translator: Any, wire_format: str, key: str) -> None:
    messages = _messages(_send(translator(), wire_format, boundary=True), key)
    assistant_at = next(i for i, m in enumerate(messages) if m["role"] == "assistant")
    after = messages[assistant_at + 1 :]
    assert any(
        b.get("type") in _IMAGE_TYPES for m in after if m["role"] == "user" for b in _blocks(m)
    ), messages
    # The person's own words still end the request.
    last = messages[-1]
    assert last["role"] == "user"
    assert "Describe what you made." in str(_blocks(last)[-1])


def test_gemini_keeps_the_picture_on_its_model_turn() -> None:
    from matrx_ai.config.assistant_turn_media import carry_assistant_media

    assert carry_assistant_media(_conversation(), "google_chat") is None


def test_the_carry_waits_for_the_tool_results_of_that_turn() -> None:
    from matrx_ai.config.assistant_turn_media import CARRIED_MEDIA_KEY, carry_assistant_media
    from matrx_ai.config.message_config import ToolCallContent, ToolResultContent

    history = [
        UnifiedMessage(role="user", content=[TextContent(text="Draw, then look it up.")]),
        UnifiedMessage(
            role="assistant",
            content=[_made_picture(), ToolCallContent(id="t1", name="search", arguments={})],
        ),
        UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="t1", call_id="t1", content="ok")]),
        UnifiedMessage(role="user", content=[TextContent(text="Now?")]),
    ]
    carried = carry_assistant_media(history, "anthropic_chat")
    assert carried is not None
    roles = [m.role for m in carried]
    assert roles == ["user", "assistant", "tool", "user", "user"], roles
    assert carried[3].metadata[CARRIED_MEDIA_KEY] is True
    # The stored conversation is never touched.
    assert isinstance(history[1].content[0], ImageContent)


def test_a_prefill_turn_is_not_ended_by_a_carried_picture() -> None:
    from matrx_ai.config.assistant_turn_media import carry_assistant_media

    history = _conversation()[:2]
    assert carry_assistant_media(history, "anthropic_chat") is None
