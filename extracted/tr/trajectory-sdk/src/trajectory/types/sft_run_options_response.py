# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, TypeAlias

from trajectory._models import BaseModel
from trajectory.types.base_model_slug import BaseModelSlug
from trajectory.types.run_option_metadata import RunOptionMetadata

SftTrainingOptionKey: TypeAlias = Literal[
  "val_enabled",
  "val_interval_steps",
  "learning_rate",
  "num_steps",
  "batch_size",
  "max_tokens_per_turn",
]


class SftModelRunOptions(BaseModel):
  base_model_slug: BaseModelSlug

  options: dict[str, RunOptionMetadata]


class SftRunOptionsResponse(BaseModel):
  models: list[SftModelRunOptions]
