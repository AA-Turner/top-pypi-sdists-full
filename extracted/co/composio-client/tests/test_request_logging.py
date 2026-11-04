from __future__ import annotations

import logging
from collections.abc import Iterator

import httpx
import pytest
import respx
from pydantic import BaseModel

from composio_client import AsyncComposio, Composio, RequestOptions

from .conftest import API_KEY, BASE_URL


class Echo(BaseModel):
    ok: bool


class ExplodingHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        raise RuntimeError("logging failed")


@pytest.fixture
def exploding_logger() -> Iterator[None]:
    logger = logging.getLogger("composio_client")
    previous_level = logger.level
    handler = ExplodingHandler()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    try:
        yield
    finally:
        logger.removeHandler(handler)
        logger.setLevel(previous_level)


@respx.mock
def test_sync_logs_retry_lifecycle_without_request_secrets(
    client: Composio, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.DEBUG, logger="composio_client")
    route = respx.post(
        f"{BASE_URL}/custom/path-secret?private=query-secret",
    ).mock(
        side_effect=[
            httpx.Response(
                500,
                headers={"retry-after": "0"},
                json={"error": "response-secret"},
            ),
            httpx.Response(200, json={"ok": True, "token": "response-token"}),
        ]
    )

    result = client._request(
        "post",
        "/custom/path-secret",
        cast_to=Echo,
        body={"private": "body-secret"},
        query={"private": "query-secret"},
        headers={"x-secret": "header-secret"},
        options=RequestOptions(max_retries=1),
    )

    messages = "\n".join(caplog.messages)
    assert result.ok is True
    assert route.call_count == 2
    assert messages.count("request attempt method=POST path=<custom> attempt=") == 2
    assert "request response method=POST path=<custom> status=500 outcome=http_error duration_ms=" in messages
    assert "request response method=POST path=<custom> status=200 outcome=success duration_ms=" in messages
    assert "request retry method=POST path=<custom> reason=status_500 next_attempt=2 remaining=1" in messages
    assert "path-secret" not in messages
    assert "body-secret" not in messages
    assert "query-secret" not in messages
    assert "header-secret" not in messages
    assert "response-secret" not in messages
    assert "response-token" not in messages
    assert "private" not in messages
    assert "x-secret" not in messages
    assert API_KEY not in messages


@respx.mock
async def test_async_logs_transport_retry_with_templated_path_without_secrets(
    async_client: AsyncComposio, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.DEBUG, logger="composio_client")
    route = respx.get(
        f"{BASE_URL}/api/v3.1/tool_router/session/path-secret?private=query-secret",
    ).mock(
        side_effect=[
            httpx.ConnectError("transport-secret"),
            httpx.Response(200, json={"ok": True}),
        ]
    )

    result = await async_client._request(
        "get",
        "/api/v3.1/tool_router/session/path-secret",
        cast_to=Echo,
        query={"private": "query-secret"},
        headers={"x-secret": "header-secret"},
        options=RequestOptions(max_retries=1),
    )

    messages = "\n".join(caplog.messages)
    assert result.ok is True
    assert route.call_count == 2
    assert (
        messages.count("request attempt method=GET path=/api/v3.1/tool_router/session/{session_id} attempt=")
        == 2
    )
    assert (
        "request retry method=GET path=/api/v3.1/tool_router/session/{session_id} "
        "reason=connection next_attempt=2 remaining=1"
    ) in messages
    assert (
        "request response method=GET path=/api/v3.1/tool_router/session/{session_id} "
        "status=200 outcome=success duration_ms="
    ) in messages
    assert "path-secret" not in messages
    assert "query-secret" not in messages
    assert "header-secret" not in messages
    assert "transport-secret" not in messages
    assert "private" not in messages
    assert "x-secret" not in messages
    assert API_KEY not in messages

    await async_client.aclose()


@respx.mock
def test_info_logs_completed_response_without_debug_attempt(
    client: Composio, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.INFO, logger="composio_client")
    respx.get(f"{BASE_URL}/api/v3.1/tools").mock(return_value=httpx.Response(200, json={"ok": True}))

    result = client._request("get", "/api/v3.1/tools", cast_to=Echo)

    messages = "\n".join(caplog.messages)
    assert result.ok is True
    assert "request attempt" not in messages
    assert (
        "request response method=GET path=/api/v3.1/tools status=200 outcome=success duration_ms=" in messages
    )


@respx.mock
def test_default_warning_level_emits_no_lifecycle_records(
    client: Composio, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.WARNING, logger="composio_client")
    respx.get(f"{BASE_URL}/api/v3.1/tools").mock(return_value=httpx.Response(200, json={"ok": True}))

    result = client._request("get", "/api/v3.1/tools", cast_to=Echo)

    assert result.ok is True
    assert caplog.messages == []


@respx.mock
def test_sync_logging_handler_failure_is_advisory(client: Composio, exploding_logger: None) -> None:
    respx.get(f"{BASE_URL}/api/v3.1/tools").mock(return_value=httpx.Response(200, json={"ok": True}))

    result = client._request("get", "/api/v3.1/tools", cast_to=Echo)

    assert result.ok is True


@respx.mock
async def test_async_logging_handler_failure_is_advisory(
    async_client: AsyncComposio, exploding_logger: None
) -> None:
    respx.get(f"{BASE_URL}/api/v3.1/tools").mock(return_value=httpx.Response(200, json={"ok": True}))

    result = await async_client._request("get", "/api/v3.1/tools", cast_to=Echo)

    assert result.ok is True
    await async_client.aclose()
