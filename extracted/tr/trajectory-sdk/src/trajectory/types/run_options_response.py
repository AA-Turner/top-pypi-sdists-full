# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, TypeAlias

from trajectory._models import BaseModel
from trajectory.types.base_model_slug import BaseModelSlug


class RunOptionMetadata(BaseModel):
  type: Literal["integer", "number", "boolean", "string"]

  min: float | None = None

  max: float | None = None

  default: bool | float | str | None

  choices: list[str] | None = None

  default_kind: Literal["fixed", "computed"]

  description: str


TrainingOptionKey: TypeAlias = Literal[
  "intelligent_density_training",
  "algorithm",
  "train_on_truncation",
  "train_on_error",
  "train_on_timeout",
  "reasoning_effort",
  "temperature",
  "top_p",
  "top_k",
  "evaluation_reasoning_effort",
  "evaluation_temperature",
  "evaluation_top_p",
  "evaluation_top_k",
  "reject_all_fail",
  "reject_all_pass",
  "reject_zero_advantage",
  "learning_rate",
  "lr_warmup_steps",
  "lr_hold_steps",
  "min_lr_ratio",
  "num_steps",
  "train_batch_size",
  "samples_per_instance",
  "max_active_rollouts",
  "max_steps_off_policy",
  "execution_timeout_seconds",
  "batch_collection_idle_timeout_seconds",
  "evaluation_enabled",
  "evaluation_frequency",
  "evaluation_max_samples",
  "evaluation_samples_per_task",
  "evaluation_max_active_rollouts",
  "evaluation_collection_timeout_seconds",
  "max_output_tokens_per_step",
  "max_total_tokens_per_trajectory",
  "max_turns_per_trajectory",
]


class ModelRunOptions(BaseModel):
  base_model_slug: BaseModelSlug

  options: dict[str, RunOptionMetadata]


class RunOptionsResponse(BaseModel):
  bench_id: str

  models: list[ModelRunOptions]
