"""Durable rerank-result cache — the same question over the same passages gets the same scores.

A cross-encoder (Cohere ``rerank-v4.0-pro`` in the AI Dream host) returns scores that drift in
the 3rd-4th decimal on every call, so two identical ``rag.search`` calls never produced identical
hits and every run-once step downstream of a search re-ran. This cache makes reranking a pure
function of its inputs and pays for each distinct (model, query, passages) once.

Key = SHA-256 over the SHA-256 of the rerank model, of the query and of every candidate passage's
CONTENT, in input order (each part hashed, so no separator inside a query can collide). A changed
library (different candidates), a changed chunk (different content) or a different model is a
different key, so it misses — never a stale answer.

ORGANIZATION IS TENANCY: a row belongs to the organization whose search paid for it, the carried
``organization_id``; uniqueness is ``(organization_id, cache_key)`` and every read filters on the
carried organization, so one organization's row is never served to another. A search with no
organization neither reads nor writes — it reranks live (the server never picks an organization).

Value = the reranker's scores in input order (the indices are the positions), stored in
``rag.rerank_cache`` through the package's own generated model (``get_db_model("RerankCache")``).
The row holds hashes and scores only, never the query or passage text. Retention is the
pair of ``platform.retention_policy`` rows for token ``rerank_cache``: the live-matching ending
archives a row untouched for 90 days, the trash ladder purges it 30 days after. A hit bumps
``hit_count`` / ``last_hit_at`` (so a reused row stays) and revives an archived row — the key is
content-addressed, so its scores are still exactly right.

A cache failure never breaks search: a read or write error reranks live and is CAPTURED
(``capture_error`` kind ``rag_rerank_cache_failed``), never swallowed.
"""

from __future__ import annotations

import hashlib
import logging
from datetime import UTC, datetime
from typing import Any

from matrx_utils import capture_error

from matrx_rag._ext import Reranker, RerankResult, try_get_db_model

logger = logging.getLogger(__name__)

RERANK_CACHE_MODEL = "RerankCache"


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def rerank_cache_key(model: str, query: str, documents: list[str]) -> str:
    """SHA-256 over the hashes of model, query and each passage's content, in order.

    Every part is a fixed-width hex digest, so no character inside a model name or query can
    shift where one part ends and the next begins."""
    parts = ["rerank-v2", _sha(model), _sha(query), str(len(documents))]
    parts += [_sha(doc or "") for doc in documents]
    return _sha(":".join(parts))


def reranker_model_id(reranker: Reranker) -> str | None:
    """The model the host reranker will use, declared up front (``Reranker.model``)."""
    model = getattr(reranker, "model", None)
    return model if isinstance(model, str) and model else None


async def _read(key: str, n_docs: int, *, organization_id: str) -> list[float] | None:
    from matrx_orm import F  # noqa: PLC0415

    model_cls = try_get_db_model(RERANK_CACHE_MODEL, schema="rag")
    if model_cls is None:
        return None
    result = await model_cls.update_where(
        {"organization_id": organization_id, "cache_key": key},
        hit_count=F("hit_count") + 1,
        last_hit_at=datetime.now(UTC),
        deleted_at=None,
    )
    if result.rows_affected == 0:
        return None
    row = result.updated_rows[0]
    scores = row.get("scores")
    if (
        not isinstance(scores, list)
        or len(scores) != n_docs
        or int(row.get("document_count") or -1) != n_docs
    ):
        raise ValueError(
            f"rag.rerank_cache row {key[:12]} holds {len(scores) if isinstance(scores, list) else 'no'} scores for {n_docs} passages"
        )
    return [float(s) for s in scores]


async def _write(
    key: str, result: RerankResult, n_docs: int, *, organization_id: str, user_id: str | None
) -> None:
    model_cls = try_get_db_model(RERANK_CACHE_MODEL, schema="rag")
    if model_cls is None:
        return
    await model_cls.insert_ignore(
        {
            "cache_key": key,
            "model": result.model,
            "document_count": n_docs,
            "scores": [float(s) for s in result.scores],
            "organization_id": organization_id,
            "created_by": user_id,
        },
        on_conflict=["organization_id", "cache_key"],
    )


async def cached_rerank(
    reranker: Reranker,
    query: str,
    documents: list[str],
    *,
    organization_id: str | None,
    user_id: str | None,
    rerank_call: Any = None,
) -> tuple[RerankResult, bool]:
    """Return ``(result, cache_hit)``. ``rerank_call`` is the live call (default ``reranker.rerank``).

    ``organization_id`` is the carried org the search is attributed to: it scopes the read and
    stamps a new row. With none the cache is not used at all (logged) — rerank live.
    """
    live = rerank_call or (lambda: reranker.rerank(query, documents))
    model = reranker_model_id(reranker)
    if model is None or not documents:
        return await live(), False
    if not organization_id:
        logger.warning("rag.search: rerank cache skipped — the search carries no organization")
        return await live(), False
    key = rerank_cache_key(model, query, documents)
    try:
        scores = await _read(key, len(documents), organization_id=organization_id)
    except Exception as exc:  # noqa: BLE001 — the cache never breaks search
        logger.warning("rag.search: rerank cache read failed, reranking live: %s", exc)
        await capture_error(
            exc, kind="rag_rerank_cache_failed", context={"op": "read", "documents": len(documents)}
        )
        scores = None
    if scores is not None:
        return RerankResult(scores=scores, model=model), True

    result = await live()
    if result.model != model or len(result.scores) != len(documents):
        logger.warning(
            "rag.search: reranker answered with model %r (declared %r) and %d scores for %d passages; not cached",
            result.model,
            model,
            len(result.scores),
            len(documents),
        )
        return result, False
    try:
        await _write(key, result, len(documents), organization_id=organization_id, user_id=user_id)
    except Exception as exc:  # noqa: BLE001 — the cache never breaks search
        logger.warning("rag.search: rerank cache write failed (result still used): %s", exc)
        await capture_error(
            exc,
            kind="rag_rerank_cache_failed",
            context={"op": "write", "documents": len(documents)},
        )
    return result, False


__all__ = ["RERANK_CACHE_MODEL", "cached_rerank", "rerank_cache_key", "reranker_model_id"]
