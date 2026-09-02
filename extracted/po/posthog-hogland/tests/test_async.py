"""Async client smoke tests."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
import respx

from conftest import TEST_BASE_URL
from hogland import AsyncHogbox, AsyncHogland, BoxView, NotFoundError


@pytest.mark.asyncio
@respx.mock
async def test_async_create_and_exec(box_view_json: dict[str, Any]) -> None:
    respx.post(f"{TEST_BASE_URL}/v1/hogboxes").mock(
        return_value=httpx.Response(200, json={**box_view_json, "id": "hb-async-1"}),
    )
    respx.post(f"{TEST_BASE_URL}/v1/hogboxes/hb-async-1/exec").mock(
        return_value=httpx.Response(
            200,
            json={
                "stdout": "hi\n",
                "stderr": "",
                "exit_code": 0,
                "timed_out": False,
                "duration_ms": 1,
            },
        ),
    )
    respx.delete(f"{TEST_BASE_URL}/v1/hogboxes/hb-async-1").mock(
        return_value=httpx.Response(204),
    )

    async with AsyncHogland(token="t", base_url=TEST_BASE_URL) as client:
        box = await client.create(cpus=1, memory_mib=1024)
        assert isinstance(box, AsyncHogbox)
        result = await box.exec(["echo", "hi"])
        assert result.exit_code == 0
        await box.delete()


@pytest.mark.asyncio
@respx.mock
async def test_async_not_found() -> None:
    respx.get(f"{TEST_BASE_URL}/v1/hogboxes/hb-missing").mock(
        return_value=httpx.Response(404, json={"detail": "gone"}),
    )
    async with AsyncHogland(token="t", base_url=TEST_BASE_URL) as client:
        with pytest.raises(NotFoundError):
            await client.get("hb-missing")


@pytest.mark.asyncio
async def test_async_proxy_url_builder(box_view_json: dict[str, Any]) -> None:
    async with AsyncHogland(token="t", base_url=TEST_BASE_URL) as client:
        view = BoxView.model_validate({**box_view_json, "id": "hb-p"})
        box = AsyncHogbox(view, client)
        assert box.proxy_url(7777) == f"{TEST_BASE_URL}/v1/hogboxes/hb-p/proxy/7777/"


@pytest.mark.asyncio
@respx.mock
async def test_async_create_with_web_port_sends_web_port(box_view_json: dict[str, Any]) -> None:
    # The async create path forwards web_port through its own
    # _build_create_body call, so pin it independently of the sync test.
    route = respx.post(f"{TEST_BASE_URL}/v1/hogboxes").mock(
        return_value=httpx.Response(200, json={**box_view_json, "id": "hb-async-exposed"}),
    )
    async with AsyncHogland(token="t", base_url=TEST_BASE_URL) as client:
        await client.create(snapshot_id="alias:foo", web_port=8000)
    sent = json.loads(route.calls.last.request.content)
    assert sent["web_port"] == 8000


@pytest.mark.asyncio
@respx.mock
async def test_async_web_url_reads_server_value(box_view_json: dict[str, Any]) -> None:
    respx.get(f"{TEST_BASE_URL}/v1/hogboxes/hb-async-w").mock(
        return_value=httpx.Response(
            200,
            json={
                **box_view_json,
                "id": "hb-async-w",
                "web_url": "https://hb-async-w.boxes.example.dev/",
            },
        ),
    )
    async with AsyncHogland(token="t", base_url=TEST_BASE_URL) as client:
        box = AsyncHogbox(BoxView.model_validate({**box_view_json, "id": "hb-async-w"}), client)
        assert await box.web_url() == "https://hb-async-w.boxes.example.dev/"
