# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class TrajectoryTerminationSubreason(BaseModel):
  reason: str

  scope: str | None
  """Scope of the limiting budget, not which execution remains open."""
