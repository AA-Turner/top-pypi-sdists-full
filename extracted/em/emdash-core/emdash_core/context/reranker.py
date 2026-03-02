"""Re-ranker for filtering context items by query relevance.

Uses a lightweight scoring system based on:
1. Text matching (query terms vs entity names/paths/descriptions)
2. Graph signals (pagerank, betweenness centrality)
3. Session signals (recency, touch frequency)
4. Longevity signals (items that keep appearing are important)
5. File co-occurrence (files with multiple entities get boosted)

This reranker requires zero external ML dependencies and runs in <10ms.
"""

import os
from typing import Optional

from .models import ContextItem
from .simple_reranker import simple_rerank_items, get_simple_rerank_scores
from ..utils.logger import log


def rerank_context_items(
    items: list[ContextItem],
    query: str,
    top_k: Optional[int] = None,
    top_percent: Optional[float] = None,
    connection=None,
) -> list[ContextItem]:
    """Re-rank context items by relevance to query.

    Args:
        items: List of context items to re-rank
        query: The user's query/task description
        top_k: Keep top K items (default from env: CONTEXT_RERANK_TOP_K=20)
        top_percent: Keep top N% items (overrides top_k if set)
        connection: Optional Kuzu connection for graph-based scoring

    Returns:
        Filtered and sorted list of context items (most relevant first)
    """
    if not items:
        return items

    if not query or not query.strip():
        log.debug("No query provided for re-ranking, returning original items")
        return items

    # Check if re-ranking is enabled
    if os.getenv("CONTEXT_RERANK_ENABLED", "true").lower() != "true":
        log.debug("Context re-ranking disabled via CONTEXT_RERANK_ENABLED")
        return items

    # Determine effective top_k
    if top_percent is not None:
        effective_top_k = max(1, int(len(items) * top_percent))
    elif top_k is not None:
        effective_top_k = min(top_k, len(items))
    else:
        effective_top_k = int(os.getenv("CONTEXT_RERANK_TOP_K", "20"))

    return simple_rerank_items(
        items=items,
        query=query,
        connection=connection,
        top_k=effective_top_k,
    )


def get_rerank_scores(
    items: list[ContextItem],
    query: str,
    connection=None,
) -> list[tuple[ContextItem, float]]:
    """Get re-rank scores for context items without filtering.

    Useful for debugging and analysis.

    Args:
        items: List of context items
        query: Query to score against
        connection: Optional Kuzu connection for graph signals

    Returns:
        List of (item, score) tuples sorted by score descending
    """
    if not items or not query:
        return [(item, 0.0) for item in items]

    scored = get_simple_rerank_scores(items, query, connection)
    # Return without component breakdown
    return [(item, score) for item, score, _ in scored]
