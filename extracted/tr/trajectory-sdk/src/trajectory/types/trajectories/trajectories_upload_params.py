# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Required, TypedDict


class TrajectoriesUploadParams(TypedDict, total=False):
  agent_id: Required[str]
  """
  Agent that owns the uploaded trajectories.
  """
  dataset: Required[str]
  """
  Dataset name to upload these trajectories into.
  """
  trajectories: Iterable[Mapping[str, Any]]
  """
  Trajectory payloads to validate, store, and index.
  """
