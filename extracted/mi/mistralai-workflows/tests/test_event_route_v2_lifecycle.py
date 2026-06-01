"""Lifecycle tests for v2 event-route publishing."""

from __future__ import annotations

import asyncio
import json
import uuid
from contextlib import contextmanager
from typing import Any, Generator
from unittest.mock import patch

import httpx
import pytest
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition
from mistralai.workflows.models import WorkflowContext
from mistralai.workflows.protocol.v2.worker import (
    EVENT_ROUTE_TOKEN_EXPIRED_CODE,
    EVENT_ROUTE_TOKEN_HEADER,
)

from . import fixtures_event_route_lifecycle as _fixtures
from .fixtures_event_route_lifecycle import (
    ContinueAsNewWorkflow,
    InterleavedWorkflow,
    IterationInput,
    RetryWorkflow,
    SingleActivityWorkflow,
    TwoActivityWorkflow,
    route_token_task,
    route_token_task_fail_once,
    route_token_task_logged,
    route_token_task_sync_point,
)
from .utils import create_http_test_worker_client, create_test_worker_with_events

_CONTEXT_PATCH = "mistralai.workflows.core._events.event_route_publisher.retrieve_context"


@pytest.fixture(autouse=True)
def _reset_event_route_lifecycle_state() -> Generator[None, None, None]:
    _fixtures._interleave_events = None
    _fixtures._activity_log.clear()
    yield
    _fixtures._interleave_events = None
    _fixtures._activity_log.clear()


class _EventRouteTracker:
    def __init__(
        self,
        execution_token: str | None = None,
        workflow_token_map: dict[str, str] | None = None,
        expire_first_event_send: bool = False,
    ) -> None:
        self.route_token_requests: list[dict[str, Any]] = []
        self.v2_request_headers: list[str | None] = []
        self._execution_token = execution_token
        self._workflow_token_map = workflow_token_map
        self._expire_first_event_send = expire_first_event_send
        self._route_token_fetches = 0
        self._expired_once = False

    def _next_context(self) -> WorkflowContext | None:
        from temporalio import activity as temporal_activity

        workflow_id = temporal_activity.info().workflow_id
        assert workflow_id is not None

        execution_token = self._execution_token
        if self._workflow_token_map is not None:
            execution_token = self._workflow_token_map.get(workflow_id)
        if execution_token is None:
            return None
        return WorkflowContext(
            namespace="test-namespace",
            execution_id=workflow_id,
            execution_token=execution_token,
        )

    def _success_response(self, request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v2/workflows/events":
            return httpx.Response(200, json={"status": "success"})

        payload = json.loads(request.content.decode())
        return httpx.Response(200, json={"status": "success", "events_received": len(payload["events"])})

    async def capture_request(self, request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v2/workflows/workers/event-route-token":
            self.route_token_requests.append(json.loads(request.content.decode()))
            self._route_token_fetches += 1
            return httpx.Response(
                200,
                json={
                    "route_token": f"route-token-{self._route_token_fetches}",
                    "expires_in_seconds": 60,
                },
            )

        if request.url.path in {"/v2/workflows/events", "/v2/workflows/events/batch"}:
            route_token = request.headers.get(EVENT_ROUTE_TOKEN_HEADER)
            self.v2_request_headers.append(route_token)
            if self._expire_first_event_send and route_token == "route-token-1" and not self._expired_once:
                self._expired_once = True
                return httpx.Response(
                    401,
                    json={"detail": "Expired route token", "code": EVENT_ROUTE_TOKEN_EXPIRED_CODE},
                )
            return self._success_response(request)

        raise AssertionError(f"Unexpected request path: {request.url.path}")

    @contextmanager
    def activate(self) -> Generator[None, None, None]:
        with patch(_CONTEXT_PATCH, side_effect=self._next_context):
            yield


@pytest.mark.asyncio
async def test_single_activity_uses_v2_route_tokens_in_worker_lifecycle(
    temporal_env: WorkflowEnvironment,
) -> None:
    tracker = _EventRouteTracker(execution_token=str(uuid.uuid4()))
    workflow_id = "test-event-route-single-activity"
    worker_client = create_http_test_worker_client(httpx.MockTransport(tracker.capture_request))

    with tracker.activate():
        async with (
            worker_client,
            EventContext(
                worker_client.events,
                worker_client,
                events_api_version="v2",
            ),
        ):
            async with create_test_worker_with_events(
                temporal_env,
                workflows=[SingleActivityWorkflow],
                activities=[route_token_task],
            ):
                workflow_def = get_workflow_definition(SingleActivityWorkflow)
                assert workflow_def is not None
                handle = await temporal_env.client.start_workflow(
                    workflow_def.name,
                    id=workflow_id,
                    task_queue="test-task-queue",
                )
                await handle.result()

    assert len(tracker.route_token_requests) == 1
    assert tracker.route_token_requests[0]["execution_token"] == tracker._execution_token
    assert tracker.route_token_requests[0]["workflow_exec_id"] == workflow_id
    assert tracker.v2_request_headers
    assert all(header == "route-token-1" for header in tracker.v2_request_headers)


@pytest.mark.asyncio
async def test_route_token_cache_is_reused_across_multiple_activities(
    temporal_env: WorkflowEnvironment,
) -> None:
    tracker = _EventRouteTracker(execution_token=str(uuid.uuid4()))
    worker_client = create_http_test_worker_client(httpx.MockTransport(tracker.capture_request))

    with tracker.activate():
        async with (
            worker_client,
            EventContext(
                worker_client.events,
                worker_client,
                events_api_version="v2",
            ),
        ):
            async with create_test_worker_with_events(
                temporal_env,
                workflows=[TwoActivityWorkflow],
                activities=[route_token_task],
            ):
                workflow_def = get_workflow_definition(TwoActivityWorkflow)
                assert workflow_def is not None
                handle = await temporal_env.client.start_workflow(
                    workflow_def.name,
                    id="test-event-route-two-activities",
                    task_queue="test-task-queue",
                )
                await handle.result()

    assert len(tracker.route_token_requests) == 1
    assert tracker.route_token_requests[0]["workflow_exec_id"] == "test-event-route-two-activities"
    assert len({header for header in tracker.v2_request_headers if header is not None}) == 1


@pytest.mark.asyncio
async def test_expired_route_token_refreshes_under_real_worker_execution(
    temporal_env: WorkflowEnvironment,
) -> None:
    tracker = _EventRouteTracker(
        execution_token=str(uuid.uuid4()),
        expire_first_event_send=True,
    )
    worker_client = create_http_test_worker_client(httpx.MockTransport(tracker.capture_request))

    with tracker.activate():
        async with (
            worker_client,
            EventContext(
                worker_client.events,
                worker_client,
                events_api_version="v2",
            ),
        ):
            async with create_test_worker_with_events(
                temporal_env,
                workflows=[TwoActivityWorkflow],
                activities=[route_token_task],
            ):
                workflow_def = get_workflow_definition(TwoActivityWorkflow)
                assert workflow_def is not None
                handle = await temporal_env.client.start_workflow(
                    workflow_def.name,
                    id="test-event-route-expired-refresh",
                    task_queue="test-task-queue",
                )
                await handle.result()

    assert len(tracker.route_token_requests) == 2
    assert "route-token-1" in tracker.v2_request_headers
    assert "route-token-2" in tracker.v2_request_headers


@pytest.mark.asyncio
async def test_route_token_cache_survives_activity_retry(
    temporal_env: WorkflowEnvironment,
) -> None:
    tracker = _EventRouteTracker(execution_token=str(uuid.uuid4()))
    worker_client = create_http_test_worker_client(httpx.MockTransport(tracker.capture_request))

    with tracker.activate():
        async with (
            worker_client,
            EventContext(
                worker_client.events,
                worker_client,
                events_api_version="v2",
            ),
        ):
            async with create_test_worker_with_events(
                temporal_env,
                workflows=[RetryWorkflow],
                activities=[route_token_task_fail_once],
            ):
                workflow_def = get_workflow_definition(RetryWorkflow)
                assert workflow_def is not None
                handle = await temporal_env.client.start_workflow(
                    workflow_def.name,
                    id="test-event-route-retry",
                    task_queue="test-task-queue",
                )
                await handle.result()

    assert len(tracker.route_token_requests) == 1


@pytest.mark.asyncio
async def test_continue_as_new_remints_for_each_root_run_scope(
    temporal_env: WorkflowEnvironment,
) -> None:
    tracker = _EventRouteTracker(execution_token=str(uuid.uuid4()))
    worker_client = create_http_test_worker_client(httpx.MockTransport(tracker.capture_request))

    with tracker.activate():
        async with (
            worker_client,
            EventContext(
                worker_client.events,
                worker_client,
                events_api_version="v2",
            ),
        ):
            async with create_test_worker_with_events(
                temporal_env,
                workflows=[ContinueAsNewWorkflow],
                activities=[route_token_task],
            ):
                workflow_def = get_workflow_definition(ContinueAsNewWorkflow)
                assert workflow_def is not None
                handle = await temporal_env.client.start_workflow(
                    workflow_def.name,
                    IterationInput(iteration=0).model_dump(),
                    id="test-event-route-can",
                    task_queue="test-task-queue",
                )
                await handle.result()

    assert len(tracker.route_token_requests) == 2
    assert {request["workflow_exec_id"] for request in tracker.route_token_requests} == {"test-event-route-can"}
    assert len({request["workflow_run_id"] for request in tracker.route_token_requests}) == 2


@pytest.mark.asyncio
async def test_interleaved_workflows_keep_route_tokens_scoped_per_execution() -> None:
    workflow_id_a = "test-event-route-interleaved-a"
    workflow_id_b = "test-event-route-interleaved-b"
    workflow_token_map = {
        workflow_id_a: str(uuid.uuid4()),
        workflow_id_b: str(uuid.uuid4()),
    }
    tracker = _EventRouteTracker(workflow_token_map=workflow_token_map)
    worker_client = create_http_test_worker_client(httpx.MockTransport(tracker.capture_request))

    _fixtures._interleave_events = {
        workflow_id_a: asyncio.Event(),
        workflow_id_b: asyncio.Event(),
    }

    try:
        # Use start_local so concurrent activities can block on asyncio.Event without time-skipping.
        async with await WorkflowEnvironment.start_local() as env:
            with tracker.activate():
                async with (
                    worker_client,
                    EventContext(
                        worker_client.events,
                        worker_client,
                        events_api_version="v2",
                    ),
                ):
                    async with create_test_worker_with_events(
                        env,
                        workflows=[InterleavedWorkflow],
                        activities=[route_token_task_sync_point, route_token_task_logged],
                    ):
                        workflow_def = get_workflow_definition(InterleavedWorkflow)
                        assert workflow_def is not None

                        handle_a = await env.client.start_workflow(
                            workflow_def.name,
                            id=workflow_id_a,
                            task_queue="test-task-queue",
                        )
                        handle_b = await env.client.start_workflow(
                            workflow_def.name,
                            id=workflow_id_b,
                            task_queue="test-task-queue",
                        )
                        await asyncio.gather(handle_a.result(), handle_b.result())
    finally:
        _fixtures._interleave_events = None

    activity_names = [name for _, name in _fixtures._activity_log]
    sync_indices = [index for index, name in enumerate(activity_names) if name == "route_token_task_sync_point"]
    logged_indices = [index for index, name in enumerate(activity_names) if name == "route_token_task_logged"]
    assert len(sync_indices) == 2
    assert len(logged_indices) == 2
    assert max(sync_indices) < min(logged_indices)

    assert len(tracker.route_token_requests) == 2
    assert {request["workflow_exec_id"] for request in tracker.route_token_requests} == {
        workflow_id_a,
        workflow_id_b,
    }
    assert {request["execution_token"] for request in tracker.route_token_requests} == set(workflow_token_map.values())
