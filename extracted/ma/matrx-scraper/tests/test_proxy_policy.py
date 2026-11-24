from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_scraper import proxy_health, scraper


@pytest.fixture(autouse=True)
def _clean_proxy_health() -> None:
    """Refusal memory is process-wide by design — never let it leak between
    tests, or a later test silently exercises the direct-first path."""
    proxy_health.reset_for_tests()
    yield
    proxy_health.reset_for_tests()


def _failed_response(reason: scraper.FailureReason) -> SimpleNamespace:
    return SimpleNamespace(
        failed=True,
        failed_primary_reason=reason,
        failed_reasons=[{reason: "failed"}],
    )


@pytest.mark.asyncio
async def test_proxy_fetch_never_falls_back_to_direct(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str | None] = []

    async def fake_fetch(
        url: str,
        request_type: scraper.RequestType,
        proxy: str | None,
        *_args: Any,
        **_kwargs: Any,
    ) -> SimpleNamespace:
        calls.append(proxy)
        return _failed_response(scraper.FailureReason.BAD_STATUS)

    monkeypatch.setenv("DATACENTER_PROXIES", "http://proxy-one,http://proxy-two")
    monkeypatch.setattr(scraper, "fetch", fake_fetch)
    monkeypatch.setattr(scraper.random, "choice", lambda values: values[0])

    response = await scraper.fetch_normally_with_proxy("https://example.com")

    assert response.failed is True
    assert calls == ["http://proxy-one", "http://proxy-two"]
    assert None not in calls


@pytest.mark.asyncio
async def test_proxy_fetch_tries_every_configured_attempt_before_exhaustion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str | None] = []
    captures: list[BaseException] = []

    async def fake_fetch(
        url: str,
        request_type: scraper.RequestType,
        proxy: str | None,
        *_args: Any,
        **_kwargs: Any,
    ) -> SimpleNamespace:
        calls.append(proxy)
        if len(calls) == 4:
            return SimpleNamespace(
                failed=False,
                failed_primary_reason=None,
                failed_reasons=[],
            )
        return _failed_response(scraper.FailureReason.PROXY_ERROR)

    async def fake_capture(exc: BaseException, **_kwargs: Any) -> None:
        captures.append(exc)

    monkeypatch.setenv(
        "DATACENTER_PROXIES",
        "http://proxy-one,http://proxy-two,http://proxy-two,http://proxy-three",
    )
    monkeypatch.setattr(scraper, "fetch", fake_fetch)
    monkeypatch.setattr(scraper.random, "choice", lambda values: values[0])
    monkeypatch.setattr(scraper.random, "shuffle", lambda values: None)
    monkeypatch.setattr("matrx_utils.capture_error", fake_capture)
    monkeypatch.setattr("matrx_utils.vcprint", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(scraper, "_proxy_pool_exhausted", False)

    response = await scraper.fetch_normally_with_proxy("https://example.com")

    assert response.failed is False
    assert calls == [
        "http://proxy-one",
        "http://proxy-two",
        "http://proxy-two",
        "http://proxy-three",
    ]
    assert captures == []


@pytest.mark.asyncio
async def test_repeated_rotating_gateway_gets_a_fresh_network_attempt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str | None] = []
    captures: list[BaseException] = []

    async def fake_fetch(*_args: Any, **kwargs: Any) -> SimpleNamespace:
        calls.append(kwargs.get("proxy") or _args[2])
        if len(calls) == 1:
            return _failed_response(scraper.FailureReason.PROXY_ERROR)
        return SimpleNamespace(failed=False, failed_primary_reason=None, failed_reasons=[])

    async def fake_capture(exc: BaseException, **_kwargs: Any) -> None:
        captures.append(exc)

    gateway = "http://rotating-paid-gateway"
    monkeypatch.setenv("DATACENTER_PROXIES", f"{gateway},{gateway}")
    monkeypatch.setattr(scraper, "fetch", fake_fetch)
    monkeypatch.setattr(scraper.random, "choice", lambda values: values[0])
    monkeypatch.setattr(scraper.random, "shuffle", lambda values: None)
    monkeypatch.setattr("matrx_utils.capture_error", fake_capture)
    monkeypatch.setattr("matrx_utils.vcprint", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(scraper, "_proxy_pool_exhausted", False)

    response = await scraper.fetch_normally_with_proxy("https://example.com")

    assert response.failed is False
    assert calls == [gateway, gateway]
    assert captures == []


@pytest.mark.asyncio
async def test_proxy_fetch_does_not_report_pool_outage_when_any_proxy_connects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captures: list[BaseException] = []
    outcomes = iter(
        [
            scraper.FailureReason.PROXY_ERROR,
            scraper.FailureReason.BAD_STATUS,
            scraper.FailureReason.PROXY_ERROR,
        ]
    )

    async def fake_fetch(*_args: Any, **_kwargs: Any) -> SimpleNamespace:
        return _failed_response(next(outcomes))

    async def fake_capture(exc: BaseException, **_kwargs: Any) -> None:
        captures.append(exc)

    monkeypatch.setenv(
        "DATACENTER_PROXIES",
        "http://proxy-one,http://proxy-two,http://proxy-three",
    )
    monkeypatch.setattr(scraper, "fetch", fake_fetch)
    monkeypatch.setattr(scraper.random, "choice", lambda values: values[0])
    monkeypatch.setattr(scraper.random, "shuffle", lambda values: None)
    monkeypatch.setattr("matrx_utils.capture_error", fake_capture)
    monkeypatch.setattr("matrx_utils.vcprint", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(scraper, "_proxy_pool_exhausted", False)

    await scraper.fetch_normally_with_proxy("https://example.com")

    assert captures == []


@pytest.mark.asyncio
async def test_proxy_fetch_fails_loudly_when_pool_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("DATACENTER_PROXIES", raising=False)

    with pytest.raises(
        scraper.ProxyConfigurationError,
        match="DATACENTER_PROXIES is missing or empty",
    ):
        await scraper.fetch_normally_with_proxy("https://example.com")


@pytest.mark.asyncio
async def test_proxy_auth_failure_is_classified_as_proxy_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_get(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
        raise RuntimeError("curl: (56) CONNECT tunnel failed, response 407")

    monkeypatch.setattr(scraper, "_curl_cffi_get_sync", fail_get)

    response = await scraper.fetch(
        "https://example.com",
        scraper.RequestType.NORMAL,
        "http://proxy",
    )

    assert response.failed_primary_reason == scraper.FailureReason.PROXY_ERROR


@pytest.mark.asyncio
async def test_proxy_pool_exhaustion_is_structured_once_without_error_log_noise(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captures: list[tuple[BaseException, str, dict[str, Any]]] = []
    prints: list[dict[str, Any]] = []

    async def fake_fetch(*_args: Any, **_kwargs: Any) -> SimpleNamespace:
        return _failed_response(scraper.FailureReason.PROXY_ERROR)

    async def fake_capture(exc: BaseException, *, kind: str, **kwargs: Any) -> None:
        captures.append((exc, kind, kwargs))

    def fake_vcprint(*_args: Any, **kwargs: Any) -> None:
        prints.append(kwargs)

    monkeypatch.setenv("DATACENTER_PROXIES", "http://proxy-one,http://proxy-two")
    monkeypatch.setattr(scraper, "fetch", fake_fetch)
    monkeypatch.setattr(scraper.random, "choice", lambda values: values[0])
    monkeypatch.setattr("matrx_utils.capture_error", fake_capture)
    monkeypatch.setattr("matrx_utils.vcprint", fake_vcprint)
    monkeypatch.setattr(scraper, "_proxy_pool_exhausted", False)

    response = await scraper.fetch_normally_with_proxy("https://example.com")
    repeated = await scraper.fetch_normally_with_proxy("https://example.org")

    assert response.failed_primary_reason == scraper.FailureReason.PROXY_ERROR
    assert repeated.failed_primary_reason == scraper.FailureReason.PROXY_ERROR
    assert len(captures) == 1
    exc, kind, kwargs = captures[0]
    assert isinstance(exc, scraper.ProxyPoolExhaustedError)
    assert str(exc) == "Configured proxy pool exhausted"
    assert kind == "scraper_proxy_pool_exhausted"
    # The SECOND refused destination is the evidence (one refused host proves nothing — 9e8a0ef6).
    assert kwargs["context"]["url"] == "https://example.org"
    assert kwargs["context"]["failure_reason"] == "proxy_error"
    # The capture carries pool telemetry, so an outage is diagnosable from the
    # error row alone instead of needing a live reproduction.
    assert kwargs["context"]["proxy_pool"]["proxy_refusals"] >= 1
    assert kwargs["context"]["proxy_pool"]["direct_fallbacks"] >= 1
    assert prints[-1]["color"] == "yellow"


@pytest.mark.asyncio
async def test_proxy_pool_exhaustion_capture_rearms_after_recovery(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captures: list[BaseException] = []
    # Two proxies per call, plus the DIRECT rescue attempt that now follows an
    # all-proxy-error round (see `scraper.direct_fallback_enabled`).
    # An outage is proven by TWO refused destinations (one refused host proves nothing — 9e8a0ef6).
    outcomes = iter(
        [
            scraper.FailureReason.PROXY_ERROR,
            scraper.FailureReason.PROXY_ERROR,
            scraper.FailureReason.REQUEST_ERROR,  # direct rescue also fails
            scraper.FailureReason.PROXY_ERROR,
            scraper.FailureReason.PROXY_ERROR,
            scraper.FailureReason.REQUEST_ERROR,  # direct rescue also fails
            scraper.FailureReason.BAD_STATUS,
            scraper.FailureReason.BAD_STATUS,
            scraper.FailureReason.PROXY_ERROR,
            scraper.FailureReason.PROXY_ERROR,
            scraper.FailureReason.REQUEST_ERROR,  # direct rescue also fails
            scraper.FailureReason.PROXY_ERROR,
            scraper.FailureReason.PROXY_ERROR,
            scraper.FailureReason.REQUEST_ERROR,  # direct rescue also fails
        ]
    )

    async def fake_fetch(*_args: Any, **_kwargs: Any) -> SimpleNamespace:
        return _failed_response(next(outcomes))

    async def fake_capture(exc: BaseException, **_kwargs: Any) -> None:
        captures.append(exc)

    monkeypatch.setenv("DATACENTER_PROXIES", "http://proxy-one,http://proxy-two")
    monkeypatch.setattr(scraper, "fetch", fake_fetch)
    monkeypatch.setattr(scraper.random, "choice", lambda values: values[0])
    monkeypatch.setattr("matrx_utils.capture_error", fake_capture)
    monkeypatch.setattr("matrx_utils.vcprint", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(scraper, "_proxy_pool_exhausted", False)

    # Distinct hosts: the refusal memory is per-host, and reusing one host
    # would send the later calls down the direct-first path instead.
    await scraper.fetch_normally_with_proxy("https://first.example/first")
    await scraper.fetch_normally_with_proxy("https://first-b.example/first")
    await scraper.fetch_normally_with_proxy("https://recovery.example/recovery")
    # A refusal moments after the pool carried a request is ONE destination
    # being declined, not exhaustion (system_error 586170ad). The pool is only
    # exhausted again once that carry has aged out of the refusal window.
    real_monotonic = proxy_health.time.monotonic
    monkeypatch.setattr(
        proxy_health.time,
        "monotonic",
        lambda: real_monotonic() + proxy_health.REFUSAL_MEMORY_SECONDS + 1,
    )
    await scraper.fetch_normally_with_proxy("https://second.example/second")
    await scraper.fetch_normally_with_proxy("https://second-b.example/second")

    assert len(captures) == 2


@pytest.mark.asyncio
async def test_host_refused_by_a_healthy_pool_is_not_pool_exhaustion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """2026-10-01 system_error 586170ad: the pool had carried 51 of 72 proxied
    requests, the vendor refused ONE destination (www.arlingtontx.gov), the
    direct fallback got the site's own bad status — and the row said
    "Configured proxy pool exhausted". A pool that is carrying other hosts is
    not exhausted, and the caller must get the site's real answer."""
    captures: list[tuple[BaseException, str, dict[str, Any]]] = []

    async def fake_fetch(
        url: str,
        _request_type: scraper.RequestType,
        proxy: str | None,
        *_args: Any,
        **_kwargs: Any,
    ) -> SimpleNamespace:
        if "arlingtontx.gov" not in url:
            return SimpleNamespace(
                failed=False, failed_primary_reason=None, failed_reasons=[]
            )
        if proxy is not None:
            return _failed_response(scraper.FailureReason.PROXY_ERROR)
        return _failed_response(scraper.FailureReason.BAD_STATUS)

    async def fake_capture(exc: BaseException, *, kind: str, **kwargs: Any) -> None:
        captures.append((exc, kind, kwargs))

    monkeypatch.setenv("DATACENTER_PROXIES", "http://proxy-one,http://proxy-two")
    monkeypatch.setattr(scraper, "fetch", fake_fetch)
    monkeypatch.setattr("matrx_utils.capture_error", fake_capture)
    monkeypatch.setattr("matrx_utils.vcprint", lambda *_a, **_k: None)
    monkeypatch.setattr(scraper, "_proxy_pool_exhausted", False)

    # The pool is healthy: it carries other destinations fine.
    for path in range(5):
        ok = await scraper.fetch_normally_with_proxy(f"https://news.example/{path}")
        assert ok.failed is False

    response = await scraper.fetch_normally_with_proxy(
        "https://www.arlingtontx.gov/News-Articles/2026/October/event"
    )

    # The caller gets the site's own answer, carried directly, and announced.
    assert response.failed_primary_reason == scraper.FailureReason.BAD_STATUS
    assert response.proxy_bypassed is True
    # And nothing claims the pool is exhausted.
    assert not any(isinstance(exc, scraper.ProxyPoolExhaustedError) for exc, _, _ in captures)
    snapshot = proxy_health.proxy_health_snapshot()
    assert snapshot["refused_hosts"] == ["www.arlingtontx.gov"]
    assert snapshot["direct_fallbacks"] == 1


@pytest.mark.asyncio
async def test_dead_pool_rescued_by_direct_is_telemetry_not_a_system_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A pool that carries nothing but whose every page the direct fallback
    delivers is pool-health telemetry (snapshot + warning log), never a
    system_error; the failed-direct case is the next test."""
    captures: list[tuple[BaseException, str, dict[str, Any]]] = []

    async def fake_fetch(
        _url: str,
        _request_type: scraper.RequestType,
        proxy: str | None,
        *_args: Any,
        **_kwargs: Any,
    ) -> SimpleNamespace:
        if proxy is not None:
            return _failed_response(scraper.FailureReason.PROXY_ERROR)
        return SimpleNamespace(failed=False, failed_primary_reason=None, failed_reasons=[])

    async def fake_capture(exc: BaseException, *, kind: str, **kwargs: Any) -> None:
        captures.append((exc, kind, kwargs))

    monkeypatch.setenv("DATACENTER_PROXIES", "http://proxy-one,http://proxy-two")
    monkeypatch.setattr(scraper, "fetch", fake_fetch)
    monkeypatch.setattr("matrx_utils.capture_error", fake_capture)
    monkeypatch.setattr("matrx_utils.vcprint", lambda *_a, **_k: None)
    monkeypatch.setattr(scraper, "_proxy_pool_exhausted", False)

    response = await scraper.fetch_normally_with_proxy("https://a.example/")
    # A second destination is the evidence the pool (not one host) is refused — 9e8a0ef6.
    await scraper.fetch_normally_with_proxy("https://b.example/")

    assert response.failed is False
    assert response.proxy_bypassed is True
    assert captures == []
    assert proxy_health.proxy_health_snapshot()["direct_fallbacks"] >= 2


@pytest.mark.asyncio
async def test_dead_pool_with_failed_direct_is_still_reported(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captures: list[tuple[BaseException, str, dict[str, Any]]] = []

    async def fake_fetch(
        _url: str,
        _request_type: scraper.RequestType,
        proxy: str | None,
        *_args: Any,
        **_kwargs: Any,
    ) -> SimpleNamespace:
        if proxy is not None:
            return _failed_response(scraper.FailureReason.PROXY_ERROR)
        return _failed_response(scraper.FailureReason.BAD_STATUS)

    async def fake_capture(exc: BaseException, *, kind: str, **kwargs: Any) -> None:
        captures.append((exc, kind, kwargs))

    monkeypatch.setenv("DATACENTER_PROXIES", "http://proxy-one,http://proxy-two")
    monkeypatch.setattr(scraper, "fetch", fake_fetch)
    monkeypatch.setattr("matrx_utils.capture_error", fake_capture)
    monkeypatch.setattr("matrx_utils.vcprint", lambda *_a, **_k: None)
    monkeypatch.setattr(scraper, "_proxy_pool_exhausted", False)

    await scraper.fetch_normally_with_proxy("https://a.example/")
    await scraper.fetch_normally_with_proxy("https://b.example/")

    assert len(captures) == 1
    assert captures[0][1] == "scraper_proxy_pool_exhausted"
    assert captures[0][2]["context"]["direct_rescued"] is False


@pytest.mark.asyncio
async def test_one_refused_host_on_a_cold_pool_is_not_pool_exhaustion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """2026-11-13 system_error 9e8a0ef6: a fresh server's first proxied request was a YouTube link — a
    destination our vendor always refuses — the direct fallback rescued it, and "Configured proxy pool
    exhausted" was still filed red because the pool had carried nothing yet. One refused destination proves
    nothing about the pool; a second, different one with still no carry does."""
    captures: list[BaseException] = []

    async def fake_fetch(url: str, _rt: Any, proxy: str | None, *_a: Any, **_k: Any) -> SimpleNamespace:
        if proxy is None and "youtube" in url:  # the direct rescue answers
            return SimpleNamespace(failed=False, failed_primary_reason=None, failed_reasons=[])
        if proxy is None:  # second destination: direct fails too, so the outage is real
            return _failed_response(scraper.FailureReason.BAD_STATUS)
        return _failed_response(scraper.FailureReason.PROXY_ERROR)

    async def fake_capture(exc: BaseException, **_kwargs: Any) -> None:
        captures.append(exc)

    monkeypatch.setenv("DATACENTER_PROXIES", "http://proxy-one,http://proxy-two")
    monkeypatch.setattr(scraper, "fetch", fake_fetch)
    monkeypatch.setattr(scraper.random, "choice", lambda values: values[0])
    monkeypatch.setattr(scraper.random, "shuffle", lambda values: None)
    monkeypatch.setattr("matrx_utils.capture_error", fake_capture)
    monkeypatch.setattr("matrx_utils.vcprint", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(scraper, "_proxy_pool_exhausted", False)

    rescued = await scraper.fetch_normally_with_proxy("https://www.youtube.com/watch?v=x")
    assert rescued.failed is False
    assert captures == []

    # A second, different destination refused with still no carry: now the pool is the problem.
    await scraper.fetch_normally_with_proxy("https://example.org/page")
    assert len(captures) == 1
    assert isinstance(captures[0], scraper.ProxyPoolExhaustedError)
