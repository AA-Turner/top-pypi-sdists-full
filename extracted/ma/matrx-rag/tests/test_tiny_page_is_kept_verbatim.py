"""A near-empty page (header, page number) is kept verbatim, never sent to the cleaner.

Live 2026-11-16: 57-99 char pages made the model write 460-660 chars ABOUT the
page; the growth guard refused it and the whole document's clean failed
(PageCleanIncompleteError). Pre-fix this test fails: the runner is called and
the page comes back degraded.
"""

from __future__ import annotations

import asyncio

import matrx_rag._ext as ext_mod
import matrx_rag.llm as llm_mod
from matrx_rag.llm import SHORT_PAGE_KIND, clean_incomplete_error, clean_pdf_pages


def _host_threshold(monkeypatch, value: int) -> None:
    async def _min_chars() -> int:
        return value

    monkeypatch.setitem(ext_mod._registry, "clean_min_page_chars", _min_chars)

TINY = "Acme Holdings - Confidential\n\nPage 3 of 41"


class _ChattyRunner:
    calls = 0

    async def clean_page(self, raw: str, *, timeout: float | None = None):
        type(self).calls += 1
        return {"text": "This page contains only a header and page number. " * 12, "section_kind": "letter"}


def test_tiny_page_is_kept_verbatim_without_calling_the_cleaner(monkeypatch):
    _host_threshold(monkeypatch, 120)
    monkeypatch.setattr(llm_mod, "_require_runner", lambda: _ChattyRunner())
    pages = asyncio.run(clean_pdf_pages([TINY]))
    assert _ChattyRunner.calls == 0
    assert not pages[0].degraded and pages[0].text == TINY
    assert pages[0].section_kind == SHORT_PAGE_KIND
    assert clean_incomplete_error(pages) is None


def test_degraded_error_names_the_guard_when_the_guard_rejected():
    from matrx_rag.llm import PageCleanDegradedError

    reason = "cleaner output is 559 chars for 130 raw chars (more than 1.3x) — not a cleanup"
    msg = str(PageCleanDegradedError(1, 1, all_failed=True, guard_rejected=True, reasons=[reason]))
    assert "never reached a provider" not in msg
    assert "output guard" in msg and "1.3x" in msg


def test_degraded_error_never_claims_no_provider_without_evidence():
    from matrx_rag.llm import PageCleanDegradedError

    msg = str(PageCleanDegradedError(2, 2, all_failed=True, reasons=["provider 529 overloaded"]))
    assert "never reached a provider" not in msg and "529" in msg


def test_the_one_short_page_rule_is_shared():
    from matrx_rag.llm import short_page_verbatim

    assert short_page_verbatim(TINY, 120).text == TINY
    assert short_page_verbatim("   ", 120) is None
    assert short_page_verbatim("x" * 120, 120) is None
    assert short_page_verbatim(TINY, 0) is None  # no host threshold = standalone = clean every page
