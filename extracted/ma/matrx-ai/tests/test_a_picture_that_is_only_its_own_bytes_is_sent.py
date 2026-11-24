"""A PICTURE THAT IS ONLY ITS OWN BYTES IS SENT, NEVER "READ" BY AN IDENTIFIER IT DOES NOT HAVE.

Live system_error 427ad97a (2026-11-12, ``media_pass_read_failed: no_identifier``): a picture carrying inline bytes
and naming no file, URL or file URI (a tool's screenshot, pasted bytes) went to the resolver by identifier, which
answered ``no_identifier``; the media pass then cleared the bytes in hand, announced the picture unreadable and filed
a platform error. Its own bytes are the only copy, so they are re-encoded for the model's vision class and sent.
"""

from __future__ import annotations

import base64
import io
from typing import Any

import pytest

from matrx_ai import _ext
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import TextContent
from matrx_ai.providers.unified_client import UnifiedAIClient


class _ResolverLikeFileManager:
    """Mirrors matrx-files' short circuit: a ref naming nothing comes back ``no_identifier``."""

    def __init__(self) -> None:
        self.reads = 0

    async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
        self.reads += 1
        if not ref.is_resolved and not ref.has_identifier():
            ref.resolver_error = "no_identifier"
        return ref


class _Messages:
    def __init__(self, messages: list[UnifiedMessage]) -> None:
        self._messages = messages

    def to_list(self) -> list[UnifiedMessage]:
        return self._messages


def _png_b64() -> str:
    from PIL import Image

    buf = io.BytesIO()
    Image.new("RGB", (64, 64), (200, 10, 10)).save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode()


@pytest.mark.asyncio
async def test_inline_bytes_naming_nothing_are_sent_not_failed(monkeypatch) -> None:
    fm = _ResolverLikeFileManager()
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: fm)
    captured: list[str] = []

    async def capture(exc: BaseException, *, kind: str, **_: Any) -> None:
        captured.append(kind)

    import matrx_connect.streaming.error_capture as ec

    monkeypatch.setattr(ec, "capture_error", capture)
    picture = ImageContent(base64_data=_png_b64(), mime_type="image/png")
    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        _Messages([UnifiedMessage(role="user", content=[TextContent(text="what is this?"), picture])]),
        model_name="gpt-5.4-nano", wire_format="openai_responses", supports_vision=True,
    )
    assert "media_pass_read_failed" not in captured, captured
    assert picture.base64_data, "the only copy of the picture was thrown away"
    assert picture.resolver_error is None
    assert fm.reads == 0, "a picture naming nothing was sent to the resolver by identifier"
