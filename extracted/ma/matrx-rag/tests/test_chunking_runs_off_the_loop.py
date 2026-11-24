"""``run_chunk`` tokenizes a document OFF the event loop.

Live 2026-11-03..04 (event_loop_stall 7a1d8edb, 5 stalls): ``run_chunk`` called ``chunk_portions`` on
the loop; it counts the tokens of every portion (pure CPU) and, on a cold process, the tokenizer's
first use downloads its vocabulary with a blocking ``requests.get``. Every request and step in the
process froze for 1-2 s per document. RED before: the chunker ran on the loop thread.
"""

from __future__ import annotations

import asyncio
import contextlib
from typing import Any

import pytest

from matrx_rag import stages
from matrx_rag.llm import CleanedPage
from matrx_rag.pdf_pipeline import _ExtractedPage


class _FakeKgChunks:
    async def delete_where(self, **kw: Any) -> int:
        return 0

    async def bulk_create(self, rows: list[dict[str, Any]]) -> None:
        return None


def _on_loop_thread() -> bool:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return False
    return True


@pytest.mark.parametrize("kind", ["page", "section"])
async def test_the_chunker_never_runs_on_the_loop(monkeypatch: pytest.MonkeyPatch, kind: str) -> None:
    seen: list[bool] = []
    real_pages, real_portions = stages.chunk_pdf_pages, None
    from matrx_rag import pdf_pipeline

    real_portions = pdf_pipeline.chunk_portions

    def spy_pages(*a: Any, **k: Any) -> Any:
        seen.append(_on_loop_thread())
        return real_pages(*a, **k)

    def spy_portions(*a: Any, **k: Any) -> Any:
        seen.append(_on_loop_thread())
        return real_portions(*a, **k)

    monkeypatch.setattr(stages, "chunk_pdf_pages", spy_pages)
    monkeypatch.setattr(pdf_pipeline, "chunk_portions", spy_portions)

    doc = {"id": "d1", "created_by": "u1", "organization_id": "o1", "name": "n",
           "mime_type": "text/plain", "source_kind": "cld_file", "source_id": "s1"}

    async def load_doc(_: str) -> dict[str, Any]:
        return doc

    async def load_pages(_: str) -> list[_ExtractedPage]:
        return [_ExtractedPage(page_index=0, text="Alpha beta gamma. " * 40, used_ocr=False, char_count=720)]

    async def load_cleaned(_: str) -> list[CleanedPage]:
        return []

    async def lookup(_: str) -> dict[int, str]:
        return {0: "p1"}

    async def kinds(_: str) -> list[str]:
        return [kind]

    async def no_locators(_: str) -> None:
        return None

    async def not_raw(_: str) -> bool:
        return False

    async def org(o: Any, _owner: Any) -> str:
        return str(o)

    import matrx_rag.ingestion as ingestion

    monkeypatch.setattr(stages, "_load_doc", load_doc)
    monkeypatch.setattr(stages, "_load_pages", load_pages)
    monkeypatch.setattr(stages, "_load_cleaned_pages", load_cleaned)
    monkeypatch.setattr(stages, "_load_page_id_lookup", lookup)
    monkeypatch.setattr(stages, "_load_portion_kinds", kinds)
    monkeypatch.setattr(stages, "_load_portion_locators", no_locators)
    monkeypatch.setattr(stages, "_any_page_text_is_raw", not_raw)
    monkeypatch.setattr(stages, "get_db_model", lambda name: _FakeKgChunks())
    monkeypatch.setattr(ingestion, "resolve_effective_org", org)

    class _Async(contextlib.AbstractAsyncContextManager):
        async def __aexit__(self, *exc: Any) -> None:
            return None

    monkeypatch.setattr(stages, "transaction", lambda *_a, **_k: _Async())
    monkeypatch.setattr(stages, "locked_transaction", lambda *_a, **_k: _Async())

    with contextlib.suppress(Exception):
        await stages.run_chunk(processed_document_id="d1", owner_id="u1")
    assert seen, "the chunker was never reached"
    assert seen == [False], "the chunker ran on the event loop thread"
