from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable, List, Type

from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from temporalio.worker.workflow_sandbox import SandboxedWorkflowRunner

from mistralai.workflows.core._events.event_activities import (
    _emit_task_completed,
    _emit_task_failed,
    _emit_task_in_progress,
    _emit_task_started,
    _emit_waiting_for_input_completed,
    _emit_waiting_for_input_failed,
    _emit_waiting_for_input_started,
    _emit_workflow_canceled,
    _emit_workflow_completed,
    _emit_workflow_failed,
    _emit_workflow_started,
    _persist_task_span_context,
)
from mistralai.workflows.core._events.event_interceptor import EventInterceptor
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.dependencies.dependency_injector import DependencyInjector
from mistralai.workflows.core.execution.sticky_session.get_sticky_worker_session import (
    GET_STICKY_WORKER_SESSION_ACTIVITY_NAME,
)
from mistralai.workflows.core.execution.sticky_session.sticky_worker_session import StickyWorkerSession
from mistralai.workflows.core.sandbox import get_sandbox_restrictions


@asynccontextmanager
async def create_test_worker(
    env: WorkflowEnvironment,
    workflows: List[Type],
    activities: List[Callable] | None = None,
    task_queue: str = "test-task-queue",
    interceptors: List | None = None,
) -> AsyncGenerator[Worker, None]:
    """Create a test worker with basic workflow event activities.

    This helper sets up a Temporal worker for testing with the necessary
    event-emitting activities pre-registered.
    """

    @activity(name=GET_STICKY_WORKER_SESSION_ACTIVITY_NAME, _skip_registering=True)
    async def get_sticky_worker_session() -> StickyWorkerSession:
        return StickyWorkerSession(task_queue=task_queue)

    all_activities = list(activities or [])
    all_activities.append(get_sticky_worker_session)
    all_activities.extend(
        [
            _emit_waiting_for_input_started,
            _emit_waiting_for_input_completed,
            _emit_waiting_for_input_failed,
            _emit_workflow_started,
            _emit_workflow_completed,
            _emit_workflow_canceled,
            _emit_workflow_failed,
            _persist_task_span_context,
        ]
    )

    worker = Worker(
        env.client,
        task_queue=task_queue,
        workflows=workflows,
        activities=all_activities,
        interceptors=interceptors or [],
        workflow_runner=SandboxedWorkflowRunner(
            restrictions=get_sandbox_restrictions(),
        ),
    )

    # Establish a DI context like the production worker does (worker.py:361).
    # Scope it to only the dependencies required by the activities under test,
    # so unrelated deps registered by other modules (e.g. webhook plugin)
    # in the same process don't get resolved and cause connection failures.
    needed_deps = DependencyInjector.collect_dependencies(all_activities)
    injector = DependencyInjector.get_singleton_instance()
    async with injector.with_scoped_dependencies(needed_deps), worker:
        yield worker


@asynccontextmanager
async def create_test_worker_with_events(
    env: WorkflowEnvironment,
    workflows: List[Type],
    activities: List[Callable] | None = None,
    task_queue: str = "test-task-queue",
    interceptors: List | None = None,
) -> AsyncGenerator[Worker, None]:
    """Create a test worker with full event support including task events.

    This helper sets up a Temporal worker for testing with both workflow
    and task event-emitting activities, plus the EventInterceptor for
    capturing custom task events.
    """

    @activity(name=GET_STICKY_WORKER_SESSION_ACTIVITY_NAME, _skip_registering=True)
    async def get_sticky_worker_session() -> StickyWorkerSession:
        return StickyWorkerSession(task_queue=task_queue)

    all_activities = list(activities or [])
    all_activities.append(get_sticky_worker_session)
    all_activities.extend(
        [
            _emit_waiting_for_input_started,
            _emit_waiting_for_input_completed,
            _emit_waiting_for_input_failed,
            _emit_workflow_started,
            _emit_workflow_completed,
            _emit_workflow_canceled,
            _emit_workflow_failed,
            _emit_task_started,
            _emit_task_in_progress,
            _emit_task_completed,
            _emit_task_failed,
            _persist_task_span_context,
        ]
    )

    worker = Worker(
        env.client,
        task_queue=task_queue,
        workflows=workflows,
        activities=all_activities,
        interceptors=[*(interceptors or []), EventInterceptor()],
        workflow_runner=SandboxedWorkflowRunner(
            restrictions=get_sandbox_restrictions(),
        ),
    )

    needed_deps = DependencyInjector.collect_dependencies(all_activities)
    injector = DependencyInjector.get_singleton_instance()
    async with injector.with_scoped_dependencies(needed_deps), worker:
        yield worker
