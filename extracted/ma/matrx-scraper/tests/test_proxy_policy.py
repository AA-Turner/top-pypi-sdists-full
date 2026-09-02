from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_scraper import scraper


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
    assert kwargs["context"] == {
        "url": "https://example.com",
        "failure_reason": "proxy_error",
    }
    assert prints[-1]["color"] == "yellow"


@pytest.mark.asyncio
async def test_proxy_pool_exhaustion_capture_rearms_after_recovery(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captures: list[BaseException] = []
    outcomes = iter(
        [
            scraper.FailureReason.PROXY_ERROR,
            scraper.FailureReason.PROXY_ERROR,
            scraper.FailureReason.BAD_STATUS,
            scraper.FailureReason.BAD_STATUS,
            scraper.FailureReason.PROXY_ERROR,
            scraper.FailureReason.PROXY_ERROR,
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

    await scraper.fetch_normally_with_proxy("https://example.com/first")
    await scraper.fetch_normally_with_proxy("https://example.com/recovery")
    await scraper.fetch_normally_with_proxy("https://example.com/second")

    assert len(captures) == 2
