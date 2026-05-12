"""Small-model strategy helpers (C9).

Local 3B-7B models lose accuracy with long histories or unranked retrieval.
This module provides two cheap, deterministic helpers the engine can call
to give those models a fairer chance at the task:

  - `compress_history(messages, budget_chars)` — keeps recent turns
    verbatim, collapses older history into a single summary message. No
    model call, no API dependency.

  - `rerank_by_relevance(query, snippets, top_k)` — ranks retrieval hits
    by simple lexical overlap with the query. The simplest thing that
    works without a re-ranker model. Drop-in for `RAGIndex` results.

Both are pure functions, easy to test, no I/O. The engine can call them
unconditionally; they're no-ops when input is small enough.
"""

from __future__ import annotations

import re

from sage.providers.base import Message

__all__ = ["compress_history", "rerank_by_relevance"]


_KEEP_VERBATIM_PAIRS = 2  # always keep the last N user+assistant pairs verbatim
_WORD_RE = re.compile(r"[a-zA-Z0-9_]+")


def _total_chars(messages: list[Message]) -> int:
    return sum(len(getattr(m, "content", "") or "") for m in messages)


def compress_history(
    messages: list[Message],
    budget_chars: int,
) -> list[Message]:
    """Compress message history to fit within a character budget.

    Strategy:
      1. If the messages already fit, return them unchanged.
      2. Otherwise: keep the last K turns (user+assistant pairs) verbatim
         and replace everything older with a single summary message that
         lists the topics covered.

    The summary is intentionally short and structural — small models
    benefit more from "you've already discussed X, Y, Z" than from
    paraphrased dialogue snippets that hallucinate.
    """
    if not messages or _total_chars(messages) <= budget_chars:
        return list(messages)

    # Walk back from the end, accumulating until we've kept K user turns.
    keep_idx_from = len(messages)
    user_seen = 0
    for i in range(len(messages) - 1, -1, -1):
        keep_idx_from = i
        if messages[i].role == "user":
            user_seen += 1
            if user_seen >= _KEEP_VERBATIM_PAIRS:
                break

    older = messages[:keep_idx_from]
    recent = messages[keep_idx_from:]

    if not older:
        # Even the recent pairs exceed the budget; nothing to compress.
        return recent

    # Build a one-paragraph digest of the older turns. We capture the
    # user-asked topics rather than assistant text because the model
    # cares more about "what has the user already asked" than its own
    # prior outputs.
    topics: list[str] = []
    for m in older:
        if m.role != "user":
            continue
        head = (m.content or "").strip().split("\n", 1)[0]
        if len(head) > 80:
            head = head[:77].rstrip() + "..."
        if head:
            topics.append(head)
    if not topics:
        topics = ["(prior conversation, no user questions captured)"]

    summary_body = (
        "EARLIER CONVERSATION (compressed): the user previously asked about: "
        + " ; ".join(topics)
    )
    # Hard cap on summary length to enforce the budget downstream.
    max_summary = max(200, budget_chars // 3)
    if len(summary_body) > max_summary:
        summary_body = summary_body[:max_summary - 3].rstrip() + "..."
    summary = Message(role="system", content=summary_body)
    return [summary] + recent


def rerank_by_relevance(
    query: str,
    snippets: list[str],
    top_k: int = 5,
) -> list[str]:
    """Rank `snippets` by lexical overlap with `query`, return top_k.

    Empty query → no ranking signal, return input order (capped by top_k).
    Empty snippets → empty list.

    The ranker uses word-set overlap weighted by inverse document length —
    a snippet that shares many query words is preferred, but extremely
    long snippets aren't rewarded just for being long. No model call.
    """
    if not snippets:
        return []
    if not query.strip():
        return list(snippets[:top_k])

    qwords = {w.lower() for w in _WORD_RE.findall(query) if len(w) > 1}
    if not qwords:
        return list(snippets[:top_k])

    scored: list[tuple[float, int, str]] = []
    for i, s in enumerate(snippets):
        swords = {w.lower() for w in _WORD_RE.findall(s) if len(w) > 1}
        if not swords:
            scored.append((0.0, i, s))
            continue
        overlap = len(qwords & swords)
        # Length normalization: 1 / sqrt(len) keeps long snippets from dominating.
        score = overlap / (len(swords) ** 0.5)
        scored.append((score, i, s))
    # Sort descending by score; tie-break by original index for stability.
    scored.sort(key=lambda t: (-t[0], t[1]))
    return [s for _, _, s in scored[:top_k]]
