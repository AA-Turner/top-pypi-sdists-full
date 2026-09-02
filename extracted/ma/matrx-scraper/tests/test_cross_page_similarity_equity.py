"""Focused contract tests for deterministic cross-page catalogue checks."""

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


def test_internal_link_equity_uses_inclusive_site_percentiles() -> None:
    pages = [_page(1, 1), _page(2, 2), _page(3, 3), _page(4, 4)]
    site = SiteAggregates()

    index_page_facts(pages, site)

    assert site.link_equity_percentile_by_page == {
        "p1": 25,
        "p2": 50,
        "p3": 75,
        "p4": 100,
    }
    assert _check_internal_link_equity(pages[0], site).status == "fail"
    assert _check_internal_link_equity(pages[1], site).status == "warn"
    assert _check_internal_link_equity(pages[3], site).status == "pass"


def test_internal_link_equity_ties_share_one_rank_and_top_ties_are_healthy() -> None:
    pages = [_page(1, 5), _page(2, 5), _page(3, 10), _page(4, 10)]
    site = SiteAggregates()

    index_page_facts(pages, site)

    assert site.link_equity_percentile_by_page == {
        "p1": 50,
        "p2": 50,
        "p3": 100,
        "p4": 100,
    }


def test_internal_link_equity_applies_published_priority_penalty() -> None:
    pages = [
        _page(i, float(i), target_keyword="commercial phrase" if i == 1 else None)
        for i in range(1, 6)
    ]
    site = SiteAggregates()
    index_page_facts(pages, site)

    outcome = _check_internal_link_equity(pages[0], site)

    assert outcome.status == "fail"
    assert outcome.score == 20
    assert outcome.issue_count == 1
    assert outcome.evidence["prioritized"] is True
    assert outcome.evidence["priority_penalty_applied"] is True
    assert "commercial phrase" in outcome.reasoning


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
