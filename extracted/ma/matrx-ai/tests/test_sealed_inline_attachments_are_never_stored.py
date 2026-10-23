"""A confidential chat's INLINE attachment (bytes never uploaded) is never validated into a row.

Without the seal an inline document is refused ("must be uploaded to storage") and the refusal
quotes the part; under a content-blanking sealed run the content funnel stores nothing at all.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.db import message_parts
from matrx_ai.db.message_parts import validate_message_content

INLINE_DOC = {
    "type": "media",
    "kind": "document",
    "base64_data": "QXR0YWNobWVudCBub3RlLiBGSUxFQ0FOQVJZWFlaLgo=",
    "mime_type": "text/plain",
    "metadata": {"name": "FILECANARYXYZ.txt"},
}


def _with_ctx(monkeypatch: pytest.MonkeyPatch, ctx: object | None) -> None:
    import matrx_ai.context.app_context as app_context

    monkeypatch.setattr(app_context, "try_get_app_context", lambda: ctx)


def test_an_unsealed_run_still_refuses_inline_bytes(monkeypatch: pytest.MonkeyPatch) -> None:
    _with_ctx(monkeypatch, None)
    with pytest.raises(ValueError, match="uploaded to storage"):
        validate_message_content([INLINE_DOC])


def test_a_sealed_run_stores_no_content_and_quotes_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    _with_ctx(monkeypatch, SimpleNamespace(sealed_conversation_id="c1", sealed_keeps_content=False))
    assert validate_message_content([{"type": "text", "text": "secret"}, INLINE_DOC]) == []


def test_an_org_that_keeps_content_still_validates(monkeypatch: pytest.MonkeyPatch) -> None:
    _with_ctx(monkeypatch, SimpleNamespace(sealed_conversation_id="c1", sealed_keeps_content=True))
    assert validate_message_content([{"type": "text", "text": "kept"}])[0]["text"] == "kept"
    assert message_parts is not None


@pytest.mark.asyncio
async def test_an_org_that_keeps_content_keeps_the_inline_file_never_refuses(monkeypatch: pytest.MonkeyPatch) -> None:
    """keep_content_on_server on: the inline file is stored like any upload and the row keeps its file_id."""
    import matrx_ai.media.media_persistence as media_persistence
    from matrx_ai.persistence.sealed import keep_inline_media_on_server

    _with_ctx(monkeypatch, SimpleNamespace(sealed_conversation_id="c1", sealed_keeps_content=True))
    saved: list[tuple[str, str]] = []

    async def fake_save(blob: str, mime: str, **_: object) -> SimpleNamespace:
        saved.append((blob, mime))
        return SimpleNamespace(file_id="f-1", url="https://files.example/f-1", size_bytes=34)

    monkeypatch.setattr(media_persistence, "save_media_envelope_async", fake_save)
    parts = await keep_inline_media_on_server([{"type": "text", "text": "kept"}, INLINE_DOC])
    assert saved == [(INLINE_DOC["base64_data"], "text/plain")]
    rows = validate_message_content(parts or [])
    assert rows[1]["file_id"] == "f-1" and "base64_data" not in rows[1]


@pytest.mark.asyncio
async def test_a_blanking_run_never_uploads_the_inline_file(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_ai.media.media_persistence as media_persistence
    from matrx_ai.persistence.sealed import keep_inline_media_on_server

    _with_ctx(monkeypatch, SimpleNamespace(sealed_conversation_id="c1", sealed_keeps_content=False))

    async def boom(*_: object, **__: object) -> None:
        raise AssertionError("a confidential run that keeps nothing must never upload")

    monkeypatch.setattr(media_persistence, "save_media_envelope_async", boom)
    assert await keep_inline_media_on_server([INLINE_DOC]) == [INLINE_DOC]
