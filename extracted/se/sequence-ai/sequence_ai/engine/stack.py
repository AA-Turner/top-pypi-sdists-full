# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A @seq.concurrent policy's acts as one batch, and its batched answer back as one answer per act - what a server does
for an infer that does not say collate=False (engine.adapter RegisteredAdapter.infer_batch), a deployment's worker and
a policy server of your own alike.

In one sentence: stack(items) walks the acts' inputs side by side → a mapping key by key, a list as one more axis, each
array, tensor or number stacked along a new first axis (B, ...), text and anything else kept as a list of B → arrays
whose first axis differs padded with zeros to the longest, `<key>_mask` beside them, (B, L) and True where real, a
key not every act sends a list with None where one sent none → unstack(out, n) splits the answer along its first
axis into the n acts' answers.

WHY the server's, not the policy author's: an author writes the batched model once and is handed the batch stacked,
unless the infer says @seq.concurrent(collate=False), which hands it the list. A batch goes in a size @seq.concurrent
lists, and acts of one that set other inference parameters go in a call of their own, padded to a listed size by the
adapter (RegisteredAdapter._stacked). WHY masked, not refused, where a first axis differs: a window is shorter at an
episode's start, and a model compiled for fixed shapes takes one shape a batch - a model whose requests may lack a
camera masks it the same way, True where real.
"""
from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

# The words every refusal ends with: what an author does about acts that do not stack.
_ESCAPE = ("or declare @seq.concurrent(sizes=[...], collate=False) and the policy's infer is handed the acts as a "
           "list, to batch in its own code")


class Unstackable(ValueError):
    """The acts of a batch cannot be one: said in words, with what to do about it."""


def stack(items: list) -> Any:
    """The acts' inputs as one batch: a mapping key by key, a list as one more axis, each array, tensor or number
    stacked along a new first axis (B, ...) - tensors on the first one's device - and text or anything else kept as a
    list of B. Arrays whose first axis differs are padded with zeros to the longest, with `<key>_mask` beside them:
    (B, L), True where the row is real."""
    rows = list(items)
    if not rows:
        raise Unstackable("a batch of no acts")
    batch, lengths = _stack(rows, "")
    if lengths is not None:
        raise Unstackable(f"the acts are arrays whose first axis differs and which have no key a mask could stand "
                          f"beside: send each act's inputs as a dict, {_ESCAPE}")
    return batch


def unstack(out: Any, n: int) -> list:
    """A batched answer as one answer per act, in the order stack took them: each array or tensor split along its first
    axis, each mapping key by key, each tuple item by item; a list is one entry an act already, and a number, a string
    or None is every act's. Any other object - a robot-arm preset's ActionChunk - is one act's answer: a batch of more
    than one answers a list of them, never one handed to every act."""
    if isinstance(out, Mapping):
        parts = {key: unstack(value, n) for key, value in out.items()}
        return [{key: part[i] for key, part in parts.items()} for i in range(n)]
    if isinstance(out, tuple):
        parts = [unstack(value, n) for value in out]
        make = getattr(type(out), "_make", tuple)              # a namedtuple stays one
        return [make(part[i] for part in parts) for i in range(n)]
    if isinstance(out, list):
        if len(out) != n:
            raise Unstackable(f"the policy's infer answered a list of {len(out)} for a batch of {n} acts: answer one "
                              f"batch whose arrays have {n} rows, or a list of {n}")
        return list(out)
    shape = getattr(out, "shape", None)
    if shape is not None and len(shape) >= 1:
        if shape[0] != n:
            raise Unstackable(f"the policy's infer answered an array of {shape[0]} rows for a batch of {n} acts: its "
                              f"first axis is the batch's")
        return [out[i] for i in range(n)]
    if n > 1 and not isinstance(out, (str, bytes, bool, int, float, complex, type(None))):
        raise Unstackable(f"the policy's infer answered one {type(out).__name__} for a batch of {n} acts: answer a "
                          f"list of {n}, one an act, or one batch whose arrays have {n} rows")
    return [out] * n


def _at(where: str) -> str:
    return f"at {where}, " if where else ""


def _stack(rows: list, where: str) -> tuple[Any, list[int] | None]:
    """The acts' values at one place (`where`, its keys joined by dots) side by side, as one: the batch's value, and
    each act's length along the first axis when those differ (None when they do not)."""
    first = rows[0]
    if isinstance(first, Mapping):
        return _stack_mappings(rows, where), None
    if isinstance(first, (list, tuple)):
        return _stack_lists(rows, where)
    if _numeric(first):
        return _stack_arrays(rows, where)
    return list(rows), None


def _stack_mappings(rows: list, where: str) -> dict:
    """The acts' dicts key by key, every key any of them sends. A key not every act sends comes as a list, None where
    an act sent none, never stacked - an array is not made up for an act that sent none: pi05-droid-qwen's robots send
    a prompt connected to it and none through its planner, and both may share a copy's batch."""
    for r in rows:
        if not isinstance(r, Mapping):
            raise Unstackable(f"{_at(where)}one act has {type(r).__name__} where another has a dict: {_ESCAPE}")
    keys = list(dict.fromkeys(key for r in rows for key in r))
    out: dict = {}
    for key in keys:
        if any(key not in r for r in rows):
            out[key] = [r.get(key) for r in rows]
            continue
        value, lengths = _stack([r[key] for r in rows], f"{where}.{key}" if where else str(key))
        out[key] = value
        if lengths is not None:
            mask = f"{key}_mask"
            if mask in keys:
                raise Unstackable(f"{_at(where)}{mask} is a key of the acts already, and the mask that says which of "
                                  f"{key}'s rows are real would replace it: rename it, {_ESCAPE}")
            out[mask] = _mask(value, lengths)
    return out


def _stack_lists(rows: list, where: str) -> tuple[Any, list[int] | None]:
    """Each act's list as one more axis: its entries stacked along a first axis of their own - alike in shape within one
    act - then the acts' stacks side by side, a shorter list padded as any first axis is."""
    inner = []
    for r in rows:
        if not isinstance(r, (list, tuple)):
            raise Unstackable(f"{_at(where)}one act has {type(r).__name__} where another has a list: {_ESCAPE}")
        if not r:
            raise Unstackable(f"{_at(where)}one act's list is empty and has no shape to stack: {_ESCAPE}")
        value, lengths = _stack(list(r), where)
        if lengths is not None:
            raise Unstackable(f"{_at(where)}one act's list holds arrays whose first axis differs; only the list's own "
                              f"length may differ between acts: {_ESCAPE}")
        inner.append(value)
    if isinstance(inner[0], list):                  # text and the like: each act's list as it was
        return [list(r) for r in rows], None
    return _stack(inner, where)


def _numeric(v: Any) -> bool:
    """A number, or an array or tensor (anything with a shape and a dtype): what stacks."""
    return isinstance(v, (bool, int, float, complex)) or (hasattr(v, "shape") and hasattr(v, "dtype"))


def _torch(values: list) -> Any:
    """The torch module, when any of `values` is one of its tensors."""
    torch = sys.modules.get("torch")
    return torch if torch is not None and any(isinstance(v, torch.Tensor) for v in values) else None


def _stack_arrays(rows: list, where: str) -> tuple[Any, list[int] | None]:
    for r in rows:
        if not _numeric(r):
            raise Unstackable(f"{_at(where)}one act has {type(r).__name__} where another has a number or an array: "
                              f"{_ESCAPE}")
    torch = _torch(rows)
    if torch is not None:
        device = next(r.device for r in rows if isinstance(r, torch.Tensor))
        arrays = [r if isinstance(r, torch.Tensor) else torch.as_tensor(r, device=device) for r in rows]
        dtype = arrays[0].dtype
        for a in arrays[1:]:
            dtype = torch.promote_types(dtype, a.dtype)
        arrays = [a.to(device=device, dtype=dtype) for a in arrays]
        joined = torch.stack
    else:
        import numpy as np

        arrays = [np.asarray(r) for r in rows]
        joined = np.stack
    shapes = [tuple(a.shape) for a in arrays]
    if len(set(shapes)) == 1:
        return joined(arrays), None
    if any(len(s) != len(shapes[0]) or not s or s[1:] != shapes[0][1:] for s in shapes):
        listed = ", ".join(str(s) for s in sorted(set(shapes)))
        raise Unstackable(f"{_at(where)}arrays of shapes {listed} cannot be one batch, as only their first axis may "
                          f"differ (padded, with a mask beside it): {_ESCAPE}")
    longest = max(s[0] for s in shapes)
    return joined([_pad(a, longest, torch) for a in arrays]), [s[0] for s in shapes]


def _pad(a: Any, length: int, torch: Any) -> Any:
    """`a` with rows of zeros after it, `length` long along its first axis."""
    more = length - a.shape[0]
    if not more:
        return a
    if torch is not None:
        return torch.cat([a, a.new_zeros((more, *a.shape[1:]))])
    import numpy as np

    return np.concatenate([a, np.zeros((more, *a.shape[1:]), dtype=a.dtype)])


def _mask(value: Any, lengths: list[int]) -> Any:
    """(B, L): True where an act's first axis has a real row, False where it was padded."""
    torch = _torch([value])
    if torch is not None:
        steps = torch.arange(value.shape[1], device=value.device)
        return steps[None, :] < torch.as_tensor(lengths, device=value.device)[:, None]
    import numpy as np

    return np.arange(value.shape[1])[None, :] < np.asarray(lengths)[:, None]
