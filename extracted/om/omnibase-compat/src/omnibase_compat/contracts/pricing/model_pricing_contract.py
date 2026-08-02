# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

# COMPAT_MIGRATION_TARGET: onex_change_control.models.pricing.model_pricing_contract
# COMPAT_REMOVAL_DATE: 2026-12-01

"""ModelPricingContract — versioned pricing contract wire DTO."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType

from pydantic import BaseModel, ConfigDict, Field, model_validator

from omnibase_compat.contracts.pricing.model_llm_pricing import ModelLlmPricing


class ModelPricingContract(BaseModel):
    """Versioned contract declaring per-LLM costs and savings methodology.

    Frozen so contract declarations are immutable after parse. Each projection
    row records the pricing contract version to enable auditable savings replay.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str = Field(..., min_length=1)
    version: int = Field(..., ge=1)
    baseline_model: str = Field(..., min_length=1)
    savings_method: str = Field(..., min_length=1)
    models: Mapping[str, ModelLlmPricing] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _freeze_models_mapping(self) -> ModelPricingContract:
        object.__setattr__(self, "models", MappingProxyType(dict(self.models)))
        return self

    @model_validator(mode="after")
    def _validate_baseline_model_in_models(self) -> ModelPricingContract:
        if self.models and self.baseline_model not in self.models:
            raise ValueError(f"baseline_model '{self.baseline_model}' must be a key in models")
        return self


__all__: list[str] = ["ModelPricingContract"]
