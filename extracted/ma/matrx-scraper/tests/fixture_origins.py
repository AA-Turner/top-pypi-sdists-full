"""The ONE test-only allowance for a loopback fixture server: exactly its origin.

Every layer of the outbound check refuses 127.0.0.1, which is correct in
production and is what tests that crawl a local fixture site run into. This
lets EXACTLY the named origins through each layer and delegates every other
URL to the real check, so a fixture link that points anywhere else is still
refused exactly as production would refuse it. The guard itself is never
widened: nothing here touches a production module's code, only its bindings,
for the life of one test.

Layers covered (each binds the check by name):
  * matrx_utils.outbound_guard.resolve_public_address / _sync — every guarded
    client, the scrape() gate and assert_public_url_async;
  * matrx_scraper.scraper's own bindings of both — fetch(), the proxy path's
    early gate, curl's per-hop pin, httpx's proxied hop hook;
  * matrx_scraper.ai_browser.url_guard.validate_public_http_url — the browser
    request guard.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit


def origin_of(url: str) -> str:
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}".lower()


def allow_fixture_origins(monkeypatch: Any, *origins: str) -> None:
    from matrx_utils import outbound_guard

    import matrx_scraper.scraper as scraper
    from matrx_scraper.ai_browser import url_guard

    allowed = {origin_of(o) for o in origins}
    real_async = outbound_guard.resolve_public_address
    real_sync = outbound_guard.resolve_public_address_sync
    real_browser = url_guard.validate_public_http_url

    def _fixture_ip(url: str) -> str | None:
        if origin_of(url) in allowed:
            return urlsplit(url).hostname or ""
        return None

    async def resolve_async(url: str, *, allow_http: bool | None = None) -> str:
        ip = _fixture_ip(url)
        return ip if ip is not None else await real_async(url, allow_http=allow_http)

    def resolve_sync(url: str, *, allow_http: bool | None = None) -> str:
        ip = _fixture_ip(url)
        return ip if ip is not None else real_sync(url, allow_http=allow_http)

    async def browser_check(url: str) -> str:
        return url if _fixture_ip(url) is not None else await real_browser(url)

    monkeypatch.setattr(outbound_guard, "resolve_public_address", resolve_async)
    monkeypatch.setattr(outbound_guard, "resolve_public_address_sync", resolve_sync)
    monkeypatch.setattr(scraper, "resolve_public_address", resolve_async)
    monkeypatch.setattr(scraper, "resolve_public_address_sync", resolve_sync)
    monkeypatch.setattr(url_guard, "validate_public_http_url", browser_check)
