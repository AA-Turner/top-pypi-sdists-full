from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from typing import Any, Protocol, runtime_checkable

logger = logging.getLogger(__name__)

# The cache row is TENANT DATA, not a shared public artifact. `scraper.
# scrape_parsed_page` is an org-scoped entity (`_is_org_scoped = True`,
# `_rls_variant = "restricted"`, `organization_id NOT NULL` with NO column
# default and NO stamping trigger in the live database), and every scraper
# router already refuses a call that names no organization
# (`matrx_connect.service_auth`, FEATURE.md § THE ORGANIZATION IS ON THE WIRE).
# So the organization is available at the write, and it is carried here — never
# rebuilt, never defaulted, never left to a trigger.
_ORG_REFUSAL = (
    "The page cache writes/reads %s, an organization-scoped row, but this call "
    "carries no organization. Pass organization_id= explicitly (routers resolve "
    "it with matrx_connect.service_auth.confirm_request_organization), or run "
    "under a request context that carries one (matrx_utils configure_context / "
    "set_manual_context). The cache never chooses an organization for you."
)


class CacheOrganizationRequired(ValueError):
    """A cache read/write reached this cache with no organization to act in."""


def resolve_cache_organization_id(
    organization_id: str | None = None, *, what: str = "scraper.scrape_parsed_page"
) -> str:
    """The organization this cache operation acts in. Refuses rather than guess.

    1. an explicit argument — the caller resolved it at the boundary and it wins;
    2. the organization on the carried request context (``matrx_utils.ctx``),
       which is what the host installs for the admitted request;
    3. nothing — raise. There is no personal, system, or platform default here.
    """
    explicit = str(organization_id or "").strip()
    if explicit:
        return explicit
    try:
        from matrx_utils.ctx import get_active_organization_id

        carried = str(get_active_organization_id() or "").strip()
    except Exception:  # noqa: BLE001 — a missing context seam is "no organization"
        carried = ""
    if carried:
        return carried
    raise CacheOrganizationRequired(_ORG_REFUSAL % what)


def _memory_key(organization_id: str, key: str) -> str:
    """L1 keys are per-organization too.

    The L2 row is org-scoped, so an L1 keyed on ``page_name`` alone would hand
    one tenant's scraped copy of a page to the next tenant that asks for the
    same URL — the same cross-tenant read, one tier up.
    """
    return f"{organization_id}\x1f{key}"


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
    async def get(self, key: str, *, organization_id: str | None = None) -> dict[str, Any] | None: ...
    async def set(
        self,
        key: str,
        url: str,
        domain: str,
        content: dict[str, Any],
        content_type: str,
        char_count: int,
        ttl_days: int = 30,
        organization_id: str | None = None,
    ) -> None: ...
    async def invalidate(self, key: str, *, organization_id: str | None = None) -> None: ...


class MemoryCache:
    """In-process TTL cache backed by cachetools.

    Partitioned by organization exactly like the two-tier cache. The no-DB
    desktop lane (matrx-local) has no request context and no tenancy at all, so
    an absent organization here is a named partition (``__no_organization__``)
    rather than a refusal — this tier writes nothing to the database, so the
    NOT NULL law it would violate does not apply. What it must never do is let
    one organization read another's entry, and the partition is what prevents
    that.
    """

    NO_ORGANIZATION = "__no_organization__"

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 1800) -> None:
        try:
            from cachetools import TTLCache
        except ImportError:
            raise ImportError("cachetools is required for MemoryCache: pip install cachetools")
        self._cache: TTLCache[str, dict[str, Any]] = TTLCache(maxsize=max_size, ttl=ttl_seconds)

    def _partition(self, organization_id: str | None) -> str:
        try:
            return resolve_cache_organization_id(organization_id, what="the in-memory page cache")
        except CacheOrganizationRequired:
            return self.NO_ORGANIZATION

    async def get(self, key: str, *, organization_id: str | None = None) -> dict[str, Any] | None:
        hit = self._cache.get(_memory_key(self._partition(organization_id), key))
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
        organization_id: str | None = None,
    ) -> None:
        self._cache[_memory_key(self._partition(organization_id), key)] = {
            "content": content,
            "url": url,
            "domain": domain,
            "scraped_at": datetime.now(UTC).isoformat(),
            "content_type": content_type,
            "char_count": char_count,
        }
        logger.debug("MemoryCache SET: %s", key)

    async def invalidate(self, key: str, *, organization_id: str | None = None) -> None:
        self._cache.pop(_memory_key(self._partition(organization_id), key), None)


class TwoTierCache:
    """L1 in-memory + L2 PostgreSQL cache, matching the scraper-service PageCache.

    All L2 reads/writes go through the matrx-orm ``ScrapeParsedPage`` model,
    which resolves its registered connection.

    🚨 **Every operation names the organization it acts in.** The L2 row is
    org-scoped tenant data, so a write with no organization is refused
    (:class:`CacheOrganizationRequired`) rather than defaulted, and a read is
    filtered by the same organization — a cache hit on another tenant's row
    would be a cross-tenant read of their scraped copy of the page.
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

    async def get(self, key: str, *, organization_id: str | None = None) -> dict[str, Any] | None:
        org = resolve_cache_organization_id(organization_id)
        mem_key = _memory_key(org, key)
        if mem_key in self._memory:
            logger.debug("Cache HIT (memory): %s", key)
            return self._memory[mem_key]

        now = datetime.now(UTC)
        rows = await (
            self._page.filter(
                page_name=key,
                organization_id=org,
                validity="active",
                expires_at__gt=now,
            )
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
            self._memory[mem_key] = data
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
        organization_id: str | None = None,
    ) -> None:
        org = resolve_cache_organization_id(organization_id)
        now = datetime.now(UTC)
        expires_at = now + timedelta(days=ttl_days)

        await self._page.update_where(
            {"page_name": key, "organization_id": org, "validity": "active"},
            validity="stale",
        )
        await self._page.create(
            page_name=key,
            organization_id=org,
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
        self._memory[_memory_key(org, key)] = data
        logger.debug("Cache SET: %s (expires %s)", key, expires_at.isoformat())

    async def invalidate(self, key: str, *, organization_id: str | None = None) -> None:
        org = resolve_cache_organization_id(organization_id)
        self._memory.pop(_memory_key(org, key), None)
        await self._page.update_where(
            {"page_name": key, "organization_id": org, "validity": "active"},
            validity="invalid",
        )
