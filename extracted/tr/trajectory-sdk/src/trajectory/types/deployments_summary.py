# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class DeploymentsSummary(BaseModel):
  """Lifecycle counts for the Deployments toolbar, kept off the paginated list."""

  total: int
  """All deployments in the organization."""

  pending: int
  """Deployments awaiting provisioning."""

  deploying: int
  """Deployments provisioning their Model Endpoint."""

  deployed: int
  """Deployments that finished deploying."""

  failed: int
  """Deployments that failed to become ready."""

  active: int
  """Deployments currently answering for their slug."""
