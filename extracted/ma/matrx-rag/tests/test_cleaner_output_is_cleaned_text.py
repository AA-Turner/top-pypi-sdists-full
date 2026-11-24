"""A cleaner answer that is not cleaned text of its page is a FAILED page.

Live 2026-10-16 (doc f5c5674a…, 3 pages, 4,661 cleaned chars): the PDF tool's
manual clean ran an audit-style agent whose answer opened
"### 1. Raw Extraction Pass (Verbatim Audit)" + a confidence tag + a ```text
fence, ran to 15-17k chars, and overwrote the good cleaned text. Every cleaner
output now passes ``cleaned_output_rejection`` before it may be written; the
junk is never written. Since 2026-11-18 the refused page keeps its OWN text as its
clean text (``CLEAN_REJECTED_KIND``) and the reason is filed — it no longer leaves
the document without clean text (``test_every_page_has_clean_text.py``).

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


def test_rejected_output_is_never_written_and_the_page_keeps_its_own_text(monkeypatch):
    """The live lane: the junk answer is never written; the page persists its RAW text marked
    ``clean_rejected_raw`` with the reason, and the good answer still persists as cleaned."""

    class _Runner:
        async def clean_page(self, raw: str, *, timeout: float | None = None):
            if raw.startswith("JUNK"):
                return {"text": LIVE_JUNK, "section_kind": "business_memo"}
            return {"text": GOOD_CLEAN, "section_kind": "business_memo"}

    monkeypatch.setattr(llm_mod, "_require_runner", lambda: _Runner())
    filed: list[str] = []

    async def _record_error(exc, **kw) -> None:
        filed.append(kw.get("kind"))

    import matrx_orm

    monkeypatch.setattr(matrx_orm, "record_error", _record_error)
    persisted: dict[int, object] = {}

    async def _persist(idx: int, page) -> None:
        persisted[idx] = page

    pages = asyncio.run(
        clean_pdf_pages(["JUNK " + RAW_PAGE, RAW_PAGE], persist_one=_persist)
    )
    assert sorted(persisted) == [0, 1]
    assert pages[0].section_kind == llm_mod.CLEAN_REJECTED_KIND and not pages[0].degraded
    assert "not cleaned text" in pages[0].kept_raw_reason
    assert pages[0].text == ("JUNK " + RAW_PAGE).strip()  # its own text, never the junk
    assert LIVE_JUNK.strip()[:40] not in persisted[0].text
    assert not pages[1].degraded and pages[1].text == GOOD_CLEAN.strip()
    assert llm_mod.clean_incomplete_error(pages) is None
    assert filed == ["rag_page_clean_kept_raw"]


def test_a_screenshot_ocr_dominated_by_interface_noise_may_clean_to_its_few_real_words():
    """Live 2026-11-18: 1463 raw chars of a screen photo (menus, icons, OCR noise) cleaned to 255 chars was judged
    "content lost". The shrink check measures the words a cleaner should keep, not raw length."""
    noise = "Q &€ WBo oO ¢: ~ (EK) = + Gq x [4 > 9 (§ S& 8 @® 23) | : ; ' ` ´ ^ ¨ ¬ ¦ ° ± ² ³ µ ¶ ·\n" * 14
    words = "Please clean my inbox of promos, social updates and receipts every few hours.\n" * 2
    raw = noise + words
    out = "Please clean my inbox of promos, social updates and receipts every few hours." * 2
    assert len(out) < len(raw) * 0.2  # the old guard rejected exactly this
    assert cleaned_output_rejection(raw, out, "") is None


def test_a_prose_page_emptied_to_a_stub_is_still_rejected():
    prose = ("The committee reviewed the quarterly margin report and agreed that the gross margin trend "
             "warrants a closer look at supplier pricing before the next board meeting.\n") * 12
    assert "less than" in (cleaned_output_rejection(prose, "Margin.", "memo") or "")


# The live page of 2026-11-18 (doc 78629ca1, an app screenshot read by OCR), names neutralized. A sidebar of one-word
# labels is interleaved with two columns of real text; the old word-count signal (1537 chars) still judged a faithful
# 251-char cleanup "content lost".
_LIVE_SCREENSHOT_OCR = (
    "ce Premier... ~ (EK) ¢: GE > Workflows ~ > Schedules ~ > Daily Check emails ~ > View ~ = + Q &€ ,e ~ QO\n"
    "Q Search Gq New chat ~ Dds x\n+ New Ge\nJ Agents\nRepeat ,\ns? AGENT P [4 Edit\n&5 Workflows Every\n22\n"
    "[=] Mandates Agiani S& ce7cs —shhours\ndo Shapes Next run Last fired\nves HGR : <> PROMPT 3 months 3 months\n"
    "; ago age Matrx Chat 4\n~ Hide prompt (812 chars) reser &\nWorkflows { See O\n_ \"every seconds\": 7\n"
    "‘= All Workflows Please go to my }\n. gmail account and Summary Input Output Full JSON Execution Core Overv\n"
    "© Workflow Studio G help me get it pea\n‘A- Workflow Runs cleaned up. I Fields on every Agent Shared from an "
    "organization you're not in\nhave almost 3,800\n& Waiting on You unread emails so = Linked +\nour goal is to go\n"
    "FJ Review in there Nothing linked yet\nconsistently and\nne F DESCRIPTION\n\\~ Analyze Runs just chop away at\n"
    "Sf Workflow Battle + An advanced, highly configurable Al assistant capable of\n©) Orchestras Here are the "
    "leveraging web search to provide timely, accurate, and context-\nEypes of emails I aware responses tailored to "
    "specific tone, length, and depth\ndon't need: ;\nAutomations - Promos, social, requirements.\n= receipts, updates\n"
    "Schedules He SYSTEM PROMPT\nf EXECUTION You are Matrx, an advanced Al assistant developed through a\n"
    "collaboration between Google and Al Matrx. You are designed to\nSurfaces provide accurate, helpful, and "
    "professional assistance across a wide\nrange of topics and questions.\nauto\nRuns # Core Capabilities...\n"
    "Auth made immediately @ Gemini 3.8 Flash\nh\neee VARIABLES (6)\ndue,\ntone response_length wuse_emojis "
    "follow_up_questions\nMax runtime 6005 farmatting eftwlea  eavelanstian laval\n~ 2 E\nMax concurrent 1 0\n"
    "© RUN HISTORY 1 (Oo\n[ Success ] 1 day ago\n¥ ae | macver ) conversation @\nscheduling.agent_task....\n"
    "Fields on every Scheduled Task in\nx None yet Add field\nSample Org\n< Linked “+\n> Cloud\nCo All windows >\n"
    "i Settings > + Reply G\n@ Sample User > & 7 errors @ @\n@® PCM &G& A General Chat Sa Text Auto\n"
)


def test_the_live_app_screenshot_may_clean_to_its_running_text():
    out = (
        "Daily Check emails. Please go to my gmail account and help me get it cleaned up. I have almost 3,800 "
        "unread emails so our goal is to go in there consistently and just chop away at it. Types of emails I "
        "don't need: promos, social, receipts, updates."
    )
    assert len(out) <= 251 and len(_LIVE_SCREENSHOT_OCR.strip()) > 1900
    assert cleaned_output_rejection(_LIVE_SCREENSHOT_OCR, out, "screenshot") is None
    # A cleaner that keeps only a heading is still caught on the same page.
    assert "less than" in (cleaned_output_rejection(_LIVE_SCREENSHOT_OCR, "Daily Check emails.", "screenshot") or "")
