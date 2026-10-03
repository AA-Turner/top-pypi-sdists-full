"""Each scraper engine connects to the IP its check approved, hop by hop.

Unlike the rebinding tests (where the transport's own check sees the private
answer and refuses, so a REMOVED pin is never exercised), DNS here stays
public and the wire records the address it was told to connect to. A removed
pin shows up as the hostname reaching the wire instead of the checked IP.

Use case: an SEO crawl of a dental group's site, ``www.harbordentalcare.com``.
"""

from __future__ import annotations

import ipaddress
import socket
from typing import Any

import httpcore
import pytest

from _loopback_target import SECRET, start_target

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

    async def getaddrinfo_async(self: Any, host: Any, port: Any, *args: Any, **kwargs: Any):
        return getaddrinfo(host, port)

    monkeypatch.setattr(socket, "getaddrinfo", getaddrinfo)
    monkeypatch.setattr(asyncio.BaseEventLoop, "getaddrinfo", getaddrinfo_async)


# ── httpx engine (direct) ────────────────────────────────────────────────────


async def test_httpx_engine_connects_to_the_checked_ip_with_the_real_host_header(
    stable_public_dns: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    from matrx_scraper.scraper import RequestType, fetch

    wire: list[tuple[str, str, Any]] = []

    async def pool(_self: Any, request: httpcore.Request) -> httpcore.Response:
        wire.append(
            (
                request.url.host.decode(),
                dict(request.headers).get(b"Host", b"").decode(),
                request.extensions.get("sni_hostname"),
            )
        )
        return httpcore.Response(
            200,
            headers=[(b"content-type", b"text/html")],
            content=b"<html><body><main>" + b"Gentle family dentistry in Harbor. " * 20 + b"</main></body></html>",
        )

    monkeypatch.setattr(httpcore.AsyncConnectionPool, "handle_async_request", pool)

    response = await fetch(f"https://{_HOST}/services", RequestType.NORMAL, None, use_curl_cffi=False)

    assert response.status_code == 200
    assert wire == [(_IP, _HOST, _HOST)]


# ── curl_cffi engine (direct): CURLOPT_RESOLVE per hop ───────────────────────


class _CurlResp:
    def __init__(self, url: str, status: int, location: str | None = None) -> None:
        self.url = url
        self.status_code = status
        self.headers = {"content-type": "text/html", **({"location": location} if location else {})}
        self.infos = {}
        self.text = "<html><body>" + "Cleanings and whitening. " * 20 + "</body></html>"
        self.content = self.text.encode()


@pytest.fixture
def curl_wire(monkeypatch: pytest.MonkeyPatch):
    """Stands in for libcurl (a dependency) — records what each hop was told."""
    import matrx_scraper.scraper as scraper

    if not scraper.CURL_CFFI_AVAILABLE:
        pytest.skip("curl_cffi not installed")
    hops: list[dict[str, Any]] = []
    script: dict[str, _CurlResp] = {}

    class _Session:
        def __init__(self, **kwargs: Any) -> None:
            self.curl_options: dict[Any, Any] = {}

        def __enter__(self):
            return self

        def __exit__(self, *a: Any) -> None:
            return None

        def get(self, url: str, **kwargs: Any) -> _CurlResp:
            hops.append({"url": url, "curl_options": dict(self.curl_options), "proxies": kwargs.get("proxies")})
            return script[url]

    monkeypatch.setattr(scraper, "CurlCffiSession", _Session)
    return hops, script


async def test_curl_engine_pins_every_hop_to_its_checked_ip(stable_public_dns: None, curl_wire) -> None:
    from curl_cffi import CurlOpt
    from matrx_scraper.scraper import RequestType, fetch

    hops, script = curl_wire
    first, second = f"http://{_HOST}/old-services", f"https://{_HOST}/services"
    script[first] = _CurlResp(first, 301, location=second)
    script[second] = _CurlResp(second, 200)

    response = await fetch(first, RequestType.NORMAL, None)

    assert response.status_code == 200
    assert [h["curl_options"].get(CurlOpt.RESOLVE) for h in hops] == [
        [f"{_HOST}:80:{_IP}"],
        [f"{_HOST}:443:{_IP}"],
    ]


async def test_curl_engine_refuses_a_redirect_hop_into_the_vpc(stable_public_dns: None, curl_wire) -> None:
    from matrx_scraper.scraper import FailureReason, RequestType, fetch

    hops, script = curl_wire
    first = f"https://{_HOST}/patient-portal"
    script[first] = _CurlResp(first, 302, location="http://10.20.4.17/admin")

    response = await fetch(first, RequestType.NORMAL, None)

    assert [h["url"] for h in hops] == [first]
    assert response.failed_primary_reason == FailureReason.ADDRESS_REFUSED


async def test_curl_engine_through_a_proxy_still_checks_every_hop(stable_public_dns: None, curl_wire) -> None:
    from matrx_scraper.scraper import FailureReason, RequestType, fetch

    hops, script = curl_wire
    first = f"https://{_HOST}/patient-portal"
    script[first] = _CurlResp(first, 302, location="http://169.254.169.254/latest/meta-data/")

    response = await fetch(first, RequestType.NORMAL, "http://proxy.datacenter.invalid:3128")

    assert [h["url"] for h in hops] == [first]
    assert hops[0]["curl_options"] == {}  # the proxy resolves; nothing of ours to pin
    assert response.failed_primary_reason == FailureReason.ADDRESS_REFUSED


# ── httpx engine through a proxy: the request hook re-checks every hop ──────


async def test_httpx_engine_through_a_proxy_refuses_a_redirect_into_the_vpc(
    stable_public_dns: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    import httpx

    from matrx_scraper.scraper import FailureReason, RequestType, fetch

    sent: list[str] = []

    class _ProxyTransport(httpx.AsyncBaseTransport):
        def __init__(self, *a: Any, **k: Any) -> None: ...

        async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
            sent.append(str(request.url))
            return httpx.Response(302, headers={"location": "http://10.20.4.17/admin"}, request=request)

    # The proxy's wire (a dependency): httpx builds its proxy transport from
    # the class bound in its client module.
    import httpx._client as httpx_client

    monkeypatch.setattr(httpx_client, "AsyncHTTPTransport", _ProxyTransport)

    response = await fetch(
        f"https://{_HOST}/patient-portal",
        RequestType.NORMAL,
        "http://proxy.datacenter.invalid:3128",
        use_curl_cffi=False,
    )

    assert sent == [f"https://{_HOST}/patient-portal"]
    assert response.failed_primary_reason == FailureReason.ADDRESS_REFUSED


# ── the browser pool: Playwright route interception, real Chromium ──────────


async def test_browser_pool_aborts_navigation_to_our_loopback() -> None:
    from matrx_scraper.browser_pool import PLAYWRIGHT_AVAILABLE, PlaywrightBrowserPool

    if not PLAYWRIGHT_AVAILABLE:
        pytest.skip("playwright not installed")
    target, stop = start_target()
    pool = PlaywrightBrowserPool(pool_size=1)
    try:
        await pool.start()
        try:
            content, *_ = await pool.fetch(target.url, timeout_ms=8000)
        except Exception:  # noqa: BLE001 — an aborted navigation raises; that is the refusal
            content = ""
    finally:
        await pool.stop()
        stop.set()

    assert target.accepted == []
    assert SECRET not in content
