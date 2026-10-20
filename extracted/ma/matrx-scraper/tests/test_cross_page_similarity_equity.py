"""Focused contract tests for deterministic cross-page catalog checks."""

from matrx_scraper.web_crawl.analysis import (
    CROSS_PAGE_CHECKS,
    PageFacts,
    SiteAggregates,
    _check_internal_link_equity,
    index_page_facts,
)


def _page(
    number: int,
    score: float | None,
    *,
    target_keyword: str | None = None,
) -> PageFacts:
    return PageFacts(
        page_id=f"p{number}",
        url=f"https://example.com/{number}",
        link_score=score,
        target_keyword=target_keyword,
    )


# Rule: internal_link_equity is n_a below LINK_EQUITY_MIN_PAGES (30) scored pages,
# so every ranking fixture below carries at least 30 scored pages.
_MIN_PAGES = 30


def test_internal_link_equity_uses_inclusive_site_percentiles() -> None:
    # 30-page site (min-pages rule), scores 1..30 -> percentile = score/30.
    # Prioritized pages are the only ones judged by rank (the catalog
    # contract). Unprioritized pages never open a finding — see the test below.
    pages = [
        _page(n, n, target_keyword="kw" if n in (3, 15, 30) else None)
        for n in range(1, _MIN_PAGES + 1)
    ]
    site = SiteAggregates()

    index_page_facts(pages, site)

    pct = site.link_equity_percentile_by_page
    assert len(pct) == _MIN_PAGES
    assert pct["p3"] == 10
    assert pct["p15"] == 50
    assert pct["p30"] == 100
    assert _check_internal_link_equity(pages[2], site).status == "fail"
    assert _check_internal_link_equity(pages[14], site).status == "warn"
    assert _check_internal_link_equity(pages[29], site).status == "pass"


def test_internal_link_equity_ties_share_one_rank_and_top_ties_are_healthy() -> None:
    # Two low ties, two mid ties, 26 neutral top-scored pages (min-pages rule).
    pages = [_page(1, 5), _page(2, 5), _page(3, 10), _page(4, 10)]
    pages += [_page(n, 20) for n in range(5, _MIN_PAGES + 1)]
    site = SiteAggregates()

    index_page_facts(pages, site)

    pct = site.link_equity_percentile_by_page
    assert pct["p1"] == pct["p2"] == round(100 * 2 / _MIN_PAGES)
    assert pct["p3"] == pct["p4"] == round(100 * 4 / _MIN_PAGES)
    assert pct["p5"] == pct["p30"] == 100


def test_internal_link_equity_applies_published_priority_penalty() -> None:
    # 30 pages (min-pages rule); scores 1..30; page 6 sits at the 20th percentile.
    pages = [
        _page(i, float(i), target_keyword="commercial phrase" if i == 6 else None)
        for i in range(1, _MIN_PAGES + 1)
    ]
    site = SiteAggregates()
    index_page_facts(pages, site)

    outcome = _check_internal_link_equity(pages[5], site)

    assert outcome.status == "fail"
    assert outcome.score == 20
    assert outcome.issue_count == 1
    assert outcome.evidence["prioritized"] is True
    assert outcome.evidence["priority_penalty_applied"] is True
    assert "commercial phrase" in outcome.reasoning


def test_internal_link_equity_below_min_pages_is_na() -> None:
    pages = [_page(n, n, target_keyword="kw") for n in (1, 2, 3, 4)]
    site = SiteAggregates()
    index_page_facts(pages, site)

    outcome = _check_internal_link_equity(pages[0], site)

    assert outcome.status == "n_a"
    assert outcome.score is None


def test_internal_link_equity_missing_score_is_honest_na() -> None:
    missing = _page(1, None)
    site = SiteAggregates()
    index_page_facts([missing, _page(2, 10)], site)

    outcome = _check_internal_link_equity(missing, site)

    assert outcome.status == "n_a"
    assert outcome.score is None
    assert outcome.remediation is not None


def test_internal_link_equity_is_registered_as_cross_page() -> None:
    assert CROSS_PAGE_CHECKS["internal_link_equity"] is _check_internal_link_equity


def test_unprioritized_low_rank_page_is_not_a_finding() -> None:
    """Real data: 1,483 of 1,488 open findings were unprioritized pages at the
    6th-33rd percentile — a rank, not a defect."""
    pages = [_page(n, n) for n in range(1, _MIN_PAGES + 1)]  # min-pages rule
    site = SiteAggregates()
    index_page_facts(pages, site)
    for page in pages:
        outcome = _check_internal_link_equity(page, site)
        assert outcome.status == "pass"
        assert outcome.evidence["pagerank_percentile"] == site.link_equity_percentile_by_page[page.page_id]
