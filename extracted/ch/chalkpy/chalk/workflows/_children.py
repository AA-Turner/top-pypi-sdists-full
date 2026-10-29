from __future__ import annotations

import inspect
from typing import Any, Mapping, TypeVar, overload

from chalk.workflows._context import ChildWorkflowHandle, current_orchestrator
from chalk.workflows._definitions import WorkflowDefinition

R = TypeVar("R")


def current_workflow_id() -> str:
    """Return the id of the running workflow, from inside a `@workflow`.

    It is the id `ChalkClient.trigger_workflow` returned (or the child's id, in a workflow
    started with `start_child`), which other workflows can pass to `send_message`. A workflow
    run directly in this process gets a generated `local-...` id.
    """
    orchestrator = current_orchestrator()
    if orchestrator is None:
        raise RuntimeError("current_workflow_id can only be called inside a @workflow")
    return orchestrator.current_workflow_id()


def parent_workflow_id() -> str | None:
    """Return the id of the workflow that started this one with `start_child`, from inside a
    `@workflow`, or `None` if it was not started as a child.

    A child can use it to message its parent without waiting to hear from it first:

    >>> from chalk.workflows import current_workflow_id, parent_workflow_id, send_message, workflow
    >>> @workflow
    ... async def sub_agent() -> None:
    ...     parent_id = parent_workflow_id()
    ...     if parent_id is not None:
    ...         await send_message(parent_id, "ready", {"agent": current_workflow_id()})
    """
    orchestrator = current_orchestrator()
    if orchestrator is None:
        raise RuntimeError("parent_workflow_id can only be called inside a @workflow")
    return orchestrator.parent_workflow_id()


@overload
async def start_child(
    workflow: WorkflowDefinition[..., R], input: Mapping[str, Any] | None = None, *, workflow_id: str | None = None
) -> ChildWorkflowHandle[R]: ...


@overload
async def start_child(
    workflow: str, input: Mapping[str, Any] | None = None, *, workflow_id: str | None = None
) -> ChildWorkflowHandle[Any]: ...


async def start_child(
    workflow: WorkflowDefinition[..., Any] | str,
    input: Mapping[str, Any] | None = None,
    *,
    workflow_id: str | None = None,
) -> ChildWorkflowHandle[Any]:
    """Start another workflow as a child of the calling `@workflow`, and return a handle to it.

    The child runs as its own workflow, on the same workers as the parent, with its own
    history; await the handle for its result and use `handle.send_message(...)` to message
    it. The workflow lineage view shows it as a child of the calling workflow.

    A child's lifetime is bounded by its parent's: if the parent completes, fails or is
    cancelled while the child is still running, the child is cancelled. It receives the
    cancellation like any cancelled workflow, so its `finally` blocks still run (for example
    to release a sandbox). Await every child before returning from the parent.

    Like a workflow started with `ChalkClient.trigger_workflow`, the child is not retried as
    a whole; retries are configured per `@task`.

    Parameters
    ----------
    workflow
        The child `@workflow`, or the name of one served by this workflow's workers.
    input
        The child's keyword arguments, by name, as for `ChalkClient.trigger_workflow`. Must
        be JSON-serializable. `None` starts a child that takes no arguments.
    workflow_id
        The child's workflow id. Defaults to one derived from the parent's id and the child's
        name. Starting a child with the id of a workflow that is still running fails.

    Examples
    --------
    >>> from chalk.workflows import start_child, workflow
    >>> @workflow
    ... async def score_segment(segment: str) -> float:
    ...     return 0.5
    >>> @workflow
    ... async def score_all(segments: list[str]) -> list[float]:
    ...     children = [await start_child(score_segment, {"segment": s}) for s in segments]
    ...     return [await child for child in children]
    """
    orchestrator = current_orchestrator()
    if orchestrator is None:
        raise RuntimeError("start_child can only be called inside a @workflow")
    kwargs = dict(input) if input is not None else {}
    if isinstance(workflow, WorkflowDefinition):
        # Fail in the parent, where the mistake is, rather than in a child that cannot start.
        try:
            inspect.signature(workflow.fn).bind(**kwargs)
        except TypeError as e:
            raise TypeError(f"Invalid input for child workflow {workflow.name!r}: {e}") from None
    return await orchestrator.start_child(workflow, kwargs, workflow_id)
