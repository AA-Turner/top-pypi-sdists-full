# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TypedDict


class AgentsUpdateParams(TypedDict, total=False):
  name: str
  """
  New agent name using only letters, digits, spaces, hyphens, underscores, and periods. Omit to
  leave unchanged.
  """
  description: str | None
  """
  New agent description. Set to null to clear it; omit to leave unchanged.
  """
  model_slug: str | None
  """
  Existing serving model slug in this organization. Set null to unassign it.
  """
