from collections.abc import AsyncIterator, Callable, Coroutine
from contextlib import asynccontextmanager
from http import HTTPStatus
from unittest.mock import patch

import httpx
import pytest

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.protocol.v2.worker import (
    EVENT_ROUTE_TOKEN_INVALID_CODE,
    EVENT_ROUTE_TOKEN_SCOPE_UNSUPPORTED_CODE,
)
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

from .utils import create_http_test_worker_client, create_test_workflow_context, create_test_workflow_event

_CONTEXT_PATCH = "mistralai.workflows.core._events.event_route_publisher.retrieve_context"
_EXECUTION_TOKEN = "00000000-0000-0000-0000-000000000001"
_TransportHandler = Callable[[httpx.Request], Coroutine[None, None, httpx.Response]]


def _make_event_context(worker_client: PrivateWorkerClient) -> EventContext:
    return EventContext(
        worker_client.events,
        worker_client,
        events_api_version="v2",
    )


@asynccontextmanager
async def _event_context_harness(capture_request: _TransportHandler) -> AsyncIterator[EventContext]:
    worker_client = create_http_test_worker_client(httpx.MockTransport(capture_request))
    with patch(_CONTEXT_PATCH, return_value=create_test_workflow_context(_EXECUTION_TOKEN)):
        async with worker_client, _make_event_context(worker_client) as event_context:
            yield event_context


class TestEventContextRouteSelection:
    @pytest.mark.asyncio
    async def test_publish_event_falls_back_to_v1_when_v2_route_returns_false(self) -> None:
        requests: list[str] = []

        async def capture_request(request: httpx.Request) -> httpx.Response:
            requests.append(request.url.path)
            if request.url.path == "/v2/workflows/workers/event-route-token":
                return httpx.Response(
                    HTTPStatus.CONFLICT,
                    json={"detail": "Unsupported scope", "code": EVENT_ROUTE_TOKEN_SCOPE_UNSUPPORTED_CODE},
                )
            if request.url.path == "/v1/workflows/events":
                return httpx.Response(200, json={"status": "success"})
            raise AssertionError(f"Unexpected request path: {request.url.path}")

        async with _event_context_harness(capture_request) as event_context:
            await event_context.publish_event(create_test_workflow_event())

        assert requests == [
            "/v2/workflows/workers/event-route-token",
            "/v1/workflows/events",
        ]

    @pytest.mark.asyncio
    async def test_publish_event_keeps_best_effort_behavior_for_hard_v2_failures(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        requests: list[str] = []

        async def capture_request(request: httpx.Request) -> httpx.Response:
            requests.append(request.url.path)
            if request.url.path == "/v2/workflows/workers/event-route-token":
                return httpx.Response(200, json={"route_token": "route-token-1", "expires_in_seconds": 60})
            if request.url.path == "/v2/workflows/events":
                return httpx.Response(
                    HTTPStatus.UNAUTHORIZED,
                    json={"detail": "Invalid route token", "code": EVENT_ROUTE_TOKEN_INVALID_CODE},
                )
            raise AssertionError(f"Unexpected request path: {request.url.path}")

        async with _event_context_harness(capture_request) as event_context:
            await event_context.publish_event(create_test_workflow_event())

        assert requests == [
            "/v2/workflows/workers/event-route-token",
            "/v2/workflows/events",
        ]
        assert "Failed to send workflow event batch" in caplog.text
