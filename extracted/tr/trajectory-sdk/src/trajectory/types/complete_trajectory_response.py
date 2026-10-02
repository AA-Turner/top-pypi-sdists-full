# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class CompleteTrajectoryResponse(BaseModel):
  trajectory_id: str

  status: str
  """Terminal trajectory status after completion."""
