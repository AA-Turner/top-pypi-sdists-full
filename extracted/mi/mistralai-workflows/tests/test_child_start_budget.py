import asyncio

import pytest
from pydantic import BaseModel

from mistralai.workflows import workflow
from mistralai.workflows.core.execution.child_start_budget import (
    DEFAULT_CHILD_START_BUDGET_BYTES,
    ChildStartBudget,
    charge_for,
)

from .utils import create_test_worker, execute_workflow_in_test_env


class TestChargeFor:
    def test_payload_below_task_budget_charged_full_size(self):
        assert charge_for(100) == 100
        assert charge_for(DEFAULT_CHILD_START_BUDGET_BYTES - 1) == DEFAULT_CHILD_START_BUDGET_BYTES - 1

    def test_payload_at_or_above_task_budget_charged_at_budget(self):
        assert charge_for(DEFAULT_CHILD_START_BUDGET_BYTES) == DEFAULT_CHILD_START_BUDGET_BYTES
        assert charge_for(5 * 1024 * 1024) == DEFAULT_CHILD_START_BUDGET_BYTES


class TestChildStartBudget:
    @pytest.mark.asyncio
    async def test_acquire_under_limit_proceeds(self):
        budget = ChildStartBudget(limit_bytes=100)
        await budget.acquire(40)
        await budget.acquire(50)  # 90 in flight, still under 100

    @pytest.mark.asyncio
    async def test_acquire_charge_above_limit_raises(self):
        # A charge above the limit is a misconfigured budget (limit below the max inline
        # charge), not an oversized input. Raise rather than deadlock the fan-out — and
        # rather than assert, so the guard survives `python -O`.
        budget = ChildStartBudget(limit_bytes=100)
        with pytest.raises(RuntimeError):
            await budget.acquire(101)

    @pytest.mark.asyncio
    async def test_release_reduces_in_flight(self):
        budget = ChildStartBudget(limit_bytes=100)
        await budget.acquire(60)
        budget.release(60)
        # Budget fully available again
        await budget.acquire(100)


# The blocking path uses workflow.wait_condition, which requires a workflow runtime, so
# the remaining tests run inside a real Temporal test environment rather than as plain
# asyncio. Under-limit and oversized paths never reach wait_condition and stay above.


class _BlockParams(BaseModel):
    pass


class _BlockResult(BaseModel):
    acquired_before_release: bool


@workflow.define(name="wfl1022-budget-block-test")
class _BudgetBlockWorkflow:
    @workflow.entrypoint
    async def run(self, params: _BlockParams) -> _BlockResult:
        budget = ChildStartBudget(limit_bytes=100)
        await budget.acquire(100)  # fill the budget

        acquired: list[int] = []

        async def waiter() -> None:
            await budget.acquire(50)  # 150 > 100 → blocks until release
            acquired.append(1)
            budget.release(50)

        waiter_task = asyncio.create_task(waiter())
        # Yield so the waiter runs and blocks before we release.
        await workflow.wait_condition(lambda: True)
        blocked_not_acquired = not acquired
        budget.release(100)  # free the budget → waiter unblocks
        await workflow.wait_condition(lambda: bool(acquired))
        await waiter_task  # surface any exception raised inside the waiter
        return _BlockResult(acquired_before_release=blocked_not_acquired)


@pytest.mark.asyncio
async def test_acquire_blocks_until_release(temporal_env):
    async with create_test_worker(temporal_env, workflows=[_BudgetBlockWorkflow]):
        result = await execute_workflow_in_test_env(temporal_env, _BudgetBlockWorkflow, _BlockParams())
    # The waiter must have been blocked (not acquired) before the release, then unblocked.
    assert result["acquired_before_release"] is True


class _FanoutParams(BaseModel):
    op_count: int = 3
    op_size: int = 60


class _FanoutResult(BaseModel):
    completed: int


@workflow.define(name="wfl1022-budget-fanout-test")
class _BudgetFanoutWorkflow:
    @workflow.entrypoint
    async def run(self, params: _FanoutParams) -> _FanoutResult:
        # limit=100, but total demand (op_count * op_size) exceeds it → ops must serialize.
        budget = ChildStartBudget(limit_bytes=100)

        async def op() -> None:
            await budget.acquire(params.op_size)
            try:
                # Hold the slot for one turn so a blocked sibling queues behind us before we release.
                await workflow.wait_condition(lambda: True)
            finally:
                budget.release(params.op_size)

        await asyncio.gather(*(op() for _ in range(params.op_count)))
        return _FanoutResult(completed=params.op_count)


@pytest.mark.asyncio
async def test_fanout_exceeding_limit_does_not_deadlock(temporal_env):
    async with create_test_worker(temporal_env, workflows=[_BudgetFanoutWorkflow]):
        result = await execute_workflow_in_test_env(
            temporal_env, _BudgetFanoutWorkflow, _FanoutParams(op_count=3, op_size=60)
        )
    assert result["completed"] == 3
