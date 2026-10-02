# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.deployment_role import DeploymentRole


class StartDeployResponse(BaseModel):
  deployment_id: str

  role: DeploymentRole
