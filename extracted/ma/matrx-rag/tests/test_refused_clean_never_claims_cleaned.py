"""A refused page cleaner never makes a document read "Cleaned" (2026-10-07).

Live: after admin@admin.com passed its weekly AI usage limit, two PDF Extractor
uploads (docs 74f47689… / 336b6377…) had 0 cleaned pages, yet
``processed_documents.clean_content`` held ~the raw text and
``clean_content_completed_at`` was stamped 4 s after creation — because
``stages.run_clean`` joined every degraded page's RAW text into clean_content
and wrote it unconditionally, then reported the stage done.

Forcing function (each leg fails on the pre-fix source):
- run_clean wrote clean_content and returned normally on a refused run;
- every page asked the cleaner again after the first refusal, and a refusal
  was filed as a ``rag_page_clean_degraded`` incident;
- a never-cleaned page (section_kind NULL, cleaned_text "") chunked to "".
"""

from __future__ import annotations

import asyncio
from typing import Any

import matrx_orm
import pytest

import matrx_rag.llm as llm_mod
from matrx_rag import stages
from matrx_rag.llm import PageCleanIncompleteError, page_text_for_downstream

LIMIT = "You've reached your AI usage limit for now. Upgrade your plan to keep going."


class _Refusal(Exception):
    is_caller_refusal = True


def _runner(monkeypatch, *, refuse: bool, calls: list[str]) -> None:
    class _Runner:
        async def clean_page(self, raw: str, *, timeout: float | None = None):
            calls.append(raw)
            if refuse:
                raise _Refusal(LIMIT)
            return {"text": f"clean {raw}", "section_kind": "letter"}

    monkeypatch.setattr(llm_mod, "_require_runner", lambda: _Runner())
    monkeypatch.setattr(llm_mod, "vcprint", lambda *a, **kw: None)


def test_refusal_stops_asking_and_files_no_incident(monkeypatch):
    calls: list[str] = []
    _runner(monkeypatch, refuse=True, calls=calls)
    recorded: list[Any] = []

    async def _record_error(exc: BaseException, **kw: Any) -> None:
        recorded.append(exc)

    monkeypatch.setattr(matrx_orm, "record_error", _record_error)
    out = asyncio.run(llm_mod.clean_pdf_pages(["p0", "p1", "p2", "p3"]))

    assert len(calls) == 1, "a quota refusal is not transient — ask once"
    assert all(c.degraded and c.refused and c.failure_reason == LIMIT for c in out)
    assert recorded == [], "a caller refusal is not an incident"
    err = llm_mod.clean_incomplete_error(out)
    assert isinstance(err, PageCleanIncompleteError)
    assert err.refused and err.is_caller_refusal
    assert "AI usage limit reached" in str(err) and LIMIT in str(err)
    assert "4 of 4 pages not cleaned" in str(err)


class _Rows:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self._rows = rows

    def filter(self, **_kw: Any) -> _Rows:
        return self

    def order_by(self, *_a: Any) -> _Rows:
        return self

    async def values(self, *_cols: str) -> list[dict[str, Any]]:
        return [dict(r) for r in self._rows]


def _wire_run_clean(monkeypatch, writes: list[tuple[str, str]]) -> None:
    from matrx_rag.pdf_pipeline import _ExtractedPage

    async def _load_pages(_pid: str):
        return [
            _ExtractedPage(page_index=i, text=f"raw page {i}", used_ocr=False, char_count=10)
            for i in range(3)
        ]

    class _Writer:
        async def update_clean_content(self, doc_id, clean_content, owner_id):
            writes.append((doc_id, clean_content))

        async def update_page_cleanup(self, **_kw: Any) -> None:
            return None

    rows = [{"page_index": i, "cleaned_text": "", "section_kind": None} for i in range(3)]
    monkeypatch.setattr(stages, "_load_pages", _load_pages)
    monkeypatch.setattr(stages, "get_db_model", lambda _name: _Rows(rows))
    monkeypatch.setattr(stages, "get_document_writer", lambda: _Writer())


def test_refused_run_clean_raises_and_never_writes_clean_content(monkeypatch):
    calls: list[str] = []
    _runner(monkeypatch, refuse=True, calls=calls)

    async def _record_error(exc: BaseException, **kw: Any) -> None:
        return None

    monkeypatch.setattr(matrx_orm, "record_error", _record_error)
    writes: list[tuple[str, str]] = []
    _wire_run_clean(monkeypatch, writes)

    with pytest.raises(PageCleanIncompleteError) as caught:
        asyncio.run(stages.run_clean(processed_document_id="d" * 36, owner_id="u" * 36))

    assert writes == [], "clean_content / clean_content_completed_at must not be stamped"
    assert caught.value.refused and LIMIT in str(caught.value)


def test_healthy_run_clean_still_writes_clean_content(monkeypatch):
    calls: list[str] = []
    _runner(monkeypatch, refuse=False, calls=calls)
    writes: list[tuple[str, str]] = []
    _wire_run_clean(monkeypatch, writes)

    asyncio.run(stages.run_clean(processed_document_id="d" * 36, owner_id="u" * 36))

    assert len(writes) == 1
    assert "clean raw page 0" in writes[0][1]


def test_never_cleaned_page_feeds_downstream_its_raw_text():
    never = {"cleaned_text": "", "section_kind": None, "raw_text": "RAW"}
    illegible = {"cleaned_text": "", "section_kind": "illegible_scan", "raw_text": "smudge"}
    assert page_text_for_downstream(never) == "RAW"
    assert page_text_for_downstream(illegible) == ""
