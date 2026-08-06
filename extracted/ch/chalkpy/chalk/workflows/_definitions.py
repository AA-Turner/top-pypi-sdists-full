from __future__ import annotations

import contextvars
import inspect
from datetime import timedelta
from typing import Any, Callable, Coroutine, Generic, Mapping, Sequence, TypeVar, cast, overload

from typing_extensions import ParamSpec

from chalk.utils.duration import Duration, parse_chalk_duration
from chalk.workflows._context import LocalOrchestrator, TaskHandle, current_orchestrator, current_orchestrator_var

P = ParamSpec("P")
R = TypeVar("R")

_DEFAULT_TASK_TIMEOUT = timedelta(minutes=10)


class TaskDefinition(Generic[P, R]):
    """A unit of work executed by a workflow.

    Calling a task always returns an awaitable of its result. Inside a running
    workflow, the call is routed through the workflow's orchestration backend
    (durable, retried, executed on a worker); outside a workflow, the underlying
    function is invoked in-process. Use `.fn` to call the raw function directly.
    """

    def __init__(
        self,
        fn: Callable[P, Any],
        *,
        name: str,
        retries: int,
        retry_delay: timedelta | None,
        timeout: timedelta,
        description: str | None,
    ):
        super().__init__()
        self.fn = fn
        self.name = name
        self.retries = retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.description = description
        self.is_async = inspect.iscoroutinefunction(fn)
        self.filename = fn.__code__.co_filename
        self.qualname = fn.__qualname__

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Coroutine[Any, Any, R]:
        orchestrator = current_orchestrator()
        if orchestrator is None:
            return self._call_plain(args, kwargs)
        return self._await_handle(orchestrator.run_task(self, args, kwargs))

    def submit(self, *args: P.args, **kwargs: P.kwargs) -> TaskHandle[R]:
        """Start the task without waiting for its result, for parallel execution
        inside a workflow. Await the returned handle (e.g. with `asyncio.gather`)
        to collect the result."""
        orchestrator = current_orchestrator()
        if orchestrator is None:
            raise RuntimeError(
                f"Task '{self.name}': .submit() may only be used inside a @workflow function. "
                + "Outside a workflow, call the task directly."
            )
        return orchestrator.submit_task(self, args, kwargs)

    async def _call_plain(self, args: Sequence[Any], kwargs: Mapping[str, Any]) -> R:
        fn = cast("Callable[..., Any]", self.fn)
        if self.is_async:
            return await fn(*args, **kwargs)
        return fn(*args, **kwargs)

    @staticmethod
    async def _await_handle(awaitable: Any) -> R:
        return await awaitable

    def __repr__(self) -> str:
        return f"chalk.workflows.task(name={self.name!r})"


class WorkflowDefinition(Generic[P, R]):
    """A durable workflow: orchestration code that invokes tasks.

    Calling a workflow definition directly runs it locally in-process (tasks
    execute locally too), which is useful for tests:

    >>> result = asyncio.run(my_workflow(x=1))  # doctest: +SKIP

    To run against a Chalk data plane, see `ChalkClient.trigger_workflow` (execute
    on deployed workers) and `ChalkClient.run_workflow` (execute this local
    definition with remote coordination).
    """

    def __init__(
        self,
        fn: Callable[P, Coroutine[Any, Any, R]],
        *,
        name: str,
        description: str | None,
        owner: str | None,
    ):
        super().__init__()
        self.fn = fn
        self.name = name
        self.description = description
        self.owner = owner
        self.filename = fn.__code__.co_filename
        self.qualname = fn.__qualname__

    async def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        if current_orchestrator() is not None:
            # Calling one workflow from another: run it inline in the caller's
            # orchestration context, so its tasks remain durable task invocations.
            return await self.fn(*args, **kwargs)
        token: contextvars.Token[Any] = current_orchestrator_var.set(LocalOrchestrator())
        try:
            return await self.fn(*args, **kwargs)
        finally:
            current_orchestrator_var.reset(token)

    def __repr__(self) -> str:
        return f"chalk.workflows.workflow(name={self.name!r})"


WORKFLOW_REGISTRY: dict[str, WorkflowDefinition[Any, Any]] = {}
TASK_REGISTRY: dict[str, TaskDefinition[Any, Any]] = {}


def _register(registry: dict[str, Any], entry: Any, kind: str) -> None:
    existing = registry.get(entry.name)
    if existing is not None and (existing.qualname, existing.filename) != (entry.qualname, entry.filename):
        raise ValueError(
            f"Duplicate {kind} name '{entry.name}': defined at {existing.filename} ({existing.qualname}) "
            + f"and {entry.filename} ({entry.qualname}). Pass name=... to disambiguate."
        )
    registry[entry.name] = entry


@overload
def task(fn: Callable[P, Coroutine[Any, Any, R]], /) -> TaskDefinition[P, R]: ...


@overload
def task(fn: Callable[P, R], /) -> TaskDefinition[P, R]: ...


@overload
def task(
    *,
    name: str | None = None,
    retries: int = 0,
    retry_delay: Duration | None = None,
    timeout: Duration | None = None,
    description: str | None = None,
) -> Callable[[Callable[P, Any]], TaskDefinition[P, Any]]: ...


def task(
    fn: Callable[..., Any] | None = None,
    /,
    *,
    name: str | None = None,
    retries: int = 0,
    retry_delay: Duration | None = None,
    timeout: Duration | None = None,
    description: str | None = None,
) -> Any:
    """Mark a function as a workflow task.

    Tasks are the retriable, durable units of work invoked by `@workflow`
    functions. A task function may be sync or async. Calling a task returns an
    awaitable of its result; inside a workflow the invocation is executed on a
    workflow worker with the configured retry policy.

    Parameters
    ----------
    name
        Unique name for the task. Defaults to the function name.
    retries
        Number of retries after the first failed attempt.
    retry_delay
        Delay between attempts, as a Chalk duration (e.g. `"30s"`) or `timedelta`.
    timeout
        Maximum duration of a single attempt. Defaults to 10 minutes.
    description
        Human-readable description; defaults to the function's docstring.

    Examples
    --------
    >>> from chalk.workflows import task
    >>> @task(retries=3, retry_delay="30s")
    ... def score_user(user_id: str) -> float:
    ...     return 0.5
    """

    def decorator(f: Callable[..., Any]) -> TaskDefinition[Any, Any]:
        definition = TaskDefinition(
            f,
            name=name or f.__name__,
            retries=retries,
            retry_delay=parse_chalk_duration(retry_delay) if retry_delay is not None else None,
            timeout=parse_chalk_duration(timeout) if timeout is not None else _DEFAULT_TASK_TIMEOUT,
            description=description if description is not None else inspect.getdoc(f),
        )
        _register(TASK_REGISTRY, definition, kind="task")
        return definition

    if fn is not None:
        return decorator(fn)
    return decorator


@overload
def workflow(fn: Callable[P, Coroutine[Any, Any, R]], /) -> WorkflowDefinition[P, R]: ...


@overload
def workflow(
    *,
    name: str | None = None,
    description: str | None = None,
    owner: str | None = None,
) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], WorkflowDefinition[P, R]]: ...


def workflow(
    fn: Callable[..., Coroutine[Any, Any, Any]] | None = None,
    /,
    *,
    name: str | None = None,
    description: str | None = None,
    owner: str | None = None,
) -> Any:
    """Mark an async function as a durable workflow.

    The decorated function contains orchestration logic only: it calls `@task`
    functions (awaiting their results) and composes their outputs. When executed
    against a Chalk data plane, the workflow's progress is durably coordinated by
    the environment's workflow orchestrator, and each task invocation runs on a
    workflow worker with the task's retry policy.

    Workflow functions must be `async def`, must be deterministic (no I/O,
    randomness, or wall-clock reads — put those in tasks), and their parameters
    and return values must be JSON-serializable.

    Parameters
    ----------
    name
        Unique name for the workflow. Defaults to the function name.
    description
        Human-readable description; defaults to the function's docstring.
    owner
        Owner of the workflow, e.g. an email address.

    Examples
    --------
    >>> from chalk.workflows import task, workflow
    >>> @task
    ... def fetch_users(segment: str) -> list[str]:
    ...     return ["u1", "u2"]
    >>> @workflow
    ... async def nightly_scoring(segment: str) -> int:
    ...     users = await fetch_users(segment)
    ...     return len(users)
    """

    def decorator(f: Callable[..., Coroutine[Any, Any, Any]]) -> WorkflowDefinition[Any, Any]:
        if not inspect.iscoroutinefunction(f):
            raise TypeError(
                f"@workflow function '{f.__qualname__}' must be 'async def': workflows await their tasks. "
                + "Blocking or CPU-bound work belongs in @task functions, which may be sync."
            )
        definition = WorkflowDefinition(
            f,
            name=name or f.__name__,
            description=description if description is not None else inspect.getdoc(f),
            owner=owner,
        )
        _register(WORKFLOW_REGISTRY, definition, kind="workflow")
        return definition

    if fn is not None:
        return decorator(fn)
    return decorator
