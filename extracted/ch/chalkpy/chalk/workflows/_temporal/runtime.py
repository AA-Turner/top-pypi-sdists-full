from __future__ import annotations

import asyncio
import contextvars
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from typing import Any, Awaitable, Callable, Iterable, Mapping, Sequence

from temporalio import activity as temporal_activity
from temporalio import workflow as temporal_workflow
from temporalio.client import Client, WorkflowExecutionStatus, WorkflowHandle
from temporalio.common import RetryPolicy
from temporalio.worker import Worker

from chalk.workflows._context import TaskHandle, current_orchestrator_var
from chalk.workflows._definitions import TASK_REGISTRY, WORKFLOW_REGISTRY, TaskDefinition, WorkflowDefinition
from chalk.workflows._messages import (
    WORKFLOW_MESSAGE_SIGNAL,
    WorkflowMessage,
    WorkflowMessageTimeoutError,
    message_from_envelope,
)

DEFAULT_TASK_QUEUE = "chalk-workflows"

# Retries are configured on `@task` via Chalk's retry parameters; a workflow-level
# Temporal retry policy would silently re-run orchestration code on task failure.
_NO_WORKFLOW_RETRIES = RetryPolicy(maximum_attempts=1)


# A task routed to its own worker runs as a child workflow of this name on that worker's
# queue: task queue triggers scale a worker on the workflows open on its queue, which a bare
# activity on the queue would not count as.
TASK_RUNNER_PREFIX = "chalk.task:"


def _task_retry_policy(task: TaskDefinition[Any, Any]) -> RetryPolicy:
    return RetryPolicy(
        maximum_attempts=task.retries + 1,
        initial_interval=task.retry_delay if task.retry_delay is not None else timedelta(seconds=1),
    )


# Time allowed for a task's own worker to scale up from zero before its activity is
# picked up, on top of the task's attempts; past it the routed call fails instead of
# waiting forever on a worker that never comes up.
_TASK_WORKER_STARTUP_ALLOWANCE = timedelta(minutes=15)


def _routed_task_schedule_to_close(task: TaskDefinition[Any, Any]) -> timedelta:
    attempts = task.retries + 1
    retry_delay = task.retry_delay if task.retry_delay is not None else timedelta(seconds=1)
    return task.timeout * attempts + retry_delay * task.retries + _TASK_WORKER_STARTUP_ALLOWANCE


def _start_task_activity(
    task: TaskDefinition[Any, Any],
    args: Sequence[Any],
    kwargs: Mapping[str, Any],
    *,
    schedule_to_close_timeout: timedelta | None = None,
) -> Any:
    return temporal_workflow.start_activity(
        task.name,
        args=[list(args), dict(kwargs)],
        start_to_close_timeout=task.timeout,
        schedule_to_close_timeout=schedule_to_close_timeout,
        retry_policy=_task_retry_policy(task),
    )


class _TemporalOrchestrator:
    """Routes task invocations made inside a compiled workflow to Temporal activities."""

    def __init__(self, messages: dict[str, deque[dict[str, Any]]]):
        super().__init__()
        # The workflow instance's buffer of delivered messages, by name; see build_workflow_class.
        self._messages = messages

    async def wait_for_message(self, name: str, timeout: timedelta | None) -> WorkflowMessage:
        queue = self._messages.setdefault(name, deque())
        deadline = None if timeout is None else temporal_workflow.now() + timeout
        # One message can wake several concurrent waiters on the same name, so a waiter that
        # finds the queue already drained waits again until the original deadline. Nothing
        # yields between the emptiness check and popleft, so exactly one waiter takes each message.
        while not queue:
            remaining = None if deadline is None else deadline - temporal_workflow.now()
            if remaining is not None and remaining <= timedelta(0):
                raise WorkflowMessageTimeoutError(f"No {name!r} message arrived within {timeout}")
            try:
                # Deterministic on replay: the signals that fill the queue are recorded in history.
                await temporal_workflow.wait_condition(lambda: len(queue) > 0, timeout=remaining)
            except asyncio.TimeoutError:
                raise WorkflowMessageTimeoutError(f"No {name!r} message arrived within {timeout}") from None
        return message_from_envelope(queue.popleft())

    def _start(self, task: TaskDefinition[Any, Any], args: Sequence[Any], kwargs: Mapping[str, Any]) -> Any:
        if task.task_queue is None:
            return _start_task_activity(task, args, kwargs)
        # Scheduled now, like `start_activity`, so `submit()`ed tasks run in parallel.
        return asyncio.ensure_future(
            temporal_workflow.execute_child_workflow(
                f"{TASK_RUNNER_PREFIX}{task.name}",
                args=[list(args), dict(kwargs)],
                task_queue=task.task_queue,
                # Attempts are the activity's retry policy, inside the child.
                retry_policy=_NO_WORKFLOW_RETRIES,
            )
        )

    def run_task(
        self, task: TaskDefinition[Any, Any], args: Sequence[Any], kwargs: Mapping[str, Any]
    ) -> Awaitable[Any]:
        return self._start(task, args, kwargs)

    def submit_task(
        self, task: TaskDefinition[Any, Any], args: Sequence[Any], kwargs: Mapping[str, Any]
    ) -> TaskHandle[Any]:
        return TaskHandle(self._start(task, args, kwargs))


def build_workflow_class(definition: WorkflowDefinition[Any, Any]) -> type:
    """Compile a Chalk workflow definition into a Temporal workflow class.

    The workflow runs unsandboxed because user workflow functions live in modules
    that import the full chalk SDK (pyarrow et al.), which Temporal's import
    sandbox cannot replay; determinism of the orchestration code is a documented
    requirement of `@workflow` instead.
    """

    def __init__(self: Any) -> None:
        # Messages delivered by the API server but not yet taken by wait_for_message. Signals can
        # arrive before `run` starts waiting (or before it starts at all), so they are buffered
        # here rather than handed straight to a waiter.
        self._chalk_messages = {}

    # Every message arrives on one signal, with its name inside the envelope; see
    # WORKFLOW_MESSAGE_SIGNAL.
    def on_message(self: Any, envelope: dict[str, Any]) -> None:
        self._chalk_messages.setdefault(str(envelope.get("name", "")), deque()).append(envelope)

    # Temporal invokes workflows with positional payloads; the SDK convention here is
    # a single JSON object holding the workflow function's keyword arguments.
    async def run(self: Any, kwargs: dict[str, Any]) -> Any:
        token: contextvars.Token[Any] = current_orchestrator_var.set(_TemporalOrchestrator(self._chalk_messages))
        try:
            return await definition.fn(**kwargs)
        finally:
            current_orchestrator_var.reset(token)

    # The class is assembled with type() and given a module-level-looking qualname:
    # temporalio rejects run methods whose qualname contains '<locals>'.
    class_name = f"ChalkWorkflow_{definition.name}"
    for method in (__init__, on_message, run):
        method.__qualname__ = f"{class_name}.{method.__name__}"
        method.__module__ = definition.fn.__module__
    cls = type(
        class_name,
        (),
        {
            "__init__": __init__,
            "on_message": temporal_workflow.signal(name=WORKFLOW_MESSAGE_SIGNAL)(on_message),
            "run": temporal_workflow.run(run),
        },
    )
    cls.__module__ = definition.fn.__module__
    return temporal_workflow.defn(name=definition.name, sandboxed=False)(cls)


def build_task_runner_workflow(task: TaskDefinition[Any, Any]) -> type:
    """Compile the child workflow that runs `task` as an activity on its own worker's queue."""

    async def run(self: Any, args: list[Any], kwargs: dict[str, Any]) -> Any:
        return await _start_task_activity(
            task, args, kwargs, schedule_to_close_timeout=_routed_task_schedule_to_close(task)
        )

    class_name = f"ChalkTaskRunner_{task.name}"
    run.__qualname__ = f"{class_name}.run"
    run.__module__ = task.fn.__module__
    cls = type(class_name, (), {"run": temporal_workflow.run(run)})
    cls.__module__ = task.fn.__module__
    return temporal_workflow.defn(name=f"{TASK_RUNNER_PREFIX}{task.name}", sandboxed=False)(cls)


def build_activity(task: TaskDefinition[Any, Any]) -> Callable[..., Any]:
    """Compile a Chalk task definition into a Temporal activity callable."""
    if task.is_async:

        @temporal_activity.defn(name=task.name)
        async def run_activity_async(args: list[Any], kwargs: dict[str, Any]) -> Any:
            return await task.fn(*args, **kwargs)

        return run_activity_async

    @temporal_activity.defn(name=task.name)
    def run_activity(args: list[Any], kwargs: dict[str, Any]) -> Any:
        return task.fn(*args, **kwargs)

    return run_activity


async def connect_workflow_orchestrator(
    address: str,
    namespace: str,
    *,
    use_tls: bool,
    bearer_token: str | None,
    environment_id: str | None,
) -> Client:
    """Connect to a Chalk workflow orchestrator's Temporal frontend.

    From outside the data plane, `address` is the orchestrator's public gateway
    (TLS, Chalk JWT required); in-cluster workers dial the frontend service
    directly, with a service-account token on a shared orchestrator and without
    one otherwise. A token that expires must be refreshed by the caller; see
    `chalk.workflows._orchestrator_auth.connect_with_token`.
    """
    rpc_metadata: dict[str, str] = {}
    if bearer_token is not None:
        if not bearer_token.lower().startswith("bearer "):
            bearer_token = f"Bearer {bearer_token}"
        rpc_metadata["authorization"] = bearer_token
    if environment_id is not None:
        rpc_metadata["x-chalk-env-id"] = environment_id
    return await Client.connect(
        address,
        namespace=namespace,
        tls=use_tls,
        rpc_metadata=rpc_metadata,
    )


def create_worker(
    client: Client,
    *,
    task_queue: str,
    workflows: Iterable[WorkflowDefinition[Any, Any]] | None = None,
    tasks: Iterable[TaskDefinition[Any, Any]] | None = None,
    task_runners: Iterable[TaskDefinition[Any, Any]] = (),
    max_concurrent_tasks: int = 16,
) -> Worker:
    """Create a Temporal worker hosting the given (default: all registered)
    Chalk workflows and tasks, plus the child workflows that run `task_runners`
    routed to this worker's queue."""
    workflow_definitions = list(workflows) if workflows is not None else list(WORKFLOW_REGISTRY.values())
    task_definitions = list(tasks) if tasks is not None else list(TASK_REGISTRY.values())
    return Worker(
        client,
        task_queue=task_queue,
        workflows=[
            *(build_workflow_class(w) for w in workflow_definitions),
            *(build_task_runner_workflow(t) for t in task_runners),
        ],
        activities=[build_activity(t) for t in task_definitions],
        activity_executor=ThreadPoolExecutor(max_workers=max_concurrent_tasks),
    )


async def start_workflow(
    client: Client,
    *,
    workflow_name: str,
    input: Mapping[str, Any] | None,
    workflow_id: str,
    task_queue: str,
) -> WorkflowHandle[Any, Any]:
    return await client.start_workflow(
        workflow_name,
        dict(input) if input is not None else {},
        id=workflow_id,
        task_queue=task_queue,
        retry_policy=_NO_WORKFLOW_RETRIES,
    )


# Backoff bounds for `wait_for_result`. Each poll is one DescribeWorkflowExecution.
_RESULT_POLL_INITIAL_SECONDS = 0.5
_RESULT_POLL_MAX_SECONDS = 5.0


async def wait_for_result(handle: WorkflowHandle[Any, Any]) -> Any:
    """Return a workflow's result by polling its status, not by holding a long poll.

    `handle.result()` blocks on a history long poll that stays open until the run
    closes. Through the orchestrator's public gateway, which bounds request duration,
    that fails for any run longer than the gateway timeout. Short describe calls do
    not, and once the run is closed `result()` answers immediately.
    """
    delay = _RESULT_POLL_INITIAL_SECONDS
    # `describe()` follows the workflow id to its latest run, so a continue-as-new
    # chain keeps polling until the final run closes.
    while (await handle.describe()).status == WorkflowExecutionStatus.RUNNING:
        await asyncio.sleep(delay)
        delay = min(delay * 2, _RESULT_POLL_MAX_SECONDS)
    return await handle.result()
