# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class CompleteTrajectoryResponse(BaseModel):
  trajectory_id: str

  status: str
  """
    Trajectory status after completion was accepted. Both `completed` and `finalizing` mean
    the ending was accepted, so a harness can exit on either. `completed` means the capture
    is readable; `finalizing` means the platform is still building it and its steps are not
    readable yet. To read steps after `finalizing`, wait the `Retry-After` header's seconds,
    then poll `GET /api/v1/trajectories/{trajectory_id}?include_steps=false` with an API key
    until its status is `completed`.
    """
