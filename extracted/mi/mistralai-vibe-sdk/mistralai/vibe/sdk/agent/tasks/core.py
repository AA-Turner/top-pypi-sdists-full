"""Task contract used by agentic work."""

from typing import Any, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, Field

from mistralai.vibe.sdk.execution_record.state import TaskState
from mistralai.vibe.sdk.transports.channel import Channel


class Card(BaseModel):
    """Serializable metadata shared by tasks and callbacks."""

    name: str
    description: str = ""
    input_schema: dict[str, Any] | None = None
    output_schema: dict[str, Any] | None = None
    callbacks: list["TaskCallback"] = Field(default_factory=list)


class TaskCallback(BaseModel):
    """Declaration of a callback that a task expects its parent to handle."""

    type: Literal["task_callback"] = "task_callback"
    card: Card


@runtime_checkable
class Task(Protocol):
    """Protocol for a task."""

    @property
    def card(self) -> Card: ...

    async def run(self, state: TaskState) -> Channel: ...


@runtime_checkable
class StatefulTask(Protocol):
    """Protocol for a task that owns a state and snapshots it to the parent."""

    @property
    def snapshot_type(self) -> str: ...


Card.model_rebuild()
TaskCallback.model_rebuild()

__all__ = ["Card", "StatefulTask", "Task", "TaskCallback"]
