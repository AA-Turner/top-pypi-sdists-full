"""Browser command contracts for direct canonical crawls."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from matrx_scraper.crawler import RENDER_HTTP_FIRST, VALID_RENDER_MODES
from matrx_scraper.user_agents import (
    MAX_USER_AGENT_LENGTH,
    InvalidUserAgentError,
    normalize_user_agent,
)

ScreenshotKind = Literal[
    "viewport_desktop",
    "viewport_laptop",
    "viewport_mobile",
    "viewport_tablet",
    "full_page",
    "desktop_full",
    "desktop_fold",
    "laptop_full",
    "tablet_full",
    "mobile_full",
    "mobile_fold",
]

InitializationStep = Literal[
    "identity",
    "sitemaps",
    "screenshots",
    "discovered",
    "url_reconciliation",
    "site_update",
]
InitializationStepStatus = Literal["started", "ok", "failed"]

# The per-step frontend contract for POST .../sites/{site_id}/initialize.
# The frontend refetches the relevant data slice when each step completes;
# these names and the event shape are a CONTRACT (see web_crawl/FEATURE.md).
InitializeStepName = Literal["identity", "screenshots", "sitemaps", "discovered"]
InitializeStepStatus = Literal["started", "complete", "failed", "skipped"]

INITIALIZATION_SCREENSHOT_KINDS: list[ScreenshotKind] = [
    "desktop_full",
    "desktop_fold",
    "mobile_full",
    "mobile_fold",
]


class InitializationError(BaseModel):
    step: InitializationStep
    error_type: str
    message: str


class SiteInitializationSummary(BaseModel):
    homepage: str = "pending"
    identity: dict[str, Any] = Field(default_factory=dict)
    sitemaps: dict[str, Any] = Field(default_factory=lambda: {"found": 0, "urls": 0})
    screenshots: dict[str, Any] = Field(default_factory=lambda: {"captured": 0})
    discovered: dict[str, int] = Field(default_factory=dict)
    url_reconciliation: dict[str, int] = Field(default_factory=dict)
    errors: list[InitializationError] = Field(default_factory=list)
    warnings: list[InitializationError] = Field(default_factory=list)


class InitializeStepEvent(BaseModel):
    """Granular machine-readable initialize progress — one event per step
    transition. ``step`` and ``status`` values plus the ``counts`` keys are a
    frontend CONTRACT (documented in web_crawl/FEATURE.md); the frontend
    refetches per-step on these events."""

    event_type: Literal["initialize_step"] = "initialize_step"
    site_id: str
    session_id: str
    step: InitializeStepName
    status: InitializeStepStatus
    message: str
    counts: dict[str, int] = Field(default_factory=dict)
    error: str | None = None
    ts: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class SitemapSyncSummary(BaseModel):
    """Summary persisted to ``web.site.initialization.sitemaps`` and emitted
    as the standalone sync command's final data event."""

    found: int = 0
    urls: int = 0
    pages_upserted: int = 0
    truncated: bool = False


class SitemapSyncProgressEvent(BaseModel):
    event_type: Literal["sitemap_sync_progress"] = "sitemap_sync_progress"
    site_id: str
    session_id: str
    status: Literal["started", "progress", "ok", "failed"]
    message: str
    summary: SitemapSyncSummary
    errors: list[str] = Field(default_factory=list)
    ts: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class GscSyncSummary(BaseModel):
    """Summary persisted to ``web.site.gsc_sync`` and emitted as the GSC sync
    command's final data event."""

    property: str = ""
    days: int = 0
    pages: int = 0
    stats_rows: int = 0
    submitted_sitemaps: list[dict[str, Any]] = Field(default_factory=list)
    skipped_out_of_scope: int = 0
    errors: list[str] = Field(default_factory=list)


class GscSyncProgressEvent(BaseModel):
    event_type: Literal["gsc_sync_progress"] = "gsc_sync_progress"
    site_id: str
    session_id: str
    status: Literal["started", "progress", "ok", "failed"]
    message: str
    summary: GscSyncSummary
    ts: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class UrlReconciliationSummary(BaseModel):
    pages_scanned: int = 0
    relations_scanned: int = 0
    aliases_matched: int = 0
    pointers_changed: int = 0
    gsc_rows_moved: int = 0
    sitemap_memberships_moved: int = 0
    cycles: int = 0
    intent_conflicts: int = 0


class UrlReconciliationProgressEvent(BaseModel):
    event_type: Literal["url_reconciliation_progress"] = "url_reconciliation_progress"
    site_id: str
    session_id: str
    status: Literal["started", "progress", "ok", "failed"]
    message: str
    summary: UrlReconciliationSummary
    ts: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class LinkResolutionSummary(BaseModel):
    """Summary emitted by the link-target backfill command."""

    scanned: int = 0
    resolved: int = 0
    unresolved: int = 0


class LinkResolutionProgressEvent(BaseModel):
    event_type: Literal["link_resolution_progress"] = "link_resolution_progress"
    site_id: str
    session_id: str
    status: Literal["started", "progress", "ok", "failed"]
    message: str
    summary: LinkResolutionSummary
    ts: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class LinkCheckSummary(BaseModel):
    """Summary emitted by the link-status verification command.

    ``0`` recorded on an edge means "no response" (DNS/TLS/timeout) — a dead
    target, distinct from unchecked NULL.
    """

    internal_scanned: int = 0
    internal_updated: int = 0
    internal_uncrawled: int = 0
    internal_unresolved: int = 0
    external_targets: int = 0
    external_cached: int = 0
    external_checked: int = 0
    external_ok: int = 0
    external_broken: int = 0
    external_unreachable: int = 0
    external_edges_updated: int = 0
    external_skipped_non_http: int = 0
    external_truncated: bool = False


class LinkCheckProgressEvent(BaseModel):
    event_type: Literal["link_check_progress"] = "link_check_progress"
    site_id: str
    session_id: str
    status: Literal["started", "progress", "ok", "failed"]
    message: str
    summary: LinkCheckSummary
    ts: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class LinkScoreSummary(BaseModel):
    """Summary emitted by the internal-link PageRank scoring command.

    ``nodes`` counts canonical page groups (a redirected duplicate is scored
    with the page it resolves to), while ``pages_scored`` counts the
    ``web.page`` rows actually written — every member of every group.
    """

    pages_captured: int = 0
    nodes: int = 0
    edges_scanned: int = 0
    edges_resolved: int = 0
    edges_unresolved: int = 0
    pages_scored: int = 0
    top_score: float | None = None
    computed_at: str | None = None


class LinkScoreProgressEvent(BaseModel):
    event_type: Literal["link_score_progress"] = "link_score_progress"
    site_id: str
    session_id: str
    status: Literal["started", "progress", "ok", "failed"]
    message: str
    summary: LinkScoreSummary
    ts: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class AnalysisSummary(BaseModel):
    """Summary emitted by the deterministic page-analysis command.

    ``n_a`` outcomes carry no score and never open findings — they mark
    evidence the crawl has not captured yet (legacy snapshot, unchecked
    links), never a silent pass.
    """

    pages_total: int = 0
    pages_analyzed: int = 0
    pages_skipped_alias: int = 0
    pages_skipped_non_html: int = 0
    pages_skipped_no_snapshot: int = 0
    # Pages analyzed from `web.crawl_url` evidence alone — a URL the crawler
    # attempted that produced no snapshot (404, 5xx, timeout, redirect loop).
    # Only the transport checks can answer for them; every content check is
    # `n_a`, never a pass.
    pages_transport_only: int = 0
    # `web.crawl_url` rows with no usable `web.page` subject to record against.
    crawl_urls_skipped_no_page: int = 0
    checks_run: int = 0
    # Checks recorded against the SITE itself rather than a page (TLS, HSTS,
    # security headers): one row per site check per run, `subject_type='site'`.
    site_checks_run: int = 0
    results_written: int = 0
    passes: int = 0
    warns: int = 0
    fails: int = 0
    not_applicable: int = 0
    check_errors: int = 0
    findings_opened: int = 0
    findings_refreshed: int = 0
    # A resolved condition detected again — the SAME finding row comes back
    # (`reconcile_findings`), so this is counted apart from a first detection.
    findings_reopened: int = 0
    findings_resolved: int = 0
    truncated: bool = False
    items_evaluated: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    # Seconds spent per named phase (evidence loaders, checks, writes) — filled
    # as each phase completes so a progress stream names the hot spot itself.
    # Added after a 100× regression hid for two days because nothing measured
    # where an 11-minute run's time went.
    timings: dict[str, float] = Field(default_factory=dict)


class AnalysisProgressEvent(BaseModel):
    event_type: Literal["analysis_progress"] = "analysis_progress"
    site_id: str
    session_id: str
    status: Literal["started", "progress", "ok", "failed"]
    message: str
    summary: AnalysisSummary
    ts: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class SiteInitializationProgressEvent(BaseModel):
    event_type: Literal["site_initialization_progress"] = "site_initialization_progress"
    site_id: str
    session_id: str
    step: InitializationStep
    status: InitializationStepStatus
    message: str
    summary: SiteInitializationSummary
    ts: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class CrawlStartRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    max_pages: int = Field(default=500, ge=1, le=50_000)
    max_depth: int | None = Field(default=None, ge=0, le=100)
    concurrency: int = Field(default=8, ge=1, le=32)
    follow_subdomains: bool = False
    # These crawls are authorized first-party crawls. The switch remains
    # explicit, but the product default intentionally ignores robots.txt.
    respect_robots: bool = False
    seed_from_sitemap: bool = True
    include_patterns: list[str] = Field(default_factory=list, max_length=100)
    exclude_patterns: list[str] = Field(default_factory=list, max_length=100)
    politeness_delay_ms: int = Field(default=0, ge=0, le=60_000)
    render_mode: str = RENDER_HTTP_FIRST
    capture_screenshots: bool = True
    screenshot_kinds: list[ScreenshotKind] = Field(default_factory=list, max_length=8)
    seed_urls: list[str] = Field(default_factory=list, max_length=50_000)
    list_mode: bool = False
    # THE MAXIMUM this crawl may ever reach against the host — NOT the rate it
    # opens at. Arman, 2026-08-20: "we should never hammer them first and then
    # just see what happens. We should start low and then keep going up."
    #
    # The crawl opens at whatever the host's pacing plan resolves (a platform's
    # published limit, a robots.txt Crawl-delay, what the last crawl of this
    # site discovered, or the floor) and climbs toward this number as the host
    # keeps answering cleanly. It is a CEILING in both directions: a lower value
    # holds the crawl down, and a higher one is reported back as reduced rather
    # than silently applied (`crawl_pacing` events, `user_max_reduced`) — a
    # silently-clamped setting is a defect.
    host_rps: float = Field(default=4.0, gt=0, le=100)
    host_burst: float = Field(default=8.0, gt=0, le=200)
    # Per-crawl User-Agent override, applied identically to BOTH fetch paths
    # (HTTP and browser) and to robots.txt / sitemap discovery.
    #
    # `None` — the default — means "no override": every transport sends exactly
    # what it sends today, so an omitted field is byte-identical to the
    # pre-override behaviour. An empty or whitespace-only string normalizes to
    # `None` as well; it NEVER becomes an empty `User-Agent:` header.
    #
    # These are authorized first-party crawls of sites we control (which is why
    # `respect_robots` defaults to false). The override exists to identify our
    # crawler honestly in the customer's logs, to reproduce what a specific bot
    # or device sees, and to satisfy a customer's own WAF rule — not to evade
    # anyone. Named presets live in `matrx_scraper.user_agents`.
    user_agent: str | None = Field(default=None, max_length=MAX_USER_AGENT_LENGTH)

    @field_validator("user_agent")
    @classmethod
    def validate_user_agent(cls, value: str | None) -> str | None:
        """One gate, shared with every transport — see `user_agents.py`.

        A UA the request accepts but a transport refuses would fail per-URL,
        mid-crawl, deep inside httpx or Playwright. It is a 422 here instead.
        """
        try:
            return normalize_user_agent(value)
        except InvalidUserAgentError as exc:
            raise ValueError(str(exc)) from None

    @field_validator("include_patterns", "exclude_patterns")
    @classmethod
    def validate_regex_patterns(cls, value: list[str]) -> list[str]:
        """Every pattern must compile — an invalid regex is a 422 at the
        request boundary, never a silently skipped filter. A skipped
        include/exclude pattern WIDENS a constrained crawl (the crawler's
        defensive skip logged a warning nobody reads and crawled pages the
        caller explicitly tried to fence off)."""
        for pattern in value:
            try:
                re.compile(pattern)
            except re.error as exc:
                raise ValueError(f"invalid regex pattern {pattern!r}: {exc}") from exc
        return value

    @field_validator("render_mode")
    @classmethod
    def validate_render_mode(cls, value: str) -> str:
        if value not in VALID_RENDER_MODES:
            raise ValueError(f"render_mode must be one of {sorted(VALID_RENDER_MODES)}")
        return value

    @field_validator("screenshot_kinds")
    @classmethod
    def validate_screenshot_kinds(cls, value: list[ScreenshotKind]) -> list[ScreenshotKind]:
        if len(value) != len(set(value)):
            raise ValueError("screenshot_kinds must be unique")
        return value

    def coverage_qualified(self) -> bool:
        return (
            not self.list_mode
            and self.max_depth is None
            and not self.include_patterns
            and not self.exclude_patterns
        )


class UserAgentPresetRecord(BaseModel):
    """One named UA choice as a client renders it.

    The person configuring a crawl is a Subject Matter Expert, not a browser
    engineer — they pick "Googlebot", never a 90-character `Mozilla/5.0 …`
    string. A UI renders THIS list as the primary control and keeps the raw
    text box as the escape hatch. Served rather than hard-coded client-side so
    the label a user reads and the value the API accepts can never drift.
    """

    key: str
    label: str
    description: str
    # `None` on the "Default" preset — meaning "do not override", which is a
    # real choice and NOT the same as sending our own bot UA.
    value: str | None = None


class UserAgentPresetsResponse(BaseModel):
    presets: list[UserAgentPresetRecord]
    max_length: int = MAX_USER_AGENT_LENGTH


class PageFetchRequest(BaseModel):
    """Direct on-demand capture of ONE canonical page (or brand-new URL).

    The URL must belong to the site's canonical host (www/apex equivalent).
    This is the "get the most updated version of this page right now" command
    — it reuses the single-URL capture pipeline (snapshot, head_tags,
    seo_metrics, screenshot) without any crawl discovery/scope machinery.
    """

    model_config = ConfigDict(extra="forbid")

    url: str = Field(min_length=1, max_length=4_000)
    capture_screenshot: bool = True


class CrawlCancelResponse(BaseModel):
    session_id: str
    accepted: bool = True
    action: Literal["cancel"] = "cancel"


# ---------------------------------------------------------------------------
# Crawl presets — a saved, named CrawlStartRequest for one site.
#
# The preset config IS a `CrawlStartRequest`; there is no parallel "preset
# config" shape to drift out of sync. A stored config that no longer validates
# is surfaced as `config_error`, never silently coerced — the whole point of a
# preset is that the user gets back exactly the crawl they saved.


class CrawlPresetSaveRequest(BaseModel):
    """Create-or-replace a preset by ``(site, name)``.

    Save is an upsert on the name because that is what the UI does: the user
    edits the knobs, types the same name, and expects the preset to change.
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2_000)
    config: CrawlStartRequest

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("name must not be blank")
        return cleaned


class CrawlPresetRecord(BaseModel):
    """One stored preset as the browser sees it."""

    id: str
    site_id: str
    name: str
    description: str | None = None
    config: CrawlStartRequest | None = None
    # Set when the stored jsonb no longer validates against CrawlStartRequest
    # (a field was renamed/removed after the preset was saved). `config` is
    # None in that case and the raw payload is preserved for repair.
    config_error: str | None = None
    raw_config: dict[str, Any] | None = None
    last_used_at: datetime | None = None
    use_count: int = 0
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CrawlPresetListResponse(BaseModel):
    """Presets for one site, most-recently-used first (never-used last)."""

    site_id: str
    presets: list[CrawlPresetRecord]
    count: int
    default_preset_id: str | None = None


class CrawlPresetDeleteResponse(BaseModel):
    preset_id: str
    deleted: bool = True


# ---------------------------------------------------------------------------
# One-click rescrape


RecrawlConfigSource = Literal["preset", "site_default_preset", "last_session", "defaults"]


class RecrawlRequest(BaseModel):
    """Body for the one-click rescrape command.

    Everything is optional — that is the point. With an empty body the server
    derives the site's own crawl config; `preset_id` pins an explicit one.
    """

    model_config = ConfigDict(extra="forbid")

    preset_id: str | None = None


class RecrawlConfigResponse(BaseModel):
    """What a rescrape WOULD run, and where the config came from.

    Returned by the preview endpoint so a one-click button can tell the user
    what it is about to do instead of asking them to trust it.
    """

    site_id: str
    source: RecrawlConfigSource
    preset_id: str | None = None
    preset_name: str | None = None
    session_id: str | None = None
    config: CrawlStartRequest


# ---------------------------------------------------------------------------
# Derived read shapes (web_crawl/insights.py)
#
# 🚨 Every one of these carries its cap AND what the cap dropped. A capped
# aggregate that reports only the rows it kept reads as "this is everything" —
# which is how a UI silently shows 1,000 of 610,000 link edges and nobody
# notices. `*_total` / `*_returned` / `*_omitted` are a CONTRACT, not decor.


class DuplicatePage(BaseModel):
    page_id: str
    url: str
    title: str | None = None
    word_count: int | None = None


class DuplicateCluster(BaseModel):
    """One set of pages whose visible text is byte-identical.

    ``fingerprint_version`` is part of the identity: two pages only cluster
    when the SAME extractor generation produced both hashes, so a re-crawl
    under a newer fingerprint never silently merges with stale evidence.
    """

    fingerprint_version: int
    exact_sha256: str
    page_count: int
    pages_omitted: int = 0
    pages: list[DuplicatePage] = Field(default_factory=list)


class DuplicateClusterReport(BaseModel):
    site_id: str
    pages_compared: int = 0
    pages_without_fingerprint: int = 0
    clusters_total: int = 0
    clusters_returned: int = 0
    clusters_omitted: int = 0
    duplicate_pages_total: int = 0
    max_clusters: int = 0
    max_pages_per_cluster: int = 0
    scan_truncated: bool = False
    clusters: list[DuplicateCluster] = Field(default_factory=list)


class LinkGraphNode(BaseModel):
    """A page in the site's current internal link graph.

    ``link_score`` (0..100 internal PageRank, ``web_crawl/link_score.py``) is
    the render size signal and the primary ranking key. It is NULL until a
    COMPLETED full crawl has been scored, so ``inbound_internal_links`` — the
    node's in-degree across the WHOLE site graph, not just the returned
    subgraph — is the fallback rank and the tiebreaker.
    """

    page_id: str
    url: str
    link_score: float | None = None
    inbound_internal_links: int = 0
    outbound_internal_links: int = 0
    http_status: int | None = None
    status: str


class LinkGraphEdge(BaseModel):
    source: str
    target: str
    link_count: int = 1


class LinkGraph(BaseModel):
    site_id: str
    # Which key actually decided who survived `max_nodes` — `link_score` once
    # the site has been scored, `inbound_internal_links` before that. The client
    # sizes nodes by whichever this names; it must never guess.
    ranking: Literal["link_score", "inbound_internal_links"] = "inbound_internal_links"
    nodes_with_link_score: int = 0
    nodes_total: int = 0
    nodes_returned: int = 0
    nodes_omitted: int = 0
    edges_total: int = 0
    edges_returned: int = 0
    edges_omitted: int = 0
    max_nodes: int = 0
    max_edges: int = 0
    scan_truncated: bool = False
    nodes: list[LinkGraphNode] = Field(default_factory=list)
    edges: list[LinkGraphEdge] = Field(default_factory=list)


class ProgressPoint(BaseModel):
    """One sampled `crawl_progress` event.

    ``pages_per_second`` is the average over the interval since the PREVIOUS
    RETURNED point, so a downsampled series still charts honest throughput
    (each plotted value describes exactly the span it is plotted across).
    """

    occurred_at: datetime
    sequence: int
    elapsed_ms: int = 0
    pages_discovered: int = 0
    pages_fetched: int = 0
    pages_failed: int = 0
    pages_in_flight: int = 0
    queue_depth: int = 0
    bytes_downloaded: int = 0
    pages_per_second: float | None = None


class ProgressSeries(BaseModel):
    session_id: str
    points_total: int = 0
    points_returned: int = 0
    points_omitted: int = 0
    max_points: int = 0
    sample_stride: int = 1
    scan_truncated: bool = False
    points: list[ProgressPoint] = Field(default_factory=list)


# ── Run-over-run diff (web_crawl/diff.py) ────────────────────────────────


class CrawlSessionRef(BaseModel):
    """Identity of one crawl session inside a diff response.

    ``pages`` is the number of canonical pages that session actually fetched
    (after alias flattening) — a diff must describe the set it COMPARED.
    ``pages_fetched`` / ``pages_failed`` are the run's own self-reported
    `stats`, carried so a history table renders from one call the way the
    legacy `list_site_diffs` did. The two can legitimately disagree: `pages`
    counts distinct canonical pages, `pages_fetched` counts fetches.
    """

    session_id: str
    site_id: str
    status: str
    mode: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    pages: int | None = None
    pages_fetched: int | None = None
    pages_failed: int | None = None


class DiffPageRef(BaseModel):
    """A page that appeared, disappeared, or came back."""

    page_id: str
    url: str
    http_status: int | None = None


class ChangedPage(BaseModel):
    """A page present in both runs whose observed state differs.

    ``changed_fields`` names exactly which of the five compared fields moved,
    so a renderer never has to diff the before/after pairs itself.
    """

    page_id: str
    url: str
    changed_fields: list[str] = Field(default_factory=list)
    http_status_before: int | None = None
    http_status_after: int | None = None
    title_before: str | None = None
    title_after: str | None = None
    meta_description_before: str | None = None
    meta_description_after: str | None = None
    content_hash_before: str | None = None
    content_hash_after: str | None = None
    word_count_before: int | None = None
    word_count_after: int | None = None


class CrawlDiffCounts(BaseModel):
    """Complete counts — never truncated, even when the arrays are.

    ``pages_returned`` is a SUBSET of ``pages_added``: a URL missing from the
    base run that the site had already seen before it — always 0 when there is
    no base run. ``pages_status_worse`` / ``pages_status_better`` are subsets
    of ``pages_changed``.
    """

    pages_added: int = 0
    pages_removed: int = 0
    pages_returned: int = 0
    pages_changed: int = 0
    pages_unchanged: int = 0
    pages_status_worse: int = 0
    pages_status_better: int = 0


class CrawlDiff(BaseModel):
    """Page-level comparison of ``compare`` against ``base``.

    ``base`` is null when the compared session is the site's first crawl — the
    counts then report every page as added, which is the truth, not an error.
    ``truncated`` means at least one array was capped or a session exceeded the
    per-session scan ceiling; the counts stay complete either way.
    """

    site_id: str
    base: CrawlSessionRef | None = None
    compare: CrawlSessionRef
    counts: CrawlDiffCounts
    added: list[DiffPageRef] = Field(default_factory=list)
    removed: list[DiffPageRef] = Field(default_factory=list)
    returned: list[DiffPageRef] = Field(default_factory=list)
    changed: list[ChangedPage] = Field(default_factory=list)
    truncated: bool = False
    computed_at: datetime


class SiteDiffSummary(BaseModel):
    """Counts-only diff of one session against its predecessor."""

    site_id: str
    session: CrawlSessionRef
    previous_session: CrawlSessionRef | None = None
    counts: CrawlDiffCounts
    truncated: bool = False
    computed_at: datetime


class SiteDiffList(BaseModel):
    site_id: str
    diffs: list[SiteDiffSummary] = Field(default_factory=list)


class PreviousSessionResponse(BaseModel):
    """The baseline a session's 'what changed' widget should diff against.

    ``previous`` is null when this is the site's first site-wide crawl.
    """

    session_id: str
    site_id: str
    previous: CrawlSessionRef | None = None


class TrafficAtRiskPage(BaseModel):
    """One URL Google is showing that our own fetch could not load."""

    page_id: str
    url: str
    http_status: int
    content_type: str | None = None
    impressions: int = 0
    clicks: int = 0
    in_sitemap: bool = False
    #: How we learned the status — 'crawl' (a full capture) or 'verification'
    #: (the cheap header-only sweep). A user asking "are you sure?" deserves the
    #: honest answer, and the two are not equally strong evidence.
    evidence_source: str = "crawl"
    last_seen: datetime | None = None


class TrafficAtRiskReport(BaseModel):
    """Pages with Google impressions whose last recorded status was not a
    success — ranked by the traffic actually at stake.

    Derived entirely from canonical evidence (`web.page.http_status_last` +
    `web.gsc_page_stat`); no table backs it and none may.
    """

    site_id: str
    pages_with_impressions: int = 0
    pages_at_risk_total: int = 0
    pages_returned: int = 0
    pages_omitted: int = 0
    impressions_at_risk: int = 0
    clicks_at_risk: int = 0
    #: Impression-weighted share of Google-visible traffic sitting on a URL we
    #: cannot load. This is the number that makes the finding actionable.
    share_of_impressions_at_risk: float = 0.0
    unverified_with_impressions: int = 0
    #: Pages whose last recorded status was 429 — a fact about OUR request rate,
    #: not about the URL. Never counted as at-risk, never silently dropped.
    throttled_not_assessed: int = 0
    max_pages: int = 0
    scan_truncated: bool = False
    pages: list[TrafficAtRiskPage] = Field(default_factory=list)


__all__ = [
    "ChangedPage",
    "CrawlDiff",
    "CrawlDiffCounts",
    "CrawlSessionRef",
    "DiffPageRef",
    "PreviousSessionResponse",
    "SiteDiffList",
    "SiteDiffSummary",
    "AnalysisProgressEvent",
    "AnalysisSummary",
    "CrawlCancelResponse",
    "CrawlPresetDeleteResponse",
    "CrawlPresetListResponse",
    "CrawlPresetRecord",
    "CrawlPresetSaveRequest",
    "CrawlStartRequest",
    "DuplicateCluster",
    "DuplicateClusterReport",
    "DuplicatePage",
    "LinkGraph",
    "LinkGraphEdge",
    "LinkGraphNode",
    "PageFetchRequest",
    "ProgressPoint",
    "ProgressSeries",
    "RecrawlConfigResponse",
    "RecrawlConfigSource",
    "RecrawlRequest",
    "GscSyncProgressEvent",
    "GscSyncSummary",
    "INITIALIZATION_SCREENSHOT_KINDS",
    "InitializeStepEvent",
    "InitializeStepName",
    "InitializeStepStatus",
    "LinkCheckProgressEvent",
    "LinkCheckSummary",
    "LinkResolutionProgressEvent",
    "LinkResolutionSummary",
    "InitializationError",
    "InitializationStep",
    "InitializationStepStatus",
    "ScreenshotKind",
    "SiteInitializationProgressEvent",
    "SiteInitializationSummary",
    "SitemapSyncProgressEvent",
    "SitemapSyncSummary",
    "UrlReconciliationProgressEvent",
    "TrafficAtRiskPage",
    "TrafficAtRiskReport",
    "UrlReconciliationSummary",
]
