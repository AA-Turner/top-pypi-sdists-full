# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TypedDict


class TrajectoriesCreateParams(TypedDict, total=False):
  agent_id: str | None
  """
  Optional agent ID to associate with the trajectory. When omitted for a new trajectory, no
  agent is assigned. When a Model Endpoint session token references an existing trajectory,
  omitting this field leaves its existing agent association unchanged.
  """
