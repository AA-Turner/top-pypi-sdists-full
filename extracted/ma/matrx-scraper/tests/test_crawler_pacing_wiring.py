"""The pacing ruling, wired into a real crawl — not just the policy unit.

`test_host_pacing.py` pins the DECISION (detect, honour robots, climb, back off).
This file pins that a `SiteCrawler` actually consumes it: that a crawl opens at
the plan's rate rather than at `host_rps`, that the rate it reports is the rate
the limiter enforces, that a 429 still teaches the other lanes, and that what a
run learned comes back out for the next one.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_scraper.crawler import (
    RENDER_HTTP_ONLY,
    SiteCrawler,
    SiteCrawlerConfig,
)
from matrx_scraper.events import CrawlPacingEvent
from matrx_scraper.host_pacing import PacingKnobs, RememberedPacing
from matrx_scraper.orchestrator import ScrapeResult
from matrx_scraper.queue_backend import InMemoryQueueBackend
from matrx_scraper.rate_limiter import host_key, shared_throttles

SITE = "https://paced.example/"
HOST = host_key(SITE)

# Fast enough that the token bucket never makes the suite wait, while still
# leaving the ramp room to move in both directions.
FAST = PacingKnobs(floor_rps=40.0, max_rps=160.0, min_rps=10.0, ramp_after_clean=2)


class _Sink:
    def __init__(self) -> None:
        self.events: list[Any] = []

    async def emit(self, event: Any) -> None:
        self.events.append(event)

    def pacing(self) -> list[CrawlPacingEvent]:
        return [e for e in self.events if isinstance(e, CrawlPacingEvent)]


def _result(url: str, status: int = 200) -> ScrapeResult:
    return ScrapeResult(
        url=url,
        response_url=url,
        success=status == 200,
        content_type="html",
        status_code=status,
        raw_html="<html><body>" + ("word " * 200) + "</body></html>",
        text_data="word " * 200,
    )


@pytest.fixture
def _no_network(monkeypatch: pytest.MonkeyPatch) -> None:
    """No probe, no fetch, no DNS. The pacing PLAN is supplied by the test."""

    async def no_probe_delay(self: SiteCrawler) -> float | None:
        return None

    async def no_probe_platform(self: SiteCrawler) -> tuple[dict[str, str] | None, str | None]:
        return None, None

    monkeypatch.setattr(SiteCrawler, "_probe_crawl_delay", no_probe_delay)
    monkeypatch.setattr(SiteCrawler, "_probe_platform", no_probe_platform)
    monkeypatch.setattr(
        "matrx_scraper.crawler.validate_public_http_url",
        lambda url: _noop(),
    )


async def _noop() -> None:
    return None


def _crawler(
    sink: _Sink,
    *,
    host_rps: float = 150.0,
    remembered: RememberedPacing | None = None,
    urls: list[str] | None = None,
) -> SiteCrawler:
    return SiteCrawler(
        run_id="pacing-wiring",
        config=SiteCrawlerConfig(
            base_url=SITE,
            render_mode=RENDER_HTTP_ONLY,
            seed_from_sitemap=False,
            list_mode=True,
            seed_urls=urls or [f"{SITE}a"],
            max_pages=50,
            concurrency=1,
            host_rps=host_rps,
        ),
        event_sink=sink,
        queue_backend=InMemoryQueueBackend(),
        pacing_knobs=FAST,
        remembered_pacing=remembered,
    )


@pytest.mark.asyncio
async def test_a_crawl_opens_at_the_floor_not_at_host_rps(
    monkeypatch: pytest.MonkeyPatch, _no_network: None
) -> None:
    """The whole point of the ruling: `host_rps` is the ceiling, not the start."""

    monkeypatch.setattr("matrx_scraper.crawler.scrape", lambda url, **kw: _async(_result(url)))
    sink = _Sink()
    crawler = _crawler(sink, host_rps=150.0)
    await crawler.run()

    opening = sink.pacing()[0]
    assert opening.reason == "plan_resolved"
    assert opening.current_rps == FAST.floor_rps
    assert opening.current_rps < 150.0
    assert opening.ceiling_rps == 150.0


@pytest.mark.asyncio
async def test_the_reported_rate_is_the_rate_the_limiter_enforces(
    monkeypatch: pytest.MonkeyPatch, _no_network: None
) -> None:
    """A pacing event nobody applied would be theatre."""

    monkeypatch.setattr("matrx_scraper.crawler.scrape", lambda url, **kw: _async(_result(url)))
    sink = _Sink()
    crawler = _crawler(sink, urls=[f"{SITE}{index}" for index in range(12)])
    await crawler.run()

    latest = sink.pacing()[-1]
    enforced_rps, _ = crawler._rate_limiter._effective(HOST)
    assert enforced_rps == pytest.approx(latest.current_rps)


@pytest.mark.asyncio
async def test_clean_responses_climb_the_rate(
    monkeypatch: pytest.MonkeyPatch, _no_network: None
) -> None:
    monkeypatch.setattr("matrx_scraper.crawler.scrape", lambda url, **kw: _async(_result(url)))
    sink = _Sink()
    crawler = _crawler(sink, urls=[f"{SITE}{index}" for index in range(12)])
    await crawler.run()

    climbs = [event for event in sink.pacing() if event.reason == "ramp_up"]
    assert climbs, "a dozen clean fetches must earn at least one climb"
    assert climbs[-1].current_rps > FAST.floor_rps


@pytest.mark.asyncio
async def test_a_429_lowers_this_crawl_AND_still_teaches_the_other_lanes(
    monkeypatch: pytest.MonkeyPatch, _no_network: None
) -> None:
    """The regression this seam exists to prevent.

    While ramp rates lived in the limiter's baseline, backing a host down to a
    fraction of a request per second collapsed `throttle_host`'s `min_rps`
    floor, so no cross-lane factor was recorded and the research and SEO lanes
    silently learned nothing from a 429 the crawler had already paid for.
    """

    monkeypatch.setattr(
        "matrx_scraper.crawler.scrape", lambda url, **kw: _async(_result(url, status=429))
    )
    sink = _Sink()
    crawler = _crawler(sink)
    await crawler.run()

    ramp = crawler._ramps[HOST]
    assert ramp.discovered_limit_rps is not None
    assert ramp.current_rps < FAST.floor_rps
    assert shared_throttles().get(HOST, 1.0) < 1.0


@pytest.mark.asyncio
async def test_a_remembered_ceiling_is_honoured_at_run_start(
    monkeypatch: pytest.MonkeyPatch, _no_network: None
) -> None:
    monkeypatch.setattr("matrx_scraper.crawler.scrape", lambda url, **kw: _async(_result(url)))
    sink = _Sink()
    crawler = _crawler(
        sink,
        host_rps=150.0,
        remembered=RememberedPacing(host=HOST, ceiling_rps=60.0, source="remembered"),
    )
    await crawler.run()

    opening = sink.pacing()[0]
    assert opening.source == "remembered"
    assert opening.ceiling_rps == pytest.approx(60.0)
    assert opening.current_rps == pytest.approx(60.0 * FAST.remembered_start_fraction)


@pytest.mark.asyncio
async def test_what_a_run_learned_comes_back_out_for_the_next_one(
    monkeypatch: pytest.MonkeyPatch, _no_network: None
) -> None:
    monkeypatch.setattr(
        "matrx_scraper.crawler.scrape", lambda url, **kw: _async(_result(url, status=429))
    )
    sink = _Sink()
    crawler = _crawler(sink)
    await crawler.run()

    learned = crawler.remembered_pacing()
    assert HOST in learned
    assert learned[HOST].ceiling_rps == pytest.approx(crawler._ramps[HOST].discovered_limit_rps)
    assert learned[HOST].limit_hits >= 1


@pytest.mark.asyncio
async def test_a_configured_maximum_below_the_floor_still_wins(
    monkeypatch: pytest.MonkeyPatch, _no_network: None
) -> None:
    """A user asking us to go slower is never overridden by the ramp's floor."""

    monkeypatch.setattr("matrx_scraper.crawler.scrape", lambda url, **kw: _async(_result(url)))
    sink = _Sink()
    crawler = _crawler(sink, host_rps=15.0, urls=[f"{SITE}{index}" for index in range(12)])
    await crawler.run()

    assert all(event.current_rps <= 15.0 for event in sink.pacing())


async def _async(value: Any) -> Any:
    return value
