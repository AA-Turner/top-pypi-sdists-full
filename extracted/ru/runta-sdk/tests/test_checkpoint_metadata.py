"""Public checkpoint metadata survives generated and paginated decoding."""

import httpx
import pytest

from runta import AsyncRunta, AsyncRuntime, Runta, Runtime, RuntimeInfo
from test_openapi_transport import _checkpoint_json, _runtime_json


CASES = [
    ({}, None, None),
    ({"kind": "full", "safe_error_code": None}, "full", None),
    (
        {"kind": "cold", "safe_error_code": "guest_shutdown_failed"},
        "cold",
        "guest_shutdown_failed",
    ),
    ({"kind": "future-kind"}, "future-kind", None),
]


def inject(client, fields):
    payload = _checkpoint_json() | fields
    if fields.get("safe_error_code"):
        payload["state"] = "failed"
    seen = []

    def handler(request):
        seen.append((request.method, request.url.path))
        if request.url.path == "/v2/checkpoints":
            after = request.url.params.get("after")
            return httpx.Response(
                200,
                json={
                    "data": [payload | {"id": "second" if after else "first"}],
                    "pagination": {
                        "has_more": not after,
                        "next_cursor": None if after else "next",
                    },
                },
            )
        return httpx.Response(200, json={"data": payload})

    transport = httpx.MockTransport(handler)
    http = client._http
    if isinstance(client, AsyncRunta) and hasattr(http, "_send_request"):

        async def send(request, timeout):
            response = await transport.handle_async_request(request)
            await response.aread()
            return response

        http._send_request = send
    else:
        http._client._httpx_args["transport"] = transport
    return seen


def assert_metadata(info, kind, error):
    assert info.kind == kind
    assert info.safe_error_code == error


@pytest.mark.parametrize("fields,kind,error", CASES)
def test_sync_get_and_paginated_list(fields, kind, error):
    with Runta(endpoint="http://test", token="test") as client:
        seen = inject(client, fields)
        assert_metadata(client.checkpoints.get("checkpoint-1"), kind, error)
        checkpoints = client.checkpoints.list()
        assert [item.id for item in checkpoints] == ["first", "second"]
        for checkpoint in checkpoints:
            assert_metadata(checkpoint, kind, error)
        assert seen == [
            ("GET", "/v2/checkpoints/checkpoint-1"),
            ("GET", "/v2/checkpoints"),
            ("GET", "/v2/checkpoints"),
        ]


@pytest.mark.asyncio
@pytest.mark.parametrize("fields,kind,error", CASES)
async def test_async_get_and_paginated_list(fields, kind, error):
    async with AsyncRunta(endpoint="http://test", token="test") as client:
        seen = inject(client, fields)
        assert_metadata(await client.checkpoints.get("checkpoint-1"), kind, error)
        checkpoints = await client.checkpoints.list()
        assert [item.id for item in checkpoints] == ["first", "second"]
        for checkpoint in checkpoints:
            assert_metadata(checkpoint, kind, error)
        assert seen == [
            ("GET", "/v2/checkpoints/checkpoint-1"),
            ("GET", "/v2/checkpoints"),
            ("GET", "/v2/checkpoints"),
        ]


@pytest.mark.parametrize(
    "fields,kind,error",
    [
        CASES[0],
        CASES[1],
        (
            {"kind": "full", "safe_error_code": "guest_shutdown_failed"},
            "full",
            "guest_shutdown_failed",
        ),
    ],
)
def test_sync_create(fields, kind, error):
    with Runta(endpoint="http://test", token="test") as client:
        seen = inject(client, fields)
        runtime = Runtime._from_info(client, RuntimeInfo.from_json(_runtime_json()))
        assert_metadata(runtime.checkpoints.create(wait=False), kind, error)
        assert seen == [("POST", "/v2/runtimes/sb-1/checkpoints")]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "fields,kind,error",
    [
        CASES[0],
        CASES[1],
        (
            {"kind": "full", "safe_error_code": "guest_shutdown_failed"},
            "full",
            "guest_shutdown_failed",
        ),
    ],
)
async def test_async_create(fields, kind, error):
    async with AsyncRunta(endpoint="http://test", token="test") as client:
        seen = inject(client, fields)
        runtime = AsyncRuntime._from_info(
            client, RuntimeInfo.from_json(_runtime_json())
        )
        assert_metadata(await runtime.checkpoints.create(wait=False), kind, error)
        assert seen == [("POST", "/v2/runtimes/sb-1/checkpoints")]
