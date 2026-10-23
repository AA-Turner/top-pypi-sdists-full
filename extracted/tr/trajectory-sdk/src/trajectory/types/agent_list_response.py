# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime

from trajectory._base_client import SyncPage
from trajectory._models import BaseModel


class AgentListItem(BaseModel):
  agent_id: str
  """Stable identifier for the agent."""

  organization_id: str
  """Organization that owns the agent."""

  name: str
  """Human-readable agent name."""

  description: str | None = None
  """Optional description of the agent's purpose."""

  created_at: datetime
  """Time the agent was created."""

  updated_at: datetime
  """Time the agent was last updated."""

  benchmark_count: int
  """Number of benchmark snapshots owned by the agent."""

  production_model_slug: str | None
  """The agent production model slug; independent of its display name."""

  is_deployed: bool
  """Whether the agent owns an active deployed model."""


class AgentListResponse(SyncPage[AgentListItem]):
  """Named response schema for the agent list endpoint."""

  items: list[AgentListItem]

  next_cursor: str | None = None

  has_more: bool

  total_count: int
  """Number of agents matching the search and filters."""
