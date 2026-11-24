"""Async LLM helpers used by the RAG pipeline.

Four jobs:

* ``clean_pdf_text`` / ``clean_pdf_pages`` — denoise + rewrap + classify a
  single page of raw PDF / OCR text. Drops layout artifacts, joins broken
  lines, removes headers / footers / page numbers. Always on, high volume
  (1 call/page). Output is a JSON object molded into :class:`CleanedPage`.
* ``contextualize_chunk`` — the 1-2 sentence "where does this sit in the
  document" prefix for Anthropic-style contextual retrieval. Off by default.
* ``expand_query`` — rewrite a search query into 2-3 paraphrases (multi-query
  retrieval). Off by default.
* ``hyde_passage`` — write a hypothetical ideal-answer passage as a HyDE
  retrieval target. Off by default.

ONE execution path: the host's agent system. Each job runs through a pinned
``agx_agent`` on matrx-ai's UnifiedAIClient (injected by the host via
``configure(rag_agent_runner=...)``), so every call gets cost/usage
attribution, version pinning, and admin-editable prompts. The runner returns
the post-parse value; ALL shared assembly (CleanedPage normalization, query
dedup/cap, document truncation) stays HERE so it lives in exactly one place.
The model is read off the pinned ``agx_agent`` row — there is no per-call
``model`` kwarg and no ``RAG_*_MODEL`` env var anymore.

There is NO raw-provider fallback. matrx-rag is an internal Matrx package: it
ALWAYS runs inside a host that wires the agent runner (the platform's reason
for existing is AI). If no runner is injected, ``_require_runner()`` raises
loudly at the first call rather than silently degrading. (The prompt
constants below remain the single source of truth the host imports to define
those four agents.)

When a runner call FAILS (provider outage after the agent's own retries),
each job applies a loud fallback (raw text for the cleaner, empty string for
the others) so an incomplete result is never silent. A MISSING runner is a
host-config error and raises; a FAILED call degrades gracefully.
"""

from __future__ import annotations

import asyncio
import logging
import re
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from collections.abc import Mapping
from typing import Any

# get_rag_agent_runner() returns the host-injected agent-backed runner. It
# reads the live registry on every call, so a runner injected AFTER import is
# still seen. _require_runner() turns "no runner" into a loud raise — the four
# jobs below run EXCLUSIVELY through the host's agx agent system.
from matrx_utils import vcprint

from matrx_rag._ext import (
    RagAgentRunner,
    get_clean_min_page_chars,
    get_context_window_chars,
    get_rag_agent_runner,
)
from matrx_rag.text_hygiene import strip_control_chars
from matrx_utils.splitting import count_tokens, split_text

logger = logging.getLogger(__name__)


def _require_runner() -> RagAgentRunner:
    """Return the host-injected agent runner, or raise loudly if absent.

    matrx-rag's LLM jobs run ONLY through the host's agent system; there is no
    raw-provider fallback. A missing runner means the host forgot to wire it
    (``matrx_rag.configure(rag_agent_runner=...)`` — aidream does this in
    ``package_integration.py``). That's a startup misconfiguration, so we
    surface it immediately instead of silently producing degraded output."""
    runner = get_rag_agent_runner()
    if runner is None:
        raise RuntimeError(
            "matrx_rag.llm requires a RagAgentRunner but none is injected. "
            "The host MUST call matrx_rag.configure(rag_agent_runner=...) at "
            "startup. matrx-rag's LLM jobs (PDF cleanup, contextualize, "
            "query-expand, HyDE) run exclusively through the host's agent "
            "system — there is no raw-provider fallback."
        )
    return runner


# CLEANUP_SYSTEM_PROMPT: the text lives in the stored rag agent (agent.definition) its mandate holds; it is no longer kept in code.


# CONTEXT_SYSTEM_PROMPT_TEMPLATE: the text lives in the stored rag agent (agent.definition) its mandate holds; it is no longer kept in code.


# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------


# Catch-all section_kind values the cleaner prompt forbids. If the model emits
# one anyway, _normalize_cleaned coerces it to "" (honestly unclassified) so a
# fake industry-agnostic bucket never enters the data. NOT a taxonomy — the
# vocabulary is open; this is only the blocklist of meaningless non-answers.
_FORBIDDEN_SECTION_KINDS = frozenset(
    {
        "other",
        "misc",
        "miscellaneous",
        "unknown",
        "unclassified",
        "general",
        "document",
        "n/a",
        "na",
        "none",
        "blank_or_garbage",
    }
)


@dataclass
class CleanedPage:
    """Result of cleaning + classifying one PDF page."""

    text: str
    # Open-vocabulary general document type. Empty string ⇒ genuinely
    # unclassified (a real failure to surface), NEVER the fake bucket "other".
    section_kind: str = ""
    section_subtype: str = ""
    section_title: str = ""
    is_continuation: bool = False
    # True ⇒ the cleaner FAILED and ``text`` is the RAW extraction, not cleaned
    # output. The page still flows downstream (a raw page beats a dropped one),
    # but it is not the quality we billed for, so it must never pass silently —
    # clean_pdf_pages aggregates this into a loud alarm.
    degraded: bool = False
    # WHY the cleaner failed (the exception's own sentence), and whether it was
    # a CALLER REFUSAL (``is_caller_refusal`` — the person's AI usage limit, no
    # credits): a refusal is not transient, so nothing retries it and the
    # stage reports it by name instead of a bare "N pages failed".
    failure_reason: str = ""
    refused: bool = False
    failure: BaseException | None = field(default=None, repr=False, compare=False)
    # The output guard REFUSED the cleaner's answer and the page kept its own text (a written page,
    # never degraded): WHY. ``clean_pdf_pages`` files these as one ``rag_page_clean_kept_raw`` row.
    kept_raw_reason: str = ""
    # True once clean_pdf_pages filed this page's failure to system_error (its one
    # PageCleanDegraded row), so the stage that fails on it does not file it again.
    recorded: bool = field(default=False, compare=False)


class PageCleanDegradedError(RuntimeError):
    """Pages whose cleaner call failed — recorded to ``system_error``, never raised."""

    def __init__(
        self,
        degraded: int,
        attempted: int,
        *,
        all_failed: bool,
        guard_rejected: bool = False,
        reasons: list[str] | None = None,
    ) -> None:
        self.degraded = degraded
        self.attempted = attempted
        self.all_failed = all_failed
        self.guard_rejected = guard_rejected
        why = "; ".join(reasons or [])[:300]
        if guard_rejected:
            # The provider ANSWERED; the output guard refused the answer.
            detail = f" (the cleaner's answer was rejected by the output guard: {why})"
        elif all_failed:
            detail = " (every page" + (f": {why}" if why else "") + ")"
        else:
            detail = ""
        super().__init__(
            f"{degraded}/{attempted} pages failed to clean{detail}"
            "; they were left uncleaned so a re-run retries them"
        )


class PageCleanKeptRawError(RuntimeError):
    """Pages whose cleaner answer the output guard refused; each kept its own text as its clean text
    (``CLEAN_REJECTED_KIND`` / ``SHORT_PAGE_KIND``). Recorded to ``system_error``, never raised."""

    def __init__(self, page_indexes: list[int], reasons: list[str]) -> None:
        self.page_indexes = page_indexes
        self.reasons = reasons
        why = "; ".join(reasons)[:300]
        super().__init__(
            f"{len(page_indexes)} page(s) kept their own text as clean text — the output guard "
            f"refused the cleaner's answer: {why}"
        )


class PageCleanIncompleteError(RuntimeError):
    """The clean stage could not clean every page — RAISED, so nothing claims "cleaned".

    The document-level ``clean_content`` / ``clean_content_completed_at`` are
    written ONLY when every page actually cleaned. Before this, a run whose
    cleaner was refused (the person's AI usage limit) joined the RAW text of
    every page into ``clean_content``, stamped it complete, and reported the
    run done (2026-10-07, docs 74f47689… / 336b6377…).

    ``refused`` mirrors ``is_caller_refusal`` on the underlying exception: a
    usage-limit / no-credit refusal is the person's to fix, never transient, so
    callers must not retry it and the stream must not file it as a crash.
    ``error_info`` is the refusal's own classified error (when it carried one),
    so a stream ending on this exception shows the gate's sentence.
    """

    def __init__(
        self, degraded: int, attempted: int, *, reason: str, refused: bool, already_recorded: bool = False
    ) -> None:
        self.degraded = degraded
        self.attempted = attempted
        self.reason = reason
        self.refused = refused
        self.is_caller_refusal = refused
        # The failure already has its system_error row (clean_pdf_pages' PageCleanDegraded);
        # a host that files failed stages skips this one (2026-11-18: one guard rejection
        # filed twice, as PageCleanDegraded and as PageCleanIncompleteError).
        self.already_recorded = already_recorded
        label = "AI usage limit reached" if refused else "the page cleaner failed"
        super().__init__(
            f"{degraded} of {attempted} pages not cleaned — {label}: "
            f"{reason or 'the cleaner gave no reason'}"
        )


def clean_incomplete_error(
    results: list[CleanedPage], skip_indexes: set[int] | None = None
) -> PageCleanIncompleteError | None:
    """THE ONE verdict on a clean run: ``None`` when every attempted page cleaned,
    else the error that must fail the stage (carrying the first refusal / failure
    as ``__cause__`` so ``usage_refusal_in`` still finds the typed refusal)."""
    skip = skip_indexes or set()
    attempted = [i for i in range(len(results)) if i not in skip]
    degraded = [results[i] for i in attempted if results[i].degraded]
    if not degraded:
        return None
    refusals = [c for c in degraded if c.refused]
    lead = refusals[0] if refusals else degraded[0]
    err = PageCleanIncompleteError(
        len(degraded),
        len(attempted),
        reason=lead.failure_reason,
        refused=bool(refusals),
        already_recorded=any(c.recorded for c in degraded),
    )
    if lead.failure is not None:
        err.__cause__ = lead.failure
        info = getattr(lead.failure, "error_info", None)
        if info is not None and refusals:
            err.error_info = info  # type: ignore[attr-defined]
    return err


def _failure_reason(exc: BaseException) -> str:
    text = str(exc).strip()
    return text or type(exc).__name__


CLEAN_FAILED_KIND = "clean_failed"

#: ``section_kind`` of a page kept VERBATIM by :func:`short_page_verbatim` (no cleaner asked).
#: It names no section: ``pdf_pipeline.chunk_pdf_pages`` treats it as neutral (it joins its
#: neighbours, never forces a parent cut, never wins the dominant-kind vote) and the host never
#: shows it to a person as a page label.
SHORT_PAGE_KIND = "short_page_verbatim"


def short_page_verbatim(raw: str, min_chars: int) -> CleanedPage | None:
    """THE ONE answer to "is this page kept verbatim instead of cleaned?" — shared by the live
    lane (``clean_pdf_text``) and the host's batch lane (submit and result handler), so both treat
    a short page identically. The threshold is the HOST's (``configure(clean_min_page_chars=...)``,
    ``get_clean_min_page_chars``); with none, ``min_chars`` is 0 and every page is cleaned.

    ``None`` when the page goes to the cleaner (``min_chars`` <= 0, a blank page, or a page at or
    over ``min_chars`` characters); else the page, its own text stripped, marked
    :data:`SHORT_PAGE_KIND` — a written page (``page_is_cleaned``), never a degraded one."""
    text = strip_control_chars(raw or "").strip()
    if min_chars <= 0 or not text or len(text) >= min_chars:
        return None
    return CleanedPage(text=text, section_kind=SHORT_PAGE_KIND)


#: Absolute floor under the output guard: a page shorter than this whose cleaner answer the guard
#: REJECTED keeps its own text verbatim (:data:`SHORT_PAGE_KIND`) instead of failing. A ratio is
#: meaningless on a few dozen chars — live 2026-11-18: a 44-char page came back 463 chars (the model
#: wrote ABOUT the page), the growth check rightly refused it, and the document was left degraded on
#: every retry. Such a page has nothing a cleaner could fix, so its raw text IS its cleaned text.
#: Holds whatever the host's ``clean_min_page_chars`` is (live it is seeded 0, so every page is sent).
#: 400, not 200 (live 2026-11-20, rag_page_clean_kept_raw x6 on one slide deck): pages of 217-270
#: chars — an exit ticket of three questions the cleaner ANSWERED, a section title under a copyright
#: stamp the cleaner rightly dropped ("content lost" by ratio), a blank worksheet it emptied — were
#: refused and kept their own text, correctly, but each filed a system error. A heading and a handful
#: of short lines (a slide, a worksheet, a stamped title) is still a page the ratio cannot judge and a
#: cleaner cannot improve; ordinary prose pages run well past 400 and still file their refusal.
TINY_PAGE_FLOOR_CHARS = 400


#: ``section_kind`` of a page whose cleaner answer the output guard REFUSED and which keeps its own
#: (raw) text as its clean text — "not cleaned", written and done, never empty (2026-11-18: a refused
#: page used to be left unwritten and the whole document's clean text was never written, on every
#: retry). Neutral like :data:`SHORT_PAGE_KIND`; chunks built from it are raw-based
#: (:func:`page_text_is_raw`), so a later successful forced clean rebuilds them.
CLEAN_REJECTED_KIND = "clean_rejected_raw"

#: Kinds that name no section: the page's text is its own raw text, kept on purpose.
VERBATIM_KINDS = frozenset({SHORT_PAGE_KIND, CLEAN_REJECTED_KIND})


def page_kept_on_rejection(raw: str, rejection: str) -> CleanedPage:
    """THE ONE answer, on both lanes, to "the guard refused this page's cleaned text": the page keeps
    its own text as its clean text — :data:`SHORT_PAGE_KIND` under :data:`TINY_PAGE_FLOOR_CHARS`,
    else :data:`CLEAN_REJECTED_KIND` — carrying the refusal in ``kept_raw_reason`` so it is recorded.
    Never degraded: a refused answer is deterministic junk, and a retry asks the same cleaner again."""
    tiny = tiny_page_kept_on_rejection(raw)
    if tiny is not None:
        # A near-empty page has nothing to clean: its own text IS the right answer, so this is not
        # a system error (live 2026-11-18: 44-char pages filed rag_page_clean_kept_raw). No reason
        # is carried, so nothing is filed; the refusal is still in the caller's log line.
        return tiny
    page = CleanedPage(text=strip_control_chars(raw or "").strip(), section_kind=CLEAN_REJECTED_KIND)
    page.kept_raw_reason = rejection
    return page


def tiny_page_kept_on_rejection(raw: str) -> CleanedPage | None:
    """THE ONE answer, on both lanes, to "the guard refused this page's cleaned text — keep it
    verbatim or fail it?": a page under :data:`TINY_PAGE_FLOOR_CHARS` is kept verbatim (a written
    page, never degraded); a longer one returns ``None`` and stays a failed page."""
    return short_page_verbatim(raw, TINY_PAGE_FLOOR_CHARS)


class PageCleanProviderStop(RuntimeError):
    """The provider's own content rules stopped the cleaner on this page (a content-safety,
    recitation or refusal stop — expected provider control flow, never a platform fault).

    Raised by the host runner. Asking again sends the same page to the same rules, so the page
    keeps its own text as its clean text (:data:`CLEAN_REJECTED_KIND`, a written page, never
    degraded) and nothing is filed to ``system_error`` (live 2026-11-20: one page stopped by a
    content-safety filter filed ``rag_page_clean_degraded`` on each of three re-runs)."""

    is_expected_provider_stop = True


def page_kept_on_provider_stop(raw: str) -> CleanedPage:
    """THE ONE answer to "the provider stopped the cleaner on this page": the page keeps its own
    text, marked :data:`CLEAN_REJECTED_KIND` (or :data:`SHORT_PAGE_KIND` when tiny), and carries
    no ``kept_raw_reason`` — expected provider control flow is not an incident."""
    tiny = tiny_page_kept_on_rejection(raw)
    if tiny is not None:
        return tiny
    return CleanedPage(text=strip_control_chars(raw or "").strip(), section_kind=CLEAN_REJECTED_KIND)


class CleanedOutputRejected(ValueError):
    """The cleaner answered, but its output is not cleaned text of the page
    (``cleaned_output_rejection`` named why). The page is a FAILED page."""


def page_text_for_downstream(page: Mapping[str, Any]) -> str:
    """THE ONE answer to "what text does chunking / clean_content use for this page?".

    A page the cleaner gave up on is saved ``cleaned_text=""`` with
    ``section_kind='clean_failed'`` (so ``page_is_cleaned`` reads it as done).
    Downstream must not lose its content: it falls back to ``raw_text``. An
    ``illegible_scan`` / blank page is genuinely empty and stays empty.
    ``page`` is any mapping with ``cleaned_text``, ``section_kind``, ``raw_text``.
    """
    if page.get("section_kind") == CLEAN_FAILED_KIND:
        return str(page.get("raw_text") or "")
    if not page_is_cleaned(page.get("cleaned_text"), page.get("section_kind")):
        # Never cleaned (the cleaner was refused or failed, so the page was left
        # unwritten for a retry): its RAW text is the only honest downstream
        # text — chunking a mixed document must not drop these pages to "".
        return str(page.get("raw_text") or "")
    return str(page.get("cleaned_text") or "")


def page_text_is_raw(page: Mapping[str, Any]) -> bool:
    """True when ``page_text_for_downstream(page)`` falls back to the page's RAW text
    (the page was never cleaned, or the cleaner gave up on it). Chunks built from such
    text are marked ``text_basis='raw'`` so a later successful clean rebuilds them."""
    return page.get("section_kind") in (CLEAN_FAILED_KIND, CLEAN_REJECTED_KIND) or not page_is_cleaned(
        page.get("cleaned_text"), page.get("section_kind")
    )


def page_is_cleaned(cleaned_text: str | None, section_kind: str | None) -> bool:
    """THE ONE answer to "has the cleaner already written this page?".

    ``cleaned_text`` is NOT NULL (defaults to ``""``), so its emptiness cannot
    tell "never cleaned" from "cleaned to nothing": the cleaner legitimately
    returns ``""`` for a page it classifies ``illegible_scan`` / ``blank_page`` /
    ``blank_or_garbage``. ``section_kind`` is NULL until the cleaner writes the
    page, so a page is cleaned when either carries the cleaner's mark. Testing
    ``cleaned_text != ""`` alone re-queued every illegible page on every batch
    resume — hundreds of times per document, forever (2026-10-06).
    """
    return section_kind is not None or bool(cleaned_text)


def normalize_cleaned_page(parsed: dict[str, Any]) -> CleanedPage:
    """Mold a parsed cleaner object into a ``CleanedPage``.

    The SINGLE normalization point shared by every path that produces a cleaned
    page — the live agent path here, and the HOST's batch lane, which receives
    the same agent's output hours later through a provider Batch API. All of
    them must produce byte-identical fields (lower-cased section codes, stripped
    text/title, coerced bool) no matter which one produced the dict, or a page
    cleaned cheaply would differ from one cleaned live. Public because the batch
    consumer lives in the host (matrx-rag cannot import matrx-ai/matrx-batch).
    """
    # Defense-in-depth against a disobedient model: the prompt FORBIDS
    # catch-all kinds, but if one slips through we drop it to "" rather than
    # poison the data with a fake bucket. "" honestly means "unclassified".
    kind = str(parsed.get("section_kind") or "").strip().lower()
    if kind in _FORBIDDEN_SECTION_KINDS:
        kind = ""
    return CleanedPage(
        text=strip_control_chars(str(parsed.get("text", ""))).strip(),
        section_kind=kind,
        section_subtype=str(parsed.get("section_subtype") or "").strip().lower(),
        section_title=str(parsed.get("section_title") or "").strip(),
        is_continuation=bool(parsed.get("is_continuation", False)),
    )


# ── Output validation: cleaned text must BE cleaned text of its input ────────
#
# Live 2026-10-16 (doc f5c5674a…): an audit-style cleaner answered a 4.6k-char
# document with 15-17k chars that opened "### 1. Raw Extraction Pass (Verbatim
# Audit)" + "`[CONFIDENCE: DIRECTLY-EXTRACTED]`" + a ```text fence, and that
# audit log overwrote the good cleaned text. Every writer of cleaned page text
# runs THIS check first; a rejected output is a FAILED page (never persisted as
# cleaned, reason recorded), so junk can never replace good text.

#: Cleaned text may legitimately grow a little (Markdown tables, rejoined
#: paragraphs) but never balloon: above this ratio of the raw length it is
#: commentary / a log, not a cleanup. ``_GROWTH_SLACK_CHARS`` keeps tiny pages
#: (a title, a signature line) from tripping the ratio on a few added chars.
MAX_CLEANED_GROWTH = 1.3
_GROWTH_SLACK_CHARS = 200
#: A legible page cleaned below this share of its raw length lost its content.
#: Only judged on pages long enough for the ratio to mean something.
MIN_CLEANED_SHARE = 0.2
_SHRINK_MIN_RAW_CHARS = 200
#: A page's SIGNAL is the text a cleaner is expected to keep: words of three or more letters. OCR of a screenshot or
#: a photo is mostly interface chrome and noise ("Gq", "~ (EK) ¢:", "Q &€ WBo"); a cleaner rightly drops that, so the
#: shrink check measures against the signal, never the raw length (live 2026-11-18: 1463 raw chars of a screenshot,
#: ~700 of signal, cleaned to 255 — a faithful cleanup judged as "content lost"). A prose page the cleaner empties
#: out still has signal ~= raw, so it is rejected exactly as before.
_SIGNAL_WORD = re.compile(r"[^\W\d_]{3,}")
#: Only a line carrying at least this many signal words is running text. A screenshot's sidebar and toolbar are one
#: or two real words a line ("Workflows", "Schedules", "Next run Last fired") — real words, but chrome the cleaner
#: rightly drops (live 2026-11-18 doc 78629ca1: a 1960-char app screenshot, 1537 chars of 3+-letter words, 26 lines of
#: running text, cleaned to 251 chars and judged "content lost"). Prose lines carry ~10 words, so a prose page's
#: signal is unchanged.
_SIGNAL_LINE_MIN_WORDS = 4


def _signal_chars(raw: str) -> int:
    """Characters of ``raw`` carried by words of 3+ letters on lines of running text (each word with its separator)."""
    total = 0
    for line in raw.splitlines():
        words = _SIGNAL_WORD.findall(line)
        if len(words) >= _SIGNAL_LINE_MIN_WORDS:
            total += sum(len(w) + 1 for w in words)
    return total
#: Kinds whose cleaned text is legitimately (near) empty.
_EMPTY_OK_KINDS = frozenset({"illegible_scan", "blank_page", "blank_or_garbage", CLEAN_FAILED_KIND})

# Markers of a response ABOUT the text rather than the text itself. Each only
# counts when the raw input does not already contain it (a document may quote
# a confidence tag or a code fence; the cleaner may keep it verbatim).
_AUDIT_MARKERS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "audit/log heading",
        re.compile(
            r"^\s{0,3}#{1,6}\s*(?:\d+[.)]\s*)?[^\n]*\b(?:raw extraction pass|verbatim audit|"
            r"cleaning (?:audit )?log|audit log|change ?log|removal log|overflow field|"
            r"cleaned output|transformation pass|cleaning pass)\b",
            re.IGNORECASE | re.MULTILINE,
        ),
    ),
    ("confidence tag", re.compile(r"\[\s*CONFIDENCE\s*:", re.IGNORECASE)),
    ("reconstruction tag", re.compile(r"\[\s*RECONSTRUCTED\s*\]", re.IGNORECASE)),
    ("page source tag", re.compile(r"^\s*\[Page \d+\]\s*$", re.IGNORECASE | re.MULTILINE)),
)
_FENCE_WRAPPED = re.compile(r"\A\s*```[^\n]*\n.*\n```\s*\Z", re.DOTALL)


def cleaned_output_rejection(raw: str, cleaned_text: str, section_kind: str = "") -> str | None:
    """THE ONE check that a cleaner's output is cleaned text of ``raw``.

    Returns ``None`` when the output is acceptable, else a short reason naming
    what was wrong (recorded as the page's failure reason). Rejects: audit /
    log headings, confidence or reconstruction tags, page-source tags and a code
    fence wrapping the whole output that the raw text did not contain; output
    longer than ``MAX_CLEANED_GROWTH``× the raw (+ a small slack); and, for a
    legible page, output shorter than ``MIN_CLEANED_SHARE``× the raw."""
    raw_s = (raw or "").strip()
    out = (cleaned_text or "").strip()
    kind = (section_kind or "").strip().lower()
    if not out:
        if kind in _EMPTY_OK_KINDS or len(raw_s) < _SHRINK_MIN_RAW_CHARS:
            return None
        return (
            f"cleaner returned empty text for a {len(raw_s)}-char page "
            f"classified {kind or 'unclassified'!r} (not illegible/blank)"
        )
    for label, pattern in _AUDIT_MARKERS:
        if pattern.search(out) and not pattern.search(raw_s):
            return f"cleaner output is not cleaned text: {label} found"
    if _FENCE_WRAPPED.match(out) and "```" not in raw_s:
        return "cleaner output is not cleaned text: wrapped in a code fence"
    limit = max(len(raw_s) * MAX_CLEANED_GROWTH, len(raw_s) + _GROWTH_SLACK_CHARS)
    if len(out) > limit:
        return (
            f"cleaner output is {len(out)} chars for {len(raw_s)} raw chars "
            f"(more than {MAX_CLEANED_GROWTH}x) — not a cleanup"
        )
    if kind not in _EMPTY_OK_KINDS and len(raw_s) >= _SHRINK_MIN_RAW_CHARS:
        signal = _signal_chars(raw_s)
        if len(out) < signal * MIN_CLEANED_SHARE:
            return (
                f"cleaner output is {len(out)} chars for {len(raw_s)} raw chars "
                f"({signal} of them words) (less than {MIN_CLEANED_SHARE}x) — content lost"
            )
    return None


def _assemble_expansions(query: str, lines: list[str], n: int) -> list[str]:
    """Assemble the final multi-query list from a model's paraphrase lines.

    Shared by both paths: prepend the ORIGINAL query, strip list/bullet
    decoration + quotes, dedup case-insensitively, cap at ``n``. Lives here
    (not in the runner) so the assembly is identical regardless of path.
    """
    out = [query]
    seen = {query.strip().lower()}
    for line in lines:
        s = line.strip().lstrip("-•0123456789. ").strip().strip('"').strip("'")
        if s and s.lower() not in seen:
            out.append(s)
            seen.add(s.lower())
        if len(out) >= n:
            break
    return out


PAGE_CLEAN_MAX_INPUT_TOKENS = 6000
"""A page longer than this is cleaned in parts, never in one call. The cleaned
page comes back inside a JSON envelope and is about as long as the raw page, so
the call needs room for roughly the whole page again; the page-cleaner's model
tops out at 16,384 output tokens, and 6,000 in leaves it more than 2x headroom.
Live 2026-10: a 95,926-token page asked for 22,939 tokens out."""

PAGE_CLEAN_MIN_SPLIT_TOKENS = 400
"""Below this a page is not halved any further: the cut would be smaller than a
sentence-sized piece and the failure is not about length."""

PAGE_CLEAN_MAX_SPLIT_DEPTH = 4
"""A page is halved at most this many times (16 parts), then it fails by name."""


class PageOutputTruncated(RuntimeError):
    """The page cleaner's answer hit the model's output limit. Raised by the host
    runner so ``clean_pdf_text`` can halve the page and clean the parts, instead
    of storing a cut-off page (or a runaway repeat) as the cleaned text."""


def _halves(raw: str) -> list[str]:
    """The page cut in two at the strongest natural break, in order."""
    budget = count_tokens(raw) // 2 + 1
    parts = [p for p in split_text(raw, budget, measure="tokens") if p.strip()]
    return parts


async def _clean_in_parts(
    runner: RagAgentRunner, raw: str, *, wait_s: float, depth: int = 0
) -> dict[str, Any]:
    """Clean ``raw`` in one call when it fits, else clean halves and join them in
    order. The first part names the page (kind, title); later parts only add text.
    A part that fails raises, so the page degrades as a whole - never half-cleaned."""
    tokens = count_tokens(raw)
    too_long = tokens > PAGE_CLEAN_MAX_INPUT_TOKENS
    if not too_long:
        try:
            return await runner.clean_page(raw, timeout=wait_s)
        except PageOutputTruncated:
            if depth >= PAGE_CLEAN_MAX_SPLIT_DEPTH or tokens < PAGE_CLEAN_MIN_SPLIT_TOKENS:
                raise
            logger.warning(
                "rag.llm: page cleaner hit its output limit on a %d-token page; halving (depth %d)",
                tokens,
                depth + 1,
            )
    elif depth >= PAGE_CLEAN_MAX_SPLIT_DEPTH:
        raise PageOutputTruncated(
            f"page of {tokens} tokens is still over {PAGE_CLEAN_MAX_INPUT_TOKENS} after "
            f"{depth} halvings"
        )
    parts = _halves(raw)
    if len(parts) < 2:
        raise PageOutputTruncated(f"page of {tokens} tokens could not be cut into parts")
    done: list[dict[str, Any]] = []
    for part in parts:  # in order, one at a time: the join order is the page order
        done.append(await _clean_in_parts(runner, part, wait_s=wait_s, depth=depth + 1))
    merged = dict(done[0])
    merged["text"] = "\n\n".join(str(d.get("text") or "").strip() for d in done)
    return merged


async def clean_pdf_text(raw: str, *, timeout: float = 60.0, min_chars: int = 0) -> CleanedPage:
    """Run one cleanup + classification pass over a single page through the
    host's page-cleaner agent.

    A page shorter than ``min_chars`` characters is kept verbatim and never
    sent (:func:`short_page_verbatim`). Provider admission is owned centrally
    by the agent runner. A page falls back to its raw text on failure, logged
    loudly so an incomplete page is never silent."""
    raw = strip_control_chars(raw)
    if not raw or not raw.strip():
        return CleanedPage(text="", section_kind="blank_or_garbage")

    short = short_page_verbatim(raw, min_chars)
    if short is not None:
        logger.info(
            "rag.llm.clean_pdf_text: page of %d chars is under %d — kept verbatim, cleaner not called",
            len(raw.strip()),
            min_chars,
        )
        return short

    runner = _require_runner()

    try:
        parsed = await _clean_in_parts(runner, raw, wait_s=timeout)
    except Exception as exc:  # noqa: BLE001
        if getattr(exc, "is_expected_provider_stop", False):
            logger.warning(
                "rag.llm.clean_pdf_text: the provider stopped the cleaner on a %d-char page (%s) — "
                "kept its own text as its clean text",
                len(raw),
                exc,
            )
            return page_kept_on_provider_stop(raw)
        refused = bool(getattr(exc, "is_caller_refusal", False))
        logger.warning(
            "rag.llm.clean_pdf_text: agent %s (%s: %s); returning raw text",
            "REFUSED" if refused else "giving up",
            type(exc).__name__,
            exc,
        )
        return CleanedPage(
            text=raw,
            section_kind="",
            degraded=True,
            failure_reason=_failure_reason(exc),
            refused=refused,
            failure=exc,
        )
    cleaned = normalize_cleaned_page(parsed)
    rejection = cleaned_output_rejection(raw, cleaned.text, cleaned.section_kind)
    if rejection is not None:
        # The page keeps its own text as its clean text, marked, and the reason rides
        # ``kept_raw_reason`` into the run's ``rag_page_clean_kept_raw`` record — never a failed
        # page that leaves the document without clean text forever.
        kept = page_kept_on_rejection(raw, rejection)
        logger.warning(
            "rag.llm.clean_pdf_text: output REJECTED (%s) on a %d-char page — kept its own text (%s)",
            rejection,
            len(kept.text),
            kept.section_kind,
        )
        return kept
    return cleaned


async def clean_pdf_pages(
    pages: list[str],
    *,
    concurrency: int = 8,
    on_progress: Callable[[int, int], Awaitable[None]] | None = None,
    persist_one: Callable[[int, CleanedPage], Awaitable[None]] | None = None,
    skip_indexes: set[int] | None = None,
    error_context: dict[str, Any] | None = None,
    before_page: Callable[[int], Awaitable[None]] | None = None,
) -> list[CleanedPage]:
    """Apply ``clean_pdf_text`` to every page in parallel.

    ``before_page(page_index)`` is awaited right before each page's cleaner call
    (the spend). It is the fence: when it raises (e.g. the document's clean hold
    was lost), that page is NOT cleaned and the exception fails the run — it is
    never turned into a degraded page.

    ``concurrency`` bounds how many pages are IN FLIGHT at once (minimum 1).
    The matrx-ai provider admission gate paces the provider call, but each page
    also does its own database work around that call (request rows, error
    capture, ``persist_one``) BEFORE reaching that gate. Unbounded, a 300-page
    PDF opened 300 page tasks at once and they drained the process's 10-slot
    database pool: 3,900 of the pool-saturation holders recorded 2026-10-27 to
    2026-11-03 sat in this function (system_error kind
    ``database_pool_saturation``).

    ``on_progress(done, total)`` fires after every page so the caller can
    emit live progress events to the UI.

    ``persist_one(page_index, cleaned)`` is the CRITICAL durability hook.
    If provided, it is awaited the moment each individual page's cleanup
    finishes — BEFORE the rest of the batch completes. This is the
    difference between "lose all the LLM work if the run dies at 50%"
    and "every cleaned page is on disk the moment it's ready."

    ``skip_indexes`` is a set of page indexes (0-based) to SKIP — pages
    that have already been cleaned in a previous run. Used for resume:
    on retry, the caller looks up which pages already have cleaned_text
    in the DB and passes those indexes here so we don't re-pay the LLM
    bill for them.

    Failures fall back to a CleanedPage holding the raw text + an empty
    section_kind ("" = unclassified) rather than dropping the page entirely.
    That degraded page is returned (so this run's downstream still has text)
    but NOT handed to ``persist_one`` — it stays uncleaned in the DB so the
    next run retries it — and the run files one ``system_error``
    (``error_context`` is merged into that row's context).

    Returns: results in the SAME ORDER as ``pages``. Skipped pages get
    a placeholder CleanedPage; the caller is expected to ignore those
    (its DB rows already carry the real cleaned_text).
    """
    total = len(pages)
    done_counter = {"n": 0}
    skip_set = skip_indexes or set()
    refusal: dict[str, CleanedPage | None] = {"page": None}
    # The host's short-page threshold, read once per run (0 = clean every page).
    min_chars = await get_clean_min_page_chars()

    async def one(idx: int, text: str) -> CleanedPage:
        # Skip-already-cleaned: don't burn LLM tokens twice.
        if idx in skip_set:
            done_counter["n"] += 1
            if on_progress is not None:
                try:
                    await on_progress(done_counter["n"], total)
                except Exception as exc:  # noqa: BLE001
                    logger.warning("clean_pdf_pages on_progress hook raised: %s", exc)
            # Sentinel — caller must NOT persist this back; its DB row
            # already has the real cleaned content.
            return CleanedPage(text=text, section_kind="")

        # At most ``concurrency`` pages run this body at once (see ``bounded``).
        if before_page is not None and refusal["page"] is None:
            await before_page(idx)
        cleaned: CleanedPage | None = None
        try:
            prior = refusal["page"]
            if prior is not None:
                # A caller refusal (usage limit / no credits) is the person's,
                # not transient: every later page would be refused the same way,
                # so do not ask again — carry the same reason.
                cleaned = CleanedPage(
                    text=text,
                    section_kind="",
                    degraded=True,
                    failure_reason=prior.failure_reason,
                    refused=True,
                    failure=prior.failure,
                )
            else:
                cleaned = await clean_pdf_text(text, min_chars=min_chars)
                if cleaned.refused and refusal["page"] is None:
                    refusal["page"] = cleaned
        except Exception as exc:  # noqa: BLE001
            # clean_pdf_text already has its own fallback; if we somehow still
            # raised, keep the raw page so the result slot remains durable.
            logger.warning("clean_pdf_pages page %d failed: %s", idx, exc)
            cleaned = CleanedPage(
                text=text,
                section_kind="",
                degraded=True,
                failure_reason=_failure_reason(exc),
                refused=bool(getattr(exc, "is_caller_refusal", False)),
                failure=exc,
            )
        finally:
            # Persist this single page IMMEDIATELY so the work survives a
            # cancellation, OOM, or any later failure. A DEGRADED page (the
            # cleaner failed; ``text`` is the RAW extraction) is NOT persisted:
            # writing raw text as ``cleaned_text`` made every resume count it as
            # cleaned, so it was never retried. Left unwritten, the next run's
            # resume re-cleans it; this run still carries the raw text in memory.
            if cleaned is not None and persist_one is not None and not cleaned.degraded:
                # Persistence failure must fail the stage loudly. A retry skips
                # pages that already landed, so completed work is not repaid.
                try:
                    await persist_one(idx, cleaned)
                except Exception as exc:  # noqa: BLE001
                    logger.error(
                        "clean_pdf_pages persist_one failed for page %d: %s — "
                        "failing the clean stage (never silently drop the LLM work)",
                        idx,
                        exc,
                    )
                    raise

            done_counter["n"] += 1
            if on_progress is not None:
                try:
                    await on_progress(done_counter["n"], total)
                except Exception as exc:  # noqa: BLE001
                    logger.warning("clean_pdf_pages on_progress hook raised: %s", exc)
        assert cleaned is not None
        return cleaned

    in_flight = asyncio.Semaphore(max(1, int(concurrency)))

    async def bounded(idx: int, text: str) -> CleanedPage:
        async with in_flight:
            return await one(idx, text)

    results: list[CleanedPage] = list(
        await asyncio.gather(*(bounded(i, p) for i, p in enumerate(pages)))
    )

    # ── Layer 1b: pages the guard refused, kept on their own text ───────────
    # Written and done (clean text = raw text, marked), but not the quality billed for: one
    # record per run, with every reason, so a refusal is never silent.
    kept_raw = [i for i in range(total) if i not in skip_set and results[i].kept_raw_reason]
    if kept_raw:
        kept_reasons = sorted({results[i].kept_raw_reason for i in kept_raw})[:5]
        logger.error(
            "rag.llm.clean_pdf_pages: %d page(s) kept their own text — the output guard refused the "
            "cleaner's answer: %s",
            len(kept_raw),
            "; ".join(kept_reasons)[:300],
        )
        from matrx_orm import record_error

        await record_error(
            PageCleanKeptRawError(kept_raw, kept_reasons),
            kind="rag_page_clean_kept_raw",
            source_app="matrx-rag",
            source_feature="rag.clean_pdf_pages",
            user_id=(error_context or {}).get("owner_id"),
            organization_id=(error_context or {}).get("organization_id"),
            error_type="PageCleanKeptRaw",
            context={
                **(error_context or {}),
                "kept_raw_page_indexes": kept_raw[:50],
                "kept_raw_kinds": sorted({results[i].section_kind for i in kept_raw}),
                "failure_reasons": kept_reasons,
            },
        )

    # ── Layer 2: the degradation alarm ───────────────────────────────────────
    # Each page's fallback ("agent failed → keep the RAW text") is correct: a raw
    # page beats a dropped page. But per-page WARNINGs are how a TOTAL cleanup
    # failure hid in plain sight — a missing ambient AppContext killed every
    # single cleaner call, every page fell back to raw, and the PDF was chunked
    # and embedded UNCLEANED. Nothing broke, nothing 500'd, the run reported
    # success, and the corpus quietly got worse. Fallbacks must be counted and
    # SCREAM in aggregate, or they are just a slow-motion outage.
    attempted = [i for i in range(total) if i not in skip_set]
    degraded = [i for i in attempted if results[i].degraded]
    if degraded:
        all_failed = len(degraded) == len(attempted)
        all_refused = all(results[i].refused for i in degraded)
        reasons = sorted({results[i].failure_reason for i in degraded if results[i].failure_reason})[:5]
        guard_rejected = all(isinstance(results[i].failure, CleanedOutputRejected) for i in degraded)
        vcprint(
            data={
                "pages_attempted": len(attempted),
                "pages_degraded": len(degraded),
                "degraded_page_indexes": degraded[:20],
                "consequence": (
                    "This run chunks + EMBEDS these pages from RAW extraction text. "
                    "They are NOT saved as cleaned, so re-running the clean retries them."
                ),
                "likely_cause": (
                    f"CALLER REFUSAL (not retried): {results[degraded[0]].failure_reason}"
                    if all_refused
                    else f"The cleaner answered but the output guard rejected it: {reasons[:1]}"
                    if guard_rejected
                    else "EVERY page failed — this is a WIRING bug, not an LLM one. The "
                    "usual culprit: no ambient AppContext (background/detached task), "
                    "so every agent run died before reaching a provider (see failure_reasons). Wrap the entry "
                    "point in matrx_connect.system_app_context."
                    if all_failed
                    else "Per-page agent failures (provider errors / timeouts) after the runner's own retries."
                ),
            },
            title=(
                "RAG PDF CLEANUP — TOTAL FAILURE (every page embedded RAW)"
                if all_failed
                else "RAG PDF CLEANUP — DEGRADED (some pages embedded RAW)"
            ),
            color="red",
            pretty=True,
        )
        logger.error(
            "rag.llm.clean_pdf_pages: %d/%d pages fell back to RAW text%s",
            len(degraded),
            len(attempted),
            f" — ALL of them: {'; '.join(reasons)[:200]}" if all_failed else "",
        )
        # A log line is not a record. File ONE system_error per degraded run so
        # the error queue shows it; the pages stay uncleaned in the DB (never
        # persisted above), so re-running the clean retries exactly them.
        # A CALLER REFUSAL (usage limit / no credits) is the person's, not an
        # incident: it is reported by the failed clean stage, never filed here.
        from matrx_orm import record_error

        if all_refused:
            return results
        await record_error(
            PageCleanDegradedError(
                len(degraded),
                len(attempted),
                all_failed=all_failed,
                guard_rejected=guard_rejected,
                reasons=reasons,
            ),
            kind="rag_page_clean_degraded",
            source_app="matrx-rag",
            source_feature="rag.clean_pdf_pages",
            user_id=(error_context or {}).get("owner_id"),
            organization_id=(error_context or {}).get("organization_id"),
            error_type="PageCleanDegraded",
            context={
                **(error_context or {}),
                "pages_attempted": len(attempted),
                "pages_degraded": len(degraded),
                "degraded_page_indexes": degraded[:50],
                "all_failed": all_failed,
                # WHY the cleaner failed — the row is undiagnosable without it (2026-11-02:
                # 24 rows a day said "never reached a provider" and nothing else).
                "failure_reasons": reasons,
            },
        )
        for i in degraded:
            results[i].recorded = True

    return results


# ---------------------------------------------------------------------------
# Contextual retrieval (Anthropic technique)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ContextWindow:
    """What part of the document one chunk was situated against.

    ``windowed`` is False when the whole document fit. When True, ``text`` is the document head
    plus the chunk's own neighbourhood, each run of omitted characters marked in the text, and
    ``record()`` is what the chunk carries (``metadata['context_window']``) so the cut survives
    as a fact, not only as words inside a prompt."""

    text: str
    windowed: bool
    document_chars: int
    head_chars: int = 0
    #: The neighbourhood ``[start, end)`` in document characters (0, 0 when none was sent).
    span_start: int = 0
    span_end: int = 0
    #: False when the chunk's text could not be found in the document: only the head was sent.
    chunk_located: bool = True

    @property
    def chars_sent(self) -> int:
        return self.head_chars + (self.span_end - self.span_start)

    def record(self) -> dict[str, Any]:
        return {
            "document_chars": self.document_chars,
            "chars_sent": self.chars_sent,
            "head_chars": self.head_chars,
            "span_start": self.span_start,
            "span_end": self.span_end,
            "chunk_located": self.chunk_located,
        }


#: Share of the window given to the document head when the chunk sits past it (the title,
#: abstract and headings that say what the whole document is); the rest is the chunk's
#: neighbourhood.
CONTEXT_HEAD_SHARE = 0.25


def _locate_chunk(document: str, chunk: str) -> int:
    """The chunk's first character in ``document``, or -1. Tries the whole chunk, then its first line."""
    pos = document.find(chunk)
    if pos >= 0:
        return pos
    probe = chunk.strip()[:200]
    return document.find(probe) if len(probe) >= 40 else -1


def situating_window(document: str, chunk: str, max_chars: int) -> ContextWindow:
    """The document context for ``chunk`` within ``max_chars``: the whole document when it fits;
    else the head plus the chunk's own neighbourhood, never the head alone for a late chunk.

    A chunk past the limit used to be situated against ``document[:60_000]`` — text that does not
    contain it — and nothing recorded that. Every omission is now marked in the text."""
    total = len(document)
    if total <= max_chars:
        return ContextWindow(text=document, windowed=False, document_chars=total)
    pos = _locate_chunk(document, chunk)
    if pos < 0:
        head = document[:max_chars]
        return ContextWindow(
            text=(
                f"[Document capped: the first {max_chars:,} of {total:,} characters; "
                f"this passage's place in the document could not be found]\n{head}"
            ),
            windowed=True,
            document_chars=total,
            head_chars=max_chars,
            chunk_located=False,
        )
    end_of_chunk = min(total, pos + len(chunk))
    if end_of_chunk <= max_chars:
        # The chunk sits inside the first ``max_chars``: one contiguous run from the start.
        return ContextWindow(
            text=(
                f"{document[:max_chars]}\n"
                f"[... characters {max_chars + 1:,}-{total:,} of {total:,} omitted ...]"
            ),
            windowed=True,
            document_chars=total,
            head_chars=max_chars,
        )
    head_n = int(max_chars * CONTEXT_HEAD_SHARE)
    budget = max_chars - head_n
    # Centre the chunk in its neighbourhood, clamped to the document's end and after the head.
    slack = max(0, budget - (end_of_chunk - pos))
    start = max(head_n, pos - slack // 2)
    end = min(total, start + budget)
    start = max(head_n, end - budget)
    parts = [
        f"[Document head: characters 1-{head_n:,} of {total:,}]",
        document[:head_n],
    ]
    if start > head_n:
        parts.append(f"[... characters {head_n + 1:,}-{start:,} omitted ...]")
    parts.append(f"[The part of the document around this passage: characters {start + 1:,}-{end:,} of {total:,}]")
    parts.append(document[start:end])
    if end < total:
        parts.append(f"[... characters {end + 1:,}-{total:,} omitted ...]")
    return ContextWindow(
        text="\n".join(parts),
        windowed=True,
        document_chars=total,
        head_chars=head_n,
        span_start=start,
        span_end=end,
    )


async def contextualize_chunk_windowed(
    document: str,
    chunk: str,
    *,
    timeout: float = 30.0,
) -> tuple[str, ContextWindow | None]:
    """``contextualize_chunk`` plus the window the chunk was situated against
    (``None`` for a blank chunk, where nothing was sent)."""
    if not chunk.strip():
        return "", None
    # The document context is bounded HERE (shared assembly) so the window lives in one place.
    window = situating_window(document, chunk, await get_context_window_chars())

    runner = _require_runner()
    try:
        out = await runner.contextualize(window.text, chunk, timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        logger.warning("rag.llm.contextualize_chunk: %s", exc)
        return "", window
    return out.strip(), window


async def contextualize_chunk(
    document: str,
    chunk: str,
    *,
    timeout: float = 30.0,
) -> str:
    """Generate the 1-2 sentence prefix that situates ``chunk`` within
    ``document`` via the host's contextualizer agent. Used by ``rag.enrich``
    to prepend before embedding. Empty string on failure. A document longer than the host's
    window is sent as its head plus the chunk's neighbourhood (``situating_window``).
    """
    prefix, _window = await contextualize_chunk_windowed(document, chunk, timeout=timeout)
    return prefix


# ---------------------------------------------------------------------------
# Query understanding — multi-query + HyDE
# ---------------------------------------------------------------------------


# MULTI_QUERY_SYSTEM: the text lives in the stored rag agent (agent.definition) its mandate holds; it is no longer kept in code.


# HYDE_SYSTEM: the text lives in the stored rag agent (agent.definition) its mandate holds; it is no longer kept in code.


async def expand_query(
    query: str,
    *,
    n: int = 3,
    timeout: float = 15.0,
) -> list[str]:
    """Generate ``n-1`` paraphrases of ``query`` via the host's query-expander
    agent so the search can fan out across multiple embedding angles. Returns
    a list with the ORIGINAL query first; deduplicates trivially. On failure
    returns just ``[query]``.
    """
    if not query.strip() or n <= 1:
        return [query]

    runner = _require_runner()
    try:
        lines = await runner.expand_query(query, n=n, timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        logger.warning("rag.llm.expand_query: %s", exc)
        return [query]
    return _assemble_expansions(query, lines, n)


async def hyde_passage(query: str, *, timeout: float = 15.0) -> str:
    """Generate a short hypothetical answer passage for HyDE retrieval via the
    host's HyDE agent.

    Empty string on failure — caller falls back to plain query embedding.
    """
    if not query.strip():
        return ""

    runner = _require_runner()
    try:
        out = await runner.hyde(query, timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        logger.warning("rag.llm.hyde_passage: %s", exc)
        return ""
    return out.strip()


# Back-compat alias — the private name predates the batch lane and is still
# referenced by tests and by matrx_rag-internal callers.
_normalize_cleaned = normalize_cleaned_page


__all__ = [
    "CleanedOutputRejected",
    "CleanedPage",
    "cleaned_output_rejection",
    "normalize_cleaned_page",
    "short_page_verbatim",
    "tiny_page_kept_on_rejection",
    "page_kept_on_rejection",
    "CLEAN_REJECTED_KIND",
    "VERBATIM_KINDS",
    "PageCleanKeptRawError",
    "SHORT_PAGE_KIND",
    "clean_pdf_pages",
    "clean_pdf_text",
    "ContextWindow",
    "contextualize_chunk",
    "contextualize_chunk_windowed",
    "situating_window",
    "expand_query",
    "hyde_passage",
]
