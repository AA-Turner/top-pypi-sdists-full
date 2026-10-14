# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory.types.agents.agent_response import AgentResponse


class AgentListResponse(SyncPage[AgentResponse]):
  """Named response schema for the agent list endpoint."""

  items: list[AgentResponse]

  next_cursor: str | None = None

  has_more: bool
