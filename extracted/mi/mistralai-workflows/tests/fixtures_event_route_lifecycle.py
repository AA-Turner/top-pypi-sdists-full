"""Workflow and activity definitions for event-route lifecycle tests.

This file is kept separate from the test module because Temporal's sandbox
re-imports the module where workflow classes are defined. The test module
imports httpx at the top level, which is restricted in the sandbox.
"""

from __future__ import annotations

import asyncio

from pydantic import BaseModel

from mistralai.workflows import Depends, activity, workflow
from mistralai.workflows.core.task import task

_interleave_events: dict[str, asyncio.Event] | None = None
_activity_log: list[tuple[str, str]] = []


@activity()
async def route_token_task(task_name: str = "route-token-task") -> str:
    async with task(task_name):
        return task_name


@workflow.define(name="test-event-route-single-activity")
class SingleActivityWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return await route_token_task()


class _RetryCounter:
    def __init__(self) -> None:
        self.count = 0


def _get_retry_counter() -> _RetryCounter:
    return _RetryCounter()


def _get_current_workflow_id() -> str:
    from temporalio import activity as temporal_activity

    workflow_id = temporal_activity.info().workflow_id
    assert workflow_id is not None
    return workflow_id


@activity()
async def route_token_task_fail_once(
    task_name: str = "route-token-retry-task",
    counter: _RetryCounter = Depends(_get_retry_counter),
) -> str:
    from temporalio.exceptions import ApplicationError

    counter.count += 1

    async with task(task_name):
        if counter.count == 1:
            raise ApplicationError("transient failure")
        return task_name


@activity()
async def route_token_task_sync_point(task_name: str = "route-token-sync-point") -> str:
    wf_id = _get_current_workflow_id()
    _activity_log.append((wf_id, "route_token_task_sync_point"))

    async with task(task_name):
        if _interleave_events is not None:
            my_event = _interleave_events[wf_id]
            other_events = [e for k, e in _interleave_events.items() if k != wf_id]
            my_event.set()
            for e in other_events:
                await e.wait()
        return task_name


@activity()
async def route_token_task_logged(task_name: str = "route-token-logged") -> str:
    wf_id = _get_current_workflow_id()
    _activity_log.append((wf_id, "route_token_task_logged"))

    async with task(task_name):
        return task_name


@workflow.define(name="test-event-route-two-activities")
class TwoActivityWorkflow:
    @workflow.entrypoint
    async def run(self) -> list[str]:
        first = await route_token_task("route-token-first")
        second = await route_token_task("route-token-second")
        return [first, second]


@workflow.define(name="test-event-route-retry")
class RetryWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return await route_token_task_fail_once()


class IterationInput(BaseModel):
    iteration: int = 0


@workflow.define(name="test-event-route-continue-as-new")
class ContinueAsNewWorkflow:
    @workflow.entrypoint
    async def run(self, params: IterationInput) -> dict[str, bool]:
        await route_token_task(f"route-token-can-{params.iteration}")
        if params.iteration < 1:
            workflow.continue_as_new(IterationInput(iteration=params.iteration + 1))
        return {"done": True}


@workflow.define(name="test-event-route-interleaved")
class InterleavedWorkflow:
    @workflow.entrypoint
    async def run(self) -> list[str]:
        first = await route_token_task_sync_point()
        second = await route_token_task_logged()
        return [first, second]
