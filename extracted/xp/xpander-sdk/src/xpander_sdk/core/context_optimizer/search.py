"""In-process search over a decrypted offloaded result — keeps token usage down
by returning only the matching parts instead of the whole blob.

Both helpers run on plaintext already in the SDK process (post-decrypt in the
agno tool hook), so there is no network or model dependency. ``grep_text`` is a
line-oriented regex/substring filter; ``bm25_rank`` is a pure-Python lexical
ranker for natural-language queries.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import List

# BM25 chunking / scoring defaults — module constants so they stay tunable.
_CHUNK_CHARS = 512
_DEFAULT_TOP_N = 5
_BM25_K1 = 1.5
_BM25_B = 0.75

# Per-line snippet budget. A single-line JSON/CSV blob can be hundreds of KB, so
# a "matching line" must be clipped — otherwise a narrowing query returns the
# whole blob and defeats the search.
_MATCH_WINDOW_CHARS = 1_000


def _clip_line(line: str, budget: int = _MATCH_WINDOW_CHARS, focus=None) -> str:
    """Clip *line* to ~budget chars. With focus=(start, end) center on it (so the
    match stays visible wherever it sits in a giant line); else clip the head."""
    if len(line) <= budget:
        return line
    if focus is None:
        return line[:budget] + f" …[+{len(line) - budget:,} chars]"
    fs, fe = focus
    half = max(0, (budget - (fe - fs)) // 2)
    lo = max(0, fs - half)
    hi = min(len(line), lo + budget)
    lo = max(0, hi - budget)
    prefix = f"…[+{lo:,} chars] " if lo > 0 else ""
    suffix = f" …[+{len(line) - hi:,} chars]" if hi < len(line) else ""
    return prefix + line[lo:hi] + suffix

_RETRY_NUDGE = (
    "Call xpworkspace-context-retrieve again on the same context_id with a "
    "different/broader query, or omit both query and semantic_query for the full result."
)

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> List[str]:
    return _TOKEN_RE.findall(text.lower())


def grep_text(
    text: str,
    pattern: str,
    context_lines: int = 2,
    max_matches: int = 50,
) -> str:
    """Return lines of *text* matching *pattern* (regex, substring fallback) with context."""
    lines = text.splitlines()
    try:
        rx = re.compile(pattern)
        matcher = lambda ln: rx.search(ln) is not None  # noqa: E731
        span_of = lambda ln: (m := rx.search(ln)) and m.span() or None  # noqa: E731
    except re.error:
        needle = pattern.lower()
        matcher = lambda ln: needle in ln.lower()  # noqa: E731
        def span_of(ln):  # noqa: E306
            idx = ln.lower().find(needle)
            return (idx, idx + len(needle)) if idx != -1 else None

    hit_idxs = [i for i, ln in enumerate(lines) if matcher(ln)]
    total = len(hit_idxs)
    if total == 0:
        return (
            f"[SEARCH] no lines match query={pattern!r} "
            f"({len(text):,} chars searched). {_RETRY_NUDGE}"
        )

    shown = hit_idxs[:max_matches]
    blocks: List[str] = []
    for i in shown:
        lo = max(0, i - context_lines)
        hi = min(len(lines), i + context_lines + 1)
        # Clip every rendered line; center the matched line on the match offset.
        block = "\n".join(
            f"{n + 1}: {_clip_line(lines[n], focus=span_of(lines[n]) if n == i else None)}"
            for n in range(lo, hi)
        )
        blocks.append(block)

    capped = "" if total <= max_matches else f" (showing first {max_matches})"
    header = (
        f"[SEARCH] query={pattern!r}: {total} matching line(s){capped}. {_RETRY_NUDGE}"
    )
    return header + "\n\n" + "\n--\n".join(blocks)


def _chunk(text: str, size: int = _CHUNK_CHARS) -> List[str]:
    """Split into ~size-char chunks on paragraph boundaries where possible."""
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: List[str] = []
    buf = ""
    for p in paras:
        if len(buf) + len(p) + 2 <= size or not buf:
            buf = f"{buf}\n\n{p}" if buf else p
        else:
            chunks.append(buf)
            buf = p
        # A single oversized paragraph is hard-split so one chunk never dwarfs the rest.
        while len(buf) > size:
            chunks.append(buf[:size])
            buf = buf[size:]
    if buf.strip():
        chunks.append(buf)
    return chunks or [text]


def bm25_rank(text: str, query: str, top_n: int = _DEFAULT_TOP_N) -> str:
    """Return the *top_n* chunks of *text* most relevant to *query*, ranked by BM25."""
    chunks = _chunk(text)
    q_terms = set(_tokenize(query))
    if not q_terms or not chunks:
        return (
            f"[SEARCH] semantic_query={query!r}: nothing to rank. {_RETRY_NUDGE}"
        )

    tokenized = [_tokenize(c) for c in chunks]
    lengths = [len(t) for t in tokenized]
    avg_len = (sum(lengths) / len(lengths)) or 1.0
    n_chunks = len(chunks)

    df = Counter()
    for toks in tokenized:
        for term in set(toks) & q_terms:
            df[term] += 1
    idf = {
        term: math.log(1 + (n_chunks - df[term] + 0.5) / (df[term] + 0.5))
        for term in q_terms
    }

    scores: List[float] = []
    for toks, length in zip(tokenized, lengths):
        tf = Counter(toks)
        score = 0.0
        for term in q_terms:
            if term not in tf:
                continue
            freq = tf[term]
            denom = freq + _BM25_K1 * (1 - _BM25_B + _BM25_B * length / avg_len)
            score += idf[term] * (freq * (_BM25_K1 + 1)) / denom
        scores.append(score)

    ranked = sorted(range(n_chunks), key=lambda i: scores[i], reverse=True)
    top = [i for i in ranked if scores[i] > 0][:top_n]
    if not top:
        return (
            f"[SEARCH] semantic_query={query!r}: no relevant chunks "
            f"({n_chunks} chunks searched). {_RETRY_NUDGE}"
        )

    header = (
        f"[SEARCH] semantic_query={query!r}: top {len(top)} of {n_chunks} chunk(s) "
        f"by relevance. {_RETRY_NUDGE}"
    )
    body = "\n--\n".join(chunks[i].strip() for i in top)
    return header + "\n\n" + body
