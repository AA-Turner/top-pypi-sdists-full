"""The SITE-level checks of the analysis catalogue.

``web.analysis_result`` has always supported three subject types — ``site``,
``page``, ``snapshot`` (``analysis_result_subject_type_valid``) — but until
2026-08-09 the sweep wrote page subjects only, so the catalogue's site-scoped
rows had nowhere to land. The four heaviest crawlability items were among them,
including ``robots_txt_health`` at weight 3.0, the joint-highest weight in the
whole catalogue.

**Why this is a sibling of ``analysis.py`` and not part of it.** The split is
per-page (``seo_audit``) vs whole-site (``web_crawl``), and both halves of the
whole-site work live in ``web_crawl``: ``analysis.py`` owns cross-PAGE checks —
they emit one verdict per page and read the page census — while this module
owns SITE-SUBJECT checks, which emit exactly one verdict for the site and read
evidence no page has (robots.txt, the sitemap graph, the host variants).
``analysis.py`` merges ``CRAWLABILITY_SITE_CHECKS`` into its ONE site-subject
registry (``analysis.SITE_CHECKS``, which also holds the TLS/HSTS/header
checks) and writes the rows; there is one sweep, one catalogue resolution, and
one finding reconciliation.

**Site subject shape (DB-enforced, ``web.validate_cross_pointers``):**
``subject_type='site'`` requires ``subject_id == site_id`` AND
``page_id IS NULL``. The same status/score contract as a page result applies —
``pass|warn|fail`` carry a score 1–100, ``n_a``/``error`` carry NULL.

**Every band below is its ``web.analysis_item`` row's ``score_contract`` made
executable.** The row is the spec; this is its ONE implementation.

**A pass on unverified evidence is a lie.** Each check answers ``n_a`` with a
one-click remediation whenever the evidence it needs was never captured — the
robots.txt file, the sitemap graph, or the host-variant probe. The capture
itself lives in ``site_probe.py``; this module never touches the network.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime

from matrx_scraper.db.models_web import (
    LinkEdge as WebLinkEdge,
    Page as WebPage,
    PageSitemap as WebPageSitemap,
    Site as WebSite,
    Sitemap as WebSitemap,
)
from matrx_scraper.robots_txt import RobotsDocument
from matrx_scraper.seo_audit import (
    RECRAWL_SITE,
    SYNC_SITEMAPS,
    CheckOutcome,
    Remediation,
    clamp_score,
    sample_urls,
)
from matrx_scraper.web_crawl.site_probe import SiteProbe, host_form, load_site_probe
from matrx_scraper.web_crawl.url_verify import VERIFICATION_METADATA_KEY

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Thresholds. Each is declared exactly ONCE, here, and is a band from the
# matching catalogue row's `score_contract`.

# Deterministic-rule checks score first-match-top-down and then map the score
# to a status. These two bounds are that mapping, and nothing else uses them.
#
# They are not arbitrary: they are the seam that makes every band below land on
# the status its own contract describes. 85 ("minor issues only", "housekeeping
# worth doing") passes — the same reading `excessive_outlinks` already applies
# to its own 85 band. 55 ("invalid directives", where the intended rules simply
# are not in force) warns. Everything the contracts call a blocking or
# duplicating condition — below 50 — fails.
SITE_PASS_MIN_SCORE = 85
SITE_WARN_MIN_SCORE = 50

# `robots_txt_health` (weight 3.0) — "Fatal availability/blocking issues floor
# the score; syntax and partial-blocking issues land mid-band; a missing file
# is only informational."
ROBOTS_SERVER_ERROR_SCORE = 5
ROBOTS_BLANKET_DISALLOW_SCORE = 5
ROBOTS_BLOCKS_WANTED_URLS_SCORE = 30
ROBOTS_SYNTAX_ERROR_SCORE = 55
ROBOTS_MISSING_SCORE = 80
ROBOTS_CLEAN_SCORE = 100
#: How many indexable/sitemap URLs are tested against the robots rules. The
#: answer is "does this file block URLs we want indexed" — a bounded sample
#: answers it; scanning 20k URLs to find the same yes would not change it.
ROBOTS_BLOCK_SCAN_LIMIT = 5_000

# `sitemap_health` (weight 2.0) — "Score reflects the dirtiest problem class
# present, then degrades with the share of junk entries."
SITEMAP_NONE_FOUND_SCORE = 50
SITEMAP_UNREACHABLE_SCORE = 20
SITEMAP_HEAVY_JUNK_SCORE = 35
SITEMAP_LIGHT_JUNK_SCORE = 65
SITEMAP_MINOR_ISSUE_SCORE = 85
SITEMAP_CLEAN_SCORE = 100
#: The junk-share boundary between the two junk bands, as a percentage.
SITEMAP_HEAVY_JUNK_PCT = 10.0
#: The protocol's per-document ceiling. Over it, a sitemap must be split —
#: advisory only, so it lands in the "minor issues" band.
SITEMAP_MAX_URLS_PER_DOC = 50_000

# `sitemap_coverage` (weight 1.5) —
# score = round(100 * covered_indexable/indexable_total)
#         - min(20, 2*sitemap_only_orphan_pct)
COVERAGE_HEALTHY_MIN_SCORE = 95
COVERAGE_GAPS_MIN_SCORE = 80
COVERAGE_ORPHAN_PENALTY_FACTOR = 2
COVERAGE_ORPHAN_PENALTY_MAX = 20

# `host_protocol_consistency` (weight 1.5) — "Multiple live versions split the
# site's identity."
HOST_MULTIPLE_LIVE_SCORE = 25
HOST_SOFT_REDIRECT_SCORE = 60
#: `<path>` and `<path>/` both serving their own 200 — the THIRD duplicate-URL
#: family the row's description has always named. Scored between the redirect
#: band and the internal-link band: it is a real duplicate (worse than links
#: merely disagreeing) but affects sampled paths, not the whole site identity.
HOST_SLASH_DUPLICATE_SCORE = 65
HOST_MIXED_INTERNAL_LINKS_SCORE = 70
HOST_CONSISTENT_SCORE = 100
#: The only redirect status that consolidates a duplicate host permanently.
HOST_PERMANENT_REDIRECT_STATUSES = frozenset({301, 308})

# Batch sizes. A site can carry 20k pages and tens of thousands of sitemap URLs;
# nothing below loads a whole table into one query.
_SITEMAP_MEMBERSHIP_BATCH = 2_000
_PAGE_LOOKUP_BATCH = 1_000
_LINK_EDGE_HOST_BATCH = 5_000
#: Internal edges scanned looking for a SECOND host form. The scan stops the
#: moment it finds one — this ceiling only bounds the "they are all consistent"
#: answer, and a truncated scan says so in its reasoning.
LINK_EDGE_HOST_SCAN_LIMIT = 50_000


# ---------------------------------------------------------------------------
# Evidence


@dataclass
class SitemapDocFacts:
    """One ``web.sitemap`` row — a declared sitemap document as last fetched."""

    url: str
    kind: str
    status_code: int | None
    fetch_error: str | None
    url_count: int | None
    is_active: bool
    last_fetched_at: datetime | None

    @property
    def unreachable(self) -> bool:
        """Fetched and refused, or fetched and unparseable."""
        if self.fetch_error:
            return True
        return self.status_code is not None and self.status_code >= 400


@dataclass
class SiteEvidence:
    """Everything the four site checks read. Built once per sweep, no network."""

    site_id: str
    root_url: str
    canonical_host_form: str
    probe: SiteProbe | None = None
    robots: RobotsDocument | None = None

    # --- sitemap graph (web.sitemap + web.page_sitemap)
    #: True once sitemap sync has produced at least one document row. Zero rows
    #: is ambiguous on its own — "this site has no sitemap" and "we never
    #: looked" are different answers and are never conflated.
    sitemap_sync_ran: bool = False
    sitemaps: list[SitemapDocFacts] = field(default_factory=list)
    sitemap_entries_total: int = 0
    entries_missing_lastmod: int = 0
    #: Canonical page ids reachable from a sitemap membership.
    sitemap_page_ids: set[str] = field(default_factory=set)
    #: Sitemap URLs the crawler has never successfully captured.
    undiscovered_urls: list[str] = field(default_factory=list)
    undiscovered_count: int = 0
    #: Junk class -> the sitemap URLs in it (all of them; sampled at emit time).
    junk_by_class: dict[str, list[str]] = field(default_factory=dict)
    junk_entry_count: int = 0

    # --- coverage (crawled indexable pages vs the sitemap set)
    indexable_total: int = 0
    indexable_in_sitemap: int = 0
    indexable_missing_from_sitemap: list[str] = field(default_factory=list)

    # --- host forms observed on internal links
    internal_link_host_forms: set[str] = field(default_factory=set)
    host_form_scan_truncated: bool = False

    #: The page census this evidence was derived from was cut short, so any
    #: whole-site ratio computed from it would understate coverage.
    pages_truncated: bool = False

    @property
    def junk_pct(self) -> float:
        if self.sitemap_entries_total <= 0:
            return 0.0
        return 100.0 * self.junk_entry_count / self.sitemap_entries_total

    @property
    def undiscovered_pct(self) -> float:
        if self.sitemap_entries_total <= 0:
            return 0.0
        return 100.0 * self.undiscovered_count / self.sitemap_entries_total


def _status_for(score: int) -> str:
    """Deterministic-rule score → the DB's status vocabulary."""

    if score >= SITE_PASS_MIN_SCORE:
        return "pass"
    if score >= SITE_WARN_MIN_SCORE:
        return "warn"
    return "fail"


def _verdict(
    score: int,
    reasoning: str,
    *,
    issue_count: int = 0,
    evidence: dict | None = None,
) -> CheckOutcome:
    score = clamp_score(score)
    return CheckOutcome(
        _status_for(score), score, reasoning, issue_count=issue_count, evidence=evidence
    )


def _missing(reasoning: str, remediation: Remediation | None = None) -> CheckOutcome:
    return CheckOutcome("n_a", None, reasoning, remediation=remediation)


# ---------------------------------------------------------------------------
# The checks


def _check_robots_txt_health(site: SiteEvidence) -> CheckOutcome:
    """`robots_txt_health` — weight 3.0, the joint-heaviest item we score."""

    capture = site.probe.robots if site.probe is not None else None
    if capture is None:
        return _missing(
            "We haven't read this site's robots.txt file yet — it's the one file "
            "that can hide the whole site from Google, so we won't guess at it.",
            RECRAWL_SITE,
        )
    if not capture.answered:
        return _missing(
            f"We tried to read {capture.url} and the site never answered "
            f"({capture.fetch_error}). Until it does, we can't say whether search "
            "engines are being let in.",
            RECRAWL_SITE,
        )

    status = capture.http_status
    if status is not None and status >= 500:
        return _verdict(
            ROBOTS_SERVER_ERROR_SCORE,
            f"robots.txt returns a {status} server error. Search engines treat a "
            "failing robots.txt as an instruction to crawl NOTHING — while this "
            "lasts, the entire site is effectively blocked.",
            issue_count=1,
            evidence={"robots_url": capture.url, "http_status": status},
        )

    document = capture.parsed()
    if document is None:
        # 3xx that never resolved, 4xx, or a body we could not read: the file is
        # not being served. Permitted, but nobody is managing it.
        return _verdict(
            ROBOTS_MISSING_SCORE,
            f"This site has no robots.txt (it answers {status}). That's allowed — "
            "search engines will crawl everything — but you have no way to steer "
            "them, and no place to point them at your sitemap.",
            issue_count=1,
            evidence={"robots_url": capture.url, "http_status": status},
        )

    blanket = document.blanket_disallow_agents()
    if blanket:
        return _verdict(
            ROBOTS_BLANKET_DISALLOW_SCORE,
            "robots.txt tells "
            + ", ".join(blanket)
            + " to stay off the ENTIRE site (`Disallow: /`). This is the single "
            "most damaging line a website can publish — nothing here can be "
            "found in search while it stands.",
            issue_count=len(blanket),
            evidence={"blocked_agents": blanket, "robots_url": capture.url},
        )

    blocked = _robots_blocked_urls(site, document)
    if blocked:
        return _verdict(
            ROBOTS_BLOCKS_WANTED_URLS_SCORE,
            f"robots.txt blocks {len(blocked)} URL(s) that this site is otherwise "
            "asking to have indexed — they are listed in the sitemap or marked "
            "indexable. Pages cannot be both advertised and forbidden.",
            issue_count=len(blocked),
            evidence={"blocked_urls": sample_urls(blocked), "robots_url": capture.url},
        )

    if document.syntax_errors:
        return _verdict(
            ROBOTS_SYNTAX_ERROR_SCORE,
            f"robots.txt has {len(document.syntax_errors)} line(s) crawlers cannot "
            "read. Search engines skip what they don't understand, so the rules on "
            "those lines are simply not in force — " + document.syntax_errors[0],
            issue_count=len(document.syntax_errors),
            evidence={
                "syntax_errors": document.syntax_errors[:5],
                "robots_url": capture.url,
            },
        )

    return _verdict(
        ROBOTS_CLEAN_SCORE,
        "robots.txt is valid, addresses "
        f"{len(document.user_agents)} crawler group(s), and blocks nothing this "
        "site wants indexed.",
        evidence={"sitemaps_declared": document.sitemaps[:5], "robots_url": capture.url},
    )


def _robots_blocked_urls(site: SiteEvidence, document: RobotsDocument) -> list[str]:
    """URLs the site advertises that its own robots.txt forbids."""

    wanted: list[str] = []
    seen: set[str] = set()
    for url in site.undiscovered_urls + site.indexable_missing_from_sitemap:
        if url not in seen:
            seen.add(url)
            wanted.append(url)
    # The sitemap-membership URLs the crawler DID capture are the other half of
    # "advertised": they are in the sitemap and they are indexable.
    for url in site.junk_by_class.get("robots_blocked", []):
        if url not in seen:
            seen.add(url)
            wanted.append(url)
    blocked = [u for u in wanted[:ROBOTS_BLOCK_SCAN_LIMIT] if not document.is_allowed(u)]
    return blocked


def _check_sitemap_health(site: SiteEvidence) -> CheckOutcome:
    """`sitemap_health` — weight 2.0. Dirtiest problem class present wins."""

    if not site.sitemap_sync_ran:
        if site.probe is None:
            return _missing(
                "We haven't looked for this site's sitemap yet.",
                SYNC_SITEMAPS,
            )
        if site.probe.reachable_sitemap_locations:
            return _missing(
                "This site publishes a sitemap, but we haven't read it yet, so we "
                "can't tell you what's in it.",
                SYNC_SITEMAPS,
            )
        return _verdict(
            SITEMAP_NONE_FOUND_SCORE,
            "This site has no XML sitemap. We checked robots.txt and the usual "
            "addresses and found nothing. A sitemap is how you hand search "
            "engines the full list of pages you want found instead of hoping "
            "they discover them by following links.",
            issue_count=1,
            evidence={
                "checked": [p.url for p in site.probe.sitemap_locations][:5],
            },
        )

    unreachable = [s for s in site.sitemaps if s.unreachable]
    if unreachable:
        first = unreachable[0]
        detail = first.fetch_error or f"HTTP {first.status_code}"
        return _verdict(
            SITEMAP_UNREACHABLE_SCORE,
            f"{len(unreachable)} of this site's {len(site.sitemaps)} sitemap file(s) "
            f"cannot be read ({detail}). A sitemap search engines can't fetch is "
            "the same as no sitemap at all, except you believe you have one.",
            issue_count=len(unreachable),
            evidence={"unreachable": sample_urls([s.url for s in unreachable])},
        )

    if site.sitemap_entries_total == 0:
        return _verdict(
            SITEMAP_NONE_FOUND_SCORE,
            f"This site's {len(site.sitemaps)} sitemap file(s) are reachable but "
            "list no URLs at all — nothing is being advertised to search engines.",
            issue_count=1,
            evidence={"sitemaps": sample_urls([s.url for s in site.sitemaps])},
        )

    junk_pct = site.junk_pct
    if site.junk_entry_count > 0:
        summary = ", ".join(
            f"{len(urls)} {label.replace('_', ' ')}"
            for label, urls in sorted(site.junk_by_class.items())
            if urls
        )
        heavy = junk_pct > SITEMAP_HEAVY_JUNK_PCT
        score = SITEMAP_HEAVY_JUNK_SCORE if heavy else SITEMAP_LIGHT_JUNK_SCORE
        return _verdict(
            score,
            f"{site.junk_entry_count} of {site.sitemap_entries_total} sitemap URLs "
            f"({junk_pct:.1f}%) should not be there — {summary}. A sitemap is a "
            "list of pages you are asking to have indexed; every entry that "
            "redirects, errors, or says noindex spends crawl budget contradicting "
            "you.",
            issue_count=site.junk_entry_count,
            evidence={
                label: sample_urls(urls)
                for label, urls in sorted(site.junk_by_class.items())
                if urls
            },
        )

    oversized = [s for s in site.sitemaps if (s.url_count or 0) > SITEMAP_MAX_URLS_PER_DOC]
    if oversized or site.entries_missing_lastmod:
        details: list[str] = []
        if oversized:
            details.append(
                f"{len(oversized)} file(s) list more than "
                f"{SITEMAP_MAX_URLS_PER_DOC:,} URLs and should be split"
            )
        if site.entries_missing_lastmod:
            details.append(
                f"{site.entries_missing_lastmod} entries carry no last-modified date, "
                "so crawlers can't tell what changed"
            )
        return _verdict(
            SITEMAP_MINOR_ISSUE_SCORE,
            "The sitemap is clean, with housekeeping worth doing: " + "; ".join(details) + ".",
            issue_count=len(oversized) + site.entries_missing_lastmod,
            evidence={"oversized": sample_urls([s.url for s in oversized])},
        )

    return _verdict(
        SITEMAP_CLEAN_SCORE,
        f"All {site.sitemap_entries_total} URLs across {len(site.sitemaps)} sitemap "
        "file(s) are reachable, indexable, and dated — nothing in here contradicts "
        "what the site is asking to have indexed.",
    )


def _check_sitemap_coverage(site: SiteEvidence) -> CheckOutcome:
    """`sitemap_coverage` — weight 1.5. The catalogue row's formula, verbatim."""

    if not site.sitemap_sync_ran:
        if site.probe is not None and not site.probe.reachable_sitemap_locations:
            return _verdict(
                clamp_score(0),
                "This site has no sitemap, so none of its pages are being "
                "advertised to search engines — every page has to be discovered "
                "by following a link.",
                issue_count=site.indexable_total,
            )
        return _missing(
            "We haven't read this site's sitemap yet, so we can't compare it with "
            "the pages we found.",
            SYNC_SITEMAPS,
        )
    if site.pages_truncated:
        return _missing(
            "This site is larger than one analysis pass covers, so any coverage "
            "figure would understate it.",
            RECRAWL_SITE,
        )
    if site.indexable_total == 0:
        return _missing(
            "We haven't captured any indexable pages for this site yet, so there "
            "is nothing to compare the sitemap against.",
            RECRAWL_SITE,
        )

    ratio = round(100 * site.indexable_in_sitemap / site.indexable_total)
    penalty = min(
        COVERAGE_ORPHAN_PENALTY_MAX,
        round(COVERAGE_ORPHAN_PENALTY_FACTOR * site.undiscovered_pct),
    )
    score = clamp_score(ratio - penalty)
    missing = site.indexable_total - site.indexable_in_sitemap

    if score >= COVERAGE_HEALTHY_MIN_SCORE:
        status = "pass"
    elif score >= COVERAGE_GAPS_MIN_SCORE:
        status = "warn"
    else:
        status = "fail"

    parts = [
        f"{site.indexable_in_sitemap} of {site.indexable_total} indexable pages "
        f"({ratio}%) are listed in the sitemap"
    ]
    if missing:
        parts.append(f"{missing} real page(s) are missing from it")
    if site.undiscovered_count:
        parts.append(
            f"{site.undiscovered_count} sitemap URL(s) "
            f"({site.undiscovered_pct:.1f}%) were never reached by the crawl — "
            "either they don't exist or nothing on the site links to them"
        )
    if status == "pass" and not missing and not site.undiscovered_count:
        reasoning = (
            f"Every one of the {site.indexable_total} indexable pages we found is "
            "in the sitemap, and every sitemap URL is a page we reached."
        )
    else:
        reasoning = "; ".join(parts) + "."

    return CheckOutcome(
        status,
        score,
        reasoning,
        issue_count=missing + site.undiscovered_count,
        evidence={
            "missing_from_sitemap": sample_urls(site.indexable_missing_from_sitemap),
            "never_reached": sample_urls(site.undiscovered_urls),
        },
    )


def _check_host_protocol_consistency(site: SiteEvidence) -> CheckOutcome:
    """`host_protocol_consistency` — weight 1.5, category ``url_architecture``."""

    if site.probe is None or not site.probe.variants:
        return _missing(
            "We haven't checked whether this site also answers on its other "
            "addresses (www / non-www, http / https).",
            RECRAWL_SITE,
        )

    canonical = site.canonical_host_form
    others = [p for p in site.probe.variants if host_form(p.url) != canonical]
    answered = [p for p in site.probe.variants if p.answered]
    if not answered:
        return _missing(
            "None of this site's addresses answered when we checked them, so we "
            "can't tell which one is the real home.",
            RECRAWL_SITE,
        )

    # Rule 1 — a variant that serves 200 in its own right (never redirecting to
    # the canonical form) is a second live copy of the whole site.
    live_duplicates = [
        p
        for p in others
        if p.final_status == 200 and p.final_url is not None and host_form(p.final_url) != canonical
    ]
    if live_duplicates:
        urls = [p.url for p in live_duplicates]
        return _verdict(
            HOST_MULTIPLE_LIVE_SCORE,
            f"This site answers on {len(live_duplicates) + 1} different addresses "
            f"({canonical} plus {', '.join(urls)}) and none of the others hands "
            "visitors over to the main one. Google sees several copies of the same "
            "website and has to guess which to rank — every link you earn is split "
            "between them.",
            issue_count=len(live_duplicates),
            evidence={"live_variants": sample_urls(urls), "canonical": canonical},
        )

    # Rule 2 — they do redirect, but not permanently or not in one hop.
    soft = [
        p
        for p in others
        if p.redirects
        and (p.http_status not in HOST_PERMANENT_REDIRECT_STATUSES or len(p.redirect_chain) > 1)
    ]
    if soft:
        detail = ", ".join(
            f"{p.url} → {p.http_status}"
            + (f" ({len(p.redirect_chain)} hops)" if len(p.redirect_chain) > 1 else "")
            for p in soft
        )
        return _verdict(
            HOST_SOFT_REDIRECT_SCORE,
            f"The site's other addresses do point at {canonical}, but not cleanly: "
            f"{detail}. A temporary redirect tells search engines the old address "
            "is still real, and every extra hop loses a little of the value the "
            "link was carrying.",
            issue_count=len(soft),
            evidence={"variants": [{"url": p.url, "status": p.http_status} for p in soft]},
        )

    # Rule 3 — the third duplicate family the row names: the same path served
    # at both `/a` and `/a/`. Measured on the probe's sampled paths only; a pair
    # where one form redirects to the other is consolidation working and never
    # lands here (`SlashPairProbe.duplicated`).
    slash_duplicates = [p for p in site.probe.slash_pairs if p.duplicated]
    if slash_duplicates:
        paths = [p.path for p in slash_duplicates]
        checked = len([p for p in site.probe.slash_pairs if p.both_answered])
        return _verdict(
            HOST_SLASH_DUPLICATE_SCORE,
            f"{len(slash_duplicates)} of the {checked} page addresses we checked "
            "answer at BOTH forms of their address — with and without the final "
            f"slash ({', '.join(paths[:3])}). Each one is the same page living at "
            "two URLs, so links and rankings split between them.",
            issue_count=len(slash_duplicates),
            evidence={
                "slash_duplicate_paths": sample_urls(paths),
                "paths_checked": checked,
            },
        )

    # Rule 4 — consolidation is correct, but the site's own links disagree.
    if len(site.internal_link_host_forms) > 1:
        forms = sorted(site.internal_link_host_forms)
        return _verdict(
            HOST_MIXED_INTERNAL_LINKS_SCORE,
            "The site's addresses redirect correctly, but its own internal links "
            f"mix {len(forms)} forms ({', '.join(forms)}). Every one of those links "
            "sends a visitor and a crawler through an extra redirect that did not "
            "need to happen.",
            issue_count=len(forms),
            evidence={"host_forms": forms, "canonical": canonical},
        )

    note = ""
    if site.host_form_scan_truncated:
        note = f" (internal links checked up to the first {LINK_EDGE_HOST_SCAN_LIMIT:,})"
    slash_checked = len([p for p in site.probe.slash_pairs if p.both_answered])
    slash_note = (
        f" We also checked {slash_checked} page address(es) with and without a "
        "final slash, and each one resolves to a single URL."
        if slash_checked
        else ""
    )
    return _verdict(
        HOST_CONSISTENT_SCORE,
        f"The site lives at one address, {canonical}, and every other form "
        f"permanently redirects to it{note}.{slash_note}",
        evidence={"canonical": canonical, "slash_pairs_checked": slash_checked},
    )


#: Catalogue item key -> the check that answers it. Merged into
#: ``analysis.SITE_CHECKS`` — the ONE site-subject registry — by an adapter that
#: hands each of these the ``SiteEvidence`` hanging off ``SiteFacts``.
CRAWLABILITY_SITE_CHECKS: dict[str, Callable[[SiteEvidence], CheckOutcome]] = {
    "robots_txt_health": _check_robots_txt_health,
    "sitemap_health": _check_sitemap_health,
    "sitemap_coverage": _check_sitemap_coverage,
    "host_protocol_consistency": _check_host_protocol_consistency,
}


# ---------------------------------------------------------------------------
# Evidence loading — batched, and never a whole table in one query.


def _is_indexable(facts: object) -> bool:
    """A page this site is asking to have indexed.

    Deliberately narrow: a 2xx page that does not say noindex. A page with no
    captured status is not counted either way — it is evidence we don't have.
    """

    status = getattr(facts, "http_status", None)
    if status is None or not (200 <= int(status) < 300):
        return False
    return getattr(facts, "noindex", None) is not True


async def load_site_evidence(
    *,
    site: WebSite,
    facts_list: list,
    pages_truncated: bool,
) -> SiteEvidence:
    """Build the site-subject evidence from stored rows plus the site probe.

    ``facts_list`` is the sweep's already-loaded page census (canonical HTML
    pages with a snapshot, plus the transport-only ones) — reused rather than
    re-queried, so the whole site-level pass costs the sitemap tables and one
    bounded link-edge scan.
    """

    site_id = str(site.id)
    root_url = str(site.root_url)
    evidence = SiteEvidence(
        site_id=site_id,
        root_url=root_url,
        canonical_host_form=host_form(root_url),
        probe=load_site_probe(site),
        pages_truncated=pages_truncated,
    )
    if evidence.probe is not None and evidence.probe.robots is not None:
        evidence.robots = evidence.probe.robots.parsed()

    facts_by_page = {f.page_id: f for f in facts_list if getattr(f, "page_id", "")}
    await _load_sitemap_evidence(evidence, facts_by_page)
    _load_coverage(evidence, facts_by_page)
    await _load_internal_link_host_forms(evidence)
    return evidence


async def _load_sitemap_evidence(evidence: SiteEvidence, facts_by_page: dict) -> None:
    documents = await WebSitemap.filter(site_id=evidence.site_id, deleted_at__isnull=True).all()
    evidence.sitemap_sync_ran = bool(documents)
    evidence.sitemaps = [
        SitemapDocFacts(
            url=str(doc.url),
            kind=str(doc.kind),
            status_code=int(doc.status_code) if doc.status_code is not None else None,
            fetch_error=doc.fetch_error,
            url_count=int(doc.url_count) if doc.url_count is not None else None,
            is_active=bool(doc.is_active),
            last_fetched_at=doc.last_fetched_at,
        )
        for doc in documents
    ]
    if not documents:
        return

    # Memberships, keyset-paged. One row per (page, sitemap); a page listed in
    # two sitemaps is ONE advertised URL, so pages are deduped before counting.
    member_page_ids: set[str] = set()
    pages_with_lastmod: set[str] = set()
    last_id: str | None = None
    while True:
        filters: dict[str, object] = {
            "site_id": evidence.site_id,
            "deleted_at__isnull": True,
        }
        if last_id is not None:
            filters["id__gt"] = last_id
        rows = (
            await WebPageSitemap.filter(**filters)
            .order_by("id")
            .limit(_SITEMAP_MEMBERSHIP_BATCH)
            .all()
        )
        if not rows:
            break
        last_id = str(rows[-1].id)
        for row in rows:
            page_id = str(row.page_id)
            member_page_ids.add(page_id)
            if row.lastmod is not None:
                pages_with_lastmod.add(page_id)
        if len(rows) < _SITEMAP_MEMBERSHIP_BATCH:
            break

    evidence.sitemap_entries_total = len(member_page_ids)
    evidence.entries_missing_lastmod = len(member_page_ids - pages_with_lastmod)
    if not member_page_ids:
        return

    # The page rows behind those memberships. Only these are loaded — a sitemap
    # URL that is an alias must credit the page it resolves to, and only the
    # page row knows that.
    ordered = sorted(member_page_ids)
    junk: dict[str, list[str]] = {
        "not_found_or_error": [],
        "redirecting": [],
        "noindexed": [],
        "non_canonical": [],
        "robots_blocked": [],
    }
    for start in range(0, len(ordered), _PAGE_LOOKUP_BATCH):
        chunk = ordered[start : start + _PAGE_LOOKUP_BATCH]
        pages = await WebPage.filter(id__in=chunk, deleted_at__isnull=True).all()
        for page in pages:
            page_id = str(page.id)
            url = str(page.url)
            canonical_id = str(page.canonical_page_id or page.id)
            evidence.sitemap_page_ids.add(canonical_id)
            facts = facts_by_page.get(canonical_id) or facts_by_page.get(page_id)
            status = page.http_status_last
            if status is None and facts is not None:
                status = facts.http_status
            verification = (page.metadata or {}).get(VERIFICATION_METADATA_KEY) or {}
            # "Undiscovered" means we have NO answer about this URL — not "we
            # have no snapshot". The verification sweep answers status without
            # capturing a body, and keying this on `latest_snapshot_id` alone
            # sent every verified URL back into "we haven't looked", discarding
            # the exact evidence this check exists to score.
            if (
                status is None
                and page.latest_snapshot_id is None
                and canonical_id not in facts_by_page
            ):
                evidence.undiscovered_count += 1
                evidence.undiscovered_urls.append(url)
                continue
            if status is not None and int(status) >= 400:
                junk["not_found_or_error"].append(url)
            elif status is not None and 300 <= int(status) < 400:
                junk["redirecting"].append(url)
            elif verification.get("redirect_material") is True:
                # The sweep follows redirects and records the FINAL status (the
                # crawler's meaning for this column), so a redirecting sitemap
                # entry reads as 200 here; the hop lives in the evidence.
                # `redirect_material`, NOT `redirected` — our stored identity
                # strips the trailing slash, so on a slash-serving site every
                # URL "redirects" to itself and reporting that would tell the
                # customer their entire sitemap is broken when nothing is.
                junk["redirecting"].append(url)
            elif canonical_id != page_id:
                junk["non_canonical"].append(url)
            elif facts is not None and getattr(facts, "noindex", None) is True:
                junk["noindexed"].append(url)
            elif evidence.robots is not None and not evidence.robots.is_allowed(url):
                junk["robots_blocked"].append(url)

    evidence.junk_by_class = {label: urls for label, urls in junk.items() if urls}
    evidence.junk_entry_count = sum(len(urls) for urls in evidence.junk_by_class.values())


def _load_coverage(evidence: SiteEvidence, facts_by_page: dict) -> None:
    for page_id, facts in facts_by_page.items():
        if not _is_indexable(facts):
            continue
        evidence.indexable_total += 1
        if page_id in evidence.sitemap_page_ids:
            evidence.indexable_in_sitemap += 1
        else:
            evidence.indexable_missing_from_sitemap.append(str(facts.url))


async def _load_internal_link_host_forms(evidence: SiteEvidence) -> None:
    """Distinct ``scheme://host`` forms the site links to internally.

    Stops the moment a SECOND form appears — that is the whole question — so
    the ceiling below only ever bounds a clean answer, which then says so.
    """

    scanned = 0
    last_id: str | None = None
    while scanned < LINK_EDGE_HOST_SCAN_LIMIT:
        filters: dict[str, object] = {
            "site_id": evidence.site_id,
            "is_internal": True,
            "deleted_at__isnull": True,
        }
        if last_id is not None:
            filters["id__gt"] = last_id
        rows = await WebLinkEdge.filter(**filters).order_by("id").limit(_LINK_EDGE_HOST_BATCH).all()
        if not rows:
            return
        last_id = str(rows[-1].id)
        scanned += len(rows)
        for row in rows:
            target = str(row.target_url)
            if "://" not in target:
                continue
            evidence.internal_link_host_forms.add(host_form(target))
        if len(evidence.internal_link_host_forms) > 1:
            return
        if len(rows) < _LINK_EDGE_HOST_BATCH:
            return
    evidence.host_form_scan_truncated = True


__all__ = [
    "COVERAGE_GAPS_MIN_SCORE",
    "COVERAGE_HEALTHY_MIN_SCORE",
    "COVERAGE_ORPHAN_PENALTY_FACTOR",
    "COVERAGE_ORPHAN_PENALTY_MAX",
    "HOST_CONSISTENT_SCORE",
    "HOST_MIXED_INTERNAL_LINKS_SCORE",
    "HOST_MULTIPLE_LIVE_SCORE",
    "HOST_PERMANENT_REDIRECT_STATUSES",
    "HOST_SOFT_REDIRECT_SCORE",
    "LINK_EDGE_HOST_SCAN_LIMIT",
    "ROBOTS_BLANKET_DISALLOW_SCORE",
    "ROBOTS_BLOCKS_WANTED_URLS_SCORE",
    "ROBOTS_BLOCK_SCAN_LIMIT",
    "ROBOTS_CLEAN_SCORE",
    "ROBOTS_MISSING_SCORE",
    "ROBOTS_SERVER_ERROR_SCORE",
    "ROBOTS_SYNTAX_ERROR_SCORE",
    "SITEMAP_CLEAN_SCORE",
    "SITEMAP_HEAVY_JUNK_PCT",
    "SITEMAP_HEAVY_JUNK_SCORE",
    "SITEMAP_LIGHT_JUNK_SCORE",
    "SITEMAP_MAX_URLS_PER_DOC",
    "SITEMAP_MINOR_ISSUE_SCORE",
    "SITEMAP_NONE_FOUND_SCORE",
    "SITEMAP_UNREACHABLE_SCORE",
    "CRAWLABILITY_SITE_CHECKS",
    "SITE_PASS_MIN_SCORE",
    "SITE_WARN_MIN_SCORE",
    "SiteEvidence",
    "SitemapDocFacts",
    "load_site_evidence",
]
