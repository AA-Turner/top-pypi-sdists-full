from __future__ import annotations

import contextvars
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from typing import Any, Awaitable, Callable, Iterable, Mapping, Sequence

from temporalio import activity as temporal_activity
from temporalio import workflow as temporal_workflow
from temporalio.client import Client, WorkflowHandle
from temporalio.common import RetryPolicy
from temporalio.worker import Worker

from chalk.workflows._context import TaskHandle, current_orchestrator_var
from chalk.workflows._definitions import TASK_REGISTRY, WORKFLOW_REGISTRY, TaskDefinition, WorkflowDefinition

DEFAULT_TASK_QUEUE = "chalk-workflows"

# Retries are configured on `@task` via Chalk's retry parameters; a workflow-level
# Temporal retry policy would silently re-run orchestration code on task failure.
_NO_WORKFLOW_RETRIES = RetryPolicy(maximum_attempts=1)


class _TemporalOrchestrator:
    """Routes task invocations made inside a compiled workflow to Temporal activities."""

    def _start(self, task: TaskDefinition[Any, Any], args: Sequence[Any], kwargs: Mapping[str, Any]) -> Any:
        return temporal_workflow.start_activity(
            task.name,
            args=[list(args), dict(kwargs)],
            start_to_close_timeout=task.timeout,
            retry_policy=RetryPolicy(
                maximum_attempts=task.retries + 1,
                initial_interval=task.retry_delay if task.retry_delay is not None else timedelta(seconds=1),
            ),
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

    # Temporal invokes workflows with positional payloads; the SDK convention here is
    # a single JSON object holding the workflow function's keyword arguments.
    async def run(self: Any, kwargs: dict[str, Any]) -> Any:
        token: contextvars.Token[Any] = current_orchestrator_var.set(_TemporalOrchestrator())
        try:
            return await definition.fn(**kwargs)
        finally:
            current_orchestrator_var.reset(token)

    # The class is assembled with type() and given a module-level-looking qualname:
    # temporalio rejects run methods whose qualname contains '<locals>'.
    class_name = f"ChalkWorkflow_{definition.name}"
    run.__qualname__ = f"{class_name}.run"
    run.__module__ = definition.fn.__module__
    cls = type(class_name, (), {"run": temporal_workflow.run(run)})
    cls.__module__ = definition.fn.__module__
    return temporal_workflow.defn(name=definition.name, sandboxed=False)(cls)


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
    directly without a token.
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
    max_concurrent_tasks: int = 16,
) -> Worker:
    """Create a Temporal worker hosting the given (default: all registered)
    Chalk workflows and tasks."""
    workflow_definitions = list(workflows) if workflows is not None else list(WORKFLOW_REGISTRY.values())
    task_definitions = list(tasks) if tasks is not None else list(TASK_REGISTRY.values())
    return Worker(
        client,
        task_queue=task_queue,
        workflows=[build_workflow_class(w) for w in workflow_definitions],
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
