"""A document whose every page is blank (a photo with no writing, an image-only scan) raises the
named NoTextToChunkError, not a bare "no_chunks_produced" crash (system_error class
sec_1c44dd99..., 2026-11-14, content_type page_photo). A page WITH text that yields no chunks stays
the plain RuntimeError — that is a real chunker bug."""

from __future__ import annotations

from typing import Any

import pytest

from matrx_rag import stages
from matrx_rag.pdf_pipeline import _ExtractedPage


def _wire(monkeypatch: pytest.MonkeyPatch, text: str) -> None:
    import matrx_rag.ingestion as ingestion

    async def load_doc(_: str) -> dict[str, Any]:
        return {"id": "d1", "created_by": "u1", "organization_id": "o1", "name": "n",
                "mime_type": "image/jpeg", "source_kind": "cld_file", "source_id": "s1"}

    async def load_pages(_: str) -> list[_ExtractedPage]:
        return [_ExtractedPage(page_index=0, text=text, used_ocr=True, char_count=len(text))]

    async def empty(_: str) -> list:
        return []

    async def kinds(_: str) -> list[str]:
        return ["page"]

    async def not_raw(_: str) -> bool:
        return False

    async def org(o: Any, _owner: Any) -> str:
        return str(o)

    monkeypatch.setattr(stages, "_load_doc", load_doc)
    monkeypatch.setattr(stages, "_load_pages", load_pages)
    monkeypatch.setattr(stages, "_load_cleaned_pages", empty)
    monkeypatch.setattr(stages, "_load_portion_kinds", kinds)
    monkeypatch.setattr(stages, "_any_page_text_is_raw", not_raw)
    monkeypatch.setattr(ingestion, "resolve_effective_org", org)
    monkeypatch.setattr(stages, "chunk_pdf_pages", lambda *_a, **_k: [])


async def test_blank_pages_raise_the_named_no_text_error(monkeypatch: pytest.MonkeyPatch) -> None:
    _wire(monkeypatch, "  \n ")
    with pytest.raises(stages.NoTextToChunkError, match="no_chunks_produced"):
        await stages.run_chunk(processed_document_id="d1", owner_id="u1")


async def test_text_that_yields_no_chunks_stays_a_real_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    _wire(monkeypatch, "Real words on the page.")
    with pytest.raises(RuntimeError, match="no_chunks_produced") as info:
        await stages.run_chunk(processed_document_id="d1", owner_id="u1")
    assert not isinstance(info.value, stages.NoTextToChunkError)
