"""Arman 2026-10-15: our own code does not refuse public-web access.

robots.txt Disallow is not obeyed by default (knob `knowledge.scraper.respect_robots`,
ships off), a 403 wall reaches the browser step the trail lists, and a bot wall is
labeled by its real reason rather than `login_wall`.
"""

from __future__ import annotations

from matrx_scraper.crawler import CRAWL_KNOB_MIRRORS, CrawlKnobs, SiteCrawler, SiteCrawlerConfig
from matrx_scraper.escalation import ESCALATABLE_REASONS, EscalationPolicy
from matrx_scraper.ladder import OWN_BROWSER_REASONS
from matrx_scraper.orchestrator import ScrapeResult, _ladder_reason
from matrx_scraper.queue_backend import InMemoryQueueBackend


def _crawler(**cfg) -> SiteCrawler:
    return SiteCrawler(
        run_id="posture",
        config=SiteCrawlerConfig(base_url="https://x.test/", **cfg),
        queue_backend=InMemoryQueueBackend(),
    )


def test_robots_disallowed_urls_are_fetched_by_default() -> None:
    crawler = _crawler()
    # No robots cache means `_process_page` never reaches the Disallow refusal.
    assert crawler._respect_robots is False
    assert crawler._robots is None
    assert SiteCrawlerConfig(base_url="https://x.test/").respect_robots is None
    assert CRAWL_KNOB_MIRRORS["respect_robots"] is False
    assert CrawlKnobs.load().respect_robots is False


def test_an_explicit_opt_in_still_turns_robots_on() -> None:
    crawler = _crawler(respect_robots=True)
    assert crawler._respect_robots is True
    assert crawler._robots is not None


def test_blocked_walls_escalate_to_the_browser() -> None:
    assert "blocked" in ESCALATABLE_REASONS
    assert EscalationPolicy().wants("blocked")
    assert "blocked" in OWN_BROWSER_REASONS


def _wall(status: int, reason: str, response_url: str = "https://x.test/a") -> ScrapeResult:
    return ScrapeResult(
        url="https://x.test/a",
        response_url=response_url,
        success=False,
        content_type="html",
        failure_reason=reason,
        status_code=status,
    )


def test_a_403_bot_wall_is_labelled_by_its_real_reason() -> None:
    assert _ladder_reason(_wall(403, "blocked")) == "blocked"
    assert _ladder_reason(_wall(403, "cloudflare_block")) == "cloudflare_block"


def test_login_wall_still_needs_login_evidence() -> None:
    assert _ladder_reason(_wall(401, "bad_status")) == "login_wall"
    assert (
        _ladder_reason(_wall(200, "bad_status", "https://x.test/accounts/login/"))
        == "login_wall"
    )
