"""RAG helpers for the NX CLI.

This module is intentionally self-contained and fails soft. If optional ranking
packages or remote Supabase memory are unavailable, it falls back to simple
local scoring instead of breaking the CLI.
"""

from __future__ import annotations

import hashlib
import logging
import math
import os
import re
import warnings
from collections import Counter

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None  # type: ignore[assignment]

try:
    from rank_bm25 import BM25Okapi
except Exception:  # pragma: no cover
    BM25Okapi = None  # type: ignore[assignment]

try:
    from turbovec import TurboQuantIndex
except Exception:  # pragma: no cover
    TurboQuantIndex = None  # type: ignore[assignment]

import nx_data

warnings.filterwarnings("ignore", category=DeprecationWarning, message="builtin type .* has no __module__ attribute")
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub.utils._http").setLevel(logging.ERROR)


EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
RERANK_MODEL_NAME = "ms-marco-MiniLM-L-12-v2"
MODEL_CACHE_DIR = os.environ.get("SENTENCE_TRANSFORMERS_HOME", os.path.expanduser("~/.nx/models"))
RERANK_CACHE_DIR = MODEL_CACHE_DIR
DEFAULT_VECTOR_DIM = 384
DEFAULT_INDEX_BIT_WIDTH = 4

_FLASHRANK_DEPS: tuple[object | None, object | None] | None = None
_SENTENCE_TRANSFORMER_CLASS = None
_SENTENCE_TRANSFORMER_LOAD_FAILED = False


def _load_flashrank_deps() -> tuple[object | None, object | None]:
    global _FLASHRANK_DEPS
    if _FLASHRANK_DEPS is not None:
        return _FLASHRANK_DEPS
    try:
        from flashrank import Ranker, RerankRequest
    except Exception:  # pragma: no cover
        _FLASHRANK_DEPS = (None, None)
    else:
        _FLASHRANK_DEPS = (Ranker, RerankRequest)
    return _FLASHRANK_DEPS


def _load_sentence_transformer_class():
    global _SENTENCE_TRANSFORMER_CLASS, _SENTENCE_TRANSFORMER_LOAD_FAILED
    if _SENTENCE_TRANSFORMER_CLASS is not None:
        return _SENTENCE_TRANSFORMER_CLASS
    if _SENTENCE_TRANSFORMER_LOAD_FAILED:
        return None
    try:
        from sentence_transformers import SentenceTransformer
    except Exception:  # pragma: no cover
        _SENTENCE_TRANSFORMER_LOAD_FAILED = True
        return None
    _SENTENCE_TRANSFORMER_CLASS = SentenceTransformer
    return _SENTENCE_TRANSFORMER_CLASS


def _tokenize(text: str) -> list[str]:
    return [token for token in re.findall(r"[a-z0-9]+", (text or "").lower()) if token]


def _hash_embedding(text: str, dims: int = 384) -> list[float]:
    vector = [0.0] * dims
    for token in _tokenize(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        bucket = int.from_bytes(digest[:4], "big") % dims
        sign = -1.0 if digest[4] % 2 else 1.0
        weight = 1.0 + (digest[5] / 255.0)
        vector[bucket] += sign * weight
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def _cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _now_iso() -> str:
    return nx_data._now_utc()  # type: ignore[attr-defined]


class NXRag:
    def __init__(self, user_id: str, world: str = "cowork", top_k: int = 5,
                 rerank: bool = True, user_jwt: str = ""):
        self.user_id = user_id
        self.world = world or "cowork"
        self.top_k = max(1, int(top_k or 5))
        self.rerank = bool(rerank)
        # Cross-tenant isolation MUST come from the DB layer (RLS), never from
        # remembering to put .eq("user_id", ...) on every query. So:
        #   - With a user JWT → RLS-scoped client (correct, enforced).
        #   - Without a JWT → NO cloud client. We do NOT fall back to the
        #     service-role key (which bypasses RLS): a missing JWT means
        #     local-only mode, where the on-disk brain is the source of truth
        #     and there is zero cross-tenant surface. Opting into service-role
        #     here was the one place an unfiltered query could leak across
        #     tenants. An explicit admin/backfill script can still pass a
        #     service client in directly if it truly needs one.
        if user_jwt:
            self._client = nx_data.init_client(user_jwt=user_jwt)
        else:
            self._client = None
        self._embedder = None
        self._allow_model_download = True
        self._local_docs: list[dict] = []
        self._dense_index = None
        self._dense_dim = DEFAULT_VECTOR_DIM
        self._ranker = None
        self._rerank_request_cls = None

    def _init_ranker(self):
        ranker_cls, rerank_request_cls = _load_flashrank_deps()
        self._rerank_request_cls = rerank_request_cls
        if ranker_cls is None:
            return None
        try:
            return ranker_cls(model_name=RERANK_MODEL_NAME, cache_dir=RERANK_CACHE_DIR)
        except Exception:
            return None

    def _get_ranker(self):
        if not self.rerank:
            return None
        if self._ranker is None:
            self._ranker = self._init_ranker()
        return self._ranker

    def _get_embedder(self):
        if self._embedder is not None:
            return self._embedder
        sentence_transformer_cls = _load_sentence_transformer_class()
        if sentence_transformer_cls is None:
            return None
        try:
            self._embedder = sentence_transformer_cls(
                EMBED_MODEL_NAME,
                cache_folder=MODEL_CACHE_DIR,
                local_files_only=True,
            )
            return self._embedder
        except Exception:
            self._embedder = None
        if not self._allow_model_download:
            return None
        try:
            self._embedder = sentence_transformer_cls(
                EMBED_MODEL_NAME,
                cache_folder=MODEL_CACHE_DIR,
            )
        except Exception:
            self._embedder = None
        return self._embedder

    def _ensure_embedder(self):
        return self._get_embedder()

    def _embed_text(self, text: str) -> list[float]:
        embedder = self._get_embedder()
        if embedder is not None:
            try:
                embedding = embedder.encode(
                    text or "",
                    convert_to_numpy=True,
                    normalize_embeddings=True,
                )
                if hasattr(embedding, "tolist"):
                    return list(embedding.tolist())
                return list(embedding)
            except Exception:
                pass
        return _hash_embedding(text, dims=DEFAULT_VECTOR_DIM)

    def _embedding(self, text: str) -> list[float]:
        return self._embed_text(text)

    def _content_hash(self, text: str, world: str) -> str:
        return hashlib.sha256(f"{world}:{text}".encode("utf-8")).hexdigest()

    def _local_doc_key(self, row: dict) -> str:
        return f"{row.get('world') or self.world}:{row.get('content_hash') or self._content_hash(row.get('content', ''), row.get('world') or self.world)}"

    def _rebuild_local_index(self):
        if TurboQuantIndex is None or np is None or not self._local_docs:
            self._dense_index = None
            return
        dim = len(self._local_docs[0].get("embedding") or []) or DEFAULT_VECTOR_DIM
        try:
            vectors = np.asarray([doc.get("embedding") or [] for doc in self._local_docs], dtype=np.float32)
            index = TurboQuantIndex(dim=dim, bit_width=DEFAULT_INDEX_BIT_WIDTH)
            index.add(vectors)
            self._dense_index = index
            self._dense_dim = dim
        except Exception:
            self._dense_index = None

    def _cache_local_row(self, row: dict):
        cached = dict(row)
        cached.setdefault("metadata", {})
        cached.setdefault("tokens", _tokenize(cached.get("content", "")))
        cached.setdefault("world", self.world)
        cached.setdefault("created_at", _now_iso())
        cached.setdefault("content_hash", self._content_hash(cached.get("content", ""), cached["world"]))
        if "embedding" not in cached:
            cached["embedding"] = self._embedding(cached.get("content", ""))

        key = self._local_doc_key(cached)
        for index, existing in enumerate(self._local_docs):
            if self._local_doc_key(existing) == key:
                self._local_docs[index] = cached
                self._rebuild_local_index()
                return

        self._local_docs.append(cached)
        self._rebuild_local_index()

    def _cache_candidates(self, candidates: list[dict], world: str):
        for candidate in candidates or []:
            content = candidate.get("content", "")
            if not content:
                continue
            scope = candidate.get("world") or world
            self._cache_local_row(
                {
                    "id": candidate.get("id"),
                    "content": content,
                    "metadata": candidate.get("metadata") or {},
                    "world": scope,
                    "created_at": candidate.get("created_at") or _now_iso(),
                    "content_hash": candidate.get("content_hash") or self._content_hash(content, scope),
                }
            )

    def _dense_search(self, query_embedding: list[float], world: str, limit: int) -> list[dict]:
        world_limit = max(1, int(limit or self.top_k))
        if self._dense_index is not None and np is not None and self._local_docs:
            try:
                k = min(len(self._local_docs), max(world_limit * 4, world_limit))
                scores, indices = self._dense_index.search(
                    np.asarray([query_embedding], dtype=np.float32),
                    k=k,
                )
                results = []
                for score, index in zip(scores[0], indices[0]):
                    position = int(index)
                    if position < 0 or position >= len(self._local_docs):
                        continue
                    doc = self._local_docs[position]
                    if doc.get("world") != world:
                        continue
                    results.append(
                        {
                            "id": doc.get("id"),
                            "content": doc.get("content", ""),
                            "metadata": doc.get("metadata") or {},
                            "world": doc.get("world"),
                            "content_hash": doc.get("content_hash"),
                            "similarity": float(score),
                        }
                    )
                    if len(results) >= world_limit:
                        break
                if results:
                    return results
            except Exception:
                pass

        fallback = []
        for doc in self._local_docs:
            if doc.get("world") != world:
                continue
            fallback.append(
                {
                    "id": doc.get("id"),
                    "content": doc.get("content", ""),
                    "metadata": doc.get("metadata") or {},
                    "world": doc.get("world"),
                    "content_hash": doc.get("content_hash"),
                    "similarity": _cosine(query_embedding, doc.get("embedding") or []),
                }
            )
        return sorted(fallback, key=lambda row: row.get("similarity", 0.0), reverse=True)[:world_limit]

    def _local_ranked_results(self, query: str, world: str, query_embedding: list[float]) -> list[dict]:
        self._cache_candidates(self._local_candidates(world, limit=self.top_k * 8), world)
        docs = [doc for doc in self._local_docs if doc.get("world") == world]
        if not docs:
            return []

        dense_hits = {
            row.get("content_hash"): float(row.get("similarity", 0.0))
            for row in self._dense_search(query_embedding, world, limit=max(self.top_k * 8, len(docs)))
        }
        bm25_scores = self._bm25_scores(query, docs)

        ranked = []
        for doc, sparse_score in zip(docs, bm25_scores):
            ranked.append(
                {
                    "id": doc.get("id"),
                    "content": doc.get("content", ""),
                    "metadata": doc.get("metadata") or {},
                    "world": doc.get("world"),
                    "content_hash": doc.get("content_hash"),
                    "similarity": dense_hits.get(doc.get("content_hash"), 0.0) + (0.1 * float(sparse_score)),
                }
            )

        return sorted(ranked, key=lambda row: row.get("similarity", 0.0), reverse=True)

    def ingest(self, content: str, metadata=None, world: str | None = None) -> bool:
        if not content:
            return False
        scope = world or self.world
        embedding = self._embedding(content)
        row = {
            "user_id": self.user_id,
            "world": scope,
            "content": content,
            "content_hash": self._content_hash(content, scope),
            "embedding": embedding,
            "tokens": _tokenize(content),
            "metadata": metadata or {},
            "created_at": _now_iso(),
        }
        self._cache_local_row(row)
        if not self._client:
            return True
        try:
            self._client.table("nx_memory").upsert(row, on_conflict="user_id,content_hash").execute()
            return True
        except Exception:
            return True

    def ingest_messages(self, messages: list[dict]) -> int:
        stored = 0
        for message in messages or []:
            if not isinstance(message, dict):
                continue
            if self.ingest(
                content=message.get("content", ""),
                metadata={
                    "role": message.get("role"),
                    "world": message.get("world"),
                    "model_used": message.get("model_used"),
                    "timestamp": message.get("timestamp"),
                    "trainable": message.get("trainable", True),
                },
                world=message.get("world") or self.world,
            ):
                stored += 1
        return stored

    def _local_candidates(self, world: str, limit: int = 40) -> list[dict]:
        if not self._client:
            return []
        try:
            result = (
                self._client.table("nx_memory")
                .select("id,content,metadata,world,created_at,content_hash")
                .eq("user_id", self.user_id)
                .eq("world", world)
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            return list(result.data or [])
        except Exception:
            return []

    def _bm25_scores(self, query: str, docs: list[dict]) -> list[float]:
        tokenized_docs = [_tokenize(doc.get("content", "")) for doc in docs]
        query_tokens = _tokenize(query)
        if BM25Okapi is not None and any(tokenized_docs):
            try:
                return list(BM25Okapi(tokenized_docs).get_scores(query_tokens))
            except Exception:
                pass
        query_counts = Counter(query_tokens)
        scores = []
        for doc_tokens in tokenized_docs:
            doc_counts = Counter(doc_tokens)
            overlap = sum(min(query_counts[token], doc_counts[token]) for token in query_counts)
            scores.append(float(overlap))
        return scores

    def _rerank_results(self, query: str, results: list[dict]) -> list[dict]:
        ranker = self._get_ranker()
        if not ranker or not self._rerank_request_cls or not results:
            return results
        try:
            request = self._rerank_request_cls(query=query, passages=[{"id": str(idx), "text": row["content"]} for idx, row in enumerate(results)])
            ranked = ranker.rerank(request)
            reranked = []
            for item in ranked:
                row = results[int(item["id"])]
                updated = dict(row)
                updated["similarity"] = max(float(updated.get("similarity", 0.0)), float(item.get("score", 0.0)))
                reranked.append(updated)
            return reranked
        except Exception:
            return results

    def query(self, query: str, world_filter: str | None = None) -> list[dict]:
        if not query:
            return []
        world = world_filter or self.world
        query_embedding = self._embedding(query)

        if self._client:
            try:
                rpc = self._client.rpc(
                    "nx_memory_search",
                    {
                        "query_embedding": query_embedding,
                        "match_world": world,
                        "match_user_id": self.user_id,
                        "match_count": self.top_k * 3,
                        "similarity_threshold": 0.15,
                    },
                ).execute()
                results = list(rpc.data or [])
            except Exception:
                results = []
        else:
            results = []

        if not results:
            results = self._local_ranked_results(query, world, query_embedding)

        results = self._rerank_results(query, results)
        return results[: self.top_k]

    def build_context(self, results: list[dict], max_chars: int = 2000) -> str:
        if not results:
            return ""
        lines = ["Relevant context from memory"]
        used = len(lines[0])
        for index, result in enumerate(results, start=1):
            similarity = float(result.get("similarity", 0.0))
            content = " ".join((result.get("content") or "").split())
            excerpt = content[:280]
            line = f"[{index}] ({similarity:.2f}) {excerpt}"
            if used + len(line) > max_chars:
                break
            lines.append(line)
            used += len(line)
        return "\n".join(lines)
