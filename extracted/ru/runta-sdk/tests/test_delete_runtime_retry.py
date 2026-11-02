from __future__ import annotations

import ssl
from types import SimpleNamespace

import httpx
import pytest

from runta import ApiError, AsyncRuntime, Runtime
from runta._internal.async_http import _AsyncHttpClient
from test_get_runtime_retry import case as case, set_handler
from test_openapi_transport import _runtime_json
from test_read_retries import call


def metadata(revision=1):
    return httpx.Response(200, json={"data": _runtime_json() | {"revision": revision}})


@pytest.mark.asyncio
@pytest.mark.parametrize("stage", ["GET", "DELETE"])
@pytest.mark.parametrize(
    "failure",
    [
        408,
        429,
        500,
        502,
        503,
        504,
        httpx.ReadError,
        httpx.RemoteProtocolError,
        httpx.ConnectError,
    ],
)
async def test_delete_retries_get_and_delete_failures(case, stage, failure):
    http, clock, _ = case
    requests = []
    failed = False
    revision = 0

    def handler(request):
        nonlocal failed, revision
        requests.append(request)
        if request.method == stage and not failed:
            failed = True
            if isinstance(failure, int):
                return httpx.Response(failure, text="temporary failure")
            raise failure("temporary failure")
        if request.method == "GET":
            revision += 1
            return metadata(revision)
        return httpx.Response(204)

    set_handler(http, handler)
    handle_type = AsyncRuntime if isinstance(http, _AsyncHttpClient) else Runtime
    handle = handle_type._from_info(
        SimpleNamespace(_http=http), SimpleNamespace(id="sb-1")
    )
    assert await call(handle, "delete") is None
    assert [request.method for request in requests] == (
        ["GET", "GET", "DELETE"]
        if stage == "GET"
        else ["GET", "DELETE", "GET", "DELETE"]
    )
    assert all(request.url.path == "/v2/runtimes/sb-1" for request in requests)
    assert clock.sleeps == [0.25]
    if stage == "DELETE":
        assert [
            request.url.params["expected_revision"]
            for request in requests
            if request.method == "DELETE"
        ] == ["1", "2"]


@pytest.mark.asyncio
@pytest.mark.parametrize("stage", ["GET", "DELETE"])
@pytest.mark.parametrize("status", [400, 401, 403, 409, 422, 501])
async def test_delete_does_not_retry_non_retryable_errors(case, stage, status):
    http, clock, _ = case
    requests = []

    def handler(request):
        requests.append(request)
        return (
            metadata()
            if request.method != stage
            else httpx.Response(status, text="failure")
        )

    set_handler(http, handler)
    with pytest.raises(ApiError) as raised:
        await call(http, "delete_runtime", "sb-1")
    assert raised.value.status_code == status
    assert len(requests) == (1 if stage == "GET" else 2)
    assert clock.sleeps == []


@pytest.mark.asyncio
@pytest.mark.parametrize("stage", ["GET", "DELETE"])
async def test_delete_certificate_failure_does_not_retry(case, stage):
    http, clock, _ = case
    requests = []
    failure = httpx.ConnectError("certificate failed")
    failure.__cause__ = ssl.SSLCertVerificationError("invalid certificate")

    def handler(request):
        requests.append(request)
        if request.method == stage:
            raise failure
        return metadata()

    set_handler(http, handler)
    with pytest.raises(ApiError) as raised:
        await call(http, "delete_runtime", "sb-1")
    assert raised.value.__cause__ is failure
    assert len(requests) == (1 if stage == "GET" else 2)
    assert clock.sleeps == []


@pytest.mark.asyncio
@pytest.mark.parametrize("stage", ["GET", "DELETE"])
async def test_delete_not_found_is_success(case, stage):
    http, clock, _ = case
    requests = []

    def handler(request):
        requests.append(request)
        return (
            metadata()
            if request.method != stage
            else httpx.Response(404, text="deleted")
        )

    set_handler(http, handler)
    assert await call(http, "delete_runtime", "sb-1") is None
    assert len(requests) == (1 if stage == "GET" else 2)
    assert clock.sleeps == []


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [202, 204])
async def test_accepted_delete_returns_without_polling(case, status):
    http, clock, _ = case
    requests = []

    def handler(request):
        requests.append(request)
        if request.method == "GET":
            return metadata()
        if status == 202:
            return httpx.Response(status, json={"data": _runtime_json()})
        return httpx.Response(status)

    set_handler(http, handler)
    assert await call(http, "delete_runtime", "sb-1") is None
    assert [request.method for request in requests] == ["GET", "DELETE"]


@pytest.mark.asyncio
async def test_lost_delete_response_followed_by_not_found_is_success(case):
    http, clock, _ = case
    requests = []
    deleted = False

    def handler(request):
        nonlocal deleted
        requests.append(request)
        if request.method == "DELETE":
            deleted = True
            raise httpx.ReadError("delete response lost")
        return httpx.Response(404, text="deleted") if deleted else metadata()

    set_handler(http, handler)
    assert await call(http, "delete_runtime", "sb-1") is None
    assert [request.method for request in requests] == ["GET", "DELETE", "GET"]


@pytest.mark.asyncio
@pytest.mark.parametrize("stage", ["GET", "DELETE"])
@pytest.mark.parametrize("attempts", [1, 3, 16])
async def test_delete_attempt_limit_preserves_last_error(case, stage, attempts):
    http, clock, _ = case
    http.retry_max_attempts = attempts
    requests = []
    failures = []

    def handler(request):
        requests.append(request)
        if request.method == stage:
            error = httpx.ReadError(f"failure {len(failures)}")
            failures.append(error)
            raise error
        return metadata()

    set_handler(http, handler)
    with pytest.raises(ApiError) as raised:
        await call(http, "delete_runtime", "sb-1")
    assert len(failures) == attempts
    assert len(requests) == attempts * (1 if stage == "GET" else 2)
    assert raised.value.__cause__ is failures[-1]
    assert len(clock.sleeps) == attempts - 1


@pytest.mark.asyncio
@pytest.mark.parametrize("stage", ["GET", "DELETE"])
async def test_repeated_internal_server_errors_exhaust_delete_attempts(case, stage):
    http, clock, _ = case
    failures = []
    requests = []

    def handler(request):
        requests.append(request)
        if request.method == stage:
            failures.append(True)
            return httpx.Response(500, text=f"internal failure {len(failures)}")
        return metadata()

    set_handler(http, handler)
    with pytest.raises(ApiError) as raised:
        await call(http, "delete_runtime", "sb-1")
    assert raised.value.status_code == 500
    assert str(raised.value).endswith("internal failure 3")
    assert len(failures) == http.retry_max_attempts
    assert len(requests) == http.retry_max_attempts * (1 if stage == "GET" else 2)
    assert clock.sleeps == [0.25, 0.25]


@pytest.mark.asyncio
@pytest.mark.parametrize("stage", ["GET", "DELETE"])
async def test_delete_honors_retry_after(case, stage):
    http, clock, _ = case
    requests = []
    failed = False

    def handler(request):
        nonlocal failed
        requests.append(request)
        if request.method == stage and not failed:
            failed = True
            return httpx.Response(429, text="limited", headers={"Retry-After": "7"})
        return metadata() if request.method == "GET" else httpx.Response(204)

    set_handler(http, handler)
    await call(http, "delete_runtime", "sb-1")
    assert clock.sleeps == [7]


@pytest.mark.asyncio
async def test_get_and_delete_share_timeout_budget(case):
    http, clock, _ = case
    requests = []

    def handler(request):
        requests.append(request)
        if request.method == "GET":
            clock.now += 475
            return metadata()
        return httpx.Response(429, text="limited", headers={"Retry-After": "600"})

    set_handler(http, handler)
    with pytest.raises(ApiError) as raised:
        await call(http, "delete_runtime", "sb-1")
    assert raised.value.status_code == 429
    assert len(requests) == 2
    assert requests[0].extensions["timeout"]["read"] == 30
    assert requests[1].extensions["timeout"]["read"] == 5
    assert clock.sleeps == [5]
    assert clock.now == 480


@pytest.mark.asyncio
async def test_delete_is_not_sent_after_get_exhausts_budget(case):
    http, clock, _ = case
    requests = []

    def handler(request):
        requests.append(request)
        clock.now += 480
        return metadata()

    set_handler(http, handler)
    with pytest.raises(TimeoutError):
        await call(http, "delete_runtime", "sb-1")
    assert [request.method for request in requests] == ["GET"]
    assert clock.sleeps == []
