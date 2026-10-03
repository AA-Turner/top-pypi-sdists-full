"""The scraper core never fetches an address inside our own network.

Break caught: ``scrape()`` / ``fetch()`` / ``fetch_normally_with_proxy()`` send
a request (direct, or as the direct fallback after the proxy pool refuses) to
loopback, the VPC or the metadata service. A real loopback server with a
planted secret is the target; it records every connection it accepts.
"""

from __future__ import annotations

import pytest

from _loopback_target import SECRET, start_refusing_proxy, start_target


@pytest.fixture
def target():
    t, stop = start_target()
    yield t
    stop.set()


@pytest.fixture(autouse=True)
def _fresh_proxy_memory():
    from matrx_scraper import proxy_health

    proxy_health.reset_for_tests()
    yield
    proxy_health.reset_for_tests()


async def test_a_direct_scrape_of_loopback_is_refused_and_never_connects(target) -> None:
    from matrx_scraper import scrape

    result = await scrape(url=target.url, use_proxy=False, escalate=False)

    assert target.accepted == []
    assert SECRET not in (result.text_data or "") + (result.raw_text or "")
    assert result.success is False
    assert result.failure_reason == "address_refused"


async def test_a_direct_fetch_of_loopback_is_refused_and_never_connects(target) -> None:
    from matrx_scraper.scraper import FailureReason, RequestType, fetch

    response = await fetch(target.url, RequestType.NORMAL, None)

    assert target.accepted == []
    assert SECRET not in (response.content or "")
    assert response.failed_primary_reason == FailureReason.ADDRESS_REFUSED


async def test_the_go_direct_first_path_after_a_pool_refusal_never_connects(
    target, monkeypatch: pytest.MonkeyPatch
) -> None:
    from matrx_scraper import proxy_health
    from matrx_scraper.scraper import fetch_normally_with_proxy

    monkeypatch.setenv("DATACENTER_PROXIES", "http://proxy.datacenter.invalid:3128")
    # The pool refused this host minutes ago (real refusal memory, not a stub).
    proxy_health.record_proxy_refusal(target.url, "proxy_error")

    response = await fetch_normally_with_proxy(target.url)

    assert target.accepted == []
    assert SECRET not in (response.content or "")


async def test_a_proxy_refused_internal_address_never_falls_back_direct(
    target, monkeypatch: pytest.MonkeyPatch
) -> None:
    from matrx_scraper.scraper import fetch_normally_with_proxy

    proxy_url, stop = start_refusing_proxy()
    try:
        monkeypatch.setenv("DATACENTER_PROXIES", proxy_url)
        response = await fetch_normally_with_proxy(target.https_url)
    finally:
        stop.set()

    # Before: every proxy refused the CONNECT, so the core retried DIRECT and
    # connected to our own loopback.
    assert target.accepted == []
    assert getattr(response, "proxy_bypassed", False) is False


async def test_fetch_refuses_before_any_engine_is_started(target, monkeypatch: pytest.MonkeyPatch) -> None:
    # The gate's own job: a refused address never reaches an engine at all
    # (no curl handle, no Chromium launch) — not just refused by one later.
    import matrx_scraper.scraper as scraper

    started: list[str] = []

    def no_engine(*args, **kwargs):
        started.append("curl")
        raise AssertionError("an engine was started for a refused address")

    monkeypatch.setattr(scraper, "_curl_cffi_get_sync", no_engine)
    monkeypatch.setattr(scraper, "async_playwright", lambda: started.append("browser"))

    for request_type in (scraper.RequestType.NORMAL, scraper.RequestType.BROWSER):
        response = await scraper.fetch(target.url, request_type, None)
        assert response.failed_primary_reason == scraper.FailureReason.ADDRESS_REFUSED

    assert started == []
    assert target.accepted == []


async def test_a_cached_copy_of_an_internal_page_is_never_served(target) -> None:
    # The scrape gate's own job: it runs BEFORE the cache, so a page stored
    # under an address we now refuse is never handed back.
    from matrx_scraper import scrape

    class _Cache:
        async def get(self, key: str, **kwargs):
            return {
                "url": target.url,
                "content_type": "html",
                "content": {"text_data": f"Service token: {SECRET}", "engine": "http"},
            }

        async def set(self, *args, **kwargs) -> None:
            return None

    result = await scrape(url=target.url, use_proxy=False, escalate=False, cache=_Cache())

    assert result.failure_reason == "address_refused"
    assert SECRET not in (result.text_data or "")
