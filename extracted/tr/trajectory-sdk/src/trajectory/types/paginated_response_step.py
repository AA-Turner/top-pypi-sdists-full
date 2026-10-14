# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory.types.trajectories.steps.step import Step


class PaginatedResponseStep(SyncPage[Step]):
  items: list[Step]

  next_cursor: str | None = None

  has_more: bool
