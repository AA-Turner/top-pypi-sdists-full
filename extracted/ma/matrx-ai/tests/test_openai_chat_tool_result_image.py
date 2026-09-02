"""Regression — OpenAI-compatible translators must not crash on
image-bearing tool results (e.g. take_screenshot).

History: every OpenAI-Chat-style translator (Cerebras, Groq, xAI, Together,
generic_openai) had its own copy of the same buggy serialisation that did
``json.dumps(content.content)`` even when the content was a list of typed
content blocks (ImageContent + TextContent). That raised
``TypeError('Object of type ImageContent is not JSON serializable')`` on
the next iteration after a screenshot tool call resolved.

The fix moved the logic into two shared primitives:
- ``ToolResultContent.to_openai_chat()`` — returns the role=tool message
- ``ToolResultContent.extract_image_blocks()`` — for the follow-up user image

These tests lock the contract so the bug class stays extinct.
"""

from __future__ import annotations

import json

import pytest

from matrx_ai.config import (
    TextContent,
    ToolCallContent,
    ToolResultContent,
    UnifiedConfig,
    UnifiedMessage,
)
from matrx_ai.config.media_config import ImageContent
from matrx_ai.providers.cerebras.translator import CerebrasTranslator
from matrx_ai.providers.generic_openai.translator import GenericOpenAITranslator
from matrx_ai.providers.groq.translator import GroqTranslator
from matrx_ai.providers.together.translator import TogetherTranslator
# NOTE: xAI is intentionally absent — it migrated to the native xai_sdk (gRPC
# proto) request shape and no longer speaks OpenAI-chat dicts. Its equivalent
# coverage lives in test_xai_native_translator.py.


def _make_screenshot_tool_result(call_id: str = "ae37f2ece") -> ToolResultContent:
    img = ImageContent(
        url=None,
        base64_data="QkFTRTY0",
        mime_type="image/jpeg",
        file_id="a07ec5f6-5dca-43c2-9aa2-009f7f96c03b",
        is_resolved=True,
        file_size=246384,
    )
    txt = TextContent(text="Screenshot: 3706x2404, 402532 bytes, format=jpeg", id="")
    return ToolResultContent(
        tool_use_id=call_id,
        call_id=call_id,
        name="take_screenshot",
        content=[img, txt],
    )


def _make_config(messages: list[UnifiedMessage], model: str = "test-model") -> UnifiedConfig:
    return UnifiedConfig(model=model, messages=messages)


# ---------------------------------------------------------------------------
# Shared primitives — ToolResultContent.to_openai_chat / extract_image_blocks
# ---------------------------------------------------------------------------


def test_to_openai_chat_serialises_typed_block_list_without_crashing():
    """The original bug — json.dumps(list_with_ImageContent_dataclass) raises
    TypeError. The fix routes through _typed_blocks_for_openai so the
    image's storage_dict is produced first."""
    tr = _make_screenshot_tool_result()
    msg = tr.to_openai_chat()
    assert msg["role"] == "tool"
    assert msg["tool_call_id"] == "ae37f2ece"
    assert isinstance(msg["content"], str)  # role=tool only accepts string
    parsed = json.loads(msg["content"])
    assert "blocks" in parsed
    assert len(parsed["blocks"]) == 2


def test_to_openai_chat_with_string_content_unchanged():
    tr = ToolResultContent(
        tool_use_id="abc", call_id="abc", name="t",
        content="plain text result",
    )
    msg = tr.to_openai_chat()
    assert msg["content"] == "plain text result"


def test_to_openai_chat_with_dict_content_json_stringified():
    tr = ToolResultContent(
        tool_use_id="abc", call_id="abc", name="t",
        content={"ok": True, "value": 42},
    )
    msg = tr.to_openai_chat()
    assert json.loads(msg["content"]) == {"ok": True, "value": 42}


def test_extract_image_blocks_returns_only_images():
    tr = _make_screenshot_tool_result()
    blocks = tr.extract_image_blocks()
    assert len(blocks) == 1
    assert blocks[0].type == "image"


def test_extract_image_blocks_returns_empty_for_non_typed_content():
    tr = ToolResultContent(
        tool_use_id="abc", call_id="abc", name="t", content={"ok": True},
    )
    assert tr.extract_image_blocks() == []


# ---------------------------------------------------------------------------
# All 5 OpenAI-compatible translators must accept the screenshot scenario
# end-to-end without raising, and must emit a follow-up user image message.
# ---------------------------------------------------------------------------


@pytest.fixture(params=[
    ("cerebras", lambda: CerebrasTranslator(debug=False), "to_cerebras", "cerebras_chat"),
    ("groq",     lambda: GroqTranslator(debug=False),     "to_groq", "groq_chat"),
    ("together", lambda: TogetherTranslator(debug=False), "to_together", "together_chat"),
    ("generic",  lambda: GenericOpenAITranslator(debug=False), "to_generic_openai", "generic_openai_chat"),
])
def translator_under_test(request):
    from matrx_ai.testing.profile_factory import make_profile

    name, factory, method, wire_format = request.param
    instance = factory()
    bound = getattr(instance, method)
    profile = make_profile(model_name="test-model", wire_format=wire_format)
    # Every chat translator takes the ResolvedCallProfile as its second arg.
    return name, (lambda cfg: bound(cfg, profile))


def test_translator_handles_screenshot_tool_result(translator_under_test):
    name, translate = translator_under_test
    tr = _make_screenshot_tool_result()
    # A realistic conversation: the tool_result MUST be paired with the
    # assistant tool_use it answers. UnifiedConfig.__post_init__ runs
    # MessageList.sanitize(), which (correctly) drops an orphan tool_result —
    # an unpaired tool_result 400s on every provider. Without the matching
    # tool_use the screenshot result would be stripped before the translator
    # ever saw it. This is exactly the shape the translator receives in prod.
    cfg = _make_config([
        UnifiedMessage(role="user", content=[TextContent(text="screenshot please")]),
        UnifiedMessage(role="assistant", content=[
            ToolCallContent(id="ae37f2ece", name="take_screenshot", arguments={}),
        ]),
        UnifiedMessage(role="tool", content=[tr]),
    ])
    out = translate(cfg)

    roles = [m.get("role") for m in out["messages"]]
    assert "tool" in roles, f"{name}: tool message missing"

    tool_msg = next(m for m in out["messages"] if m.get("role") == "tool")
    assert tool_msg["tool_call_id"] == "ae37f2ece"
    assert isinstance(tool_msg["content"], str), \
        f"{name}: role=tool content must be string, got {type(tool_msg['content'])}"

    follow_up = [m for m in out["messages"]
                 if m.get("role") == "user" and isinstance(m.get("content"), list)]
    assert len(follow_up) >= 1, \
        f"{name}: expected a follow-up user message carrying the image"

    image_parts = [
        p for m in follow_up for p in m["content"]
        if isinstance(p, dict) and p.get("type") == "image_url"
    ]
    assert len(image_parts) == 1, \
        f"{name}: expected exactly one image_url part in follow-up user message"
    assert image_parts[0]["image_url"]["url"].startswith("data:image/jpeg;base64,")


def test_translator_handles_user_message_with_image(translator_under_test):
    """All OpenAI-chat translators must render ImageContent on a user message
    as a chat-completions multimodal content array — Cerebras / Groq /
    Together used to silently drop ImageContent before this refactor."""
    name, translate = translator_under_test
    cfg = _make_config([
        UnifiedMessage(role="user", content=[
            TextContent(text="What's in this?"),
            ImageContent(url="https://example.com/cat.jpg", mime_type="image/jpeg"),
        ]),
    ])
    out = translate(cfg)
    user_msg = next(m for m in out["messages"] if m.get("role") == "user")
    assert isinstance(user_msg["content"], list), \
        f"{name}: image-bearing user message must emit content array"
    types = [p.get("type") for p in user_msg["content"]]
    assert "image_url" in types, f"{name}: image_url part missing"
    assert "text" in types, f"{name}: text part missing"
