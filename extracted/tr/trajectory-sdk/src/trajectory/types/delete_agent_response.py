# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class DeleteAgentResponse(BaseModel):
  agent_id: str
  """ID of the deleted agent."""
