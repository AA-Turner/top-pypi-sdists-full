# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Pydantic models for cloud connector version operations.

This module defines the data models used for connector version management
and pinning operations in Airbyte Cloud.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ConnectorVersionInfo(BaseModel):
    """Information about a cloud connector's version.

    This model represents the current version state of a deployed connector,
    including whether a version override (pin) is active.
    """

    connector_id: str = Field(description="The ID of the deployed connector")
    connector_type: Literal["source", "destination"] = Field(
        description="The type of connector (source or destination)"
    )
    version: str = Field(description="The current version string (e.g., '0.1.0')")
    is_version_pinned: bool = Field(
        description="Whether a version override is active for this connector"
    )

    def __str__(self) -> str:
        """Return a string representation of the version."""
        pinned_suffix = " (pinned)" if self.is_version_pinned else ""
        return (
            f"{self.connector_type} {self.connector_id}: {self.version}{pinned_suffix}"
        )


class VersionOverrideOperationResult(BaseModel):
    """Result of a version override operation (set or clear).

    This model provides detailed information about the outcome of a version
    pinning or unpinning operation.
    """

    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Human-readable message describing the result")
    connector_id: str = Field(description="The ID of the connector that was modified")
    connector_type: Literal["source", "destination"] = Field(
        description="The type of connector (source or destination)"
    )
    previous_version: str | None = Field(
        default=None,
        description="The version before the operation (None if not available)",
    )
    new_version: str | None = Field(
        default=None,
        description="The version after the operation (None if cleared or failed)",
    )
    was_pinned_before: bool | None = Field(
        default=None,
        description="Whether a pin was active before the operation",
    )
    is_pinned_after: bool | None = Field(
        default=None,
        description="Whether a pin is active after the operation",
    )
    customer_tier: str | None = Field(
        default=None,
        description="Customer tier of the affected entity (TIER_0, TIER_1, TIER_2). "
        "Included as a guardrail annotation.",
    )
    is_eu: bool | None = Field(
        default=None,
        description="Whether the affected entity is in the EU region.",
    )
    tier_warning: str | None = Field(
        default=None,
        description="Warning message if the operation targets a sensitive customer tier.",
    )

    def __str__(self) -> str:
        """Return a string representation of the operation result."""
        if self.success:
            return f"✓ {self.message}"
        return f"✗ {self.message}"


class WorkspaceVersionOverrideResult(BaseModel):
    """Result of a workspace-level version override operation.

    This model provides detailed information about the outcome of a workspace-level
    version pinning or unpinning operation.
    """

    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Human-readable message describing the result")
    workspace_id: str = Field(description="The workspace ID")
    connector_name: str = Field(
        description="The connector name (e.g., 'source-github')"
    )
    connector_type: Literal["source", "destination"] = Field(
        description="The type of connector (source or destination)"
    )
    version: str | None = Field(
        default=None,
        description="The version that was pinned (None if cleared or failed)",
    )
    customer_tier: str | None = Field(
        default=None,
        description="Customer tier of the workspace's organization (TIER_0, TIER_1, TIER_2). "
        "Included as a guardrail annotation.",
    )
    is_eu: bool | None = Field(
        default=None,
        description="Whether the workspace is in the EU region.",
    )
    tier_warning: str | None = Field(
        default=None,
        description="Warning message if the operation targets a sensitive customer tier.",
    )

    def __str__(self) -> str:
        """Return a string representation of the operation result."""
        if self.success:
            return f"✓ {self.message}"
        return f"✗ {self.message}"


class OrganizationVersionOverrideResult(BaseModel):
    """Result of an organization-level version override operation.

    This model provides detailed information about the outcome of an organization-level
    version pinning or unpinning operation.
    """

    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Human-readable message describing the result")
    organization_id: str = Field(description="The organization ID")
    connector_name: str = Field(
        description="The connector name (e.g., 'source-github')"
    )
    connector_type: Literal["source", "destination"] = Field(
        description="The type of connector (source or destination)"
    )
    version: str | None = Field(
        default=None,
        description="The version that was pinned (None if cleared or failed)",
    )
    customer_tier: str | None = Field(
        default=None,
        description="Customer tier of the organization (TIER_0, TIER_1, TIER_2). "
        "Included as a guardrail annotation.",
    )
    tier_warning: str | None = Field(
        default=None,
        description="Warning message if the operation targets a sensitive customer tier.",
    )

    def __str__(self) -> str:
        """Return a string representation of the operation result."""
        if self.success:
            return f"✓ {self.message}"
        return f"✗ {self.message}"


class OrganizationInfo(BaseModel):
    """Basic organization identity from the Config API.

    Returned by `POST /v1/organizations/get`.
    """

    organization_id: str = Field(
        alias="organizationId",
        description="The organization UUID",
    )
    organization_name: str = Field(
        alias="organizationName",
        description="The display name of the organization",
    )
    email: str | None = Field(
        default=None,
        description="Organization contact email (may be absent)",
    )
    is_agentic: bool | None = Field(
        default=None,
        alias="isAgentic",
        description="Whether the organization is flagged as agentic.",
    )


class OrganizationAgenticFlagInfo(BaseModel):
    """Current managed agentic organization status for an organization."""

    organization_id: str = Field(description="The organization UUID")
    organization_name: str | None = Field(
        default=None,
        description="The display name of the organization",
    )
    email: str | None = Field(
        default=None,
        description="Organization contact email (may be absent)",
    )
    tombstone: bool = Field(description="Whether the organization is tombstoned")
    is_agentic: bool = Field(
        description=(
            "Whether the organization is managed by the Airbyte Agents product. "
            "`False` means a standard Cloud org; `True` means an org managed "
            "via the app.agents.ai interfaces."
        )
    )
    customer_tier: str | None = Field(
        default=None,
        description="Customer tier of the organization (TIER_0, TIER_1, TIER_2)",
    )
    tier_warning: str | None = Field(
        default=None,
        description="Warning message if the organization is a sensitive customer tier",
    )


class OrganizationAgenticFlagBatchInfo(BaseModel):
    """Current managed agentic organization status for one or more organizations."""

    organizations: list[OrganizationAgenticFlagInfo] = Field(
        description="Organizations that were found."
    )
    missing_organization_ids: list[str] = Field(
        default_factory=list,
        description="Requested organization IDs that were not found.",
    )


class OrganizationAgenticFlagUpdateResult(BaseModel):
    """Result of a managed agentic organization status update."""

    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Human-readable message describing the result")
    organization_id: str = Field(description="The organization UUID")
    organization_name: str | None = Field(
        default=None,
        description="The display name of the organization",
    )
    email: str | None = Field(
        default=None,
        description="Organization contact email (may be absent)",
    )
    previous_is_agentic: bool | None = Field(
        default=None,
        description="The managed agentic organization status before the update.",
    )
    new_is_agentic: bool | None = Field(
        default=None,
        description="The managed agentic organization status after the update.",
    )
    customer_tier: str | None = Field(
        default=None,
        description="Customer tier of the organization (TIER_0, TIER_1, TIER_2)",
    )
    tier_warning: str | None = Field(
        default=None,
        description="Warning message if the organization is a sensitive customer tier",
    )

    def __str__(self) -> str:
        """Return a string representation of the operation result."""
        if self.success:
            return f"OK {self.message}"
        return f"FAILED {self.message}"


class OrganizationAgenticFlagBatchUpdateResult(BaseModel):
    """Result of updating one or more managed agentic organization statuses."""

    success: bool = Field(description="Whether every requested update succeeded")
    message: str = Field(description="Human-readable message describing the result")
    results: list[OrganizationAgenticFlagUpdateResult] = Field(
        description="Per-organization update results."
    )


class OrganizationPaymentConfigInfo(BaseModel):
    """Current payment configuration for an organization.

    Returned by the `GET /api/v1/organization_payment_config/{organizationId}` endpoint.
    """

    organization_id: str = Field(description="The organization UUID")
    payment_status: str = Field(
        description="Payment status: `uninitialized`, `okay`, `grace_period`, "
        "`disabled`, `locked`, or `manual`"
    )
    subscription_status: str = Field(
        description="Subscription status: `pre_subscription`, `subscribed`, or `unsubscribed`"
    )
    payment_provider_id: str | None = Field(
        default=None,
        description="External payment provider ID (e.g. Stripe customer ID)",
    )
    grace_period_end_at: str | None = Field(
        default=None,
        description="ISO 8601 datetime when the grace period ends (if active)",
    )
    usage_category_overwrite: str | None = Field(
        default=None,
        description="Usage category override: `free` or `internal` (if set)",
    )
    customer_tier: str | None = Field(
        default=None,
        description="Customer tier of the organization (TIER_0, TIER_1, TIER_2)",
    )
    tier_warning: str | None = Field(
        default=None,
        description="Warning message if the organization is a sensitive customer tier",
    )

    def __str__(self) -> str:
        """Return a human-readable summary."""
        parts = [
            f"org={self.organization_id}",
            f"status={self.payment_status}",
            f"subscription={self.subscription_status}",
        ]
        if self.grace_period_end_at:
            parts.append(f"grace_period_ends={self.grace_period_end_at}")
        if self.customer_tier:
            parts.append(f"tier={self.customer_tier}")
        return " | ".join(parts)


class OrganizationPaymentConfigUpdateResult(BaseModel):
    """Result of an organization payment config update operation."""

    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Human-readable message describing the result")
    organization_id: str = Field(description="The organization UUID")
    payment_status: str | None = Field(
        default=None,
        description="The payment status after the update",
    )
    grace_period_end_at: str | None = Field(
        default=None,
        description="The grace period end datetime after the update (if applicable)",
    )
    customer_tier: str | None = Field(
        default=None,
        description="Customer tier of the organization (TIER_0, TIER_1, TIER_2)",
    )
    tier_warning: str | None = Field(
        default=None,
        description="Warning message if the organization is a sensitive customer tier",
    )

    def __str__(self) -> str:
        """Return a string representation of the operation result."""
        if self.success:
            return f"OK {self.message}"
        return f"FAILED {self.message}"


class ConnectorRolloutStartResult(BaseModel):
    """Result of a connector rollout start operation.

    This model provides detailed information about the outcome of starting
    a connector rollout workflow.
    """

    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Human-readable message describing the result")
    docker_repository: str | None = Field(
        default=None,
        description="The docker repository (e.g., 'airbyte/source-github')",
    )
    docker_image_tag: str | None = Field(
        default=None,
        description="The docker image tag (e.g., '1.2.0-rc.2')",
    )
    actor_definition_id: str | None = Field(
        default=None,
        description="The actor definition ID (UUID)",
    )
    rollout_strategy: Literal["manual", "automated", "overridden"] | None = Field(
        default=None,
        description="The rollout strategy used",
    )

    def __str__(self) -> str:
        """Return a string representation of the operation result."""
        if self.success:
            return f"OK {self.message}"
        return f"FAILED {self.message}"


class ConnectorRolloutProgressResult(BaseModel):
    """Result of a connector rollout progress operation.

    This model provides detailed information about the outcome of progressing
    a connector rollout (pinning actors to the RC version).
    """

    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Human-readable message describing the result")
    rollout_id: str | None = Field(
        default=None,
        description="The rollout ID that was progressed",
    )
    docker_repository: str | None = Field(
        default=None,
        description="The docker repository (e.g., 'airbyte/source-github')",
    )
    docker_image_tag: str | None = Field(
        default=None,
        description="The docker image tag (e.g., '1.2.0-rc.2')",
    )
    target_percentage: int | None = Field(
        default=None,
        description="The target percentage of actors to pin",
    )

    def __str__(self) -> str:
        """Return a string representation of the operation result."""
        if self.success:
            return f"OK {self.message}"
        return f"FAILED {self.message}"


class ConnectorRolloutFinalizeResult(BaseModel):
    """Result of a connector rollout finalization operation.

    This model provides detailed information about the outcome of finalizing
    a connector rollout (promote, rollback, or cancel).
    """

    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Human-readable message describing the result")
    rollout_id: str | None = Field(
        default=None,
        description="The rollout ID that was finalized",
    )
    docker_repository: str | None = Field(
        default=None,
        description="The docker repository (e.g., 'airbyte/source-github')",
    )
    docker_image_tag: str | None = Field(
        default=None,
        description="The docker image tag (e.g., '1.2.0-rc.2')",
    )
    state: Literal["succeeded", "failed_rolled_back", "canceled"] | None = Field(
        default=None,
        description="The final state of the rollout",
    )

    def __str__(self) -> str:
        """Return a string representation of the operation result."""
        if self.success:
            return f"OK {self.message}"
        return f"FAILED {self.message}"
