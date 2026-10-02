# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class EvalTrajectoryReward(BaseModel):
  trajectory_id: str | None = None
  """Trajectory identifier, when one was recorded."""

  reward: float
  """Reward assigned to the trajectory."""

  task_id: str | None = None
  """Benchmark task identifier, when one was recorded."""


class EvalTrajectoryRewardsResponse(BaseModel):
  eval_run_id: str
  """Evaluation run whose trajectory rewards are returned."""

  trajectory_rewards: list[EvalTrajectoryReward]
  """Per-trajectory rewards recorded for the evaluation run."""
