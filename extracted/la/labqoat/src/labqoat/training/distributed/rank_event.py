"""Typed local rank progress on an invocation-owned process channel."""

from dataclasses import dataclass
from typing import Literal

from labqoat.json_document import JsonDocument
from labqoat.training.recovery.restore_state import RestoreState


@dataclass(frozen=True)
class RankEvent:
    """Keep actual restoration and terminal results distinct from permission to train."""

    rank: int
    phase: Literal["restored", "completed", "failed"]
    state: RestoreState | None = None
    output: JsonDocument | None = None
    reason: str = ""
