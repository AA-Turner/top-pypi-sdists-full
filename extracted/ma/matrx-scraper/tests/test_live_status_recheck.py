"""A crawl's status code is a fact about the moment of the crawl.

Real case (allgreenrecycling.com, 2026-10-05): the stored crawl said HTTP 500
for /compliance and three more pages; live they answered 200, and the new
attention budget would have put "Server Errors (5xx)" first. A 404 page stayed
404. Expected results written from that; planted breaks below.
"""

import asyncio
from types import SimpleNamespace

from matrx_scraper.web_crawl.analysis import recheck_failing_statuses


class FakeVerifier:
    def __init__(self, answers: dict[str, tuple[int, str | None]]):
        self.answers = answers
        self.asked: list[str] = []

    async def verify(self, url: str):
        self.asked.append(url)
        # A URL the test did not script (the trailing-slash form the recheck
        # also asks on a 404) answers 404 like the page itself.
        status, error = self.answers.get(url, (404, None))
        return SimpleNamespace(http_status=status, error=error, final_url=url)


def page(page_id: str, url: str, status: int | None):
    return SimpleNamespace(page_id=page_id, url=url, http_status=status)


def test_a_recovered_page_carries_its_current_status_and_a_dead_one_stays_dead() -> None:
    pages = [
        page("p1", "https://allgreenrecycling.com/compliance", 500),
        page("p2", "https://allgreenrecycling.com/industries-served", 404),
        page("p3", "https://allgreenrecycling.com/", 200),
    ]
    verifier = FakeVerifier({
        "https://allgreenrecycling.com/compliance": (200, None),
        "https://allgreenrecycling.com/industries-served": (404, None),
    })
    rechecks = asyncio.run(recheck_failing_statuses(pages, verifier=verifier))
    assert pages[0].http_status == 200 and rechecks["p1"]["crawl_status"] == 500
    assert pages[1].http_status == 404 and rechecks["p2"]["live_status"] == 404
    # A page the crawl saw healthy is not asked again.
    assert "https://allgreenrecycling.com/" not in verifier.asked and "p3" not in rechecks


def test_planted_break_no_answer_is_never_a_recovery() -> None:
    pages = [page("p1", "https://example.com/x", 500)]
    verifier = FakeVerifier({"https://example.com/x": (0, "ConnectTimeout")})
    rechecks = asyncio.run(recheck_failing_statuses(pages, verifier=verifier))
    assert pages[0].http_status == 500
    assert rechecks["p1"]["error"] == "ConnectTimeout"


def test_a_changed_error_is_reported_as_it_is_now() -> None:
    pages = [page("p1", "https://example.com/y", 500)]
    verifier = FakeVerifier({"https://example.com/y": (404, None)})
    asyncio.run(recheck_failing_statuses(pages, verifier=verifier))
    assert pages[0].http_status == 404  # a 404 today, not yesterday's 500


def test_the_homepage_is_rechecked_first_when_over_the_cap() -> None:
    pages = [page(f"p{i}", f"https://example.com/deep/{i}", 500) for i in range(3)]
    pages.append(page("home", "https://example.com/", 500))
    answers = {p.url: (200, None) for p in pages}
    verifier = FakeVerifier(answers)
    asyncio.run(recheck_failing_statuses(pages, verifier=verifier, limit=1))
    assert verifier.asked == ["https://example.com/"]
