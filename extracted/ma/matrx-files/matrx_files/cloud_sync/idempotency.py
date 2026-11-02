"""Idempotency-key memoization for combined operations.

Backs the ``X-Idempotency-Key`` header on combined-op endpoints (POST
/assets with bundled share/permissions/variants, PATCH /files/{id}
union, POST /files/bulk). Retry-safe: the same key + the same request
body returns the original response envelope verbatim. The same key
with a *different* body returns 409 Conflict (the FE accidentally
reused a key for two distinct requests).

Backed by the ``files.idempotency`` table. 24h TTL by default; a
host-side cron sweeps expired rows.
"""

from __future__ import annotations

from typing import Any

from matrx_utils import stable_hash, vcprint

from .db import _models, _vals


class IdempotencyConflict(Exception):
    """Same key, different body. Caller must use a fresh key."""

    def __init__(self, key: str) -> None:
        super().__init__(f"Idempotency key {key!r} was already used with a different request body")
        self.key = key


def hash_request(*, endpoint: str, body: dict | list | str | None) -> str:
    """Deterministic SHA-256 of the canonical request envelope.

    Body is JSON-serialized with sorted keys so semantically-equivalent
    dicts hash identically. Returns a hex digest.
    """
    return stable_hash({"endpoint": endpoint, "body": body})


class IdempotencyStore:
    """Async accessor for the ``files.idempotency`` table.

    Usage from within a combined-op handler:

        store = IdempotencyStore(fm)
        cached = await store.lookup(
            owner_id=owner_id, key=request.headers["X-Idempotency-Key"],
            endpoint="POST /assets", body=payload,
        )
        if cached is not None:
            return cached["response_body"], cached["status_code"]

        # ... do the work, build envelope ...

        await store.persist(
            owner_id=owner_id, key=request.headers["X-Idempotency-Key"],
            endpoint="POST /assets", body=payload,
            status_code=200, response_body=envelope,
            resource_id=envelope["file_id"], resource_type="file",
        )
        return envelope, 200
    """

    def __init__(self, fm: Any) -> None:
        if fm is None or fm.sync_engine is None:
            raise RuntimeError("IdempotencyStore needs a FileManager with cloud_sync configured")
        self._fm = fm

    async def lookup(
        self,
        *,
        owner_id: str,
        key: str | None,
        endpoint: str,
        body: dict | list | str | None,
    ) -> dict | None:
        """Return the cached response when (owner, key) matches AND the
        request hash matches. Raises IdempotencyConflict when the key
        was already used with a different body. Returns ``None`` when
        no cached entry exists.

        A ``None`` ``key`` short-circuits to ``None`` (no idempotency
        requested).
        """
        if not key:
            return None
        request_hash = hash_request(endpoint=endpoint, body=body)
        try:
            mf, _ = _models()
            rows = _vals(
                await mf.Idempotency.filter(owner_id=owner_id, idempotency_key=key)
                .limit(1)
                .values(
                    "idempotency_key",
                    "request_hash",
                    "status_code",
                    "response_body",
                    "resource_id",
                    "resource_type",
                    "expires_at",
                )
            )
        except Exception as e:
            vcprint(f"[idempotency] lookup failed: {e!r}", color="yellow")
            return None
        row = rows[0] if rows else None
        if not row:
            return None
        if row.get("request_hash") != request_hash:
            raise IdempotencyConflict(key)
        return row

    async def persist(
        self,
        *,
        owner_id: str,
        key: str | None,
        endpoint: str,
        body: dict | list | str | None,
        status_code: int,
        response_body: dict,
        resource_id: str | None = None,
        resource_type: str | None = None,
    ) -> None:
        """Memoize the response. No-op when ``key`` is falsy. Idempotent
        — UPSERT so accidental re-persistence is safe.
        """
        if not key:
            return
        request_hash = hash_request(endpoint=endpoint, body=body)
        try:
            mf, _ = _models()
            await mf.Idempotency.upsert(
                {
                    "owner_id": owner_id,
                    "idempotency_key": key,
                    "request_hash": request_hash,
                    "endpoint": endpoint,
                    "status_code": status_code,
                    "response_body": response_body,
                    "resource_id": resource_id,
                    "resource_type": resource_type,
                },
                on_conflict=["owner_id", "idempotency_key"],
            )
        except Exception as e:
            vcprint(f"[idempotency] persist failed: {e!r}", color="yellow")


__all__ = ["IdempotencyStore", "IdempotencyConflict", "hash_request"]
