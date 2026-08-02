# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

# COMPAT_MIGRATION_TARGET: onex_change_control.models.pricing.model_llm_pricing
# COMPAT_REMOVAL_DATE: 2026-12-01

"""ModelLlmPricing — per-LLM token and runner cost declaration."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ModelLlmPricing(BaseModel):
    """Per-LLM token and infrastructure cost declaration.

    All costs are non-negative. runner_cost_per_hour covers GPU/CPU
    infrastructure amortized per hour; zero for cloud-billed models.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    input_cost_per_1k_tokens: float = Field(..., ge=0.0)
    output_cost_per_1k_tokens: float = Field(..., ge=0.0)
    runner_cost_per_hour: float = Field(default=0.0, ge=0.0)


__all__: list[str] = ["ModelLlmPricing"]
