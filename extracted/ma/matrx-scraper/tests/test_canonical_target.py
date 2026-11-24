"""A same-site canonical naming another URL is judged by its TARGET
(canonical_conflicts.score_contract). 2026-10-30: 2,837 High findings on 34
sites were `?sort=` / `?add-to-cart=` / `/collections/x/products/y` variants
correctly naming their clean address."""

from __future__ import annotations

from matrx_scraper.seo_audit import normalized_url_key
from matrx_scraper.web_crawl.analysis import PAGE_CHECKS, PageFacts, SiteAggregates

CLEAN = "https://shop.example/products/mug"
VARIANT = "https://shop.example/collections/cups/products/mug"


def _variant() -> PageFacts:
    return PageFacts(
        url=VARIANT, page_id="pv", http_status=200, head_captured=True,
        canonical_url=CLEAN, canonical_matches=False,
    )


def _site(target: PageFacts | None = None, sitemap: set[str] | None = None) -> SiteAggregates:
    site = SiteAggregates()
    site.sitemap_page_ids = sitemap if sitemap is not None else set()
    if target is not None:
        site.facts_by_url[normalized_url_key(target.url)] = target
    return site


def _run(site):
    return PAGE_CHECKS["canonical_conflicts"](_variant(), site)


def _target(**kw) -> PageFacts:
    base = dict(url=CLEAN, page_id="pc", http_status=200, head_captured=True,
                canonical_url=CLEAN, canonical_matches=True)
    base.update(kw)
    return PageFacts(**base)


def test_a_variant_naming_its_working_clean_page_is_no_conflict():
    o = _run(_site(_target()))
    assert o.status == "pass" and o.score == 100
    assert "Nothing to fix" in o.reasoning


def test_an_uncrawled_target_is_still_no_conflict():
    o = _run(_site(None))
    assert o.status == "pass" and "not crawled yet" in o.reasoning


def test_a_broken_target_fails_at_10():
    o = _run(_site(_target(http_status=404)))
    assert o.status == "fail" and o.score == 10


def test_a_noindexed_target_fails_at_10():
    o = _run(_site(_target(noindex=True)))
    assert o.score == 10


def test_a_redirecting_target_fails_at_30():
    o = _run(_site(_target(redirect_chain=[{"url": CLEAN, "status": 301}])))
    assert o.score == 30


def test_a_chained_canonical_fails_at_30():
    o = _run(_site(_target(canonical_url="https://shop.example/other", canonical_matches=False)))
    assert o.score == 30


def test_a_variant_the_sitemap_lists_contradicts_the_sitemap():
    o = _run(_site(_target(), sitemap={"pv"}))
    assert o.status == "warn" and o.score == 55 and "sitemap" in o.reasoning
