from __future__ import annotations

import asyncio
import inspect
import uuid
from types import SimpleNamespace

import httpx
import pytest

from runta import (
    ApiError,
    AsyncRuntime,
    Runtime,
    RuntimeManager,
    AsyncRuntimeManager,
    CheckpointManager,
    AsyncCheckpointManager,
    SecretManager,
    AsyncSecretManager,
    ExecutionError,
)
from runta._internal.async_http import _AsyncHttpClient
from runta._internal.execution import Execution, AsyncExecution, ExecutionState
from runta._internal.retry import (
    read_deadline,
    read_retry_deadline,
)
from test_get_runtime_retry import case as case, set_handler
from test_openapi_transport import _runtime_json, _checkpoint_json, _secret_json


async def call(target, method, *args, **kwargs):
    result = getattr(target, method)(*args, **kwargs)
    return await result if inspect.isawaitable(result) else result


READS = [
    "get_runtime",
    "list_runtimes",
    "get_checkpoint",
    "list_checkpoints",
    "get_secret",
    "list_secrets",
    "read_file",
]


def response_for(method):
    if method == "read_file":
        return httpx.Response(200, content=b"\x00binary\xff")
    model = (
        _runtime_json()
        if "runtime" in method
        else _checkpoint_json()
        if "checkpoint" in method
        else _secret_json()
    )
    payload = {"data": [model] if method.startswith("list") else model}
    if method in {"list_runtimes", "list_checkpoints"}:
        payload["pagination"] = {"has_more": False, "next_cursor": None}
    return httpx.Response(200, json=payload)


def arguments(method):
    return (
        ()
        if method.startswith("list")
        else ("id", "/binary")
        if method == "read_file"
        else ("id",)
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("method", READS)
@pytest.mark.parametrize("status", [429, 503, 403])
async def test_read_operations_share_retry_policy(case, method, status):
    http, clock, _ = case
    requests = []

    def handler(request):
        requests.append(request)
        if len(requests) == 1:
            return httpx.Response(status, text="failure", headers={"Retry-After": "2"})
        return response_for(method)

    set_handler(http, handler)
    if status == 403:
        with pytest.raises(ApiError):
            await call(http, method, *arguments(method))
        assert len(requests) == 1
        assert clock.sleeps == []
    else:
        result = await call(http, method, *arguments(method))
        if method == "read_file":
            assert result == b"\x00binary\xff"
        assert len(requests) == 2
        assert clock.sleeps == [2 if status == 429 else 0.25]


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["list_runtimes", "list_checkpoints"])
async def test_failed_page_retries_same_cursor_without_duplicate_results(case, method):
    http, clock, _ = case
    cursors = []
    model = _runtime_json() if method == "list_runtimes" else _checkpoint_json()

    def handler(request):
        cursor = request.url.params.get("after")
        cursors.append(cursor)
        if len(cursors) == 2:
            return httpx.Response(503, text="temporary failure")
        return httpx.Response(
            200,
            json={
                "data": [model | {"id": "first" if cursor is None else "second"}],
                "pagination": {
                    "has_more": cursor is None,
                    "next_cursor": "cursor-2" if cursor is None else None,
                },
            },
        )

    set_handler(http, handler)
    assert [item.id for item in await call(http, method)] == ["first", "second"]
    assert cursors == [None, "cursor-2", "cursor-2"]


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["list_runtimes", "list_checkpoints"])
async def test_pages_share_one_deadline(case, method):
    http, clock, _ = case
    requests = []
    model = _runtime_json() if method == "list_runtimes" else _checkpoint_json()

    def handler(request):
        requests.append(request)
        if len(requests) == 1:
            clock.now += 475
            return httpx.Response(
                200,
                json={
                    "data": [model],
                    "pagination": {"has_more": True, "next_cursor": "next"},
                },
            )
        return httpx.Response(429, text="limited", headers={"Retry-After": "100"})

    set_handler(http, handler)
    with pytest.raises(ApiError):
        await call(http, method)
    assert len(requests) == 2
    assert requests[1].extensions["timeout"]["read"] == 5
    assert clock.sleeps == [5]
    assert clock.now == 480


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["list_runtimes", "list_checkpoints"])
@pytest.mark.parametrize(
    "invalid", [b"not JSON", b'{"data": [], "pagination": {"has_more": true}}']
)
async def test_invalid_list_response_does_not_retry(case, method, invalid):
    http, clock, _ = case
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(200, content=invalid)

    set_handler(http, handler)
    with pytest.raises(ApiError):
        await call(http, method)
    assert len(requests) == 1
    assert clock.sleeps == []


def manager_for(http, resource):
    asynchronous = isinstance(http, _AsyncHttpClient)
    types = {
        "runtime": (RuntimeManager, AsyncRuntimeManager),
        "checkpoint": (CheckpointManager, AsyncCheckpointManager),
        "secret": (SecretManager, AsyncSecretManager),
    }
    return types[resource][asynchronous]._from_owner(SimpleNamespace(_http=http))


@pytest.mark.asyncio
@pytest.mark.parametrize("resource", ["runtime", "checkpoint", "secret"])
async def test_name_lookup_retries_direct_get(case, resource):
    http, clock, _ = case
    paths = []

    def handler(request):
        paths.append(request.url.path)
        if len(paths) == 1:
            return httpx.Response(429, text="limited", headers={"Retry-After": "2"})
        payload = response_for("get_" + resource).json()
        payload["data"]["display_name"] = "worker"
        return httpx.Response(200, json=payload)

    set_handler(http, handler)
    result = await call(manager_for(http, resource), "get", "worker")
    assert (result.name if resource == "runtime" else result.display_name) == "worker"
    assert len(paths) == 2 and paths[0] == paths[1]
    assert paths[0].endswith("/worker")
    assert clock.sleeps == [2]


@pytest.mark.asyncio
@pytest.mark.parametrize("resource", ["runtime", "checkpoint", "secret"])
async def test_uuid_lookup_keeps_retries(case, resource):
    http, clock, _ = case
    calls = []

    def handler(request):
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(429, text="limited", headers={"Retry-After": "2"})
        return response_for("get_" + resource)

    set_handler(http, handler)
    await call(manager_for(http, resource), "get", str(uuid.uuid4()))
    assert len(calls) == 2
    assert clock.sleeps == [2]


@pytest.mark.asyncio
@pytest.mark.parametrize("resource", ["runtime", "checkpoint"])
async def test_readiness_bounds_get_retry_budget(case, resource):
    http, clock, _ = case
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(429, text="limited", headers={"Retry-After": "600"})

    set_handler(http, handler)
    if resource == "runtime":
        runtime_type = AsyncRuntime if isinstance(http, _AsyncHttpClient) else Runtime
        target = runtime_type._from_info(
            SimpleNamespace(_http=http),
            SimpleNamespace(id=str(uuid.uuid4()), status="creating"),
        )
        args = ()
    else:
        target = manager_for(http, "checkpoint")
        args = (str(uuid.uuid4()),)
    with pytest.raises(TimeoutError):
        await call(target, "wait_until_ready", *args, timeout=4)
    assert requests[0].extensions["timeout"]["read"] == 4
    assert clock.now == 4
    assert clock.sleeps == [4]
    assert read_retry_deadline() == 484


@pytest.mark.asyncio
async def test_readiness_name_fallback_shares_deadline(case):
    http, clock, _ = case
    requests = []

    def handler(request):
        requests.append(request)
        if request.url.path.endswith("/worker"):
            clock.now += 1
            return httpx.Response(404, text="missing")
        return httpx.Response(429, text="limited", headers={"Retry-After": "600"})

    set_handler(http, handler)
    with pytest.raises(TimeoutError):
        await call(
            manager_for(http, "checkpoint"), "wait_until_ready", "worker", timeout=4
        )
    assert len(requests) == 2
    assert requests[1].extensions["timeout"]["read"] == 3
    assert clock.now == 4


@pytest.mark.asyncio
async def test_execution_file_reads_do_not_multiply_attempts(case):
    http, clock, _ = case
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(503, text="unavailable")

    set_handler(http, handler)
    handle_type = AsyncExecution if isinstance(http, _AsyncHttpClient) else Execution
    handle = handle_type(
        SimpleNamespace(id="runtime", _client=SimpleNamespace(_http=http)),
        str(uuid.uuid4()),
    )
    with pytest.raises(ExecutionError):
        await call(handle, "_output", ExecutionState("completed", 0))
    assert len(requests) == http.retry_max_attempts


@pytest.mark.asyncio
async def test_health_remains_single_attempt(case):
    http, clock, _ = case
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(503, text="unavailable")

    set_handler(http, handler)
    with pytest.raises(ApiError):
        await call(http, "health")
    assert len(requests) == 1
    assert clock.sleeps == []


@pytest.mark.asyncio
async def test_read_context_isolated_and_restored(monkeypatch):
    monkeypatch.setattr("runta._internal.retry.time.monotonic", lambda: 0)
    entered = asyncio.Event()
    inspected = asyncio.Event()

    async def limited():
        with read_deadline(5):
            with read_deadline(10):
                assert read_retry_deadline() == 5
            entered.set()
            await inspected.wait()
            assert read_retry_deadline() == 5
        assert read_retry_deadline() == 480

    async def independent():
        await entered.wait()
        assert read_retry_deadline() == 480
        inspected.set()

    await asyncio.gather(limited(), independent())
