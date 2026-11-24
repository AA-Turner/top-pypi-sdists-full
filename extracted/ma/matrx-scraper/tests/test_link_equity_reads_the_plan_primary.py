"""internal_link_equity's "prioritized page" is the page whose SEO plan names a primary keyword.

The target keyword's one home is ``web.page.desired_values.keyword_plan.primary_keyword_id``.
The retired text column held a value on 12 pages while the plans held 629, so a check that read
the column judged almost no prioritized page at all.
"""

from types import SimpleNamespace

from matrx_scraper.web_crawl import analysis

RETIRED = "target" + "_keyword"


def _page(desired_values, **extra):
    return SimpleNamespace(id="p1", url="https://acme.example/a", link_score=0.4, desired_values=desired_values, **extra)


def test_the_plan_primary_makes_a_page_prioritized() -> None:
    page = _page({"keyword_plan": {"primary_keyword_id": " 7b1c0e9a-0000-4000-8000-000000000001 "}})
    assert analysis._page_link_facts(page) == (0.4, "7b1c0e9a-0000-4000-8000-000000000001")
    facts = analysis._extract_transport_facts(page, {"http_status": 200})
    assert facts.primary_keyword_id == "7b1c0e9a-0000-4000-8000-000000000001"


def test_the_retired_column_alone_prioritizes_nothing() -> None:
    page = _page({}, **{RETIRED: "emergency plumber"})
    assert analysis._page_link_facts(page) == (0.4, None)
    assert not hasattr(analysis.PageFacts(url="https://acme.example/a"), RETIRED)


def test_a_blank_or_malformed_plan_is_not_prioritized() -> None:
    for desired in (None, [], {"keyword_plan": None}, {"keyword_plan": {"primary_keyword_id": "  "}},
                    {"keyword_plan": {"primary_keyword_id": 7}}):
        assert analysis._page_link_facts(_page(desired))[1] is None
