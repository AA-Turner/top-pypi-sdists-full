import asyncio
import dataclasses
from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager
from datetime import timedelta
from http import HTTPStatus
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import AsyncMock, patch

import httpx
import pytest
import temporalio.activity
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from pydantic import TypeAdapter
from temporalio.client import WorkflowExecutionStatus, WorkflowFailureError, WorkflowHandle
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError, ApplicationError, CancelledError
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core import metrics as workflows_metrics
from mistralai.workflows.core._events import event_activities, event_context
from mistralai.workflows.core._events.event_context import (
    EVENT_PUBLISH_FAILED_ERROR_TYPE,
    EventContext,
    V1EventRouteForbiddenError,
    _is_permanent_publish_error,
    activity_attempts_exhausted,
)
from mistralai.workflows.core._events.event_interceptor import _is_final_attempt
from mistralai.workflows.core._events.event_utils import EMITTER_ACTIVITY_NAMES
from mistralai.workflows.protocol.v1.events import (
    ActivityTaskCompleted,
    ActivityTaskFailed,
    ActivityTaskStarted,
    CustomTaskFailed,
    CustomTaskInProgress,
    CustomTaskStarted,
    WorkflowEvent,
    WorkflowExecutionCanceled,
    WorkflowExecutionCompleted,
    WorkflowExecutionFailed,
    WorkflowExecutionStarted,
)
from mistralai.workflows.protocol.v2.worker import EVENT_ROUTE_TOKEN_EXPIRED_CODE, EVENT_ROUTE_TOKEN_INVALID_CODE
from mistralai.workflows.testing import create_test_worker_with_events, wait_for_pending_inputs
from mistralai.workflows.worker_client.errors import NoResponseError, SDKError

from .fixtures import FailingWorkflow
from .fixtures_interactive_workflow import SimpleApprovalWorkflow
from .fixtures_task import (
    FailingTaskInWorkflowWorkflow,
    FailingTaskNoRetryWorkflow,
    StatefulTaskWorkflow,
    TaskInWorkflowWorkflow,
    failing_task_no_retry_activity,
    simple_task_activity,
    stateful_task_activity,
)

_event_adapter: TypeAdapter[WorkflowEvent] = TypeAdapter(WorkflowEvent)
_WORKFLOWS = [
    TaskInWorkflowWorkflow,
    FailingTaskInWorkflowWorkflow,
    FailingWorkflow,
    SimpleApprovalWorkflow,
    StatefulTaskWorkflow,
    FailingTaskNoRetryWorkflow,
]
_ACTIVITIES = [simple_task_activity, stateful_task_activity, failing_task_no_retry_activity]


def _http_error(status: HTTPStatus, code: str | None = None) -> SDKError:
    body = {"code": code} if code else None
    return SDKError("rejected", httpx.Response(status, json=body, request=httpx.Request("POST", "http://api/events")))


_BAD_REQUEST = _http_error(HTTPStatus.BAD_REQUEST)


@dataclasses.dataclass
class _EventsApi:
    rejected_types: tuple[type, ...]
    error: Exception
    rejections_left: int | None = None
    hang: bool = False
    rejected: list[WorkflowEvent] = dataclasses.field(default_factory=list)
    delivered: list[WorkflowEvent] = dataclasses.field(default_factory=list)

    def client(self) -> AsyncMock:
        async def send_events(*, events: list[Any], **kwargs: Any) -> None:
            parsed = [_event_adapter.validate_python(event) for event in events]
            rejected = next((e for e in parsed if self._rejects(e)), None)
            if rejected is not None:
                self.rejected.append(rejected)
                if self.rejections_left is not None:
                    self.rejections_left -= 1
                if self.hang:
                    await asyncio.Event().wait()
                raise self.error
            self.delivered.extend(parsed)

        async def send_event(*, event: Any, **kwargs: Any) -> None:
            await send_events(events=[event])

        client = AsyncMock()
        client.send_event_async = AsyncMock(side_effect=send_event)
        client.send_events_batch_async = AsyncMock(side_effect=send_events)
        return client

    def _rejects(self, event: WorkflowEvent) -> bool:
        # The emitter local activities send activity events too; only the user activity's are targeted.
        activity_name = getattr(event.attributes, "activity_name", None)
        return (
            isinstance(event, self.rejected_types)
            and activity_name not in EMITTER_ACTIVITY_NAMES
            and self.rejections_left != 0
        )

    def delivered_of(self, event_type: type) -> list[WorkflowEvent]:
        return [e for e in self.delivered if isinstance(e, event_type)]


@asynccontextmanager
async def _started(
    api: _EventsApi, env: WorkflowEnvironment, workflow: type, *args: Any, workflow_id: str
) -> AsyncIterator[WorkflowHandle]:
    async with EventContext(api.client()):
        async with create_test_worker_with_events(env, workflows=_WORKFLOWS, activities=_ACTIVITIES):
            yield await env.client.start_workflow(
                workflow,
                args=list(args),
                id=workflow_id,
                task_queue="test-task-queue",
                execution_timeout=timedelta(seconds=30),
            )


async def _run(api: _EventsApi, env: WorkflowEnvironment, workflow: type, *args: Any, workflow_id: str) -> Any:
    async with _started(api, env, workflow, *args, workflow_id=workflow_id) as handle:
        return await handle.result()


@pytest.fixture
def fast_emitter_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        event_activities,
        "_EMITTER_RETRY_POLICY",
        dataclasses.replace(event_activities._EMITTER_RETRY_POLICY, initial_interval=timedelta(milliseconds=50)),
    )


@pytest.fixture
def fast_publish_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(event_context, "_PUBLISH_RETRY_INITIAL_BACKOFF_SECONDS", 0.01)


@pytest.fixture
def publish_metrics() -> Iterator[InMemoryMetricReader]:
    reader = InMemoryMetricReader()
    meter_provider = MeterProvider(metric_readers=[reader])
    with (
        patch.object(workflows_metrics, "_counters", {}),
        patch.object(workflows_metrics.metrics, "get_meter", meter_provider.get_meter),
    ):
        yield reader


def _read_publish_retries(reader: InMemoryMetricReader) -> int:
    data = reader.get_metrics_data()
    return sum(
        int(point.value)
        for resource_metric in (data.resource_metrics if data else [])
        for scope_metric in resource_metric.scope_metrics
        for metric in scope_metric.metrics
        if metric.name == "mistral_workflows_event_publish_retries"
        for point in metric.data.data_points
    )


def _user_activity_events[E: WorkflowEvent](api: _EventsApi, event_type: type[E]) -> list[E]:
    return [e for e in api.delivered_of(event_type) if e.attributes.activity_name not in EMITTER_ACTIVITY_NAMES]


class TestActivityFinalAttempt:
    @pytest.mark.parametrize(
        ("retry_policy", "attempt", "error", "final"),
        [
            (RetryPolicy(maximum_attempts=3), 2, ValueError(), False),
            (RetryPolicy(maximum_attempts=3), 3, ValueError(), True),
            (RetryPolicy(maximum_attempts=0), 50, ValueError(), False),
            (RetryPolicy(maximum_attempts=0), 1, ApplicationError("x", non_retryable=True), True),
            (None, 1, ValueError(), True),
        ],
    )
    def test_unlimited_retries_are_never_final_unless_non_retryable(
        self, retry_policy: RetryPolicy | None, attempt: int, error: Exception, final: bool
    ) -> None:
        info = cast(temporalio.activity.Info, SimpleNamespace(retry_policy=retry_policy, attempt=attempt))
        assert _is_final_attempt(info, error) is final

    @pytest.mark.parametrize(
        ("retry_policy", "attempt", "exhausted"),
        [
            (RetryPolicy(maximum_attempts=3), 2, False),
            (RetryPolicy(maximum_attempts=3), 3, True),
            (RetryPolicy(maximum_attempts=0), 50, False),
            (None, 1, False),
        ],
    )
    def test_attempts_are_exhausted_only_at_a_known_maximum(
        self, retry_policy: RetryPolicy | None, attempt: int, exhausted: bool
    ) -> None:
        info = cast(temporalio.activity.Info, SimpleNamespace(retry_policy=retry_policy, attempt=attempt))
        assert activity_attempts_exhausted(info) is exhausted


class TestPublishErrorClassification:
    @pytest.mark.parametrize(
        ("error", "permanent"),
        [
            *[(_http_error(status), True) for status in (400, 401, 404)],
            *[(_http_error(status), False) for status in (408, 429, 503)],
            *[
                (_http_error(HTTPStatus.UNAUTHORIZED, code), False)
                for code in (EVENT_ROUTE_TOKEN_EXPIRED_CODE, EVENT_ROUTE_TOKEN_INVALID_CODE)
            ],
            (V1EventRouteForbiddenError("v2-only"), True),
            (AttributeError("no such client method"), True),
            (httpx.ConnectError("down"), False),
            (TimeoutError(), False),
            (NoResponseError(), False),
        ],
    )
    def test_only_errors_that_can_never_succeed_are_permanent(self, error: Exception, permanent: bool) -> None:
        assert _is_permanent_publish_error(error) is permanent


@pytest.mark.usefixtures("fast_emitter_retries")
class TestDurableWorkflowEvents:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("event_type", "error"),
        [
            (WorkflowExecutionStarted, httpx.ConnectError("down")),
            (CustomTaskInProgress, _http_error(HTTPStatus.SERVICE_UNAVAILABLE)),
            (WorkflowExecutionCompleted, _http_error(HTTPStatus.TOO_MANY_REQUESTS)),
        ],
    )
    async def test_transient_failure_delays_the_workflow_until_the_event_is_published(
        self, temporal_env: WorkflowEnvironment, event_type: type, error: Exception
    ) -> None:
        api = _EventsApi(rejected_types=(event_type,), error=error, rejections_left=2)

        await _run(api, temporal_env, TaskInWorkflowWorkflow, workflow_id=f"transient-{event_type.__name__}")

        assert len(api.rejected) == 2
        assert api.rejected[0].event_id in {e.event_id for e in api.delivered}

    @pytest.mark.asyncio
    @pytest.mark.parametrize("event_type", [WorkflowExecutionStarted, CustomTaskStarted, WorkflowExecutionCompleted])
    async def test_too_large_event_is_dropped_without_failing_the_workflow(
        self, temporal_env: WorkflowEnvironment, event_type: type
    ) -> None:
        api = _EventsApi(rejected_types=(event_type,), error=_http_error(HTTPStatus.REQUEST_ENTITY_TOO_LARGE))

        await _run(api, temporal_env, TaskInWorkflowWorkflow, workflow_id=f"too-large-{event_type.__name__}")

        assert api.rejected
        assert not api.delivered_of(event_type)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("event_type", "workflow", "args", "error", "detail"),
        [
            (WorkflowExecutionStarted, TaskInWorkflowWorkflow, (), _BAD_REQUEST, "HTTP 400"),
            (CustomTaskStarted, TaskInWorkflowWorkflow, (), _BAD_REQUEST, "HTTP 400"),
            (WorkflowExecutionCompleted, TaskInWorkflowWorkflow, (), _BAD_REQUEST, "HTTP 400"),
            (CustomTaskStarted, SimpleApprovalWorkflow, ({"request_id": "request"},), _BAD_REQUEST, "HTTP 400"),
            (CustomTaskStarted, TaskInWorkflowWorkflow, (), AttributeError("broken client"), "broken client"),
        ],
    )
    async def test_permanent_failure_fails_the_workflow_with_a_clear_error(
        self,
        temporal_env: WorkflowEnvironment,
        event_type: type,
        workflow: type,
        args: tuple[Any, ...],
        error: Exception,
        detail: str,
    ) -> None:
        api = _EventsApi(rejected_types=(event_type,), error=error)
        workflow_id = f"permanent-{workflow.__name__}-{event_type.__name__}-{type(error).__name__}"

        with pytest.raises(WorkflowFailureError) as exc_info:
            await _run(api, temporal_env, workflow, *args, workflow_id=workflow_id)

        cause = exc_info.value.cause
        assert isinstance(cause, ApplicationError)
        assert cause.type == EVENT_PUBLISH_FAILED_ERROR_TYPE
        assert api.rejected[0].event_type in cause.message
        assert detail in cause.message
        assert len(api.rejected) == 1
        [failed] = api.delivered_of(WorkflowExecutionFailed)
        assert cause.message in failed.attributes.failure.message

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("workflow", "args", "rejected_type", "error_message"),
        [
            (FailingWorkflow, ("boom",), WorkflowExecutionFailed, "Intentional failure: boom"),
            (FailingTaskInWorkflowWorkflow, (), CustomTaskFailed, "Task body failed"),
        ],
    )
    async def test_permanent_failure_does_not_hide_the_workflow_error(
        self,
        temporal_env: WorkflowEnvironment,
        workflow: type,
        args: tuple[Any, ...],
        rejected_type: type,
        error_message: str,
    ) -> None:
        api = _EventsApi(rejected_types=(rejected_type,), error=_BAD_REQUEST)

        with pytest.raises(WorkflowFailureError) as exc_info:
            await _run(api, temporal_env, workflow, *args, workflow_id=f"hidden-{workflow.__name__}")

        cause = exc_info.value.cause
        assert isinstance(cause, ApplicationError)
        assert cause.message == error_message
        assert len(api.rejected) == 1

    @pytest.mark.asyncio
    async def test_permanent_failure_does_not_hide_the_cancellation(self, temporal_env: WorkflowEnvironment) -> None:
        api = _EventsApi(
            rejected_types=(CustomTaskFailed, WorkflowExecutionCanceled),
            error=_BAD_REQUEST,
        )

        async with _started(
            api, temporal_env, SimpleApprovalWorkflow, {"request_id": "request"}, workflow_id="hidden-cancel"
        ) as handle:
            await wait_for_pending_inputs(handle)
            await handle.cancel()

            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()

        assert isinstance(exc_info.value.cause, CancelledError)
        assert (await handle.describe()).status == WorkflowExecutionStatus.CANCELED
        assert [type(e) for e in api.rejected] == [CustomTaskFailed, WorkflowExecutionCanceled]


@pytest.mark.usefixtures("fast_publish_retries")
class TestDurableActivityEvents:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("event_type", "error"),
        [
            (ActivityTaskStarted, httpx.ConnectError("down")),
            (CustomTaskInProgress, _http_error(HTTPStatus.SERVICE_UNAVAILABLE)),
            (ActivityTaskCompleted, _http_error(HTTPStatus.TOO_MANY_REQUESTS)),
        ],
    )
    async def test_transient_failure_delays_the_activity_until_the_event_is_published(
        self, temporal_env: WorkflowEnvironment, event_type: type, error: Exception
    ) -> None:
        api = _EventsApi(rejected_types=(event_type,), error=error, rejections_left=2)

        await _run(api, temporal_env, StatefulTaskWorkflow, workflow_id=f"activity-transient-{event_type.__name__}")

        assert len(api.rejected) == 2
        assert api.rejected[0].event_id in {e.event_id for e in api.delivered}
        assert len(_user_activity_events(api, ActivityTaskStarted)) == 1

    @pytest.mark.asyncio
    async def test_transient_failure_past_the_budget_reruns_the_activity(
        self, temporal_env: WorkflowEnvironment, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(event_context, "_PUBLISH_RETRY_BUDGET_SECONDS", 0)
        api = _EventsApi(
            rejected_types=(CustomTaskInProgress,),
            error=_http_error(HTTPStatus.SERVICE_UNAVAILABLE),
            rejections_left=1,
        )

        await _run(api, temporal_env, StatefulTaskWorkflow, workflow_id="activity-past-budget")

        assert len({e.event_id for e in _user_activity_events(api, ActivityTaskStarted)}) == 1
        # The test server leaves activity_info().retry_policy unset, so the attempt reports Failed, not Retrying.
        [attempt_failure] = _user_activity_events(api, ActivityTaskFailed)
        assert "could not be published" in attempt_failure.attributes.failure.message
        assert len(_user_activity_events(api, ActivityTaskCompleted)) == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize("event_type", [CustomTaskInProgress, ActivityTaskCompleted])
    async def test_too_large_event_is_dropped_without_failing_the_activity(
        self, temporal_env: WorkflowEnvironment, event_type: type
    ) -> None:
        api = _EventsApi(rejected_types=(event_type,), error=_http_error(HTTPStatus.REQUEST_ENTITY_TOO_LARGE))

        await _run(api, temporal_env, StatefulTaskWorkflow, workflow_id=f"activity-too-large-{event_type.__name__}")

        assert {e.event_id for e in api.rejected}.isdisjoint(e.event_id for e in api.delivered)
        assert len(_user_activity_events(api, ActivityTaskStarted)) == 1
        assert _user_activity_events(api, ActivityTaskFailed) == []

    @pytest.mark.asyncio
    @pytest.mark.parametrize("event_type", [ActivityTaskStarted, CustomTaskInProgress, ActivityTaskCompleted])
    async def test_permanent_failure_fails_the_activity_with_a_clear_error(
        self, temporal_env: WorkflowEnvironment, event_type: type
    ) -> None:
        api = _EventsApi(rejected_types=(event_type,), error=_BAD_REQUEST)

        with pytest.raises(WorkflowFailureError) as exc_info:
            await _run(api, temporal_env, StatefulTaskWorkflow, workflow_id=f"activity-permanent-{event_type.__name__}")

        assert isinstance(exc_info.value.cause, ActivityError)
        cause = exc_info.value.cause.cause
        assert isinstance(cause, ApplicationError)
        assert cause.type == EVENT_PUBLISH_FAILED_ERROR_TYPE
        assert "HTTP 400" in cause.message
        assert len(api.rejected) == 1
        [failed] = _user_activity_events(api, ActivityTaskFailed)
        assert cause.message in failed.attributes.failure.message

    @pytest.mark.asyncio
    @pytest.mark.parametrize("rejected_type", [CustomTaskFailed, ActivityTaskFailed])
    async def test_permanent_failure_does_not_hide_the_activity_error(
        self, temporal_env: WorkflowEnvironment, rejected_type: type
    ) -> None:
        api = _EventsApi(rejected_types=(rejected_type,), error=_BAD_REQUEST)

        with pytest.raises(WorkflowFailureError) as exc_info:
            await _run(
                api, temporal_env, FailingTaskNoRetryWorkflow, workflow_id=f"activity-hidden-{rejected_type.__name__}"
            )

        assert isinstance(exc_info.value.cause, ActivityError)
        cause = exc_info.value.cause.cause
        assert isinstance(cause, ApplicationError)
        assert cause.message == "Intentional test error"
        assert len(api.rejected) == 1

    @pytest.mark.asyncio
    async def test_failure_event_that_cannot_be_encoded_does_not_hide_the_activity_error(
        self, temporal_env: WorkflowEnvironment, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        encode = event_context.maybe_encode_event

        async def fail_on_activity_failed(event: WorkflowEvent, encoder: Any) -> WorkflowEvent:
            if isinstance(event, ActivityTaskFailed):
                raise ValueError("unencodable")
            return await encode(event, encoder)

        monkeypatch.setattr(event_context, "maybe_encode_event", fail_on_activity_failed)
        api = _EventsApi(rejected_types=(), error=_BAD_REQUEST)

        with pytest.raises(WorkflowFailureError) as exc_info:
            await _run(api, temporal_env, FailingTaskNoRetryWorkflow, workflow_id="activity-unencodable-failure")

        assert isinstance(exc_info.value.cause, ActivityError)
        assert exc_info.value.cause.cause.message == "Intentional test error"


# One event sent from workflow code (local activity emitter) and one sent from inside an activity.
_PUBLISH_PATHS = [
    pytest.param(TaskInWorkflowWorkflow, CustomTaskStarted, id="workflow-code"),
    pytest.param(StatefulTaskWorkflow, CustomTaskInProgress, id="activity"),
]


async def _wait_for_rejections(api: _EventsApi, count: int) -> None:
    async with asyncio.timeout(10):
        while len(api.rejected) < count:
            await asyncio.sleep(0.01)


@pytest.mark.usefixtures("fast_emitter_retries", "fast_publish_retries")
class TestEventPublishMetrics:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("workflow", "event_type", "hang"),
        [
            pytest.param(TaskInWorkflowWorkflow, CustomTaskStarted, False, id="workflow-code"),
            pytest.param(StatefulTaskWorkflow, CustomTaskInProgress, False, id="activity"),
            # Temporal cancels the emitter at its start-to-close timeout while the request still hangs.
            pytest.param(TaskInWorkflowWorkflow, CustomTaskStarted, True, id="workflow-code-hung-api"),
        ],
    )
    async def test_retries_are_counted_and_logged_with_the_stuck_run(
        self,
        temporal_env: WorkflowEnvironment,
        publish_metrics: InMemoryMetricReader,
        caplog: pytest.LogCaptureFixture,
        monkeypatch: pytest.MonkeyPatch,
        workflow: type,
        event_type: type,
        hang: bool,
    ) -> None:
        if hang:
            monkeypatch.setattr(event_activities, "_EMITTER_START_TO_CLOSE_TIMEOUT", timedelta(milliseconds=200))
        api = _EventsApi(rejected_types=(event_type,), error=_http_error(HTTPStatus.SERVICE_UNAVAILABLE), hang=hang)
        workflow_id = f"metrics-stalled-{workflow.__name__}-{hang}"

        async with _started(api, temporal_env, workflow, workflow_id=workflow_id) as handle:
            await _wait_for_rejections(api, 2)
            api.rejections_left = 0
            await handle.result()

        assert _read_publish_retries(publish_metrics) >= 2
        retry_logs = [r.getMessage() for r in caplog.records if "Retrying workflow event batch" in r.getMessage()]
        assert retry_logs
        assert all(api.rejected[0].workflow_run_id in message for message in retry_logs)

    @pytest.mark.asyncio
    async def test_cancelling_the_workflow_mid_publish_is_not_a_retry(
        self, temporal_env: WorkflowEnvironment, publish_metrics: InMemoryMetricReader, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Long enough that the cancellation, not the emitter timeout, interrupts the hung request.
        monkeypatch.setattr(event_activities, "_EMITTER_START_TO_CLOSE_TIMEOUT", timedelta(seconds=60))
        api = _EventsApi(rejected_types=(CustomTaskStarted,), error=_BAD_REQUEST, hang=True)

        async with _started(api, temporal_env, TaskInWorkflowWorkflow, workflow_id="metrics-cancelled") as handle:
            await _wait_for_rejections(api, 1)
            api.rejections_left = 0
            await handle.cancel()
            with pytest.raises(WorkflowFailureError):
                await handle.result()

        assert _read_publish_retries(publish_metrics) == 0

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("workflow", "event_type"), _PUBLISH_PATHS)
    async def test_permanent_failure_is_logged_with_the_failed_run(
        self,
        temporal_env: WorkflowEnvironment,
        caplog: pytest.LogCaptureFixture,
        workflow: type,
        event_type: type,
    ) -> None:
        api = _EventsApi(rejected_types=(event_type,), error=_BAD_REQUEST)

        with pytest.raises(WorkflowFailureError):
            await _run(api, temporal_env, workflow, workflow_id=f"metrics-permanent-{workflow.__name__}")

        [rejected] = api.rejected
        [record] = [r for r in caplog.records if "Workflow event permanently failed to publish" in r.getMessage()]
        assert "workflow.run_id" in record.getMessage()
        assert rejected.workflow_run_id in record.getMessage()
        assert rejected.event_type in record.getMessage()
