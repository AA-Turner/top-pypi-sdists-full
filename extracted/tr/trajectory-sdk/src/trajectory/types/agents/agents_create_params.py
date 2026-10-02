# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Required, TypedDict


class AgentsCreateParams(TypedDict, total=False):
  name: Required[str]
  """
  Agent name, unique within the organization. Only letters, digits, spaces, hyphens,
  underscores, and periods.
  """
  description: str | None
  """
  Optional description of the agent's purpose.
  """
