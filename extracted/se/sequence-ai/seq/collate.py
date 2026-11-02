"""
A @seq.concurrent policy's list of requests as one batch, and its batched answer back as one answer per request:
`seq.collate(obs, buckets=[1, 2, 4, 8], group_by=...)` and `seq.uncollate(out, n)`. Optional - an infer that stacks its
own list is served the same.

In one sentence: collate(items) walks the requests side by side → a mapping key by key, a list as one more axis, each
array or number stacked along a new first axis (B, ...), text and anything else kept as a list of B → arrays whose
first axis differs padded with zeros to the longest, `<key>_mask` beside them, (B, L) and True where real → B padded to
the smallest bucket that holds it by repeating the last request → uncollate(out, n) splits the answer along its first
axis and keeps the first n.

WHY padded and masked, not refused: a window is shorter at an episode's start when the policy declares pad="drop", and
a model compiled for fixed shapes (torch.compile, CUDA graphs, TensorRT) takes one shape a batch - openpi masks the
cameras a request lacks the same way (image_masks, True where real). WHY only the first axis: frames of two sizes are a
camera fitted other than declared, which padding would hide - a Stream's camera has the worker fit them before infer is
handed them. WHY the last request again in a bucket's spare rows, not zeros: a model that normalizes its inputs reads
a row of zeros as nothing it was trained on, and those rows are left out of the answer anyway.

"""
from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

__all__ = ["collate", "uncollate"]


def collate(items: Any, *, buckets: Any = None, group_by: Any = None) -> Any:
    """The requests a @seq.concurrent infer is handed, as one batch: a mapping key by key, a list as one more axis, each
    array, tensor or number stacked along a new first axis (B, ...) - tensors on the first one's device - and text or
    anything else kept as a list of B. Arrays whose first axis differs are padded with zeros to the longest, with
    `<key>_mask` beside them: (B, L), True where the row is real.

    `buckets`: the batch sizes the model was compiled for, e.g. [1, 2, 4, 8]: B is padded to the smallest that holds it
    by repeating the last request; seq.uncollate(out, n) leaves those rows out again. `group_by`: one value a request
    (a seed, a number of denoising steps) - requests whose values differ go in batches of their own,
    returned as [(indices, batch), ...] in the order each value first appears."""
    rows = list(items)
    if not rows:
        raise ValueError("seq.collate: no requests to batch")
    if group_by is not None:
        values = list(group_by)
        if len(values) != len(rows):
            raise ValueError(f"seq.collate: group_by gives {len(values)} values for {len(rows)} requests; give one a "
                             "request")
        groups: dict = {}
        for i, value in enumerate(values):
            try:
                groups.setdefault(value, []).append(i)
            except TypeError:
                raise TypeError(f"seq.collate: group_by's values are compared as keys, and {type(value).__name__} "
                                "is not one: give a number, a string or a tuple of them") from None
        return [(idx, collate([rows[i] for i in idx], buckets=buckets)) for idx in groups.values()]
    rows += [rows[-1]] * (_bucket(len(rows), buckets) - len(rows))
    batch, lengths = _stack(rows, "")
    if lengths is not None:
        raise ValueError("seq.collate: the requests are arrays whose first axis differs; hand each as a dict, so the "
                         "mask that says which rows are real has a key to stand beside")
    return batch


def uncollate(out: Any, n: int) -> list:
    """A batched answer as one answer per request, in the order seq.collate took them: each array or tensor split along
    its first axis and its first `n` rows kept (the rest are a bucket's padding), each mapping key by key, each tuple
    item by item; a list is one entry a request already, and anything else - a number, a string - is every request's."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"seq.uncollate: n is how many requests the batch answers, got {n!r}")
    if isinstance(out, Mapping):
        parts = {key: uncollate(value, n) for key, value in out.items()}
        return [{key: part[i] for key, part in parts.items()} for i in range(n)]
    if isinstance(out, tuple):
        parts = [uncollate(value, n) for value in out]
        make = getattr(type(out), "_make", tuple)
        return [make(part[i] for part in parts) for i in range(n)]
    if isinstance(out, list):
        if len(out) < n:
            raise ValueError(f"seq.uncollate: a list of {len(out)} answers for {n} requests")
        return out[:n]
    shape = getattr(out, "shape", None)
    if shape is not None and len(shape) >= 1:
        if shape[0] < n:
            raise ValueError(f"seq.uncollate: {shape[0]} rows for {n} requests")
        return [out[i] for i in range(n)]
    return [out] * n


def _bucket(n: int, buckets: Any) -> int:
    """The smallest of `buckets` that holds a batch of n; n itself without buckets."""
    if buckets is None:
        return n
    sizes = sorted(int(b) for b in buckets)
    if not sizes or sizes[0] < 1:
        raise ValueError("seq.collate: buckets are batch sizes, each 1 or more")
    for size in sizes:
        if size >= n:
            return size
    raise ValueError(f"seq.collate: a batch of {n} is larger than the largest bucket, {sizes[-1]}; list each size "
                     "@seq.concurrent(sizes=[...]) lists among the buckets")


def _at(where: str) -> str:
    return f"{where}: " if where else ""


def _stack(rows: list, where: str) -> tuple[Any, list[int] | None]:
    """The requests' values at one place (`where`, its keys joined by dots) side by side, as one: the batch's value, and
    each request's length along the first axis when those differ (None when they do not)."""
    first = rows[0]
    if isinstance(first, Mapping):
        return _stack_mappings(rows, where), None
    if isinstance(first, (list, tuple)):
        return _stack_lists(rows, where)
    if _numeric(first):
        return _stack_arrays(rows, where)
    return list(rows), None


def _stack_mappings(rows: list, where: str) -> dict:
    keys = list(rows[0])
    for r in rows[1:]:
        if not isinstance(r, Mapping) or set(r) != set(keys):
            has = sorted(map(str, r)) if isinstance(r, Mapping) else type(r).__name__
            raise ValueError(f"seq.collate: {_at(where)}every request needs the same keys: one has {has}, another "
                             f"{sorted(map(str, keys))}")
    out: dict = {}
    for key in keys:
        value, lengths = _stack([r[key] for r in rows], f"{where}.{key}" if where else str(key))
        out[key] = value
        if lengths is not None:
            mask = f"{key}_mask"
            if mask in rows[0]:
                raise ValueError(f"seq.collate: {_at(where)}{mask} is a key of the requests already, and the mask "
                                 f"that says which of {key}'s rows are real would replace it")
            out[mask] = _mask(value, lengths)
    return out


def _stack_lists(rows: list, where: str) -> tuple[Any, list[int] | None]:
    """Each request's list as one more axis: its entries stacked along a first axis of their own - alike in shape within
    one request - then the requests' stacks side by side, a shorter list padded as any first axis is."""
    inner = []
    for r in rows:
        if not isinstance(r, (list, tuple)):
            raise ValueError(f"seq.collate: {_at(where)}one request has {type(r).__name__} where another has a list")
        if not r:
            raise ValueError(f"seq.collate: {_at(where)}one request's list is empty: it has no shape to stack")
        value, lengths = _stack(list(r), where)
        if lengths is not None:
            raise ValueError(f"seq.collate: {_at(where)}one request's list holds arrays whose first axis differs; only "
                             "the list's own length may differ between requests")
        inner.append(value)
    if isinstance(inner[0], list):
        return [list(r) for r in rows], None
    return _stack(inner, where)


def _numeric(v: Any) -> bool:
    """A number, or an array or tensor (anything with a shape and a dtype): what stacks."""
    return isinstance(v, (bool, int, float, complex)) or (hasattr(v, "shape") and hasattr(v, "dtype"))


def _torch(values: list):
    """The torch module, when any of `values` is one of its tensors."""
    torch = sys.modules.get("torch")
    return torch if torch is not None and any(isinstance(v, torch.Tensor) for v in values) else None


def _numpy():
    try:
        import numpy
    except ImportError:
        raise ImportError("seq.collate stacks arrays with numpy: pip install numpy") from None
    return numpy


def _stack_arrays(rows: list, where: str) -> tuple[Any, list[int] | None]:
    for r in rows:
        if not _numeric(r):
            raise ValueError(f"seq.collate: {_at(where)}one request has {type(r).__name__} where another has a number "
                             "or an array")
    torch = _torch(rows)
    if torch is not None:
        device = next(r.device for r in rows if isinstance(r, torch.Tensor))
        arrays = [r if isinstance(r, torch.Tensor) else torch.as_tensor(r, device=device) for r in rows]
        dtype = arrays[0].dtype
        for a in arrays[1:]:
            dtype = torch.promote_types(dtype, a.dtype)
        arrays = [a.to(device=device, dtype=dtype) for a in arrays]
        stack = torch.stack
    else:
        np = _numpy()
        arrays = [np.asarray(r) for r in rows]
        stack = np.stack
    shapes = [tuple(a.shape) for a in arrays]
    if len(set(shapes)) == 1:
        return stack(arrays), None
    if any(len(s) != len(shapes[0]) or not s or s[1:] != shapes[0][1:] for s in shapes):
        listed = ", ".join(str(s) for s in sorted(set(shapes)))
        raise ValueError(f"seq.collate: {_at(where)}arrays of shapes {listed} cannot be one batch: only their first "
                         "axis may differ, padded with a mask beside it")
    longest = max(s[0] for s in shapes)
    return stack([_pad(a, longest, torch) for a in arrays]), [s[0] for s in shapes]


def _pad(a: Any, length: int, torch: Any) -> Any:
    """`a` with rows of zeros after it, `length` long along its first axis."""
    more = length - a.shape[0]
    if not more:
        return a
    if torch is not None:
        return torch.cat([a, a.new_zeros((more, *a.shape[1:]))])
    np = _numpy()
    return np.concatenate([a, np.zeros((more, *a.shape[1:]), dtype=a.dtype)])


def _mask(value: Any, lengths: list[int]) -> Any:
    """(B, L): True where a request's first axis has a real row, False where it was padded."""
    torch = _torch([value])
    if torch is not None:
        steps = torch.arange(value.shape[1], device=value.device)
        return steps[None, :] < torch.as_tensor(lengths, device=value.device)[:, None]
    np = _numpy()
    return np.arange(value.shape[1])[None, :] < np.asarray(lengths)[:, None]
