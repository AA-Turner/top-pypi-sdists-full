# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Required, TypedDict


class DatasetsCreateParams(TypedDict, total=False):
  agent_id: str | None
  """
  The dataset's agent ID. Provide agent_id or agent_name.
  """
  agent_name: str | None
  """
  The dataset's agent name. Provide agent_id or agent_name.
  """
  name: Required[str]
  """
  Dataset name; datasets that share a name are versions of it. Only letters, digits, spaces,
  hyphens, underscores, and periods.
  """
