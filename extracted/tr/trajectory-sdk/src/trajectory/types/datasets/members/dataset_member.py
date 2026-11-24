# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel


class DatasetMember(BaseModel):
  trajectory_id: str

  split: Literal["train", "heldout"]

  source_type: str
  """Kind of source the trajectory was added from."""

  source_id: str
  """Identifier of the source the trajectory was added from."""

  reward: float
  """The attempt's reward when it was added."""
