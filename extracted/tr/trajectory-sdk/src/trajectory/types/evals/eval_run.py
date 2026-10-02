# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime

from trajectory._models import BaseModel
from trajectory.types.async_failure import AsyncFailure
from trajectory.types.evals.eval_run_lifecycle_status import EvalRunLifecycleStatus
from trajectory.types.run_options import RunOptions


class EvalRun(BaseModel):
  agent_id: str | None
  """Persisted owner; null for unassigned legacy runs."""

  eval_run_id: str
  """Unique evaluation run identifier."""

  bench_id: str
  """Benchmark evaluated by this run."""

  display_name: str | None
  """User-facing name for the evaluation run; null for legacy rows."""

  base_model_slug: str | None = None
  """Base model evaluated by this run."""

  options: RunOptions

  status: EvalRunLifecycleStatus | None
  """Current evaluation lifecycle status; null for legacy rows."""

  parent_checkpoint_id: str | None = None
  """Checkpoint evaluated by this run, when applicable."""

  training_run_id: str | None = None
  """Training run that produced the evaluated checkpoint."""

  step: int | None = None
  """Evaluated checkpoint training step."""

  reward_mean: float | None = None
  """Completed evaluation mean reward."""

  created_at: datetime
  """Time when the evaluation run was created."""

  updated_at: datetime
  """Time when the evaluation run was last updated."""

  completed_at: datetime | None = None
  """Time when the evaluation reached a terminal status."""

  failure: AsyncFailure | None = None
  """Structured failure when status is failed."""
