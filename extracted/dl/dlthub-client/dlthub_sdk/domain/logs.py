"""Log lines — what a run printed, historic or live."""

from __future__ import annotations

# Python internals
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any

# Current package
from dlthub_sdk._glue.context import _Ctx

if TYPE_CHECKING:
    # Typing only: domain never imports _gen at runtime.
    # Current package
    from dlthub_sdk._gen.logs.models import LogLine as LogLinePayload


@dataclass(frozen=True)
class LogLine:
    """One line a run emitted.

    Attributes:
        content: What was written.
        line_num: Its position in the run's log.
        phase: Which producer emitted it — ``program`` is the user's own code,
            and ``setup``, ``runner`` and ``provider`` are the platform's. A
            plain string, not an enum: the platform types it open so a producer
            can add one without older clients rejecting the line.
        reported_at: When the producer reported it.
    """

    content: str
    line_num: int
    phase: str
    reported_at: datetime

    @staticmethod
    def _from_payload(_ctx: _Ctx[Any], payload: LogLinePayload) -> LogLine:
        return LogLine(
            content=payload.content,
            line_num=payload.line_num,
            phase=payload.phase,
            reported_at=payload.reported_at,
        )
