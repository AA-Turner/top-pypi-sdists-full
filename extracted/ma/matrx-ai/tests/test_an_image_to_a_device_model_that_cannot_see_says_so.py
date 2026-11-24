"""An image sent to a model on this computer that cannot see gives ONE honest line — no error, no
silent drop.

One-chat plan C2: a person attaches an image, then switches the chat to a text-only model on their
computer (or attaches it after the switch). ``UnifiedAIClient.execute`` runs the media fallback
with the device route's own capabilities (``supports_vision`` from the model's declared input) on
the ``device_chat`` wire; the host's image resolver turns the image into text. Until 2026-11-08 the
only notice was a ``media_notice`` data event no chat renders: the person's image was quietly
replaced. Locked here, through the real fallback and the real device translator:

1. no image part reaches llama-server (it would refuse a model without a vision projector);
2. the person gets exactly one ``media_converted`` warning line, even when a loop converts the
   same image on every provider call (promoted to a visible line by @ai-matrx/chat);
3. the same image to a vision model is sent as an image and says nothing.

The resolver is a stand-in for the host's (aidream ``media_resolvers/local_media.resolve_image``,
OCR) installed through the package's one seam, ``register_media_resolver``.
"""

from __future__ import annotations

import asyncio
import json

import pytest
from matrx_connect.emitters.stream_emitter import StreamEmitter

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.served_via import ServedVia
from matrx_ai.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_ai.processing.media_fallback import handler as media_handler
from matrx_ai.processing.media_fallback.handler import (
    MEDIA_CONVERTED_CODE,
    MediaResolveContext,
    ResolverResult,
    preprocess_unsupported_media,
    register_media_resolver,
)
from matrx_ai.providers.device.device_api import DeviceChat
from matrx_ai.providers.provider_io_capabilities import MediaContainer
from matrx_ai.testing.profile_factory import make_profile

DEVICE = "506e6752-13b3-4616-b99e-dab6f0e436ab"
MODEL = "qwen-3-4b"
PIXEL = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="


def _profile(inputs: list[str]):
    return make_profile(
        model_name=MODEL, wire_format="device_chat", vendor="device", provider_model_id=MODEL,
        capabilities={"input": inputs, "output": ["text"], "features": ["function_calling"], "interaction": "turn"},
    ).model_copy(update={"route_kind": "device", "served_via": ServedVia.model_validate(
        {"provider": "device", "app_instance_id": DEVICE, "local_model_id": MODEL})})


def _chat() -> MessageList:
    return MessageList(_messages=[
        UnifiedMessage(role="user", content=[
            TextContent(text="What does this receipt say?"),
            ImageContent(base64_data=PIXEL, mime_type="image/png"),
        ]),
    ])


async def _ocr(content, ctx: MediaResolveContext) -> ResolverResult:
    return ResolverResult(
        replacement=TextContent(text="[Image converted to OCR text]\n\nTOTAL 12.00"),
        action="extracted",
        user_message=f"Image converted to text because {ctx.model_name} cannot read images directly.",
        system_message="ImageContent converted to OCR text (11 chars).",
    )


@pytest.fixture(autouse=True)
def _host_resolver(monkeypatch):
    monkeypatch.setattr(media_handler, "_RESOLVERS", dict(media_handler._RESOLVERS))
    register_media_resolver(MediaContainer.IMAGE, _ocr)


async def _send(messages: MessageList, profile) -> dict:
    """What ``UnifiedAIClient.execute`` does for the device route: fallback, then the translator."""
    converted, _usage = await preprocess_unsupported_media(
        messages, profile.wire_format, model_name=MODEL,
        model_supports_vision=profile.capabilities.supports_vision,
    )
    for _ in range(5):  # the warning rides a detached task (send_client_warning)
        await asyncio.sleep(0)
    return DeviceChat().to_provider_config(UnifiedConfig(model=MODEL, messages=converted), profile)


@pytest.mark.asyncio
async def test_a_text_only_device_model_gets_text_and_the_person_one_line() -> None:
    profile = _profile(["text"])
    assert profile.capabilities.supports_vision is False
    emitter = StreamEmitter()
    token = set_app_context(AppContext(user_id="u-1", emitter=emitter, metadata={}))
    try:
        messages = _chat()
        body = await _send(messages, profile)
        await _send(messages, profile)  # the loop's next provider call converts it again
        warnings = [w for w in emitter.take_warnings() if w["code"] == MEDIA_CONVERTED_CODE]
    finally:
        clear_app_context(token)
    wire = json.dumps(body["messages"])
    assert "image_url" not in wire and PIXEL not in wire, "the image reached a model that cannot see"
    assert "TOTAL 12.00" in wire, "the image's text never reached the model"
    assert len(warnings) == 1, f"expected one line, got {warnings}"
    assert warnings[0]["user_message"] == f"Image converted to text because {MODEL} cannot read images directly."
    assert warnings[0].get("count", 1) == 1


@pytest.mark.asyncio
async def test_a_vision_device_model_gets_the_image_and_no_line() -> None:
    profile = _profile(["text", "image"])
    emitter = StreamEmitter()
    token = set_app_context(AppContext(user_id="u-1", emitter=emitter, metadata={}))
    try:
        body = await _send(_chat(), profile)
        warnings = [w for w in emitter.take_warnings() if w["code"] == MEDIA_CONVERTED_CODE]
    finally:
        clear_app_context(token)
    assert "image_url" in json.dumps(body["messages"])
    assert warnings == []
