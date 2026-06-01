# originally implemented in https://github.com/mistralai/dashboard/pull/21280
import asyncio
from unittest.mock import AsyncMock

import pytest
from httpx import Response

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.protocol.v1.events import (
    CustomTaskStarted,
    CustomTaskStartedAttributes,
)
from mistralai.workflows.worker_client.errors import SDKError
from mistralai.workflows.worker_client.events import Events


@pytest.fixture
def event() -> CustomTaskStarted:
    return CustomTaskStarted(
        event_id="evt-1",
        root_workflow_exec_id="root-1",
        workflow_exec_id="exec-1",
        workflow_run_id="run-1",
        workflow_name="test-workflow",
        attributes=CustomTaskStartedAttributes(custom_task_id="task-1", custom_task_type="test-task"),
    )


@pytest.fixture
def events(event: CustomTaskStarted) -> list[CustomTaskStarted]:
    return [event, event]


@pytest.fixture
def mock_client() -> AsyncMock:
    return AsyncMock(spec=Events)


@pytest.fixture
def event_context(mock_client: AsyncMock) -> EventContext:
    return EventContext(mock_client)


class TestSendEventsBatchFallback:
    @pytest.mark.asyncio
    async def test_fallback_on_404(self, events: list[CustomTaskStarted], mock_client: AsyncMock):
        """When the batch endpoint returns 404, fall back to individual sends."""
        mock_client.send_event_async = AsyncMock(return_value=None)
        mock_client.send_events_batch_async = AsyncMock(side_effect=SDKError("Not Found", Response(status_code=404)))

        async with EventContext(mock_client) as event_context:
            assert event_context._batch_events_supported
            await event_context.publish_events_batch(events)
            assert mock_client.send_event_async.call_count == 2
            assert mock_client.send_events_batch_async.call_count == 1
            assert not event_context._batch_events_supported

    @pytest.mark.asyncio
    async def test_subsequent_calls_skip_batch_endpoint(self, events: list[CustomTaskStarted], mock_client: AsyncMock):
        """After a 404, subsequent calls should use the fallback directly without hitting _request."""
        mock_client.send_event_async = AsyncMock(return_value=None)
        mock_client.send_events_batch_async = AsyncMock(side_effect=SDKError("Not Found", Response(status_code=404)))

        async with EventContext(mock_client) as event_context:
            # First call: trigger fallback via 404
            assert event_context._batch_events_supported
            await event_context.publish_events_batch(events)
            assert mock_client.send_event_async.call_count == 2
            assert mock_client.send_events_batch_async.call_count == 1
            assert not event_context._batch_events_supported

            # Second call: _request should not be called
            await event_context.publish_events_batch(events)
            assert mock_client.send_event_async.call_count == 4
            assert mock_client.send_events_batch_async.call_count == 1

    @pytest.mark.asyncio
    async def test_non_404_error_is_raised(self, events: list[CustomTaskStarted], mock_client: AsyncMock):
        """Non-404 errors should be raised normally, not trigger fallback."""
        mock_client.send_event_async = AsyncMock(return_value=None)
        mock_client.send_events_batch_async = AsyncMock(return_value=None)

        async with EventContext(mock_client) as event_context:
            assert event_context._batch_events_supported
            await event_context.publish_events_batch(events)
            assert mock_client.send_event_async.call_count == 0
            assert mock_client.send_events_batch_async.call_count == 1
            assert event_context._batch_events_supported

    @pytest.mark.asyncio
    async def test_batch_success_does_not_disable_fallback(
        self, events: list[CustomTaskStarted], mock_client: AsyncMock
    ):
        """Successful batch send keeps batch support enabled."""
        mock_client.send_event_async = AsyncMock(return_value=None)
        mock_client.send_events_batch_async = AsyncMock(return_value=None)

        async with EventContext(mock_client) as event_context:
            await event_context.publish_events_batch(events)
            assert event_context._batch_events_supported

    @pytest.mark.asyncio
    async def test_fallback_preserves_event_order(self, mock_client: AsyncMock):
        """Fallback sends events sequentially, preserving order.

        track_send yields to the event loop with a reverse-proportional delay
        so that under concurrent execution (asyncio.gather) later events would
        finish first, scrambling the order. Sequential awaits are unaffected.
        """
        sent_ids: list[str] = []
        num_events = 5

        async def track_send(*, event, **kwargs) -> None:
            idx = int(event["event_id"].split("-")[1])
            for _ in range(num_events - idx):
                await asyncio.sleep(0)
            sent_ids.append(event["event_id"])

        mock_client.send_event_async = track_send
        mock_client.send_events_batch_async = AsyncMock(side_effect=SDKError("Not Found", Response(status_code=404)))

        events = [
            CustomTaskStarted(
                event_id=f"evt-{i}",
                root_workflow_exec_id="root-1",
                workflow_exec_id="exec-1",
                workflow_run_id="run-1",
                workflow_name="test-workflow",
                attributes=CustomTaskStartedAttributes(custom_task_id=f"task-{i}", custom_task_type="test-task"),
            )
            for i in range(num_events)
        ]

        async with EventContext(mock_client) as event_context:
            await event_context.publish_events_batch(events)

        assert sent_ids == [f"evt-{i}" for i in range(num_events)]
