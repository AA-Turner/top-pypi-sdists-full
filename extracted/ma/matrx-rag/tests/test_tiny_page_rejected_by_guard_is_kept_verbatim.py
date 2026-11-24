"""A tiny page whose cleaner answer the output guard refuses keeps its own text, never fails.

Live 2026-11-18 (rag_page_clean_degraded x3): a 44-char page came back 463 chars, the growth check
refused it (more than 1.3x) and the document stayed degraded on every retry, because the host's
short-page threshold (knowledge.page_clean_min_chars) is seeded 0. A ratio means nothing on a few
dozen chars, so the guard has an absolute floor. Pre-fix: the page comes back degraded.
"""

from __future__ import annotations

import asyncio

import matrx_rag._ext as ext_mod
import matrx_rag.llm as llm_mod
from matrx_rag.llm import SHORT_PAGE_KIND, clean_incomplete_error, clean_pdf_pages, tiny_page_kept_on_rejection

TINY = "Quarterly Report\nPrepared for the Board 2026"  # 44 chars, as live


class _ChattyRunner:
    async def clean_page(self, raw: str, *, timeout: float | None = None):
        return {"text": "This page is a title page that names the report and its audience. " * 7, "section_kind": "cover"}


def _threshold_off(monkeypatch) -> None:
    async def _zero() -> int:
        return 0

    monkeypatch.setitem(ext_mod._registry, "clean_min_page_chars", _zero)


def test_a_tiny_page_the_guard_refuses_is_kept_verbatim(monkeypatch):
    _threshold_off(monkeypatch)
    monkeypatch.setattr(llm_mod, "_require_runner", lambda: _ChattyRunner())
    pages = asyncio.run(clean_pdf_pages([TINY]))
    assert not pages[0].degraded and pages[0].text == TINY.strip()
    assert pages[0].section_kind == SHORT_PAGE_KIND
    assert clean_incomplete_error(pages) is None


def test_a_long_page_the_guard_refuses_still_fails():
    long_raw = "Running text of a real page. " * 20
    assert len(long_raw.strip()) >= llm_mod.TINY_PAGE_FLOOR_CHARS
    assert tiny_page_kept_on_rejection(long_raw) is None
    assert tiny_page_kept_on_rejection(TINY).text == TINY.strip()


def test_a_tiny_page_kept_verbatim_files_no_system_error(monkeypatch):
    """Live 2026-11-18 (rag_page_clean_kept_raw x2): a 44-char page kept on its own text is the
    right answer, not an error. Pre-fix: one record_error row of that kind per run."""
    import matrx_orm

    _threshold_off(monkeypatch)
    monkeypatch.setattr(llm_mod, "_require_runner", lambda: _ChattyRunner())
    filed: list[str] = []

    async def _record(exc, **kw):
        filed.append(kw.get("kind"))

    monkeypatch.setattr(matrx_orm, "record_error", _record)
    pages = asyncio.run(clean_pdf_pages([TINY]))
    assert pages[0].text == TINY.strip() and not pages[0].kept_raw_reason
    assert "rag_page_clean_kept_raw" not in filed
