import asyncio
from datetime import timedelta

from mistralai.workflows import activity, workflow
from mistralai.workflows.core.activity import activity_heartbeat
from mistralai.workflows.testing import (
    HeartbeatProcessingParams,
    HeartbeatProcessingResult,
)


class ActivityTracker:
    def __init__(self) -> None:
        self.items_processed = 0
        self.heartbeat_count = 0
        self.cancelled = False


fixture_activity_tracker = ActivityTracker()


@activity(start_to_close_timeout=timedelta(seconds=3), heartbeat_timeout=timedelta(seconds=0.5), _skip_registering=True)
async def process_with_heartbeat(params: HeartbeatProcessingParams) -> HeartbeatProcessingResult:
    fixture_activity_tracker.items_processed = 0
    fixture_activity_tracker.heartbeat_count = 0
    fixture_activity_tracker.cancelled = False

    try:
        for item_num in range(1, params.total_items + 1):
            await asyncio.sleep(1.0 / params.items_per_second)

            fixture_activity_tracker.items_processed = item_num

            activity_heartbeat(
                {
                    "items_processed": item_num,
                    "total_items": params.total_items,
                    "progress_percentage": round(item_num / params.total_items * 100, 1),
                }
            )
            fixture_activity_tracker.heartbeat_count += 1

            if params.get_stuck_at_item and item_num >= params.get_stuck_at_item:
                await asyncio.sleep(999999)

            if params.crash_at_item and item_num >= params.crash_at_item:
                raise RuntimeError(f"Simulated crash at item {item_num}")

        return HeartbeatProcessingResult(
            items_processed=params.total_items,
            heartbeat_count=fixture_activity_tracker.heartbeat_count,
            completed=True,
        )

    except asyncio.CancelledError:
        fixture_activity_tracker.cancelled = True
        raise


@workflow.define(name="heartbeat_workflow")
class HeartbeatWorkflow:
    @workflow.entrypoint
    async def run(self, params: HeartbeatProcessingParams) -> HeartbeatProcessingResult:
        return await process_with_heartbeat(params)
