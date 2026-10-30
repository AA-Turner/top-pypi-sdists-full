import asyncio
import dataclasses
from collections import defaultdict
from datetime import timedelta
from typing import Any, NamedTuple
from unittest.mock import AsyncMock

import pytest
from pydantic import TypeAdapter
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._events import event_activities
from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.protocol.v1.events import (
    CustomTaskCompleted,
    CustomTaskInProgress,
    CustomTaskStarted,
    WorkflowEvent,
    WorkflowExecutionStarted,
)
from mistralai.workflows.testing import create_test_worker_with_events

from .fixtures_task import (
    EmitterInUserActivityWorkflow,
    TaskInWorkflowWorkflow,
    emit_task_from_user_activity,
    simple_task_activity,
)

_event_adapter: TypeAdapter[WorkflowEvent] = TypeAdapter(WorkflowEvent)


class _LogicalEvent(NamedTuple):
    event_type: str
    attributes: str


def _logical(event: WorkflowEvent) -> _LogicalEvent:
    return _LogicalEvent(event.event_type, event.attributes.model_dump_json())


def _events_client(captured: list[WorkflowEvent], hang_on: type | None = None, hang_times: int = 0) -> AsyncMock:
    hangs_left = hang_times

    async def send_event(*, event: Any, **kwargs: Any) -> None:
        nonlocal hangs_left
        parsed = _event_adapter.validate_python(event)
        captured.append(parsed)
        if hang_on is not None and isinstance(parsed, hang_on) and hangs_left > 0:
            hangs_left -= 1
            await asyncio.Event().wait()

    client = AsyncMock()
    client.send_event_async = AsyncMock(side_effect=send_event)
    return client


async def _run_workflow(
    env: WorkflowEnvironment,
    events_client: AsyncMock,
    workflow: type,
    activities: list[Any],
    workflow_id: str,
    *args: Any,
) -> None:
    async with EventContext(events_client):
        async with create_test_worker_with_events(env, workflows=[workflow], activities=activities):
            await env.client.execute_workflow(workflow, *args, id=workflow_id, task_queue="test-task-queue")


async def _run_task_workflow(env: WorkflowEnvironment, events_client: AsyncMock, workflow_id: str) -> None:
    await _run_workflow(env, events_client, TaskInWorkflowWorkflow, [simple_task_activity], workflow_id)


class TestEmitterEventIds:
    @pytest.mark.asyncio
    async def test_every_event_of_a_run_has_a_distinct_id(self, temporal_env: WorkflowEnvironment) -> None:
        captured: list[WorkflowEvent] = []

        await _run_task_workflow(temporal_env, _events_client(captured), "distinct-ids")

        assert len({e.event_id for e in captured}) == len(captured)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("run_locally", [False, True])
    async def test_events_emitted_from_a_user_activity_keep_distinct_ids(
        self, temporal_env: WorkflowEnvironment, run_locally: bool
    ) -> None:
        captured: list[WorkflowEvent] = []

        await _run_workflow(
            temporal_env,
            _events_client(captured),
            EmitterInUserActivityWorkflow,
            [emit_task_from_user_activity],
            f"user-activity-{run_locally}",
            run_locally,
        )

        emitted = [e for e in captured if isinstance(e, (CustomTaskStarted, CustomTaskCompleted))]
        assert [type(e) for e in emitted] == [CustomTaskStarted, CustomTaskCompleted]
        assert emitted[0].event_id != emitted[1].event_id

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("event_type", "hang_times"),
        [
            (WorkflowExecutionStarted, 1),
            (CustomTaskStarted, 1),
            (CustomTaskInProgress, 1),
            (CustomTaskStarted, 4),
            (CustomTaskInProgress, 4),
        ],
    )
    async def test_retried_emitter_resends_each_event_under_one_id(
        self,
        temporal_env: WorkflowEnvironment,
        monkeypatch: pytest.MonkeyPatch,
        event_type: type,
        hang_times: int,
    ) -> None:
        monkeypatch.setattr(event_activities, "_EMITTER_START_TO_CLOSE_TIMEOUT", timedelta(seconds=1))
        monkeypatch.setattr(
            event_activities,
            "_EMITTER_RETRY_POLICY",
            dataclasses.replace(event_activities._EMITTER_RETRY_POLICY, initial_interval=timedelta(milliseconds=100)),
        )
        captured: list[WorkflowEvent] = []

        await _run_task_workflow(
            temporal_env,
            _events_client(captured, hang_on=event_type, hang_times=hang_times),
            f"resend-{event_type.__name__}-{hang_times}",
        )

        ids_by_event: defaultdict[_LogicalEvent, set[str]] = defaultdict(set)
        events_by_id: defaultdict[str, set[_LogicalEvent]] = defaultdict(set)
        for e in captured:
            ids_by_event[_logical(e)].add(e.event_id)
            events_by_id[e.event_id].add(_logical(e))
        assert all(len(ids) == 1 for ids in ids_by_event.values())
        assert all(len(events) == 1 for events in events_by_id.values())
        first_hung = next(e for e in captured if isinstance(e, event_type))
        assert sum(_logical(e) == _logical(first_hung) for e in captured) == hang_times + 1
