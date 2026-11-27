import json
from collections.abc import AsyncIterator, Callable, Coroutine
from contextlib import asynccontextmanager
from dataclasses import dataclass
from http import HTTPStatus
from typing import Any
from unittest.mock import patch

import httpx
import pytest

from mistralai.workflows.core._events.event_route_publisher import EventRoutePublisher
from mistralai.workflows.exceptions import WorkflowsException
from mistralai.workflows.protocol.v1.events import WorkflowEvent
from mistralai.workflows.protocol.v2.worker import (
    EVENT_ROUTE_EXECUTION_TOKEN_NOT_FOUND_CODE,
    EVENT_ROUTE_SCOPE_NOT_FOUND_CODE,
    EVENT_ROUTE_TOKEN_EXPIRED_CODE,
    EVENT_ROUTE_TOKEN_HEADER,
    EVENT_ROUTE_TOKEN_INVALID_CODE,
    EVENT_ROUTE_TOKEN_SCOPE_UNSUPPORTED_CODE,
)

from .utils import create_http_test_worker_client, create_test_workflow_context, create_test_workflow_event

_CONTEXT_PATCH = "mistralai.workflows.core._events.event_route_publisher.retrieve_context"
_EXECUTION_TOKEN = "00000000-0000-0000-0000-000000000001"
_TransportHandler = Callable[[httpx.Request], Coroutine[None, None, httpx.Response]]
_TransportOverride = Callable[[httpx.Request], httpx.Response]


def _make_event_batch(count: int) -> list[WorkflowEvent]:
    return [create_test_workflow_event(event_id=f"evt-{index}") for index in range(count)]


def _route_token_response(route_token: str) -> httpx.Response:
    return httpx.Response(200, json={"route_token": route_token, "expires_in_seconds": 60})


def _event_publish_success_response(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/v2/workflows/events":
        return httpx.Response(200, json={"status": "success"})

    payload = json.loads(request.content.decode())
    return httpx.Response(200, json={"status": "success", "events_received": len(payload["events"])})


def _assert_workflows_exception_code(
    exc_info: pytest.ExceptionInfo[WorkflowsException],
    status: HTTPStatus,
    code: str,
) -> None:
    assert exc_info.value.status == status
    assert exc_info.value.code == code


class _MockEventRouteTransport:
    def __init__(
        self,
        *,
        overrides: dict[str, _TransportOverride] | None = None,
    ) -> None:
        self.requests: list[tuple[str, str | None]] = []
        self._route_token_fetches = 0
        self._overrides = overrides or {}

    async def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append((request.url.path, request.headers.get(EVENT_ROUTE_TOKEN_HEADER)))

        override = self._overrides.get(request.url.path)
        if override is not None:
            return override(request)

        if request.url.path == "/v2/workflows/workers/event-route-token":
            self._route_token_fetches += 1
            return _route_token_response(f"route-token-{self._route_token_fetches}")

        if request.url.path in {"/v2/workflows/events", "/v2/workflows/events/batch"}:
            return _event_publish_success_response(request)

        raise AssertionError(f"Unexpected request path: {request.url.path}")


@asynccontextmanager
async def _publisher_harness(
    capture_request: _TransportHandler,
) -> AsyncIterator[EventRoutePublisher]:
    worker_client = create_http_test_worker_client(httpx.MockTransport(capture_request))
    publisher = EventRoutePublisher(worker_client)

    async with worker_client:
        yield publisher


@dataclass(frozen=True)
class _V2FailureScenario:
    failure_path: str
    status: HTTPStatus
    body: dict[str, str]


_V2_FAILURE_SCENARIOS = (
    pytest.param(
        _V2FailureScenario(
            failure_path="/v2/workflows/workers/event-route-token",
            status=HTTPStatus.NOT_FOUND,
            body={"detail": "Execution token not found", "code": EVENT_ROUTE_EXECUTION_TOKEN_NOT_FOUND_CODE},
        ),
        id="exchange-404",
    ),
    pytest.param(
        _V2FailureScenario(
            failure_path="/v2/workflows/workers/event-route-token",
            status=HTTPStatus.CONFLICT,
            body={"detail": "Unsupported scope", "code": EVENT_ROUTE_TOKEN_SCOPE_UNSUPPORTED_CODE},
        ),
        id="scope-unsupported-exchange",
    ),
    pytest.param(
        _V2FailureScenario(
            failure_path="/v2/workflows/workers/event-route-token",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            body={"detail": "Token endpoint unavailable"},
        ),
        id="exchange-500",
    ),
    pytest.param(
        _V2FailureScenario(
            failure_path="/v2/workflows/events",
            status=HTTPStatus.NOT_FOUND,
            body={"detail": "Exact execution row not materialized", "code": EVENT_ROUTE_SCOPE_NOT_FOUND_CODE},
        ),
        id="send-404",
    ),
)

_EVENT_CASES = (
    pytest.param([create_test_workflow_event()], "/v2/workflows/events", id="single"),
    pytest.param(_make_event_batch(2), "/v2/workflows/events/batch", id="batch"),
)


class TestEventRoutePublisher:
    @pytest.mark.asyncio
    async def test_empty_batch_does_not_publish(self) -> None:
        transport = _MockEventRouteTransport()

        async with _publisher_harness(transport) as publisher:
            await publisher.publish([])
        assert transport.requests == []

    @pytest.mark.asyncio
    async def test_mint_request_identifies_run_by_ids(self) -> None:
        # The route token is minted from (workflow_exec_id, workflow_run_id), not a secret token.
        captured: dict[str, Any] = {}

        async def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path == "/v2/workflows/workers/event-route-token":
                captured.update(json.loads(request.content.decode()))
                return _route_token_response("route-token-1")
            return _event_publish_success_response(request)

        async with _publisher_harness(handler) as publisher:
            await publisher.publish([create_test_workflow_event(workflow_exec_id="exec-1", workflow_run_id="run-1")])

        assert captured["workflow_exec_id"] == "exec-1"
        assert captured["workflow_run_id"] == "run-1"
        assert captured.get("execution_token") is None

    @pytest.mark.asyncio
    async def test_token_less_request_surfaces_rejected_run_identity(self) -> None:
        def reject(request: httpx.Request) -> httpx.Response:
            return httpx.Response(HTTPStatus.UNPROCESSABLE_ENTITY, json={"detail": "execution_token required"})

        transport = _MockEventRouteTransport(overrides={"/v2/workflows/workers/event-route-token": reject})

        async with _publisher_harness(transport) as publisher:
            with pytest.raises(WorkflowsException) as exc_info:
                await publisher.publish([create_test_workflow_event()])

        assert exc_info.value.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert [path for path, _ in transport.requests] == ["/v2/workflows/workers/event-route-token"]

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "response",
        [
            pytest.param(
                httpx.Response(HTTPStatus.NOT_FOUND, json={"detail": "Not Found"}),
                id="route-absent-fastapi-json",
            ),
            pytest.param(
                httpx.Response(HTTPStatus.NOT_FOUND, text="<html>404</html>"),
                id="route-absent-gateway-html",
            ),
            pytest.param(
                httpx.Response(
                    HTTPStatus.SERVICE_UNAVAILABLE, json={"detail": "Event route token service is not enabled"}
                ),
                id="token-service-off",
            ),
        ],
    )
    async def test_unusable_v2_route_surfaces_error(self, response: httpx.Response) -> None:
        def reject(request: httpx.Request) -> httpx.Response:
            return response

        transport = _MockEventRouteTransport(overrides={"/v2/workflows/workers/event-route-token": reject})

        async with _publisher_harness(transport) as publisher:
            with pytest.raises(WorkflowsException) as exc_info:
                await publisher.publish([create_test_workflow_event()])

        assert exc_info.value.status == response.status_code
        assert [path for path, _ in transport.requests] == ["/v2/workflows/workers/event-route-token"]

    @pytest.mark.asyncio
    async def test_sends_execution_token_when_present_and_surfaces_errors(self) -> None:
        # With a token in context, it's sent (older APIs still work) and a mint error surfaces
        # instead of falling back to v1.
        captured: dict[str, Any] = {}

        async def handler(request: httpx.Request) -> httpx.Response:
            captured.update(json.loads(request.content.decode()))
            return httpx.Response(HTTPStatus.UNPROCESSABLE_ENTITY, json={"detail": "nope"})

        with patch(_CONTEXT_PATCH, return_value=create_test_workflow_context(_EXECUTION_TOKEN)):
            async with _publisher_harness(handler) as publisher:
                with pytest.raises(WorkflowsException):
                    await publisher.publish([create_test_workflow_event()])

        assert captured.get("execution_token") == _EXECUTION_TOKEN

    @pytest.mark.asyncio
    async def test_mixed_scope_batch_raises(self) -> None:
        transport = _MockEventRouteTransport()
        events = [
            create_test_workflow_event(workflow_exec_id="exec-a", workflow_run_id="run-a"),
            create_test_workflow_event(event_id="evt-1", workflow_exec_id="exec-b", workflow_run_id="run-b"),
        ]

        async with _publisher_harness(transport) as publisher:
            with pytest.raises(WorkflowsException):
                await publisher.publish(events)
        assert transport.requests == []

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("events", "send_path"),
        _EVENT_CASES,
    )
    async def test_expired_route_token_refreshes_and_retries_once(
        self,
        events: list[WorkflowEvent],
        send_path: str,
    ) -> None:
        def send_expired_then_succeed(request: httpx.Request) -> httpx.Response:
            if request.headers[EVENT_ROUTE_TOKEN_HEADER] == "route-token-1":
                return httpx.Response(
                    HTTPStatus.UNAUTHORIZED,
                    json={"detail": "Expired route token", "code": EVENT_ROUTE_TOKEN_EXPIRED_CODE},
                )
            if request.headers[EVENT_ROUTE_TOKEN_HEADER] == "route-token-2":
                return _event_publish_success_response(request)
            raise AssertionError(f"Unexpected request path: {request.url.path}")

        transport = _MockEventRouteTransport(overrides={send_path: send_expired_then_succeed})

        async with _publisher_harness(transport) as publisher:
            await publisher.publish(events)

        assert transport.requests == [
            ("/v2/workflows/workers/event-route-token", None),
            (send_path, "route-token-1"),
            ("/v2/workflows/workers/event-route-token", None),
            (send_path, "route-token-2"),
        ]

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("events", "send_path"), _EVENT_CASES)
    @pytest.mark.parametrize("scenario", _V2_FAILURE_SCENARIOS)
    async def test_v2_failure_raises_without_downgrade(
        self,
        scenario: _V2FailureScenario,
        events: list[WorkflowEvent],
        send_path: str,
    ) -> None:
        failure_path = scenario.failure_path
        if failure_path == "/v2/workflows/events":
            failure_path = send_path

        def fail_request(request: httpx.Request) -> httpx.Response:
            return httpx.Response(scenario.status, json=scenario.body)

        transport = _MockEventRouteTransport(overrides={failure_path: fail_request})

        async with _publisher_harness(transport) as publisher:
            with pytest.raises(WorkflowsException) as exc_info:
                await publisher.publish(events)

        assert exc_info.value.status == scenario.status
        expected_code = scenario.body.get("code")
        if expected_code is not None:
            assert exc_info.value.code == expected_code

        if scenario.failure_path == "/v2/workflows/workers/event-route-token":
            assert [path for path, _ in transport.requests] == ["/v2/workflows/workers/event-route-token"]
            return
        assert [path for path, _ in transport.requests] == ["/v2/workflows/workers/event-route-token", send_path]

    @pytest.mark.asyncio
    async def test_route_token_cache_is_reused_per_run(self) -> None:
        transport = _MockEventRouteTransport()

        async with _publisher_harness(transport) as publisher:
            await publisher.publish([create_test_workflow_event(event_id="evt-1")])
            await publisher.publish([create_test_workflow_event(event_id="evt-2")])

        assert transport.requests == [
            ("/v2/workflows/workers/event-route-token", None),
            ("/v2/workflows/events", "route-token-1"),
            ("/v2/workflows/events", "route-token-1"),
        ]

    @pytest.mark.asyncio
    async def test_route_token_transport_failure_raises(self) -> None:
        def fail_route_token(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("token endpoint unavailable", request=request)

        transport = _MockEventRouteTransport(overrides={"/v2/workflows/workers/event-route-token": fail_route_token})

        async with _publisher_harness(transport) as publisher:
            with pytest.raises(WorkflowsException):
                await publisher.publish([create_test_workflow_event()])

        assert [path for path, _ in transport.requests] == ["/v2/workflows/workers/event-route-token"]

    @pytest.mark.asyncio
    async def test_uses_v2_for_child_workflow_events(self) -> None:
        transport = _MockEventRouteTransport()

        async with _publisher_harness(transport) as publisher:
            await publisher.publish([create_test_workflow_event(parent_workflow_exec_id="parent-1")])

        assert transport.requests == [
            ("/v2/workflows/workers/event-route-token", None),
            ("/v2/workflows/events", "route-token-1"),
        ]

    @pytest.mark.asyncio
    async def test_uses_v2_for_child_workflow_event_batch(self) -> None:
        transport = _MockEventRouteTransport()

        async with _publisher_harness(transport) as publisher:
            await publisher.publish(
                [
                    create_test_workflow_event(),
                    create_test_workflow_event(event_id="evt-1", parent_workflow_exec_id="parent-1"),
                ]
            )

        assert transport.requests == [
            ("/v2/workflows/workers/event-route-token", None),
            ("/v2/workflows/events/batch", "route-token-1"),
        ]

    @pytest.mark.asyncio
    async def test_invalid_route_token_is_evicted_before_next_publish(self) -> None:
        def send_invalid_then_succeed(request: httpx.Request) -> httpx.Response:
            if request.headers[EVENT_ROUTE_TOKEN_HEADER] == "route-token-1":
                return httpx.Response(
                    HTTPStatus.UNAUTHORIZED,
                    json={"detail": "Invalid route token", "code": EVENT_ROUTE_TOKEN_INVALID_CODE},
                )
            if request.headers[EVENT_ROUTE_TOKEN_HEADER] == "route-token-2":
                return _event_publish_success_response(request)
            raise AssertionError(f"Unexpected request path: {request.url.path}")

        transport = _MockEventRouteTransport(overrides={"/v2/workflows/events": send_invalid_then_succeed})

        async with _publisher_harness(transport) as publisher:
            with pytest.raises(WorkflowsException) as exc_info:
                await publisher.publish([create_test_workflow_event(event_id="evt-1")])
            _assert_workflows_exception_code(exc_info, HTTPStatus.UNAUTHORIZED, EVENT_ROUTE_TOKEN_INVALID_CODE)

            await publisher.publish([create_test_workflow_event(event_id="evt-2")])

        assert transport.requests == [
            ("/v2/workflows/workers/event-route-token", None),
            ("/v2/workflows/events", "route-token-1"),
            ("/v2/workflows/workers/event-route-token", None),
            ("/v2/workflows/events", "route-token-2"),
        ]
