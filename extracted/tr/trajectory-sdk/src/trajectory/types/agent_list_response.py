# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.agents.agent_response import AgentResponse


class AgentListResponse(BaseModel):
  """Named response schema for the agent list endpoint."""

  items: list[AgentResponse]

  next_cursor: str | None = None

  has_more: bool
