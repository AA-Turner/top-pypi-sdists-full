# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class CreateTrajectoryResponse(BaseModel):
  tid: str
  """ID of the created or existing trajectory."""
