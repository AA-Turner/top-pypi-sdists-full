"""The TRL trainer kinds a tracker records, picked once by the trainer's class chain (RL plan §6.6). Nothing from TRL
is imported: a class is matched by name, the nearest first, so a subclass records as its parent."""

from __future__ import annotations

from typing import Any

from ..recorder import Recorder
from .async_queue import AsyncQueueRecorder
from .distillation import DistillationRecorder
from .gkd import GkdRecorder
from .gold import GoldRecorder
from .grpo import GrpoRecorder
from .sft import SftRecorder

#: Every kind; `SftRecorder` only with `record_sft=True`.
RECORDERS: tuple[type[Recorder], ...] = (
    GrpoRecorder, AsyncQueueRecorder, DistillationRecorder, GkdRecorder, GoldRecorder, SftRecorder,
)

__all__ = ["RECORDERS", "is_sft_trainer", "pick_recorder"]


def pick_recorder(trainer: Any, *, should_record_sft: bool) -> type[Recorder] | None:
    """The recorder for ``trainer``: the first class along its chain one recorder names."""
    by_name = {name: recorder for recorder in RECORDERS for name in recorder.names}
    for cls in type(trainer).__mro__:
        recorder = by_name.get(cls.__name__)
        if recorder is SftRecorder and not should_record_sft:
            return None
        if recorder is not None:
            return recorder
    return None


def is_sft_trainer(trainer: Any) -> bool:
    """Is ``trainer`` an SFTTrainer by the same rule: the nearest class along its chain a recorder names is
    SFTTrainer (GKD subclasses SFTTrainer and stays a distillation trainer)."""
    by_name = {name: recorder for recorder in RECORDERS for name in recorder.names}
    for cls in type(trainer).__mro__:
        recorder = by_name.get(cls.__name__)
        if recorder is not None:
            return recorder is SftRecorder
    return False
