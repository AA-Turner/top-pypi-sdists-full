from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from typing import Any, Protocol, runtime_checkable

logger = logging.getLogger(__name__)


def _parsed_page_model() -> Any:
    """Resolve the L2 model — lazily, and ONLY for the tier that has an L2.

    This module used to import ``matrx_scraper.db.models_scraper`` at module
    scope, which drags in ``matrx_scraper.db`` → matrx-orm. matrx-orm is the
    ``[db]`` extra, so a consumer that installed
    ``matrx-scraper[browser,pdf,ocr]`` and asked only for :class:`MemoryCache`
    still paid for it — and matrx-local's local lane (the no-DB, no-proxy
    desktop lane) died at ``from matrx_scraper.cache import MemoryCache`` with
    ``ImportError: cannot import name 'PLATFORM_DB_ENV_PREFIX' from
    'matrx_orm'`` the moment the installed matrx-orm was older than the one
    ``db/__init__.py`` needs. An optional extra must never be reachable from a
    core import; pinned by ``tests/test_host_independence.py``.
    """
    from matrx_scraper.db.models_scraper import ScrapeParsedPage

    return ScrapeParsedPage


@runtime_checkable
class CacheBackend(Protocol):
    async def get(self, key: str) -> dict[str, Any] | None: ...
    async def set(
        self,
        key: str,
        url: str,
        domain: str,
        content: dict[str, Any],
        content_type: str,
        char_count: int,
        ttl_days: int = 30,
    ) -> None: ...
    async def invalidate(self, key: str) -> None: ...


class MemoryCache:
    """In-process TTL cache backed by cachetools."""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 1800) -> None:
        try:
            from cachetools import TTLCache
        except ImportError:
            raise ImportError("cachetools is required for MemoryCache: pip install cachetools")
        self._cache: TTLCache[str, dict[str, Any]] = TTLCache(maxsize=max_size, ttl=ttl_seconds)

    async def get(self, key: str) -> dict[str, Any] | None:
        hit = self._cache.get(key)
        if hit is not None:
            logger.debug("MemoryCache HIT: %s", key)
        return hit

    async def set(
        self,
        key: str,
        url: str,
        domain: str,
        content: dict[str, Any],
        content_type: str,
        char_count: int,
        ttl_days: int = 30,
    ) -> None:
        self._cache[key] = {
            "content": content,
            "url": url,
            "domain": domain,
            "scraped_at": datetime.now(UTC).isoformat(),
            "content_type": content_type,
            "char_count": char_count,
        }
        logger.debug("MemoryCache SET: %s", key)

    async def invalidate(self, key: str) -> None:
        self._cache.pop(key, None)


class TwoTierCache:
    """L1 in-memory + L2 PostgreSQL cache, matching the scraper-service PageCache.

    All L2 reads/writes go through the matrx-orm ``ScrapeParsedPage`` model,
    which resolves its registered connection.
    """

    def __init__(
        self,
        pool: Any | None = None,
        max_size: int = 1000,
        ttl_seconds: int = 1800,
    ) -> None:
        # Backward-compatible host wiring only. L2 access is exclusively
        # through ScrapeParsedPage and never through the injected raw pool.
        _ = pool
        try:
            from cachetools import TTLCache
        except ImportError:
            raise ImportError("cachetools is required for TwoTierCache: pip install cachetools")
        self._memory: TTLCache[str, dict[str, Any]] = TTLCache(maxsize=max_size, ttl=ttl_seconds)
        # Resolve the L2 model here, not at import: constructing a TwoTierCache
        # IS the declaration that this consumer has the [db] extra, so a missing
        # or mismatched matrx-orm fails loud at the point of the wrong choice.
        self._page = _parsed_page_model()

    async def get(self, key: str) -> dict[str, Any] | None:
        if key in self._memory:
            logger.debug("Cache HIT (memory): %s", key)
            return self._memory[key]

        now = datetime.now(UTC)
        rows = await (
            self._page.filter(page_name=key, validity="active", expires_at__gt=now)
            .limit(1)
            .values("content", "url", "domain", "scraped_at", "content_type", "char_count")
        )

        if rows:
            row = rows[0]
            data = {
                "content": row["content"],
                "url": row["url"],
                "domain": row["domain"],
                "scraped_at": row["scraped_at"].isoformat() if row["scraped_at"] else None,
                "content_type": row["content_type"],
                "char_count": row["char_count"],
            }
            self._memory[key] = data
            logger.debug("Cache HIT (db): %s", key)
            return data

        logger.debug("Cache MISS: %s", key)
        return None

    async def set(
        self,
        key: str,
        url: str,
        domain: str,
        content: dict[str, Any],
        content_type: str,
        char_count: int,
        ttl_days: int = 30,
    ) -> None:
        now = datetime.now(UTC)
        expires_at = now + timedelta(days=ttl_days)

        await self._page.update_where(
            {"page_name": key, "validity": "active"},
            validity="stale",
        )
        await self._page.create(
            page_name=key,
            url=url,
            domain=domain,
            scraped_at=now,
            expires_at=expires_at,
            validity="active",
            content=content,
            char_count=char_count,
            content_type=content_type,
        )

        data = {
            "content": content,
            "url": url,
            "domain": domain,
            "scraped_at": now.isoformat(),
            "content_type": content_type,
            "char_count": char_count,
        }
        self._memory[key] = data
        logger.debug("Cache SET: %s (expires %s)", key, expires_at.isoformat())

    async def invalidate(self, key: str) -> None:
        self._memory.pop(key, None)
        await self._page.update_where(
            {"page_name": key, "validity": "active"},
            validity="invalid",
        )
