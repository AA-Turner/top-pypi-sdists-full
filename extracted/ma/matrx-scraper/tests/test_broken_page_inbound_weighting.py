"""A 404's score follows `broken_page_4xx.score_contract`: how hard the site
still asks for the address. Before 2026-10-14 every 4xx scored a flat 10, so an
address nothing links to read as Critical and the reader was never told who
still points at it.
"""

from __future__ import annotations

import pytest

from matrx_scraper.web_crawl.analysis import PAGE_CHECKS, PageFacts, SiteAggregates

PAGE = "p-404"


def _site(inlinks: int, *, sitemap: bool | None = False, graph: bool = True) -> SiteAggregates:
    site = SiteAggregates()
    site.internal_edges_resolved = 500 if graph else 0
    site.inlinks = {PAGE: {f"src-{i}" for i in range(inlinks)}} if inlinks else {}
    site.sitemap_page_ids = None if sitemap is None else ({PAGE} if sitemap else set())
    return site


def _run(site: SiteAggregates):
    facts = PageFacts(url="https://example.com/gone", page_id=PAGE, http_status=404)
    return PAGE_CHECKS["broken_page_4xx"](facts, site)


@pytest.mark.parametrize(
    ("inlinks", "sitemap", "score"),
    [(1072, False, 5), (10, False, 5), (0, True, 5), (3, False, 15), (1, False, 15)],
)
def test_score_follows_the_contract(inlinks, sitemap, score):
    outcome = _run(_site(inlinks, sitemap=sitemap))
    assert outcome.status == "fail"
    assert outcome.score == score
    assert outcome.evidence["inlink_pages"] == inlinks
    assert outcome.evidence["in_sitemap"] is sitemap


def test_reason_names_who_still_links():
    outcome = _run(_site(1072))
    assert "1,072 of your own pages still link to it" in outcome.reasoning


def test_no_link_graph_is_unknown_not_zero():
    outcome = _run(_site(0, graph=False))
    assert outcome.score == 10
    assert "inlink_pages" not in outcome.evidence


def test_unloaded_sitemap_is_not_absent():
    site = _site(0, sitemap=None)
    site.ever_worked_page_ids = {PAGE}
    outcome = _run(site)
    assert outcome.evidence["in_sitemap"] is None
    assert outcome.score == 40


def test_an_address_nothing_vouches_for_is_not_a_broken_page():
    # THE EVIDENCE RULE (Arman, 2026-10-14): a hand-seeded /services/service-1
    # that never existed, with no links, no sitemap entry and no Google
    # presence, is not a defect.
    site = _site(0, sitemap=False)
    site.ever_worked_page_ids = set()
    outcome = _run(site)
    assert outcome.status == "n_a"
    assert "It isn't a broken page" in outcome.reasoning


@pytest.mark.parametrize("vouch", ["ever_worked", "google"])
def test_a_past_life_or_google_makes_it_real(vouch):
    from matrx_scraper.web_crawl.analysis import GscPeriod, PageGscStats

    site = _site(0, sitemap=False)
    site.ever_worked_page_ids = {PAGE} if vouch == "ever_worked" else set()
    if vouch == "google":
        site.gsc.bound = True
        site.gsc.by_page[PAGE] = PageGscStats(quarter=GscPeriod(impressions=40))
    outcome = _run(site)
    assert outcome.status == "fail" and outcome.score == 40


def test_a_working_page_passes_untouched():
    facts = PageFacts(url="https://example.com/ok", page_id=PAGE, http_status=200)
    assert PAGE_CHECKS["broken_page_4xx"](facts, _site(5)).status == "pass"


@pytest.mark.parametrize("status", [401, 403, 429])
def test_a_wall_is_never_a_broken_page(status):
    # 2026-10-14: 84 of 115 open "broken page" findings were one host's 429.
    facts = PageFacts(url="https://example.com/x", page_id=PAGE, http_status=status)
    outcome = PAGE_CHECKS["broken_page_4xx"](facts, _site(40))
    assert outcome.status == "n_a"
    assert outcome.reasoning.startswith("Blocked — could not assess")


class _FakeOutcome:
    def __init__(self, status, final_url=None):
        self.http_status = status
        self.final_url = final_url
        self.error = None


class _FakeVerifier:
    def __init__(self, answers):
        self.answers = answers
        self.asked: list[str] = []

    async def verify(self, url):
        self.asked.append(url)
        return _FakeOutcome(*self.answers.get(url, (404,)))


def _recheck(answers, url="https://example.com/industries-served"):
    import asyncio

    from matrx_scraper.web_crawl.analysis import recheck_failing_statuses

    facts = PageFacts(url=url, page_id=PAGE, http_status=404)
    verifier = _FakeVerifier(answers)
    rechecks = asyncio.run(recheck_failing_statuses([facts], verifier=verifier))
    return facts, rechecks[PAGE], verifier


def test_slash_form_that_works_is_never_broken():
    # Live 2026-10-14: /industries-served 404, /industries-served/ 301 -> /industries/ 200.
    facts, record, _ = _recheck(
        {
            "https://example.com/industries-served": (404,),
            "https://example.com/industries-served/": (200, "https://example.com/industries/"),
        }
    )
    assert facts.http_status == 200
    assert record["slash_variant"]["final_url"] == "https://example.com/industries/"
    assert PAGE_CHECKS["broken_page_4xx"](facts, _site(1072)).status == "pass"


def test_slash_form_that_also_fails_stays_broken():
    facts, record, _ = _recheck({})
    assert facts.http_status == 404
    assert record["slash_variant"]["status"] == 404


def test_file_paths_are_not_slash_probed():
    _, record, verifier = _recheck({}, url="https://example.com/doc.pdf")
    assert "slash_variant" not in record
    assert verifier.asked == ["https://example.com/doc.pdf"]
