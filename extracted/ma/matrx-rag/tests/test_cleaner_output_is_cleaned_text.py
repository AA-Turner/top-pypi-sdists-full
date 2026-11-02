"""A cleaner answer that is not cleaned text of its page is a FAILED page.

Live 2026-10-16 (doc f5c5674a…, 3 pages, 4,661 cleaned chars): the PDF tool's
manual clean ran an audit-style agent whose answer opened
"### 1. Raw Extraction Pass (Verbatim Audit)" + a confidence tag + a ```text
fence, ran to 15-17k chars, and overwrote the good cleaned text. Every cleaner
output now passes ``cleaned_output_rejection`` before it may be written; a
rejected page is degraded (never persisted as cleaned) with the reason.

Forcing function: pre-fix there is no ``cleaned_output_rejection`` and
``clean_pdf_text`` returns the junk as a cleaned page (every leg fails).
"""

from __future__ import annotations

import asyncio

import matrx_rag.llm as llm_mod
from matrx_rag.llm import clean_pdf_pages, cleaned_output_rejection

RAW_PAGE = (
    "Pg 1 ln 1 Cmvam700i: Gross margin review for the third quarter.\n"
    "The regional team reported steady volume and lower freight costs, with\n"
    "returns down two points against plan. Pricing held across the portfolio,\n"
    "and the new distributor in Tucson ramped faster than forecast. Inventory\n"
    "turns improved to 6.1 and receivables aged under 45 days rose to 88%.\n"
    "Next steps: confirm the Q4 promotion calendar and finalize vendor terms.\n"
) * 4

GOOD_CLEAN = (
    "Gross margin review for the third quarter.\n\n"
    "The regional team reported steady volume and lower freight costs, with returns "
    "down two points against plan. Pricing held across the portfolio, and the new "
    "distributor in Tucson ramped faster than forecast. Inventory turns improved to "
    "6.1 and receivables aged under 45 days rose to 88%.\n\n"
    "Next steps: confirm the Q4 promotion calendar and finalize vendor terms."
) * 2

# The exact opening of the live junk, then the dump it carried.
LIVE_JUNK = (
    "### 1. Raw Extraction Pass (Verbatim Audit)\n\n"
    "`[CONFIDENCE: DIRECTLY-EXTRACTED]`\n\n"
    "```text\n[Page 1]\n" + RAW_PAGE + "```\n\n"
    "### 2. Cleaning Log\n- Stripped repeated header 'Pg 1 ln 1'\n\n"
    "### 3. Cleaned Output\n" + GOOD_CLEAN
)


def test_good_cleaned_text_is_accepted():
    assert cleaned_output_rejection(RAW_PAGE, GOOD_CLEAN, "business_memo") is None


def test_the_exact_live_audit_log_is_rejected():
    reason = cleaned_output_rejection(RAW_PAGE, LIVE_JUNK, "business_memo")
    assert reason is not None and "not cleaned text" in reason


def test_each_junk_shape_is_rejected_on_its_own():
    body = GOOD_CLEAN[:400]
    shapes = {
        "heading": "### 1. Raw Extraction Pass (Verbatim Audit)\n\n" + body,
        "confidence": "`[CONFIDENCE: DIRECTLY-EXTRACTED]`\n\n" + body,
        "reconstructed": body + "\n\n[RECONSTRUCTED] table",
        "page tag": "[Page 1]\n" + body,
        "fence": "```text\n" + body + "\n```",
    }
    for name, out in shapes.items():
        assert cleaned_output_rejection(RAW_PAGE, out, "business_memo"), name


def test_markers_already_in_the_raw_text_are_kept_verbatim():
    raw = "```python\nprint('hi')\n```\nSee [CONFIDENCE: HIGH] in the appendix. " * 6
    assert cleaned_output_rejection(raw, raw.strip(), "api_documentation") is None


def test_ballooned_and_gutted_outputs_are_rejected():
    assert "more than" in (cleaned_output_rejection(RAW_PAGE, GOOD_CLEAN * 4, "memo") or "")
    assert "less than" in (cleaned_output_rejection(RAW_PAGE, "Gross margin.", "memo") or "")
    assert cleaned_output_rejection(RAW_PAGE, "", "business_memo")  # empty, legible kind


def test_illegible_blank_and_tiny_pages_may_clean_to_little():
    assert cleaned_output_rejection(RAW_PAGE, "", "illegible_scan") is None
    assert cleaned_output_rejection(RAW_PAGE, "", "blank_page") is None
    assert cleaned_output_rejection("Page 3", "", "letter") is None
    assert cleaned_output_rejection("Signed, J. Ortega", "Signed, J. Ortega.", "letter") is None


def test_rejected_output_is_a_failed_page_never_persisted(monkeypatch):
    """The live lane: the junk answer becomes a degraded page with the reason,
    ``persist_one`` never sees it, and the good answer still persists."""

    class _Runner:
        async def clean_page(self, raw: str, *, timeout: float | None = None):
            if raw.startswith("JUNK"):
                return {"text": LIVE_JUNK, "section_kind": "business_memo"}
            return {"text": GOOD_CLEAN, "section_kind": "business_memo"}

    monkeypatch.setattr(llm_mod, "_require_runner", lambda: _Runner())
    persisted: list[int] = []

    async def _persist(idx: int, _page) -> None:
        persisted.append(idx)

    pages = asyncio.run(
        clean_pdf_pages(["JUNK " + RAW_PAGE, RAW_PAGE], persist_one=_persist)
    )
    assert persisted == [1]
    assert pages[0].degraded and "not cleaned text" in pages[0].failure_reason
    assert pages[0].text.startswith("JUNK ")  # raw text in memory, never the junk
    assert not pages[1].degraded and pages[1].text == GOOD_CLEAN.strip()
    err = llm_mod.clean_incomplete_error(pages)
    assert err is not None and "not cleaned text" in str(err)
