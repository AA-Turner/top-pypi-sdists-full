# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.async_failure import AsyncFailure
from trajectory.types.training.training_run_lifecycle_status import TrainingRunLifecycleStatus


class TrainingProgressResponse(BaseModel):
  training_run_id: str
  """Training run whose progress is returned."""

  status: TrainingRunLifecycleStatus
  """Recorded status of the training run."""

  failure: AsyncFailure | None = None
  """Structured failure details when the training run failed."""

  completed_steps: int
  """Training steps of the run that have recorded a trainer metric."""

  total_steps: int | None = None
  """Steps the run's config budgets, or null when it set no budget."""
