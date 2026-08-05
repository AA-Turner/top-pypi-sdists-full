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


class ConnectionResourceRequirementsInfo(BaseModel):
    """Current connection-level resource requirements."""

    connection_id: str = Field(description="The connection ID")
    cpu_request: str | None = Field(
        default=None,
        description="Explicit CPU request, or `None` when inherited from defaults.",
    )
    cpu_limit: str | None = Field(
        default=None,
        description="Explicit CPU limit, or `None` when inherited from defaults.",
    )
    memory_request: str | None = Field(
        default=None,
        description="Explicit memory request, or `None` when inherited from defaults.",
    )
    memory_limit: str | None = Field(
        default=None,
        description="Explicit memory limit, or `None` when inherited from defaults.",
    )
    ephemeral_storage_request: str | None = Field(
        default=None,
        description="Explicit ephemeral-storage request, or `None` when inherited.",
    )
    ephemeral_storage_limit: str | None = Field(
        default=None,
        description="Explicit ephemeral-storage limit, or `None` when inherited.",
    )
    cpu_rung: str = Field(
        description="CPU ladder rung, `DEFAULT`, or `OFF_LADDER`.",
    )
    next_cpu_rung: str | None = Field(
        default=None,
        description="Next higher CPU ladder rung, if one exists.",
    )
    memory_rung: str = Field(
        description="Memory ladder rung, `DEFAULT`, or `OFF_LADDER`.",
    )
    next_memory_rung: str | None = Field(
        default=None,
        description="Next higher memory ladder rung, if one exists.",
    )
    disk_rung: str = Field(
        description="Ephemeral-storage ladder rung, `DEFAULT`, or `OFF_LADDER`.",
    )
    next_disk_rung: str | None = Field(
        default=None,
        description="Next higher ephemeral-storage ladder rung, if one exists.",
    )
    was_overridden: bool = Field(
        description="Whether any connection-level resource requirement is set"
    )
    is_on_defaults: bool = Field(
        description="Whether the connection inherits resource defaults"
    )


class ConnectionResourceRequirementsOperationResult(BaseModel):
    """Result of setting or clearing connection-level resource requirements."""

    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Human-readable result message")
    connection_id: str = Field(description="The connection ID")
    previous_cpu_request: str | None = Field(
        default=None,
        description="CPU request before the operation.",
    )
    previous_cpu_limit: str | None = Field(
        default=None,
        description="CPU limit before the operation.",
    )
    previous_memory_request: str | None = Field(
        default=None,
        description="Memory request before the operation.",
    )
    previous_memory_limit: str | None = Field(
        default=None,
        description="Memory limit before the operation.",
    )
    new_cpu_request: str | None = Field(
        default=None,
        description="CPU request after the operation.",
    )
    new_cpu_limit: str | None = Field(
        default=None,
        description="CPU limit after the operation.",
    )
    new_memory_request: str | None = Field(
        default=None,
        description="Memory request after the operation.",
    )
    new_memory_limit: str | None = Field(
        default=None,
        description="Memory limit after the operation.",
    )
    previous_ephemeral_storage_request: str | None = Field(
        default=None,
        description="Ephemeral-storage request before the operation.",
    )
    previous_ephemeral_storage_limit: str | None = Field(
        default=None,
        description="Ephemeral-storage limit before the operation.",
    )
    new_ephemeral_storage_request: str | None = Field(
        default=None,
        description="Ephemeral-storage request after the operation.",
    )
    new_ephemeral_storage_limit: str | None = Field(
        default=None,
        description="Ephemeral-storage limit after the operation.",
    )
    was_overridden_before: bool | None = Field(
        default=None,
        description="Whether any resource override existed before the operation.",
    )
    is_overridden_after: bool | None = Field(
        default=None,
        description="Whether any resource override exists after the operation.",
    )
    customer_tier: str | None = Field(
        default=None,
        description="Customer tier of the affected connection.",
    )
    tier_warning: str | None = Field(
        default=None,
        description="Warning for sensitive customer tiers.",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Warnings raised by the operation.",
    )
    reset_required: bool = Field(
        default=True,
        description="Whether the connection must be reset for new resources to take effect",
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
        description="Customer tier of the affected entity (TIER_0, TIER_1, TIER_2, UNKNOWN). "
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
    warnings: list[str] = Field(
        default_factory=list,
        description="Warnings raised by this operation.",
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
        description="Customer tier of the workspace's organization (TIER_0, TIER_1, TIER_2, UNKNOWN). "
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
    warnings: list[str] = Field(
        default_factory=list,
        description="Warnings raised by this operation.",
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
        description="Customer tier of the organization (TIER_0, TIER_1, TIER_2, UNKNOWN). "
        "Included as a guardrail annotation.",
    )
    tier_warning: str | None = Field(
        default=None,
        description="Warning message if the operation targets a sensitive customer tier.",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Warnings raised by this operation.",
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
        description="Customer tier of the organization (TIER_0, TIER_1, TIER_2, UNKNOWN)",
    )
    tier_warning: str | None = Field(
        default=None,
        description="Warning message if the organization is a sensitive customer tier",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Warnings raised while resolving this result.",
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
        description="Customer tier of the organization (TIER_0, TIER_1, TIER_2, UNKNOWN)",
    )
    tier_warning: str | None = Field(
        default=None,
        description="Warning message if the organization is a sensitive customer tier",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Warnings raised by this operation.",
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


class OrbSubscriptionInfo(BaseModel):
    """Summary of an Orb billing subscription for an organization."""

    subscription_id: str = Field(description="The Orb subscription ID")
    status: str = Field(description="Subscription status (e.g. `active`, `ended`)")
    plan_name: str | None = Field(
        default=None,
        description="Display name of the Orb plan (e.g. `Airbyte Partner`)",
    )
    plan_id: str | None = Field(
        default=None,
        description="Orb internal plan ID",
    )
    external_plan_id: str | None = Field(
        default=None,
        description="External plan ID configured in Orb",
    )
    start_date: str | None = Field(
        default=None,
        description="ISO 8601 date when the subscription started",
    )
    end_date: str | None = Field(
        default=None,
        description="ISO 8601 date when the subscription ends (if applicable)",
    )
    orb_customer_id: str | None = Field(
        default=None,
        description="Orb internal customer ID",
    )

    def __str__(self) -> str:
        """Return a human-readable summary."""
        plan_label = (
            self.plan_name or self.external_plan_id or self.plan_id or "unknown"
        )
        return f"{self.status} | plan={plan_label}"


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
        description="Customer tier of the organization (TIER_0, TIER_1, TIER_2, UNKNOWN)",
    )
    tier_warning: str | None = Field(
        default=None,
        description="Warning message if the organization is a sensitive customer tier",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Warnings raised while resolving this result.",
    )
    orb_subscription: OrbSubscriptionInfo | None = Field(
        default=None,
        description="Current Orb billing subscription info (if `ORB_API_KEY` is configured)",
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
        if self.orb_subscription:
            parts.append(f"orb_plan={self.orb_subscription}")
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
    permanent_waiver_type: str | None = Field(
        default=None,
        description="Permanent billing waiver after the update: `free`, `internal`, or `None`",
    )
    customer_tier: str | None = Field(
        default=None,
        description="Customer tier of the organization (TIER_0, TIER_1, TIER_2, UNKNOWN)",
    )
    tier_warning: str | None = Field(
        default=None,
        description="Warning message if the organization is a sensitive customer tier",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Warnings raised by this operation.",
    )
    orb_plan_change: str | None = Field(
        default=None,
        description="Result of the Orb plan change (e.g. `Changed to Airbyte Partner`), "
        "or `None` if no Orb plan change was attempted",
    )
    entitlement_plan_change: str | None = Field(
        default=None,
        description="Result of the Stigg entitlement plan change "
        "(e.g. `Changed to PARTNER`), or `None` if not attempted",
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
