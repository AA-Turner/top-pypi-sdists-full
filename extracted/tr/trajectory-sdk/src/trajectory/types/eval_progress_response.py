# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.async_failure import AsyncFailure
from trajectory.types.evals.eval_run_lifecycle_status import EvalRunLifecycleStatus


class EvalProgressResponse(BaseModel):
  eval_run_id: str
  """Evaluation run whose progress is returned."""

  status: EvalRunLifecycleStatus | None = None
  """Recorded status of the evaluation run."""

  failure: AsyncFailure | None = None
  """Structured failure details when the evaluation failed."""

  terminal_rollouts: int
  """Rollouts of the run that have reached a terminal status."""

  total_rollouts: int
  """Rollouts the run's config schedules: its sampled tasks times the group size."""
