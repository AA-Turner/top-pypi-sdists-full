from __future__ import annotations

import json
import os

import httpx

from durable_agents import DurableClient, parse_sse_text


def test_client_sends_auth_header_and_uses_constructor_base_url() -> None:
    captured: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["authorization"] = request.headers.get("Authorization", "")
        return httpx.Response(200, json={"data": [], "next_cursor": None})

    client = DurableClient(
        api_key="test-secret",
        base_url="https://example.test",
        transport=httpx.MockTransport(handler),
    )
    try:
        client.models.list()
    finally:
        client.close()

    assert captured["url"] == "https://example.test/api/durable/models"
    assert captured["authorization"] == "Bearer test-secret"


def test_client_allows_environment_base_url_override() -> None:
    previous = os.environ.get("DURABLE_API_BASE_URL")
    os.environ["DURABLE_API_BASE_URL"] = "https://env.example.test"
    captured: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        return httpx.Response(200, json={"data": [], "next_cursor": None})

    try:
        client = DurableClient(transport=httpx.MockTransport(handler))
        try:
            client.models.list()
        finally:
            client.close()
    finally:
        if previous is None:
            os.environ.pop("DURABLE_API_BASE_URL", None)
        else:
            os.environ["DURABLE_API_BASE_URL"] = previous

    assert captured["url"] == "https://env.example.test/api/durable/models"


def test_client_prompts_interactive_agent_through_agent_runs_endpoint() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["method"] = request.method
        captured["json"] = json.loads(request.content)
        return httpx.Response(200, json={"id": "run_123"})

    client = DurableClient(
        api_key="test-secret",
        base_url="https://example.test",
        transport=httpx.MockTransport(handler),
    )
    try:
        client.agents.prompt("agent_123", {"prompt": "Reply READY."})
    finally:
        client.close()

    assert captured["url"] == "https://example.test/api/durable/agents/agent_123/runs"
    assert captured["method"] == "POST"
    assert captured["json"] == {"prompt": "Reply READY."}


def test_parse_sse_text_supports_event_and_json_data_blocks() -> None:
    events = parse_sse_text('event: update\ndata: {"status":"ready"}\n\n')

    assert len(events) == 1
    assert events[0].event == "update"
    assert events[0].data == {"status": "ready"}
