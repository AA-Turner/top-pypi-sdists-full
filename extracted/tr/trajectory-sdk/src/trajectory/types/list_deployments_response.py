# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.deployments.deployment import Deployment


class ListDeploymentsResponse(BaseModel):
  items: list[Deployment]
  """Deployments on this page, newest first."""

  next_cursor: str | None = None
  """Cursor for the next page; null on the last page."""

  has_more: bool
  """True when another page is available."""
