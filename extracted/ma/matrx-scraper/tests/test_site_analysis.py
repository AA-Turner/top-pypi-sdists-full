"""The SITE-subject crawlability checks — pure-logic tests (no DB, no network).

Each check is a `web.analysis_item` row's `score_contract` made executable, so
these tests walk that contract rule by rule, top-down, and pin two things every
one of them must satisfy:

1. **The DB write contract.** `pass|warn|fail` carry a score 1–100; `n_a` and
   `error` carry NULL (`analysis_result_status_score_valid`). Every outcome
   here is asserted against that shape, exactly as the page checks are.
2. **A pass on unverified evidence is a lie.** Every check has a
   missing-evidence path, and that path is `n_a` with a one-click remediation —
   never a pass, and never prose telling a non-technical user to run a command.
"""

from __future__ import annotations

import pytest

from matrx_scraper.seo_audit import CheckOutcome
from matrx_scraper.web_crawl.site_analysis import (
    COVERAGE_HEALTHY_MIN_SCORE,
    CRAWLABILITY_SITE_CHECKS,
    HOST_CONSISTENT_SCORE,
    HOST_MIXED_INTERNAL_LINKS_SCORE,
    HOST_MULTIPLE_LIVE_SCORE,
    HOST_SLASH_DUPLICATE_SCORE,
    HOST_SOFT_REDIRECT_SCORE,
    ROBOTS_BLANKET_DISALLOW_SCORE,
    ROBOTS_BLOCKS_WANTED_URLS_SCORE,
    ROBOTS_CLEAN_SCORE,
    ROBOTS_MISSING_SCORE,
    ROBOTS_SERVER_ERROR_SCORE,
    ROBOTS_SYNTAX_ERROR_SCORE,
    SITEMAP_CLEAN_SCORE,
    SITEMAP_HEAVY_JUNK_SCORE,
    SITEMAP_LIGHT_JUNK_SCORE,
    SITEMAP_MAX_URLS_PER_DOC,
    SITEMAP_MINOR_ISSUE_SCORE,
    SITEMAP_NONE_FOUND_SCORE,
    SITEMAP_UNREACHABLE_SCORE,
    SiteEvidence,
    SitemapDocFacts,
    _check_host_protocol_consistency,
    _check_robots_txt_health,
    _check_sitemap_coverage,
    _check_sitemap_health,
)
from matrx_scraper.web_crawl.site_probe import (
    RobotsCapture,
    SiteProbe,
    SlashPairProbe,
    UrlProbe,
    host_form,
)

ROOT = "https://example.com/"


def assert_db_valid(outcome: CheckOutcome) -> None:
    """Mirror of analysis_result_status_score_valid + status_valid."""
    assert outcome.status in ("pass", "warn", "fail", "n_a")
    if outcome.status in ("pass", "warn", "fail"):
        assert outcome.score is not None and 1 <= outcome.score <= 100
    else:
        assert outcome.score is None
    assert outcome.reasoning


def assert_missing_evidence(outcome: CheckOutcome) -> None:
    """An n_a for missing evidence carries the one-click fix, not a lecture."""
    assert outcome.status == "n_a"
    assert outcome.score is None
    assert outcome.remediation is not None, "no dead ends — n_a must bind an action"
    lowered = outcome.reasoning.lower()
    for forbidden in ("run the", "command", "endpoint", "re-run"):
        assert forbidden not in lowered, (
            f"reasoning tells the user to run something: {outcome.reasoning}"
        )


def robots(
    content: str | None, status: int | None = 200, error: str | None = None
) -> RobotsCapture:
    return RobotsCapture(
        url="https://example.com/robots.txt",
        http_status=status,
        content=content,
        fetch_error=error,
    )


def probe(
    *,
    robots_capture: RobotsCapture | None = None,
    variants: list[UrlProbe] | None = None,
    sitemap_locations: list[UrlProbe] | None = None,
    slash_pairs: list[SlashPairProbe] | None = None,
) -> SiteProbe:
    return SiteProbe(
        captured_at="2026-08-09T00:00:00+00:00",
        root_url=ROOT,
        robots=robots_capture,
        variants=variants or [],
        sitemap_locations=sitemap_locations or [],
        slash_pairs=slash_pairs or [],
    )


def slash_pair(path: str, *, duplicated: bool) -> SlashPairProbe:
    """A probed `<path>` / `<path>/` pair, either duplicated or consolidated."""
    bare_url = f"https://example.com{path}"
    slashed_url = f"{bare_url}/"
    if duplicated:
        return SlashPairProbe(path=path, bare=resolves(bare_url), slashed=resolves(slashed_url))
    # The slashed form hands over to the bare one — consolidation working.
    return SlashPairProbe(
        path=path, bare=resolves(bare_url), slashed=redirects_to(slashed_url, bare_url)
    )


def evidence(**overrides) -> SiteEvidence:
    base = dict(
        site_id="site-1",
        root_url=ROOT,
        canonical_host_form=host_form(ROOT),
    )
    base.update(overrides)
    return SiteEvidence(**base)


def resolves(url: str, status: int = 200) -> UrlProbe:
    """A variant that answers on its own — a second live copy of the site."""
    return UrlProbe(url=url, http_status=status, final_url=url, final_status=status)


def redirects_to(url: str, target: str, status: int = 301, hops: int = 1) -> UrlProbe:
    chain = [{"url": url, "status": status}]
    for _ in range(hops - 1):
        chain.append({"url": target, "status": 301})
    return UrlProbe(
        url=url,
        http_status=status,
        final_url=target,
        final_status=200,
        redirect_chain=chain,
    )


# ---------------------------------------------------------------------------
# robots_txt_health — weight 3.0, first-match-top-down


def test_robots_no_probe_is_missing_evidence_not_a_pass():
    assert_missing_evidence(_check_robots_txt_health(evidence()))


def test_robots_unanswered_fetch_is_missing_evidence():
    outcome = _check_robots_txt_health(
        evidence(probe=probe(robots_capture=robots(None, status=None, error="ConnectError: nope")))
    )
    assert_missing_evidence(outcome)
    assert "ConnectError" in outcome.reasoning


@pytest.mark.parametrize("status", [500, 502, 503])
def test_robots_5xx_floors_the_score(status):
    outcome = _check_robots_txt_health(
        evidence(probe=probe(robots_capture=robots(None, status=status)))
    )
    assert_db_valid(outcome)
    assert outcome.score == ROBOTS_SERVER_ERROR_SCORE
    assert outcome.status == "fail"


def test_robots_blanket_disallow_floors_the_score():
    outcome = _check_robots_txt_health(
        evidence(probe=probe(robots_capture=robots("User-agent: *\nDisallow: /\n")))
    )
    assert_db_valid(outcome)
    assert outcome.score == ROBOTS_BLANKET_DISALLOW_SCORE
    assert outcome.status == "fail"


def test_robots_blocking_advertised_urls_lands_mid_band():
    outcome = _check_robots_txt_health(
        evidence(
            probe=probe(robots_capture=robots("User-agent: *\nDisallow: /blog/\n")),
            indexable_missing_from_sitemap=["https://example.com/blog/post-1"],
        )
    )
    assert_db_valid(outcome)
    assert outcome.score == ROBOTS_BLOCKS_WANTED_URLS_SCORE
    assert outcome.issue_count == 1


def test_robots_blocking_ranks_above_syntax_errors():
    """First-match-top-down: the worse rule wins even when both apply."""
    outcome = _check_robots_txt_health(
        evidence(
            probe=probe(robots_capture=robots("User-agent: *\nDisallow: /blog/\nDissalow: /x\n")),
            indexable_missing_from_sitemap=["https://example.com/blog/post-1"],
        )
    )
    assert outcome.score == ROBOTS_BLOCKS_WANTED_URLS_SCORE


def test_robots_syntax_errors_land_mid_band():
    outcome = _check_robots_txt_health(
        evidence(probe=probe(robots_capture=robots("User-agent: *\nDissalow: /admin\n")))
    )
    assert_db_valid(outcome)
    assert outcome.score == ROBOTS_SYNTAX_ERROR_SCORE
    assert outcome.status == "warn"


def test_robots_404_is_informational_not_a_defect():
    outcome = _check_robots_txt_health(
        evidence(probe=probe(robots_capture=robots(None, status=404)))
    )
    assert_db_valid(outcome)
    assert outcome.score == ROBOTS_MISSING_SCORE


def test_robots_clean_file_passes():
    outcome = _check_robots_txt_health(
        evidence(
            probe=probe(
                robots_capture=robots(
                    "User-agent: *\nDisallow: /admin/\nSitemap: https://example.com/sitemap.xml\n"
                )
            ),
            indexable_missing_from_sitemap=["https://example.com/blog/post-1"],
        )
    )
    assert_db_valid(outcome)
    assert outcome.status == "pass"
    assert outcome.score == ROBOTS_CLEAN_SCORE


# ---------------------------------------------------------------------------
# sitemap_health — weight 2.0


def test_sitemap_health_never_looked_is_missing_evidence():
    assert_missing_evidence(_check_sitemap_health(evidence()))


def test_sitemap_health_found_but_unread_is_missing_evidence():
    outcome = _check_sitemap_health(
        evidence(probe=probe(sitemap_locations=[resolves("https://example.com/sitemap.xml")]))
    )
    assert_missing_evidence(outcome)


def test_sitemap_health_proven_absent_scores_the_missing_band():
    outcome = _check_sitemap_health(
        evidence(
            probe=probe(
                sitemap_locations=[
                    UrlProbe(
                        url="https://example.com/sitemap.xml", http_status=404, final_status=404
                    )
                ]
            )
        )
    )
    assert_db_valid(outcome)
    assert outcome.score == SITEMAP_NONE_FOUND_SCORE


def _doc(**overrides) -> SitemapDocFacts:
    base = dict(
        url="https://example.com/sitemap.xml",
        kind="urlset",
        status_code=200,
        fetch_error=None,
        url_count=10,
        is_active=True,
        last_fetched_at=None,
    )
    base.update(overrides)
    return SitemapDocFacts(**base)


def test_sitemap_health_unreachable_document_is_the_worst_band():
    outcome = _check_sitemap_health(
        evidence(
            sitemap_sync_ran=True,
            sitemaps=[_doc(status_code=503)],
            sitemap_entries_total=10,
        )
    )
    assert_db_valid(outcome)
    assert outcome.score == SITEMAP_UNREACHABLE_SCORE


def test_sitemap_health_fetch_error_counts_as_unreachable():
    outcome = _check_sitemap_health(
        evidence(
            sitemap_sync_ran=True,
            sitemaps=[_doc(status_code=200, fetch_error="XML is not well-formed")],
            sitemap_entries_total=10,
        )
    )
    assert outcome.score == SITEMAP_UNREACHABLE_SCORE


def test_sitemap_health_heavy_junk_band():
    outcome = _check_sitemap_health(
        evidence(
            sitemap_sync_ran=True,
            sitemaps=[_doc(url_count=100)],
            sitemap_entries_total=100,
            junk_by_class={"redirecting": [f"https://example.com/{i}" for i in range(11)]},
            junk_entry_count=11,
        )
    )
    assert_db_valid(outcome)
    assert outcome.score == SITEMAP_HEAVY_JUNK_SCORE
    assert outcome.issue_count == 11


def test_sitemap_health_light_junk_band():
    outcome = _check_sitemap_health(
        evidence(
            sitemap_sync_ran=True,
            sitemaps=[_doc(url_count=100)],
            sitemap_entries_total=100,
            junk_by_class={"noindexed": ["https://example.com/a"]},
            junk_entry_count=1,
        )
    )
    assert_db_valid(outcome)
    assert outcome.score == SITEMAP_LIGHT_JUNK_SCORE


def test_sitemap_health_ten_percent_is_still_the_light_band():
    """The contract's boundary is `>10%` heavy, `1-10%` light — exactly 10 is light."""
    outcome = _check_sitemap_health(
        evidence(
            sitemap_sync_ran=True,
            sitemaps=[_doc(url_count=100)],
            sitemap_entries_total=100,
            junk_by_class={"noindexed": [f"https://example.com/{i}" for i in range(10)]},
            junk_entry_count=10,
        )
    )
    assert outcome.score == SITEMAP_LIGHT_JUNK_SCORE


def test_sitemap_health_minor_issues_band():
    outcome = _check_sitemap_health(
        evidence(
            sitemap_sync_ran=True,
            sitemaps=[_doc(url_count=SITEMAP_MAX_URLS_PER_DOC + 1)],
            sitemap_entries_total=100,
            entries_missing_lastmod=100,
        )
    )
    assert_db_valid(outcome)
    assert outcome.score == SITEMAP_MINOR_ISSUE_SCORE
    assert outcome.status == "pass"


def test_sitemap_health_clean_sitemap_passes():
    outcome = _check_sitemap_health(
        evidence(
            sitemap_sync_ran=True,
            sitemaps=[_doc()],
            sitemap_entries_total=10,
        )
    )
    assert_db_valid(outcome)
    assert outcome.score == SITEMAP_CLEAN_SCORE
    assert outcome.status == "pass"


def test_sitemap_health_empty_sitemap_is_not_clean():
    outcome = _check_sitemap_health(
        evidence(sitemap_sync_ran=True, sitemaps=[_doc(url_count=0)], sitemap_entries_total=0)
    )
    assert_db_valid(outcome)
    assert outcome.score == SITEMAP_NONE_FOUND_SCORE


# ---------------------------------------------------------------------------
# sitemap_coverage — weight 1.5, the row's formula verbatim


def test_coverage_never_synced_is_missing_evidence():
    assert_missing_evidence(_check_sitemap_coverage(evidence()))


def test_coverage_with_no_sitemap_at_all_is_scored_not_skipped():
    outcome = _check_sitemap_coverage(
        evidence(
            probe=probe(
                sitemap_locations=[
                    UrlProbe(
                        url="https://example.com/sitemap.xml", http_status=404, final_status=404
                    )
                ]
            ),
            indexable_total=40,
        )
    )
    assert_db_valid(outcome)
    assert outcome.status == "fail"


def test_coverage_no_indexable_pages_is_missing_evidence():
    assert_missing_evidence(
        _check_sitemap_coverage(evidence(sitemap_sync_ran=True, indexable_total=0))
    )


def test_coverage_truncated_census_refuses_to_score():
    assert_missing_evidence(
        _check_sitemap_coverage(
            evidence(sitemap_sync_ran=True, indexable_total=10, pages_truncated=True)
        )
    )


def test_coverage_full_coverage_passes():
    outcome = _check_sitemap_coverage(
        evidence(
            sitemap_sync_ran=True,
            indexable_total=50,
            indexable_in_sitemap=50,
            sitemap_entries_total=50,
        )
    )
    assert_db_valid(outcome)
    assert outcome.score == 100
    assert outcome.status == "pass"
    assert outcome.score >= COVERAGE_HEALTHY_MIN_SCORE


def test_coverage_formula_matches_the_catalogue_row():
    """score = round(100 * covered/total) - min(20, 2*orphan_pct)."""
    outcome = _check_sitemap_coverage(
        evidence(
            sitemap_sync_ran=True,
            indexable_total=100,
            indexable_in_sitemap=90,
            sitemap_entries_total=100,
            undiscovered_count=5,
            undiscovered_urls=[f"https://example.com/ghost-{i}" for i in range(5)],
        )
    )
    assert_db_valid(outcome)
    # 90% coverage, 5% orphan → 90 - min(20, 10) = 80
    assert outcome.score == 80
    assert outcome.status == "warn"
    assert outcome.issue_count == 15


def test_coverage_orphan_penalty_is_capped():
    outcome = _check_sitemap_coverage(
        evidence(
            sitemap_sync_ran=True,
            indexable_total=100,
            indexable_in_sitemap=100,
            sitemap_entries_total=100,
            undiscovered_count=100,
            undiscovered_urls=["https://example.com/ghost"],
        )
    )
    # 100% coverage, 100% orphan → 100 - min(20, 200) = 80
    assert outcome.score == 80


def test_coverage_bad_coverage_fails():
    outcome = _check_sitemap_coverage(
        evidence(
            sitemap_sync_ran=True,
            indexable_total=100,
            indexable_in_sitemap=40,
            sitemap_entries_total=40,
        )
    )
    assert_db_valid(outcome)
    assert outcome.score == 40
    assert outcome.status == "fail"


# ---------------------------------------------------------------------------
# host_protocol_consistency — weight 1.5, category url_architecture


def test_host_no_probe_is_missing_evidence():
    assert_missing_evidence(_check_host_protocol_consistency(evidence()))


def test_host_nothing_answered_is_missing_evidence():
    assert_missing_evidence(
        _check_host_protocol_consistency(
            evidence(
                probe=probe(
                    variants=[
                        UrlProbe(url="https://example.com/", fetch_error="ConnectTimeout"),
                        UrlProbe(url="http://example.com/", fetch_error="ConnectTimeout"),
                    ]
                )
            )
        )
    )


def test_host_two_live_variants_is_the_worst_band():
    outcome = _check_host_protocol_consistency(
        evidence(
            probe=probe(
                variants=[
                    resolves("https://example.com/"),
                    resolves("https://www.example.com/"),
                ]
            )
        )
    )
    assert_db_valid(outcome)
    assert outcome.score == HOST_MULTIPLE_LIVE_SCORE
    assert outcome.status == "fail"


def test_host_temporary_redirect_lands_in_the_soft_band():
    outcome = _check_host_protocol_consistency(
        evidence(
            probe=probe(
                variants=[
                    resolves("https://example.com/"),
                    redirects_to("https://www.example.com/", "https://example.com/", status=302),
                ]
            )
        )
    )
    assert_db_valid(outcome)
    assert outcome.score == HOST_SOFT_REDIRECT_SCORE


def test_host_redirect_chain_lands_in_the_soft_band():
    outcome = _check_host_protocol_consistency(
        evidence(
            probe=probe(
                variants=[
                    resolves("https://example.com/"),
                    redirects_to(
                        "http://www.example.com/", "https://example.com/", status=301, hops=2
                    ),
                ]
            )
        )
    )
    assert outcome.score == HOST_SOFT_REDIRECT_SCORE


def test_host_trailing_slash_duplicate_is_scored_the_third_family():
    """The band the row's description always named and nothing measured."""
    outcome = _check_host_protocol_consistency(
        evidence(
            probe=probe(
                variants=[
                    resolves("https://example.com/"),
                    redirects_to("https://www.example.com/", "https://example.com/"),
                ],
                slash_pairs=[
                    slash_pair("/about", duplicated=True),
                    slash_pair("/contact", duplicated=False),
                ],
            ),
            internal_link_host_forms={"https://example.com"},
        )
    )
    assert_db_valid(outcome)
    assert outcome.score == HOST_SLASH_DUPLICATE_SCORE
    assert outcome.issue_count == 1
    assert "/about" in outcome.reasoning
    assert outcome.evidence["paths_checked"] == 2


def test_host_slash_pair_that_consolidates_is_not_a_duplicate():
    outcome = _check_host_protocol_consistency(
        evidence(
            probe=probe(
                variants=[resolves("https://example.com/")],
                slash_pairs=[slash_pair("/about", duplicated=False)],
            ),
            internal_link_host_forms={"https://example.com"},
        )
    )
    assert outcome.score == HOST_CONSISTENT_SCORE
    assert outcome.evidence["slash_pairs_checked"] == 1


def test_host_slash_pair_that_never_answered_scores_nothing():
    """An unreachable pair is missing evidence, never a duplicate verdict."""
    dead = SlashPairProbe(
        path="/about",
        bare=UrlProbe(url="https://example.com/about", fetch_error="ConnectTimeout"),
        slashed=UrlProbe(url="https://example.com/about/", fetch_error="ConnectTimeout"),
    )
    outcome = _check_host_protocol_consistency(
        evidence(
            probe=probe(variants=[resolves("https://example.com/")], slash_pairs=[dead]),
            internal_link_host_forms={"https://example.com"},
        )
    )
    assert outcome.score == HOST_CONSISTENT_SCORE
    assert outcome.evidence["slash_pairs_checked"] == 0


def test_host_live_variant_still_outranks_a_slash_duplicate():
    """First-match-top-down: the whole-site duplicate is the worse fact."""
    outcome = _check_host_protocol_consistency(
        evidence(
            probe=probe(
                variants=[
                    resolves("https://example.com/"),
                    resolves("https://www.example.com/"),
                ],
                slash_pairs=[slash_pair("/about", duplicated=True)],
            )
        )
    )
    assert outcome.score == HOST_MULTIPLE_LIVE_SCORE


def test_host_mixed_internal_links_despite_clean_redirects():
    outcome = _check_host_protocol_consistency(
        evidence(
            probe=probe(
                variants=[
                    resolves("https://example.com/"),
                    redirects_to("https://www.example.com/", "https://example.com/"),
                ]
            ),
            internal_link_host_forms={"https://example.com", "https://www.example.com"},
        )
    )
    assert_db_valid(outcome)
    assert outcome.score == HOST_MIXED_INTERNAL_LINKS_SCORE
    assert outcome.status == "warn"


def test_host_single_form_with_clean_301s_passes():
    outcome = _check_host_protocol_consistency(
        evidence(
            probe=probe(
                variants=[
                    resolves("https://example.com/"),
                    redirects_to("https://www.example.com/", "https://example.com/"),
                    redirects_to("http://example.com/", "https://example.com/", status=308),
                ]
            ),
            internal_link_host_forms={"https://example.com"},
        )
    )
    assert_db_valid(outcome)
    assert outcome.score == HOST_CONSISTENT_SCORE
    assert outcome.status == "pass"


def test_host_truncated_link_scan_is_disclosed_in_the_pass():
    outcome = _check_host_protocol_consistency(
        evidence(
            probe=probe(variants=[resolves("https://example.com/")]),
            internal_link_host_forms={"https://example.com"},
            host_form_scan_truncated=True,
        )
    )
    assert outcome.status == "pass"
    assert "internal links checked up to" in outcome.reasoning


# ---------------------------------------------------------------------------
# Contract-wide


@pytest.mark.parametrize("key", sorted(CRAWLABILITY_SITE_CHECKS))
def test_every_site_check_answers_na_on_empty_evidence(key):
    """No evidence at all → n_a with a one-click fix. Never a silent pass."""
    outcome = CRAWLABILITY_SITE_CHECKS[key](evidence())
    assert_db_valid(outcome)
    assert_missing_evidence(outcome)


@pytest.mark.parametrize("key", sorted(CRAWLABILITY_SITE_CHECKS))
def test_every_site_check_is_db_valid_on_a_healthy_site(key):
    healthy = evidence(
        probe=probe(
            robots_capture=robots(
                "User-agent: *\nDisallow: /admin/\nSitemap: https://example.com/sitemap.xml\n"
            ),
            variants=[
                resolves("https://example.com/"),
                redirects_to("https://www.example.com/", "https://example.com/"),
            ],
            sitemap_locations=[resolves("https://example.com/sitemap.xml")],
        ),
        sitemap_sync_ran=True,
        sitemaps=[_doc()],
        sitemap_entries_total=10,
        sitemap_page_ids={f"p{i}" for i in range(10)},
        indexable_total=10,
        indexable_in_sitemap=10,
        internal_link_host_forms={"https://example.com"},
    )
    outcome = CRAWLABILITY_SITE_CHECKS[key](healthy)
    assert_db_valid(outcome)
    assert outcome.status == "pass", f"{key} flagged a healthy site: {outcome.reasoning}"
