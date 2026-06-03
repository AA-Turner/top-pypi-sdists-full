"""ChromaDB integration for knowledge vector search.

Extracted from knowledge.py — functions receive KnowledgeManager instance
to access _fs, _conn, _chroma_client, _chroma_collection.
"""
from __future__ import annotations


def ensure_chroma(km) -> bool:
    """Lazily initialize Chroma PersistentClient and collection.

    Backfills existing entries with embeddings from SQLite on first run.
    Returns True if Chroma is ready, False otherwise.

    When chromadb has not been imported yet, return False immediately
    instead of paying the ~900ms import cost.
    """
    import sys
    from kanban_framework.domain.knowledge_lazy import _get_chromadb, _unpack_embedding

    if "chromadb" not in sys.modules:
        if not _get_chromadb():
            return False
    if km._chroma_collection is not None:
        return True
    try:
        chroma_dir = str(km._fs.kanban_dir / "knowledge" / "chroma")
        km._chroma_client = _get_chromadb().PersistentClient(path=chroma_dir)
        km._chroma_collection = km._chroma_client.get_or_create_collection(
            name="knowledge_entries",
            metadata={"hnsw:space": "cosine"},
        )
        # Backfill existing entries that have embeddings
        existing_ids = set(km._chroma_collection.get()["ids"])
        rows = km._conn.execute(
            "SELECT * FROM entries WHERE embedding IS NOT NULL"
        ).fetchall()
        for r in rows:
            eid = r["id"]
            if eid in existing_ids:
                continue
            emb_blob = r["embedding"]
            if not emb_blob:
                continue
            e_vec = _unpack_embedding(emb_blob)
            title = r["title"] or ""
            content = r["content"] or ""
            text = title + " " + content
            km._chroma_collection.add(
                ids=[eid],
                embeddings=[e_vec],
                documents=[text],
                metadatas=[{
                    "id": eid,
                    "domain": r["domain"],
                    "category": r["category"],
                    "title": title,
                    "status": r["status"],
                    "biz_context": r["biz_context"] if "biz_context" in r.keys() else None,
                }],
            )
        return True
    except Exception:
        return False


def defer_embed_and_chroma(km, entry_id, title, content, domain, category, status, biz_context=None):
    """Compute embedding + upsert to Chroma synchronously.

    Previously ran in a background thread, but this caused #366:
    new entries had no embedding immediately after add_entry returned,
    making hybrid/semantic search return low scores for the new entry.
    Embedding computation is typically <1s, so synchronous is acceptable.
    """
    from kanban_framework.domain.knowledge_lazy import _embed

    try:
        text = (title or "") + " " + (content or "")
        emb = _embed(text)
        if emb is not None:
            km._conn.execute(
                "UPDATE entries SET embedding=? WHERE id=?",
                (emb, entry_id),
            )
            km._conn.commit()
        chroma_upsert_entry(km, entry_id, title, content, domain, category, status, biz_context=biz_context)
    except Exception:
        pass


def chroma_upsert_entry(km, entry_id, title, content, domain, category, status, biz_context=None):
    """Upsert a single entry to Chroma. Silently ignores failures."""
    from kanban_framework.domain.knowledge_lazy import _embed, _unpack_embedding

    if not ensure_chroma(km):
        return
    try:
        text = (title or "") + " " + (content or "")
        emb = _embed(text)
        if emb is None:
            return
        e_vec = _unpack_embedding(emb)
        km._chroma_collection.upsert(
            ids=[entry_id],
            embeddings=[e_vec],
            documents=[text],
            metadatas=[{
                "id": entry_id,
                "domain": domain,
                "category": category,
                "title": title,
                "status": status,
                "biz_context": biz_context,
            }],
        )
    except Exception:
        pass  # Chroma failure must not block SQLite writes


def chroma_delete_entry(km, entry_id):
    """Remove an entry from Chroma by ID. Silently ignores failures."""
    if km._chroma_collection is None:
        return
    try:
        km._chroma_collection.delete(ids=[entry_id])
    except Exception:
        pass
