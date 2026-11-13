"""The loss hooks, picked once by the trainer's class chain (nearest first), and the trainer kinds no hook covers.
Nothing from TRL is imported: a class is matched by name, so GKD (an SFTTrainer subclass) is found as GKD. A subclass
that defines its own loss method (TRL's GMPOTrainer `_compute_loss`) is declared unsupported: the hook rebuilds the
base class's formula only."""

from __future__ import annotations

from typing import Any

from ..declarations import OVERRIDE_SUFFIX, UNSUPPORTED
from ..hook import LossHook
from .async_grpo import AsyncGrpoLoss
from .distillation import DistillationLoss
from .gkd import GkdLoss
from .gold import GoldLoss
from .grpo import GrpoLoss
from .rloo import RlooLoss
from .sft import SftLoss

HOOKS: tuple[type[LossHook], ...] = (GrpoLoss, RlooLoss, AsyncGrpoLoss, DistillationLoss, GkdLoss, GoldLoss, SftLoss)

__all__ = ["HOOKS", "pick_hook"]


def pick_hook(trainer: Any) -> tuple[type[LossHook] | None, list[str]]:
    """The hook for ``trainer``, else none and the trainer kind it cannot cover (an `UNSUPPORTED` key)."""
    by_name = {name: hook for hook in HOOKS for name in hook.names}
    for cls in type(trainer).__mro__:
        if cls.__name__ in UNSUPPORTED:
            return None, [cls.__name__]
        if cls.__name__ in by_name:
            hook = by_name[cls.__name__]
            owner = next((found for found in type(trainer).__mro__ if hook.loss_method in vars(found)), None)
            if owner is not cls:
                name = (owner or type(trainer)).__name__
                return None, [f"{name}{OVERRIDE_SUFFIX}{hook.loss_method}"]
            return hook, []
    return None, []
