"""A stored file PIL cannot identify is a permanent, announced outcome: not retried, not a system_error (LIVE-ERRORS-2)."""

from __future__ import annotations

from typing import Any

from matrx_ai import _ext
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import TextContent
from matrx_ai.providers.unified_client import (
    READ_FAILURE_NOT_A_PICTURE,
    READ_FAILURE_TRANSIENT,
    UnifiedAIClient,
    _read_failure_reason,
)

ERR = "variant_render_failed: UnidentifiedImageError: cannot identify image file <_io.BytesIO object at 0x7f>"


def test_unidentified_image_is_permanent_but_other_render_failures_stay_transient() -> None:
    assert _read_failure_reason(ERR) == READ_FAILURE_NOT_A_PICTURE
    assert _read_failure_reason("variant_render_failed: RuntimeError: decoder jpeg not found") == READ_FAILURE_TRANSIENT


class _FM:
    calls = 0

    async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
        type(self).calls += 1
        ref.resolver_error = ERR
        ref.is_resolved = False
        return ref


class _Messages:
    def __init__(self, m: list[UnifiedMessage]) -> None:
        self._m = m

    def to_list(self) -> list[UnifiedMessage]:
        return self._m


async def test_not_a_picture_is_read_once_and_raises_no_system_error(monkeypatch) -> None:
    _FM.calls = 0
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _FM())
    captured: list[str] = []

    async def capture(exc: BaseException, *, kind: str, **_: Any) -> None:
        captured.append(kind)

    import matrx_connect.streaming.error_capture as ec

    monkeypatch.setattr(ec, "capture_error", capture)
    picture = ImageContent(file_id="stored", mime_type="image/jpeg", is_resolved=False)
    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        _Messages([UnifiedMessage(role="user", content=[TextContent(text="x"), picture])]),
        model_name="claude-sonnet-4-6", wire_format="anthropic_chat", supports_vision=True,
    )
    assert _FM.calls == 1
    assert captured == []
    assert picture.resolved_url is None and not picture.base64_data
