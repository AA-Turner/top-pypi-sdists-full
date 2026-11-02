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

from matrx_rag._ext import RagAgentRunner, get_rag_agent_runner
from matrx_rag.text_hygiene import strip_control_chars

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


class PageCleanDegradedError(RuntimeError):
    """Pages whose cleaner call failed — recorded to ``system_error``, never raised."""

    def __init__(self, degraded: int, attempted: int, *, all_failed: bool) -> None:
        self.degraded = degraded
        self.attempted = attempted
        self.all_failed = all_failed
        super().__init__(
            f"{degraded}/{attempted} pages failed to clean"
            + (" (every page — the cleaner never reached a provider)" if all_failed else "")
            + "; they were left uncleaned so a re-run retries them"
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

    def __init__(self, degraded: int, attempted: int, *, reason: str, refused: bool) -> None:
        self.degraded = degraded
        self.attempted = attempted
        self.reason = reason
        self.refused = refused
        self.is_caller_refusal = refused
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
    return page.get("section_kind") == CLEAN_FAILED_KIND or not page_is_cleaned(
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
    if (
        kind not in _EMPTY_OK_KINDS
        and len(raw_s) >= _SHRINK_MIN_RAW_CHARS
        and len(out) < len(raw_s) * MIN_CLEANED_SHARE
    ):
        return (
            f"cleaner output is {len(out)} chars for {len(raw_s)} raw chars "
            f"(less than {MIN_CLEANED_SHARE}x) — content lost"
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


async def clean_pdf_text(raw: str, *, timeout: float = 60.0) -> CleanedPage:
    """Run one cleanup + classification pass over a single page through the
    host's page-cleaner agent.

    Provider admission is owned centrally by the agent runner. A page falls
    back to its raw text on failure, logged loudly so an incomplete page is
    never silent."""
    raw = strip_control_chars(raw)
    if not raw or not raw.strip():
        return CleanedPage(text="", section_kind="blank_or_garbage")

    runner = _require_runner()

    try:
        parsed = await runner.clean_page(raw, timeout=timeout)
    except Exception as exc:  # noqa: BLE001
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
        # A FAILED page, never a cleaned one: degraded pages are not persisted,
        # so junk can never overwrite a page's good cleaned text.
        logger.warning("rag.llm.clean_pdf_text: output REJECTED (%s); returning raw text", rejection)
        return CleanedPage(
            text=raw,
            section_kind="",
            degraded=True,
            failure_reason=rejection,
            failure=CleanedOutputRejected(rejection),
        )
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

    ``concurrency`` remains only for API compatibility and is ignored. The
    central matrx-ai provider admission gate owns provider-safe pacing.

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

        # All independent page tasks start immediately. UnifiedAIClient queues
        # only at the provider boundary when the provider requires it.
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
                cleaned = await clean_pdf_text(text)
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

    results: list[CleanedPage] = list(
        await asyncio.gather(*(one(i, p) for i, p in enumerate(pages)))
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
                    else "EVERY page failed — this is a WIRING bug, not an LLM one. The "
                    "usual culprit: no ambient AppContext (background/detached task), "
                    "so every agent run died before reaching a provider. Wrap the entry "
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
            " — ALL of them; the cleaner never reached a provider" if all_failed else "",
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
            PageCleanDegradedError(len(degraded), len(attempted), all_failed=all_failed),
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
            },
        )

    return results


# ---------------------------------------------------------------------------
# Contextual retrieval (Anthropic technique)
# ---------------------------------------------------------------------------


async def contextualize_chunk(
    document: str,
    chunk: str,
    *,
    timeout: float = 30.0,
) -> str:
    """Generate the 1-2 sentence prefix that situates ``chunk`` within
    ``document`` via the host's contextualizer agent. Used by ``rag.enrich``
    to prepend before embedding. Empty string on failure.
    """
    if not chunk.strip():
        return ""
    # Truncate the document HERE (shared assembly) so the system-prompt context
    # window is capped in exactly one place.
    doc = document[:60_000]

    runner = _require_runner()
    try:
        out = await runner.contextualize(doc, chunk, timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        logger.warning("rag.llm.contextualize_chunk: %s", exc)
        return ""
    return out.strip()


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
    "clean_pdf_pages",
    "clean_pdf_text",
    "contextualize_chunk",
    "expand_query",
    "hyde_passage",
]
