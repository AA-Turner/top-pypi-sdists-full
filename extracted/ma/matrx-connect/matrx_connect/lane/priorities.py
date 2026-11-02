from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any


class TaskPriority(IntEnum):
    """Strict priority tiers inside a RequestLane.

    Workers pull tasks in numeric order — lower wins — so BLOCKING always
    runs before NORMAL, which always runs before DEFERRED. A flood of
    DEFERRED labelers can never starve a BLOCKING persist.
    """

    BLOCKING = 0
    NORMAL = 1
    DEFERRED = 2


@dataclass(slots=True)
class TaskRecord:
    """Bookkeeping for one task submitted to a lane.

    Retained for the lifetime of the lane (capped via LaneConfig.max_task_records)
    so observability endpoints can answer "what is request X doing right now".
    """

    id: str
    name: str
    priority: TaskPriority
    bucket: str
    coalesce_key: str | None
    retry_safe: bool
    submitted_at: float
    started_at: float | None = None
    completed_at: float | None = None
    attempts: int = 0
    status: str = "queued"  # queued | running | succeeded | failed | cancelled
    error_class: str | None = None
    error_msg: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)
