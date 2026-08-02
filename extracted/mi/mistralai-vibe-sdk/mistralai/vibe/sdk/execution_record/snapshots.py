"""Typed compact state snapshots recorded in task history.

A snapshot is a task-owned ``StateEntry`` whose ``payload.type`` is a
namespaced discriminator (e.g. ``"builtin.todo"``) and whose
``payload.content`` is the JSON state to carry. Because a
completed child task's ``TaskState`` is embedded in its parent's
``TaskResultEntry``, a snapshot written into a child's history is durable.
"""

from copy import deepcopy
from typing import Any

from mistralai.vibe.sdk.execution_record.state import (
    JsonValue,
    StateEntry,
    StateEntryPayload,
    TaskResultEntry,
    TaskState,
)
from mistralai.vibe.sdk.execution_record.types import GenerationStatus

__all__ = [
    "make_snapshot_entry",
    "latest_snapshot_index",
    "latest_snapshot_entry",
    "latest_snapshot",
    "latest_child_snapshot_entry",
    "seed_child_state",
]


def make_snapshot_entry(
    snapshot_type: str,
    content: JsonValue,
    *,
    generation_status: GenerationStatus = "complete",
    annotations: dict[str, Any] | None = None,
) -> StateEntry:
    """Build a snapshot ``StateEntry`` of the given type."""
    return StateEntry(
        payload=StateEntryPayload(type=snapshot_type, content=content),
        generation_status=generation_status,
        annotations=annotations,
    )


def latest_snapshot_index(state: TaskState, snapshot_type: str) -> int | None:
    """Return the index of the newest ``StateEntry`` of ``snapshot_type``, or ``None``."""
    for index in range(len(state.history) - 1, -1, -1):
        entry = state.history[index]
        if isinstance(entry, StateEntry) and entry.payload.type == snapshot_type:
            return index


def latest_snapshot_entry(state: TaskState, snapshot_type: str) -> StateEntry | None:
    """Return the newest ``StateEntry`` in ``state.history`` of ``snapshot_type``."""
    index = latest_snapshot_index(state, snapshot_type)
    if index is None:
        return None

    entry = state.history[index]
    if isinstance(entry, StateEntry):
        return entry


def latest_snapshot(state: TaskState, snapshot_type: str) -> JsonValue | None:
    """Return the content of the newest snapshot of ``snapshot_type``, or ``None``."""
    entry = latest_snapshot_entry(state, snapshot_type)
    if not entry:
        return None

    return entry.payload.content


def latest_child_snapshot_entry(
    parent: TaskState,
    *,
    task_name: str,
    snapshot_type: str,
) -> StateEntry | None:
    """Find the latest completed child snapshot for a given task name and type."""
    for entry in reversed(parent.history):
        if not isinstance(entry, TaskResultEntry):
            continue
        if entry.generation_status != "complete" or entry.payload.name != task_name:
            continue

        child = entry.payload.state
        if child is None or child.output.status != "completed":
            continue

        snapshot = latest_snapshot_entry(child, snapshot_type)
        if snapshot:
            return snapshot


def seed_child_state(
    child_state: TaskState,
    parent: TaskState,
    *,
    task_name: str,
    snapshot_type: str,
) -> TaskState:
    """Seed a fresh child ``TaskState`` with the latest matching snapshot."""
    snapshot = latest_child_snapshot_entry(parent, task_name=task_name, snapshot_type=snapshot_type)
    if not snapshot:
        return child_state

    return child_state.model_copy(
        update={"history": [make_snapshot_entry(snapshot_type, deepcopy(snapshot.payload.content))]}
    )
