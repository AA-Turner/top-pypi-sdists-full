from collections.abc import AsyncIterator, Callable, Coroutine
from contextlib import asynccontextmanager
from http import HTTPStatus
from unittest.mock import MagicMock

import httpx
import pytest

from mistralai.workflows.core._events.event_context import EventContext, V1EventRouteForbiddenError
from mistralai.workflows.protocol.v2.worker import (
    EVENT_ROUTE_TOKEN_INVALID_CODE,
    EVENT_ROUTE_TOKEN_SCOPE_UNSUPPORTED_CODE,
)
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

from .utils import create_http_test_worker_client, create_test_workflow_event

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
    async with worker_client, _make_event_context(worker_client) as event_context:
        yield event_context


class TestEventContextRouteSelection:
    @pytest.mark.asyncio
    async def test_publish_event_does_not_fall_back_to_v1_on_v2_route_error(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        requests: list[str] = []

        async def capture_request(request: httpx.Request) -> httpx.Response:
            requests.append(request.url.path)
            if request.url.path == "/v2/workflows/workers/event-route-token":
                return httpx.Response(
                    HTTPStatus.CONFLICT,
                    json={"detail": "Unsupported scope", "code": EVENT_ROUTE_TOKEN_SCOPE_UNSUPPORTED_CODE},
                )
            raise AssertionError(f"Unexpected request path: {request.url.path}")

        async with _event_context_harness(capture_request) as event_context:
            await event_context.publish_event(create_test_workflow_event())

        assert requests == ["/v2/workflows/workers/event-route-token"]
        assert "Failed to send workflow event batch" in caplog.text

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


class TestV2OnlyEventRoute:
    @pytest.mark.asyncio
    async def test_raises_when_v1_would_be_used(self) -> None:
        # No v2 publisher (no worker client) → v1 is the only route → forbidden under v2-only.
        ctx = EventContext(MagicMock(), worker_client=None, events_api_version="v2-only")
        async with ctx:
            with pytest.raises(V1EventRouteForbiddenError):
                await ctx.publish_event(create_test_workflow_event())

    @pytest.mark.asyncio
    async def test_allows_v2(self) -> None:
        async def capture_request(request: httpx.Request) -> httpx.Response:
            if request.url.path == "/v2/workflows/workers/event-route-token":
                return httpx.Response(200, json={"route_token": "rt", "expires_in_seconds": 60})
            return httpx.Response(200, json={"status": "success"})

        worker_client = create_http_test_worker_client(httpx.MockTransport(capture_request))
        # v2-only mints by run identity (no token needed), so the v2 publish happens and no v1 fallback is attempted.
        async with (
            worker_client,
            EventContext(
                worker_client.events,
                worker_client,
                events_api_version="v2-only",
            ) as ctx,
        ):
            await ctx.publish_event(create_test_workflow_event())
