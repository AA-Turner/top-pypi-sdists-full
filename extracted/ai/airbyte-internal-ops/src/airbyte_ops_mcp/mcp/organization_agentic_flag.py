# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for organization `is_agentic` flag management.

Provides tools to read and update the Airbyte Cloud organization `is_agentic`
flag.

## MCP reference

.. include:: ../../../docs/mcp-generated/organization_agentic_flag.md
    :start-line: 2
"""

# NOTE: We intentionally do NOT use `from __future__ import annotations` here.
# FastMCP has issues resolving forward references when PEP 563 deferred annotations
# are used. See: https://github.com/jlowin/fastmcp/issues/905

__all__: list[str] = []

from typing import Annotated

from airbyte import constants
from fastmcp import Context, FastMCP
from fastmcp_extensions import get_mcp_config, mcp_tool, register_mcp_tools
from pydantic import Field

from airbyte_ops_mcp.approval_resolution import (
    ApprovalResolutionError,
    resolve_admin_email_from_approval,
)
from airbyte_ops_mcp.cloud_admin.auth import (
    CloudAuthError,
    require_internal_admin_flag_only,
)
from airbyte_ops_mcp.cloud_admin.models import (
    OrganizationAgenticFlagBatchInfo,
    OrganizationAgenticFlagBatchUpdateResult,
    OrganizationAgenticFlagInfo,
    OrganizationAgenticFlagUpdateResult,
    OrganizationInfo,
)
from airbyte_ops_mcp.cloud_admin.organization_agentic_flag import (
    OrganizationAgenticFlagAPIError,
)
from airbyte_ops_mcp.cloud_admin.organization_agentic_flag import (
    get_organization_info as _get_organization_info,
)
from airbyte_ops_mcp.cloud_admin.organization_agentic_flag import (
    set_organization_agentic_status as _set_organization_agentic_status,
)
from airbyte_ops_mcp.cloud_admin.version_overrides import validate_tier_filter
from airbyte_ops_mcp.constants import ServerConfigKey
from airbyte_ops_mcp.mcp.organization_payment_config import (
    _build_tier_warning,
    _validate_organization_name,
)
from airbyte_ops_mcp.prod_db_access.queries import (
    query_organization_agentic_flags,
)
from airbyte_ops_mcp.tier_cache import TierFilter, get_org_tier


def _normalize_organization_ids(organization_ids: str | list[str]) -> list[str]:
    """Normalize one organization ID or a list of organization IDs."""
    ids = [organization_ids] if isinstance(organization_ids, str) else organization_ids

    normalized = [org_id.strip() for org_id in ids if org_id and org_id.strip()]
    return list(dict.fromkeys(normalized))


def _build_update_failure_results(
    organization_ids: list[str],
    message: str,
) -> list[OrganizationAgenticFlagUpdateResult]:
    """Build per-org failure results for request-level validation failures."""
    return [
        OrganizationAgenticFlagUpdateResult(
            success=False,
            message=message,
            organization_id=organization_id,
        )
        for organization_id in organization_ids
    ]


def _resolve_cloud_auth(ctx: Context) -> tuple[str | None, str | None, str | None]:
    """Resolve auth credentials, returning `(bearer_token, client_id, client_secret)`."""
    bearer_token = get_mcp_config(ctx, ServerConfigKey.BEARER_TOKEN)
    if bearer_token:
        return bearer_token, None, None

    client_id = get_mcp_config(ctx, ServerConfigKey.CLIENT_ID)
    client_secret = get_mcp_config(ctx, ServerConfigKey.CLIENT_SECRET)
    return None, client_id, client_secret


def _org_info_to_flag_info(
    org_info: OrganizationInfo,
    customer_tier: str | None = None,
    tier_warning: str | None = None,
) -> OrganizationAgenticFlagInfo:
    """Convert Config API organization info into agentic flag info."""
    return OrganizationAgenticFlagInfo(
        organization_id=org_info.organization_id,
        organization_name=org_info.organization_name,
        email=org_info.email,
        tombstone=False,
        is_agentic=org_info.is_agentic or False,
        customer_tier=customer_tier,
        tier_warning=tier_warning,
    )


def _row_to_flag_info(
    row: dict[str, object],
    customer_tier: str | None = None,
    tier_warning: str | None = None,
) -> OrganizationAgenticFlagInfo:
    """Convert a DB row into agentic flag info."""
    return OrganizationAgenticFlagInfo(
        organization_id=str(row["organization_id"]),
        organization_name=str(row["organization_name"])
        if row["organization_name"] is not None
        else None,
        email=str(row["email"]) if row["email"] is not None else None,
        tombstone=bool(row["tombstone"]),
        is_agentic=bool(row["is_agentic"]),
        customer_tier=customer_tier,
        tier_warning=tier_warning,
    )


@mcp_tool(
    destructive=False,
    idempotent=True,
    open_world=True,
)
def get_organization_agentic_flag(
    organization_ids: Annotated[
        str | list[str],
        Field(
            description="One organization UUID, or a list of organization UUIDs.",
        ),
    ],
    config_api_root: Annotated[
        str | None,
        Field(
            description="Optional Config API root URL override. When omitted, "
            "the tool reads from the Prod DB replica.",
            default=None,
        ),
    ] = None,
    *,
    ctx: Context,
) -> OrganizationAgenticFlagBatchInfo:
    """Get the current `is_agentic` flag for one or more organizations."""
    normalized_ids = _normalize_organization_ids(organization_ids)
    if not normalized_ids:
        return OrganizationAgenticFlagBatchInfo(
            organizations=[],
            missing_organization_ids=[],
        )

    if config_api_root is None:
        rows = query_organization_agentic_flags(normalized_ids)
        rows_by_org_id = {str(row["organization_id"]): row for row in rows}
        organizations: list[OrganizationAgenticFlagInfo] = []
        for organization_id in normalized_ids:
            row = rows_by_org_id.get(organization_id)
            if row is None:
                continue
            tier_result = get_org_tier(organization_id)
            organizations.append(
                _row_to_flag_info(
                    row,
                    customer_tier=tier_result.customer_tier,
                    tier_warning=_build_tier_warning(tier_result.customer_tier),
                )
            )
        return OrganizationAgenticFlagBatchInfo(
            organizations=organizations,
            missing_organization_ids=[
                organization_id
                for organization_id in normalized_ids
                if organization_id not in rows_by_org_id
            ],
        )

    resolved_api_root = config_api_root or constants.CLOUD_CONFIG_API_ROOT
    bearer_token, client_id, client_secret = _resolve_cloud_auth(ctx)

    organizations: list[OrganizationAgenticFlagInfo] = []
    missing_organization_ids: list[str] = []
    for organization_id in normalized_ids:
        try:
            org_info = _get_organization_info(
                organization_id=organization_id,
                config_api_root=resolved_api_root,
                client_id=client_id,
                client_secret=client_secret,
                bearer_token=bearer_token,
            )
        except OrganizationAgenticFlagAPIError:
            missing_organization_ids.append(organization_id)
            continue
        if org_info is None:
            missing_organization_ids.append(organization_id)
            continue

        tier_result = get_org_tier(organization_id)
        organizations.append(
            _org_info_to_flag_info(
                org_info,
                customer_tier=tier_result.customer_tier,
                tier_warning=_build_tier_warning(tier_result.customer_tier),
            )
        )

    return OrganizationAgenticFlagBatchInfo(
        organizations=organizations,
        missing_organization_ids=missing_organization_ids,
    )


@mcp_tool(
    destructive=True,
    idempotent=True,
    open_world=True,
)
def update_organization_agentic_flag(
    organization_ids: Annotated[
        str | list[str],
        Field(
            description="One organization UUID, or a list of organization UUIDs.",
        ),
    ],
    is_agentic: Annotated[
        bool,
        Field(description="The desired `is_agentic` value."),
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
            "organization name, email address, or email domain. Required when "
            "updating a single organization. Ignored for multi-org updates; use "
            "`organization_names` instead.",
            default=None,
        ),
    ] = None,
    organization_names: Annotated[
        dict[str, str] | None,
        Field(
            description="Per-organization confirmation for multi-org updates. "
            "Keys are organization UUIDs; values may be organization names, "
            "email addresses, or email domains.",
            default=None,
        ),
    ] = None,
    customer_tier_filter: Annotated[
        TierFilter,
        Field(
            description=(
                "Required tier filter: 'TIER_0', 'TIER_1', 'TIER_2', or 'ALL'. "
                "The operation is rejected if the actual customer tier does not match. "
                "Use 'ALL' to proceed regardless of tier after human approval."
            ),
        ),
    ] = "TIER_2",
    *,
    ctx: Context,
) -> OrganizationAgenticFlagBatchUpdateResult:
    """Update the `is_agentic` flag for one or more organizations.

    All updates require human-in-the-loop approval via `escalate_to_human`.
    The tool validates each organization identity before writing the flag.
    """
    normalized_ids = _normalize_organization_ids(organization_ids)
    if not normalized_ids:
        return OrganizationAgenticFlagBatchUpdateResult(
            success=False,
            message="No organization IDs provided.",
            results=[],
        )

    try:
        require_internal_admin_flag_only()
    except CloudAuthError as e:
        return OrganizationAgenticFlagBatchUpdateResult(
            success=False,
            message=f"Admin authentication failed: {e}",
            results=_build_update_failure_results(
                normalized_ids, f"Admin authentication failed: {e}"
            ),
        )

    try:
        resolve_admin_email_from_approval(
            approval_comment_url=approval_comment_url,
        )
    except ApprovalResolutionError as e:
        return OrganizationAgenticFlagBatchUpdateResult(
            success=False,
            message=str(e),
            results=_build_update_failure_results(normalized_ids, str(e)),
        )

    bearer_token, client_id, client_secret = _resolve_cloud_auth(ctx)

    results: list[OrganizationAgenticFlagUpdateResult] = []
    for organization_id in normalized_ids:
        rows = query_organization_agentic_flags([organization_id])
        if not rows:
            results.append(
                OrganizationAgenticFlagUpdateResult(
                    success=False,
                    message=f"Organization {organization_id} not found.",
                    organization_id=organization_id,
                )
            )
            continue

        current_info = _row_to_flag_info(rows[0])
        if current_info.tombstone:
            results.append(
                OrganizationAgenticFlagUpdateResult(
                    success=False,
                    message=f"Organization {organization_id} is tombstoned.",
                    organization_id=organization_id,
                    organization_name=current_info.organization_name,
                    email=current_info.email,
                    previous_is_agentic=current_info.is_agentic,
                )
            )
            continue

        org_info = OrganizationInfo.model_validate(
            {
                "organizationId": current_info.organization_id,
                "organizationName": current_info.organization_name or "",
                "email": current_info.email,
                "isAgentic": current_info.is_agentic,
            }
        )
        expected_name = (
            organization_names.get(organization_id)
            if organization_names is not None
            else organization_name
        )
        name_ok, name_error = _validate_organization_name(
            organization_id, expected_name, org_info
        )
        if not name_ok:
            results.append(
                OrganizationAgenticFlagUpdateResult(
                    success=False,
                    message=name_error or "Organization name validation failed.",
                    organization_id=organization_id,
                    organization_name=current_info.organization_name,
                    email=current_info.email,
                    previous_is_agentic=current_info.is_agentic,
                )
            )
            continue

        tier_result = get_org_tier(organization_id)
        customer_tier = tier_result.customer_tier
        tier_warning = _build_tier_warning(customer_tier)
        tier_ok, tier_error = validate_tier_filter(customer_tier, customer_tier_filter)
        if not tier_ok:
            results.append(
                OrganizationAgenticFlagUpdateResult(
                    success=False,
                    message=tier_error or "Customer tier validation failed.",
                    organization_id=organization_id,
                    organization_name=current_info.organization_name,
                    email=current_info.email,
                    previous_is_agentic=current_info.is_agentic,
                    customer_tier=customer_tier,
                    tier_warning=tier_warning,
                )
            )
            continue
        previous_is_agentic = current_info.is_agentic

        if previous_is_agentic == is_agentic:
            results.append(
                OrganizationAgenticFlagUpdateResult(
                    success=True,
                    message=(
                        f"Organization {organization_id} already has managed agentic "
                        f"org status {is_agentic}."
                    ),
                    organization_id=organization_id,
                    organization_name=current_info.organization_name,
                    email=current_info.email,
                    previous_is_agentic=previous_is_agentic,
                    new_is_agentic=is_agentic,
                    customer_tier=customer_tier,
                    tier_warning=tier_warning,
                )
            )
            continue

        try:
            updated = _set_organization_agentic_status(
                organization_id=organization_id,
                is_agentic=is_agentic,
                config_api_root=constants.CLOUD_CONFIG_API_ROOT,
                client_id=client_id,
                client_secret=client_secret,
                bearer_token=bearer_token,
            )
        except Exception as e:
            results.append(
                OrganizationAgenticFlagUpdateResult(
                    success=False,
                    message=str(e),
                    organization_id=organization_id,
                    organization_name=current_info.organization_name,
                    email=current_info.email,
                    previous_is_agentic=previous_is_agentic,
                    customer_tier=customer_tier,
                    tier_warning=tier_warning,
                )
            )
            continue

        updated_info = _org_info_to_flag_info(
            updated,
            customer_tier=customer_tier,
            tier_warning=tier_warning,
        )
        results.append(
            OrganizationAgenticFlagUpdateResult(
                success=True,
                message=(
                    f"Organization {organization_id} updated managed agentic org "
                    f"status to {updated_info.is_agentic}."
                ),
                organization_id=organization_id,
                organization_name=updated_info.organization_name,
                email=updated_info.email,
                previous_is_agentic=previous_is_agentic,
                new_is_agentic=updated_info.is_agentic,
                customer_tier=customer_tier,
                tier_warning=tier_warning,
            )
        )

    success = all(result.success for result in results)
    return OrganizationAgenticFlagBatchUpdateResult(
        success=success,
        message=(
            f"Updated {sum(result.success for result in results)} of "
            f"{len(results)} organization agentic flag request(s)."
        ),
        results=results,
    )


def register_organization_agentic_flag_tools(app: FastMCP) -> None:
    """Register organization agentic flag MCP tools."""
    register_mcp_tools(app, mcp_module=__name__)
