# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.base_model_slug import BaseModelSlug


class ModelPricing(BaseModel):
  input: float

  output: float

  cached_input: float | None = None


class SupportedModelInfo(BaseModel):
  base_model_slug: BaseModelSlug

  model_name: str

  pricing: ModelPricing


class ListSupportedModelsResponse(BaseModel):
  items: list[SupportedModelInfo]
