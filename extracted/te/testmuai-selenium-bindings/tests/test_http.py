"""Test the HTTP retry helper."""
import httpx
import pytest
import respx

from testmu_selenium._helpers._http import (
    TransientHTTPError,
    make_http_request_with_retry,
)


@pytest.fixture(autouse=True)
def _no_wait(monkeypatch):
    """Strip tenacity sleep so retry tests run instantly.

    The decorated function carries a `.retry` attribute (tenacity Retrying instance);
    swapping its `sleep` callable to a no-op preserves attempt counting without
    real backoff delays.
    """
    monkeypatch.setattr(make_http_request_with_retry.retry, "sleep", lambda _seconds: None)


@respx.mock
def test_get_success():
    respx.get("https://example.com/api").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    resp = make_http_request_with_retry("GET", "https://example.com/api", silent=True)
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}


@respx.mock
def test_post_with_json_body():
    route = respx.post("https://example.com/api").mock(return_value=httpx.Response(201))
    resp = make_http_request_with_retry(
        "POST", "https://example.com/api", json_data={"k": "v"}, silent=True
    )
    assert resp.status_code == 201
    # Verify the JSON body was actually sent
    assert route.called
    sent_request = route.calls.last.request
    assert sent_request.content == b'{"k":"v"}'


@respx.mock
def test_post_with_raw_data():
    route = respx.post("https://example.com/api").mock(return_value=httpx.Response(200))
    resp = make_http_request_with_retry(
        "POST", "https://example.com/api", data="raw-payload", silent=True
    )
    assert resp.status_code == 200
    assert route.calls.last.request.content == b"raw-payload"


@respx.mock
def test_5xx_retries_then_succeeds():
    route = respx.get("https://example.com/flaky").mock(side_effect=[
        httpx.Response(503),
        httpx.Response(200, json={"ok": True}),
    ])
    resp = make_http_request_with_retry("GET", "https://example.com/flaky", silent=True)
    assert resp.status_code == 200
    assert route.call_count == 2


@respx.mock
def test_4xx_does_not_retry():
    route = respx.get("https://example.com/notfound").mock(
        return_value=httpx.Response(404)
    )
    resp = make_http_request_with_retry(
        "GET", "https://example.com/notfound", silent=True
    )
    assert resp.status_code == 404
    assert route.call_count == 1


@respx.mock
def test_persistent_5xx_exhausts_and_raises_transient():
    """Tenacity is configured with stop_after_attempt(3) and reraise=True; after
    the 3rd attempt also returns 503, TransientHTTPError must propagate."""
    route = respx.get("https://example.com/dead").mock(
        return_value=httpx.Response(503)
    )
    with pytest.raises(TransientHTTPError) as exc_info:
        make_http_request_with_retry("GET", "https://example.com/dead", silent=True)
    assert exc_info.value.status_code == 503
    assert route.call_count == 3


@respx.mock
def test_transient_408_429_499_502_504_all_retry():
    """All transient codes in the set should trigger a retry path."""
    for code in (408, 429, 499, 502, 504):
        respx.reset()
        route = respx.get("https://example.com/x").mock(side_effect=[
            httpx.Response(code),
            httpx.Response(200),
        ])
        resp = make_http_request_with_retry(
            "GET", "https://example.com/x", silent=True
        )
        assert resp.status_code == 200, f"transient code {code} did not recover"
        assert route.call_count == 2, f"transient code {code} did not retry"


@respx.mock
def test_headers_and_auth_are_forwarded():
    route = respx.get("https://example.com/secure").mock(
        return_value=httpx.Response(200)
    )
    resp = make_http_request_with_retry(
        "GET",
        "https://example.com/secure",
        headers={"X-Custom": "yes"},
        auth=("user", "pass"),
        silent=True,
    )
    assert resp.status_code == 200
    sent = route.calls.last.request
    assert sent.headers.get("x-custom") == "yes"
    # httpx serializes basic auth into the Authorization header
    assert sent.headers.get("authorization", "").lower().startswith("basic ")
