"""Cheap URL verification — fills `web.page.http_status_last` / `content_type_last`
for registry rows NOTHING has ever fetched.

`web.page` is an anchor registry: sitemap sync and Google Search Console declare
URLs into it without fetching them. On 2026-08-11 that left **7,423 of 10,424
live rows** (4,511 sitemap-declared, 3,607 GSC-declared) with BOTH status columns
NULL — the registry knew those URLs existed and knew nothing else about them.

Two things were broken by that silence, and both are fixed by filling the columns
rather than by any new logic:

1. **Classification leaned on URL shape alone.** `matrx_utils.web_page_class`
   reads two signals — the recorded content type and the URL's shape — and the
   first was silent for 80% of the registry.

2. **A sitemap full of dead URLs was undetectable.** The catalogue check
   `sitemap_health` (weight 2.0) has ALWAYS promised the band ">10% of sitemap
   URLs are non-200, redirected, noindexed or robots-blocked", and
   `site_analysis._load_sitemap_membership` has ALWAYS classified junk off
   `page.http_status_last`. With that column NULL those URLs fell into
   `undiscovered` — "we haven't looked" — so the check scored the small fetched
   subset and reported a clean sitemap for a site whose sitemap was full of 404s.
   **This module writes no findings. It supplies the evidence the existing check
   was already written to consume.**

**A verification is not a capture.** It issues HEAD (falling back to a ranged GET
for the many servers that answer HEAD with 403/405) and reads the response line
and headers. No body, no parse, no `web.snapshot` row — snapshots are immutable
append-only facts about a CAPTURE (`web.reject_immutable_fact_mutation`), and
minting one from a header-only probe would be a lie in the fact table. A page
that needs content still needs a crawl; this only answers "does this URL answer,
and with what".

**Redirects are followed, and `http_status_last` records the FINAL status** —
exactly what the crawler records, because one column may not mean two things
depending on which writer touched it. The hop that a redirect represents is kept
as evidence in `page.metadata['url_verification']`, which is where the
"this sitemap URL redirects" finding reads it from.

**Durability** follows the platform standard
(`common-docs/policies/durable-work-queue-standard.md`): the frontier is
`runtime.work_item` rows scoped to one batch `global_execution`, claimed
`FOR UPDATE SKIP LOCKED` under a lease. Process death is a non-event — the
reaper returns expired leases to pending and a resumed run claims the same
frontier (the execution is found by link, never recreated). Nothing about
progress lives in process memory.

**Writes never clobber a crawl.** Every persist is a compare-and-swap guarded on
`http_status_last IS NULL`: a real crawl that landed while the sweep was in
flight always wins, and the sweep silently declines to overwrite it.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Protocol
from urllib.parse import urlsplit

import httpx
from matrx_orm import JsonbMerge
from matrx_utils import utcnow

from matrx_scraper.db.models_web import (
    GscPageStat as WebGscPageStat,
    Page as WebPage,
    PageSitemap as WebPageSitemap,
)
from matrx_scraper.robots_txt import ROBOTS_MAX_BYTES, RobotsDocument, parse_robots_txt
from matrx_scraper.scraper import content_type_from_header
from matrx_scraper.utils.url import url_match_key, validate_public_http_url

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# CAPS constants. Changing behaviour is a code push, never an env var.

#: Where a verification's own evidence lands on the page row.
VERIFICATION_METADATA_KEY = "url_verification"
#: Bump when the stored shape changes; an older record is IGNORED rather than
#: misread (the same rule `site_probe` follows).
VERIFICATION_FORMAT_VERSION = 1

#: Written to `content_type_last` when a response arrived but said nothing usable
#: about its type. Distinct from NULL ("nobody has ever looked") and treated as
#: no-signal by `web_page_class.UNKNOWN_CONTENT_TYPES` — recording ignorance as a
#: verdict is how a real page gets hidden from its own audit.
UNKNOWN_CONTENT_TYPE = "unknown"

#: Recorded when no response ever arrived (DNS failure, TLS error, timeout,
#: connection reset). Mirrors `link_check`'s convention so "dead host" reads as
#: broken, never as unchecked.
NO_RESPONSE_STATUS = 0

REQUEST_TIMEOUT_SECONDS = 15.0
USER_AGENT = "MatrxScraperBot/url-verify (+https://aimatrx.com)"
#: HEAD is wildly inconsistently supported. These say "this host dislikes HEAD",
#: not "this URL is broken", so they earn the GET fallback.
HEAD_FALLBACK_STATUSES = frozenset({400, 401, 403, 405, 406, 409, 501, 502})
#: The GET fallback asks for the first byte only. A server that honours it sends
#: 206 and one byte; one that ignores it sends 200 and a body we never read
#: (the response is streamed and closed at the headers).
RANGE_HEADER = {"Range": "bytes=0-0"}

DEFAULT_GLOBAL_CONCURRENCY = 8
#: Minimum gap between two requests to one host. 0.25s = 4 rps, the
#: `HostRateLimiter` class default, for a header-only probe that costs a
#: fraction of a full page fetch.
#:
#: This sweep does NOT ramp. The crawler does (`host_pacing.py`, Arman
#: 2026-08-20) and its limiter now OPENS at the pacing floor, so this constant no
#: longer mirrors what a crawl actually does. It stays because a host that ever
#: pushes back still slows this sweep down: `slot()` divides its interval by the
#: process-wide throttle factor, which the crawler records on every 429 —
#: cross-lane learning is the protection here, not a lower constant.
#: Deliberately not slower: at 2 rps a 3,400-URL sitemap takes half an hour and
#: the sweep stops being cheap enough to run.
DEFAULT_PER_HOST_SPACING_SECONDS = 0.25
ITEM_MAX_ATTEMPTS = 5
RETRY_BACKOFF_SECONDS = 30.0
#: How many items one claim pulls. Small enough that a crashed worker strands
#: little and the lease below stays short, large enough to keep the round-trip
#: count sane.
CLAIM_BATCH_SIZE = 5

#: Worst case for ONE item: a HEAD that burns its full timeout, then the GET
#: fallback burning its own.
_WORST_CASE_ITEM_SECONDS = 2 * REQUEST_TIMEOUT_SECONDS

#: Lease per claimed BATCH — DERIVED, never a hand-picked number.
#:
#: A claim leases every item in the batch from the moment it is taken, but the
#: last item is not touched until the ones ahead of it finish. The lease must
#: therefore cover the whole batch's worst case, not one item's. Hardcoded at
#: 120s against a 20-item batch it did not: on allgreenrecycling.com (a site
#: answering 500s and timeouts) leases expired under live workers, the reaper
#: re-issued the items, and the sweep logged a stream of lost settle-CAS
#: warnings. Nothing was lost — the persist compare-and-swap made the duplicate
#: work harmless and the alarm is exactly what it is for — but the work was
#: wasted, and the cause was two constants that could drift apart. Now they
#: cannot: change either one and the lease follows.
#: 3x headroom covers scheduler jitter and pool contention.
ITEM_LEASE_SECONDS = int(CLAIM_BATCH_SIZE * _WORST_CASE_ITEM_SECONDS * 3)

#: Statuses that mean "ask again later" — the answer is about the moment, not the
#: URL. Everything else (including every 4xx) is a TERMINAL answer and is
#: recorded as the truth about that URL.
RETRYABLE_STATUSES = frozenset({408, 425, 429, 500, 502, 503, 504})

_SEED_SCAN_BATCH = 1_000
ROBOTS_PATH = "/robots.txt"
#: How often a streaming caller hears about progress, in URLs checked.
PROGRESS_EVERY = 25

#: How long a worker waits before re-checking for items released from a
#: `not_before` retry backoff. Comfortably under RETRY_BACKOFF_SECONDS.
IDLE_POLL_SECONDS = 5.0
#: Hard ceiling on ONE run's wall clock. Reaching it is not data loss — every
#: unfinished item stays PENDING and durable — but it must be said out loud,
#: never reported as a completed sweep.
MAX_DRAIN_SECONDS = 3_600.0

#: Called with the running summary so a streaming caller can report live counts.
ProgressCallback = Callable[["VerificationSummary"], Awaitable[None]]


class _FrontierStore(Protocol):
    """The slice of `matrx_runtime.ExecutionStore` this sweep needs.

    Declared structurally so the sweep is testable against the in-memory store
    (and so matrx-runtime stays an optional dependency of this package).
    """

    async def seed_work_items(
        self, execution_id: str, seeds: Any, *, now: datetime
    ) -> list[str]: ...
    async def claim_work_items(
        self, execution_id: str, *, holder: str, lease_seconds: int, limit: int, now: datetime
    ) -> list[Any]: ...
    async def complete_work_item(self, item_id: str, *, holder: str, now: datetime) -> bool: ...
    async def fail_work_item(
        self,
        item_id: str,
        *,
        holder: str,
        error: Any,
        retry: bool,
        backoff_seconds: float,
        now: datetime,
    ) -> Any: ...
    async def work_item_counts(self, execution_id: str) -> dict[Any, int]: ...


@dataclass
class VerificationSummary:
    """What one sweep run did. Every number is derived from work the run
    actually performed — never from the size of the frontier it hoped to do.

    🚨 **Two different units live here; do not read one as the other.**

    `checked` / `ok` / `broken` / `redirected` / `by_content_type` count
    **RESPONSES**, and a retryable answer is retried, so one URL can contribute
    several. `seeded` / `persisted` / `terminal_failures` count **URLs**.

    This is not pedantry — it misled its own author on the first live run:
    vasaro.com reported `broken=1089` and it read as "1,089 broken pages". The
    real number was **25** URLs that ever failed terminally; the rest were one
    host handing out 429s that later succeeded on retry. `terminal_failures` is
    the number a human actually wants.
    """

    seeded: int = 0
    #: RESPONSES received, retries included.
    checked: int = 0
    #: URLs whose answer was recorded on the page row.
    persisted: int = 0
    ok: int = 0
    broken: int = 0
    #: URLs PERSISTED with a failing status (>=400, or 0 = no response at all).
    #: The honest "this many URLs are actually broken" count.
    terminal_failures: int = 0
    redirected: int = 0
    redirected_materially: int = 0
    unreachable: int = 0
    unknown_content_type: int = 0
    robots_skipped: int = 0
    ssrf_rejected: int = 0
    retried: int = 0
    lost_to_crawl: int = 0
    by_content_type: dict[str, int] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "seeded": self.seeded,
            "checked": self.checked,
            "persisted": self.persisted,
            "terminal_failures": self.terminal_failures,
            "ok": self.ok,
            "broken": self.broken,
            "redirected": self.redirected,
            "redirected_materially": self.redirected_materially,
            "unreachable": self.unreachable,
            "unknown_content_type": self.unknown_content_type,
            "robots_skipped": self.robots_skipped,
            "ssrf_rejected": self.ssrf_rejected,
            "retried": self.retried,
            "lost_to_crawl": self.lost_to_crawl,
            "by_content_type": dict(self.by_content_type),
        }


@dataclass
class VerificationOutcome:
    """One URL's answer. `retryable` is the only field the queue reads."""

    url: str
    http_status: int
    content_type: str | None
    final_url: str
    redirected: bool
    hop_status: int | None = None
    method: str = "HEAD"
    error: str | None = None
    retryable: bool = False

    @property
    def redirect_is_material(self) -> bool:
        """True only when the redirect went somewhere genuinely ELSE.

        `normalize_url` — our stored identity — strips the trailing slash, so on
        a site that serves the slash form EVERY stored URL 301s to itself. That
        redirect is a fact about OUR url form, not about the site: reporting it
        would tell a customer their whole sitemap is broken when nothing is.
        The durable-work-queue Identity Contract says exactly this — "a redirect
        is not reported as a finding until we have confirmed we requested the
        canonical form" — and we did not.

        `url_match_key` is the existing alias matcher (scheme/www/slash
        insensitive), so this reuses the platform's one definition of "the same
        URL in a different dress" instead of inventing a second.

        Live proof (www.pbw-law.com, 2026-08-11): 422 of 429 URLs "redirected",
        every one of them a bare trailing-slash 301 to itself.
        """
        if not self.redirected:
            return False
        return url_match_key(self.final_url) != url_match_key(self.url)


def classify_status(status: int) -> bool:
    """True when this status means "ask again later", not "this is the answer"."""
    return status in RETRYABLE_STATUSES


class PoliteVerifier:
    """Bounded, polite, SSRF-checked HEAD→ranged-GET prober.

    Politeness matches the crawler's contract rather than reinventing it: a
    global concurrency ceiling, per-host serialization with a minimum spacing,
    and `validate_public_http_url` immediately before every request so a
    DNS-rebound or literal-IP target cannot reach an internal address.
    """

    def __init__(
        self,
        http: httpx.AsyncClient,
        *,
        concurrency: int = DEFAULT_GLOBAL_CONCURRENCY,
        per_host_spacing_s: float = DEFAULT_PER_HOST_SPACING_SECONDS,
    ) -> None:
        self._http = http
        self._global = asyncio.Semaphore(concurrency)
        self._spacing_s = per_host_spacing_s
        self._host_locks: dict[str, asyncio.Lock] = {}
        self._host_last: dict[str, float] = {}

    async def verify(self, url: str) -> VerificationOutcome:
        host = urlsplit(url).netloc.lower()
        lock = self._host_locks.setdefault(host, asyncio.Lock())
        async with self._global:
            async with lock:
                elapsed = time.monotonic() - self._host_last.get(host, 0.0)
                if elapsed < self._spacing_s:
                    await asyncio.sleep(self._spacing_s - elapsed)
                try:
                    return await self._probe(url)
                finally:
                    self._host_last[host] = time.monotonic()

    async def _probe(self, url: str) -> VerificationOutcome:
        # Re-validated per request, not once at seed time: DNS can change under
        # us, and this is the last moment before bytes leave the box.
        try:
            await validate_public_http_url(url)
        except ValueError as exc:
            return VerificationOutcome(
                url=url,
                http_status=NO_RESPONSE_STATUS,
                content_type=None,
                final_url=url,
                redirected=False,
                method="none",
                error=f"rejected before request: {exc}",
                retryable=False,
            )

        head_error: str | None = None
        try:
            response = await self._http.head(url)
            if response.status_code not in HEAD_FALLBACK_STATUSES:
                return self._outcome(url, response, "HEAD")
        except httpx.HTTPError as exc:
            head_error = f"{type(exc).__name__}: {exc}"

        try:
            async with self._http.stream("GET", url, headers=RANGE_HEADER) as response:
                # Headers are already in hand here; the body is never read and
                # the connection closes on exit. That is the whole point.
                return self._outcome(url, response, "GET")
        except httpx.HTTPError as exc:
            message = f"{type(exc).__name__}: {exc}"
            if head_error is not None:
                message = f"HEAD {head_error}; GET {message}"
            logger.info("url verify: no response from %s (%s)", url, message)
            return VerificationOutcome(
                url=url,
                http_status=NO_RESPONSE_STATUS,
                content_type=None,
                final_url=url,
                redirected=False,
                method="GET",
                error=message,
                # A transport failure is a moment, not a verdict — but the
                # attempt budget stops it from retrying forever.
                retryable=True,
            )

    @staticmethod
    def _outcome(url: str, response: httpx.Response, method: str) -> VerificationOutcome:
        token = content_type_from_header(response.headers.get("content-type"))
        history = list(response.history)
        return VerificationOutcome(
            url=url,
            http_status=response.status_code,
            content_type=str(token) if token is not None else None,
            final_url=str(response.url),
            redirected=bool(history),
            hop_status=history[0].status_code if history else None,
            method=method,
            retryable=classify_status(response.status_code),
        )


async def load_site_robots(http: httpx.AsyncClient, root_url: str) -> RobotsDocument | None:
    """The site's robots.txt, or None when it could not be read.

    None means "no rules known", and the sweep then verifies everything —
    robots.txt is a deny list, so an unreadable one may never invent a block
    (the same fail-open rule `RobotsDocument.is_allowed` follows).
    """
    parts = urlsplit(root_url)
    if not parts.scheme or not parts.netloc:
        return None
    robots_url = f"{parts.scheme}://{parts.netloc}{ROBOTS_PATH}"
    try:
        await validate_public_http_url(robots_url)
        response = await http.get(robots_url)
    except (httpx.HTTPError, ValueError) as exc:
        logger.info("url verify: robots.txt unreadable at %s (%s)", robots_url, exc)
        return None
    if response.status_code >= 400:
        return None
    return parse_robots_txt(response.text[:ROBOTS_MAX_BYTES])


# ---------------------------------------------------------------------------
# Phase 1 — durable seeding


async def collect_unverified_pages(site_id: str, *, limit: int) -> list[dict[str, Any]]:
    """Never-fetched live page rows for one site, PRIORITIZED.

    Order matters because the sweep is bounded: a wrong status costs the
    customer traffic only where the URL is actually being offered to Google.

      1. URLs in a sitemap AND carrying GSC impressions — the site asks Google
         to index it and Google is already showing it.
      2. URLs with GSC impressions — Google shows it; if we cannot fetch it,
         that is a live traffic risk.
      3. URLs in a sitemap — the site is advertising it.
      4. Everything else.

    "Never fetched" is BOTH columns NULL. A row with a status but no content
    type has been looked at (see UNKNOWN_CONTENT_TYPE) and is not re-swept.
    """

    rows = await (
        WebPage.filter(
            site_id=site_id,
            deleted_at__isnull=True,
            http_status_last__isnull=True,
            content_type_last__isnull=True,
        )
        .order_by("id")
        .values("id", "url")
    )
    if not rows:
        return []

    page_ids = [str(r["id"]) for r in rows]
    in_sitemap = await _page_ids_in_sitemap(site_id, page_ids)
    impressions = await _gsc_impressions(site_id, page_ids)

    def rank(row: dict[str, Any]) -> tuple[int, int]:
        pid = str(row["id"])
        sitemap = pid in in_sitemap
        shown = impressions.get(pid, 0)
        if sitemap and shown > 0:
            tier = 0
        elif shown > 0:
            tier = 1
        elif sitemap:
            tier = 2
        else:
            tier = 3
        # Within a tier, the most-shown URL first.
        return (tier, -shown)

    ordered = sorted(rows, key=rank)
    return [
        {
            "page_id": str(r["id"]),
            "url": str(r["url"]),
            "in_sitemap": str(r["id"]) in in_sitemap,
            "gsc_impressions": impressions.get(str(r["id"]), 0),
        }
        for r in ordered[:limit]
    ]


async def _page_ids_in_sitemap(site_id: str, page_ids: list[str]) -> set[str]:
    found: set[str] = set()
    for start in range(0, len(page_ids), _SEED_SCAN_BATCH):
        chunk = page_ids[start : start + _SEED_SCAN_BATCH]
        rows = await WebPageSitemap.filter(
            site_id=site_id, deleted_at__isnull=True, page_id__in=chunk
        ).values("page_id")
        found.update(str(r["page_id"]) for r in rows)
    return found


async def _gsc_impressions(site_id: str, page_ids: list[str]) -> dict[str, int]:
    totals: dict[str, int] = {}
    for start in range(0, len(page_ids), _SEED_SCAN_BATCH):
        chunk = page_ids[start : start + _SEED_SCAN_BATCH]
        rows = await WebGscPageStat.filter(
            site_id=site_id, deleted_at__isnull=True, page_id__in=chunk
        ).values("page_id", "impressions")
        for row in rows:
            pid = str(row["page_id"])
            totals[pid] = totals.get(pid, 0) + int(row["impressions"] or 0)
    return totals


# ---------------------------------------------------------------------------
# Persistence


async def persist_verification(page_id: str, outcome: VerificationOutcome) -> bool:
    """Record one answer on the page row. Returns False when a crawl won the race.

    Compare-and-swap on `http_status_last IS NULL`: the sweep only ever fills a
    hole. If a real crawl landed a status while this probe was in flight, the
    crawl's richer answer stands and this write is declined — never overwritten,
    never "merged".
    """

    evidence: dict[str, Any] = {
        "format_version": VERIFICATION_FORMAT_VERSION,
        "checked_at": utcnow().isoformat(),
        "method": outcome.method,
        "http_status": outcome.http_status,
        "content_type": outcome.content_type,
        "redirected": outcome.redirected,
        # The finding-worthy flag. `redirected` alone is dominated by
        # trailing-slash self-redirects — see VerificationOutcome.
        "redirect_material": outcome.redirect_is_material,
        "final_url": outcome.final_url,
    }
    if outcome.hop_status is not None:
        evidence["first_hop_status"] = outcome.hop_status
    if outcome.error is not None:
        evidence["error"] = outcome.error[:500]

    result = await WebPage.update_where(
        {
            "id": page_id,
            "http_status_last__isnull": True,
            "content_type_last__isnull": True,
            "deleted_at__isnull": True,
        },
        http_status_last=outcome.http_status,
        content_type_last=outcome.content_type or UNKNOWN_CONTENT_TYPE,
        last_seen=utcnow(),
        # Merged, never assigned: `metadata` carries other writers' keys and a
        # wholesale SET would silently erase them.
        metadata=JsonbMerge("metadata", {VERIFICATION_METADATA_KEY: evidence}),
    )
    return result.rows_affected > 0


# ---------------------------------------------------------------------------
# Phases 2-5 — the durable worker loop


async def seed_frontier(
    store: _FrontierStore,
    execution_id: str,
    candidates: list[dict[str, Any]],
) -> int:
    """Commit the work set BEFORE any probing starts (standard, phase 1).

    Identity is the page id, not the URL: the registry has already canonicalized
    the URL into that row, and a `UNIQUE (execution_id, canonical_key)` on the
    work item makes a re-seed of the same page impossible at the storage layer
    rather than merely avoided here. Re-running a resumed sweep therefore adds
    nothing and loses nothing.
    """
    from matrx_runtime import WorkItemSeed

    if not candidates:
        return 0
    seeds = [
        WorkItemSeed(
            canonical_key=c["page_id"],
            raw_key=c["url"],
            payload={
                "url": c["url"],
                "in_sitemap": c["in_sitemap"],
                "gsc_impressions": c["gsc_impressions"],
            },
            max_attempts=ITEM_MAX_ATTEMPTS,
        )
        for c in candidates
    ]
    landed = await store.seed_work_items(execution_id, seeds, now=datetime.now(UTC))
    return len(landed)


async def _verify_one(
    item: Any,
    *,
    verifier: PoliteVerifier,
    robots: RobotsDocument | None,
    summary: VerificationSummary,
) -> tuple[bool, str | None]:
    """Probe + persist one claimed item. Returns (settled_ok, retry_error)."""

    payload = item.payload or {}
    url = str(payload.get("url") or item.raw_key or "")
    page_id = str(item.canonical_key)
    if not url:
        return True, None

    if robots is not None and not robots.is_allowed(url, USER_AGENT):
        # Not an error and not a retry: the site told us not to fetch it. The
        # row stays unverified, which is the honest record.
        summary.robots_skipped += 1
        return True, None

    outcome = await verifier.verify(url)
    summary.checked += 1

    if outcome.method == "none":
        summary.ssrf_rejected += 1
    if outcome.http_status == NO_RESPONSE_STATUS:
        summary.unreachable += 1
    elif outcome.http_status >= 400:
        summary.broken += 1
    else:
        summary.ok += 1
    if outcome.redirected:
        summary.redirected += 1
    if outcome.redirect_is_material:
        summary.redirected_materially += 1
    token = outcome.content_type or UNKNOWN_CONTENT_TYPE
    if outcome.content_type is None:
        summary.unknown_content_type += 1
    summary.by_content_type[token] = summary.by_content_type.get(token, 0) + 1

    if outcome.retryable:
        summary.retried += 1
        return False, outcome.error or f"HTTP {outcome.http_status}"

    persisted = await persist_verification(page_id, outcome)
    if persisted:
        summary.persisted += 1
        if outcome.http_status == NO_RESPONSE_STATUS or outcome.http_status >= 400:
            summary.terminal_failures += 1
    else:
        # A real crawl filled the row while we were probing. Correct outcome,
        # worth counting — a high number means the sweep is racing a crawl and
        # should be scheduled apart from it.
        summary.lost_to_crawl += 1
    return True, None


async def run_frontier(
    store: _FrontierStore,
    execution_id: str,
    *,
    holder: str,
    robots: RobotsDocument | None = None,
    concurrency: int = DEFAULT_GLOBAL_CONCURRENCY,
    per_host_spacing_s: float = DEFAULT_PER_HOST_SPACING_SECONDS,
    summary: VerificationSummary | None = None,
    http: httpx.AsyncClient | None = None,
    on_progress: ProgressCallback | None = None,
) -> VerificationSummary:
    """Drain the frontier: claim → probe → persist → settle, until empty.

    Every worker is stateless and interchangeable. Claims are atomic
    (`FOR UPDATE SKIP LOCKED` inside the store) and leased, so two workers never
    take the same item and a worker that dies mid-item strands nothing beyond
    its lease. **Killing this process at any point loses at most the in-flight
    probes** — the frontier and every persisted answer are already in the DB, and
    a resumed run claims exactly what is left.
    """
    from matrx_runtime import ExecutionError, WorkItemState

    summary = summary or VerificationSummary()
    started_at = time.monotonic()
    owns_client = http is None
    client = http or httpx.AsyncClient(
        timeout=REQUEST_TIMEOUT_SECONDS,
        follow_redirects=True,
        headers={"User-Agent": USER_AGENT},
    )
    verifier = PoliteVerifier(
        client, concurrency=concurrency, per_host_spacing_s=per_host_spacing_s
    )

    async def worker(index: int) -> None:
        # Per-claim fencing suffix: a stalled worker's settle must never CAS-match
        # a NEWER claim of the same item after a lease reclaim (the bug the crawl
        # frontier already learned — FOUND_DEFECTS 2026-07-29 F2).
        while True:
            claim_holder = f"{holder}:w{index}:{int(time.monotonic() * 1000)}"
            claimed = await store.claim_work_items(
                execution_id,
                holder=claim_holder,
                lease_seconds=ITEM_LEASE_SECONDS,
                limit=CLAIM_BATCH_SIZE,
                now=datetime.now(UTC),
            )
            if not claimed:
                # An empty claim does NOT mean the job is done — a retryable
                # item sits on a `not_before` backoff and is unclaimable for a
                # while, so exiting here abandons it. The standard is explicit:
                # a job is complete only when zero items are pending AND every
                # retryable failure has exhausted its budget. Skipping this
                # check left titaniummarketing.com at 27 of 64 URLs verified
                # while the run reported success.
                counts = await store.work_item_counts(execution_id)
                outstanding = counts.get(WorkItemState.PENDING, 0) + counts.get(
                    WorkItemState.IN_PROGRESS, 0
                )
                if outstanding == 0:
                    return
                if time.monotonic() - started_at > MAX_DRAIN_SECONDS:
                    # Bounded so one unreachable host cannot pin a worker
                    # forever. The items stay PENDING and durable — the next
                    # run (or the boot resume) claims them.
                    logger.warning(
                        "url verify: worker %d stopping with %d item(s) still "
                        "outstanding after %.0fs — they remain queued and will be "
                        "picked up by the next run, not lost",
                        index,
                        outstanding,
                        MAX_DRAIN_SECONDS,
                    )
                    return
                await asyncio.sleep(IDLE_POLL_SECONDS)
                continue
            for item in claimed:
                try:
                    settled, retry_error = await _verify_one(
                        item, verifier=verifier, robots=robots, summary=summary
                    )
                except Exception as exc:
                    logger.exception("url verify: item %s raised", item.id)
                    settled, retry_error = False, f"{type(exc).__name__}: {exc}"

                if on_progress is not None and summary.checked % PROGRESS_EVERY == 0:
                    await on_progress(summary)

                if settled:
                    ok = await store.complete_work_item(
                        item.id, holder=claim_holder, now=datetime.now(UTC)
                    )
                    if not ok:
                        logger.warning(
                            "url verify: lost the settle CAS for item %s — its lease "
                            "expired and a newer claim owns it (duplicate work "
                            "happened; the persist CAS made it harmless)",
                            item.id,
                        )
                    continue

                state = await store.fail_work_item(
                    item.id,
                    holder=claim_holder,
                    error=ExecutionError(
                        error_type="url_verify_failed", message=str(retry_error)[:2000]
                    ),
                    retry=True,
                    backoff_seconds=RETRY_BACKOFF_SECONDS,
                    now=datetime.now(UTC),
                )
                if state is WorkItemState.DEAD_LETTER:
                    # Exhausted its attempt budget on retryable answers. The URL
                    # stays unverified — say so; a silent dead-letter reads as
                    # "swept clean" when it is not.
                    logger.warning(
                        "url verify: %s dead-lettered after %d attempts — it never "
                        "gave a terminal answer and remains unverified",
                        item.raw_key,
                        ITEM_MAX_ATTEMPTS,
                    )

    try:
        await asyncio.gather(*(worker(i) for i in range(max(1, concurrency))))
    finally:
        if owns_client:
            await client.aclose()
    return summary


__all__ = [
    "CLAIM_BATCH_SIZE",
    "DEFAULT_GLOBAL_CONCURRENCY",
    "HEAD_FALLBACK_STATUSES",
    "ITEM_LEASE_SECONDS",
    "ITEM_MAX_ATTEMPTS",
    "NO_RESPONSE_STATUS",
    "RETRYABLE_STATUSES",
    "UNKNOWN_CONTENT_TYPE",
    "VERIFICATION_METADATA_KEY",
    "PoliteVerifier",
    "VerificationOutcome",
    "VerificationSummary",
    "classify_status",
    "collect_unverified_pages",
    "load_site_robots",
    "persist_verification",
    "run_frontier",
    "seed_frontier",
]
