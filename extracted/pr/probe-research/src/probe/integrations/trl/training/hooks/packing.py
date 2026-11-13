"""A padding-free / packed SFT row split back into its examples (`sft_trainer.py:176-230`; spike S1, plan D10): the
collator flattens a micro-batch into ONE row and restarts `position_ids` at each example (`cu_seq_lens_q` holds the
boundaries). Pure tensor code, so a framework bump that moves a boundary fails the CPU test, not the next GPU pass."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def shift_to_targets(values: Mapping[str, Any], label_mask: Any, total: int) -> tuple[dict[str, Any], Any]:
    """The fused LM head's position `t` scores token `t + 1` ([N - 1] values for [N] tokens): each value placed at the
    token it scores, so it lands in that token's example (a segment's first token is never trained: the collator
    masks it)."""
    import torch.nn.functional as functional

    shift = int(total - label_mask.shape[-1])
    placed = {name: functional.pad(value, (shift, 0)) for name, value in values.items()}
    return placed, functional.pad(label_mask, (shift, 0))


def to_segments(values: Mapping[str, Any], mask: Any, ids: Any, starts: list[int], total: int) -> tuple:
    """Flat [N] per-token tensors -> [segments, longest] by the segment ``starts`` (host ints): returns (values,
    mask, ids, kept) in segment order, zero past each segment's end (kept 0 there)."""
    import torch

    bounds = [*starts, total]
    lengths = [end - start for start, end in zip(bounds[:-1], bounds[1:], strict=True)]
    count, longest = len(lengths), max(lengths)
    device = mask.device
    segment = torch.repeat_interleave(torch.arange(count, device=device), torch.tensor(lengths, device=device))
    offset = torch.arange(total, device=device) - torch.tensor(starts, device=device)[segment]

    def place(flat: Any) -> Any:
        out = torch.zeros(count, longest, dtype=flat.dtype, device=device)
        out[segment, offset] = flat
        return out

    kept = place(torch.ones(total, dtype=torch.long, device=device))
    return {name: place(value) for name, value in values.items()}, place(mask), place(ids), kept
