"""Training datums that are built from trajectory spans only when read.

A ``TrainingBatch`` keeps, per datum, a reference to the trajectory's spans
and the resolved values that decide what it trains (run, advantage,
normalization, and any proximal-policy correction). Reading an element builds
that datum; nothing keeps it afterwards. The trainer passes batches to the
client, which encodes each datum straight into its request, so training data
never accumulates in client memory.
"""

from collections.abc import Sequence
from dataclasses import dataclass, replace

import numpy as np


@dataclass(frozen=True)
class _Build:
    """Settings shared by every datum of one ``build_batch`` call."""

    current_step: int | None
    max_staleness: int | None
    requirements: object
    include_loss_mask: bool
    # A loss binding whose ``encode_metadata`` applies, or None.
    loss: object


@dataclass(frozen=True)
class _Item:
    source: object  # Trajectory._datum_source()
    run: int
    advantage: float
    denominator: float
    length: int
    # Whether any position has a nonzero advantage after normalization.
    advantaged: bool
    routing_handle: bool
    recovered: bool
    build: _Build
    # (proximal logprob row, max importance weight) for decoupled PPO.
    proximal: tuple | None = None
    # Converts a datum into a custom loss's inputs.
    custom: object = None
    drop_recovery: bool = False
    drop_routing: bool = False


class TrainingBatch(Sequence):
    """Datums built on access. Slices and sums are batches too."""

    __slots__ = ("_items",)

    def __init__(self, items=()):
        self._items = tuple(items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return TrainingBatch(self._items[index])
        return _datum(self._items[index])

    def __iter__(self):
        for item in self._items:
            yield _datum(item)

    def __add__(self, other):
        if not isinstance(other, TrainingBatch):
            return NotImplemented
        return TrainingBatch(self._items + other._items)

    def with_items(self, **changes):
        return TrainingBatch(replace(item, **changes) for item in self._items)

    def with_proximal(self, rows, max_importance_weight):
        return TrainingBatch(
            replace(item, proximal=(row, max_importance_weight))
            for item, row in zip(self._items, rows, strict=True)
        )

    def lengths(self):
        """Each datum's input length, without building it."""
        return [item.length for item in self._items]

    def advantaged(self):
        """Whether any datum has a nonzero advantage, before PPO correction."""
        return any(item.advantaged for item in self._items)

    def routing(self):
        """Per datum: (has a routing capture, restored from a checkpoint)."""
        return [
            (
                item.routing_handle and not item.drop_routing,
                item.recovered and not item.drop_recovery,
            )
            for item in self._items
        ]


def _datum(item):
    build = item.build
    data, masks = item.source._data(
        item.advantage,
        current_step=build.current_step,
        max_staleness=build.max_staleness,
        requirements=build.requirements,
        masks=build.include_loss_mask,
        runs=(item.run,),
    )
    (datum,) = data
    if build.include_loss_mask:
        datum["loss_mask"] = masks[0]
    # Divide in float64 and round once, as the wire float32 cast did.
    datum["advantages"] = (
        datum["advantages"].astype(np.float64) / item.denominator
    ).astype(np.float32)
    if build.loss is not None:
        (datum,) = build.loss.encode_metadata([datum])
    if item.proximal is not None:
        datum, _ = decouple_datum(datum, *item.proximal)
    if item.custom is not None:
        datum = item.custom(datum)
    if item.drop_recovery:
        datum.pop("_rl_recovered_routing", None)
    if item.drop_routing:
        datum = {k: v for k, v in datum.items() if not k.startswith("expert_routing_")}
    return datum


def decouple_datum(datum, row, max_importance_weight):
    """Apply a proximal-policy correction to one datum; see ``decouple_ppo``.

    Returns the corrected datum and the importance ratios it used.
    """
    # Copies: restored journal arrays are read-only and shared.
    old = np.array(datum["old_logprobs"], dtype=np.float64)
    adv = np.array(datum["advantages"], dtype=np.float64)
    prox = np.asarray(row, dtype=np.float64)
    # River predicts n-1 tokens; some forward transports retain a trailing
    # masked position. Both forms have the same prediction alignment.
    if prox.shape == (len(old) - 1,):
        prox = np.concatenate((prox, [0.0]))
    if prox.shape != old.shape or not np.all(np.isfinite(prox[adv != 0])):
        raise ValueError(
            "proximal logprobs do not align with generated prediction positions"
        )
    mask = adv != 0
    ratio = np.exp(np.minimum(prox[mask] - old[mask], np.log(max_importance_weight)))
    adv[mask] *= ratio
    new_old = old.copy()
    new_old[mask] = prox[mask]
    return (
        {
            **datum,
            "old_logprobs": new_old.astype(np.float32),
            "advantages": adv.astype(np.float32),
        },
        ratio,
    )
