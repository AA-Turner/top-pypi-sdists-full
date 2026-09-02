"""`seo_audit` is the ONE implementation of every per-page SEO check.

Before 2026-08-09 the same checks existed three times — `seo_audit`,
`web_crawl/analysis.py`, and aidream's `crawl_service.IssueDetector` — with
independently drifting thresholds. These tests are the forcing function that
keeps them collapsed:

1. every per-page verdict comes from `seo_audit.PAGE_CHECKS` and nowhere else
   (the sweep's registry entries ARE those functions, not copies of them);
2. every threshold is declared exactly once, in `seo_audit` (or in
   `meta_metrics`, which owns the SERP length limits as a TS mirror);
3. each check fires for its own defect and stays quiet for everyone else's;
4. every rule the deleted `IssueDetector` had still fires — nothing was lost
   in the consolidation.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from matrx_scraper import seo_audit
from matrx_scraper.seo_audit import (
    CONTENT_DEPTH_ARTICLE_MIN_WORDS,
    CONTENT_DEPTH_ARTICLE_TARGET_WORDS,
    CONTENT_DEPTH_COMMERCE_MIN_WORDS,
    CONTENT_FAIL_WORDS,
    CONTENT_OK_WORDS,
    CONTENT_WARN_WORDS,
    HEADING_SKIP_FAIL_COUNT,
    IMAGE_ALT_FAIL_COUNT,
    IMAGE_ALT_FAIL_RATIO,
    LARGE_PAGE_BYTES,
    PAGE_CHECKS,
    REDIRECT_CHAIN_MAX_HOPS,
    TTFB_GOOD_MS,
    TTFB_POOR_MS,
    SOFT_404_EMPTY_MAX_WORDS,
    SOFT_404_PHRASE_MAX_WORDS,
    TEMPORARY_REDIRECT_STATUSES,
    TEXT_HTML_RATIO_FAIL,
    TEXT_HTML_RATIO_WARN,
    SOCIAL_META_PASS_SCORE,
    SOCIAL_META_WARN_SCORE,
    SOCIAL_NO_TWITTER_CARD_PENALTY,
    SOCIAL_OG_URL_CONFLICT_PENALTY,
    VIEWPORT_ZOOM_LOCK_MAX_SCALE,
    CheckOutcome,
    PageEvidence,
    audit_html,
    evidence_from_audit,
    run_page_checks,
)
from matrx_scraper.web_crawl import analysis, site_analysis

PACKAGE_ROOT = Path(seo_audit.__file__).parent

# Thresholds that must exist in exactly ONE module of the package.
SINGLE_HOME_THRESHOLDS = (
    "CONTENT_OK_WORDS",
    "CONTENT_WARN_WORDS",
    "CONTENT_FAIL_WORDS",
    "CONTENT_DEPTH_ARTICLE_MIN_WORDS",
    "CONTENT_DEPTH_ARTICLE_TARGET_WORDS",
    "CONTENT_DEPTH_COMMERCE_MIN_WORDS",
    "HEADING_SKIP_FAIL_COUNT",
    "HEADING_EMPTY_FAIL_RATIO",
    "TEXT_HTML_RATIO_FAIL",
    "TEXT_HTML_RATIO_WARN",
    "SOFT_404_PHRASE_MAX_WORDS",
    "SOFT_404_EMPTY_MAX_WORDS",
    "SOFT_404_TITLE_PATTERN",
    "TEMPORARY_REDIRECT_STATUSES",
    "IMAGE_ALT_FAIL_RATIO",
    "IMAGE_ALT_FAIL_COUNT",
    "REDIRECT_CHAIN_MAX_HOPS",
    "LARGE_PAGE_BYTES",
    "TTFB_GOOD_MS",
    "TTFB_POOR_MS",
    "VIEWPORT_ZOOM_LOCK_MAX_SCALE",
    "VIEWPORT_ZOOM_DISABLED_VALUES",
    "OG_IMAGE_SUPPORTED_EXTENSIONS",
    "SOCIAL_REQUIRED_OG_TAGS",
    "SOCIAL_OG_URL_CONFLICT_PENALTY",
    "SOCIAL_NO_TWITTER_CARD_PENALTY",
    "SOCIAL_META_PASS_SCORE",
    "SOCIAL_META_WARN_SCORE",
    "META_REFRESH_INSTANT_MAX_SECONDS",
    "SECURITY_RESPONSE_HEADERS",
    "HTTP_VARIANT_PERMANENT_REDIRECTS",
)

# Thresholds owned by the SITE checks, which live in `web_crawl/analysis.py`
# (a site verdict is not a per-page verdict and must never be built in
# `seo_audit`). Same rule, different single home.
SITE_THRESHOLDS = (
    "BASELINE_SECURITY_HEADERS",
    "SECURITY_HEADER_MISSING_PENALTY",
    "SECURITY_HEADER_MIN_SCORE",
    "SECURITY_HEADER_SAMPLE_LIMIT",
    "HSTS_MIN_MAX_AGE_SECONDS",
    "TLS_EXPIRY_CRITICAL_DAYS",
    "TLS_EXPIRY_WARN_DAYS",
)

# Thresholds owned by the crawlability half of the site family. Same rule, a
# different home: they belong beside the checks that read them, in
# `web_crawl/site_analysis.py`, and nowhere else.
CRAWLABILITY_SITE_THRESHOLDS = (
    "SITE_PASS_MIN_SCORE",
    "SITE_WARN_MIN_SCORE",
    "ROBOTS_SERVER_ERROR_SCORE",
    "ROBOTS_BLANKET_DISALLOW_SCORE",
    "ROBOTS_BLOCKS_WANTED_URLS_SCORE",
    "ROBOTS_SYNTAX_ERROR_SCORE",
    "ROBOTS_MISSING_SCORE",
    "ROBOTS_CLEAN_SCORE",
    "ROBOTS_BLOCK_SCAN_LIMIT",
    "SITEMAP_NONE_FOUND_SCORE",
    "SITEMAP_UNREACHABLE_SCORE",
    "SITEMAP_HEAVY_JUNK_SCORE",
    "SITEMAP_LIGHT_JUNK_SCORE",
    "SITEMAP_MINOR_ISSUE_SCORE",
    "SITEMAP_CLEAN_SCORE",
    "SITEMAP_HEAVY_JUNK_PCT",
    "SITEMAP_MAX_URLS_PER_DOC",
    "COVERAGE_HEALTHY_MIN_SCORE",
    "COVERAGE_GAPS_MIN_SCORE",
    "COVERAGE_ORPHAN_PENALTY_FACTOR",
    "COVERAGE_ORPHAN_PENALTY_MAX",
    "HOST_MULTIPLE_LIVE_SCORE",
    "HOST_SOFT_REDIRECT_SCORE",
    "HOST_SLASH_DUPLICATE_SCORE",
    "HOST_MIXED_INTERNAL_LINKS_SCORE",
    "HOST_CONSISTENT_SCORE",
    "HOST_PERMANENT_REDIRECT_STATUSES",
    "LINK_EDGE_HOST_SCAN_LIMIT",
)

# A social card with nothing wrong with it — the five required OG tags, a
# Twitter card, and an og:url that agrees with `healthy()`'s canonical.
COMPLETE_OG = {
    "og:title": "A perfectly reasonable page title here",
    "og:description": "A description of the page, for the share preview.",
    "og:image": "https://cdn.example.com/share.png",
    "og:url": "https://example.com/a",
    "og:type": "article",
}


def healthy(**overrides) -> PageEvidence:
    """A page with nothing wrong with it — every check must pass or be n_a."""
    base = dict(
        url="https://example.com/a",
        title="A perfectly reasonable page title here",
        title_metrics={"ok": True, "character_count": 39, "pixel_width": 300},
        description=(
            "A meta description that is long enough to look like real prose written "
            "for a human being to read in a search result."
        ),
        description_metrics={"ok": True, "character_count": 128, "pixel_width": 700},
        meta_robots="index, follow",
        canonical_url="https://example.com/a",
        canonical_matches=True,
        noindex=False,
        nofollow=False,
        h1_count=1,
        headings=[
            {"level": 1, "text": "One"},
            {"level": 2, "text": "Two"},
            {"level": 3, "text": "Three"},
            {"level": 2, "text": "Back up a level"},
        ],
        word_count=800,
        text_bytes=40_000,
        image_count=4,
        images_missing_alt=0,
        http_status=200,
        redirect_chain=[],
        mixed_content=[],
        response_bytes=120_000,
        response_time_ms=250,
        ttfb_ms=180,
        head_captured=True,
        lang="en-US",
        og=dict(COMPLETE_OG),
        twitter={"twitter:card": "summary_large_image"},
        head_meta={"viewport": "width=device-width, initial-scale=1", "refresh": None},
    )
    base.update(overrides)
    return PageEvidence(**base)


def assert_db_valid(outcome: CheckOutcome) -> None:
    """Mirror of analysis_result_status_score_valid + status_valid."""
    assert outcome.status in ("pass", "warn", "fail", "n_a")
    if outcome.status in ("pass", "warn", "fail"):
        assert outcome.score is not None and 1 <= outcome.score <= 100
    else:
        assert outcome.score is None
    assert outcome.reasoning


def flagged(evidence: PageEvidence) -> set[str]:
    """Names of the checks that returned warn or fail."""
    return {
        key
        for key, outcome in run_page_checks(evidence).items()
        if outcome.status in ("warn", "fail")
    }


# ---------------------------------------------------------------------------
# 1. One implementation


def test_sweep_registry_entries_are_the_seo_audit_functions():
    """Every catalogued per-page check dispatches into `seo_audit`.

    Not "produces the same answer" — literally closes over the same function
    object. A re-implementation in analysis.py fails here immediately.
    """
    for key in analysis.CATALOGUED_PAGE_CHECKS:
        adapted = analysis.PAGE_CHECKS[key]
        closed_over = {cell.cell_contents for cell in (adapted.__closure__ or ())}
        assert PAGE_CHECKS[key] in closed_over, (
            f"{key} in web_crawl/analysis.py does not dispatch to seo_audit.PAGE_CHECKS"
        )


def test_analysis_module_defines_no_per_page_check():
    """analysis.py may implement CROSS-page checks only."""
    source = Path(analysis.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    defined = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name.startswith("_check_")
    }
    cross_page = {f"_check_{key}" for key in analysis.CROSS_PAGE_CHECKS}
    assert defined == cross_page, (
        "web_crawl/analysis.py implements a check that is not cross-page: "
        f"{sorted(defined - cross_page)}"
    )


def test_site_checks_are_never_page_checks_and_live_in_their_own_modules():
    """The other direction: a SITE verdict never leaks into `seo_audit`.

    `tls_certificate`, `hsts_policy` and `security_headers` describe the host,
    not a page. Implementing one in `seo_audit.PAGE_CHECKS` would write the same
    answer onto every page row and let one page resolve a finding the rest still
    trip; implementing a per-page check in a site registry would hide it from
    every consumer of the canonical per-page registry.

    Two homes, one registry: the security site checks live in `analysis.py` as
    `_site_check_*`, the crawlability ones in `site_analysis.py`, and
    `analysis.SITE_CHECKS` is the ONE registry the sweep writes from.
    """
    assert not set(analysis.SITE_CHECKS) & set(PAGE_CHECKS), (
        "a check is registered as BOTH a site check and a per-page check"
    )
    assert set(site_analysis.CRAWLABILITY_SITE_CHECKS) <= set(analysis.SITE_CHECKS), (
        "a crawlability site check is implemented but never recorded"
    )
    source = Path(analysis.__file__).read_text(encoding="utf-8")
    defined = {
        node.name
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.FunctionDef) and node.name.startswith("_site_check_")
    }
    orphans = defined - {f"_site_check_{key}" for key in analysis.SITE_CHECKS}
    assert not orphans, f"site check(s) implemented but never registered: {sorted(orphans)}"


@pytest.mark.parametrize("name", SITE_THRESHOLDS)
def test_site_threshold_is_declared_exactly_once_in_the_package(name):
    homes = []
    for path in PACKAGE_ROOT.rglob("*.py"):
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
                homes.append(path.relative_to(PACKAGE_ROOT).as_posix())
    assert homes == ["web_crawl/analysis.py"], (
        f"{name} is declared in {homes} — it must live in one place"
    )


@pytest.mark.parametrize("name", CRAWLABILITY_SITE_THRESHOLDS)
def test_crawlability_site_threshold_is_declared_exactly_once(name):
    homes = []
    for path in PACKAGE_ROOT.rglob("*.py"):
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
                homes.append(path.relative_to(PACKAGE_ROOT).as_posix())
    assert homes == ["web_crawl/site_analysis.py"], (
        f"{name} is declared in {homes} — it must live in one place"
    )


def test_site_analysis_module_defines_only_site_checks():
    """`site_analysis.py` may implement SITE-subject checks only.

    The same forcing function as `test_analysis_module_defines_no_per_page_check`,
    one module over: a per-page or cross-page rule implemented here would be a
    second home for a verdict that already has one.
    """
    source = Path(site_analysis.__file__).read_text(encoding="utf-8")
    defined = {
        node.name
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.FunctionDef) and node.name.startswith("_check_")
    }
    expected = {f"_check_{key}" for key in site_analysis.CRAWLABILITY_SITE_CHECKS}
    assert defined == expected, (
        "web_crawl/site_analysis.py implements a check that is not a registered "
        f"site check: {sorted(defined - expected)}"
    )


def test_every_crawlability_site_check_is_reachable_from_the_sweep_registry():
    """The adapter in analysis.py dispatches to THIS function object.

    Not "produces the same answer" — a re-implementation on either side fails
    here immediately, exactly as the per-page adapter test does.
    """
    for key, check in site_analysis.CRAWLABILITY_SITE_CHECKS.items():
        adapted = analysis.SITE_CHECKS[key]
        closed_over = {cell.cell_contents for cell in (adapted.__closure__ or ())}
        assert check in closed_over, (
            f"{key} in analysis.SITE_CHECKS does not dispatch to site_analysis"
        )


def test_every_catalogued_key_is_a_canonical_check():
    unknown = set(analysis.CATALOGUED_PAGE_CHECKS) - set(PAGE_CHECKS)
    assert not unknown, f"sweep claims per-page checks seo_audit does not define: {unknown}"
    assert not set(analysis.CROSS_PAGE_CHECKS) & set(PAGE_CHECKS), (
        "a check is registered as BOTH per-page and cross-page"
    )


def test_uncatalogued_checks_are_reported_not_swallowed():
    """A canonical check with no catalogue row must be nameable, and loud.

    `analyze_site_pages` writes this list into `summary.errors` on every run;
    the failure mode this prevents is a check quietly computing nothing.
    """
    reported = analysis._uncatalogued_page_checks()
    assert reported == sorted(set(PAGE_CHECKS) - set(analysis.CATALOGUED_PAGE_CHECKS))
    for key in reported:
        assert key in PAGE_CHECKS


# ---------------------------------------------------------------------------
# 2. One home per threshold


@pytest.mark.parametrize("name", SINGLE_HOME_THRESHOLDS)
def test_threshold_is_declared_exactly_once_in_the_package(name):
    homes = []
    for path in PACKAGE_ROOT.rglob("*.py"):
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
                homes.append(path.relative_to(PACKAGE_ROOT).as_posix())
    assert homes == ["seo_audit.py"], f"{name} is declared in {homes} — it must live in one place"


def test_serp_length_limits_are_not_redeclared_in_seo_audit():
    """meta_metrics owns them (TS mirror); a second copy would drift."""
    source = (PACKAGE_ROOT / "seo_audit.py").read_text(encoding="utf-8")
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                assert not (
                    isinstance(target, ast.Name) and target.id.endswith("_SEO_MAX_CHARS")
                ), "SERP length limits belong to meta_metrics, not seo_audit"


# ---------------------------------------------------------------------------
# 3. Each check fires for its own defect, and only its own


def test_a_healthy_page_trips_nothing():
    outcomes = run_page_checks(healthy())
    for key, outcome in outcomes.items():
        assert_db_valid(outcome)
        assert outcome.status in ("pass", "n_a"), f"{key} flagged a healthy page: {outcome}"


@pytest.mark.parametrize(
    ("overrides", "expected"),
    [
        # --- title
        ({"title": None, "title_metrics": {}}, {"title_presence"}),
        (
            {
                "title_metrics": {
                    "ok": False,
                    "character_count": 9,
                    "issues": ["Title is too short"],
                }
            },
            {"title_length"},
        ),
        # --- meta description
        ({"description": None, "description_metrics": {}}, {"meta_description_presence"}),
        (
            {
                "description_metrics": {
                    "ok": False,
                    "character_count": 12,
                    "issues": ["Description is too short"],
                }
            },
            {"meta_description_length"},
        ),
        # --- structure
        ({"h1_count": 0}, {"h1_presence"}),
        ({"h1_count": 3}, {"h1_presence"}),
        # `healthy()` declares og:type=article, so a page short enough to be
        # thin is ALSO short for its own declared type — both verdicts are true
        # and they are deliberately different questions (absolute floor vs
        # per-type expectation).
        ({"word_count": CONTENT_OK_WORDS - 1}, {"thin_content", "content_depth"}),
        (
            {"word_count": CONTENT_FAIL_WORDS - 1},
            {"thin_content", "content_depth"},
        ),
        # --- outline
        (
            {"headings": [{"level": 1, "text": "A"}, {"level": 4, "text": "B"}]},
            {"heading_hierarchy"},
        ),
        (
            {"headings": [{"level": lvl, "text": f"h{lvl}"} for lvl in (1, 3, 1, 3, 1, 3, 1, 3)]},
            {"heading_hierarchy"},
        ),
        (
            {"headings": [{"level": 1, "text": ""}, {"level": 2, "text": "Real"}]},
            {"heading_hierarchy"},
        ),
        ({"headings": []}, {"heading_hierarchy"}),
        # --- content depth (its own defect: long enough to clear the thin-content
        # floor, short for a page that calls itself an article)
        ({"word_count": CONTENT_DEPTH_ARTICLE_MIN_WORDS - 1}, {"content_depth"}),
        # --- text-to-HTML ratio
        ({"text_bytes": 1_000}, {"text_html_ratio"}),
        # --- soft 404: a 200 that titles itself an error and carries nothing
        (
            {"title": "404 — Page Not Found", "word_count": 12},
            {"soft_404_detection", "thin_content", "content_depth"},
        ),
        # --- temporary redirect: a 302 hop on the way to a 200
        (
            {
                "redirect_chain": [
                    {"status": 302, "url": "https://example.com/old"},
                    {"status": 200, "url": "https://example.com/a"},
                ]
            },
            {"temporary_redirect_usage"},
        ),
        ({"image_count": 10, "images_missing_alt": 2}, {"image_alt_presence"}),
        # --- indexability
        ({"meta_robots": "noindex", "noindex": True}, {"meta_robots_conflicts"}),
        ({"meta_robots": "index, nofollow", "nofollow": True}, {"meta_robots_conflicts"}),
        ({"canonical_url": None}, {"canonical_presence"}),
        (
            {
                "canonical_url": "https://example.com/b",
                "canonical_matches": False,
                # og:url follows the canonical, so ONLY the canonical check trips.
                "og": {**COMPLETE_OG, "og:url": "https://example.com/b"},
            },
            {"canonical_conflicts"},
        ),
        # --- transport (rules that existed ONLY in the deleted IssueDetector)
        ({"http_status": 404}, {"broken_page_4xx"}),
        ({"http_status": 503}, {"server_error_5xx"}),
        ({"http_status": 0}, {"server_error_5xx"}),
        ({"http_status": 301}, {"redirect_chain"}),
        (
            {
                "redirect_chain": [
                    {"url": "https://example.com/1"},
                    {"url": "https://example.com/2"},
                    {"url": "https://example.com/a"},
                ]
            },
            {"redirect_chain"},
        ),
        (
            {
                "redirect_chain": [
                    {"url": "https://example.com/a"},
                    {"url": "https://example.com/b"},
                    {"url": "https://example.com/a"},
                ]
            },
            {"redirect_chain", "redirect_loop"},
        ),
        # --- mobile rendering
        ({"head_meta": {"viewport": None, "refresh": None}}, {"viewport_meta"}),
        (
            {"head_meta": {"viewport": "width=1024", "refresh": None}},
            {"viewport_meta"},
        ),
        (
            {
                "head_meta": {
                    "viewport": "width=device-width, initial-scale=1, user-scalable=no",
                    "refresh": None,
                }
            },
            {"viewport_meta"},
        ),
        (
            {
                "head_meta": {
                    "viewport": "width=device-width, initial-scale=1, maximum-scale=1",
                    "refresh": None,
                }
            },
            {"viewport_meta"},
        ),
        # --- language
        ({"lang": None}, {"html_lang_validity"}),
        ({"lang": "english"}, {"html_lang_validity"}),
        # --- social card
        (
            {"og": {**COMPLETE_OG, "og:image": ""}},
            {"og_image_validity", "social_meta_completeness"},
        ),
        ({"og": {**COMPLETE_OG, "og:image": "/share.png"}}, {"og_image_validity"}),
        (
            {"og": {**COMPLETE_OG, "og:image": "https://cdn.example.com/a.svg"}},
            {"og_image_validity"},
        ),
        (
            {"og": {k: v for k, v in COMPLETE_OG.items() if k != "og:type"}},
            {"social_meta_completeness"},
        ),
        ({"twitter": {}}, {"social_meta_completeness"}),
        (
            {"og": {**COMPLETE_OG, "og:url": "https://example.com/somewhere-else"}},
            {"social_meta_completeness"},
        ),
        # --- meta refresh standing in for an HTTP redirect
        (
            {
                "head_meta": {
                    "viewport": "width=device-width",
                    "refresh": "0; url=https://example.com/b",
                }
            },
            {"meta_refresh_redirect"},
        ),
        (
            {
                "head_meta": {
                    "viewport": "width=device-width",
                    "refresh": "5; url=https://example.com/b",
                }
            },
            {"meta_refresh_redirect"},
        ),
        ({"pagination": {"next": "https://example.com/a"}}, {"pagination_markup"}),
        ({"mixed_content": ["http://cdn.example.com/x.png"]}, {"mixed_content"}),
        ({"url": "http://example.com/a"}, {"https_enforcement"}),
        # A 5 MB document carrying the same 40 KB of text IS both defects: too
        # heavy, and almost none of that weight is content.
        (
            {"response_bytes": LARGE_PAGE_BYTES + 1},
            {"page_weight", "text_html_ratio"},
        ),
        ({"ttfb_ms": TTFB_POOR_MS + 1}, {"ttfb_server_response"}),
    ],
)
def test_one_defect_trips_exactly_its_own_check(overrides, expected):
    evidence = healthy(**overrides)
    assert flagged(evidence) == expected
    for outcome in run_page_checks(evidence).values():
        assert_db_valid(outcome)


@pytest.mark.parametrize(
    ("ttfb", "status", "score"),
    [
        (0, "pass", 100),
        (400, "pass", 95),
        (TTFB_GOOD_MS, "pass", 90),
        (TTFB_GOOD_MS + 1, "warn", 89),
        (1_300, "warn", 70),  # exact midpoint — floor, so JS Math.floor agrees
        (TTFB_POOR_MS, "warn", 50),
        (TTFB_POOR_MS + 1, "fail", 49),
        (3_000, "fail", 37),
        (20_000, "fail", 1),  # clamped, never below 1
    ],
)
def test_ttfb_bands_are_the_catalogue_rows_formula(ttfb, status, score):
    """The `ttfb_server_response` row publishes these bands; the code owes them.

    Row `score_contract.formula`: ttfb<=800 → 90-100; 800-1800 → 50-89 linear;
    >1800 → max(1, 49 - (ttfb-1800)/100). Every boundary is asserted, because
    a boundary that drifts is a scoring change nobody agreed to.
    """
    outcome = seo_audit.check_ttfb_server_response(healthy(ttfb_ms=ttfb))
    assert (outcome.status, outcome.score) == (status, score)
    assert_db_valid(outcome)


def test_ttfb_never_falls_back_to_total_response_time():
    """The old-snapshot path: a total was recorded, TTFB was not.

    Every `web.snapshot` written before TTFB capture landed has
    `perf.response_time_ms` and no `perf.ttfb_ms`, as does anything the browser
    transport fetched. Total elapsed also covers the body download, so reusing
    it would score a fast server as slow (and, on a fast download, a slow one
    as fine). The only honest answer is n_a — with a one-click re-capture.
    """
    outcome = seo_audit.check_ttfb_server_response(healthy(response_time_ms=8_400, ttfb_ms=None))
    assert outcome.status == "n_a"
    assert outcome.score is None
    assert outcome.remediation is not None
    assert "8400" not in outcome.reasoning and "8,400" not in outcome.reasoning
    assert_db_valid(outcome)


def test_page_weight_grades_the_html_document_only():
    """The row is narrowed to what is measured: HTML document bytes.

    Subresource transfer sizes are never captured — the crawl reads subresource
    URLs out of the markup and never fetches them — so there is no total page
    weight to grade, and the catalogue row must not promise one. This test is
    the pin: if total weight ever IS captured, this fails and the row, the
    check, and its bands move together.
    """
    assert seo_audit.check_page_weight(healthy(response_bytes=None)).status == "n_a"
    ok = seo_audit.check_page_weight(healthy(response_bytes=LARGE_PAGE_BYTES))
    assert (ok.status, ok.score) == ("pass", 100)
    over = seo_audit.check_page_weight(healthy(response_bytes=LARGE_PAGE_BYTES + 1))
    assert over.status == "warn"
    assert "HTML document" in over.reasoning
    assert over.evidence == {"bytes": LARGE_PAGE_BYTES + 1}


def test_thin_content_bands_are_the_canonical_three():
    assert seo_audit.check_thin_content(healthy(word_count=CONTENT_OK_WORDS)).status == "pass"
    assert seo_audit.check_thin_content(healthy(word_count=CONTENT_WARN_WORDS)).status == "warn"
    assert seo_audit.check_thin_content(healthy(word_count=CONTENT_FAIL_WORDS)).status == "warn"
    assert seo_audit.check_thin_content(healthy(word_count=CONTENT_FAIL_WORDS - 1)).status == "fail"


def test_heading_hierarchy_separates_the_outline_bands():
    clean = seo_audit.check_heading_hierarchy(healthy())
    assert clean.status == "pass" and clean.score == 100

    one_skip = seo_audit.check_heading_hierarchy(
        healthy(headings=[{"level": 1, "text": "A"}, {"level": 3, "text": "B"}])
    )
    assert one_skip.status == "warn" and one_skip.score == 70

    many_skips = seo_audit.check_heading_hierarchy(
        healthy(
            headings=[
                {"level": lvl, "text": f"h{lvl}"} for lvl in (1, 3) * (HEADING_SKIP_FAIL_COUNT + 1)
            ]
        )
    )
    assert many_skips.status == "warn" and many_skips.score == 45

    # A page that starts at h2 has a MISSING H1 — that is check_h1_presence's
    # verdict, and counting it here too would charge the same defect twice.
    starts_low = seo_audit.check_heading_hierarchy(
        healthy(headings=[{"level": 2, "text": "A"}, {"level": 3, "text": "B"}])
    )
    assert starts_low.status == "pass"

    # No headings is only a defect once there is content to organise.
    assert seo_audit.check_heading_hierarchy(healthy(headings=[])).status == "warn"
    assert seo_audit.check_heading_hierarchy(healthy(headings=[], word_count=10)).status == "pass"

    # Never captured is not "none" — it is unknown, and it must say so.
    unknown = seo_audit.check_heading_hierarchy(healthy(headings=None))
    assert unknown.status == "n_a" and unknown.remediation is not None


def test_content_depth_is_per_type_and_never_a_second_thin_content():
    """The distinction that keeps `content_depth` from duplicating `thin_content`."""
    # A page that declares no type has no expectation to be held to.
    typeless = healthy(og={}, schema_types=[], word_count=120)
    assert seo_audit.check_content_depth(typeless).status == "n_a"
    # ...while the absolute floor still fires for it. Different questions.
    assert seo_audit.check_thin_content(typeless).status == "warn"

    article_short = healthy(word_count=CONTENT_DEPTH_ARTICLE_MIN_WORDS - 1)
    assert seo_audit.check_content_depth(article_short).score == 55
    # Deep enough for the thin-content floor, shallow for an article: this is
    # exactly the gap `content_depth` exists to report.
    assert seo_audit.check_thin_content(article_short).status == "pass"

    solid = seo_audit.check_content_depth(
        healthy(word_count=CONTENT_DEPTH_ARTICLE_TARGET_WORDS - 1)
    )
    assert solid.status == "pass" and solid.score == 80
    full = seo_audit.check_content_depth(healthy(word_count=CONTENT_DEPTH_ARTICLE_TARGET_WORDS))
    assert full.status == "pass" and full.score == 100

    # The SAME word count is a shallow article and a normal product page.
    product = healthy(og={**COMPLETE_OG, "og:type": "product"}, word_count=300)
    assert seo_audit.check_content_depth(product).status == "pass"
    empty_product = healthy(
        schema_types=["Product"],
        og={},
        word_count=CONTENT_DEPTH_COMMERCE_MIN_WORDS - 1,
    )
    assert seo_audit.check_content_depth(empty_product).score == 60

    # Utility pages are exempt by the row's own rule.
    assert (
        seo_audit.check_content_depth(
            healthy(schema_types=["ContactPage"], og={}, word_count=20)
        ).status
        == "pass"
    )


def test_text_html_ratio_only_reacts_to_the_extremes():
    html_bytes = 100_000
    bloated = healthy(
        response_bytes=html_bytes, text_bytes=int(html_bytes * TEXT_HTML_RATIO_FAIL) - 1
    )
    assert seo_audit.check_text_html_ratio(bloated).status == "warn"
    middling = healthy(
        response_bytes=html_bytes, text_bytes=int(html_bytes * TEXT_HTML_RATIO_WARN) - 1
    )
    assert seo_audit.check_text_html_ratio(middling).status == "pass"
    healthy_ratio = healthy(
        response_bytes=html_bytes, text_bytes=int(html_bytes * TEXT_HTML_RATIO_WARN) + 1
    )
    assert seo_audit.check_text_html_ratio(healthy_ratio).status == "pass"
    missing = seo_audit.check_text_html_ratio(healthy(text_bytes=None))
    assert missing.status == "n_a" and missing.remediation is not None


def test_soft_404_needs_a_200_and_scores_signals_separately():
    error_page = healthy(title="Page Not Found", word_count=SOFT_404_PHRASE_MAX_WORDS - 1)
    strong = seo_audit.check_soft_404_detection(error_page)
    assert strong.status == "fail" and strong.score == 15

    empty = seo_audit.check_soft_404_detection(healthy(word_count=SOFT_404_EMPTY_MAX_WORDS - 1))
    assert empty.status == "warn" and empty.score == 40

    phrasing_only = seo_audit.check_soft_404_detection(healthy(title="404 error"))
    assert phrasing_only.status == "warn" and phrasing_only.score == 70

    thin_only = seo_audit.check_soft_404_detection(
        healthy(word_count=SOFT_404_PHRASE_MAX_WORDS - 1)
    )
    assert thin_only.status == "warn" and thin_only.score == 70

    # An honest 404 is not a soft 404 — that is `broken_page_4xx`'s job.
    honest = seo_audit.check_soft_404_detection(
        healthy(http_status=404, title="Page Not Found", word_count=5)
    )
    assert honest.status == "pass"
    assert seo_audit.check_soft_404_detection(healthy()).status == "pass"


def test_temporary_redirect_reads_hop_statuses_and_never_guesses():
    for status in sorted(TEMPORARY_REDIRECT_STATUSES):
        chain = healthy(
            redirect_chain=[
                {"status": status, "url": "https://example.com/old"},
                {"status": 200, "url": "https://example.com/a"},
            ]
        )
        outcome = seo_audit.check_temporary_redirect_usage(chain)
        assert outcome.status == "warn" and outcome.score == 65

    permanent = healthy(
        redirect_chain=[
            {"status": 301, "url": "https://example.com/old"},
            {"status": 200, "url": "https://example.com/a"},
        ]
    )
    assert seo_audit.check_temporary_redirect_usage(permanent).status == "pass"
    assert seo_audit.check_temporary_redirect_usage(healthy()).status == "pass"

    # A chain recorded without hop statuses cannot be judged — say so.
    statusless = seo_audit.check_temporary_redirect_usage(
        healthy(redirect_chain=[{"url": "https://example.com/old"}])
    )
    assert statusless.status == "n_a" and statusless.remediation is not None
    # And a URL that was never fetched is unknown, not clean.
    assert (
        seo_audit.check_temporary_redirect_usage(PageEvidence(url="https://example.com/a")).status
        == "n_a"
    )


def test_image_alt_escalates_at_both_declared_bounds():
    ratio_fail = healthy(image_count=10, images_missing_alt=int(10 * IMAGE_ALT_FAIL_RATIO))
    assert seo_audit.check_image_alt_presence(ratio_fail).status == "fail"
    count_fail = healthy(image_count=100, images_missing_alt=IMAGE_ALT_FAIL_COUNT)
    assert seo_audit.check_image_alt_presence(count_fail).status == "fail"
    warn = healthy(image_count=100, images_missing_alt=IMAGE_ALT_FAIL_COUNT - 1)
    assert seo_audit.check_image_alt_presence(warn).status == "warn"


def test_viewport_bands_are_the_catalogue_rows_four():
    """Missing < fixed-width < zoom-locked < responsive, per the score_contract."""
    missing = seo_audit.check_viewport_meta(healthy(head_meta={"viewport": " ", "refresh": None}))
    fixed = seo_audit.check_viewport_meta(
        healthy(head_meta={"viewport": "width=980", "refresh": None})
    )
    locked = seo_audit.check_viewport_meta(
        healthy(
            head_meta={
                "viewport": f"width=device-width, maximum-scale={VIEWPORT_ZOOM_LOCK_MAX_SCALE}",
                "refresh": None,
            }
        )
    )
    good = seo_audit.check_viewport_meta(healthy())
    assert [o.status for o in (missing, fixed, locked, good)] == ["fail", "fail", "warn", "pass"]
    assert missing.score < fixed.score < locked.score < good.score


def test_viewport_is_n_a_on_a_snapshot_that_never_captured_it():
    """The 2.0-weight check must never invent a missing tag for an old snapshot."""
    outcome = seo_audit.check_viewport_meta(healthy(head_meta=None))
    assert outcome.status == "n_a" and outcome.score is None
    assert outcome.remediation is not None


def test_html_lang_accepts_real_bcp47_and_rejects_prose():
    for tag in ("en", "en-US", "zh-Hant-TW", "de-CH-1901", "pt-BR"):
        assert seo_audit.check_html_lang_validity(healthy(lang=tag)).status == "pass", tag
    for tag in ("english", "en_US", "e", "en-", "12345"):
        assert seo_audit.check_html_lang_validity(healthy(lang=tag)).status == "fail", tag


def test_social_completeness_scores_the_catalogue_formula():
    full = seo_audit.check_social_meta_completeness(healthy())
    assert full.status == "pass" and full.score == SOCIAL_META_PASS_SCORE

    no_card = seo_audit.check_social_meta_completeness(healthy(twitter={}))
    assert no_card.score == SOCIAL_META_PASS_SCORE - SOCIAL_NO_TWITTER_CARD_PENALTY

    conflict = seo_audit.check_social_meta_completeness(
        healthy(og={**COMPLETE_OG, "og:url": "https://example.com/other"})
    )
    assert conflict.score == SOCIAL_META_PASS_SCORE - SOCIAL_OG_URL_CONFLICT_PENALTY

    one_tag = seo_audit.check_social_meta_completeness(
        healthy(og={"og:title": "Only a title"}, twitter={})
    )
    assert one_tag.status == "fail" and one_tag.score < SOCIAL_META_WARN_SCORE


def test_og_url_trailing_slash_is_not_a_canonical_conflict():
    outcome = seo_audit.check_social_meta_completeness(
        healthy(og={**COMPLETE_OG, "og:url": "https://EXAMPLE.com/a/"})
    )
    assert outcome.status == "pass"


def test_meta_refresh_separates_a_redirect_from_a_page_reload():
    instant = seo_audit.check_meta_refresh_redirect(
        healthy(head_meta={"viewport": "width=device-width", "refresh": "0;url=/b"})
    )
    delayed = seo_audit.check_meta_refresh_redirect(
        healthy(head_meta={"viewport": "width=device-width", "refresh": "5; url=/b"})
    )
    # No target: the page refreshes ITSELF. Not a redirect, so not this check's
    # defect — the catalogue row is about standing in for an HTTP redirect.
    reload_only = seo_audit.check_meta_refresh_redirect(
        healthy(head_meta={"viewport": "width=device-width", "refresh": "30"})
    )
    assert [o.status for o in (instant, delayed, reload_only)] == ["fail", "warn", "pass"]
    assert instant.score < delayed.score


def test_redirect_loop_is_a_fail_and_a_short_chain_is_not():
    short = healthy(
        redirect_chain=[{"url": "https://example.com/1"}, {"url": "https://example.com/a"}]
    )
    assert len(short.redirect_chain) <= REDIRECT_CHAIN_MAX_HOPS
    assert seo_audit.check_redirect_chain(short).status == "pass"
    assert seo_audit.check_redirect_loop(short).status == "pass"
    loop = healthy(
        redirect_chain=[
            {"url": "https://example.com/a"},
            {"url": "https://example.com/b"},
            {"url": "https://example.com/a"},
        ]
    )
    outcome = seo_audit.check_redirect_loop(loop)
    assert outcome.status == "fail" and "LOOP" in outcome.reasoning


# A check whose "no evidence" state is genuinely clean, not unknown: no robots
# directives, no insecure resources, and no redirect chain are all real passes.
_CLEAN_ON_ABSENCE = (
    "meta_robots_conflicts",
    "mixed_content",
    "redirect_chain",
    "redirect_loop",
    "url_design_quality",
)


def test_missing_evidence_is_never_a_silent_pass():
    """Every field absent → n_a or fail, never a pass on nothing."""
    blank = PageEvidence(url="https://example.com/a")
    for key, outcome in run_page_checks(blank).items():
        assert_db_valid(outcome)
        assert outcome.status != "pass" or key in _CLEAN_ON_ABSENCE, (
            f"{key} passed a page with no evidence at all"
        )


# ---------------------------------------------------------------------------
# 4. End to end from real HTML


def test_audit_html_output_feeds_the_checks_directly():
    html = """
    <html lang="en"><head>
      <title>Hi</title>
      <link rel="canonical" href="https://example.com/other">
      <meta name="robots" content="noindex">
    </head><body>
      <h1>One</h1><h1>Two</h1>
      <img src="/a.png">
      <img src="http://cdn.example.com/b.png" alt="ok">
      <p>Short body.</p>
    </body></html>
    """
    evidence = evidence_from_audit(
        audit_html(html, "https://example.com/page"),
        http_status=200,
        redirect_chain=[],
        response_bytes=4_000,
        response_time_ms=90,
    )
    tripped = flagged(evidence)
    assert {
        "title_length",
        "meta_description_presence",
        "h1_presence",
        "thin_content",
        "image_alt_presence",
        "meta_robots_conflicts",
        "canonical_conflicts",
        "mixed_content",
    } <= tripped
    for outcome in run_page_checks(evidence).values():
        assert_db_valid(outcome)


def test_a_clean_document_passes_every_check_end_to_end():
    # The document declares og:type=article, so it must clear the ARTICLE
    # expectation, not merely the absolute thin-content floor.
    body = " ".join(f"word{i}" for i in range(CONTENT_DEPTH_ARTICLE_TARGET_WORDS + 50))
    html = f"""
    <html lang="en"><head>
      <title>A clear, useful page title for readers</title>
      <meta name="description" content="{"A useful summary of the page. " * 4}">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta property="og:title" content="A clear, useful page title for readers">
      <meta property="og:description" content="A useful summary of the page.">
      <meta property="og:image" content="https://cdn.example.com/share.png">
      <meta property="og:url" content="https://example.com/page">
      <meta property="og:type" content="article">
      <meta name="twitter:card" content="summary_large_image">
      <link rel="canonical" href="https://example.com/page">
    </head><body><h1>Heading</h1><img src="/a.webp" alt="described" width="800" height="600"><p>{body}</p></body></html>
    """
    evidence = evidence_from_audit(
        audit_html(html, "https://example.com/page"),
        http_status=200,
        response_bytes=50_000,
        response_time_ms=120,
    )
    assert flagged(evidence) == set()
