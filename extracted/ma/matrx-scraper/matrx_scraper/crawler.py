"""Site crawler — async BFS over an entire website with typed progress events.

This is the platform crawler used by the aidream Scraper Admin (Screaming-Frog-
class crawls up to ~50,000 pages). Standalone-friendly: works with default
in-memory queue + no event sink, and degrades gracefully when robots.txt /
sitemap discovery fails.

Capabilities (per scope):
  * Async BFS with concurrency, max_pages, max_depth, follow_subdomains.
  * robots.txt parsing (urllib.robotparser, cached per host).
  * sitemap.xml + sitemap_index.xml seeding.
  * include / exclude path patterns (regex).
  * Render modes: http_only | http_first | browser_always | browser_with_screenshot.
  * Per-page error reporting (no silent except). Failures emit a typed event.
  * Pluggable QueueBackend (default in-memory; host swaps in Postgres-backed).
  * Pluggable CrawlEventSink (default no-op; host wires it to the streaming Emitter).
  * Optional body-persistence callback so the host can store HTML/markdown in S3.
  * Optional screenshot-capture callback so the host can persist screenshots.
"""

from __future__ import annotations

import asyncio
import ipaddress
import logging
import re
import time
import xml.etree.ElementTree as ET
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any, Protocol
from urllib import robotparser
from urllib.parse import urljoin, urlparse

import httpx
import tldextract

from matrx_scraper.events import (
    CrawlCompletedEvent,
    CrawlEvent,
    CrawlPageDiscoveredEvent,
    CrawlUrlClassifiedEvent,
    CrawlUrlsClassifiedEvent,
    CrawlPageFailedEvent,
    CrawlPageFetchedEvent,
    CrawlPageParsedEvent,
    CrawlPacingEvent,
    CrawlProgressEvent,
    CrawlStartedEvent,
    CrawlWarningEvent,
    HeadingEntry,
    HreflangEntry,
    LinkEntry,
    PageSummary,
    UrlDecision,
)
from matrx_scraper.image_evidence import enrich_image_inventory
from matrx_scraper.orchestrator import (
    ScrapeResult,
    _build_result_from_response,  # internal — also used here for browser_with_screenshot path
    scrape,
)
from matrx_scraper.queue_backend import (
    InMemoryQueueBackend,
    QueueBackend,
    QueueItem,
)
from matrx_scraper.parser.hashing import compute_text_fingerprint
from matrx_scraper.host_pacing import (
    DEFAULT_KNOBS,
    HostPacingPlan,
    HostRamp,
    PacingKnobs,
    RememberedPacing,
    resolve_plan,
)
from matrx_scraper.host_platform import detect_platform
from matrx_scraper.robots_txt import parse_robots_txt
from matrx_scraper.rate_limiter import HostRateLimiter, host_key
from matrx_scraper.recipes import RecipeBackend
from matrx_scraper.sampling import StableHashSampler, stable_hash_sample
from matrx_scraper.scraper import (
    ContentType,
    FailureReason,
    RequestType,
    Response,
    detect_challenge_reasons,
    detect_content_type_from_url,
    detect_response_content_type,
    get_required_random_proxy,
    primary_failure_reason,
)
from matrx_scraper.seo_audit import IMAGE_INVENTORY_LIMIT, audit_html
from matrx_scraper.user_agents import normalize_user_agent
from matrx_scraper.utils.url import normalize_url, validate_public_http_url

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Public protocols (host-injected)
# ---------------------------------------------------------------------------


class CrawlEventSink(Protocol):
    """Async sink for typed crawl events. Default is no-op."""

    async def emit(self, event: CrawlEvent) -> None: ...


class _NoopSink:
    async def emit(self, event: CrawlEvent) -> None:  # noqa: ARG002
        return None


# Body persister: receives raw bytes (HTML), returns dict with keys like
# {'body_file_id', 'markdown_file_id'} as the host sees fit. The crawler does
# not assume any particular storage backend.
BodyPersister = Callable[
    ["PersistRequest"],
    Awaitable["PersistResult"],
]


class _CrawlPersistenceErrorInfo:
    error_type = "canonical_crawl_persistence_error"
    user_message = (
        "We could not save one of the captured pages. "
        "Please retry the crawl; if it continues, contact support."
    )


class CrawlPersistenceError(RuntimeError):
    """Safe stream boundary for internal canonical persistence failures."""

    error_info = _CrawlPersistenceErrorInfo()

    def __init__(self) -> None:
        super().__init__(self.error_info.user_message)


@dataclass
class CapturedShot:
    """One screenshot produced during a browser_with_screenshot fetch.

    Mirrors `browser_pool.CapturedScreenshot` but kept here as a plain
    dataclass so the body persister contract doesn't depend on the
    Playwright-only browser_pool module.
    """

    kind: str
    width: int
    height: int
    bytes: bytes


@dataclass
class PersistRequest:
    run_id: str
    url: str
    final_url: str
    body: str | bytes | None
    markdown: str | None
    screenshots: list[CapturedShot] = field(default_factory=list)
    mime_type: str | None = "text/html"
    extractor_results: dict[str, Any] = field(default_factory=dict)
    page_summary: PageSummary | None = None


_BODY_FORMATS: dict[str, tuple[str, str]] = {
    "html": ("html", "text/html"),
    "text/html": ("html", "text/html"),
    "md": ("md", "text/markdown"),
    "text/markdown": ("md", "text/markdown"),
    "json": ("json", "application/json"),
    "application/json": ("json", "application/json"),
    "xml": ("xml", "application/xml"),
    "application/xml": ("xml", "application/xml"),
    "text/xml": ("xml", "text/xml"),
    "txt": ("txt", "text/plain"),
    "text/plain": ("txt", "text/plain"),
    "pdf": ("pdf", "application/pdf"),
    "application/pdf": ("pdf", "application/pdf"),
    "image": ("bin", "application/octet-stream"),
    "image/png": ("png", "image/png"),
    "image/jpeg": ("jpg", "image/jpeg"),
    "image/gif": ("gif", "image/gif"),
    "image/webp": ("webp", "image/webp"),
    "image/svg+xml": ("svg", "image/svg+xml"),
}


def resolve_body_artifact_format(mime_type: str | None) -> tuple[str, str]:
    """Return a safe file extension and canonical MIME for a captured body."""

    normalized = (mime_type or "").split(";", 1)[0].strip().lower()
    return _BODY_FORMATS.get(normalized, ("bin", normalized or "application/octet-stream"))


@dataclass
class PersistResult:
    body_file_id: str | None = None
    markdown_file_id: str | None = None
    screenshot_file_ids: dict[str, str] = field(default_factory=dict)
    page_id: str | None = None
    snapshot_id: str | None = None
    # Non-fatal notices the persister wants surfaced on the session's event
    # stream (e.g. dismissal-memory revives). Each entry: {"message": str,
    # "context": dict}. The crawler emits one CrawlWarningEvent per entry.
    warnings: list[dict[str, Any]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Render modes
# ---------------------------------------------------------------------------


# Kept as plain strings for forward-compatibility — the API surface uses
# Literal-typed Pydantic fields anyway, and string equality keeps the crawler
# itself tiny.
RENDER_HTTP_ONLY = "http_only"
RENDER_HTTP_FIRST = "http_first"
RENDER_BROWSER_ALWAYS = "browser_always"
RENDER_BROWSER_WITH_SCREENSHOT = "browser_with_screenshot"
VALID_RENDER_MODES = {
    RENDER_HTTP_ONLY,
    RENDER_HTTP_FIRST,
    RENDER_BROWSER_ALWAYS,
    RENDER_BROWSER_WITH_SCREENSHOT,
}


# --- Rate-limit response handling (HTTP 429 / 503) -------------------------
# A rate-limited response is the origin saying "slow down", NOT "this page is
# broken". Treating it as a permanent failure (the old behavior) meant that the
# instant a crawl tripped a host's limit, every remaining URL failed too. We
# instead adaptively throttle the host and requeue the URL a bounded number of
# times. These are CODE CONSTANTS (behavior, not per-deployment config) — never
# env vars. Tune here and ship a build; that beats a silent env drift.
RATE_LIMIT_STATUSES = frozenset({429, 503})
MAX_RATE_LIMIT_RETRIES = 5
RATE_LIMIT_THROTTLE_FACTOR = 0.5  # multiply host rps by this on each 429
RATE_LIMIT_MIN_RPS = 0.5  # never throttle a host below this

# The whole pacing probe — robots.txt AND the platform fingerprint, run together
# — gets ONE wall-clock budget, after which the crawl opens at the floor and
# climbs. Deciding how fast to go must never be a visible part of how long a
# crawl takes, and a host that is slow to answer its own root is exactly the
# host we would have opened cautiously against anyway.
PACING_PROBE_BUDGET_SECONDS = 5.0
PACING_PROBE_TIMEOUT_SECONDS = 4.0


# ---------------------------------------------------------------------------
# URL helpers
# ---------------------------------------------------------------------------


def _normalise_url(url: str) -> str:
    return normalize_url(url)


# Offline public-suffix extraction: the bundled PSL snapshot only, NEVER a
# runtime network fetch (suffix_list_urls=() disables tldextract's live
# download). Module-level singleton — instantiation loads the snapshot once.
# include_psl_private_domains: github.io / *.blogspot.com etc. are registries
# too — two project sites there are different owners, not one site.
_TLD_EXTRACTOR = tldextract.TLDExtract(suffix_list_urls=(), include_psl_private_domains=True)


def _registrable_domain(host: str) -> str:
    """The real registrable domain per the Public Suffix List.

    The old "last two labels" heuristic treated every multi-label public
    suffix as one site: evil.co.uk == example.co.uk (both "co.uk"), and any
    two github.io projects matched each other — so follow_subdomains could
    walk a crawl onto a stranger's domain.
    """
    lowered = host.lower()
    extracted = _TLD_EXTRACTOR(lowered)
    if extracted.domain and extracted.suffix:
        return f"{extracted.domain}.{extracted.suffix}"
    # No recognized public suffix — an IP literal is its own identity; a
    # bare/internal/test hostname (e.g. *.example, *.internal) keeps the old
    # last-two-labels heuristic so subdomain matching still works there.
    try:
        ipaddress.ip_address(lowered.strip("[]"))
        return lowered
    except ValueError:
        pass
    parts = lowered.split(".")
    if len(parts) <= 2:
        return lowered
    return ".".join(parts[-2:])


def _is_same_host(url: str, base_host: str, follow_subdomains: bool) -> bool:
    host = urlparse(url).netloc.lower()
    if not host:
        return False
    if host == base_host:
        return True
    # www.<domain> and the apex are UNCONDITIONALLY the same site, in both
    # directions — a site registered as https://example.com whose sitemap
    # serves https://www.example.com/... (or vice versa) must never classify
    # its own URLs as outside_site_scope. Every other subdomain still honors
    # follow_subdomains below.
    if host.removeprefix("www.") == base_host.removeprefix("www."):
        return True
    if follow_subdomains:
        return _registrable_domain(host) == _registrable_domain(base_host)
    return False


def _compile_patterns(patterns: list[str]) -> tuple[list[re.Pattern[str]], list[dict[str, str]]]:
    """Compile include/exclude patterns, returning ``(compiled, invalid)``.

    Invalid patterns should be UNREACHABLE — ``CrawlStartRequest`` rejects
    them with a 422 at the request boundary. This defensive skip stays for
    non-contract callers, but any skip it performs is reported back so the
    crawler can emit a durable ``crawl_warning``: a silently dropped pattern
    WIDENS a constrained crawl.
    """
    compiled: list[re.Pattern[str]] = []
    invalid: list[dict[str, str]] = []
    for p in patterns:
        try:
            compiled.append(re.compile(p))
        except re.error as exc:
            logger.error(
                "invalid crawler pattern reached the crawler (request validation "
                "should have rejected it), skipping: %r (%s)",
                p,
                exc,
            )
            invalid.append({"pattern": p, "error": str(exc)})
    return compiled, invalid


# ---------------------------------------------------------------------------
# robots.txt cache
# ---------------------------------------------------------------------------


class _RobotsCache:
    def __init__(self, user_agent: str, fetch_timeout: float = 10.0) -> None:
        self.user_agent = user_agent
        self.fetch_timeout = fetch_timeout
        self._parsers: dict[str, robotparser.RobotFileParser] = {}
        self._lock = asyncio.Lock()

    async def can_fetch(self, url: str) -> bool:
        parsed = urlparse(url)
        if not parsed.netloc:
            return False
        host_key = f"{parsed.scheme}://{parsed.netloc}"
        rp = await self._get_or_load(host_key)
        if rp is None:
            # robots.txt unreachable — fail-open (matches Googlebot behavior).
            return True
        try:
            return rp.can_fetch(self.user_agent, url)
        except Exception:
            return True

    async def _get_or_load(self, host_key: str) -> robotparser.RobotFileParser | None:
        async with self._lock:
            if host_key in self._parsers:
                return self._parsers[host_key]
        rp = robotparser.RobotFileParser()
        rp.set_url(f"{host_key}/robots.txt")
        try:
            async with httpx.AsyncClient(
                timeout=self.fetch_timeout, follow_redirects=True
            ) as client:
                resp = await client.get(
                    f"{host_key}/robots.txt", headers={"User-Agent": self.user_agent}
                )
                if 200 <= resp.status_code < 300 and resp.text:
                    rp.parse(resp.text.splitlines())
                else:
                    rp = None  # treat as no robots.txt → fail-open
        except Exception as exc:
            logger.info("robots.txt fetch failed for %s: %s", host_key, exc)
            rp = None
        async with self._lock:
            self._parsers[host_key] = rp  # type: ignore[assignment]
        return rp


# ---------------------------------------------------------------------------
# Sitemap discovery
# ---------------------------------------------------------------------------


_SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


async def _discover_sitemap_urls(
    base_url: str,
    *,
    user_agent: str,
    request_timeout: float = 15.0,
    max_urls: int = 50_000,
) -> list[str]:
    """Best-effort sitemap walk with stable, order-independent URL sampling."""
    parsed = urlparse(base_url)
    if not parsed.netloc:
        return []
    candidates = [
        f"{parsed.scheme}://{parsed.netloc}/sitemap.xml",
        f"{parsed.scheme}://{parsed.netloc}/sitemap_index.xml",
    ]

    found = StableHashSampler[str](
        max_urls,
        key=lambda url: url,
        namespace=f"sitemap-urls:{parsed.netloc}",
    )
    seen_sitemaps: set[str] = set()
    max_sitemaps = 200

    async with httpx.AsyncClient(
        timeout=request_timeout,
        follow_redirects=True,
        headers={"User-Agent": user_agent},
    ) as client:
        # Also peek at robots.txt for explicit `Sitemap:` directives.
        try:
            r = await client.get(f"{parsed.scheme}://{parsed.netloc}/robots.txt")
            if 200 <= r.status_code < 300:
                for line in r.text.splitlines():
                    if line.lower().startswith("sitemap:"):
                        candidates.append(line.split(":", 1)[1].strip())
        except Exception:
            pass

        async def _fetch(url: str) -> None:
            if url in seen_sitemaps or len(seen_sitemaps) >= max_sitemaps:
                return
            seen_sitemaps.add(url)
            try:
                resp = await client.get(url)
            except Exception:
                return
            if not (200 <= resp.status_code < 300):
                return
            try:
                root = ET.fromstring(resp.content)
            except ET.ParseError:
                return
            tag = root.tag.lower()
            if tag.endswith("sitemapindex"):
                child_locs = [
                    el.text.strip()
                    for el in root.findall(".//sm:sitemap/sm:loc", _SITEMAP_NS)
                    if el.text
                ]
                for child in stable_hash_sample(
                    child_locs,
                    max_sitemaps,
                    key=lambda child_url: child_url,
                    namespace=f"sitemap-children:{url}",
                ):
                    await _fetch(child)
            elif tag.endswith("urlset"):
                for el in root.findall(".//sm:url/sm:loc", _SITEMAP_NS):
                    if el.text:
                        found.offer(el.text.strip())

        for c in list(candidates):
            await _fetch(c)

    return found.items()


# ---------------------------------------------------------------------------
# SiteCrawler
# ---------------------------------------------------------------------------


@dataclass
class SiteCrawlerConfig:
    base_url: str
    max_pages: int = 200
    max_depth: int | None = None
    concurrency: int = 8
    follow_subdomains: bool = False
    respect_robots: bool = True
    seed_from_sitemap: bool = True
    # The bot identity used for robots.txt matching and sitemap discovery. It
    # has NEVER been the UA of the page fetches themselves (those go through
    # the scraper's rotating browser header profiles / the browser pool's
    # device profiles).
    user_agent: str = "MatrxScraperBot/0.1 (+https://aimatrx.com)"
    # Caller-supplied per-crawl UA override. When set it applies to EVERYTHING
    # this crawl sends — robots.txt, sitemap discovery, HTTP page fetches, and
    # the browser context — so the crawl behaves identically regardless of
    # `render_mode`. `None` (the default) means no override: every request is
    # byte-identical to what it was before this field existed.
    user_agent_override: str | None = None
    include_patterns: list[str] = field(default_factory=list)
    exclude_patterns: list[str] = field(default_factory=list)
    politeness_delay_ms: int = 0
    render_mode: str = RENDER_HTTP_FIRST
    capture_screenshots: bool = False
    browser_navigation_timeout_ms: int = 45_000
    browser_settle_timeout_ms: int = 5_000
    progress_every_n_pages: int = 5
    progress_every_seconds: float = 5.0
    # List mode — when set, the crawler ONLY visits these URLs (no sitemap,
    # no link discovery). Useful for re-auditing a known set or comparing
    # two runs against an identical URL list.
    seed_urls: list[str] = field(default_factory=list)
    list_mode: bool = False
    # Per-host rate limit (steady-state RPS + burst capacity). Distinct from
    # politeness_delay_ms which is a per-worker sleep — these flags are
    # honored across all workers so concurrency=8 against the same host
    # doesn't blow past the cap.
    # THE MAXIMUM, not the opening rate. Arman, 2026-08-20: "we should never
    # hammer them first and then just see what happens. We should start low and
    # then keep going up." A crawl OPENS at whatever `host_pacing` resolves
    # (a platform's published limit, robots.txt Crawl-delay, what the last run
    # discovered, or the floor) and climbs toward — never past — this number.
    host_rps: float = 4.0
    host_burst: float = 8.0
    # Set false to pin the crawl at `host_rps` with no detection and no ramp.
    # This exists for tests and for a host that has been explicitly measured;
    # it is NOT a per-crawl option and no request field sets it.
    adaptive_pacing: bool = True


class SiteCrawler:
    """Crawls a website starting from a seed URL with typed progress events."""

    def __init__(
        self,
        run_id: str,
        config: SiteCrawlerConfig,
        *,
        event_sink: CrawlEventSink | None = None,
        queue_backend: QueueBackend | None = None,
        body_persister: BodyPersister | None = None,
        cache: Any = None,
        domain_config: Any = None,
        browser_pool: Any = None,
        recipe_backend: RecipeBackend | None = None,
        recipe_action_runner: Any | None = None,
        screenshot_kinds: list[str] | None = None,
        extractor_runner: Any | None = None,
        strict_persistence: bool = False,
        retain_results: bool = True,
        pacing_knobs: PacingKnobs | None = None,
        remembered_pacing: RememberedPacing | None = None,
    ) -> None:
        if config.render_mode not in VALID_RENDER_MODES:
            raise ValueError(
                f"render_mode must be one of {sorted(VALID_RENDER_MODES)}, got {config.render_mode!r}"
            )
        self.run_id = run_id
        self.config = config
        self.event_sink: CrawlEventSink = event_sink or _NoopSink()
        self.queue: QueueBackend = queue_backend or InMemoryQueueBackend()
        self.body_persister = body_persister
        self.cache = cache
        self.domain_config = domain_config
        self.browser_pool = browser_pool
        self.recipe_backend = recipe_backend
        self.recipe_action_runner = recipe_action_runner
        self.screenshot_kinds = list(screenshot_kinds or [])
        # Extractor runner: async callable (html, url) -> dict[str, Any].
        # Optional — host injects to enable per-host custom extraction.
        self.extractor_runner = extractor_runner
        self.strict_persistence = strict_persistence
        self.retain_results = retain_results

        # Derived
        self.seed_url = _normalise_url(config.base_url)
        self.base_host = urlparse(self.seed_url).netloc.lower()
        self._include, include_invalid = _compile_patterns(config.include_patterns)
        self._exclude, exclude_invalid = _compile_patterns(config.exclude_patterns)
        # Reported as durable crawl_warning events at run() start — __init__
        # cannot emit (the sink is async).
        self._invalid_patterns: list[dict[str, str]] = [
            {**item, "kind": "include"} for item in include_invalid
        ] + [{**item, "kind": "exclude"} for item in exclude_invalid]
        # ONE resolved UA for this crawl. An override wins everywhere it is
        # set; deriving it once here is what keeps robots.txt, sitemap
        # discovery, the HTTP fetch and the browser context from disagreeing.
        self.user_agent = normalize_user_agent(config.user_agent_override) or config.user_agent
        # The override (or None) as handed to the transports. Distinct from
        # `self.user_agent` on purpose: robots/sitemap always need SOME agent
        # string, while the transports need to know whether to override at all.
        self._user_agent_override = normalize_user_agent(config.user_agent_override)
        self._robots = _RobotsCache(self.user_agent) if config.respect_robots else None
        # --- pacing ---------------------------------------------------
        # The limiter's DEFAULT is the floor, not the requested rate: a host
        # this crawl never planned for (a followed subdomain, an off-site
        # redirect) is the one we know least about, so it gets the most
        # cautious rate rather than the most aggressive one.
        self._pacing_knobs = pacing_knobs or DEFAULT_KNOBS
        self._remembered_pacing = remembered_pacing
        self._adaptive_pacing = config.adaptive_pacing
        self._rate_limiter = HostRateLimiter(
            default_rps=(
                self._pacing_knobs.floor_rps if config.adaptive_pacing else config.host_rps
            ),
            default_burst=(
                max(1.0, self._pacing_knobs.floor_rps * 2.0)
                if config.adaptive_pacing
                else config.host_burst
            ),
        )
        # One ramp per host key. The seed host's is built from a real probe in
        # `_establish_pacing`; any other host met mid-crawl gets a floor plan
        # lazily and climbs from there.
        self._ramps: dict[str, HostRamp] = {}
        # The seed host's robots.txt pacing directive, reused for its subdomains
        # (which are usually the same operator) and nothing else.
        self._crawl_delay_seconds: float | None = None
        self._pacing_plan: HostPacingPlan | None = None

        # Counters (used by progress events)
        self._pages_discovered = 0
        self._pages_fetched = 0
        self._pages_failed = 0
        # A page slot is consumed before a worker dequeues work. Counting only
        # completed fetches allows every concurrent worker to pass the limit at
        # once and overshoot max_pages by up to concurrency - 1.
        self._pages_reserved = 0
        self._page_slot_lock = asyncio.Lock()
        self._bytes_downloaded = 0
        self._cancel = asyncio.Event()
        self._semaphore = asyncio.Semaphore(config.concurrency)
        self._started_at: float | None = None
        self._last_progress_at: float = 0.0
        self._progress_emitted_at_pages = 0
        # url -> how many times a rate-limit (429/503) response has requeued it.
        # Bounds retries per URL across requeues within one run.
        self._rate_limit_attempts: dict[str, int] = {}
        # One authoritative proxy failure opens a run-scoped circuit breaker.
        # A broken shared proxy should cost one bounded retry, not one failed
        # round-trip for every URL in a 500-page crawl.
        self._proxy_disabled = False

        # Results — kept for callers that just want the data back. Not
        # populated for very large crawls (host writes to DB instead).
        self.results: dict[str, ScrapeResult] = {}

    # ------------------------------------------------------------------
    # Public lifecycle
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Pacing — detect the host, then climb (never open by hammering)
    # ------------------------------------------------------------------

    async def _establish_pacing(self) -> None:
        """Decide the seed host's opening rate BEFORE any page is fetched.

        Two cheap requests, once per crawl, run together: robots.txt (for a
        stated ``Crawl-delay``) and the base URL (for the platform fingerprint
        in its response headers). Both fail OPEN — an unreachable robots.txt or
        a base URL that 500s means we simply know less, which the plan already
        handles by opening at the floor. Neither may fail a crawl.
        """

        if not self._adaptive_pacing:
            return

        key = host_key(self.seed_url) or self.base_host
        try:
            delay_result, probe_result = await asyncio.wait_for(
                asyncio.gather(
                    self._probe_crawl_delay(),
                    self._probe_platform(),
                    return_exceptions=True,
                ),
                timeout=PACING_PROBE_BUDGET_SECONDS,
            )
        except TimeoutError:
            logger.info("pacing probe budget exhausted for %s — opening at the floor", key)
            delay_result, probe_result = None, (None, None)
        if isinstance(delay_result, BaseException):
            logger.info("crawl-delay probe raised for %s: %s", key, delay_result)
            delay_result = None
        if isinstance(probe_result, BaseException):
            logger.info("platform probe raised for %s: %s", key, probe_result)
            probe_result = (None, None)
        headers, html = probe_result

        self._crawl_delay_seconds = delay_result
        plan = resolve_plan(
            key,
            user_max_rps=self.config.host_rps,
            platform=detect_platform(headers=headers, html=html),
            crawl_delay_seconds=delay_result,
            remembered=self._remembered_pacing,
            knobs=self._pacing_knobs,
        )
        self._pacing_plan = plan
        ramp = HostRamp(plan=plan, knobs=self._pacing_knobs)
        self._ramps[key] = ramp
        self._rate_limiter.set_ramp_rate(key, ramp.current_rps)
        await self._emit(
            CrawlPacingEvent(
                run_id=self.run_id,
                host=key,
                **self._pacing_payload(ramp),
                reason="plan_resolved",
            )
        )

    async def _probe_crawl_delay(self) -> float | None:
        """The seed host's stated ``Crawl-delay`` / ``Request-rate``, if any.

        Read regardless of ``respect_robots``. That switch governs ACCESS — may
        we fetch this path — and these crawls are authorized first-party crawls
        that deliberately ignore it. Pacing is a different question: a site
        stating how fast it wants to be read is telling us something true about
        its own capacity, and honouring it costs us nothing but politeness.
        """

        url = f"{urlparse(self.seed_url).scheme}://{urlparse(self.seed_url).netloc}/robots.txt"
        try:
            # The SAME egress gate every page fetch passes. A probe is a request
            # like any other: skipping it here would have handed the crawler a
            # second, ungated way to reach an internal address.
            await validate_public_http_url(url)
            async with httpx.AsyncClient(
                timeout=PACING_PROBE_TIMEOUT_SECONDS, follow_redirects=True
            ) as client:
                resp = await client.get(url, headers={"User-Agent": self.user_agent})
            if not (200 <= resp.status_code < 300) or not resp.text:
                return None
            return parse_robots_txt(resp.text).crawl_delay_for(self.user_agent)
        except Exception as exc:
            logger.info("crawl-delay probe failed for %s: %s", url, exc)
            return None

    async def _probe_platform(self) -> tuple[dict[str, str] | None, str | None]:
        """One GET of the base URL, for its response headers and head markup.

        Deliberately a probe rather than a per-page detection: the platform is a
        property of the HOST, so paying for it once beats regexing every page of
        a 5,000-page crawl for an answer that cannot change.
        """

        try:
            await validate_public_http_url(self.seed_url)
            async with httpx.AsyncClient(
                timeout=PACING_PROBE_TIMEOUT_SECONDS, follow_redirects=True
            ) as client:
                resp = await client.get(self.seed_url, headers={"User-Agent": self.user_agent})
            # A 4xx/5xx still carries the server's own headers, which is where
            # the strongest fingerprints live — the body is what becomes
            # useless, so it is dropped rather than the whole probe.
            body = resp.text[:200_000] if 200 <= resp.status_code < 300 else None
            return dict(resp.headers), body
        except Exception as exc:
            logger.info("platform probe failed for %s: %s", self.seed_url, exc)
            return None, None

    def _ramp_for(self, url: str) -> HostRamp | None:
        """The ramp governing this URL's host, created lazily at the floor."""

        if not self._adaptive_pacing:
            return None
        key = host_key(url)
        if not key:
            return None
        ramp = self._ramps.get(key)
        if ramp is None:
            plan = resolve_plan(
                key,
                user_max_rps=self.config.host_rps,
                crawl_delay_seconds=(
                    self._crawl_delay_seconds
                    if key == (host_key(self.seed_url) or self.base_host)
                    else None
                ),
                knobs=self._pacing_knobs,
            )
            ramp = HostRamp(plan=plan, knobs=self._pacing_knobs)
            self._ramps[key] = ramp
            self._rate_limiter.set_ramp_rate(key, ramp.current_rps)
        return ramp

    def _apply_rate(self, key: str, ramp: HostRamp) -> None:
        self._rate_limiter.set_ramp_rate(key, ramp.current_rps)

    async def _note_clean_response(self, url: str, response_ms: int | None) -> None:
        """One clean fetch — the only thing that earns a climb."""

        ramp = self._ramp_for(url)
        if ramp is None:
            return
        before = ramp.current_rps
        changed = ramp.observe_success(latency_ms=float(response_ms) if response_ms else None)
        if changed is None:
            return
        key = host_key(url)
        self._apply_rate(key, ramp)
        await self._emit(
            CrawlPacingEvent(
                run_id=self.run_id,
                host=key,
                **self._pacing_payload(ramp),
                # A clean response can LOWER the rate: sustained latency growth
                # is the host straining without ever saying 429, and the ruling
                # covers it — back off before being told to.
                reason="ramp_up" if changed > before else "latency_backoff",
            )
        )

    async def _note_host_pushback(self, url: str, *, reason: str) -> None:
        """The host said slow down. Back off, and remember the rate that did it."""

        ramp = self._ramp_for(url)
        if ramp is None:
            return
        ramp.observe_limit(reason=reason)
        key = host_key(url)
        self._apply_rate(key, ramp)
        await self._emit(
            CrawlPacingEvent(
                run_id=self.run_id,
                host=key,
                **self._pacing_payload(ramp),
                reason=reason,
            )
        )

    @staticmethod
    def _pacing_payload(ramp: HostRamp) -> dict[str, Any]:
        snap = ramp.snapshot()
        return {
            "current_rps": float(snap["current_rps"]),
            "ceiling_rps": float(snap["effective_ceiling_rps"]),
            "discovered_ceiling_rps": snap["discovered_ceiling_rps"],
            "source": str(snap["source"]),
            "platform": snap["platform"],
            "platform_display": snap["platform_display"],
            "fronted_by": snap["fronted_by"],
            "crawl_delay_seconds": snap["crawl_delay_seconds"],
            "notes": list(snap["notes"]),
            "user_max_reduced": bool(snap["user_max_reduced"]),
            "limit_hits": int(snap["limit_hits"]),
        }

    def pacing_snapshots(self) -> dict[str, dict[str, Any]]:
        """Every host's live pacing state. The host persists and renders this."""

        return {key: ramp.snapshot() for key, ramp in self._ramps.items()}

    def remembered_pacing(self) -> dict[str, RememberedPacing]:
        """What this run learned, for the next one. Empty when it learned nothing."""

        out: dict[str, RememberedPacing] = {}
        for key, ramp in self._ramps.items():
            memory = ramp.to_remembered()
            if memory is not None:
                out[key] = memory
        return out

    async def run(self) -> dict[str, ScrapeResult]:
        self._started_at = time.monotonic()

        # Should be unreachable (CrawlStartRequest 422s invalid patterns), but
        # if a non-contract caller got one past __init__, the skip must be a
        # DURABLE warning — a dropped include/exclude widens the crawl.
        # Decide how fast this host may be crawled BEFORE any worker starts.
        # Two probe requests, once, so the crawl never opens by hammering.
        await self._establish_pacing()

        for item in self._invalid_patterns:
            await self._emit(
                CrawlWarningEvent(
                    run_id=self.run_id,
                    message=(
                        f"invalid {item['kind']} pattern was skipped — the crawl runs "
                        f"WIDER than requested: {item['pattern']!r} ({item['error']})"
                    ),
                    context=dict(item),
                )
            )

        seeded_from_sitemap = 0
        if self.config.list_mode and self.config.seed_urls:
            # Pure list mode — only visit the URLs the caller provided. Skip
            # sitemap discovery and don't follow internal links during crawl.
            for u in self.config.seed_urls:
                if await self.queue.enqueue(QueueItem(_normalise_url(u), 0, None, "seed")):
                    self._pages_discovered += 1
        else:
            # Discovery mode — sitemap first (if enabled), then the seed,
            # plus any explicit seed_urls the caller wants merged in.
            if self.config.seed_from_sitemap:
                try:
                    sitemap_urls = await _discover_sitemap_urls(
                        self.seed_url,
                        user_agent=self.user_agent,
                        max_urls=self.config.max_pages,
                    )
                    # A sitemap routinely carries thousands of URLs — the same
                    # O(1)-events-per-batch rule applies here as for page links.
                    seeded_from_sitemap = await self._classify_and_enqueue_batch(
                        list(sitemap_urls),
                        depth=0,
                        parent_url=None,
                        source="sitemap",
                    )
                except Exception as exc:
                    await self._emit(
                        CrawlWarningEvent(
                            run_id=self.run_id,
                            message=f"sitemap discovery failed: {type(exc).__name__}: {exc}",
                        )
                    )

            if await self.queue.enqueue(QueueItem(self.seed_url, 0, None, "seed")):
                self._pages_discovered += 1

            for u in self.config.seed_urls:
                if await self.queue.enqueue(QueueItem(_normalise_url(u), 0, None, "seed")):
                    self._pages_discovered += 1

        await self._emit(
            CrawlStartedEvent(
                run_id=self.run_id,
                base_url=self.seed_url,
                config={
                    "max_pages": self.config.max_pages,
                    "max_depth": self.config.max_depth,
                    "concurrency": self.config.concurrency,
                    "follow_subdomains": self.config.follow_subdomains,
                    "respect_robots": self.config.respect_robots,
                    "seed_from_sitemap": self.config.seed_from_sitemap,
                    "user_agent": self.user_agent,
                    "user_agent_override": self._user_agent_override,
                    "include_patterns": self.config.include_patterns,
                    "exclude_patterns": self.config.exclude_patterns,
                    "render_mode": self.config.render_mode,
                    "politeness_delay_ms": self.config.politeness_delay_ms,
                    "capture_screenshots": self.config.capture_screenshots,
                },
                seeded_from_sitemap=seeded_from_sitemap,
                initial_queue_depth=await self.queue.queue_depth(),
            )
        )

        # Main BFS loop — spawn workers up to concurrency, refill from queue.
        workers = [asyncio.create_task(self._worker()) for _ in range(self.config.concurrency)]
        try:
            while True:
                for worker in workers:
                    if worker.done() and not worker.cancelled():
                        exc = worker.exception()
                        if exc is not None:
                            raise exc
                if self._cancel.is_set():
                    break
                # Stop conditions: no work in flight AND queue is empty AND we hit
                # max_pages OR queue is just empty.
                qd, inflight = await self.queue.counts()
                if qd == 0 and inflight == 0 and self._pages_reserved == 0:
                    break
                # The page-budget stop MUST also wait for reserved slots to
                # resolve. A reserved slot means a worker is between
                # `_reserve_page_slot()` and settling its item — on a durable
                # frontier its claim may not be VISIBLE yet (`counts()` is a DB
                # read racing the claim's commit), so `inflight == 0` alone is
                # not "nothing is being worked". The old condition
                # (`fetched + reserved >= max_pages and inflight == 0`) broke
                # out of this loop the instant a single-URL run's only worker
                # reserved its slot, cancelled that worker mid-claim, and
                # stranded the item IN_PROGRESS — every scheduled `page_fetch`
                # of cosmeticinjectables.com died this way in <1s with
                # `pages_fetched=0, pages_failed=0` (176 failed sessions,
                # 2026-08-12/13).
                if (
                    self._pages_fetched >= self.config.max_pages
                    and inflight == 0
                    and self._pages_reserved == 0
                ):
                    break
                await self._maybe_emit_progress()
                await asyncio.sleep(0.1)
        finally:
            for w in workers:
                w.cancel()
            await asyncio.gather(*workers, return_exceptions=True)

        duration_ms = int((time.monotonic() - (self._started_at or time.monotonic())) * 1000)
        status = "canceled" if self._cancel.is_set() else "completed"
        remaining_queue_depth = await self.queue.queue_depth()
        remaining_in_flight = await self.queue.in_flight_count()
        limit_reached = self._pages_fetched >= self.config.max_pages and remaining_queue_depth > 0

        # TRUNCATION GATE — a run that stopped with work still on the frontier
        # did NOT complete, and must never be recorded as if it did.
        #
        # This exists because it happened: a crawl that lost its client stopped
        # mid-run and wrote `status='complete'` with `pages_fetched: 0`, leaving
        # its claimed work item in flight forever. In the UI and in
        # `web.crawl_session` that was indistinguishable from a real crawl of a
        # site with nothing on it — the single most expensive kind of lie a
        # pipeline can tell, because nobody goes looking for a success.
        #
        # Three legitimate ways to end with work left, none of which this flags:
        # a user cancel (`_cancel` set), hitting the page budget
        # (`limit_reached`), and an empty frontier. Anything else means the loop
        # tore down while the crawl still had work — the run is FAILED, which is
        # also what makes it eligible for the existing crash-resume sweep
        # instead of being buried as a success.
        truncated = (
            status == "completed"
            and not limit_reached
            and (remaining_in_flight > 0 or remaining_queue_depth > 0)
        )
        truncation_error: str | None = None
        if truncated:
            status = "failed"
            truncation_error = (
                f"Run ended with work still on the frontier — {remaining_in_flight} item(s) "
                f"in flight and {remaining_queue_depth} queued, after fetching "
                f"{self._pages_fetched} of {self._pages_discovered} discovered page(s). "
                "The crawl was truncated; it did not finish."
            )
            logger.error(
                "CRAWL TRUNCATED (run %s): %s Something stopped the run loop while the "
                "crawl still had work — this is never normal. The session is recorded "
                "FAILED (not complete) so it stays resumable.",
                self.run_id,
                truncation_error,
            )
            await self._emit(
                CrawlWarningEvent(
                    run_id=self.run_id,
                    message=truncation_error,
                    context={
                        "truncated": True,
                        "remaining_in_flight": remaining_in_flight,
                        "remaining_queue_depth": remaining_queue_depth,
                        "pages_fetched": self._pages_fetched,
                    },
                )
            )

        # Dead-lettered items are the frontier's zombie backstop firing: the
        # store terminally parked a URL the crawler still believed was queued
        # (see runtime_queue.DEFAULT_ITEM_MAX_ATTEMPTS). Those pages were
        # neither fetched nor counted failed, so a run that has any can never
        # claim full coverage. Duck-typed: only the durable backend can
        # dead-letter, so only it exposes the count.
        dead_letter_probe = getattr(self.queue, "dead_letter_count", None)
        dead_lettered = 0
        if dead_letter_probe is not None:
            try:
                dead_lettered = int(await dead_letter_probe())
            except Exception:
                logger.exception("could not read the frontier's dead-letter count")
        if dead_lettered:
            await self._emit(
                CrawlWarningEvent(
                    run_id=self.run_id,
                    message=(
                        f"{dead_lettered} frontier item(s) were DEAD-LETTERED by the "
                        "durable store's attempt budget — those URLs were neither "
                        "fetched nor recorded failed, so this run does NOT have "
                        "full coverage."
                    ),
                    context={"dead_lettered": dead_lettered},
                )
            )

        coverage_complete = (
            status == "completed"
            and remaining_queue_depth == 0
            and remaining_in_flight == 0
            and self._pages_failed == 0
            and dead_lettered == 0
            and not limit_reached
        )
        await self._emit(
            CrawlCompletedEvent(
                run_id=self.run_id,
                pages_discovered=self._pages_discovered,
                pages_fetched=self._pages_fetched,
                pages_failed=self._pages_failed,
                issues_count=0,  # host fills this in after issue detection runs
                duration_ms=duration_ms,
                bytes_downloaded=self._bytes_downloaded,
                status=status,
                coverage_complete=coverage_complete,
                limit_reached=limit_reached,
                remaining_queue_depth=remaining_queue_depth,
                error_message=truncation_error,
            )
        )
        return self.results

    def cancel(self) -> None:
        self._cancel.set()

    # ------------------------------------------------------------------
    # Worker
    # ------------------------------------------------------------------

    async def _worker(self) -> None:
        while not self._cancel.is_set():
            if not await self._reserve_page_slot():
                return
            try:
                item = await self.queue.dequeue()
            except asyncio.CancelledError:
                await self._release_page_slot()
                raise
            if item is None:
                await self._release_page_slot()
                # Queue empty — wait briefly; the run loop decides when to stop.
                await asyncio.sleep(0.1)
                # If still empty and no in-flight, the loop will exit and cancel us.
                queue_depth, inflight = await self.queue.counts()
                if queue_depth == 0 and inflight == 0:
                    return
                continue
            try:
                await self._process(item)
            finally:
                await self._release_page_slot()

    async def _reserve_page_slot(self) -> bool:
        """Atomically reserve one dispatch slot under the crawl's hard cap."""
        async with self._page_slot_lock:
            if self._pages_fetched + self._pages_reserved >= self.config.max_pages:
                return False
            self._pages_reserved += 1
            return True

    async def _release_page_slot(self) -> None:
        """Return a reservation when no queue item was dispatched."""
        async with self._page_slot_lock:
            self._pages_reserved -= 1

    async def _process(self, item: QueueItem) -> None:
        if self._cancel.is_set():
            # A cancelled item was never processed — recording it "done" (or any
            # terminal state) would poison a durable frontier's record: a future
            # resume must see it as STILL TO DO. will_retry=True returns it to
            # pending. No spin risk on the in-memory frontier: workers stop
            # dequeuing the moment the cancel flag is set (_worker's loop
            # condition), so a requeued item is never picked up again this run.
            await self.queue.mark_failed(item.url, "crawl_cancelled", will_retry=True)
            return

        # Discover event — fired for everything we pull from the queue. Seed
        # + sitemap items already had `_pages_discovered` bumped when enqueued;
        # link-discovered items got bumped when we enqueued them. Either way,
        # we emit the event here so the FE sees the lifecycle.
        await self._emit(
            CrawlPageDiscoveredEvent(
                run_id=self.run_id,
                url=item.url,
                depth=item.depth,
                parent_url=item.parent_url,
                source=item.source,  # type: ignore[arg-type]
            )
        )

        if self.config.politeness_delay_ms > 0:
            await asyncio.sleep(self.config.politeness_delay_ms / 1000.0)

        # Per-host rate limit — applied to ALL workers, so concurrency=8 against
        # the same host doesn't exceed `host_rps`. Times out cleanly if the
        # bucket can't refill in time; treat that as a transient skip.
        try:
            await self._rate_limiter.acquire(item.url)
        except TimeoutError:
            # Bounded like the HTTP 429 path (same counter): the CRAWLER owns
            # retry policy — an unbounded will_retry=True here made the store's
            # attempt budget the de-facto policy on a durable frontier (silent
            # dead-letter), and counting each retry as a failure double-counted
            # one page. Retries are warnings; only exhaustion is a failure.
            attempts = self._rate_limit_attempts.get(item.url, 0) + 1
            self._rate_limit_attempts[item.url] = attempts
            if attempts <= MAX_RATE_LIMIT_RETRIES:
                await self._emit(
                    CrawlWarningEvent(
                        run_id=self.run_id,
                        message=(
                            f"{item.url} — per-host rate limit timed out; requeued "
                            f"(attempt {attempts}/{MAX_RATE_LIMIT_RETRIES})"
                        ),
                    )
                )
                await self.queue.mark_failed(item.url, "rate_limit_timeout", will_retry=True)
                return
            await self._emit(
                CrawlPageFailedEvent(
                    run_id=self.run_id,
                    url=item.url,
                    error_class="RateLimitTimeout",
                    error_message=(
                        f"per-host rate limit timed out for {item.url} after "
                        f"{MAX_RATE_LIMIT_RETRIES} retries"
                    ),
                )
            )
            await self.queue.mark_failed(item.url, "rate_limit_timeout", will_retry=False)
            self._pages_failed += 1
            return

        async with self._semaphore:
            t0 = time.monotonic()
            try:
                await validate_public_http_url(item.url)
                # robots.txt check (fail-open if unreachable)
                if self._robots is not None:
                    if not await self._robots.can_fetch(item.url):
                        await self._emit(
                            CrawlPageFailedEvent(
                                run_id=self.run_id,
                                url=item.url,
                                error_class="RobotsDisallowed",
                                error_message=f"robots.txt disallows {item.url} for {self.user_agent}",
                            )
                        )
                        await self.queue.mark_failed(item.url, "robots_disallowed")
                        self._pages_failed += 1
                        return

                request_type = self._pick_request_type()
                use_proxy = not self._proxy_disabled
                if self.domain_config is not None:
                    try:
                        proxy_type = self.domain_config.get_proxy_type(item.url)
                        if proxy_type == "none":
                            use_proxy = False
                    except Exception:
                        pass

                # Branch on render mode. The screenshot path needs the same
                # browser session that's about to read the HTML, so we drive
                # Playwright directly via PlaywrightBrowserPool.fetch_with_capture
                # — recipes get a chance to run, then we synthesise a
                # ScrapeResult through the orchestrator's parser so every
                # downstream consumer (parser/links/SEO audit) sees the same
                # post-recipe HTML.
                shots: list[CapturedShot] = []
                recipe = None
                if self.recipe_backend is not None:
                    try:
                        recipe = await self.recipe_backend.find_for_url(item.url)
                    except Exception:
                        logger.exception("recipe lookup failed")

                url_content_hint = detect_content_type_from_url(item.url)
                browser_capture_supported = url_content_hint not in {
                    ContentType.PDF,
                    ContentType.JSON,
                    ContentType.XML,
                    ContentType.PLAIN_TEXT,
                    ContentType.IMAGE,
                }
                if not browser_capture_supported:
                    request_type = RequestType.NORMAL
                if (
                    self._wants_screenshots()
                    and browser_capture_supported
                    and self.browser_pool is not None
                    and hasattr(self.browser_pool, "fetch_with_capture")
                ):
                    kinds = self.screenshot_kinds or ["viewport_desktop", "full_page"]
                    expectation_recorder = getattr(
                        self.body_persister,
                        "record_screenshots_expected",
                        None,
                    )
                    if expectation_recorder is not None:
                        await expectation_recorder(len(kinds))
                    actions = list(recipe.actions) if recipe else []
                    try:
                        captured = await self.browser_pool.fetch_with_capture(
                            item.url,
                            proxy=get_required_random_proxy() if use_proxy else None,
                            timeout_ms=self.config.browser_navigation_timeout_ms,
                            settle_timeout_ms=self.config.browser_settle_timeout_ms,
                            screenshot_kinds=kinds,
                            recipe_actions=actions,
                            action_runner=self.recipe_action_runner,
                            **self._pool_ua_kwargs(),
                        )
                    except Exception as proxy_exc:
                        if not use_proxy:
                            raise
                        await self._emit_proxy_bypass(item.url, error=proxy_exc)
                        use_proxy = False
                        captured = await self.browser_pool.fetch_with_capture(
                            item.url,
                            proxy=None,
                            timeout_ms=self.config.browser_navigation_timeout_ms,
                            settle_timeout_ms=self.config.browser_settle_timeout_ms,
                            screenshot_kinds=kinds,
                            recipe_actions=actions,
                            action_runner=self.recipe_action_runner,
                            **self._pool_ua_kwargs(),
                        )
                    if self._is_proxy_failure_status(captured.status_code) and use_proxy:
                        await self._emit_proxy_bypass(
                            item.url,
                            status=captured.status_code,
                        )
                        use_proxy = False
                        captured = await self.browser_pool.fetch_with_capture(
                            item.url,
                            proxy=None,
                            timeout_ms=self.config.browser_navigation_timeout_ms,
                            settle_timeout_ms=self.config.browser_settle_timeout_ms,
                            screenshot_kinds=kinds,
                            recipe_actions=actions,
                            action_runner=self.recipe_action_runner,
                            **self._pool_ua_kwargs(),
                        )
                    # Hand the rendered HTML to the orchestrator's parser so we
                    # match the regular path's ScrapeResult shape.
                    content_type_raw = captured.headers.get("content-type", "")
                    content_type, _ = detect_response_content_type(
                        url=captured.response_url or item.url,
                        content_type_raw=content_type_raw,
                        content=captured.content,
                    )
                    # A FAILING browser response gets the SAME challenge
                    # classification the HTTP path uses (one classifier, not a
                    # second hand-rolled copy) — otherwise a WAF interstitial
                    # rendered by the browser is labelled `bad_status`, misread
                    # as a rate limit, and requeued 5× for nothing. Only failing
                    # responses are classified: a healthy page may legitimately
                    # embed a Turnstile widget (a protected contact form), and
                    # that must never mark the page failed.
                    browser_failure_reasons: list[dict] = []
                    if captured.status_code >= 400:
                        browser_failure_reasons = detect_challenge_reasons(
                            html=captured.content, title=captured.title
                        )
                        browser_failure_reasons.append(
                            {FailureReason.BAD_STATUS: f"Status code {captured.status_code}"}
                        )
                    response = Response(
                        request_url=item.url,
                        proxy_used=use_proxy,
                        request_type=RequestType.BROWSER,
                        content_type=content_type,
                        extension="",
                        content_type_raw=content_type_raw,
                        response_url=captured.response_url,
                        response_headers=captured.headers,
                        title=captured.title,
                        status_code=captured.status_code,
                        redirect_chain=captured.redirect_chain,
                        content=captured.content,
                        failed=bool(browser_failure_reasons),
                        failed_primary_reason=(
                            primary_failure_reason(browser_failure_reasons)
                            if browser_failure_reasons
                            else None
                        ),
                        failed_reasons=browser_failure_reasons,
                    )
                    # Same rule as the main fetch path (orchestrator.scrape):
                    # parsing is CPU-bound (a PDF body here parses the whole
                    # document) and must not block the event loop — every other
                    # worker, the heartbeat, and the stream stall behind it.
                    result = await asyncio.to_thread(_build_result_from_response, response)
                    response_ms = int((time.monotonic() - t0) * 1000)
                    shots = [
                        CapturedShot(kind=s.kind, width=s.width, height=s.height, bytes=s.bytes)
                        for s in captured.screenshots
                    ]
                    actual_kinds = [shot.kind for shot in shots]
                    if actual_kinds != kinds:
                        missing = [kind for kind in kinds if kind not in actual_kinds]
                        unexpected = [kind for kind in actual_kinds if kind not in kinds]
                        capture_failures = [
                            {
                                "kind": failure.kind,
                                "error_class": failure.error_class,
                                "error_message": failure.error_message,
                            }
                            for failure in getattr(captured, "screenshot_failures", [])
                        ]
                        warning_message = (
                            f"Screenshot capture was incomplete for {item.url}; "
                            "the fetched page content was retained."
                        )
                        logger.warning(
                            "%s expected=%s actual=%s missing=%s unexpected=%s failures=%s",
                            warning_message,
                            kinds,
                            actual_kinds,
                            missing,
                            unexpected,
                            capture_failures,
                        )
                        await self._emit(
                            CrawlWarningEvent(
                                run_id=self.run_id,
                                message=warning_message,
                                context={
                                    "url": item.url,
                                    "expected": kinds,
                                    "captured": actual_kinds,
                                    "missing": missing,
                                    "unexpected": unexpected,
                                    "failures": capture_failures,
                                },
                            )
                        )
                    capture_recorder = getattr(
                        self.body_persister,
                        "record_screenshots_captured",
                        None,
                    )
                    if capture_recorder is not None:
                        await capture_recorder(len(shots))
                else:
                    try:
                        result = await scrape(
                            item.url,
                            use_proxy=use_proxy,
                            request_type=request_type,
                            cache=self.cache,
                            domain_config=self.domain_config,
                            browser_pool=self.browser_pool,
                            user_agent=self._user_agent_override,
                        )
                    except Exception as proxy_exc:
                        if not use_proxy:
                            raise
                        await self._emit_proxy_bypass(item.url, error=proxy_exc)
                        use_proxy = False
                        result = await scrape(
                            item.url,
                            use_proxy=False,
                            request_type=request_type,
                            cache=None,
                            domain_config=self.domain_config,
                            browser_pool=self.browser_pool,
                            user_agent=self._user_agent_override,
                        )
                    if self._is_proxy_failure_status(result.status_code) and use_proxy:
                        await self._emit_proxy_bypass(
                            item.url,
                            status=result.status_code,
                        )
                        use_proxy = False
                        result = await scrape(
                            item.url,
                            use_proxy=False,
                            request_type=request_type,
                            cache=None,
                            domain_config=self.domain_config,
                            browser_pool=self.browser_pool,
                            user_agent=self._user_agent_override,
                        )
                    response_ms = int((time.monotonic() - t0) * 1000)

                    # http_first → escalate to the browser when plain HTTP was
                    # insufficient. Two triggers:
                    #   1. Thin content — a JS-rendered page returned a shell.
                    #   2. A block/transport failure a real browser routinely
                    #      gets past (Cloudflare/WAF challenges, TLS-fingerprint
                    #      blocks, 403s, connection resets). Without this, the
                    #      non-screenshot path hard-failed every page the HTTP
                    #      client couldn't reach while the screenshot path —
                    #      already browser-driven — crawled the same site fine.
                    # 429/503 are deliberately excluded: the adaptive throttle +
                    # bounded requeue below own rate-limit responses.
                    if (
                        self.config.render_mode == RENDER_HTTP_FIRST
                        and request_type == RequestType.NORMAL
                        and browser_capture_supported
                        and self.browser_pool is not None
                        and (
                            (result.success and self._is_thin(result))
                            or (not result.success and self._browser_may_recover(result))
                        )
                    ):
                        if not result.success:
                            await self._emit(
                                CrawlWarningEvent(
                                    run_id=self.run_id,
                                    message=(
                                        f"{item.url} — HTTP fetch failed "
                                        f"({result.failure_reason or 'unknown'}); retrying "
                                        "with browser rendering."
                                    ),
                                    context={
                                        "url": item.url,
                                        "fallback": "browser",
                                        "http_status": result.status_code or 0,
                                        "failure_reason": result.failure_reason,
                                        "failure_details": result.failure_details,
                                    },
                                )
                            )
                        browser_result = await self._browser_refetch(item, use_proxy=use_proxy)
                        # Thin-content escalations keep the browser result
                        # unconditionally (today's behavior). Block/failure
                        # escalations keep it only on success — the original
                        # HTTP failure is the more accurate diagnosis when
                        # the browser also fails.
                        if browser_result is not None and (
                            result.success or browser_result.success
                        ):
                            result = browser_result
                            # Timing belongs to the result we KEEP. Stamping
                            # it unconditionally attributed the browser's
                            # navigation time to a retained HTTP failure.
                            response_ms = int((time.monotonic() - t0) * 1000)

                bytes_total = self._estimate_bytes(result)
                self._bytes_downloaded += bytes_total

                final_url = result.response_url or item.url
                await validate_public_http_url(final_url)

                # HTTP 429/503 = the origin throttling us, not a broken page.
                # Back the host off and requeue (bounded) instead of failing.
                # Emit NEITHER a page_fetched (a throttled response fetched no
                # content) NOR a terminal failure until retries are exhausted —
                # so a retrying URL never inflates the fetched/failed counters.
                # A recognized bot-protection challenge is EXCLUDED: it wears a
                # 429/503 but no amount of throttling gets past a WAF, and
                # requeueing it 5× on the same HTTP client only burns the crawl
                # budget before mislabelling the page "RateLimited".
                status = result.status_code or 0
                if status in RATE_LIMIT_STATUSES and not self._is_challenge(result):
                    attempts = self._rate_limit_attempts.get(item.url, 0) + 1
                    self._rate_limit_attempts[item.url] = attempts
                    # The ramp owns THIS crawl's rate (and records the rate that
                    # provoked the limit as the discovered ceiling). The shared
                    # throttle is still recorded so the other lanes — research,
                    # SEO capture — learn from what the crawl discovered; a
                    # ramp-driven host is exempt from applying it twice.
                    await self._note_host_pushback(item.url, reason=f"http_{status}")
                    new_rps, _ = self._rate_limiter.throttle_host(
                        item.url,
                        factor=RATE_LIMIT_THROTTLE_FACTOR,
                        min_rps=RATE_LIMIT_MIN_RPS,
                    )
                    ramp = self._ramp_for(item.url)
                    if ramp is not None:
                        new_rps = ramp.current_rps
                    if attempts <= MAX_RATE_LIMIT_RETRIES:
                        await self._emit(
                            CrawlWarningEvent(
                                run_id=self.run_id,
                                message=(
                                    f"{item.url} — rate limited (HTTP {status}); throttled "
                                    f"{urlparse(item.url).netloc} to {new_rps:.2f} rps and "
                                    f"requeued (attempt {attempts}/{MAX_RATE_LIMIT_RETRIES})"
                                ),
                            )
                        )
                        await self.queue.mark_failed(item.url, f"http_{status}", will_retry=True)
                        return
                    # Retries exhausted. LAYER 2 before the terminal failure: a
                    # persistent 429/503 that throttling never clears is often a
                    # block with an unrecognized signature (the challenge check
                    # above only knows the signatures we've seen). Spend ONE
                    # browser navigation on it — the same fetch that recovers a
                    # labelled challenge — rather than hard-failing a page the
                    # screenshot path would have crawled fine.
                    escalated: ScrapeResult | None = None
                    if (
                        self.config.render_mode == RENDER_HTTP_FIRST
                        and request_type == RequestType.NORMAL
                        and browser_capture_supported
                        and self.browser_pool is not None
                    ):
                        await self._emit(
                            CrawlWarningEvent(
                                run_id=self.run_id,
                                message=(
                                    f"{item.url} — still HTTP {status} after "
                                    f"{MAX_RATE_LIMIT_RETRIES} throttled retries; "
                                    "trying the browser once before failing it."
                                ),
                                context={
                                    "url": item.url,
                                    "fallback": "browser",
                                    "http_status": status,
                                    "trigger": "rate_limit_exhausted",
                                },
                            )
                        )
                        escalated = await self._browser_refetch(item, use_proxy=use_proxy)
                    if escalated is None or not escalated.success:
                        self._pages_failed += 1
                        await self._emit(
                            CrawlPageFailedEvent(
                                run_id=self.run_id,
                                url=item.url,
                                error_class="RateLimited",
                                error_message=(
                                    f"HTTP {status}: host kept rate-limiting after "
                                    f"{MAX_RATE_LIMIT_RETRIES} throttled retries"
                                ),
                                attempt=attempts,
                            )
                        )
                        await self.queue.mark_failed(item.url, f"http_{status}_exhausted")
                        return
                    # The browser got the page. Re-derive everything the fetched
                    # event reports from the result we actually keep, then fall
                    # through to the normal fetched/parsed/persist path.
                    self._rate_limit_attempts.pop(item.url, None)
                    result = escalated
                    status = result.status_code or 0
                    final_url = result.response_url or item.url
                    await validate_public_http_url(final_url)
                    bytes_total = self._estimate_bytes(result)
                    self._bytes_downloaded += bytes_total
                    response_ms = int((time.monotonic() - t0) * 1000)

                await self._emit(
                    CrawlPageFetchedEvent(
                        run_id=self.run_id,
                        url=item.url,
                        final_url=final_url,
                        http_status=status,
                        response_time_ms=response_ms,
                        bytes=bytes_total,
                        mime_type=result.content_type,
                        redirected=(final_url != item.url),
                        redirect_chain=list(result.redirect_chain or []),
                    )
                )

                low_text_details = [
                    detail[FailureReason.LOW_TEXT_CONTENT.value]
                    for detail in result.failure_details
                    if FailureReason.LOW_TEXT_CONTENT.value in detail
                ]
                if low_text_details:
                    await self._emit(
                        CrawlWarningEvent(
                            run_id=self.run_id,
                            message=(
                                f"{item.url} produced little extracted body text; "
                                "the successful response is still being preserved."
                            ),
                            context={
                                "url": item.url,
                                "signal": FailureReason.LOW_TEXT_CONTENT.value,
                                "details": low_text_details,
                                "http_status": status,
                                "bytes": bytes_total,
                                "crawl_continued": True,
                            },
                        )
                    )

                if not result.success:
                    self._pages_failed += 1
                    await self._emit(
                        CrawlPageFailedEvent(
                            run_id=self.run_id,
                            url=item.url,
                            error_class=result.failure_reason or "ScrapeFailed",
                            error_message=self._failure_message(result),
                        )
                    )
                    await self.queue.mark_failed(item.url, result.failure_reason or "failed")
                    return

                # A clean fetch is the ONLY thing that earns a climb — this is
                # the "keep pushing up higher" half of the ruling. It is placed
                # after the failure return above so a 200-shaped failure never
                # buys the crawl more speed.
                await self._note_clean_response(final_url, response_ms)

                # Run any matching custom extractors against the raw HTML so
                # the host can persist them alongside the page row.
                extractor_results: dict[str, Any] = {}
                if self.extractor_runner is not None and result.raw_html:
                    try:
                        extractor_results = (
                            await self.extractor_runner(
                                result.raw_html,
                                final_url,
                            )
                            or {}
                        )
                    except Exception:
                        logger.exception("extractor runner failed for %s", item.url)

                # Build the complete page summary before persistence. Canonical
                # web persistence needs the extracted signals to create the
                # immutable snapshot in the same operation as its artifacts.
                summary = self._build_summary(result, item, response_ms, bytes_total, None)
                await enrich_image_inventory(summary.image_inventory)

                # Persist body + screenshots (storage + canonical snapshot via host)
                if self.body_persister is not None:
                    try:
                        persisted = await self.body_persister(
                            PersistRequest(
                                run_id=self.run_id,
                                url=item.url,
                                final_url=final_url,
                                body=(
                                    result.raw_body
                                    if result.raw_body is not None
                                    else result.raw_html or result.text_data or result.raw_text
                                ),
                                markdown=result.markdown_renderable,
                                screenshots=shots,
                                mime_type=result.content_type_raw or result.content_type,
                                extractor_results=extractor_results,
                                page_summary=summary,
                            )
                        )
                        if persisted:
                            summary.page_id = getattr(persisted, "page_id", None)
                            summary.snapshot_id = getattr(persisted, "snapshot_id", None)
                            for notice in getattr(persisted, "warnings", None) or []:
                                await self._emit(
                                    CrawlWarningEvent(
                                        run_id=self.run_id,
                                        message=str(notice.get("message", "")),
                                        context=dict(notice.get("context") or {}),
                                    )
                                )
                    except Exception as exc:
                        logger.warning(
                            "body_persister failed for %s: %s", item.url, exc, exc_info=True
                        )
                        await self._emit(
                            CrawlWarningEvent(
                                run_id=self.run_id,
                                message=CrawlPersistenceError.error_info.user_message,
                                context={
                                    "url": item.url,
                                    "failure_scope": "page",
                                    "crawl_continued": True,
                                },
                            )
                        )
                        if self.strict_persistence:
                            raise CrawlPersistenceError() from exc

                await self._emit(CrawlPageParsedEvent(run_id=self.run_id, page=summary))

                if self.retain_results:
                    self.results[item.url] = result
                self._pages_fetched += 1

                # Discover only real navigational links from the canonical HTML
                # audit. The generic scraper result intentionally includes every
                # href/src resource (scripts, images, oEmbed alternates, feeds);
                # treating those machine resources as crawlable pages creates
                # false page identities and false HTML-audit failures.
                #
                # Children are enqueued BEFORE the parent settles: on a durable
                # frontier, settling first opens a crash window where the parent
                # is recorded done but its links were never seeded — the subtree
                # silently vanishes from any resumed run. Seed-then-settle keeps
                # the frontier at-least-once.
                await self._enqueue_links(summary, item)
                await self.queue.mark_done(item.url)

                await self._maybe_emit_progress()

            except asyncio.CancelledError:
                # The worker task was torn down mid-item (run-loop exit, host
                # shutdown, external cancel of `run()`), NOT the user-cancel
                # flag (handled at the top of `_process`). The item was never
                # terminally processed: without a settle, a durable frontier
                # keeps the claim IN_PROGRESS until the lease reaper (600s) —
                # and the run's own truncation gate correctly reports it as
                # stranded. Return it to pending, shielded so the cancellation
                # already unwinding this task cannot abort the settle write.
                try:
                    await asyncio.shield(
                        self.queue.mark_failed(item.url, "worker_cancelled", will_retry=True)
                    )
                except asyncio.CancelledError:
                    pass  # a second cancel hit the await; the shielded settle still runs
                except Exception:
                    logger.warning(
                        "could not requeue in-flight item %s during worker cancellation "
                        "(the frontier lease reaper is the backstop)",
                        item.url,
                        exc_info=True,
                    )
                raise
            except Exception as exc:
                self._pages_failed += 1
                try:
                    await self._emit(
                        CrawlPageFailedEvent(
                            run_id=self.run_id,
                            url=item.url,
                            error_class=type(exc).__name__,
                            error_message=str(exc),
                        )
                    )
                finally:
                    await self.queue.mark_failed(item.url, f"{type(exc).__name__}: {exc}")
                    logger.warning("crawler error on %s: %s", item.url, exc, exc_info=True)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _pool_ua_kwargs(self) -> dict[str, str]:
        """The UA kwarg for the injected browser pool — present only when the
        caller actually asked for an override.

        `browser_pool` is a duck-typed seam a host supplies. Always sending
        `user_agent=None` would break every pool built before this field
        existed, for no benefit. When an override IS requested and the pool
        cannot take it, the resulting TypeError is the CORRECT outcome: a pool
        that quietly ignored the UA would fetch under a different identity than
        the HTTP path, which is exactly the split-identity crawl this field
        exists to prevent.
        """
        return {"user_agent": self._user_agent_override} if self._user_agent_override else {}

    def _wants_screenshots(self) -> bool:
        return (
            self.config.render_mode == RENDER_BROWSER_WITH_SCREENSHOT
            or self.config.capture_screenshots
        )

    async def _emit_proxy_bypass(
        self,
        url: str,
        *,
        status: int | None = None,
        error: Exception | None = None,
    ) -> None:
        self._proxy_disabled = True
        outcome = f"HTTP {status}" if status is not None else type(error).__name__
        logger.warning(
            "proxied request failed for %s with %s; retrying directly",
            url,
            outcome,
        )
        context: dict[str, Any] = {
            "url": url,
            "fallback": "direct",
            "proxy_circuit_open": True,
        }
        if status is not None:
            context["proxy_status"] = status
        if error is not None:
            context["proxy_error_class"] = type(error).__name__
        await self._emit(
            CrawlWarningEvent(
                run_id=self.run_id,
                message=(
                    f"The configured proxy could not return an authoritative "
                    f"response for {url} ({outcome}); "
                    "retrying the page directly."
                ),
                context=context,
            )
        )

    @staticmethod
    def _is_proxy_failure_status(status: int | None) -> bool:
        return status == 407 or (status is not None and status >= 500)

    def _pick_request_type(self) -> RequestType:
        if self.config.render_mode in (RENDER_BROWSER_ALWAYS, RENDER_BROWSER_WITH_SCREENSHOT):
            return RequestType.BROWSER
        if self.config.capture_screenshots:
            return RequestType.BROWSER
        return RequestType.NORMAL

    # Failure classes a real browser routinely recovers where the HTTP client
    # cannot: bot-protection challenges and TLS/transport-level rejections.
    # Rate limits (429/503) are excluded — the adaptive host throttle owns them.
    BROWSER_RECOVERABLE_REASONS = frozenset(
        {
            FailureReason.CLOUDFLARE_BLOCK.value,
            FailureReason.BLOCKED.value,
            FailureReason.REQUEST_ERROR.value,
        }
    )

    # A bot-protection interstitial. Cloudflare serves these with any status it
    # likes — 403, 429, and 503 are all common — so a challenge OUTRANKS both
    # the rate-limit exclusion and whatever `failure_reason` label won the
    # primary slot. "503" from a challenge is not the origin throttling us; it
    # is the WAF, and a real browser is exactly what gets past it.
    CHALLENGE_REASONS = frozenset(
        {
            FailureReason.CLOUDFLARE_BLOCK.value,
            FailureReason.BLOCKED.value,
        }
    )

    # A transport error whose text matches one of these is the host being
    # ABSENT or refusing TCP — a browser fails identically, so spending a full
    # navigation (and a pooled browser slot) on it is pure waste. A crawl of a
    # site with a broken link graph would otherwise pay one render per dead
    # link. Anything else at the transport layer (TLS/fingerprint rejections,
    # resets mid-handshake) IS worth one browser attempt.
    UNREACHABLE_ERROR_SIGNATURES = (
        "name or service not known",
        "nodename nor servname",
        "temporary failure in name resolution",
        "could not resolve host",
        "connection refused",
        "no route to host",
        "network is unreachable",
        "getaddrinfo",
    )

    def _looks_unreachable(self, result: ScrapeResult) -> bool:
        for detail in result.failure_details:
            for value in detail.values():
                text = str(value).lower()
                if any(sig in text for sig in self.UNREACHABLE_ERROR_SIGNATURES):
                    return True
        return False

    async def _browser_refetch(self, item: QueueItem, *, use_proxy: bool) -> ScrapeResult | None:
        """ONE browser navigation of a URL the HTTP client couldn't get.

        The single escalation primitive both triggers share (a classified block
        and an exhausted rate limit). Returns None when the browser itself
        fails — the caller decides whether to keep the HTTP diagnosis.
        """
        if self.browser_pool is None:
            return None
        try:
            return await scrape(
                item.url,
                use_proxy=use_proxy,
                request_type=RequestType.BROWSER,
                cache=self.cache,
                domain_config=self.domain_config,
                browser_pool=self.browser_pool,
                user_agent=self._user_agent_override,
            )
        except Exception as exc:
            logger.info("browser fallback failed for %s: %s", item.url, exc)
            return None

    @staticmethod
    def _failure_reasons(result: ScrapeResult) -> set[str]:
        """EVERY reason recorded for this fetch, not just the primary label.

        A response carries a list of reasons; only one wins `failure_reason`.
        Keying a decision on the primary alone silently ignores the rest — which
        is how a challenge page that also carried `bad_status` escaped
        escalation for months.
        """
        reasons = {str(key) for detail in result.failure_details for key in detail}
        if result.failure_reason:
            reasons.add(str(result.failure_reason))
        return reasons

    def _is_challenge(self, result: ScrapeResult) -> bool:
        return bool(self._failure_reasons(result) & self.CHALLENGE_REASONS)

    def _browser_may_recover(self, result: ScrapeResult) -> bool:
        reasons = self._failure_reasons(result)
        # A challenge beats the rate-limit exclusion: a WAF interstitial served
        # as 429/503 is a block wearing a throttle's status code.
        if reasons & self.CHALLENGE_REASONS:
            return True
        status = result.status_code or 0
        if status in RATE_LIMIT_STATUSES:
            return False
        if FailureReason.REQUEST_ERROR.value in reasons and self._looks_unreachable(result):
            return False
        if reasons & self.BROWSER_RECOVERABLE_REASONS:
            return True
        # 403 without a recognized block signature is still usually an
        # anti-bot rejection of the HTTP client, not a real permission wall.
        return status == 403

    @staticmethod
    def _failure_message(result: ScrapeResult) -> str:
        """Human-diagnosable failure text — reason plus the recorded details.

        The old `str(failure_reason)` produced page_failed events that said
        only "request_error", which made whole failed crawls undiagnosable
        from the durable event log.
        """
        parts: list[str] = []
        for detail in result.failure_details:
            for key, value in detail.items():
                text = str(value).strip()
                parts.append(f"{key}: {text}" if text and text != str(key) else str(key))
        base = result.failure_reason or "scrape returned success=False"
        if not parts:
            return str(base)
        return f"{base} — " + "; ".join(parts[:5])

    def _is_thin(self, result: ScrapeResult) -> bool:
        text = (
            result.text_data
            or result.ai_research_content
            or result.ai_content
            or result.raw_text
            or ""
        )
        return len(text.split()) < 200

    def _estimate_bytes(self, result: ScrapeResult) -> int:
        # Rough estimate — the orchestrator doesn't surface byte size today.
        if isinstance(result.raw_body, bytes):
            return len(result.raw_body)
        text = result.raw_body or result.text_data or result.ai_content or result.raw_text or ""
        return len(text.encode("utf-8", errors="ignore"))

    async def _enqueue_links(self, summary: PageSummary, parent: QueueItem) -> None:
        # In list mode the user wants ONLY the URLs they provided.
        if self.config.list_mode:
            return
        if self.config.max_depth is not None and parent.depth >= self.config.max_depth:
            return
        queue_depth, _ = await self.queue.counts()
        if self._pages_fetched + queue_depth >= self.config.max_pages:
            return
        links = [link.target_url for link in summary.links]
        await self._classify_and_enqueue_batch(
            links,
            depth=parent.depth + 1,
            parent_url=parent.url,
            source="link",
        )

    async def _classify_and_enqueue_batch(
        self,
        raw_urls: list[str],
        *,
        depth: int,
        parent_url: str | None,
        source: str,
    ) -> int:
        """Classify a whole page's URL set and enqueue the survivors.

        ONE pass, ONE known-URL lookup, ONE enqueue, ONE event — regardless of
        how many links the page carries. See CrawlUrlsClassifiedEvent for why
        the per-link shape is forbidden.
        """
        if not raw_urls:
            return 0

        decisions: list[UrlDecision] = []
        # normalized url -> the raw url it came from (first wins, so the ledger
        # records the anchor the crawler actually followed).
        candidates: dict[str, str] = {}
        for raw in raw_urls:
            try:
                norm = _normalise_url(urljoin(parent_url, raw) if parent_url else raw)
            except Exception as exc:
                decisions.append(
                    UrlDecision(
                        raw_url=raw,
                        depth=depth,
                        source=source,  # type: ignore[arg-type]
                        classification="invalid",
                        outcome="skipped",
                        reason_code="invalid_url",
                        reason=str(exc),
                    )
                )
                continue
            classification, outcome, reason_code = self._classify_pure(norm, depth)
            if reason_code != "accepted":
                decisions.append(
                    UrlDecision(
                        raw_url=raw,
                        normalized_url=norm,
                        depth=depth,
                        source=source,  # type: ignore[arg-type]
                        classification=classification,
                        outcome=outcome,  # type: ignore[arg-type]
                        reason_code=reason_code,
                    )
                )
                continue
            if norm in candidates:
                continue
            candidates[norm] = raw

        # ONE round-trip for the whole page's surviving candidate set.
        already_known = await self.queue.known_urls(list(candidates))
        to_enqueue: list[QueueItem] = []
        for norm, raw in candidates.items():
            if norm in already_known:
                decisions.append(
                    UrlDecision(
                        raw_url=raw,
                        normalized_url=norm,
                        depth=depth,
                        source=source,  # type: ignore[arg-type]
                        classification="internal",
                        outcome="duplicate",
                        reason_code="already_known",
                    )
                )
                continue
            to_enqueue.append(QueueItem(norm, depth, parent_url, source))

        accepted_items = await self.queue.enqueue_many(to_enqueue)
        accepted_urls = {item.url for item in accepted_items}
        for item in to_enqueue:
            raw = candidates[item.url]
            landed = item.url in accepted_urls
            decisions.append(
                UrlDecision(
                    raw_url=raw,
                    normalized_url=item.url,
                    depth=depth,
                    source=source,  # type: ignore[arg-type]
                    classification="internal",
                    outcome="accepted" if landed else "duplicate",
                    is_in_scope=True,
                    reason_code="accepted" if landed else "enqueue_race_duplicate",
                )
            )
        self._pages_discovered += len(accepted_items)

        by_reason: dict[str, int] = {}
        for decision in decisions:
            by_reason[decision.reason_code] = by_reason.get(decision.reason_code, 0) + 1
        await self._emit(
            CrawlUrlsClassifiedEvent(
                run_id=self.run_id,
                parent_url=parent_url,
                depth=depth,
                source=source,  # type: ignore[arg-type]
                total=len(decisions),
                accepted=len(accepted_items),
                by_reason=by_reason,
                decisions=decisions,
            )
        )
        return len(accepted_items)

    def _classify_pure(self, url: str, depth: int) -> tuple[str, str, str]:
        """Scope decision with NO backend lookup — (classification, outcome, reason_code).

        Deliberately excludes the already-known test: that is the only check
        needing a backend round-trip, so it is hoisted out and done in bulk.
        Cheap rejects run first, which also shrinks the bulk lookup set.

        `outcome` is returned explicitly, never derived from `classification` —
        an out-of-scope URL is an `excluded` outcome while an unparseable one is
        `skipped`, and deriving that mapping silently reclassified every
        external link in the crawl ledger.
        """
        if not url.startswith(("http://", "https://")):
            return "invalid", "skipped", "unsupported_scheme"
        if not _is_same_host(url, self.base_host, self.config.follow_subdomains):
            return "external", "excluded", "outside_site_scope"
        if self.config.max_depth is not None and depth > self.config.max_depth:
            return "excluded", "excluded", "max_depth"
        path = urlparse(url).path or "/"
        if self._exclude and any(p.search(path) for p in self._exclude):
            return "excluded", "excluded", "exclude_pattern"
        if self._include and not any(p.search(path) for p in self._include):
            return "excluded", "excluded", "include_pattern_miss"
        return "internal", "skipped", "accepted"

    async def _should_enqueue(self, url: str, depth: int) -> bool:
        accepted, _, _, _ = await self._classify_enqueue(url, depth)
        return accepted

    async def _classify_enqueue(
        self,
        url: str,
        depth: int,
    ) -> tuple[bool, str, str, str]:
        """Single-URL classification — for one-off callers only.

        Bulk paths MUST use `_classify_and_enqueue_batch`; this issues a
        backend round-trip per URL and is not safe to call in a link loop.
        """
        classification, outcome, reason_code = self._classify_pure(url, depth)
        if reason_code != "accepted":
            return False, classification, outcome, reason_code
        if await self.queue.is_known(url):
            return False, "internal", "duplicate", "already_known"
        return True, "internal", "skipped", "accepted"

    async def _emit_url_decision(
        self,
        raw_url: str,
        *,
        depth: int,
        parent_url: str | None,
        source: str,
        classification: str,
        outcome: str,
        reason_code: str,
        normalized_url: str | None = None,
        reason: str | None = None,
    ) -> None:
        await self._emit(
            CrawlUrlClassifiedEvent(
                run_id=self.run_id,
                raw_url=raw_url,
                normalized_url=normalized_url,
                depth=depth,
                parent_url=parent_url,
                source=source,  # type: ignore[arg-type]
                classification=classification,  # type: ignore[arg-type]
                outcome=outcome,  # type: ignore[arg-type]
                is_in_scope=classification == "internal",
                reason_code=reason_code,
                reason=reason,
            )
        )

    async def _emit(self, event: CrawlEvent) -> None:
        try:
            await self.event_sink.emit(event)
        except Exception:
            if self.strict_persistence:
                logger.exception("event sink raised — aborting strict crawl")
                raise
            logger.exception("event sink raised — continuing non-strict crawl")

    async def _maybe_emit_progress(self) -> None:
        now = time.monotonic()
        every_n = max(1, self.config.progress_every_n_pages)
        # Gate on "have N pages completed SINCE the last emit", never on
        # `pages_fetched % N == 0`. The modulo form is a level test on a value
        # the run loop re-reads every 100ms, so a fetch count that merely SITS
        # on a multiple of N emits ~10 events/second for as long as it sits
        # there — flooding the event sink's ordering lock and starving the
        # crawl itself. This is an edge test: it can only fire on advance.
        emit_due_to_count = (self._pages_fetched - self._progress_emitted_at_pages) >= every_n
        emit_due_to_time = (now - self._last_progress_at) >= max(
            1.0, self.config.progress_every_seconds
        )
        if not (emit_due_to_count or emit_due_to_time):
            return
        self._last_progress_at = now
        self._progress_emitted_at_pages = self._pages_fetched
        progress_queue_depth, progress_in_flight = await self.queue.counts()
        elapsed = int((now - (self._started_at or now)) * 1000)
        await self._emit(
            CrawlProgressEvent(
                run_id=self.run_id,
                pages_discovered=self._pages_discovered,
                pages_fetched=self._pages_fetched,
                pages_failed=self._pages_failed,
                pages_in_flight=progress_in_flight,
                queue_depth=progress_queue_depth,
                bytes_downloaded=self._bytes_downloaded,
                elapsed_ms=elapsed,
            )
        )

    def _build_summary(
        self,
        result: ScrapeResult,
        item: QueueItem,
        response_ms: int,
        bytes_total: int,
        page_id: str | None,
    ) -> PageSummary:
        """Build the typed page summary using the canonical SEO audit.

        Re-parses the raw HTML through `seo_audit.audit_html` so the crawler's
        output matches the chrome-extension audit field-for-field (audit.ts).
        Falls back to the orchestrator's already-parsed metadata when raw HTML
        is unavailable (non-HTML content, cache hit, etc.).
        """
        final_url = result.response_url or item.url

        # Redirect chain — the real multi-hop chain captured by the transport
        # (curl_cffi manual walk, httpx response.history, Playwright
        # redirected_from). Every transport now records hops, so a missing
        # chain means an older cache hit or a transport bug. The fallback
        # synthesis records status=None for the unknown hop — NEVER a
        # fabricated 301 (the old synthesis stamped real 302/307/308 and
        # browser redirects as 301, which is a lie in the evidence record).
        redirect_chain: list[dict[str, Any]] = list(result.redirect_chain or [])
        if not redirect_chain:
            if final_url != item.url:
                redirect_chain = [
                    {"status": None, "url": item.url},
                    {"status": result.status_code or None, "url": final_url},
                ]
            else:
                redirect_chain = [{"status": result.status_code or None, "url": item.url}]

        if result.raw_html:
            audit = audit_html(result.raw_html, final_url)
            return PageSummary(
                url=item.url,
                final_url=final_url,
                http_status=result.status_code or None,
                mime_type=result.content_type,
                title=audit.title or result.title,
                meta_description=audit.meta_description,
                meta_robots=audit.robots,
                canonical_url=audit.canonical,
                lang=audit.lang,
                h1=audit.h1,
                h2=audit.h2,
                h1_count=audit.h1_count,
                headings_full=[HeadingEntry(level=h.level, text=h.text) for h in audit.headings],
                hreflang=[HreflangEntry(lang=h.lang, href=h.href) for h in audit.hreflang],
                head_meta={"viewport": audit.viewport, "refresh": audit.meta_refresh},
                og_tags=audit.og,
                twitter_tags=audit.twitter,
                schema_org=audit.schema_org,
                schema_types=audit.schema_types,
                structured_data=audit.structured_data,
                page_identity={
                    **audit.page_identity,
                    "cms": result.cms or audit.page_identity.get("cms"),
                    "published_at": result.published_at or audit.page_identity.get("published_at"),
                    "modified_at": result.modified_at or audit.page_identity.get("modified_at"),
                },
                word_count=audit.word_count,
                sentence_count=audit.sentence_count,
                flesch_reading_ease=audit.flesch_reading_ease,
                text_bytes=audit.text_bytes,
                text_hash=audit.text_hash,
                content_fingerprint=audit.content_fingerprint,
                internal_links=audit.internal_links,
                external_links=audit.external_links,
                link_count=audit.link_count,
                images_count=audit.images_total,
                images_missing_alt=audit.images_missing_alt,
                image_inventory=audit.image_inventory,
                resources=audit.resources,
                links=[
                    LinkEntry(
                        target_url=link.target_url,
                        anchor_text=link.anchor_text,
                        rel=link.rel,
                        link_type=link.link_type,  # type: ignore[arg-type]
                        nofollow=link.nofollow,
                    )
                    for link in audit.links
                ],
                mixed_content=audit.mixed_content,
                response_headers=result.security_headers,
                redirect_chain=redirect_chain,
                pagination=audit.pagination,
                response_time_ms=response_ms,
                # From the transport, NOT the wall clock above: `response_ms`
                # times the whole scrape (fetch + parse), `ttfb_ms` is the
                # server's own response latency. None when unmeasured.
                ttfb_ms=result.ttfb_ms,
                bytes=bytes_total,
                depth=item.depth,
                page_id=page_id,
            )

        # Fallback path — no raw HTML (non-HTML content, cached fetch, etc.)
        meta = result.metadata if isinstance(result.metadata, dict) else {}
        title = result.title or (meta.get("title") if isinstance(meta, dict) else None) or ""
        meta_desc = meta.get("description") if isinstance(meta, dict) else None
        canonical = meta.get("canonical") if isinstance(meta, dict) else None
        robots = meta.get("robots") if isinstance(meta, dict) else None
        text = result.text_data or result.ai_content or result.raw_text or ""
        word_count = len(text.split()) if text else 0
        sentence_count = len([s for s in text.split(". ") if s.strip()]) if text else 0
        fingerprint = compute_text_fingerprint(text)

        internal_links = 0
        external_links = 0
        if result.links and isinstance(result.links, dict):
            internal_links = len(result.links.get("internal") or [])
            external_links = len(result.links.get("external") or [])
        images_count = 0
        images_missing_alt = 0
        if isinstance(result.images, list):
            images_count = len(result.images)
            for img in result.images:
                if isinstance(img, dict) and not (img.get("alt") or "").strip():
                    images_missing_alt += 1
        image_inventory = [image for image in (result.images or []) if isinstance(image, dict)][
            :IMAGE_INVENTORY_LIMIT
        ]
        resource_items: list[dict[str, Any]] = []
        resource_counts: dict[str, int] = {}
        if isinstance(result.links, dict):
            for result_key, kind in (
                ("images", "image"),
                ("videos", "video"),
                ("audio", "audio"),
                ("documents", "document"),
                ("archives", "archive"),
                ("others", "other"),
            ):
                values = result.links.get(result_key) or []
                if not isinstance(values, list):
                    continue
                for value in values:
                    if not isinstance(value, str):
                        continue
                    resource_items.append(
                        {
                            "kind": kind,
                            "url": value,
                            "tag": "unknown",
                            "source_attribute": "unknown",
                        }
                    )
                    resource_counts[kind] = resource_counts.get(kind, 0) + 1

        return PageSummary(
            url=item.url,
            final_url=final_url,
            http_status=result.status_code or None,
            mime_type=result.content_type,
            title=title,
            meta_description=meta_desc if isinstance(meta_desc, str) else None,
            canonical_url=canonical if isinstance(canonical, str) else None,
            meta_robots=robots if isinstance(robots, str) else None,
            word_count=word_count or None,
            sentence_count=sentence_count or None,
            internal_links=internal_links,
            external_links=external_links,
            link_count=internal_links + external_links,
            images_count=images_count,
            images_missing_alt=images_missing_alt,
            image_inventory=image_inventory,
            resources={
                "count": len(resource_items),
                "counts": resource_counts,
                "items": resource_items,
                "truncated": False,
            },
            structured_data={
                "schema_types": [],
                "schema_org": {},
                "json_ld": [],
                "json_ld_raw": result.structured_data
                if isinstance(result.structured_data, list)
                else [],
                "microdata": [],
                "rdfa": [],
                "microformats": [],
                "blocks": [],
                "parse_errors": [],
            },
            page_identity={
                "cms": result.cms,
                "featured_image": result.main_image,
                "published_at": result.published_at,
                "modified_at": result.modified_at,
            },
            response_time_ms=response_ms,
            ttfb_ms=result.ttfb_ms,
            bytes=bytes_total,
            depth=item.depth,
            page_id=page_id,
            text_hash=fingerprint["exact_sha256"] if fingerprint else None,
            content_fingerprint=fingerprint,
            redirect_chain=redirect_chain,
            response_headers=result.security_headers,
        )


# ---------------------------------------------------------------------------
# Convenience function — preserves the legacy signature for callers that just
# want a results dict back.
# ---------------------------------------------------------------------------


async def crawl_site(
    seed_url: str,
    *,
    max_pages: int = 200,
    concurrency: int = 8,
    max_depth: int | None = None,
    follow_subdomains: bool = False,
    respect_robots: bool = True,
    seed_from_sitemap: bool = True,
    user_agent: str = "MatrxScraperBot/0.1 (+https://aimatrx.com)",
    user_agent_override: str | None = None,
    include_patterns: list[str] | None = None,
    exclude_patterns: list[str] | None = None,
    render_mode: str = RENDER_HTTP_FIRST,
    event_sink: CrawlEventSink | None = None,
    queue_backend: QueueBackend | None = None,
    body_persister: BodyPersister | None = None,
    cache: Any = None,
    domain_config: Any = None,
    browser_pool: Any = None,
    run_id: str | None = None,
) -> dict[str, ScrapeResult]:
    """Crawl an entire website and return all parsed results.

    For long-running crawls (>~500 pages) prefer driving SiteCrawler directly
    so you can persist results and progress as they arrive.
    """
    import uuid as _uuid

    cfg = SiteCrawlerConfig(
        base_url=seed_url,
        max_pages=max_pages,
        max_depth=max_depth,
        concurrency=concurrency,
        follow_subdomains=follow_subdomains,
        respect_robots=respect_robots,
        seed_from_sitemap=seed_from_sitemap,
        user_agent=user_agent,
        user_agent_override=user_agent_override,
        include_patterns=include_patterns or [],
        exclude_patterns=exclude_patterns or [],
        render_mode=render_mode,
    )
    crawler = SiteCrawler(
        run_id=run_id or str(_uuid.uuid4()),
        config=cfg,
        event_sink=event_sink,
        queue_backend=queue_backend,
        body_persister=body_persister,
        cache=cache,
        domain_config=domain_config,
        browser_pool=browser_pool,
    )
    return await crawler.run()


__all__ = [
    "SiteCrawler",
    "SiteCrawlerConfig",
    "CrawlEventSink",
    "PersistRequest",
    "PersistResult",
    "BodyPersister",
    "crawl_site",
    "RENDER_HTTP_ONLY",
    "RENDER_HTTP_FIRST",
    "RENDER_BROWSER_ALWAYS",
    "RENDER_BROWSER_WITH_SCREENSHOT",
    "VALID_RENDER_MODES",
]
