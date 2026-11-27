import asyncio
from contextlib import AbstractContextManager, nullcontext
from functools import partial
from typing import Any
from unittest.mock import patch

import pytest
from pydantic import BaseModel
from temporalio.client import WorkflowHistory
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Replayer, Worker
from temporalio.worker.workflow_sandbox import SandboxedWorkflowRunner

from mistralai.workflows import prepare_workflows
from mistralai.workflows.core._events import event_interceptor
from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core._events.event_interceptor import EventInterceptor
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.execution.workflow_run_config import RECORD_WORKFLOW_RUN_CONFIG_PATCH, WorkflowRunConfig
from mistralai.workflows.core.sandbox import get_sandbox_restrictions
from mistralai.workflows.core.task import task
from mistralai.workflows.core.temporal.context_handler_interceptor import ContextHandlerInterceptor
from mistralai.workflows.core.utils.contextvars import unwrap_contextual_result
from mistralai.workflows.core.workflow import workflow
from mistralai.workflows.protocol.v1.events import WorkflowEvent, WorkflowEventCategory, WorkflowEventType
from mistralai.workflows.testing import ALL_EVENT_CATEGORIES

from .fixtures_event_batch import ManualEventsAcrossSignalsWorkflow, ManualEventsWorkflow
from .utils import create_capturing_mock_event_publisher, create_test_worker_with_events


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


class TestManualEventReplayDeterminism:
    @pytest.mark.asyncio
    async def test_old_run_publishes_new_batches_after_upgrade(self, temporal_env: WorkflowEnvironment) -> None:
        events: list[Any] = []

        async def publish_without_history(context: EventContext, batch: list[WorkflowEvent]) -> None:
            await context._event_publisher.publish(batch)

        published_after_restart: list[list[dict[str, int]]] = []
        # Keep queries off a stopped worker's sticky queue in the time-skipping server.
        with patch("mistralai.workflows.testing.test_worker.Worker", partial(Worker, max_cached_workflows=0)):
            async with EventContext(create_capturing_mock_event_publisher(events)):
                with patch.object(EventContext, "publish_events_batch", publish_without_history):
                    async with create_test_worker_with_events(
                        temporal_env, workflows=[ManualEventsAcrossSignalsWorkflow]
                    ):
                        handle = await temporal_env.client.start_workflow(
                            "manual_events_across_signals", id="manual-event-upgrade", task_queue="test-task-queue"
                        )
                        async with asyncio.timeout(10):
                            while await handle.query("published_batches") != 1:
                                await asyncio.sleep(0.01)
                old_history = await handle.fetch_history()
                assert "durable-manual-event-batches" not in old_history.to_json()
                assert any(e.event_type == WorkflowEventType.CUSTOM_TASK_COMPLETED for e in events)
                events.clear()

                for step in (2, 3):
                    async with create_test_worker_with_events(
                        temporal_env, workflows=[ManualEventsAcrossSignalsWorkflow]
                    ):
                        await handle.signal("advance")
                        if step == 3:
                            await asyncio.wait_for(handle.result(), timeout=10)
                        else:
                            async with asyncio.timeout(10):
                                while await handle.query("published_batches") != step:
                                    await asyncio.sleep(0.01)
                    published_after_restart.append(
                        [
                            e.attributes.payload.value
                            for e in events
                            if e.event_type == WorkflowEventType.CUSTOM_TASK_COMPLETED
                        ]
                    )
                history = await handle.fetch_history()

        replay_events: list[Any] = []
        async with EventContext(create_capturing_mock_event_publisher(replay_events)):
            with prepare_workflows([ManualEventsAcrossSignalsWorkflow], replay_only=True) as prepared:
                await Replayer(
                    workflows=prepared,
                    interceptors=[EventInterceptor()],
                    workflow_runner=SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
                ).replay_workflow(history)
        assert replay_events == []
        assert published_after_restart == [[{"batch": 1}], [{"batch": 1}, {"batch": 2}]]
        assert {e.event_id for e in events if e.event_type == WorkflowEventType.CUSTOM_TASK_COMPLETED} == {
            "reused-user-event-id"
        }

    @pytest.mark.asyncio
    @pytest.mark.parametrize("history_kind", ["current", "direct-publish"])
    async def test_replay_does_not_publish_again(
        self, temporal_env_with_converter: WorkflowEnvironment, history_kind: str
    ) -> None:
        execution_events: list[Any] = []

        async def publish_without_history(context: EventContext, events: list[WorkflowEvent]) -> None:
            await context._event_publisher.publish(events)

        legacy_publisher: AbstractContextManager[Any] = nullcontext()
        if history_kind == "direct-publish":
            legacy_publisher = patch.object(EventContext, "publish_events_batch", publish_without_history)
        env = temporal_env_with_converter
        async with EventContext(create_capturing_mock_event_publisher(execution_events)):
            with legacy_publisher:
                async with create_test_worker_with_events(
                    env, workflows=[ManualEventsWorkflow], interceptors=[ContextHandlerInterceptor()]
                ):
                    handle = await env.client.start_workflow(
                        "manual_events", id="manual-event-replay", task_queue="test-task-queue"
                    )
                    assert unwrap_contextual_result(await handle.result())[1] == {"result": "done"}
                    history = await handle.fetch_history()

        assert any(e.event_type == WorkflowEventType.CUSTOM_TASK_COMPLETED for e in execution_events)
        replay_events: list[Any] = []
        async with EventContext(create_capturing_mock_event_publisher(replay_events)):
            with prepare_workflows([ManualEventsWorkflow], replay_only=True) as prepared:
                replayer = Replayer(
                    workflows=prepared,
                    interceptors=[ContextHandlerInterceptor(), EventInterceptor()],
                    data_converter=env.client.data_converter,
                    workflow_runner=SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
                )
                await replayer.replay_workflow(history)

        assert replay_events == []


class TestTaskReplayDeterminism:
    @pytest.mark.asyncio
    async def test_events_published_during_execution_not_during_replay(self, temporal_env: WorkflowEnvironment) -> None:
        """Events published during first run, none during replay, no nondeterminism."""
        execution_events: list[Any] = []
        replay_events: list[Any] = []

        mock_client = create_capturing_mock_event_publisher(execution_events)

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

        mock_client_replay = create_capturing_mock_event_publisher(replay_events)

        async with EventContext(mock_client_replay):
            with prepare_workflows([TaskWithActivitiesWorkflow], replay_only=True) as prepared:
                replayer = Replayer(
                    workflows=prepared,
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
        mock_client = create_capturing_mock_event_publisher(execution_events)

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
        mock_client_replay = create_capturing_mock_event_publisher(replay_events)

        async with EventContext(mock_client_replay):
            with prepare_workflows([TaskWithActivitiesWorkflow], replay_only=True) as prepared:
                replayer = Replayer(
                    workflows=prepared,
                    interceptors=[EventInterceptor()],
                    workflow_runner=SandboxedWorkflowRunner(
                        restrictions=get_sandbox_restrictions(),
                    ),
                )
                await replayer.replay_workflow(history)

        assert len(replay_events) == 0, "No events should be published during replay"


_DEFAULT = frozenset({WorkflowEventCategory.WORKFLOW, WorkflowEventCategory.CUSTOM_TASK})
_NO_WORKFLOW = frozenset({WorkflowEventCategory.CUSTOM_TASK})


async def _record_history(
    env: WorkflowEnvironment, workflow_cls: type, categories: frozenset[WorkflowEventCategory], workflow_id: str
) -> WorkflowHistory:
    async with EventContext(create_capturing_mock_event_publisher([]), emitted_event_categories=categories):
        async with create_test_worker_with_events(env, workflows=[workflow_cls], activities=[do_step]):
            handle = await env.client.start_workflow(
                "replay_test_task_workflow", id=workflow_id, task_queue="test-task-queue"
            )
            await handle.result()
            return await handle.fetch_history()


async def _replay(history: WorkflowHistory, categories: frozenset[WorkflowEventCategory]) -> list[Any]:
    replay_events: list[Any] = []
    async with EventContext(create_capturing_mock_event_publisher(replay_events), emitted_event_categories=categories):
        with prepare_workflows([TaskWithActivitiesWorkflow], replay_only=True) as prepared:
            replayer = Replayer(
                workflows=prepared,
                interceptors=[EventInterceptor()],
                workflow_runner=SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
            )
            await replayer.replay_workflow(history)
    return replay_events


class TestWorkflowRunConfigReplay:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("recorded_with", "replayed_with"),
        [
            pytest.param(_DEFAULT, _NO_WORKFLOW, id="workflow-disabled-after-start"),
            pytest.param(_NO_WORKFLOW, _DEFAULT, id="workflow-re-enabled-after-start"),
            pytest.param(_DEFAULT, ALL_EVENT_CATEGORIES, id="activity-enabled-after-start"),
        ],
    )
    async def test_run_keeps_the_settings_it_started_with(
        self,
        temporal_env: WorkflowEnvironment,
        recorded_with: frozenset[WorkflowEventCategory],
        replayed_with: frozenset[WorkflowEventCategory],
    ) -> None:
        history = await _record_history(temporal_env, TaskWithActivitiesWorkflow, recorded_with, "replay-run-config")

        assert await _replay(history, replayed_with) == []

    @pytest.mark.asyncio
    @pytest.mark.parametrize("replayed_with", [_DEFAULT, _NO_WORKFLOW], ids=["default", "workflow-disabled"])
    async def test_history_from_before_the_patch_replays(
        self,
        temporal_env: WorkflowEnvironment,
        replayed_with: frozenset[WorkflowEventCategory],
    ) -> None:
        async def record_like_before_the_patch() -> WorkflowRunConfig:
            return WorkflowRunConfig()

        with pytest.MonkeyPatch.context() as monkeypatch:
            monkeypatch.setattr(event_interceptor, "record_workflow_run_config", record_like_before_the_patch)
            history = await _record_history(temporal_env, TaskWithActivitiesWorkflow, _DEFAULT, "replay-pre-run-config")
        assert RECORD_WORKFLOW_RUN_CONFIG_PATCH not in str(history.to_json())

        assert await _replay(history, replayed_with) == []
