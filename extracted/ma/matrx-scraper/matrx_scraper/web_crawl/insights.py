"""Derived read shapes over canonical crawl evidence — clusters, graph, series.

These are the three aggregations a browser CANNOT assemble by reading rows
directly from Supabase (the rule the rest of the canonical crawler follows):
each one is a group-by / rank / downsample over evidence that is already
persisted, and each one must be capped before it reaches a renderer.

Ported from the legacy `aidream/services/scraper/crawl_service.py` reads
(`duplicate_clusters`, `link_graph`, `run_timeseries`) as part of the
one-crawler consolidation. **No new table was added and none is needed** —
every fact these shapes need is already canonical:

- duplicate clusters ← ``web.snapshot.extracted.fingerprint`` (the SAME key
  ``analysis._check_duplicate_content_exact`` groups on, so a page flagged as
  a duplicate always appears in exactly one cluster here; pinned by
  ``tests/test_crawl_insights.py::test_cluster_membership_matches_analysis_check``)
- link graph ← ``web.link_edge`` (populated by ``link_resolution`` /
  ``link_check``) + ``web.page`` (ranked and sized by ``page.link_score``, the
  internal PageRank ``web_crawl/link_score.py`` writes; in-degree ranks the
  pages a completed full crawl has not scored yet). Both edge endpoints are
  canonical by construction — ``link_resolution`` writes
  ``target_page_id = page.canonical_page_id`` and snapshots hang off canonical
  pages — so the node set needs no alias collapse.
- progress series ← ``web.crawl_event`` rows of type ``crawl_progress``, whose
  payload is the full ``CrawlProgressEvent`` (``persistence.persist_event``).
  The legacy ``scraper.crawl_progress_snapshots`` table has no canonical twin
  and must never grow one — it was a second copy of the event ledger.

🚨 **Every cap is surfaced, never silent.** ``web.link_edge`` alone holds
~610k rows; an uncapped graph melts the browser, and a capped one that reports
only what it kept lies about the site. Each response carries
``*_total`` / ``*_returned`` / ``*_omitted`` so a UI can say "showing 1,000 of
18,432" instead of implying completeness.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from datetime import datetime
from math import ceil
from typing import Any

from matrx_orm import Count, Subquery

from matrx_scraper.db.models_web import (
    CrawlEvent as WebCrawlEvent,
    GscPageStat as WebGscPageStat,
    LinkEdge as WebLinkEdge,
    Page as WebPage,
    PageSitemap as WebPageSitemap,
    Snapshot as WebSnapshot,
)
from matrx_scraper.web_crawl.contracts import (
    DuplicateCluster,
    DuplicateClusterReport,
    DuplicatePage,
    LinkGraph,
    LinkGraphEdge,
    LinkGraphNode,
    ProgressPoint,
    ProgressSeries,
    TrafficAtRiskPage,
    TrafficAtRiskReport,
)
from matrx_utils.web_page_class import is_machine_resource
from matrx_scraper.web_crawl.persistence import WebCrawlRepository
from matrx_scraper.web_crawl.url_verify import VERIFICATION_METADATA_KEY

logger = logging.getLogger(__name__)

# Page census batching mirrors `analysis._load_page_facts` — same tables, same
# ordering, same scan ceiling, so the two sweeps agree about what "the site's
# pages" means instead of drifting into two different populations.
_PAGE_BATCH_SIZE = 500
_SNAPSHOT_BATCH_SIZE = 200
_MAX_PAGES_SCANNED = 20_000
# A `crawl_progress` event lands roughly once per second of crawl, so a long
# run can carry tens of thousands. The scan ceiling bounds memory; hitting it
# sets `scan_truncated` rather than quietly charting a partial run.
_PROGRESS_BATCH_SIZE = 2_000
_MAX_PROGRESS_SCANNED = 50_000

DUPLICATE_MAX_CLUSTERS = 100
DUPLICATE_MAX_PAGES_PER_CLUSTER = 50
GRAPH_MAX_NODES = 1_000
GRAPH_MAX_EDGES = 5_000
PROGRESS_MAX_POINTS = 500

#: Default cap for the traffic-at-risk list. A user acts on the worst offenders;
#: the report always says how many it omitted (`pages_omitted`).
TRAFFIC_AT_RISK_MAX_PAGES = 200
_GSC_BATCH_SIZE = 2_000
#: Ceiling on DISTINCT pages scanned from `web.gsc_page_stat`. Hitting it sets
#: `scan_truncated`, never a silently short list.
_MAX_GSC_PAGES_SCANNED = 50_000

#: Statuses that describe OUR request rather than the resource. A 429 means we
#: asked too fast; it is not evidence the URL is broken for anyone else, and
#: presenting it as lost traffic is a false alarm of the worst kind — it points
#: the customer at pages that are fine. Reported as
#: `throttled_not_assessed` so the gap in coverage stays visible.
THROTTLED_STATUSES = frozenset({429})

PROGRESS_EVENT_TYPE = "crawl_progress"


# ---------------------------------------------------------------------------
# Pure shaping — no DB. The algorithms live here so they are testable without
# a database and reusable by any caller that already holds the rows.


def _fingerprint_key(extracted: dict[str, Any] | None) -> tuple[int, str] | None:
    """``(fingerprint_version, exact_sha256)`` for a snapshot, or None.

    ONE reader of this jsonb path on the cluster side. The version is part of
    the key on purpose: hashes from two extractor generations are not
    comparable, so they must never land in the same cluster.
    """

    fingerprint = (extracted or {}).get("fingerprint") or {}
    if not isinstance(fingerprint, dict):
        return None
    version = fingerprint.get("version")
    sha = fingerprint.get("exact_sha256")
    if not isinstance(version, int) or not isinstance(sha, str) or not sha:
        return None
    return (version, sha)


def build_duplicate_clusters(
    rows: Sequence[tuple[tuple[int, str] | None, DuplicatePage]],
    *,
    site_id: str,
    max_clusters: int = DUPLICATE_MAX_CLUSTERS,
    max_pages_per_cluster: int = DUPLICATE_MAX_PAGES_PER_CLUSTER,
    scan_truncated: bool = False,
) -> DuplicateClusterReport:
    """Group fingerprinted pages into duplicate-content clusters.

    A cluster is >= 2 pages sharing one ``(fingerprint_version, exact_sha256)``.
    Ordering is largest-first, then by hash so equal-size clusters are stable
    across calls (a jittering list looks like data churn to a user).
    """

    grouped: dict[tuple[int, str], list[DuplicatePage]] = {}
    without_fingerprint = 0
    for key, page in rows:
        if key is None:
            without_fingerprint += 1
            continue
        grouped.setdefault(key, []).append(page)

    duplicates = [(key, pages) for key, pages in grouped.items() if len(pages) >= 2]
    duplicates.sort(key=lambda item: (-len(item[1]), item[0][1]))

    clusters: list[DuplicateCluster] = []
    for (version, sha), pages in duplicates[:max_clusters]:
        ordered = sorted(pages, key=lambda p: p.url)
        kept = ordered[:max_pages_per_cluster]
        clusters.append(
            DuplicateCluster(
                fingerprint_version=version,
                exact_sha256=sha,
                page_count=len(ordered),
                pages_omitted=len(ordered) - len(kept),
                pages=kept,
            )
        )

    return DuplicateClusterReport(
        site_id=site_id,
        pages_compared=len(rows),
        pages_without_fingerprint=without_fingerprint,
        clusters_total=len(duplicates),
        clusters_returned=len(clusters),
        clusters_omitted=len(duplicates) - len(clusters),
        duplicate_pages_total=sum(len(pages) for _, pages in duplicates),
        max_clusters=max_clusters,
        max_pages_per_cluster=max_pages_per_cluster,
        scan_truncated=scan_truncated,
        clusters=clusters,
    )


def rank_and_cap_nodes(
    candidates: Sequence[LinkGraphNode],
    *,
    max_nodes: int = GRAPH_MAX_NODES,
) -> list[LinkGraphNode]:
    """Keep the ``max_nodes`` most important pages, deterministically.

    ``link_score`` (``web_crawl/link_score.py``'s internal PageRank) is the
    ranking key — the same number that sizes the nodes. It is NULL until a
    COMPLETED full crawl has been scored, so in-degree ranks the unscored
    (never mixed: an unscored page sorts below every scored one rather than
    competing on a different scale). URL breaks remaining ties so two calls
    over unchanged data return the same subgraph — a graph that reshuffles on
    every refresh is unreadable.
    """

    ordered = sorted(
        candidates,
        key=lambda node: (
            node.link_score is None,
            -(node.link_score or 0.0),
            -node.inbound_internal_links,
            -node.outbound_internal_links,
            node.url,
        ),
    )
    return ordered[:max_nodes]


def build_progress_series(
    raw: Sequence[ProgressPoint],
    *,
    session_id: str,
    max_points: int = PROGRESS_MAX_POINTS,
    scan_truncated: bool = False,
) -> ProgressSeries:
    """Downsample a run's progress events and derive throughput.

    The FIRST and LAST samples are always kept — the last one carries the run's
    final counters, and a chart that drops it under-reports the whole crawl.
    ``pages_per_second`` is computed AFTER downsampling, so each plotted value
    is the true average across the span it is drawn over.
    """

    total = len(raw)
    if total == 0:
        return ProgressSeries(
            session_id=session_id,
            max_points=max_points,
            scan_truncated=scan_truncated,
        )

    stride = 1 if total <= max_points else ceil(total / max_points)
    kept = list(raw[::stride])
    if kept[-1] is not raw[-1]:
        if len(kept) >= max_points:
            kept[-1] = raw[-1]
        else:
            kept.append(raw[-1])

    points: list[ProgressPoint] = []
    previous: ProgressPoint | None = None
    for point in kept:
        rate: float | None = None
        if previous is None:
            elapsed_s = point.elapsed_ms / 1000.0
            if elapsed_s > 0:
                rate = round(point.pages_fetched / elapsed_s, 4)
        else:
            span = (point.occurred_at - previous.occurred_at).total_seconds()
            delta = point.pages_fetched - previous.pages_fetched
            # A RESUMED session re-runs under the same session_id with counters
            # restarting from zero, so `delta` can legitimately go negative.
            # Report no rate rather than a nonsense negative throughput.
            if span > 0 and delta >= 0:
                rate = round(delta / span, 4)
        points.append(point.model_copy(update={"pages_per_second": rate}))
        previous = point

    return ProgressSeries(
        session_id=session_id,
        points_total=total,
        points_returned=len(points),
        points_omitted=total - len(points),
        max_points=max_points,
        sample_stride=stride,
        scan_truncated=scan_truncated,
        points=points,
    )


def _progress_point(sequence: int, occurred_at: datetime, payload: dict[str, Any]) -> ProgressPoint:
    def _int(key: str) -> int:
        value = payload.get(key)
        return int(value) if isinstance(value, int | float) else 0

    return ProgressPoint(
        occurred_at=occurred_at,
        sequence=sequence,
        elapsed_ms=_int("elapsed_ms"),
        pages_discovered=_int("pages_discovered"),
        pages_fetched=_int("pages_fetched"),
        pages_failed=_int("pages_failed"),
        pages_in_flight=_int("pages_in_flight"),
        queue_depth=_int("queue_depth"),
        bytes_downloaded=_int("bytes_downloaded"),
    )


# ---------------------------------------------------------------------------
# Loaders — thin DB reads bound to the caller's RLS claims.
#
# Authorization reuses the crawler's own gates: `site_identity` (a site the
# caller cannot SELECT under RLS raises LookupError) and `assert_session_access`.
# Every query then runs inside `repo.rls()` so Postgres, not this module, is
# the authority on what the caller may read.


async def load_duplicate_clusters(
    claims: dict[str, Any],
    site_id: str,
    *,
    max_clusters: int = DUPLICATE_MAX_CLUSTERS,
    max_pages_per_cluster: int = DUPLICATE_MAX_PAGES_PER_CLUSTER,
) -> DuplicateClusterReport:
    repo = WebCrawlRepository(claims)
    await repo.site_identity(site_id)

    rows: list[tuple[tuple[int, str] | None, DuplicatePage]] = []
    scan_truncated = False
    async with repo.rls():
        last_id: str | None = None
        while True:
            filters: dict[str, Any] = {
                "site_id": site_id,
                "deleted_at__isnull": True,
                "latest_snapshot_id__isnull": False,
            }
            if last_id is not None:
                filters["id__gt"] = last_id
            pages = await WebPage.filter(**filters).order_by("id").limit(_PAGE_BATCH_SIZE).all()
            if not pages:
                break
            last_id = str(pages[-1].id)

            candidates = [
                page
                for page in pages
                # Alias pages are the same document under another URL; counting
                # them would manufacture duplicates that do not exist.
                if str(page.canonical_page_id) == str(page.id)
                and not is_machine_resource(page.url, page.content_type_last)
            ]
            for start in range(0, len(candidates), _SNAPSHOT_BATCH_SIZE):
                chunk = candidates[start : start + _SNAPSHOT_BATCH_SIZE]
                snapshots = await WebSnapshot.filter(
                    id__in=[str(p.latest_snapshot_id) for p in chunk],
                    deleted_at__isnull=True,
                ).all()
                by_id = {str(s.id): s for s in snapshots}
                for page in chunk:
                    snap = by_id.get(str(page.latest_snapshot_id))
                    if snap is None:
                        continue
                    title = (snap.head_tags or {}).get("title")
                    rows.append(
                        (
                            _fingerprint_key(snap.extracted),
                            DuplicatePage(
                                page_id=str(page.id),
                                url=str(page.url),
                                title=title if isinstance(title, str) and title.strip() else None,
                                word_count=(
                                    int(snap.word_count) if snap.word_count is not None else None
                                ),
                            ),
                        )
                    )

            if len(rows) >= _MAX_PAGES_SCANNED:
                scan_truncated = True
                break
            if len(pages) < _PAGE_BATCH_SIZE:
                break

    return build_duplicate_clusters(
        rows,
        site_id=site_id,
        max_clusters=max_clusters,
        max_pages_per_cluster=max_pages_per_cluster,
        scan_truncated=scan_truncated,
    )


async def load_link_graph(
    claims: dict[str, Any],
    site_id: str,
    *,
    max_nodes: int = GRAPH_MAX_NODES,
    max_edges: int = GRAPH_MAX_EDGES,
) -> LinkGraph:
    repo = WebCrawlRepository(claims)
    await repo.site_identity(site_id)

    async with repo.rls():
        # Edges are scoped to each page's CURRENT snapshot — historical crawl
        # edges would draw links the site no longer has. Expressed as a
        # sub-select so ~610k edge rows are filtered in Postgres, never by
        # shipping tens of thousands of snapshot ids into an IN list.
        current_snapshots = Subquery(
            WebPage.filter(
                site_id=site_id,
                deleted_at__isnull=True,
                latest_snapshot_id__isnull=False,
            ).select("latest_snapshot_id")
        )
        edge_base = WebLinkEdge.filter(
            site_id=site_id,
            is_internal=True,
            deleted_at__isnull=True,
            target_page_id__isnull=False,
            snapshot_id__in=current_snapshots,
        )
        inbound_rows = await (
            edge_base.group_by("target_page_id")
            .annotate(inbound=Count())
            .values("target_page_id", "inbound")
        )
        outbound_rows = await (
            edge_base.group_by("source_page_id")
            .annotate(outbound=Count())
            .values("source_page_id", "outbound")
        )
        inbound = {str(r["target_page_id"]): int(r["inbound"]) for r in inbound_rows}
        outbound = {str(r["source_page_id"]): int(r["outbound"]) for r in outbound_rows}

        candidates: list[LinkGraphNode] = []
        scan_truncated = False
        last_id: str | None = None
        while True:
            filters: dict[str, Any] = {"site_id": site_id, "deleted_at__isnull": True}
            if last_id is not None:
                filters["id__gt"] = last_id
            pages = await WebPage.filter(**filters).order_by("id").limit(_PAGE_BATCH_SIZE).all()
            if not pages:
                break
            last_id = str(pages[-1].id)
            for page in pages:
                page_id = str(page.id)
                if str(page.canonical_page_id) != page_id:
                    continue
                candidates.append(
                    LinkGraphNode(
                        page_id=page_id,
                        url=str(page.url),
                        link_score=(
                            float(page.link_score) if page.link_score is not None else None
                        ),
                        inbound_internal_links=inbound.get(page_id, 0),
                        outbound_internal_links=outbound.get(page_id, 0),
                        http_status=(
                            int(page.http_status_last)
                            if page.http_status_last is not None
                            else None
                        ),
                        status=str(page.status),
                    )
                )
            if len(candidates) >= _MAX_PAGES_SCANNED:
                scan_truncated = True
                break
            if len(pages) < _PAGE_BATCH_SIZE:
                break

        nodes = rank_and_cap_nodes(candidates, max_nodes=max_nodes)
        node_ids = [node.page_id for node in nodes]

        edges: list[LinkGraphEdge] = []
        edges_total = 0
        if node_ids:
            # Both endpoints must be in the returned node set, so every edge
            # the client receives is drawable. Parallel edges (same pair, many
            # anchors) collapse to one weighted edge in Postgres.
            scoped = edge_base.filter(source_page_id__in=node_ids, target_page_id__in=node_ids)
            totals = await scoped.aggregate(
                pairs=Count("source_page_id", "target_page_id", distinct=True)
            )
            edges_total = int(totals.get("pairs") or 0)
            pair_rows = await (
                scoped.group_by("source_page_id", "target_page_id")
                .annotate(link_count=Count())
                .order_by("-link_count", "source_page_id", "target_page_id")
                .limit(max_edges)
                .values("source_page_id", "target_page_id", "link_count")
            )
            edges = [
                LinkGraphEdge(
                    source=str(row["source_page_id"]),
                    target=str(row["target_page_id"]),
                    link_count=int(row["link_count"]),
                )
                for row in pair_rows
            ]

    scored = sum(1 for node in candidates if node.link_score is not None)
    return LinkGraph(
        site_id=site_id,
        ranking="link_score" if scored else "inbound_internal_links",
        nodes_with_link_score=scored,
        nodes_total=len(candidates),
        nodes_returned=len(nodes),
        nodes_omitted=len(candidates) - len(nodes),
        edges_total=edges_total,
        edges_returned=len(edges),
        edges_omitted=max(0, edges_total - len(edges)),
        max_nodes=max_nodes,
        max_edges=max_edges,
        scan_truncated=scan_truncated,
        nodes=nodes,
        edges=edges,
    )


async def load_progress_series(
    claims: dict[str, Any],
    session_id: str,
    *,
    max_points: int = PROGRESS_MAX_POINTS,
) -> ProgressSeries:
    repo = WebCrawlRepository(claims)
    await repo.assert_session_access(session_id)

    raw: list[ProgressPoint] = []
    scan_truncated = False
    async with repo.rls():
        last_sequence: int | None = None
        while True:
            filters: dict[str, Any] = {
                "session_id": session_id,
                "event_type": PROGRESS_EVENT_TYPE,
                "deleted_at__isnull": True,
            }
            if last_sequence is not None:
                filters["sequence__gt"] = last_sequence
            rows = await (
                WebCrawlEvent.filter(**filters)
                .order_by("sequence")
                .limit(_PROGRESS_BATCH_SIZE)
                .values("sequence", "occurred_at", "payload")
            )
            if not rows:
                break
            last_sequence = int(rows[-1]["sequence"])
            for row in rows:
                payload = row["payload"]
                raw.append(
                    _progress_point(
                        int(row["sequence"]),
                        row["occurred_at"],
                        payload if isinstance(payload, dict) else {},
                    )
                )
            if len(raw) >= _MAX_PROGRESS_SCANNED:
                scan_truncated = True
                break
            if len(rows) < _PROGRESS_BATCH_SIZE:
                break

    return build_progress_series(
        raw,
        session_id=session_id,
        max_points=max_points,
        scan_truncated=scan_truncated,
    )


async def load_traffic_at_risk(
    claims: dict[str, Any],
    site_id: str,
    *,
    max_pages: int = TRAFFIC_AT_RISK_MAX_PAGES,
) -> TrafficAtRiskReport:
    """URLs Google is showing that our own fetch could not load.

    The single most expensive thing a site can be doing silently: Google sends
    people to a URL, the URL answers 404/500/nothing, and nobody notices because
    no surface joined "Google shows this" to "we cannot fetch this". Both halves
    were already canonical (`web.gsc_page_stat.impressions` and
    `web.page.http_status_last`) — the join is what did not exist, and until the
    verification sweep filled the status column for GSC-declared URLs, it could
    not have been computed for most of them anyway.

    Ranked by impressions, because the point is the traffic at stake, not the
    row count. `unverified_with_impressions` reports how many Google-visible
    URLs we still have NO status for — the honest "this list may be incomplete"
    number, never omitted.
    """

    repo = WebCrawlRepository(claims)
    await repo.site_identity(site_id)

    async with repo.rls():
        impressions: dict[str, int] = {}
        clicks: dict[str, int] = {}
        last_id: str | None = None
        scan_truncated = False
        while True:
            filters: dict[str, Any] = {"site_id": site_id, "deleted_at__isnull": True}
            if last_id is not None:
                filters["id__gt"] = last_id
            rows = await (
                WebGscPageStat.filter(**filters)
                .order_by("id")
                .limit(_GSC_BATCH_SIZE)
                .values("id", "page_id", "impressions", "clicks")
            )
            if not rows:
                break
            last_id = str(rows[-1]["id"])
            for row in rows:
                page_id = str(row["page_id"])
                impressions[page_id] = impressions.get(page_id, 0) + int(row["impressions"] or 0)
                clicks[page_id] = clicks.get(page_id, 0) + int(row["clicks"] or 0)
            if len(impressions) >= _MAX_GSC_PAGES_SCANNED:
                scan_truncated = True
                break
            if len(rows) < _GSC_BATCH_SIZE:
                break

        page_ids = [pid for pid, shown in impressions.items() if shown > 0]
        at_risk: list[TrafficAtRiskPage] = []
        unverified = 0
        throttled = 0
        sitemap_ids: set[str] = set()
        for start in range(0, len(page_ids), _PAGE_BATCH_SIZE):
            chunk = page_ids[start : start + _PAGE_BATCH_SIZE]
            members = await WebPageSitemap.filter(
                site_id=site_id, deleted_at__isnull=True, page_id__in=chunk
            ).values("page_id")
            sitemap_ids.update(str(m["page_id"]) for m in members)
            pages = await WebPage.filter(id__in=chunk, deleted_at__isnull=True).values(
                "id", "url", "http_status_last", "content_type_last", "metadata", "last_seen"
            )
            for page in pages:
                status = page["http_status_last"]
                if status is None:
                    unverified += 1
                    continue
                status = int(status)
                if 200 <= status < 400:
                    continue
                if status in THROTTLED_STATUSES:
                    # 429 is a fact about OUR request rate, not about the URL.
                    # Counting it as at-risk told iopbm.com that 99.18% of its
                    # Google traffic was on broken pages when the only thing
                    # that had happened was our own crawler getting throttled.
                    # Reported separately, never silently dropped.
                    throttled += 1
                    continue
                page_id = str(page["id"])
                verification = (page["metadata"] or {}).get(VERIFICATION_METADATA_KEY)
                at_risk.append(
                    TrafficAtRiskPage(
                        page_id=page_id,
                        url=str(page["url"]),
                        http_status=status,
                        content_type=page["content_type_last"],
                        impressions=impressions.get(page_id, 0),
                        clicks=clicks.get(page_id, 0),
                        in_sitemap=page_id in sitemap_ids,
                        evidence_source="verification" if verification else "crawl",
                        last_seen=page["last_seen"],
                    )
                )

    at_risk.sort(key=lambda p: (-p.impressions, -p.clicks, p.url))
    total_impressions = sum(impressions.values())
    at_risk_impressions = sum(p.impressions for p in at_risk)
    returned = at_risk[:max_pages]
    return TrafficAtRiskReport(
        site_id=site_id,
        pages_with_impressions=len(page_ids),
        pages_at_risk_total=len(at_risk),
        pages_returned=len(returned),
        pages_omitted=max(0, len(at_risk) - len(returned)),
        impressions_at_risk=at_risk_impressions,
        clicks_at_risk=sum(p.clicks for p in at_risk),
        share_of_impressions_at_risk=(
            round(100.0 * at_risk_impressions / total_impressions, 2) if total_impressions else 0.0
        ),
        unverified_with_impressions=unverified,
        throttled_not_assessed=throttled,
        max_pages=max_pages,
        scan_truncated=scan_truncated,
        pages=returned,
    )


__all__ = [
    "TRAFFIC_AT_RISK_MAX_PAGES",
    "load_traffic_at_risk",
    "DUPLICATE_MAX_CLUSTERS",
    "DUPLICATE_MAX_PAGES_PER_CLUSTER",
    "GRAPH_MAX_EDGES",
    "GRAPH_MAX_NODES",
    "PROGRESS_MAX_POINTS",
    "build_duplicate_clusters",
    "build_progress_series",
    "load_duplicate_clusters",
    "load_link_graph",
    "load_progress_series",
    "rank_and_cap_nodes",
]
