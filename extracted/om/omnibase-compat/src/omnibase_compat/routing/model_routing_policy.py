# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

# COMPAT_MIGRATION_TARGET: omnibase_core.models.routing.model_routing_policy
# COMPAT_REMOVAL_DATE: 2026-10-01

"""ModelRoutingPolicy — contract-declared LLM routing policy.

Declared in a node's contract.yaml under the `model_routing` key.
No model IDs, base URLs, or timeouts appear in handler source — they are
resolved at runtime from model_registry.yaml via the model_id keys declared here.
"""

from __future__ import annotations

from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ModelCiOverridePolicy(BaseModel):
    """CI-mode override: when ONEX_CI_MODE=true, use this primary model_id instead."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    primary: str = Field(..., description="model_id key to use in CI mode.")


class ModelRoutingPolicy(BaseModel):
    """Contract-declared LLM routing policy for a node handler.

    Frozen + extra=forbid so contract declarations are immutable and typos fail
    loudly at parse time rather than silently using defaults.

    Timeout math invariant: total_budget = timeout_per_attempt_s * max_retries.
    Never compute as total / retries.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    primary: str = Field(..., description="model_id key (e.g. 'qwen3-coder-30b').")
    fallback: str | None = Field(
        default=None,
        description="model_id key for fallback. Required when fallback_allowed_roles non-empty.",
    )
    timeout_per_attempt_s: float = Field(
        default=30.0,
        description="Per-attempt budget in seconds. Total = timeout_per_attempt_s * max_retries.",
        gt=0,
    )
    max_retries: int = Field(
        default=2,
        description="Maximum number of retry attempts per request.",
        ge=1,
    )
    reason_for_fallback: str = Field(
        default="",
        description="Required when fallback is declared. Describes why fallback may be needed.",
    )
    fallback_allowed_roles: list[str] = Field(
        default_factory=list,
        description=(
            "Roles permitted to trigger fallback (e.g. ['reviewer','designer','fixer']). "
            "Empty list = no fallback for any role."
        ),
    )
    max_tokens: int = Field(
        default=4096,
        description="Maximum tokens in the model response.",
        gt=0,
    )
    temperature: float = Field(
        default=0.2,
        description="Sampling temperature.",
        ge=0.0,
        le=2.0,
    )
    call_style: Literal["sync", "async"] = Field(
        default="async",
        description="Whether to invoke the model synchronously or asynchronously.",
    )
    ci_override: ModelCiOverridePolicy | None = Field(
        default=None,
        description="Override policy applied when ONEX_CI_MODE=true.",
    )

    @model_validator(mode="after")
    def _fallback_required_when_roles_declared(self) -> Self:
        if self.fallback_allowed_roles and self.fallback is None:
            msg = "fallback must be set when fallback_allowed_roles is non-empty"
            raise ValueError(msg)
        return self


__all__: list[str] = [
    "ModelCiOverridePolicy",
    "ModelRoutingPolicy",
]
