"""Typed data models for Connector Pinning."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from airbyte_ops_mcp.tier_cache import TierFilter
from pydantic import BaseModel

ConnectorType = Literal["source", "destination"]
OverrideAction = Literal["set", "unset"]
ScopeType = Literal["actor", "workspace", "organization"]
VersionOverrideToolName = Literal["set_version_override",]

CustomerTierFilter = TierFilter

__all__ = [
    "ConnectorOption",
    "ConnectorRelease",
    "ConnectorRollout",
    "ConnectorType",
    "ConnectorVersion",
    "ContextResolution",
    "CurrentVersionState",
    "CustomerTierFilter",
    "OperationPreview",
    "OperationResult",
    "OverrideAction",
    "OverridePlan",
    "ScopeType",
    "ScopedConfiguration",
    "VersionOverridePayload",
    "VersionOverrideTargetPayload",
    "VersionOverrideToolName",
    "VersionPinRow",
    "build_version_override_payload",
    "version_override_tool_name",
]


class OverridePlan(BaseModel):
    """Connector version override plan staged by the app."""

    action: OverrideAction
    connector_id: str
    connector_name: str
    connector_type: ConnectorType
    scope_type: ScopeType
    organization_id: str
    workspace_id: str | None = None
    actor_id: str | None = None
    scope_id: str = ""
    version: str | None
    override_reason: str
    override_reason_reference_url: str
    approval_comment_url: str | None = None
    user_email: str | None = None
    customer_tier_filter: TierFilter
    force: bool


class VersionOverrideTargetPayload(BaseModel):
    """Normalized target for a connector version override."""

    scope: ScopeType
    organization_id: str
    connector_type: ConnectorType
    workspace_id: str | None = None
    actor_id: str | None = None
    connector_name: str | None = None


class VersionOverridePayload(BaseModel):
    """Payload for a normalized connector version override."""

    target: VersionOverrideTargetPayload
    version: str | None
    unset: bool
    override_reason: str | None
    override_reason_reference_url: str | None
    approval_comment_url: str | None
    ai_agent_session_url: str | None
    user_email: str | None
    force: bool
    customer_tier_filter: TierFilter


class OperationPreview(BaseModel):
    """Safe preview of the tool call that would be made."""

    tool_name: VersionOverrideToolName
    mutating: bool
    mode: str
    payload: VersionOverridePayload
    required_approval_fields: tuple[str, ...]
    warnings: tuple[str, ...]


class OperationResult(BaseModel):
    """Result of applying a connector version override plan."""

    tool_name: VersionOverrideToolName
    success: bool
    mutating: bool
    mode: str
    message: str
    payload: VersionOverridePayload


@dataclass(frozen=True)
class ConnectorOption:
    """Connector definition shown in the search/select flow."""

    id: str
    name: str
    connector_type: ConnectorType
    latest_version: str
    docker_repository: str


@dataclass(frozen=True)
class ConnectorRelease:
    """Recently published connector release option."""

    version_id: str
    connector_id: str
    connector_name: str
    connector_type: ConnectorType
    docker_image_tag: str
    docker_repository: str
    release_stage: str
    last_published: str


@dataclass(frozen=True)
class ConnectorVersion:
    """Published connector version row."""

    version_id: str
    docker_image_tag: str
    docker_repository: str
    release_stage: str
    support_level: str
    cdk_version: str
    language: str
    last_published: str


@dataclass(frozen=True)
class ConnectorRollout:
    """Active progressive rollout row."""

    rollout_id: str
    connector_id: str
    connector_name: str
    connector_type: ConnectorType
    docker_repository: str
    state: str
    rc_docker_image_tag: str
    initial_docker_image_tag: str
    current_target_rollout_pct: str
    final_target_rollout_pct: str
    created_at: str
    updated_at: str
    rollout_strategy: str = ""
    rc_pin_count: int = 0


@dataclass(frozen=True)
class ScopedConfiguration:
    """Connector version override configuration."""

    id: str
    connector_id: str
    connector_name: str
    connector_type: ConnectorType
    scope_type: ScopeType
    scope_id: str
    scope_name: str
    value_name: str
    description: str
    origin_type: str
    origin_name: str
    expires_at: str
    reference_url: str


@dataclass(frozen=True)
class VersionPinRow:
    """A single pin row for display in the version pin list."""

    scope_type: str
    scope_id: str
    scope_url: str
    origin_type: str
    origin_name: str
    description: str
    created_at: str
    created_at_display: str
    expires_at: str
    expires_at_display: str
    reference_url: str
    scope_name: str = ""


@dataclass(frozen=True)
class ContextResolution:
    """Resolved organization/workspace/actor context for a GUID."""

    scope_type: ScopeType
    scope_id: str
    organization_id: str
    scope_name: str = ""
    workspace_id: str | None = None
    workspace_name: str = ""
    organization_name: str = ""
    actor_id: str | None = None
    actor_type: str = ""


@dataclass(frozen=True)
class CurrentVersionState:
    """Current version context for a connector and scope."""

    connector_id: str
    connector_name: str
    connector_type: ConnectorType
    latest_version: str
    active_version: str
    is_version_pinned: bool
    active_scope: ScopeType | None
    active_scope_id: str | None
    ancestor_configurations: tuple[ScopedConfiguration, ...]
    descendant_configurations: tuple[ScopedConfiguration, ...]


def version_override_tool_name(
    scope_type: ScopeType,
) -> VersionOverrideToolName:
    """Return the override tool name for `scope_type`."""
    return "set_version_override"


def build_version_override_payload(
    plan: OverridePlan,
) -> VersionOverridePayload:
    """Build a typed payload for a connector version override plan."""
    if plan.scope_type == "actor":
        target = VersionOverrideTargetPayload(
            scope="actor",
            organization_id=plan.organization_id,
            connector_type=plan.connector_type,
            workspace_id=plan.workspace_id,
            actor_id=plan.actor_id,
        )
    elif plan.scope_type == "workspace":
        target = VersionOverrideTargetPayload(
            scope="workspace",
            organization_id=plan.organization_id,
            connector_type=plan.connector_type,
            workspace_id=plan.workspace_id,
            connector_name=plan.connector_name,
        )
    else:
        target = VersionOverrideTargetPayload(
            scope="organization",
            organization_id=plan.organization_id,
            connector_type=plan.connector_type,
            connector_name=plan.connector_name,
        )
    return VersionOverridePayload(
        target=target,
        version=None if plan.action == "unset" else plan.version,
        unset=plan.action == "unset",
        override_reason=plan.override_reason or None,
        override_reason_reference_url=plan.override_reason_reference_url or None,
        approval_comment_url=plan.approval_comment_url or None,
        ai_agent_session_url=None,
        user_email=plan.user_email,
        force=plan.force,
        customer_tier_filter=plan.customer_tier_filter,
    )
