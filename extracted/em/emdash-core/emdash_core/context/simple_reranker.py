"""Simple re-ranker for context items - no ML dependencies.

A lightweight alternative to the cross-encoder reranker that uses:
1. Text matching (query terms vs entity names/paths/descriptions)
2. Graph signals (pagerank, betweenness centrality)
3. Session signals (recency, touch frequency)
4. Longevity signals (items that keep appearing are important)

This reranker requires zero external dependencies and runs in <10ms.
"""

import math
import os
import re
from datetime import datetime
from typing import Optional

from .models import ContextItem
from .longevity import get_longevity_score, record_reranked_items
from ..utils.logger import log


# ============================================================================
# Tokenization
# ============================================================================

# Common code stopwords to filter out
CODE_STOPWORDS = frozenset({
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "need", "dare",
    "ought", "used", "to", "of", "in", "for", "on", "with", "at", "by",
    "from", "as", "into", "through", "during", "before", "after", "above",
    "below", "between", "under", "again", "further", "then", "once",
    "and", "but", "or", "nor", "so", "yet", "both", "either", "neither",
    "not", "only", "own", "same", "than", "too", "very", "just",
    "get", "set", "init", "self", "cls", "this", "that", "these", "those",
    "def", "class", "function", "method", "return", "import", "from",
    "if", "else", "elif", "try", "except", "finally", "raise", "assert",
    "for", "while", "break", "continue", "pass", "lambda", "yield",
    "true", "false", "none", "null", "undefined",
})

# Regex for splitting code identifiers
SPLIT_PATTERN = re.compile(r'[._/\\:\-\s]+|(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])')


def tokenize(text: str) -> set[str]:
    """Tokenize text into normalized terms for matching.

    Handles:
    - camelCase: "getUserName" -> {"get", "user", "name"}
    - snake_case: "get_user_name" -> {"get", "user", "name"}
    - paths: "src/auth/service.py" -> {"src", "auth", "service", "py"}

    Args:
        text: Text to tokenize

    Returns:
        Set of lowercase tokens (stopwords removed)
    """
    if not text:
        return set()

    # Split by common delimiters and camelCase boundaries
    # Important: split BEFORE lowercasing to preserve camelCase boundaries
    tokens = SPLIT_PATTERN.split(text)

    # Lowercase and filter: non-empty, not stopwords, length > 1
    return {
        token.lower() for token in tokens
        if token and len(token) > 1 and token.lower() not in CODE_STOPWORDS
    }


def tokenize_query(query: str) -> set[str]:
    """Tokenize a user query, preserving important terms.

    Less aggressive filtering than code tokenization.
    """
    if not query:
        return set()

    # Simple word split for queries
    words = re.split(r'\s+', query.lower())

    # Also split camelCase/snake_case if present
    tokens = set()
    for word in words:
        tokens.update(SPLIT_PATTERN.split(word))

    # Filter but keep more terms (queries are short)
    return {token for token in tokens if token and len(token) > 1}


# ============================================================================
# Scoring Functions
# ============================================================================

def text_match_score(query_tokens: set[str], item: ContextItem) -> float:
    """Score based on query term overlap with entity text.

    Args:
        query_tokens: Pre-tokenized query terms
        item: Context item to score

    Returns:
        Score between 0.0 and 1.0
    """
    if not query_tokens:
        return 0.0

    # Tokenize item fields
    name_tokens = tokenize(item.qualified_name)
    path_tokens = tokenize(item.file_path) if item.file_path else set()
    desc_tokens = tokenize(item.description) if item.description else set()

    # Calculate overlap ratios
    query_size = len(query_tokens)

    # Name matches are most important
    name_overlap = len(query_tokens & name_tokens)
    name_score = name_overlap / query_size if query_size else 0

    # Boost for exact substring match in name
    name_lower = item.qualified_name.lower()
    exact_boost = 0.0
    for token in query_tokens:
        if token in name_lower:
            exact_boost += 0.1
    exact_boost = min(0.3, exact_boost)  # Cap at 0.3

    # Path matches
    path_overlap = len(query_tokens & path_tokens)
    path_score = path_overlap / query_size if query_size else 0

    # Description matches
    desc_overlap = len(query_tokens & desc_tokens)
    desc_score = desc_overlap / query_size if query_size else 0

    # Weighted combination
    score = (
        name_score * 0.50 +
        exact_boost +
        path_score * 0.15 +
        desc_score * 0.05
    )

    return min(1.0, score)


def graph_boost_score(
    item: ContextItem,
    connection=None,
    _cache: dict = {},
) -> float:
    """Score based on graph centrality metrics.

    Uses pagerank and betweenness centrality from the graph database.
    Results are cached per qualified_name to avoid repeated queries.

    Args:
        item: Context item to score
        connection: Kuzu database connection (optional)

    Returns:
        Score between 0.0 and 1.0
    """
    if connection is None:
        return 0.0

    qname = item.qualified_name

    # Check cache
    if qname in _cache:
        return _cache[qname]

    try:
        # Determine node table from entity type
        entity_type = item.entity_type
        if entity_type not in ("Function", "Class", "File"):
            _cache[qname] = 0.0
            return 0.0

        # Query for centrality metrics
        conn = connection.connect()

        if entity_type == "File":
            # Files use path as key
            query = f"""
                MATCH (n:File {{path: $path}})
                RETURN n.commit_importance, n.commit_count
            """
            result = conn.execute(query, {"path": item.file_path or qname})
        else:
            # Functions/Classes use qualified_name
            query = f"""
                MATCH (n:{entity_type} {{qualified_name: $qname}})
                RETURN n.pagerank, n.betweenness
            """
            result = conn.execute(query, {"qname": qname})

        if result.has_next():
            row = result.get_next()
            val1 = row[0] or 0.0
            val2 = row[1] or 0.0

            if entity_type == "File":
                # For files: use commit importance and count
                score = min(1.0, val1 * 0.5 + (val2 / 100) * 0.5)
            else:
                # For functions/classes: pagerank + betweenness
                # Normalize assuming pagerank max ~0.1, betweenness max ~0.5
                score = min(1.0, val1 * 5 + val2 * 1)

            _cache[qname] = score
            return score

        _cache[qname] = 0.0
        return 0.0

    except Exception as e:
        log.debug(f"Graph boost query failed for {qname}: {e}")
        _cache[qname] = 0.0
        return 0.0


def session_boost_score(item: ContextItem, now: Optional[datetime] = None) -> float:
    """Score based on session activity signals.

    Args:
        item: Context item to score
        now: Current time (for testing)

    Returns:
        Score between 0.0 and 1.0
    """
    if now is None:
        now = datetime.now()

    # Recency score: very slow decay (half-life = 48 hours = 2880 minutes)
    recency = 0.0
    if item.last_touched:
        age_seconds = (now - item.last_touched).total_seconds()
        age_minutes = max(0, age_seconds / 60)
        recency = math.exp(-0.693 * age_minutes / 2880)

    # Frequency score: logarithmic scaling (diminishing returns)
    frequency = 0.0
    if item.touch_count > 0:
        # log(1) = 0, log(e) = 1, log(e^2) = 2, etc.
        # Normalize so touch_count=10 gives ~0.7
        frequency = min(1.0, math.log(item.touch_count + 1) / 3)

    # Combine: frequency is more important now (recency barely decays)
    return recency * 0.3 + frequency * 0.7


def neighbor_boost_score(query_tokens: set[str], item: ContextItem) -> float:
    """Boost score if neighbors match query terms.

    Args:
        query_tokens: Pre-tokenized query terms
        item: Context item with neighbors

    Returns:
        Boost score between 0.0 and 0.3
    """
    if not query_tokens or not item.neighbors:
        return 0.0

    # Check if any neighbor names match query
    matches = 0
    for neighbor in item.neighbors[:10]:  # Limit to first 10
        neighbor_tokens = tokenize(neighbor)
        if query_tokens & neighbor_tokens:
            matches += 1

    # Cap at 3 matches = 0.3 boost
    return min(0.3, matches * 0.1)


def file_cooccurrence_boost(
    item: ContextItem, file_entity_counts: dict[str, int]
) -> float:
    """Boost score for files with multiple entities in context.

    If multiple entities from the same file appear in the context frame,
    it suggests the file is a focal point of the current work.

    Args:
        item: Context item to score
        file_entity_counts: Dict mapping file_path to entity count in context

    Returns:
        Score between 0.0 and 1.0
    """
    if not item.file_path:
        return 0.0

    count = file_entity_counts.get(item.file_path, 0)

    # Score progression:
    # 1 entity = 0.0 (no co-occurrence)
    # 2 entities = 0.3
    # 3 entities = 0.5
    # 4 entities = 0.6
    # 5+ entities = 0.7 (capped)
    if count <= 1:
        return 0.0

    # Log scale for diminishing returns
    return min(0.7, math.log(count) / 2.5)


# ============================================================================
# Main Reranking Function
# ============================================================================

def simple_rerank_items(
    items: list[ContextItem],
    query: str,
    connection=None,
    top_k: Optional[int] = None,
    weights: Optional[dict] = None,
) -> list[ContextItem]:
    """Re-rank context items using simple heuristics.

    Scoring formula:
        final_score = (
            base_score * W_BASE +
            text_match * W_TEXT +
            graph_boost * W_GRAPH +
            session_boost * W_SESSION +
            neighbor_boost * W_NEIGHBOR +
            longevity * W_LONGEVITY +
            file_cooccur * W_FILE_COOCCUR
        )

    Args:
        items: List of context items to re-rank
        query: User query for relevance matching
        connection: Optional Kuzu connection for graph signals
        top_k: Number of top items to return (default: 20)
        weights: Optional weight overrides {base, text, graph, session, neighbor, longevity, file_cooccur}

    Returns:
        Sorted list of top-k items (most relevant first)
    """
    import time
    start_time = time.time()

    if not items:
        return items

    if not query or not query.strip():
        log.debug("No query provided, returning items by base score")
        return sorted(items, key=lambda x: x.score, reverse=True)[:top_k or 20]

    # Default weights
    w = {
        "base": 0.15,        # Tool-based relevance (already computed)
        "text": 0.35,        # Query-entity text matching
        "graph": 0.10,       # PageRank/betweenness
        "session": 0.10,     # Recency and frequency
        "neighbor": 0.05,    # Neighbor matching
        "longevity": 0.15,   # Items that keep appearing
        "file_cooccur": 0.10,  # Files with multiple entities
    }
    if weights:
        w.update(weights)

    # Pre-tokenize query once
    query_tokens = tokenize_query(query)
    now = datetime.now()

    # Build file entity counts for co-occurrence boost
    file_entity_counts: dict[str, int] = {}
    for item in items:
        if item.file_path:
            file_entity_counts[item.file_path] = file_entity_counts.get(item.file_path, 0) + 1

    # Score all items
    scored_items = []
    for item in items:
        # Base score from tool-based relevance
        base = item.score

        # Text matching score
        text = text_match_score(query_tokens, item)

        # Graph centrality boost (if connection available)
        graph = graph_boost_score(item, connection) if connection else 0.0

        # Session activity boost
        session = session_boost_score(item, now)

        # Neighbor matching boost
        neighbor = neighbor_boost_score(query_tokens, item)

        # Longevity boost (items that keep appearing)
        longevity = get_longevity_score(item.qualified_name)

        # File co-occurrence boost (multiple entities from same file)
        file_cooccur = file_cooccurrence_boost(item, file_entity_counts)

        # Compute final score
        final_score = (
            base * w["base"] +
            text * w["text"] +
            graph * w["graph"] +
            session * w["session"] +
            neighbor * w["neighbor"] +
            longevity * w["longevity"] +
            file_cooccur * w["file_cooccur"]
        )

        scored_items.append((item, final_score))

    # Sort by score descending
    scored_items.sort(key=lambda x: x[1], reverse=True)

    # Determine how many to keep
    if top_k is None:
        top_k = int(os.getenv("CONTEXT_RERANK_TOP_K", "20"))
    keep_count = min(top_k, len(scored_items))

    duration_ms = (time.time() - start_time) * 1000

    # Log statistics
    if scored_items:
        max_score = scored_items[0][1]
        min_score = scored_items[-1][1] if scored_items else 0
        log.info(
            f"Simple re-rank: {len(items)} -> {keep_count} items "
            f"in {duration_ms:.1f}ms | "
            f"scores [{min_score:.3f}-{max_score:.3f}] | "
            f"query: '{query[:40]}...'"
        )

    # Record appearances for longevity tracking
    result_items = [item for item, score in scored_items[:keep_count]]
    record_reranked_items([item.qualified_name for item in result_items])

    return result_items


def get_simple_rerank_scores(
    items: list[ContextItem],
    query: str,
    connection=None,
) -> list[tuple[ContextItem, float, dict]]:
    """Get detailed scoring breakdown for debugging.

    Args:
        items: List of context items
        query: Query to score against
        connection: Optional Kuzu connection

    Returns:
        List of (item, total_score, component_scores) sorted by score
    """
    if not items:
        return []

    query_tokens = tokenize_query(query) if query else set()
    now = datetime.now()

    # Build file entity counts for co-occurrence boost
    file_entity_counts: dict[str, int] = {}
    for item in items:
        if item.file_path:
            file_entity_counts[item.file_path] = file_entity_counts.get(item.file_path, 0) + 1

    results = []
    for item in items:
        components = {
            "base": item.score,
            "text": text_match_score(query_tokens, item),
            "graph": graph_boost_score(item, connection) if connection else 0.0,
            "session": session_boost_score(item, now),
            "neighbor": neighbor_boost_score(query_tokens, item),
            "longevity": get_longevity_score(item.qualified_name),
            "file_cooccur": file_cooccurrence_boost(item, file_entity_counts),
        }

        total = (
            components["base"] * 0.15 +
            components["text"] * 0.35 +
            components["graph"] * 0.10 +
            components["session"] * 0.10 +
            components["neighbor"] * 0.05 +
            components["longevity"] * 0.15 +
            components["file_cooccur"] * 0.10
        )

        results.append((item, total, components))

    results.sort(key=lambda x: x[1], reverse=True)
    return results
