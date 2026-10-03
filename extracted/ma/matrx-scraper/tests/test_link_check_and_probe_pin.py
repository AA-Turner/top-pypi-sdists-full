"""The link checker and the site probe connect only to addresses that passed the check.

``check_urls`` is THE link checker (the site crawler and outreach broken-link
prospecting both call it) and checks the outbound hrefs of pages we do not
own. ``probe_site`` reads a site's robots, TLS and URL variants. Use case: an
SEO crawl of Harbor Dental Care.
"""

from __future__ import annotations

import ipaddress
import socket
from typing import Any

import httpcore
import pytest

from _loopback_target import start_target

_HOST = "www.harbordentalcare.com"
_IP = "151.101.65.140"


@pytest.fixture
def stable_public_dns(monkeypatch: pytest.MonkeyPatch) -> None:
    import asyncio

    def getaddrinfo(host: Any, port: Any, *args: Any, **kwargs: Any):
        name = host.decode() if isinstance(host, bytes) else str(host)
        ip = _IP if name == _HOST else name
        ipaddress.ip_address(ip)
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, int(port or 0)))]

    async def loop_getaddrinfo(_loop: Any, host: Any, port: Any, *args: Any, **kwargs: Any):
        return getaddrinfo(host, port)

    monkeypatch.setattr(socket, "getaddrinfo", getaddrinfo)
    monkeypatch.setattr(asyncio.BaseEventLoop, "getaddrinfo", loop_getaddrinfo)


@pytest.fixture
def wire(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, str]]:
    sent: list[tuple[str, str]] = []

    async def pool(_self: Any, request: httpcore.Request) -> httpcore.Response:
        sent.append((request.url.host.decode(), dict(request.headers).get(b"Host", b"").decode()))
        return httpcore.Response(200, headers=[(b"content-type", b"text/plain")], content=b"User-agent: *\n")

    monkeypatch.setattr(httpcore.AsyncConnectionPool, "handle_async_request", pool)
    return sent


async def test_check_urls_never_reaches_our_loopback() -> None:
    from matrx_scraper.web_crawl.link_check import check_urls

    target, stop = start_target()
    try:
        statuses = await check_urls([target.url], per_host_spacing_s=0.0)
    finally:
        stop.set()

    assert target.accepted == []
    assert statuses.get(target.url) != 200


async def test_check_urls_connects_to_the_checked_ip(stable_public_dns: None, wire) -> None:
    from matrx_scraper.web_crawl.link_check import check_urls

    await check_urls([f"https://{_HOST}/new-patient-specials"], per_host_spacing_s=0.0)

    assert wire and set(wire) == {(_IP, _HOST)}


async def test_probe_site_connects_to_the_checked_ip(
    stable_public_dns: None, wire, monkeypatch: pytest.MonkeyPatch
) -> None:
    from matrx_scraper.web_crawl import site_probe as sp

    async def no_tls(*args: Any, **kwargs: Any) -> None:
        return None  # the TLS capture opens its own socket; not the HTTP path under test

    monkeypatch.setattr(sp, "_capture_tls", no_tls)

    await sp.probe_site(f"https://{_HOST}/", [f"https://{_HOST}/services"])

    assert wire and set(wire) == {(_IP, _HOST)}
