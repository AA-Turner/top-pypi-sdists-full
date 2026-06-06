import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest
from pydantic import TypeAdapter

from mistralai.workflows.core._events.event_context import (
    BackgroundEventPublisher,
    EventContext,
)
from mistralai.workflows.core.task.task import Task
from mistralai.workflows.protocol.v1.events import (
    CustomTaskCompleted,
    CustomTaskInProgress,
    CustomTaskStarted,
    CustomTaskStartedAttributes,
    WorkflowEvent,
)

_event_adapter = TypeAdapter(WorkflowEvent)


def _make_event(idx: int = 0) -> CustomTaskStarted:
    """Create a real event object for testing."""
    return CustomTaskStarted(
        event_id=f"evt-{idx}",
        root_workflow_exec_id="root-1",
        workflow_exec_id="exec-1",
        workflow_run_id="run-1",
        workflow_name="test-workflow",
        attributes=CustomTaskStartedAttributes(
            custom_task_id=f"task-{idx}",
            custom_task_type="test-task",
        ),
    )


def mock_activity_info() -> Mock:
    info = Mock()
    info.workflow_id = "test-workflow-id"
    info.workflow_run_id = "test-run-id"
    info.workflow_type = "test-workflow-type"
    info.activity_id = "test-activity-id"
    info.task_token = b"test-task-token"
    return info


@pytest.fixture
def mock_workflows_client() -> AsyncMock:
    client = AsyncMock()
    client.send_event_async = AsyncMock(return_value=None)
    client.send_events_batch_async = AsyncMock(return_value=None)
    return client


@pytest.fixture
async def event_context(mock_workflows_client: AsyncMock) -> EventContext:
    return EventContext(mock_workflows_client)


@pytest.fixture
async def background_publisher(event_context: EventContext) -> BackgroundEventPublisher:
    return BackgroundEventPublisher(event_context)


class TestEventContextSequentialPublishing:
    @pytest.mark.asyncio
    async def test_sequential_publishing_preserves_order(
        self, event_context: EventContext, mock_workflows_client: AsyncMock
    ) -> None:
        events = [_make_event(i) for i in range(3)]

        async with event_context:
            for event in events:
                await event_context.publish_event(event)

        assert mock_workflows_client.send_event_async.call_count == 3
        calls = mock_workflows_client.send_event_async.call_args_list
        for i, c in enumerate(calls):
            assert c.kwargs["event"]["event_id"] == f"evt-{i}"


class TestBackgroundEventPublisherConcurrency:
    @pytest.mark.asyncio
    async def test_batching_sends_all_queued_events_at_once(
        self,
        event_context: EventContext,
        background_publisher: BackgroundEventPublisher,
        mock_workflows_client: AsyncMock,
    ) -> None:
        """Verify that when multiple events are queued, they're sent in a single batch call."""
        batch_calls = []

        async def track_batch_send(*, events: list, **kwargs) -> None:
            batch_calls.append(len(events))

        mock_workflows_client.send_event_async = AsyncMock()
        mock_workflows_client.send_events_batch_async = AsyncMock(side_effect=track_batch_send)

        async with event_context:
            events = [_make_event(i) for i in range(10)]
            for event in events:
                background_publisher.publish_event_background(event)

            await background_publisher.drain()
            await background_publisher.shutdown()

        # Should have made a single batch call with all 10 events
        assert len(batch_calls) == 1
        assert batch_calls[0] == 10
        # Single event endpoint should never be called
        assert mock_workflows_client.send_event_async.call_count == 0

    @pytest.mark.asyncio
    async def test_concurrent_background_tasks_ordered_by_queue(
        self,
        event_context: EventContext,
        background_publisher: BackgroundEventPublisher,
        mock_workflows_client: AsyncMock,
    ) -> None:
        events_sent: list[str] = []
        send_lock = asyncio.Lock()

        async def track_send(*, event, **kwargs) -> None:
            await asyncio.sleep(0.01)
            async with send_lock:
                events_sent.append(event["event_id"])

        async def track_send_batch(*, events, **kwargs) -> None:
            await asyncio.sleep(0.01)
            async with send_lock:
                for e in events:
                    events_sent.append(e["event_id"])

        mock_workflows_client.send_event_async = track_send
        mock_workflows_client.send_events_batch_async = track_send_batch

        async with event_context:
            events = [_make_event(i) for i in range(5)]

            for event in events:
                background_publisher.publish_event_background(event)

            await background_publisher.drain()
            await background_publisher.shutdown()

        assert len(events_sent) == 5
        assert events_sent == [f"evt-{i}" for i in range(5)]

    @pytest.mark.asyncio
    async def test_drain_waits_for_all_pending_events(
        self,
        event_context: EventContext,
        background_publisher: BackgroundEventPublisher,
        mock_workflows_client: AsyncMock,
    ) -> None:
        slow_send_started = False
        slow_send_finished = False

        async def slow_send(*, event, **kwargs) -> None:
            nonlocal slow_send_started, slow_send_finished
            slow_send_started = True
            await asyncio.sleep(0.2)
            slow_send_finished = True

        mock_workflows_client.send_event_async = slow_send

        async with event_context:
            event = _make_event()
            background_publisher.publish_event_background(event)

            await background_publisher.drain()
            await background_publisher.shutdown()

        assert slow_send_started
        assert slow_send_finished

    @pytest.mark.asyncio
    async def test_adaptive_drain_timeout_with_many_events(
        self,
        event_context: EventContext,
        background_publisher: BackgroundEventPublisher,
        mock_workflows_client: AsyncMock,
    ) -> None:
        """Reproduces WFL-365: with many events in flight, the old fixed 10s
        timeout would expire before all events are sent. The adaptive drain
        timeout scales with the number of pending events."""
        event_count = 1000
        events_sent = []

        async def slow_send(*, event, **kwargs) -> None:
            await asyncio.sleep(0.015)
            events_sent.append(event)

        async def slow_send_batch(*, events, **kwargs) -> None:
            await asyncio.sleep(0.015)
            events_sent.extend(events)

        mock_workflows_client.send_event_async = slow_send
        mock_workflows_client.send_events_batch_async = slow_send_batch

        async with event_context:
            for i in range(event_count):
                background_publisher.publish_event_background(_make_event(i))

            await background_publisher.drain()
            await background_publisher.shutdown()

        assert len(events_sent) == event_count

    @pytest.mark.asyncio
    async def test_multiple_drains_are_safe(
        self,
        event_context: EventContext,
        background_publisher: BackgroundEventPublisher,
        mock_workflows_client: AsyncMock,
    ) -> None:
        async with event_context:
            event = _make_event()
            background_publisher.publish_event_background(event)

            await background_publisher.drain()
            assert mock_workflows_client.send_event_async.call_count == 1

            await background_publisher.drain()
            assert mock_workflows_client.send_event_async.call_count == 1

            await background_publisher.shutdown()

    @pytest.mark.asyncio
    async def test_encoding_failure_does_not_stall_queue(
        self,
        event_context: EventContext,
        background_publisher: BackgroundEventPublisher,
        mock_workflows_client: AsyncMock,
    ) -> None:
        """Verify that encoding failures don't prevent drain() from completing.

        When maybe_encode_event raises an exception, the sender loop should:
        1. Call task_done() for the failed event (so drain doesn't hang)
        2. Continue processing remaining events
        3. Successfully send events that encode correctly
        """
        events_sent: list[str] = []
        fail_on_indices = {1, 3, 5}  # These events will fail to encode

        async def track_send_batch(*, events, **kwargs) -> None:
            for e in events:
                events_sent.append(e["event_id"])

        mock_workflows_client.send_events_batch_async = AsyncMock(side_effect=track_send_batch)

        call_count = 0

        async def flaky_encode(event, encoder):
            nonlocal call_count
            idx = call_count
            call_count += 1
            if idx in fail_on_indices:
                raise ValueError(f"Simulated encoding failure for event {idx}")
            return event

        async with event_context:
            with patch(
                "mistralai.workflows.core._events.event_context.maybe_encode_event",
                side_effect=flaky_encode,
            ):
                for i in range(7):
                    background_publisher.publish_event_background(_make_event(i))

                # drain() should complete without hanging despite encoding failures
                await asyncio.wait_for(background_publisher.drain(), timeout=5.0)
                await background_publisher.shutdown()

        # Events 0, 2, 4, 6 should have been sent (indices 1, 3, 5 failed)
        assert len(events_sent) == 4
        assert set(events_sent) == {"evt-0", "evt-2", "evt-4", "evt-6"}


class TestTaskEventOrdering:
    @pytest.mark.asyncio
    async def test_task_events_strict_order(
        self,
        event_context: EventContext,
        background_publisher: BackgroundEventPublisher,
        mock_workflows_client: AsyncMock,
    ) -> None:
        events_sent = []

        async def track_send(*, event, **kwargs) -> None:
            await asyncio.sleep(0.01)
            events_sent.append(_event_adapter.validate_python(event))

        async def track_send_batch(*, events, **kwargs) -> None:
            await asyncio.sleep(0.01)
            for e in events:
                events_sent.append(_event_adapter.validate_python(e))

        mock_workflows_client.send_event_async = track_send
        mock_workflows_client.send_events_batch_async = track_send_batch

        async with event_context:
            with patch(
                "mistralai.workflows.core.task.task.BackgroundEventPublisher.get_current",
                return_value=background_publisher,
            ):
                with patch("mistralai.workflows.core.task.task.temporalio.activity.in_activity", return_value=True):
                    with patch(
                        "mistralai.workflows.core._events.event_utils.temporalio.activity.info",
                        return_value=mock_activity_info(),
                    ):
                        with patch(
                            "mistralai.workflows.core.task.task.should_publish_event",
                            return_value=True,
                        ):
                            task: Task[dict[str, int]] = Task(type="test-task", state={"progress": 0})

                            async with task as t:
                                await t.set_state({"progress": 50})
                                await t.set_state({"progress": 100})

            await background_publisher.drain()
            await background_publisher.shutdown()

        assert len(events_sent) == 4
        assert isinstance(events_sent[0], CustomTaskStarted)
        assert isinstance(events_sent[1], CustomTaskInProgress)
        assert isinstance(events_sent[2], CustomTaskInProgress)
        assert isinstance(events_sent[3], CustomTaskCompleted)

    @pytest.mark.asyncio
    async def test_concurrent_tasks_maintain_individual_order(
        self,
        event_context: EventContext,
        background_publisher: BackgroundEventPublisher,
        mock_workflows_client: AsyncMock,
    ) -> None:
        events_sent = []
        send_lock = asyncio.Lock()

        async def track_send(*, event, **kwargs) -> None:
            await asyncio.sleep(0.01)
            async with send_lock:
                events_sent.append(_event_adapter.validate_python(event))

        async def track_send_batch(*, events, **kwargs) -> None:
            await asyncio.sleep(0.01)
            async with send_lock:
                for e in events:
                    events_sent.append(_event_adapter.validate_python(e))

        mock_workflows_client.send_event_async = track_send
        mock_workflows_client.send_events_batch_async = track_send_batch

        async def run_task(task_type: str) -> None:
            with patch(
                "mistralai.workflows.core.task.task.BackgroundEventPublisher.get_current",
                return_value=background_publisher,
            ):
                with patch("mistralai.workflows.core.task.task.temporalio.activity.in_activity", return_value=True):
                    with patch(
                        "mistralai.workflows.core._events.event_utils.temporalio.activity.info",
                        return_value=mock_activity_info(),
                    ):
                        with patch(
                            "mistralai.workflows.core.task.task.should_publish_event",
                            return_value=True,
                        ):
                            task: Task[dict[str, int]] = Task(type=task_type, state={"step": 0})
                            async with task as t:
                                await t.set_state({"step": 1})

        async with event_context:
            await asyncio.gather(run_task("task-A"), run_task("task-B"))
            await background_publisher.drain()
            await background_publisher.shutdown()

        assert len(events_sent) == 6

        task_a_events = [e for e in events_sent if getattr(e.attributes, "custom_task_type", None) == "task-A"]
        task_b_events = [e for e in events_sent if getattr(e.attributes, "custom_task_type", None) == "task-B"]

        assert len(task_a_events) == 3
        assert len(task_b_events) == 3

        assert isinstance(task_a_events[0], CustomTaskStarted)
        assert isinstance(task_a_events[1], CustomTaskInProgress)
        assert isinstance(task_a_events[2], CustomTaskCompleted)

        assert isinstance(task_b_events[0], CustomTaskStarted)
        assert isinstance(task_b_events[1], CustomTaskInProgress)
        assert isinstance(task_b_events[2], CustomTaskCompleted)


class TestRaceConditionPrevention:
    @pytest.mark.asyncio
    async def test_custom_task_events_before_activity_completion(
        self,
        event_context: EventContext,
        background_publisher: BackgroundEventPublisher,
        mock_workflows_client: AsyncMock,
    ) -> None:
        events_sent = []

        async def track_send(*, event, **kwargs) -> None:
            events_sent.append(_event_adapter.validate_python(event))

        async def track_send_batch(*, events, **kwargs) -> None:
            for e in events:
                events_sent.append(_event_adapter.validate_python(e))

        mock_workflows_client.send_event_async = track_send
        mock_workflows_client.send_events_batch_async = track_send_batch

        async with event_context:
            with patch(
                "mistralai.workflows.core.task.task.BackgroundEventPublisher.get_current",
                return_value=background_publisher,
            ):
                with patch("mistralai.workflows.core.task.task.temporalio.activity.in_activity", return_value=True):
                    with patch(
                        "mistralai.workflows.core._events.event_utils.temporalio.activity.info",
                        return_value=mock_activity_info(),
                    ):
                        with patch(
                            "mistralai.workflows.core.task.task.should_publish_event",
                            return_value=True,
                        ):
                            task: Task[None] = Task(type="test-task")
                            async with task:
                                pass

            await background_publisher.drain()
            await background_publisher.shutdown()

            activity_completed_event = _make_event(99)
            await event_context.publish_event(activity_completed_event)

        assert len(events_sent) == 3
        assert isinstance(events_sent[0], CustomTaskStarted)
        assert isinstance(events_sent[1], CustomTaskCompleted)
        assert events_sent[2].event_id == "evt-99"

    @pytest.mark.asyncio
    async def test_workflow_completion_after_all_activity_events(
        self,
        event_context: EventContext,
        background_publisher: BackgroundEventPublisher,
        mock_workflows_client: AsyncMock,
    ) -> None:
        events_sent = []

        async def track_send(*, event, **kwargs) -> None:
            events_sent.append(_event_adapter.validate_python(event))

        async def track_send_batch(*, events, **kwargs) -> None:
            for e in events:
                events_sent.append(_event_adapter.validate_python(e))

        mock_workflows_client.send_event_async = track_send
        mock_workflows_client.send_events_batch_async = track_send_batch

        async with event_context:
            with patch(
                "mistralai.workflows.core.task.task.BackgroundEventPublisher.get_current",
                return_value=background_publisher,
            ):
                with patch("mistralai.workflows.core.task.task.temporalio.activity.in_activity", return_value=True):
                    with patch(
                        "mistralai.workflows.core._events.event_utils.temporalio.activity.info",
                        return_value=mock_activity_info(),
                    ):
                        with patch(
                            "mistralai.workflows.core.task.task.should_publish_event",
                            return_value=True,
                        ):
                            task: Task[None] = Task(type="test-task")
                            async with task:
                                pass

            await background_publisher.drain()
            await background_publisher.shutdown()

            activity_completed = _make_event(98)
            await event_context.publish_event(activity_completed)

            workflow_completed = _make_event(99)
            await event_context.publish_event(workflow_completed)

        assert len(events_sent) == 4
        assert isinstance(events_sent[0], CustomTaskStarted)
        assert isinstance(events_sent[1], CustomTaskCompleted)
        assert events_sent[2].event_id == "evt-98"
        assert events_sent[3].event_id == "evt-99"


class TestTaskActivityOnlyValidation:
    def test_task_creation_in_activity_succeeds(self) -> None:
        with patch("mistralai.workflows.core.task.task.temporalio.activity.in_activity", return_value=True):
            task: Task[None] = Task(type="test-task")
            assert task.type == "test-task"

    def test_task_creation_in_workflow_succeeds(self) -> None:
        """Tasks can now be used in workflows via local activities."""
        with patch("mistralai.workflows.core.task.task.temporalio.workflow.in_workflow", return_value=True):
            with patch("mistralai.workflows.core.task.task.temporalio.workflow.uuid4", return_value="mock-uuid"):
                task: Task[None] = Task(type="test-task", id="explicit-id")
                assert task.type == "test-task"
                assert task.id == "explicit-id"
