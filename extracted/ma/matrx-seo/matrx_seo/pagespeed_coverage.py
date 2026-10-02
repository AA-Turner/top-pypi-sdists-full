"""PageSpeed coverage planner — WHICH pages get measured, in what order, within
what budget. Pure domain logic: no DB, no I/O, no clock of its own.

## The problem this solves

PageSpeed Insights is slow (~20-40s per call) and metered against a per-project
daily quota. Measuring every page of every site on every cycle is impossible and
pointless: one 4,400-page site would consume an entire day's budget and starve
the other eleven, and most of those pages get no traffic.

So the planner answers three questions, in this order:

1. **Coverage first.** A page that has NEVER been measured outranks any refresh.
   The goal "every page gets at least one speed test" is only reachable if
   first-ever measurements are never crowded out by re-measuring the homepage.
2. **Importance second.** Within each class, rank by what the site actually
   cares about — real Search Console traffic where we have it, internal-link
   PageRank where we don't, URL depth as the last resort.
3. **Fairness third.** Sites take turns. A per-site cycle cap means the biggest
   site advances by a bounded batch per cycle instead of monopolizing the run.

Rotation needs no cursor: measuring a page stamps `last_measured_at`, which
drops it out of the NEVER class, so the next cycle naturally picks up the next
batch. State lives in the data, not in a pointer that can drift.

That same property is what makes an unauditable page a POISON PILL — it never
gets stamped, so it never leaves the front of the queue. `classify_psi_failure`
is the gate that answers "provider blip or dead page?"; see its section below.

## Strategies — mobile first, deliberately

A first-ever measurement is **mobile only** for every page. Google ranks on
mobile, and mobile-only doubles how far a fixed budget reaches (10.7k pages
instead of 21.4k requests). Desktop is added to important pages on their first
due refresh. `at least one speed test per page` is satisfied by the mobile
pass; desktop is depth, not coverage.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Literal

from matrx_utils.web_page_class import is_machine_resource_url
from pydantic import BaseModel, ConfigDict, Field

Strategy = Literal["mobile", "desktop"]
ImportanceTier = Literal["critical", "high", "normal", "low"]
SelectionReason = Literal["never_measured", "content_changed", "refresh_due"]
PsiFailureKind = Literal["terminal", "transient"]

# ---------------------------------------------------------------------------
# BUDGET — plain module constants, never env vars (root CLAUDE.md: config is
# code, so a missing value can never silently change behavior in production).
# ---------------------------------------------------------------------------

#: Google's keyed PSI quota is 25,000 requests/day/project. We deliberately sit
#: far under it: the same GCP project serves other Google APIs, and on-demand
#: user-triggered runs must never be starved by the background sweep. This is
#: also above what PSI's real throughput can deliver in a day, so the binding
#: constraint stays wall-clock, not quota.
DAILY_REQUEST_BUDGET = 1_500

#: One site's maximum REQUESTS per cycle. The batch size that stops a
#: 4,400-page site from eating the whole budget.
PER_SITE_CYCLE_REQUEST_CAP = 100

#: Refresh cadence per importance tier. A measured page is not re-measured
#: until this much time has passed — unless its content changed.
REFRESH_CADENCE_DAYS: dict[ImportanceTier, int] = {
    "critical": 7,
    "high": 30,
    "normal": 90,
    "low": 180,
}

#: Tiers important enough to also measure on desktop.
DESKTOP_TIERS: frozenset[str] = frozenset({"critical", "high"})

#: Importance percentile cutoffs within a site (fraction ranked at or above).
CRITICAL_PERCENTILE = 0.05
HIGH_PERCENTILE = 0.25

#: Promotion above "low" requires a REAL importance signal — measured traffic,
#: computed PageRank, or being the homepage. Percentile alone is not enough:
#: on a site where 250 pages carry no signal at all, every score is identical
#: and the top 25% is decided by nothing but a tie-break on id. Promoting those
#: spends a second (desktop) request on pages we know nothing about, and halves
#: how far the budget reaches. URL depth orders pages; it never promotes them.
MIN_SCORE_FOR_HIGH = 1.0


# A crawler records every URL it discovers, including assets. PageSpeed can
# only audit a rendered HTML document — pointing it at an image or a sitemap
# burns a request and stores a meaningless score. Measured 2026-08-09: 877 of
# the platform's ~10.5k "active" pages were assets (428 .jpg, 301 .png, 68
# .jpeg, 56 .webp, 21 .pdf, 5 .xml) — 8% of the entire budget, wasted. The
# extension list that used to live here is now matrx_utils.web_page_class,
# shared with matrx-scraper's page-vs-machine-resource gate.

#: `web.page.content_type_last` values that are definitely not an HTML document.
#: It is NULL for most rows (9,411 of 11,505 measured), so it can only ever
#: CONFIRM a rejection — the URL suffix carries the weight.
_NON_HTML_CONTENT_TYPES = frozenset(
    {"image", "json", "xml", "pdf", "css", "js", "md", "txt", "font", "video", "audio"}
)


def is_measurable_page(url: str, content_type: str | None = None) -> bool:
    """Can PageSpeed Insights meaningfully audit this URL?

    Conservative in the RIGHT direction: an extension-less URL is assumed to be
    a page (most real pages have no suffix), so this only ever rejects what it
    positively recognizes as an asset. A wrongly-kept page costs one request; a
    wrongly-dropped page would silently never be covered.
    """
    if content_type:
        # Accepts both the bare tokens the crawler stores ("image", "xml") and
        # a full MIME type ("image/png; charset=..."), so neither shape slips
        # through — real rows contain the former, providers send the latter.
        normalized = content_type.split(";")[0].strip().lower()
        if normalized in _NON_HTML_CONTENT_TYPES:
            return False
        if normalized.split("/", 1)[0] in _NON_HTML_CONTENT_TYPES:
            return False
    # The shared URL-shape rule covers BOTH asset extensions and extension-less
    # machine endpoints. The latter is why this delegates rather than keeping a
    # local suffix regex: `/wp-json/wp/v2/compliance/21086` has no suffix, so a
    # suffix-only test measured WordPress REST endpoints as if they were pages —
    # every WordPress site on the platform burned PSI budget on its own API.
    return not is_machine_resource_url(url)


# ---------------------------------------------------------------------------
# FAILURE CLASSIFICATION — the poison-pill gate.
#
# WHY THIS EXISTS (2026-08-13). A failed PSI call writes no `page_performance`
# row, so the page keeps `last_measured_at IS NULL`, stays in the
# never-measured class, and is therefore ranked FIRST on the very next cycle.
# A page that genuinely cannot be audited is not a page we retry — it is a
# page that wins the top of the queue forever. Live proof: three pages ate
# 156 of the sweep's 271 runs and drove the failure rate to 84% in 24 hours,
# because each 10-request cycle spent 6-7 of its requests on the same three
# URLs and reported the whole cycle failed.
#
# So a failure has to answer ONE question before the next cycle: was this the
# PROVIDER having a bad minute, or is this PAGE unauditable? The first must
# retry (PSI 5xx and read timeouts are routine and self-heal). The second must
# be quarantined after a few confirmations, loudly and reversibly.
# ---------------------------------------------------------------------------

#: Lighthouse error codes that describe THE PAGE, not the provider. Each means
#: Lighthouse reached a verdict and the verdict is "there is nothing here I can
#: audit" — retrying the identical URL a minute later reproduces it exactly.
TERMINAL_LIGHTHOUSE_CODES: frozenset[str] = frozenset(
    {
        "NO_FCP",  # rendered, but painted no content at all
        "FAILED_DOCUMENT_REQUEST",  # the document never loaded
        "ERRORED_DOCUMENT_REQUEST",  # the server answered with an error status
        "DNS_FAILURE",  # the host does not resolve
        "INVALID_URL",  # PSI refuses to accept the URL
        "NOT_HTML",  # the response is not a document
        "PAGE_HUNG",  # the page never became interactive
        "CHROME_INTERSTITIAL_ERROR",  # blocked by a cert / safe-browsing wall
    }
)

#: Consecutive TERMINAL verdicts before a page/strategy leaves the sweep. Three
#: 10-minute cycles ≈ 30 minutes of confirmation — long enough that a genuine
#: one-off deploy blip on the customer's site cannot quarantine them, short
#: enough that a dead page costs 3 requests instead of 97.
TERMINAL_FAILURES_BEFORE_QUARANTINE = 3

#: A quarantine EXPIRES. Sites get fixed, and nothing should require a human to
#: notice before a repaired page is measured again. After this long the page is
#: re-admitted on probation (counter reset); if it is still broken it costs one
#: request a week instead of ~900.
QUARANTINE_RETRY_AFTER_DAYS = 7


class PsiFailureVerdict(BaseModel):
    """Why one PSI attempt failed, and whether the page should be retried."""

    model_config = ConfigDict(extra="forbid")

    kind: PsiFailureKind
    #: Stable token for grouping — a Lighthouse code, or one of the transient
    #: buckets below. Stored on the health ledger so a human sees the pattern.
    code: str


def classify_psi_failure(message: str) -> PsiFailureVerdict:
    """Terminal (this page cannot be audited) vs transient (try again).

    Conservative in the RIGHT direction, and it is the OPPOSITE direction from
    `is_measurable_page`: an unrecognized failure is **transient**. A wrongly
    retried page costs one request per cycle and is visible in the run history;
    a wrongly quarantined page silently stops being covered, which is the one
    outcome this whole module exists to prevent.
    """
    haystack = message.upper()
    for code in sorted(TERMINAL_LIGHTHOUSE_CODES):
        if code in haystack:
            return PsiFailureVerdict(kind="terminal", code=code)
    if "HTTP 429" in haystack or ("RATE" in haystack and "LIMIT" in haystack):
        return PsiFailureVerdict(kind="transient", code="rate_limited")
    if "TIMEOUT" in haystack:
        return PsiFailureVerdict(kind="transient", code="timeout")
    if "HTTP 5" in haystack:
        return PsiFailureVerdict(kind="transient", code="provider_5xx")
    return PsiFailureVerdict(kind="transient", code="unknown")


class CoveragePage(BaseModel):
    """One candidate page, with everything the ranking needs already resolved."""

    model_config = ConfigDict(extra="forbid")

    page_id: str
    site_id: str
    url: str
    is_homepage: bool = False
    #: Path depth — number of non-empty URL path segments. 0 = homepage.
    depth: int = 0
    #: Google Search Console, trailing window. The strongest importance signal.
    clicks: int = 0
    impressions: int = 0
    #: Internal-link PageRank (`web.page.link_score`). None when never computed.
    link_score: Decimal | None = None
    #: When PSI last successfully measured this page (any strategy).
    last_measured_at: datetime | None = None
    #: When the crawler last saw the page's content_hash change.
    last_changed_at: datetime | None = None

    @property
    def measured(self) -> bool:
        return self.last_measured_at is not None


class PageSelection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page_id: str
    site_id: str
    url: str
    strategies: list[Strategy]
    reason: SelectionReason
    tier: ImportanceTier
    score: float
    requests: int


class SiteAllocation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    site_id: str
    candidate_pages: int
    never_measured: int
    changed: int
    refresh_due: int
    selected_pages: int
    requests: int
    capped: bool = False
    #: Pages still never measured after this cycle — the coverage backlog.
    remaining_never_measured: int = 0


class CoveragePlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_budget: int
    requests_planned: int
    selections: list[PageSelection] = Field(default_factory=list)
    per_site: list[SiteAllocation] = Field(default_factory=list)
    #: True when budget ran out with work still queued — the caller should say
    #: so rather than implying the sweep finished the job.
    budget_exhausted: bool = False

    @property
    def total_pages(self) -> int:
        return len(self.selections)


def importance_score(page: CoveragePage) -> float:
    """Rank a page by how much its speed actually matters.

    Traffic dominates when we have it (a page with real clicks IS important, no
    modelling required). PageRank carries sites with no Search Console binding.
    Depth is the floor so ordering is never arbitrary. Log scaling keeps one
    10,000-impression page from flattening every other signal to noise.
    """
    score = 0.0
    if page.clicks > 0:
        score += 10.0 * math.log10(1 + page.clicks)
    if page.impressions > 0:
        score += 3.0 * math.log10(1 + page.impressions)
    if page.link_score is not None:
        # link_score is a PageRank-style probability: tiny values, wide range.
        score += 8.0 * math.log10(1 + float(page.link_score) * 1_000)
    if page.is_homepage:
        score += 25.0
    # Shallow pages matter more; strictly a tiebreaker next to the signals above.
    score += max(0.0, 3.0 - 0.5 * page.depth)
    return score


def _importance_order_key(score: float, page: CoveragePage) -> tuple[int, int, int, float, str]:
    """Order known search demand before inferred internal importance.

    The numeric score blends GSC traffic, PageRank, homepage status, and depth.
    It is useful for tier thresholds, but a large internal-link score must never
    place a two-click page ahead of a 48-click page in the user-facing queue.
    Clicks lead, impressions break equal-click ties, and the blended score is
    used only after those observed demand signals.
    """
    has_search_demand = page.clicks > 0 or page.impressions > 0
    return (
        -int(has_search_demand),
        -page.clicks,
        -page.impressions,
        -score,
        page.page_id,
    )


def has_importance_signal(page: CoveragePage) -> bool:
    """Do we actually KNOW something about this page's importance?

    Traffic and PageRank are measurements; being the homepage is structural
    fact. URL depth is none of those — it is a guess used only to order pages
    that are otherwise indistinguishable.
    """
    return bool(
        page.is_homepage or page.clicks > 0 or page.impressions > 0 or page.link_score is not None
    )


def _tier_for(rank: int, total: int, score: float, page: CoveragePage) -> ImportanceTier:
    if page.is_homepage:
        return "critical"
    # No signal → "low" regardless of percentile. See MIN_SCORE_FOR_HIGH.
    if total <= 0 or not has_importance_signal(page):
        return "low"
    percentile = rank / total
    if percentile <= CRITICAL_PERCENTILE and score >= MIN_SCORE_FOR_HIGH:
        return "critical"
    if percentile <= HIGH_PERCENTILE and score >= MIN_SCORE_FOR_HIGH:
        return "high"
    if score >= MIN_SCORE_FOR_HIGH:
        return "normal"
    return "low"


def _strategies_for(tier: ImportanceTier, reason: SelectionReason) -> list[Strategy]:
    # Coverage means one successful mobile measurement. Running desktop in the
    # same first-ever pass halves the number of pages reached and makes a
    # short recurring cycle much more vulnerable to process restarts. Important
    # pages receive desktop on their first due refresh; mobile remains the
    # ranking/indexing baseline for every page.
    if reason == "never_measured":
        return ["mobile"]
    return ["mobile", "desktop"] if tier in DESKTOP_TIERS else ["mobile"]


def _reason_for(page: CoveragePage, now: datetime, tier: ImportanceTier) -> SelectionReason | None:
    if not page.measured:
        return "never_measured"
    measured_at = page.last_measured_at
    assert measured_at is not None  # guarded by .measured
    if page.last_changed_at is not None and page.last_changed_at > measured_at:
        return "content_changed"
    if now - measured_at >= timedelta(days=REFRESH_CADENCE_DAYS[tier]):
        return "refresh_due"
    return None


#: Ordering of the work classes. Coverage before freshness before cadence.
_REASON_RANK: dict[SelectionReason, int] = {
    "never_measured": 0,
    "content_changed": 1,
    "refresh_due": 2,
}


class _Candidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: CoveragePage
    reason: SelectionReason
    tier: ImportanceTier
    score: float
    strategies: list[Strategy]

    @property
    def requests(self) -> int:
        return len(self.strategies)


def _site_candidates(pages: list[CoveragePage], now: datetime) -> list[_Candidate]:
    """Score, tier and filter one site's pages into ordered work."""
    scored = sorted(
        ((importance_score(page), page) for page in pages),
        key=lambda pair: _importance_order_key(pair[0], pair[1]),
    )
    total = len(scored)
    candidates: list[_Candidate] = []
    for rank, (score, page) in enumerate(scored):
        tier = _tier_for(rank, total, score, page)
        reason = _reason_for(page, now, tier)
        if reason is None:
            continue
        strategies = _strategies_for(tier, reason)
        # A page measured on mobile only, now important enough for desktop,
        # should not be blocked from its desktop pass by the cadence gate —
        # but that is a refresh, not coverage, so it keeps its normal reason.
        candidates.append(
            _Candidate(page=page, reason=reason, tier=tier, score=score, strategies=strategies)
        )
    candidates.sort(
        key=lambda c: (_REASON_RANK[c.reason], *_importance_order_key(c.score, c.page)),
    )
    return candidates


def plan_pagespeed_coverage(
    pages_by_site: dict[str, list[CoveragePage]],
    *,
    now: datetime,
    request_budget: int = DAILY_REQUEST_BUDGET,
    per_site_request_cap: int = PER_SITE_CYCLE_REQUEST_CAP,
) -> CoveragePlan:
    """Build one cycle's PageSpeed plan.

    Sites are served round-robin in whole pages so that a large site cannot
    consume the budget before a small site is reached — the fairness property
    that makes "every active project gets covered" true rather than aspirational.
    """
    if request_budget < 0 or per_site_request_cap < 1:
        raise ValueError("request_budget must be >= 0 and per_site_request_cap >= 1")

    queues: dict[str, list[_Candidate]] = {}
    allocations: dict[str, SiteAllocation] = {}
    for site_id, pages in pages_by_site.items():
        candidates = _site_candidates(pages, now)
        queues[site_id] = candidates
        allocations[site_id] = SiteAllocation(
            site_id=site_id,
            candidate_pages=len(candidates),
            never_measured=sum(1 for c in candidates if c.reason == "never_measured"),
            changed=sum(1 for c in candidates if c.reason == "content_changed"),
            refresh_due=sum(1 for c in candidates if c.reason == "refresh_due"),
            selected_pages=0,
            requests=0,
        )

    selections: list[PageSelection] = []
    spent = 0
    # Deterministic, fair order ACROSS repeated short cycles: the least-covered
    # sites go first. Ordering by raw backlog starved small sites whenever one
    # cycle's request budget was smaller than the site count; the same huge
    # sites won every run. Coverage ratio changes after each successful page,
    # giving the next cycle a cursor-free rotation.
    order = sorted(
        queues,
        key=lambda sid: (
            -(allocations[sid].never_measured / max(1, len(pages_by_site[sid]))),
            sid,
        ),
    )
    cursors = dict.fromkeys(order, 0)
    progressed = True
    while progressed and spent < request_budget:
        progressed = False
        for site_id in order:
            if spent >= request_budget:
                break
            queue = queues[site_id]
            index = cursors[site_id]
            if index >= len(queue):
                continue
            allocation = allocations[site_id]
            candidate = queue[index]
            if allocation.requests + candidate.requests > per_site_request_cap:
                allocation.capped = True
                continue
            if spent + candidate.requests > request_budget:
                # Not enough budget for this page's full strategy set. Do not
                # half-measure it — leave it for the next cycle so a page is
                # never recorded as covered on a partial pass.
                continue
            cursors[site_id] = index + 1
            spent += candidate.requests
            allocation.requests += candidate.requests
            allocation.selected_pages += 1
            selections.append(
                PageSelection(
                    page_id=candidate.page.page_id,
                    site_id=site_id,
                    url=candidate.page.url,
                    strategies=candidate.strategies,
                    reason=candidate.reason,
                    tier=candidate.tier,
                    score=round(candidate.score, 4),
                    requests=candidate.requests,
                )
            )
            progressed = True

    for site_id, allocation in allocations.items():
        taken = queues[site_id][: cursors[site_id]]
        covered = sum(1 for c in taken if c.reason == "never_measured")
        allocation.remaining_never_measured = allocation.never_measured - covered

    outstanding = any(cursors[sid] < len(queues[sid]) for sid in queues)
    return CoveragePlan(
        request_budget=request_budget,
        requests_planned=spent,
        selections=selections,
        per_site=[allocations[sid] for sid in order],
        budget_exhausted=outstanding,
    )


__all__ = [
    "CRITICAL_PERCENTILE",
    "DAILY_REQUEST_BUDGET",
    "DESKTOP_TIERS",
    "HIGH_PERCENTILE",
    "PER_SITE_CYCLE_REQUEST_CAP",
    "QUARANTINE_RETRY_AFTER_DAYS",
    "REFRESH_CADENCE_DAYS",
    "TERMINAL_FAILURES_BEFORE_QUARANTINE",
    "TERMINAL_LIGHTHOUSE_CODES",
    "CoveragePage",
    "CoveragePlan",
    "ImportanceTier",
    "PageSelection",
    "PsiFailureKind",
    "PsiFailureVerdict",
    "SelectionReason",
    "SiteAllocation",
    "Strategy",
    "classify_psi_failure",
    "has_importance_signal",
    "importance_score",
    "is_measurable_page",
    "plan_pagespeed_coverage",
]
