from typing import Any

import pytest
from pydantic import BaseModel
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Replayer
from temporalio.worker.workflow_sandbox import SandboxedWorkflowRunner

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core._events.event_interceptor import EventInterceptor
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.sandbox import get_sandbox_restrictions
from mistralai.workflows.core.task import task
from mistralai.workflows.core.workflow import workflow
from mistralai.workflows.protocol.v1.events import WorkflowEventType

from .utils import create_capturing_mock_events_client, create_test_worker_with_events


class TaskState(BaseModel):
    progress: int = 0


@activity(name="replay_test_step")
async def do_step(name: str) -> str:
    return f"{name}_done"


@workflow.define(name="replay_test_task_workflow")
class TaskWithActivitiesWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        async with task("work", state=TaskState()) as t:
            await t.update_state({"progress": 50})
            result = await do_step("step1")
            await t.update_state({"progress": 100})
            return {"result": result, "progress": t.state.progress}


class TestTaskReplayDeterminism:
    @pytest.mark.asyncio
    async def test_events_published_during_execution_not_during_replay(self, temporal_env: WorkflowEnvironment) -> None:
        """Events published during first run, none during replay, no nondeterminism."""
        execution_events: list[Any] = []
        replay_events: list[Any] = []

        mock_client = create_capturing_mock_events_client(execution_events)

        async with EventContext(mock_client):
            async with create_test_worker_with_events(
                temporal_env,
                workflows=[TaskWithActivitiesWorkflow],
                activities=[do_step],
            ):
                handle = await temporal_env.client.start_workflow(
                    "replay_test_task_workflow",
                    id="replay-test",
                    task_queue="test-task-queue",
                )
                await handle.result()
                history = await handle.fetch_history()

        assert len(execution_events) > 0, "Events should be published during execution"

        event_types = {e.event_type for e in execution_events}
        assert WorkflowEventType.WORKFLOW_EXECUTION_STARTED in event_types
        assert WorkflowEventType.WORKFLOW_EXECUTION_COMPLETED in event_types
        assert WorkflowEventType.CUSTOM_TASK_STARTED in event_types
        assert WorkflowEventType.CUSTOM_TASK_COMPLETED in event_types

        mock_client_replay = create_capturing_mock_events_client(replay_events)

        async with EventContext(mock_client_replay):
            replayer = Replayer(
                workflows=[TaskWithActivitiesWorkflow],
                interceptors=[EventInterceptor()],
                workflow_runner=SandboxedWorkflowRunner(
                    restrictions=get_sandbox_restrictions(),
                ),
            )
            await replayer.replay_workflow(history)

        assert len(replay_events) == 0, "No events should be published during replay"

    @pytest.mark.asyncio
    async def test_replay_determinism_with_span_context_persistence(self, temporal_env: WorkflowEnvironment) -> None:
        """Replay succeeds without nondeterminism errors after adding _persist_task_span_context."""
        execution_events: list[Any] = []
        mock_client = create_capturing_mock_events_client(execution_events)

        async with EventContext(mock_client):
            async with create_test_worker_with_events(
                temporal_env,
                workflows=[TaskWithActivitiesWorkflow],
                activities=[do_step],
            ):
                handle = await temporal_env.client.start_workflow(
                    "replay_test_task_workflow",
                    id="replay-span-context-test",
                    task_queue="test-task-queue",
                )
                await handle.result()
                history = await handle.fetch_history()

        # Replay the workflow (simulates worker restart) — must not raise
        replay_events: list[Any] = []
        mock_client_replay = create_capturing_mock_events_client(replay_events)

        async with EventContext(mock_client_replay):
            replayer = Replayer(
                workflows=[TaskWithActivitiesWorkflow],
                interceptors=[EventInterceptor()],
                workflow_runner=SandboxedWorkflowRunner(
                    restrictions=get_sandbox_restrictions(),
                ),
            )
            await replayer.replay_workflow(history)

        assert len(replay_events) == 0, "No events should be published during replay"
