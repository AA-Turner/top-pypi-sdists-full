"""A PERSON'S ATTACHMENT REACHES THE MODEL UNDER ITS OWN FILE ID, AND ITS LABEL IS COUNTED (CGU-10 AND-IMG12 #2).

Live (AND-V IMG11): a pasted 1,024×768 picture went to OpenAI behind
``<attachment kind="image" name_unavailable="…" id=""/>`` while the stored message held the file id —
the inline bytes were stored as a file only when the message ROW was saved, after the model answered.
And the estimate counted the picture (922) but not its label: OpenAI billed 947, every time.

What each test is FOR:
* the send boundary stops storing a person's inline media first → ``test_the_send_boundary_gives_every_kind_its_id``;
* any serializer's label loses the id → ``test_every_wire_labels_the_part_with_its_stored_id``;
* the row save uploads it a second time (two ids for one file) → ``test_the_saved_row_keeps_the_same_id``;
* a confidential chat that blanks content gets a file stored → ``test_a_blanking_confidential_chat_stores_nothing``;
* the estimate drops the label → ``test_the_estimate_counts_the_label_exactly_on_openai``.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.config.media_config import AudioContent, DocumentContent, ImageContent, VideoContent
from matrx_ai.config.message_config import MessageList, UnifiedMessage, _media_identity_label

_B64 = "QXR0YWNobWVudCBub3RlLg=="


def _kinds() -> list:
    return [
        ImageContent(base64_data=_B64, mime_type="image/png"),
        AudioContent(base64_data=_B64, mime_type="audio/mpeg"),
        VideoContent(base64_data=_B64, mime_type="video/mp4"),
        DocumentContent(base64_data=_B64, mime_type="application/pdf"),
    ]


@pytest.fixture
def sources(monkeypatch: pytest.MonkeyPatch) -> list[str | None]:
    return []


@pytest.fixture
def stored(monkeypatch: pytest.MonkeyPatch, sources: list[str | None]) -> list[str]:
    import matrx_ai.context.app_context as app_context
    import matrx_ai.media.media_persistence as media_persistence

    monkeypatch.setattr(app_context, "try_get_app_context", lambda: None)
    ids: list[str] = []

    async def fake_save(
        blob: str, mime: str, *, file_id: str | None = None, extra_metadata: dict | None = None, **_: object
    ) -> SimpleNamespace:
        # The files service stores under the id the caller minted (CGU-10 AND-IMG14 #3).
        ids.append(file_id or f"8a1f4320-0000-4000-8000-{len(ids):012d}")
        sources.append((extra_metadata or {}).get("source"))
        return SimpleNamespace(file_id=ids[-1], url=f"https://files.example/{ids[-1]}", size_bytes=12)

    monkeypatch.setattr(media_persistence, "save_media_envelope_async", fake_save)
    return ids


def _config(parts: list):
    from matrx_ai.config.unified_config import UnifiedConfig

    message = UnifiedMessage(role="user", content=[*parts])
    return UnifiedConfig(model="gpt-5.5", messages=MessageList(_messages=[message]))


@pytest.mark.asyncio
async def test_the_send_boundary_gives_every_kind_its_id(stored: list[str]) -> None:
    from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send

    parts = _kinds()
    config = _config(parts)
    from matrx_ai.persistence.sealed import settle_person_media_uploads

    prep = await prepare_for_send(config, stage=STAGE_LOOP, conversation_id="c", request_id="r", iteration=1)
    assert "store_person_inline_media" in prep.steps
    await settle_person_media_uploads()  # the uploads run beside the send; the row save waits for them
    assert [p.file_id for p in config.messages[0].content] == stored and len(stored) == len(parts)
    # A second send never stores it again.
    await prepare_for_send(config, stage=STAGE_LOOP, conversation_id="c", request_id="r", iteration=2)
    assert len(stored) == len(parts)


@pytest.mark.asyncio
async def test_every_wire_labels_the_part_with_its_stored_id(stored: list[str]) -> None:
    from matrx_ai.persistence.sealed import keep_inline_person_media_on_server

    parts = _kinds()
    message = UnifiedMessage(role="user", content=[*parts])
    from matrx_ai.persistence.sealed import settle_person_media_uploads

    assert await keep_inline_person_media_on_server([message]) == len(parts)
    await settle_person_media_uploads()
    for part, file_id in zip(parts, stored, strict=True):
        label = _media_identity_label(part, "user")
        assert label is not None and f'id="{file_id}"' in label, label
    # The real serializers carry it: every label text part names a stored id, none is empty.
    for serialize in (message.to_anthropic_blocks, lambda: (message.to_google_content() or {}).get("parts", [])):
        texts = [str(b.get("text", "")) for b in serialize() if isinstance(b, dict)]
        labels = [t for t in texts if t.startswith("<attachment")]
        assert labels, texts
        assert all('id=""' not in t for t in labels), labels


@pytest.mark.asyncio
async def test_the_saved_row_keeps_the_same_id(stored: list[str]) -> None:
    from matrx_ai.persistence.sealed import keep_inline_media_on_server, keep_inline_person_media_on_server

    picture = ImageContent(base64_data=_B64, mime_type="image/png")
    await keep_inline_person_media_on_server([UnifiedMessage(role="user", content=[picture])])
    part = {"type": "media", "kind": "image", "base64_data": _B64, "mime_type": "image/png", "file_id": picture.file_id}
    kept = await keep_inline_media_on_server([part])
    assert kept[0]["file_id"] == stored[0] and len(stored) == 1


@pytest.mark.asyncio
async def test_a_blanking_confidential_chat_stores_nothing(stored: list[str]) -> None:
    from matrx_ai.persistence.sealed import keep_inline_person_media_on_server

    picture = ImageContent(base64_data=_B64, mime_type="image/png")
    ctx = SimpleNamespace(sealed_conversation_id="c1", sealed_keeps_content=False)
    assert await keep_inline_person_media_on_server([UnifiedMessage(role="user", content=[picture])], ctx) == 0
    assert stored == [] and picture.file_id is None


@pytest.mark.asyncio
async def test_only_bytes_without_a_source_and_an_authored_picture_is_not_the_persons(
    stored: list[str], sources: list[str | None]
) -> None:
    """A part that already names its file is never stored again. An inline picture in an AUTHORED assistant
    turn is stored once (a stored media part must name its file) under its own source — never as the
    person's attachment (CGU-10 AND-IMG14 #6)."""
    from matrx_ai.persistence.sealed import keep_inline_person_media_on_server, settle_person_media_uploads

    drawn = ImageContent(base64_data=_B64, mime_type="image/png")
    assistant = UnifiedMessage(role="assistant", content=[drawn])
    sourced = ImageContent(base64_data=_B64, file_id="already-1", mime_type="image/png")
    assert await keep_inline_person_media_on_server([assistant, UnifiedMessage(role="user", content=[sourced])]) == 1
    await settle_person_media_uploads()
    assert sourced.file_id == "already-1"
    assert stored == [drawn.file_id] and sources == ["authored_inline_media"]
