"""Deterministic per-page audit analysis — the ``system_rules`` provider.

Commissioned 2026-08-08 (Arman's ruling: `web.analysis_result` had been empty
platform-wide since design). This module is the zero-token half of the analysis
catalogue: every check is a NAMED ``web.analysis_item`` row (extend the
catalogue, never invent ad-hoc keys), computed purely from evidence the crawler
already persists — snapshot metrics, head tags, headings, image inventory,
content fingerprints, and link edges. No network, no model calls.

🚨 **This module implements NO per-page check.** Every per-page verdict —
title, description, headings, thin content, image alt, robots, canonical,
transport — lives ONCE in ``seo_audit.PAGE_CHECKS`` and is consumed here.
What lives here is the job ``seo_audit`` structurally cannot do: CROSS-PAGE
work (duplicate titles/descriptions/content across a whole crawl, per-page
link-status rollups from ``web.link_edge``) plus the DB read/write plumbing.
Adding a per-page check here instead of in ``seo_audit`` re-creates exactly
the three-way drift this consolidation removed (2026-08-09).

Canvas doctrine rung 3+5: each check encodes an expert reflex as a named
server-side algorithm whose REASONING is persisted with the result
(``metadata.reasoning``), and deterministic code runs before any AI provider.

Write contract (all DB-enforced, see ``web.validate_cross_pointers``):

- ``web.analysis_result`` is IMMUTABLE — insert-only observations. ``status``
  pass|warn|fail requires ``score`` 1–100; ``n_a``/``error`` require NULL.
  Denormalized ``item_key``/``category``/``subcategory`` must match the
  catalogue row. Page subjects carry ``subject_id == page_id``.
- ``web.finding`` is the mutable lifecycle register: at most ONE open finding
  per (site, subject, item). A warn/fail result opens or refreshes it; a pass
  resolves it. Suppression is user-owned — never touched here.
"""

from __future__ import annotations

import asyncio
import logging
import re
from bisect import bisect_right
from time import perf_counter
from collections.abc import Awaitable, Callable
from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime, timedelta
from typing import Any
from urllib.parse import urlsplit

from matrx_orm import Avg, Max, Min, Sum

from matrx_scraper.db.models_seo_host import SeoPagePerformance
from matrx_scraper.db.models_web import (
    AnalysisItem as WebAnalysisItem,
    AnalysisResult as WebAnalysisResult,
    CrawlUrl as WebCrawlUrl,
    GscPageStat as WebGscPageStat,
    LinkEdge as WebLinkEdge,
    Page as WebPage,
    Provider as WebProvider,
    Site as WebSite,
    Snapshot as WebSnapshot,
)
from matrx_scraper.crawler import _normalise_url
from matrx_scraper.seo_audit import (
    BUSINESS_CORE_PROPERTIES,
    BUSINESS_ENHANCED_PROPERTIES,
    BUSINESS_MISSING_CORE_FAIL_COUNT,
    CHECK_EVIDENCE_SAMPLE_LIMIT,
    CHECK_SITE_LINKS,
    HREFLANG_RECIPROCITY_FAIL_SCORE,
    LAB_PERFORMANCE_MAX_AGE_DAYS,
    PAGE_CHECKS as SEO_PAGE_CHECKS,
    RECAPTURE_PAGE,
    RECRAWL_SITE,
    SYNC_GSC,
    STRUCTURED_DATA_EVIDENCE_LIMIT,
    CheckOutcome,
    PageEvidence,
    business_entities_in,
    clamp_score,
    hreflang_entries,
    lab_performance_from_lighthouse,
    normalized_url_key,
    registrable_host,
    sample_urls,
)
from matrx_scraper.web_crawl.analysis_write import (
    insert_results,
    reconcile_findings,
    severity_for,
)
from matrx_scraper.web_crawl.contracts import AnalysisSummary
from matrx_scraper.web_crawl.gsc_cannibalization import (
    GscCannibalizationEvidence,
    check_gsc_keyword_cannibalization,
    load_gsc_keyword_cannibalization,
)
from matrx_scraper.web_crawl.link_score import SiteLinkGraph, build_site_graph
from matrx_utils.web_page_class import is_machine_resource
from matrx_utils import capture_error
from pydantic import ValidationError

from ..check_payloads import evidence_kind_for, evidence_model_for
from matrx_scraper.web_crawl.near_duplicate import (
    NearDuplicatePage,
    NearDuplicateReport,
    build_near_duplicate_report,
)
from matrx_scraper.web_crawl.persistence import url_hash
from matrx_scraper.web_crawl.site_analysis import (
    CRAWLABILITY_SITE_CHECKS,
    SiteEvidence,
    load_site_evidence,
)
from matrx_scraper.web_crawl.site_probe import (
    SiteProbe,
    http_origin_probe,
    load_site_probe,
    page_http_variant_probe,
)

logger = logging.getLogger(__name__)

# Provider + versioning. Bump ANALYZER_VERSION on any scoring-rule change so
# results from different rule generations are distinguishable.
#   1.0 — initial deterministic sweep (2026-08-08).
#   1.1 — eight transport/pagination checks became recordable, external-link
#         rot became a separate audit, TTFB switched from total response time
#         to true TTFB, and page_weight was narrowed to the HTML document
#         (2026-08-09). The generations are not comparable.
RULES_PROVIDER_KEY = "system_rules"
ANALYZER_VERSION = "1.2"

_PAGE_BATCH_SIZE = 500
# The snapshot-less crawl_url walk reads narrow `.values()` projections, so it
# can take far bigger bites than the hydrated page census (176k rows at 500 per
# round trip was 350 sequential queries for six columns each).
_CRAWL_URL_BATCH_SIZE = 5_000
_SNAPSHOT_BATCH_SIZE = 200
_LAB_PERFORMANCE_BATCH_SIZE = 200
_EDGE_BATCH_SIZE = 5_000
_RESULT_INSERT_BATCH = 500
_MAX_PAGES_PER_RUN = 20_000
ProgressCallback = Callable[[str, AnalysisSummary], Awaitable[None]]

# A page the crawler marked as gone (410/404-confirmed) is not a live known
# page — it must not inflate the orphan denominator.
_GONE_PAGE_STATUS = "gone"

# ---------------------------------------------------------------------------
# Internal-linking thresholds. Every band below is the `web.analysis_item`
# row's `score_contract` made executable — the row is the spec, this is its ONE
# implementation. Each band is `(inclusive upper bound, status, score)`,
# evaluated top-down (`first_match_top_down`), with a final band for everything
# above the last bound.

# `excessive_outlinks` — total links (internal + external) on one page.
# 151–300 records an 85 as a PASS: dilution worth knowing about on a hub page,
# not a defect worth a finding.
OUTLINK_BANDS: tuple[tuple[int, str, int], ...] = (
    (150, "pass", 100),
    (300, "pass", 85),
    (500, "warn", 65),
)
OUTLINK_EXCESSIVE = ("fail", 45)

# `nofollow_internal_links` — internal links carrying rel=nofollow/ugc/sponsored.
NOFOLLOW_REL_TOKENS = frozenset({"nofollow", "ugc", "sponsored"})
NOFOLLOW_INTERNAL_BANDS: tuple[tuple[int, str, int], ...] = (
    (0, "pass", 100),
    (9, "warn", 70),
)
NOFOLLOW_INTERNAL_EXCESSIVE = ("fail", 45)

# `anchor_text_descriptiveness` — the share of internal anchors that carry a
# relevance signal. Generic phrases are matched on the FULL normalized anchor
# (punctuation stripped): "read more about pricing" is descriptive, "read more"
# is not.
GENERIC_ANCHOR_PHRASES = frozenset(
    {
        "click",
        "click here",
        "click this link",
        "continue",
        "continue reading",
        "details",
        "download",
        "find out more",
        "full story",
        "go",
        "here",
        "info",
        "learn more",
        "link",
        "more",
        "more info",
        "more information",
        "read",
        "read more",
        "read this",
        "see",
        "see more",
        "this",
        "this article",
        "this link",
        "this page",
        "this post",
        "view",
        "view more",
        "visit",
        "website",
    }
)
_BARE_URL_ANCHOR = re.compile(r"^(?:https?://|www\.|[a-z0-9-]+\.[a-z]{2,}(?:/|$))", re.IGNORECASE)
ANCHOR_DESCRIPTIVE_FAIL_SCORE = 60
ANCHOR_DESCRIPTIVE_WARN_SCORE = 85

# `crawl_depth` — clicks from the homepage over the internal link graph.
CRAWL_DEPTH_BANDS: tuple[tuple[int, str, int], ...] = (
    (3, "pass", 100),
    (4, "warn", 75),
    (5, "warn", 55),
)
CRAWL_DEPTH_SEVERE = ("fail", 35)

# `internal_inlink_coverage` — unique internal pages linking to this page.
# Zero is deliberately absent: that is `orphan_pages`' verdict, not this one's.
INLINK_COVERAGE_BANDS: tuple[tuple[int, str, int], ...] = (
    (1, "warn", 45),
    (4, "warn", 70),
)
INLINK_COVERAGE_HEALTHY = ("pass", 100)

# `orphan_pages` — the site-wide formula from the catalogue row:
# score = round(100 * (1 - orphans / known_live_pages)), floored when orphans
# are the majority of the site.
ORPHAN_MAJORITY_RATIO = 0.5
ORPHAN_SCORE_FLOOR = 5

# 🚨 The share of known live pages that must actually have been CAPTURED before
# an absence of inbound links means anything. A half-finished crawl manufactures
# orphans wholesale: the pages that link to a captured page simply were not
# fetched, so it looks unreachable. Measured on a real site (2026-08-09): a
# crawl that died with 119 pages fetched and 181 still queued made 81 of 124
# captured pages look orphaned — every one of them a lie. `link_score` refuses
# to score a partial crawl for the same reason; these two checks refuse to
# judge one.
LINK_GRAPH_MIN_CAPTURE_RATIO = 0.8

# `internal_link_equity` — percentile rank of the canonical `web.page.link_score`
# PageRank. The catalogue contract adds one deliberate override: a prioritized
# page (`target_keyword` set) in the bottom quartile can score no higher than 40.
LINK_EQUITY_PRIORITY_QUARTILE = 25
LINK_EQUITY_PRIORITY_SCORE_CAP = 40
LINK_EQUITY_PASS_SCORE = 80
LINK_EQUITY_WARN_SCORE = 50

# --- `search_signals` — what GOOGLE ITSELF reported, not what we inferred ---
# Every threshold below comes from the catalogue row's `score_contract`; the
# one thing the contracts do NOT supply is the position→CTR curve, declared
# once here. All of it reads `web.gsc_page_stat`, whose rows are written by
# `gsc_sync` (dimensions date × page).

#: Length of every comparison window, in days. GSC's own reporting default.
GSC_PERIOD_DAYS = 28
#: How far back `gsc_performance_decay`'s "last quarter" window ENDS.
GSC_DECAY_QUARTER_LAG_DAYS = 90
#: Shortest synced history that can answer decay at all — the quarter window
#: must fit entirely inside the data. Below this the check is `n_a`, never a
#: pass: a site synced for 28 days has no evidence of a 90-day trend.
GSC_DECAY_MIN_HISTORY_DAYS = GSC_DECAY_QUARTER_LAG_DAYS + GSC_PERIOD_DAYS
#: "Only pages with >= 50 clicks in the baseline period are scored."
GSC_DECAY_MIN_BASELINE_CLICKS = 50
#: Decline bands, contract-verbatim, evaluated first-match top-down. The first
#: two require the drop to hold across BOTH comparisons (prior period AND last
#: quarter); the third reads the prior-period comparison alone.
GSC_DECAY_SEVERE_DROP = 0.50
GSC_DECAY_SEVERE_SCORE = 30
GSC_DECAY_MODERATE_DROP = 0.25
GSC_DECAY_MODERATE_SCORE = 55
GSC_DECAY_MILD_DROP = 0.10
GSC_DECAY_MILD_SCORE = 75

#: "Only pages with >= 100 impressions are scored; others skipped."
GSC_CTR_MIN_IMPRESSIONS = 100
#: The severe band additionally requires real volume behind the miss.
GSC_CTR_SEVERE_IMPRESSIONS = 1000
GSC_CTR_SEVERE_RATIO = 0.30
GSC_CTR_SEVERE_SCORE = 35
GSC_CTR_POOR_RATIO = 0.50
GSC_CTR_POOR_SCORE = 55
GSC_CTR_FAIR_RATIO = 0.80
GSC_CTR_FAIR_SCORE = 75

#: Expected organic CTR by average position, 1-indexed (index 0 = position 1).
#: The contract says "expected-for-position" without supplying the curve, so
#: this is it — one declaration, used by nothing else.
GSC_EXPECTED_CTR_BY_POSITION: tuple[float, ...] = (
    0.28,
    0.15,
    0.11,
    0.08,
    0.06,
    0.05,
    0.04,
    0.032,
    0.028,
    0.025,
)
#: Positions 11–20 (page two) and anything deeper — one flat expectation each,
#: because below page one the curve is noise, not signal.
GSC_EXPECTED_CTR_PAGE_TWO = 0.015
GSC_EXPECTED_CTR_DEEP = 0.008
GSC_EXPECTED_CTR_DEEP_POSITION = 20

#: A score at or above this is a pass; at or above the second, a warn.
GSC_PASS_SCORE_FLOOR = 80
GSC_WARN_SCORE_FLOOR = 50
GSC_HEALTHY_SCORE = 100

# ---------------------------------------------------------------------------
# Evidence structs


@dataclass
class PageFacts(PageEvidence):
    """Per-page evidence from the latest accepted snapshot.

    Extends the canonical ``seo_audit.PageEvidence`` so every per-page check
    consumes it directly — the persisted-snapshot sweep and a live one-shot
    audit run the SAME functions over the SAME struct. The extra fields here
    are the ones only a site-wide sweep needs (row identity + the duplicate-
    content fingerprint that cross-page checks group on).
    """

    page_id: str = ""
    latest_snapshot_id: str = ""
    fingerprint_version: int | None = None
    exact_sha256: str | None = None
    simhash64: str | None = None
    link_score: float | None = None
    target_keyword: str | None = None


@dataclass
class SiteAggregates:
    """Site-wide groupings the cross-page checks read."""

    pages_by_title: dict[str, list[PageFacts]] = field(default_factory=dict)
    pages_by_description: dict[str, list[PageFacts]] = field(default_factory=dict)
    pages_by_sha: dict[tuple[int, str], list[PageFacts]] = field(default_factory=dict)
    # source page id -> (broken URLs, redirecting URLs, edges with known status)
    link_stats: dict[str, PageLinkStats] = field(default_factory=dict)
    # canonical target page id -> the canonical source pages linking to it.
    # Self-links are excluded: a page is not its own inbound signal.
    inlinks: dict[str, set[str]] = field(default_factory=dict)
    # canonical page id -> clicks from the homepage over the internal graph.
    # Absent from this map = unreachable, which is `orphan_pages`' domain.
    depth_by_page: dict[str, int] = field(default_factory=dict)
    homepage_page_id: str | None = None
    # Internal edges that resolved to a registered page. Zero means the site
    # has NO link graph at all — missing evidence (`n_a`), never "every page
    # is orphaned".
    internal_edges_resolved: int = 0
    # canonical page id -> inclusive percentile (1..100) of the existing
    # internal PageRank score. Built once from the page census; no graph reload.
    link_equity_percentile_by_page: dict[str, int] = field(default_factory=dict)
    orphans: OrphanCensus = field(default_factory=lambda: OrphanCensus())
    # Google's own numbers for this site. The default says "not connected",
    # which is what every `search_signals` check reports until
    # `_load_gsc_stats` proves otherwise.
    gsc: SiteGscEvidence = field(default_factory=lambda: SiteGscEvidence())
    # The site's own business identity as declared in structured data.
    business: SiteBusinessEvidence = field(default_factory=lambda: SiteBusinessEvidence())
    # normalized page URL -> the normalized hreflang targets THAT page declares.
    # Keyed by URL, not page id, because an hreflang annotation names a URL and
    # the return tag has to be found by that name.
    hreflang_targets: dict[str, set[str]] = field(default_factory=dict)


@dataclass
class OrphanCensus:
    """Site-wide orphan accounting for the `orphan_pages` formula.

    The catalogue row scores the SITE ("share of live known pages that are
    orphaned") while this sweep records per-page subjects, so the site score is
    computed once here and stamped on each orphaned page's result.

    The two orphan classes are counted apart on purpose. A page the crawler
    actually fetched that nothing links to is a confirmed in-graph dead end. A
    page known only from a sitemap, GSC, or a manual import was never captured
    at all — orphaned in the same link graph, but calling it "a crawled page
    with no inlinks" would misstate what we observed. Both count toward the
    site ratio; only the crawled class can carry a per-page verdict, because
    only it has a subject with evidence to point at.
    """

    # False until the whole page registry was read — a truncated run cannot
    # honestly divide by "known live pages".
    complete: bool = False
    known_live_pages: int = 0
    captured_pages: int = 0
    crawled_orphan_ids: set[str] = field(default_factory=set)
    uncrawled_orphans: int = 0
    uncrawled_orphan_urls: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.crawled_orphan_ids) + self.uncrawled_orphans

    @property
    def capture_ratio(self) -> float:
        if self.known_live_pages <= 0:
            return 0.0
        return self.captured_pages / self.known_live_pages

    @property
    def graph_is_representative(self) -> bool:
        """Is the link graph complete enough for MISSING links to mean anything?"""
        return self.complete and self.capture_ratio >= LINK_GRAPH_MIN_CAPTURE_RATIO

    def site_score(self) -> int:
        """The catalogue row's formula, verbatim."""
        if self.known_live_pages <= 0:
            return 100
        ratio = self.total / self.known_live_pages
        score = round(100 * (1 - ratio))
        if self.total > 0 and ratio > ORPHAN_MAJORITY_RATIO:
            score = max(ORPHAN_SCORE_FLOOR, score)
        return clamp_score(score)


@dataclass
class PageLinkStats:
    """Outbound-link facts for ONE source page, from its CURRENT snapshot.

    Verified statuses (internal and external counted apart — a broken internal
    link is a self-inflicted dead end, a broken external one is rot in someone
    else's site that still costs this page trust) plus the structural counts
    the internal-linking checks read: how many links the page emits at all, how
    many internal ones are nofollowed, and how many carry an anchor that
    actually says something.
    """

    checked: int = 0
    broken: list[str] = field(default_factory=list)
    redirecting: list[str] = field(default_factory=list)
    external_checked: int = 0
    external_broken: list[str] = field(default_factory=list)
    outlinks_total: int = 0
    internal_outlinks: int = 0
    nofollow_internal_count: int = 0
    nofollow_internal_samples: list[str] = field(default_factory=list)
    descriptive_anchors: int = 0
    generic_anchor_targets: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class GscPeriod:
    """One date window's Google totals for ONE page.

    ``position`` is the mean of the daily average positions Google reported;
    ``None`` means Google reported impressions with no position at all.
    """

    clicks: int = 0
    impressions: int = 0
    position: float | None = None

    @property
    def ctr(self) -> float | None:
        """Click-through rate recomputed from the totals.

        Never the stored per-day ``ctr`` column: averaging daily rates over a
        window silently weights a 3-impression day the same as a 3,000-
        impression one.
        """
        if self.impressions <= 0:
            return None
        return self.clicks / self.impressions


@dataclass
class PageGscStats:
    """One page's Google numbers across the three comparison windows."""

    current: GscPeriod = field(default_factory=GscPeriod)
    prior: GscPeriod = field(default_factory=GscPeriod)
    quarter: GscPeriod = field(default_factory=GscPeriod)


@dataclass
class SiteGscEvidence:
    """What Google itself reported for this site — and whether it can be read.

    The default instance is the HONEST default: no property bound, nothing
    synced. Every `search_signals` check therefore answers ``n_a`` naming that
    fact when nobody loaded evidence, and can never fabricate a pass out of a
    site Google has never been asked about.
    """

    bound: bool = False
    #: Why the property is unusable, in the binding parser's own words.
    unbound_reason: str = "no Google Search Console property is bound to this site"
    earliest_date: date | None = None
    latest_date: date | None = None
    by_page: dict[str, PageGscStats] = field(default_factory=dict)

    @property
    def synced(self) -> bool:
        return self.latest_date is not None

    @property
    def history_days(self) -> int:
        if self.latest_date is None or self.earliest_date is None:
            return 0
        return (self.latest_date - self.earliest_date).days + 1


@dataclass
class SiteBusinessEvidence:
    """The business entity this SITE declares, gathered from every page.

    `local_business_markup` is a SITE-level catalogue item — its score contract
    asks whether Organization/LocalBusiness markup exists "anywhere on site"
    and whether NAP values agree "across own pages". Neither question can be
    answered from one page, which is why the check is cross-page even though
    its verdict is recorded per page.
    """

    #: Pages whose snapshot actually carried a structured-data capture. Zero
    #: means the evidence is missing (`n_a`), NOT that the site has no markup.
    pages_captured: int = 0
    #: One normalized entity per declaration: types + the NAP/enhanced values.
    entities: list[dict[str, Any]] = field(default_factory=list)


class AnalysisRunResult:
    def __init__(self, summary: AnalysisSummary, *, result_id: str | None = None) -> None:
        self.summary = summary
        # One representative immutable result row is the analysis stage's
        # pointer. The full run remains queryable by that row's run_id.
        self.result_id = result_id


def _norm_text(value: str | None) -> str | None:
    if value is None:
        return None
    collapsed = re.sub(r"\s+", " ", value).strip().lower()
    return collapsed or None


# ---------------------------------------------------------------------------
# The CROSS-PAGE checks — the only checks this module implements. Each needs
# the whole crawled site (or the site's verified link statuses) and therefore
# cannot live in the per-page primitive. Per-page checks are imported from
# `seo_audit`; see the module docstring.


def _check_title_duplication(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    norm = _norm_text(facts.title)
    if norm is None:
        return CheckOutcome(
            "n_a",
            None,
            "This page has no title yet, so there is nothing to compare with the rest of the site.",
        )
    partners = [p for p in site.pages_by_title.get(norm, []) if p.page_id != facts.page_id]
    if not partners:
        return CheckOutcome("pass", 100, "Title is unique across the crawled site.")
    n = len(partners)
    status = "warn" if n <= 2 else "fail"
    score = clamp_score(45 - 10 * (n - 1)) if n <= 2 else clamp_score(25 - 2 * (n - 3))
    return CheckOutcome(
        status,
        score,
        (
            f'Title "{(facts.title or "")[:80]}" is shared by {n} other page(s) — '
            "duplicate titles make Google pick which page to rank."
        ),
        issue_count=n,
        evidence={"duplicate_pages": sample_urls([p.url for p in partners])},
    )


def _check_meta_description_duplication(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    norm = _norm_text(facts.description)
    if norm is None:
        return CheckOutcome(
            "n_a",
            None,
            "This page has no meta description yet, so there is nothing to compare "
            "with the rest of the site.",
        )
    partners = [p for p in site.pages_by_description.get(norm, []) if p.page_id != facts.page_id]
    if not partners:
        return CheckOutcome("pass", 100, "Meta description is unique across the crawled site.")
    n = len(partners)
    status = "warn" if n <= 2 else "fail"
    score = clamp_score(50 - 10 * (n - 1)) if n <= 2 else clamp_score(28 - 2 * (n - 3))
    return CheckOutcome(
        status,
        score,
        f"Meta description is shared by {n} other page(s) — duplicated snippets "
        "blur which page answers the query.",
        issue_count=n,
        evidence={"duplicate_pages": sample_urls([p.url for p in partners])},
    )


def _check_broken_internal_links(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    stats = site.link_stats.get(facts.page_id)
    if stats is None or stats.checked == 0:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't checked this page's links yet.",
            remediation=CHECK_SITE_LINKS,
        )
    if not stats.broken:
        return CheckOutcome("pass", 100, f"All {stats.checked} verified internal links resolve.")
    n = len(stats.broken)
    return CheckOutcome(
        "fail",
        clamp_score(60 - 15 * n),
        f"{n} internal link(s) on this page point at broken targets (4xx/5xx/no "
        "response) — dead ends for users and crawlers.",
        issue_count=n,
        evidence={"broken_targets": sample_urls(stats.broken)},
    )


def _check_broken_external_links(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    stats = site.link_stats.get(facts.page_id)
    if stats is None or stats.external_checked == 0:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't checked this page's links to other websites yet.",
            remediation=CHECK_SITE_LINKS,
        )
    if not stats.external_broken:
        return CheckOutcome(
            "pass", 100, f"All {stats.external_checked} verified external links resolve."
        )
    n = len(stats.external_broken)
    # Warn, not fail: the target is someone else's site. It still costs the
    # page trust and sends users to a dead end, so it is never silent.
    return CheckOutcome(
        "warn",
        clamp_score(75 - 10 * n),
        f"{n} external link(s) on this page point at broken targets (4xx/5xx/no "
        "response) — outbound rot sends users off a cliff and signals a stale page.",
        issue_count=n,
        evidence={"broken_targets": sample_urls(stats.external_broken)},
    )


def _check_internal_redirect_links(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    stats = site.link_stats.get(facts.page_id)
    if stats is None or stats.checked == 0:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't checked this page's links yet.",
            remediation=CHECK_SITE_LINKS,
        )
    if not stats.redirecting:
        return CheckOutcome(
            "pass", 100, "No verified internal link on this page goes through a redirect."
        )
    n = len(stats.redirecting)
    return CheckOutcome(
        "warn",
        clamp_score(85 - 10 * n),
        f"{n} internal link(s) point at redirecting URLs — each hop wastes crawl "
        "budget and dilutes signals; link straight to the final URL.",
        issue_count=n,
        evidence={"redirecting_targets": sample_urls(stats.redirecting)},
    )


def _check_duplicate_content_exact(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    if facts.exact_sha256 is None or facts.fingerprint_version is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't fingerprinted this page's text yet, so we can't compare "
            "it with the rest of the site.",
            remediation=RECAPTURE_PAGE,
        )
    key = (facts.fingerprint_version, facts.exact_sha256)
    partners = [p for p in site.pages_by_sha.get(key, []) if p.page_id != facts.page_id]
    if not partners:
        return CheckOutcome("pass", 100, "Visible text is unique across the crawled site.")
    n = len(partners)
    return CheckOutcome(
        "fail",
        clamp_score(30 - 5 * (n - 1)),
        f"Visible text is EXACTLY identical to {n} other page(s) — pure duplicate "
        "content; canonicalize or differentiate.",
        issue_count=n,
        evidence={"duplicate_pages": sample_urls([p.url for p in partners])},
    )


def _band(
    bands: tuple[tuple[int, str, int], ...], above: tuple[str, int], value: int
) -> tuple[str, int]:
    """First band whose inclusive upper bound covers ``value`` (top-down)."""
    for bound, status, score in bands:
        if value <= bound:
            return status, score
    return above


def _normalize_anchor(anchor: str | None) -> str:
    """Anchor text reduced to the words that carry meaning."""
    if not anchor:
        return ""
    collapsed = re.sub(r"\s+", " ", anchor).strip().lower()
    return re.sub(r"^[^\w]+|[^\w]+$", "", collapsed)


def _is_descriptive_anchor(anchor: str | None) -> bool:
    """Deterministic only — no model call, ever (the catalogue row says so).

    Non-descriptive means: nothing at all (an empty anchor, which is also how
    an image link with no alt text arrives), a bare URL, or a phrase from the
    generic list. Everything else is credited — this check must never punish a
    real anchor it simply does not recognize.
    """
    normalized = _normalize_anchor(anchor)
    if not normalized:
        return False
    if _BARE_URL_ANCHOR.match(normalized):
        return False
    return normalized not in GENERIC_ANCHOR_PHRASES


def _check_excessive_outlinks(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    stats = site.link_stats.get(facts.page_id)
    if stats is None or stats.outlinks_total == 0:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't recorded the links on this page yet.",
            remediation=RECAPTURE_PAGE,
        )
    total = stats.outlinks_total
    status, score = _band(OUTLINK_BANDS, OUTLINK_EXCESSIVE, total)
    if status == "pass" and score == 100:
        return CheckOutcome(
            "pass", 100, f"{total} links on the page — a normal, focused link budget."
        )
    return CheckOutcome(
        status,
        score,
        f"{total} links on this page ({stats.internal_outlinks} internal) — every "
        "extra link splits the equity this page passes on and is a classic sign "
        "of an index/tag page rather than a destination.",
        issue_count=total,
        evidence={"outlinks_total": total, "internal_outlinks": stats.internal_outlinks},
    )


def _check_nofollow_internal_links(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    stats = site.link_stats.get(facts.page_id)
    if stats is None or stats.outlinks_total == 0:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't recorded the links on this page yet.",
            remediation=RECAPTURE_PAGE,
        )
    n = stats.nofollow_internal_count
    status, score = _band(NOFOLLOW_INTERNAL_BANDS, NOFOLLOW_INTERNAL_EXCESSIVE, n)
    if n == 0:
        return CheckOutcome(
            "pass",
            score,
            f"None of the {stats.internal_outlinks} internal links on this page are nofollowed.",
        )
    return CheckOutcome(
        status,
        score,
        f"{n} internal link(s) carry rel=nofollow/ugc/sponsored — you are telling "
        "search engines not to pass value between your OWN pages, which is almost "
        "always an accident of a plugin or template.",
        issue_count=n,
        evidence={"nofollowed_targets": sample_urls(stats.nofollow_internal_samples)},
    )


def _check_anchor_text_descriptiveness(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    stats = site.link_stats.get(facts.page_id)
    if stats is None or stats.outlinks_total == 0:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't recorded the wording of this page's links yet.",
            remediation=RECAPTURE_PAGE,
        )
    if stats.internal_outlinks == 0:
        # The catalogue row is explicit: "100 when no internal links".
        return CheckOutcome("pass", 100, "This page emits no internal links to describe.")
    score = clamp_score(round(100 * stats.descriptive_anchors / stats.internal_outlinks))
    generic = stats.internal_outlinks - stats.descriptive_anchors
    if score >= ANCHOR_DESCRIPTIVE_WARN_SCORE:
        return CheckOutcome(
            "pass",
            score,
            f"{stats.descriptive_anchors} of {stats.internal_outlinks} internal "
            "anchors describe where they go.",
        )
    status = "fail" if score < ANCHOR_DESCRIPTIVE_FAIL_SCORE else "warn"
    return CheckOutcome(
        status,
        score,
        f"{generic} of {stats.internal_outlinks} internal links use a generic, "
        'empty, or bare-URL anchor ("click here", "read more", an image with no '
        "alt text) — the anchor is the strongest hint you give about what the "
        "target page is for, and these give none.",
        issue_count=generic,
        evidence={"generic_anchor_targets": sample_urls(stats.generic_anchor_targets)},
    )


def _check_crawl_depth(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    if site.homepage_page_id is None:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't crawled this site's homepage yet, so we can't work out "
            "how many clicks it takes to reach this page.",
            remediation=RECRAWL_SITE,
        )
    depth = site.depth_by_page.get(facts.page_id)
    if depth is None:
        # Deliberately NOT a fail: the catalogue row hands unreachable pages to
        # `orphan_pages`, and two items scoring the same defect double-counts it.
        return CheckOutcome(
            "n_a",
            None,
            "No click path from the homepage reaches this page — see the orphan "
            "pages check, which owns unreachable pages.",
        )
    status, score = _band(CRAWL_DEPTH_BANDS, CRAWL_DEPTH_SEVERE, depth)
    if status != "pass" and not site.orphans.graph_is_representative:
        # A shortest path found is REAL, but a partial crawl can only overstate
        # it — the shortcut may run through a page we never fetched. A shallow
        # pass survives that (more pages can only shorten the path); a penalty
        # does not, so it waits for the full picture instead of blaming a page
        # that may be one click from the homepage.
        return CheckOutcome(
            "n_a",
            None,
            f"The shortest path we can see is {depth} clicks, but we've captured "
            f"only {site.orphans.captured_pages} of the "
            f"{site.orphans.known_live_pages} pages we know about — a shorter "
            "route may run through a page we never fetched. Finish a full crawl "
            "and this answers properly.",
            remediation=RECRAWL_SITE,
        )
    if status == "pass":
        return CheckOutcome(
            "pass",
            score,
            f"{depth} click(s) from the homepage — comfortably reachable for "
            "crawlers and for people.",
        )
    return CheckOutcome(
        status,
        score,
        f"This page is {depth} clicks from the homepage — pages this deep get "
        "crawled less often and inherit less authority; link to it from a "
        "higher-level hub page.",
        issue_count=depth,
        evidence={"depth": depth},
    )


def _partial_graph_outcome(site: SiteAggregates) -> CheckOutcome | None:
    """The ONE gate both inbound-link checks share.

    Both answer a question about links that are NOT there, and a crawl that did
    not finish is full of links that are not there YET. Answering anyway is how
    a half-finished crawl becomes dozens of confident, wrong findings on pages
    that are perfectly well linked.
    """

    census = site.orphans
    if site.internal_edges_resolved == 0:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't mapped how this site's pages link to each other yet.",
            remediation=RECRAWL_SITE,
        )
    if not census.graph_is_representative:
        return CheckOutcome(
            "n_a",
            None,
            f"We've captured only {census.captured_pages} of the "
            f"{census.known_live_pages} pages we know about on this site, so we'd "
            'mostly be reporting "nothing links here" about pages whose linking '
            "pages we never fetched. Finish a full crawl and this answers properly.",
            remediation=RECRAWL_SITE,
        )
    return None


def _check_internal_inlink_coverage(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    blocked = _partial_graph_outcome(site)
    if blocked is not None:
        return blocked
    n = len(site.inlinks.get(facts.page_id, ()))
    if n == 0:
        return CheckOutcome(
            "n_a",
            None,
            "No internal page links here at all — see the orphan pages check, "
            "which owns pages with zero inlinks.",
        )
    status, score = _band(INLINK_COVERAGE_BANDS, INLINK_COVERAGE_HEALTHY, n)
    if status == "pass":
        return CheckOutcome("pass", score, f"{n} other pages on this site link here.")
    return CheckOutcome(
        status,
        score,
        f"Only {n} other page(s) on this site link here — a near-orphan is "
        "technically reachable but reads as unimportant to search engines, so it "
        "is crawled rarely and ranks below its content's worth.",
        issue_count=n,
        evidence={"unique_inlinks": n},
    )


def _check_internal_link_equity(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    """Score the PageRank percentile the canonical link-score job already wrote."""
    if facts.link_score is None:
        return CheckOutcome(
            "n_a",
            None,
            "This page does not have an internal link-equity score yet. Finish a "
            "full crawl so the site's canonical PageRank can be computed.",
            remediation=RECRAWL_SITE,
        )
    percentile = site.link_equity_percentile_by_page.get(facts.page_id)
    if percentile is None:
        return CheckOutcome(
            "n_a",
            None,
            "The site's link-equity distribution could not be built from the "
            "stored PageRank scores. Recompute it with a full crawl.",
            remediation=RECRAWL_SITE,
        )

    prioritized = bool(facts.target_keyword and facts.target_keyword.strip())
    score = percentile
    priority_penalty = prioritized and percentile < LINK_EQUITY_PRIORITY_QUARTILE
    if priority_penalty:
        score = min(score, LINK_EQUITY_PRIORITY_SCORE_CAP)

    if score >= LINK_EQUITY_PASS_SCORE:
        status = "pass"
    elif score >= LINK_EQUITY_WARN_SCORE:
        status = "warn"
    else:
        status = "fail"

    evidence = {
        "link_score": facts.link_score,
        "pagerank_percentile": percentile,
        "pages_scored": len(site.link_equity_percentile_by_page),
        "prioritized": prioritized,
        "priority_penalty_applied": priority_penalty,
    }
    if status == "pass":
        return CheckOutcome(
            "pass",
            score,
            f"This page is in the {percentile}th percentile of the site's internal "
            "PageRank distribution — internal links give it strong visibility.",
            evidence=evidence,
        )
    priority_note = (
        f' It is prioritized for "{facts.target_keyword}", so its bottom-quartile '
        "position is capped at 40 by the catalogue contract."
        if priority_penalty
        else ""
    )
    return CheckOutcome(
        status,
        score,
        f"This page is only in the {percentile}th percentile of the site's internal "
        "PageRank distribution — stronger contextual links from important pages "
        f"would pass more authority to it.{priority_note}",
        issue_count=1,
        evidence=evidence,
    )


def _check_orphan_pages(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    census = site.orphans
    blocked = _partial_graph_outcome(site)
    if blocked is not None:
        return blocked
    if facts.page_id == site.homepage_page_id:
        return CheckOutcome(
            "pass", 100, "This is the site root — the entry point is never an orphan."
        )
    if len(site.inlinks.get(facts.page_id, ())) > 0:
        return CheckOutcome(
            "pass",
            100,
            "This page is linked from elsewhere on the site."
            + (
                f" (Site-wide, {census.total} of {census.known_live_pages} known "
                f"live pages are orphaned, {census.uncrawled_orphans} of them known "
                "only from a sitemap/GSC and never captured.)"
                if census.total
                else ""
            ),
        )
    site_wide = (
        f"Site-wide, {census.total} of {census.known_live_pages} known live pages "
        f"are orphaned ({census.uncrawled_orphans} of those were never captured at "
        "all)."
    )
    if not facts.latest_snapshot_id:
        # Known from a sitemap, GSC, or a manual import — never captured. It is
        # orphaned in the same link graph, but it is NOT a confirmed page with
        # no inlinks: it may not resolve at all. Saying otherwise sends the user
        # hunting for a linking problem when the URL itself may be the problem.
        return CheckOutcome(
            "fail",
            census.site_score(),
            "This URL is known from a sitemap, Search Console, or a manual import, "
            "nothing on the site links to it, and we have never successfully "
            f"captured it — so we cannot confirm the page even exists. {site_wide} "
            "Check the URL loads, then link to it from a relevant page.",
            issue_count=1,
            evidence={
                "captured": False,
                "crawled_orphans": len(census.crawled_orphan_ids),
                "known_uncrawled_orphans": census.uncrawled_orphans,
                "known_live_pages": census.known_live_pages,
            },
            remediation=RECAPTURE_PAGE,
        )
    return CheckOutcome(
        "fail",
        census.site_score(),
        "This page was crawled successfully but NOTHING on the site links to it — "
        "search engines and visitors can only reach it if they already know the "
        f"URL. {site_wide}",
        issue_count=1,
        evidence={
            "captured": True,
            "crawled_orphans": len(census.crawled_orphan_ids),
            "known_uncrawled_orphans": census.uncrawled_orphans,
            "known_uncrawled_orphan_samples": sample_urls(census.uncrawled_orphan_urls),
            "known_live_pages": census.known_live_pages,
        },
    )


# ---------------------------------------------------------------------------
# `search_signals` — the checks that read GOOGLE'S OWN numbers.
#
# These are not inferences about how a page might perform; they are what Google
# reported it actually did. They live here rather than in `seo_audit` for a
# structural reason: the evidence is `web.gsc_page_stat` rows, and `seo_audit`
# is a standalone module that never touches the database.


def _gsc_windows(latest: date) -> tuple[tuple[date, date], ...]:
    """The three comparison windows, ending at the freshest synced day.

    Anchored to the DATA, never to "today": GSC lags reality by a couple of
    days, and a sweep run on a Monday must not report a phantom collapse just
    because the weekend has not landed yet.
    """
    current_start = latest - timedelta(days=GSC_PERIOD_DAYS - 1)
    prior_end = current_start - timedelta(days=1)
    prior_start = prior_end - timedelta(days=GSC_PERIOD_DAYS - 1)
    quarter_end = latest - timedelta(days=GSC_DECAY_QUARTER_LAG_DAYS)
    quarter_start = quarter_end - timedelta(days=GSC_PERIOD_DAYS - 1)
    return (current_start, latest), (prior_start, prior_end), (quarter_start, quarter_end)


def expected_ctr_for_position(position: float) -> float:
    """The CTR a page at this average position would normally earn."""
    rank = max(1, round(position))
    if rank <= len(GSC_EXPECTED_CTR_BY_POSITION):
        return GSC_EXPECTED_CTR_BY_POSITION[rank - 1]
    if rank <= GSC_EXPECTED_CTR_DEEP_POSITION:
        return GSC_EXPECTED_CTR_PAGE_TWO
    return GSC_EXPECTED_CTR_DEEP


def _gsc_status_for(score: int) -> str:
    if score >= GSC_PASS_SCORE_FLOOR:
        return "pass"
    return "warn" if score >= GSC_WARN_SCORE_FLOOR else "fail"


def _times(count: int) -> str:
    """ "once" / "1,240 times" — the reader is a person, not a log parser."""
    return "once" if count == 1 else f"{count:,} times"


def _people(count: int) -> str:
    return "1 person" if count == 1 else f"{count:,} people"


def _gsc_unavailable(site: SiteAggregates) -> CheckOutcome | None:
    """The site-level reason no Google data can be read, if there is one.

    Shared by every `search_signals` check so an unconnected site gets ONE
    consistent, non-technical explanation instead of four different ones.
    """
    gsc = site.gsc
    if not gsc.bound:
        return CheckOutcome(
            "n_a",
            None,
            "Google Search Console is not connected for this site — or its "
            "connection is switched off — so Google's own record of how this page "
            "performs in search cannot be read. Connect a Search Console property "
            "in this site's settings and this check starts answering.",
            # The parser's own sentence, kept OUT of the prose (it names a JSON
            # path) but attached so an operator can see which of the two it was.
            evidence={"gsc_binding": gsc.unbound_reason},
        )
    if not gsc.synced:
        return CheckOutcome(
            "n_a",
            None,
            "Search Console is connected but no data has been pulled from it yet, "
            "so there is nothing from Google to measure.",
            remediation=SYNC_GSC,
        )
    return None


def _check_gsc_ctr_opportunity(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    unavailable = _gsc_unavailable(site)
    if unavailable is not None:
        return unavailable
    gsc = site.gsc
    window = f"the {GSC_PERIOD_DAYS} days ending {gsc.latest_date:%-d %b %Y}"
    current = (gsc.by_page.get(facts.page_id) or PageGscStats()).current
    if current.impressions <= 0:
        return CheckOutcome(
            "n_a",
            None,
            f"Google never showed this page in search results during {window}, so "
            "there is no click-through rate to judge.",
        )
    if current.impressions < GSC_CTR_MIN_IMPRESSIONS:
        return CheckOutcome(
            "n_a",
            None,
            f"Google showed this page only {_times(current.impressions)} in {window} "
            f"— below the {GSC_CTR_MIN_IMPRESSIONS} appearances needed before a "
            "click-through rate means anything.",
        )
    if current.position is None:
        return CheckOutcome(
            "n_a",
            None,
            f"Google reported {current.impressions} impressions for this page in "
            f"{window} but no average position, so there is nothing to compare its "
            "click-through rate against.",
        )

    actual = current.ctr or 0.0
    expected = expected_ctr_for_position(current.position)
    ratio = actual / expected
    expected_clicks = round(expected * current.impressions)
    missed_clicks = max(0, expected_clicks - current.clicks)
    evidence = {
        "window": {"days": GSC_PERIOD_DAYS, "ending": gsc.latest_date.isoformat()},
        "impressions": current.impressions,
        "clicks": current.clicks,
        "ctr": round(actual, 4),
        "expected_ctr": expected,
        "average_position": round(current.position, 1),
        "missed_clicks": missed_clicks,
    }

    if ratio < GSC_CTR_SEVERE_RATIO and current.impressions >= GSC_CTR_SEVERE_IMPRESSIONS:
        score = GSC_CTR_SEVERE_SCORE
    elif ratio < GSC_CTR_POOR_RATIO:
        score = GSC_CTR_POOR_SCORE
    elif ratio < GSC_CTR_FAIR_RATIO:
        score = GSC_CTR_FAIR_SCORE
    else:
        score = GSC_HEALTHY_SCORE

    status = _gsc_status_for(score)
    if status == "pass":
        return CheckOutcome(
            "pass",
            score,
            f"Google showed this page {_times(current.impressions)} in {window} at "
            f"average position {current.position:.1f}, and {_people(current.clicks)} "
            f"clicked ({actual:.1%}) — at or above the {expected:.1%} a page in that "
            "spot normally earns.",
            evidence=evidence,
        )
    return CheckOutcome(
        status,
        score,
        f"Google showed this page {_times(current.impressions)} in {window} at "
        f"average position {current.position:.1f}, but only {_people(current.clicks)} "
        f"clicked ({actual:.1%}) — a page in that spot normally earns {expected:.1%}. "
        f"Roughly {missed_clicks:,} more visits would have come from the ranking this "
        "page has already earned; they went to competitors whose title and description "
        "read better in the results list. Rewriting those two lines is the cheapest "
        "win available here.",
        issue_count=1,
        evidence=evidence,
    )


def _check_gsc_performance_decay(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    unavailable = _gsc_unavailable(site)
    if unavailable is not None:
        return unavailable
    gsc = site.gsc
    if gsc.history_days < GSC_DECAY_MIN_HISTORY_DAYS:
        return CheckOutcome(
            "n_a",
            None,
            f"Only {gsc.history_days} day(s) of Search Console data have been pulled "
            f"for this site. Spotting a real decline means comparing the last "
            f"{GSC_PERIOD_DAYS} days against the same stretch a quarter ago, which "
            f"needs at least {GSC_DECAY_MIN_HISTORY_DAYS} days of history.",
            remediation=SYNC_GSC,
        )

    stats = gsc.by_page.get(facts.page_id) or PageGscStats()
    current, prior, quarter = stats.current, stats.prior, stats.quarter
    (_, _), (prior_start, prior_end), (quarter_start, quarter_end) = _gsc_windows(gsc.latest_date)
    if prior.clicks < GSC_DECAY_MIN_BASELINE_CLICKS:
        return CheckOutcome(
            "n_a",
            None,
            f"This page earned {prior.clicks} click(s) from Google in the "
            f"{GSC_PERIOD_DAYS} days before the current period, below the "
            f"{GSC_DECAY_MIN_BASELINE_CLICKS} needed before a drop can be told "
            "apart from ordinary week-to-week noise.",
        )

    prior_drop = (prior.clicks - current.clicks) / prior.clicks
    # The contract's top two bands require the decline to hold across BOTH
    # comparisons, so they read the SMALLER of the two.
    if quarter.clicks > 0:
        quarter_drop = (quarter.clicks - current.clicks) / quarter.clicks
        both_drop = min(prior_drop, quarter_drop)
    else:
        # Zero clicks a quarter ago is NOT missing data — the history gate above
        # already proved that window is synced. The page simply earned nothing
        # then, so it cannot be in decline against it: there is no percentage to
        # report, and the both-comparison bands cannot apply. It can still trip
        # the third band on the prior-period comparison alone.
        quarter_drop = None
        both_drop = min(prior_drop, 0.0)
    evidence = {
        "current": {"clicks": current.clicks, "impressions": current.impressions},
        "prior": {
            "clicks": prior.clicks,
            "impressions": prior.impressions,
            "from": prior_start.isoformat(),
            "to": prior_end.isoformat(),
        },
        "quarter": {
            "clicks": quarter.clicks,
            "impressions": quarter.impressions,
            "from": quarter_start.isoformat(),
            "to": quarter_end.isoformat(),
        },
        "drop_vs_prior": round(prior_drop, 4),
        "drop_vs_quarter": None if quarter_drop is None else round(quarter_drop, 4),
    }

    if both_drop > GSC_DECAY_SEVERE_DROP:
        score = GSC_DECAY_SEVERE_SCORE
    elif both_drop >= GSC_DECAY_MODERATE_DROP:
        score = GSC_DECAY_MODERATE_SCORE
    elif prior_drop >= GSC_DECAY_MILD_DROP:
        score = GSC_DECAY_MILD_SCORE
    else:
        score = GSC_HEALTHY_SCORE

    if score == GSC_HEALTHY_SCORE:
        direction = "grown" if current.clicks >= prior.clicks else "held steady"
        return CheckOutcome(
            "pass",
            score,
            f"Google traffic to this page has {direction}: {current.clicks:,} clicks in "
            f"the last {GSC_PERIOD_DAYS} days against {prior.clicks:,} in the "
            f"{GSC_PERIOD_DAYS} before that.",
            evidence=evidence,
        )
    quarter_clause = f" and {quarter.clicks:,} a quarter ago" if quarter_drop is not None else ""
    return CheckOutcome(
        _gsc_status_for(score),
        score,
        f"Google traffic to this page is falling: {current.clicks:,} clicks in the "
        f"last {GSC_PERIOD_DAYS} days against {prior.clicks:,} in the "
        f"{GSC_PERIOD_DAYS} before that{quarter_clause} — down {prior_drop:.0%}. "
        "A page that used to earn traffic and no longer does is usually one whose "
        "answer has gone out of date while competitors published fresher ones. "
        "Refresh it before the ranking is gone entirely.",
        issue_count=1,
        evidence=evidence,
    )


# Cross-page checks — implemented here because each needs the whole site.
def index_page_facts(facts_list: list[PageFacts], aggregates: SiteAggregates) -> None:
    """Group the loaded page evidence into everything the cross-page checks read.

    Pure — no DB, no network. `_load_page_facts` calls it after the census, and
    it is the ONE place a cross-page grouping is built, so a test that exercises
    a cross-page check exercises the real aggregation rather than a hand-built
    lookalike that can silently disagree with it.
    """
    for facts in facts_list:
        title_norm = _norm_text(facts.title)
        if title_norm:
            aggregates.pages_by_title.setdefault(title_norm, []).append(facts)
        desc_norm = _norm_text(facts.description)
        if desc_norm:
            aggregates.pages_by_description.setdefault(desc_norm, []).append(facts)
        if facts.exact_sha256 is not None and facts.fingerprint_version is not None:
            aggregates.pages_by_sha.setdefault(
                (facts.fingerprint_version, facts.exact_sha256), []
            ).append(facts)
        # The site's business identity + the hreflang graph, from evidence the
        # snapshot already carries.
        if facts.structured_data:
            aggregates.business.pages_captured += 1
            aggregates.business.entities.extend(business_entities_in(facts.structured_data))
        entries = hreflang_entries(facts)
        # A crawled page with NO hreflang still has to be KNOWN, or a target that
        # merely forgot its return tag would read as "we never crawled it".
        targets = aggregates.hreflang_targets.setdefault(normalized_url_key(facts.url), set())
        targets.update(normalized_url_key(href) for _, href in entries)

    # Inclusive percentile rank: all pages tied for the highest score receive
    # 100, and ties elsewhere receive the same deterministic rank. This is the
    # catalogue's `pagerank_percentile`, built from the already-persisted
    # `web.page.link_score` values without loading or recomputing the graph.
    scored = sorted(facts.link_score for facts in facts_list if facts.link_score is not None)
    if scored:
        total = len(scored)
        for facts in facts_list:
            if facts.link_score is None:
                continue
            aggregates.link_equity_percentile_by_page[facts.page_id] = clamp_score(
                round(100 * bisect_right(scored, facts.link_score) / total)
            )


def _check_local_business_markup(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    """Does this SITE declare a complete, self-consistent business entity?

    The catalogue row is site-level by construction — "anywhere on site" and
    "across own pages" are questions one page cannot answer — so the verdict is
    computed from the site aggregate and recorded on every page subject.
    """
    business = site.business
    if business.pages_captured == 0:
        return CheckOutcome(
            "n_a",
            None,
            "We haven't captured structured data for any page on this site yet.",
            remediation=RECRAWL_SITE,
        )
    if not business.entities:
        return CheckOutcome(
            "warn",
            50,
            "No page on this site says who the business is in structured data "
            "(Organization or LocalBusiness markup). Search engines then have to "
            "infer your name, address and phone number from page text, and map, "
            "knowledge-panel and local results are the first things you lose.",
            issue_count=1,
        )

    # The most complete declaration is the site's claim; a stub entity on one
    # page must not condemn a full one on another.
    def stated(entity: dict[str, Any]) -> int:
        return sum(1 for prop in BUSINESS_CORE_PROPERTIES if entity.get(prop))

    best = max(business.entities, key=stated)
    missing_core = [prop for prop in BUSINESS_CORE_PROPERTIES if not best.get(prop)]
    if len(missing_core) >= BUSINESS_MISSING_CORE_FAIL_COUNT:
        return CheckOutcome(
            "warn",
            65,
            f"The business markup on this site never states its "
            f"{' or '.join(missing_core)}. Those are the properties local search "
            "matches on, so incomplete markup is close to no markup at all.",
            issue_count=len(missing_core),
            evidence={"missing": missing_core, "types": best.get("types")},
        )

    conflicts: dict[str, list[str]] = {}
    for prop in BUSINESS_CORE_PROPERTIES:
        values = sorted({e[prop] for e in business.entities if e.get(prop)})
        if len(values) > 1:
            conflicts[prop] = values[:STRUCTURED_DATA_EVIDENCE_LIMIT]
    if conflicts:
        return CheckOutcome(
            "warn",
            55,
            "Pages on this site disagree about the business's "
            f"{', '.join(conflicts)} in their structured data. Search engines "
            "treat conflicting name/address/phone values as two different "
            "businesses and trust neither.",
            issue_count=len(conflicts),
            evidence={"conflicting_values": conflicts},
        )

    missing_enhanced = [prop for prop in BUSINESS_ENHANCED_PROPERTIES if not best.get(prop)]
    detail = (
        f" It does not state {', '.join(missing_enhanced)}, which local results use "
        "when they have it."
        if missing_enhanced
        else ""
    )
    return CheckOutcome(
        "pass",
        100,
        f"The site declares a consistent {'/'.join(best.get('types') or ['business'])} "
        f"entity with its name, address and phone number.{detail}",
        evidence={"missing_recommended": missing_enhanced} if missing_enhanced else None,
    )


def _check_hreflang_reciprocity(facts: PageFacts, site: SiteAggregates) -> CheckOutcome:
    """Do this page's hreflang targets link BACK to it?

    Google ignores an annotation with no return tag, so a one-way hreflang set
    is work that buys nothing. Reciprocity is verifiable only for targets this
    crawl actually holds: a target on ANOTHER site (the common case for a
    country-domain cluster — example.de ↔ example.fr) cannot be confirmed or
    denied from this site's crawl, and is reported as such rather than failed.
    """
    entries = hreflang_entries(facts)
    if not entries:
        return CheckOutcome(
            "n_a", None, "This page declares no hreflang annotations to return-check."
        )

    self_key = normalized_url_key(facts.url)
    self_host = registrable_host(facts.url)
    targets = {
        normalized_url_key(href): href
        for _, href in entries
        if normalized_url_key(href) != self_key
    }
    if not targets:
        return CheckOutcome(
            "pass",
            100,
            "This page's only hreflang annotation is its own self-reference, so "
            "there is no return tag to be missing.",
        )

    off_site: list[str] = []
    uncrawled: list[str] = []
    reciprocal: list[str] = []
    missing: list[str] = []
    for key, href in targets.items():
        if registrable_host(href) != self_host:
            off_site.append(href)
        elif key not in site.hreflang_targets:
            uncrawled.append(href)
        elif self_key in site.hreflang_targets[key]:
            reciprocal.append(href)
        else:
            missing.append(href)

    verifiable = len(reciprocal) + len(missing)
    if verifiable == 0:
        unverifiable = off_site + uncrawled
        why = (
            "they live on other domains, which this site's crawl cannot see into"
            if off_site and not uncrawled
            else "this crawl does not include them"
        )
        return CheckOutcome(
            "n_a",
            None,
            f"This page names {len(unverifiable)} language version(s), but {why}. "
            "Return tags can only be confirmed against pages we have crawled — "
            "crawl the other site to check the pair.",
            evidence={"unverified_targets": sample_urls(unverifiable)},
            remediation=RECRAWL_SITE if uncrawled else None,
        )

    score = clamp_score(round(100 * len(reciprocal) / verifiable))
    if not missing:
        note = (
            f" ({len(off_site) + len(uncrawled)} more are on pages this crawl does "
            "not cover and were not judged.)"
            if off_site or uncrawled
            else ""
        )
        return CheckOutcome(
            "pass",
            100,
            f"All {verifiable} checkable hreflang target(s) link back to this page.{note}",
        )
    status = "fail" if score < HREFLANG_RECIPROCITY_FAIL_SCORE else "warn"
    return CheckOutcome(
        status,
        score,
        f"{len(missing)} of {verifiable} hreflang target(s) never link back to this "
        "page. Google discards a one-way annotation, so those language versions "
        "are being declared for nothing.",
        issue_count=len(missing),
        evidence={
            "missing_return_tags": sample_urls(missing),
            **(
                {"unverified_targets": sample_urls(off_site + uncrawled)}
                if off_site or uncrawled
                else {}
            ),
        },
    )


CROSS_PAGE_CHECKS: dict[str, Callable[[PageFacts, SiteAggregates], CheckOutcome]] = {
    "title_duplication": _check_title_duplication,
    "meta_description_duplication": _check_meta_description_duplication,
    "broken_internal_links": _check_broken_internal_links,
    "broken_external_links": _check_broken_external_links,
    "internal_redirect_links": _check_internal_redirect_links,
    "duplicate_content_exact": _check_duplicate_content_exact,
    # Internal linking / architecture — every one reads the site's own
    # `web.link_edge` graph, so none of them can live in the per-page module.
    "excessive_outlinks": _check_excessive_outlinks,
    "nofollow_internal_links": _check_nofollow_internal_links,
    "anchor_text_descriptiveness": _check_anchor_text_descriptiveness,
    "crawl_depth": _check_crawl_depth,
    "internal_inlink_coverage": _check_internal_inlink_coverage,
    "internal_link_equity": _check_internal_link_equity,
    "orphan_pages": _check_orphan_pages,
    # Search signals — Google's own reporting for this site (`web.gsc_page_stat`).
    # Cross-page by construction: the evidence is a site-wide load, and the
    # windows are anchored to the site's freshest synced day.
    "gsc_ctr_opportunity": _check_gsc_ctr_opportunity,
    "gsc_performance_decay": _check_gsc_performance_decay,
    # Structured data + international. Both read the whole site: the business
    # entity is declared once for the site, and a return tag by definition
    # lives on the OTHER page.
    "local_business_markup": _check_local_business_markup,
    "hreflang_reciprocity": _check_hreflang_reciprocity,
}

# ---------------------------------------------------------------------------
# SITE-SUBJECT checks. A second family, and a different subject: these describe
# the SITE (`subject_type='site'`, `subject_id == site_id`, `page_id` NULL —
# `web.validate_cross_pointers` enforces exactly that shape), not any one page.
# TLS and HSTS are properties of the host; the baseline security headers are
# sampled across pages because a header set that differs per page is itself the
# defect. Recording them per page would write the same verdict thousands of
# times and let one page "resolve" a finding the rest still trip.
#
# Every band below is the matching `web.analysis_item` row's `score_contract`,
# verbatim. Each function is PURE — evidence in, `CheckOutcome` out, no I/O.

# The four baseline headers `security_headers` scores, and the row's formula:
# 100 - 15 per missing header, floored at 40.
BASELINE_SECURITY_HEADERS: tuple[str, ...] = (
    "x-content-type-options",
    "x-frame-options",
    "referrer-policy",
    "content-security-policy",
)
SECURITY_HEADER_MISSING_PENALTY = 15
SECURITY_HEADER_MIN_SCORE = 40
# How many pages' header sets one site verdict samples. The catalogue row says
# "sampled across the site"; a full census would read every snapshot to answer
# a question a couple of dozen pages already answer.
SECURITY_HEADER_SAMPLE_LIMIT = 25

# HSTS max-age worth having: the row's "6 months", in seconds.
HSTS_MIN_MAX_AGE_SECONDS = 15_552_000

# Certificate expiry proximity bands, in days.
TLS_EXPIRY_CRITICAL_DAYS = 7
TLS_EXPIRY_WARN_DAYS = 21


@dataclass
class TlsFacts:
    """One site's TLS handshake facts.

    Produced from the persisted site probe. Missing or failed capture remains
    ``None`` so the check can never pass on a certificate nobody inspected.
    """

    days_to_expiry: int | None = None
    expired: bool = False
    trusted: bool = True
    hostname_match: bool = True
    issuer: str | None = None
    not_after: str | None = None


@dataclass
class SiteFacts:
    """Evidence for the SITE as a subject, derived from its pages.

    Built by `_build_site_facts` from the same `PageFacts` the per-page checks
    consume — no extra DB pass. `header_samples` holds only pages that actually
    captured headers, so "no samples" stays distinguishable from "no headers".
    """

    site_id: str
    pages_with_evidence: int = 0
    https_pages: int = 0
    http_pages: int = 0
    # (page url, security headers) for up to SECURITY_HEADER_SAMPLE_LIMIT pages
    # whose capture recorded headers at all.
    header_samples: list[tuple[str, dict[str, str]]] = field(default_factory=list)
    tls: TlsFacts | None = None
    # Crawlability evidence that is NOT derivable from the page census —
    # robots.txt, the sitemap graph, the host-variant probe. Loaded from the DB
    # by `site_analysis.load_site_evidence`; None means that load failed, which
    # the crawlability checks answer `n_a` for rather than guessing.
    crawlability: SiteEvidence | None = None
    # Canonical `seo.search_performance_daily` query×page evidence. This is
    # deliberately separate from legacy `web.gsc_page_stat` page totals.
    gsc_cannibalization: GscCannibalizationEvidence = field(
        default_factory=GscCannibalizationEvidence
    )
    near_duplicates: NearDuplicateReport | None = None


def _tls_facts_from_probe(probe: object, *, computed_at: datetime) -> TlsFacts | None:
    capture = getattr(probe, "tls", None)
    if capture is None or any(
        value is None for value in (capture.trusted, capture.hostname_match, capture.expired)
    ):
        return None
    days_to_expiry = None
    if capture.not_after:
        expires_at = datetime.fromisoformat(capture.not_after)
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)
        days_to_expiry = (expires_at - computed_at).days
    return TlsFacts(
        days_to_expiry=days_to_expiry,
        expired=capture.expired,
        trusted=capture.trusted,
        hostname_match=capture.hostname_match,
        issuer=capture.issuer,
        not_after=capture.not_after,
    )


def _hsts_max_age(value: str) -> int | None:
    match = re.search(r"max-age\s*=\s*\"?(\d+)", value, flags=re.IGNORECASE)
    return int(match.group(1)) if match else None


def _site_check_security_headers(site: SiteFacts) -> CheckOutcome:
    if not site.header_samples:
        return CheckOutcome(
            "n_a",
            None,
            "No response headers captured for any page of this site — re-crawl to "
            "collect them (older snapshots predate header capture).",
        )
    # A header counts as present only when EVERY sampled page sends it. Partial
    # coverage is the defect the sampling exists to find: a security header that
    # protects the homepage and not the checkout page protects nothing.
    coverage: dict[str, int] = {}
    for _url, headers in site.header_samples:
        has_csp = bool(headers.get("content-security-policy"))
        frame_ancestors = "frame-ancestors" in (headers.get("content-security-policy") or "")
        for name in BASELINE_SECURITY_HEADERS:
            if name == "x-frame-options":
                present = bool(headers.get(name)) or frame_ancestors
            elif name == "content-security-policy":
                present = has_csp
            else:
                present = bool(headers.get(name))
            coverage[name] = coverage.get(name, 0) + (1 if present else 0)

    sampled = len(site.header_samples)
    missing = [name for name in BASELINE_SECURITY_HEADERS if coverage.get(name, 0) < sampled]
    evidence = {
        "pages_sampled": sampled,
        "header_coverage": {name: coverage.get(name, 0) for name in BASELINE_SECURITY_HEADERS},
        "missing_headers": missing,
    }
    if not missing:
        return CheckOutcome(
            "pass",
            100,
            f"All {len(BASELINE_SECURITY_HEADERS)} baseline security headers are "
            f"present on every one of the {sampled} sampled page(s).",
            evidence=evidence,
        )
    score = max(
        SECURITY_HEADER_MIN_SCORE,
        100 - SECURITY_HEADER_MISSING_PENALTY * len(missing),
    )
    partial = [name for name in missing if 0 < coverage.get(name, 0) < sampled]
    detail = (
        f" {', '.join(partial)} appear on some pages but not all — inconsistent "
        "coverage is its own defect."
        if partial
        else ""
    )
    return CheckOutcome(
        "warn",
        clamp_score(score),
        f"{len(missing)} of {len(BASELINE_SECURITY_HEADERS)} baseline security "
        f"headers are not sent on every page ({', '.join(missing)}).{detail} These "
        "are the headers that stop your pages being framed, sniffed, or used to "
        "leak a visitor's referrer.",
        issue_count=len(missing),
        evidence=evidence,
    )


def _site_check_hsts_policy(site: SiteFacts) -> CheckOutcome:
    if not site.header_samples:
        return CheckOutcome(
            "n_a",
            None,
            "No response headers captured for any page of this site — re-crawl to "
            "collect them (older snapshots predate header capture).",
        )
    if site.https_pages == 0:
        return CheckOutcome(
            "n_a",
            None,
            "No page of this site is served over HTTPS, so HSTS does not apply yet "
            "(see https_enforcement — that is the failure to fix first).",
        )

    values = [
        (url, headers.get("strict-transport-security")) for url, headers in site.header_samples
    ]
    without = [url for url, value in values if not value]
    sampled = len(values)
    if without:
        return CheckOutcome(
            "warn",
            55,
            f"{len(without)} of {sampled} sampled page(s) send no "
            "Strict-Transport-Security header — a visitor's first request can still "
            "be made over plain HTTP and intercepted before the redirect happens.",
            issue_count=len(without),
            evidence={"pages_sampled": sampled, "pages_without_hsts": sample_urls(without)},
        )

    max_ages = {url: _hsts_max_age(value or "") for url, value in values}
    unparsable = [url for url, age in max_ages.items() if age is None]
    if unparsable:
        return CheckOutcome(
            "warn",
            55,
            f"{len(unparsable)} of {sampled} sampled page(s) send a "
            "Strict-Transport-Security header with no readable max-age — a policy "
            "with no lifetime is no policy.",
            issue_count=len(unparsable),
            evidence={"pages_sampled": sampled, "pages_unparsable": sample_urls(unparsable)},
        )

    weakest_url, weakest = min(max_ages.items(), key=lambda pair: pair[1] or 0)
    include_subdomains = all("includesubdomains" in (value or "").lower() for _url, value in values)
    evidence = {
        "pages_sampled": sampled,
        "min_max_age_seconds": weakest,
        "weakest_page": weakest_url,
        "include_subdomains": include_subdomains,
    }
    if (weakest or 0) < HSTS_MIN_MAX_AGE_SECONDS:
        return CheckOutcome(
            "warn",
            75,
            f"HSTS is present but its shortest max-age is {weakest} seconds — under "
            f"the {HSTS_MIN_MAX_AGE_SECONDS}-second (6 month) baseline, so browsers "
            "forget the policy quickly and the first-request window reopens.",
            issue_count=1,
            evidence=evidence,
        )
    suffix = (
        ""
        if include_subdomains
        else " Consider adding includeSubDomains so subdomains are covered too."
    )
    return CheckOutcome(
        "pass",
        100,
        f"HSTS is sent on every sampled page with a max-age of at least {weakest} seconds.{suffix}",
        evidence=evidence,
    )


def _site_check_tls_certificate(site: SiteFacts) -> CheckOutcome:
    tls = site.tls
    if tls is None:
        return CheckOutcome(
            "n_a",
            None,
            "No usable TLS certificate facts were captured for this site. Run a "
            "fresh crawl to retry the certificate trust, hostname and expiry check.",
            remediation=RECRAWL_SITE,
        )
    if tls.expired or not tls.trusted or not tls.hostname_match:
        reasons = []
        if tls.expired:
            reasons.append("it has EXPIRED")
        if not tls.trusted:
            reasons.append("its chain is not trusted")
        if not tls.hostname_match:
            reasons.append("it does not match this hostname")
        return CheckOutcome(
            "fail",
            1,
            "The TLS certificate is unusable: "
            + ", and ".join(reasons)
            + ". Every visitor gets a full-page browser warning and search engines "
            "stop crawling — this takes the site offline in practice.",
            issue_count=1,
            evidence={"issuer": tls.issuer, "not_after": tls.not_after},
        )
    days = tls.days_to_expiry
    if days is None:
        return CheckOutcome(
            "n_a",
            None,
            "The captured TLS facts carry no expiry date, so expiry proximity cannot be "
            "scored. Run a fresh crawl to retry the certificate inspection.",
            remediation=RECRAWL_SITE,
        )
    evidence = {
        "days_to_expiry": days,
        "issuer": tls.issuer,
        "not_after": tls.not_after,
    }
    if days <= TLS_EXPIRY_CRITICAL_DAYS:
        return CheckOutcome(
            "fail",
            20,
            f"The TLS certificate expires in {days} day(s). When it lapses every "
            "visitor sees a security warning instead of the site — renew now.",
            issue_count=1,
            evidence=evidence,
        )
    if days <= TLS_EXPIRY_WARN_DAYS:
        return CheckOutcome(
            "warn",
            50,
            f"The TLS certificate expires in {days} day(s) — inside the "
            f"{TLS_EXPIRY_WARN_DAYS}-day renewal window; confirm auto-renewal is "
            "working before it becomes an outage.",
            issue_count=1,
            evidence=evidence,
        )
    return CheckOutcome(
        "pass",
        100,
        f"The TLS certificate is valid, trusted, matches the hostname, and has "
        f"{days} day(s) to run.",
        evidence=evidence,
    )


def _site_check_near_duplicate_content(site: SiteFacts) -> CheckOutcome:
    report = site.near_duplicates
    if report is not None and report.indexable_pages == 0:
        return CheckOutcome(
            "n_a",
            None,
            "No indexable pages were available, so there is no valid denominator for "
            "the site-wide near-duplicate score.",
            evidence=report.evidence(),
            remediation=RECRAWL_SITE,
        )
    if report is None or report.score is None:
        missing_fingerprints = report.pages_without_fingerprint if report else 0
        missing_indexability = report.pages_without_indexability if report else 0
        return CheckOutcome(
            "n_a",
            None,
            "A complete site score needs both indexability and content fingerprints "
            f"for every page; this crawl is missing {missing_fingerprints} fingerprint(s) "
            f"and {missing_indexability} indexability verdict(s).",
            evidence=report.evidence() if report else {},
            remediation=RECRAWL_SITE,
        )
    if report.score >= 95:
        status = "pass"
    elif report.score >= 80:
        status = "warn"
    else:
        status = "fail"
    return CheckOutcome(
        status,
        report.score,
        f"{report.near_duplicate_pages} of {report.indexable_pages} indexable page(s) "
        f"belong to an unconsolidated cluster with at least 90% content similarity.",
        issue_count=report.near_duplicate_pages,
        evidence=report.evidence(),
    )


# Registry: catalogue item key -> site check. Each key MUST be a builtin
# `web.analysis_item` row whose `metadata.subject` is `site`.
def _adapt_crawlability(key: str) -> Callable[[SiteFacts], CheckOutcome]:
    """Give a crawlability check the site-registry signature. No logic, ever."""

    check = CRAWLABILITY_SITE_CHECKS[key]

    def run(site: SiteFacts) -> CheckOutcome:
        if site.crawlability is None:
            return CheckOutcome(
                "n_a",
                None,
                "We could not read this site's sitemap and robots evidence on this "
                "run, so we are not guessing at a score.",
                remediation=RECRAWL_SITE,
            )
        return check(site.crawlability)

    return run


SITE_CHECKS: dict[str, Callable[[SiteFacts], CheckOutcome]] = {
    "security_headers": _site_check_security_headers,
    "hsts_policy": _site_check_hsts_policy,
    "tls_certificate": _site_check_tls_certificate,
    "near_duplicate_content": _site_check_near_duplicate_content,
    "gsc_keyword_cannibalization": lambda site: check_gsc_keyword_cannibalization(
        site.gsc_cannibalization
    ),
    # Crawlability + URL architecture — the whole-site evidence no page carries.
    **{key: _adapt_crawlability(key) for key in CRAWLABILITY_SITE_CHECKS},
}


def _build_site_facts(site_id: str, facts_list: list[PageFacts]) -> SiteFacts:
    """Fold the per-page evidence into the site's own evidence. Pure."""
    facts = SiteFacts(site_id=site_id)
    for page in facts_list:
        scheme = urlsplit(page.url).scheme.lower()
        if scheme == "https":
            facts.https_pages += 1
        elif scheme == "http":
            facts.http_pages += 1
        if page.response_headers is None:
            continue
        facts.pages_with_evidence += 1
        if len(facts.header_samples) < SECURITY_HEADER_SAMPLE_LIMIT:
            facts.header_samples.append((page.url, dict(page.response_headers)))
    facts.near_duplicates = build_near_duplicate_report(
        [
            NearDuplicatePage(
                page_id=page.page_id,
                url=page.url,
                fingerprint_version=page.fingerprint_version,
                simhash64=page.simhash64,
                canonical_url=page.canonical_url,
                indexable=None if page.noindex is None else not page.noindex,
            )
            for page in facts_list
        ]
    )
    return facts


# Per-page checks this sweep emits — each name is a `seo_audit.PAGE_CHECKS`
# entry that also has a builtin `web.analysis_item` catalogue row. It is NOT a
# second implementation list: the function comes from `seo_audit`, this tuple
# only says which of them the catalogue can currently record.
#
# A canonical check missing from this tuple has no catalogue row yet. That is
# NOT allowed to be silent — `analyze_site_pages` screams about the gap on
# every run (see `_uncatalogued_page_checks`).
CATALOGUED_PAGE_CHECKS: tuple[str, ...] = (
    "title_presence",
    "title_length",
    "meta_description_presence",
    "meta_description_length",
    "h1_presence",
    # Outline + content volume. `content_depth` is the per-TYPE counterpart to
    # `thin_content`'s absolute floor and answers n_a when the page declares no
    # type — never a second thin-content verdict.
    "heading_hierarchy",
    "thin_content",
    "content_depth",
    "text_html_ratio",
    "image_alt_presence",
    # Images & media. All five read `snapshot.images.items`; `broken_images`
    # and `image_oversized` answer n_a until an image-fetch pass captures
    # per-image status and bytes (FOUND_DEFECTS.md).
    "image_dimension_attrs",
    "image_lazy_loading",
    "image_modern_format",
    "image_oversized",
    "broken_images",
    # Head metadata the capture already stored but nothing had ever judged:
    # the mobile viewport, the language tag, and the social share card.
    "viewport_meta",
    "html_lang_validity",
    "hreflang_validity",
    "structured_data_validity",
    "og_image_validity",
    "social_meta_completeness",
    "meta_robots_conflicts",
    "canonical_presence",
    "canonical_conflicts",
    "meta_refresh_redirect",
    # Transport + pagination. Every one of these existed ONLY in the deleted
    # aidream `IssueDetector`; each maps to a catalogue row that predated the
    # code by months and had never been populated by anything.
    "broken_page_4xx",
    "server_error_5xx",
    "redirect_chain",
    "redirect_loop",
    # Single-session tier only — the multi-session persistence band of
    # `temporary_redirect_usage` needs prior sessions this sweep never reads
    # (FOUND_DEFECTS.md), and `soft_404_detection` scores page-local signals
    # only (the site-404-template hash match is filed there too).
    "temporary_redirect_usage",
    "soft_404_detection",
    "mixed_content",
    "https_enforcement",
    "page_weight",
    "ttfb_server_response",
    "pagination_markup",
    # Pure URL-shape verdict. `seo_audit` owns the implementation; the sweep
    # supplies `web.page.url` through PageFacts and records the same outcome.
    "url_design_quality",
    # Lab performance. These score `seo.page_performance` — the PageSpeed store
    # matrx-seo writes — NOT the crawl: no HTTP fetch can produce a Core Web
    # Vital. A page PageSpeed has never measured answers n_a with the one-click
    # "measure this page", never a pass (`_load_lab_performance`).
    "cwv_lcp",
    "cwv_inp_tbt",
    "cwv_cls",
    "asset_delivery",
    "caching_policy",
)


def _adapt(key: str) -> Callable[[PageFacts, SiteAggregates], CheckOutcome]:
    """Give a per-page check the cross-page signature. No logic, ever."""
    check = SEO_PAGE_CHECKS[key]
    return lambda facts, _site: check(facts)


# Registry: catalogue item key -> check function. Adding a PER-PAGE check means
# adding it to `seo_audit.PAGE_CHECKS`, adding a `web.analysis_item` row, then
# naming it in CATALOGUED_PAGE_CHECKS. Never implement one here.
PAGE_CHECKS: dict[str, Callable[[PageFacts, SiteAggregates], CheckOutcome]] = {
    **{key: _adapt(key) for key in CATALOGUED_PAGE_CHECKS},
    **CROSS_PAGE_CHECKS,
}


def _uncatalogued_page_checks() -> list[str]:
    """Canonical per-page checks this sweep cannot record yet.

    A non-empty list means `seo_audit` gained a check whose `web.analysis_item`
    row was never seeded — real SEO evidence the platform computes and then
    throws away. Loud on every run until the catalogue catches up.
    """
    return sorted(set(SEO_PAGE_CHECKS) - set(CATALOGUED_PAGE_CHECKS))


# ---------------------------------------------------------------------------
# Evidence loading


def _page_link_facts(page: WebPage) -> tuple[float | None, str | None]:
    """Normalize optional page-ranking evidence at the model boundary.

    These columns are nullable and older/narrow projections may omit them
    entirely. Both states mean "not captured", never a score of zero or an
    empty target keyword.
    """
    raw_score = getattr(page, "link_score", None)
    raw_keyword = getattr(page, "target_keyword", None)
    return (
        float(raw_score) if raw_score is not None else None,
        raw_keyword.strip() if isinstance(raw_keyword, str) and raw_keyword.strip() else None,
    )


def _extract_page_facts(page: WebPage, snap: WebSnapshot) -> PageFacts:
    head = snap.head_tags or {}
    seo = snap.seo_metrics or {}
    audit = snap.audit_metrics or {}
    headings = snap.headings or {}
    images = snap.images or {}
    extracted = snap.extracted or {}
    indexability = audit.get("indexability") or {}
    audit_headings = audit.get("headings") or {}
    fingerprint = extracted.get("fingerprint") or {}

    title = head.get("title")
    description = head.get("meta_description")
    lang = head.get("lang")
    og = head.get("og")
    twitter = head.get("twitter")
    head_meta = head.get("meta")
    h1_count = headings.get("h1_count")
    if h1_count is None:
        h1_count = audit_headings.get("h1_count")

    # The complete outline in document order, and the page's own type claim —
    # what `heading_hierarchy` and `content_depth` read.
    heading_items = headings.get("all")
    if heading_items is None:
        heading_items = audit_headings.get("all")
    schema_types = (snap.structured_data or {}).get("schema_types")

    # Per-<img> inventory in DOM order — what the five images_media checks read.
    image_items = images.get("items")

    fp_version = fingerprint.get("version")
    exact_sha = fingerprint.get("exact_sha256")
    simhash64 = fingerprint.get("simhash64")

    # Transport evidence the capture already persisted. Carried even while the
    # matching catalogue rows are missing, so the transport checks light up the
    # moment those rows land — no second pass over the snapshots.
    perf = snap.perf or {}
    redirect_chain = extracted.get("redirect_chain")
    mixed_content = extracted.get("mixed_content")
    response_headers = extracted.get("response_headers")
    pagination = extracted.get("pagination")
    response_time_ms = perf.get("response_time_ms")
    # Absent on every snapshot captured before TTFB was measured, and on
    # anything the browser transport fetched. Left as None so the TTFB check
    # answers n_a — it must NEVER be back-filled from response_time_ms, which
    # includes the body download and would score a fast server as slow.
    ttfb_ms = perf.get("ttfb_ms")
    response_bytes = perf.get("bytes")
    # Visible-text bytes — the numerator of `text_html_ratio`. Absent on
    # snapshots captured before the field existed, which is an honest n_a.
    text_bytes = extracted.get("text_bytes")
    link_score, target_keyword = _page_link_facts(page)

    return PageFacts(
        page_id=str(page.id),
        url=str(page.url),
        title=title if isinstance(title, str) and title.strip() else None,
        title_metrics=seo.get("title") or {},
        description=description if isinstance(description, str) and description.strip() else None,
        description_metrics=seo.get("description") or {},
        meta_robots=head.get("meta_robots"),
        canonical_url=head.get("canonical_url"),
        canonical_matches=indexability.get("canonical_matches"),
        noindex=indexability.get("noindex"),
        nofollow=indexability.get("nofollow"),
        h1_count=int(h1_count) if isinstance(h1_count, int | float) else None,
        # The full outline (`headings.all`). `None` when the key is absent —
        # the snapshot predates it — so `heading_hierarchy` answers n_a instead
        # of reading "no headings" off a key that was never written.
        headings=(
            [item for item in heading_items if isinstance(item, dict)]
            if isinstance(heading_items, list)
            else None
        ),
        word_count=int(snap.word_count) if snap.word_count is not None else None,
        text_bytes=text_bytes if isinstance(text_bytes, int) else None,
        # schema.org @type values, for `content_depth`'s per-type expectation.
        schema_types=(
            [t for t in schema_types if isinstance(t, str)]
            if isinstance(schema_types, list)
            else None
        ),
        image_count=images.get("count") if isinstance(images.get("count"), int) else None,
        images_missing_alt=(
            images.get("missing_alt") if isinstance(images.get("missing_alt"), int) else None
        ),
        image_items=[item for item in image_items if isinstance(item, dict)]
        if isinstance(image_items, list)
        else [],
        fingerprint_version=fp_version if isinstance(fp_version, int) else None,
        exact_sha256=exact_sha if isinstance(exact_sha, str) else None,
        simhash64=simhash64 if isinstance(simhash64, str) else None,
        link_score=link_score,
        target_keyword=target_keyword,
        http_status=int(snap.http_status) if snap.http_status is not None else None,
        redirect_chain=[h for h in redirect_chain if isinstance(h, dict)]
        if isinstance(redirect_chain, list)
        else [],
        mixed_content=[u for u in mixed_content if isinstance(u, str)]
        if isinstance(mixed_content, list)
        else [],
        # Security headers captured at fetch time (allowlisted at the source by
        # `seo_audit.security_response_headers`). `None` — the key absent, or a
        # snapshot older than header capture — means the site security checks
        # answer `n_a`; `{}` means the server genuinely sent none of them.
        response_headers=(
            {k: v for k, v in response_headers.items() if isinstance(v, str)}
            if isinstance(response_headers, dict)
            else None
        ),
        response_bytes=response_bytes if isinstance(response_bytes, int) else None,
        response_time_ms=response_time_ms if isinstance(response_time_ms, int) else None,
        ttfb_ms=ttfb_ms if isinstance(ttfb_ms, int) else None,
        pagination=pagination if isinstance(pagination, dict) else {},
        # Head metadata. `og`/`twitter`/`meta` stay None when the snapshot never
        # carried the key, so their checks answer n_a rather than reporting a
        # tag as missing on evidence that was never captured.
        head_captured=True,
        lang=lang.strip() if isinstance(lang, str) and lang.strip() else None,
        og={k: v for k, v in og.items() if isinstance(v, str)} if isinstance(og, dict) else {},
        twitter=(
            {k: v for k, v in twitter.items() if isinstance(v, str)}
            if isinstance(twitter, dict)
            else {}
        ),
        head_meta=head_meta if isinstance(head_meta, dict) else None,
        # International + structured data. `snapshot.structured_data` is the
        # COMPLETE capture — parsed JSON-LD, the original script strings with
        # their parse errors, microdata, RDFa — so the checks validate the
        # stored payload and never re-parse the page.
        hreflang=[item for item in (head.get("hreflang") or []) if isinstance(item, dict)]
        if isinstance(head.get("hreflang"), list)
        else [],
        structured_data=snap.structured_data if isinstance(snap.structured_data, dict) else {},
        latest_snapshot_id=str(snap.id),
    )


def _extract_transport_facts(page: WebPage, crawl_url: dict[str, Any]) -> PageFacts:
    """Evidence for a URL the crawler attempted that produced NO snapshot.

    A 404, a 5xx, a timeout, or a redirect loop usually earns no
    ``web.snapshot`` at all — which is exactly why the transport checks would
    never fire for the URLs most likely to need them. ``web.crawl_url`` carries
    the terminal outcome (``http_status``) and the full hop chain
    (``metadata.redirect_chain``, written at insert by
    ``persistence.crawl_url_fetch_metadata``) for precisely this case.

    Every CONTENT field is left unset. That is the honest state — nothing was
    parsed — and the canonical checks answer ``n_a`` for absent evidence rather
    than passing on nothing (``test_seo_checks_single_source`` pins that).
    """

    metadata = crawl_url.get("metadata") or {}
    chain = metadata.get("redirect_chain") if isinstance(metadata, dict) else None
    link_score, target_keyword = _page_link_facts(page)
    http_status = crawl_url.get("http_status")
    return PageFacts(
        page_id=str(page.id),
        url=str(page.url),
        link_score=link_score,
        target_keyword=target_keyword,
        http_status=int(http_status) if http_status is not None else None,
        redirect_chain=[hop for hop in chain if isinstance(hop, dict)]
        if isinstance(chain, list)
        else [],
    )


def _crawl_url_recency(crawl_url: dict[str, Any]) -> tuple[datetime, int]:
    """Newest-attempt ordering key: completion time, then session sequence."""
    when = crawl_url.get("completed_at") or crawl_url.get("discovered_at")
    return (when, int(crawl_url.get("sequence") or 0))


async def _load_transport_only_facts(
    site_id: str,
    pages_without_snapshot: dict[str, WebPage],
    analyzed_page_ids: set[str],
    remaining: int,
    summary: AnalysisSummary,
) -> list[PageFacts]:
    """Facts for attempted URLs that never earned an accepted snapshot.

    Walks ``web.crawl_url`` (snapshot-less rows only) in id-keyset batches and
    keeps the NEWEST attempt per page. A row whose ``page_id`` is NULL, or
    whose page is not a live canonical HTML page of this site, is skipped and
    counted — never a failure, and never silent.

    Reads ``.values(...)`` projections, never hydrated models: a large site's
    ledger holds 100k+ snapshot-less rows (datadestruction: 176k), and this
    loader only needs six columns of each.
    """

    if remaining <= 0:
        return []

    latest_by_page: dict[str, dict[str, Any]] = {}
    last_id: str | None = None
    while True:
        filters: dict[str, object] = {
            "site_id": site_id,
            "deleted_at__isnull": True,
            "snapshot_id__isnull": True,
        }
        if last_id is not None:
            filters["id__gt"] = last_id
        rows = await (
            WebCrawlUrl.filter(**filters)
            .order_by("id")
            .limit(_CRAWL_URL_BATCH_SIZE)
            .values(
                "id",
                "page_id",
                "http_status",
                "metadata",
                "completed_at",
                "discovered_at",
                "sequence",
            )
        )
        if not rows:
            break
        last_id = str(rows[-1]["id"])

        for row in rows:
            if row["page_id"] is None:
                # The URL never resolved to a page row, so there is no
                # subject_id to record a verdict against.
                summary.crawl_urls_skipped_no_page += 1
                continue
            page_id = str(row["page_id"])
            if page_id in analyzed_page_ids:
                continue  # already analyzed from its snapshot — richer evidence wins
            page = pages_without_snapshot.get(page_id)
            if page is None:
                # Deleted, an alias, or non-HTML — the page census already
                # counted why it is out of scope.
                summary.crawl_urls_skipped_no_page += 1
                continue
            current = latest_by_page.get(page_id)
            if current is None or _crawl_url_recency(row) >= _crawl_url_recency(current):
                latest_by_page[page_id] = row

        if len(latest_by_page) >= remaining or len(rows) < _CRAWL_URL_BATCH_SIZE:
            break

    facts: list[PageFacts] = []
    for page_id, crawl_url in latest_by_page.items():
        if len(facts) >= remaining:
            break
        facts.append(_extract_transport_facts(pages_without_snapshot[page_id], crawl_url))
        summary.pages_skipped_no_snapshot -= 1
        summary.pages_transport_only += 1
    return facts


@dataclass
class _PageRegistry:
    """Every page row the sweep saw, kept for the site-wide link questions.

    ``graph_rows`` feeds ``link_score.build_site_graph`` — the ONE place that
    knows how a link target URL resolves to a canonical page — so an internal
    link that points at a redirecting alias credits the page it resolves to,
    exactly as link scoring does. ``census_rows`` is the orphan denominator:
    live, canonical, HTML-or-unknown pages, each flagged with whether the
    crawler ever actually captured it.
    """

    graph_rows: list[dict[str, object]] = field(default_factory=list)
    census_rows: list[tuple[str, str, bool]] = field(default_factory=list)
    complete: bool = True


async def _load_page_facts(
    site_id: str, summary: AnalysisSummary, root_url: str
) -> tuple[list[PageFacts], SiteAggregates]:
    facts_list: list[PageFacts] = []
    aggregates = SiteAggregates()
    registry = _PageRegistry()
    # Live canonical HTML pages with no accepted snapshot — the transport-only
    # candidates. A 404/5xx/loop URL lands here, and before 2026-08-09 it was
    # dropped from the sweep entirely.
    pages_without_snapshot: dict[str, WebPage] = {}
    last_id: str | None = None
    truncated = False
    census_start = perf_counter()
    while True:
        filters: dict[str, object] = {"site_id": site_id, "deleted_at__isnull": True}
        if last_id is not None:
            filters["id__gt"] = last_id
        pages = await WebPage.filter(**filters).order_by("id").limit(_PAGE_BATCH_SIZE).all()
        if not pages:
            break
        last_id = str(pages[-1].id)

        candidates: list[WebPage] = []
        for page in pages:
            summary.pages_total += 1
            # Aliases and non-HTML pages never get a verdict, but they DO
            # resolve link targets, so every row joins the graph registry.
            registry.graph_rows.append(
                {
                    "id": str(page.id),
                    "url_hash": str(page.url_hash),
                    "canonical_page_id": str(page.canonical_page_id or page.id),
                    "latest_snapshot_id": page.latest_snapshot_id,
                }
            )
            if str(page.canonical_page_id) != str(page.id):
                summary.pages_skipped_alias += 1
                continue
            if is_machine_resource(page.url, page.content_type_last):
                summary.pages_skipped_non_html += 1
                continue
            if page.status != _GONE_PAGE_STATUS:
                registry.census_rows.append(
                    (str(page.id), str(page.url), page.latest_snapshot_id is not None)
                )
            if page.latest_snapshot_id is None:
                summary.pages_skipped_no_snapshot += 1
                pages_without_snapshot[str(page.id)] = page
                continue
            candidates.append(page)

        for start in range(0, len(candidates), _SNAPSHOT_BATCH_SIZE):
            chunk = candidates[start : start + _SNAPSHOT_BATCH_SIZE]
            snapshot_ids = [str(p.latest_snapshot_id) for p in chunk]
            snapshots = await WebSnapshot.filter(id__in=snapshot_ids, deleted_at__isnull=True).all()
            by_id = {str(s.id): s for s in snapshots}
            for page in chunk:
                snap = by_id.get(str(page.latest_snapshot_id))
                if snap is None:
                    summary.pages_skipped_no_snapshot += 1
                    pages_without_snapshot[str(page.id)] = page
                    continue
                facts_list.append(_extract_page_facts(page, snap))

        if len(facts_list) >= _MAX_PAGES_PER_RUN:
            truncated = True
            registry.complete = False
            break
        if len(pages) < _PAGE_BATCH_SIZE:
            break

    summary.timings["page_census"] = round(perf_counter() - census_start, 3)

    step_start = perf_counter()
    facts_list.extend(
        await _load_transport_only_facts(
            site_id,
            pages_without_snapshot,
            {f.page_id for f in facts_list},
            _MAX_PAGES_PER_RUN - len(facts_list),
            summary,
        )
    )
    summary.timings["transport_only_facts"] = round(perf_counter() - step_start, 3)
    if len(facts_list) >= _MAX_PAGES_PER_RUN:
        truncated = True

    if truncated:
        summary.truncated = True
        summary.errors.append(
            f"page census truncated at {_MAX_PAGES_PER_RUN} pages — "
            "analysis covered the first slice only"
        )

    index_page_facts(facts_list, aggregates)

    step_start = perf_counter()
    await _load_lab_performance(facts_list)
    summary.timings["lab_performance"] = round(perf_counter() - step_start, 3)
    step_start = perf_counter()
    await _load_link_stats(site_id, facts_list, aggregates, registry, root_url)
    summary.timings["link_stats"] = round(perf_counter() - step_start, 3)
    return facts_list, aggregates


async def _load_lab_performance(facts_list: list[PageFacts]) -> None:
    """Attach each page's newest PageSpeed observation, in place.

    `seo.page_performance` is matrx-seo's table and its ONLY writer is the
    `run_collection("pagespeed_insights", …)` funnel; this reads it through the
    narrow mirror in `db/models_seo_host.py`. A page with no row keeps
    `lab_performance=None`, and every Core Web Vitals check answers `n_a` with
    a one-click "measure this page" — never an invented pass.

    MOBILE wins when both strategies were sampled: Google's Core Web Vitals
    thresholds (and the catalogue rows' bands) are the mobile ones, and mobile
    is the indexing crawler.

    One query per batch, `DISTINCT ON (page_id, strategy)` — at most two rows
    per page reach memory however long the sampling history is.
    """
    if not facts_list:
        return
    by_page = {facts.page_id: facts for facts in facts_list if facts.page_id}
    cutoff = datetime.now(UTC) - timedelta(days=LAB_PERFORMANCE_MAX_AGE_DAYS)
    page_ids = list(by_page)
    for start in range(0, len(page_ids), _LAB_PERFORMANCE_BATCH_SIZE):
        chunk = page_ids[start : start + _LAB_PERFORMANCE_BATCH_SIZE]
        rows = (
            await SeoPagePerformance.filter(page_id__in=chunk, observed_at__gte=cutoff)
            .distinct("page_id", "strategy")
            .order_by("page_id", "strategy", "-observed_at")
            .all()
        )
        newest: dict[str, SeoPagePerformance] = {}
        for row in rows:
            page_id = str(row.page_id)
            incumbent = newest.get(page_id)
            if incumbent is None or _lab_row_rank(row) > _lab_row_rank(incumbent):
                newest[page_id] = row
        for page_id, row in newest.items():
            by_page[page_id].lab_performance = lab_performance_from_lighthouse(
                row.lighthouse,
                strategy=str(row.strategy),
                observed_at=row.observed_at,
            )


def _lab_row_rank(row: SeoPagePerformance) -> tuple[int, datetime]:
    """Mobile first, then most recent — the pick order for one page's samples."""
    return (1 if str(row.strategy) == "mobile" else 0, row.observed_at)


async def _load_gsc_stats(site: WebSite, aggregates: SiteAggregates) -> None:
    """Roll `web.gsc_page_stat` up into the three comparison windows.

    FOUR queries total, whatever the size of the site: one for the synced date
    span, then one grouped rollup per window. The per-day rows are never loaded
    — a 20k-page site with a year of history is millions of rows, and the
    checks only ever read per-page totals.

    Binding is resolved through `gsc_sync.parse_gsc_binding`, the ONE parser of
    that shape, so "connected" here can never mean something different from
    what the sync itself would accept.
    """

    from matrx_scraper.web_crawl.gsc_sync import parse_gsc_binding

    try:
        parse_gsc_binding(site.integrations)
    except ValueError as exc:
        aggregates.gsc = SiteGscEvidence(bound=False, unbound_reason=str(exc))
        return

    evidence = SiteGscEvidence(bound=True)
    aggregates.gsc = evidence
    site_id = str(site.id)
    span = await (
        WebGscPageStat.filter(site_id=site_id, deleted_at__isnull=True)
        .group_by("site_id")
        .annotate(earliest=Min("date"), latest=Max("date"))
        .values("earliest", "latest")
    )
    if not span or span[0]["latest"] is None:
        return
    evidence.earliest_date = span[0]["earliest"]
    evidence.latest_date = span[0]["latest"]

    windows = _gsc_windows(evidence.latest_date)
    for name, (start, end) in zip(("current", "prior", "quarter"), windows, strict=True):
        rows = await (
            WebGscPageStat.filter(
                site_id=site_id,
                deleted_at__isnull=True,
                date__gte=start,
                date__lte=end,
            )
            .group_by("page_id")
            .annotate(
                clicks=Sum("clicks"),
                impressions=Sum("impressions"),
                position=Avg("position"),
            )
            .values("page_id", "clicks", "impressions", "position")
        )
        for row in rows:
            stats = evidence.by_page.setdefault(str(row["page_id"]), PageGscStats())
            position = row["position"]
            setattr(
                stats,
                name,
                GscPeriod(
                    clicks=int(row["clicks"] or 0),
                    impressions=int(row["impressions"] or 0),
                    position=float(position) if position is not None else None,
                ),
            )


def _rel_tokens(rel: str | None) -> set[str]:
    return {token for token in re.split(r"[\s,]+", (rel or "").lower()) if token}


def _accumulate_edge(
    row: dict[str, object],
    stats: PageLinkStats,
    graph: SiteLinkGraph,
    aggregates: SiteAggregates,
    adjacency: dict[str, set[str]],
) -> None:
    """Fold ONE ``web.link_edge`` row into every aggregate that reads it."""

    target_url = str(row["target_url"])
    http_status = row["http_status"]
    stats.outlinks_total += 1

    if not row["is_internal"]:
        if http_status is not None:
            stats.external_checked += 1
            if int(http_status) == 0 or int(http_status) >= 400:
                stats.external_broken.append(target_url)
        return

    stats.internal_outlinks += 1
    if http_status is not None:
        stats.checked += 1
        status = int(http_status)
        if status == 0 or status >= 400:
            stats.broken.append(target_url)
        elif 300 <= status < 400:
            stats.redirecting.append(target_url)

    if _rel_tokens(row["rel"]) & NOFOLLOW_REL_TOKENS:
        stats.nofollow_internal_count += 1
        if len(stats.nofollow_internal_samples) < CHECK_EVIDENCE_SAMPLE_LIMIT:
            stats.nofollow_internal_samples.append(target_url)

    if _is_descriptive_anchor(row["anchor_text"]):
        stats.descriptive_anchors += 1
    elif len(stats.generic_anchor_targets) < CHECK_EVIDENCE_SAMPLE_LIMIT:
        stats.generic_anchor_targets.append(target_url)

    source_id = graph.canonical_by_page.get(str(row["source_page_id"]))
    target_id = graph.canonical_by_hash.get(url_hash(_normalise_url(target_url)))
    if source_id is None or target_id is None or source_id == target_id:
        # An unregistered target (a link to a URL the crawl never registered)
        # or a self-link. Neither is an inbound signal, and neither shortens a
        # click path. `link_score` drops the same rows for the same reason.
        return
    aggregates.internal_edges_resolved += 1
    aggregates.inlinks.setdefault(target_id, set()).add(source_id)
    adjacency.setdefault(source_id, set()).add(target_id)


def _bfs_depths(homepage_id: str, adjacency: dict[str, set[str]]) -> dict[str, int]:
    """Clicks from the homepage — a plain BFS, so the answer is the SHORTEST path."""

    depths = {homepage_id: 0}
    frontier = [homepage_id]
    depth = 0
    while frontier:
        depth += 1
        next_frontier: list[str] = []
        for node in frontier:
            for target in adjacency.get(node, ()):
                if target not in depths:
                    depths[target] = depth
                    next_frontier.append(target)
        frontier = next_frontier
    return depths


def _build_orphan_census(registry: _PageRegistry, aggregates: SiteAggregates) -> OrphanCensus:
    """The orphan population, with the two classes kept apart.

    A page with zero inbound internal links is orphaned either way, but WHAT we
    know about it differs completely: one was fetched and rendered (a real dead
    end in the graph), the other exists only as a URL somebody listed and may
    not even resolve. Conflating them turns "your sitemap is stale" into "your
    site is broken".
    """

    census = OrphanCensus(complete=registry.complete)
    for page_id, url, captured in registry.census_rows:
        census.known_live_pages += 1
        census.captured_pages += 1 if captured else 0
        if page_id == aggregates.homepage_page_id:
            continue
        if aggregates.inlinks.get(page_id):
            continue
        if captured:
            census.crawled_orphan_ids.add(page_id)
            continue
        census.uncrawled_orphans += 1
        if len(census.uncrawled_orphan_urls) < CHECK_EVIDENCE_SAMPLE_LIMIT:
            census.uncrawled_orphan_urls.append(url)
    return census


async def _load_link_stats(
    site_id: str,
    facts_list: list[PageFacts],
    aggregates: SiteAggregates,
    registry: _PageRegistry,
    root_url: str,
) -> None:
    """ONE pass over the site's CURRENT link edges → every link aggregate.

    Per-source verified statuses (broken/redirecting, internal and external
    counted apart — ``link_check.check_site_links`` populates ``http_status``
    on both, and the external half went unaudited until 2026-08-09), plus the
    structural facts the internal-linking items read: outbound volume, internal
    nofollows, anchor descriptiveness, the inbound-link map, and the click-depth
    BFS from the homepage.

    Historical crawl edges would inflate every one of those counts, so edges are
    scoped to each page's latest snapshot — the same definition of "current"
    that ``link_score`` and ``insights`` use. Snapshots are chunked, and edges
    are keyset-paginated INSIDE each chunk, because a 20k-page site's edge table
    does not fit in memory (nor does it need to).

    Verified-status counts still admit only edges with a non-NULL
    ``http_status``: ``0`` means "no response" (dead), NULL means "never
    checked" and is excluded. Structural counts admit every edge — they are
    facts of the page's own markup and need no link check to be true.
    """

    graph = build_site_graph(registry.graph_rows)
    adjacency: dict[str, set[str]] = {}
    # Transport-only facts carry no snapshot id — they have no link edges to
    # roll up, and their outbound link checks stay `n_a`.
    snapshot_to_page = {f.latest_snapshot_id: f.page_id for f in facts_list if f.latest_snapshot_id}
    snapshot_ids = list(snapshot_to_page)
    for start in range(0, len(snapshot_ids), _SNAPSHOT_BATCH_SIZE):
        chunk = snapshot_ids[start : start + _SNAPSHOT_BATCH_SIZE]
        last_edge_id: str | None = None
        while True:
            filters: dict[str, object] = {
                "site_id": site_id,
                "snapshot_id__in": chunk,
                "deleted_at__isnull": True,
            }
            if last_edge_id is not None:
                filters["id__gt"] = last_edge_id
            rows = await (
                WebLinkEdge.filter(**filters)
                .order_by("id")
                .limit(_EDGE_BATCH_SIZE)
                .values(
                    "id",
                    "snapshot_id",
                    "source_page_id",
                    "target_url",
                    "is_internal",
                    "rel",
                    "anchor_text",
                    "http_status",
                )
            )
            if not rows:
                break
            last_edge_id = str(rows[-1]["id"])
            for row in rows:
                page_id = snapshot_to_page.get(str(row["snapshot_id"]))
                if page_id is None:
                    continue
                stats = aggregates.link_stats.setdefault(page_id, PageLinkStats())
                _accumulate_edge(row, stats, graph, aggregates, adjacency)
            if len(rows) < _EDGE_BATCH_SIZE:
                break

    aggregates.homepage_page_id = graph.canonical_by_hash.get(url_hash(_normalise_url(root_url)))
    if aggregates.homepage_page_id is not None:
        aggregates.depth_by_page = _bfs_depths(aggregates.homepage_page_id, adjacency)
    aggregates.orphans = _build_orphan_census(registry, aggregates)


# ---------------------------------------------------------------------------
# Catalogue + provider resolution


async def _resolve_catalogue() -> tuple[WebProvider, dict[str, WebAnalysisItem]]:
    provider = await WebProvider.get_or_none(key=RULES_PROVIDER_KEY)
    if provider is None:
        raise RuntimeError(
            f"analysis provider '{RULES_PROVIDER_KEY}' is missing from web.provider — "
            "the catalogue is the contract; seed it before running analysis"
        )
    registered = list(PAGE_CHECKS) + list(SITE_CHECKS)
    items = await WebAnalysisItem.filter(
        key__in=registered, is_builtin=True, deleted_at__isnull=True
    ).all()
    by_key: dict[str, WebAnalysisItem] = {}
    for item in items:
        if item.key in by_key:
            raise RuntimeError(
                f"analysis_item key '{item.key}' has multiple builtin rows — "
                "catalogue integrity violation; fix the catalogue first"
            )
        by_key[item.key] = item
    missing = sorted(set(registered) - set(by_key))
    if missing:
        raise RuntimeError(
            "analysis catalogue is missing builtin item(s) for registered checks: "
            + ", ".join(missing)
        )
    return provider, by_key


# ---------------------------------------------------------------------------
# Entry point


def _typed_evidence(item_key: str, evidence: dict) -> dict:
    """Stamp one check's evidence with its declared shape.

    The payload is computed by our own code, so its shape is knowable and
    therefore declared (`check_payloads`). Stamping `__kind` here — at the ONE
    seam where evidence enters the row — is what makes it renderable, typed on
    the frontend, and addressable by a workflow node, instead of an opaque blob
    every consumer has to re-guess.

    Loud-open, never lossy: an undeclared check or a payload the model rejects
    is logged and passed through UNCHANGED. Evidence we paid to compute is
    never dropped to satisfy a schema — the log is how the gap gets closed.
    """
    model = evidence_model_for(item_key)
    kind = evidence_kind_for(item_key)
    if model is None or kind is None:
        logger.warning(
            "analysis check %s emitted evidence with no declared payload shape "
            "(keys: %s) — add a model to matrx_scraper.check_payloads",
            item_key,
            ", ".join(sorted(evidence)),
        )
        return evidence
    try:
        parsed = model.model_validate(evidence)
    except ValidationError:
        logger.exception(
            "analysis check %s produced evidence its declared shape %s rejects "
            "(keys: %s) — passing through untyped",
            item_key,
            kind,
            ", ".join(sorted(evidence)),
        )
        return evidence
    unknown = sorted(set(evidence) - set(model.model_fields))
    if unknown:
        logger.warning(
            "analysis check %s emitted undeclared evidence field(s) %s — kept, "
            "but %s should declare them",
            item_key,
            ", ".join(unknown),
            model.__name__,
        )
    # `exclude_unset` keeps exactly the keys this branch supplied, so an
    # explicit null ("measured, absent") stays distinct from "branch never set
    # it" — and `extra="allow"` carries anything undeclared through intact.
    return {"__kind": kind, **parsed.model_dump(exclude_unset=True)}


def _result_metadata(outcome: CheckOutcome, item_key: str) -> dict:
    """The `web.analysis_result.metadata` envelope for one verdict."""
    metadata: dict = {
        "reasoning": outcome.reasoning,
        "analyzer": {"version": ANALYZER_VERSION},
    }
    if outcome.evidence:
        metadata["evidence"] = _typed_evidence(item_key, outcome.evidence)
    if outcome.remediation is not None:
        # The one-click fix, machine-readable. matrx-frontend reads
        # `metadata.remediation` off the row and renders the button — the
        # reasoning sentence never tells a user to run a command (NO DEAD ENDS).
        metadata["remediation"] = asdict(outcome.remediation)
    return metadata


def _tally(summary: AnalysisSummary, status: str) -> None:
    summary.checks_run += 1
    if status == "pass":
        summary.passes += 1
    elif status == "warn":
        summary.warns += 1
    elif status == "fail":
        summary.fails += 1
    elif status == "n_a":
        summary.not_applicable += 1
    else:
        summary.check_errors += 1


def stamp_http_variant_evidence(
    facts_list: list[PageFacts],
    probe: SiteProbe | None,
    root_url: str,
) -> str | None:
    """Give every page the best http:// evidence available for it.

    `https_enforcement`'s redirect bands are about THIS page's insecure twin.
    The PAGE's own probe is used whenever the site probe sampled that path; the
    site's http:// ORIGIN result is the fallback and labels itself
    (`scope="origin"`) so the check never claims more than it has. Before
    2026-08-13 every page was stamped with the origin, so a server that
    redirects its root while answering deep paths over HTTP scored `pass`
    site-wide — the defect this function exists to end.

    Returns a message when the evidence is DEGRADED (no page-level probe landed
    on a single analyzed page), so the caller can be loud about it. Never
    fatal: with neither probe the field stays None and the check answers `n_a`.
    """

    origin_variant = http_origin_probe(probe, root_url)
    page_hits = 0
    for facts in facts_list:
        page_variant = page_http_variant_probe(probe, facts.url)
        if page_variant is not None:
            facts.http_variant_probe = page_variant
            page_hits += 1
        elif origin_variant is not None:
            facts.http_variant_probe = origin_variant
    if not facts_list or page_hits:
        return None
    if origin_variant is not None:
        return (
            "No per-page http:// probe was stored for any analyzed page — "
            "https_enforcement scored its redirect bands from the site's http:// "
            "ORIGIN probe, which cannot see a deep path served over HTTP"
        )
    return (
        "No http:// probe was stored at all — https_enforcement can only judge "
        "each page's own scheme"
    )


async def analyze_site_pages(
    *,
    site_id: str,
    run_id: str | None = None,
    on_progress: ProgressCallback | None = None,
) -> AnalysisRunResult:
    """Run every registered deterministic page check for one site.

    ``run_id`` (optional) is the crawl session to stamp on the immutable
    results — the DB requires it to be a session of the SAME site. Importable
    directly (workflow-node ready); the standalone command and the post-crawl
    step are thin wrappers.
    """

    summary = AnalysisSummary(items_evaluated=sorted(set(PAGE_CHECKS) | set(SITE_CHECKS)))

    async def report(message: str) -> None:
        if on_progress is not None:
            await on_progress(message, summary)
        else:
            # The post-crawl path runs with no progress consumer; yield anyway
            # so a long pure-Python stretch cannot starve the event loop (and
            # with it the session heartbeat that keeps the reaper away).
            await asyncio.sleep(0)

    class _timed:
        """Time one named phase into ``summary.timings`` and report it.

        The timings dict is the profiler this worker ships with: a slow run's
        NDJSON stream and stored stats now NAME the hot phase instead of
        leaving the next agent to guess (the 2026-08-11 regression hid in an
        unmeasured evidence loader for two days).
        """

        def __init__(self, name: str) -> None:
            self.name = name

        async def __aenter__(self) -> None:
            self._start = perf_counter()

        async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
            elapsed = round(perf_counter() - self._start, 3)
            summary.timings[self.name] = elapsed
            if exc_type is None:
                await report(f"{self.name.replace('_', ' ').capitalize()} finished in {elapsed}s.")

    site = await WebSite.get_or_none(id=site_id, deleted_at__isnull=True)
    if site is None:
        raise LookupError(f"site {site_id} not found")
    organization_id = str(site.organization_id)

    uncatalogued = _uncatalogued_page_checks()
    if uncatalogued:
        # A canonical per-page check the platform computes but cannot record.
        # Never silent: real SEO evidence is being discarded every run.
        message = (
            "seo_audit defines per-page check(s) with no builtin web.analysis_item "
            "row — they are NOT being recorded: " + ", ".join(uncatalogued)
        )
        logger.error("ANALYSIS CATALOGUE BEHIND CODE — %s", message)
        summary.errors.append(message)

    provider, items_by_key = await _resolve_catalogue()
    await report("Loading page evidence…")
    async with _timed("page_evidence"):
        facts_list, aggregates = await _load_page_facts(site_id, summary, str(site.root_url))
    # Google's own numbers. A site with no Search Console property is the
    # ordinary case, not an error: the checks answer `n_a` naming that, and the
    # rest of the sweep is untouched.
    async with _timed("gsc_page_stats"):
        try:
            await _load_gsc_stats(site, aggregates)
        except Exception as exc:
            logger.exception("GSC evidence load failed for site %s", site_id)
            await capture_error(
                exc, kind="site_analysis_gsc_evidence_failed", context={"site_id": site_id}
            )
            summary.errors.append(
                f"Google Search Console evidence could not be loaded: {type(exc).__name__}: {exc}"
            )
            aggregates.gsc = SiteGscEvidence(
                bound=False,
                unbound_reason=(
                    f"reading the stored Search Console data failed — {type(exc).__name__}"
                ),
            )
    await report(f"Evaluating {len(PAGE_CHECKS)} checks across {len(facts_list)} pages…")

    stored_probe = load_site_probe(site)
    degraded = stamp_http_variant_evidence(facts_list, stored_probe, str(site.root_url))
    if degraded is not None:
        logger.warning("HTTPS EVIDENCE DEGRADED for site %s — %s", site_id, degraded)
        summary.errors.append(degraded)

    computed_at = datetime.now(UTC)
    # Results flush to the DB INCREMENTALLY (durable-work-queue baseline): a
    # run killed mid-way must leave its finished pages' observations behind,
    # not 39 minutes of work and zero rows (datadestruction, 3× on 2026-08-11).
    # `written` keeps every (row, created) pair for the finding reconciliation.
    rows: list[dict] = []
    written: list[tuple[dict, WebAnalysisResult]] = []

    async def flush_rows() -> None:
        if not rows:
            return
        created = await insert_results(rows)
        written.extend(zip(list(rows), created, strict=True))
        summary.results_written = len(written)
        rows.clear()

    async with _timed("page_checks"):
        for facts in facts_list:
            summary.pages_analyzed += 1
            for item_key, check in PAGE_CHECKS.items():
                item = items_by_key[item_key]
                try:
                    outcome = check(facts, aggregates)
                except Exception as exc:  # a broken rule must not kill the run
                    logger.exception(
                        "analysis check %s crashed on page %s", item_key, facts.page_id
                    )
                    summary.errors.append(
                        f"{item_key} crashed on {facts.url}: {type(exc).__name__}: {exc}"
                    )
                    await capture_error(
                        exc,
                        kind="page_analysis_check_failed",
                        context={"site_id": site_id, "page_id": facts.page_id, "item_key": item_key},
                    )
                    outcome = CheckOutcome(
                        "error", None, f"Check crashed: {type(exc).__name__}: {exc}"
                    )
                severity = severity_for(item, outcome.score)
                metadata = _result_metadata(outcome, item.key)
                rows.append(
                    {
                        "organization_id": organization_id,
                        "site_id": site_id,
                        "subject_type": "page",
                        "subject_id": facts.page_id,
                        "page_id": facts.page_id,
                        "item_id": str(item.id),
                        "item_key": item.key,
                        "category": item.category,
                        "subcategory": item.subcategory,
                        "provider_id": str(provider.id),
                        "provider_version": ANALYZER_VERSION,
                        "run_id": run_id,
                        "computed_at": computed_at,
                        "status": outcome.status,
                        "score": outcome.score,
                        "severity": severity,
                        "issue_count": outcome.issue_count,
                        "confidence": 1,
                        "metadata": metadata,
                    }
                )
                _tally(summary, outcome.status)
            if len(rows) >= _RESULT_INSERT_BATCH:
                await flush_rows()
            if summary.pages_analyzed % 200 == 0:
                await report(
                    f"Evaluated {summary.pages_analyzed}/{len(facts_list)} pages "
                    f"({summary.fails} fails, {summary.warns} warns so far)…"
                )

    # --- Site subjects. One row per site check, `subject_id == site_id` and
    # `page_id` NULL — `web.validate_cross_pointers` enforces exactly that
    # shape. These answer for the HOST, not for any one page: the TLS
    # certificate, the HSTS policy, and the baseline security headers sampled
    # across the site.
    site_facts = _build_site_facts(site_id, facts_list)
    if stored_probe is not None:
        site_facts.tls = _tls_facts_from_probe(stored_probe, computed_at=computed_at)
    async with _timed("gsc_cannibalization"):
        try:
            site_facts.gsc_cannibalization = await load_gsc_keyword_cannibalization(site_id)
        except Exception as exc:
            logger.exception("GSC cannibalization evidence load failed for site %s", site_id)
            await capture_error(
                exc,
                kind="site_analysis_gsc_cannibalization_failed",
                context={"site_id": site_id},
            )
            summary.errors.append(
                "GSC keyword cannibalization evidence could not be loaded: "
                f"{type(exc).__name__}: {exc}"
            )
    async with _timed("site_evidence"):
        try:
            site_facts.crawlability = await load_site_evidence(
                site=site,
                facts_list=facts_list,
                pages_truncated=summary.truncated,
            )
        except Exception as exc:
            # The page verdicts are already computed; a sitemap/robots read that
            # fails must not throw them away. It is never silent either — the
            # crawlability checks answer `n_a` and the run reports why.
            logger.exception("site-level evidence load failed for site %s", site_id)
            await capture_error(
                exc, kind="site_analysis_evidence_failed", context={"site_id": site_id}
            )
            summary.errors.append(
                f"site-level crawlability evidence could not be loaded: {type(exc).__name__}: {exc}"
            )
    for item_key, site_check in SITE_CHECKS.items():
        item = items_by_key[item_key]
        try:
            outcome = site_check(site_facts)
        except Exception as exc:  # a broken rule must not kill the run
            logger.exception("site analysis check %s crashed on site %s", item_key, site_id)
            await capture_error(
                exc,
                kind="site_analysis_check_failed",
                context={"site_id": site_id, "item_key": item_key},
            )
            summary.errors.append(
                f"{item_key} crashed on site {site_id}: {type(exc).__name__}: {exc}"
            )
            outcome = CheckOutcome("error", None, f"Check crashed: {type(exc).__name__}: {exc}")
        rows.append(
            {
                "organization_id": organization_id,
                "site_id": site_id,
                "subject_type": "site",
                "subject_id": site_id,
                "page_id": None,
                "item_id": str(item.id),
                "item_key": item.key,
                "category": item.category,
                "subcategory": item.subcategory,
                "provider_id": str(provider.id),
                "provider_version": ANALYZER_VERSION,
                "run_id": run_id,
                "computed_at": computed_at,
                "status": outcome.status,
                "score": outcome.score,
                "severity": severity_for(item, outcome.score),
                "issue_count": outcome.issue_count,
                "confidence": 1,
                "metadata": _result_metadata(outcome, item.key),
            }
        )
        summary.site_checks_run += 1
        _tally(summary, outcome.status)

    await report(f"Writing the final {len(rows)} analysis results…")
    async with _timed("result_writes"):
        await flush_rows()

    await report("Reconciling the finding register…")
    async with _timed("finding_reconciliation"):
        await reconcile_findings(
            site_id=site_id,
            organization_id=organization_id,
            computed_at=computed_at,
            results=written,
            summary=summary,
        )
    return AnalysisRunResult(
        summary,
        result_id=str(written[0][1].id) if written else None,
    )


__all__ = [
    "ANALYZER_VERSION",
    "CATALOGUED_PAGE_CHECKS",
    "CROSS_PAGE_CHECKS",
    "PAGE_CHECKS",
    "AnalysisRunResult",
    "GscPeriod",
    "OrphanCensus",
    "PageFacts",
    "PageGscStats",
    "PageLinkStats",
    "ProgressCallback",
    "RULES_PROVIDER_KEY",
    "SITE_CHECKS",
    "SiteAggregates",
    "SiteBusinessEvidence",
    "SiteGscEvidence",
    "expected_ctr_for_position",
    "SiteFacts",
    "TlsFacts",
    "analyze_site_pages",
    "index_page_facts",
]
