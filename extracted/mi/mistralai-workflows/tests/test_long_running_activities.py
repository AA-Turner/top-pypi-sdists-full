"""Tests for heartbeat_timeout support in long-running activities.

These tests verify that the heartbeat_timeout parameter in @activity:
1. Enables fast detection of stuck activities (seconds, not minutes)
2. Records progress via heartbeat() calls
"""

import asyncio
from typing import Any

import pytest

from mistralai.workflows.testing import (
    HeartbeatProcessingParams,
)

from .fixtures_long_running_activities import (
    HeartbeatWorkflow,
    fixture_activity_tracker,
    process_with_heartbeat,
)
from .utils import create_test_worker


class TestHeartbeatTimeout:
    @pytest.mark.asyncio
    async def test_detects_stuck_activity_quickly(self, temporal_env: Any) -> None:
        start_time = asyncio.get_event_loop().time()

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

            with pytest.raises(Exception) as exc_info:
                await handle.result()

            detection_time = asyncio.get_event_loop().time() - start_time

        # Heartbeat timeout should detect stuck activity faster than start_to_close_timeout
        assert detection_time < 8, (
            f"Detection took {detection_time:.1f}s, expected < 8s. "
            "Heartbeat timeout should trigger faster than full start_to_close_timeout cycle."
        )

        # Workflow should have failed (Temporal wraps the error message)
        assert exc_info.value is not None, "Activity should have failed due to heartbeat timeout"

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
