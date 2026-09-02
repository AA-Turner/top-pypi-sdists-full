"""Deterministic page-analysis checks — pure-logic tests (no DB).

Locks the analysis contract: every outcome's status/score pairing satisfies
the ``analysis_result_status_score_valid`` DB constraint (pass/warn/fail →
score 1–100; n_a → None), missing evidence is ``n_a`` (never a silent pass),
and cross-page checks read the site aggregates.

The per-page checks are imported from ``seo_audit`` — their ONE home. That
they are exercised here through ``PageFacts`` is the point: the sweep runs the
same functions a live audit does. See ``test_seo_checks_single_source.py``.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from matrx_scraper.seo_audit import (
    CheckOutcome,
    check_canonical_conflicts,
    check_h1_presence,
    check_image_alt_presence,
    check_meta_robots_conflicts,
    check_thin_content,
    check_title_length,
    check_title_presence,
)
from matrx_scraper.web_crawl import analysis as analysis_module
from matrx_scraper.web_crawl.analysis import (
    PAGE_CHECKS,
    OrphanCensus,
    PageFacts,
    PageLinkStats,
    SiteAggregates,
    _check_anchor_text_descriptiveness,
    _check_broken_external_links,
    _check_broken_internal_links,
    _check_crawl_depth,
    _check_duplicate_content_exact,
    _check_excessive_outlinks,
    _check_internal_inlink_coverage,
    _check_internal_redirect_links,
    _check_nofollow_internal_links,
    _check_orphan_pages,
    _check_title_duplication,
    _is_descriptive_anchor,
    _norm_text,
)


def _check_title_presence(facts, _site):
    return check_title_presence(facts)


def _check_title_length(facts, _site):
    return check_title_length(facts)


def _check_h1_presence(facts, _site):
    return check_h1_presence(facts)


def _check_thin_content(facts, _site):
    return check_thin_content(facts)


def _check_image_alt_presence(facts, _site):
    return check_image_alt_presence(facts)


def _check_meta_robots_conflicts(facts, _site):
    return check_meta_robots_conflicts(facts)


def _check_canonical_conflicts(facts, _site):
    return check_canonical_conflicts(facts)


def make_facts(**overrides) -> PageFacts:
    base = dict(
        page_id="p1",
        url="https://example.com/a",
        title="A perfectly reasonable page title here",
        title_metrics={"ok": True, "character_count": 39, "pixel_width": 300},
        description="A description that is long enough to look like real prose for testing.",
        description_metrics={"ok": True, "character_count": 71, "pixel_width": 500},
        meta_robots="index, follow",
        canonical_url="https://example.com/a",
        canonical_matches=True,
        noindex=False,
        nofollow=False,
        h1_count=1,
        word_count=800,
        image_count=4,
        images_missing_alt=0,
        fingerprint_version=1,
        exact_sha256="abc",
        http_status=200,
        latest_snapshot_id="s1",
    )
    base.update(overrides)
    return PageFacts(**base)


def assert_db_valid(outcome: CheckOutcome) -> None:
    """Mirror of analysis_result_status_score_valid + status_valid."""
    assert outcome.status in ("pass", "warn", "fail", "n_a", "error")
    if outcome.status in ("pass", "warn", "fail"):
        assert outcome.score is not None and 1 <= outcome.score <= 100
    else:
        assert outcome.score is None
    assert outcome.reasoning  # reasoning is the point — never empty


def test_every_check_is_db_valid_on_a_healthy_page():
    site = SiteAggregates()
    facts = make_facts()
    site.pages_by_title[_norm_text(facts.title)] = [facts]
    site.pages_by_sha[(1, "abc")] = [facts]
    site.link_stats["p1"] = PageLinkStats(checked=10)
    for key, check in PAGE_CHECKS.items():
        outcome = check(facts, site)
        assert_db_valid(outcome)
        assert outcome.status in ("pass", "n_a"), f"{key} flagged a healthy page"


def test_title_presence():
    assert _check_title_presence(make_facts(), SiteAggregates()).status == "pass"
    missing = _check_title_presence(make_facts(title=None), SiteAggregates())
    assert missing.status == "fail" and missing.score == 5


def test_title_length_missing_metrics_is_na_not_pass():
    outcome = _check_title_length(make_facts(title_metrics={}), SiteAggregates())
    assert outcome.status == "n_a" and outcome.score is None


def test_title_duplication_counts_partners():
    a = make_facts(page_id="p1", url="https://example.com/a")
    b = make_facts(page_id="p2", url="https://example.com/b")
    site = SiteAggregates()
    site.pages_by_title[_norm_text(a.title)] = [a, b]
    outcome = _check_title_duplication(a, site)
    assert outcome.status == "warn" and outcome.issue_count == 1
    assert "https://example.com/b" in outcome.evidence["duplicate_pages"]
    # Many partners escalate to fail.
    partners = [make_facts(page_id=f"p{i}", url=f"https://example.com/{i}") for i in range(2, 8)]
    site.pages_by_title[_norm_text(a.title)] = [a, *partners]
    outcome = _check_title_duplication(a, site)
    assert outcome.status == "fail"
    assert_db_valid(outcome)


def test_h1_presence_variants():
    assert _check_h1_presence(make_facts(h1_count=1), SiteAggregates()).status == "pass"
    assert _check_h1_presence(make_facts(h1_count=0), SiteAggregates()).status == "fail"
    multiple = _check_h1_presence(make_facts(h1_count=3), SiteAggregates())
    assert multiple.status == "warn" and multiple.issue_count == 2
    assert _check_h1_presence(make_facts(h1_count=None), SiteAggregates()).status == "n_a"


def test_thin_content_bands():
    assert _check_thin_content(make_facts(word_count=500), SiteAggregates()).status == "pass"
    assert _check_thin_content(make_facts(word_count=250), SiteAggregates()).status == "warn"
    assert _check_thin_content(make_facts(word_count=150), SiteAggregates()).status == "warn"
    fail = _check_thin_content(make_facts(word_count=30), SiteAggregates())
    assert fail.status == "fail"
    assert_db_valid(fail)


def test_image_alt_presence():
    assert (
        _check_image_alt_presence(
            make_facts(image_count=0, images_missing_alt=0), SiteAggregates()
        ).status
        == "n_a"
    )
    warn = _check_image_alt_presence(
        make_facts(image_count=10, images_missing_alt=2), SiteAggregates()
    )
    assert warn.status == "warn" and warn.issue_count == 2
    fail = _check_image_alt_presence(
        make_facts(image_count=10, images_missing_alt=8), SiteAggregates()
    )
    assert fail.status == "fail"
    assert_db_valid(fail)
    legacy = _check_image_alt_presence(
        make_facts(image_count=None, images_missing_alt=None), SiteAggregates()
    )
    assert legacy.status == "n_a"


def test_meta_robots_conflicts():
    assert _check_meta_robots_conflicts(make_facts(), SiteAggregates()).status == "pass"
    noindex = _check_meta_robots_conflicts(
        make_facts(noindex=True, meta_robots="noindex"), SiteAggregates()
    )
    assert noindex.status == "fail" and noindex.score == 10
    conflict = _check_meta_robots_conflicts(
        make_facts(meta_robots="index, noindex"), SiteAggregates()
    )
    assert conflict.status == "fail"
    nofollow = _check_meta_robots_conflicts(
        make_facts(nofollow=True, meta_robots="index, nofollow"), SiteAggregates()
    )
    assert nofollow.status == "warn"


def test_canonical_conflicts():
    assert _check_canonical_conflicts(make_facts(), SiteAggregates()).status == "pass"
    other = _check_canonical_conflicts(
        make_facts(canonical_url="https://example.com/b", canonical_matches=False),
        SiteAggregates(),
    )
    assert other.status == "warn"
    cross = _check_canonical_conflicts(
        make_facts(canonical_url="https://other-site.com/a", canonical_matches=False),
        SiteAggregates(),
    )
    assert cross.status == "fail"
    noindexed = _check_canonical_conflicts(
        make_facts(canonical_url="https://example.com/b", canonical_matches=False, noindex=True),
        SiteAggregates(),
    )
    assert noindexed.status == "fail"
    # www variants are the same registrable host — never cross-host.
    www = _check_canonical_conflicts(
        make_facts(canonical_url="https://www.example.com/a", canonical_matches=False),
        SiteAggregates(),
    )
    assert www.status == "warn"


def test_link_checks_require_verified_statuses():
    site = SiteAggregates()
    assert _check_broken_internal_links(make_facts(), site).status == "n_a"
    site.link_stats["p1"] = PageLinkStats(
        checked=5, broken=["https://example.com/dead"], redirecting=["https://example.com/old"]
    )
    broken = _check_broken_internal_links(make_facts(), site)
    assert broken.status == "fail" and broken.issue_count == 1
    assert_db_valid(broken)
    redirecting = _check_internal_redirect_links(make_facts(), site)
    assert redirecting.status == "warn" and redirecting.issue_count == 1
    clean = PageLinkStats(checked=5)
    site.link_stats["p1"] = clean
    assert _check_broken_internal_links(make_facts(), site).status == "pass"
    assert _check_internal_redirect_links(make_facts(), site).status == "pass"


def test_broken_external_links_are_counted_separately_from_internal():
    """External link rot is its own verdict — the internal check must not see it.

    Before the 2026-08-09 consolidation the sweep loaded ONLY internal edges,
    so a page full of dead outbound links scored a clean 100.
    """
    site = SiteAggregates()
    assert _check_broken_external_links(make_facts(), site).status == "n_a"

    # Internal all healthy, external rotten: exactly one check fires.
    site.link_stats["p1"] = PageLinkStats(
        checked=5,
        external_checked=4,
        external_broken=["https://gone.example.org/a", "https://gone.example.org/b"],
    )
    external = _check_broken_external_links(make_facts(), site)
    assert external.status == "warn" and external.issue_count == 2
    assert_db_valid(external)
    assert _check_broken_internal_links(make_facts(), site).status == "pass"

    # Verified but clean.
    site.link_stats["p1"] = PageLinkStats(checked=5, external_checked=4)
    assert _check_broken_external_links(make_facts(), site).status == "pass"


def test_broken_external_links_score_floor_holds():
    site = SiteAggregates()
    site.link_stats["p1"] = PageLinkStats(
        external_checked=100, external_broken=[f"https://gone.example.org/{i}" for i in range(60)]
    )
    assert_db_valid(_check_broken_external_links(make_facts(), site))


def test_duplicate_content_exact_same_version_only():
    a = make_facts(page_id="p1")
    b = make_facts(page_id="p2", url="https://example.com/b")
    site = SiteAggregates()
    site.pages_by_sha[(1, "abc")] = [a, b]
    dup = _check_duplicate_content_exact(a, site)
    assert dup.status == "fail" and dup.issue_count == 1
    assert_db_valid(dup)
    no_fp = _check_duplicate_content_exact(
        make_facts(exact_sha256=None, fingerprint_version=None), site
    )
    assert no_fp.status == "n_a"


def test_many_duplicates_never_break_the_score_floor():
    a = make_facts(page_id="p1")
    partners = [make_facts(page_id=f"p{i}", url=f"https://example.com/{i}") for i in range(2, 60)]
    site = SiteAggregates()
    site.pages_by_sha[(1, "abc")] = [a, *partners]
    site.pages_by_title[_norm_text(a.title)] = [a, *partners]
    site.link_stats["p1"] = PageLinkStats(
        checked=100, broken=[f"u{i}" for i in range(50)], redirecting=[f"r{i}" for i in range(50)]
    )
    for check in (
        _check_duplicate_content_exact,
        _check_title_duplication,
        _check_broken_internal_links,
        _check_internal_redirect_links,
    ):
        assert_db_valid(check(a, site))


@pytest.mark.parametrize("key", sorted(PAGE_CHECKS))
def test_empty_evidence_page_is_db_valid(key):
    """A page with NO usable evidence produces valid n_a/fail rows, never a crash."""
    facts = make_facts(
        title=None,
        title_metrics={},
        description=None,
        description_metrics={},
        meta_robots=None,
        canonical_url=None,
        canonical_matches=None,
        noindex=None,
        nofollow=None,
        h1_count=None,
        word_count=None,
        image_count=None,
        images_missing_alt=None,
        fingerprint_version=None,
        exact_sha256=None,
    )
    assert_db_valid(PAGE_CHECKS[key](facts, SiteAggregates()))


# ---------------------------------------------------------------------------
# Internal linking / architecture — the checks that read `web.link_edge`.
#
# Each one gets the same two proofs: it fires for ITS OWN defect on an
# otherwise-healthy site, and it stays quiet for everyone else's.

INTERNAL_LINKING_CHECKS = {
    "excessive_outlinks": _check_excessive_outlinks,
    "nofollow_internal_links": _check_nofollow_internal_links,
    "anchor_text_descriptiveness": _check_anchor_text_descriptiveness,
    "crawl_depth": _check_crawl_depth,
    "internal_inlink_coverage": _check_internal_inlink_coverage,
    "orphan_pages": _check_orphan_pages,
}

HOME_ID = "home"


def healthy_stats(**overrides) -> PageLinkStats:
    base = dict(
        checked=20,
        outlinks_total=40,
        internal_outlinks=20,
        nofollow_internal_count=0,
        descriptive_anchors=20,
    )
    base.update(overrides)
    return PageLinkStats(**base)


def linked_site(facts: PageFacts, stats: PageLinkStats | None = None, **overrides):
    """A site where this page is healthy in every internal-linking sense."""
    site = SiteAggregates()
    site.link_stats[facts.page_id] = stats if stats is not None else healthy_stats()
    site.homepage_page_id = HOME_ID
    site.depth_by_page = {HOME_ID: 0, facts.page_id: 2}
    site.inlinks = {facts.page_id: {HOME_ID, "p2", "p3", "p4", "p5"}}
    site.internal_edges_resolved = 12
    site.orphans = OrphanCensus(complete=True, known_live_pages=10, captured_pages=10)
    for key, value in overrides.items():
        setattr(site, key, value)
    return site


def flagged_linking(facts: PageFacts, site: SiteAggregates) -> set[str]:
    flagged = set()
    for key, check in INTERNAL_LINKING_CHECKS.items():
        outcome = check(facts, site)
        assert_db_valid(outcome)
        if outcome.status in ("warn", "fail"):
            flagged.add(key)
    return flagged


def test_a_well_linked_page_trips_no_internal_linking_check():
    facts = make_facts()
    site = linked_site(facts)
    for key, check in INTERNAL_LINKING_CHECKS.items():
        outcome = check(facts, site)
        assert_db_valid(outcome)
        assert outcome.status == "pass", f"{key} flagged a well-linked page: {outcome}"


@pytest.mark.parametrize("key", sorted(INTERNAL_LINKING_CHECKS))
def test_internal_linking_checks_are_n_a_without_a_link_graph(key):
    """No edges recorded is missing evidence — never a silent pass."""
    outcome = INTERNAL_LINKING_CHECKS[key](make_facts(), SiteAggregates())
    assert outcome.status == "n_a" and outcome.score is None
    assert_db_valid(outcome)


# --- excessive_outlinks


@pytest.mark.parametrize(
    ("total", "status", "score"),
    [(150, "pass", 100), (300, "pass", 85), (500, "warn", 65), (501, "fail", 45)],
)
def test_excessive_outlinks_bands(total, status, score):
    facts = make_facts()
    site = linked_site(facts, healthy_stats(outlinks_total=total))
    outcome = _check_excessive_outlinks(facts, site)
    assert (outcome.status, outcome.score) == (status, score)
    assert_db_valid(outcome)


def test_excessive_outlinks_fires_alone():
    facts = make_facts()
    site = linked_site(facts, healthy_stats(outlinks_total=900))
    assert flagged_linking(facts, site) == {"excessive_outlinks"}


# --- nofollow_internal_links


@pytest.mark.parametrize(
    ("count", "status", "score"),
    [(0, "pass", 100), (1, "warn", 70), (9, "warn", 70), (10, "fail", 45)],
)
def test_nofollow_internal_bands(count, status, score):
    facts = make_facts()
    stats = healthy_stats(
        nofollow_internal_count=count,
        nofollow_internal_samples=[f"https://example.com/n{i}" for i in range(min(count, 5))],
    )
    outcome = _check_nofollow_internal_links(facts, linked_site(facts, stats))
    assert (outcome.status, outcome.score) == (status, score)
    assert_db_valid(outcome)


def test_nofollow_internal_fires_alone():
    facts = make_facts()
    site = linked_site(facts, healthy_stats(nofollow_internal_count=12))
    assert flagged_linking(facts, site) == {"nofollow_internal_links"}


# --- anchor_text_descriptiveness


@pytest.mark.parametrize(
    "anchor",
    [
        "Click here",
        "read more",
        "  LEARN MORE!  ",
        "",
        None,
        "https://example.com/a",
        "www.example.com",
    ],
)
def test_generic_and_empty_anchors_are_not_descriptive(anchor):
    assert _is_descriptive_anchor(anchor) is False


@pytest.mark.parametrize(
    "anchor",
    [
        "read more about our pricing plans",
        "Enterprise SEO audit checklist",
        "2026 benchmark report",
    ],
)
def test_real_anchors_are_credited(anchor):
    assert _is_descriptive_anchor(anchor) is True


def test_anchor_descriptiveness_is_the_catalogue_formula():
    facts = make_facts()
    stats = healthy_stats(
        internal_outlinks=20,
        descriptive_anchors=9,
        generic_anchor_targets=["https://example.com/x"],
    )
    outcome = _check_anchor_text_descriptiveness(facts, linked_site(facts, stats))
    assert outcome.score == 45  # round(100 * 9/20)
    assert outcome.status == "fail" and outcome.issue_count == 11
    assert_db_valid(outcome)


def test_anchor_descriptiveness_passes_a_page_with_no_internal_links():
    """The catalogue row is explicit: 100 when there are no internal links."""
    facts = make_facts()
    stats = healthy_stats(outlinks_total=6, internal_outlinks=0, descriptive_anchors=0)
    outcome = _check_anchor_text_descriptiveness(facts, linked_site(facts, stats))
    assert (outcome.status, outcome.score) == ("pass", 100)


def test_anchor_descriptiveness_fires_alone():
    facts = make_facts()
    site = linked_site(facts, healthy_stats(descriptive_anchors=2))
    assert flagged_linking(facts, site) == {"anchor_text_descriptiveness"}


# --- crawl_depth


@pytest.mark.parametrize(
    ("depth", "status", "score"),
    [
        (0, "pass", 100),
        (3, "pass", 100),
        (4, "warn", 75),
        (5, "warn", 55),
        (6, "fail", 35),
        (11, "fail", 35),
    ],
)
def test_crawl_depth_bands(depth, status, score):
    facts = make_facts()
    site = linked_site(facts)
    site.depth_by_page[facts.page_id] = depth
    outcome = _check_crawl_depth(facts, site)
    assert (outcome.status, outcome.score) == (status, score)
    assert_db_valid(outcome)


def test_crawl_depth_hands_unreachable_pages_to_the_orphan_check():
    """Two items must never score the same defect — the row says so."""
    facts = make_facts()
    site = linked_site(facts)
    site.depth_by_page = {HOME_ID: 0}
    outcome = _check_crawl_depth(facts, site)
    assert outcome.status == "n_a" and "orphan" in outcome.reasoning.lower()
    assert_db_valid(outcome)


def test_crawl_depth_is_n_a_without_a_homepage():
    facts = make_facts()
    site = linked_site(facts, homepage_page_id=None)
    assert _check_crawl_depth(facts, site).status == "n_a"


def test_crawl_depth_fires_alone():
    facts = make_facts()
    site = linked_site(facts)
    site.depth_by_page[facts.page_id] = 8
    assert flagged_linking(facts, site) == {"crawl_depth"}


# --- internal_inlink_coverage


@pytest.mark.parametrize(
    ("inlinks", "status", "score"),
    [(1, "warn", 45), (2, "warn", 70), (4, "warn", 70), (5, "pass", 100)],
)
def test_inlink_coverage_bands(inlinks, status, score):
    facts = make_facts()
    site = linked_site(facts)
    site.inlinks = {facts.page_id: {f"src{i}" for i in range(inlinks)}}
    outcome = _check_internal_inlink_coverage(facts, site)
    assert (outcome.status, outcome.score) == (status, score)
    assert_db_valid(outcome)


def test_inlink_coverage_hands_zero_to_the_orphan_check():
    facts = make_facts()
    site = linked_site(facts)
    site.inlinks = {}
    outcome = _check_internal_inlink_coverage(facts, site)
    assert outcome.status == "n_a" and "orphan" in outcome.reasoning.lower()


def test_inlink_coverage_fires_alone():
    facts = make_facts()
    site = linked_site(facts)
    site.inlinks = {facts.page_id: {HOME_ID}}
    assert flagged_linking(facts, site) == {"internal_inlink_coverage"}


# --- orphan_pages


def test_orphan_pages_flags_a_crawled_page_nothing_links_to():
    facts = make_facts()
    site = linked_site(facts)
    site.inlinks = {}
    site.orphans = OrphanCensus(
        complete=True,
        known_live_pages=10,
        captured_pages=10,
        crawled_orphan_ids={facts.page_id},
    )
    outcome = _check_orphan_pages(facts, site)
    assert outcome.status == "fail" and outcome.score == 90  # round(100 * (1 - 1/10))
    assert outcome.evidence["captured"] is not False
    assert "crawled successfully" in outcome.reasoning
    assert_db_valid(outcome)
    # …and it is the ONLY check that fires, because inlink coverage defers.
    assert flagged_linking(facts, site) == {"orphan_pages"}


def test_a_known_but_never_captured_url_is_reported_as_a_different_problem():
    """A sitemap/GSC-only URL is not the same finding as a crawled dead end."""
    facts = make_facts(latest_snapshot_id="")
    site = linked_site(facts)
    site.inlinks = {}
    site.orphans = OrphanCensus(
        complete=True,
        known_live_pages=10,
        captured_pages=9,
        uncrawled_orphans=1,
        uncrawled_orphan_urls=[facts.url],
    )
    outcome = _check_orphan_pages(facts, site)
    assert outcome.status == "fail" and outcome.score == 90
    assert outcome.evidence["captured"] is False
    assert "never successfully" in outcome.reasoning
    assert "crawled successfully" not in outcome.reasoning
    assert_db_valid(outcome)


def test_the_site_root_is_never_an_orphan():
    facts = make_facts(page_id=HOME_ID)
    site = linked_site(facts)
    site.inlinks = {}
    site.orphans = OrphanCensus(complete=True, known_live_pages=10, captured_pages=10)
    assert _check_orphan_pages(facts, site).status == "pass"


def test_orphan_pages_is_n_a_when_the_census_is_incomplete():
    """A truncated run cannot honestly divide by "known live pages"."""
    facts = make_facts()
    site = linked_site(facts)
    site.inlinks = {}
    site.orphans = OrphanCensus(complete=False, known_live_pages=10, captured_pages=10)
    outcome = _check_orphan_pages(facts, site)
    assert outcome.status == "n_a" and outcome.score is None


def test_orphan_site_score_is_the_catalogue_formula_including_its_floor():
    healthy = OrphanCensus(
        complete=True, known_live_pages=100, captured_pages=98, uncrawled_orphans=2
    )
    assert healthy.site_score() == 98
    majority = OrphanCensus(
        complete=True, known_live_pages=100, captured_pages=1, uncrawled_orphans=99
    )
    assert majority.site_score() == 5  # floored, not 1
    none_known = OrphanCensus(complete=True, known_live_pages=0)
    assert none_known.site_score() == 100


def test_both_orphan_classes_count_toward_the_site_ratio():
    census = OrphanCensus(
        complete=True,
        known_live_pages=10,
        crawled_orphan_ids={"p1", "p2"},
        uncrawled_orphans=3,
    )
    assert census.total == 5
    assert census.site_score() == 50


# ---------------------------------------------------------------------------
# One home per threshold — the internal-linking bands live in analysis.py only.


@pytest.mark.parametrize(
    "name",
    [
        "OUTLINK_BANDS",
        "OUTLINK_EXCESSIVE",
        "NOFOLLOW_REL_TOKENS",
        "NOFOLLOW_INTERNAL_BANDS",
        "NOFOLLOW_INTERNAL_EXCESSIVE",
        "GENERIC_ANCHOR_PHRASES",
        "ANCHOR_DESCRIPTIVE_FAIL_SCORE",
        "ANCHOR_DESCRIPTIVE_WARN_SCORE",
        "CRAWL_DEPTH_BANDS",
        "CRAWL_DEPTH_SEVERE",
        "INLINK_COVERAGE_BANDS",
        "INLINK_COVERAGE_HEALTHY",
        "ORPHAN_MAJORITY_RATIO",
        "ORPHAN_SCORE_FLOOR",
        "LINK_GRAPH_MIN_CAPTURE_RATIO",
    ],
)
def test_internal_linking_threshold_is_declared_exactly_once(name):
    package_root = Path(analysis_module.__file__).parent.parent
    homes = []
    for path in package_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            targets = (
                node.targets
                if isinstance(node, ast.Assign)
                else [node.target]
                if isinstance(node, ast.AnnAssign)
                else []
            )
            if any(isinstance(t, ast.Name) and t.id == name for t in targets):
                homes.append(path.relative_to(package_root).as_posix())
    assert homes == ["web_crawl/analysis.py"], f"{name} is declared in {homes}"


def test_a_half_crawled_site_never_manufactures_orphans():
    """The failure this gate exists for, measured on a real site.

    A crawl of titaniummarketing.com died with 119 pages fetched and 181 still
    queued. Of the 124 captured pages, 81 had no inbound internal link — not
    because they are orphans, but because the pages that link to them were
    never fetched. Both inbound-link checks must refuse to answer.
    """
    facts = make_facts()
    site = linked_site(facts)
    site.inlinks = {}
    site.orphans = OrphanCensus(complete=True, known_live_pages=271, captured_pages=124)
    assert site.orphans.graph_is_representative is False
    for check in (_check_orphan_pages, _check_internal_inlink_coverage):
        outcome = check(facts, site)
        assert outcome.status == "n_a" and outcome.score is None
        assert "124" in outcome.reasoning and "271" in outcome.reasoning
        assert outcome.remediation is not None
        assert_db_valid(outcome)


def test_the_capture_gate_opens_at_the_declared_ratio():
    ratio = analysis_module.LINK_GRAPH_MIN_CAPTURE_RATIO
    just_under = OrphanCensus(
        complete=True, known_live_pages=100, captured_pages=int(ratio * 100) - 1
    )
    exactly = OrphanCensus(complete=True, known_live_pages=100, captured_pages=int(ratio * 100))
    assert just_under.graph_is_representative is False
    assert exactly.graph_is_representative is True
    # A truncated registry is never representative, however well covered.
    assert (
        OrphanCensus(complete=False, known_live_pages=10, captured_pages=10).graph_is_representative
        is False
    )


def test_crawl_depth_keeps_a_shallow_pass_but_withholds_a_penalty_on_a_partial_graph():
    """More pages can only SHORTEN a path — so a pass survives, a penalty waits."""
    facts = make_facts()
    site = linked_site(facts)
    site.orphans = OrphanCensus(complete=True, known_live_pages=271, captured_pages=124)
    site.depth_by_page[facts.page_id] = 2
    assert _check_crawl_depth(facts, site).status == "pass"
    site.depth_by_page[facts.page_id] = 6
    deep = _check_crawl_depth(facts, site)
    assert deep.status == "n_a" and deep.score is None
    assert "6 clicks" in deep.reasoning and deep.remediation is not None
    assert_db_valid(deep)
