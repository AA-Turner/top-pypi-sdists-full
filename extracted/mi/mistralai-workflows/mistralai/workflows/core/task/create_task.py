from typing import Any, cast, overload

from pydantic import BaseModel

from mistralai.workflows.core.task.protocol import StatefulTaskProtocol, StatelessTaskProtocol
from mistralai.workflows.core.task.task import Task


def _infer_task_type_from_state(state: Any) -> str | None:
    """Attempt to infer task type from state object."""
    if isinstance(state, BaseModel):
        # Use model_config.title if available
        title = state.model_config.get("title")
        if title:
            return title
        return type(state).__name__

    if hasattr(state, "__dataclass_fields__"):
        # Dataclass: use class name
        return type(state).__name__

    if isinstance(state, dict):
        # Cannot infer type from dict
        return None

    # For other typed objects, use class name
    if hasattr(state, "__class__") and not isinstance(state, (str, int, float, bool, list, tuple, set)):
        return type(state).__name__

    return None


@overload
def task(type: str, *, id: str | None = None) -> StatelessTaskProtocol: ...


@overload
def task[T](type: str, state: T, *, id: str | None = None) -> StatefulTaskProtocol[T]: ...


def task[T](
    type: str, state: T | None = None, *, id: str | None = None
) -> StatelessTaskProtocol | StatefulTaskProtocol[T]:
    """
    Create an observable task that emits lifecycle events.

    Tasks track bounded operations (LLM streaming, file processing, agent traces) with
    clear start/end boundaries for UI and observability.

    Args:
        type: Task type identifier.
        state: Initial state. When provided, enables `set_state()` and `update_state()` methods.
        id: Optional explicit task ID. If not provided, a UUID is generated automatically.

    Returns:
        StatefulTaskProtocol: When state is provided - includes state management methods.
        StatelessTaskProtocol: When state is omitted - lifecycle events only.

    Examples:
        Stateless (lifecycle events only):
        >>> with task("cleanup"):
        ...     do_cleanup()

        Stateful with dict:
        >>> with task("export", state={"progress": 0}) as t:
        ...     t.update_state({"progress": 50})  # Partial update
        ...     t.set_state({"progress": 100})    # Full replacement

        Stateful with Pydantic model:
        >>> class ExportState(BaseModel):
        ...     progress: int = 0
        ...     status: str = "pending"

        >>> with task("export", state=ExportState()) as t:
        ...     t.update_state({"progress": 50, "status": "processing"})
        ...     t.set_state(ExportState(progress=100, status="done"))

        With explicit task ID:
        >>> task_id = str(uuid.uuid4())
        >>> with task("wait_for_input", state=state, id=task_id) as t:
        ...     # Task will use the provided id instead of generating one
        ...     pass
    """
    return Task[T](type=type, state=state, id=id)


def task_from[T](state: T, type: str | None = None, *, id: str | None = None) -> StatefulTaskProtocol[T]:
    """
    Create a stateful task, inferring type from state when not provided.

    Args:
        state: Initial state (required). Type is inferred from Pydantic models or dataclasses.
        type: Explicit task type. If None, inferred from state.
        id: Optional explicit task ID. If not provided, a UUID is generated automatically.

    Returns:
        StatefulTaskProtocol: Task with state management methods (`set_state()`, `update_state()`).

    Raises:
        ValueError: If type cannot be inferred (e.g., dict or primitive state without explicit type).

    Examples:
        >>> class ProcessingState(BaseModel):
        ...     model_config = ConfigDict(title="document_processing")
        ...     progress: float = 0.0

        >>> with task_from(ProcessingState()) as t:  # type="document_processing"
        ...     t.update_state({"progress": 0.5})

        >>> with task_from({"progress": 0}, type="export") as t:  # Explicit type required for dict
        ...     t.update_state({"progress": 100})

        >>> with task_from(ProcessingState(), id="custom-id") as t:
        ...     t.update_state({"progress": 0.5})
    """
    if type is None:
        inferred = _infer_task_type_from_state(state)
        if not inferred:
            raise ValueError(
                "Could not infer task type from state (e.g. dict or primitive). Please pass an explicit type argument."
            )
        type = inferred

    return cast(StatefulTaskProtocol[T], Task[T](type=type, state=state, id=id))


__all__ = ["task", "task_from", "_infer_task_type_from_state"]
