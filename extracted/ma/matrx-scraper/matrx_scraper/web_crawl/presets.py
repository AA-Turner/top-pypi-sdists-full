"""Crawl presets and one-click rescrape config derivation.

A **preset** is a saved, named ``CrawlStartRequest`` bound to one ``web.site``.
The stored config IS the request model — there is no parallel preset-config
shape, so a preset can never encode a crawl the crawler cannot run.

**Recrawl derivation** answers the only question a "Rescrape" button has: *with
what config?* Resolution order, most specific first:

1. an explicitly named preset (``preset_id``),
2. the site's pinned default preset (``web.site.settings.crawl.default_preset_id``),
3. the most recent site-wide crawl session's persisted request,
4. ``CrawlStartRequest()`` defaults.

Every answer reports its ``source`` (and the preset/session it came from) so the
UI states what it is about to run instead of asking the user to trust it.

Authorization is the site's, always: reads require ``viewer`` on the site,
writes require ``editor``. Both are enforced by RLS on ``web.crawl_preset``
inside the claim-bound session — the same kernel every other ``web.*`` row uses.
"""

from __future__ import annotations

import logging

from pydantic import ValidationError

from matrx_orm import F, OrderBy
from matrx_utils import utcnow

from matrx_scraper.db.models_web import (
    CrawlPreset as WebCrawlPreset,
    CrawlSession as WebCrawlSession,
    Site as WebSite,
)
from matrx_scraper.web_crawl.contracts import (
    CrawlPresetRecord,
    CrawlPresetSaveRequest,
    CrawlStartRequest,
    RecrawlConfigResponse,
)
from matrx_scraper.web_crawl.persistence import WebCrawlRepository

logger = logging.getLogger(__name__)

# A preset is only meaningful for a crawl the whole site goes through; a
# homepage bootstrap or a single page fetch is not a config anyone re-runs.
RECRAWL_SOURCE_MODES = ("full", "list")
# How far back the derivation looks for a reusable session request. A site with
# a long history of non-crawl sessions (sitemap/gsc/analysis all create rows)
# still finds its last real crawl; beyond this we fall back to defaults rather
# than scan the whole ledger.
SESSION_SCAN_LIMIT = 50
# Presets are a human-curated list, not a data set.
PRESET_LIST_LIMIT = 200
# Where a site pins its default preset inside the namespaced settings bag.
SITE_SETTINGS_CRAWL_KEY = "crawl"
SITE_SETTINGS_DEFAULT_PRESET_KEY = "default_preset_id"

_SAVE_UPDATE_FIELDS = ["description", "config", "deleted_at"]


def _record(row: WebCrawlPreset) -> CrawlPresetRecord:
    """Project a stored row, keeping a config that no longer validates VISIBLE.

    Dropping an unparseable preset from the list would make the user's saved
    work vanish with no explanation; coercing it would silently run a crawl
    they never configured. Neither is acceptable — so it comes back flagged,
    with the raw payload attached so it can be repaired.
    """

    raw = row.config if isinstance(row.config, dict) else {}
    config: CrawlStartRequest | None = None
    config_error: str | None = None
    try:
        config = CrawlStartRequest.model_validate(raw)
    except ValidationError as exc:
        config_error = f"stored crawl config is no longer valid: {exc.error_count()} problem(s)"
        logger.warning("crawl preset %s has an invalid stored config: %s", row.id, exc)
    return CrawlPresetRecord(
        id=str(row.id),
        site_id=str(row.site_id),
        name=row.name,
        description=row.description,
        config=config,
        config_error=config_error,
        raw_config=raw if config is None else None,
        last_used_at=row.last_used_at,
        use_count=int(row.use_count or 0),
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class CrawlPresetRepository:
    """RLS-scoped CRUD for ``web.crawl_preset``.

    Composes the canonical :class:`WebCrawlRepository` rather than re-deriving
    claims or re-opening a session — one claim-bound session builder for the
    whole crawler.
    """

    def __init__(self, repository: WebCrawlRepository) -> None:
        self.repository = repository

    async def list_for_site(self, site_id: str) -> list[CrawlPresetRecord]:
        """Presets for a site, most-recently-used first, never-used last."""

        async with self.repository.rls():
            rows = await (
                WebCrawlPreset.filter(site_id=site_id, deleted_at__isnull=True)
                .order_by(OrderBy("last_used_at", descending=True, nulls="last"), "name")
                .limit(PRESET_LIST_LIMIT)
                .all(use_cache=False)
            )
        return [_record(row) for row in rows]

    async def load(self, preset_id: str) -> WebCrawlPreset:
        async with self.repository.rls():
            row = await WebCrawlPreset.get_or_none(
                use_cache=False,
                id=preset_id,
                deleted_at__isnull=True,
            )
        if row is None:
            raise LookupError(f"crawl preset {preset_id} does not exist or is not accessible")
        return row

    async def save(self, site_id: str, request: CrawlPresetSaveRequest) -> CrawlPresetRecord:
        """Upsert by ``(site_id, name)``.

        ``deleted_at`` is cleared on update: re-saving a name the user deleted
        restores that preset with the new config rather than failing on a
        unique key they cannot see.
        """

        async with self.repository.rls():
            row = await WebCrawlPreset.upsert(
                {
                    "site_id": site_id,
                    "name": request.name,
                    "description": request.description,
                    "config": request.config.model_dump(mode="json"),
                    "deleted_at": None,
                },
                conflict_fields=["site_id", "name"],
                update_fields=_SAVE_UPDATE_FIELDS,
            )
        return _record(row)

    async def touch(self, preset_id: str) -> None:
        """Bump ``last_used_at`` + ``use_count`` — an atomic ``F`` counter, so
        two concurrent crawls from one preset cannot lose an increment."""

        async with self.repository.rls():
            await WebCrawlPreset.update_where(
                {"id": preset_id, "deleted_at__isnull": True},
                last_used_at=utcnow(),
                use_count=F("use_count") + 1,
            )

    async def delete(self, preset_id: str) -> bool:
        """Soft-delete. Returns False when nothing was deleted (already gone,
        or not visible to this user) so the route can answer 404 honestly."""

        async with self.repository.rls():
            result = await WebCrawlPreset.update_where(
                {"id": preset_id, "deleted_at__isnull": True},
                deleted_at=utcnow(),
            )
        return bool(result.rows_affected)

    async def default_preset_id(self, site_id: str) -> str | None:
        """The site's pinned default preset id, if it pinned one.

        Lives in the namespaced ``web.site.settings`` bag (``settings.crawl``)
        beside every other per-site setting — not a dedicated column, and not a
        second copy of the config.
        """

        async with self.repository.rls():
            site = await WebSite.get_or_none(use_cache=False, id=site_id, deleted_at__isnull=True)
        if site is None:
            raise LookupError(f"site {site_id} does not exist or is not accessible")
        settings = site.settings if isinstance(site.settings, dict) else {}
        crawl = settings.get(SITE_SETTINGS_CRAWL_KEY)
        if not isinstance(crawl, dict):
            return None
        value = crawl.get(SITE_SETTINGS_DEFAULT_PRESET_KEY)
        return str(value) if value else None

    async def last_session_request(self, site_id: str) -> tuple[str, CrawlStartRequest] | None:
        """The most recent site-wide crawl's persisted request, if any.

        Reads the same ``scope["request"]`` blob resume rebuilds from, so a
        rescrape reruns exactly what the last crawl ran.
        """

        async with self.repository.rls():
            sessions = await (
                WebCrawlSession.filter(site_id=site_id, deleted_at__isnull=True)
                .order_by("-created_at")
                .limit(SESSION_SCAN_LIMIT)
                .all(use_cache=False)
            )
        for session in sessions:
            scope = session.scope if isinstance(session.scope, dict) else {}
            if scope.get("mode") not in RECRAWL_SOURCE_MODES:
                continue
            payload = scope.get("request")
            if not isinstance(payload, dict):
                continue
            try:
                return str(session.id), CrawlStartRequest.model_validate(payload)
            except ValidationError as exc:
                # A request shape that has since changed must not poison the
                # button — fall through to the next session, then to defaults.
                logger.warning(
                    "crawl session %s has an unusable persisted request: %s", session.id, exc
                )
        return None


async def derive_recrawl_config(
    presets: CrawlPresetRepository,
    site_id: str,
    *,
    preset_id: str | None = None,
) -> RecrawlConfigResponse:
    """Resolve the config a one-click rescrape of ``site_id`` would run.

    Never returns ``None``: the last step is the request model's own defaults,
    so the button always has something to run. An explicitly named preset that
    does not resolve is an ERROR, not a silent downgrade to defaults — the user
    asked for that preset.
    """

    if preset_id:
        row = await presets.load(preset_id)
        if str(row.site_id) != str(site_id):
            raise PermissionError(f"crawl preset {preset_id} belongs to another site")
        record = _record(row)
        if record.config is None:
            raise ValueError(record.config_error or "stored crawl config is not valid")
        return RecrawlConfigResponse(
            site_id=site_id,
            source="preset",
            preset_id=record.id,
            preset_name=record.name,
            config=record.config,
        )

    pinned = await presets.default_preset_id(site_id)
    if pinned:
        try:
            row = await presets.load(pinned)
        except LookupError:
            # A pinned preset that was deleted must not brick the button; it
            # degrades to the next source, loudly.
            logger.warning("site %s pins crawl preset %s, which no longer exists", site_id, pinned)
        else:
            record = _record(row)
            if str(row.site_id) == str(site_id) and record.config is not None:
                return RecrawlConfigResponse(
                    site_id=site_id,
                    source="site_default_preset",
                    preset_id=record.id,
                    preset_name=record.name,
                    config=record.config,
                )
            logger.warning(
                "site %s pins crawl preset %s, which is unusable: %s",
                site_id,
                pinned,
                record.config_error or "belongs to another site",
            )

    previous = await presets.last_session_request(site_id)
    if previous is not None:
        session_id, config = previous
        return RecrawlConfigResponse(
            site_id=site_id,
            source="last_session",
            session_id=session_id,
            config=config,
        )

    return RecrawlConfigResponse(
        site_id=site_id,
        source="defaults",
        config=CrawlStartRequest(),
    )


__all__: list[str] = [
    "CrawlPresetRepository",
    "PRESET_LIST_LIMIT",
    "RECRAWL_SOURCE_MODES",
    "SESSION_SCAN_LIMIT",
    "SITE_SETTINGS_CRAWL_KEY",
    "SITE_SETTINGS_DEFAULT_PRESET_KEY",
    "derive_recrawl_config",
]
