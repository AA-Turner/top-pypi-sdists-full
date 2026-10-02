# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class LogTrajectoryRewardResponse(BaseModel):
  ok: bool
  """True when the reward was stored or already present."""

  trajectory_id: str

  status: str
  """Current trajectory status after the write."""
