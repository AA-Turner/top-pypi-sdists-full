"""Offline smoke tests for the public calls shown in the Python docs."""

from __future__ import annotations

import httpx
import pytest

from composio_client import AsyncComposio, Composio, ProjectAuth

BASE_URL = "https://docs.invalid"
SESSION = {
    "config": {},
    "config_version": 1,
    "mcp": {},
    "session_id": "sess_123",
    "tool_router_tools": [],
}


def response_for(request: httpx.Request) -> httpx.Response:
    path = request.url.path
    if path.endswith("/execute"):
        return httpx.Response(200, json={"data": {}, "log_id": "log_123"})
    if path.endswith("/config_history"):
        return httpx.Response(
            200,
            json={"current_page": 1, "items": [], "total_items": 0, "total_pages": 1},
        )
    if path.endswith("/items"):
        return httpx.Response(200, json={"items": []})
    return httpx.Response(200, json=SESSION)


def sync_client() -> Composio:
    return Composio(
        auth=ProjectAuth("ak_test"),
        base_url=BASE_URL,
        http_client=httpx.Client(transport=httpx.MockTransport(response_for)),
    )


def test_readme_flat_usage() -> None:
    with sync_client() as client:
        session = client.tool_router.session.create(user_id="user@example.com")
        result = client.tool_router.session.execute(
            session.session_id,
            tool_slug="GITHUB_CREATE_ISSUE",
            arguments={"owner": "composiohq", "repo": "composio", "title": "Example"},
        )

    assert session.session_id == "sess_123"
    assert result.log_id == "log_123"


@pytest.mark.asyncio
async def test_readme_async_usage() -> None:
    transport = httpx.MockTransport(response_for)
    async with AsyncComposio(
        auth=ProjectAuth("ak_test"),
        base_url=BASE_URL,
        http_client=httpx.AsyncClient(transport=transport),
    ) as client:
        session = await client.tool_router.session.create(user_id="user@example.com")

    assert session.session_id == "sess_123"


def test_readme_raw_and_streaming_usage() -> None:
    with sync_client() as client:
        raw = client.tool_router.session.with_raw_response.retrieve("sess_123")
        assert raw.status_code == 200
        assert raw.parse().session_id == "sess_123"

        with client.tool_router.session.with_streaming_response.retrieve("sess_123") as streamed:
            assert streamed.json() == SESSION
            assert streamed.read()
            assert streamed.parse().session_id == "sess_123"


def test_migration_flat_and_aggregate_examples() -> None:
    with sync_client() as client:
        assert client.tool_router.session.create(user_id="user@example.com").session_id == "sess_123"
        assert client.tool_router.session.create({"user_id": "user@example.com"}).session_id == "sess_123"
        assert client.tool_router.session.config_history("sess_123", limit=25).total_items == 0
        assert client.tool_router.session.config_history("sess_123", query={"limit": 25}).total_items == 0
        assert client.tool_router.session.files.list("mount_123", session_id="sess_123").items == []
        assert client.tool_router.session.files.list("sess_123", "mount_123").items == []
