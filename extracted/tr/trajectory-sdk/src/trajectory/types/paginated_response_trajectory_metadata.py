# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.trajectory_metadata import TrajectoryMetadata


class PaginatedResponseTrajectoryMetadata(BaseModel):
  items: list[TrajectoryMetadata]

  next_cursor: str | None = None

  has_more: bool
