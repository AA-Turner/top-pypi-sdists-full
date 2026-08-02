"""Immer-like produce() and diff() for Pydantic v2 models.

This module provides two complementary mutation-tracking mechanisms
that return typed Op objects (RFC 6902 JSON Patch operations) from
patch.py. These are the foundation for streaming state updates: the
dispatch loop uses them to compute patches that describe what changed
in the TaskState after each event.

produce(base, recipe) — recording mode
    Creates a draft proxy around a Pydantic BaseModel. The recipe
    function mutates the draft imperatively (attribute assignment,
    list append, etc.). During mutation, Op objects are recorded
    automatically. After the recipe returns, a new model is built
    with structural sharing via model_copy(update=...). The base
    object is never modified.

    Returns (new_model, list[Op]). The ops describe changes to
    base.model_dump(mode="json") — i.e., they target the JSON
    projection, not the Python object graph.

diff(old, new) — structural diff
    Computes patches that transform old into new. Uses Python
    reference equality (`is`) to skip unchanged subtrees, making
    it O(changed nodes) rather than O(total nodes). Detects string
    prefix growth and emits AppendOp for efficient token streaming.

    Returns list[Op].

    The optional output_index_offset is only valid when old/new are both lists.
    It lets callers diff sliced lists while preserving absolute indexes in
    emitted patch paths.

Draft proxies:
    ModelDraft — intercepts __getattr__/__setattr__ on Pydantic
    models. Reads return child drafts for nested models/lists/dicts.
    Writes stage updates and record patches. String append detection
    emits AppendOp instead of ReplaceOp when the new value extends
    the old value.

    ListDraft — copy-on-write list proxy. Supports append, extend,
    pop, insert, index assignment, iteration, and len.

    DictDraft — copy-on-write dict proxy.

@immer_reducer — decorator that bridges recipe_with_effects and
    reducers. A recipe_with_effects is the inner function that
    mutates a draft and returns effects. The decorator wraps it
    into a proper reducer that returns (new_state, patches, effects).
    See the immer_reducer docstring for details.

See also: documentation/rfc-python-immer.md for the original design
RFC with rationale and edge-case analysis.
"""

import functools
from collections.abc import Callable, Iterator
from typing import Any

from pydantic import BaseModel

from mistralai.vibe.sdk.execution_record.patching.types import (
    AddOp,
    AppendOp,
    Op,
    RemoveOp,
    ReplaceOp,
)
from mistralai.vibe.sdk.execution_record.pointers import append_segment

# ---------------------------------------------------------------------------
# Draft proxy classes
# ---------------------------------------------------------------------------


class _PatchRecorder:
    """Accumulates Op objects during a produce() recipe."""

    def __init__(self) -> None:
        self.ops: list[Op] = []

    def record(self, op: Op) -> None:
        self.ops.append(op)


def _serialize_value(value: Any) -> Any:
    """Serialize a value for use in patch ops (JSON projection)."""
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, list):
        return [_serialize_value(v) for v in value]
    if isinstance(value, dict):
        return {k: _serialize_value(v) for k, v in value.items()}
    return value


class ModelDraft:
    """Draft proxy for a Pydantic BaseModel.

    Intercepts attribute reads and writes. Reads return child drafts
    for draftable fields. Writes stage updates and record patches.
    String append detection emits AppendOp instead of ReplaceOp when
    the new value extends the old value.
    """

    def __init__(
        self,
        base: BaseModel,
        path: str,
        recorder: _PatchRecorder,
        parent: "ModelDraft | ListDraft | None" = None,
        parent_key: str | int | None = None,
    ) -> None:
        """Initialize a model draft proxy.

        Args:
            base: The original Pydantic model to proxy. Never modified.
            path: JSON Pointer path to this node (e.g., "" for root,
                "/history" for a nested field).
            recorder: Shared patch recorder that accumulates Op objects.
            parent: Parent draft (for dirty-flag propagation up the tree).
            parent_key: Key or index in the parent that points to this draft.
        """
        object.__setattr__(self, "_base", base)
        object.__setattr__(self, "_path", path)
        object.__setattr__(self, "_recorder", recorder)
        object.__setattr__(self, "_updates", {})
        object.__setattr__(self, "_child_drafts", {})
        object.__setattr__(self, "_dirty", False)
        object.__setattr__(self, "_parent", parent)
        object.__setattr__(self, "_parent_key", parent_key)

    def _mark_dirty(self) -> None:
        object.__setattr__(self, "_dirty", True)
        parent: ModelDraft | ListDraft | None = object.__getattribute__(self, "_parent")
        if parent is not None:
            parent._mark_dirty()

    def __getattr__(self, name: str) -> Any:
        updates: dict[str, Any] = object.__getattribute__(self, "_updates")
        if name in updates:
            val = updates[name]
            return self._maybe_wrap(name, val)

        base: BaseModel = object.__getattribute__(self, "_base")
        if not hasattr(base, name):
            raise AttributeError(f"'{type(base).__name__}' has no attribute '{name}'")

        child_drafts: dict[str, Any] = object.__getattribute__(self, "_child_drafts")
        if name in child_drafts:
            return child_drafts[name]

        val = getattr(base, name)
        return self._maybe_wrap(name, val)

    def _maybe_wrap(self, name: str, val: Any) -> Any:
        child_drafts: dict[str, Any] = object.__getattribute__(self, "_child_drafts")
        if name in child_drafts:
            return child_drafts[name]

        path: str = object.__getattribute__(self, "_path")
        recorder: _PatchRecorder = object.__getattribute__(self, "_recorder")
        child_path = append_segment(path, name)

        if isinstance(val, BaseModel):
            draft: Any = ModelDraft(val, child_path, recorder, parent=self, parent_key=name)
            child_drafts[name] = draft
            return draft
        if isinstance(val, list):
            draft = ListDraft(val, child_path, recorder, parent=self, parent_key=name)
            child_drafts[name] = draft
            return draft
        if isinstance(val, dict):
            draft = DictDraft(val, child_path, recorder, parent=self, parent_key=name)
            child_drafts[name] = draft
            return draft

        return val

    def __setattr__(self, name: str, value: Any) -> None:
        path: str = object.__getattribute__(self, "_path")
        recorder: _PatchRecorder = object.__getattribute__(self, "_recorder")
        updates: dict[str, Any] = object.__getattribute__(self, "_updates")
        base: BaseModel = object.__getattribute__(self, "_base")

        field_path = append_segment(path, name)

        # String append detection
        if isinstance(value, str):
            old_val = updates.get(name, getattr(base, name, None))
            if isinstance(old_val, str) and value.startswith(old_val) and len(value) > len(old_val):
                appended = value[len(old_val) :]
                recorder.record(AppendOp(path=field_path, value=appended))
                updates[name] = value
                self._mark_dirty()
                child_drafts: dict[str, Any] = object.__getattribute__(self, "_child_drafts")
                child_drafts.pop(name, None)
                return

        recorder.record(ReplaceOp(path=field_path, value=_serialize_value(value)))
        updates[name] = value
        self._mark_dirty()
        child_drafts = object.__getattribute__(self, "_child_drafts")
        child_drafts.pop(name, None)

    def _commit(self) -> BaseModel:
        """Build the new model with structural sharing."""
        base: BaseModel = object.__getattribute__(self, "_base")
        dirty: bool = object.__getattribute__(self, "_dirty")

        if not dirty:
            return base

        updates: dict[str, Any] = dict(object.__getattribute__(self, "_updates"))
        child_drafts: dict[str, Any] = object.__getattribute__(self, "_child_drafts")

        for name, child in child_drafts.items():
            if name not in updates:
                committed = child._commit()
                if committed is not getattr(base, name):
                    updates[name] = committed

        if not updates:
            return base

        return base.model_copy(update=updates)


class ListDraft:
    """Draft proxy for a list.

    Supports append, extend, pop, insert, index assignment, iteration,
    and len. Copy-on-write: the list is shallow-copied on first mutation.
    """

    def __init__(
        self,
        base: list[Any],
        path: str,
        recorder: _PatchRecorder,
        parent: "ModelDraft | ListDraft | None" = None,
        parent_key: str | int | None = None,
    ) -> None:
        """Initialize a list draft proxy.

        Args:
            base: The original list to proxy. Never modified.
            path: JSON Pointer path to this list node.
            recorder: Shared patch recorder that accumulates Op objects.
            parent: Parent draft (for dirty-flag propagation up the tree).
            parent_key: Key or index in the parent that points to this draft.
        """
        object.__setattr__(self, "_base", base)
        object.__setattr__(self, "_copy", None)
        object.__setattr__(self, "_path", path)
        object.__setattr__(self, "_recorder", recorder)
        object.__setattr__(self, "_child_drafts", {})
        object.__setattr__(self, "_dirty", False)
        object.__setattr__(self, "_parent", parent)
        object.__setattr__(self, "_parent_key", parent_key)

    def _mark_dirty(self) -> None:
        object.__setattr__(self, "_dirty", True)
        parent: ModelDraft | ListDraft | None = object.__getattribute__(self, "_parent")
        if parent is not None:
            parent._mark_dirty()

    def _ensure_copy(self) -> list[Any]:
        copy: list[Any] | None = object.__getattribute__(self, "_copy")
        if copy is None:
            base: list[Any] = object.__getattribute__(self, "_base")
            copy = list(base)
            object.__setattr__(self, "_copy", copy)
        return copy

    def _current(self) -> list[Any]:
        copy: list[Any] | None = object.__getattribute__(self, "_copy")
        if copy is not None:
            return copy
        base: list[Any] = object.__getattribute__(self, "_base")
        return base

    def __getitem__(self, index: int) -> Any:
        current = self._current()
        if index < 0:
            index = len(current) + index
        val = current[index]

        child_drafts: dict[int, Any] = object.__getattribute__(self, "_child_drafts")
        if index in child_drafts:
            return child_drafts[index]

        path: str = object.__getattribute__(self, "_path")
        recorder: _PatchRecorder = object.__getattribute__(self, "_recorder")
        child_path = f"{path}/{index}"

        if isinstance(val, BaseModel):
            draft: Any = ModelDraft(val, child_path, recorder, parent=self, parent_key=index)
            child_drafts[index] = draft
            return draft
        if isinstance(val, list):
            draft = ListDraft(val, child_path, recorder, parent=self, parent_key=index)
            child_drafts[index] = draft
            return draft

        return val

    def __setitem__(self, index: int, value: Any) -> None:
        path: str = object.__getattribute__(self, "_path")
        recorder: _PatchRecorder = object.__getattribute__(self, "_recorder")

        copy = self._ensure_copy()
        if index < 0:
            index = len(copy) + index
        copy[index] = value
        self._mark_dirty()

        recorder.record(ReplaceOp(path=append_segment(path, index), value=_serialize_value(value)))

        child_drafts: dict[int, Any] = object.__getattribute__(self, "_child_drafts")
        child_drafts.pop(index, None)

    def append(self, value: Any) -> None:
        path: str = object.__getattribute__(self, "_path")
        recorder: _PatchRecorder = object.__getattribute__(self, "_recorder")

        copy = self._ensure_copy()
        copy.append(value)
        self._mark_dirty()

        recorder.record(AddOp(path=append_segment(path, "-"), value=_serialize_value(value)))

    def extend(self, values: list[Any]) -> None:
        for v in values:
            self.append(v)

    def __len__(self) -> int:
        return len(self._current())

    def __iter__(self) -> Iterator[Any]:
        return iter(self._current())

    def __contains__(self, item: Any) -> bool:
        return item in self._current()

    def pop(self, index: int = -1) -> Any:
        path: str = object.__getattribute__(self, "_path")
        recorder: _PatchRecorder = object.__getattribute__(self, "_recorder")

        copy = self._ensure_copy()
        if index < 0:
            index = len(copy) + index
        val = copy.pop(index)
        self._mark_dirty()

        recorder.record(RemoveOp(path=append_segment(path, index)))
        return val

    def insert(self, index: int, value: Any) -> None:
        path: str = object.__getattribute__(self, "_path")
        recorder: _PatchRecorder = object.__getattribute__(self, "_recorder")

        copy = self._ensure_copy()
        copy.insert(index, value)
        self._mark_dirty()

        recorder.record(AddOp(path=append_segment(path, index), value=_serialize_value(value)))

    def _commit(self) -> list[Any]:
        """Build the committed list with child drafts committed."""
        dirty: bool = object.__getattribute__(self, "_dirty")
        if not dirty:
            base: list[Any] = object.__getattribute__(self, "_base")
            return base

        current = list(self._current())
        child_drafts: dict[int, Any] = object.__getattribute__(self, "_child_drafts")

        for idx, child in child_drafts.items():
            if isinstance(idx, int) and idx < len(current):
                current[idx] = child._commit()

        return current


class DictDraft:
    """Draft proxy for a dict.

    Supports key get/set, containment checks, iteration, len, and
    keys/values/items. Copy-on-write: the dict is shallow-copied on
    first mutation. Distinguishes new keys (AddOp) from existing keys
    (ReplaceOp).
    """

    def __init__(
        self,
        base: dict[str, Any],
        path: str,
        recorder: _PatchRecorder,
        parent: "ModelDraft | ListDraft | None" = None,
        parent_key: str | int | None = None,
    ) -> None:
        """Initialize a dict draft proxy.

        Args:
            base: The original dict to proxy. Never modified.
            path: JSON Pointer path to this dict node.
            recorder: Shared patch recorder that accumulates Op objects.
            parent: Parent draft (for dirty-flag propagation up the tree).
            parent_key: Key or index in the parent that points to this draft.
        """
        object.__setattr__(self, "_base", base)
        object.__setattr__(self, "_copy", None)
        object.__setattr__(self, "_path", path)
        object.__setattr__(self, "_recorder", recorder)
        object.__setattr__(self, "_dirty", False)
        object.__setattr__(self, "_parent", parent)
        object.__setattr__(self, "_parent_key", parent_key)

    def _mark_dirty(self) -> None:
        object.__setattr__(self, "_dirty", True)
        parent: ModelDraft | ListDraft | None = object.__getattribute__(self, "_parent")
        if parent is not None:
            parent._mark_dirty()

    def _ensure_copy(self) -> dict[str, Any]:
        copy: dict[str, Any] | None = object.__getattribute__(self, "_copy")
        if copy is None:
            base: dict[str, Any] = object.__getattribute__(self, "_base")
            copy = dict(base)
            object.__setattr__(self, "_copy", copy)
        return copy

    def _current(self) -> dict[str, Any]:
        copy: dict[str, Any] | None = object.__getattribute__(self, "_copy")
        if copy is not None:
            return copy
        base: dict[str, Any] = object.__getattribute__(self, "_base")
        return base

    def __getitem__(self, key: str) -> Any:
        return self._current()[key]

    def __setitem__(self, key: str, value: Any) -> None:
        path: str = object.__getattribute__(self, "_path")
        recorder: _PatchRecorder = object.__getattribute__(self, "_recorder")

        copy = self._ensure_copy()
        is_new = key not in copy
        copy[key] = value
        self._mark_dirty()

        field_path = append_segment(path, key)
        if is_new:
            recorder.record(AddOp(path=field_path, value=_serialize_value(value)))
        else:
            recorder.record(ReplaceOp(path=field_path, value=_serialize_value(value)))

    def __contains__(self, key: object) -> bool:
        return key in self._current()

    def __iter__(self) -> Iterator[str]:
        return iter(self._current())

    def __len__(self) -> int:
        return len(self._current())

    def keys(self) -> Any:
        return self._current().keys()

    def values(self) -> Any:
        return self._current().values()

    def items(self) -> Any:
        return self._current().items()

    def _commit(self) -> dict[str, Any]:
        dirty: bool = object.__getattribute__(self, "_dirty")
        if not dirty:
            base: dict[str, Any] = object.__getattribute__(self, "_base")
            return base
        return dict(self._current())


# Public alias. recipe_with_effects functions receive a Draft as their
# first argument. Also used by produce() recipes.
Draft = ModelDraft


# ---------------------------------------------------------------------------
# produce()
# ---------------------------------------------------------------------------


def produce[T: BaseModel](base: T, recipe: Callable[[Draft], None]) -> tuple[T, list[Op]]:
    """Apply recipe mutations to base, returning new state and patch ops.

    The base object is never modified. Ops apply to
    base.model_dump(mode="json").

    Args:
        base: A Pydantic v2 BaseModel instance.
        recipe: A function that receives a Draft proxy and mutates it.

    Returns:
        (new_base, ops) where new_base has structural sharing with
        base for unchanged subtrees.
    """
    recorder = _PatchRecorder()
    draft = ModelDraft(base, "", recorder)

    recipe(draft)

    new_state = draft._commit()
    return new_state, recorder.ops  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# diff()
# ---------------------------------------------------------------------------


def diff(
    old: Any,
    new: Any,
    output_prefix: str = "",
    *,
    output_index_offset: int = 0,
) -> list[Op]:
    """Compute patches that transform old into new.

    Leverages reference equality (Python `is`) to skip unchanged
    subtrees. O(changed nodes).

    Args:
        old: The original state.
        new: The updated state.
        output_prefix: JSON Pointer prefix for emitted patch paths.
        output_index_offset: Offset for concrete indexes emitted from a
            root-level list diff. Only valid when old and new are both lists.

    Returns:
        A list of typed Op objects representing the changes.
    """
    if output_index_offset < 0:
        msg = f"diff output_index_offset must be non-negative, got {output_index_offset}"
        raise ValueError(msg)
    if output_index_offset and not (isinstance(old, list) and isinstance(new, list)):
        msg = "diff output_index_offset is only valid when old and new are lists"
        raise ValueError(msg)

    if old is new:
        return []

    ops: list[Op] = []

    if isinstance(old, BaseModel) and isinstance(new, BaseModel):
        if type(old) is not type(new):
            ops.append(ReplaceOp(path=output_prefix or "/", value=_serialize_value(new)))
            return ops
        # Compare field by field using reference equality
        for field_name in type(old).model_fields:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            field_path = append_segment(output_prefix, field_name)
            ops.extend(_diff_values(old_val, new_val, field_path))
    elif isinstance(old, list) and isinstance(new, list):
        ops.extend(_diff_lists(old, new, output_prefix, index_offset=output_index_offset))
    elif isinstance(old, dict) and isinstance(new, dict):
        ops.extend(_diff_dicts(old, new, output_prefix))
    elif isinstance(old, str) and isinstance(new, str):
        if old != new:
            if new.startswith(old) and len(new) > len(old):
                ops.append(AppendOp(path=output_prefix, value=new[len(old) :]))
            else:
                ops.append(ReplaceOp(path=output_prefix, value=new))
    elif old != new:
        ops.append(ReplaceOp(path=output_prefix, value=_serialize_value(new)))

    return ops


def _diff_values(old: Any, new: Any, path: str) -> list[Op]:
    """Diff two arbitrary values at a given path."""
    if old is new:
        return []

    if isinstance(old, BaseModel) and isinstance(new, BaseModel):
        return diff(old, new, path)
    if isinstance(old, list) and isinstance(new, list):
        return _diff_lists(old, new, path)
    if isinstance(old, dict) and isinstance(new, dict):
        return _diff_dicts(old, new, path)
    if isinstance(old, str) and isinstance(new, str):
        if old == new:
            return []
        if new.startswith(old) and len(new) > len(old):
            return [AppendOp(path=path, value=new[len(old) :])]
        return [ReplaceOp(path=path, value=new)]
    if old != new:
        return [ReplaceOp(path=path, value=_serialize_value(new))]
    return []


def _diff_lists(
    old: list[Any],
    new: list[Any],
    path: str,
    *,
    index_offset: int = 0,
) -> list[Op]:
    """Diff two lists element by element."""
    ops: list[Op] = []
    min_len = min(len(old), len(new))

    # Compare shared elements
    for i in range(min_len):
        if old[i] is not new[i]:
            ops.extend(_diff_values(old[i], new[i], append_segment(path, i + index_offset)))

    # New elements appended
    for i in range(min_len, len(new)):
        ops.append(AddOp(path=append_segment(path, "-"), value=_serialize_value(new[i])))

    # Elements removed from the end
    if len(new) < len(old):
        for i in range(len(old) - 1, min_len - 1, -1):
            ops.append(RemoveOp(path=append_segment(path, i + index_offset)))

    return ops


def _diff_dicts(old: dict[str, Any], new: dict[str, Any], path: str) -> list[Op]:
    """Diff two dicts key by key."""
    ops: list[Op] = []
    all_keys = set(old.keys()) | set(new.keys())

    for key in sorted(all_keys):
        field_path = append_segment(path, key)
        if key in old and key not in new:
            ops.append(RemoveOp(path=field_path))
        elif key not in old and key in new:
            ops.append(AddOp(path=field_path, value=_serialize_value(new[key])))
        else:
            ops.extend(_diff_values(old[key], new[key], field_path))

    return ops


# ---------------------------------------------------------------------------
# @immer_reducer decorator
# ---------------------------------------------------------------------------


def immer_reducer(
    recipe_with_effects: Callable[..., Any],
) -> Callable[..., Any]:
    """Decorator that wraps a recipe_with_effects into a reducer.

    Vocabulary:
        recipe_with_effects — the inner function you write. It
                  receives a mutable Draft proxy and an event,
                  mutates the draft imperatively, and returns a list
                  of effects to execute. It does NOT return new state;
                  state changes are captured automatically by the
                  draft proxy. The name reflects both responsibilities:
                  it is a recipe (mutates draft) that also returns
                  effects.
        reducer — the outer function produced by this decorator. It
                  takes (state, event, ...), calls produce() with
                  the recipe_with_effects, and returns
                  (new_state, patches, effects). This is the standard
                  reducer signature consumed by ExecutionLoop.

    recipe_with_effects signature (what you write):
        fn(draft: Draft, event: E, ...) -> list[Eff]

    Reducer signature (what the decorator returns):
        wrapper(state: TaskState, event: E, ...) -> (new_state, patches, effects)
    """

    @functools.wraps(recipe_with_effects)
    def wrapper(
        state: Any, event: Any, *args: Any, **kwargs: Any
    ) -> tuple[Any, list[Op], list[Any]]:
        effects: list[Any] = []

        def inner_recipe(draft: Draft) -> None:
            nonlocal effects
            effects = recipe_with_effects(draft, event, *args, **kwargs)

        new_state, patches = produce(state, inner_recipe)
        return (new_state, patches, effects)

    return wrapper


__all__ = [
    "DictDraft",
    "Draft",
    "ListDraft",
    "ModelDraft",
    "diff",
    "immer_reducer",
    "produce",
]
