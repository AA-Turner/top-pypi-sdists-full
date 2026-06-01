"""
Improved workflow demonstrating rate limiting functionality in Mistral Workflows.
This version includes:
1. Multiple rate-limited activities with different limits (1-5 executions per time window)
2. Workflow that runs based on n_turns parameter
3. Dynamic selection of activity based on rate limit parameter
"""

import asyncio
import json

import temporalio.workflow as temporal_workflow
from pydantic import BaseModel, Field

from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.rate_limiting.rate_limit import RateLimit
from mistralai.workflows.core.workflow import workflow

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.get_logger(__name__)


class ActivityParams(BaseModel):
    turn_data: str = Field(..., description="The data for this turn")


# Define multiple rate-limited activities with different limits (1-5)
@activity(rate_limit=RateLimit(time_window_in_sec=1, max_execution=1))
async def process_turn_rate1(params: ActivityParams) -> None:
    """Process turn with rate limit of 1 execution per 2 seconds."""
    pass


@activity(rate_limit=RateLimit(time_window_in_sec=1, max_execution=2))
async def process_turn_rate2(params: ActivityParams) -> None:
    """Process turn with rate limit of 2 executions per 2 seconds."""
    pass


@activity(rate_limit=RateLimit(time_window_in_sec=1, max_execution=3))
async def process_turn_rate3(params: ActivityParams) -> None:
    """Process turn with rate limit of 3 executions per 2 seconds."""
    pass


@activity(rate_limit=RateLimit(time_window_in_sec=1, max_execution=4))
async def process_turn_rate4(params: ActivityParams) -> None:
    """Process turn with rate limit of 4 executions per 2 seconds."""
    pass


@activity(rate_limit=RateLimit(time_window_in_sec=1, max_execution=5))
async def process_turn_rate5(params: ActivityParams) -> None:
    """Process turn with rate limit of 5 executions per 2 seconds."""
    pass


class Params(BaseModel):
    n_turns: int = Field(..., description="Number of turns to process")
    rate_limit: int = Field(1, description="Rate limit to use (1-5 executions per 2 seconds)")


class Result(BaseModel):
    total_turns_processed: int = Field(..., description="Total turns processed")
    processing_time: float = Field(..., description="Total processing time in seconds")
    rate_limit: int = Field(..., description="Rate limit used")


@workflow.define(name="rate-limited-workflow")
class RateLimitedWorkflow:
    """
    A workflow that demonstrates rate limiting functionality with multiple rate limits.
    This workflow:
    1. Processes multiple turns with configurable rate limiting
    2. Dynamically selects the appropriate rate-limited activity
    3. Measures and reports processing metrics
    """

    @workflow.entrypoint
    async def execute(self, params: Params) -> Result:
        """
        Execute the workflow with rate-limited activities.

        Args:
            params.n_turns: Number of turns to process
            params.rate_limit: Rate limit to use (1-5)

        Returns:
            Processing results including metrics
        """
        logger.info("[step 0] Starting workflow", n_turns=params.n_turns, rate_limit=params.rate_limit)

        # Select the appropriate activity based on rate limit parameter
        activity_map = {
            1: process_turn_rate1,
            2: process_turn_rate2,
            3: process_turn_rate3,
            4: process_turn_rate4,
            5: process_turn_rate5,
        }
        selected_activity = activity_map[params.rate_limit]

        logger.info("[step 1] Starting rate-limited workflow execution...")
        start_time = temporal_workflow.time()

        # Process all turns using the selected rate-limited activity
        tasks = []
        for turn in range(params.n_turns):
            turn_data = f"turn-{turn}-rate-{params.rate_limit}"
            tasks.append(selected_activity(ActivityParams(turn_data=turn_data)))

        await asyncio.gather(*tasks)

        duration = temporal_workflow.time() - start_time
        turns_per_second = params.n_turns / duration if duration > 0 else 0

        logger.info(
            "[step 2] Completed processing",
            duration=duration,
            turns_per_second=turns_per_second,
            expected_rate=params.rate_limit / 2,  # Since time window is 2 seconds
        )

        return Result(total_turns_processed=params.n_turns, processing_time=duration, rate_limit=params.rate_limit)


async def main() -> None:
    """Run the rate-limited workflow example."""
    import os
    import time
    from uuid import uuid4

    os.environ["DANGEROUSLY_FORCE_FAIL_WORKFLOW_ON_ERROR"] = "true"
    os.environ["RETRY_POLICY_MAX_ATTEMPTS"] = "1"

    from mistralai.workflows.core.config.config import config
    from mistralai.workflows.core.temporal.temporal_client import create_temporal_client

    start_time = time.time()
    client = await create_temporal_client()

    # Start the worker
    from mistralai.workflows.core.worker import run_worker

    worker_task = await run_worker([RateLimitedWorkflow], detach=True)
    assert worker_task is not None

    try:
        # Execute the workflow with different rate limits
        n_turns = 100
        logger.info(f"Starting workflows with {n_turns} turns each")
        results = []
        for _ in range(3):
            results_ = await asyncio.gather(
                *[
                    client.execute_workflow(
                        RateLimitedWorkflow.execute,
                        Params(n_turns=n_turns, rate_limit=rate_limit),
                        id=f"rate-limited-workflow-{uuid4()}",
                        task_queue=config.temporal.namespace,
                    )
                    for rate_limit in [1, 2, 3, 4, 5]
                ]
            )
            results.extend(results_)
        json_result = [r.model_dump() for r in results]
        print(json.dumps(json_result))  # noqa: T201
    finally:
        # Clean up
        worker_task.cancel()
        try:
            await worker_task
        except asyncio.CancelledError:
            pass

    duration = round(time.time() - start_time)
    logger.info(f"All workflows completed in {duration} seconds")


if __name__ == "__main__":
    asyncio.run(main())
