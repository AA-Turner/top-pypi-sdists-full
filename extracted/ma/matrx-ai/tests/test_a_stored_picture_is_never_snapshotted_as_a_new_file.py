"""A STORED PICTURE IS NEVER SAVED AGAIN AS A NEW FILE BY THE REQUEST SNAPSHOT (CGU-10 AND-IMG17).

Live (server 58769ff, 2026-11-12, run 284122ea): every follow-up turn in a chat with history photos saved each
photo's bytes AGAIN as a new ``request-snapshots`` file (~850 KB, ~0.9 s each, one after another, before the
turn's save): 5 photos 4.8 s, 20 photos 16.7 s of our server's own time. The provider-shaped copy of a request
carries a picture's bytes with no file beside them, so the snapshot writer treated them as unknown. The media
pass now records which stored file (and vision class) those bytes are, and the writer references it.
"""

from __future__ import annotations

import base64
from typing import Any

import pytest

from matrx_ai import _ext
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import TextContent
from matrx_ai.orchestrator.execution_state import ExecutionState, _execution_state, set_execution_state
from matrx_ai.providers.snapshot_redactors import apply_redactors, redactors_with_stored_blobs
from matrx_ai.providers.unified_client import UnifiedAIClient

VARIANT = b"\xff\xd8\xff\xe0" + b"v" * 200_000  # a JPEG-headed blob over the snapshot's inline limit
VARIANT_B64 = base64.b64encode(VARIANT).decode()


class _FileManager:
    async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
        ref.base64_data, ref.mime_type, ref.is_resolved = VARIANT_B64, "image/jpeg", True
        return ref


class _Messages:
    def __init__(self, messages: list[UnifiedMessage]) -> None:
        self._messages = messages

    def to_list(self) -> list[UnifiedMessage]:
        return self._messages


@pytest.mark.asyncio
async def test_the_snapshot_references_the_picture_it_was_sent(monkeypatch) -> None:
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _FileManager())
    state = ExecutionState()
    token = set_execution_state(state)
    picture = ImageContent(file_id="stored-photo", mime_type="image/jpeg", resolved_url="https://cdn.example/p.jpg",
                           is_resolved=True)
    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        _Messages([UnifiedMessage(role="user", content=[TextContent(text="and now?"), picture])]),
        model_name="claude-sonnet-4-6", wire_format="anthropic", supports_vision=True,
    )
    _execution_state.reset(token)
    assert state.snapshot_media_blobs, "the media pass did not say which file the bytes are"

    uploads: list[str] = []

    async def store(raw: bytes, mime: str, sha: str, **_: Any) -> str:
        uploads.append(sha)
        return "a-new-snapshot-file"

    wire = {"messages": [{"role": "user", "content": [
        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": VARIANT_B64}}]}]}
    redactors = await redactors_with_stored_blobs(
        wire, user_id="u", organization_id="o", store=store, known=dict(state.snapshot_media_blobs)
    )
    stored = apply_redactors(wire, redactors)["messages"][0]["content"][0]["source"]["data"]
    assert uploads == [], "the picture's bytes were saved again as a new file"
    assert "stored-photo" in stored and "anthropic_sonnet_default" in stored, stored[-400:]


@pytest.mark.asyncio
async def test_bytes_no_picture_names_are_still_kept() -> None:
    """The store is still the home for bytes that name no file (a tool's inline output): never a lost blob."""
    uploads: list[str] = []

    async def store(raw: bytes, mime: str, sha: str, **_: Any) -> str:
        uploads.append(sha)
        return "snapshot-file"

    wire = {"messages": [{"role": "user", "content": [
        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": VARIANT_B64}}]}]}
    await redactors_with_stored_blobs(wire, user_id="u", organization_id="o", store=store, known={})
    assert len(uploads) == 1
