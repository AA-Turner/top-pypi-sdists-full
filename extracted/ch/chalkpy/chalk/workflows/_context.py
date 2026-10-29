from __future__ import annotations

import asyncio
import contextvars
import uuid
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Generator, Generic, Mapping, Protocol, Sequence, TypeVar

if TYPE_CHECKING:
    from chalk.workflows._definitions import TaskDefinition, WorkflowDefinition
    from chalk.workflows._messages import WorkflowMessage

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


class ChildWorkflowHandle(Generic[R]):
    """A handle to a child workflow started with `chalk.workflows.start_child(...)`.

    Await the handle to obtain the child's result, and use `send_message` to message it:

    >>> child = await start_child(review_account, {"account_id": "acct-1"})  # doctest: +SKIP
    >>> await child.send_message("review", {"approved": True})  # doctest: +SKIP
    >>> result = await child  # doctest: +SKIP
    """

    def __init__(
        self,
        workflow_id: str,
        result: Awaitable[R],
        send_message: Callable[[str, Any], Awaitable[None]],
    ):
        super().__init__()
        self.workflow_id = workflow_id
        self._result = result
        self._send_message = send_message

    def __await__(self) -> Generator[Any, None, R]:
        return self._result.__await__()

    async def send_message(self, name: str, payload: Any) -> None:
        """Send the child a message, which it receives with `wait_for_message(name)`.
        Equivalent to `chalk.workflows.send_message(handle.workflow_id, name, payload)`."""
        await self._send_message(name, payload)


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

    def wait_for_message(self, name: str, timeout: timedelta | None) -> Awaitable[WorkflowMessage]: ...

    def start_child(
        self,
        workflow: WorkflowDefinition[Any, Any] | str,
        kwargs: Mapping[str, Any],
        workflow_id: str | None,
    ) -> Awaitable[ChildWorkflowHandle[Any]]: ...

    def send_message(self, workflow_id: str, name: str, payload: Any) -> Awaitable[None]: ...

    def current_workflow_id(self) -> str: ...

    def parent_workflow_id(self) -> str | None: ...


# Messages queued by `chalk.workflows.local_messages` for workflows run by a LocalOrchestrator.
local_messages_var: contextvars.ContextVar[list[WorkflowMessage] | None] = contextvars.ContextVar(
    "chalk_workflow_local_messages", default=None
)

current_orchestrator_var: contextvars.ContextVar[WorkflowOrchestrator | None] = contextvars.ContextVar(
    "chalk_workflow_orchestrator", default=None
)


def current_orchestrator() -> WorkflowOrchestrator | None:
    return current_orchestrator_var.get()


def local_workflow_id(name: str) -> str:
    return f"local-{name}-{uuid.uuid4().hex[:12]}"


class LocalOrchestrator:
    """Executes tasks in-process. Used when a workflow function is invoked directly
    (local runs and unit tests) rather than under a durable execution backend."""

    def __init__(self, workflow_id: str, parent_workflow_id: str | None = None):
        super().__init__()
        self.workflow_id = workflow_id
        self._parent_workflow_id = parent_workflow_id
        # This invocation's running children, by id; a child leaves when it finishes.
        self._children: dict[str, asyncio.Future[Any]] = {}

    def current_workflow_id(self) -> str:
        return self.workflow_id

    def parent_workflow_id(self) -> str | None:
        return self._parent_workflow_id

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

    async def wait_for_message(self, name: str, timeout: timedelta | None) -> WorkflowMessage:
        # A direct local run has no address anyone could send to, so it only sees messages
        # queued in advance; waiting would hang forever.
        queued = local_messages_var.get()
        if queued is not None:
            for i, message in enumerate(queued):
                if message.name == name:
                    return queued.pop(i)
        raise RuntimeError(
            f"No local message named {name!r}. A workflow run directly in this process only receives "
            + "messages queued with chalk.workflows.local_messages(...); run it on the workflow orchestrator "
            + "(ChalkClient.trigger_workflow or run_workflow) to receive messages sent to it."
        )

    async def start_child(
        self,
        workflow: WorkflowDefinition[Any, Any] | str,
        kwargs: Mapping[str, Any],
        workflow_id: str | None,
    ) -> ChildWorkflowHandle[Any]:
        if isinstance(workflow, str):
            from chalk.workflows._definitions import WORKFLOW_REGISTRY

            definition = WORKFLOW_REGISTRY.get(workflow)
            if definition is None:
                raise ValueError(f"No workflow named {workflow!r} is defined in this process")
        else:
            definition = workflow

        child_id = workflow_id if workflow_id is not None else local_workflow_id(definition.name)
        # The orchestrator refuses to start a workflow whose id is still running.
        if child_id in self._children:
            raise RuntimeError(f"Cannot start child workflow {child_id!r}: a child with that id is still running")

        async def run_child() -> Any:
            # The child runs in its own task (and so its own context): messages queued with
            # local_messages(...) are the parent's, not the child's.
            local_messages_var.set(None)
            orchestrator = LocalOrchestrator(child_id, parent_workflow_id=self.workflow_id)
            current_orchestrator_var.set(orchestrator)
            try:
                return await definition.fn(**kwargs)
            finally:
                await orchestrator.close()

        child = asyncio.ensure_future(run_child())
        self._children[child_id] = child
        child.add_done_callback(lambda _: self._children.pop(child_id, None))
        return ChildWorkflowHandle(
            child_id,
            child,
            lambda name, payload: self.send_message(child_id, name, payload),
        )

    async def close(self) -> None:
        """Cancel the children still running when this invocation exits, and wait for their
        `finally` blocks, as the orchestrator does for a child whose parent closes first."""
        children = list(self._children.values())
        for child in children:
            child.cancel()
        await asyncio.gather(*children, return_exceptions=True)

    async def send_message(self, workflow_id: str, name: str, payload: Any) -> None:
        raise RuntimeError(
            f"Cannot send message {name!r} to workflow {workflow_id!r}: a workflow run directly in this process "
            + "has no orchestrator to deliver messages between workflows. Run it on the workflow orchestrator "
            + "(ChalkClient.trigger_workflow or run_workflow) to message other workflows."
        )
