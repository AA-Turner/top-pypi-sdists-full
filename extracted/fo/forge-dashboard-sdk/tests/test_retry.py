"""Unit tests for the retry transport against a fake/mocked transport
(``httpx.MockTransport``), per rules/sdk-generation.md's "unit-test only
the hand-written parts" -- this never exercises a real network call or the
generated client.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from email.utils import format_datetime

import httpx
import pytest

from forge_dashboard.retry import (
    AsyncRetryTransport,
    RetryConfig,
    RetryTransport,
    _backoff_seconds,
    _retry_after_seconds,
    _should_retry,
)


def _counting_handler(statuses: list[int], headers: list[dict[str, str]] | None = None) -> httpx.MockTransport:
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        i = min(calls["n"], len(statuses) - 1)
        calls["n"] += 1
        h = headers[i] if headers else {}
        return httpx.Response(statuses[i], headers=h, request=request)

    transport = httpx.MockTransport(handler)
    transport.calls = calls  # type: ignore[attr-defined]
    return transport


def test_retries_5xx_then_succeeds(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []
    monkeypatch.setattr("forge_dashboard.retry.time.sleep", sleeps.append)

    mock = _counting_handler([500, 500, 200])
    retry_transport = RetryTransport(transport=mock, retry=RetryConfig(max_retries=3, base_seconds=0.01))
    request = httpx.Request("GET", "https://example.test/api/version")

    response = retry_transport.handle_request(request)

    assert response.status_code == 200
    assert mock.calls["n"] == 3  # type: ignore[attr-defined]
    assert len(sleeps) == 2


def test_never_retries_other_4xx(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []
    monkeypatch.setattr("forge_dashboard.retry.time.sleep", sleeps.append)

    mock = _counting_handler([404, 200])
    retry_transport = RetryTransport(transport=mock, retry=RetryConfig(max_retries=3, base_seconds=0.01))
    request = httpx.Request("GET", "https://example.test/api/repos/nope")

    response = retry_transport.handle_request(request)

    assert response.status_code == 404
    assert mock.calls["n"] == 1  # type: ignore[attr-defined]
    assert sleeps == []


def test_exhausts_max_retries_and_returns_last_response(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("forge_dashboard.retry.time.sleep", lambda _seconds: None)

    mock = _counting_handler([500, 500, 500, 500, 500])
    retry_transport = RetryTransport(transport=mock, retry=RetryConfig(max_retries=2, base_seconds=0.01))
    request = httpx.Request("GET", "https://example.test/api/version")

    response = retry_transport.handle_request(request)

    assert response.status_code == 500
    # first attempt + 2 retries
    assert mock.calls["n"] == 3  # type: ignore[attr-defined]


def test_retries_transport_error_then_succeeds(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []
    monkeypatch.setattr("forge_dashboard.retry.time.sleep", sleeps.append)

    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            raise httpx.ConnectError("connection reset", request=request)
        return httpx.Response(200, request=request)

    retry_transport = RetryTransport(
        transport=httpx.MockTransport(handler), retry=RetryConfig(max_retries=2, base_seconds=0.01)
    )
    request = httpx.Request("GET", "https://example.test/api/version")

    response = retry_transport.handle_request(request)

    assert response.status_code == 200
    assert calls["n"] == 2
    # Not a throwaway None -- a real computed backoff delay.
    assert len(sleeps) == 1
    assert isinstance(sleeps[0], float)
    assert sleeps[0] >= 0


def test_transport_error_exhausts_retries_after_correct_attempt_count(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("forge_dashboard.retry.time.sleep", lambda _seconds: None)

    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        raise httpx.ConnectError("connection reset", request=request)

    retry_transport = RetryTransport(
        transport=httpx.MockTransport(handler), retry=RetryConfig(max_retries=2, base_seconds=0.01)
    )

    with pytest.raises(httpx.ConnectError):
        retry_transport.handle_request(httpx.Request("GET", "https://example.test/api/version"))

    # first attempt + 2 retries, no more, no fewer -- pins the attempt
    # counter's increment (not a no-op or an off-by-N step) against the
    # configured max_retries.
    assert calls["n"] == 3


def test_retry_after_seconds_header_takes_priority_over_backoff(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []
    monkeypatch.setattr("forge_dashboard.retry.time.sleep", sleeps.append)

    mock = _counting_handler([429, 200], headers=[{"Retry-After": "7"}, {}])
    retry_transport = RetryTransport(transport=mock, retry=RetryConfig(max_retries=3, base_seconds=100.0))

    response = retry_transport.handle_request(httpx.Request("GET", "https://example.test/api/repos"))

    assert response.status_code == 200
    assert sleeps == [7.0]


def test_retry_after_seconds_helper_parses_http_date() -> None:
    future = datetime.now(UTC) + timedelta(seconds=5)
    header = format_datetime(future, usegmt=True)
    response = httpx.Response(429, headers={"Retry-After": header})

    delay = _retry_after_seconds(response)

    assert delay is not None
    assert 4.0 <= delay <= 5.5


def test_retry_after_seconds_helper_returns_none_when_absent() -> None:
    assert _retry_after_seconds(httpx.Response(500)) is None


def test_retry_after_seconds_helper_ignores_garbage() -> None:
    assert _retry_after_seconds(httpx.Response(429, headers={"Retry-After": "not-a-date"})) is None


def test_retry_after_seconds_helper_parses_naive_http_date() -> None:
    # A date string with no zone parses to a naive datetime -- exercises
    # the tzinfo-is-None branch that assumes UTC.
    response = httpx.Response(429, headers={"Retry-After": "Mon, 01 Jan 2035 00:00:00"})

    delay = _retry_after_seconds(response)

    assert delay is not None
    assert delay > 0


def test_retry_after_seconds_helper_clamps_past_date_to_zero() -> None:
    past = datetime.now(UTC) - timedelta(seconds=30)
    header = format_datetime(past, usegmt=True)

    assert _retry_after_seconds(httpx.Response(429, headers={"Retry-After": header})) == 0.0


def test_should_retry_raises_without_response_or_exception() -> None:
    with pytest.raises(ValueError) as exc_info:
        _should_retry(0, RetryConfig(), None, None)
    assert str(exc_info.value) == "_should_retry needs a response or an exception"


def test_backoff_seconds_formula(monkeypatch: pytest.MonkeyPatch) -> None:
    config = RetryConfig(max_retries=5, base_seconds=1.0)

    # Pin jitter to the low end of random.uniform(0, backoff): result is
    # exactly backoff / 2, so this also nails down the exponent (2.0**attempt,
    # not 2.0*attempt -- degenerate at attempt=2) and the "/ 2" divisor.
    monkeypatch.setattr("forge_dashboard.retry.random.uniform", lambda lo, _hi: lo)
    assert _backoff_seconds(0, config) == pytest.approx(0.5)
    assert _backoff_seconds(1, config) == pytest.approx(1.0)
    assert _backoff_seconds(3, config) == pytest.approx(4.0)

    # Pin jitter to the high end: result is exactly backoff.
    monkeypatch.setattr("forge_dashboard.retry.random.uniform", lambda _lo, hi: hi)
    assert _backoff_seconds(0, config) == pytest.approx(1.0)
    assert _backoff_seconds(1, config) == pytest.approx(2.0)


def test_async_retries_5xx_then_succeeds(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    monkeypatch.setattr("forge_dashboard.retry.asyncio.sleep", fake_sleep)

    calls = {"n": 0}

    async def handler(request: httpx.Request) -> httpx.Response:
        i = min(calls["n"], 2)
        calls["n"] += 1
        return httpx.Response([500, 500, 200][i], request=request)

    transport = AsyncRetryTransport(
        transport=httpx.MockTransport(handler), retry=RetryConfig(max_retries=3, base_seconds=0.01)
    )

    async def run() -> httpx.Response:
        return await transport.handle_async_request(httpx.Request("GET", "https://example.test/api/version"))

    response = asyncio.run(run())

    assert response.status_code == 200
    assert calls["n"] == 3
    assert len(sleeps) == 2


def test_async_never_retries_other_4xx() -> None:
    calls = {"n": 0}

    async def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(403, request=request)

    transport = AsyncRetryTransport(
        transport=httpx.MockTransport(handler), retry=RetryConfig(max_retries=3, base_seconds=0.01)
    )

    async def run() -> httpx.Response:
        return await transport.handle_async_request(httpx.Request("GET", "https://example.test/api/repos"))

    response = asyncio.run(run())

    assert response.status_code == 403
    assert calls["n"] == 1


def test_async_retries_transport_error_then_succeeds(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    monkeypatch.setattr("forge_dashboard.retry.asyncio.sleep", fake_sleep)

    calls = {"n": 0}

    async def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            raise httpx.ConnectError("connection reset", request=request)
        return httpx.Response(200, request=request)

    transport = AsyncRetryTransport(
        transport=httpx.MockTransport(handler), retry=RetryConfig(max_retries=2, base_seconds=0.01)
    )

    async def run() -> httpx.Response:
        return await transport.handle_async_request(httpx.Request("GET", "https://example.test/api/version"))

    response = asyncio.run(run())

    assert response.status_code == 200
    assert calls["n"] == 2
    assert len(sleeps) == 1
    assert isinstance(sleeps[0], float)


def test_async_transport_error_exhausts_retries_after_correct_attempt_count(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_sleep(_seconds: float) -> None:
        return None

    monkeypatch.setattr("forge_dashboard.retry.asyncio.sleep", fake_sleep)

    calls = {"n": 0}

    async def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        raise httpx.ConnectError("connection reset", request=request)

    transport = AsyncRetryTransport(
        transport=httpx.MockTransport(handler), retry=RetryConfig(max_retries=2, base_seconds=0.01)
    )

    async def run() -> httpx.Response:
        return await transport.handle_async_request(httpx.Request("GET", "https://example.test/api/version"))

    with pytest.raises(httpx.ConnectError):
        asyncio.run(run())

    assert calls["n"] == 3


def test_async_exhausts_max_retries_and_returns_last_response(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    monkeypatch.setattr("forge_dashboard.retry.asyncio.sleep", fake_sleep)

    calls = {"n": 0}

    async def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        # A Retry-After header makes the delay depend on *this* response
        # object specifically -- a huge base_seconds means any fallback
        # to the generic backoff (or to no response at all) would sleep
        # far longer than 9 seconds, so pytest.approx below would fail.
        return httpx.Response(500, headers={"Retry-After": "9"}, request=request)

    transport = AsyncRetryTransport(
        transport=httpx.MockTransport(handler), retry=RetryConfig(max_retries=2, base_seconds=1000.0)
    )

    async def run() -> httpx.Response:
        return await transport.handle_async_request(httpx.Request("GET", "https://example.test/api/version"))

    response = asyncio.run(run())

    assert response.status_code == 500
    # first attempt + 2 retries -- pins the attempt counter's starting
    # value and increment against max_retries, not just the eventual
    # status code (a wrong counter can still coincidentally return the
    # same last response with a different call count).
    assert calls["n"] == 3
    assert sleeps == [9.0, 9.0]


def test_default_sync_transport_is_a_real_http_transport() -> None:
    assert isinstance(RetryTransport()._transport, httpx.HTTPTransport)


def test_default_async_transport_is_a_real_http_transport() -> None:
    assert isinstance(AsyncRetryTransport()._transport, httpx.AsyncHTTPTransport)


def test_sync_transport_error_raises_once_retries_exhausted(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("forge_dashboard.retry.time.sleep", lambda _seconds: None)

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection reset", request=request)

    retry_transport = RetryTransport(
        transport=httpx.MockTransport(handler), retry=RetryConfig(max_retries=1, base_seconds=0.01)
    )

    with pytest.raises(httpx.ConnectError):
        retry_transport.handle_request(httpx.Request("GET", "https://example.test/api/version"))


def test_close_and_aclose_delegate_to_wrapped_transport() -> None:
    closed = {"sync": False, "async": False}

    class FakeSyncTransport(httpx.BaseTransport):
        def handle_request(self, request: httpx.Request) -> httpx.Response:  # pragma: no cover - unused
            raise NotImplementedError

        def close(self) -> None:
            closed["sync"] = True

    class FakeAsyncTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request: httpx.Request) -> httpx.Response:  # pragma: no cover - unused
            raise NotImplementedError

        async def aclose(self) -> None:
            closed["async"] = True

    RetryTransport(transport=FakeSyncTransport()).close()
    asyncio.run(AsyncRetryTransport(transport=FakeAsyncTransport()).aclose())

    assert closed == {"sync": True, "async": True}
