# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime

from trajectory._models import BaseModel
from trajectory.types.async_failure import AsyncFailure
from trajectory.types.deployment_role import DeploymentRole
from trajectory.types.deployments.deployment_lifecycle_status import DeploymentLifecycleStatus


class Deployment(BaseModel):
  """Spanner-backed deployment lifecycle row for the platform UI."""

  deployment_id: str
  """Deployment row id."""

  agent_id: str | None = None
  """Owning agent; null for unassigned legacy deployments."""

  model_slug: str
  """Human-readable slug this deployment serves under."""

  model_slug_id: str
  """Id of the slug this deployment serves under."""

  status: DeploymentLifecycleStatus
  """Deployment lifecycle state."""

  role: DeploymentRole
  """Whether this is the production or a test deployment."""

  is_active: bool
  """True when this deployment currently answers for the slug."""

  checkpoint_id: str
  """Trajectory checkpoint selected when the deployment was created."""

  model_endpoint_id: str | None = None
  """Model Endpoint serving this deployment."""

  base_model_slug: str
  """Base model of the source checkpoint."""

  checkpoint_step: int
  """Training step of the source checkpoint."""

  created_by: str | None = None
  """Email of the user who requested this deployment."""

  completed_at: datetime | None = None
  """
    When the deployment first became DEPLOYED; unlike updated_at, later promote/demote
    transitions never overwrite this.
    """

  created_at: datetime
  """When the deployment was requested."""

  updated_at: datetime | None = None
  """Last lifecycle transition; null until the row first moves."""

  failure: AsyncFailure | None = None
  """Structured failure when status is FAILED."""
