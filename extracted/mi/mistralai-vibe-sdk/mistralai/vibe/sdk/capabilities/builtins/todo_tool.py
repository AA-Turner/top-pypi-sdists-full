"""Builtin todo tool for the Vibe SDK."""

from collections import Counter
from typing import Literal

from pydantic import BaseModel, Field

from mistralai.vibe.sdk.capabilities import tool
from mistralai.vibe.sdk.utils.types import NonEmptyStr

__all__ = [
    "TODO_SNAPSHOT_TYPE",
    "TodoStatus",
    "TodoItem",
    "TodoCounts",
    "TodoArgs",
    "TodoResult",
    "todo",
]

TODO_SNAPSHOT_TYPE = "builtin.todo"

TodoStatus = Literal["pending", "in_progress", "completed", "cancelled", "blocked"]

TODO_DESCRIPTION = (
    "Track and manage a task list for multi-step work. Call without 'todos' to "
    "read the current list; call with 'todos' to replace the entire list; call "
    "with an empty 'todos' list to clear it. The full list and status counts are "
    "always returned. List order is meaningful and represents execution "
    "priority; any number of items may be 'in_progress'.\n\n"
    "Use this for complex tasks, when the user explicitly asks for progress "
    "tracking, or when a request contains multiple actionable items. Do not use "
    "it for trivial one-step work or purely informational conversation.\n\n"
    "Mark an item 'in_progress' when starting it and 'completed' immediately "
    "after the work is actually finished. Use 'blocked' only when progress "
    "genuinely depends on missing input or an external condition. Keep item "
    "content stable and actionable."
)


class TodoItem(BaseModel):
    content: NonEmptyStr = Field(description="Non-empty, actionable task description.")
    status: TodoStatus = Field(description="Current execution status of the task.")


class TodoCounts(BaseModel):
    total: int
    pending: int
    in_progress: int
    completed: int
    cancelled: int
    blocked: int


class TodoArgs(BaseModel):
    todos: list[TodoItem] | None = Field(
        default=None,
        description=(
            "Optional full replacement list. Omit to read the current list. Pass "
            "an empty list to clear it."
        ),
    )


class TodoResult(BaseModel):
    todos: list[TodoItem]
    counts: TodoCounts


@tool(
    name="todo",
    description=TODO_DESCRIPTION,
    input_schema=TodoArgs,
    snapshot_type=TODO_SNAPSHOT_TYPE,
    snapshot_schema=TodoResult,
)
def todo(args: TodoArgs, state: TodoResult | None = None) -> TodoResult:
    if args.todos is not None:
        # Replace the full list.
        items = args.todos
    elif state is not None:
        # Rebuild the list from the latest persisted snapshot.
        items = state.todos
    else:
        # First read with no prior snapshot: an empty list.
        items = []

    by_status = Counter(item.status for item in items)

    return TodoResult(
        todos=items,
        counts=TodoCounts(
            total=len(items),
            pending=by_status["pending"],
            in_progress=by_status["in_progress"],
            completed=by_status["completed"],
            cancelled=by_status["cancelled"],
            blocked=by_status["blocked"],
        ),
    )
