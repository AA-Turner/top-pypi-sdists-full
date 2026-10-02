# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime

from trajectory._models import BaseModel


class AgentResponse(BaseModel):
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

  benchmark_ids: list[str]
  """Benchmarks owned by the agent."""

  model_slug: str | None
  """The agent's stable serving model slug."""
