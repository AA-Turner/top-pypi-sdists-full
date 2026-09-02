from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any, Protocol, runtime_checkable
from uuid import UUID

logger = logging.getLogger(__name__)


def _domain_models() -> tuple[Any, Any, Any, Any]:
    """Resolve the ``scraper.*`` models — lazily, and only for the Postgres store.

    These were imported at module scope, so ``from matrx_scraper.domain_config
    import StaticDomainConfigStore`` — the static, zero-DB store a desktop or
    standalone consumer uses — pulled in ``matrx_scraper.db`` and therefore
    matrx-orm, an OPTIONAL ``[db]`` extra. Same defect as ``cache.py``; pinned
    by ``tests/test_host_independence.py``.
    """
    from matrx_scraper.db.models_scraper import (
        ScrapeDomain,
        ScrapeDomainSettings,
        ScrapePathOverride,
        ScrapePathPattern,
    )

    return ScrapeDomain, ScrapeDomainSettings, ScrapePathOverride, ScrapePathPattern


REFRESH_INTERVAL_SECONDS = 300


@runtime_checkable
class DomainConfigBackend(Protocol):
    def is_scrape_allowed(self, url: str) -> bool: ...
    def get_proxy_type(self, url: str) -> str: ...
    def get_overrides_for_path(self, url: str, path: str) -> dict[str, list[dict[str, object]]]: ...


# ---------------------------------------------------------------------------
# Pydantic-free data classes (keep package dependency-light)
# ---------------------------------------------------------------------------


class OverrideRule:
    __slots__ = (
        "id",
        "path_pattern_id",
        "is_active",
        "config_type",
        "selector_type",
        "match_type",
        "action",
        "values",
    )

    def __init__(
        self,
        id: UUID,
        path_pattern_id: UUID,
        is_active: bool = True,
        config_type: str = "content_filter",
        selector_type: str = "",
        match_type: str = "exact",
        action: str = "add",
        values: list[str] | None = None,
    ) -> None:
        self.id = id
        self.path_pattern_id = path_pattern_id
        self.is_active = is_active
        self.config_type = config_type
        self.selector_type = selector_type
        self.match_type = match_type
        self.action = action
        self.values = values or []


class PathPatternConfig:
    __slots__ = (
        "id",
        "domain_id",
        "pattern",
        "overrides",
        "policy_action",
        "min_content_chars",
        "min_real_content_chars",
        "content_selector",
        "policy_notes",
        "category",
        "category_reason",
    )

    def __init__(
        self,
        id: UUID,
        domain_id: UUID,
        pattern: str,
        *,
        policy_action: str | None = None,
        min_content_chars: int | None = None,
        min_real_content_chars: int | None = None,
        content_selector: str | None = None,
        policy_notes: str | None = None,
        category: str | None = None,
        category_reason: str | None = None,
    ) -> None:
        self.id = id
        self.domain_id = domain_id
        self.pattern = pattern
        self.overrides: list[OverrideRule] = []
        self.policy_action = policy_action
        self.min_content_chars = min_content_chars
        self.min_real_content_chars = min_real_content_chars
        self.content_selector = content_selector
        self.policy_notes = policy_notes
        self.category = category
        self.category_reason = category_reason


class DomainSettings:
    __slots__ = ("id", "domain_id", "enabled", "proxy_type")

    def __init__(
        self, id: UUID, domain_id: UUID, enabled: bool = True, proxy_type: str = "datacenter"
    ) -> None:
        self.id = id
        self.domain_id = domain_id
        self.enabled = enabled
        self.proxy_type = proxy_type


class DomainConfig:
    __slots__ = (
        "id",
        "url",
        "common_name",
        "scrape_allowed",
        "settings",
        "path_patterns",
        "policy_action",
        "min_content_chars",
        "min_real_content_chars",
        "content_selector",
        "policy_notes",
        "category",
        "category_reason",
    )

    def __init__(
        self,
        id: UUID,
        url: str,
        common_name: str | None = None,
        scrape_allowed: bool = True,
        settings: DomainSettings | None = None,
        *,
        policy_action: str | None = None,
        min_content_chars: int | None = None,
        min_real_content_chars: int | None = None,
        content_selector: str | None = None,
        policy_notes: str | None = None,
        category: str | None = None,
        category_reason: str | None = None,
    ) -> None:
        self.id = id
        self.url = url
        self.common_name = common_name
        self.scrape_allowed = scrape_allowed
        self.settings = settings
        self.path_patterns: list[PathPatternConfig] = []
        self.policy_action = policy_action
        self.min_content_chars = min_content_chars
        self.min_real_content_chars = min_real_content_chars
        self.content_selector = content_selector
        self.policy_notes = policy_notes
        self.category = category
        self.category_reason = category_reason


# ---------------------------------------------------------------------------
# Static (in-memory) implementation for tests / offline use
# ---------------------------------------------------------------------------


class StaticDomainConfigStore:
    """Hardcoded domain rules — no DB required."""

    def __init__(self, blocked_domains: set[str] | None = None) -> None:
        self._blocked = blocked_domains or set()

    def is_scrape_allowed(self, url: str) -> bool:
        from matrx_scraper.utils.url import extract_domain

        return extract_domain(url) not in self._blocked

    def get_proxy_type(self, url: str) -> str:
        return "datacenter"

    def get_overrides_for_path(self, url: str, path: str) -> dict[str, list[dict[str, object]]]:
        return {}


# ---------------------------------------------------------------------------
# PostgreSQL-backed implementation
# ---------------------------------------------------------------------------


class PostgresDomainConfigStore:
    """Loads domain configs from PostgreSQL and refreshes periodically."""

    def __init__(self, pool: Any | None = None) -> None:
        # Backward-compatible host wiring only. All DB access is through the
        # package's matrx-orm models; the injected raw pool is never used.
        _ = pool
        # Constructing the Postgres store IS the declaration that this consumer
        # has the [db] extra — resolve here, so a missing/mismatched matrx-orm
        # fails loud at the point of the wrong choice, not at someone else's import.
        (
            self._m_domain,
            self._m_settings,
            self._m_override,
            self._m_pattern,
        ) = _domain_models()
        self._domains: dict[str, DomainConfig] = {}
        self._refresh_task: asyncio.Task[None] | None = None
        self._healthy = False
        self._last_error: str | None = None

    async def start(self) -> None:
        # The initial load is part of readiness. Registering an empty, fail-open
        # store after a schema error makes health checks lie and silently disables
        # permission/proxy/path rules.
        try:
            await self._refresh(raise_on_error=True)
        except Exception as exc:
            logger.critical(
                "🚨 PostgresDomainConfigStore: INITIAL load FAILED. Refusing to "
                "register an inert fail-open store with zero domain configs; "
                "fix the canonical scrape_domain* schema.",
            )
            raise RuntimeError("domain config initial load failed") from exc
        self._refresh_task = asyncio.create_task(self._periodic_refresh())
        logger.info("PostgresDomainConfigStore started (%d domains)", len(self._domains))

    async def stop(self) -> None:
        if self._refresh_task and not self._refresh_task.done():
            self._refresh_task.cancel()
            try:
                await self._refresh_task
            except asyncio.CancelledError:
                pass
        logger.info("PostgresDomainConfigStore stopped")

    async def refresh(self) -> None:
        await self._refresh()

    async def _refresh(self, *, raise_on_error: bool = False) -> None:
        try:
            domains = await self._load_all_domains()
            self._domains = {d.url: d for d in domains}
            self._healthy = True
            self._last_error = None
            logger.debug("PostgresDomainConfigStore refreshed: %d domains", len(self._domains))
        except Exception as exc:
            self._healthy = False
            self._last_error = f"{type(exc).__name__}: {exc}"
            logger.exception("Failed to refresh PostgresDomainConfigStore")
            if raise_on_error:
                raise

    @property
    def healthy(self) -> bool:
        return self._healthy

    async def _periodic_refresh(self) -> None:
        while True:
            await asyncio.sleep(REFRESH_INTERVAL_SECONDS)
            await self._refresh()

    def _get_domain(self, url: str) -> DomainConfig | None:
        from matrx_scraper.utils.url import extract_domain

        domain_name = extract_domain(url)
        return self._domains.get(domain_name)

    def get_domain_by_host(self, host: str) -> DomainConfig | None:
        return self._domains.get(host.lower())

    def is_scrape_allowed(self, url: str) -> bool:
        config = self._get_domain(url)
        if config is None:
            return True
        return config.scrape_allowed

    def get_proxy_type(self, url: str) -> str:
        config = self._get_domain(url)
        if config is None or config.settings is None:
            return "datacenter"
        return config.settings.proxy_type

    def get_overrides_for_path(self, url: str, path: str) -> dict[str, list[dict[str, object]]]:
        config = self._get_domain(url)
        if config is None or not config.path_patterns:
            return {}

        from matrx_scraper.utils.url import match_path

        patterns = [pp.pattern for pp in config.path_patterns]
        matched = match_path(path, patterns)
        if matched is None:
            return {}

        for pp in config.path_patterns:
            if pp.pattern == matched:
                result: dict[str, list[dict[str, object]]] = {
                    "content_filter": [],
                    "main_content": [],
                }
                for override in pp.overrides:
                    if not override.is_active:
                        continue
                    result[override.config_type].append(
                        {
                            "selector_type": override.selector_type,
                            "match_type": override.match_type,
                            "action": override.action,
                            "values": override.values,
                        }
                    )
                return result
        return {}

    @property
    def all_domains(self) -> list[DomainConfig]:
        return list(self._domains.values())

    # ------------------------------------------------------------------
    # DB queries
    # ------------------------------------------------------------------

    async def _load_all_domains(self) -> list[DomainConfig]:
        domain_rows = (
            await self._m_domain.filter()
            .order_by("url")
            .values(
                "id",
                "url",
                "common_name",
                "scrape_allowed",
                "policy_action",
                "min_content_chars",
                "min_real_content_chars",
                "content_selector",
                "policy_notes",
                "category",
                "category_reason",
            )
        )

        domains: dict[UUID, DomainConfig] = {}
        for row in domain_rows:
            domain_id = row["id"]
            domains[domain_id] = DomainConfig(
                id=domain_id,
                url=row["url"],
                common_name=row["common_name"],
                scrape_allowed=row["scrape_allowed"],
                settings=None,
                policy_action=row["policy_action"],
                min_content_chars=row["min_content_chars"],
                min_real_content_chars=row["min_real_content_chars"],
                content_selector=row["content_selector"],
                policy_notes=row["policy_notes"],
                category=row["category"],
                category_reason=row["category_reason"],
            )

        if not domains:
            return []

        settings_rows = await self._m_settings.filter(domain_id__in=list(domains.keys())).values(
            "id", "domain_id", "enabled", "proxy_type"
        )
        for row in settings_rows:
            domain_id = row["domain_id"]
            if domain_id in domains:
                domains[domain_id].settings = DomainSettings(
                    id=row["id"],
                    domain_id=domain_id,
                    enabled=row["enabled"],
                    proxy_type=row["proxy_type"],
                )

        pp_rows = await (
            self._m_pattern.filter(scrape_domain_id__in=list(domains.keys()))
            .order_by("scrape_domain_id", "path_pattern")
            .values(
                "id",
                "scrape_domain_id",
                "path_pattern",
                "policy_action",
                "min_content_chars",
                "min_real_content_chars",
                "content_selector",
                "policy_notes",
                "category",
                "category_reason",
            )
        )

        patterns: dict[UUID, PathPatternConfig] = {}
        for row in pp_rows:
            domain_id = row["scrape_domain_id"]
            pp = PathPatternConfig(
                id=row["id"],
                domain_id=domain_id,
                pattern=row["path_pattern"],
                policy_action=row["policy_action"],
                min_content_chars=row["min_content_chars"],
                min_real_content_chars=row["min_real_content_chars"],
                content_selector=row["content_selector"],
                policy_notes=row["policy_notes"],
                category=row["category"],
                category_reason=row["category_reason"],
            )
            patterns[pp.id] = pp
            if domain_id in domains:
                domains[domain_id].path_patterns.append(pp)

        if patterns:
            override_rows = await (
                self._m_override.filter(path_pattern_id__in=list(patterns.keys()))
                .order_by("path_pattern_id")
                .values(
                    "id",
                    "path_pattern_id",
                    "is_active",
                    "config_type",
                    "selector_type",
                    "match_type",
                    "action",
                    "values",
                )
            )

            for row in override_rows:
                # jsonb column — the ORM returns it already decoded as a
                # native list (never a string to re-`json.loads`).
                override = OverrideRule(
                    id=row["id"],
                    path_pattern_id=row["path_pattern_id"],
                    is_active=row["is_active"],
                    config_type=row["config_type"],
                    selector_type=row["selector_type"],
                    match_type=row["match_type"],
                    action=row["action"],
                    values=row["values"],
                )
                if row["path_pattern_id"] in patterns:
                    patterns[row["path_pattern_id"]].overrides.append(override)

        return list(domains.values())

    async def upsert_domain(
        self,
        url: str,
        common_name: str | None,
        scrape_allowed: bool,
        enabled: bool,
        proxy_type: str,
    ) -> dict[str, Any]:
        now = datetime.now(UTC)
        domain = await self._m_domain.upsert(
            {
                "url": url,
                "common_name": common_name,
                "scrape_allowed": scrape_allowed,
                "updated_at": now,
            },
            conflict_fields=["url"],
            update_fields=["common_name", "scrape_allowed", "updated_at"],
        )
        domain_id = domain.id

        await self._m_settings.upsert(
            {
                "domain_id": domain_id,
                "enabled": enabled,
                "proxy_type": proxy_type,
                "updated_at": now,
            },
            conflict_fields=["domain_id"],
            update_fields=["enabled", "proxy_type", "updated_at"],
        )

        await self._refresh()
        return {"id": str(domain_id), "url": url, "scrape_allowed": scrape_allowed}
