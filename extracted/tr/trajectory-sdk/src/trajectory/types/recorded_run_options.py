# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel
from trajectory.types.priority_aggregation import PriorityAggregation
from trajectory.types.priority_trait import PriorityTrait


class RecordedRunOptions(BaseModel):
  """Recorded settings retain values outside the public launch limits."""

  load_weights_only: bool | None = None

  density_aware_training: bool | None = None

  algorithm: str | None = None

  train_on_truncation: bool | None = None

  train_on_error: bool | None = None

  train_on_timeout: bool | None = None

  val_enabled: bool | None = None

  val_interval_steps: int | None = None

  val_num_tasks: int | None = None

  val_trajectories_per_task: int | None = None

  val_max_concurrent_trajectories: int | None = None

  val_final_wait_timeout_seconds: float | None = None

  learning_rate: float | None = None

  lr_warmup_steps: int | None = None

  lr_hold_steps: int | None = None

  lr_min_ratio: float | None = None

  reasoning_effort: (
    Literal["off", "on", "minimal", "low", "medium", "high", "xhigh", "max"] | None
  ) = None

  temperature: float | None = None

  top_p: float | None = None

  top_k: int | None = None

  val_reasoning_effort: (
    Literal["off", "on", "minimal", "low", "medium", "high", "xhigh", "max"] | None
  ) = None

  val_temperature: float | None = None

  val_top_p: float | None = None

  val_top_k: int | None = None

  val_max_output_tokens_per_turn: int | None = None

  val_max_output_tokens_per_trajectory: int | None = None

  val_max_turns_per_trajectory: int | None = None

  val_trajectory_timeout_seconds: int | None = None

  num_steps: int | None = None

  batch_size: int | None = None

  group_size: int | None = None

  priority_trait: PriorityTrait | None = None

  priority_aggregation: PriorityAggregation | None = None

  min_trajectories_per_group: int | None = None

  max_concurrent_trajectories: int | None = None

  max_staleness: int | None = None

  train_on_all_fail: bool | None = None

  train_on_all_pass: bool | None = None

  train_on_zero_advantage: bool | None = None

  trajectory_timeout_seconds: int | None = None

  batch_timeout_seconds: int | None = None

  max_output_tokens_per_turn: int | None = None

  max_output_tokens_per_trajectory: int | None = None

  max_turns_per_trajectory: int | None = None
