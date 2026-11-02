"""matrx-connect lane — structured concurrency per user request.

One ``RequestLane`` per atomic user action (=cx_user_request.id). Owns every
async operation spawned during that action — reads, writes, tool calls,
labelers, sub-workflow steps. Provides:

- Strict priority queues (BLOCKING / NORMAL / DEFERRED)
- Per-lane bucket semaphores (db_write, ai_api, file_io, …) that cap fan-out
  per request — independent from matrx-orm's global write queue
- Drain protocol that lets DEFERRED tail work finish after the main task ends
- Transient-error retry gated by an opt-in ``retry_safe`` flag (callers assert
  the operation is idempotent)
- Context inheritance via a ContextVar, so child agents and parallel workflow
  steps automatically join the parent lane

Read /Users/armanisadeghi/.claude/plans/the-first-thing-we-lucky-pebble.md for
the full design doctrine.
"""

from matrx_connect.lane.contextvar import get_current_lane
from matrx_connect.lane.core import (
    Finalizer,
    FinalizerContext,
    LaneClosedError,
    LaneConfig,
    LaneDrainTimeoutError,
    RequestLane,
    configure,
    get_config,
)
from matrx_connect.lane.priorities import TaskPriority, TaskRecord

__all__ = [
    "Finalizer",
    "FinalizerContext",
    "LaneClosedError",
    "LaneConfig",
    "LaneDrainTimeoutError",
    "RequestLane",
    "TaskPriority",
    "TaskRecord",
    "configure",
    "get_config",
    "get_current_lane",
]
