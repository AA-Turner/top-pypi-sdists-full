"""Every page that has raw text ends with clean text — a page the output guard refuses keeps its own
text, marked so, and the refusal is recorded with its reason (live 2026-11-18).

Live: a Matrx Scan PDF import (document 9ea26230…, fd602314…, 2fc44e44…) showed pages, raw text and
chunks but NO clean text. One page held "Quarterly lease renewal for the north office" (44 chars);
the page cleaner answered 417-463 chars; ``cleaned_output_rejection`` refused it ("more than 1.3x —
not a cleanup"); the page came back degraded, was never written, and ``run_clean`` raised
``PageCleanIncompleteError`` — so ``clean_content`` was never written, on every retry, because the
same page went to the same cleaner again. A tiny-page floor (200 chars) landed the same morning; a
longer refused page still failed the whole document's clean text forever.

The contract these tests hold (the owner's rule for scans: every scan ends with raw text, clean text
and chunks): a page whose cleaning is skipped or refused has clean text EQUAL TO ITS RAW TEXT, a
``section_kind`` that says why (``short_page_verbatim`` / ``clean_rejected_raw``), and the refusal's
reason filed as one ``system_error`` row. A CALLER REFUSAL (usage limit) and a provider failure are
not refusals by the guard: those still fail the stage and are retried (2026-10-07 law, unchanged).

The break each test catches:
- a guard-refused page is not written, or written empty, or the document's clean text is not written;
- the refused page is written without a status (an operator could not tell it was never cleaned);
- the reason is dropped (nothing filed) — "nothing fails silently";
- the passthrough leaks onto a usage-limit refusal (which must still fail the stage).
"""

from __future__ import annotations

import asyncio
from typing import Any

import matrx_orm
import pytest

import matrx_rag._ext as ext_mod
import matrx_rag.llm as llm_mod
from matrx_rag import stages
from matrx_rag.llm import (
    SHORT_PAGE_KIND,
    PageCleanIncompleteError,
    page_is_cleaned,
    page_text_is_raw,
)

# A two-page PDF with its own text layer: an ordinary memo page and a short heading page.
MEMO = (
    "Quarterly lease renewal for the north office\n"
    + "The landlord proposed a three percent increase effective at the start of the next term. "
    "Facilities recommends accepting if the parking allotment is restored to twelve spaces and "
    "the HVAC service contract is moved to the landlord's account.\n" * 3
)
HEADING = "Quarterly lease renewal for the north office"  # 44 chars — the live page
# What the live cleaner did: kept the text and wrote far more around it.
PADDING = " " + ("This page appears to be part of a scanned business document about a lease. " * 9)


def _wire(
    monkeypatch,
    texts: list[str],
    answer,
    *,
    min_chars: int = 0,
) -> tuple[dict[int, dict[str, Any]], list[str], list[dict[str, Any]]]:
    """Run ``stages.run_clean`` over ``texts`` (pages read from the PDF's own text layer) with a
    stubbed cleaner ``answer(raw) -> dict | Exception``. Returns page writes, doc writes, errors."""
    from matrx_rag.pdf_pipeline import _ExtractedPage

    class _Runner:
        async def clean_page(self, raw: str, *, timeout: float | None = None) -> dict[str, Any]:
            out = answer(raw)
            if isinstance(out, BaseException):
                raise out
            return out

    monkeypatch.setattr(llm_mod, "_require_runner", lambda: _Runner())
    monkeypatch.setattr(llm_mod, "vcprint", lambda *a, **kw: None)

    errors: list[dict[str, Any]] = []

    async def _record_error(exc: BaseException, **kw: Any) -> None:
        errors.append({"exc": exc, **kw})

    monkeypatch.setattr(matrx_orm, "record_error", _record_error)

    async def _min() -> int:
        return min_chars

    monkeypatch.setitem(ext_mod._registry, "clean_min_page_chars", _min)

    async def _load_pages(_pid: str):
        return [
            _ExtractedPage(page_index=i, text=t, used_ocr=False, char_count=len(t))
            for i, t in enumerate(texts)
        ]

    page_writes: dict[int, dict[str, Any]] = {}
    doc_writes: list[str] = []

    class _Writer:
        async def update_clean_content(self, doc_id, clean_content, owner_id):
            doc_writes.append(clean_content)

        async def update_page_cleanup(self, **kw: Any) -> None:
            page_writes[kw["page_index"]] = kw

    class _Rows:
        def filter(self, **_kw: Any) -> _Rows:
            return self

        def order_by(self, *_a: Any) -> _Rows:
            return self

        async def values(self, *_cols: str) -> list[dict[str, Any]]:
            return [{"page_index": i, "cleaned_text": "", "section_kind": None} for i in range(len(texts))]

    monkeypatch.setattr(stages, "_load_pages", _load_pages)
    monkeypatch.setattr(stages, "get_db_model", lambda _name: _Rows())
    monkeypatch.setattr(stages, "get_document_writer", lambda: _Writer())
    return page_writes, doc_writes, errors


def _run_clean() -> Any:
    return asyncio.run(stages.run_clean(processed_document_id="d" * 36, owner_id="u" * 36))


def _kept_raw_errors(errors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [e for e in errors if e.get("kind") == "rag_page_clean_kept_raw"]


def test_whole_pdf_with_its_own_text_layer_ends_with_clean_text_when_a_long_page_is_refused(monkeypatch):
    """The long memo page balloons (refused, over the tiny floor); the heading cleans honestly.
    The document still gets clean text; the refused page holds its raw text, marked, reason filed."""

    def answer(raw: str):
        if raw == MEMO:
            return {"text": raw + PADDING * 3, "section_kind": "business_memo"}
        return {"text": raw.strip(), "section_kind": "title_page"}

    page_writes, doc_writes, errors = _wire(monkeypatch, [MEMO, HEADING], answer)
    _run_clean()

    refused = page_writes[0]
    assert refused["cleaned_text"] == MEMO.strip(), "a refused page keeps its own text as clean text"
    assert refused["section_kind"] == llm_mod.CLEAN_REJECTED_KIND
    assert page_is_cleaned(refused["cleaned_text"], refused["section_kind"])
    assert page_text_is_raw({**refused, "raw_text": MEMO}), "chunks from it are marked raw-based"
    assert page_writes[1]["cleaned_text"] == HEADING
    assert doc_writes == [f"{MEMO.strip()}\n\n{HEADING}"], "the document's clean text is written"
    kept = _kept_raw_errors(errors)
    assert len(kept) == 1 and "not a cleanup" in str(kept[0]["exc"])
    assert kept[0]["context"]["kept_raw_page_indexes"] == [0]


def test_a_short_page_refused_by_the_guard_keeps_its_line_and_files_no_error(monkeypatch):
    """The exact live page: 44 chars, short-page knob off (0), cleaner answers ~460 chars."""
    page_writes, doc_writes, errors = _wire(
        monkeypatch, [HEADING, HEADING], lambda raw: {"text": raw + PADDING, "section_kind": "letter"}
    )
    _run_clean()

    for i in (0, 1):
        assert page_writes[i]["cleaned_text"] == HEADING
        assert page_writes[i]["section_kind"] == SHORT_PAGE_KIND
    assert doc_writes == [f"{HEADING}\n\n{HEADING}"]
    assert _kept_raw_errors(errors) == []  # a tiny page kept verbatim is correct, not a system error


def test_a_gutted_answer_is_refused_and_the_page_keeps_its_text(monkeypatch):
    """The other side of the guard: the cleaner drops most of a legible page."""
    page_writes, doc_writes, errors = _wire(
        monkeypatch, [MEMO], lambda raw: {"text": "Lease.", "section_kind": "business_memo"}
    )
    _run_clean()

    assert page_writes[0]["cleaned_text"] == MEMO.strip()
    assert page_writes[0]["section_kind"] == llm_mod.CLEAN_REJECTED_KIND
    assert doc_writes == [MEMO.strip()]
    assert "less than" in str(_kept_raw_errors(errors)[0]["exc"])


def test_a_usage_limit_refusal_still_fails_the_stage(monkeypatch):
    """The passthrough is for the guard's refusal only — a caller refusal is the person's to fix
    and must never be stamped as clean text (2026-10-07)."""

    class _Refused(RuntimeError):
        is_caller_refusal = True

    page_writes, doc_writes, errors = _wire(monkeypatch, [MEMO], lambda raw: _Refused("AI usage limit reached"))
    with pytest.raises(PageCleanIncompleteError):
        _run_clean()
    assert page_writes == {} and doc_writes == []
    assert _kept_raw_errors(errors) == []
