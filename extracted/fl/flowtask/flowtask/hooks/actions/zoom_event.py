import asyncio
import hashlib
import json
import re
from datetime import datetime, timezone
from typing import ClassVar, Optional

from asyncdb import AsyncPool
from pydantic import BaseModel, Field

from flowtask.conf import default_dsn
from .abstract import AbstractAction


_PERSISTED_HEADERS = ("x-zm-trackingid", "x-zm-request-timestamp")

_TABLE_IDENT_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_.]{0,127}$")


class ZoomEventEnvelope(BaseModel):
    event: str = Field(..., min_length=1)
    account_id: str | None = None
    event_ts: datetime


class PersistZoomEvent(AbstractAction):
    """Persists every validated Zoom webhook event to navigator.zoom_events_raw."""

    table: str = "navigator.zoom_events_raw"
    dsn: str | None = None
    pool_size: int = 5

    _pool: ClassVar[Optional[object]] = None
    _pool_lock: ClassVar[Optional[asyncio.Lock]] = None

    async def open(self) -> None:
        if not _TABLE_IDENT_RE.fullmatch(self.table):
            raise ValueError(f"unsafe table identifier: {self.table!r}")
        if self.__class__._pool_lock is None:
            self.__class__._pool_lock = asyncio.Lock()
        async with self.__class__._pool_lock:
            if self.__class__._pool is None:
                pool = AsyncPool("pg", dsn=self.dsn or default_dsn, min_size=1, max_size=self.pool_size)
                await pool.connect()
                self.__class__._pool = pool

    async def close(self) -> None:
        pass  # pool lives for the duration of the process; shutdown is handled at app teardown

    async def run(
        self,
        hook,
        *,
        payload: dict | None = None,
        raw_body: bytes = b"",
        headers: dict | None = None,
        **_kwargs,
    ) -> int | None:
        if payload is None:
            self._logger.warning("PersistZoomEvent: missing payload kwarg")
            return None

        try:
            event_name = payload.get("event", "")
            event_ts_ms = payload.get("event_ts")
            event_ts = (
                datetime.fromtimestamp(event_ts_ms / 1000, tz=timezone.utc)
                if event_ts_ms
                else datetime.now(timezone.utc)
            )
            account_id = (payload.get("payload") or {}).get("account_id")
            envelope = ZoomEventEnvelope(
                event=event_name, account_id=account_id, event_ts=event_ts
            )
        except Exception as exc:
            self._logger.warning("PersistZoomEvent: invalid envelope: %s", exc)
            return None

        dedupe_hash = _compute_dedupe_hash(envelope.event, payload)
        persist_headers = {
            str(k): str(v)
            for k, v in (headers or {}).items()
            if k.lower() in _PERSISTED_HEADERS
        }

        sql = (
            f"INSERT INTO {self.table} "
            "(event, account_id, event_ts, dedupe_hash, headers, raw) "
            "VALUES ($1, $2, $3, $4, $5, $6) "
            "ON CONFLICT (dedupe_hash) DO NOTHING RETURNING id"
        )
        args = (
            envelope.event,
            envelope.account_id,
            envelope.event_ts,
            dedupe_hash,
            persist_headers,
            payload,
        )
        async with self.__class__._pool.acquire() as conn:
            row = await conn.fetch_one(sql, *args)
        return row["id"] if row else None


def _compute_dedupe_hash(event: str, payload: dict) -> str:
    """Return a SHA-256 hex digest that uniquely identifies this event.

    SMS events use a stable key built from session_id + message_id so that
    retries of the same SMS don't create duplicate rows. All other events use
    a canonical-JSON hash (sort_keys + compact separators).
    """
    if event in ("phone.sms_sent", "phone.sms_received"):
        obj = ((payload.get("payload") or {}).get("object") or {})
        sid = obj.get("session_id")
        mid = obj.get("message_id")
        if sid and mid:
            return hashlib.sha256(
                f"{event}:{sid}:{mid}".encode()
            ).hexdigest()
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()
