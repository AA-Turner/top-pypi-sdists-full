# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.async_failure import AsyncFailure
from trajectory.types.evals.eval_run_lifecycle_status import EvalRunLifecycleStatus


class EvalLiveSummary(BaseModel):
  waiting_rollouts: int
  """Attempts waiting to execute, including startup work."""

  running_rollouts: int
  """Active attempts executing or being stopped."""

  awaiting_result_rollouts: int
  """Finished captures awaiting cleanup, scoring, or outcome reconciliation."""

  scored_rollouts: int
  """Completed attempts with a selected numeric score."""

  failed_rollouts: int
  """Attempts that failed execution or scoring."""

  cancelled_rollouts: int
  """Attempts whose cancellation is complete."""

  provisional_reward_mean: float | None
  """Mean of the scored attempts; null before the first score."""

  final_reward_mean: float | None
  """Authoritative mean when the evaluation completed successfully."""


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

  live: EvalLiveSummary | None = None
  """
    Consistent execution and scoring snapshot for native evaluations; absent for historical
    runs.
    """
