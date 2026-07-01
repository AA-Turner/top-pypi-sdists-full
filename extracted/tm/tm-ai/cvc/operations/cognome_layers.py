"""
cvc.operations.cognome_layers — L2 (semantic re-rank) and L3 (overflow
compression) of the COGNOME stack.

Both layers are **additive refinements** on top of L1's heuristic
selection.  If either fails, misbehaves, or is disabled, L1 still
produces a correct Engram.  This is a hard design contract — memory
quality may degrade gracefully; memory correctness never breaks.

Design properties
-----------------
* **Pure Python, zero LLM cost.**  Neither layer calls an LLM on the
  hot path.  They run in microseconds on the CPU.
* **Deterministic.**  Same inputs ⇒ same outputs.  Preserves the
  L1 property that identical DAG state + query ⇒ byte-identical Engram.
* **Budget-respecting.**  L3 never pushes the total token cost past
  the caller's budget; it uses a dedicated compression reserve carved
  out *inside* the budget.
* **Automatic.**  Both layers are on by default (``cognome_l2_enabled``
  and ``cognome_l3_enabled`` in ``CVCConfig``).  The developer never
  toggles them.
"""

from __future__ import annotations

import logging
import re
from typing import Iterable

from cvc.operations.cognome import Noeme, estimate_tokens

logger = logging.getLogger("cvc.operations.cognome_layers")


# ---------------------------------------------------------------------------
# L2 — Semantic re-ranker (noeme granularity)
# ---------------------------------------------------------------------------

_BIGRAM_WEIGHT = 2.0
_UNIGRAM_WEIGHT = 1.0
_L2_BOOST = 0.6  # How strongly the semantic signal shifts L1's score.

_WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{1,}")


def _tokens(text: str) -> list[str]:
    return [m.group(0).lower() for m in _WORD_RE.finditer(text or "")]


def _bigrams(tokens: list[str]) -> set[tuple[str, str]]:
    return set(zip(tokens, tokens[1:])) if len(tokens) >= 2 else set()


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    if inter == 0:
        return 0.0
    return inter / float(len(a | b))


class SemanticReranker:
    """
    Re-rank a list of noemata by noeme-level semantic similarity to the query.

    L1 scores at the *commit* level, so every noeme emitted from the same
    commit inherits the same semantic signal.  L2 breaks ties within a
    commit by looking at the noeme *text* itself — a commit may have a
    great summary but a poor tool-output noeme for the current query, and
    L2 deprioritises the latter.

    The implementation is purely lexical (unigram + bigram Jaccard) so it
    has zero runtime dependencies and runs in microseconds.  Quality is
    adequate for the "within-commit differentiation" job; the L1 semantic
    distance from ChromaDB still carries the heavy lifting at the
    commit-selection stage.
    """

    def __init__(self, boost: float = _L2_BOOST) -> None:
        self.boost = boost

    def rerank(self, noemata: list[Noeme], query: str) -> list[Noeme]:
        """Return a NEW list, scored and sorted high-to-low."""
        if not noemata or not query:
            return noemata
        q_tokens = _tokens(query)
        if not q_tokens:
            return noemata
        q_uni = set(q_tokens)
        q_bi = _bigrams(q_tokens)

        reranked: list[Noeme] = []
        for n in noemata:
            n_tokens = _tokens(n.text)
            uni_sim = _jaccard(q_uni, set(n_tokens))
            bi_sim = _jaccard(q_bi, _bigrams(n_tokens))
            sem = (_BIGRAM_WEIGHT * bi_sim + _UNIGRAM_WEIGHT * uni_sim) / (
                _BIGRAM_WEIGHT + _UNIGRAM_WEIGHT
            )
            # Multiplicative boost — L1's score still dominates.  The
            # L2 signal is a within-bucket tiebreaker.
            new_score = n.score * (1.0 + self.boost * sem)
            reranked.append(n.model_copy(update={"score": new_score}))

        reranked.sort(key=lambda n: (-n.score, n.source_commit, n.kind))
        return reranked


# ---------------------------------------------------------------------------
# L3 — Extractive overflow compressor
# ---------------------------------------------------------------------------

_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+|\n+")
_MIN_SENTENCE_LEN = 12
_MAX_SENTENCES_PER_NOEME = 8


def _split_sentences(text: str) -> list[str]:
    out: list[str] = []
    for piece in _SENTENCE_RE.split(text or ""):
        piece = piece.strip()
        if len(piece) >= _MIN_SENTENCE_LEN:
            out.append(piece)
        if len(out) >= _MAX_SENTENCES_PER_NOEME:
            break
    return out


def _sentence_score(sentence: str, query_tokens: set[str]) -> float:
    if not query_tokens:
        return 0.0
    s_tokens = set(_tokens(sentence))
    if not s_tokens:
        return 0.0
    inter = len(query_tokens & s_tokens)
    if inter == 0:
        return 0.0
    # Prefer short information-dense sentences.
    density = inter / float(len(s_tokens))
    recall = inter / float(len(query_tokens))
    return recall + 0.5 * density


class ExtractiveOverflowCompressor:
    """
    Collapse budget-overflow noemata into ONE compressed noeme.

    Operates after L1+L2 have already selected the top noemata that fit
    in the main budget.  The remaining (overflow) noemata would otherwise
    be dropped outright.  L3 instead extracts the highest-scoring
    sentences from the overflow pool, fits them into a small reserved
    compression budget, and emits the result as a single synthetic
    noeme tagged ``kind="summary"``.

    Why extractive, not LLM-based?
      * **Determinism** — identical inputs ⇒ identical outputs, keeps the
        Engram hash stable and cacheable.
      * **Zero cost** — never burns user tokens or credits.
      * **Zero latency** — runs in microseconds; does not block the turn.
      * **Safe** — cannot hallucinate because it only concatenates
        verbatim sentences from the dropped noemata.

    The result is a single :class:`Noeme` with ``source_commit`` set to
    a stable aggregate key so downstream hashing stays deterministic.
    """

    def compress(
        self,
        overflow: Iterable[Noeme],
        *,
        query: str,
        compression_budget_tokens: int,
    ) -> Noeme | None:
        if compression_budget_tokens <= 0:
            return None
        overflow_list = list(overflow)
        if not overflow_list:
            return None

        query_tokens = set(_tokens(query))

        # Collect scored sentences from all dropped noemata.
        scored: list[tuple[float, str, str]] = []  # (score, sentence, source_commit)
        for n in overflow_list:
            for sent in _split_sentences(n.text):
                sc = _sentence_score(sent, query_tokens)
                if sc <= 0:
                    # Low-signal sentence — keep a dampened floor so
                    # short overflow pools still contribute.
                    sc = 0.0001
                scored.append((sc, sent, n.source_commit))

        if not scored:
            return None

        # Sort by score desc, then sentence asc for determinism.
        scored.sort(key=lambda t: (-t[0], t[1]))

        # Greedy pack into the compression budget.
        picked: list[tuple[str, str]] = []
        total = 0
        for _score, sent, src in scored:
            t = estimate_tokens(sent)
            if total + t > compression_budget_tokens:
                continue
            picked.append((sent, src))
            total += t
            if total >= compression_budget_tokens:
                break

        if not picked:
            return None

        # Build a compact summary text.  Include the source-commit
        # prefixes so the render function still surfaces provenance
        # (via the NOTE prefix applied by Noeme.render()).
        body_parts = []
        sources: list[str] = []
        for sent, src in picked:
            body_parts.append(f"{src[:8]}: {sent}")
            sources.append(src)
        text = " | ".join(body_parts)

        # Use a stable synthetic source_commit so Engram hashes are
        # deterministic across runs — pick the earliest source hash.
        agg_source = min(sources)

        return Noeme(
            source_commit=agg_source,
            kind="summary",
            text=f"(compressed from {len(overflow_list)}) {text}",
            score=0.0,  # already budgeted, ordering irrelevant
            token_estimate=estimate_tokens(text),
        )


# ---------------------------------------------------------------------------
# No-op fallbacks (for tests / disabled layers)
# ---------------------------------------------------------------------------


class NoopReranker(SemanticReranker):
    def rerank(self, noemata: list[Noeme], query: str) -> list[Noeme]:  # noqa: ARG002
        return noemata


class NoopCompressor(ExtractiveOverflowCompressor):
    def compress(
        self,
        overflow: Iterable[Noeme],  # noqa: ARG002
        *,
        query: str,  # noqa: ARG002
        compression_budget_tokens: int,  # noqa: ARG002
    ) -> Noeme | None:
        return None
