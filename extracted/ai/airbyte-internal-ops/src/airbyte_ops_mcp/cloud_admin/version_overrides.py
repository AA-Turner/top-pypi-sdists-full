# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Core version-override business logic for Airbyte Cloud connectors.

Presentation-layer-agnostic helpers for the three override scopes
(`actor`, `workspace`, `organization`) plus the read path. Both the MCP
tool layer and the CLI dispatcher call into this module so they share a
single source of truth for tier guardrails, audit-message construction,
existing-pin checks, and `cloud_admin.api_client` invocation.

Authentication is supplied as an explicit `ResolvedCloudAuth` rather than
a `fastmcp.Context`, so this module has no presentation-layer dependencies.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Literal

import requests as _requests
from airbyte import constants
from airbyte.exceptions import PyAirbyteInputError

from airbyte_ops_mcp.approval_resolution import (
    ApprovalResolutionError,
    resolve_admin_email_from_approval,
)
from airbyte_ops_mcp.cloud_admin import api_client
from airbyte_ops_mcp.cloud_admin.api_client import (
    _get_access_token,
    _ScopeType,
)
from airbyte_ops_mcp.cloud_admin.auth import (
    CloudAuthError,
    require_internal_admin_flag_only,
)
from airbyte_ops_mcp.cloud_admin.models import (
    ConnectorVersionInfo,
    OrganizationVersionOverrideResult,
    VersionOverrideOperationResult,
    WorkspaceVersionOverrideResult,
)
from airbyte_ops_mcp.cloud_admin.registry_lookup import (
    resolve_canonical_name_to_definition_id,
)
from airbyte_ops_mcp.cloud_admin.version_guard import (
    check_existing_pins,
)
from airbyte_ops_mcp.constants import USER_AGENT
from airbyte_ops_mcp.slack_api import SlackAPIError
from airbyte_ops_mcp.slack_posting import post_channel_message
from airbyte_ops_mcp.tier_cache import TierFilter, get_org_tier, resolve_workspace

logger = logging.getLogger(__name__)

# Slack channel for version override audit trail (mirrors Retool notifications).
_VERSION_OVERRIDE_SLACK_CHANNEL = "C06D5RCLBV4"


@dataclass(frozen=True)
class ResolvedCloudAuth:
    """Resolved authentication for Airbyte Cloud API calls.

    Either `bearer_token` OR (`client_id` AND `client_secret`) will be set.
    """

    bearer_token: str | None = None
    client_id: str | None = None
    client_secret: str | None = None


def build_tier_warning(customer_tier: str) -> str | None:
    """Return a warning message for sensitive customer tiers, or `None`."""
    if customer_tier == "TIER_0":
        return (
            "WARNING: This is a TIER_0 (highest-value) customer. "
            "Proceed with extreme caution."
        )
    if customer_tier == "TIER_1":
        return "WARNING: This is a TIER_1 (high-value) customer. Proceed with caution."
    return None


def validate_tier_filter(
    actual_tier: str,
    requested_filter: TierFilter,
) -> tuple[bool, str | None]:
    """Check whether `actual_tier` matches `requested_filter`.

    Returns `(ok, error_message)`. When `ok` is `False` the caller should
    reject the operation with `error_message`.
    """
    if requested_filter == "ALL":
        return True, None
    if actual_tier != requested_filter:
        return False, (
            f"Tier mismatch: the target entity is {actual_tier} but the requested "
            f"tier filter is {requested_filter}. Either specify the correct tier "
            f"or use 'ALL' to proceed with a warning."
        )
    return True, None


def _validate_admin_and_authorization(
    *,
    issue_url: str | None,
    approval_comment_url: str | None,
) -> tuple[str | None, str | None]:
    """Run admin-flag and authorization-parameter checks.

    Returns `(admin_user_email, error_message)`. Exactly one will be non-`None`:
    on success the resolved admin email; on failure the error message to
    propagate to the caller.
    """
    try:
        require_internal_admin_flag_only()
    except CloudAuthError as e:
        return None, f"Admin authentication failed: {e}"

    validation_errors: list[str] = []

    if not issue_url:
        validation_errors.append(
            "issue_url is required for authorization (GitHub issue URL)"
        )
    elif not issue_url.startswith("https://github.com/"):
        validation_errors.append(
            f"issue_url must be a valid GitHub URL (https://github.com/...), got: {issue_url}"
        )

    if not approval_comment_url:
        validation_errors.append(
            "'approval_comment_url' is required. Use `escalate_to_human` with "
            "`approval_requested=True` to obtain a Slack approval record URL."
        )

    if validation_errors:
        return None, "Authorization validation failed: " + "; ".join(validation_errors)

    assert approval_comment_url is not None  # narrowed by validation above
    try:
        admin_user_email = resolve_admin_email_from_approval(
            approval_comment_url=approval_comment_url,
        )
    except ApprovalResolutionError as e:
        return None, str(e)

    return admin_user_email, None


def _build_audit_reason(
    *,
    override_reason: str | None,
    issue_url: str | None,
    approval_comment_url: str | None,
    ai_agent_session_url: str | None,
    unset: bool,
) -> str | None:
    """Augment `override_reason` with audit fields for `set` operations."""
    if unset or not override_reason:
        return override_reason

    parts = [override_reason]
    if issue_url:
        parts.append(f"Issue: {issue_url}")
    if approval_comment_url:
        parts.append(f"Approval: {approval_comment_url}")
    if ai_agent_session_url:
        parts.append(f"AI Session: {ai_agent_session_url}")
    return " | ".join(parts)


def _notify_version_override_slack(
    *,
    action: Literal["set", "removed"],
    scope_type: str,
    scope_id: str,
    connector_name: str,
    connector_type: str,
    version: str | None,
    admin_user_email: str | None,
    override_reason: str | None,
    issue_url: str | None,
    ai_agent_session_url: str | None,
    override_reason_reference_url: str | None,
) -> None:
    """Post a version-override audit notification to the Slack channel.

    Best-effort: logs and swallows errors so a Slack failure never blocks
    the override operation itself.
    """
    action_label = "set" if action == "set" else "removed"
    header = f"Devin (via MCP) {action_label} a connector version override:"

    lines = [header]
    lines.append(f">*Connector:* `{connector_name}` ({connector_type})")
    lines.append(f">*Scope:* {scope_type} (`{scope_id}`)")
    if version:
        lines.append(f">*Version:* `{version}`")
    if admin_user_email:
        lines.append(f">*Approved by:* {admin_user_email}")
    if override_reason:
        lines.append(f">*Reason:* {override_reason}")
    if issue_url:
        lines.append(f">*Issue:* {issue_url}")
    if override_reason_reference_url:
        lines.append(f">*Reference URL:* {override_reason_reference_url}")
    if ai_agent_session_url:
        lines.append(f">*AI Session:* {ai_agent_session_url}")

    text = "\n".join(lines)
    try:
        post_channel_message(_VERSION_OVERRIDE_SLACK_CHANNEL, text)
    except (SlackAPIError, _requests.RequestException):
        logger.warning(
            "Failed to post version-override notification to Slack",
            exc_info=True,
        )


def get_connector_version_info(
    *,
    auth: ResolvedCloudAuth,
    workspace_id: str,
    actor_id: str,
    actor_type: Literal["source", "destination"],
    config_api_root: str | None = None,
) -> ConnectorVersionInfo:
    """Read the current version info for a deployed connector.

    The returned `is_version_pinned` flag is sourced from the scoped-config
    contexts when available (which surface system-generated pins such as
    breaking-change migrations), falling back to the API's
    `isVersionOverrideApplied` flag when the scoped-config block is empty.
    """
    version_data = api_client.get_connector_version(
        connector_id=actor_id,
        connector_type=actor_type,
        config_api_root=config_api_root or constants.CLOUD_CONFIG_API_ROOT,
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        bearer_token=auth.bearer_token,
        workspace_id=workspace_id,
    )

    scoped_configs = version_data.get("scopedConfigs", {})
    has_any_pin = (
        any(config is not None for config in scoped_configs.values())
        if scoped_configs
        else False
    )
    is_pinned = (
        has_any_pin if scoped_configs else version_data["isVersionOverrideApplied"]
    )

    return ConnectorVersionInfo(
        connector_id=actor_id,
        connector_type=actor_type,
        version=version_data["dockerImageTag"],
        is_version_pinned=is_pinned,
    )


def set_actor_version_override(
    *,
    auth: ResolvedCloudAuth,
    workspace_id: str,
    actor_id: str,
    actor_type: Literal["source", "destination"],
    approval_comment_url: str | None,
    version: str | None,
    unset: bool,
    override_reason: str | None,
    override_reason_reference_url: str | None,
    issue_url: str | None,
    ai_agent_session_url: str | None,
    customer_tier_filter: TierFilter,
    force: bool = False,
    config_api_root: str | None = None,
) -> VersionOverrideOperationResult:
    """Set or clear an actor-scope (single deployed connector) version pin.

    All admin-flag, authorization-parameter, tier, and existing-pin guard
    checks are enforced here. The returned `VersionOverrideOperationResult`
    is the same shape produced by the corresponding MCP tool.
    """
    admin_user_email, auth_error = _validate_admin_and_authorization(
        issue_url=issue_url,
        approval_comment_url=approval_comment_url,
    )
    if auth_error is not None:
        return VersionOverrideOperationResult(
            success=False,
            message=auth_error,
            connector_id=actor_id,
            connector_type=actor_type,
        )

    ws_resolution = resolve_workspace(workspace_id)
    if not ws_resolution.organization_id:
        return VersionOverrideOperationResult(
            success=False,
            message=f"Could not resolve organization for workspace {workspace_id}",
            connector_id=actor_id,
            connector_type=actor_type,
        )

    customer_tier = ws_resolution.customer_tier
    is_eu = (
        ws_resolution.dataplane_name == "EU" if ws_resolution.dataplane_name else None
    )
    tier_warning = build_tier_warning(customer_tier)

    tier_ok, tier_error = validate_tier_filter(customer_tier, customer_tier_filter)
    if not tier_ok:
        return VersionOverrideOperationResult(
            success=False,
            message=tier_error or "Tier filter mismatch",
            connector_id=actor_id,
            connector_type=actor_type,
            customer_tier=customer_tier,
            is_eu=is_eu,
            tier_warning=tier_warning,
        )

    enhanced_override_reason = _build_audit_reason(
        override_reason=override_reason,
        issue_url=issue_url,
        approval_comment_url=approval_comment_url,
        ai_agent_session_url=ai_agent_session_url,
        unset=unset,
    )

    resolved_config_api_root = config_api_root or constants.CLOUD_CONFIG_API_ROOT
    try:
        current_version_data = api_client.get_connector_version(
            connector_id=actor_id,
            connector_type=actor_type,
            config_api_root=resolved_config_api_root,
            client_id=auth.client_id,
            client_secret=auth.client_secret,
            bearer_token=auth.bearer_token,
        )
        current_version = current_version_data["dockerImageTag"]
        was_pinned_before = current_version_data["isVersionOverrideApplied"]
    except CloudAuthError as e:
        return VersionOverrideOperationResult(
            success=False,
            message=f"Failed to resolve credentials or get connector: {e}",
            connector_id=actor_id,
            connector_type=actor_type,
        )

    if not unset and version:
        try:
            access_token = _get_access_token(
                auth.client_id, auth.client_secret, auth.bearer_token
            )
            get_endpoint = f"{resolved_config_api_root}/{actor_type}s/get"
            get_resp = _requests.post(
                get_endpoint,
                json={f"{actor_type}Id": actor_id},
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "User-Agent": USER_AGENT,
                    "Content-Type": "application/json",
                },
                timeout=30,
            )
            get_resp.raise_for_status()
            actor_definition_id = get_resp.json().get(f"{actor_type}DefinitionId")
            if not actor_definition_id:
                return VersionOverrideOperationResult(
                    success=False,
                    message=f"Could not find {actor_type}DefinitionId in connector info for actor {actor_id}",
                    connector_id=actor_id,
                    connector_type=actor_type,
                    previous_version=current_version,
                    was_pinned_before=was_pinned_before,
                )

            guard = check_existing_pins(
                scopes=[
                    (_ScopeType.ACTOR, actor_id, "actor"),
                    (_ScopeType.WORKSPACE, workspace_id, "workspace"),
                    (
                        _ScopeType.ORGANIZATION,
                        ws_resolution.organization_id,
                        "organization",
                    ),
                ],
                actor_definition_id=actor_definition_id,
                config_api_root=resolved_config_api_root,
                access_token=access_token,
                target_version=version,
                force=force,
            )
            if guard.blocked:
                assert guard.error_msg is not None
                return VersionOverrideOperationResult(
                    success=False,
                    message=guard.error_msg,
                    connector_id=actor_id,
                    connector_type=actor_type,
                    previous_version=current_version,
                    was_pinned_before=was_pinned_before,
                )
        except (
            PyAirbyteInputError,
            CloudAuthError,
            _requests.exceptions.HTTPError,
        ) as e:
            return VersionOverrideOperationResult(
                success=False,
                message=f"Pin guard check failed: {e}",
                connector_id=actor_id,
                connector_type=actor_type,
                previous_version=current_version,
                was_pinned_before=was_pinned_before,
            )

    try:
        result = api_client.set_connector_version_override(
            connector_id=actor_id,
            connector_type=actor_type,
            config_api_root=resolved_config_api_root,
            client_id=auth.client_id,
            client_secret=auth.client_secret,
            workspace_id=workspace_id,
            version=version,
            unset=unset,
            override_reason=enhanced_override_reason,
            override_reason_reference_url=override_reason_reference_url,
            user_email=admin_user_email,
            bearer_token=auth.bearer_token,
        )

        updated_version_data = api_client.get_connector_version(
            connector_id=actor_id,
            connector_type=actor_type,
            config_api_root=resolved_config_api_root,
            client_id=auth.client_id,
            client_secret=auth.client_secret,
            bearer_token=auth.bearer_token,
        )
        new_version = updated_version_data["dockerImageTag"] if not unset else None
        is_pinned_after = updated_version_data["isVersionOverrideApplied"]

        if unset:
            if result:
                message = "Successfully cleared version override. Connector will now use default version."
            else:
                message = "No version override was active (nothing to clear)"
        else:
            message = f"Successfully pinned connector to version {version}"

        if tier_warning:
            message = f"{tier_warning} {message}"

        # Only notify when something actually changed (skip no-op unsets).
        if not unset or result:
            _notify_version_override_slack(
                action="removed" if unset else "set",
                scope_type="actor",
                scope_id=actor_id,
                connector_name=f"{actor_type} ({actor_id})",
                connector_type=actor_type,
                version=version,
                admin_user_email=admin_user_email,
                override_reason=override_reason,
                issue_url=issue_url,
                ai_agent_session_url=ai_agent_session_url,
                override_reason_reference_url=override_reason_reference_url,
            )

        return VersionOverrideOperationResult(
            success=True,
            message=message,
            connector_id=actor_id,
            connector_type=actor_type,
            previous_version=current_version,
            new_version=new_version,
            was_pinned_before=was_pinned_before,
            is_pinned_after=is_pinned_after,
            customer_tier=customer_tier,
            is_eu=is_eu,
            tier_warning=tier_warning,
        )
    except PyAirbyteInputError as e:
        return VersionOverrideOperationResult(
            success=False,
            message=str(e),
            connector_id=actor_id,
            connector_type=actor_type,
            previous_version=current_version,
            was_pinned_before=was_pinned_before,
        )


def set_workspace_version_override(
    *,
    auth: ResolvedCloudAuth,
    workspace_id: str,
    connector_name: str,
    connector_type: Literal["source", "destination"],
    approval_comment_url: str | None,
    version: str | None,
    unset: bool,
    override_reason: str | None,
    override_reason_reference_url: str | None,
    issue_url: str | None,
    ai_agent_session_url: str | None,
    customer_tier_filter: TierFilter,
    force: bool = False,
    config_api_root: str | None = None,
) -> WorkspaceVersionOverrideResult:
    """Set or clear a workspace-scope version pin for a connector type.

    Pins (or clears) the override for ALL instances of `connector_name` in
    `workspace_id`.
    """
    admin_user_email, auth_error = _validate_admin_and_authorization(
        issue_url=issue_url,
        approval_comment_url=approval_comment_url,
    )
    if auth_error is not None:
        return WorkspaceVersionOverrideResult(
            success=False,
            message=auth_error,
            workspace_id=workspace_id,
            connector_name=connector_name,
            connector_type=connector_type,
        )

    ws_resolution = resolve_workspace(workspace_id)
    if not ws_resolution.organization_id:
        return WorkspaceVersionOverrideResult(
            success=False,
            message=f"Could not resolve organization for workspace {workspace_id}",
            workspace_id=workspace_id,
            connector_name=connector_name,
            connector_type=connector_type,
        )

    customer_tier = ws_resolution.customer_tier
    is_eu = (
        ws_resolution.dataplane_name == "EU" if ws_resolution.dataplane_name else None
    )
    tier_warning = build_tier_warning(customer_tier)

    tier_ok, tier_error = validate_tier_filter(customer_tier, customer_tier_filter)
    if not tier_ok:
        return WorkspaceVersionOverrideResult(
            success=False,
            message=tier_error or "Tier filter mismatch",
            workspace_id=workspace_id,
            connector_name=connector_name,
            connector_type=connector_type,
            customer_tier=customer_tier,
            is_eu=is_eu,
            tier_warning=tier_warning,
        )

    enhanced_override_reason = _build_audit_reason(
        override_reason=override_reason,
        issue_url=issue_url,
        approval_comment_url=approval_comment_url,
        ai_agent_session_url=ai_agent_session_url,
        unset=unset,
    )

    resolved_config_api_root = config_api_root or constants.CLOUD_CONFIG_API_ROOT

    if not unset and version:
        try:
            access_token = _get_access_token(
                auth.client_id, auth.client_secret, auth.bearer_token
            )
            actor_definition_id = resolve_canonical_name_to_definition_id(
                connector_name
            )

            guard = check_existing_pins(
                scopes=[
                    (_ScopeType.WORKSPACE, workspace_id, "workspace"),
                    (
                        _ScopeType.ORGANIZATION,
                        ws_resolution.organization_id,
                        "organization",
                    ),
                ],
                actor_definition_id=actor_definition_id,
                config_api_root=resolved_config_api_root,
                access_token=access_token,
                target_version=version,
                force=force,
            )
            if guard.blocked:
                assert guard.error_msg is not None
                return WorkspaceVersionOverrideResult(
                    success=False,
                    message=guard.error_msg,
                    workspace_id=workspace_id,
                    connector_name=connector_name,
                    connector_type=connector_type,
                )
        except (PyAirbyteInputError, CloudAuthError) as e:
            return WorkspaceVersionOverrideResult(
                success=False,
                message=f"Pin guard check failed: {e}",
                workspace_id=workspace_id,
                connector_name=connector_name,
                connector_type=connector_type,
            )

    try:
        result = api_client.set_workspace_connector_version_override(
            workspace_id=workspace_id,
            connector_name=connector_name,
            connector_type=connector_type,
            config_api_root=resolved_config_api_root,
            client_id=auth.client_id,
            client_secret=auth.client_secret,
            bearer_token=auth.bearer_token,
            version=version,
            unset=unset,
            override_reason=enhanced_override_reason,
            override_reason_reference_url=override_reason_reference_url,
            user_email=admin_user_email,
        )

        if unset:
            if result:
                message = f"Successfully cleared workspace-level version override for {connector_name}."
            else:
                message = f"No workspace-level version override was active for {connector_name} (nothing to clear)"
        else:
            message = f"Successfully pinned {connector_name} to version {version} at workspace level."

        if tier_warning:
            message = f"{tier_warning} {message}"

        # Only notify when something actually changed (skip no-op unsets).
        if not unset or result:
            _notify_version_override_slack(
                action="removed" if unset else "set",
                scope_type="workspace",
                scope_id=workspace_id,
                connector_name=connector_name,
                connector_type=connector_type,
                version=version,
                admin_user_email=admin_user_email,
                override_reason=override_reason,
                issue_url=issue_url,
                ai_agent_session_url=ai_agent_session_url,
                override_reason_reference_url=override_reason_reference_url,
            )

        return WorkspaceVersionOverrideResult(
            success=True,
            message=message,
            workspace_id=workspace_id,
            connector_name=connector_name,
            connector_type=connector_type,
            version=version if not unset else None,
            customer_tier=customer_tier,
            is_eu=is_eu,
            tier_warning=tier_warning,
        )
    except PyAirbyteInputError as e:
        return WorkspaceVersionOverrideResult(
            success=False,
            message=str(e),
            workspace_id=workspace_id,
            connector_name=connector_name,
            connector_type=connector_type,
        )
    except CloudAuthError as e:
        return WorkspaceVersionOverrideResult(
            success=False,
            message=f"Authentication failed: {e}",
            workspace_id=workspace_id,
            connector_name=connector_name,
            connector_type=connector_type,
        )


def set_organization_version_override(
    *,
    auth: ResolvedCloudAuth,
    organization_id: str,
    connector_name: str,
    connector_type: Literal["source", "destination"],
    approval_comment_url: str | None,
    version: str | None,
    unset: bool,
    override_reason: str | None,
    override_reason_reference_url: str | None,
    issue_url: str | None,
    ai_agent_session_url: str | None,
    customer_tier_filter: TierFilter,
    force: bool = False,
    config_api_root: str | None = None,
) -> OrganizationVersionOverrideResult:
    """Set or clear an organization-scope version pin for a connector type.

    Pins (or clears) the override for ALL instances of `connector_name` in
    every workspace under `organization_id`.
    """
    admin_user_email, auth_error = _validate_admin_and_authorization(
        issue_url=issue_url,
        approval_comment_url=approval_comment_url,
    )
    if auth_error is not None:
        return OrganizationVersionOverrideResult(
            success=False,
            message=auth_error,
            organization_id=organization_id,
            connector_name=connector_name,
            connector_type=connector_type,
        )

    tier_result = get_org_tier(organization_id)
    customer_tier = tier_result.customer_tier
    tier_warning = build_tier_warning(customer_tier)

    tier_ok, tier_error = validate_tier_filter(customer_tier, customer_tier_filter)
    if not tier_ok:
        return OrganizationVersionOverrideResult(
            success=False,
            message=tier_error or "Tier filter mismatch",
            organization_id=organization_id,
            connector_name=connector_name,
            connector_type=connector_type,
            customer_tier=customer_tier,
            tier_warning=tier_warning,
        )

    enhanced_override_reason = _build_audit_reason(
        override_reason=override_reason,
        issue_url=issue_url,
        approval_comment_url=approval_comment_url,
        ai_agent_session_url=ai_agent_session_url,
        unset=unset,
    )

    resolved_config_api_root = config_api_root or constants.CLOUD_CONFIG_API_ROOT

    if not unset and version:
        try:
            access_token = _get_access_token(
                auth.client_id, auth.client_secret, auth.bearer_token
            )
            actor_definition_id = resolve_canonical_name_to_definition_id(
                connector_name
            )

            guard = check_existing_pins(
                scopes=[
                    (_ScopeType.ORGANIZATION, organization_id, "organization"),
                ],
                actor_definition_id=actor_definition_id,
                config_api_root=resolved_config_api_root,
                access_token=access_token,
                target_version=version,
                force=force,
            )
            if guard.blocked:
                assert guard.error_msg is not None
                return OrganizationVersionOverrideResult(
                    success=False,
                    message=guard.error_msg,
                    organization_id=organization_id,
                    connector_name=connector_name,
                    connector_type=connector_type,
                )
        except (PyAirbyteInputError, CloudAuthError) as e:
            return OrganizationVersionOverrideResult(
                success=False,
                message=f"Pin guard check failed: {e}",
                organization_id=organization_id,
                connector_name=connector_name,
                connector_type=connector_type,
            )

    try:
        result = api_client.set_organization_connector_version_override(
            organization_id=organization_id,
            connector_name=connector_name,
            connector_type=connector_type,
            config_api_root=resolved_config_api_root,
            client_id=auth.client_id,
            client_secret=auth.client_secret,
            bearer_token=auth.bearer_token,
            version=version,
            unset=unset,
            override_reason=enhanced_override_reason,
            override_reason_reference_url=override_reason_reference_url,
            user_email=admin_user_email,
        )

        if unset:
            if result:
                message = f"Successfully cleared organization-level version override for {connector_name}."
            else:
                message = f"No organization-level version override was active for {connector_name} (nothing to clear)"
        else:
            message = f"Successfully pinned {connector_name} to version {version} at organization level."

        if tier_warning:
            message = f"{tier_warning} {message}"

        # Only notify when something actually changed (skip no-op unsets).
        if not unset or result:
            _notify_version_override_slack(
                action="removed" if unset else "set",
                scope_type="organization",
                scope_id=organization_id,
                connector_name=connector_name,
                connector_type=connector_type,
                version=version,
                admin_user_email=admin_user_email,
                override_reason=override_reason,
                issue_url=issue_url,
                ai_agent_session_url=ai_agent_session_url,
                override_reason_reference_url=override_reason_reference_url,
            )

        return OrganizationVersionOverrideResult(
            success=True,
            message=message,
            organization_id=organization_id,
            connector_name=connector_name,
            connector_type=connector_type,
            version=version if not unset else None,
            customer_tier=customer_tier,
            tier_warning=tier_warning,
        )
    except PyAirbyteInputError as e:
        return OrganizationVersionOverrideResult(
            success=False,
            message=str(e),
            organization_id=organization_id,
            connector_name=connector_name,
            connector_type=connector_type,
        )
    except CloudAuthError as e:
        return OrganizationVersionOverrideResult(
            success=False,
            message=f"Authentication failed: {e}",
            organization_id=organization_id,
            connector_name=connector_name,
            connector_type=connector_type,
        )
