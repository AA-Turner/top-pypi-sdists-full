# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class CompleteTrajectoryResponse(BaseModel):
  trajectory_id: str

  status: str
  """
    Trajectory status after completion was accepted: `completed` or `finalizing` are success
    states
    """
