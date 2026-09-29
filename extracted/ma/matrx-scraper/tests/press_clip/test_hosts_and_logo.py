"""Request-level host blocking and the logo ladder's order — pure parts."""

from __future__ import annotations

import pytest

from matrx_scraper.press_clip.hosts import BLOCKED_HOST_TOKENS, is_blocked_host
from matrx_scraper.press_clip.logo import resolve_logo

# newsjack skills/press-clip/clip.mjs @092d882, BLOCK_HOSTS — every token, verbatim.
UPSTREAM_TOKENS = (
    "doubleclick googlesyndication googletagservices google-analytics googletagmanager "
    r"adservice\.google amazon-adsystem adsystem taboola outbrain zergnet connatix "
    r"spot\.im openweb disqus criteo pubmatic rubiconproject adnxs moatads scorecardresearch "
    "zemanta sharethrough teads indexww casalemedia 3lift districtm smartadserver yieldmo "
    r"sailthru piano\.io permutive chartbeat parsely nativo bidswitch adlightning confiant"
).split()


def test_host_list_is_upstream_verbatim():
    assert tuple(BLOCKED_HOST_TOKENS) == tuple(t.replace("\\.", ".") for t in UPSTREAM_TOKENS)


@pytest.mark.parametrize(
    "host",
    [
        "securepubads.g.doubleclick.net",
        "pagead2.googlesyndication.com",
        "cdn.taboola.com",
        "widgets.outbrain.com",
        "www.zergnet.com",
        "launcher.spot.im",
        "c.amazon-adsystem.com",
        "static.chartbeat.com",
        "cdn.PARSELY.com",
    ],
)
def test_ad_and_recirculation_hosts_are_blocked(host):
    assert is_blocked_host(host) is True


@pytest.mark.parametrize(
    "host",
    ["www.wastedive.com", "www.indianchemicalnews.com", "s.yimg.com", "piano-lessons.com", ""],
)
def test_first_party_and_lookalike_hosts_pass(host):
    assert is_blocked_host(host) is False


def _recorder(calls, name, value):
    async def detect():
        calls.append(name)
        return value

    return detect


async def test_explicit_logo_wins_and_nothing_is_probed():
    calls: list[str] = []
    got = await resolve_logo(
        explicit_url="https://cdn.example/logo.svg",
        article_masthead=_recorder(calls, "article", ("https://a/logo.png", "")),
        home_masthead=_recorder(calls, "home", ("https://h/logo.png", "")),
        fallback=_recorder(calls, "fallback", "https://a/favicon.ico"),
    )
    assert (got.source, got.url) == ("explicit", "https://cdn.example/logo.svg")
    assert calls == []


async def test_article_masthead_before_home_page():
    calls: list[str] = []
    got = await resolve_logo(
        explicit_url=None,
        article_masthead=_recorder(calls, "article", ("", "<svg/>")),
        home_masthead=_recorder(calls, "home", ("https://h/logo.png", "")),
        fallback=_recorder(calls, "fallback", "https://a/favicon.ico"),
    )
    assert (got.source, got.svg) == ("article_masthead", "<svg/>")
    assert calls == ["article"]


async def test_home_page_before_og_logo_or_favicon():
    calls: list[str] = []
    got = await resolve_logo(
        explicit_url=None,
        article_masthead=_recorder(calls, "article", ("", "")),
        home_masthead=_recorder(calls, "home", ("https://h/logo.png", "")),
        fallback=_recorder(calls, "fallback", "https://a/favicon.ico"),
    )
    assert (got.source, got.url) == ("home_masthead", "https://h/logo.png")
    assert calls == ["article", "home"]


async def test_home_page_failure_is_best_effort_then_fallback():
    calls: list[str] = []

    async def broken_home():
        calls.append("home")
        raise TimeoutError("home page did not load")

    got = await resolve_logo(
        explicit_url=None,
        article_masthead=_recorder(calls, "article", ("", "")),
        home_masthead=broken_home,
        fallback=_recorder(calls, "fallback", "https://a/favicon.ico"),
    )
    assert (got.source, got.url) == ("og_logo_or_favicon", "https://a/favicon.ico")
    assert calls == ["article", "home", "fallback"]
    assert any("home page did not load" in n for n in got.notes)


async def test_text_wordmark_is_the_last_resort_and_says_so():
    calls: list[str] = []
    got = await resolve_logo(
        explicit_url=None,
        article_masthead=_recorder(calls, "article", ("", "")),
        home_masthead=_recorder(calls, "home", ("", "")),
        fallback=_recorder(calls, "fallback", ""),
    )
    assert got.source == "text_wordmark"
    assert got.url is None and got.svg is None
    assert calls == ["article", "home", "fallback"]


async def test_blocking_happens_at_the_request_level_in_a_real_browser():
    """Blocked hosts are aborted before any byte loads; everything else falls
    through to the handlers registered before it (in production, the SSRF
    egress guard), and the count is what the render reports."""
    from playwright.async_api import async_playwright

    from matrx_scraper.press_clip.renderer import BlockCounter, install_block_route

    html = (
        "<html><body><p>story</p>"
        '<img src="https://securepubads.g.doubleclick.net/ad.png">'
        '<script src="https://cdn.taboola.com/loader.js"></script>'
        '<img src="https://www.example-news.com/photo.jpg">'
        "</body></html>"
    )
    passed_through: list[str] = []

    async def base(route):  # stands in for the egress guard: registered FIRST, runs LAST
        passed_through.append(route.request.url)
        await route.fulfill(status=200, body="")

    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=True)
    try:
        context = await browser.new_context()
        await context.route("**/*", base)
        counter = BlockCounter()
        await install_block_route(context, counter)
        page = await context.new_page()
        await page.set_content(html, wait_until="load")
        await page.wait_for_timeout(300)
    finally:
        await browser.close()
        await pw.stop()
    assert counter.count == 2
    assert sorted(counter.hosts) == ["cdn.taboola.com", "securepubads.g.doubleclick.net"]
    assert passed_through == ["https://www.example-news.com/photo.jpg"]
