"""Idempotency-key memoization for combined operations.

Backs the ``X-Idempotency-Key`` header on combined-op endpoints (POST
/assets with bundled share/permissions/variants, PATCH /files/{id}
union, POST /files/bulk). Retry-safe: the same key + the same request
body returns the original response envelope verbatim. The same key
with a *different* body returns 409 Conflict (the FE accidentally
reused a key for two distinct requests).

Backed by the ``files.idempotency`` table. 24h TTL by default; a
host-side cron sweeps expired rows.

**Claim mode** (``claim`` / ``record_resource`` / ``complete`` / ``release``) is for work that
must never run twice and may outlive its request (a streaming save that detaches): the row is
inserted BEFORE the work (insert-then-check, ``ON CONFLICT DO NOTHING``) with ``status_code``
``CLAIM_IN_PROGRESS`` and the live run's ``request_id``; a repeat reads it back as
``in_progress`` (rejoin that run) or ``completed`` (the stored result). A claim whose run is no
longer live (the caller's ``is_live``) is taken over. Claim-mode writes RAISE on failure — a
claim that silently did not land is a second run.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Literal
from collections.abc import Awaitable, Callable

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

    async def claim(
        self,
        *,
        owner_id: str,
        key: str,
        endpoint: str,
        body: dict | list | str | None,
        request_id: str,
        lifetime: timedelta,
        is_live: Callable[[str], Awaitable[bool]],
        start_grace: timedelta = timedelta(0),
    ) -> IdempotencyClaim:
        """Take ``(owner, key)`` BEFORE the work. Raises ``IdempotencyConflict`` for another body.

        ``start_grace``: a claim younger than this counts as live whatever ``is_live`` says — the
        claim is written before the run registers anywhere ``is_live`` can see, so a retry landing
        in that gap would otherwise take over a run that is only starting (two results)."""
        request_hash = hash_request(endpoint=endpoint, body=body)
        mf, _ = _models()
        in_progress = {"status": "in_progress", "request_id": request_id, "claimed_at": datetime.now(UTC).isoformat()}
        landed = await mf.Idempotency.insert_ignore(
            {
                "owner_id": owner_id,
                "idempotency_key": key,
                "request_hash": request_hash,
                "endpoint": endpoint,
                "status_code": CLAIM_IN_PROGRESS,
                "response_body": in_progress,
                "expires_at": datetime.now(UTC) + lifetime,
            },
            on_conflict=["owner_id", "idempotency_key"],
        )
        if landed is not None:
            return IdempotencyClaim("won", request_id=request_id)
        row = await _claim_row(mf, owner_id, key)
        if row is None:  # swept between the two statements: claim again
            return await self.claim(
                owner_id=owner_id, key=key, endpoint=endpoint, body=body,
                request_id=request_id, lifetime=lifetime, is_live=is_live, start_grace=start_grace,
            )
        if row.get("request_hash") != request_hash:
            raise IdempotencyConflict(key)
        stored = row.get("response_body") or {}
        if row.get("status_code") != CLAIM_IN_PROGRESS:
            return IdempotencyClaim(
                "completed", response_body=stored, status_code=row.get("status_code"),
                resource_id=str(row["resource_id"]) if row.get("resource_id") else None,
            )
        live_request = stored.get("request_id")
        if live_request and (_claimed_within(stored, start_grace) or await is_live(str(live_request))):
            return IdempotencyClaim("in_progress", request_id=str(live_request))
        # Take over ATOMICALLY: one conditional update, keyed to the exact claim we read (its
        # ``expires_at`` is rewritten by every claim and takeover). Two retries taking over the same
        # dead run race here; Postgres lets exactly one UPDATE match, the other changes 0 rows.
        took = await mf.Idempotency.filter(
            owner_id=owner_id, idempotency_key=key,
            status_code=CLAIM_IN_PROGRESS, expires_at=row.get("expires_at"),
        ).update(response_body=in_progress, expires_at=datetime.now(UTC) + lifetime)
        if not took:
            # Another retry won the takeover a moment ago: its run is the one to rejoin.
            winner = await _claim_row(mf, owner_id, key)
            if winner is None:
                return await self.claim(
                    owner_id=owner_id, key=key, endpoint=endpoint, body=body,
                    request_id=request_id, lifetime=lifetime, is_live=is_live, start_grace=start_grace,
                )
            if winner.get("status_code") != CLAIM_IN_PROGRESS:
                return IdempotencyClaim(
                    "completed", response_body=winner.get("response_body") or {},
                    status_code=winner.get("status_code"),
                    resource_id=str(winner["resource_id"]) if winner.get("resource_id") else None,
                )
            return IdempotencyClaim(
                "in_progress", request_id=str((winner.get("response_body") or {}).get("request_id") or "")
            )
        return IdempotencyClaim(
            "won", request_id=request_id, took_over=True,
            resource_id=str(row["resource_id"]) if row.get("resource_id") else None,
        )

    async def record_resource(self, *, owner_id: str, key: str, resource_id: str, resource_type: str) -> None:
        """Name what a claimed run produced the moment it exists (a takeover then knows it)."""
        mf, _ = _models()
        await mf.Idempotency.filter(owner_id=owner_id, idempotency_key=key).update(
            resource_id=resource_id, resource_type=resource_type
        )

    async def complete(
        self, *, owner_id: str, key: str, status_code: int, response_body: dict, resource_id: str | None = None
    ) -> None:
        """Store the claimed run's result; a repeat now gets it verbatim."""
        mf, _ = _models()
        values: dict[str, Any] = {"status_code": status_code, "response_body": response_body}
        if resource_id:
            values["resource_id"] = resource_id
        await mf.Idempotency.filter(owner_id=owner_id, idempotency_key=key).update(**values)

    async def release(self, *, owner_id: str, key: str) -> None:
        """Drop a claim whose run produced nothing, so the next try starts clean."""
        mf, _ = _models()
        await mf.Idempotency.filter(owner_id=owner_id, idempotency_key=key).delete()

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


#: ``status_code`` of a claim whose work is still running (HTTP "Accepted").
CLAIM_IN_PROGRESS = 202


@dataclass(frozen=True)
class IdempotencyClaim:
    """What ``IdempotencyStore.claim`` decided.

    ``won``: this caller does the work (``took_over`` when it replaced a dead run's claim;
    ``resource_id`` then names what the dead run already produced). ``in_progress``: another
    run is live — rejoin ``request_id``. ``completed``: ``response_body`` is the stored result."""

    outcome: Literal["won", "in_progress", "completed"]
    request_id: str | None = None
    response_body: dict | None = None
    status_code: int | None = None
    resource_id: str | None = None
    took_over: bool = False


def _claimed_within(stored: dict, grace: timedelta) -> bool:
    """True when the in-progress claim was written less than ``grace`` ago (an unparseable or absent
    ``claimed_at`` — a claim written before it was recorded — is not young)."""
    if grace <= timedelta(0) or not stored.get("claimed_at"):
        return False
    try:
        claimed = datetime.fromisoformat(str(stored["claimed_at"]))
    except ValueError:
        return False
    return datetime.now(UTC) - claimed < grace


async def _claim_row(mf: Any, owner_id: str, key: str) -> dict | None:
    raw = (
        await mf.Idempotency.filter(owner_id=owner_id, idempotency_key=key)
        .limit(1)
        .values("request_hash", "status_code", "response_body", "resource_id", "expires_at")
    )
    rows = _vals(raw)
    if not rows:
        return None
    # ``expires_at`` stays the database's own value: the takeover compares it exactly (CAS).
    return {**rows[0], "expires_at": raw[0].get("expires_at")}


__all__ = [
    "CLAIM_IN_PROGRESS",
    "IdempotencyClaim",
    "IdempotencyConflict",
    "IdempotencyStore",
    "hash_request",
]
