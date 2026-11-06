# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, TypeAlias

from trajectory._models import BaseModel
from trajectory.types.base_model_slug import BaseModelSlug


class RunOptionMetadata(BaseModel):
  type: Literal["integer", "number", "boolean", "string"]

  min: float | None = None

  max: float | None = None

  default: bool | int | float | str | None

  choices: list[str] | None = None

  default_kind: Literal["fixed", "computed"]

  description: str


TrainingOptionKey: TypeAlias = Literal[
  "density_aware_training",
  "algorithm",
  "train_on_truncation",
  "train_on_error",
  "train_on_timeout",
  "reasoning_effort",
  "temperature",
  "top_p",
  "top_k",
  "val_reasoning_effort",
  "val_temperature",
  "val_top_p",
  "val_top_k",
  "val_max_output_tokens_per_turn",
  "val_max_output_tokens_per_trajectory",
  "val_max_turns_per_trajectory",
  "val_trajectory_timeout_seconds",
  "train_on_all_fail",
  "train_on_all_pass",
  "train_on_zero_advantage",
  "learning_rate",
  "lr_warmup_steps",
  "lr_hold_steps",
  "lr_min_ratio",
  "num_steps",
  "batch_size",
  "min_trajectories_per_group",
  "group_size",
  "max_concurrent_trajectories",
  "max_staleness",
  "trajectory_timeout_seconds",
  "batch_timeout_seconds",
  "val_enabled",
  "val_interval_steps",
  "val_num_tasks",
  "val_trajectories_per_task",
  "val_max_concurrent_trajectories",
  "val_final_wait_timeout_seconds",
  "max_output_tokens_per_turn",
  "max_output_tokens_per_trajectory",
  "max_turns_per_trajectory",
]


class ModelRunOptions(BaseModel):
  base_model_slug: BaseModelSlug

  options: dict[str, RunOptionMetadata]


class RunOptionsResponse(BaseModel):
  bench_id: str = ""
  """Deprecated and always empty; run options are the same for every benchmark."""

  models: list[ModelRunOptions]
