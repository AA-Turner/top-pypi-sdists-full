from __future__ import annotations

"""Minimal spin algebra for symbolic interactions."""

from enum import Enum
from dataclasses import dataclass
from typing import Tuple


class SpinState(Enum):
    CURIOSITY = "curiosity"
    DUTY = "duty"
    DELIGHT = "delight"
    INQUIRY = "inquiry"


@dataclass
class SpinInteraction:
    """Resulting state of combining two spins."""

    left: SpinState
    right: SpinState
    result: SpinState


def combine_spins(a: SpinState, b: SpinState) -> SpinInteraction:
    """Return deterministic result for simple spin combinations."""
    table = {
        (SpinState.CURIOSITY, SpinState.DUTY): SpinState.INQUIRY,
        (SpinState.DUTY, SpinState.CURIOSITY): SpinState.INQUIRY,
        (SpinState.CURIOSITY, SpinState.DELIGHT): SpinState.DELIGHT,
    }
    result = table.get((a, b), a)
    return SpinInteraction(left=a, right=b, result=result)

__all__ = ["SpinState", "SpinInteraction", "combine_spins"]
