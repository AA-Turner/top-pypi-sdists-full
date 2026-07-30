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
from typing import Literal, TypeAlias

import google.auth.credentials
import requests as _requests
from airbyte import constants
from airbyte.exceptions import PyAirbyteInputError

from airbyte_ops_mcp.approval_resolution import (
    ApprovalStatus,
    check_approval_status,
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
from airbyte_ops_mcp.cloud_admin.payment_config import (
    get_organization_info,
)
from airbyte_ops_mcp.cloud_admin.version_guard import (
    check_existing_pins,
)
from airbyte_ops_mcp.constants import USER_AGENT
from airbyte_ops_mcp.gcp_auth import _get_identity_from_credentials
from airbyte_ops_mcp.internal_team_roster import fetch_roster, search_roster
from airbyte_ops_mcp.slack_api import SlackAPIError
from airbyte_ops_mcp.slack_posting import post_channel_message
from airbyte_ops_mcp.tier_cache import (
    TierFilter,
    TierSourceHealth,
    get_org_tier,
    resolve_workspace,
    tier_source_warnings,
)

logger = logging.getLogger(__name__)

_VERSION_OVERRIDE_SLACK_CHANNEL = "C06D5RCLBV4"

VersionOverrideScope: TypeAlias = Literal["actor", "workspace", "organization"]
VersionOverrideConnectorType: TypeAlias = Literal["source", "destination"]
VersionOverrideResult: TypeAlias = (
    VersionOverrideOperationResult
    | WorkspaceVersionOverrideResult
    | OrganizationVersionOverrideResult
)


@dataclass(frozen=True)
class ResolvedCloudAuth:
    """Resolved authentication for Airbyte Cloud API calls.

    Either `bearer_token` OR (`client_id` AND `client_secret`) will be set.
    """

    bearer_token: str | None = None
    client_id: str | None = None
    client_secret: str | None = None


@dataclass(frozen=True)
class VersionOverrideTarget:
    """Normalized target for a connector version override operation."""

    scope: VersionOverrideScope
    organization_id: str
    connector_type: VersionOverrideConnectorType
    workspace_id: str | None = None
    actor_id: str | None = None
    connector_name: str | None = None


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
    *,
    source_health: TierSourceHealth | None = None,
    organization_id: str | None = None,
) -> tuple[bool, str | None]:
    """Check whether `actual_tier` matches `requested_filter`.

    Returns `(ok, error_message)`. When `ok` is `False` the caller should
    reject the operation with `error_message`.
    """
    if source_health is not None and source_health.degraded:
        if requested_filter == "UNKNOWN":
            logger.warning(
                "Proceeding with indeterminate customer tier for organization %s: %s",
                organization_id or "<unknown>",
                source_health.reason or "tier source degraded",
            )
            return True, None
        return False, (
            "Customer tier is indeterminable because the tier source is degraded "
            f"({source_health.reason or 'source unavailable'}); acknowledge with "
            "tier filter 'UNKNOWN'."
        )
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
    user_email: str | None = None,
) -> tuple[str | None, str | None]:
    """Run admin-flag and authorization-parameter checks.

    Returns `(admin_user_email, error_message)`. Exactly one will be non-`None`:
    on success the resolved admin email; on failure the error message to
    propagate to the caller.

    **Webapp bypass:** When `user_email` is provided and the process is
    running inside the Ops Webapp (detected via env var), the
    `issue_url` and `approval_comment_url` requirements are skipped.
    The human operator is already authenticated via OAuth — the approval
    is implicit in their button click.
    """
    try:
        require_internal_admin_flag_only()
    except CloudAuthError as e:
        return None, f"Admin authentication failed: {e}"

    # Webapp bypass: check_approval_status handles env var detection.
    approval = check_approval_status(
        approval_comment_url=approval_comment_url,
        user_email=user_email,
    )
    if approval.status == ApprovalStatus.APPROVED:
        return approval.admin_email, None

    # For NEEDS_APPROVAL in agent mode, also validate issue_url.
    if approval.status == ApprovalStatus.NEEDS_APPROVAL:
        validation_errors: list[str] = []
        if not issue_url:
            validation_errors.append(
                "issue_url is required for authorization (GitHub issue URL)"
            )
        elif not issue_url.startswith("https://github.com/"):
            validation_errors.append(
                f"issue_url must be a valid GitHub URL (https://github.com/...), got: {issue_url}"
            )
        validation_errors.append(approval.reason or "Approval URL is required")
        return None, "Authorization validation failed: " + "; ".join(validation_errors)

    # REJECTED
    return None, approval.reason or "Approval check failed"


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


_CLOUD_UI_BASE = "https://cloud.airbyte.com"


def _fetch_organization_name(
    organization_id: str,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> str | None:
    """Best-effort fetch of organization display name from the Config API."""
    try:
        info = get_organization_info(
            organization_id=organization_id,
            config_api_root=config_api_root,
            client_id=client_id,
            client_secret=client_secret,
            bearer_token=bearer_token,
        )
        if info:
            return info.organization_name
    except Exception:
        logger.debug("Could not fetch org name for %s", organization_id, exc_info=True)
    return None


def _fetch_actor_notification_context(
    *,
    auth: ResolvedCloudAuth,
    actor_id: str,
    actor_type: VersionOverrideConnectorType,
    config_api_root: str,
) -> tuple[str | None, str | None]:
    """Best-effort fetch of actor and connector display names for Slack."""
    try:
        access_token = _get_access_token(
            client_id=auth.client_id,
            client_secret=auth.client_secret,
            bearer_token=auth.bearer_token,
            config_api_root=config_api_root,
        )
        response = _requests.post(
            f"{config_api_root}/{actor_type}s/get",
            json={f"{actor_type}Id": actor_id},
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": USER_AGENT,
                "Content-Type": "application/json",
            },
            timeout=10,
        )
        if not response.ok:
            return None, None
        actor_data = response.json()
        return actor_data.get("name"), actor_data.get(f"{actor_type}Name")
    except (PyAirbyteInputError, _requests.RequestException, ValueError, KeyError):
        logger.debug("Could not fetch actor details for notification", exc_info=True)
        return None, None


def _resolve_slack_tag(email: str) -> str:
    """Best-effort resolve an email to a Slack `<@USER_ID>` mention.

    Returns `<@SLACK_ID> (email)` when the roster lookup succeeds, or
    the plain email string as fallback.
    """
    try:
        roster = fetch_roster()
        matches = search_roster(roster, email)
        for person in matches:
            slack_id = person.get("slack_id")
            person_email = person.get("slack_email")
            if (
                slack_id
                and isinstance(person_email, str)
                and person_email.lower() == email.lower()
            ):
                return f"<@{slack_id}> ({email})"
    except Exception:
        logger.debug("Could not resolve Slack ID for %s", email, exc_info=True)
    return email


def _build_scope_line(
    scope_type: str,
    scope_id: str,
    *,
    workspace_id: str | None = None,
    organization_name: str | None = None,
    actor_name: str | None = None,
    connector_type: str | None = None,
) -> str:
    """Build the Scope line with a hyperlink when possible."""
    if scope_type == "actor" and workspace_id and connector_type:
        url = f"{_CLOUD_UI_BASE}/workspaces/{workspace_id}/{connector_type}/{scope_id}"
        label = actor_name or scope_id
        return f">*Scope:* <{url}|{label}> (actor)"
    if scope_type == "workspace":
        url = f"{_CLOUD_UI_BASE}/workspaces/{scope_id}"
        return f">*Scope:* <{url}|{scope_id}> (workspace)"
    if scope_type == "organization":
        url = f"{_CLOUD_UI_BASE}/organization/{scope_id}/workspaces"
        label = organization_name or scope_id
        return f">*Scope:* <{url}|{label}> (organization)"
    return f">*Scope:* {scope_type} ({scope_id})"


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
    workspace_id: str | None = None,
    organization_name: str | None = None,
    actor_name: str | None = None,
) -> None:
    """Post a version-override audit notification to the Slack channel.

    Best-effort: logs and swallows errors so a Slack failure never blocks
    the override operation itself.
    """
    emoji = "📍" if action == "set" else "📌"
    action_label = "Set" if action == "set" else "Removed"
    header = f"{emoji} *Connector Version Pin — {action_label}*"

    lines = [header]

    # Connector + version on one line when setting.
    if version:
        lines.append(f">*Connector:* {connector_name} · `{version}`")
    else:
        lines.append(f">*Connector:* {connector_name}")

    # Scope with hyperlink.
    lines.append(
        _build_scope_line(
            scope_type,
            scope_id,
            workspace_id=workspace_id,
            organization_name=organization_name,
            actor_name=actor_name,
            connector_type=connector_type,
        )
    )

    # Workspace context (when scope is actor, show the parent workspace).
    if scope_type == "actor" and workspace_id:
        ws_url = f"{_CLOUD_UI_BASE}/workspaces/{workspace_id}"
        lines.append(f">*Workspace:* <{ws_url}|{workspace_id}>")

    # Reason first — most important context for auditors.
    if override_reason:
        lines.append(f">*Reason:* {override_reason}")

    if organization_name and scope_type != "organization":
        lines.append(f">*Organization:* {organization_name}")

    if issue_url:
        lines.append(f">*Issue:* {issue_url}")
    if override_reason_reference_url:
        lines.append(f">*Reference:* {override_reason_reference_url}")
    if ai_agent_session_url:
        lines.append(f">*AI Session:* <{ai_agent_session_url}|View Session>")

    # Approved-by last — least interesting for quick scanning.
    if admin_user_email:
        slack_tag = _resolve_slack_tag(admin_user_email)
        lines.append(f">*Approved by:* {slack_tag}")

    try:
        post_channel_message(_VERSION_OVERRIDE_SLACK_CHANNEL, "\n".join(lines))
    except (SlackAPIError, _requests.RequestException):
        logger.warning(
            "Failed to post version-override notification to Slack",
            exc_info=True,
        )


def _validate_version_override_target(target: VersionOverrideTarget) -> None:
    """Fail when target IDs are incompatible with `target.scope`."""
    if target.scope == "actor":
        if not target.workspace_id:
            raise PyAirbyteInputError(
                message="Actor-scope version override target requires workspace_id.",
            )
        if not target.actor_id:
            raise PyAirbyteInputError(
                message="Actor-scope version override target requires actor_id.",
            )
        if target.connector_name is not None:
            raise PyAirbyteInputError(
                message="Actor-scope version override target must not include connector_name.",
            )
        return

    if target.scope == "workspace":
        if not target.workspace_id:
            raise PyAirbyteInputError(
                message="Workspace-scope version override target requires workspace_id.",
            )
        if not target.connector_name:
            raise PyAirbyteInputError(
                message="Workspace-scope version override target requires connector_name.",
            )
        if target.actor_id is not None:
            raise PyAirbyteInputError(
                message="Workspace-scope version override target must not include actor_id.",
            )
        return

    if not target.connector_name:
        raise PyAirbyteInputError(
            message="Organization-scope version override target requires connector_name.",
        )
    if target.workspace_id is not None:
        raise PyAirbyteInputError(
            message="Organization-scope version override target must not include workspace_id.",
        )
    if target.actor_id is not None:
        raise PyAirbyteInputError(
            message="Organization-scope version override target must not include actor_id.",
        )


def _resolve_target_context(
    target: VersionOverrideTarget,
    *,
    gcs_credentials: google.auth.credentials.Credentials | None = None,
) -> tuple[str, bool | None, str | None, TierSourceHealth | None]:
    """Resolve customer tier, EU region, and error message for `target`."""
    if target.scope in ("actor", "workspace"):
        assert target.workspace_id is not None
        ws_resolution = resolve_workspace(
            workspace_id=target.workspace_id,
            credentials=gcs_credentials,
            allow_degraded=True,
        )
        if not ws_resolution.organization_id:
            return (
                ws_resolution.customer_tier,
                ws_resolution.is_eu,
                "Could not resolve organization for workspace.",
                ws_resolution.source_health,
            )
        if ws_resolution.organization_id != target.organization_id:
            return (
                ws_resolution.customer_tier,
                ws_resolution.is_eu,
                "Target organization_id does not match workspace organization.",
                ws_resolution.source_health,
            )
        return (
            ws_resolution.customer_tier,
            ws_resolution.is_eu,
            None,
            ws_resolution.source_health,
        )

    tier_result = get_org_tier(
        organization_id=target.organization_id,
        credentials=gcs_credentials,
        allow_degraded=True,
    )
    return (
        tier_result.customer_tier,
        None,
        None,
        tier_result.source_health,
    )


def _guard_existing_pins(
    *,
    auth: ResolvedCloudAuth,
    target: VersionOverrideTarget,
    version: str | None,
    unset: bool,
    force: bool,
    config_api_root: str,
) -> str | None:
    """Return a blocking message when an existing pin guard fails."""
    if unset or version is None:
        return None

    try:
        access_token = _get_access_token(
            auth.client_id,
            auth.client_secret,
            auth.bearer_token,
            config_api_root,
        )
        if target.scope == "actor":
            assert target.actor_id is not None
            get_endpoint = f"{config_api_root}/{target.connector_type}s/get"
            get_resp = _requests.post(
                get_endpoint,
                json={f"{target.connector_type}Id": target.actor_id},
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "User-Agent": USER_AGENT,
                    "Content-Type": "application/json",
                },
                timeout=30,
            )
            get_resp.raise_for_status()
            actor_definition_id = get_resp.json().get(
                f"{target.connector_type}DefinitionId"
            )
            if not actor_definition_id:
                return "Could not find connector definition ID for actor."
            scopes = [
                (_ScopeType.ACTOR, target.actor_id, "actor"),
                (_ScopeType.WORKSPACE, target.workspace_id or "", "workspace"),
                (_ScopeType.ORGANIZATION, target.organization_id, "organization"),
            ]
        else:
            assert target.connector_name is not None
            actor_definition_id = api_client._resolve_connector_definition_id(
                connector_name=target.connector_name,
                connector_type=target.connector_type,
                config_api_root=config_api_root,
                access_token=access_token,
            )
            if target.scope == "workspace":
                scopes = [
                    (_ScopeType.WORKSPACE, target.workspace_id or "", "workspace"),
                    (_ScopeType.ORGANIZATION, target.organization_id, "organization"),
                ]
            else:
                scopes = [
                    (_ScopeType.ORGANIZATION, target.organization_id, "organization"),
                ]

        guard = check_existing_pins(
            scopes=scopes,
            actor_definition_id=actor_definition_id,
            config_api_root=config_api_root,
            access_token=access_token,
            target_version=version,
            force=force,
        )
    except (
        PyAirbyteInputError,
        CloudAuthError,
        _requests.exceptions.HTTPError,
    ) as e:
        return f"Pin guard check failed: {e}"

    return guard.error_msg


def apply_version_override_to_config_api(
    *,
    auth: ResolvedCloudAuth,
    target: VersionOverrideTarget,
    version: str | None,
    unset: bool,
    override_reason: str | None,
    override_reason_reference_url: str | None,
    user_email: str | None,
    config_api_root: str | None = None,
) -> bool:
    """Apply a normalized version override target to the Config API."""
    _validate_version_override_target(target)
    resolved_config_api_root = config_api_root or constants.CLOUD_CONFIG_API_ROOT

    if target.scope == "actor":
        assert target.workspace_id is not None
        assert target.actor_id is not None
        return api_client.set_connector_version_override(
            connector_id=target.actor_id,
            connector_type=target.connector_type,
            config_api_root=resolved_config_api_root,
            client_id=auth.client_id,
            client_secret=auth.client_secret,
            workspace_id=target.workspace_id,
            version=version,
            unset=unset,
            override_reason=override_reason,
            override_reason_reference_url=override_reason_reference_url,
            user_email=user_email,
            bearer_token=auth.bearer_token,
        )

    if target.scope == "workspace":
        assert target.workspace_id is not None
        assert target.connector_name is not None
        return api_client.set_workspace_connector_version_override(
            workspace_id=target.workspace_id,
            connector_name=target.connector_name,
            connector_type=target.connector_type,
            config_api_root=resolved_config_api_root,
            client_id=auth.client_id,
            client_secret=auth.client_secret,
            bearer_token=auth.bearer_token,
            version=version,
            unset=unset,
            override_reason=override_reason,
            override_reason_reference_url=override_reason_reference_url,
            user_email=user_email,
        )

    assert target.connector_name is not None
    return api_client.set_organization_connector_version_override(
        organization_id=target.organization_id,
        connector_name=target.connector_name,
        connector_type=target.connector_type,
        config_api_root=resolved_config_api_root,
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        bearer_token=auth.bearer_token,
        version=version,
        unset=unset,
        override_reason=override_reason,
        override_reason_reference_url=override_reason_reference_url,
        user_email=user_email,
    )


def _describe_auth_context(
    *,
    user_email: str | None,
    gcs_credentials: google.auth.credentials.Credentials | None,
    auth: ResolvedCloudAuth,
) -> str:
    """Build a human-readable summary of the auth identities in use.

    Included in error messages so operators can debug permission failures.
    """
    parts: list[str] = []
    if user_email:
        parts.append(f"webapp_user={user_email}")
    if gcs_credentials is not None:
        tier_identity = _get_identity_from_credentials(gcs_credentials)
        if tier_identity:
            parts.append(f"tier_identity={tier_identity}")
        else:
            parts.append("tier_identity=application_default")
    else:
        parts.append("tier_identity=none")
    if auth.bearer_token:
        parts.append("config_api_auth=bearer_token")
    elif auth.client_id:
        parts.append("config_api_auth=client_credentials")
    else:
        parts.append("config_api_auth=none")
    return f"Auth context: [{', '.join(parts)}]"


def set_version_override(
    *,
    auth: ResolvedCloudAuth,
    target: VersionOverrideTarget,
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
    user_email: str | None = None,
    gcs_credentials: google.auth.credentials.Credentials | None = None,
) -> VersionOverrideResult:
    """Set or clear a connector version override through one normalized path."""
    _validate_version_override_target(target)
    result_kwargs = _result_identity_kwargs(target)
    auth_context = _describe_auth_context(
        user_email=user_email,
        gcs_credentials=gcs_credentials,
        auth=auth,
    )

    admin_user_email, auth_error = _validate_admin_and_authorization(
        issue_url=issue_url,
        approval_comment_url=approval_comment_url,
        user_email=user_email,
    )
    if auth_error is not None:
        return _build_version_override_result(
            target=target,
            success=False,
            message=f"{auth_error} ({auth_context})",
            result_kwargs=result_kwargs,
        )

    try:
        (
            customer_tier,
            is_eu,
            context_error,
            source_health,
        ) = _resolve_target_context(target, gcs_credentials=gcs_credentials)
    except Exception as exc:
        logger.exception("Tier resolution failed for %s", target)
        return _build_version_override_result(
            target=target,
            success=False,
            message=f"Tier resolution failed: {exc} ({auth_context})",
            result_kwargs=result_kwargs,
        )
    tier_warning = build_tier_warning(customer_tier)
    if context_error is not None:
        return _build_version_override_result(
            target=target,
            success=False,
            message=f"{context_error} ({auth_context})",
            customer_tier=customer_tier,
            is_eu=is_eu,
            tier_warning=tier_warning,
            source_health=source_health,
            result_kwargs=result_kwargs,
        )

    tier_ok, tier_error = validate_tier_filter(
        customer_tier,
        customer_tier_filter,
        source_health=source_health,
        organization_id=target.organization_id,
    )
    if not tier_ok:
        return _build_version_override_result(
            target=target,
            success=False,
            message=f"{tier_error or 'Tier filter mismatch'} ({auth_context})",
            customer_tier=customer_tier,
            is_eu=is_eu,
            tier_warning=tier_warning,
            source_health=source_health,
            result_kwargs=result_kwargs,
        )

    enhanced_override_reason = _build_audit_reason(
        override_reason=override_reason,
        issue_url=issue_url,
        approval_comment_url=approval_comment_url,
        ai_agent_session_url=ai_agent_session_url,
        unset=unset,
    )
    resolved_config_api_root = config_api_root or constants.CLOUD_CONFIG_API_ROOT
    guard_error = _guard_existing_pins(
        auth=auth,
        target=target,
        version=version,
        unset=unset,
        force=force,
        config_api_root=resolved_config_api_root,
    )
    if guard_error is not None:
        return _build_version_override_result(
            target=target,
            success=False,
            message=f"{guard_error} ({auth_context})",
            customer_tier=customer_tier,
            is_eu=is_eu,
            tier_warning=tier_warning,
            source_health=source_health,
            result_kwargs=result_kwargs,
        )

    try:
        result = apply_version_override_to_config_api(
            auth=auth,
            target=target,
            version=version,
            unset=unset,
            override_reason=enhanced_override_reason,
            override_reason_reference_url=override_reason_reference_url,
            user_email=admin_user_email,
            config_api_root=resolved_config_api_root,
        )
    except PyAirbyteInputError as e:
        return _build_version_override_result(
            target=target,
            success=False,
            message=f"{e} ({auth_context})",
            customer_tier=customer_tier,
            is_eu=is_eu,
            tier_warning=tier_warning,
            source_health=source_health,
            result_kwargs=result_kwargs,
        )

    message = _version_override_success_message(
        target=target,
        result=result,
        version=version,
        unset=unset,
    )
    if tier_warning:
        message = f"{tier_warning} {message}"

    if not unset or result:
        scope_id = {
            "actor": target.actor_id,
            "workspace": target.workspace_id,
            "organization": target.organization_id,
        }[target.scope]
        assert scope_id is not None
        actor_display_name: str | None = None
        connector_def_name: str | None = None
        if target.scope == "actor":
            assert target.actor_id is not None
            actor_display_name, connector_def_name = _fetch_actor_notification_context(
                auth=auth,
                actor_id=target.actor_id,
                actor_type=target.connector_type,
                config_api_root=resolved_config_api_root,
            )

        organization_name = _fetch_organization_name(
            target.organization_id,
            resolved_config_api_root,
            client_id=auth.client_id,
            client_secret=auth.client_secret,
            bearer_token=auth.bearer_token,
        )
        connector_name = connector_def_name or (
            f"{target.connector_type} ({target.actor_id})"
            if target.scope == "actor"
            else target.connector_name
        )
        assert connector_name is not None
        _notify_version_override_slack(
            action="removed" if unset else "set",
            scope_type=target.scope,
            scope_id=scope_id,
            connector_name=connector_name,
            connector_type=target.connector_type,
            version=version,
            admin_user_email=admin_user_email,
            override_reason=override_reason,
            issue_url=issue_url,
            ai_agent_session_url=ai_agent_session_url,
            override_reason_reference_url=override_reason_reference_url,
            workspace_id=target.workspace_id,
            organization_name=organization_name,
            actor_name=actor_display_name,
        )

    return _build_version_override_result(
        target=target,
        success=True,
        message=message,
        version=version if not unset else None,
        new_version=version if target.scope == "actor" and not unset else None,
        is_pinned_after=None if unset else True,
        customer_tier=customer_tier,
        is_eu=is_eu,
        tier_warning=tier_warning,
        source_health=source_health,
        result_kwargs=result_kwargs,
    )


@dataclass(frozen=True)
class _VersionOverrideResultKwargs:
    """Shared identity fields for the historical result models."""

    connector_id: str | None = None
    workspace_id: str | None = None
    organization_id: str | None = None
    connector_name: str | None = None


def _result_identity_kwargs(
    target: VersionOverrideTarget,
) -> _VersionOverrideResultKwargs:
    """Return identity fields shared by result models."""
    if target.scope == "actor":
        assert target.actor_id is not None
        return _VersionOverrideResultKwargs(connector_id=target.actor_id)
    if target.scope == "workspace":
        assert target.workspace_id is not None
        assert target.connector_name is not None
        return _VersionOverrideResultKwargs(
            workspace_id=target.workspace_id,
            connector_name=target.connector_name,
        )
    assert target.connector_name is not None
    return _VersionOverrideResultKwargs(
        organization_id=target.organization_id,
        connector_name=target.connector_name,
    )


def _build_version_override_result(
    *,
    target: VersionOverrideTarget,
    success: bool,
    message: str,
    result_kwargs: _VersionOverrideResultKwargs,
    connector_type: VersionOverrideConnectorType | None = None,
    version: str | None = None,
    new_version: str | None = None,
    is_pinned_after: bool | None = None,
    customer_tier: str | None = None,
    is_eu: bool | None = None,
    tier_warning: str | None = None,
    source_health: TierSourceHealth | None = None,
) -> VersionOverrideResult:
    """Build the historical result model for `target.scope`."""
    if connector_type is None:
        connector_type = target.connector_type
    warnings = tier_source_warnings(source_health)
    if target.scope == "actor":
        assert result_kwargs.connector_id is not None
        return VersionOverrideOperationResult(
            success=success,
            message=message,
            connector_id=result_kwargs.connector_id,
            connector_type=connector_type,
            new_version=new_version,
            is_pinned_after=is_pinned_after,
            customer_tier=customer_tier,
            is_eu=is_eu,
            tier_warning=tier_warning,
            warnings=warnings,
        )
    if target.scope == "workspace":
        assert result_kwargs.workspace_id is not None
        assert result_kwargs.connector_name is not None
        return WorkspaceVersionOverrideResult(
            success=success,
            message=message,
            workspace_id=result_kwargs.workspace_id,
            connector_name=result_kwargs.connector_name,
            connector_type=connector_type,
            version=version,
            customer_tier=customer_tier,
            is_eu=is_eu,
            tier_warning=tier_warning,
            warnings=warnings,
        )
    assert result_kwargs.organization_id is not None
    assert result_kwargs.connector_name is not None
    return OrganizationVersionOverrideResult(
        success=success,
        message=message,
        organization_id=result_kwargs.organization_id,
        connector_name=result_kwargs.connector_name,
        connector_type=connector_type,
        version=version,
        customer_tier=customer_tier,
        tier_warning=tier_warning,
        warnings=warnings,
    )


def _version_override_success_message(
    *,
    target: VersionOverrideTarget,
    result: bool,
    version: str | None,
    unset: bool,
) -> str:
    """Return a human-readable success message for `target.scope`."""
    if target.scope == "actor":
        if unset:
            if result:
                return "Successfully cleared version override. Connector will now use default version."
            return "No version override was active (nothing to clear)"
        return f"Successfully pinned connector to version {version}"

    assert target.connector_name is not None
    if target.scope == "workspace":
        if unset:
            if result:
                return f"Successfully cleared workspace-level version override for {target.connector_name}."
            return f"No workspace-level version override was active for {target.connector_name} (nothing to clear)"
        return f"Successfully pinned {target.connector_name} to version {version} at workspace level."

    if unset:
        if result:
            return f"Successfully cleared organization-level version override for {target.connector_name}."
        return f"No organization-level version override was active for {target.connector_name} (nothing to clear)"
    return f"Successfully pinned {target.connector_name} to version {version} at organization level."


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
    ws_resolution = resolve_workspace(
        workspace_id=workspace_id,
        allow_degraded=True,
    )
    if not ws_resolution.organization_id:
        return VersionOverrideOperationResult(
            success=False,
            message=f"Could not resolve organization for workspace {workspace_id}",
            connector_id=actor_id,
            connector_type=actor_type,
        )

    result = set_version_override(
        auth=auth,
        target=VersionOverrideTarget(
            scope="actor",
            organization_id=ws_resolution.organization_id,
            workspace_id=workspace_id,
            actor_id=actor_id,
            connector_type=actor_type,
        ),
        approval_comment_url=approval_comment_url,
        version=version,
        unset=unset,
        override_reason=override_reason,
        override_reason_reference_url=override_reason_reference_url,
        issue_url=issue_url,
        ai_agent_session_url=ai_agent_session_url,
        customer_tier_filter=customer_tier_filter,
        force=force,
        config_api_root=config_api_root,
    )
    assert isinstance(result, VersionOverrideOperationResult)
    return result


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
    ws_resolution = resolve_workspace(
        workspace_id=workspace_id,
        allow_degraded=True,
    )
    if not ws_resolution.organization_id:
        return WorkspaceVersionOverrideResult(
            success=False,
            message=f"Could not resolve organization for workspace {workspace_id}",
            workspace_id=workspace_id,
            connector_name=connector_name,
            connector_type=connector_type,
        )

    result = set_version_override(
        auth=auth,
        target=VersionOverrideTarget(
            scope="workspace",
            organization_id=ws_resolution.organization_id,
            workspace_id=workspace_id,
            connector_name=connector_name,
            connector_type=connector_type,
        ),
        approval_comment_url=approval_comment_url,
        version=version,
        unset=unset,
        override_reason=override_reason,
        override_reason_reference_url=override_reason_reference_url,
        issue_url=issue_url,
        ai_agent_session_url=ai_agent_session_url,
        customer_tier_filter=customer_tier_filter,
        force=force,
        config_api_root=config_api_root,
    )
    assert isinstance(result, WorkspaceVersionOverrideResult)
    return result


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
    result = set_version_override(
        auth=auth,
        target=VersionOverrideTarget(
            scope="organization",
            organization_id=organization_id,
            connector_name=connector_name,
            connector_type=connector_type,
        ),
        approval_comment_url=approval_comment_url,
        version=version,
        unset=unset,
        override_reason=override_reason,
        override_reason_reference_url=override_reason_reference_url,
        issue_url=issue_url,
        ai_agent_session_url=ai_agent_session_url,
        customer_tier_filter=customer_tier_filter,
        force=force,
        config_api_root=config_api_root,
    )
    assert isinstance(result, OrganizationVersionOverrideResult)
    return result
