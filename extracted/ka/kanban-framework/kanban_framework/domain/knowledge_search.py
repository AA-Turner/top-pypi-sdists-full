"""Search implementations for knowledge DB — FTS5, semantic, hybrid, intent-based.

Extracted from knowledge.py — functions receive KnowledgeManager instance
for access to _conn, _row_to_dict, and other internal state.
"""
from __future__ import annotations

import sqlite3


def _filter_by_biz(results: list[dict], biz_context: str) -> list[dict]:
    """Filter results: keep entries with NULL biz_context or matching biz_context."""
    allowed = set(biz_context.split(","))
    return [
        r for r in results
        if r.get("biz_context") is None
        or allowed & set((r.get("biz_context") or "").split(","))
    ]


def fts_safe(conn, query, params):
    """Execute FTS5 MATCH safely, falling back to empty on syntax error."""
    try:
        return conn.execute(query, params).fetchall()
    except sqlite3.OperationalError:
        return []


def search_fts(km, keyword: str, limit: int = 20, *, biz_context: str | None = None) -> list[dict]:
    """FTS5 keyword search with jieba segmentation and BM25 ranking."""
    from kanban_framework.domain.knowledge_lazy import (
        _expand_abbreviations, _get_jieba, _substring_match_score, _stale_penalty,
    )

    if not keyword:
        return []

    conn = km._conn
    row_to_dict = km._row_to_dict
    expanded = _expand_abbreviations(keyword)

    if any('一' <= c <= '鿿' for c in keyword) and _get_jieba():
        segmented = " ".join(w for w in _get_jieba().cut(expanded) if w.strip())
        query = """SELECT e.*, rank FROM entries_fts f
                   JOIN entries e ON e.rowid = f.rowid
                   WHERE entries_fts MATCH ? AND e.status='active' ORDER BY rank LIMIT ?"""
        params = [segmented, limit]
        rows = fts_safe(conn, query, params)
        if not rows and " " in segmented:
            or_query = segmented.replace(" ", " OR ")
            params = [or_query, limit]
            rows = fts_safe(conn, query, params)
        if not rows:
            params = [keyword, limit]
            rows = fts_safe(conn, query, params)
    else:
        query = """SELECT e.*, rank FROM entries_fts f
                   JOIN entries e ON e.rowid = f.rowid
                   WHERE entries_fts MATCH ? AND e.status='active' ORDER BY rank LIMIT ?"""
        for q in (expanded, keyword):
            if q == keyword and expanded == keyword:
                params = [keyword, limit]
                rows = fts_safe(conn, query, params)
                break
            params = [q, limit]
            rows = fts_safe(conn, query, params)
            if rows:
                break
        else:
            rows = []

    results = [row_to_dict(r) for r in rows]

    if keyword and results:
        for r in results:
            title_bonus = _substring_match_score(keyword, r.get("title", ""))
            content_bonus = _substring_match_score(keyword, r.get("content", ""))
            bonus = max(title_bonus, content_bonus)
            if bonus > 0:
                current_score = r.get("score", 0.0)
                r["score"] = float(current_score) + bonus

    if not results and keyword:
        kw = f"%{keyword}%"
        like_rows = conn.execute(
            "SELECT * FROM entries WHERE status='active' AND "
            "(title LIKE ? OR content LIKE ?) LIMIT ?",
            (kw, kw, limit),
        ).fetchall()
        results = [row_to_dict(r) for r in like_rows]

    for r in results:
        r["_stale_penalty"] = _stale_penalty(r.get("stale_at"))

    if biz_context is not None:
        results = _filter_by_biz(results, biz_context)
    return results


def search_semantic(km, query: str, limit: int = 20, *, biz_context: str | None = None) -> list[dict]:
    """Semantic search using Chroma ANN with cosine distance.

    Falls back to full-table cosine scan, then to keyword search.
    """
    from kanban_framework.domain.knowledge_lazy import (
        _EMBED_FAILED, _get_embed_model, _embed, _unpack_embedding, _cosine_similarity,
    )
    from kanban_framework.domain.knowledge_chroma import ensure_chroma

    if not query or _EMBED_FAILED:
        return search_fts(km, query, limit=limit) if query else []

    model = _get_embed_model()
    if model is None:
        return search_fts(km, query, limit=limit)

    import sys
    if "chromadb" not in sys.modules and "fastembed" not in sys.modules:
        return search_fts(km, query, limit=limit)

    q_emb = _embed(query)
    if q_emb is None:
        return search_fts(km, query, limit=limit)

    q_vec = _unpack_embedding(q_emb)

    if ensure_chroma(km):
        try:
            results = km._chroma_collection.query(
                query_embeddings=[q_vec],
                n_results=limit,
            )
            ids = results.get("ids", [[]])[0]
            if ids is not None and len(ids) > 0:
                distances = results.get("distances", [[]])[0]
                entries = []
                for idx, eid in enumerate(ids):
                    entry = km.get_entry(eid)
                    if entry:
                        if distances and idx < len(distances):
                            entry["score"] = round(1.0 - distances[idx], 4)
                        entries.append(entry)
                if biz_context is not None:
                    entries = _filter_by_biz(entries, biz_context)
                return entries
        except Exception:
            pass

    # Fallback: full-table cosine scan
    rows = km._conn.execute(
        "SELECT * FROM entries WHERE embedding IS NOT NULL AND status='active'"
    ).fetchall()

    scored = []
    for r in rows:
        emb_blob = r["embedding"]
        if not emb_blob:
            continue
        e_vec = _unpack_embedding(emb_blob)
        score = _cosine_similarity(q_vec, e_vec)
        entry = km._row_to_dict(r)
        scored.append((score, entry))

    scored.sort(key=lambda x: x[0], reverse=True)
    results = []
    for s, e in scored[:limit]:
        e["score"] = round(s, 4)
        results.append(e)
    if biz_context is not None:
        results = _filter_by_biz(results, biz_context)
    return results


def search_hybrid(km, keyword: str, limit: int = 20, *, biz_context: str | None = None) -> list[dict]:
    """Hybrid search: BM25 keyword + semantic vector fused via RRF.

    Uses search_fts and search_semantic to avoid backend recursion.
    Sets normalized relevance score on output entries.
    """
    kw_results = search_fts(km, keyword, limit=limit * 2, biz_context=biz_context) if keyword else []
    try:
        sem_results = search_semantic(km, keyword, limit=limit * 2, biz_context=biz_context)
    except Exception:
        sem_results = []

    if not sem_results:
        # Still set relevance for keyword-only results
        for i, r in enumerate(kw_results[:limit]):
            r["relevance"] = round(1.0 - i * 0.01, 4) if i < 100 else 0.0
        return kw_results[:limit]

    # RRF (Reciprocal Rank Fusion)
    rrf_scores: dict[str, float] = {}
    _RRF_K = 60.0

    for rank, r in enumerate(kw_results, 1):
        eid = r["id"]
        rrf_scores[eid] = rrf_scores.get(eid, 0) + 1.0 / (_RRF_K + rank)

    for rank, r in enumerate(sem_results, 1):
        eid = r["id"]
        rrf_scores[eid] = rrf_scores.get(eid, 0) + 1.0 / (_RRF_K + rank)

    all_entries = {r["id"]: r for r in kw_results + sem_results}
    ranked = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

    # Normalize RRF scores to 0-1 range for relevance
    max_rrf = ranked[0][1] if ranked else 1.0
    results = []
    for eid, s in ranked[:limit]:
        if eid in all_entries:
            entry = all_entries[eid]
            entry["relevance"] = round(s / max_rrf, 4) if max_rrf > 0 else 0.0
            results.append(entry)
    return results


def search_by_intent(km, intent: str, query: str, limit: int = 20, *, biz_context: str | None = None, **context) -> list[dict]:
    """Route a search to the right strategy based on retrieval intent.

    Intents:
    - pitfall_check: prioritize high-severity pitfall entries by keyword
    - constraint_lookup: exact match on tags + source.file context
    - experience_reuse: semantic similarity + domain boost + recency
    - general (default): standard hybrid search
    """
    backend = km._backend

    if intent == "pitfall_check":
        results = backend.search(query, limit=limit * 2, biz_context=biz_context)
        domain = context.get("domain")
        scored = []
        for r in results:
            score = float(r.get("score", 0))
            if r.get("severity") == "high":
                score *= 1.5
            if r.get("category") == "踩坑":
                score *= 1.3
            if domain and r.get("domain") == domain:
                score *= 1.2
            scored.append((score, r))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [e for _, e in scored[:limit]]

    elif intent == "constraint_lookup":
        keyword_results = backend.search(query, limit=limit, biz_context=biz_context)
        source_file = context.get("source_file")
        domain = context.get("domain")
        if source_file:
            keyword_results = [
                r for r in keyword_results
                if source_file in str(r.get("source", ""))
            ]
        if domain:
            domain_filtered = [r for r in keyword_results if r.get("domain") == domain]
            if domain_filtered:
                keyword_results = domain_filtered
        keyword_results.sort(
            key=lambda r: 1 if "must_not" in str(r.get("tags", "")) else 0,
            reverse=True,
        )
        return keyword_results[:limit]

    elif intent == "experience_reuse":
        results = backend.search_hybrid(query, limit=limit * 2, biz_context=biz_context)
        domain = context.get("domain")
        scored = []
        for r in results:
            score = float(r.get("relevance") or r.get("score", 0))
            if domain and r.get("domain") == domain:
                score *= 1.2
            if r.get("type") == "procedure":
                score *= 1.3
            rc = r.get("referenced_count", 0)
            if rc > 0:
                score *= min(1.0 + rc * 0.05, 1.5)
            scored.append((score, r))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [e for _, e in scored[:limit]]

    else:
        return backend.search_hybrid(query, limit=limit, biz_context=biz_context)
