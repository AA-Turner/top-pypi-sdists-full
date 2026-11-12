# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, TypeAlias

from trajectory._models import BaseModel
from trajectory.types.base_model_slug import BaseModelSlug

InputModality: TypeAlias = Literal["text", "image"]


class ModelPricing(BaseModel):
  input: float

  output: float


class SupportedModelInfo(BaseModel):
  base_model_slug: BaseModelSlug

  model_name: str

  pricing: ModelPricing

  checkpoint: str | None = None
  """
    Upstream checkpoint that runs and trains this model, when Trajectory hosts it. It can
    differ from base_model_slug, for example a vision-language build of the same weights.
    Null for models served by an external API.
    """

  max_context_tokens: int | None = None
  """
    Largest prompt plus completion, in tokens, a single sampling call accepts. Null when the
    provider sets the limit.
    """

  input_modalities: list[InputModality]
  """Content parts the model accepts in chat completions; image marks vision models."""


class ListSupportedModelsResponse(BaseModel):
  items: list[SupportedModelInfo]
