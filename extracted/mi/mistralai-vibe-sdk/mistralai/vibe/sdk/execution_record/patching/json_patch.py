"""Apply JSON Patch (RFC 6902) operations to TaskState models.

Provides apply_patches() which takes a TaskState and a list of Op objects
and returns a new TaskState with the operations applied. Handles the
common patch paths:

- /output — replace the task output
- /history/- — append a new entry to the history list
- /history/N — insert at index N, or append when N == len(history)
- /history/N/... — update a nested field on an existing history entry
  (recursive descent through payload, sub-models, and list elements)

Values in AddOp and ReplaceOp are deserialized back into typed Pydantic
models (HistoryEntry, TaskOutput) using Pydantic's TypeAdapter.

This module is a general-purpose utility — it knows about TaskState
structure but is not specific to any particular task pattern (agent,
tool, orchestrator, etc.).
"""

from collections.abc import Sequence
from typing import Any

from mistralai.vibe.sdk.execution_record.patching.types import AddOp, AppendOp, Op, ReplaceOp
from mistralai.vibe.sdk.execution_record.pointers import (
    join_segments,
    prepend_pointer,
    split_pointer,
)
from mistralai.vibe.sdk.execution_record.state import (
    CompletedOutput,
    FailedOutput,
    PendingOutput,
    TaskState,
    content_blocks,
    content_text,
)


def _normalize_ops(patches: Sequence[Op] | list[Op | list[Op]]) -> list[Op]:
    """Flatten a list of Ops or Op batches into a flat list of Ops."""
    result: list[Op] = []
    for item in patches:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result


def apply_patches(state: TaskState, patches: Sequence[Op] | list[Op | list[Op]]) -> TaskState:
    """Apply a list of patch operations to a TaskState.

    Each element in patches may be a single Op or a list of Ops (a batch).
    Returns a new TaskState with all operations applied. The original
    state is never modified.

    Args:
        state: The TaskState to apply patches to.
        patches: List of Op objects (or batches). Supported ops:
            AddOp, ReplaceOp, AppendOp.
    """
    current = state
    for op in _normalize_ops(patches):
        current = _apply_single_op(current, op)
    return current


def reroute_patches(patches: Sequence[Op] | list[Op | list[Op]], prefix: str) -> list[Op]:
    """Re-root patch paths by prepending a prefix.

    Takes a list of patch operations (possibly batches) and returns a flat
    list of Op objects with the prefix prepended to each path.

    Example: ReplaceOp(path="/output", value=X) with prefix
    "/history/3/payload/state" becomes
    ReplaceOp(path="/history/3/payload/state/output", value=X).

    Args:
        patches: List of Op objects (or batches) to reroute.
        prefix: JSON Pointer path prefix to prepend to each op's path.
    """
    return [
        op.model_copy(update={"path": prepend_pointer(prefix, op.path)})
        for op in _normalize_ops(patches)
    ]


def _apply_single_op(state: TaskState, op: Op) -> TaskState:
    """Apply a single Op to a TaskState, returning a new TaskState."""
    path: str = op.path
    parts = split_pointer(path)

    if not parts:
        return state

    # /output
    if parts[0] == "output" and len(parts) == 1 and isinstance(op, ReplaceOp):
        output = _deserialize_output(op.value)
        return state.model_copy(update={"output": output})

    # /history/- (append to top-level history)
    if parts == ["history", "-"] and isinstance(op, AddOp):
        entry = _deserialize_history_entry(op.value)
        return state.model_copy(update={"history": [*state.history, entry]})

    # /history/N (insert/append) or /history/N/... (update nested entry field)
    if parts[0] == "history" and len(parts) >= 2 and parts[1].isdigit():
        idx = int(parts[1])
        if len(parts) == 2 and isinstance(op, AddOp) and idx <= len(state.history):
            entry = _deserialize_history_entry(op.value)
            new_history = list(state.history)
            new_history.insert(idx, entry)
            return state.model_copy(update={"history": new_history})
        if idx < len(state.history):
            entry = state.history[idx]
            sub_path = join_segments(parts[2:]) if len(parts) > 2 else ""
            new_entry = _apply_op_to_entry(entry, sub_path, op)
            new_history = list(state.history)
            new_history[idx] = new_entry
            return state.model_copy(update={"history": new_history})

    # Fallback: return unchanged
    return state


def _deserialize_output(value: Any) -> Any:
    """Deserialize a TaskOutput from a dict."""
    if isinstance(value, dict):
        status = value.get("status")
        if status == "completed":
            return CompletedOutput.model_validate(value)
        if status == "failed":
            return FailedOutput(error=value.get("error", ""))
        if status in {"pending", "running"}:
            return PendingOutput()
    return value


def _deserialize_history_entry(value: Any) -> Any:
    """Deserialize a HistoryEntry from a dict."""
    from mistralai.vibe.sdk.execution_record.state import HistoryEntry

    if isinstance(value, dict):
        from pydantic import TypeAdapter

        adapter: TypeAdapter[HistoryEntry] = TypeAdapter(HistoryEntry)
        return adapter.validate_python(value)
    return value


def _deserialize_content_block(value: Any) -> Any:
    """Deserialize a ContentBlock from a dict."""
    from mistralai.vibe.sdk.execution_record.state import ContentBlock

    if isinstance(value, dict):
        from pydantic import TypeAdapter

        adapter: TypeAdapter[ContentBlock] = TypeAdapter(ContentBlock)
        return adapter.validate_python(value)
    return value


def _apply_op_to_entry(entry: Any, sub_path: str, op: Op) -> Any:
    """Apply an op to a nested field of a history entry."""
    if not sub_path or sub_path == "/":
        if isinstance(op, ReplaceOp):
            return _deserialize_history_entry(op.value)
        return entry

    parts = split_pointer(sub_path)

    # Single level like /generation_status or /payload
    if len(parts) == 1:
        field_name = parts[0]
        if isinstance(op, ReplaceOp):
            return entry.model_copy(update={field_name: op.value})
        if isinstance(op, AppendOp):
            old_val = getattr(entry, field_name, "")
            return entry.model_copy(update={field_name: old_val + op.value})

    # Deeper paths: /payload/content, /payload/role, etc.
    if len(parts) >= 2 and parts[0] == "payload":
        payload = entry.payload
        remaining = join_segments(parts[1:])
        new_payload = _apply_op_to_model(payload, remaining, op)
        return entry.model_copy(update={"payload": new_payload})

    return entry


def _apply_op_to_model(model: Any, path: str, op: Op) -> Any:
    """Apply an op to a Pydantic model at a given sub-path (recursive)."""
    parts = split_pointer(path)
    if not parts:
        return model

    field_name = parts[0]

    if len(parts) == 1:
        if isinstance(op, ReplaceOp):
            value = op.value
            # Deserialize known nested types
            if field_name == "output" and isinstance(value, dict):
                value = _deserialize_output(value)
            if field_name == "content":
                if value is None or isinstance(value, str):
                    value = content_blocks(value)
                elif isinstance(value, list):
                    value = [_deserialize_content_block(item) for item in value]
            return model.model_copy(update={field_name: value})
        if isinstance(op, AppendOp):
            old_val = getattr(model, field_name, "")
            if field_name == "content":
                new_value = content_blocks(content_text(old_val) + str(op.value))
                return model.model_copy(update={field_name: new_value})
            return model.model_copy(update={field_name: old_val + op.value})
        return model

    # /field/- (append to list field)
    if len(parts) == 2 and parts[1] == "-" and isinstance(op, AddOp):
        old_list = getattr(model, field_name, [])
        value = op.value
        if field_name == "history":
            value = _deserialize_history_entry(value)
        if field_name == "content":
            value = _deserialize_content_block(value)
        return model.model_copy(update={field_name: [*old_list, value]})

    # Recurse into nested model
    child = getattr(model, field_name, None)
    if child is not None and hasattr(child, "model_copy"):
        remaining = join_segments(parts[1:])
        new_child = _apply_op_to_model(child, remaining, op)
        return model.model_copy(update={field_name: new_child})

    # /field/N (insert/append) or /field/N/... (descend into list element by index)
    if isinstance(child, list) and len(parts) >= 2 and parts[1].isdigit():
        idx = int(parts[1])
        if not parts[2:] and isinstance(op, AddOp) and idx <= len(child):
            value = op.value
            if field_name == "history":
                value = _deserialize_history_entry(value)
            if field_name == "content":
                value = _deserialize_content_block(value)
            new_list = list(child)
            new_list.insert(idx, value)
            return model.model_copy(update={field_name: new_list})
        if idx < len(child):
            element = child[idx]
            remaining = join_segments(parts[2:]) if len(parts) > 2 else ""
            if remaining and hasattr(element, "model_copy"):
                new_element = _apply_op_to_model(element, remaining, op)
            elif isinstance(op, ReplaceOp) and not remaining:
                new_element = op.value
                if field_name == "history":
                    new_element = _deserialize_history_entry(new_element)
                if field_name == "content":
                    new_element = _deserialize_content_block(new_element)
            else:
                return model
            new_list = list(child)
            new_list[idx] = new_element
            return model.model_copy(update={field_name: new_list})

    return model


__all__ = ["apply_patches", "reroute_patches"]
