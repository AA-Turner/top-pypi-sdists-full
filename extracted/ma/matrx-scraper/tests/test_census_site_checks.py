"""Census 2026-10-14 fixes for the site/cross-page checks: each test fails on the old behavior."""

from __future__ import annotations

import asyncio
from datetime import UTC, date, datetime, timedelta

import httpx
import pytest

from matrx_scraper import audit_metrics, sitemaps
from matrx_scraper.seo_audit import CheckOutcome
from matrx_scraper.web_crawl import analysis as A
from matrx_scraper.web_crawl import link_check
from matrx_scraper.web_crawl import site_analysis as S
from matrx_scraper.web_crawl.site_probe import RobotsCapture, SiteProbe, UrlProbe, host_form

ROOT = "https://example.com/"


def valid(o: CheckOutcome) -> CheckOutcome:
    assert o.status in ("pass", "warn", "fail", "n_a")
    if o.status == "n_a":
        assert o.score is None
    else:
        assert o.score is not None and 1 <= o.score <= 100
    assert o.reasoning
    return o


def facts(**kw) -> A.PageFacts:
    base = dict(
        page_id="p1", url="https://example.com/a", title="T", meta_robots="noindex",
        noindex=True, nofollow=False, http_status=200, latest_snapshot_id="s1",
        head_captured=True, canonical_url="https://example.com/a", canonical_matches=True,
    )
    base.update(kw)
    return A.PageFacts(**base)


def site(f: A.PageFacts, **kw) -> A.SiteAggregates:
    s = A.SiteAggregates()
    s.internal_edges_resolved = 20
    s.homepage_page_id = "home"
    s.orphans = A.OrphanCensus(complete=True, known_live_pages=10, captured_pages=10)
    s.sitemap_page_ids = set()
    for k, v in kw.items():
        setattr(s, k, v)
    return s


# 1 -------------------------------------------------------------------------
class _FakeHttp:
    def __init__(self, head: int, get: int) -> None:
        self.head_status, self.get_status = head, get

    async def head(self, url):
        return httpx.Response(self.head_status)

    def stream(self, method, url):
        status = self.get_status

        class Ctx:
            async def __aenter__(self_inner):
                return httpx.Response(status)

            async def __aexit__(self_inner, *a):
                return False

        return Ctx()


@pytest.mark.parametrize(
    "head,get,expected",
    [(404, 200, 200), (404, 404, 404), (410, 200, 200), (429, 200, 200), (503, 200, 200), (404, 403, 403)],
)
def test_head_404_is_confirmed_with_get(head, get, expected):
    checker = link_check._PoliteChecker(_FakeHttp(head, get), 1, 0)
    assert asyncio.run(checker._request("https://zenoti.example/x")) == expected


# 2 -------------------------------------------------------------------------
def _robots_check(f, s):
    return A.PAGE_CHECKS["meta_robots_conflicts"](f, s)


def test_noindex_in_sitemap_is_the_failure():
    f = facts()
    o = valid(_robots_check(f, site(f, sitemap_page_ids={"p1"})))
    assert o.status == "fail" and o.score == 10 and "sitemap" in o.reasoning


def test_noindex_with_five_inlinks_is_the_failure():
    f = facts()
    o = valid(_robots_check(f, site(f, inlinks={"p1": {"a", "b", "c", "d", "e"}})))
    assert o.status == "fail" and o.score == 10


def test_unpromoted_noindex_is_deliberate():
    f = facts()
    o = valid(_robots_check(f, site(f, inlinks={"p1": {"a"}})))
    assert o.status == "pass" and o.score == 85


def test_noindex_promotion_unknown_keeps_the_failure():
    f = facts()
    s = site(f, sitemap_page_ids=None)
    assert _robots_check(f, s).status == "fail"


# 3 -------------------------------------------------------------------------
def _edge(target, anchor, source="p1"):
    return {
        "target_url": target, "http_status": 200, "is_internal": True, "rel": None,
        "anchor_text": anchor, "source_page_id": source,
    }


def _graph():
    class G:
        canonical_by_page = {"p1": "p1"}
        canonical_by_hash: dict = {}

    return G()


def _anchor_outcome(edges):
    f = facts(noindex=False)
    s = site(f)
    stats = A.PageLinkStats()
    for e in edges:
        A._accumulate_edge(e, stats, _graph(), s, {})
    s.link_stats["p1"] = stats
    return valid(A._check_anchor_text_descriptiveness(f, s))


def test_target_with_a_descriptive_twin_is_fine():
    o = _anchor_outcome([_edge("https://example.com/", ""), _edge("https://example.com/", "Home"),
                         _edge("https://example.com/x", "Our pricing plans")])
    assert o.status == "pass" and o.score == 100


def test_media_links_are_not_judged():
    o = _anchor_outcome([_edge("https://example.com/wp-content/uploads/a.jpg", ""),
                         _edge("https://example.com/y", "Our pricing plans")])
    assert o.score == 100


def test_self_links_are_not_judged():
    f = facts(noindex=False)
    s = site(f)
    g = _graph()
    from matrx_scraper.crawler import _normalise_url
    from matrx_scraper.web_crawl.persistence import url_hash

    g.canonical_by_hash = {url_hash(_normalise_url("https://example.com/a")): "p1"}
    stats = A.PageLinkStats()
    A._accumulate_edge(_edge("https://example.com/a", "read more"), stats, g, s, {})
    s.link_stats["p1"] = stats
    assert A._check_anchor_text_descriptiveness(f, s).score == 100


def test_generic_only_target_still_fails():
    o = _anchor_outcome([_edge(f"https://example.com/p{i}", "read more") for i in range(4)])
    assert o.status in ("warn", "fail") and o.score < 85


# 4 -------------------------------------------------------------------------
def _outlinks(url, total):
    f = facts(url=url, noindex=False)
    s = site(f)
    s.link_stats["p1"] = A.PageLinkStats(outlinks_total=total, internal_outlinks=total)
    return valid(A._check_excessive_outlinks(f, s))


def test_outlinks_at_parser_cap_is_n_a_at_least():
    o = _outlinks("https://example.com/a", A.ANCHOR_RECORD_LIMIT)
    assert o.status == "n_a" and "at least" in o.reasoning


def test_html_sitemap_page_is_not_judged():
    assert _outlinks("https://example.com/sitemap", 400).status == "n_a"
    assert _outlinks("https://example.com/a", 400).status == "warn"


# 5 -------------------------------------------------------------------------
def test_link_equity_needs_thirty_pages():
    f = facts(noindex=False, link_score=0.1, target_keyword="kw")
    s = site(f, link_equity_percentile_by_page={f"p{i}": 50 for i in range(4)})
    s.link_equity_percentile_by_page["p1"] = 50
    assert valid(A._check_internal_link_equity(f, s)).status == "n_a"
    s.link_equity_percentile_by_page = {f"p{i}": 50 for i in range(40)} | {"p1": 50}
    assert A._check_internal_link_equity(f, s).status in ("warn", "fail")


# 6 -------------------------------------------------------------------------
def test_coverage_and_orphans_wait_for_a_complete_crawl():
    f = facts(noindex=False)
    s = site(f, inlinks={"p1": {"a"}})
    s.orphans = A.OrphanCensus(complete=False, known_live_pages=10, captured_pages=10)
    assert A._check_internal_inlink_coverage(f, s).status == "n_a"
    assert A._check_orphan_pages(f, s).status == "n_a"


def test_orphan_not_stood_for_a_page_that_now_404s_or_redirects():
    f = facts(noindex=False, http_status=404)
    assert valid(A._check_orphan_pages(f, site(f))).status == "n_a"
    f = facts(noindex=False, http_status=301)
    assert A._check_orphan_pages(f, site(f)).status == "n_a"


def test_orphan_score_is_not_the_site_score():
    f = facts(noindex=False)
    s = site(f)
    s.orphans = A.OrphanCensus(complete=True, known_live_pages=300, captured_pages=300,
                               crawled_orphan_ids={"p1"})
    o = valid(A._check_orphan_pages(f, s))
    assert o.status == "fail" and o.score == A.ORPHAN_PAGE_SCORE != s.orphans.site_score()


# 7 -------------------------------------------------------------------------
def _dup(n):
    f = facts(title="Same", noindex=False)
    s = A.SiteAggregates()
    s.pages_by_title = {"same": [f] + [facts(page_id=f"o{i}", title="Same") for i in range(n)]}
    return valid(A._check_title_duplication(f, s))


@pytest.mark.parametrize("n,score", [(1, 65), (2, 45), (9, 45), (10, 25)])
def test_title_duplication_contract_scores(n, score):
    assert _dup(n).score == score


# 8 -------------------------------------------------------------------------
def _gsc(position, impressions, clicks, latest=None):
    f = facts(noindex=False)
    s = site(f)
    latest = latest or datetime.now(UTC).date() - timedelta(days=3)
    s.gsc = A.SiteGscEvidence(bound=True, earliest_date=latest - timedelta(days=60), latest_date=latest)
    s.gsc.by_page["p1"] = A.PageGscStats(current=A.GscPeriod(clicks=clicks, impressions=impressions, position=position))
    return valid(A._check_gsc_ctr_opportunity(f, s))


def test_ctr_opens_on_page_one_with_real_missed_clicks():
    o = _gsc(3.0, 2000, 10)
    assert o.status in ("warn", "fail")


def test_ctr_page_two_is_not_a_snippet_problem():
    o = _gsc(25.0, 3000, 3)
    assert o.status == "n_a" and "earned" not in o.reasoning


def test_ctr_needs_ten_missed_clicks():
    assert _gsc(2.0, 120, 14).status == "n_a"


def test_ctr_stale_data_is_n_a_naming_the_date():
    old = datetime.now(UTC).date() - timedelta(days=60)
    o = _gsc(3.0, 2000, 10, latest=old)
    assert o.status == "n_a" and f"{old:%-d %b %Y}" in o.reasoning


# 9 -------------------------------------------------------------------------
def test_cannibalization_names_urls_and_the_winner():
    from matrx_scraper.web_crawl.gsc_cannibalization import (
        CannibalPage, CannibalQuery, GscCannibalizationEvidence,
    )

    ev = GscCannibalizationEvidence(
        available=True, latest_date=date(2026, 10, 1), significant_queries=2, cannibalized_queries=1,
        samples=[CannibalQuery("kw", 900, (CannibalPage("a", 500, 0.55), CannibalPage("b", 400, 0.45)))],
    )
    sf = A.SiteFacts(site_id="s", gsc_cannibalization=ev, page_urls={"a": "https://x.com/a", "b": "https://x.com/b"})
    o = valid(A._site_check_gsc_keyword_cannibalization(sf))
    pages = o.evidence["samples"][0]["pages"]
    assert pages[0]["url"] == "https://x.com/a"
    assert "https://x.com/a leads" in o.reasoning and "301" in o.reasoning


# 10 ------------------------------------------------------------------------
def _ev(**kw):
    base = dict(site_id="s", root_url=ROOT, canonical_host_form=host_form(ROOT))
    base.update(kw)
    return S.SiteEvidence(**base)


class _Page:
    def __init__(self, i, status):
        self.id = i
        self.url = f"https://example.com/{i}"
        self.canonical_page_id = None
        self.http_status_last = status
        self.latest_snapshot_id = "s"
        self.metadata = {}


def test_walls_and_5xx_sitemap_entries_are_not_dead():
    ev = _ev(sitemap_sync_ran=True)
    pages = [_Page("a", 429), _Page("b", 405), _Page("c", 522), _Page("d", 200)]
    S.fold_sitemap_members(ev, member_page_ids={"a", "b", "c", "d"}, pages_with_lastmod={"a", "b", "c", "d"},
                           member_pages=pages, facts_by_page={})
    assert ev.junk_entry_count == 0 and ev.unverifiable_count == 3
    ev.sitemaps = [S.SitemapDocFacts("https://example.com/sitemap.xml", "urlset", 200, None, 4, True, None)]
    o = valid(S._check_sitemap_health(ev))
    assert o.status == "pass" and "could not check" in o.reasoning


def test_a_real_404_entry_is_still_dead():
    ev = _ev(sitemap_sync_ran=True)
    S.fold_sitemap_members(ev, member_page_ids={"a"}, pages_with_lastmod={"a"},
                           member_pages=[_Page("a", 404)], facts_by_page={})
    assert ev.junk_entry_count == 1


def test_transient_sitemap_file_failure_is_not_unreadable():
    for kw in (dict(status_code=526, fetch_error="HTTP 526"), dict(status_code=None, fetch_error="ReadTimeout: x"),
               dict(status_code=403, fetch_error="HTTP 403")):
        ev = _ev(sitemap_sync_ran=True, sitemap_entries_total=10)
        ev.sitemaps = [S.SitemapDocFacts("https://example.com/sitemap.xml", "unknown", url_count=0,
                                         is_active=True, last_fetched_at=None, **kw)]
        assert valid(S._check_sitemap_health(ev)).score != S.SITEMAP_UNREACHABLE_SCORE


def test_guessed_html_sitemap_path_is_never_judged():
    ev = _ev(sitemap_sync_ran=True, sitemap_entries_total=10)
    ev.sitemaps = [S.SitemapDocFacts("https://example.com/sitemap_index.xml", "unknown", 200,
                                     "ValueError: malformed sitemap XML: mismatched tag", 0, True, None)]
    assert S._check_sitemap_health(ev).score != S.SITEMAP_UNREACHABLE_SCORE


def test_rss_and_atom_sitemaps_parse():
    rss = b"<rss><channel><item><link>https://x.com/a</link></item><item><link>https://x.com/b</link></item></channel></rss>"
    assert [e.loc for e in sitemaps.parse_sitemap_document(rss).entries] == ["https://x.com/a", "https://x.com/b"]
    atom = b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><link href="https://x.com/c"/></entry></feed>'
    assert sitemaps.parse_sitemap_document(atom).entries[0].loc == "https://x.com/c"


def test_html_body_is_detected_for_guessed_paths():
    assert sitemaps.looks_like_html(b"<!DOCTYPE html><html>", "text/html")
    assert not sitemaps.looks_like_html(b"<?xml version='1.0'?><urlset/>", "text/xml")


# 11 ------------------------------------------------------------------------
def test_coverage_is_n_a_when_crawl_incomplete():
    ev = _ev(sitemap_sync_ran=True, crawl_complete=False, indexable_total=1, indexable_in_sitemap=0,
             sitemap_entries_total=12000, undiscovered_count=12000)
    assert valid(S._check_sitemap_coverage(ev)).status == "n_a"


def test_noindex_pages_are_not_missing_from_the_sitemap():
    noindexed = facts(noindex=None, meta_robots="noindex, follow")
    ev = _ev(sitemap_sync_ran=True)
    S._load_coverage(ev, {"p1": noindexed})
    assert ev.indexable_total == 0


# 12 ------------------------------------------------------------------------
def _chain(url, target, status, hops):
    chain = [{"url": url, "status": status}] + [{"url": target, "status": 301}] * (hops - 1)
    return UrlProbe(url=url, http_status=status, final_url=target, final_status=200, redirect_chain=chain)


def _host_probe(*variants):
    return SiteProbe(captured_at="2026-08-09T00:00:00+00:00", root_url=ROOT, variants=list(variants),
                     sitemap_locations=[], slash_pairs=[])


def test_variants_redirecting_to_the_real_host_are_consolidated():
    www = "https://www.example.com/"
    ev = _ev(root_url=ROOT, canonical_host_form="https://example.com", probe=_host_probe(
        UrlProbe(url=ROOT, http_status=200, final_url=ROOT, final_status=200),
        _chain("http://example.com/", www, 308, 1), _chain("http://www.example.com/", www, 308, 1)))
    o = valid(S._check_host_protocol_consistency(ev))
    assert o.score != S.HOST_MULTIPLE_LIVE_SCORE


def test_two_hop_301_is_clean_and_three_hops_fire_with_honest_text():
    main = UrlProbe(url=ROOT, http_status=200, final_url=ROOT, final_status=200)
    ev = _ev(probe=_host_probe(main, _chain("http://www.example.com/", ROOT, 301, 2)))
    assert S._check_host_protocol_consistency(ev).score == S.HOST_CONSISTENT_SCORE
    ev = _ev(probe=_host_probe(main, _chain("http://www.example.com/", ROOT, 301, 3)))
    o = S._check_host_protocol_consistency(ev)
    assert o.score == S.HOST_SOFT_REDIRECT_SCORE and "temporary" not in o.reasoning and "3 redirect hops" in o.reasoning
    ev = _ev(probe=_host_probe(main, _chain("http://www.example.com/", ROOT, 302, 1)))
    assert "temporary 302" in S._check_host_protocol_consistency(ev).reasoning


# 13 ------------------------------------------------------------------------
def test_canonical_matching_requested_url_or_hop_is_self():
    right = audit_metrics.evaluate_indexability(200, None, "https://x.com/blog/", [], "https://x.com/blog/page/7?et", "https://x.com/blog/")
    assert right["ok"] and "Canonical points elsewhere" not in str(right["issues"])
    hop = audit_metrics.evaluate_indexability(
        200, None, "https://x.com/blog/", [{"url": "https://x.com/blog", "status": 301}, {"url": "https://x.com/blog/"}],
        "https://x.com/garbage")
    assert "Canonical points elsewhere" not in str(hop["issues"])
    wrong = audit_metrics.evaluate_indexability(200, None, "https://x.com/other", [], "https://x.com/a", "https://x.com/a")
    assert "Canonical points elsewhere" in str(wrong["issues"])


# 14 ------------------------------------------------------------------------
def test_html_robots_txt_is_said_plainly_without_dumping_html():
    html = "<!doctype html>\n<!--[if lt IE 7 ]> <html class='ie6'> <![endif]-->\n<html><head><title>x</title></head></html>"
    cap = RobotsCapture(url="https://example.com/robots.txt", http_status=200, content=html)
    ev = _ev(probe=SiteProbe(captured_at="2026-08-09T00:00:00+00:00", root_url=ROOT, robots=cap))
    o = valid(S._check_robots_txt_health(ev))
    assert "web page, not a rules file" in o.reasoning
    assert "syntax_errors" not in (o.evidence or {}) and "<!--" not in o.reasoning


# 15 ------------------------------------------------------------------------
def test_csp_only_missing_is_not_a_finding():
    full = {"x-frame-options": "DENY", "x-content-type-options": "nosniff", "referrer-policy": "no-referrer"}
    sf = A.SiteFacts(site_id="s", header_samples=[("https://x.com/", full)])
    o = valid(A._site_check_security_headers(sf))
    assert o.status == "pass"
    sf = A.SiteFacts(site_id="s", header_samples=[("https://x.com/", {})])
    assert A._site_check_security_headers(sf).status == "warn"
