"""Sitemap sync — sitemaps become first-class ``web.sitemap`` rows and feed
the canonical ``web.page`` registry through ``web.page_sitemap`` memberships.

Importable service functions only (no HTTP concerns) so the same operation
runs as the standalone streaming command, as the initialize-site step, and —
later — as a workflow node. All DB access is matrx-orm; writes are batched
and idempotent (every statement is an upsert on the table's arbiter).
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any
from urllib.parse import urlparse

from matrx_orm import transaction
from matrx_utils import utcnow

from matrx_scraper.db.models_web import (
    PageSitemap as WebPageSitemap,
    Sitemap as WebSitemap,
)
from matrx_scraper.db.web import WEB_DB_NAME
from matrx_scraper.sitemaps import (
    DEFAULT_MAX_SITEMAP_DEPTH,
    DEFAULT_MAX_SITEMAP_DOCS,
    DEFAULT_MAX_SITEMAP_URLS,
    SitemapCrawl,
    SitemapUrlEntry,
    crawl_sitemap_documents,
)
from matrx_scraper.web_crawl.contracts import SitemapSyncSummary
from matrx_scraper.web_crawl.persistence import url_hash
from matrx_scraper.web_crawl.upsert_rows import dedupe_upsert_rows
from matrx_scraper.web_crawl.url_identity import (
    RevivedDismissal,
    append_dismissal_marker,
    upsert_observed_page_urls,
)
from matrx_scraper.utils.url import normalize_url, validate_and_correct_url

logger = logging.getLogger(__name__)


def normalize_sitemap_loc(loc: str) -> str | None:
    """ONE gate for a sitemap `<loc>` value: validate/correct, then normalize.

    `normalize_url` assumes a schemed URL — feeding it a scheme-less loc
    (`www.example.com/page`, a routinely-seen sitemap malformation) mangles the
    identity instead of recovering it. `validate_and_correct_url` is the same
    correction the crawl seed path runs: it prefixes a recoverable scheme-less
    host with https://, and rejects (ValueError) anything that is not a public
    http(s) URL — non-http schemes, missing hosts, localhost/internal targets.
    Returns None for a loc that cannot become a valid public page URL; the
    caller counts those loudly, never silently drops them.
    """
    try:
        corrected = validate_and_correct_url(loc)
    except ValueError:
        return None
    return normalize_url(corrected)


_PAGE_BATCH_SIZE = 500

ProgressCallback = Callable[[str, SitemapSyncSummary], Awaitable[None]]


class SitemapSyncResult:
    """Outcome of one sitemap sync run."""

    def __init__(
        self,
        summary: SitemapSyncSummary,
        errors: list[str],
        revived_after_dismissal: list[RevivedDismissal] | None = None,
    ) -> None:
        self.summary = summary
        self.errors = errors
        # Rows the user had dismissed that this sync re-observed and revived
        # (dismissal memory) — surfaced loudly by every runner, never silent.
        self.revived_after_dismissal = list(revived_after_dismissal or [])


async def _report(
    on_progress: ProgressCallback | None,
    message: str,
    summary: SitemapSyncSummary,
) -> None:
    if on_progress is not None:
        await on_progress(message, summary)


async def _upsert_sitemap_documents(
    *,
    site_id: str,
    organization_id: str,
    user_id: str,
    crawl: SitemapCrawl,
    session_id: str | None = None,
    revived: list[RevivedDismissal] | None = None,
) -> dict[str, str]:
    """Upsert one ``web.sitemap`` row per fetched document.

    Documents arrive parents-before-children, so ``parent_sitemap_id`` always
    resolves against a row written earlier in the same pass. A sitemap that
    disappeared is simply absent from ``crawl`` — its row is untouched and its
    ``last_seen`` stops advancing.
    """

    now = utcnow()
    sitemap_ids: dict[str, str] = {}
    async with transaction(WEB_DB_NAME):
        for doc in crawl.documents:
            parent_id = sitemap_ids.get(doc.parent_url) if doc.parent_url else None
            succeeded = doc.fetch_error is None
            # A fetch failure records the failure without clobbering what a
            # prior successful fetch learned: kind/counts/last_seen only
            # advance when the document was actually parsed this run.
            update_fields = (
                [
                    "kind",
                    "parent_sitemap_id",
                    "status_code",
                    "url_count",
                    "child_count",
                    "is_active",
                    "last_seen",
                    "last_fetched_at",
                ]
                if succeeded
                else ["status_code", "last_fetched_at"]
            )
            row = await WebSitemap.upsert(
                {
                    "organization_id": organization_id,
                    "created_by": user_id,
                    "site_id": site_id,
                    "url": doc.url,
                    "kind": doc.kind,
                    "parent_sitemap_id": parent_id,
                    "status_code": doc.status_code,
                    "url_count": doc.url_count,
                    "child_count": doc.child_count,
                    "is_active": True,
                    "first_seen": now,
                    "last_seen": now if succeeded else None,
                    "last_fetched_at": now,
                    "fetch_error": doc.fetch_error,
                },
                on_conflict=["site_id", "url"],
                update_fields=update_fields,
            )
            sitemap_id = str(row.id)
            sitemap_ids[doc.url] = sitemap_id
            # ``fetch_error`` must be able to CLEAR on a successful re-fetch;
            # upsert omits None values, so write it explicitly when it differs.
            if row.fetch_error != doc.fetch_error:
                await WebSitemap.update_where({"id": sitemap_id}, fetch_error=doc.fetch_error)
            # A successfully re-fetched sitemap EXISTS again — a soft-deleted
            # row must become visible, not stay invisibly refreshed forever
            # (same None-omission reason as fetch_error above) — and it
            # permanently remembers that the user dismissed it (dismissal
            # memory: crawler = reality; a dismissal is never silently
            # ignored, never forgotten).
            if succeeded and row.deleted_at is not None:
                revived_metadata = append_dismissal_marker(
                    getattr(row, "metadata", None),
                    dismissed_at=row.deleted_at,
                    session_id=session_id,
                )
                await WebSitemap.update_where(
                    {"id": sitemap_id},
                    deleted_at=None,
                    metadata=revived_metadata,
                )
                logger.warning(
                    "re-observed a sitemap the user previously dismissed — "
                    "reviving with dismissal memory: %s (dismissed_at=%s, "
                    "cycles=%d, session=%s)",
                    doc.url,
                    row.deleted_at,
                    len(revived_metadata["dismissals"]),
                    session_id,
                )
                if revived is not None:
                    revived.append(
                        RevivedDismissal(
                            row_id=sitemap_id,
                            url=doc.url,
                            dismissed_at=str(row.deleted_at),
                            dismissal_count=len(revived_metadata["dismissals"]),
                        )
                    )
    return sitemap_ids


async def _upsert_pages_and_memberships(
    *,
    site_id: str,
    organization_id: str,
    user_id: str,
    crawl: SitemapCrawl,
    sitemap_ids: dict[str, str],
    summary: SitemapSyncSummary,
    on_progress: ProgressCallback | None,
    errors: list[str],
    session_id: str | None = None,
    revived: list[RevivedDismissal] | None = None,
) -> None:
    now = utcnow()
    page_rows: dict[str, dict[str, Any]] = {}
    memberships: dict[tuple[str, str], SitemapUrlEntry] = {}
    skipped_invalid = 0

    for doc in crawl.documents:
        if doc.kind != "urlset":
            continue
        sitemap_id = sitemap_ids.get(doc.url)
        if sitemap_id is None:
            raise RuntimeError(f"sitemap row missing for fetched document {doc.url}")
        for entry in doc.entries:
            normalized = normalize_sitemap_loc(entry.loc)
            if normalized is None:
                skipped_invalid += 1
                continue
            digest = url_hash(normalized)
            page_rows.setdefault(
                digest,
                {
                    "organization_id": organization_id,
                    "created_by": user_id,
                    "site_id": site_id,
                    "url": normalized,
                    "url_hash": digest,
                    "path": urlparse(normalized).path or "/",
                    "provenance": "sitemap",
                    "status": "active",
                    "first_seen": now,
                    "last_seen": now,
                },
            )
            # First occurrence wins so a duplicate <url> with no metadata
            # cannot blank out an earlier entry's lastmod/changefreq/priority.
            memberships.setdefault((digest, sitemap_id), entry)

    if skipped_invalid:
        errors.append(
            f"skipped {skipped_invalid} sitemap URL entries that could not be "
            "corrected into valid public http(s) URLs"
        )

    ordered_digests = list(page_rows)
    resolutions = await upsert_observed_page_urls(
        site_id=site_id,
        organization_id=organization_id,
        user_id=user_id,
        urls=[str(page_rows[digest]["url"]) for digest in ordered_digests],
        provenance="sitemap",
        session_id=session_id,
        revived=revived,
    )
    page_ids = {
        digest: resolutions[str(page_rows[digest]["url"])].canonical_page_id
        for digest in ordered_digests
    }
    summary.pages_upserted = len(page_ids)
    await _report(
        on_progress,
        f"Matched {len(page_ids)} sitemap URLs to canonical pages…",
        summary,
    )

    # Two DISTINCT sitemap URLs in one document can resolve to ONE canonical
    # page (an alias, or two raw URLs that normalize together), so the
    # (page_id, sitemap_id) arbiter can repeat even though (digest, sitemap_id)
    # was unique. Sending both in one statement is a hard
    # CardinalityViolationError that killed the whole sync.
    membership_rows = dedupe_upsert_rows(
        [
            {
                "organization_id": organization_id,
                "created_by": user_id,
                "site_id": site_id,
                "page_id": page_ids[digest],
                "sitemap_id": sitemap_id,
                "lastmod": entry.lastmod,
                "changefreq": entry.changefreq,
                "priority": entry.priority,
                "first_seen": now,
                "last_seen": now,
            }
            for (digest, sitemap_id), entry in memberships.items()
            if digest in page_ids
        ],
        on_conflict=["page_id", "sitemap_id"],
        context=f"sitemap sync memberships (site {site_id})",
    )
    for start in range(0, len(membership_rows), _PAGE_BATCH_SIZE):
        batch = membership_rows[start : start + _PAGE_BATCH_SIZE]
        async with transaction(WEB_DB_NAME):
            upserted = await WebPageSitemap.bulk_upsert(
                batch,
                on_conflict=["page_id", "sitemap_id"],
                update_fields=["lastmod", "changefreq", "priority", "last_seen"],
            )
            # A membership observed in this sync EXISTS again — revive any
            # soft-deleted row the upsert refreshed (upsert cannot SET a
            # column to NULL, so the revive is an explicit follow-up write).
            revive_ids = [str(row.id) for row in upserted if row.deleted_at is not None]
            if revive_ids:
                await WebPageSitemap.update_where({"id__in": revive_ids}, deleted_at=None)


async def sync_site_sitemaps(
    *,
    site_id: str,
    organization_id: str,
    user_id: str,
    root_url: str,
    max_docs: int = DEFAULT_MAX_SITEMAP_DOCS,
    max_depth: int = DEFAULT_MAX_SITEMAP_DEPTH,
    max_urls: int = DEFAULT_MAX_SITEMAP_URLS,
    on_progress: ProgressCallback | None = None,
    session_id: str | None = None,
) -> SitemapSyncResult:
    """Discover, fetch, and persist a site's sitemap graph.

    Idempotent and re-runnable: sitemap rows upsert on ``(site_id, url)``,
    pages on ``(site_id, url_hash)`` (new rows born with
    ``provenance='sitemap'``; existing rows only advance ``last_seen``), and
    memberships on ``(page_id, sitemap_id)``. Bounds are recorded loudly in
    the summary (``truncated``) and the returned errors — never silently.
    """

    summary = SitemapSyncSummary()
    errors: list[str] = []

    await _report(on_progress, "Discovering sitemap documents…", summary)
    crawl = await crawl_sitemap_documents(
        root_url,
        max_docs=max_docs,
        max_depth=max_depth,
        max_urls=max_urls,
    )
    errors.extend(crawl.errors)
    errors.extend(crawl.truncation_reasons)
    summary.found = len(crawl.documents)
    summary.urls = crawl.url_total
    summary.truncated = crawl.truncated
    await _report(
        on_progress,
        f"Found {summary.found} sitemap documents containing {summary.urls} URLs…",
        summary,
    )

    revived: list[RevivedDismissal] = []
    sitemap_ids = await _upsert_sitemap_documents(
        site_id=site_id,
        organization_id=organization_id,
        user_id=user_id,
        crawl=crawl,
        session_id=session_id,
        revived=revived,
    )
    await _upsert_pages_and_memberships(
        site_id=site_id,
        organization_id=organization_id,
        user_id=user_id,
        crawl=crawl,
        sitemap_ids=sitemap_ids,
        summary=summary,
        on_progress=on_progress,
        errors=errors,
        session_id=session_id,
        revived=revived,
    )
    # Dismissal memory is NEVER silent: each revive rides the durable errors
    # list (summary lines shown in the live feed and persisted with the run).
    for entry in revived:
        errors.append(
            "Re-observed a page/sitemap you previously dismissed — it is "
            f"visible again and remembers the dismissal: {entry.url}"
        )
    if crawl.truncated:
        logger.warning(
            "sitemap sync for site %s truncated: %s",
            site_id,
            "; ".join(crawl.truncation_reasons),
        )
    return SitemapSyncResult(summary, errors, revived_after_dismissal=revived)


__all__ = [
    "ProgressCallback",
    "SitemapSyncResult",
    "sync_site_sitemaps",
]
