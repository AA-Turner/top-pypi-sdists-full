# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for LaunchDarkly flag organization targeting.

This module exposes tools for reading LaunchDarkly feature flags and for
adding or removing individual organization targets on allowlisted flags
(those tagged `ops-mcp`), gated by human-in-the-loop approval.

## MCP reference

.. include:: ../../../docs/mcp-generated/feature_flags.md
    :start-line: 2
"""

# NOTE: We intentionally do NOT use `from __future__ import annotations` here.
# FastMCP has issues resolving forward references when PEP 563 deferred
# annotations are used. See: https://github.com/jlowin/fastmcp/issues/905

__all__: list[str] = []

from typing import Annotated, Any, Literal

from fastmcp import Context, FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import Field

from airbyte_ops_mcp.approval_resolution import (
    ApprovalResolutionError,
    resolve_admin_email_from_approval,
)
from airbyte_ops_mcp.cloud_admin import launchdarkly_flags
from airbyte_ops_mcp.cloud_admin.auth import (
    CloudAuthError,
    require_internal_admin_flag_only,
)
from airbyte_ops_mcp.cloud_admin.launchdarkly_flags import (
    LD_OPS_MCP_TAG,
    LaunchDarklyAPIError,
    LaunchDarklyVerificationError,
    apply_org_target_change,
    build_change_comment,
    flag_is_ops_targetable,
    list_flags,
    select_variation,
    variation_id_of,
)
from airbyte_ops_mcp.cloud_admin.models import (
    LDFeatureFlagInfo,
    LDFeatureFlagList,
    LDFlagOrgTargetUpdateResult,
    LDFlagVariationInfo,
    OrganizationAgenticFlagInfo,
    OrganizationInfo,
)
from airbyte_ops_mcp.mcp.organization_admin import (
    _row_to_flag_info,
    _validate_organization_name,
)
from airbyte_ops_mcp.prod_db_access.queries import query_organization_agentic_flags
from airbyte_ops_mcp.tier_cache import (
    get_org_tier,
    tier_source_warnings,
)


def _flag_to_targets_info(flag: dict[str, Any]) -> LDFeatureFlagInfo:
    """Convert a raw LaunchDarkly flag dict into org-targeting info."""
    env = (flag.get("environments") or {}).get("production") or {}
    variations: list[LDFlagVariationInfo] = []
    for index, variation in enumerate(flag.get("variations") or []):
        variations.append(
            LDFlagVariationInfo(
                index=index,
                variation_id=variation_id_of(variation),
                name=variation.get("name"),
                value=variation.get("value"),
                organization_targets=launchdarkly_flags.get_org_targets(flag, index),
            )
        )
    return LDFeatureFlagInfo(
        flag_key=str(flag.get("key")),
        flag_name=flag.get("name"),
        kind=flag.get("kind"),
        tags=list(flag.get("tags") or []),
        ops_mcp_addressable=flag_is_ops_targetable(flag),
        on=bool(env.get("on")),
        variations=variations,
    )


def _failure_result(
    message: str,
    flag_key: str,
    organization_id: str,
    action: Literal["add", "remove"],
    **kwargs: Any,
) -> LDFlagOrgTargetUpdateResult:
    """Build a `success=False` update result for a rejected request."""
    return LDFlagOrgTargetUpdateResult(
        success=False,
        message=message,
        flag_key=flag_key,
        organization_id=organization_id,
        action=action,
        **kwargs,
    )


def _success_result(
    message: str,
    flag_key: str,
    organization_id: str,
    action: Literal["add", "remove"],
    **kwargs: Any,
) -> LDFlagOrgTargetUpdateResult:
    """Build a `success=True` update result."""
    return LDFlagOrgTargetUpdateResult(
        success=True,
        message=message,
        flag_key=flag_key,
        organization_id=organization_id,
        action=action,
        **kwargs,
    )


def _load_target_organization(
    organization_id: str,
    organization_name: str | None,
) -> tuple[OrganizationAgenticFlagInfo | None, str | None]:
    """Look up the target organization and validate `organization_name`.

    Returns `(info, error_message)`; `error_message` is `None` on success.
    `info` is returned alongside the error when the organization exists but
    failed the tombstone or name check, so callers can report identity.
    """
    rows = query_organization_agentic_flags([organization_id])
    if not rows:
        return None, f"Organization {organization_id} not found."
    current_info = _row_to_flag_info(rows[0])
    if current_info.tombstone:
        return current_info, f"Organization {organization_id} is tombstoned."
    org_info = OrganizationInfo.model_validate(
        {
            "organizationId": current_info.organization_id,
            "organizationName": current_info.organization_name or "",
            "email": current_info.email,
            "isAgentic": current_info.is_agentic,
        }
    )
    name_ok, name_error = _validate_organization_name(
        organization_id, organization_name, org_info
    )
    if not name_ok:
        return current_info, name_error or "Organization name validation failed."
    return current_info, None


@mcp_tool(
    destructive=False,
    idempotent=True,
    open_world=True,
)
def list_launchdarkly_feature_flags(
    tag: Annotated[
        str | None,
        Field(
            description="Optional LaunchDarkly tag filter, passed through to "
            "the API. Use 'ops-mcp' to list only flags addressable by "
            "`update_launchdarkly_feature_flag_targeting`.",
            default=None,
        ),
    ] = None,
    flag_contains: Annotated[
        str | None,
        Field(
            description="Optional case-insensitive substring matched against "
            "the flag key or display name.",
            default=None,
        ),
    ] = None,
    limit: Annotated[
        int,
        Field(
            description="Maximum number of flags to return.",
            ge=1,
            le=500,
        ),
    ] = 50,
    *,
    ctx: Context,
) -> LDFeatureFlagList:
    """List LaunchDarkly feature flags with their organization targets.

    Returns flags in the `default` project with each variation's individual
    `organization` targets in the `production` environment. Results can be
    narrowed by the LaunchDarkly `tag` filter and by a case-insensitive
    `flag_contains` substring on the flag key or display name, and are
    truncated to `limit`.

    The `ops_mcp_addressable` field marks flags tagged `ops-mcp` — only
    those may be modified with `update_launchdarkly_feature_flag_targeting`.
    """
    flags = list_flags(tag=tag)
    if flag_contains is not None:
        needle = flag_contains.lower()
        flags = [
            flag
            for flag in flags
            if needle in str(flag.get("key") or "").lower()
            or needle in str(flag.get("name") or "").lower()
        ]
    truncated = len(flags) > limit
    return LDFeatureFlagList(
        flags=[_flag_to_targets_info(flag) for flag in flags[:limit]],
        total_returned=min(len(flags), limit),
        truncated=truncated,
    )


@mcp_tool(
    destructive=False,
    idempotent=True,
    open_world=True,
)
def describe_launchdarkly_feature_flag(
    flag_key: Annotated[
        str,
        Field(description="The LaunchDarkly flag key."),
    ],
    *,
    ctx: Context,
) -> LDFeatureFlagInfo:
    """Get a LaunchDarkly flag's production organization targets.

    Works for any flag in the `default` project, including untagged flags;
    the result's `ops_mcp_addressable` field reports whether the flag carries
    the `ops-mcp` tag required by `update_launchdarkly_feature_flag_targeting`.
    """
    flag = launchdarkly_flags.get_flag(flag_key)
    return _flag_to_targets_info(flag)


@mcp_tool(
    destructive=True,
    idempotent=True,
    open_world=True,
)
def update_launchdarkly_feature_flag_targeting(
    flag_key: Annotated[
        str,
        Field(description="The LaunchDarkly flag key."),
    ],
    organization_id: Annotated[
        str,
        Field(description="The Airbyte Cloud organization UUID to target."),
    ],
    action: Annotated[
        Literal["add", "remove"],
        Field(
            description="Whether to add or remove the organization as an "
            "individual target."
        ),
    ],
    approval_comment_url: Annotated[
        str,
        Field(
            description="URL to the Slack approval record. Obtain this by calling "
            "`escalate_to_human` with `approval_requested=True`; the backend "
            "delivers the approval record URL when a human clicks Approve.",
        ),
    ],
    organization_name: Annotated[
        str | None,
        Field(
            description="Confirmation of the target organization. Accepts the "
            "organization name, email address, or email domain. Required.",
            default=None,
        ),
    ] = None,
    variation: Annotated[
        str | None,
        Field(
            description="Variation to target, matched case-insensitively on the "
            "variation name or on `str(value)` (so 'true'/'false' work). "
            "For `add`: optional for boolean flags (defaults to the `True` "
            "variation), required for multivariate flags. For `remove`: "
            "omitting it removes the organization from whichever variation "
            "currently targets it.",
            default=None,
        ),
    ] = None,
    agent_session_url: Annotated[
        str | None,
        Field(
            description="Optional agent session URL recorded in the "
            "LaunchDarkly change comment for auditability.",
            default=None,
        ),
    ] = None,
    *,
    ctx: Context,
) -> LDFlagOrgTargetUpdateResult:
    """Add or remove an organization as an individual target on a flag.

    Guardrails:

    - Only emits `addTargets`/`removeTargets` semantic-patch instructions on
      `contextKind=organization` individual targets.
    - Only writes to the `production` environment of the `default` project.
    - Only flags tagged `ops-mcp` in LaunchDarkly are eligible; all other
      flags are rejected before any write.
    - Requires human-in-the-loop approval: call `escalate_to_human` with
      `approval_requested=True` and pass the resulting approval record URL
      as `approval_comment_url`.
    """
    try:
        require_internal_admin_flag_only()
    except CloudAuthError as e:
        return _failure_result(
            f"Admin authentication failed: {e}",
            flag_key,
            organization_id,
            action,
        )

    organization_id = organization_id.strip().lower()

    try:
        flag = launchdarkly_flags.get_flag(flag_key)
    except LaunchDarklyAPIError as e:
        return _failure_result(str(e), flag_key, organization_id, action)
    if not flag_is_ops_targetable(flag):
        return _failure_result(
            f"Flag {flag_key!r} is not addressable by Ops MCP. Add the "
            f"{LD_OPS_MCP_TAG!r} tag to the flag in LaunchDarkly to opt it in.",
            flag_key,
            organization_id,
            action,
        )

    try:
        selection = select_variation(
            flag,
            action=action,
            organization_id=organization_id,
            variation=variation,
        )
    except LaunchDarklyAPIError as e:
        return _failure_result(str(e), flag_key, organization_id, action)

    try:
        approver_email = resolve_admin_email_from_approval(
            approval_comment_url=approval_comment_url,
        )
    except ApprovalResolutionError as e:
        return _failure_result(str(e), flag_key, organization_id, action)

    current_info, org_error = _load_target_organization(
        organization_id, organization_name
    )
    if org_error is not None:
        return _failure_result(
            org_error,
            flag_key,
            organization_id,
            action,
            organization_name=(
                current_info.organization_name if current_info else None
            ),
            email=current_info.email if current_info else None,
        )
    assert current_info is not None

    tier_result = get_org_tier(
        organization_id=organization_id,
        allow_degraded=True,
    )
    customer_tier = tier_result.customer_tier
    warnings = tier_source_warnings(tier_result.source_health)

    previous_targets = selection.previous_targets
    already_targeted = organization_id in previous_targets
    result_kwargs: dict[str, Any] = {
        "organization_name": current_info.organization_name,
        "email": current_info.email,
        "variation_name": selection.name,
        "previous_targets": previous_targets,
        "customer_tier": customer_tier,
        "warnings": warnings,
    }
    if action == "add" and already_targeted:
        return _success_result(
            f"Organization {organization_id} is already individually "
            f"targeted on flag {flag_key!r}.",
            flag_key,
            organization_id,
            action,
            new_targets=previous_targets,
            **result_kwargs,
        )
    if action == "remove" and (selection.index is None or not already_targeted):
        return _success_result(
            f"Organization {organization_id} is not individually "
            f"targeted on flag {flag_key!r}; nothing to remove.",
            flag_key,
            organization_id,
            action,
            new_targets=previous_targets,
            **result_kwargs,
        )

    comment = build_change_comment(
        action,
        organization_id,
        approver_email,
        agent_session_url,
    )
    try:
        new_targets, warnings = apply_org_target_change(
            flag_key,
            action=action,
            selection=selection,
            organization_id=organization_id,
            comment=comment,
            verify_all_variations=(action == "remove" and variation is None),
        )
    except LaunchDarklyVerificationError as e:
        return _failure_result(
            str(e),
            flag_key,
            organization_id,
            action,
            new_targets=e.new_targets,
            **result_kwargs,
        )
    except LaunchDarklyAPIError as e:
        return _failure_result(
            str(e), flag_key, organization_id, action, **result_kwargs
        )
    result_kwargs["warnings"] = warnings

    verb = "added to" if action == "add" else "removed from"
    return _success_result(
        f"Organization {organization_id} {verb} the individual targets "
        f"of flag {flag_key!r}.",
        flag_key,
        organization_id,
        action,
        new_targets=new_targets,
        **result_kwargs,
    )


def register_launchdarkly_ops_tools(app: FastMCP) -> None:
    """Register launchdarkly_ops tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
