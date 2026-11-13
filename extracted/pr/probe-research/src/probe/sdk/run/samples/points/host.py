"""A loss hook's numbers for one micro-batch brought to the host in ONE device-to-host copy: the per-row columns, the
loss mask's flags and any scalar tensors (the reported loss, candidate means) joined on the device, then one
`.tolist()`. Every `.item()`, `float(tensor)` or `.tolist()` a hook adds is another GPU sync per micro-batch."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class HostTable:
    #: Per row, each column's value, in the order given.
    rows: list[list[float]]
    #: Per row, its mask flags (1.0 / 0.0 a token).
    flags: list[list[float]]
    #: Each scalar given, as a float (a Python number passes through; None stays None).
    scalars: list[float | None]


def copy_to_host(columns: Sequence[Any], flags: Any, scalars: Sequence[Any] = (), *,
                 lengths: Sequence[int] | None = None) -> HostTable:  # fmt: skip
    """``columns``: per-row tensors ([rows]); ``flags``: the mask as float, [rows, tokens], or flat ([sum of
    ``lengths``]) with ``lengths`` giving each row's own length (rows of very different lengths: never pad them to the
    longest; host ints, never a device tensor, whose every element would be a sync); ``scalars``: tensors with one
    element, Python numbers or None. Everything goes to float64 on the flags' device first, then ONE copy. Shapes are
    checked before the copy (a wrong length would silently hand one row another's flags)."""
    import torch

    rows_given = len(columns[0]) if columns else 0
    if lengths is not None and (len(lengths) != rows_given or sum(int(n) for n in lengths) != flags.numel()):
        raise ValueError(f"lengths {list(lengths)} do not split {flags.numel()} mask values into {rows_given} rows")
    if lengths is None and (flags.dim() != 2 or flags.shape[0] != rows_given):
        raise ValueError(f"a [rows, tokens] mask for {rows_given} rows was expected, got {tuple(flags.shape)}")
    device = flags.device
    table = torch.stack([column.detach().to(device=device, dtype=torch.float64) for column in columns], dim=1)
    width, rows = table.shape[1], table.shape[0]
    mask = flags.detach().to(device=device, dtype=torch.float64).reshape(-1)
    on_device = [index for index, value in enumerate(scalars) if isinstance(value, torch.Tensor) and value.numel()]
    parts = [table.reshape(-1), mask] + [scalars[index].detach().reshape(-1)[:1].to(device=device, dtype=torch.float64)
                                         for index in on_device]  # fmt: skip
    copied = torch.cat(parts).tolist()  # the one copy
    cells, mask_size = rows * width, mask.numel()
    host_rows = [copied[index * width:(index + 1) * width] for index in range(rows)]
    flat_flags, tail = copied[cells:cells + mask_size], copied[cells + mask_size:]
    if lengths is None:
        size = mask_size // rows if rows else 0
        host_flags = [flat_flags[index * size:(index + 1) * size] for index in range(rows)]
    else:
        starts = [0]
        for length in lengths:
            starts.append(starts[-1] + int(length))
        host_flags = [flat_flags[starts[index]:starts[index + 1]] for index in range(rows)]
    found = [None if value is None or isinstance(value, torch.Tensor) else float(value) for value in scalars]
    for position, index in enumerate(on_device):
        found[index] = tail[position]
    return HostTable(rows=host_rows, flags=host_flags, scalars=found)
