# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from trajectory._models import BaseModel


class DatasetVersion(BaseModel):
  dataset_id: str
  """Identifier of this dataset version."""

  agent_id: str | None
  """The agent that owns the dataset; null for datasets created before agents owned them."""

  name: str
  """Dataset name shared by its versions."""

  status: Literal["draft", "finalized"]
  """`draft` state allows trajectories to be added; `finalized` can be used for training."""

  created_at: datetime
  """Time the draft was created."""

  finalized_at: datetime | None
  """Time the version was finalized; the newest finalized version is the name's latest."""

  train_count: int
  """Number of train trajectories."""

  heldout_count: int
  """Number of heldout trajectories."""

  lineage: list[dict[str, Any]]
  """Each finished add or copy: its runs or source dataset, filter and count added."""
