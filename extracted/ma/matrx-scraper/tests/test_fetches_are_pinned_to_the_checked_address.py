"""The scraper's own HTTP fetches connect only to the address that passed the check.

``validate_public_http_url`` resolves a host and refuses non-public answers,
but a plain client then resolves AGAIN to connect. A name that answers public
the first time and private the second (DNS rebinding) walked straight past it,
and two fetches (the robots cache and the crawler's sitemap discovery) were
never checked at all. Every fetch here now goes through
``matrx_scraper.utils.url.public_http_client`` — the outbound guard with plain
http allowed, because crawling http sites is this package's job.

Use case: a dental group asks for an SEO crawl of its site. The site's own DNS
is the attacker's: ``rebind.harbordentalcare.com`` answers a public CDN
address to the validator, then a VPC address to the connection.

DNS and the wire are stubbed beneath httpx; the clients stay real.
"""

from __future__ import annotations

import ipaddress
import socket
from collections import Counter
from typing import Any

import httpcore
import pytest

_PUBLIC = "151.101.65.140"
_PRIVATE = "10.20.4.17"


@pytest.fixture
def wire(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    sent: list[str] = []
    lookups: Counter[str] = Counter()

    def getaddrinfo(host: Any, port: Any, *args: Any, **kwargs: Any):
        name = host.decode() if isinstance(host, bytes) else str(host)
        lookups[name] += 1
        if name == "rebind.harbordentalcare.com":
            ip = _PUBLIC if lookups[name] == 1 else _PRIVATE
        elif name == "intranet.harbordentalcare.com":
            ip = _PRIVATE
        else:
            ip = name
        try:
            ipaddress.ip_address(ip)
        except ValueError as exc:
            raise socket.gaierror(socket.EAI_NONAME, "Name or service not known") from exc
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, int(port or 0)))]

    async def getaddrinfo_async(self: Any, host: Any, port: Any, *args: Any, **kwargs: Any):
        return getaddrinfo(host, port)

    async def pool(_self: Any, request: httpcore.Request) -> httpcore.Response:
        sent.append(request.url.host.decode())
        return httpcore.Response(200, headers=[(b"content-type", b"text/plain")], content=b"User-agent: *\n")

    import asyncio

    monkeypatch.setattr(socket, "getaddrinfo", getaddrinfo)
    monkeypatch.setattr(asyncio.BaseEventLoop, "getaddrinfo", getaddrinfo_async)
    monkeypatch.setattr(httpcore.AsyncConnectionPool, "handle_async_request", pool)
    return sent


async def test_sitemap_crawl_never_connects_to_a_rebound_address(wire: list[str]) -> None:
    from matrx_scraper.sitemaps import crawl_sitemap_documents

    try:
        await crawl_sitemap_documents("https://rebind.harbordentalcare.com/")
    except Exception:  # noqa: BLE001 — the outcome shape is not under test; the wire is
        pass
    assert wire == []


async def test_robots_cache_never_fetches_an_internal_host(wire: list[str]) -> None:
    from matrx_scraper.crawler import _RobotsCache

    await _RobotsCache("MatrxScraperBot/0.1").can_fetch("https://intranet.harbordentalcare.com/hours")
    assert wire == []


async def test_crawler_sitemap_discovery_never_fetches_an_internal_host(wire: list[str]) -> None:
    from matrx_scraper.crawler import _discover_sitemap_urls

    await _discover_sitemap_urls("https://intranet.harbordentalcare.com/", user_agent="MatrxScraperBot/0.1")
    assert wire == []


async def test_crawler_probes_never_connect_to_a_rebound_address(wire: list[str]) -> None:
    from matrx_scraper.crawler import SiteCrawler, SiteCrawlerConfig

    crawler = SiteCrawler(
        "crawl-harbor-1", SiteCrawlerConfig(base_url="https://rebind.harbordentalcare.com/")
    )
    assert await crawler._probe_crawl_delay() is None
    assert await crawler._probe_platform() == (None, None)
    assert wire == []


async def test_image_evidence_never_connects_to_a_rebound_address(wire: list[str]) -> None:
    from matrx_scraper.image_evidence import enrich_image_inventory

    items: list[dict[str, Any]] = [{"src": "https://rebind.harbordentalcare.com/smile-gallery/before.jpg"}]
    await enrich_image_inventory(items)
    assert wire == []


async def test_preview_never_connects_to_a_rebound_address(
    wire: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    import matrx_scraper.preview as preview

    async def no_screenshot(url: str) -> None:
        return None

    monkeypatch.setattr(preview, "_take_homepage_screenshot", no_screenshot)
    await preview.quick_preview("https://rebind.harbordentalcare.com/")
    assert wire == []


async def test_a_public_site_is_still_fetched_and_pinned(wire: list[str]) -> None:
    from matrx_scraper.crawler import _RobotsCache

    assert await _RobotsCache("MatrxScraperBot/0.1").can_fetch(f"http://{_PUBLIC}/hours") is True
    assert wire == [_PUBLIC]
