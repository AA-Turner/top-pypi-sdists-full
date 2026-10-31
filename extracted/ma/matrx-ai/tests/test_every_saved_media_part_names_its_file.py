"""Every media part a run sends as inline bytes is saved naming its file (url or file_id).

Live defect (2026-10-30): podcast extraction from a file URL failed AFTER the model answered, in
both the user_input and host_turn forms, because the message save refused the inline PDF:
``DocumentMediaPart requires 'url' or 'file_id'``. The class: any internal caller that resolves a
reference to bytes itself (``_resolve_file_block``, face frames, ...) built a part with bytes only,
and persistence strips bytes. Each test here failed before the fix.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.db.message_parts import validate_message_content

KINDS = {
    "image": "image/png",
    "audio": "audio/mpeg",
    "video": "video/mp4",
    "document": "application/pdf",
}


def _inline(kind: str) -> dict:
    return {"type": "media", "kind": kind, "base64_data": "QUJD", "mime_type": KINDS[kind]}


@pytest.fixture
def saved(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, str]]:
    import matrx_ai.context.app_context as app_context
    import matrx_ai.media.media_persistence as media_persistence

    monkeypatch.setattr(app_context, "try_get_app_context", lambda: SimpleNamespace())
    calls: list[tuple[str, str]] = []

    async def fake_save(blob: str, mime: str, **_: object) -> SimpleNamespace:
        calls.append((blob, mime))
        return SimpleNamespace(file_id=f"f-{len(calls)}", url=f"https://files.example/f-{len(calls)}", size_bytes=3)

    monkeypatch.setattr(media_persistence, "save_media_envelope_async", fake_save)
    return calls


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", sorted(KINDS))
async def test_an_ordinary_run_saves_inline_media_of_every_kind(kind: str, saved: list) -> None:
    from matrx_ai.persistence.sealed import stored_message_content

    rows = await stored_message_content([{"type": "text", "text": "t"}, _inline(kind)])
    assert saved == [("QUJD", KINDS[kind])]
    assert rows[1]["file_id"] == "f-1" and "base64_data" not in rows[1]


@pytest.mark.asyncio
async def test_a_part_that_names_its_source_is_never_uploaded_again(saved: list) -> None:
    from matrx_ai.persistence.sealed import stored_message_content

    part = {**_inline("document"), "url": "https://example.com/a.pdf"}
    rows = await stored_message_content([part])
    assert saved == [] and rows[0]["url"] == "https://example.com/a.pdf"


@pytest.mark.asyncio
async def test_the_podcast_extractor_file_block_saves(monkeypatch: pytest.MonkeyPatch, saved: list) -> None:
    """The live path: _resolve_file_block -> HostTurn attachment -> the saved user message."""
    import matrx_ai.agent_runners.podcast_generator as pg
    from matrx_ai.config.unified_config import UnifiedMessage
    from matrx_ai.persistence.sealed import stored_message_content

    url = "https://example.com/brief.pdf"

    class FM:
        async def resolve_media_async(self, ref, needs_bytes=True):
            ref.base64_data, ref.mime_type = "JVBERi0=", "application/pdf"

    monkeypatch.setattr(pg, "has_ext", lambda name: True)
    monkeypatch.setattr(pg, "get_ext", lambda name: (lambda: FM()))
    block = await pg._resolve_file_block(url)
    message = UnifiedMessage.from_dict({"role": "user", "content": [{"type": "input_text", "text": "x"}, block]})
    rows = await stored_message_content(message.to_storage_dict()["content"])
    doc = [r for r in rows if r.get("kind") == "document"][0]
    assert doc["url"] == url and saved == []
    with pytest.raises(ValueError, match="requires 'url' or 'file_id'"):
        validate_message_content([{k: v for k, v in message.to_storage_dict()["content"][1].items() if k != "url"}])
