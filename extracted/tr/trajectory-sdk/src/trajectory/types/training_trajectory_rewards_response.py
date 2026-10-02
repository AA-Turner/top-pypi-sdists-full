# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class TrajectoryReward(BaseModel):
  trajectory_id: str | None = None
  """Trajectory identifier, when one was recorded."""

  reward: float
  """Reward assigned to the trajectory."""


class TrainingTrajectoryRewardsResponse(BaseModel):
  training_run_id: str
  """Training run whose trajectory rewards are returned."""

  step: int
  """Training step used to select trajectories."""

  trajectory_rewards: list[TrajectoryReward]
  """Per-trajectory rewards recorded for the selected training step."""
