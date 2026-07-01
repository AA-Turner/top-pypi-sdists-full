"""
cvc.operations.cognome — L1 of the COGNOME substrate ("the smart librarian").

The COGNOME replaces the .md-file memory paradigm used by every current agent
framework (Claude Code's ``CLAUDE.md``, Cursor rules, OpenHands/upstream
scratchpads, Letta memory blocks, Mem0 fact graphs).  Those systems all share
one flaw: memory grows as text and is re-injected into every prompt, so the
token bill scales with history.

COGNOME inverts that: instead of sending *everything we have* and hoping the
LLM picks out what it needs, we **compile** a minimal, query-specific
*Engram* — a tightly formatted snippet carrying only the noemata (facts,
distilled summaries, file provenance, tool-output excerpts) that the current
intent actually requires.  The resulting string is tiny (typically a few
hundred tokens) and rides on CVC's existing provider-level prompt-cache
headers, so the second turn on the same topic is effectively free.

This module implements **Layer 1 (L1) only**: pure heuristic compilation.
No neural net, no training, no LLM call.  It is deterministic, runs on
every request on the CPU in sub-millisecond time, and produces real token
savings on day one.  L2 (a tiny learned soft-prompt trained during idle
time) and L3 (optional GPU LoRA) are explicitly *not* part of this module
— they will be introduced as additive heads that refine L1's selection
without replacing it, so L1 is the lasting foundation.

Design principles
-----------------
* **Deterministic.** Same DAG state + same query + same budget ⇒ byte-for-byte
  identical Engram.  Enables CAS-style caching and reproducibility audits.
* **Budgeted.** Every Engram has a hard token ceiling.  We never silently
  overflow; we drop the lowest-scoring noemata.
* **Provenance-preserved.** Every Engram carries the list of source commit
  hashes it was distilled from, so an agent action can always be traced
  back through the Merkle DAG.
* **Provider-agnostic.** The Engram is a plain string plus metadata.  The
  existing adapters decide how to inject it (cache-controlled system block,
  cached prefix, prepended user turn, etc.).
"""

from __future__ import annotations

import hashlib
import logging
import re
import time
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from cvc.core.database import ContextDatabase

logger = logging.getLogger("cvc.operations.cognome")


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Rough token estimator: 1 token ≈ 4 characters for English / code.  This is
# deliberately pessimistic (slightly overestimates) so a budget of N tokens
# never produces an Engram that actually exceeds N tokens at the provider.
_CHARS_PER_TOKEN = 4

# How many candidate commits we fetch from Tier 3 / Tier 1 before scoring.
# Higher = better recall, marginally more CPU.  5x final budget is plenty.
_CANDIDATE_MULTIPLIER = 5
_MIN_CANDIDATES = 8
_MAX_CANDIDATES = 64

# Scoring weights (heuristic, tuned for coding-agent traffic).
_W_SEMANTIC = 1.0  # Vector-store distance signal
_W_KEYWORD = 0.6  # Literal term overlap in commit message / summary
_W_RECENCY = 0.25  # Exponential decay on age
_W_TYPE_BONUS = 0.15  # Bonus for high-value commit types
_RECENCY_HALFLIFE_S = 7 * 24 * 3600.0  # One week

# Commit types that typically carry the most reusable cognition.
_HIGH_VALUE_TYPES = frozenset(
    {
        "analysis",
        "distillation",
        "generation",
        "merge",
        "anchor",
    }
)

# Stopwords stripped from the keyword-overlap score.  Short list on purpose —
# code identifiers like "id", "is", "to" are often meaningful tokens.
_STOPWORDS = frozenset(
    {
        "the",
        "a",
        "an",
        "and",
        "or",
        "of",
        "in",
        "on",
        "at",
        "for",
        "with",
        "how",
        "what",
        "why",
        "when",
        "where",
        "which",
        "do",
        "does",
        "did",
        "my",
        "our",
        "this",
        "that",
        "these",
        "those",
        "i",
        "we",
        "you",
    }
)

# Noise patterns — commit messages matching these are low-value boilerplate
# that wastes token budget.  Compiled once at import time.
_NOISE_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, re.IGNORECASE)
    for p in (
        r"^session end at turn \d+$",
        r"^auto-checkpoint at turn \d+$",
        r"^manual checkpoint at turn \d+$",
        r"^genesis\b",
        r"^telepathic tool sync:",
        r"^raw output of \w+",
        r"^smart compaction:",
        r"^restored to [0-9a-f]+:",
    )
)


def estimate_tokens(text: str) -> int:
    """Cheap, conservative token estimate — no tokenizer dependency."""
    if not text:
        return 0
    return max(1, (len(text) + _CHARS_PER_TOKEN - 1) // _CHARS_PER_TOKEN)


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


class Noeme(BaseModel):
    """
    One addressable atom of compiled cognition.

    A Noeme is the smallest unit the compiler emits into an Engram.  It is
    not a Merkle node itself — it is a *projection* of one commit (or a
    fragment of one) filtered and scored against the current query.
    """

    source_commit: str  # full SHA-256 of the commit this came from
    kind: str  # 'message' | 'summary' | 'reasoning' | 'tool'
    text: str
    score: float = 0.0
    token_estimate: int = 0

    def render(self) -> str:
        """Return the Engram-ready string form (single line prefix + body)."""
        prefix = {
            "summary": "SUMMARY",
            "message": "NOTE",
            "reasoning": "THOUGHT",
            "tool": "TOOL",
        }.get(self.kind, "NOTE")
        return f"[{prefix} {self.source_commit[:8]}] {self.text}"


class CompiledEngram(BaseModel):
    """
    The compiled output handed to an adapter.

    An Engram is provider-agnostic: it's a plain string plus metadata.  The
    adapter decides whether to inject it as a cached system block (Anthropic),
    a ``store: true`` prefix (OpenAI), or a ``cachedContent`` block (Gemini).
    """

    preamble: str  # the string to prepend to the prompt
    query: str  # the query that produced this Engram
    source_commits: list[str] = Field(default_factory=list)
    noeme_count: int = 0
    token_estimate: int = 0  # tokens in `preamble`
    baseline_token_estimate: int = 0  # what the raw full context would cost
    compression_ratio: float = 0.0  # 1 - tokens/baseline, clamped to [0, 1]
    budget_tokens: int = 0
    engram_hash: str = ""  # sha256(preamble) — stable cache key
    created_at: float = Field(default_factory=time.time)

    def cache_key(self) -> str:
        """Stable identifier suitable for use as a prompt-cache handle."""
        return self.engram_hash


# ---------------------------------------------------------------------------
# Compiler
# ---------------------------------------------------------------------------


class CognomeCompiler:
    """
    Heuristic context compiler — L1 of the COGNOME stack.

    The compiler takes a natural-language *query* and a *budget* in tokens,
    and returns a :class:`CompiledEngram` containing the highest-scoring
    noemata from the Merkle DAG that fit within the budget.

    This class is intentionally **stateless** with respect to the workspace
    — every call reads the current DAG fresh through the provided
    :class:`ContextDatabase`.  Callers that need caching should hash the
    returned :attr:`CompiledEngram.engram_hash`.
    """

    def __init__(
        self,
        db: ContextDatabase,
        *,
        default_budget_tokens: int = 1200,
        enable_l2: bool = True,
        enable_l3: bool = True,
        l3_overflow_fraction: float = 0.15,
    ) -> None:
        self.db = db
        self.default_budget_tokens = default_budget_tokens
        # L2/L3 are additive refiners — see cognome_layers for contract.
        # Imported locally to avoid a circular dependency at module load.
        from cvc.operations.cognome_layers import (
            ExtractiveOverflowCompressor,
            NoopCompressor,
            NoopReranker,
            SemanticReranker,
        )

        self._l2 = SemanticReranker() if enable_l2 else NoopReranker()
        self._l3 = ExtractiveOverflowCompressor() if enable_l3 else NoopCompressor()
        self._l3_overflow_fraction = max(0.0, min(0.5, l3_overflow_fraction))

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def compile(
        self,
        query: str,
        *,
        budget_tokens: int | None = None,
        branch: str | None = None,
        max_candidates: int | None = None,
    ) -> CompiledEngram:
        """
        Produce an Engram for *query* under *budget_tokens*.

        Parameters
        ----------
        query:
            Natural language intent of the upcoming LLM turn.
        budget_tokens:
            Hard ceiling on the Engram's token cost.  The compiler will drop
            the lowest-scoring noemata until the total fits.  Defaults to
            :attr:`default_budget_tokens`.
        branch:
            If set, restricts candidate commits to this branch's ancestry.
        max_candidates:
            Upper bound on how many commits to score before truncating to
            budget.  Defaults to an adaptive value based on budget.
        """
        budget = budget_tokens if budget_tokens is not None else self.default_budget_tokens
        if budget <= 0:
            return _empty_engram(query, budget)

        n_candidates = max_candidates or _adaptive_candidate_count(budget)
        candidates = self._gather_candidates(query, n_candidates, branch)
        if not candidates:
            return _empty_engram(query, budget)

        query_terms = _keyword_tokens(query)
        now = time.time()
        noemata: list[Noeme] = []
        for cand in candidates:
            noemata.extend(self._noemata_for(cand, query_terms, now))

        # Sort high-score first, then stable tiebreak on commit hash for
        # deterministic Engram hashes across runs.
        noemata.sort(key=lambda n: (-n.score, n.source_commit, n.kind))

        # --- L2: semantic re-rank at noeme granularity ------------------
        # Additive refinement on top of the L1 commit-level scoring.
        # Gracefully degrades to a noop if anything goes wrong.
        try:
            noemata = self._l2.rerank(noemata, query)
        except Exception as exc:  # pragma: no cover — defensive
            logger.debug("cognome L2 rerank failed (non-fatal): %s", exc)

        # Fit-to-budget: greedily accept noemata until we hit the ceiling.
        # We reserve a small header allowance up-front, then re-measure the
        # fully rendered preamble at the end and drop trailing noemata if
        # the real token count still exceeds budget (defensive — the
        # per-noeme estimate can undercount by a token or two).
        baseline_tokens = sum(n.token_estimate for n in noemata)
        header_reserve = estimate_tokens(_render_preamble(query, []))
        # L3 reservation: carve out a slice of the budget for an overflow
        # summary.  Only applied if there actually is overflow; otherwise
        # the reservation is reclaimed by a second-pass fill below.
        compression_reserve = int(max(0, budget - header_reserve) * self._l3_overflow_fraction)
        effective_budget = max(0, budget - header_reserve - compression_reserve)
        selected: list[Noeme] = []
        running = 0
        cutoff_idx = 0
        for i, n in enumerate(noemata):
            if running + n.token_estimate > effective_budget:
                cutoff_idx = i
                continue
            selected.append(n)
            running += n.token_estimate
            cutoff_idx = i + 1
            if running >= effective_budget:
                break

        # --- L3: extractive compression of the overflow tail ------------
        overflow = noemata[cutoff_idx:]
        compressed_noeme: Noeme | None = None
        if overflow and compression_reserve > 0:
            try:
                compressed_noeme = self._l3.compress(
                    overflow,
                    query=query,
                    compression_budget_tokens=compression_reserve,
                )
            except Exception as exc:  # pragma: no cover — defensive
                logger.debug("cognome L3 compress failed (non-fatal): %s", exc)
                compressed_noeme = None

        if compressed_noeme is not None and compressed_noeme.token_estimate > 0:
            selected.append(compressed_noeme)
            running += compressed_noeme.token_estimate
        else:
            # No overflow — reclaim the reserved compression budget by
            # greedily filling in more of the tail.  Keeps L3 purely
            # additive (never shrinks the non-overflow case).
            for n in noemata[len(selected) :]:
                if running + n.token_estimate > effective_budget + compression_reserve:
                    continue
                selected.append(n)
                running += n.token_estimate

        preamble = _render_preamble(query, selected)
        preamble_tokens = estimate_tokens(preamble)
        # Hard ceiling — pop the lowest-scoring noemata if we still overshoot.
        while preamble_tokens > budget and selected:
            selected.pop()
            preamble = _render_preamble(query, selected)
            preamble_tokens = estimate_tokens(preamble)
        compression = 0.0
        if baseline_tokens > 0:
            compression = max(0.0, min(1.0, 1.0 - preamble_tokens / baseline_tokens))

        source_commits = sorted({n.source_commit for n in selected})
        engram_hash = hashlib.sha256(preamble.encode("utf-8")).hexdigest()

        logger.debug(
            "cognome compile: query=%r budget=%d noemata=%d/%d tokens=%d/%d ratio=%.2f",
            query,
            budget,
            len(selected),
            len(noemata),
            preamble_tokens,
            baseline_tokens,
            compression,
        )

        return CompiledEngram(
            preamble=preamble,
            query=query,
            source_commits=source_commits,
            noeme_count=len(selected),
            token_estimate=preamble_tokens,
            baseline_token_estimate=baseline_tokens,
            compression_ratio=compression,
            budget_tokens=budget,
            engram_hash=engram_hash,
        )

    # ------------------------------------------------------------------
    # Candidate gathering
    # ------------------------------------------------------------------

    def _gather_candidates(
        self,
        query: str,
        n_candidates: int,
        branch: str | None,
    ) -> list[dict[str, Any]]:
        """
        Return up to *n_candidates* commit dicts ranked by preliminary
        relevance.  Uses Tier 3 vector search when available, falls back
        to recent-commit scan on the index.
        """
        out: dict[str, dict[str, Any]] = {}

        # Primary: semantic search (if ChromaDB is available).
        try:
            results = self.db.search_conversations(query, limit=n_candidates, deep=False)
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("cognome: semantic search failed (%s); using recency fallback", exc)
            results = []

        for r in results:
            ch = r.get("commit_hash")
            if not ch:
                continue
            out[ch] = r

        # Fallback / supplement: most recent commits on the active branch.
        # This guarantees that a cold workspace (empty vector store) still
        # gets useful candidates.
        if len(out) < n_candidates:
            try:
                recent = self.db.index.list_commits(branch=branch, limit=n_candidates * 2)
            except TypeError:
                recent = self.db.index.list_commits(limit=n_candidates * 2)
            for c in recent:
                if c.commit_hash in out:
                    continue
                out[c.commit_hash] = {
                    "commit_hash": c.commit_hash,
                    "short_hash": c.commit_hash[:12],
                    "message": c.message,
                    "timestamp": c.metadata.timestamp,
                    "provider": c.metadata.provider or "",
                    "model": c.metadata.model or "",
                    "commit_type": c.commit_type.value,
                    "relevance_source": "recency",
                    "distance": 1.0,
                }
                if len(out) >= n_candidates:
                    break

        return list(out.values())

    # ------------------------------------------------------------------
    # Per-commit noemata extraction + scoring
    # ------------------------------------------------------------------

    def _noemata_for(
        self,
        cand: dict[str, Any],
        query_terms: set[str],
        now: float,
    ) -> list[Noeme]:
        """Project a candidate commit into zero or more scored Noemes."""
        ch = cand.get("commit_hash") or ""
        if not ch:
            return []

        ts = float(cand.get("timestamp") or 0.0)
        ctype = str(cand.get("commit_type") or "").lower()
        distance = float(cand.get("distance") or 1.0)

        # Base score components.
        semantic_score = _W_SEMANTIC * (1.0 / (1.0 + max(0.0, distance)))
        recency_score = _W_RECENCY * _recency_weight(now, ts)
        type_bonus = _W_TYPE_BONUS if ctype in _HIGH_VALUE_TYPES else 0.0

        results: list[Noeme] = []

        # 1. Commit message itself is always a candidate Noeme.
        msg = (cand.get("message") or "").strip()
        if msg and not _is_noise(msg):
            kw = _W_KEYWORD * _keyword_overlap(msg, query_terms)
            score = semantic_score + kw + recency_score + type_bonus
            text = _truncate(msg, 240)
            results.append(
                Noeme(
                    source_commit=ch,
                    kind="message",
                    text=text,
                    score=score,
                    token_estimate=estimate_tokens(text) + 4,  # header overhead
                )
            )

        # 2. Distilled summary (if the blob carries one) — these are the
        # highest-value noemata by design.
        summary = self._load_summary(ch)
        if summary:
            kw = _W_KEYWORD * _keyword_overlap(summary, query_terms)
            score = semantic_score + kw + recency_score + type_bonus + 0.2
            text = _truncate(summary, 480)
            results.append(
                Noeme(
                    source_commit=ch,
                    kind="summary",
                    text=text,
                    score=score,
                    token_estimate=estimate_tokens(text) + 4,
                )
            )

        # 3. Query-matching excerpts from the deep-search hits, if present.
        for mm in cand.get("matching_messages", [])[:2]:
            body = (mm.get("content") or "").strip()
            if not body or _is_noise(body):
                continue
            kw = _W_KEYWORD * _keyword_overlap(body, query_terms)
            # Excerpts already passed a relevance filter upstream — weight
            # keyword overlap a bit higher here.
            score = semantic_score * 0.7 + kw * 1.2 + recency_score * 0.5
            text = _truncate(body, 360)
            results.append(
                Noeme(
                    source_commit=ch,
                    kind="message",
                    text=text,
                    score=score,
                    token_estimate=estimate_tokens(text) + 4,
                )
            )

        return results

    def _load_summary(self, commit_hash: str) -> str | None:
        """Fetch ``content_blob.distilled_summary`` if it exists on disk."""
        try:
            blob = self.db.retrieve_blob(commit_hash)
        except Exception:
            return None
        if blob is None:
            return None
        summary = getattr(blob, "distilled_summary", None)
        if summary and isinstance(summary, str) and summary.strip():
            return summary.strip()
        return None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]+")


def _is_noise(text: str) -> bool:
    """Return True if *text* matches a known low-value boilerplate pattern."""
    stripped = " ".join(text.split())  # collapse whitespace
    return any(p.search(stripped) for p in _NOISE_PATTERNS)


def _keyword_tokens(text: str) -> set[str]:
    """Lowercase identifier / word tokens minus stopwords."""
    return {
        t.lower()
        for t in _WORD_RE.findall(text or "")
        if len(t) > 1 and t.lower() not in _STOPWORDS
    }


def _keyword_overlap(text: str, query_terms: set[str]) -> float:
    if not query_terms:
        return 0.0
    terms = _keyword_tokens(text)
    if not terms:
        return 0.0
    hits = len(terms & query_terms)
    if hits == 0:
        return 0.0
    # Overlap fraction over query side — rewards covering the query more
    # than flooding the response with unrelated tokens.
    return hits / len(query_terms)


def _recency_weight(now: float, ts: float) -> float:
    if ts <= 0:
        return 0.0
    age = max(0.0, now - ts)
    # Exponential decay with a one-week half-life.
    return 0.5 ** (age / _RECENCY_HALFLIFE_S)


def _truncate(text: str, max_chars: int) -> str:
    text = " ".join(text.split())  # collapse whitespace
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "…"


def _adaptive_candidate_count(budget_tokens: int) -> int:
    approx = budget_tokens // 40  # rough # of noemata that could fit
    approx *= _CANDIDATE_MULTIPLIER
    return max(_MIN_CANDIDATES, min(_MAX_CANDIDATES, approx))


def _render_preamble(query: str, noemata: list[Noeme]) -> str:
    if not noemata:
        return ""
    lines = [
        "# COGNOME Engram (L1)",
        f"# query: {_truncate(query, 200)}",
        f"# noemata: {len(noemata)}",
        "",
    ]
    lines.extend(n.render() for n in noemata)
    return "\n".join(lines)


def _empty_engram(query: str, budget: int) -> CompiledEngram:
    return CompiledEngram(
        preamble="",
        query=query,
        source_commits=[],
        noeme_count=0,
        token_estimate=0,
        baseline_token_estimate=0,
        compression_ratio=0.0,
        budget_tokens=max(0, budget),
        engram_hash=hashlib.sha256(b"").hexdigest(),
    )
