# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime
from typing import Literal

from trajectory._models import BaseModel
from trajectory.types.async_failure import AsyncFailure


class DatasetOperation(BaseModel):
  """Asynchronous add of trajectories to a draft dataset."""

  operation_id: str
  """Identifier to poll for the add's status."""

  dataset_id: str
  """The draft the trajectories are added to."""

  status: Literal["queued", "running", "succeeded", "failed"]
  """queued until a worker starts it; the draft can be finalized once it has finished."""

  added_count: int
  """Trajectories added to the draft so far."""

  skipped_count: int
  """Selected trajectories skipped because the draft already had them."""

  error: AsyncFailure | None
  """Why the add failed, once failed; trajectories added before it stay."""

  source_errors: list[AsyncFailure]
  """Any failed run IDs and their failure reasons; trajectories from the other runs stay."""

  created_at: datetime
  """Time the add was accepted."""

  completed_at: datetime | None
  """Time the add succeeded or failed."""
