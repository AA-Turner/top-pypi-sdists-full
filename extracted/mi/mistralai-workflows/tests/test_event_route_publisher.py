import json
from collections.abc import AsyncIterator, Callable, Coroutine
from contextlib import asynccontextmanager
from dataclasses import dataclass
from http import HTTPStatus
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
    execution_token: str | None = _EXECUTION_TOKEN,
    events_api_version: str = "v2",
) -> AsyncIterator[EventRoutePublisher]:
    worker_client = create_http_test_worker_client(httpx.MockTransport(capture_request))
    publisher = EventRoutePublisher(worker_client, events_api_version=events_api_version)
    workflow_context = None if execution_token is None else create_test_workflow_context(execution_token)

    with patch(_CONTEXT_PATCH, return_value=workflow_context):
        async with worker_client:
            yield publisher


@dataclass(frozen=True)
class _Coded404Scenario:
    failure_path: str
    detail: str
    code: str


@dataclass(frozen=True)
class _DowngradeScenario:
    failure_path: str
    status: HTTPStatus
    body: dict[str, str]


_CODED_404_SCENARIOS = (
    pytest.param(
        _Coded404Scenario(
            failure_path="/v2/workflows/workers/event-route-token",
            detail="Execution token not found",
            code=EVENT_ROUTE_EXECUTION_TOKEN_NOT_FOUND_CODE,
        ),
        id="exchange-404",
    ),
    pytest.param(
        _Coded404Scenario(
            failure_path="/v2/workflows/events",
            detail="Exact execution row not materialized",
            code=EVENT_ROUTE_SCOPE_NOT_FOUND_CODE,
        ),
        id="send-404",
    ),
)

_DOWNGRADE_SCENARIOS = (
    pytest.param(
        _DowngradeScenario(
            failure_path="/v2/workflows/workers/event-route-token",
            status=HTTPStatus.CONFLICT,
            body={"detail": "Unsupported scope", "code": EVENT_ROUTE_TOKEN_SCOPE_UNSUPPORTED_CODE},
        ),
        id="scope-unsupported-exchange",
    ),
    pytest.param(
        _DowngradeScenario(
            failure_path="/v2/workflows/workers/event-route-token",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            body={"detail": "Token endpoint unavailable"},
        ),
        id="exchange-500",
    ),
    pytest.param(
        _DowngradeScenario(
            failure_path="/v2/workflows/events",
            status=HTTPStatus.NOT_FOUND,
            body={"detail": "Not found"},
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
    @pytest.mark.parametrize(
        ("events", "events_api_version", "execution_token"),
        [
            pytest.param([], "v2", _EXECUTION_TOKEN, id="empty-batch"),
            pytest.param([create_test_workflow_event()], "v1", _EXECUTION_TOKEN, id="v1-mode"),
            pytest.param([create_test_workflow_event()], "v2", None, id="no-execution-token"),
            pytest.param(
                [
                    create_test_workflow_event(),
                    create_test_workflow_event(event_id="evt-1", parent_workflow_exec_id="parent"),
                ],
                "v2",
                _EXECUTION_TOKEN,
                id="child-event-in-batch",
            ),
            pytest.param(
                [
                    create_test_workflow_event(workflow_exec_id="exec-a", workflow_run_id="run-a"),
                    create_test_workflow_event(
                        event_id="evt-1",
                        workflow_exec_id="exec-b",
                        workflow_run_id="run-b",
                    ),
                ],
                "v2",
                _EXECUTION_TOKEN,
                id="mixed-scopes",
            ),
        ],
    )
    async def test_publish_events_skips_v2(
        self,
        events: list[WorkflowEvent],
        events_api_version: str,
        execution_token: str | None,
    ) -> None:
        transport = _MockEventRouteTransport()

        async with _publisher_harness(
            transport,
            execution_token=execution_token,
            events_api_version=events_api_version,
        ) as publisher:
            assert await publisher.publish_events(events) is False
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
            assert await publisher.publish_events(events) is True

        assert transport.requests == [
            ("/v2/workflows/workers/event-route-token", None),
            (send_path, "route-token-1"),
            ("/v2/workflows/workers/event-route-token", None),
            (send_path, "route-token-2"),
        ]

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("events", "send_path"), _EVENT_CASES)
    @pytest.mark.parametrize("scenario", _CODED_404_SCENARIOS)
    async def test_coded_404_does_not_downgrade(
        self,
        scenario: _Coded404Scenario,
        events: list[WorkflowEvent],
        send_path: str,
    ) -> None:
        failure_path = scenario.failure_path
        if failure_path == "/v2/workflows/events":
            failure_path = send_path

        def fail_request(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                HTTPStatus.NOT_FOUND,
                json={"detail": scenario.detail, "code": scenario.code},
            )

        transport = _MockEventRouteTransport(overrides={failure_path: fail_request})

        async with _publisher_harness(transport) as publisher:
            with pytest.raises(WorkflowsException) as exc_info:
                await publisher.publish_events(events)

        _assert_workflows_exception_code(exc_info, HTTPStatus.NOT_FOUND, scenario.code)
        if scenario.failure_path == "/v2/workflows/workers/event-route-token":
            assert [path for path, _ in transport.requests] == ["/v2/workflows/workers/event-route-token"]
            return
        assert [path for path, _ in transport.requests] == ["/v2/workflows/workers/event-route-token", send_path]

    @pytest.mark.asyncio
    async def test_route_token_cache_is_reused_per_run(self) -> None:
        transport = _MockEventRouteTransport()

        async with _publisher_harness(transport) as publisher:
            assert await publisher.publish_events([create_test_workflow_event(event_id="evt-1")]) is True
            assert await publisher.publish_events([create_test_workflow_event(event_id="evt-2")]) is True

        assert transport.requests == [
            ("/v2/workflows/workers/event-route-token", None),
            ("/v2/workflows/events", "route-token-1"),
            ("/v2/workflows/events", "route-token-1"),
        ]

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("events", "send_path"), _EVENT_CASES)
    @pytest.mark.parametrize("scenario", _DOWNGRADE_SCENARIOS)
    async def test_publish_events_returns_false_for_downgradable_v2_failures(
        self,
        scenario: _DowngradeScenario,
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
            assert await publisher.publish_events(events) is False

        if scenario.failure_path == "/v2/workflows/workers/event-route-token":
            assert [path for path, _ in transport.requests] == ["/v2/workflows/workers/event-route-token"]
            return
        assert [path for path, _ in transport.requests] == ["/v2/workflows/workers/event-route-token", send_path]

    @pytest.mark.asyncio
    async def test_publish_events_returns_false_for_route_token_transport_failures(self) -> None:
        def fail_route_token(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("token endpoint unavailable", request=request)

        transport = _MockEventRouteTransport(overrides={"/v2/workflows/workers/event-route-token": fail_route_token})

        async with _publisher_harness(transport) as publisher:
            assert await publisher.publish_events([create_test_workflow_event()]) is False

        assert [path for path, _ in transport.requests] == ["/v2/workflows/workers/event-route-token"]

    @pytest.mark.asyncio
    async def test_publish_events_returns_false_for_child_workflow_events(self) -> None:
        transport = _MockEventRouteTransport()

        async with _publisher_harness(transport) as publisher:
            assert (
                await publisher.publish_events([create_test_workflow_event(parent_workflow_exec_id="parent-1")])
                is False
            )
        assert transport.requests == []

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
                await publisher.publish_events([create_test_workflow_event(event_id="evt-1")])
            _assert_workflows_exception_code(exc_info, HTTPStatus.UNAUTHORIZED, EVENT_ROUTE_TOKEN_INVALID_CODE)

            assert await publisher.publish_events([create_test_workflow_event(event_id="evt-2")]) is True

        assert transport.requests == [
            ("/v2/workflows/workers/event-route-token", None),
            ("/v2/workflows/events", "route-token-1"),
            ("/v2/workflows/workers/event-route-token", None),
            ("/v2/workflows/events", "route-token-2"),
        ]
