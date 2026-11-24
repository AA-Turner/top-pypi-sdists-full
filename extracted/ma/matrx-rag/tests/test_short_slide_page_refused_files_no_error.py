"""A short slide/worksheet page whose cleaner answer the guard refuses keeps its own text and files
NO system error — the same rule as a tiny page, for the whole short-page class.

Live 2026-11-20 (rag_page_clean_kept_raw x6, doc b56d1bab…, a chemistry slide deck): pages of
217-270 chars — an exit ticket of three questions, a copyright-stamped section title, a blank
redox worksheet — were refused by the output guard (the cleaner ANSWERED the questions, 571-1542
chars; or dropped the copyright stamp leaving 28-37 chars, judged "content lost"; or returned
nothing). Each page rightly kept its own text, but because it sat just over the old 200-char tiny
floor every one filed a system error. A page that short has nothing a cleaner could improve: its
own text IS its clean text. Pre-fix: each case files one ``rag_page_clean_kept_raw`` row.
"""

from __future__ import annotations

import asyncio

import matrx_orm
import pytest

import matrx_rag._ext as ext_mod
import matrx_rag.llm as llm_mod
from matrx_rag.llm import SHORT_PAGE_KIND, clean_incomplete_error, clean_pdf_pages, page_kept_on_rejection

EXIT_TICKET = (
    "Final exit ticket\n"
    "1. Write a net ionic equation for AgNO\u2083(aq) + NaCl(aq).\n"
    "2. Explain why HF stays intact in an ionic equation.\n"
    "3. For Zn + Cu\u00b2\u207a \u2192 Zn\u00b2\u207a + Cu, identify both agents.\n"
    "4. Name one idea you can explain and one you still need to practice.\n"
    "68\n"
)
STAMPED_TITLE = (
    "Masterton/Hurley, Chemistry: Principles and Reactions, 8th Edition. \u00a9 2016 Cengage. All Rights Reserved. \n"
    "May not be scanned, copied or duplicated, or posted to a publicly accessible website, in whole or in part.\n"
    "Flow Chart for Solution \nStoichiometry\n"
)
WORKSHEET = (
    "Which reactions are redox?\nReaction\nRedox?\nReason\n"
    "Mg + 2H\u207a \u2192 Mg\u00b2\u207a + H\u2082\n_____\n_____\nAg\u207a + Cl\u207b \u2192 AgCl\n_____\n_____\n"
    "H\u207a + OH\u207b \u2192 H\u2082O\n_____\n_____\nZn + Cu\u00b2\u207a \u2192 Zn\u00b2\u207a + Cu\n_____\n_____\n"
    "Use oxidation number changes rather than the reaction pattern alone.\n63\n"
)
ANSWERS = "1. AgNO3 + NaCl gives Ag+ + Cl- -> AgCl(s), with Na+ and NO3- as spectators. " * 7

# (raw page, what the live cleaner answered)
LIVE = {
    "answered_questions": (EXIT_TICKET, ANSWERS),
    "dropped_copyright_stamp": (STAMPED_TITLE, "Flow Chart for Solution Stoichiometry"),
    "emptied_worksheet": (WORKSHEET, ""),
}


class _LiveRunner:
    async def clean_page(self, raw: str, *, timeout: float | None = None):
        for page, answer in LIVE.values():
            if raw == page:
                return {"text": answer, "section_kind": ""}
        raise AssertionError("unexpected page")


@pytest.mark.parametrize("case", sorted(LIVE))
def test_the_guard_refuses_and_the_page_keeps_its_text_without_a_reason(case):
    raw, answer = LIVE[case]
    assert len(raw.strip()) > 200  # over the old floor: the live pages filed an error
    rejection = llm_mod.cleaned_output_rejection(raw, answer, "")
    assert rejection is not None  # the guard is right to refuse
    page = page_kept_on_rejection(raw, rejection)
    assert page.text == raw.strip() and page.section_kind == SHORT_PAGE_KIND
    assert not page.kept_raw_reason  # nothing to file (the batch lane files only on a reason)


def test_a_short_slide_deck_files_no_system_error(monkeypatch):
    async def _zero() -> int:
        return 0

    monkeypatch.setitem(ext_mod._registry, "clean_min_page_chars", _zero)
    monkeypatch.setattr(llm_mod, "_require_runner", lambda: _LiveRunner())
    filed: list[str] = []

    async def _record(exc, **kw):
        filed.append(kw.get("kind"))

    monkeypatch.setattr(matrx_orm, "record_error", _record)
    raws = [raw for raw, _ in LIVE.values()]
    pages = asyncio.run(clean_pdf_pages(raws))
    assert [p.text for p in pages] == [r.strip() for r in raws]
    assert all(not p.degraded and p.section_kind == SHORT_PAGE_KIND for p in pages)
    assert clean_incomplete_error(pages) is None
    assert filed == []


def test_a_real_page_the_guard_refuses_still_files_its_reason():
    raw = "The landlord proposed a three percent increase effective at the start of the next term.\n" * 6
    rejection = llm_mod.cleaned_output_rejection(raw, raw * 3, "memo")
    assert rejection is not None
    page = page_kept_on_rejection(raw, rejection)
    assert page.section_kind == llm_mod.CLEAN_REJECTED_KIND and page.kept_raw_reason == rejection
