# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class HeldOutReward(BaseModel):
  step: int
  """Training step associated with this held-out reward."""

  held_out_reward: float
  """Held-out reward recorded for the step."""

  round_completed: bool | None = None
  """Whether evaluation scheduling finished; does not imply every sample succeeded."""

  expected_samples: int | None = None
  """Configured eval tasks times samples per task."""

  completed_samples: int | None = None
  """Samples marked completed before trajectory loading."""

  failed_samples: int | None = None
  """Samples marked failed; excluded from the loaded-trajectory mean."""

  cancelled_samples: int | None = None
  """Samples marked cancelled; excluded from the loaded-trajectory mean."""

  loaded_trajectories: int | None = None
  """Actual trajectory denominator of held_out_reward; may be smaller than expected_samples."""


class HeldOutRewardsByStepResponse(BaseModel):
  training_run_id: str
  """Training run whose held-out rewards are returned."""

  held_out_rewards: list[HeldOutReward]
  """Held-out rewards grouped by training step."""
