"""A catalog model that "can see images" but sits on a computer WITHOUT its vision projector (mmproj)
cannot see them: llama-server refuses an image it has no projector for.

One-chat C2 follow-up. Vision on a device route is true only when the device reports the projector
file; otherwise the image takes the same convert-to-text path with the ``media_converted`` line.
Locked through the real profile resolution, the real media fallback and the real device translator.
"""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.emitters.stream_emitter import StreamEmitter

from matrx_ai.catalog import device_placement
from matrx_ai.catalog.resolve import resolve_call_profile
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

DEVICE = "6f1c2a7e-3b9d-4c1e-8f0a-2d4b6c8e0a13"
MODEL_ID = "2c4e6a80-9b1d-4f3e-8a5c-7e9f1b3d5a70"
MODEL = "qwen3-vl-4b"
SV = ServedVia.model_validate({"provider": "device", "app_instance_id": DEVICE, "local_model_id": MODEL_ID})
PIXEL = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="


def _catalog_model(projector: bool | None) -> Any:
    """What the host's placement check answers for a catalog model; ``None`` = reports nothing."""
    if projector is None:
        return None
    return device_placement.DeviceCatalogModel(vision_projector=projector)


@pytest.fixture
def seeded(monkeypatch: pytest.MonkeyPatch):
    from matrx_ai.catalog.manager import ai_catalog_manager
    from matrx_ai.db.ai_models.ai_model_manager import ai_model_manager_instance

    ai_catalog_manager.load_from_rows(
        endpoints=[], apis=[], offerings=[], settings=[], providers={"prov": "Qwen"},
        models=[{"id": MODEL_ID, "name": MODEL, "provider_id": "prov"}],
    )

    async def load_model(ref: str) -> Any:
        if ref not in (MODEL_ID, MODEL):
            return None
        return SimpleNamespace(
            id=MODEL_ID, name=MODEL, provider_id="prov", max_tokens=8192,
            # The catalog says this model can see images.
            capabilities={"input": ["text", "image"], "output": ["text"], "features": ["function_calling"]},
            pricing=None,
        )

    monkeypatch.setattr(ai_model_manager_instance, "load_model", load_model)
    monkeypatch.setattr(media_handler, "_RESOLVERS", dict(media_handler._RESOLVERS))

    async def ocr(content: Any, ctx: MediaResolveContext) -> ResolverResult:
        return ResolverResult(
            replacement=TextContent(text="[Image converted to OCR text]\n\nTOTAL 12.00"),
            action="extracted",
            user_message=f"Image converted to text because {ctx.model_name} cannot read images directly.",
            system_message="ImageContent converted to OCR text (11 chars).",
        )

    register_media_resolver(MediaContainer.IMAGE, ocr)
    verdict: dict[str, Any] = {"value": _catalog_model(False)}

    async def check(served_via: ServedVia, *, model_id: str) -> Any:
        return verdict["value"]

    device_placement.configure_device_placement(check)
    yield verdict
    device_placement.configure_device_placement(None)


def _chat() -> MessageList:
    return MessageList(_messages=[
        UnifiedMessage(role="user", content=[
            TextContent(text="What does this receipt say?"),
            ImageContent(base64_data=PIXEL, mime_type="image/png"),
        ]),
    ])


async def _send(messages: MessageList, profile: Any) -> dict:
    converted, _ = await preprocess_unsupported_media(
        messages, profile.wire_format, model_name=MODEL,
        model_supports_vision=profile.capabilities.supports_vision,
    )
    for _ in range(5):
        await asyncio.sleep(0)
    return DeviceChat().to_provider_config(UnifiedConfig(model=MODEL, messages=converted), profile)


@pytest.mark.asyncio
async def test_no_projector_on_the_device_means_no_vision_and_the_image_becomes_text(seeded) -> None:
    profile = await resolve_call_profile(MODEL_ID, served_via=SV)
    assert profile.capabilities.supports_vision is False
    emitter = StreamEmitter()
    token = set_app_context(AppContext(user_id="u-1", emitter=emitter, metadata={}))
    try:
        body = await _send(_chat(), profile)
        warnings = [w for w in emitter.take_warnings() if w["code"] == MEDIA_CONVERTED_CODE]
    finally:
        clear_app_context(token)
    wire = json.dumps(body["messages"])
    assert "image_url" not in wire and PIXEL not in wire, "an image reached a model with no projector"
    assert "TOTAL 12.00" in wire
    assert len(warnings) == 1


@pytest.mark.asyncio
async def test_a_reported_projector_keeps_vision_and_sends_the_image(seeded) -> None:
    seeded["value"] = _catalog_model(True)
    profile = await resolve_call_profile(MODEL_ID, served_via=SV)
    assert profile.capabilities.supports_vision is True
    body = await _send(_chat(), profile)
    assert "image_url" in json.dumps(body["messages"])


@pytest.mark.asyncio
async def test_a_host_that_reports_nothing_leaves_the_catalogs_word_alone(seeded) -> None:
    seeded["value"] = _catalog_model(None)
    profile = await resolve_call_profile(MODEL_ID, served_via=SV)
    assert profile.capabilities.supports_vision is True
