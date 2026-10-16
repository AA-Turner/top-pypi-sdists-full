"""Tests for heartbeat_timeout support in long-running activities.

These tests verify that the heartbeat_timeout parameter in @activity:
1. Enables fast detection of stuck activities (seconds, not minutes)
2. Records progress via heartbeat() calls
"""

from typing import Any

import pytest
from temporalio.client import WorkflowFailureError
from temporalio.exceptions import ActivityError, TimeoutType
from temporalio.exceptions import TimeoutError as TemporalTimeoutError

from mistralai.workflows.testing import (
    HeartbeatProcessingParams,
)

from .fixtures_long_running_activities import (
    HeartbeatWorkflow,
    fixture_activity_tracker,
    process_with_heartbeat,
)
from .utils import create_test_worker


def _unwrap_activity_errors(exc: BaseException | None) -> BaseException | None:
    while isinstance(exc, ActivityError) and exc.cause is not None:
        exc = exc.cause
    return exc


class TestHeartbeatTimeout:
    @pytest.mark.asyncio
    async def test_detects_stuck_activity_via_heartbeat_timeout(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[HeartbeatWorkflow],
            activities=[process_with_heartbeat],
        ):
            handle = await temporal_env.client.start_workflow(
                "heartbeat_workflow",
                HeartbeatProcessingParams(
                    total_items=1000,
                    items_per_second=100,
                    get_stuck_at_item=100,
                ).model_dump(),
                id="test-stuck-detection",
                task_queue="test-task-queue",
            )

            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()

        # The stuck activity must be caught by the heartbeat timeout, not by the
        # start_to_close timeout: that distinction is what heartbeat_timeout buys.
        # Wall-clock assertions here were flaky on loaded CI agents.
        cause = _unwrap_activity_errors(exc_info.value.cause)
        assert isinstance(cause, TemporalTimeoutError), (
            f"Expected a Temporal timeout failure, got {type(cause).__name__}: {cause}"
        )
        assert cause.type == TimeoutType.HEARTBEAT, (
            f"Expected a HEARTBEAT timeout, got {cause.type}: heartbeat_timeout must detect "
            "the stuck activity before start_to_close_timeout expires"
        )

        # Activity should have processed items before getting stuck
        assert fixture_activity_tracker.heartbeat_count >= 50, (
            f"Expected ~100 heartbeats before stuck, got {fixture_activity_tracker.heartbeat_count}"
        )

    @pytest.mark.asyncio
    async def test_records_progress_via_heartbeats(self, temporal_env: Any) -> None:
        total_items = 50

        async with create_test_worker(
            temporal_env,
            workflows=[HeartbeatWorkflow],
            activities=[process_with_heartbeat],
        ):
            handle = await temporal_env.client.start_workflow(
                "heartbeat_workflow",
                HeartbeatProcessingParams(
                    total_items=total_items,
                    items_per_second=100,
                ).model_dump(),
                id="test-heartbeat-progress",
                task_queue="test-task-queue",
            )

            result = await handle.result()

        # Workflow completed successfully
        assert result["completed"] is True

        # Heartbeat count should match items processed (one heartbeat per item)
        assert result["heartbeat_count"] == total_items, (
            f"Expected {total_items} heartbeats, got {result['heartbeat_count']}"
        )
        assert result["items_processed"] == total_items


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
