from __future__ import annotations

import asyncio
import contextvars
from typing import TYPE_CHECKING, Any, Awaitable, Generator, Generic, Mapping, Protocol, Sequence, TypeVar

if TYPE_CHECKING:
    from chalk.workflows._definitions import TaskDefinition

R = TypeVar("R")


class TaskHandle(Generic[R]):
    """A handle to a task submitted with `task.submit(...)` inside a workflow.

    Await the handle to obtain the task's result:

    >>> handle = my_task.submit(1)  # doctest: +SKIP
    >>> result = await handle  # doctest: +SKIP
    """

    def __init__(self, awaitable: Awaitable[R]):
        super().__init__()
        self._awaitable = awaitable

    def __await__(self) -> Generator[Any, None, R]:
        return self._awaitable.__await__()


class WorkflowOrchestrator(Protocol):
    """Backend that executes task invocations made inside a running workflow.

    Implementations: `LocalOrchestrator` (in-process asyncio) and the Temporal-backed
    orchestrator in `chalk.workflows._temporal`. User code never sees this type.
    """

    def run_task(
        self,
        task: TaskDefinition[Any, Any],
        args: Sequence[Any],
        kwargs: Mapping[str, Any],
    ) -> Awaitable[Any]: ...

    def submit_task(
        self,
        task: TaskDefinition[Any, Any],
        args: Sequence[Any],
        kwargs: Mapping[str, Any],
    ) -> TaskHandle[Any]: ...


current_orchestrator_var: contextvars.ContextVar[WorkflowOrchestrator | None] = contextvars.ContextVar(
    "chalk_workflow_orchestrator", default=None
)


def current_orchestrator() -> WorkflowOrchestrator | None:
    return current_orchestrator_var.get()


class LocalOrchestrator:
    """Executes tasks in-process. Used when a workflow function is invoked directly
    (local runs and unit tests) rather than under a durable execution backend."""

    async def _execute(
        self,
        task: TaskDefinition[Any, Any],
        args: Sequence[Any],
        kwargs: Mapping[str, Any],
    ) -> Any:
        attempts = task.retries + 1
        last_error: BaseException | None = None
        for attempt in range(attempts):
            try:
                if task.is_async:
                    return await task.fn(*args, **kwargs)
                # Sync tasks run in a thread so local workflows can still make progress
                # on other submitted tasks, mirroring how sync tasks execute in a
                # worker thread pool under a durable backend.
                return await asyncio.to_thread(task.fn, *args, **kwargs)
            except Exception as e:  # noqa: PERF203
                last_error = e
                if attempt + 1 < attempts and task.retry_delay is not None:
                    await asyncio.sleep(task.retry_delay.total_seconds())
        assert last_error is not None
        raise last_error

    def run_task(
        self,
        task: TaskDefinition[Any, Any],
        args: Sequence[Any],
        kwargs: Mapping[str, Any],
    ) -> Awaitable[Any]:
        return self._execute(task, args, kwargs)

    def submit_task(
        self,
        task: TaskDefinition[Any, Any],
        args: Sequence[Any],
        kwargs: Mapping[str, Any],
    ) -> TaskHandle[Any]:
        return TaskHandle(asyncio.ensure_future(self._execute(task, args, kwargs)))
