"""Direct state sink transport projection helpers."""

from pydantic import BaseModel, Field

from mistralai.vibe.sdk.execution_record.patching.produce import diff
from mistralai.vibe.sdk.execution_record.patching.types import Op
from mistralai.vibe.sdk.execution_record.state import TaskState


class FixedHistoryScope(BaseModel):
    """Stream ownership for one existing top-level history entry."""

    index: int = Field(ge=0)


class AppendHistoryScope(BaseModel):
    """Stream ownership for history entries appended after ``start_index``."""

    start_index: int = Field(ge=0)


HistoryScope = FixedHistoryScope | AppendHistoryScope


def _project_history_patches(
    previous: TaskState,
    new_state: TaskState,
    scope: HistoryScope | None,
) -> list[Op]:
    if scope is None:
        return diff(previous.history, new_state.history, "/history")

    if isinstance(scope, FixedHistoryScope):
        index = scope.index
        if index >= len(previous.history) or index >= len(new_state.history):
            msg = f"Fixed stream scope /history/{index} is outside the available history"
            raise ValueError(msg)
        return diff(previous.history[index], new_state.history[index], f"/history/{index}")

    start_index = scope.start_index
    if start_index > len(previous.history) or start_index > len(new_state.history):
        msg = f"Append stream scope starts outside the available history: {start_index}"
        raise ValueError(msg)
    return diff(
        previous.history[start_index:],
        new_state.history[start_index:],
        "/history",
        output_index_offset=start_index,
    )


__all__ = [
    "AppendHistoryScope",
    "FixedHistoryScope",
    "HistoryScope",
    "_project_history_patches",
]
