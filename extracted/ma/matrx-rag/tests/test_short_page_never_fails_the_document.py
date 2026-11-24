"""A scan of one-line pages is never a failed document (live 2026-11-16).

Live: a Matrx Scan save whose three pages each held ONE short line (scan
d52fcf5a…, document cf097a01…) failed processing, and the retry-processing door
answered "Processing failed again" on every press. The clean stage sent each
78-char line to the page cleaner, the cleaner answered 559 chars, the growth
check (``cleaned_output_rejection``) rightly rejected that, the page came back
degraded, and ``stages.run_clean`` raised ``PageCleanIncompleteError`` for the
whole document — the same way on every retry, because the same line went to the
same cleaner again.

The break each test catches:
- the short-page threshold is not applied (or not read from the host seam): a
  one-line page reaches the cleaner and run_clean raises;
- a short page is kept but not persisted, or persisted under the wrong text or
  without its ``short_page_verbatim`` mark (an operator could not tell it was
  never cleaned, and a retry would re-pay it);
- the threshold leaks onto ordinary pages: a page at/over it stops being cleaned.
- (2026-11-18) a page under the guard's absolute floor whose answer is refused fails the document
  instead of keeping its own text (``short_page_verbatim``); a longer refused page keeps its own
  text too, marked ``clean_rejected_raw`` (``test_every_page_has_clean_text.py``).
"""

from __future__ import annotations

import asyncio
from typing import Any

import matrx_orm

import matrx_rag._ext as ext_mod
import matrx_rag.llm as llm_mod
from matrx_rag import stages
from matrx_rag.llm import SHORT_PAGE_KIND, page_is_cleaned

# Three real one-line scan pages: a receipt total, a parcel label, a sticky note.
RECEIPT = "Harbor Hardware  receipt 4471  total due $38.16  paid by card ending 0921"
LABEL = "Ship to: Marisol Ortega, 118 Cedar Row, Unit 4, Portland OR 97214"
NOTE = "Call the boiler technician back before Thursday re: invoice 2209"
# An ordinary page: several paragraphs with a running header the cleaner removes.
LONG_PAGE = (
    "QUARTERLY MAINTENANCE REPORT          Page 3 of 9\n"
    + "The north wing boiler was serviced on the second visit. The technician replaced the "
    "ignition electrode and recalibrated the pressure relief valve, which had drifted to "
    "a setting above the manufacturer's limit. No leaks were found in the supply lines.\n" * 3
)
# What the live cleaner did to a one-line page: kept the line and wrote ~480 chars more.
EXPANSION = " " + ("This page appears to contain a single line of text from a scanned document. " * 6)

THRESHOLD = 300


def _runner(monkeypatch, calls: list[str]) -> None:
    class _Runner:
        async def clean_page(self, raw: str, *, timeout: float | None = None) -> dict[str, Any]:
            calls.append(raw)
            if len(raw) < 200:  # the live behaviour on a one-line page
                return {"text": raw + EXPANSION, "section_kind": "receipt"}
            # An honest cleanup of a long page: running header dropped.
            body = raw.split("\n", 1)[1]
            return {"text": body.strip(), "section_kind": "maintenance_report"}

    monkeypatch.setattr(llm_mod, "_require_runner", lambda: _Runner())
    monkeypatch.setattr(llm_mod, "vcprint", lambda *a, **kw: None)

    async def _record_error(exc: BaseException, **kw: Any) -> None:
        return None

    monkeypatch.setattr(matrx_orm, "record_error", _record_error)


def _threshold(monkeypatch, value: int | None) -> None:
    if value is None:
        monkeypatch.delitem(ext_mod._registry, "clean_min_page_chars", raising=False)
        return

    async def _min_chars() -> int:
        return value

    monkeypatch.setitem(ext_mod._registry, "clean_min_page_chars", _min_chars)


class _Rows:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self._rows = rows

    def filter(self, **_kw: Any) -> _Rows:
        return self

    def order_by(self, *_a: Any) -> _Rows:
        return self

    async def values(self, *_cols: str) -> list[dict[str, Any]]:
        return [dict(r) for r in self._rows]


def _wire_run_clean(
    monkeypatch, texts: list[str], page_writes: dict[int, dict[str, Any]], doc_writes: list[str]
) -> None:
    from matrx_rag.pdf_pipeline import _ExtractedPage

    async def _load_pages(_pid: str):
        return [
            _ExtractedPage(page_index=i, text=t, used_ocr=False, char_count=len(t))
            for i, t in enumerate(texts)
        ]

    class _Writer:
        async def update_clean_content(self, doc_id, clean_content, owner_id):
            doc_writes.append(clean_content)

        async def update_page_cleanup(self, **kw: Any) -> None:
            page_writes[kw["page_index"]] = kw

    # The retry-processing case: the failed run persisted nothing for these pages.
    rows = [{"page_index": i, "cleaned_text": "", "section_kind": None} for i in range(len(texts))]
    monkeypatch.setattr(stages, "_load_pages", _load_pages)
    monkeypatch.setattr(stages, "get_db_model", lambda _name: _Rows(rows))
    monkeypatch.setattr(stages, "get_document_writer", lambda: _Writer())


def _run_clean() -> Any:
    return asyncio.run(stages.run_clean(processed_document_id="d" * 36, owner_id="u" * 36))


def test_scan_of_one_line_pages_completes_with_every_page_holding_its_line(monkeypatch):
    calls: list[str] = []
    _runner(monkeypatch, calls)
    _threshold(monkeypatch, THRESHOLD)
    page_writes: dict[int, dict[str, Any]] = {}
    doc_writes: list[str] = []
    _wire_run_clean(monkeypatch, [RECEIPT, LABEL, NOTE], page_writes, doc_writes)

    _run_clean()

    assert calls == [], "a one-line page must never reach the cleaner"
    for i, line in enumerate([RECEIPT, LABEL, NOTE]):
        written = page_writes[i]
        assert written["cleaned_text"] == line
        assert written["section_kind"] == SHORT_PAGE_KIND
        # A retry reads the page as written and never re-pays it.
        assert page_is_cleaned(written["cleaned_text"], written["section_kind"])
    assert doc_writes == [f"{RECEIPT}\n\n{LABEL}\n\n{NOTE}"]


def test_mixed_scan_cleans_the_long_page_and_keeps_the_short_one(monkeypatch):
    calls: list[str] = []
    _runner(monkeypatch, calls)
    _threshold(monkeypatch, THRESHOLD)
    page_writes: dict[int, dict[str, Any]] = {}
    doc_writes: list[str] = []
    _wire_run_clean(monkeypatch, [LONG_PAGE, NOTE], page_writes, doc_writes)

    _run_clean()

    assert calls == [LONG_PAGE], "the ordinary page is cleaned exactly as before"
    assert "Page 3 of 9" not in page_writes[0]["cleaned_text"]
    assert page_writes[0]["cleaned_text"].startswith("The north wing boiler")
    assert page_writes[0]["section_kind"] == "maintenance_report"
    assert page_writes[1]["cleaned_text"] == NOTE
    assert page_writes[1]["section_kind"] == SHORT_PAGE_KIND


def test_page_at_the_threshold_is_still_cleaned(monkeypatch):
    calls: list[str] = []
    _runner(monkeypatch, calls)
    _threshold(monkeypatch, len(NOTE))  # NOTE is exactly at the threshold, not under it
    page_writes: dict[int, dict[str, Any]] = {}
    _wire_run_clean(monkeypatch, [NOTE], page_writes, [])

    # The cleaner is asked (the threshold does not leak) and expands it; the guard refuses that, and
    # since the page is under the guard's absolute floor (TINY_PAGE_FLOOR_CHARS, 2026-11-18) it keeps
    # its own text instead of failing the document.
    _run_clean()
    assert calls == [NOTE]
    assert page_writes[0]["cleaned_text"] == NOTE
    assert page_writes[0]["section_kind"] == SHORT_PAGE_KIND


def test_a_long_page_the_guard_refuses_keeps_its_own_text_marked_rejected(monkeypatch):
    class _Ballooning:
        async def clean_page(self, raw: str, *, timeout: float | None = None) -> dict[str, Any]:
            return {"text": raw * 3, "section_kind": "maintenance_report"}

    _runner(monkeypatch, [])
    monkeypatch.setattr(llm_mod, "_require_runner", lambda: _Ballooning())
    _threshold(monkeypatch, THRESHOLD)
    page_writes: dict[int, dict[str, Any]] = {}
    doc_writes: list[str] = []
    _wire_run_clean(monkeypatch, [LONG_PAGE], page_writes, doc_writes)

    _run_clean()
    assert page_writes[0]["cleaned_text"] == LONG_PAGE.strip()
    assert page_writes[0]["section_kind"] == llm_mod.CLEAN_REJECTED_KIND
    assert doc_writes == [LONG_PAGE.strip()]


def test_without_a_host_threshold_every_page_goes_to_the_cleaner(monkeypatch):
    calls: list[str] = []
    _runner(monkeypatch, calls)
    _threshold(monkeypatch, None)
    page_writes: dict[int, dict[str, Any]] = {}
    _wire_run_clean(monkeypatch, [RECEIPT, LABEL], page_writes, [])

    _run_clean()  # both ballooned answers are refused; both pages are under the guard's floor, so kept
    assert sorted(calls) == sorted([RECEIPT, LABEL])
    assert {w["section_kind"] for w in page_writes.values()} == {SHORT_PAGE_KIND}
