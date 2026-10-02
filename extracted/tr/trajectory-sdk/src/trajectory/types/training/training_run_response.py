# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime

from trajectory._models import BaseModel
from trajectory.types.async_failure import AsyncFailure
from trajectory.types.run_options import RunOptions
from trajectory.types.training.training_run_lifecycle_status import TrainingRunLifecycleStatus


class TrainingRunResponse(BaseModel):
  agent_id: str | None
  """Persisted owner; null for unassigned legacy runs."""

  parent_checkpoint_id: str | None = None

  training_run_id: str

  pipeline_run_id: str | None

  display_name: str | None
  """User-facing training run name; null for legacy rows."""

  status: TrainingRunLifecycleStatus

  bench_id: str | None

  base_model_slug: str

  options: RunOptions

  created_by: str

  created_at: datetime

  failure: AsyncFailure | None = None
  """Structured failure when status is failed."""

  has_training_execution: bool
  """Whether a training execution has been assigned."""
