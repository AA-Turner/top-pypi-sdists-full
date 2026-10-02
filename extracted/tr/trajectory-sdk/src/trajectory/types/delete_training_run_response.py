# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class DeleteTrainingRunResponse(BaseModel):
  training_run_id: str
  """ID of the deleted training run."""
