# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory.types.trajectory_metadata import TrajectoryMetadata


class PaginatedResponseTrajectoryMetadata(SyncPage[TrajectoryMetadata]):
  items: list[TrajectoryMetadata]

  next_cursor: str | None = None

  has_more: bool
