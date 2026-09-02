"""Authenticated browser-direct commands for canonical site crawls.

There are intentionally no list/detail/history ROW routes here. The browser
reads all stored site/page/session/snapshot/event data directly from Supabase.
This router starts new live work, cancels it, and serves the DERIVED shapes a
client cannot assemble from row reads — duplicate-content clusters, the
internal link graph, a run's progress series (`web_crawl/insights.py`), and
run-over-run diffs (`web_crawl/diff.py`). Every one of them is an aggregation
or comparison over evidence that is already canonical, computed on demand
against no cache table, and every one of them is capped.

It also owns crawl CONFIGURATION — presets and the rescrape derivation. A
preset is a command INPUT, not stored evidence, and its recency ordering plus
the "what would Rescrape run?" resolution order must have exactly one
implementation; see `web_crawl/presets.py`.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import StreamingResponse

from matrx_connect import AppContext, context_dep
from matrx_connect.streaming import create_streaming_response

from matrx_scraper.user_agents import presets_payload
from matrx_scraper.web_crawl.contracts import (
    CrawlCancelResponse,
    CrawlDiff,
    PreviousSessionResponse,
    SiteDiffList,
    CrawlPresetDeleteResponse,
    CrawlPresetListResponse,
    CrawlPresetRecord,
    CrawlPresetSaveRequest,
    CrawlStartRequest,
    DuplicateClusterReport,
    TrafficAtRiskReport,
    LinkGraph,
    PageFetchRequest,
    ProgressSeries,
    RecrawlConfigResponse,
    RecrawlRequest,
    UserAgentPresetRecord,
    UserAgentPresetsResponse,
)
from matrx_scraper.web_crawl.diff import (
    DEFAULT_SITE_DIFF_LIMIT,
    MAX_SITE_DIFF_LIMIT,
    load_previous_session,
    load_session_diff,
    load_site_diffs,
    load_site_session_diff,
)
from matrx_scraper.web_crawl.insights import (
    DUPLICATE_MAX_CLUSTERS,
    DUPLICATE_MAX_PAGES_PER_CLUSTER,
    GRAPH_MAX_EDGES,
    GRAPH_MAX_NODES,
    PROGRESS_MAX_POINTS,
    TRAFFIC_AT_RISK_MAX_PAGES,
    load_duplicate_clusters,
    load_traffic_at_risk,
    load_link_graph,
    load_progress_series,
)
from matrx_scraper.web_crawl.persistence import build_user_claims
from matrx_scraper.web_crawl.service import (
    PreparedAnalysis,
    PreparedCrawl,
    PreparedGscSync,
    PreparedLinkCheck,
    PreparedLinkResolution,
    PreparedLinkScore,
    PreparedSitemapSync,
    PreparedUrlReconciliation,
    get_web_crawl_service,
)

router = APIRouter()


def _stream_headers(
    response: StreamingResponse,
    prepared: (
        PreparedCrawl
        | PreparedSitemapSync
        | PreparedGscSync
        | PreparedLinkResolution
        | PreparedLinkCheck
        | PreparedLinkScore
        | PreparedUrlReconciliation
        | PreparedAnalysis
    ),
) -> StreamingResponse:
    response.headers["X-Crawl-Session-Id"] = prepared.session_id
    response.headers["X-Site-Id"] = prepared.site_id
    return response


@router.post("/crawler/sites/{site_id}/sessions")
async def start_crawl(
    site_id: str,
    request: CrawlStartRequest,
    ctx: AppContext = Depends(context_dep),
) -> StreamingResponse:
    service = get_web_crawl_service()
    try:
        prepared = await service.prepare_start(ctx, site_id, request)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        # One active site-wide crawl per site — mirror resume's contract.
        if "already active" in str(exc):
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    response = create_streaming_response(
        ctx,
        service.run_prepared,
        prepared,
        initial_message="Starting site crawl…",
        debug_label="CanonicalSiteCrawl",
    )
    return _stream_headers(response, prepared)


@router.post("/crawler/sessions/{session_id}/resume")
async def resume_crawl(
    session_id: str,
    ctx: AppContext = Depends(context_dep),
) -> StreamingResponse:
    """Continue a CRASHED crawl session from its durable frontier.

    The session's persisted request is rebuilt (max_pages shrunk by pages
    already fetched) and the run reattaches to the SAME batch execution's
    pending work items. 409 when a run of this session is already active
    ANYWHERE — this process's broker, another process's live run lease, or a
    claimant that won the lease compare-and-swap first; 422 when the session is
    not resumable (finished, cancelled, short-run mode, resume-attempt cap).
    """
    service = get_web_crawl_service()
    try:
        prepared = await service.prepare_resume(ctx, session_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        if "already active" in str(exc):
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    response = create_streaming_response(
        ctx,
        service.run_prepared,
        prepared,
        initial_message="Resuming site crawl…",
        debug_label="CanonicalSiteCrawlResume",
    )
    return _stream_headers(response, prepared)


@router.post("/crawler/sites/{site_id}/bootstrap")
async def bootstrap_site(
    site_id: str,
    ctx: AppContext = Depends(context_dep),
) -> StreamingResponse:
    """Capture the homepage immediately after the frontend creates a site."""

    service = get_web_crawl_service()
    try:
        prepared = await service.prepare_bootstrap(ctx, site_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    response = create_streaming_response(
        ctx,
        service.run_prepared,
        prepared,
        initial_message="Capturing site homepage…",
        debug_label="CanonicalSiteBootstrap",
    )
    return _stream_headers(response, prepared)


@router.post("/crawler/sites/{site_id}/pages/fetch")
async def fetch_page(
    site_id: str,
    request: PageFetchRequest,
    ctx: AppContext = Depends(context_dep),
) -> StreamingResponse:
    """Capture the freshest version of ONE page (existing or brand-new URL)."""

    service = get_web_crawl_service()
    try:
        prepared = await service.prepare_page_fetch(
            ctx,
            site_id,
            request.url,
            capture_screenshot=request.capture_screenshot,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    response = create_streaming_response(
        ctx,
        service.run_prepared,
        prepared,
        initial_message="Fetching the latest version of this page…",
        debug_label="CanonicalPageFetch",
    )
    return _stream_headers(response, prepared)


@router.post("/crawler/sites/{site_id}/initialize")
async def initialize_site(
    site_id: str,
    ctx: AppContext = Depends(context_dep),
) -> StreamingResponse:
    """Initialize a canonical marketing site and stream step progress."""

    service = get_web_crawl_service()
    try:
        prepared = await service.prepare_initialize(ctx, site_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    response = create_streaming_response(
        ctx,
        service.run_initialize,
        prepared,
        initial_message="Initializing site…",
        debug_label="CanonicalSiteInitialization",
    )
    return _stream_headers(response, prepared)


@router.post("/crawler/sites/{site_id}/sitemaps/sync")
async def sync_sitemaps(
    site_id: str,
    ctx: AppContext = Depends(context_dep),
) -> StreamingResponse:
    """Sync the site's sitemap graph into web.sitemap / web.page / web.page_sitemap."""

    service = get_web_crawl_service()
    try:
        prepared = await service.prepare_sitemap_sync(ctx, site_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    response = create_streaming_response(
        ctx,
        service.run_sitemap_sync,
        prepared,
        initial_message="Syncing sitemaps…",
        debug_label="CanonicalSitemapSync",
    )
    return _stream_headers(response, prepared)


@router.post("/crawler/sites/{site_id}/gsc/sync")
async def sync_gsc(
    site_id: str,
    ctx: AppContext = Depends(context_dep),
) -> StreamingResponse:
    """Sync the site's bound Google Search Console property into
    web.gsc_page_stat / web.page and record the run on web.site."""

    service = get_web_crawl_service()
    try:
        prepared = await service.prepare_gsc_sync(ctx, site_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    response = create_streaming_response(
        ctx,
        service.run_gsc_sync,
        prepared,
        initial_message="Syncing Google Search Console…",
        debug_label="CanonicalGscSync",
    )
    return _stream_headers(response, prepared)


@router.post("/crawler/sites/{site_id}/links/resolve")
async def resolve_links(
    site_id: str,
    ctx: AppContext = Depends(context_dep),
) -> StreamingResponse:
    """Backfill web.link_edge.target_page_id for the site's internal edges."""

    service = get_web_crawl_service()
    try:
        prepared = await service.prepare_link_resolution(ctx, site_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    response = create_streaming_response(
        ctx,
        service.run_link_resolution,
        prepared,
        initial_message="Resolving internal link targets…",
        debug_label="CanonicalLinkResolution",
    )
    return _stream_headers(response, prepared)


@router.post("/crawler/sites/{site_id}/links/score")
async def score_links(
    site_id: str,
    ctx: AppContext = Depends(context_dep),
) -> StreamingResponse:
    """Recompute web.page.link_score — internal-link PageRank over the site's
    current link graph. Runs automatically after a full crawl; this is the
    on-demand recompute / retry path."""

    service = get_web_crawl_service()
    try:
        prepared = await service.prepare_link_score(ctx, site_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    response = create_streaming_response(
        ctx,
        service.run_link_score,
        prepared,
        initial_message="Computing internal link scores…",
        debug_label="CanonicalLinkScore",
    )
    return _stream_headers(response, prepared)


@router.post("/crawler/sites/{site_id}/urls/reconcile")
async def reconcile_urls(
    site_id: str,
    ctx: AppContext = Depends(context_dep),
) -> StreamingResponse:
    """Re-match every GSC, sitemap, and crawl URL to one canonical page."""

    service = get_web_crawl_service()
    try:
        prepared = await service.prepare_url_reconciliation(ctx, site_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    response = create_streaming_response(
        ctx,
        service.run_url_reconciliation,
        prepared,
        initial_message="Reconciling canonical URL identities…",
        debug_label="CanonicalUrlReconciliation",
    )
    return _stream_headers(response, prepared)


@router.post("/crawler/sites/{site_id}/links/check")
async def check_links(
    site_id: str,
    ctx: AppContext = Depends(context_dep),
) -> StreamingResponse:
    """Populate web.link_edge.http_status for the site's internal + external
    edges so broken-link detection has data to work with."""

    service = get_web_crawl_service()
    try:
        prepared = await service.prepare_link_check(ctx, site_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    response = create_streaming_response(
        ctx,
        service.run_link_check,
        prepared,
        initial_message="Checking link targets…",
        debug_label="CanonicalLinkCheck",
    )
    return _stream_headers(response, prepared)


@router.post("/crawler/sites/{site_id}/analyze")
async def analyze_site(
    site_id: str,
    ctx: AppContext = Depends(context_dep),
) -> StreamingResponse:
    """Run the deterministic page-analysis catalogue over the site's stored
    crawl evidence, writing web.analysis_result + web.finding rows."""

    service = get_web_crawl_service()
    try:
        prepared = await service.prepare_analysis(ctx, site_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        if "already active" in str(exc):
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        raise
    response = create_streaming_response(
        ctx,
        service.run_analysis,
        prepared,
        initial_message="Analyzing pages against the audit catalogue…",
        debug_label="CanonicalPageAnalysis",
    )
    return _stream_headers(response, prepared)


@router.post("/crawler/sessions/{session_id}/cancel")
async def cancel_crawl(
    session_id: str,
    ctx: AppContext = Depends(context_dep),
) -> CrawlCancelResponse:
    service = get_web_crawl_service()
    try:
        await service.cancel(ctx, session_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return CrawlCancelResponse(session_id=session_id)


# ---------------------------------------------------------------------------
# Derived reads. Each response reports what its cap DROPPED (`*_omitted`,
# `scan_truncated`) — a capped aggregate that only reports what it kept reads
# as "this is everything", and `web.link_edge` alone holds ~610k rows.


@router.get("/crawler/sites/{site_id}/duplicate-clusters")
async def duplicate_clusters(
    site_id: str,
    max_clusters: int = Query(DUPLICATE_MAX_CLUSTERS, ge=1, le=1_000),
    max_pages_per_cluster: int = Query(DUPLICATE_MAX_PAGES_PER_CLUSTER, ge=2, le=500),
    ctx: AppContext = Depends(context_dep),
) -> DuplicateClusterReport:
    """Pages whose visible text is byte-identical, grouped into clusters.

    Same fingerprint key the `duplicate_content_exact` analysis check uses, so
    a page flagged there always appears in exactly one cluster here.
    """

    try:
        return await load_duplicate_clusters(
            build_user_claims(ctx),
            site_id,
            max_clusters=max_clusters,
            max_pages_per_cluster=max_pages_per_cluster,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/crawler/sites/{site_id}/traffic-at-risk")
async def traffic_at_risk(
    site_id: str,
    max_pages: int = Query(TRAFFIC_AT_RISK_MAX_PAGES, ge=1, le=2_000),
    ctx: AppContext = Depends(context_dep),
) -> TrafficAtRiskReport:
    """URLs Google is showing that our own fetch could not load.

    Ranked by impressions — the point is the traffic at stake, not the row
    count. `unverified_with_impressions` says how many Google-visible URLs we
    still have no status for, so the list never implies completeness it lacks.
    """

    try:
        return await load_traffic_at_risk(build_user_claims(ctx), site_id, max_pages=max_pages)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/crawler/sites/{site_id}/link-graph")
async def link_graph(
    site_id: str,
    max_nodes: int = Query(GRAPH_MAX_NODES, ge=1, le=5_000),
    max_edges: int = Query(GRAPH_MAX_EDGES, ge=1, le=20_000),
    ctx: AppContext = Depends(context_dep),
) -> LinkGraph:
    """The site's CURRENT internal link graph, ranked by in-degree and capped.

    Nodes are the most-linked-to canonical pages; edges are returned only when
    BOTH endpoints survived `max_nodes`, so every edge is drawable.
    """

    try:
        return await load_link_graph(
            build_user_claims(ctx),
            site_id,
            max_nodes=max_nodes,
            max_edges=max_edges,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/crawler/sessions/{session_id}/progress-series")
async def progress_series(
    session_id: str,
    max_points: int = Query(PROGRESS_MAX_POINTS, ge=2, le=5_000),
    ctx: AppContext = Depends(context_dep),
) -> ProgressSeries:
    """Pages-per-second / queue-depth timeseries for one crawl session.

    Derived from the `crawl_progress` rows already in `web.crawl_event` — there
    is deliberately no snapshots table.
    """

    try:
        return await load_progress_series(
            build_user_claims(ctx),
            session_id,
            max_points=max_points,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/crawler/sessions/{session_id}/previous")
async def previous_session(
    session_id: str,
    ctx: AppContext = Depends(context_dep),
) -> PreviousSessionResponse:
    """The baseline this session's 'what changed' widget should diff against.

    The most recent site-WIDE crawl (`full` / `list`) of the same site that ran
    before this one. `previous` is null on a site's first crawl.
    """

    try:
        return await load_previous_session(build_user_claims(ctx), session_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/crawler/sessions/{base_session_id}/diff/{compare_session_id}")
async def session_diff(
    base_session_id: str,
    compare_session_id: str,
    ctx: AppContext = Depends(context_dep),
) -> CrawlDiff:
    """Page-level diff of two crawl sessions of the SAME site.

    Added / removed / returned URLs plus per-page status, title, meta
    description, content-hash, and word-count changes. Derived on demand from
    `web.crawl_url` + `web.page` + `web.snapshot` — there is no diff cache
    table; see `web_crawl/diff.py` for why.
    """

    try:
        return await load_session_diff(build_user_claims(ctx), base_session_id, compare_session_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/crawler/sites/{site_id}/diffs")
async def site_diffs(
    site_id: str,
    limit: int = Query(DEFAULT_SITE_DIFF_LIMIT, ge=1, le=MAX_SITE_DIFF_LIMIT),
    ctx: AppContext = Depends(context_dep),
) -> SiteDiffList:
    """Counts-only diff of each recent site-wide crawl against its predecessor."""

    try:
        return await load_site_diffs(build_user_claims(ctx), site_id, limit=limit)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/crawler/sites/{site_id}/diffs/{session_id}")
async def site_session_diff(
    site_id: str,
    session_id: str,
    ctx: AppContext = Depends(context_dep),
) -> CrawlDiff:
    """Full diff of one of the site's crawl sessions against its predecessor."""

    try:
        return await load_site_session_diff(build_user_claims(ctx), site_id, session_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


# ---------------------------------------------------------------------------
# User-Agent presets — the named choices a crawl-config UI offers.


@router.get("/crawler/user-agents")
async def list_user_agent_presets(
    ctx: AppContext = Depends(context_dep),
) -> UserAgentPresetsResponse:
    """The named User-Agent choices for `CrawlStartRequest.user_agent`.

    Served rather than hard-coded in each client so the label a user reads and
    the value the API accepts cannot drift apart. A client renders these as the
    primary control; the raw string field stays available as the escape hatch,
    bounded by `max_length`.
    """

    return UserAgentPresetsResponse(
        presets=[UserAgentPresetRecord(**preset) for preset in presets_payload()]
    )


# ---------------------------------------------------------------------------
# Crawl presets — saved, named crawl configs for one site.


@router.get("/crawler/sites/{site_id}/presets")
async def list_crawl_presets(
    site_id: str,
    ctx: AppContext = Depends(context_dep),
) -> CrawlPresetListResponse:
    """The site's presets, most-recently-used first, never-used last.

    Also reports the site's pinned `default_preset_id` so a client can show
    which one a one-click rescrape would pick.
    """

    service = get_web_crawl_service()
    try:
        return await service.list_presets(ctx, site_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/crawler/sites/{site_id}/presets")
async def save_crawl_preset(
    site_id: str,
    request: CrawlPresetSaveRequest,
    ctx: AppContext = Depends(context_dep),
) -> CrawlPresetRecord:
    """Create or replace a preset by name. Requires site editor access."""

    service = get_web_crawl_service()
    try:
        return await service.save_preset(ctx, site_id, request)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.delete("/crawler/sites/{site_id}/presets/{preset_id}")
async def delete_crawl_preset(
    site_id: str,
    preset_id: str,
    ctx: AppContext = Depends(context_dep),
) -> CrawlPresetDeleteResponse:
    """Soft-delete a preset. Requires site editor access."""

    service = get_web_crawl_service()
    try:
        return await service.delete_preset(ctx, site_id, preset_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


# ---------------------------------------------------------------------------
# One-click rescrape


@router.get("/crawler/sites/{site_id}/recrawl-config")
async def preview_recrawl_config(
    site_id: str,
    preset_id: str | None = Query(default=None),
    ctx: AppContext = Depends(context_dep),
) -> RecrawlConfigResponse:
    """What a one-click rescrape WOULD run, and where the config came from.

    A Rescrape button that cannot say what it is about to do is a dead end;
    this is that answer, resolved by the same code the command uses.
    """

    service = get_web_crawl_service()
    try:
        return await service.recrawl_config(ctx, site_id, preset_id=preset_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/crawler/sites/{site_id}/rescrape")
async def rescrape_site(
    site_id: str,
    request: RecrawlRequest | None = None,
    ctx: AppContext = Depends(context_dep),
) -> StreamingResponse:
    """Crawl this site again with no request body required.

    The config is derived (named preset -> the site's pinned default preset ->
    the last site-wide crawl's persisted request -> defaults) and the run then
    behaves exactly like `POST /crawler/sites/{site_id}/sessions`.
    """

    service = get_web_crawl_service()
    preset_id = request.preset_id if request is not None else None
    try:
        prepared = await service.prepare_rescrape(ctx, site_id, preset_id=preset_id)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        if "already active" in str(exc):
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    response = create_streaming_response(
        ctx,
        service.run_prepared,
        prepared,
        initial_message="Re-crawling site…",
        debug_label="CanonicalSiteRescrape",
    )
    return _stream_headers(response, prepared)


__all__ = ["router"]
