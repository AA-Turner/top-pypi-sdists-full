from __future__ import annotations

import socket
import ssl
from types import SimpleNamespace
from unittest.mock import AsyncMock

import httpx
import pytest
import pytest_asyncio

from runta import ApiError, PatchRuntimeResourceRequests, PatchRuntimeResources
from runta._internal.async_http import _AsyncHttpClient
from runta._internal.sync_http import _SyncHttpClient
from test_openapi_transport import _runtime_json
from http_mock import set_handler


@pytest_asyncio.fixture(params=[False, True], ids=["sync", "async"])
async def case(request, monkeypatch):
    asynchronous = request.param
    clock = SimpleNamespace(now=0.0, sleeps=[])

    def sleep(delay):
        clock.sleeps.append(delay)
        clock.now += delay

    monkeypatch.setattr("runta._internal.retry.time.monotonic", lambda: clock.now)
    monkeypatch.setattr("runta._internal.retry.time.time", lambda: 1700000000.0)
    monkeypatch.setattr("runta._internal.retry.time.sleep", sleep)
    monkeypatch.setattr(
        "runta._internal.retry.asyncio.sleep", AsyncMock(side_effect=sleep)
    )
    monkeypatch.setattr(
        "runta._internal.retry.random.uniform", lambda low, high: min(0.25, high)
    )
    client_type = _AsyncHttpClient if asynchronous else _SyncHttpClient
    http = client_type("http://runta.test", "test", timeout=30, retry_max_attempts=3)

    async def invoke(method="get_runtime", **kwargs):
        result = getattr(http, method)("sb-1", **kwargs)
        return await result if asynchronous else result

    yield http, clock, invoke
    if asynchronous:
        await http.close()
    else:
        http.close()


def success():
    return httpx.Response(200, json={"data": _runtime_json()})


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "failure",
    [
        408,
        429,
        502,
        503,
        504,
        httpx.ReadError,
        httpx.RemoteProtocolError,
        httpx.ConnectError,
        httpx.ReadTimeout,
    ],
)
async def test_transient_get_failure_retries(case, failure):
    http, clock, invoke = case
    requests = []

    def handler(request):
        requests.append(request)
        if len(requests) == 1:
            if isinstance(failure, int):
                return httpx.Response(failure, text="temporary failure")
            raise failure("temporary failure")
        return success()

    set_handler(http, handler)
    assert (await invoke()).id == "sb-1"
    assert len(requests) == 2
    assert clock.sleeps == [0.25]
    assert all(request.method == "GET" for request in requests)
    assert all(request.extensions["timeout"]["read"] == 30 for request in requests)


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [400, 401, 403, 404, 409, 422, 500, 501])
async def test_deterministic_http_error_does_not_retry(case, status):
    http, clock, invoke = case
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(status, text="deterministic failure")

    set_handler(http, handler)
    with pytest.raises(ApiError) as raised:
        await invoke()
    assert raised.value.status_code == status
    assert len(calls) == 1
    assert clock.sleeps == []


@pytest.mark.asyncio
@pytest.mark.parametrize("reason", ["certificate", "dns", "parameter"])
async def test_deterministic_local_error_does_not_retry(case, reason):
    http, clock, invoke = case
    calls = []
    if reason == "parameter":
        failure = ValueError("invalid parameter")
    else:
        failure = httpx.ConnectError("connection failed")
        failure.__cause__ = (
            ssl.SSLCertVerificationError("invalid certificate")
            if reason == "certificate"
            else socket.gaierror(socket.EAI_NONAME, "unknown host")
        )

    def handler(request):
        calls.append(request)
        raise failure

    set_handler(http, handler)
    with pytest.raises(ValueError if reason == "parameter" else ApiError) as raised:
        await invoke()
    assert raised.value is failure or raised.value.__cause__ is failure
    assert len(calls) == 1
    assert clock.sleeps == []


@pytest.mark.asyncio
@pytest.mark.parametrize("attempts", [1, 3, 16])
async def test_attempt_limit_preserves_last_error(case, attempts):
    http, clock, invoke = case
    http.retry_max_attempts = attempts
    failures = []

    def handler(request):
        failure = httpx.ReadError(f"failure {len(failures) + 1}")
        failures.append(failure)
        raise failure

    set_handler(http, handler)
    with pytest.raises(ApiError) as raised:
        await invoke()
    assert len(failures) == attempts
    assert raised.value.__cause__ is failures[-1]
    assert len(clock.sleeps) == attempts - 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("7", 7),
        ("0", 0),
        ("Tue, 14 Nov 2023 22:13:33 GMT", 13),
        ("Tue, 14 Nov 2023 22:13:00 GMT", 0),
        ("invalid", 0.25),
        ("-3", 0.25),
        ("1.5", 0.25),
        (None, 0.25),
    ],
)
async def test_retry_after_for_get(case, header, expected):
    http, clock, invoke = case
    calls = []

    def handler(request):
        calls.append(request)
        if len(calls) == 1:
            headers = {} if header is None else {"rEtRy-AfTeR": header}
            return httpx.Response(429, text="rate limited", headers=headers)
        return success()

    set_handler(http, handler)
    assert (await invoke()).id == "sb-1"
    assert clock.sleeps == [expected]
    assert len(calls) == 2


@pytest.mark.asyncio
async def test_retry_after_from_error_envelope(case):
    http, clock, invoke = case
    calls = []

    def handler(request):
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(
                429,
                json={
                    "error": {"code": "resource_exhausted", "message": "limited"},
                    "request_id": "test",
                },
                headers={"Retry-After": "9"},
            )
        return success()

    set_handler(http, handler)
    assert (await invoke()).id == "sb-1"
    assert clock.sleeps == [9]


@pytest.mark.asyncio
async def test_retry_after_exceeding_budget_does_not_retry_early(case):
    http, clock, invoke = case
    calls = []

    def handler(request):
        calls.append(request)
        clock.now += 20
        return httpx.Response(429, text="limited", headers={"Retry-After": "600"})

    set_handler(http, handler)
    with pytest.raises(ApiError) as raised:
        await invoke()
    assert raised.value.status_code == 429
    assert len(calls) == 1
    assert clock.sleeps == [460]
    assert clock.now == 480


@pytest.mark.asyncio
async def test_request_timeout_shrinks_with_budget(case):
    http, clock, invoke = case
    requests = []

    def handler(request):
        requests.append(request)
        if len(requests) == 1:
            clock.now += 475
            return httpx.Response(503, text="unavailable")
        return success()

    set_handler(http, handler)
    assert (await invoke()).id == "sb-1"
    assert requests[1].extensions["timeout"]["read"] == 4.75


@pytest.mark.asyncio
async def test_patch_gets_do_not_multiply_retry_attempts(case):
    http, clock, invoke = case
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(429, text="limited", headers={"Retry-After": "100"})

    set_handler(http, handler)
    with pytest.raises(ApiError):
        await invoke(
            "patch_runtime",
            resources=PatchRuntimeResources(
                requests=PatchRuntimeResourceRequests(memory_mib=2048)
            ),
        )
    assert len(requests) == http.retry_max_attempts
    assert all(request.method == "GET" for request in requests)
    # Other operations keep their existing jitter rather than using Retry-After.
    assert clock.sleeps == [0.25, 0.25]
