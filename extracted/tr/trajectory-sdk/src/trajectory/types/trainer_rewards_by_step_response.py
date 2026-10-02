# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class TrainerReward(BaseModel):
  step: int
  """Training step associated with this trainer reward."""

  trainer_reward: float
  """Trainer reward recorded for the step."""


class TrainerRewardsByStepResponse(BaseModel):
  training_run_id: str
  """Training run whose trainer rewards are returned."""

  trainer_rewards: list[TrainerReward]
  """Trainer rewards grouped by training step."""
