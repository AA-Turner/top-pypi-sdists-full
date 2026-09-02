"""Link-status verification — populates ``web.link_edge.http_status``.

The crawl write path records link edges but never checks their targets, so
every edge is born with ``http_status IS NULL`` and broken-link detection is
impossible downstream (frontend defect ledger D74). This importable service
fills the column, loudly, in two passes:

- **Internal edges** need no network: an accepted target snapshot in the SAME
  session wins, then the target URL's ``web.crawl_url`` outcome supplies
  4xx/5xx evidence for targets which correctly earned no snapshot. Historical
  edges fall back to the target page's latest accepted snapshot.
- **External edges** reuse a recent status for the same site + URL, then get a
  bounded live check per DISTINCT uncached target URL: HEAD
  first, GET fallback (some hosts reject HEAD), redirects followed, final
  status recorded. Global + per-host concurrency caps and per-host spacing
  keep this polite. A network-level failure (DNS, TLS, timeout) records
  status ``0`` — "no response", distinct from unchecked NULL — so a dead
  domain reads as broken, not as never-checked.

Idempotent and re-runnable: each run only touches edges whose ``http_status``
is still NULL (pass ``recheck=True`` to re-verify previously checked edges).

**There is ONE link checker in this platform and it is here.** The polite
HTTP prober (:class:`_PoliteChecker`) is exposed as :func:`check_urls` for
callers that hold a list of URLs rather than a site's ``link_edge`` rows — the
outreach broken-link prospecting pass checks the outbound links of pages we do
not own and therefore has no edge rows at all. It consumes the SAME prober, the
same HEAD→GET fallback, the same per-host spacing, and the same "status ``0``
means no response, which is not the same as unchecked" rule. A second checker
would drift on exactly those three, so do not write one.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Awaitable, Callable, Iterable
from datetime import timedelta
from urllib.parse import urlsplit

import httpx

from matrx_orm import Now, transaction
from matrx_orm.operations.bulk_update_values import bulk_update_by_pk
from matrx_utils import utcnow

from matrx_scraper.db.models_web import (
    CrawlUrl as WebCrawlUrl,
    LinkEdge as WebLinkEdge,
    Page as WebPage,
    Snapshot as WebSnapshot,
)
from matrx_scraper.db.web import WEB_DB_NAME
from matrx_scraper.web_crawl.contracts import LinkCheckSummary
from matrx_scraper.web_crawl.persistence import url_hash
from matrx_scraper.crawler import _normalise_url

logger = logging.getLogger(__name__)

_EDGE_BATCH_SIZE = 1_000
_CACHE_TARGET_BATCH_SIZE = 500
_DEFAULT_MAX_EXTERNAL_TARGETS = 500
_DEFAULT_GLOBAL_CONCURRENCY = 10
_DEFAULT_PER_HOST_SPACING_S = 0.5
_REQUEST_TIMEOUT_S = 10.0
_EXTERNAL_STATUS_TTL = timedelta(hours=24)
_USER_AGENT = "MatrxScraperBot/0.1 (+https://aimatrx.com)"
# Statuses that mean "this host dislikes HEAD", not "this target is broken".
_HEAD_FALLBACK_STATUSES = frozenset({400, 403, 405, 500, 501})

ProgressCallback = Callable[[str, LinkCheckSummary], Awaitable[None]]


class LinkCheckResult:
    """Outcome of one link-status verification run."""

    def __init__(self, summary: LinkCheckSummary) -> None:
        self.summary = summary


async def _report(
    on_progress: ProgressCallback | None,
    message: str,
    summary: LinkCheckSummary,
) -> None:
    if on_progress is not None:
        await on_progress(message, summary)


def _status_filters(
    site_id: str,
    *,
    internal: bool,
    recheck: bool,
    snapshot_ids: list[str] | None,
) -> dict[str, object]:
    filters: dict[str, object] = {
        "site_id": site_id,
        "is_internal": internal,
        "deleted_at__isnull": True,
    }
    if not recheck:
        filters["http_status__isnull"] = True
    if snapshot_ids is not None:
        filters["snapshot_id__in"] = snapshot_ids
    return filters


def _select_internal_status(
    *,
    source_snapshot_id: str,
    target_url: str,
    target_page_id: str | None,
    session_by_snapshot: dict[str, str],
    same_session_status_by_page: dict[tuple[str, str], int],
    crawl_status_by_session_hash: dict[tuple[str, str], int],
    snapshot_by_page: dict[str, str],
    statuses_by_snapshot: dict[str, int],
) -> int | None:
    """Choose same-session transport truth before historical snapshot truth."""

    session_id = session_by_snapshot.get(source_snapshot_id)
    if session_id is not None:
        if target_page_id is not None:
            accepted_status = same_session_status_by_page.get((session_id, target_page_id))
            if accepted_status is not None:
                return accepted_status
        status = crawl_status_by_session_hash.get(
            (session_id, url_hash(_normalise_url(target_url)))
        )
        if status is not None:
            return status
    fallback_snapshot_id = (
        snapshot_by_page.get(target_page_id) if target_page_id is not None else None
    )
    return (
        statuses_by_snapshot.get(fallback_snapshot_id) if fallback_snapshot_id is not None else None
    )


async def _apply_status_updates(updates: list[dict[str, object]]) -> int:
    """Set ``http_status`` on edges by pk; screams on partial application."""

    if not updates:
        return 0
    async with transaction(WEB_DB_NAME):
        updated = await bulk_update_by_pk(
            WebLinkEdge,
            updates,
            casts={"id": "uuid", "http_status": "integer"},
            set_expressions={"updated_at": Now()},
        )
    if updated != len(updates):
        raise RuntimeError(
            f"link check updated {updated} of {len(updates)} edges — "
            "refusing to under-report silently"
        )
    return updated


async def _check_internal_edges(
    site_id: str,
    *,
    recheck: bool,
    snapshot_ids: list[str] | None,
    summary: LinkCheckSummary,
    on_progress: ProgressCallback | None,
) -> None:
    """Resolve internal status from this crawl's own URL ledger.

    The canonical page pointer intentionally names only accepted captures, so
    it cannot answer for a target that returned 404/500 and earned no snapshot.
    ``crawl_url`` is the complete per-session transport ledger and is therefore
    the primary source; latest snapshot is only a legacy-edge fallback.
    """

    last_id: str | None = None
    while True:
        filters = _status_filters(
            site_id,
            internal=True,
            recheck=recheck,
            snapshot_ids=snapshot_ids,
        )
        if last_id is not None:
            filters["id__gt"] = last_id
        edges = await WebLinkEdge.filter(**filters).order_by("id").limit(_EDGE_BATCH_SIZE).all()
        if not edges:
            break
        last_id = str(edges[-1].id)
        summary.internal_scanned += len(edges)

        source_snapshot_ids = list({str(edge.snapshot_id) for edge in edges})
        source_snapshots = await WebSnapshot.filter(id__in=source_snapshot_ids).values(
            "id", "session_id"
        )
        session_by_snapshot = {str(row["id"]): str(row["session_id"]) for row in source_snapshots}
        session_ids = list(set(session_by_snapshot.values()))
        target_page_ids = list(
            {str(edge.target_page_id) for edge in edges if edge.target_page_id is not None}
        )
        same_session_status_by_page: dict[tuple[str, str], int] = {}
        if session_ids and target_page_ids:
            accepted_rows = await (
                WebSnapshot.filter(
                    site_id=site_id,
                    session_id__in=session_ids,
                    page_id__in=target_page_ids,
                    http_status__isnull=False,
                    deleted_at__isnull=True,
                )
                .order_by("-captured_at", "-id")
                .values("session_id", "page_id", "http_status")
            )
            for row in accepted_rows:
                key = (str(row["session_id"]), str(row["page_id"]))
                same_session_status_by_page.setdefault(key, int(row["http_status"]))
        target_hashes = list({url_hash(_normalise_url(str(edge.target_url))) for edge in edges})
        crawl_status_by_session_hash: dict[tuple[str, str], int] = {}
        if session_ids and target_hashes:
            crawl_rows = await (
                WebCrawlUrl.filter(
                    site_id=site_id,
                    session_id__in=session_ids,
                    url_hash__in=target_hashes,
                    http_status__isnull=False,
                    deleted_at__isnull=True,
                )
                .order_by("-completed_at", "-id")
                .values("session_id", "url_hash", "http_status")
            )
            for row in crawl_rows:
                key = (str(row["session_id"]), str(row["url_hash"]))
                crawl_status_by_session_hash.setdefault(key, int(row["http_status"]))

        pages = await WebPage.filter(id__in=target_page_ids, deleted_at__isnull=True).all()
        snapshot_by_page: dict[str, str] = {
            str(page.id): str(page.latest_snapshot_id)
            for page in pages
            if page.latest_snapshot_id is not None
        }
        statuses_by_snapshot: dict[str, int] = {}
        fallback_snapshot_ids = list(set(snapshot_by_page.values()))
        if fallback_snapshot_ids:
            snapshots = await WebSnapshot.filter(id__in=fallback_snapshot_ids).all()
            statuses_by_snapshot = {
                str(snap.id): int(snap.http_status)
                for snap in snapshots
                if snap.http_status is not None
            }

        updates: list[dict[str, object]] = []
        for edge in edges:
            status = _select_internal_status(
                source_snapshot_id=str(edge.snapshot_id),
                target_url=str(edge.target_url),
                target_page_id=(
                    str(edge.target_page_id) if edge.target_page_id is not None else None
                ),
                session_by_snapshot=session_by_snapshot,
                same_session_status_by_page=same_session_status_by_page,
                crawl_status_by_session_hash=crawl_status_by_session_hash,
                snapshot_by_page=snapshot_by_page,
                statuses_by_snapshot=statuses_by_snapshot,
            )
            if status is None:
                if edge.target_page_id is None:
                    summary.internal_unresolved += 1
                else:
                    summary.internal_uncrawled += 1
            elif edge.http_status != status:
                updates.append({"id": str(edge.id), "http_status": status})
        summary.internal_updated += await _apply_status_updates(updates)
        await _report(
            on_progress,
            (
                f"Internal: scanned {summary.internal_scanned}, updated "
                f"{summary.internal_updated}, {summary.internal_uncrawled} "
                "target(s) never crawled…"
            ),
            summary,
        )
        if len(edges) < _EDGE_BATCH_SIZE:
            break


class _PoliteChecker:
    """Bounded external URL checker: global semaphore + per-host spacing."""

    def __init__(self, http: httpx.AsyncClient, concurrency: int, spacing_s: float) -> None:
        self._http = http
        self._global = asyncio.Semaphore(concurrency)
        self._spacing_s = spacing_s
        self._host_locks: dict[str, asyncio.Lock] = {}
        self._host_last: dict[str, float] = {}

    async def check(self, url: str) -> int:
        host = urlsplit(url).netloc.lower()
        lock = self._host_locks.setdefault(host, asyncio.Lock())
        async with self._global:
            async with lock:
                elapsed = time.monotonic() - self._host_last.get(host, 0.0)
                if elapsed < self._spacing_s:
                    await asyncio.sleep(self._spacing_s - elapsed)
                try:
                    return await self._request(url)
                finally:
                    self._host_last[host] = time.monotonic()

    async def _request(self, url: str) -> int:
        try:
            response = await self._http.head(url)
            if response.status_code not in _HEAD_FALLBACK_STATUSES:
                return response.status_code
        except httpx.HTTPError:
            pass  # fall through to GET — HEAD handling is wildly inconsistent
        try:
            async with self._http.stream("GET", url) as response:
                return response.status_code
        except httpx.HTTPError as exc:
            logger.info("link check: no response from %s (%s)", url, type(exc).__name__)
            return 0


async def check_urls(
    urls: Iterable[str],
    *,
    concurrency: int = _DEFAULT_GLOBAL_CONCURRENCY,
    per_host_spacing_s: float = _DEFAULT_PER_HOST_SPACING_S,
    on_result: Callable[[str, int], Awaitable[None]] | None = None,
) -> dict[str, int]:
    """Live-check a list of URLs politely — ``{url: final HTTP status}``.

    **THE ONE CHECKER, for callers that hold URLs instead of link edges.** The
    site crawler owns ``web.link_edge`` rows and calls this through
    :func:`_check_external_edges`; outreach broken-link prospecting checks the
    outbound links of pages we do not own and has no edge rows at all. Both get
    the same prober, so the three things that actually matter can never drift:
    HEAD first with a GET fallback (host HEAD handling is wildly inconsistent),
    redirects followed to a final status, and a global semaphore plus per-host
    spacing so a page with forty links to one host is not a small flood.

    Status ``0`` means **no response** — DNS failure, TLS failure, timeout. It is
    deliberately not ``None``: a dead domain is broken evidence, and it must
    never read as "we never looked".

    Non-http(s) targets and duplicates are dropped before any request, so the
    returned map is keyed by the distinct URLs actually checked. ``on_result``
    is awaited once per completed URL, in completion order, for callers that
    stream progress or persist as they go.
    """
    targets = list(dict.fromkeys(url for url in urls if url.startswith(("http://", "https://"))))
    if not targets:
        return {}
    statuses: dict[str, int] = {}
    async with httpx.AsyncClient(
        timeout=_REQUEST_TIMEOUT_S,
        follow_redirects=True,
        headers={"User-Agent": _USER_AGENT},
    ) as http:
        checker = _PoliteChecker(http, concurrency, per_host_spacing_s)

        async def check_one(target: str) -> tuple[str, int]:
            return target, await checker.check(target)

        pending = [asyncio.create_task(check_one(target)) for target in targets]
        for future in asyncio.as_completed(pending):
            target, status = await future
            statuses[target] = status
            if on_result is not None:
                await on_result(target, status)
    return statuses


async def _load_cached_external_statuses(
    site_id: str,
    targets: list[str],
) -> dict[str, int]:
    """Newest still-fresh status per target, from existing link evidence.

    This deliberately adds no cache table: a prior ``link_edge`` observation is
    the evidence and ``updated_at`` is when its derived status was verified.
    """

    if not targets:
        return {}
    cached: dict[str, int] = {}
    cutoff = utcnow() - _EXTERNAL_STATUS_TTL
    for start in range(0, len(targets), _CACHE_TARGET_BATCH_SIZE):
        batch = targets[start : start + _CACHE_TARGET_BATCH_SIZE]
        rows = await (
            WebLinkEdge.filter(
                site_id=site_id,
                target_url__in=batch,
                http_status__isnull=False,
                updated_at__gte=cutoff,
                deleted_at__isnull=True,
            )
            .order_by("-updated_at", "-id")
            .values("target_url", "http_status")
        )
        for row in rows:
            cached.setdefault(str(row["target_url"]), int(row["http_status"]))
    return cached


async def _check_external_edges(
    site_id: str,
    *,
    recheck: bool,
    snapshot_ids: list[str] | None,
    max_targets: int,
    concurrency: int,
    per_host_spacing_s: float,
    summary: LinkCheckSummary,
    on_progress: ProgressCallback | None,
) -> None:
    """Live-check each distinct external target and stamp all of its edges."""

    filters = _status_filters(
        site_id,
        internal=False,
        recheck=recheck,
        snapshot_ids=snapshot_ids,
    )
    edges = await WebLinkEdge.filter(**filters).order_by("id").all()
    if not edges:
        return
    edge_ids_by_target: dict[str, list[str]] = {}
    for edge in edges:
        target = str(edge.target_url)
        if target.startswith(("http://", "https://")):
            edge_ids_by_target.setdefault(target, []).append(str(edge.id))
        else:
            summary.external_skipped_non_http += 1

    targets = list(edge_ids_by_target)
    cached = {} if recheck else await _load_cached_external_statuses(site_id, targets)
    if cached:
        cache_updates = [
            {"id": edge_id, "http_status": cached[target]}
            for target, edge_ids in edge_ids_by_target.items()
            if target in cached
            for edge_id in edge_ids
        ]
        summary.external_cached = len(cached)
        summary.external_edges_updated += await _apply_status_updates(cache_updates)
        targets = [target for target in targets if target not in cached]
    if len(targets) > max_targets:
        summary.external_truncated = True
        targets = targets[:max_targets]
    summary.external_targets = len(targets)

    updates: list[dict[str, object]] = []

    async def record(target: str, status: int) -> None:
        nonlocal updates
        summary.external_checked += 1
        if status == 0:
            summary.external_unreachable += 1
        elif status >= 400:
            summary.external_broken += 1
        else:
            summary.external_ok += 1
        updates.extend(
            {"id": edge_id, "http_status": status} for edge_id in edge_ids_by_target[target]
        )
        if summary.external_checked % 25 == 0:
            summary.external_edges_updated += await _apply_status_updates(updates)
            updates = []
            await _report(
                on_progress,
                (
                    f"External: checked {summary.external_checked}/"
                    f"{summary.external_targets} targets — "
                    f"{summary.external_broken} broken, "
                    f"{summary.external_unreachable} unreachable…"
                ),
                summary,
            )

    await check_urls(
        targets,
        concurrency=concurrency,
        per_host_spacing_s=per_host_spacing_s,
        on_result=record,
    )
    summary.external_edges_updated += await _apply_status_updates(updates)


async def check_site_links(
    *,
    site_id: str,
    session_id: str | None = None,
    recheck: bool = False,
    max_external_targets: int = _DEFAULT_MAX_EXTERNAL_TARGETS,
    concurrency: int = _DEFAULT_GLOBAL_CONCURRENCY,
    per_host_spacing_s: float = _DEFAULT_PER_HOST_SPACING_S,
    on_progress: ProgressCallback | None = None,
) -> LinkCheckResult:
    """Populate ``web.link_edge.http_status`` for one site (both passes).

    ``session_id`` scopes automatic post-crawl work to that crawl's immutable
    snapshots. The standalone command intentionally omits it and can backfill
    historical unchecked edges. This preserves an honest pre-evidence state
    for old crawl reports until the user re-crawls.
    """

    summary = LinkCheckSummary()
    snapshot_ids: list[str] | None = None
    if session_id is not None:
        rows = await WebSnapshot.filter(
            site_id=site_id,
            session_id=session_id,
            deleted_at__isnull=True,
        ).values("id")
        snapshot_ids = [str(row["id"]) for row in rows]
    await _check_internal_edges(
        site_id,
        recheck=recheck,
        snapshot_ids=snapshot_ids,
        summary=summary,
        on_progress=on_progress,
    )
    await _check_external_edges(
        site_id,
        recheck=recheck,
        snapshot_ids=snapshot_ids,
        max_targets=max_external_targets,
        concurrency=concurrency,
        per_host_spacing_s=per_host_spacing_s,
        summary=summary,
        on_progress=on_progress,
    )
    return LinkCheckResult(summary)


__all__ = [
    "LinkCheckResult",
    "ProgressCallback",
    "check_site_links",
    "check_urls",
]
