from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable, List, Type

from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from temporalio.worker.workflow_sandbox import SandboxedWorkflowRunner

from mistralai.workflows.core._events.event_activities import (
    _emit_events_batch,
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
from mistralai.workflows.core._registration.registration_activity import _register_execution
from mistralai.workflows.core._registration.search_key_ingestion import _delete_search_keys, _upsert_search_keys
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.config.config import AppConfig, resolve_worker_config
from mistralai.workflows.core.definition._workflow_preparation import prepare_workflows
from mistralai.workflows.core.dependencies.dependency_injector import DependencyInjector
from mistralai.workflows.core.execution.concurrency._execute_activities_in_batch import execute_activity_in_batch
from mistralai.workflows.core.execution.sticky_session.get_sticky_worker_session import (
    GET_STICKY_WORKER_SESSION_ACTIVITY_NAME,
)
from mistralai.workflows.core.execution.sticky_session.sticky_worker_session import StickyWorkerSession
from mistralai.workflows.core.execution.workflow_run_config import _record_workflow_run_config
from mistralai.workflows.core.sandbox import get_sandbox_restrictions


def get_internal_activities() -> list[Callable]:
    """The SDK's own activities that a worker built with `temporalio.worker.Worker` must register.

    The SDK schedules them itself (event emitters, execution registration, the run-config snapshot, ...), so a
    workflow fails on a worker that lacks one. `run_worker` and the testing helpers register them; a hand-built
    worker should add this list to its own activities instead of naming them, so a new SDK activity needs no
    change. Plugins' own activities are not included.
    """
    return [
        _emit_events_batch,
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
        _record_workflow_run_config,
        _register_execution,
        _upsert_search_keys,
        _delete_search_keys,
        execute_activity_in_batch,
    ]


def _activity_name(activity_fn: Callable) -> str:
    defn = getattr(activity_fn, "__temporal_activity_definition", None)
    return defn.name if defn is not None else activity_fn.__name__


def _with_internal_activities(activities: List[Callable]) -> list[Callable]:
    """Add the internal activities the caller doesn't already pass, since Temporal rejects a name registered twice."""
    names = {_activity_name(a) for a in activities}
    return [*activities, *(a for a in get_internal_activities() if _activity_name(a) not in names)]


def _test_worker_config(task_queue: str) -> AppConfig:
    config = resolve_worker_config(None).model_copy(deep=True)
    config.worker.deployment_name = task_queue
    return config


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

    all_activities = _with_internal_activities([*(activities or []), get_sticky_worker_session])

    with prepare_workflows(workflows, config=_test_worker_config(task_queue)) as prepared_workflows:
        worker = Worker(
            env.client,
            task_queue=task_queue,
            workflows=prepared_workflows,
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

    all_activities = _with_internal_activities([*(activities or []), get_sticky_worker_session])

    with prepare_workflows(workflows, config=_test_worker_config(task_queue)) as prepared_workflows:
        worker = Worker(
            env.client,
            task_queue=task_queue,
            workflows=prepared_workflows,
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
