"""A numeric host in any non-canonical form is refused before any engine sees it.

The bypass (WF-027, final verifier): on macOS ``getaddrinfo('0177.0.0.1')``
reads the leading-zero octet as DECIMAL (177.0.0.1, public) while curl reads it
as OCTAL (127.0.0.1) and treats the host as an IP literal, so CURLOPT_RESOLVE
never applied — a direct scrape returned the planted secret. The rule now: a
host that looks numeric must be canonical dotted-decimal, or it is refused
outright, never "resolved to see". A real loopback server holds the secret and
records every connection it accepts.
"""

from __future__ import annotations

import pytest

from _loopback_target import SECRET, start_refusing_proxy, start_target

FORMS = ["0177.0.0.1", "0x7f.0.0.1", "017700000001", "127.000.000.001", "0127.0.0.1", "127.1", "0x7f.1"]


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


@pytest.mark.parametrize("host", FORMS)
def test_the_guard_refuses_every_noncanonical_numeric_host(host: str) -> None:
    from matrx_utils import outbound_guard as og

    for url in (f"http://{host}:8080/admin", f"https://{host}/admin"):
        with pytest.raises(og.OutboundUrlRefused) as caught:
            og.check_url_shape(url, allow_http=True)
        assert str(caught.value) == og.NUMERIC_HOST_SENTENCE


@pytest.mark.parametrize("host", ["151.101.65.140", "8.8.8.8", "www.harbordentalcare.com", "bad.cafe", "0x.example"])
def test_canonical_addresses_and_names_are_not_numeric_refusals(host: str) -> None:
    from matrx_utils import outbound_guard as og

    assert og.check_url_shape(f"https://{host}/", allow_http=True) == f"https://{host}/"


@pytest.mark.parametrize("host", FORMS)
async def test_a_direct_scrape_never_reaches_loopback_through_a_numeric_form(target, host: str) -> None:
    from matrx_scraper import scrape

    result = await scrape(url=f"http://{host}:{target.port}/admin", use_proxy=False, escalate=False)

    assert target.accepted == []
    assert SECRET not in (result.text_data or "") + (result.raw_text or "")
    assert result.failure_reason == "address_refused"


@pytest.mark.parametrize("use_curl_cffi", [True, False], ids=["curl", "httpx"])
@pytest.mark.parametrize("host", FORMS)
async def test_each_http_engine_refuses_a_numeric_form(target, host: str, use_curl_cffi: bool) -> None:
    from matrx_scraper.scraper import FailureReason, RequestType, fetch

    response = await fetch(f"http://{host}:{target.port}/admin", RequestType.NORMAL, None, use_curl_cffi=use_curl_cffi)

    assert target.accepted == []
    assert SECRET not in (response.content or "")
    assert response.failed_primary_reason == FailureReason.ADDRESS_REFUSED


@pytest.mark.parametrize("host", ["0177.0.0.1", "0x7f.0.0.1", "127.1"])
async def test_the_browser_engine_refuses_a_numeric_form(target, host: str) -> None:
    from matrx_scraper.browser_pool import PLAYWRIGHT_AVAILABLE, PlaywrightBrowserPool
    from matrx_scraper.scraper import RequestType, fetch

    if not PLAYWRIGHT_AVAILABLE:
        pytest.skip("playwright not installed")
    url = f"http://{host}:{target.port}/admin"
    response = await fetch(url, RequestType.BROWSER, None)
    assert SECRET not in (response.content or "")

    pool = PlaywrightBrowserPool(pool_size=1)
    try:
        await pool.start()
        try:
            content, *_ = await pool.fetch(url, timeout_ms=8000)
        except Exception:  # noqa: BLE001 — an aborted navigation raises; that is the refusal
            content = ""
    finally:
        await pool.stop()

    assert target.accepted == []
    assert SECRET not in content


@pytest.mark.parametrize("host", ["0177.0.0.1", "0x7f.0.0.1"])
async def test_a_proxy_refused_numeric_form_never_falls_back_direct(
    target, host: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    from matrx_scraper.scraper import fetch_normally_with_proxy

    proxy_url, stop = start_refusing_proxy()
    try:
        monkeypatch.setenv("DATACENTER_PROXIES", proxy_url)
        response = await fetch_normally_with_proxy(f"https://{host}:{target.port}/admin")
    finally:
        stop.set()

    assert target.accepted == []
    assert getattr(response, "proxy_bypassed", False) is False


def test_curl_never_gets_a_literal_host_other_than_the_checked_ip(monkeypatch: pytest.MonkeyPatch) -> None:
    # Belt and braces, independent of the host rule: curl connects to a literal
    # IP host as-is and ignores CURLOPT_RESOLVE, so the hop pin refuses any
    # literal that is not exactly the address the check approved — here a
    # check (stubbed to the macOS decimal reading) says 177.0.0.1 for a host
    # curl would read as 127.0.0.1.
    import matrx_scraper.scraper as scraper
    from matrx_utils.outbound_guard import OutboundUrlRefused

    monkeypatch.setattr(scraper, "resolve_public_address_sync", lambda url, allow_http=None: "177.0.0.1")
    monkeypatch.setattr(scraper.ipaddress, "ip_address", _lenient_ip_address(scraper.ipaddress.ip_address))

    with pytest.raises(OutboundUrlRefused):
        scraper._curl_pin_options("http://0177.0.0.1:8080/admin", direct=True)


def _lenient_ip_address(real):
    """Reads a leading-zero octet as OCTAL, as curl does (Python refuses it)."""
    import socket

    def parse(value):
        try:
            return real(value)
        except ValueError:
            return real(socket.inet_ntoa(socket.inet_aton(value)))

    return parse


# ── the rule holds on its own: Unicode look-alike digits, IPv6-embedded forms ─

UNICODE_FORMS = ["０１７７.0.0.1", "0１77.0.0.1", "０ｘ７ｆ.1"]


@pytest.mark.parametrize("host", UNICODE_FORMS)
def test_the_guard_refuses_fullwidth_numeric_hosts(host: str) -> None:
    # NFKC folds fullwidth digits/letters to ASCII — and so do resolvers (macOS
    # getaddrinfo read "０１７７.0.0.1" as 177.0.0.1). The pattern must see what
    # they see.
    from matrx_utils import outbound_guard as og

    with pytest.raises(og.OutboundUrlRefused) as caught:
        og.check_url_shape(f"http://{host}:8080/admin", allow_http=True)
    assert str(caught.value) == og.NUMERIC_HOST_SENTENCE


@pytest.mark.parametrize("host", UNICODE_FORMS)
async def test_a_direct_scrape_refuses_fullwidth_numeric_hosts(target, host: str) -> None:
    from matrx_scraper import scrape

    result = await scrape(url=f"http://{host}:{target.port}/admin", use_proxy=False, escalate=False)

    assert target.accepted == []
    assert SECRET not in (result.text_data or "") + (result.raw_text or "")
    assert result.failure_reason == "address_refused"


def test_a_real_internationalized_name_is_not_a_numeric_refusal() -> None:
    from matrx_utils import outbound_guard as og

    assert og.check_url_shape("https://zahnarzt-müller.de/termine", allow_http=True)


@pytest.mark.parametrize("host", ["[::ffff:0177.0.0.1]", "[::ffff:127.1]", "[::ffff:0x7f.0.0.1]"])
async def test_an_ipv6_embedded_noncanonical_form_is_a_refusal_not_an_exception(target, host: str) -> None:
    from matrx_utils import outbound_guard as og

    from matrx_scraper.scraper import FailureReason, RequestType, fetch

    with pytest.raises(og.OutboundUrlRefused):
        og.check_url_shape(f"http://{host}:{target.port}/admin", allow_http=True)

    response = await fetch(f"http://{host}:{target.port}/admin", RequestType.NORMAL, None)

    assert target.accepted == []
    assert response.failed_primary_reason == FailureReason.ADDRESS_REFUSED
    assert response.failed_reasons and list(response.failed_reasons[0].values())[0].endswith(".")
