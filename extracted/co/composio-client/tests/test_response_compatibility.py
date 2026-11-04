"""Stainless-compatible raw responses, streaming, files, and request bodies."""

from __future__ import annotations

import inspect
from pathlib import Path

import httpx
import pytest
import respx
from pydantic import BaseModel

from composio_client import AsyncComposio, Composio, file_from_path
from composio_client._response import (
    APIResponse,
    AsyncAPIResponse,
    AsyncResponseContextManager,
    ResponseContextManager,
)
from composio_client._streaming import SSEDecoder

from .conftest import BASE_URL

RAW_PATH = "/api/v3.1/raw-compatibility"


class Named(BaseModel):
    name: str


def test_file_from_path_returns_the_stainless_file_tuple(tmp_path: Path) -> None:
    source = tmp_path / "payload.bin"
    source.write_bytes(b"payload")

    assert file_from_path(str(source)) == ("payload.bin", b"payload")


def test_raw_method_signatures_retain_stainless_parameters() -> None:
    get = inspect.signature(Composio.get).parameters
    post = inspect.signature(Composio.post).parameters
    async_post = inspect.signature(AsyncComposio.post).parameters

    assert list(get)[:6] == ["self", "path", "cast_to", "options", "stream", "stream_cls"]
    assert list(post)[:9] == [
        "self",
        "path",
        "cast_to",
        "body",
        "content",
        "options",
        "files",
        "stream",
        "stream_cls",
    ]
    assert list(async_post)[:9] == [
        "self",
        "path",
        "cast_to",
        "body",
        "content",
        "files",
        "options",
        "stream",
        "stream_cls",
    ]


@respx.mock
def test_binary_content_is_sent_without_json_serialization(client: Composio) -> None:
    route = respx.post(f"{BASE_URL}{RAW_PATH}").mock(
        return_value=httpx.Response(200, json={"name": "binary"})
    )

    result = client.post(RAW_PATH, cast_to=Named, content=b"raw-bytes")

    assert result == Named(name="binary")
    assert route.calls.last.request.content == b"raw-bytes"
    assert "application/json" not in route.calls.last.request.headers.get("content-type", "")


@respx.mock
def test_multipart_files_and_form_body_reach_httpx(client: Composio) -> None:
    route = respx.post(f"{BASE_URL}{RAW_PATH}").mock(
        return_value=httpx.Response(200, json={"name": "upload"})
    )

    result = client.post(
        RAW_PATH,
        cast_to=Named,
        body={"purpose": "test"},
        files={"asset": ("asset.txt", b"contents", "text/plain")},
    )

    request = route.calls.last.request
    assert result == Named(name="upload")
    assert request.headers["content-type"].startswith("multipart/form-data; boundary=")
    assert b'name="purpose"' in request.content
    assert b"test" in request.content
    assert b'filename="asset.txt"' in request.content
    assert b"contents" in request.content


@respx.mock
def test_public_request_accepts_final_request_options(client: Composio) -> None:
    route = respx.get(f"{BASE_URL}{RAW_PATH}").mock(
        return_value=httpx.Response(200, json={"name": "requested"})
    )

    result = client.request(
        Named,
        {
            "method": "get",
            "url": RAW_PATH,
            "params": {"limit": 1},
            "headers": {"x-trace": "trace"},
        },
    )

    assert result == Named(name="requested")
    assert route.calls.last.request.url.params["limit"] == "1"
    assert route.calls.last.request.headers["x-trace"] == "trace"


@respx.mock
def test_raw_response_parses_on_demand_and_exposes_http_metadata(client: Composio) -> None:
    respx.get(f"{BASE_URL}{RAW_PATH}").mock(
        return_value=httpx.Response(201, json={"name": "raw"}, headers={"x-result": "yes"})
    )

    response = client._request_raw("get", RAW_PATH, cast_to=Named)

    assert isinstance(response, APIResponse)
    assert response.status_code == 201
    assert response.headers["x-result"] == "yes"
    assert response.parse() == Named(name="raw")
    assert response.parse(to=dict) == {"name": "raw"}
    response.close()
    assert response.is_closed


@respx.mock
def test_streaming_response_context_is_lazy_and_closes(client: Composio) -> None:
    route = respx.get(f"{BASE_URL}{RAW_PATH}").mock(
        return_value=httpx.Response(200, json={"name": "streamed"})
    )
    context = ResponseContextManager(lambda: client._request_raw("get", RAW_PATH, cast_to=Named, stream=True))

    assert not route.called
    with context as response:
        assert route.called
        assert not response.is_closed
        assert response.parse() == Named(name="streamed")
    assert response.is_closed


def test_sse_decoder_preserves_fields_and_multiline_data() -> None:
    decoder = SSEDecoder()

    events = list(
        decoder.iter_bytes(
            iter(
                [
                    b": ignored\r\nid: event-1\r\nevent: update\r\n",
                    b"retry: 1500\r\ndata: first\r\ndata: second\r\n\r\n",
                    b"id: bad\0value\ndata: third\n\n",
                ]
            )
        )
    )

    assert [(event.event, event.data, event.id, event.retry) for event in events] == [
        ("update", "first\nsecond", "event-1", 1500),
        (None, "third", "event-1", None),
    ]


@pytest.mark.asyncio
async def test_async_raw_response_and_context_are_awaitable(async_client: AsyncComposio) -> None:
    with respx.mock:
        route = respx.get(f"{BASE_URL}{RAW_PATH}").mock(
            return_value=httpx.Response(200, json={"name": "async"})
        )
        context = AsyncResponseContextManager(
            async_client._request_raw("get", RAW_PATH, cast_to=Named, stream=True)
        )

        assert not route.called
        async with context as response:
            assert isinstance(response, AsyncAPIResponse)
            assert not response.is_closed
            assert await response.parse() == Named(name="async")
        assert response.is_closed
