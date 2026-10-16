# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any

from trajectory._models import BaseModel
from trajectory.types.trajectories.steps.step import Step
from trajectory.types.trajectory_rollout_status import TrajectoryRolloutStatus


class RewardComponent(BaseModel):
  name: str
  """Reward component name."""

  value: float
  """Raw value as logged."""

  scaled_value: float
  """Value scaled to [0, 1]: (value - score_range_min) / (score_range_max - score_range_min)."""

  weight: float
  """Weight of this component in the logged reward."""

  score_range_min: float

  score_range_max: float

  explanation: str | None = None


class Trajectory(BaseModel):
  trajectory_id: str

  organization_id: str

  dataset_id: str | None = None

  dataset_name: str | None = None

  dataset_source: str | None = None

  dataset_gcs_prefix: str | None = None

  trace_id: str | None = None

  model_id: str | None = None

  model_association_source: str | None = None

  model_association_metadata: dict[str, Any] | None = None

  source: str

  status: str | None = None

  reward: float | None = None

  num_steps: int | None = None

  created_at: str

  training_run_id: str | None = None

  task_id: str | None = None

  policy_step: int | None = None
  """Sampled policy step, not optimizer step."""

  rollout: TrajectoryRolloutStatus | None = None

  gcs_blob_uri: str | None = None

  error: str | None = None

  steps: list[Step] | None = None

  reward_components: list[RewardComponent] | None = None
  """Logged reward components, in logged order."""
