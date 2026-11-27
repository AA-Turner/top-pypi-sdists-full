import asyncio
import contextlib
import gc
from typing import Any, Literal

import pytest
from temporalio.api.enums.v1 import PendingActivityState
from temporalio.client import WorkflowFailureError, WorkflowHandle
from temporalio.common import RetryPolicy
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import _workflow_instance

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core.temporal.context_handler_interceptor import ContextHandlerInterceptor
from mistralai.workflows.protocol.v1.events import (
    CustomTaskFailed,
    WorkflowEventCategory,
    WorkflowExecutionCanceled,
    WorkflowExecutionCompleted,
    WorkflowExecutionFailed,
    WorkflowExecutionStarted,
)
from mistralai.workflows.testing import (
    activity_completed,
    activity_started,
    compare_itemwise,
    wait_for_pending_inputs,
    workflow_completed,
    workflow_failed,
    workflow_started,
)

from .fixtures import (
    CancelledInActivityWorkflow,
    CancelledInChildParentWorkflow,
    CancelledWhileWaitingWorkflow,
    CancelsOwnActivityWorkflow,
    CANParams,
    ChildWorkflow,
    ContinueAsNewWorkflow,
    FailingWorkflow,
    ParentWorkflow,
    ParkedWorkflowWithFailingCleanup,
    PureWorkflow,
    RetryingWorkflow,
    block_until_cancelled,
)
from .fixtures_interactive_workflow import SimpleApprovalWorkflow
from .utils import create_capturing_mock_event_publisher, create_test_worker_with_events, emitted


@pytest.mark.asyncio
async def test_basic_workflow_emits_lifecycle_events(
    temporal_env: WorkflowEnvironment, event_categories: frozenset[WorkflowEventCategory]
) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_event_publisher(captured_events)

    async with EventContext(mock_client, emitted_event_categories=event_categories):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[PureWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "pure_workflow",
                {"name": "test-value"},
                id="test-basic-workflow-events",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert result["result"] == "Workflow says: test-value"

            expected_events = [
                activity_started("__internal__emit_workflow_started", workflow_name="pure_workflow"),
                workflow_started("pure_workflow"),
                activity_completed("__internal__emit_workflow_started", workflow_name="pure_workflow"),
                activity_started("__internal__emit_workflow_completed", workflow_name="pure_workflow"),
                workflow_completed("pure_workflow"),
                activity_completed("__internal__emit_workflow_completed", workflow_name="pure_workflow"),
            ]

            errors = compare_itemwise(
                emitted(expected_events, event_categories),
                captured_events,
                exclude_paths={
                    "event_id",
                    "event_timestamp",
                    "root_workflow_exec_id",
                    "parent_workflow_exec_id",
                    "workflow_exec_id",
                    "workflow_run_id",
                    "attributes.task_id",
                    "attributes.input",
                    "attributes.result",
                },
            )
            assert len(errors) == 0, "Event sequence mismatch:\n" + "\n".join(errors)


@pytest.mark.asyncio
async def test_child_workflow_started_event_has_parent_exec_id(
    temporal_env_with_converter: WorkflowEnvironment,
) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_event_publisher(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env_with_converter,
            workflows=[ParentWorkflow, ChildWorkflow],
            interceptors=[ContextHandlerInterceptor()],
        ):
            handle = await temporal_env_with_converter.client.start_workflow(
                "parent_workflow",
                "test-child-events",
                id="test-child-parent-exec-id",
                task_queue="test-task-queue",
            )
            await handle.result()

    started_events = [e for e in captured_events if isinstance(e, WorkflowExecutionStarted)]
    parent_started = next(e for e in started_events if e.workflow_name == "parent_workflow")
    child_started = next(e for e in started_events if e.workflow_name == "child_workflow")

    assert parent_started.parent_workflow_exec_id is None
    assert child_started.parent_workflow_exec_id == parent_started.workflow_exec_id


@pytest.mark.asyncio
async def test_workflow_started_event_has_no_display_name(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_event_publisher(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[PureWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "pure_workflow",
                {"name": "test-value"},
                id="test-no-display-name-events",
                task_queue="test-task-queue",
            )

            await handle.result()

            started_events = [e for e in captured_events if isinstance(e, WorkflowExecutionStarted)]
            assert len(started_events) == 1
            assert started_events[0].attributes.display_name is None


@pytest.mark.asyncio
async def test_workflow_failure_emits_failed_event(
    temporal_env: WorkflowEnvironment, event_categories: frozenset[WorkflowEventCategory]
) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_event_publisher(captured_events)

    async with EventContext(mock_client, emitted_event_categories=event_categories):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[FailingWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "failing_workflow",
                {"message": "test-error"},
                id="test-workflow-failure-events",
                retry_policy=RetryPolicy(maximum_attempts=1),
                task_queue="test-task-queue",
            )

            async def wait_for_events(expected_count: int, timeout_seconds: float = 5.0) -> None:
                loop = asyncio.get_running_loop()
                deadline = loop.time() + timeout_seconds
                while loop.time() < deadline:
                    if len(captured_events) >= expected_count:
                        return
                    await asyncio.sleep(0.1)
                raise TimeoutError("Did not receive expected workflow events in time")

            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()
            assert "Intentional failure: test-error" in str(exc_info.value.cause)

            expected_events = [
                activity_started("__internal__emit_workflow_started", workflow_name="failing_workflow"),
                workflow_started("failing_workflow"),
                activity_completed("__internal__emit_workflow_started", workflow_name="failing_workflow"),
                activity_started("__internal__emit_workflow_failed", workflow_name="failing_workflow"),
                workflow_failed("failing_workflow"),
                activity_completed("__internal__emit_workflow_failed", workflow_name="failing_workflow"),
            ]
            await wait_for_events(expected_count=len(emitted(expected_events, event_categories)))

            errors = compare_itemwise(
                emitted(expected_events, event_categories),
                captured_events,
                exclude_paths={
                    "event_id",
                    "event_timestamp",
                    "root_workflow_exec_id",
                    "parent_workflow_exec_id",
                    "workflow_exec_id",
                    "workflow_run_id",
                    "attributes.task_id",
                    "attributes.input",
                    "attributes.result",
                    "attributes.failure.message",
                },
            )
            assert len(errors) == 0, "Event sequence mismatch:\n" + "\n".join(errors)


@pytest.mark.asyncio
async def test_continue_as_new_event_has_continued_run_id(
    temporal_env_with_converter: WorkflowEnvironment,
) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_event_publisher(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env_with_converter,
            workflows=[ContinueAsNewWorkflow],
            interceptors=[ContextHandlerInterceptor()],
        ):
            handle = await temporal_env_with_converter.client.start_workflow(
                "test-events-can-workflow",
                CANParams(iteration=0),
                id="test-can-continued-run-id",
                task_queue="test-task-queue",
            )
            await handle.result()

    started_events = [
        e
        for e in captured_events
        if isinstance(e, WorkflowExecutionStarted) and e.workflow_name == "test-events-can-workflow"
    ]
    assert len(started_events) == 2

    first_run = started_events[0]
    second_run = started_events[1]

    assert first_run.continued_run_id is None
    assert second_run.continued_run_id == first_run.workflow_run_id


@pytest.mark.asyncio
async def test_retrying_workflow_has_attempt_and_continued_run_id(
    temporal_env_with_converter: WorkflowEnvironment,
) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_event_publisher(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env_with_converter,
            workflows=[RetryingWorkflow],
            interceptors=[ContextHandlerInterceptor()],
        ):
            handle = await temporal_env_with_converter.client.start_workflow(
                "test-events-retrying-workflow",
                id="test-retrying-workflow-events",
                task_queue="test-task-queue",
                retry_policy=RetryPolicy(maximum_attempts=2),
            )
            await handle.result()

    started_events = [
        e
        for e in captured_events
        if isinstance(e, WorkflowExecutionStarted) and e.workflow_name == "test-events-retrying-workflow"
    ]
    assert len(started_events) == 2

    first_run = started_events[0]
    second_run = started_events[1]

    assert first_run.attributes.attempt == 1
    assert first_run.continued_run_id is None

    assert second_run.attributes.attempt == 2
    assert second_run.continued_run_id == first_run.workflow_run_id


async def _wait_until_parked(handle: WorkflowHandle[Any, Any], timeout_seconds: float = 10.0) -> None:
    """Wait until every workflow task the run was given has completed.

    Terminating a run while a workflow task is outstanding makes the worker evict it, and these
    tests need a run the worker never evicts. Commands such as markers or search attribute updates
    can follow the last completed task in the history, so look for whichever comes last.
    """
    deadline = asyncio.get_running_loop().time() + timeout_seconds
    while True:
        events = (await handle.fetch_history()).events
        for event in reversed(events):
            if event.HasField("workflow_task_completed_event_attributes"):
                return
            if event.HasField("workflow_task_scheduled_event_attributes"):
                break
        if asyncio.get_running_loop().time() > deadline:
            tail = [event.WhichOneof("attributes") for event in events[-6:]]
            raise AssertionError(
                f"workflow {handle.id} still had a workflow task outstanding after {timeout_seconds}s: {tail}"
            )
        await asyncio.sleep(0.05)


def _close_unevicted_runs_in_next_activation(
    monkeypatch: pytest.MonkeyPatch, workflow_id: str
) -> list[_workflow_instance._WorkflowInstanceImpl]:
    """Close the coroutines of a run the worker never evicted, the way the garbage collector does:
    while another workflow's activation is running. Returns the runs still left to close."""
    unevicted_runs = [
        instance
        for instance in gc.get_objects()
        if type(instance) is _workflow_instance._WorkflowInstanceImpl
        and instance.workflow_info().workflow_id == workflow_id
        and instance._tasks
    ]
    assert unevicted_runs

    original_run_once = _workflow_instance._WorkflowInstanceImpl._run_once

    def run_once_after_closing(self: _workflow_instance._WorkflowInstanceImpl, **kwargs: Any) -> None:
        while unevicted_runs:
            asyncio._set_running_loop(self)
            try:
                for task in list(unevicted_runs.pop()._tasks):
                    # The collector only reports "coroutine ignored GeneratorExit" as unraisable.
                    with contextlib.suppress(RuntimeError):
                        task.get_coro().close()
            finally:
                asyncio._set_running_loop(None)
        original_run_once(self, **kwargs)

    monkeypatch.setattr(_workflow_instance._WorkflowInstanceImpl, "_run_once", run_once_after_closing)
    return unevicted_runs


@pytest.mark.asyncio
@pytest.mark.parametrize("outcome", ["failed", "cancelled", "completed"])
async def test_closing_an_unevicted_run_does_not_report_a_terminal_status_for_the_active_workflow(
    temporal_env: WorkflowEnvironment,
    monkeypatch: pytest.MonkeyPatch,
    outcome: Literal["failed", "cancelled", "completed"],
) -> None:
    """Python closes the coroutines of a run that was never evicted on whatever thread collects them,
    often while another workflow is running.

    The closed run's terminal status must not be emitted as the active workflow's.
    """
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_event_publisher(captured_events)

    # Automatic collection would close the terminated run at a random point; the test closes it.
    gc.disable()
    try:
        async with EventContext(mock_client):
            async with create_test_worker_with_events(temporal_env, workflows=[ParkedWorkflowWithFailingCleanup]):
                parked = await temporal_env.client.start_workflow(
                    "parked_workflow_with_failing_cleanup",
                    {"outcome": outcome},
                    id="unevicted-run",
                    task_queue="test-task-queue",
                )
                try:
                    await _wait_until_parked(parked)
                finally:
                    await parked.terminate()

            unevicted_runs = _close_unevicted_runs_in_next_activation(monkeypatch, "unevicted-run")

            async with create_test_worker_with_events(temporal_env, workflows=[PureWorkflow]):
                active = await temporal_env.client.start_workflow(
                    "pure_workflow",
                    {"name": "active"},
                    id="active-run",
                    task_queue="test-task-queue",
                )
                await active.result()
    finally:
        gc.enable()

    assert not unevicted_runs
    terminal_types = (WorkflowExecutionFailed, WorkflowExecutionCanceled)
    assert [event for event in captured_events if isinstance(event, terminal_types)] == []
    assert len([event for event in captured_events if isinstance(event, WorkflowExecutionCompleted)]) == 1


@pytest.mark.asyncio
async def test_closing_an_unevicted_wait_for_input_leaves_the_active_workflow_alone(
    temporal_env: WorkflowEnvironment,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A run closed while waiting for input must not fail its input task, or clear its waiting state,
    on the workflow that is running at that moment."""
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_event_publisher(captured_events)

    # Automatic collection would close the terminated run at a random point; the test closes it.
    gc.disable()
    try:
        async with EventContext(mock_client):
            async with create_test_worker_with_events(temporal_env, workflows=[SimpleApprovalWorkflow]):
                parked = await temporal_env.client.start_workflow(
                    "simple_approval_workflow",
                    {"request_id": "req-unevicted"},
                    id="unevicted-waiting-run",
                    task_queue="test-task-queue",
                )
                try:
                    await wait_for_pending_inputs(parked, expected_count=1)
                    await _wait_until_parked(parked)
                finally:
                    await parked.terminate()

            unevicted_runs = _close_unevicted_runs_in_next_activation(monkeypatch, "unevicted-waiting-run")

            async with create_test_worker_with_events(temporal_env, workflows=[PureWorkflow]):
                active = await temporal_env.client.start_workflow(
                    "pure_workflow",
                    {"name": "active"},
                    id="active-run",
                    task_queue="test-task-queue",
                )
                await active.result()
                active_history = (await active.fetch_history()).events
    finally:
        gc.enable()

    assert not unevicted_runs
    assert [event for event in captured_events if isinstance(event, CustomTaskFailed)] == []
    # patched() upserts TemporalChangeVersion; only the waiting state of the closed run must not leak here.
    upserted_keys = {
        key
        for event in active_history
        if event.HasField("upsert_workflow_search_attributes_event_attributes")
        for key in event.upsert_workflow_search_attributes_event_attributes.search_attributes.indexed_fields
    }
    assert upserted_keys <= {"TemporalChangeVersion"}


async def _wait_for_pending_activity(handle: WorkflowHandle[Any, Any], timeout_seconds: float = 10.0) -> None:
    deadline = asyncio.get_running_loop().time() + timeout_seconds
    while not any(
        a.state == PendingActivityState.PENDING_ACTIVITY_STATE_STARTED
        for a in (await handle.describe()).raw_description.pending_activities
    ):
        if asyncio.get_running_loop().time() > deadline:
            raise AssertionError(f"workflow {handle.id} never started its activity")
        await asyncio.sleep(0.05)


async def _wait_for_terminal_events(
    captured_events: list[Any], expected_count: int, timeout_seconds: float = 10.0
) -> list[Any]:
    deadline = asyncio.get_running_loop().time() + timeout_seconds
    while True:
        terminal = [e for e in captured_events if isinstance(e, (WorkflowExecutionCanceled, WorkflowExecutionFailed))]
        if len(terminal) >= expected_count or asyncio.get_running_loop().time() > deadline:
            return terminal
        await asyncio.sleep(0.05)


class TestCancellationDuringAwaitedWork:
    """A cancel that reaches the workflow as a cancelled activity or child must be reported as CANCELED."""

    @pytest.mark.asyncio
    async def test_cancel_while_awaiting_activity_emits_canceled(self, temporal_env: WorkflowEnvironment) -> None:
        captured_events: list[Any] = []
        mock_client = create_capturing_mock_event_publisher(captured_events)

        async with EventContext(mock_client):
            async with create_test_worker_with_events(
                temporal_env, workflows=[CancelledInActivityWorkflow], activities=[block_until_cancelled]
            ):
                handle = await temporal_env.client.start_workflow(
                    "cancelled_in_activity_workflow",
                    {"name": "x"},
                    id="test-cancel-while-awaiting-activity",
                    task_queue="test-task-queue",
                )
                await _wait_for_pending_activity(handle)

                await handle.cancel()
                with pytest.raises(WorkflowFailureError):
                    await handle.result()

                terminal = await _wait_for_terminal_events(captured_events, expected_count=1)
                assert [type(e) for e in terminal] == [WorkflowExecutionCanceled]

    @pytest.mark.asyncio
    async def test_cancel_while_awaiting_child_emits_canceled_for_parent_and_child(
        self, temporal_env: WorkflowEnvironment
    ) -> None:
        captured_events: list[Any] = []
        mock_client = create_capturing_mock_event_publisher(captured_events)

        async with EventContext(mock_client):
            async with create_test_worker_with_events(
                temporal_env,
                workflows=[CancelledInChildParentWorkflow, CancelledInActivityWorkflow],
                activities=[block_until_cancelled],
            ):
                handle = await temporal_env.client.start_workflow(
                    "cancelled_in_child_parent_workflow",
                    {"name": "x"},
                    id="test-cancel-while-awaiting-child",
                    task_queue="test-task-queue",
                )
                deadline = asyncio.get_running_loop().time() + 10.0
                while not (children := (await handle.describe()).raw_description.pending_children):
                    assert asyncio.get_running_loop().time() < deadline, "child workflow never started"
                    await asyncio.sleep(0.05)
                await _wait_for_pending_activity(temporal_env.client.get_workflow_handle(children[0].workflow_id))

                await handle.cancel()
                with pytest.raises(WorkflowFailureError):
                    await handle.result()

                terminal = await _wait_for_terminal_events(captured_events, expected_count=2)
                assert sorted((e.workflow_name, type(e).__name__) for e in terminal) == [
                    ("cancelled_in_activity_workflow", "WorkflowExecutionCanceled"),
                    ("cancelled_in_child_parent_workflow", "WorkflowExecutionCanceled"),
                ]

    @pytest.mark.asyncio
    async def test_cancelling_its_own_activity_without_a_run_cancel_emits_failed(
        self, temporal_env: WorkflowEnvironment
    ) -> None:
        captured_events: list[Any] = []
        mock_client = create_capturing_mock_event_publisher(captured_events)

        async with EventContext(mock_client):
            async with create_test_worker_with_events(
                temporal_env, workflows=[CancelsOwnActivityWorkflow], activities=[block_until_cancelled]
            ):
                handle = await temporal_env.client.start_workflow(
                    "cancels_own_activity_workflow",
                    {"name": "x"},
                    id="test-cancels-own-activity",
                    task_queue="test-task-queue",
                )
                await _wait_for_pending_activity(handle)

                await handle.signal("cancel_activity")
                with pytest.raises(WorkflowFailureError):
                    await handle.result()

                terminal = await _wait_for_terminal_events(captured_events, expected_count=1)
                assert [type(e) for e in terminal] == [WorkflowExecutionFailed]

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("workflow_name", "awaits_activity"),
        [("cancelled_while_waiting_workflow", False), ("cancelled_in_activity_workflow", True)],
    )
    async def test_canceled_event_carries_the_cancel_reason(
        self, temporal_env: WorkflowEnvironment, workflow_name: str, awaits_activity: bool
    ) -> None:
        captured_events: list[Any] = []
        mock_client = create_capturing_mock_event_publisher(captured_events)

        async with EventContext(mock_client):
            async with create_test_worker_with_events(
                temporal_env,
                workflows=[CancelledWhileWaitingWorkflow, CancelledInActivityWorkflow],
                activities=[block_until_cancelled],
            ):
                handle = await temporal_env.client.start_workflow(
                    workflow_name,
                    {"name": "x"},
                    id=f"test-cancel-reason-{workflow_name}",
                    task_queue="test-task-queue",
                )
                if awaits_activity:
                    await _wait_for_pending_activity(handle)
                else:
                    while not any(isinstance(e, WorkflowExecutionStarted) for e in captured_events):
                        await asyncio.sleep(0.05)
                    await _wait_until_parked(handle)

                await handle.cancel(reason="budget exceeded")
                with pytest.raises(WorkflowFailureError):
                    await handle.result()

                terminal = await _wait_for_terminal_events(captured_events, expected_count=1)
                assert [(type(e), e.attributes.reason) for e in terminal] == [
                    (WorkflowExecutionCanceled, "budget exceeded")
                ]
