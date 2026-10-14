# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory._models import BaseModel


class EvalTrajectoryReward(BaseModel):
  trajectory_id: str
  """Trajectory identifier."""

  reward: float
  """Reward assigned to the trajectory."""

  task_id: str | None = None
  """Benchmark task identifier, when one was recorded."""


class EvalTrajectoryRewardsPage(SyncPage[EvalTrajectoryReward]):
  items: list[EvalTrajectoryReward]

  next_cursor: str | None = None

  has_more: bool

  eval_run_id: str
  """Evaluation run whose trajectory rewards are returned."""
