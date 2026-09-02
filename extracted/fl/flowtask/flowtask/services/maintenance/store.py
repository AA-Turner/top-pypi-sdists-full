"""Persistence for the Maintenance service.

Failures, startup-job outcomes and maintenance windows are persisted to Redis
so the status page survives restarts and can be audited (SOC2 CC8). Redis is
optional: if it is unreachable the store degrades gracefully to an in-process
fallback and flags itself as ``degraded`` instead of raising, so a monitoring
surface never takes the server down with it.
"""
from __future__ import annotations

import logging
from collections import deque
from typing import Optional

import orjson

try:  # redis is a hard dependency of Flowtask, but keep the import defensive.
    from redis import asyncio as aioredis
    from redis.exceptions import RedisError
except ImportError:  # pragma: no cover - redis always present in prod
    aioredis = None  # type: ignore[assignment]

    class RedisError(Exception):  # type: ignore[no-redef]
        """Fallback error type when redis is unavailable."""


from .models import FailureRecord, MaintenanceWindow

logger = logging.getLogger(__name__)

# How many failure records to retain (both in Redis and in-memory fallback).
MAX_FAILURES = 500


class MaintenanceStore:
    """Redis-backed store with an in-memory fallback.

    Args:
        redis_url: Redis DSN. When ``None`` (or unreachable) the store keeps
            everything in memory and marks itself :attr:`degraded`.
        namespace: Key prefix for every Redis key owned by this store.
    """

    def __init__(
        self,
        redis_url: Optional[str] = None,
        *,
        namespace: str = "flowtask:maintenance",
    ) -> None:
        self.redis_url = redis_url
        self.namespace = namespace
        self._redis = None
        self.degraded: bool = False
        self.logger = logger
        # In-memory fallbacks (also used as a mirror when Redis is down).
        self._mem_failures: deque = deque(maxlen=MAX_FAILURES)
        self._mem_startup: dict[str, dict] = {}
        self._mem_windows: dict[str, dict] = {}

    # -- key helpers -------------------------------------------------------
    def _key(self, suffix: str) -> str:
        return f"{self.namespace}:{suffix}"

    @property
    def _failures_key(self) -> str:
        return self._key("failures")

    @property
    def _startup_key(self) -> str:
        return self._key("startup")

    @property
    def _windows_key(self) -> str:
        return self._key("windows")

    # -- lifecycle ---------------------------------------------------------
    async def open(self) -> "MaintenanceStore":
        """Connect to Redis, degrading to memory on any failure."""
        if aioredis is None or not self.redis_url:
            self.degraded = True
            self.logger.warning(
                "MaintenanceStore running WITHOUT Redis; using in-memory store."
            )
            return self
        try:
            self._redis = aioredis.from_url(
                self.redis_url, encoding="utf-8", decode_responses=True
            )
            await self._redis.ping()
            self.degraded = False
        except (RedisError, OSError) as err:
            self.degraded = True
            self._redis = None
            self.logger.warning(
                "MaintenanceStore could not reach Redis (%s); "
                "falling back to in-memory store.",
                err,
            )
        return self

    async def close(self) -> None:
        """Close the Redis connection if one was opened."""
        if self._redis is not None:
            try:
                await self._redis.close()
                await self._redis.connection_pool.disconnect()
            except Exception:  # pragma: no cover - best-effort teardown
                pass
            finally:
                self._redis = None

    # -- failures ----------------------------------------------------------
    async def record_failure(self, component: str, detail: str = "") -> FailureRecord:
        """Persist a failure/incident and return the stored record."""
        record = FailureRecord(component=component, detail=detail)
        payload = orjson.dumps(record.model_dump(mode="json")).decode("utf-8")
        self._mem_failures.appendleft(payload)
        if self._redis is not None:
            try:
                pipe = self._redis.pipeline()
                pipe.lpush(self._failures_key, payload)
                pipe.ltrim(self._failures_key, 0, MAX_FAILURES - 1)
                await pipe.execute()
            except RedisError as err:  # pragma: no cover - network dependent
                self.degraded = True
                self.logger.error("Failed to persist failure to Redis: %s", err)
        return record

    async def recent_failures(self, limit: int = 50) -> list[FailureRecord]:
        """Return the most recent failures, newest first."""
        raw: list[str] = []
        if self._redis is not None:
            try:
                raw = await self._redis.lrange(self._failures_key, 0, limit - 1)
            except RedisError as err:  # pragma: no cover - network dependent
                self.degraded = True
                self.logger.error("Failed to read failures from Redis: %s", err)
        if not raw:
            raw = list(self._mem_failures)[:limit]
        return [FailureRecord(**orjson.loads(item)) for item in raw]

    # -- startup-job outcomes ---------------------------------------------
    async def set_startup(self, name: str, ok: bool, detail: str = "") -> None:
        """Record the outcome of a startup job/probe."""
        record = FailureRecord(component=name, detail=detail).model_dump(mode="json")
        record["ok"] = ok
        payload = orjson.dumps(record).decode("utf-8")
        self._mem_startup[name] = record
        if self._redis is not None:
            try:
                await self._redis.hset(self._startup_key, name, payload)
            except RedisError as err:  # pragma: no cover - network dependent
                self.degraded = True
                self.logger.error("Failed to persist startup state: %s", err)

    async def get_startup(self) -> dict[str, dict]:
        """Return the recorded startup-job outcomes keyed by name."""
        if self._redis is not None:
            try:
                raw = await self._redis.hgetall(self._startup_key)
                if raw:
                    return {k: orjson.loads(v) for k, v in raw.items()}
            except RedisError as err:  # pragma: no cover - network dependent
                self.degraded = True
                self.logger.error("Failed to read startup state: %s", err)
        return dict(self._mem_startup)

    # -- maintenance windows ----------------------------------------------
    async def save_window(self, window: MaintenanceWindow) -> MaintenanceWindow:
        """Persist a maintenance window (must already carry an identifier)."""
        if not window.identifier:
            raise ValueError("MaintenanceWindow requires an identifier to be saved")
        payload = orjson.dumps(window.model_dump(mode="json")).decode("utf-8")
        self._mem_windows[window.identifier] = orjson.loads(payload)
        if self._redis is not None:
            try:
                await self._redis.hset(self._windows_key, window.identifier, payload)
            except RedisError as err:  # pragma: no cover - network dependent
                self.degraded = True
                self.logger.error("Failed to persist maintenance window: %s", err)
        return window

    async def list_windows(self) -> list[MaintenanceWindow]:
        """Return every stored maintenance window sorted by start time."""
        raw: dict[str, str] = {}
        if self._redis is not None:
            try:
                raw = await self._redis.hgetall(self._windows_key)
            except RedisError as err:  # pragma: no cover - network dependent
                self.degraded = True
                self.logger.error("Failed to read maintenance windows: %s", err)
        items: list[dict] = []
        if raw:
            items = [orjson.loads(v) for v in raw.values()]
        else:
            items = list(self._mem_windows.values())
        windows = [MaintenanceWindow(**item) for item in items]
        windows.sort(key=lambda w: (w.day, w.start_time))
        return windows

    async def remove_window(self, identifier: str) -> bool:
        """Delete a maintenance window; return ``True`` when one was removed."""
        existed = self._mem_windows.pop(identifier, None) is not None
        if self._redis is not None:
            try:
                removed = await self._redis.hdel(self._windows_key, identifier)
                existed = existed or bool(removed)
            except RedisError as err:  # pragma: no cover - network dependent
                self.degraded = True
                self.logger.error("Failed to remove maintenance window: %s", err)
        return existed
