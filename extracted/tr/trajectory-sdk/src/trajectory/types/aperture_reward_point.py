# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class ApertureRewardPoint(BaseModel):
  step: int

  avg_reward: float

  trajectory_count: int

  pending_count: int
