"""An image from an earlier turn, sent again to a model that cannot see, is converted ONCE and
announced ONCE.

One-chat C2 follow-up. History is replayed on every turn; before this, each later turn to a
text-only model ran the resolver again (OCR, or a paid video transcript) and drew the
``media_converted`` line again. The conversion now rides the item's own ``metadata`` (stored with
the message by ``to_storage_dict``, so a reloaded history carries it): turn 2 reuses the stored
text and says nothing.
"""

from __future__ import annotations

import asyncio

import pytest
from matrx_connect.emitters.stream_emitter import StreamEmitter

from matrx_ai.config import MessageList, TextContent, UnifiedMessage
from matrx_ai.config.media_config import ImageContent, reconstruct_media_content
from matrx_ai.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_ai.processing.media_fallback import handler as media_handler
from matrx_ai.processing.media_fallback.handler import (
    MEDIA_CONVERTED_CODE,
    MediaResolveContext,
    ResolverResult,
    preprocess_unsupported_media,
    register_media_resolver,
)
from matrx_ai.providers.provider_io_capabilities import MediaContainer

PIXEL = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="


@pytest.fixture
def resolver_calls(monkeypatch):
    monkeypatch.setattr(media_handler, "_RESOLVERS", dict(media_handler._RESOLVERS))
    calls: list[str] = []

    async def ocr(content, ctx: MediaResolveContext) -> ResolverResult:
        calls.append(ctx.model_name)
        return ResolverResult(
            replacement=TextContent(
                text="[Image converted to OCR text]\n\nTOTAL 12.00",
                metadata={"original_type": "image", "conversion": "ocr"},
            ),
            action="extracted",
            user_message="Image converted to text because a model cannot read images directly.",
            system_message="ImageContent converted to OCR text.",
        )

    register_media_resolver(MediaContainer.IMAGE, ocr)
    return calls


def _history(image: ImageContent) -> MessageList:
    return MessageList(_messages=[
        UnifiedMessage(role="user", content=[TextContent(text="What is the total?"), image]),
    ])


async def _one_turn(messages: MessageList, model: str) -> tuple[MessageList, list[dict]]:
    """One request: its own context (a new turn), the fallback, the warnings the person got."""
    emitter = StreamEmitter()
    token = set_app_context(AppContext(user_id="u-1", emitter=emitter, metadata={}))
    try:
        converted, _ = await preprocess_unsupported_media(
            messages, "device_chat", model_name=model, model_supports_vision=False
        )
        for _ in range(5):
            await asyncio.sleep(0)
        warnings = [w for w in emitter.take_warnings() if w["code"] == MEDIA_CONVERTED_CODE]
    finally:
        clear_app_context(token)
    return converted, warnings


def _texts(messages: MessageList) -> str:
    return "".join(getattr(c, "text", "") for m in messages.to_list() for c in m.content)


@pytest.mark.asyncio
async def test_a_later_turn_reuses_the_stored_text_and_says_nothing(resolver_calls) -> None:
    history = _history(ImageContent(base64_data=PIXEL, mime_type="image/png"))
    first, first_warnings = await _one_turn(history, "qwen3-4b")
    second, second_warnings = await _one_turn(history, "qwen3-4b")
    assert "TOTAL 12.00" in _texts(first) and "TOTAL 12.00" in _texts(second)
    assert resolver_calls == ["qwen3-4b"], f"the image was converted again: {resolver_calls}"
    assert len(first_warnings) == 1
    assert second_warnings == [], f"the same image was announced again: {second_warnings}"


@pytest.mark.asyncio
async def test_the_stored_conversion_survives_a_reload_of_the_message(resolver_calls) -> None:
    image = ImageContent(base64_data=PIXEL, mime_type="image/png")
    await _one_turn(_history(image), "qwen3-4b")
    reloaded = reconstruct_media_content(image.to_storage_dict())
    again, warnings = await _one_turn(_history(reloaded), "another-text-model")
    assert "TOTAL 12.00" in _texts(again)
    assert resolver_calls == ["qwen3-4b"] and warnings == []


@pytest.mark.asyncio
async def test_a_different_image_is_still_converted_and_announced(resolver_calls) -> None:
    await _one_turn(_history(ImageContent(base64_data=PIXEL, mime_type="image/png")), "qwen3-4b")
    _, warnings = await _one_turn(_history(ImageContent(base64_data=PIXEL, mime_type="image/png")), "qwen3-4b")
    assert len(resolver_calls) == 2 and len(warnings) == 1
