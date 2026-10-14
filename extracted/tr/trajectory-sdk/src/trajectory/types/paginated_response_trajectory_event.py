# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory.types.trajectory_event import TrajectoryEvent


class PaginatedResponseTrajectoryEvent(SyncPage[TrajectoryEvent]):
  items: list[TrajectoryEvent]

  next_cursor: str | None = None

  has_more: bool
