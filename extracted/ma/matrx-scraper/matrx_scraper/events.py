"""Typed crawl-progress events.

These are Pydantic models intentionally defined inside matrx-scraper so the
package stays standalone — the host (aidream) wraps them and forwards to the
matrx-connect Emitter via send_data(). The shape is the wire contract between
the crawler and any frontend consuming the JSONL stream.

Every event carries `event_type` so the FE reducer can discriminate without
having to inspect every field.
"""

from __future__ import annotations

from datetime import datetime, UTC
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


def _utcnow() -> str:
    return datetime.now(UTC).isoformat()


CrawlEventType = Literal[
    "crawl_session_created",
    "crawl_started",
    "page_discovered",
    "url_classified",
    "urls_classified",
    "page_fetched",
    "page_captured",
    "page_parsed",
    "page_failed",
    "crawl_progress",
    "issue_detected",
    "crawl_completed",
    "crawl_warning",
    "crawl_pacing",
]


class _BaseCrawlEvent(BaseModel):
    model_config = ConfigDict(extra="ignore")

    event_type: CrawlEventType
    run_id: str
    # ``session_id`` is the canonical web.crawl_session identifier. ``run_id``
    # remains on the wire for compatibility with the existing crawler engine,
    # but direct crawler transports always make the two values identical.
    session_id: str | None = None
    site_id: str | None = None
    sequence: int | None = Field(default=None, ge=1)
    ts: str = Field(default_factory=_utcnow)

    @model_validator(mode="after")
    def _canonicalize_session_id(self) -> _BaseCrawlEvent:
        if self.session_id is None:
            self.session_id = self.run_id
        elif self.session_id != self.run_id:
            raise ValueError("run_id and session_id must identify the same crawl session")
        return self


class CrawlSessionCreatedEvent(_BaseCrawlEvent):
    event_type: Literal["crawl_session_created"] = "crawl_session_created"
    status: Literal["queued"] = "queued"


class CrawlStartedEvent(_BaseCrawlEvent):
    event_type: Literal["crawl_started"] = "crawl_started"
    base_url: str
    config: dict[str, Any] = Field(default_factory=dict)
    seeded_from_sitemap: int = 0
    initial_queue_depth: int = 1


class CrawlPageDiscoveredEvent(_BaseCrawlEvent):
    event_type: Literal["page_discovered"] = "page_discovered"
    url: str
    depth: int
    parent_url: str | None = None
    source: Literal["seed", "sitemap", "link"] = "link"


class CrawlUrlClassifiedEvent(_BaseCrawlEvent):
    event_type: Literal["url_classified"] = "url_classified"
    raw_url: str
    normalized_url: str | None = None
    depth: int = 0
    parent_url: str | None = None
    source: Literal["seed", "sitemap", "link"] = "link"
    classification: Literal["internal", "external", "asset", "invalid", "excluded"]
    outcome: Literal["skipped", "excluded", "duplicate"]
    is_in_scope: bool = False
    reason_code: str
    reason: str | None = None


class UrlDecision(BaseModel):
    """One URL's scope decision — the durable `crawl_url` ledger row shape."""

    raw_url: str
    normalized_url: str | None = None
    depth: int = 0
    source: Literal["seed", "sitemap", "link"] = "link"
    classification: Literal["internal", "external", "asset", "invalid", "excluded"]
    outcome: Literal["skipped", "excluded", "duplicate", "accepted"]
    is_in_scope: bool = False
    reason_code: str
    reason: str | None = None


class CrawlUrlsClassifiedEvent(_BaseCrawlEvent):
    """Every scope decision made while processing ONE page, as ONE event.

    THE INVARIANT: a page emits O(1) events, never O(links). Emitting one
    event per discovered link put ~170 events on the wire per page, each one
    taking a full DB transaction under the event sink's global ordering lock —
    which made crawl throughput a function of link count rather than page
    count. Never reintroduce a per-link event.

    `decisions` carries the full ledger for persistence; `for_wire()` strips it
    because the UI only ever needs the counts.
    """

    event_type: Literal["urls_classified"] = "urls_classified"
    parent_url: str | None = None
    depth: int = 0
    source: Literal["seed", "sitemap", "link"] = "link"
    total: int = 0
    accepted: int = 0
    by_reason: dict[str, int] = Field(default_factory=dict)
    decisions: list[UrlDecision] = Field(default_factory=list)

    def for_wire(self) -> CrawlUrlsClassifiedEvent:
        return self.model_copy(update={"decisions": []})


class CrawlPageCapturedEvent(_BaseCrawlEvent):
    """A visual capture landed — carries the file_id the client renders.

    Only `file_id` goes on the wire; the client resolves it through the files
    layer (which owns signing, caching, and re-minting). Never put a signed URL
    or a storage_uri on this event.
    """

    event_type: Literal["page_captured"] = "page_captured"
    url: str
    final_url: str | None = None
    page_id: str | None = None
    kind: str
    file_id: str
    width: int
    height: int
    bytes: int = 0
    # Page basics the capture row renders alongside the image, so the UI needs
    # no second fetch to show a useful row.
    title: str | None = None
    http_status: int | None = None
    capture_reason: Literal["new", "changed", "stale", "forced"] = "new"


class CrawlPageFetchedEvent(_BaseCrawlEvent):
    event_type: Literal["page_fetched"] = "page_fetched"
    url: str
    final_url: str
    http_status: int
    response_time_ms: int
    bytes: int
    mime_type: str | None = None
    redirected: bool = False
    # Full hop chain — list of {status, url}, oldest first, final URL last.
    # Same shape as PageSummary.redirect_chain; carried here so FAILED urls
    # (e.g. redirect-to-404) keep their hop evidence in web.crawl_url too.
    redirect_chain: list[dict[str, Any]] = Field(default_factory=list)


class HeadingEntry(BaseModel):
    level: int  # 1..6
    text: str


class HreflangEntry(BaseModel):
    lang: str
    href: str


class LinkEntry(BaseModel):
    target_url: str
    anchor_text: str = ""
    rel: str | None = None
    link_type: Literal["internal", "external", "subdomain"] = "external"
    nofollow: bool = False


class PageSummary(BaseModel):
    """Summary emitted on `page_parsed`.

    Carries the full SEO signal set so the host can persist it without
    re-parsing. Mirrors the chrome-extension SEO audit shape (audit.ts) so
    a single page row in the DB matches what the side-panel audit shows.

    The full row is written to the database out-of-band; this is also what
    the live UI needs to render a row in the Screaming-Frog-style grid.
    """

    url: str
    final_url: str | None = None
    http_status: int | None = None
    mime_type: str | None = None

    # Core SEO
    title: str | None = None
    meta_description: str | None = None
    meta_robots: str | None = None
    canonical_url: str | None = None
    lang: str | None = None

    # Headings — kept as both the typed list and a count for fast filters
    h1: list[str] = Field(default_factory=list)
    h2: list[str] = Field(default_factory=list)
    h1_count: int = 0
    headings_full: list[HeadingEntry] = Field(default_factory=list)

    # Multilingual variants
    hreflang: list[HreflangEntry] = Field(default_factory=list)

    # The two head metas that are neither SEO text nor transport:
    # {"viewport": str | None, "refresh": str | None}. None (not {}) when the
    # capture had no HTML to read them from — the checks answer n_a for that,
    # instead of reporting a tag as missing on a page nobody parsed.
    head_meta: dict[str, Any] | None = None

    # Social cards + structured data
    og_tags: dict[str, Any] = Field(default_factory=dict)
    twitter_tags: dict[str, Any] = Field(default_factory=dict)
    schema_org: dict[str, Any] = Field(default_factory=dict)
    schema_types: list[str] = Field(default_factory=list)
    structured_data: dict[str, Any] = Field(default_factory=dict)
    page_identity: dict[str, Any] = Field(default_factory=dict)

    # Body stats
    word_count: int | None = None
    sentence_count: int | None = None
    flesch_reading_ease: float | None = None
    # UTF-8 byte length of the SAME visible text `word_count` counts — the
    # numerator of `text_html_ratio` (its denominator is `bytes`, the raw HTML).
    text_bytes: int | None = None
    text_hash: str | None = None
    # Versioned duplicate-detection fingerprint over the same text as
    # word_count — {version, exact_sha256, simhash64, shingle_size,
    # token_count} from parser/hashing.compute_text_fingerprint.
    content_fingerprint: dict[str, Any] | None = None

    # Link / image counts (full graph in crawl_links)
    internal_links: int = 0
    external_links: int = 0
    link_count: int = 0
    images_count: int = 0
    images_missing_alt: int = 0
    image_inventory: list[dict[str, Any]] = Field(default_factory=list)
    resources: dict[str, Any] = Field(default_factory=dict)

    # Full link rows — anchor text + rel + type. Persisted to crawl_links.
    links: list[LinkEntry] = Field(default_factory=list)
    # http:// resources loaded on https:// page (security audit).
    mixed_content: list[str] = Field(default_factory=list)
    # Security-relevant response headers only, lower-cased — the allowlist in
    # `seo_audit.SECURITY_RESPONSE_HEADERS` (HSTS, CSP, X-Frame-Options, …).
    # NEVER the full header set: it carries `set-cookie` and credential echoes
    # that must not be persisted. `None` = the fetch recorded no headers at all
    # (cached rebuild), which the security checks answer `n_a` for.
    response_headers: dict[str, str] | None = None
    # Redirect chain — list of {status, url} hops. Length 1 = no redirect.
    redirect_chain: list[dict[str, Any]] = Field(default_factory=list)
    # Pagination — {prev, next} captured from rel="prev"/"next" link tags.
    pagination: dict[str, Any] = Field(default_factory=dict)

    # Response info
    # Total elapsed around the fetch — server think time PLUS body download.
    response_time_ms: int | None = None
    # TRUE time to first byte from the transport, redirect hops included, and
    # the ONLY input the `ttfb_server_response` check grades. None = the
    # transport could not measure it (the browser path); consumers answer
    # "not measured" rather than reaching for `response_time_ms`.
    ttfb_ms: int | None = None
    bytes: int | None = None
    depth: int = 0
    page_id: str | None = None  # filled by host after DB insert; None in standalone mode
    snapshot_id: str | None = None  # canonical web.snapshot captured for this page


class CrawlPageParsedEvent(_BaseCrawlEvent):
    event_type: Literal["page_parsed"] = "page_parsed"
    page: PageSummary


class CrawlPageFailedEvent(_BaseCrawlEvent):
    event_type: Literal["page_failed"] = "page_failed"
    url: str
    error_class: str
    error_message: str
    attempt: int = 1
    will_retry: bool = False


class CrawlProgressEvent(_BaseCrawlEvent):
    event_type: Literal["crawl_progress"] = "crawl_progress"
    pages_discovered: int
    pages_fetched: int
    pages_failed: int
    pages_in_flight: int
    queue_depth: int
    bytes_downloaded: int = 0
    elapsed_ms: int = 0


class CrawlIssueDetectedEvent(_BaseCrawlEvent):
    event_type: Literal["issue_detected"] = "issue_detected"
    issue_type: str  # broken_link | redirect_chain | missing_title | …
    severity: Literal["critical", "warning", "info"] = "warning"
    page_url: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class CrawlPacingEvent(_BaseCrawlEvent):
    """How fast we are crawling this host right now, and WHY.

    Arman's crawler vision point 8: a silently-clamped setting is a defect. This
    event is the un-silencing — it fires when the plan is first resolved, on
    every ramp step, and on every back-off, so the live UI can show the rate
    moving and name the rule that set the ceiling.
    """

    event_type: Literal["crawl_pacing"] = "crawl_pacing"
    host: str
    current_rps: float
    ceiling_rps: float
    #: Set only once the host has ACTUALLY pushed back. None means "not yet
    #: found", never "unlimited".
    discovered_ceiling_rps: float | None = None
    source: str = "floor"
    platform: str | None = None
    platform_display: str | None = None
    fronted_by: str | None = None
    crawl_delay_seconds: float | None = None
    #: True when the user asked for more than this host is being held to. The UI
    #: must show the real number and this flag, never the requested one alone.
    user_max_reduced: bool = False
    limit_hits: int = 0
    notes: list[str] = Field(default_factory=list)
    reason: str = "plan_resolved"


class CrawlWarningEvent(_BaseCrawlEvent):
    event_type: Literal["crawl_warning"] = "crawl_warning"
    message: str
    context: dict[str, Any] = Field(default_factory=dict)


class CrawlCompletedEvent(_BaseCrawlEvent):
    event_type: Literal["crawl_completed"] = "crawl_completed"
    pages_discovered: int = 0
    pages_fetched: int
    pages_failed: int
    issues_count: int
    duration_ms: int
    bytes_downloaded: int = 0
    status: Literal["completed", "canceled", "failed"] = "completed"
    error_message: str | None = None
    # Static request scope is not enough to authorize negative reconciliation.
    # The run must also prove at runtime that it drained discovery without a
    # cap, cancellation, or failed fetch that could hide downstream pages.
    coverage_complete: bool = False
    limit_reached: bool = False
    remaining_queue_depth: int = Field(default=0, ge=0)


CrawlEvent = (
    CrawlSessionCreatedEvent
    | CrawlStartedEvent
    | CrawlPageDiscoveredEvent
    | CrawlUrlClassifiedEvent
    | CrawlUrlsClassifiedEvent
    | CrawlPageFetchedEvent
    | CrawlPageCapturedEvent
    | CrawlPageParsedEvent
    | CrawlPageFailedEvent
    | CrawlProgressEvent
    | CrawlIssueDetectedEvent
    | CrawlWarningEvent
    | CrawlCompletedEvent
)


__all__ = [
    "CrawlEvent",
    "CrawlEventType",
    "CrawlSessionCreatedEvent",
    "CrawlStartedEvent",
    "CrawlPageDiscoveredEvent",
    "CrawlUrlClassifiedEvent",
    "CrawlUrlsClassifiedEvent",
    "CrawlPageFetchedEvent",
    "CrawlPageCapturedEvent",
    "CrawlPageParsedEvent",
    "UrlDecision",
    "CrawlPageFailedEvent",
    "CrawlProgressEvent",
    "CrawlIssueDetectedEvent",
    "CrawlWarningEvent",
    "CrawlCompletedEvent",
    "PageSummary",
    "HeadingEntry",
    "HreflangEntry",
    "LinkEntry",
]
