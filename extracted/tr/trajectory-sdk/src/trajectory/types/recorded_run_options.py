# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.training_algorithm import TrainingAlgorithm


class RecordedRunOptions(BaseModel):
  """Recorded settings retain values outside the public launch limits."""

  intelligent_density_training: bool | None = None

  algorithm: TrainingAlgorithm | None = None

  train_on_truncation: bool | None = None

  train_on_error: bool | None = None

  train_on_timeout: bool | None = None

  evaluation_max_samples: int | None = None

  evaluation_samples_per_task: int | None = None

  evaluation_max_active_rollouts: int | None = None

  evaluation_collection_timeout_seconds: float | None = None

  learning_rate: float | None = None

  lr_warmup_steps: int | None = None

  lr_hold_steps: int | None = None

  min_lr_ratio: float | None = None

  disable_thinking: bool | None = None

  num_steps: int | None = None

  train_batch_size: int | None = None

  samples_per_instance: int | None = None

  n_parallel_agents: int | None = None

  execution_timeout_seconds: int | None = None

  batch_collection_idle_timeout_seconds: int | None = None

  max_output_tokens_per_step: int | None = None

  max_total_tokens_per_trajectory: int | None = None

  max_turns_per_trajectory: int | None = None
