from collections.abc import AsyncIterator, Callable, Coroutine
from contextlib import asynccontextmanager
from http import HTTPStatus

import httpx
import pytest
from temporalio.exceptions import ApplicationError

from mistralai.workflows.core._events import event_context as event_context_module
from mistralai.workflows.core._events.event_context import EVENT_PUBLISH_FAILED_ERROR_TYPE, EventContext
from mistralai.workflows.core._events.event_route_publisher import EventRoutePublisher
from mistralai.workflows.protocol.v2.worker import (
    EVENT_ROUTE_TOKEN_EXPIRED_CODE,
    EVENT_ROUTE_TOKEN_INVALID_CODE,
    EVENT_ROUTE_TOKEN_SCOPE_UNSUPPORTED_CODE,
)
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

from .utils import create_http_test_worker_client, create_test_workflow_event

_TransportHandler = Callable[[httpx.Request], Coroutine[None, None, httpx.Response]]


def _make_event_context(worker_client: PrivateWorkerClient) -> EventContext:
    return EventContext(EventRoutePublisher(worker_client))


@asynccontextmanager
async def _event_context_harness(capture_request: _TransportHandler) -> AsyncIterator[EventContext]:
    worker_client = create_http_test_worker_client(httpx.MockTransport(capture_request))
    async with worker_client, _make_event_context(worker_client) as event_context:
        yield event_context


class TestEventContextRouteSelection:
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
            with pytest.raises(ApplicationError, match="HTTP 409") as exc_info:
                await event_context.publish_event(create_test_workflow_event())

        assert exc_info.value.type == EVENT_PUBLISH_FAILED_ERROR_TYPE
        assert exc_info.value.non_retryable
        assert requests == ["/v2/workflows/workers/event-route-token"]
        assert "Workflow event permanently failed to publish" in caplog.text

    @pytest.mark.parametrize(
        "error_code", [EVENT_ROUTE_TOKEN_EXPIRED_CODE, EVENT_ROUTE_TOKEN_INVALID_CODE], ids=["expired", "invalid"]
    )
    async def test_publish_event_refreshes_rejected_route_tokens(
        self,
        error_code: str,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(event_context_module, "_PUBLISH_RETRY_INITIAL_BACKOFF_SECONDS", 0.01)
        requests: list[str] = []

        async def capture_request(request: httpx.Request) -> httpx.Response:
            requests.append(request.url.path)
            if request.url.path == "/v2/workflows/workers/event-route-token":
                return httpx.Response(200, json={"route_token": "route-token-1", "expires_in_seconds": 60})
            if request.url.path == "/v2/workflows/events":
                if requests.count("/v2/workflows/events") == 2:
                    return httpx.Response(200, json={})
                # The API also reports a token signed with a rotated key as invalid, so both codes refresh.
                return httpx.Response(
                    HTTPStatus.UNAUTHORIZED,
                    json={"detail": "Rejected route token", "code": error_code},
                )
            raise AssertionError(f"Unexpected request path: {request.url.path}")

        async with _event_context_harness(capture_request) as event_context:
            await event_context.publish_event(create_test_workflow_event())

        assert (
            requests
            == [
                "/v2/workflows/workers/event-route-token",
                "/v2/workflows/events",
            ]
            * 2
        )


class TestSharedRouteTokenManager:
    async def test_other_clients_reuse_the_event_route_token(self) -> None:
        requests: list[str] = []

        async def capture_request(request: httpx.Request) -> httpx.Response:
            requests.append(request.url.path)
            if request.url.path == "/v2/workflows/workers/event-route-token":
                return httpx.Response(200, json={"route_token": "route-token-1", "expires_in_seconds": 60})
            if request.url.path == "/v2/workflows/events":
                return httpx.Response(200, json={})
            raise AssertionError(f"Unexpected request path: {request.url.path}")

        worker_client = create_http_test_worker_client(httpx.MockTransport(capture_request))
        publisher = EventRoutePublisher(worker_client)
        event = create_test_workflow_event()
        async with (
            worker_client,
            EventContext(
                publisher,
                worker_client=worker_client,
                route_token_manager=publisher.route_token_manager,
            ) as event_context,
        ):
            await event_context.publish_event(event)
            manager = event_context.event_route_token_manager
            assert manager is publisher.route_token_manager
            assert event_context.worker_client is worker_client
            token = await manager.get_token(event.workflow_exec_id, event.workflow_run_id)

        assert token == "route-token-1"
        assert requests.count("/v2/workflows/workers/event-route-token") == 1
