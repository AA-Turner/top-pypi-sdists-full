# SPDX-FileCopyrightText: 2026 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_core.models.delegation.wire
# COMPAT_REMOVAL_DATE: 2026-12-01

"""Strict v2 terminal transport DTOs for the delegation bus seam.

V2 deliberately has no v1 upcast path.  Producers must stamp the routing
disposition and, when routed, the stable backend identity and route-time
pricing-manifest version that produced the terminal record.
"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Annotated, Literal, Self
from urllib.parse import urlparse
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


@unique
class EnumDelegationRoutingDisposition(StrEnum):
    """Whether a terminal result reached a selected delegation backend."""

    ROUTED = "routed"
    UNROUTED = "unrouted"


@unique
class EnumDelegationTerminalOutcome(StrEnum):
    """Authoritative terminal outcome emitted by the producing boundary."""

    COMPLETED = "completed"
    FAILED = "failed"


@unique
class EnumDelegationTerminalFailureCause(StrEnum):
    """Mirror of the existing typed provider failure-cause vocabulary."""

    PROVIDER_QUOTA_EXHAUSTED = "provider_quota_exhausted"
    AUTH_FAILED = "auth_failed"
    PROVIDER_ERROR = "provider_error"


@unique
class EnumDelegationUnroutedReason(StrEnum):
    """Closed reasons for a terminal that never selected a backend."""

    NO_ELIGIBLE_BACKEND = "no_eligible_backend"
    ROUTING_POLICY_REJECTED = "routing_policy_rejected"
    ROUTING_CONFIGURATION_INVALID = "routing_configuration_invalid"


@unique
class EnumQualityScoreComparison(StrEnum):
    """Mirror of the existing typed relationship between a score and its bar."""

    BELOW_BAR = "below_bar"
    AT_OR_ABOVE_BAR = "at_or_above_bar"


class _ModelDelegationTerminalCommonV2(BaseModel):
    """Fields shared by every v2 terminal, retained from the v1 terminal seam."""

    model_config = ConfigDict(frozen=True, extra="forbid", from_attributes=True)

    correlation_id: UUID = Field(..., description="Delegation correlation identity.")
    task_type: str = Field(..., min_length=1, description="Original task classification.")
    model_used: str = Field(
        ...,
        description="Producer-stamped model diagnostic; never routing authority.",
    )
    endpoint_url: str = Field(
        ...,
        description="Producer-stamped endpoint diagnostic; never routing authority.",
    )
    terminal_outcome: EnumDelegationTerminalOutcome = Field(
        ..., description="Producer-stamped terminal outcome."
    )
    content: str = Field(..., description="Terminal response content; may be empty on failure.")
    quality_passed: bool = Field(..., description="Authoritative quality-gate verdict.")
    quality_score: float = Field(..., ge=0.0, le=1.0, description="Quality score from 0 to 1.")
    required_quality_bar: float | None = Field(
        ..., ge=0.0, le=1.0, description="Applied quality bar, if one was evaluated."
    )
    score_vs_required_bar: EnumQualityScoreComparison | None = Field(
        ..., description="Typed score/bar relationship, if a bar was evaluated."
    )
    failed_acceptance_criteria: tuple[str, ...] = Field(
        ..., description="Authoritative failed quality criteria."
    )
    latency_ms: int = Field(..., ge=0, description="End-to-end terminal latency.")
    prompt_tokens: int = Field(..., ge=0, description="Prompt-token count.")
    completion_tokens: int = Field(..., ge=0, description="Completion-token count.")
    total_tokens: int = Field(..., ge=0, description="Total token count.")
    fallback_to_claude: bool = Field(..., description="Whether Claude fallback was used.")
    failure_reason: str = Field(..., description="Human-readable failure detail, if any.")
    tokens_to_compliance: int = Field(..., ge=0, description="Tokens consumed to compliance.")
    compliance_attempts: int = Field(..., ge=1, description="Inference calls to compliance.")
    escalation_count: int = Field(..., ge=0, description="Number of tier escalations.")
    escalation_history: tuple[dict[str, object], ...] = Field(
        ..., description="Existing serialized escalation history without v2 reinterpretation."
    )
    terminal_failure_reason: str | None = Field(
        ..., description="Terminal failure reason, if one was produced."
    )
    terminal_failure_cause: EnumDelegationTerminalFailureCause | None = Field(
        ..., description="Typed provider failure cause, if one was produced."
    )
    routing_tiers_hash: str | None = Field(
        ..., description="Routing-tiers contract hash, if producer-stamped."
    )
    escalation_config_hash: str | None = Field(
        ..., description="Escalation-config hash, if producer-stamped."
    )
    attempts_count: int = Field(..., ge=1, description="Authoritative total delegation attempts.")
    cumulative_attempt_cost: float = Field(..., ge=0.0, description="Cumulative attempt cost.")
    cumulative_input_tokens: int = Field(..., ge=0, description="Cumulative input tokens.")
    cumulative_output_tokens: int = Field(..., ge=0, description="Cumulative output tokens.")
    final_attempt_cost: float = Field(..., ge=0.0, description="Final attempt cost.")
    context_pack_hash: str = Field(..., description="Context-pack hash, if any.")
    cost_tier_name: str = Field(..., description="Authoritative serving cost-tier name, if any.")
    tenant_id: str | None = Field(..., description="Resolved tenant identity, if any.")

    @model_validator(mode="after")
    def validate_common_terminal_truth(self) -> Self:
        """Preserve the existing common terminal invariants without defaults."""
        if self.total_tokens != self.prompt_tokens + self.completion_tokens:
            msg = "total_tokens must equal prompt_tokens + completion_tokens"
            raise ValueError(msg)
        if any(not criterion.strip() for criterion in self.failed_acceptance_criteria):
            msg = "failed_acceptance_criteria entries must not be blank"
            raise ValueError(msg)

        required_bar = self.required_quality_bar
        comparison = self.score_vs_required_bar
        if (required_bar is None) != (comparison is None):
            msg = "required_quality_bar and score_vs_required_bar must be provided together"
            raise ValueError(msg)
        if required_bar is not None and comparison is not None:
            expected = (
                EnumQualityScoreComparison.BELOW_BAR
                if self.quality_score < required_bar
                else EnumQualityScoreComparison.AT_OR_ABOVE_BAR
            )
            if comparison is not expected:
                msg = "score_vs_required_bar must match quality_score and required_quality_bar"
                raise ValueError(msg)
            if comparison is EnumQualityScoreComparison.BELOW_BAR and self.quality_passed:
                msg = "quality_passed terminal cannot be below required_quality_bar"
                raise ValueError(msg)
            if (
                comparison is EnumQualityScoreComparison.AT_OR_ABOVE_BAR
                and not self.quality_passed
                and not self.failed_acceptance_criteria
            ):
                msg = "quality-failed terminal at or above required_quality_bar requires criteria"
                raise ValueError(msg)
        if self.quality_passed and self.failed_acceptance_criteria:
            msg = "quality_passed terminal cannot carry failed_acceptance_criteria"
            raise ValueError(msg)
        if self.quality_passed and self.terminal_failure_cause is not None:
            msg = "quality_passed terminal cannot carry terminal_failure_cause"
            raise ValueError(msg)
        return self


class ModelDelegationTerminalRoutedV2(_ModelDelegationTerminalCommonV2):
    """Terminal whose routing boundary selected a stable backend identity."""

    routing_disposition: Literal[EnumDelegationRoutingDisposition.ROUTED] = Field(
        ..., description="Confirms that a backend was selected."
    )
    backend_ref: str = Field(
        ..., min_length=1, description="Stable selected backend reference, never a URL."
    )
    pricing_manifest_version: int = Field(
        ..., gt=0, description="Positive route-time pricing manifest version."
    )

    @field_validator("backend_ref")
    @classmethod
    def validate_backend_ref(cls, value: str) -> str:
        """Reject URI-shaped values and preserve stable backend-id references."""
        if value != value.strip() or not value:
            msg = "backend_ref must be nonblank and must not have surrounding whitespace"
            raise ValueError(msg)
        parsed = urlparse(value)
        if parsed.scheme or parsed.netloc:
            msg = "backend_ref must be a stable backend reference, not a URL or URI"
            raise ValueError(msg)
        return value

    @model_validator(mode="after")
    def validate_routed_terminal_truth(self) -> Self:
        """Completed terminals are necessarily routed and quality-accepted."""
        if (
            self.terminal_outcome is EnumDelegationTerminalOutcome.COMPLETED
            and not self.quality_passed
        ):
            msg = "completed routed terminal requires quality_passed=true"
            raise ValueError(msg)
        return self


class ModelDelegationTerminalUnroutedV2(_ModelDelegationTerminalCommonV2):
    """Failure terminal whose routing boundary selected no backend."""

    routing_disposition: Literal[EnumDelegationRoutingDisposition.UNROUTED] = Field(
        ..., description="Confirms that no backend was selected."
    )
    terminal_outcome: Literal[EnumDelegationTerminalOutcome.FAILED] = Field(
        ..., description="An unrouted terminal is always failed."
    )
    unrouted_reason: EnumDelegationUnroutedReason = Field(
        ..., description="Closed producer-stamped reason no backend was selected."
    )

    @model_validator(mode="after")
    def validate_unrouted_terminal_truth(self) -> Self:
        """No-route terminals cannot claim a successful quality verdict."""
        if self.quality_passed:
            msg = "unrouted terminal requires quality_passed=false"
            raise ValueError(msg)
        return self


type ModelDelegationTerminalTransportV2 = Annotated[
    ModelDelegationTerminalRoutedV2 | ModelDelegationTerminalUnroutedV2,
    Field(discriminator="routing_disposition"),
]


__all__: list[str] = [
    "EnumDelegationRoutingDisposition",
    "EnumDelegationTerminalFailureCause",
    "EnumDelegationTerminalOutcome",
    "EnumDelegationUnroutedReason",
    "EnumQualityScoreComparison",
    "ModelDelegationTerminalRoutedV2",
    "ModelDelegationTerminalTransportV2",
    "ModelDelegationTerminalUnroutedV2",
]
