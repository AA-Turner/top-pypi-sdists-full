"""A document's chunks are keyed on the document's OWN source kind (SOURCE-CONVERGENCE §3.4).

``run_chunk`` wrote every chunk as ``source_kind="cld_file"`` — correct while the engine was
file-only, wrong the moment a landed transcript or web page is re-driven from its row: its chunks
were filed as a file's (``cld_file`` + the transcript's id), invisible to every per-kind filter and
colliding with the file namespace. Found landing the Phase 1a fixtures live (2026-09-25).

The guard runs the real chunker over a fake page set and asserts the rows it hands the database —
and the prior-chunk delete — carry the document's kind, for a file AND for a transcript.
"""

from __future__ import annotations

import contextlib
from typing import Any

import pytest

from matrx_rag import stages
from matrx_rag.llm import CleanedPage
from matrx_rag.pdf_pipeline import _ExtractedPage


class _FakeKgChunks:
    def __init__(self) -> None:
        self.deleted: list[dict[str, Any]] = []
        self.created: list[dict[str, Any]] = []

    async def delete_where(self, **kw: Any) -> int:
        self.deleted.append(kw)
        return 0

    async def bulk_create(self, rows: list[dict[str, Any]]) -> None:
        self.created.extend(rows)


@pytest.mark.parametrize("kind", ["cld_file", "transcript", "scrape_parsed_page"])
async def test_run_chunk_keys_chunks_on_the_documents_kind(monkeypatch: pytest.MonkeyPatch, kind: str) -> None:
    fake = _FakeKgChunks()
    doc = {
        "id": "d1",
        "created_by": "u1",
        "organization_id": "o1",
        "name": "n",
        "mime_type": "text/plain",
        "source_kind": kind,
        "source_id": "s1",
    }

    async def load_doc(_: str) -> dict[str, Any]:
        return doc

    async def load_pages(_: str) -> list[_ExtractedPage]:
        return [_ExtractedPage(page_index=0, text="Alpha beta gamma. " * 40, used_ocr=False, char_count=720)]

    async def load_cleaned(_: str) -> list[CleanedPage]:
        return []

    async def lookup(_: str) -> dict[int, str]:
        return {0: "p1"}

    async def org(o: Any, _owner: Any) -> str:
        return str(o)

    import matrx_rag.ingestion as ingestion

    monkeypatch.setattr(stages, "_load_doc", load_doc)
    monkeypatch.setattr(stages, "_load_pages", load_pages)
    monkeypatch.setattr(stages, "_load_cleaned_pages", load_cleaned)
    monkeypatch.setattr(stages, "_load_page_id_lookup", lookup)

    async def kinds(_: str) -> list[str]:
        return ["page"]

    monkeypatch.setattr(stages, "_load_portion_kinds", kinds)

    async def not_raw(_: str) -> bool:
        return False

    monkeypatch.setattr(stages, "_any_page_text_is_raw", not_raw)
    monkeypatch.setattr(stages, "get_db_model", lambda name: fake)
    monkeypatch.setattr(ingestion, "resolve_effective_org", org)

    class _Async(contextlib.AbstractAsyncContextManager):
        async def __aexit__(self, *exc: Any) -> None:
            return None

    monkeypatch.setattr(stages, "transaction", lambda *_a, **_k: _Async())

    await stages.run_chunk(processed_document_id="d1", owner_id="u1")
    assert fake.created, "the chunker produced no rows"
    assert {r["source_kind"] for r in fake.created} == {kind}
    assert fake.deleted == [{"source_kind": kind, "source_id": "s1", "field_id__isnull": True}]


async def test_portions_are_chunked_once_each(monkeypatch: pytest.MonkeyPatch) -> None:
    """Two short transcript turns -> ONE window chunk holding both turns once each, anchored to its
    first segment (a caption-sized chunk is not retrievable, audit 2026-09-26); never a parent plus
    an identical child, never one turn twice (verifier, 2026-09-25)."""
    fake = _FakeKgChunks()
    doc = {"id": "d1", "created_by": "u1", "organization_id": "o1", "name": "n", "mime_type": "text/plain",
           "source_kind": "transcript", "source_id": "t1"}
    texts = ["Ann: we begin the test.", "Bob: portions carry timestamps."]

    async def load_doc(_: str) -> dict[str, Any]:
        return doc

    async def load_pages(_: str) -> list[_ExtractedPage]:
        return [_ExtractedPage(page_index=i, text=t, used_ocr=False, char_count=len(t)) for i, t in enumerate(texts)]

    async def load_cleaned(_: str) -> list[CleanedPage]:
        return [CleanedPage(text=t, section_kind="segment", section_title=None) for t in texts]

    async def lookup(_: str) -> dict[int, str]:
        return {0: "p0", 1: "p1"}

    async def kinds(_: str) -> list[str]:
        return ["segment", "segment"]

    async def locators(_: str) -> list[dict[str, Any]]:
        return [{"t0_ms": 0, "t1_ms": 1500, "speaker": "Ann"}, {"t0_ms": 1500, "t1_ms": 3200, "speaker": "Bob"}]

    async def org(o: Any, _owner: Any) -> str:
        return str(o)

    import matrx_rag.ingestion as ingestion

    async def _not_raw(_: str) -> bool:
        return False

    class _Async(contextlib.AbstractAsyncContextManager):
        async def __aexit__(self, *exc: Any) -> None:
            return None

    for name, fn in [("_load_doc", load_doc), ("_load_pages", load_pages), ("_load_cleaned_pages", load_cleaned),
                     ("_load_page_id_lookup", lookup), ("_load_portion_kinds", kinds),
                     ("_load_portion_locators", locators),
                     ("_any_page_text_is_raw", _not_raw)]:
        monkeypatch.setattr(stages, name, fn)
    monkeypatch.setattr(stages, "get_db_model", lambda name: fake)
    monkeypatch.setattr(stages, "transaction", lambda *_a, **_k: _Async())
    monkeypatch.setattr(ingestion, "resolve_effective_org", org)

    await stages.run_chunk(processed_document_id="d1", owner_id="u1")
    got = [(r["content_text"], r["page_numbers"], r["primary_page_id"]) for r in fake.created]
    assert len(got) == 1, got
    text, pages, primary = got[0]
    assert pages == [1, 2] and primary == "p0"
    assert text.count("we begin the test.") == 1 and text.count("portions carry timestamps.") == 1
