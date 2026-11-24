# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime
from typing import Literal

from trajectory._models import BaseModel
from trajectory.types.async_failure import AsyncFailure
from trajectory.types.recorded_run_options import RecordedRunOptions
from trajectory.types.rl.training_run_lifecycle_status import TrainingRunLifecycleStatus


class SftRecordedRunOptions(BaseModel):
  """
  What an SFT run records; values may lie outside the limits SftTrainingOptions launches
  with.
  """

  algorithm: Literal["sft"]

  dataset_id: str | None = None

  full_parameter: bool | None = None

  val_enabled: bool | None = None

  val_interval_steps: int | None = None

  learning_rate: float | None = None

  num_steps: int | None = None

  batch_size: int | None = None

  max_tokens_per_turn: int | None = None

  tokens_per_batch: int | None = None


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

  options: RecordedRunOptions | SftRecordedRunOptions

  created_by: str

  created_at: datetime

  failure: AsyncFailure | None = None
  """Structured failure when status is failed."""

  has_training_execution: bool
  """Whether a training execution has been assigned."""
