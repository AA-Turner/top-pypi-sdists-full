"""AN UNREADABLE PICTURE STAYS IN HER STORED TURN, AND THE PERSON IS TOLD (CGU-10 AND-V IMG18, findings F1 + F2).

AND-IMG18 N4 swaps a picture the media pass could not read for ``UNREADABLE_PICTURE_TEXT`` IN PLACE, in
``config.messages`` — the same list ``CompletedRequest.to_storage_dict`` writes at the end of the turn. The
turn's new user message (and any new tool-result screenshot) has no id yet, so it is INSERTED from that list:

* F1 — one transient storage read failure (S3 ``SlowDown``) permanently replaces the picture in the stored
  ``chat.message.content`` — the model's lossless replay copy every later turn is rebuilt from — with a text
  part (the display copy ``user_content`` keeps it), and ``content_text`` (the one projection the N5 readers
  use) returns the stand-in as her words. The stand-in carries no marker (``is_unsaved_attachment_stand_in``
  is the existing one).
* F2 — the stand-in is announced to the model and to the admin error log only; the person in the chat
  is never told (Law 4: a stand-in announces itself). ``announce_tool_adaptations`` shows the pattern
  (``emitter.send_warning(WarningPayload(...))``).

Fixed: the picture is swapped only on a SEND-ONLY copy (``_without_unreadable_pictures`` + ``_provider_view``), never in
the stored list; the stand-in is marked (``UNREADABLE_PICTURE_KEY``) so ``content_text`` skips it; a ``WarningPayload`` tells her.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai import _ext
from matrx_ai.config import UnifiedConfig
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.message_config import UnifiedMessage, content_text
from matrx_ai.config.unified_content import TextContent
from matrx_ai.providers.unified_client import UnifiedAIClient

FILE_ID = "11111111-1111-1111-1111-111111111111"


class _FailingFileManager:
    async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
        ref.resolver_error = "storage_read_failed: SlowDown"
        ref.is_resolved = False
        return ref


async def _failed_turn(monkeypatch) -> UnifiedConfig:
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _FailingFileManager())

    async def _capture(*_: Any, **__: Any) -> None:
        return None

    import matrx_connect.streaming.error_capture as ec

    monkeypatch.setattr(ec, "capture_error", _capture)
    import matrx_ai.providers.unified_client as uc

    monkeypatch.setattr(uc, "_MEDIA_PASS_RETRY_BACKOFF_S", 0.0)
    picture = ImageContent(file_id=FILE_ID, mime_type="image/jpeg", resolved_url="https://x/master.jpg", is_resolved=True)
    config = UnifiedConfig(
        model="claude-sonnet-5-5",
        messages=[UnifiedMessage(role="user", content=[TextContent(text="what is this?"), picture])],
    )
    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        config.messages, model_name="claude-sonnet-5-5", wire_format="anthropic_chat", supports_vision=True,
    )
    return config


@pytest.mark.asyncio
async def test_her_stored_turn_still_names_the_picture(monkeypatch) -> None:
    stored = (await _failed_turn(monkeypatch)).to_storage_dict()["messages"][0]["content"]
    assert any(isinstance(p, dict) and p.get("file_id") == FILE_ID and p.get("type") != "text" for p in stored), stored


@pytest.mark.asyncio
async def test_the_stand_in_is_never_her_words(monkeypatch) -> None:
    stored = (await _failed_turn(monkeypatch)).to_storage_dict()["messages"][0]["content"]
    assert content_text(stored) == "what is this?", content_text(stored)


@pytest.mark.asyncio
async def test_the_person_is_told(monkeypatch) -> None:
    warnings: list[Any] = []

    class _Emitter:
        async def send_warning(self, payload: Any) -> None:
            warnings.append(payload)

        def __getattr__(self, name: str) -> Any:
            async def _noop(*_: Any, **__: Any) -> None:
                return None

            return _noop

    class _Ctx:
        emitter = _Emitter()

    import matrx_connect.context.app_context as ac

    monkeypatch.setattr(ac, "try_get_app_context", lambda: _Ctx())
    await _failed_turn(monkeypatch)
    assert warnings, "a picture was dropped from the turn and nothing told the person"
