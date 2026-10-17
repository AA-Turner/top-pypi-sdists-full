# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class CompleteTrajectoryResponse(BaseModel):
  trajectory_id: str

  status: str
  """
    Trajectory status after completion was accepted: `completed` once its capture is
    readable, or `finalizing` while the capture is still being built. Finalization continues
    durably: wait the `Retry-After` header's seconds, then poll `GET
    /api/v1/trajectories/{trajectory_id}?include_steps=false` until its status is
    `completed`.
    """
