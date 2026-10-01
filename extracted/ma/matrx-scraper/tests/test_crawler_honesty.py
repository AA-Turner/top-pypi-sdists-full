"""Crawler honesty — OPENSEO-TOOLS-SPEC §8.1 / acceptance T12 (Lane H).

Every behaviour here is proven against a REAL HTTP server on loopback (aiohttp),
fetched by the REAL crawler and transport (curl_cffi / httpx) — never a stubbed
``scrape``. The only stand-in is the network policy (``local_network``): the SSRF gate
lets exactly this server's origin through.

Behaviours (one test each, every one fails on the pre-change code):

* ``Retry-After`` (seconds or HTTP-date) is honoured, else
  ``crawl.retry_after_default_s × 2^(n−1)``;
* a 429 pauses ALL new requests of the crawl, not just one worker's host;
* more than ``crawl.max_consecutive_429`` 429s in a row stops the crawl as
  ``stopped`` (session ``partial``, ``stats.stop_reason='rate_limited'``), and every
  URL left unfetched is recorded ``RateLimitTimeout``;
* a 429 retried more than ``crawl.max_retries_per_url`` times fails ``RateLimited``;
* ``cf-mitigated`` → ``cloudflare_block``; 401/403 → ``blocked``;
* blocked targets are never counted as broken internal links;
* link-discovered URLs are fetched before sitemap-only URLs (``crawl.link_first``);
* a page body over ``crawl.html_max_bytes`` is truncated with a page notice.
"""

from __future__ import annotations

import asyncio
import time
from datetime import UTC, datetime, timedelta
from email.utils import format_datetime
from typing import Any

import pytest
from aiohttp import web

from conftest import FAST_CRAWL_KNOBS, bind_crawl_knobs
from matrx_scraper.crawler import RENDER_HTTP_ONLY, SiteCrawler, SiteCrawlerConfig
from matrx_scraper.events import (
    CrawlCompletedEvent,
    CrawlEvent,
    CrawlPageFailedEvent,
    CrawlPageFetchedEvent,
    CrawlWarningEvent,
)
from matrx_scraper.queue_backend import InMemoryQueueBackend
from matrx_scraper.rate_limiter import CrawlPause, parse_retry_after
from matrx_scraper.scraper import FailureReason, wall_reason_from_status

PROSE = " ".join(
    "Our cleaners press every shirt by hand and return it folded the same day." for _ in range(8)
)


class Sink:
    def __init__(self) -> None:
        self.events: list[CrawlEvent] = []

    async def emit(self, event: CrawlEvent) -> None:
        self.events.append(event)

    def of(self, kind: type) -> list[Any]:
        return [e for e in self.events if isinstance(e, kind)]


def page(title: str, links: list[str] = ()) -> str:
    anchors = "".join(f'<p><a href="{href}">{href} details page</a></p>' for href in links)
    return (
        f"<!doctype html><html><head><title>{title}</title></head>"
        f"<body><main><h1>{title}</h1><p>{PROSE}</p>{anchors}</main></body></html>"
    )


class LocalSite:
    """A real HTTP server on 127.0.0.1 whose routes the test declares."""

    def __init__(self, routes: dict[str, Any]) -> None:
        self.routes = routes
        self.hits: list[tuple[float, str, int]] = []  # (arrival, path, status sent)
        self._runner: web.AppRunner | None = None
        self.origin = ""

    async def _handle(self, request: web.Request) -> web.StreamResponse:
        path = request.path
        spec = self.routes.get(path)
        if spec is None:
            response = web.Response(status=404, text="not here")
        elif callable(spec):
            response = spec(request)
        else:
            response = web.Response(text=spec, content_type="text/html")
        self.hits.append((time.monotonic(), path, response.status))
        return response

    async def __aenter__(self) -> LocalSite:
        app = web.Application()
        app.router.add_route("GET", "/{tail:.*}", self._handle)
        app.router.add_route("HEAD", "/{tail:.*}", self._handle)
        self._runner = web.AppRunner(app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, "127.0.0.1", 0)
        await site.start()
        port = site._server.sockets[0].getsockname()[1]  # noqa: SLF001
        self.origin = f"http://127.0.0.1:{port}"
        return self

    async def __aexit__(self, *exc: object) -> None:
        assert self._runner is not None
        await self._runner.cleanup()

    def page_hits(self) -> list[tuple[float, str, int]]:
        return [h for h in self.hits if not h[1].endswith((".txt", ".xml"))]


@pytest.fixture
def local_network(monkeypatch: pytest.MonkeyPatch):
    """The ONE stand-in: the crawler's SSRF gate refuses loopback, so exactly this
    server's origin is let through; every other URL still meets the real gate.
    The datacenter proxy pool is ours, not the site's — the crawl goes direct."""

    from matrx_scraper import crawler, sitemaps
    from matrx_scraper.utils import url as url_utils

    monkeypatch.delenv("DATACENTER_PROXIES", raising=False)
    real_public = url_utils.validate_public_http_url

    def allow(origin: str) -> None:
        async def validate_public(url: str) -> str:
            if url.startswith(origin + "/") or url == origin:
                return url
            return await real_public(url)

        for module in (crawler, sitemaps):
            if hasattr(module, "validate_public_http_url"):
                monkeypatch.setattr(module, "validate_public_http_url", validate_public)

    return allow


def crawler_for(site: LocalSite, sink: Sink, **config: Any) -> SiteCrawler:
    defaults: dict[str, Any] = dict(
        base_url=f"{site.origin}/",
        max_pages=50,
        concurrency=2,
        respect_robots=False,
        seed_from_sitemap=False,
        render_mode=RENDER_HTTP_ONLY,
        host_rps=1000.0,
    )
    defaults.update(config)
    return SiteCrawler(
        run_id="honesty",
        config=SiteCrawlerConfig(**defaults),
        event_sink=sink,
        queue_backend=InMemoryQueueBackend(),
    )


def too_many(retry_after: str | None):
    def respond(_request: web.Request) -> web.Response:
        headers = {"Retry-After": retry_after} if retry_after is not None else {}
        return web.Response(status=429, text="slow down", headers=headers)

    return respond


# ---------------------------------------------------------------------------
# Retry-After parsing and the backoff formula


def test_retry_after_accepts_seconds_and_http_date() -> None:
    now = datetime(2026, 9, 28, 12, 0, 0, tzinfo=UTC)
    assert parse_retry_after("2") == 2.0
    assert (
        parse_retry_after(format_datetime(now + timedelta(seconds=90), usegmt=True), now=now)
        == 90.0
    )
    assert (
        parse_retry_after(format_datetime(now - timedelta(seconds=5), usegmt=True), now=now) == 0.0
    )
    assert parse_retry_after("soon") is None
    assert parse_retry_after(None) is None


def test_pause_backoff_doubles_without_retry_after_and_obeys_it_when_sent() -> None:
    pause = CrawlPause(default_s=30, max_consecutive=3, max_cooldown_s=1800)
    assert pause.record_limit(None) == 30
    assert pause.record_limit(None) == 60
    assert pause.record_limit(7) == 7  # the site's own number wins
    pause.record_success()
    assert pause.record_limit(None) == 30  # a clean answer restarts the streak


def test_stop_rule_is_more_than_the_knob_in_a_row_or_over_the_cooldown() -> None:
    pause = CrawlPause(default_s=0, max_consecutive=3, max_cooldown_s=1800)
    for _ in range(3):
        pause.record_limit(0)
    assert pause.stop_reason() is None  # 3 in a row is still allowed
    pause.record_limit(0)
    assert "4 requests in a row" in (pause.stop_reason() or "")
    long_wait = CrawlPause(default_s=0, max_consecutive=99, max_cooldown_s=60)
    long_wait.record_limit(61)
    assert "minutes in total" in (long_wait.stop_reason() or "")


# ---------------------------------------------------------------------------
# T12 — a real 429 host


@pytest.mark.asyncio
async def test_a_429_pauses_every_request_for_retry_after_then_stops_partial(local_network) -> None:
    """T12: 429 + ``Retry-After: 2`` pauses ALL requests ~2 s; >3 in a row ends
    the crawl `stopped` / `rate_limited`, unfetched URLs `RateLimitTimeout`."""

    children = [f"/p{i}" for i in range(1, 9)]
    routes: dict[str, Any] = {"/": page("Home", children)}
    routes.update({path: too_many("2") for path in children})
    async with LocalSite(routes) as site:
        local_network(site.origin)
        sink = Sink()
        crawler = crawler_for(site, sink, concurrency=3)
        started = time.monotonic()
        await asyncio.wait_for(crawler.run(), timeout=60)
        elapsed = time.monotonic() - started

    completed = sink.of(CrawlCompletedEvent)[-1]
    assert completed.status == "stopped"
    assert completed.stop_reason == "rate_limited"
    assert completed.coverage_complete is False
    assert "stopped early" in (completed.error_message or "")

    # Crawl-wide pause: after every 429 the server saw, no request of ANY path
    # arrives until the Retry-After is (nearly) over. Requests already in flight
    # when the 429 landed arrive within milliseconds, hence the 0.3 s grace.
    too_many_at = [t for t, _path, status in site.hits if status == 429]
    assert len(too_many_at) >= 4
    for t429 in too_many_at:
        early = [
            (round(t - t429, 2), path)
            for t, path, _status in site.hits
            if 0.3 < t - t429 < 1.8 and t > t429
        ]
        assert early == [], f"requests arrived during the pause after a 429: {early}"
    assert elapsed >= 2.0

    failed = sink.of(CrawlPageFailedEvent)
    classes = {event.error_class for event in failed}
    assert classes == {"RateLimitTimeout"}, classes
    fetched_urls = {e.url for e in sink.of(CrawlPageFetchedEvent)}
    unfetched = {f"{site.origin}{p}" for p in children}
    assert {e.url for e in failed} == unfetched - fetched_urls
    warnings = [w for w in sink.of(CrawlWarningEvent) if w.context.get("stop_reason")]
    assert warnings and warnings[0].context["stop_reason"] == "rate_limited"
    paused = [w for w in sink.of(CrawlWarningEvent) if w.context.get("pause_source")]
    assert paused and paused[0].context["pause_source"] == "Retry-After"
    assert paused[0].context["pause_seconds"] == 2.0


@pytest.mark.asyncio
async def test_a_url_429_more_than_max_retries_fails_rate_limited(local_network) -> None:
    """Retries per URL are the knob (3), and the 4th 429 is `RateLimited`; clean
    answers from other pages keep the crawl-wide streak from stopping the run."""

    bind_crawl_knobs({**FAST_CRAWL_KNOBS, "crawl.max_consecutive_429": 99})
    healthy = [f"/ok{i}" for i in range(1, 4)]
    routes: dict[str, Any] = {"/": page("Home", ["/busy", *healthy]), "/busy": too_many("0")}
    routes.update({path: page(path) for path in healthy})
    async with LocalSite(routes) as site:
        local_network(site.origin)
        sink = Sink()
        await asyncio.wait_for(crawler_for(site, sink).run(), timeout=60)

    busy_hits = [h for h in site.hits if h[1] == "/busy"]
    assert len(busy_hits) == 1 + 3  # the first try + crawl.max_retries_per_url
    failed = sink.of(CrawlPageFailedEvent)
    assert [(e.url, e.error_class) for e in failed] == [(f"{site.origin}/busy", "RateLimited")]
    assert sink.of(CrawlCompletedEvent)[-1].status == "completed"


@pytest.mark.asyncio
async def test_no_retry_after_uses_the_default_backoff_knob(local_network) -> None:
    bind_crawl_knobs({**FAST_CRAWL_KNOBS, "crawl.retry_after_default_s": 0.75})
    state = {"n": 0}

    def once_then_ok(_request: web.Request) -> web.Response:
        state["n"] += 1
        if state["n"] == 1:
            return web.Response(status=429, text="slow down")
        return web.Response(text=page("Later"), content_type="text/html")

    async with LocalSite({"/": page("Home", ["/later"]), "/later": once_then_ok}) as site:
        local_network(site.origin)
        sink = Sink()
        await asyncio.wait_for(crawler_for(site, sink).run(), timeout=60)

    later = [t for t, path, _ in site.hits if path == "/later"]
    assert len(later) == 2
    assert later[1] - later[0] >= 0.7  # 0.75 × 2^0
    paused = [w for w in sink.of(CrawlWarningEvent) if w.context.get("pause_source")]
    assert paused[0].context["pause_source"] == "backoff"
    assert sink.of(CrawlCompletedEvent)[-1].status == "completed"


# ---------------------------------------------------------------------------
# Walls


def test_wall_order_429_then_cf_mitigated_then_401_403() -> None:
    assert wall_reason_from_status(429, {"cf-mitigated": "challenge"}) is None
    assert (
        wall_reason_from_status(503, {"CF-Mitigated": "challenge"})[0]
        is FailureReason.CLOUDFLARE_BLOCK
    )
    assert (
        wall_reason_from_status(403, {"cf-mitigated": "challenge"})[0]
        is FailureReason.CLOUDFLARE_BLOCK
    )
    assert wall_reason_from_status(401, {})[0] is FailureReason.BLOCKED
    assert wall_reason_from_status(403, {})[0] is FailureReason.BLOCKED
    assert wall_reason_from_status(404, {}) is None
    assert wall_reason_from_status(200, {}) is None


@pytest.mark.asyncio
async def test_walls_are_recorded_with_the_existing_reason_codes(local_network) -> None:
    routes = {
        "/": page("Home", ["/private", "/members", "/challenge", "/gone"]),
        "/private": lambda _r: web.Response(status=403, text="Forbidden"),
        "/members": lambda _r: web.Response(status=401, text="Unauthorized"),
        "/challenge": lambda _r: web.Response(
            status=503, text="One moment", headers={"cf-mitigated": "challenge"}
        ),
        "/gone": lambda _r: web.Response(status=404, text="Not found"),
    }
    async with LocalSite(routes) as site:
        local_network(site.origin)
        sink = Sink()
        await asyncio.wait_for(crawler_for(site, sink).run(), timeout=60)

    by_url = {e.url.rsplit("/", 1)[-1]: e.error_class for e in sink.of(CrawlPageFailedEvent)}
    # error_class IS the persisted web.crawl_url.reason_code (persistence.py).
    assert by_url == {
        "private": "blocked",
        "members": "blocked",
        "challenge": "cloudflare_block",
        "gone": "bad_status",
    }
    # A cf-mitigated 503 is a wall, never mistaken for a throttle and requeued
    # (one direct retry after the proxy refusal is the proxy-bypass rule).
    assert len([h for h in site.hits if h[1] == "/challenge"]) <= 2
    assert not [w for w in sink.of(CrawlWarningEvent) if "rate limited" in w.message]


def test_blocked_targets_are_never_broken_links() -> None:
    from matrx_scraper.crawler import _normalise_url
    from matrx_scraper.web_crawl.analysis import (
        PageLinkStats,
        _check_broken_internal_links,
        _split_blocked_targets,
    )
    from matrx_scraper.web_crawl.persistence import url_hash

    stats = PageLinkStats(
        checked=3,
        broken=["https://x.test/private", "https://x.test/gone", "https://x.test/wall"],
    )
    blocked = {
        url_hash(_normalise_url(u)) for u in ("https://x.test/private", "https://x.test/wall")
    }
    _split_blocked_targets(stats, blocked)
    assert stats.broken == ["https://x.test/gone"]
    assert stats.blocked == ["https://x.test/private", "https://x.test/wall"]
    assert stats.checked == 1

    class Facts:
        page_id = "p1"

    class Site:
        link_stats = {"p1": stats}

    outcome = _check_broken_internal_links(Facts(), Site())
    assert outcome.issue_count == 1
    assert "2 more target(s) blocked our crawler" in outcome.reasoning


# ---------------------------------------------------------------------------
# Order and size


def _sitemap(origin: str, paths: list[str]) -> str:
    urls = "".join(f"<url><loc>{origin}{p}</loc></url>" for p in paths)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    )


async def _crawl_order(local_network, link_first: bool) -> list[str]:
    bind_crawl_knobs({**FAST_CRAWL_KNOBS, "crawl.link_first": link_first})
    routes: dict[str, Any] = {
        "/": page("Home", ["/a"]),
        "/a": page("A", ["/b"]),
        "/b": page("B"),
        "/s1": page("Sitemap only one"),
        "/s2": page("Sitemap only two"),
    }
    async with LocalSite(routes) as site:
        routes["/sitemap.xml"] = lambda _r: web.Response(
            text=_sitemap(site.origin, ["/s1", "/a", "/s2"]), content_type="application/xml"
        )
        local_network(site.origin)
        sink = Sink()
        crawler = crawler_for(site, sink, concurrency=1, seed_from_sitemap=True)
        await asyncio.wait_for(crawler.run(), timeout=60)
    assert sink.of(CrawlCompletedEvent)[-1].status == "completed"
    return [path for _t, path, _s in site.page_hits() if path in {"/", "/a", "/b", "/s1", "/s2"}]


@pytest.mark.asyncio
async def test_link_discovered_urls_are_fetched_before_sitemap_only_urls(local_network) -> None:
    order = await _crawl_order(local_network, link_first=True)
    fetched = [p for p in order if p != "/"] if order.count("/") > 1 else order
    assert set(order) == {"/", "/a", "/b", "/s1", "/s2"}
    last_link = max(fetched.index("/a"), fetched.index("/b"))
    first_sitemap = min(fetched.index("/s1"), fetched.index("/s2"))
    assert last_link < first_sitemap, order
    # Each URL fetched once — the linked /a also listed in the sitemap is not refetched.
    assert fetched.count("/a") == 1


@pytest.mark.asyncio
async def test_link_first_off_keeps_sitemap_first(local_network) -> None:
    order = await _crawl_order(local_network, link_first=False)
    assert order.index("/s1") < order.index("/b"), order


@pytest.mark.asyncio
async def test_page_body_over_the_byte_cap_is_truncated_with_a_notice(local_network) -> None:
    bind_crawl_knobs({**FAST_CRAWL_KNOBS, "crawl.html_max_bytes": 2000})
    big = page("Big", []).replace("</main>", "<p>" + ("x" * 5000) + "</p></main>")
    async with LocalSite({"/": page("Home", ["/big"]), "/big": big}) as site:
        local_network(site.origin)
        sink = Sink()
        crawler = crawler_for(site, sink)
        await asyncio.wait_for(crawler.run(), timeout=60)

    notices = [w for w in sink.of(CrawlWarningEvent) if w.context.get("signal") == "html_truncated"]
    assert [n.context["url"] for n in notices] == [f"{site.origin}/big"]
    assert notices[0].context["original_bytes"] > 5000
    assert notices[0].context["kept_bytes"] == 2000
    kept = crawler.results[f"{site.origin}/big"].raw_html or ""
    assert len(kept.encode()) <= 2000
    home = crawler.results[f"{site.origin}/"].raw_html or ""
    assert "</html>" in home  # an under-cap page is untouched


# ---------------------------------------------------------------------------
# Every crawl.* knob is overridable per organization (and person, and site):
# the crawl resolves them for ITS scope, once per run.


@pytest.mark.asyncio
async def test_an_org_override_changes_the_crawl_for_that_org_only(local_network) -> None:
    from matrx_scraper.parser.knobs import KnobScope, configure_parser_knobs

    org_a, org_b, site_id = "org-a", "org-b", "site-1"
    calls: list[KnobScope] = []

    async def scoped(keys: list[str], scope: KnobScope) -> dict[str, object]:
        # Stands in for the host resolver's ANSWER only: org A has overridden
        # the byte cap; org B has not. Resolution itself is proven live.
        calls.append(scope)
        values = {k: FAST_CRAWL_KNOBS[k] for k in keys}
        if scope.organization_id == org_a:
            values["crawl.html_max_bytes"] = 2000
        return values

    configure_parser_knobs(lambda key: FAST_CRAWL_KNOBS[key], scoped_reader=scoped)
    big = page("Big").replace("</main>", "<p>" + ("x" * 5000) + "</p></main>")
    truncated: dict[str, list[str]] = {}
    async with LocalSite({"/": page("Home", ["/big"]), "/big": big}) as site:
        local_network(site.origin)
        for org in (org_a, org_b):
            sink = Sink()
            crawler = SiteCrawler(
                run_id=f"scoped-{org}",
                config=SiteCrawlerConfig(
                    base_url=f"{site.origin}/",
                    concurrency=2,
                    respect_robots=False,
                    seed_from_sitemap=False,
                    render_mode=RENDER_HTTP_ONLY,
                    host_rps=1000.0,
                ),
                event_sink=sink,
                queue_backend=InMemoryQueueBackend(),
                knob_scope=KnobScope(organization_id=org, user_id="u-1", site_id=site_id),
            )
            await asyncio.wait_for(crawler.run(), timeout=60)
            truncated[org] = [
                w.context["url"]
                for w in sink.of(CrawlWarningEvent)
                if w.context.get("signal") == "html_truncated"
            ]

    assert truncated[org_a] == [f"{site.origin}/big"]
    assert truncated[org_b] == []
    # One resolution per crawl run, carrying the org, person and site.
    assert [(c.organization_id, c.user_id, c.site_id) for c in calls] == [
        (org_a, "u-1", site_id),
        (org_b, "u-1", site_id),
    ]


@pytest.mark.asyncio
async def test_progress_counts_a_page_as_downloaded_the_moment_its_response_lands(
    local_network,
) -> None:
    """2026-09-14: the header read "0 fetched" for two minutes while pages were
    landing, because `pages_fetched` only counts a page once its capture is
    persisted (screenshots + storage). Heartbeats must carry the responses
    received (`pages_downloaded`) so a live count can move with the fetches."""

    from matrx_scraper.events import CrawlProgressEvent

    async def slow_capture(_request: object) -> None:
        await asyncio.sleep(2.5)
        return None

    routes: dict[str, Any] = {"/": page("Home", ["/a", "/b"]), "/a": page("A", []), "/b": page("B", [])}
    async with LocalSite(routes) as site:
        local_network(site.origin)
        sink = Sink()
        crawler = crawler_for(site, sink, concurrency=1, progress_every_seconds=1.0)
        crawler.body_persister = slow_capture
        await asyncio.wait_for(crawler.run(), timeout=60)

    mid_capture = [
        e for e in sink.of(CrawlProgressEvent) if e.pages_downloaded > e.pages_fetched
    ]
    assert mid_capture, "no heartbeat reported a downloaded page still being captured"
    assert mid_capture[0].pages_fetched == 0 and mid_capture[0].pages_downloaded >= 1
    completed = sink.of(CrawlCompletedEvent)[-1]
    assert completed.pages_downloaded == completed.pages_fetched == 3
