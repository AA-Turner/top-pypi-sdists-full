# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class TrainingCheckpointResponse(BaseModel):
  training_run_id: str

  step_index: int
  """Training step whose committed checkpoint was resolved."""

  checkpoint_id: str
  """Committed checkpoint id for deploy or checkpoint eval."""

  base_model_slug: str
  """Base model slug the checkpoint was trained from."""

  is_deployable: bool = False
  """Whether the checkpoint has restorable Tinker state for deployment."""
