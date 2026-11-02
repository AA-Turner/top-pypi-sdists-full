"""External-AI-call observability for matrx-rag.

Why this exists
---------------
matrx-rag's built-in providers — ``DefaultOpenAIVoyageProvider`` (embeddings)
— talk to OpenAI / Voyage via their
own SDK clients. The aidream host also wires extraction adapters
(``GlinerNerExtractor`` → Fastino) and a future big-model NER finisher that
hit external APIs without going through matrx-ai's ``UnifiedAIClient``. None
of these paths were riding the canonical cost-tracking pipeline, so:

  * matrx-ai's per-call ``cx_request`` cost rows did not exist for them
  * matrx-ai's structured stream events did not fire
  * matrx-ai's print pipeline that announces every external AI call was silent

On 2026-06-03 we discovered the consequence: a quadratic suggestion loop
fired ~6 000 serial OpenAI embedding round-trips for a single note, in
complete silence, with no operator-visible trace. That class of failure
becomes structurally impossible the moment every call site here is
required to announce itself AND every call increments a running tally
the operator can read at the end of a script / request / job.

The contract
------------
Every external AI call from matrx-rag (embeddings, chat, extraction)
goes through a context-manager wrapper in this module that:

  * Prints a cyan START block before the SDK call
    (provider, model, batch/text sizes, estimated tokens + cost, plus an
    optional request_preview when verbose is on)
  * Prints a green DONE block after success
    (with vectors_returned / output_chars + elapsed_ms + an optional
    response_preview)
  * Prints a red FAILED block on exception
  * Increments the process-wide ``AICallTally`` so an end-of-script
    summary (``print_tally_summary()``) shows total calls, characters,
    elapsed time, and estimated cost broken down by provider × kind ×
    purpose × model.

The tally is the safety net. If you can read the summary at the end of a
run and the numbers don't match your mental model, something silent
happened — and now you can see it.
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any

# ── Announcement gate (debug-only verbose) ──────────────────────────────
# The per-call START / DONE / PROGRESS blocks are pure operator-debugging
# noise in normal operation — a single 350-page PDF emits hundreds of them.
# They are gated behind this toggle so a host (the content-processing
# orchestrator) can turn them on ONLY when ``debug=True`` is passed.
#
# CRITICAL: this gates ONLY the visual announcement. The running ``_tally``
# is ALWAYS incremented (cost/perf telemetry is never silenced), and the
# red FAILED blocks ALWAYS print (an error must never be invisible).
# Default ON so existing scripts (e2e tests, backfills) are unaffected.
ANNOUNCE_AI_CALLS: bool = True


def set_ai_call_announcements(enabled: bool) -> None:
    """Turn the per-call START/DONE/PROGRESS announcement blocks on/off.

    Errors (red FAILED blocks) and the cost tally are unaffected — they
    always run. Used by the content-processing orchestrator to keep the
    terminal quiet unless the caller asked for ``debug=True``."""
    global ANNOUNCE_AI_CALLS  # noqa: PLW0603
    ANNOUNCE_AI_CALLS = bool(enabled)


def set_ai_call_verbose(enabled: bool) -> None:
    """Turn the request/response PREVIEW (truncated content) on/off."""
    global VERBOSE_AI_CALLS  # noqa: PLW0603
    VERBOSE_AI_CALLS = bool(enabled)


def _vcprint(**kwargs: Any) -> None:
    """Lazy, cycle-safe proxy around ``matrx_utils.vcprint``.

    Importing ``matrx_utils`` at module top — or even at first call —
    is unsafe because the matrx_utils package has multiple circular
    import paths through its own submodules (code_context, data_handling).
    Going straight to the leaf module that defines ``vcprint`` sidesteps
    every cycle.

    If even the leaf import fails for some exotic reason we fall back to
    a plain ``print`` so the announcement never silently disappears —
    observability must NEVER be the thing that crashes a save-hook.

    Announcement gate: when ``ANNOUNCE_AI_CALLS`` is False every non-error
    block is suppressed (red ``color="red"`` FAILED blocks always survive).
    """
    if not ANNOUNCE_AI_CALLS and kwargs.get("color") != "red":
        return
    try:
        from matrx_utils.fancy_prints.fancy_prints import (  # noqa: PLC0415
            vcprint as _real_vcprint,
        )
    except Exception:  # noqa: BLE001 — fall through to plain print
        title = kwargs.get("title", "AI CALL")
        data = kwargs.get("data")
        print(f"\n{title}:\n  {data}\n", flush=True)
        return
    _real_vcprint(**kwargs)


# ── Verbose-mode toggle ─────────────────────────────────────────────────
# Verbose mode includes a truncated request_preview / response_preview
# in every announcement so you can see WHAT was sent, not just metadata.
# Code-reviewed constants, not env vars (were AI_CALL_PREVIEW_MAX_CHARS /
# VERBOSE_AI_CALLS). Default ON — truncation cost is microseconds and the
# operator benefit (catching "wrong text was embedded") is enormous; the
# tally is kept either way.
_PREVIEW_MAX_CHARS = 500
VERBOSE_AI_CALLS: bool = True


def _verbose_default() -> bool:
    return VERBOSE_AI_CALLS


# ── Extraction-call noise control ───────────────────────────────────────
# The GLiNER extraction path fires one START + one DONE block per chunk.
# Once that path is stable this is pure noise — hundreds of identical
# green blocks burying the warnings/errors that actually matter. So for
# extraction (and ONLY extraction) the per-call START/DONE blocks are
# SILENT by default; what survives is:
#   * every FAILED block (errors always print)
#   * a WARNING block for a call that returned 0 spans (the one per-call
#     signal worth seeing — "we paid and got nothing")
#   * a periodic PROGRESS block every N successful calls with running
#     counts, characters, elapsed and estimated cost (from the tally).
# EXTRACTION_VERBOSE / EXTRACTION_PROGRESS_EVERY are code-reviewed constants,
# not env vars. Flip EXTRACTION_VERBOSE True to restore per-call START/DONE
# blocks; set PROGRESS_EVERY to 0 to disable the periodic progress block.
EXTRACTION_VERBOSE: bool = False


def _extraction_verbose() -> bool:
    return EXTRACTION_VERBOSE


_EXTRACTION_PROGRESS_EVERY = 10
_extraction_counter_lock = threading.Lock()
_extraction_completed = 0


def _bump_extraction_progress() -> int:
    """Increment the completed-extraction counter; return the new value."""
    global _extraction_completed  # noqa: PLW0603
    with _extraction_counter_lock:
        _extraction_completed += 1
        return _extraction_completed


def _print_extraction_progress() -> None:
    """Emit a compact running-total block for the extraction buckets only,
    pulled straight from the live tally so the numbers are authoritative."""
    snap = _tally.snapshot()
    calls = 0
    failed = 0
    input_chars = 0
    spans = 0
    elapsed_ms = 0
    cost = 0.0
    for bucket in snap["buckets"]:
        if bucket["kind"] != "extraction":
            continue
        calls += bucket["calls"]
        failed += bucket["failed"]
        input_chars += bucket["input_chars"]
        spans += bucket["output_chars"]  # extraction repurposes output_chars as span count
        elapsed_ms += bucket["elapsed_ms"]
        cost += bucket["estimated_cost_usd"]
    avg_ms = round(elapsed_ms / calls) if calls else 0
    _vcprint(
        data={
            "calls": calls,
            "failed": failed,
            "spans_returned": spans,
            "input_chars": input_chars,
            "avg_ms": avg_ms,
            "elapsed_ms": elapsed_ms,
            "estimated_cost_usd": round(cost, 6),
        },
        title="AI CALL → extraction PROGRESS",
        color="yellow",
        pretty=True,
    )


def _preview(text: str | None, *, limit: int | None = None) -> str:
    """Truncate ``text`` for an operator-visible preview. ``limit`` falls
    back to ``AI_CALL_PREVIEW_MAX_CHARS`` (500). Single-line normalized so
    the vcprint block stays readable."""
    if text is None:
        return ""
    s = " ".join(str(text).split())
    cap = limit or _PREVIEW_MAX_CHARS
    if len(s) <= cap:
        return s
    return f"{s[:cap]} …[+{len(s) - cap} more chars]"


# ── Cost estimates ──────────────────────────────────────────────────────
# These are operator-visible breadcrumbs, not invoiced amounts. Real
# billing comes from the provider invoice. Update as price pages move.
# Voyage text-embedding list prices: https://docs.voyageai.com/docs/pricing
# (verified 2026-07-07). OpenAI: https://platform.openai.com/docs/pricing
_EMBEDDING_PRICE_PER_M_TOKENS: dict[str, float] = {
    # OpenAI text embeddings (USD per 1M tokens)
    "text-embedding-3-small": 0.02,
    "text-embedding-3-large": 0.13,
    "text-embedding-ada-002": 0.10,
    # Voyage 4 series (current defaults — voyage-4-large is prose default)
    "voyage-4-large": 0.12,
    "voyage-4": 0.06,
    "voyage-4-lite": 0.02,
    "voyage-context-3": 0.18,
    "voyage-code-3": 0.18,
    # Voyage domain / legacy text embeddings still reachable via explicit model
    "voyage-finance-2": 0.12,
    "voyage-law-2": 0.12,
    "voyage-code-2": 0.12,
    "voyage-3-large": 0.18,
    "voyage-3.5": 0.06,
    "voyage-3.5-lite": 0.02,
    "voyage-3": 0.06,
    "voyage-2": 0.10,
    "voyage-large-2": 0.12,
}

# Dedupe missing-price alarms: one red banner per (price_table, model) per process.
# Subsequent missing-cost calls still record cost_is_exact=False and cost_usd=null/0.
_MISSING_PRICE_ALARM_KEYS: set[tuple[str, str]] = set()

_CHAT_INPUT_PRICE_PER_M_TOKENS: dict[str, float] = {
    "gpt-5.4": 0.15,
    "gpt-5-mini": 0.25,
    "gpt-4.1-mini": 0.40,
    "gpt-4o-mini": 0.15,
    "gpt-4o": 2.50,
    "claude-haiku-4.5": 1.00,
    "claude-sonnet-4.6": 3.00,
    "claude-opus-4.5": 15.00,
}

_CHAT_OUTPUT_PRICE_PER_M_TOKENS: dict[str, float] = {
    "gpt-5.4": 0.60,
    "gpt-5-mini": 2.00,
    "gpt-4.1-mini": 1.60,
    "gpt-4o-mini": 0.60,
    "gpt-4o": 10.00,
    "claude-haiku-4.5": 5.00,
    "claude-sonnet-4.6": 15.00,
    "claude-opus-4.5": 75.00,
}

# Extraction providers (Fastino GLiNER) are contract-priced, so there is no
# per-call invoice figure to read back. Per Arman (2026-06-09) we model it at
# a flat $0.0005 per 1,000 tokens, derived from the EXACT input character
# count of each call. This is the one component that is a *sized estimate* by
# design — being slightly off on an individual call (token heuristic) is
# acceptable; the LLM + embedding components are exact.
# A code-reviewed constant, not an env var (was GLINER_USD_PER_1K_TOKENS).
_EXTRACTION_USD_PER_1K_TOKENS: float = 0.0005


def _estimate_tokens(chars: int) -> int:
    # ~4 chars per token is the standard cheap heuristic for English-ish
    # text. We use it consistently across embeddings and chat so the
    # estimate is comparable between call sites.
    return max(1, chars // 4)


def _alarm_missing_price(
    *,
    price_table: str,
    model: str,
    context: str,
    provider: str | None = None,
) -> None:
    """Scream once per (price_table, model) when we cannot compute a dollar cost.

    Red blocks bypass ANNOUNCE_AI_CALLS — a missing price must never be silent."""
    key = (price_table, model)
    if key in _MISSING_PRICE_ALARM_KEYS:
        return
    _MISSING_PRICE_ALARM_KEYS.add(key)
    map_name = {
        "embedding": "_EMBEDDING_PRICE_PER_M_TOKENS",
        "chat_input": "_CHAT_INPUT_PRICE_PER_M_TOKENS",
        "chat_output": "_CHAT_OUTPUT_PRICE_PER_M_TOKENS",
    }.get(price_table, f"_{price_table.upper()}_PRICE_PER_M_TOKENS")
    fix_hint = (
        "Add the model to the matching price map in "
        "packages/matrx-rag/matrx_rag/_observability.py "
        f"({map_name}). Verify against the provider's official pricing page before adding."
    )
    _vcprint(
        data={
            "price_table": price_table,
            "model": model,
            "provider": provider,
            "context": context,
            "fix": fix_hint,
            "note": (
                "Cost telemetry for this model will show cost_usd=null and "
                "cost_is_exact=false until the price map is updated. "
                "Further alarms for this model are suppressed this process."
            ),
        },
        title="[matrx-rag] MISSING EMBEDDING/CHAT PRICE — cost cannot be computed",
        color="red",
        pretty=True,
    )


def _embedding_price_per_m_tokens(model: str, *, context: str) -> float | None:
    price = _EMBEDDING_PRICE_PER_M_TOKENS.get(model)
    if price is None:
        _alarm_missing_price(price_table="embedding", model=model, context=context)
    return price


def _chat_input_price_per_m_tokens(model: str, *, context: str) -> float | None:
    price = _CHAT_INPUT_PRICE_PER_M_TOKENS.get(model)
    if price is None:
        _alarm_missing_price(price_table="chat_input", model=model, context=context)
    return price


def _chat_output_price_per_m_tokens(model: str, *, context: str) -> float | None:
    price = _CHAT_OUTPUT_PRICE_PER_M_TOKENS.get(model)
    if price is None:
        _alarm_missing_price(price_table="chat_output", model=model, context=context)
    return price


def _embedding_cost_usd(model: str, total_chars: int, *, context: str) -> float | None:
    """ESTIMATE: cost from the char→token heuristic. Used only as a fallback
    when the provider response did not return a real token count."""
    price = _embedding_price_per_m_tokens(model, context=context)
    if price is None:
        return None
    tokens = _estimate_tokens(total_chars)
    return (tokens / 1_000_000.0) * price


def _embedding_cost_from_tokens(model: str, actual_tokens: int, *, context: str) -> float | None:
    """EXACT quantity: provider-reported token count × published list price.

    Exact barring private contract discounts. Returns None when list price
    is missing from the map — caller must treat cost_is_exact as False."""
    price = _embedding_price_per_m_tokens(model, context=context)
    if price is None:
        return None
    return (max(0, actual_tokens) / 1_000_000.0) * price


def _chat_input_cost_usd(model: str, input_chars: int, *, context: str) -> float | None:
    price = _chat_input_price_per_m_tokens(model, context=context)
    if price is None:
        return None
    tokens = _estimate_tokens(input_chars)
    return (tokens / 1_000_000.0) * price


def _chat_output_cost_usd(model: str, output_chars: int, *, context: str) -> float | None:
    price = _chat_output_price_per_m_tokens(model, context=context)
    if price is None:
        return None
    tokens = _estimate_tokens(output_chars)
    return (tokens / 1_000_000.0) * price


def _extraction_cost_usd(input_chars: int) -> float:
    """SIZED ESTIMATE: $0.0005 per 1,000 tokens, tokens derived from the
    EXACT input character count of the call."""
    tokens = _estimate_tokens(input_chars)
    return (tokens / 1_000.0) * _EXTRACTION_USD_PER_1K_TOKENS


# ── Process-wide AI-call tally ──────────────────────────────────────────


@dataclass
class _BucketStats:
    calls: int = 0
    failed: int = 0
    input_chars: int = 0
    output_chars: int = 0
    input_tokens: int = 0  # provider-reported when available, else heuristic
    elapsed_ms: int = 0
    estimated_cost_usd: float = 0.0
    cost_is_exact: bool = True  # False if ANY call lacked provider tokens OR list price
    # Cache-served work — texts answered from the content-addressable
    # embedding cache without a provider call. These are NOT counted in
    # ``calls`` (no provider round-trip happened) so the paid-cost totals
    # stay honest. ``cost_saved_usd`` is the list-price the cache avoided.
    cache_hits: int = 0
    cost_saved_usd: float = 0.0


@dataclass
class AICallTally:
    """Running totals of every external AI call this process has made
    since the last ``tally_reset()``. Buckets are keyed by
    ``(provider, kind, purpose, model)``. Safe to read from any thread —
    increments are protected by a single lock."""

    started_at: float = field(default_factory=time.time)
    by_bucket: dict[tuple[str, str, str, str], _BucketStats] = field(
        default_factory=lambda: defaultdict(_BucketStats)
    )
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def record(
        self,
        *,
        provider: str,
        kind: str,
        purpose: str,
        model: str,
        input_chars: int,
        output_chars: int,
        elapsed_ms: int,
        cost_usd: float | None,
        input_tokens: int = 0,
        cost_is_exact: bool = False,
        failed: bool = False,
    ) -> None:
        key = (provider, kind, purpose or "<unspecified>", model)
        with self._lock:
            bucket = self.by_bucket[key]
            bucket.calls += 1
            if failed:
                bucket.failed += 1
            bucket.input_chars += int(input_chars or 0)
            bucket.output_chars += int(output_chars or 0)
            bucket.input_tokens += int(input_tokens or 0)
            bucket.elapsed_ms += int(elapsed_ms or 0)
            bucket.estimated_cost_usd += float(cost_usd or 0.0)
            # A bucket is "exact" only if EVERY call into it was exact.
            if not cost_is_exact:
                bucket.cost_is_exact = False
        _feed_run_collector(
            kind=kind,
            cost_usd=float(cost_usd or 0.0),
            input_tokens=int(input_tokens or 0),
            cost_is_exact=cost_is_exact,
        )

    def record_cache_served(
        self,
        *,
        provider: str,
        kind: str,
        purpose: str,
        model: str,
        hits: int,
        input_chars: int,
        cost_saved_usd: float,
    ) -> None:
        """Record work answered from a content-addressable cache (no
        provider call). Goes into its OWN bucket so the paid-cost totals
        are never inflated. ``hits`` is the number of texts served from
        cache; ``cost_saved_usd`` is the list-price the cache avoided.

        Without this, a fully-cached run shows ``$0 / 0 calls`` for the
        embedding component — indistinguishable from "embeddings never
        ran" or "the tally is broken". Recording the hits makes the $0
        self-explanatory: it was paid once, in a prior run."""
        key = (provider, kind, purpose or "<unspecified>", model)
        with self._lock:
            bucket = self.by_bucket[key]
            bucket.cache_hits += int(hits or 0)
            bucket.input_chars += int(input_chars or 0)
            bucket.cost_saved_usd += float(cost_saved_usd or 0.0)
        _feed_run_collector(
            kind=kind,
            cost_usd=0.0,
            cache_hits=int(hits or 0),
            cost_saved_usd=float(cost_saved_usd or 0.0),
        )

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            buckets: list[dict[str, Any]] = []
            total_calls = 0
            total_failed = 0
            total_input = 0
            total_output = 0
            total_elapsed = 0
            total_cost = 0.0
            total_cache_hits = 0
            total_saved = 0.0
            for (provider, kind, purpose, model), stats in sorted(self.by_bucket.items()):
                buckets.append(
                    {
                        "provider": provider,
                        "kind": kind,
                        "purpose": purpose,
                        "model": model,
                        "calls": stats.calls,
                        "failed": stats.failed,
                        "input_chars": stats.input_chars,
                        "output_chars": stats.output_chars,
                        "input_tokens": stats.input_tokens,
                        "elapsed_ms": stats.elapsed_ms,
                        "estimated_cost_usd": round(stats.estimated_cost_usd, 6),
                        "cost_is_exact": stats.cost_is_exact,
                        "cache_hits": stats.cache_hits,
                        "cost_saved_usd": round(stats.cost_saved_usd, 6),
                    }
                )
                total_calls += stats.calls
                total_failed += stats.failed
                total_input += stats.input_chars
                total_output += stats.output_chars
                total_elapsed += stats.elapsed_ms
                total_cost += stats.estimated_cost_usd
                total_cache_hits += stats.cache_hits
                total_saved += stats.cost_saved_usd
            return {
                "started_at": self.started_at,
                "wall_clock_seconds": round(time.time() - self.started_at, 3),
                "totals": {
                    "calls": total_calls,
                    "failed": total_failed,
                    "input_chars": total_input,
                    "output_chars": total_output,
                    "elapsed_ms": total_elapsed,
                    "estimated_cost_usd": round(total_cost, 6),
                    "cache_hits": total_cache_hits,
                    "cost_saved_usd": round(total_saved, 6),
                },
                "buckets": buckets,
            }


_tally = AICallTally()


# ---------------------------------------------------------------------------
# Per-run cost collection (WP-08 — the ingest_run ledger's stage split)
# ---------------------------------------------------------------------------
# The global tally is process-wide and can only answer "what has this process
# spent since reset" — useless for attributing cost to ONE ingest run when
# several run concurrently. The collector is a contextvar: a host wraps one
# logical run in ``collect_run_costs()`` and every AI call recorded anywhere
# inside that async context (embedding batches, PDF-cleanup chat calls,
# extraction calls, cache hits) is ALSO added to the run's collector.
# Contextvars propagate through ``await`` and ``asyncio.gather``, so the
# embedding batch fan-out lands in the right run. Zero cost when no collector
# is active (the common path).


@dataclass
class RunCostCollector:
    """Stage-split cost accumulator for one logical ingest run.

    ``embedding_*`` — provider embedding calls (plus cache hits served).
    ``extraction_*`` — true NER extraction calls (kind="extraction").
    ``chat_*`` — every other provider LLM call matrx-rag made for the run
    (PDF cleanup, contextualize, vision captions). Kept separate so the
    host's ledger never reports cleanup spend as extraction spend.
    Enrichment-agent cost is host-side and never flows through this module.
    """

    embedding_calls: int = 0
    embedding_tokens: int = 0
    embedding_cost_usd: float = 0.0
    embedding_cache_hits: int = 0
    embedding_cost_saved_usd: float = 0.0
    extraction_calls: int = 0
    extraction_cost_usd: float = 0.0
    chat_calls: int = 0
    chat_cost_usd: float = 0.0
    cost_is_exact: bool = True  # False if ANY call lacked provider tokens or list price
    # Secret-guard counters (2026-09-13 leak: a note holding a raw .env dump was
    # indexed verbatim and served back by knowledge_search). Not money — but the
    # host's rag.ingest_run row is the ONE row per ingest attempt, so it is also
    # the only honest place to record "this source carried N credentials and they
    # were redacted before anything was stored". NAMES ONLY, never values.
    secrets_redacted: int = 0
    secret_names: list[str] = field(default_factory=list)


_run_collector: ContextVar[RunCostCollector | None] = ContextVar(
    "matrx_rag_run_cost_collector", default=None
)


@contextmanager
def collect_run_costs() -> Iterator[RunCostCollector]:
    """Collect every AI call recorded inside this context into one
    :class:`RunCostCollector`. Reentrant-safe: an inner collector shadows the
    outer one for its duration (costs are not double-collected)."""
    collector = RunCostCollector()
    token = _run_collector.set(collector)
    try:
        yield collector
    finally:
        _run_collector.reset(token)


def _feed_run_collector(
    *,
    kind: str,
    cost_usd: float,
    input_tokens: int = 0,
    cache_hits: int = 0,
    cost_saved_usd: float = 0.0,
    cost_is_exact: bool = True,
) -> None:
    collector = _run_collector.get()
    if collector is None:
        return
    if kind == "embedding":
        if cache_hits:
            collector.embedding_cache_hits += cache_hits
            collector.embedding_cost_saved_usd += cost_saved_usd
        else:
            collector.embedding_calls += 1
            collector.embedding_tokens += int(input_tokens or 0)
            collector.embedding_cost_usd += float(cost_usd or 0.0)
    elif kind == "extraction":
        collector.extraction_calls += 1
        collector.extraction_cost_usd += float(cost_usd or 0.0)
    else:  # chat — cleanup / contextualize / vision captions
        collector.chat_calls += 1
        collector.chat_cost_usd += float(cost_usd or 0.0)
    if not cost_is_exact and not cache_hits:
        collector.cost_is_exact = False


def record_secret_redaction(*, count: int, names: Iterable[str]) -> None:
    """Add a secret-redaction event to the active run collector (if any).

    Called by :mod:`matrx_rag.secret_guard` after redaction ran. Zero cost when
    no collector is open. NAMES ONLY — a secret value must never reach this
    function, the collector, the ledger row, or a log line.
    """
    collector = _run_collector.get()
    if collector is None or count <= 0:
        return
    collector.secrets_redacted += int(count)
    for name in names:
        if name and name not in collector.secret_names:
            collector.secret_names.append(str(name))


def tally_reset() -> None:
    """Clear the global tally and restart the wall clock. A long-running
    script (the e2e test, a batch backfill) should call this BEFORE the
    work starts and ``print_tally_summary`` AFTER. Returns ``None`` so
    you can chain it without a temp."""
    global _tally  # noqa: PLW0603
    _tally = AICallTally()


def tally_snapshot() -> dict[str, Any]:
    """Read-only snapshot of the current tally (safe to log, dump, etc.)."""
    return _tally.snapshot()


def record_chat_call(
    *,
    provider: str,
    model: str,
    purpose: str,
    cost_usd: float | None,
    input_chars: int = 0,
    output_chars: int = 0,
    input_tokens: int = 0,
    elapsed_ms: int = 0,
    cost_is_exact: bool = True,
    failed: bool = False,
) -> None:
    """Record a completed chat call into the process-wide tally WITHOUT the
    ``announce_chat_call`` context manager.

    For callers that ran the chat through a DIFFERENT execution stack (the
    agent path: matrx-ai's ``UnifiedAIClient`` via a ``NamedAgent``) and
    already hold the EXACT provider usage + cost. Direct ``LLMProvider`` chat
    calls feed the tally from inside ``announce_chat_call``; this is its
    agent-path twin, so the content-processing money-block stays honest about
    cleanup cost. Use the canonical ``purpose`` strings (``pdf_cleanup`` /
    ``contextual_retrieval`` / ``multi_query_expansion`` / ``hyde``) so the
    agent calls land in the same bucket the money-block expects.

    Cost-tracking is never silenced; there is no announcement gate here (this
    records telemetry only — the agent stack does its own visible logging)."""
    if cost_usd is None:
        _alarm_missing_price(
            price_table="chat_input",
            model=model,
            context="record_chat_call",
            provider=provider,
        )
        cost_is_exact = False
    _tally.record(
        provider=provider,
        kind="chat",
        purpose=purpose or "chat",
        model=model,
        input_chars=input_chars,
        output_chars=output_chars,
        input_tokens=input_tokens,
        elapsed_ms=elapsed_ms,
        cost_usd=cost_usd or 0.0,
        cost_is_exact=cost_is_exact,
        failed=failed,
    )


def print_tally_summary(*, title: str = "AI CALL TALLY (since last reset)") -> None:
    """vcprint the tally as a structured block. Designed to be the FINAL
    output of any script that hit external AI providers, so you can
    eyeball "did we spend what we expected" before walking away."""
    snap = tally_snapshot()
    _vcprint(
        data=snap,
        title=title,
        color="yellow",
        pretty=True,
    )


# ── Announcement context managers ───────────────────────────────────────


@contextmanager
def announce_embedding_call(
    *,
    provider: str,
    model: str,
    texts: list[str],
    input_type: str | None = None,
    verbose: bool | None = None,
) -> Iterator[dict[str, object]]:
    """Wrap an embedding SDK call with a START/DONE vcprint pair AND a
    tally increment. Yields a small dict the caller mutates to record
    ``vectors_returned``; on exit (success or exception) we print the
    DONE/FAILED block and record into the global tally."""
    verbose_on = _verbose_default() if verbose is None else bool(verbose)
    batch_size = len(texts)
    total_chars = sum(len(t) for t in texts)
    estimated_tokens = _estimate_tokens(total_chars)
    estimated_cost = _embedding_cost_usd(model, total_chars, context="embedding_start_estimate")

    start_data: dict[str, Any] = {
        "provider": provider,
        "model": model,
        "batch_size": batch_size,
        "total_chars": total_chars,
        "estimated_tokens": estimated_tokens,
        "estimated_cost_usd": estimated_cost,
        "input_type": input_type,
    }
    if verbose_on:
        start_data["request_preview"] = [_preview(t, limit=120) for t in texts[:5]]
        if batch_size > 5:
            start_data["request_preview_note"] = f"showing first 5 of {batch_size} texts"
    _vcprint(
        data=start_data,
        title=f"AI CALL → {provider} embeddings.create (START)",
        color="cyan",
        pretty=True,
    )

    # Caller MUST set state["vectors_returned"]; SHOULD set
    # state["actual_tokens"] from the provider response usage so we cost
    # the batch EXACTLY instead of via the char heuristic.
    state: dict[str, object] = {"vectors_returned": 0, "actual_tokens": 0, "error": None}
    started = time.monotonic()
    try:
        yield state
    except Exception as exc:  # noqa: BLE001
        state["error"] = repr(exc)
        elapsed_ms = int((time.monotonic() - started) * 1000)
        _vcprint(
            data={
                "provider": provider,
                "model": model,
                "batch_size": batch_size,
                "elapsed_ms": elapsed_ms,
                "error": state["error"],
            },
            title=f"AI CALL → {provider} embeddings.create (FAILED)",
            color="red",
            pretty=True,
        )
        _tally.record(
            provider=provider,
            kind="embedding",
            purpose=input_type or "embedding",
            model=model,
            input_chars=total_chars,
            output_chars=0,
            elapsed_ms=elapsed_ms,
            cost_usd=0.0,
            failed=True,
        )
        raise
    elapsed_ms = int((time.monotonic() - started) * 1000)
    # Prefer provider-reported token count; fall back to char heuristic only
    # when the response carried no usage figure.
    actual_tokens = int(state.get("actual_tokens") or 0)
    if actual_tokens > 0:
        billed_tokens = actual_tokens
        tokens_source = "provider_usage"
        final_cost = _embedding_cost_from_tokens(
            model, actual_tokens, context="embedding_done_provider_tokens"
        )
    else:
        billed_tokens = estimated_tokens
        tokens_source = "char_heuristic"
        final_cost = _embedding_cost_usd(
            model, total_chars, context="embedding_done_char_heuristic"
        )
    # cost_is_exact: provider token count AND a real list price — never True
    # when cost_usd is null (missing price map entry).
    cost_is_exact = final_cost is not None and tokens_source == "provider_usage"
    _vcprint(
        data={
            "provider": provider,
            "model": model,
            "batch_size": batch_size,
            "vectors_returned": state["vectors_returned"],
            "total_chars": total_chars,
            "billed_tokens": billed_tokens,
            "tokens_source": tokens_source,
            "cost_usd": final_cost,
            "cost_is_exact": cost_is_exact,
            "cost_pricing_missing": final_cost is None,
            "elapsed_ms": elapsed_ms,
        },
        title=f"AI CALL → {provider} embeddings.create (DONE)",
        color="green",
        pretty=True,
    )
    _tally.record(
        provider=provider,
        kind="embedding",
        purpose=input_type or "embedding",
        model=model,
        input_chars=total_chars,
        output_chars=0,
        input_tokens=billed_tokens,
        elapsed_ms=elapsed_ms,
        cost_usd=final_cost or 0.0,
        cost_is_exact=cost_is_exact,
    )
    _report_embedding_spend(
        provider=provider,
        model=model,
        tokens=billed_tokens,
        cost_usd=final_cost,
        cost_is_exact=cost_is_exact,
        input_type=input_type,
        batch_size=batch_size,
    )


def _report_embedding_spend(**spend: Any) -> None:
    """Hand one paid embeddings call to the host's spend sink (``configure(embedding_spend_sink=)``).

    These calls are direct SDK calls the host's billing seam never sees; without the sink the
    spend reaches no ledger. No sink wired = a standalone host, nothing to bill. A sink that
    raises is logged loudly and never fails the embedding that already happened.
    """
    from matrx_rag._ext import get_ext  # noqa: PLC0415

    sink = get_ext("embedding_spend_sink")
    if sink is None:
        return
    try:
        sink(**spend)
    except Exception as exc:  # noqa: BLE001
        _vcprint(
            data={"error": f"{type(exc).__name__}: {exc}", **spend},
            title="matrx-rag: embedding spend sink FAILED — this call's spend is on no ledger",
            color="red",
            pretty=True,
        )


def record_embedding_cache_hits(
    *,
    provider: str,
    model: str,
    hits: int,
    input_chars: int,
    input_type: str | None = None,
    verbose: bool | None = None,
) -> None:
    """Record texts served from the content-addressable embedding cache —
    no provider call was made. This exists so a fully-cached run is
    HONEST instead of silently reporting ``$0 / 0 calls`` for embeddings
    (which reads identically to "embeddings never ran"). The dollars are
    the list-price the cache AVOIDED (a sized estimate from the char→token
    heuristic, since a cache hit carries no provider token count); the
    paid cost is, correctly, $0."""
    if hits <= 0:
        return
    # Price map keys are bare model names ("text-embedding-3-small");
    # callers pass the routed form ("openai:text-embedding-3-small").
    price_key = model.split(":", 1)[-1]
    saved = _embedding_cost_usd(price_key, input_chars, context="embedding_cache_saved_estimate")
    if saved is None:
        saved = 0.0
    _tally.record_cache_served(
        provider="cache",
        kind="embedding",
        purpose=input_type or "embedding",
        model=model,
        hits=hits,
        input_chars=input_chars,
        cost_saved_usd=saved,
    )
    verbose_on = _verbose_default() if verbose is None else bool(verbose)
    if verbose_on:
        _vcprint(
            data={
                "provider": provider,
                "model": model,
                "served_from_cache": hits,
                "total_chars": input_chars,
                "cost_paid_usd": 0.0,
                "cost_saved_estimate_usd": round(saved, 6),
            },
            title="AI CALL → embedding cache (HIT — no provider call)",
            color="green",
            pretty=True,
        )


@contextmanager
def announce_chat_call(
    *,
    provider: str,
    model: str,
    messages: list[dict[str, object]],
    response_format: str | None = None,
    purpose: str | None = None,
    verbose: bool | None = None,
) -> Iterator[dict[str, object]]:
    """Wrap a chat-completion SDK call with a START/DONE/FAILED vcprint
    triplet AND a tally increment. ``purpose`` is the operator-readable
    tag ("pdf_cleanup", "contextual_retrieval", "hyde",
    "ner_finisher", "multi_query_expansion") — strongly encouraged."""
    verbose_on = _verbose_default() if verbose is None else bool(verbose)
    input_chars = sum(len(str(m.get("content", ""))) for m in messages)
    estimated_input_tokens = _estimate_tokens(input_chars)
    estimated_input_cost = _chat_input_cost_usd(
        model, input_chars, context="chat_start_input_estimate"
    )

    start_data: dict[str, Any] = {
        "provider": provider,
        "model": model,
        "purpose": purpose or "<unspecified>",
        "messages": len(messages),
        "input_chars": input_chars,
        "estimated_input_tokens": estimated_input_tokens,
        "estimated_input_cost_usd": estimated_input_cost,
        "response_format": response_format,
    }
    if verbose_on:
        start_data["request_preview"] = [
            {
                "role": str(m.get("role") or ""),
                "content": _preview(str(m.get("content", ""))),
            }
            for m in messages
        ]
    _vcprint(
        data=start_data,
        title=f"AI CALL → {provider} chat.completions.create (START)",
        color="cyan",
        pretty=True,
    )

    state: dict[str, object] = {"output_chars": 0, "output_text": "", "error": None}
    started = time.monotonic()
    try:
        yield state
    except Exception as exc:  # noqa: BLE001
        state["error"] = repr(exc)
        elapsed_ms = int((time.monotonic() - started) * 1000)
        _vcprint(
            data={
                "provider": provider,
                "model": model,
                "purpose": purpose or "<unspecified>",
                "elapsed_ms": elapsed_ms,
                "error": state["error"],
            },
            title=f"AI CALL → {provider} chat.completions.create (FAILED)",
            color="red",
            pretty=True,
        )
        _tally.record(
            provider=provider,
            kind="chat",
            purpose=purpose or "chat",
            model=model,
            input_chars=input_chars,
            output_chars=0,
            elapsed_ms=elapsed_ms,
            cost_usd=0.0,
            failed=True,
        )
        raise
    elapsed_ms = int((time.monotonic() - started) * 1000)
    output_chars = int(state.get("output_chars", 0) or 0)
    output_text = str(state.get("output_text") or "")
    estimated_output_tokens = _estimate_tokens(output_chars)
    estimated_output_cost = _chat_output_cost_usd(
        model, output_chars, context="chat_done_output_estimate"
    )
    total_cost = None
    if estimated_input_cost is not None and estimated_output_cost is not None:
        total_cost = round(estimated_input_cost + estimated_output_cost, 6)
    chat_cost_is_exact = total_cost is not None
    done_data: dict[str, Any] = {
        "provider": provider,
        "model": model,
        "purpose": purpose or "<unspecified>",
        "input_chars": input_chars,
        "estimated_input_tokens": estimated_input_tokens,
        "estimated_input_cost_usd": estimated_input_cost,
        "output_chars": output_chars,
        "estimated_output_tokens": estimated_output_tokens,
        "estimated_output_cost_usd": estimated_output_cost,
        "estimated_total_cost_usd": total_cost,
        "cost_is_exact": chat_cost_is_exact,
        "cost_pricing_missing": total_cost is None,
        "elapsed_ms": elapsed_ms,
    }
    if verbose_on and output_text:
        done_data["response_preview"] = _preview(output_text)
    _vcprint(
        data=done_data,
        title=f"AI CALL → {provider} chat.completions.create (DONE)",
        color="green",
        pretty=True,
    )
    _tally.record(
        provider=provider,
        kind="chat",
        purpose=purpose or "chat",
        model=model,
        input_chars=input_chars,
        output_chars=output_chars,
        elapsed_ms=elapsed_ms,
        cost_usd=total_cost or 0.0,
        cost_is_exact=chat_cost_is_exact,
    )


@contextmanager
def announce_extraction_call(
    *,
    provider: str,
    model: str,
    text: str,
    labels: list[str] | None = None,
    threshold: float | None = None,
    purpose: str | None = None,
    verbose: bool | None = None,
) -> Iterator[dict[str, object]]:
    """Wrap a span-extraction call (Fastino GLiNER2 today) with a
    START/DONE/FAILED vcprint triplet AND a tally increment. ``purpose``
    is the operator tag (e.g. ``"ner_extract"``); ``labels`` is the
    GLiNER label set; ``threshold`` is the confidence cutoff. Yields a
    mutable state dict — caller MUST set ``state["spans_returned"]``."""
    quiet = not _extraction_verbose()
    verbose_on = _verbose_default() if verbose is None else bool(verbose)
    input_chars = len(text or "")
    estimated_tokens = _estimate_tokens(input_chars)
    estimated_cost = _extraction_cost_usd(input_chars)

    if not quiet:
        start_data: dict[str, Any] = {
            "provider": provider,
            "model": model,
            "purpose": purpose or "ner_extract",
            "input_chars": input_chars,
            "estimated_tokens": estimated_tokens,
            "estimated_cost_usd": estimated_cost,
            "labels": labels,
            "threshold": threshold,
        }
        if verbose_on:
            start_data["request_preview"] = _preview(text)
        _vcprint(
            data=start_data,
            title=f"AI CALL → {provider} extraction (START)",
            color="cyan",
            pretty=True,
        )

    state: dict[str, object] = {"spans_returned": 0, "error": None}
    started = time.monotonic()
    try:
        yield state
    except Exception as exc:  # noqa: BLE001
        state["error"] = repr(exc)
        elapsed_ms = int((time.monotonic() - started) * 1000)
        _vcprint(
            data={
                "provider": provider,
                "model": model,
                "purpose": purpose or "ner_extract",
                "elapsed_ms": elapsed_ms,
                "error": state["error"],
            },
            title=f"AI CALL → {provider} extraction (FAILED)",
            color="red",
            pretty=True,
        )
        _tally.record(
            provider=provider,
            kind="extraction",
            purpose=purpose or "ner_extract",
            model=model,
            input_chars=input_chars,
            output_chars=0,
            elapsed_ms=elapsed_ms,
            cost_usd=0.0,
            failed=True,
        )
        raise
    elapsed_ms = int((time.monotonic() - started) * 1000)
    spans_returned = int(state.get("spans_returned", 0) or 0)
    _tally.record(
        provider=provider,
        kind="extraction",
        purpose=purpose or "ner_extract",
        model=model,
        input_chars=input_chars,
        output_chars=spans_returned,  # repurpose: # spans = "output"
        input_tokens=estimated_tokens,
        elapsed_ms=elapsed_ms,
        cost_usd=estimated_cost,
        cost_is_exact=False,  # sized estimate: $/1k tokens from char heuristic
    )

    if quiet:
        # A call that returned NOTHING is the one per-call signal worth a
        # warning even in quiet mode — we paid for it and got no spans.
        if spans_returned == 0 and input_chars > 0:
            _vcprint(
                data={
                    "provider": provider,
                    "model": model,
                    "purpose": purpose or "ner_extract",
                    "input_chars": input_chars,
                    "elapsed_ms": elapsed_ms,
                    "request_preview": _preview(text),
                },
                title=f"AI CALL → {provider} extraction (WARNING: 0 spans)",
                color="yellow",
                pretty=True,
            )
        completed = _bump_extraction_progress()
        if _EXTRACTION_PROGRESS_EVERY > 0 and completed % _EXTRACTION_PROGRESS_EVERY == 0:
            _print_extraction_progress()
        return

    _vcprint(
        data={
            "provider": provider,
            "model": model,
            "purpose": purpose or "ner_extract",
            "spans_returned": spans_returned,
            "input_chars": input_chars,
            "estimated_tokens": estimated_tokens,
            "estimated_cost_usd": estimated_cost,
            "elapsed_ms": elapsed_ms,
        },
        title=f"AI CALL → {provider} extraction (DONE)",
        color="green",
        pretty=True,
    )


__all__ = [
    "AICallTally",
    "RunCostCollector",
    "collect_run_costs",
    "announce_chat_call",
    "announce_embedding_call",
    "announce_extraction_call",
    "print_tally_summary",
    "record_chat_call",
    "record_secret_redaction",
    "tally_reset",
    "tally_snapshot",
]
