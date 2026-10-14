# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory._models import BaseModel


class TrajectoryReward(BaseModel):
  trajectory_id: str
  """Trajectory identifier."""

  reward: float
  """Reward assigned to the trajectory."""


class TrainingTrajectoryRewardsPage(SyncPage[TrajectoryReward]):
  items: list[TrajectoryReward]

  next_cursor: str | None = None

  has_more: bool

  training_run_id: str
  """Training run whose trajectory rewards are returned."""

  step: int
  """Training step used to select trajectories."""
