# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.trajectory_event import TrajectoryEvent


class PaginatedResponseTrajectoryEvent(BaseModel):
  items: list[TrajectoryEvent]

  next_cursor: str | None = None

  has_more: bool
