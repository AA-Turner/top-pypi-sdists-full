"""QMD — Hybrid BM25 + Vector memory search engine.

When ``memory.backend = "qmd"`` in config, this backend provides
hybrid search over memory markdown files by combining:

1. **BM25 keyword search** — via SQLite FTS5 (delegated to MemoryIndex)
2. **Vector semantic search** — via the EmbeddingService + cosine similarity

Results are merged using Reciprocal Rank Fusion (RRF), matching
OpenClaw's union approach: results from *either* search contribute
to the final ranking.

If the embedding service is unavailable (no API key, network failure),
QMD gracefully degrades to BM25-only — identical to the SQLite backend.
"""

import logging
import math
import sqlite3
import struct
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from .memory_index import MemoryIndex, SearchHit

logger = logging.getLogger(__name__)

# RRF constant — controls how much rank position matters vs score.
# k=60 is the standard value from the original RRF paper (Cormack et al.).
_RRF_K = 60


@dataclass
class QmdConfig:
    """Configuration for the QMD hybrid search backend."""

    # Result limits
    max_results: int = 5
    timeout_ms: int = 3000
    max_snippet_chars: int = 700

    # Embedding model (string like "openai:text-embedding-3-small" or None for auto)
    embedding_model: Optional[str] = None

    # Weight balance between BM25 and vector search (0.0 = BM25 only, 1.0 = vector only)
    vector_weight: float = 0.5

    # How many candidates to fetch from each backend before merging
    candidate_multiplier: int = 3


class QmdIndex:
    """Hybrid BM25 + vector search over memory markdown files.

    Uses the built-in :class:`MemoryIndex` (SQLite FTS5) for keyword
    search and the ``EmbeddingService`` for semantic search. Results
    are merged using Reciprocal Rank Fusion (RRF).

    If embeddings are unavailable, falls back to BM25-only (identical
    to the plain SQLite backend, zero degradation).

    Usage::

        sqlite_index = MemoryIndex(db_path, workspace_dir)
        qmd = QmdIndex(bm25=sqlite_index, workspace_dir=workspace_dir)
        qmd.sync_now("boot")
        hits = qmd.search("user preferences")
    """

    def __init__(
        self,
        bm25: MemoryIndex,
        workspace_dir: Path,
        config: Optional[QmdConfig] = None,
    ) -> None:
        self._bm25 = bm25
        self._workspace = Path(workspace_dir).resolve()
        self._cfg = config or QmdConfig()
        self._dirty_paths: set[str] = set()

        # Vector storage (separate SQLite db alongside the FTS index)
        self._vec_db_path = self._workspace / "memory" / "vectors.sqlite"
        self._vec_conn: Optional[sqlite3.Connection] = None

        # Embedding service (lazy-loaded)
        self._embedding_service = None
        self._embeddings_available: Optional[bool] = None

        self._ensure_vector_db()

    # ------------------------------------------------------------------
    # Public interface (matches MemoryIndex)
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
        limit: int = 0,
        timeout_ms: int = 0,
    ) -> list[SearchHit]:
        """Hybrid search: BM25 + vector, merged via RRF.

        Args:
            query: Search query string.
            limit: Max results (0 → use config default).
            timeout_ms: Timeout in ms (0 → use config default).

        Returns:
            List of :class:`SearchHit` sorted by relevance.
        """
        limit = limit or self._cfg.max_results
        n_candidates = limit * self._cfg.candidate_multiplier

        # Sync dirty files before searching
        if self._dirty_paths:
            self.sync_now("onSearch")

        # 1. BM25 results (always available)
        bm25_hits = self._bm25.search(query, limit=n_candidates)

        # 2. Vector results (if embeddings available)
        vector_hits: list[SearchHit] = []
        if self._is_embeddings_available():
            try:
                vector_hits = self._vector_search(query, limit=n_candidates)
            except Exception as exc:
                logger.warning("Vector search failed (using BM25 only): %s", exc)

        # 3. Merge via RRF (or return BM25-only if no vector results)
        if not vector_hits:
            return bm25_hits[:limit]

        merged = self._rrf_merge(bm25_hits, vector_hits, limit)
        return merged

    def mark_dirty(self, path: str) -> None:
        """Mark a file as needing re-indexing in both BM25 and vector stores."""
        self._dirty_paths.add(path)
        self._bm25.mark_dirty(path)

    def sync_now(self, reason: str = "boot") -> None:
        """Re-index dirty files in both BM25 and vector stores.

        BM25 re-indexing is fast (in-process FTS5). Vector embedding
        is async-friendly but runs synchronously here — only dirty
        chunks are re-embedded.
        """
        # Sync BM25 first (fast)
        self._bm25.sync_now(reason)

        # Then embed any new/changed chunks
        if self._is_embeddings_available():
            try:
                self._sync_vectors(reason)
            except Exception as exc:
                logger.warning("Vector sync failed (non-fatal): %s", exc)

        self._dirty_paths.clear()

    def close(self) -> None:
        """Close underlying resources."""
        self._bm25.close()
        if self._vec_conn is not None:
            self._vec_conn.close()
            self._vec_conn = None

    # ------------------------------------------------------------------
    # Vector database setup
    # ------------------------------------------------------------------

    def _ensure_vector_db(self) -> None:
        """Create the vector storage database if it doesn't exist."""
        self._vec_db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = self._get_vec_conn()
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS vectors (
                path TEXT NOT NULL,
                start_line INTEGER NOT NULL,
                end_line INTEGER NOT NULL,
                content TEXT NOT NULL,
                embedding BLOB NOT NULL,
                model_name TEXT NOT NULL,
                indexed_at REAL NOT NULL,
                PRIMARY KEY (path, start_line)
            );

            CREATE INDEX IF NOT EXISTS idx_vectors_path
                ON vectors(path);
            """
        )
        conn.commit()

    def _get_vec_conn(self) -> sqlite3.Connection:
        """Get or create the vector database connection."""
        if self._vec_conn is None:
            self._vec_conn = sqlite3.connect(str(self._vec_db_path), timeout=5)
            self._vec_conn.execute("PRAGMA journal_mode=WAL")
            self._vec_conn.execute("PRAGMA synchronous=NORMAL")
        return self._vec_conn

    # ------------------------------------------------------------------
    # Embedding service
    # ------------------------------------------------------------------

    def _is_embeddings_available(self) -> bool:
        """Check if the embedding service is available (lazy probe)."""
        if self._embeddings_available is not None:
            return self._embeddings_available

        try:
            service = self._get_embedding_service()
            self._embeddings_available = service is not None and service.is_available
        except Exception:
            self._embeddings_available = False

        if self._embeddings_available:
            logger.info("QMD vector search: embeddings available (model=%s)", self._model_name())
        else:
            logger.info("QMD vector search: embeddings unavailable, using BM25 only")

        return self._embeddings_available

    def _get_embedding_service(self):
        """Lazy-load the EmbeddingService."""
        if self._embedding_service is not None:
            return self._embedding_service

        try:
            from ...embeddings import EmbeddingService, EmbeddingModel

            model = None
            if self._cfg.embedding_model:
                model = EmbeddingModel.from_string(self._cfg.embedding_model)

            self._embedding_service = EmbeddingService(model=model)
            return self._embedding_service
        except Exception as exc:
            logger.debug("Could not initialise EmbeddingService: %s", exc)
            return None

    def _model_name(self) -> str:
        """Get the active embedding model name for tracking."""
        svc = self._get_embedding_service()
        if svc and svc.model:
            return svc.model.model_id
        return "unknown"

    # ------------------------------------------------------------------
    # Vector sync (embed chunks)
    # ------------------------------------------------------------------

    def _sync_vectors(self, reason: str) -> None:
        """Embed new/changed chunks from the BM25 index into the vector store.

        Reads chunks from the BM25 SQLite database, checks which ones
        are missing or stale in the vector store, and embeds them.
        """
        start = time.monotonic()
        svc = self._get_embedding_service()
        if not svc or not svc.is_available:
            return

        model_name = self._model_name()
        bm25_conn = self._bm25._get_conn()
        vec_conn = self._get_vec_conn()

        # Get all chunks from BM25 index
        bm25_rows = bm25_conn.execute(
            "SELECT path, start_line, end_line, content, indexed_at FROM chunks"
        ).fetchall()

        if not bm25_rows:
            return

        # Get existing vector timestamps
        existing = {}
        for row in vec_conn.execute(
            "SELECT path, start_line, indexed_at, model_name FROM vectors"
        ).fetchall():
            existing[(row[0], row[1])] = (row[2], row[3])

        # Find chunks that need embedding
        to_embed: list[tuple[str, int, int, str, float]] = []
        for path, start_line, end_line, content, indexed_at in bm25_rows:
            key = (path, start_line)
            if key in existing:
                old_ts, old_model = existing[key]
                if old_ts >= indexed_at and old_model == model_name:
                    continue  # Already up to date
            to_embed.append((path, start_line, end_line, content, indexed_at))

        # Remove vectors for paths that no longer have BM25 chunks
        bm25_paths = {row[0] for row in bm25_rows}
        vec_paths = {k[0] for k in existing}
        for stale_path in vec_paths - bm25_paths:
            vec_conn.execute("DELETE FROM vectors WHERE path = ?", (stale_path,))

        if not to_embed:
            vec_conn.commit()
            elapsed = time.monotonic() - start
            logger.debug("QMD vector sync (%s): nothing to embed (%.2fs)", reason, elapsed)
            return

        # Batch embed
        texts = [row[3] for row in to_embed]
        embeddings = svc.embed_texts(texts)

        # Store results
        now = time.time()
        embedded_count = 0
        for i, (path, start_line, end_line, content, _) in enumerate(to_embed):
            vec = embeddings[i] if i < len(embeddings) else None
            if vec is None:
                continue

            blob = _pack_vector(vec)
            vec_conn.execute(
                """
                INSERT OR REPLACE INTO vectors
                    (path, start_line, end_line, content, embedding, model_name, indexed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (path, start_line, end_line, content, blob, model_name, now),
            )
            embedded_count += 1

        vec_conn.commit()
        elapsed = time.monotonic() - start
        logger.info(
            "QMD vector sync (%s): embedded %d/%d chunks in %.2fs",
            reason, embedded_count, len(to_embed), elapsed,
        )

    # ------------------------------------------------------------------
    # Vector search
    # ------------------------------------------------------------------

    def _vector_search(self, query: str, limit: int) -> list[SearchHit]:
        """Search memory via vector cosine similarity.

        Embeds the query, then computes cosine similarity against all
        stored vectors. Returns top-k results as SearchHit objects.
        """
        svc = self._get_embedding_service()
        if not svc:
            return []

        # Embed query (uses query-specific prefix for models that need it)
        query_vec = svc.embed_query(query)
        if query_vec is None:
            return []

        # Load all stored vectors
        vec_conn = self._get_vec_conn()
        rows = vec_conn.execute(
            "SELECT path, start_line, end_line, content, embedding FROM vectors"
        ).fetchall()

        if not rows:
            return []

        # Compute cosine similarity
        max_snippet = self._cfg.max_snippet_chars
        scored: list[tuple[float, str, int, int, str]] = []

        for path, start_line, end_line, content, blob in rows:
            stored_vec = _unpack_vector(blob)
            sim = _cosine_similarity(query_vec, stored_vec)
            scored.append((sim, path, start_line, end_line, content))

        # Sort by similarity (highest first) and take top-k
        scored.sort(key=lambda x: x[0], reverse=True)

        hits: list[SearchHit] = []
        for sim, path, start_line, end_line, content in scored[:limit]:
            snippet = content
            if len(snippet) > max_snippet:
                snippet = snippet[:max_snippet] + "..."
            hits.append(SearchHit(
                path=path,
                start_line=start_line,
                end_line=end_line,
                snippet=snippet,
                score=round(sim, 4),
            ))

        return hits

    # ------------------------------------------------------------------
    # RRF merge (union ranking)
    # ------------------------------------------------------------------

    @staticmethod
    def _rrf_merge(
        bm25_hits: list[SearchHit],
        vector_hits: list[SearchHit],
        limit: int,
    ) -> list[SearchHit]:
        """Merge BM25 and vector results via Reciprocal Rank Fusion.

        RRF score = 1/(k + rank_bm25) + 1/(k + rank_vector)

        Uses *union* — a hit from either list contributes, matching
        OpenClaw's approach. If a chunk appears in both lists, its
        scores are summed.
        """
        # Build lookup: (path, start_line) → SearchHit + RRF score
        merged: dict[tuple[str, int], tuple[SearchHit, float]] = {}

        for rank, hit in enumerate(bm25_hits):
            key = (hit.path, hit.start_line)
            rrf_score = 1.0 / (_RRF_K + rank + 1)
            if key in merged:
                old_hit, old_score = merged[key]
                merged[key] = (old_hit, old_score + rrf_score)
            else:
                merged[key] = (hit, rrf_score)

        for rank, hit in enumerate(vector_hits):
            key = (hit.path, hit.start_line)
            rrf_score = 1.0 / (_RRF_K + rank + 1)
            if key in merged:
                old_hit, old_score = merged[key]
                merged[key] = (old_hit, old_score + rrf_score)
            else:
                merged[key] = (hit, rrf_score)

        # Sort by combined RRF score
        ranked = sorted(merged.values(), key=lambda x: x[1], reverse=True)

        # Return SearchHit with RRF score
        return [
            SearchHit(
                path=hit.path,
                start_line=hit.start_line,
                end_line=hit.end_line,
                snippet=hit.snippet,
                score=round(rrf_score, 6),
            )
            for hit, rrf_score in ranked[:limit]
        ]


# ======================================================================
# Pure-Python vector utilities (no numpy dependency)
# ======================================================================

def _pack_vector(vec: list[float]) -> bytes:
    """Pack a float vector into a compact bytes blob (float32)."""
    return struct.pack(f"<{len(vec)}f", *vec)


def _unpack_vector(blob: bytes) -> list[float]:
    """Unpack a bytes blob back into a float vector."""
    n = len(blob) // 4  # float32 = 4 bytes
    return list(struct.unpack(f"<{n}f", blob))


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors.

    Returns 0.0 on degenerate inputs (zero-length vectors, mismatched dims).
    """
    if len(a) != len(b) or not a:
        return 0.0

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    return dot / (norm_a * norm_b)
