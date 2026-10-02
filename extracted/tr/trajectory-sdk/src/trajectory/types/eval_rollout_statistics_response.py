# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime

from trajectory._models import BaseModel


class EvalRolloutStatisticResponse(BaseModel):
  eval_run_id: str
  """Evaluation run that produced this snapshot."""

  stage: str
  """Pipeline stage that produced the trajectories."""

  knob_name: str
  """Trajectory setting represented by the distribution."""

  unit: str
  """Unit used by the setting and sample values."""

  samples: list[float] | None = None
  """Observed values."""

  sample_count: int
  """Number of trajectories sampled."""

  created_at: datetime
  """Time when the underlying evaluation completed."""


class EvalRolloutStatisticsResponse(BaseModel):
  eval_run_id: str
  """Evaluation run whose rollouts were sampled."""

  snapshots: list[EvalRolloutStatisticResponse]
  """Runtime-computed distributions for the evaluation."""
