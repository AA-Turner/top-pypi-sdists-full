# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime

from trajectory._models import BaseModel


class TrainingCheckpointResponse(BaseModel):
  training_run_id: str

  step_index: int
  """
    Training step whose committed checkpoint was resolved; step 0 precedes optimizer
    updates.
    """

  checkpoint_id: str
  """Committed checkpoint id for deploy or checkpoint eval."""

  base_model_slug: str
  """Base model slug the checkpoint was trained from."""

  created_at: datetime
  """Time the checkpoint was created, in UTC."""

  is_deployable: bool = False
  """Whether the checkpoint has saved Tinker weights for serving."""
