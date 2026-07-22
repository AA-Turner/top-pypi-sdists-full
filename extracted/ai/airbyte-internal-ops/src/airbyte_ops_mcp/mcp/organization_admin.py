# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for organization administration: is_agentic flag, payment config, and customer-tier lookup/cache.

## MCP reference

.. include:: ../../../docs/mcp-generated/organization_admin.md
    :start-line: 2
"""

# NOTE: We intentionally do NOT use `from __future__ import annotations` here.
# FastMCP has issues resolving forward references when PEP 563 deferred annotations
# are used. See: https://github.com/jlowin/fastmcp/issues/905
# Python 3.12+ supports modern type hint syntax natively, so this is not needed.

__all__: list[str] = []

import logging
import re
from datetime import date, datetime, timedelta, timezone
from typing import Annotated, Any, Literal

import requests
from airbyte import constants
from fastmcp import Context, FastMCP
from fastmcp_extensions import get_mcp_config, mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field
from zoneinfo import ZoneInfo

from airbyte_ops_mcp.approval_resolution import (
    ApprovalResolutionError,
    resolve_admin_email_from_approval,
)
from airbyte_ops_mcp.cloud_admin.auth import (
    CloudAuthError,
    require_internal_admin_flag_only,
)
from airbyte_ops_mcp.cloud_admin.entitlements import (
    WAIVER_TYPE_TO_ENTITLEMENT_PLAN,
    EntitlementAPIError,
    update_entitlement_plan,
)
from airbyte_ops_mcp.cloud_admin.models import (
    OrbSubscriptionInfo,
    OrganizationAgenticFlagBatchInfo,
    OrganizationAgenticFlagBatchUpdateResult,
    OrganizationAgenticFlagInfo,
    OrganizationAgenticFlagUpdateResult,
    OrganizationInfo,
    OrganizationPaymentConfigInfo,
    OrganizationPaymentConfigUpdateResult,
)
from airbyte_ops_mcp.cloud_admin.orb_billing import (
    OrbAPIError,
    _get_orb_api_key,
    _resolve_plan_id,
    extract_subscription_summary,
    get_active_subscription,
    schedule_plan_change,
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
from airbyte_ops_mcp.cloud_admin.payment_config import (
    PaymentConfigAPIError,
    get_organization_info,
)
from airbyte_ops_mcp.cloud_admin.payment_config import (
    get_organization_payment_config as _get_organization_payment_config,
)
from airbyte_ops_mcp.cloud_admin.payment_config import (
    update_organization_payment_config as _update_organization_payment_config,
)
from airbyte_ops_mcp.cloud_admin.version_overrides import validate_tier_filter
from airbyte_ops_mcp.constants import ServerConfigKey
from airbyte_ops_mcp.prod_db_access.queries import (
    query_connection_workspace_details,
    query_organization_agentic_flags,
)
from airbyte_ops_mcp.tier_cache import (
    CustomerTier,
    TierCacheStats,
    TierFilter,
    TierSummary,
    build_tier_summary,
    get_cache_stats,
    get_org_tier,
    get_org_tiers,
    refresh_tier_cache,
    resolve_workspaces,
)


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


logger = logging.getLogger(__name__)

_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

_DAYS_PATTERN = re.compile(r"^\d+$")

_PACIFIC = ZoneInfo("America/Los_Angeles")


def _build_tier_warning(customer_tier: str) -> str | None:
    """Build a warning message for sensitive customer tiers."""
    if customer_tier == "TIER_0":
        return (
            "WARNING: This is a TIER_0 (highest-value) customer. "
            "Proceed with extreme caution."
        )
    if customer_tier == "TIER_1":
        return "WARNING: This is a TIER_1 (high-value) customer. Proceed with caution."
    return None


def _fetch_orb_subscription_info(
    organization_id: str,
) -> OrbSubscriptionInfo | None:
    """Try to fetch the active Orb subscription for an organization.

    Returns `None` silently if the Orb API key is not configured or if no
    active subscription is found. Logs warnings on API errors but does not
    raise — Orb data is supplemental, not required.
    """
    orb_api_key = _get_orb_api_key()
    if not orb_api_key:
        return None

    try:
        active_sub = get_active_subscription(organization_id, orb_api_key)
    except (OrbAPIError, requests.RequestException):
        logger.warning(
            "Failed to fetch Orb subscription for org %s",
            organization_id,
            exc_info=True,
        )
        return None

    if active_sub is None:
        return None

    summary = extract_subscription_summary(active_sub)
    return OrbSubscriptionInfo(
        subscription_id=summary["subscription_id"],
        status=summary["status"],
        plan_name=summary.get("plan_name"),
        plan_id=summary.get("plan_id"),
        external_plan_id=summary.get("external_plan_id"),
        start_date=summary.get("start_date"),
        end_date=summary.get("end_date"),
        orb_customer_id=summary.get("orb_customer_id"),
    )


def _validate_organization_name(
    organization_id: str,
    organization_name: str | None,
    org_info: OrganizationInfo,
) -> tuple[bool, str | None]:
    """Validate `organization_name` against the org record from the Config API.

    Accepts the org's literal name, email, or email domain as valid inputs.

    Returns `(ok, error_message)`. On success `error_message` is `None`.
    """
    org_db_name: str = org_info.organization_name or ""
    org_db_email: str = org_info.email or ""
    org_db_domain: str = org_db_email.split("@", 1)[-1] if "@" in org_db_email else ""

    valid_identifiers = [
        v
        for v in [org_db_name.lower(), org_db_email.lower(), org_db_domain.lower()]
        if v
    ]

    identifier_parts = []
    if org_db_name:
        identifier_parts.append(f"'{org_db_name}' (org name)")
    if org_db_email:
        identifier_parts.append(f"'{org_db_email}' (email)")
    if org_db_domain:
        identifier_parts.append(f"'{org_db_domain}' (email domain)")

    if not identifier_parts:
        return (
            False,
            f"Organization {organization_id} has no name or email on record.",
        )

    hint_message = (
        f"To confirm, resend with `organization_name` set to one of: "
        f"{', '.join(identifier_parts)}. "
        f"Double-check that this is the correct organization before retrying. "
        f"If there is any doubt, confirm with your user."
    )

    if organization_name is None:
        return (
            False,
            (
                f"`organization_name` is required to confirm the target organization. "
                f"{hint_message}"
            ),
        )

    if organization_name.strip().lower().lstrip("@") not in valid_identifiers:
        return (
            False,
            (
                f"Organization name mismatch: '{organization_name}' does not match "
                f"organization {organization_id}. {hint_message}"
            ),
        )

    return True, None


def _format_grace_period_end(target_date: date) -> str:
    """Build a backend-compatible datetime string for 11:59 PM Pacific on `target_date`.

    The result is converted to UTC and formatted as
    `yyyy-MM-dd'T'HH:mm:ss.SSS+0000` to match the Java `@JsonFormat` annotation.
    """
    end_pacific = datetime(
        target_date.year,
        target_date.month,
        target_date.day,
        23,
        59,
        59,
        tzinfo=_PACIFIC,
    )
    end_utc = end_pacific.astimezone(timezone.utc)
    return end_utc.strftime("%Y-%m-%dT%H:%M:%S.000+0000")


def _parse_grace_period_value(
    value: str,
) -> tuple[str | None, str | None]:
    """Parse `set_grace_period` into an ISO 8601 datetime string or an action keyword.

    Dates and day offsets resolve to 11:59 PM Pacific Time on the target date.
    Day offsets use the current date in Pacific Time as the starting point.

    Returns `(iso_datetime_or_action, error_message)`.
    On success `error_message` is `None`.
    """
    value = value.strip()

    if value.lower() == "cancel":
        return "cancel", None

    today_pacific = datetime.now(tz=_PACIFIC).date()

    if _DATE_PATTERN.match(value):
        try:
            parsed = date.fromisoformat(value)
        except ValueError:
            return None, f"Invalid date: {value}. Use YYYY-MM-DD format."
        if parsed < today_pacific:
            return None, f"Grace period end date {value} is in the past."
        if (parsed - today_pacific).days > 90:
            return None, (
                f"Grace period end date {value} is more than 90 days in the future. "
                "Maximum grace period is 90 days."
            )
        return _format_grace_period_end(parsed), None

    if _DAYS_PATTERN.match(value):
        days = int(value)
        if days < 1 or days > 90:
            return None, f"Days must be between 1 and 90, got {days}."
        target_date = today_pacific + timedelta(days=days)
        return _format_grace_period_end(target_date), None

    return None, (
        f"Invalid `set_grace_period` value: '{value}'. "
        "Expected a date (YYYY-MM-DD), an integer number of days, or 'cancel'."
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def get_organization_payment_config(
    organization_id: Annotated[
        str,
        "The organization UUID.",
    ],
    config_api_root: Annotated[
        str | None,
        Field(
            description="Optional Config API root URL override. "
            "Defaults to Airbyte Cloud (`https://cloud.airbyte.com/api/v1`).",
            default=None,
        ),
    ] = None,
    *,
    ctx: Context,
) -> OrganizationPaymentConfigInfo:
    """Get the current payment configuration for an organization.

    Returns payment status, subscription status, grace period info,
    usage category override, and current Orb billing plan (when
    `ORB_API_KEY` is configured). No PII or sensitive payment details
    are included in the response.

    Authentication credentials are resolved in priority order:
    1. Bearer token (Authorization header or AIRBYTE_CLOUD_BEARER_TOKEN env var)
    2. HTTP headers: X-Airbyte-Cloud-Client-Id, X-Airbyte-Cloud-Client-Secret
    3. Environment variables: AIRBYTE_CLOUD_CLIENT_ID, AIRBYTE_CLOUD_CLIENT_SECRET
    """
    resolved_api_root = config_api_root or constants.CLOUD_CONFIG_API_ROOT
    bearer_token, client_id, client_secret = _resolve_cloud_auth(ctx)

    data = _get_organization_payment_config(
        organization_id=organization_id,
        config_api_root=resolved_api_root,
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
    )

    # Enrich with tier info
    tier_result = get_org_tier(organization_id)
    tier_warning = _build_tier_warning(tier_result.customer_tier)

    # Enrich with Orb subscription info (best-effort)
    orb_subscription = _fetch_orb_subscription_info(organization_id)

    return OrganizationPaymentConfigInfo(
        organization_id=data["organizationId"],
        payment_status=data["paymentStatus"],
        subscription_status=data["subscriptionStatus"],
        payment_provider_id=data.get("paymentProviderId"),
        grace_period_end_at=data.get("gracePeriodEndAt"),
        usage_category_overwrite=data.get("usageCategoryOverwrite"),
        customer_tier=tier_result.customer_tier,
        tier_warning=tier_warning,
        orb_subscription=orb_subscription,
    )


@mcp_tool(
    destructive=True,
    idempotent=False,
    open_world=True,
)
def update_organization_payment_config(
    organization_id: Annotated[
        str,
        "The organization UUID.",
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
            "organization name, email address, or email domain. Required to "
            "prevent accidental modifications to the wrong organization. "
            "If omitted or mismatched, the tool returns an error with the valid "
            "identifiers so you can verify and retry.",
            default=None,
        ),
    ] = None,
    set_grace_period: Annotated[
        str | None,
        Field(
            description="Set or modify the grace period. Accepts three forms: "
            "(1) A date in `YYYY-MM-DD` format — grace period ends at 11:59 PM Pacific on that date. "
            "(2) An integer number of days (1-90) from today (Pacific Time) — "
            "grace period ends at 11:59 PM Pacific on the resulting date. "
            "(3) `'cancel'` to terminate the current grace period "
            "(sets status to `manual`). "
            "Requires `set_grace_period_reason` when setting or extending.",
            default=None,
        ),
    ] = None,
    set_grace_period_reason: Annotated[
        str | None,
        Field(
            description="Reason for starting, extending, or canceling the grace "
            "period. Required when `set_grace_period` is a date or number of days.",
            default=None,
        ),
    ] = None,
    set_permanent_waiver_type: Annotated[
        Literal["free", "internal", "none"] | None,
        Field(
            description="Set a permanent billing waiver for the organization. "
            "Use `'free'` for partner accounts that should not be billed, "
            "`'internal'` for Airbyte-internal organizations, "
            "or `'none'` to remove an existing waiver. "
            "Mutually exclusive with `set_grace_period`.",
            default=None,
        ),
    ] = None,
    set_permanent_waiver_reason: Annotated[
        str | None,
        Field(
            description="Reason for setting the permanent billing waiver. "
            "Required when `set_permanent_waiver_type` is provided.",
            default=None,
        ),
    ] = None,
    config_api_root: Annotated[
        str | None,
        Field(
            description="Optional Config API root URL override. "
            "Defaults to Airbyte Cloud (`https://cloud.airbyte.com/api/v1`).",
            default=None,
        ),
    ] = None,
    *,
    ctx: Context,
) -> OrganizationPaymentConfigUpdateResult:
    """Update the payment configuration for an organization.

    All updates require human-in-the-loop approval via `escalate_to_human`.

    Use `set_grace_period` to start, extend, or cancel a grace period.
    If the org is not already in `manual` status, the tool automatically
    transitions to `manual` first before setting the grace period.

    Use `set_permanent_waiver_type` to mark an organization as a partner (`free`)
    or internal (`internal`) account. This is mutually exclusive with
    `set_grace_period` — only one may be provided per call. Setting the waiver
    type to `free` or `internal` also changes the Orb billing plan (`free` →
    Airbyte Partner, `internal` → Airbyte Internal). The `ORB_API_KEY`
    environment variable must be configured for waiver type changes.

    The `organization_name` parameter is a safety check: the tool looks up the
    organization via the Config API and verifies that the provided name, email, or
    email domain matches. If omitted or mismatched, the tool returns the valid
    identifiers so the caller can verify and retry.
    """
    # --- Validate that an action was specified ---
    if set_grace_period is None and set_permanent_waiver_type is None:
        return OrganizationPaymentConfigUpdateResult(
            success=False,
            message="No action specified. Provide `set_grace_period` with a date "
            "(YYYY-MM-DD), number of days (1-90), or 'cancel'; or "
            "`set_permanent_waiver_type` with 'free' (partner) or 'internal'.",
            organization_id=organization_id,
        )

    # --- Validate mutual exclusivity ---
    if set_grace_period is not None and set_permanent_waiver_type is not None:
        return OrganizationPaymentConfigUpdateResult(
            success=False,
            message="`set_grace_period` and `set_permanent_waiver_type` are "
            "mutually exclusive. Provide only one per call.",
            organization_id=organization_id,
        )

    # --- Validate waiver reason is provided when waiver type is set ---
    if set_permanent_waiver_type is not None and not set_permanent_waiver_reason:
        return OrganizationPaymentConfigUpdateResult(
            success=False,
            message="`set_permanent_waiver_reason` is required when "
            "`set_permanent_waiver_type` is provided.",
            organization_id=organization_id,
        )

    # --- Validate ORB_API_KEY is configured for waiver type changes ---
    if set_permanent_waiver_type in ("free", "internal") and not _get_orb_api_key():
        return OrganizationPaymentConfigUpdateResult(
            success=False,
            message="`ORB_API_KEY` environment variable is not configured. "
            "It is required when setting `set_permanent_waiver_type` to "
            "'free' or 'internal' because the Orb billing plan must also "
            "be changed.",
            organization_id=organization_id,
        )

    # --- Validate admin access ---
    try:
        require_internal_admin_flag_only()
    except CloudAuthError as e:
        return OrganizationPaymentConfigUpdateResult(
            success=False,
            message=f"Admin authentication failed: {e}",
            organization_id=organization_id,
        )

    # --- Resolve approval ---
    try:
        resolve_admin_email_from_approval(
            approval_comment_url=approval_comment_url,
        )
    except ApprovalResolutionError as e:
        return OrganizationPaymentConfigUpdateResult(
            success=False,
            message=str(e),
            organization_id=organization_id,
        )

    # --- Resolve auth ---
    resolved_api_root = config_api_root or constants.CLOUD_CONFIG_API_ROOT
    bearer_token, client_id, client_secret = _resolve_cloud_auth(ctx)

    # --- Look up organization info via Config API ---
    try:
        org_info = get_organization_info(
            organization_id=organization_id,
            config_api_root=resolved_api_root,
            client_id=client_id,
            client_secret=client_secret,
            bearer_token=bearer_token,
        )
    except PaymentConfigAPIError as e:
        return OrganizationPaymentConfigUpdateResult(
            success=False,
            message=f"Failed to fetch organization info: {e}",
            organization_id=organization_id,
        )
    if org_info is None:
        return OrganizationPaymentConfigUpdateResult(
            success=False,
            message=f"Organization {organization_id} not found.",
            organization_id=organization_id,
        )

    # --- Validate organization name (safety check) ---
    name_ok, name_error = _validate_organization_name(
        organization_id, organization_name, org_info
    )
    if not name_ok:
        return OrganizationPaymentConfigUpdateResult(
            success=False,
            message=name_error or "Organization name validation failed.",
            organization_id=organization_id,
        )

    # --- Enrich with tier info ---
    tier_result = get_org_tier(organization_id)
    customer_tier = tier_result.customer_tier
    tier_warning = _build_tier_warning(customer_tier)

    # --- Permanent-waiver-only path (no grace period change) ---
    #
    # Statuses that the API cannot set back: uninitialized, okay, disabled.
    # If the org is in one of these, we transition to 'manual' first (same
    # pattern the grace-period path uses).
    _api_nonsettable_statuses = ("uninitialized", "okay", "disabled")

    if set_grace_period is None:
        # Only set_permanent_waiver_type was requested
        assert set_permanent_waiver_type is not None
        try:
            current_config = _get_organization_payment_config(
                organization_id=organization_id,
                config_api_root=resolved_api_root,
                client_id=client_id,
                client_secret=client_secret,
                bearer_token=bearer_token,
            )
        except PaymentConfigAPIError as e:
            return OrganizationPaymentConfigUpdateResult(
                success=False,
                message=f"Failed to fetch current config: {e}",
                organization_id=organization_id,
                customer_tier=customer_tier,
                tier_warning=tier_warning,
            )
        current_status = current_config["paymentStatus"]

        # Transition to 'manual' if current status is not API-settable
        target_status = current_status
        if current_status in _api_nonsettable_statuses:
            try:
                _update_organization_payment_config(
                    organization_id=organization_id,
                    payment_status="manual",
                    config_api_root=resolved_api_root,
                    client_id=client_id,
                    client_secret=client_secret,
                    bearer_token=bearer_token,
                    new_grace_period_reason=(
                        f"Transitioned to manual for permanent waiver: "
                        f"{set_permanent_waiver_reason}"
                    ),
                )
                target_status = "manual"
            except PaymentConfigAPIError as e:
                return OrganizationPaymentConfigUpdateResult(
                    success=False,
                    message=f"Failed to transition from '{current_status}' "
                    f"to 'manual': {e}",
                    organization_id=organization_id,
                    payment_status=current_status,
                    customer_tier=customer_tier,
                    tier_warning=tier_warning,
                )

        try:
            data = _update_organization_payment_config(
                organization_id=organization_id,
                payment_status=target_status,
                config_api_root=resolved_api_root,
                client_id=client_id,
                client_secret=client_secret,
                bearer_token=bearer_token,
                usage_category_overwrite=(
                    set_permanent_waiver_type
                    if set_permanent_waiver_type != "none"
                    else ""
                ),
            )
        except PaymentConfigAPIError as e:
            return OrganizationPaymentConfigUpdateResult(
                success=False,
                message=f"Failed to set permanent waiver type: {e}",
                organization_id=organization_id,
                payment_status=target_status,
                customer_tier=customer_tier,
                tier_warning=tier_warning,
            )
        parts = [
            f"Permanent waiver type set to '{set_permanent_waiver_type}' "
            f"for org {organization_id}.",
        ]
        if current_status in _api_nonsettable_statuses:
            parts.append(
                f"Payment status transitioned from '{current_status}' to 'manual'."
            )

        # --- Orb plan change (required for "free" / "internal") ---
        orb_plan_change_result: str | None = None
        if set_permanent_waiver_type in ("free", "internal"):
            # ORB_API_KEY is validated at the top of the function, so this
            # is guaranteed to be non-None here.
            orb_api_key = _get_orb_api_key()
            assert orb_api_key, "ORB_API_KEY should have been validated earlier"
            try:
                active_sub = get_active_subscription(organization_id, orb_api_key)
                if active_sub is None:
                    parts.append(
                        "Orb plan change skipped: no active subscription "
                        "found for this organization in Orb."
                    )
                    orb_plan_change_result = "Skipped: no active Orb subscription"
                else:
                    target_plan_id = _resolve_plan_id(set_permanent_waiver_type)
                    current_plan_id = (active_sub.get("plan") or {}).get("id")
                    current_plan_name = (active_sub.get("plan") or {}).get(
                        "name", current_plan_id or "unknown"
                    )
                    if current_plan_id == target_plan_id:
                        orb_plan_change_result = (
                            f"Already on plan '{current_plan_name}'"
                        )
                        parts.append(f"Orb plan already set to '{current_plan_name}'.")
                    else:
                        schedule_plan_change(
                            subscription_id=active_sub["id"],
                            plan_id=target_plan_id,
                            api_key=orb_api_key,
                        )
                        orb_plan_change_result = (
                            f"Changed from '{current_plan_name}' to '{target_plan_id}'"
                        )
                        parts.append(f"Orb plan changed to '{target_plan_id}'.")
            except (OrbAPIError, requests.RequestException) as e:
                parts.append(f"Orb plan change failed: {e}")
                orb_plan_change_result = f"Failed: {e}"

        # --- Entitlement plan update (Stigg) ---
        entitlement_plan_change_result: str | None = None
        target_entitlement_plan = WAIVER_TYPE_TO_ENTITLEMENT_PLAN.get(
            set_permanent_waiver_type
        )
        if target_entitlement_plan:
            try:
                update_entitlement_plan(
                    organization_id=organization_id,
                    plan_name=target_entitlement_plan,
                    config_api_root=resolved_api_root,
                    client_id=client_id,
                    client_secret=client_secret,
                    bearer_token=bearer_token,
                )
                entitlement_plan_change_result = f"Changed to {target_entitlement_plan}"
                parts.append(
                    f"Entitlement plan updated to '{target_entitlement_plan}'."
                )
            except EntitlementAPIError as e:
                parts.append(f"Entitlement plan update failed: {e}")
                entitlement_plan_change_result = f"Failed: {e}"

        return OrganizationPaymentConfigUpdateResult(
            success=True,
            message=" ".join(parts),
            organization_id=organization_id,
            payment_status=data["paymentStatus"],
            grace_period_end_at=data.get("gracePeriodEndAt"),
            permanent_waiver_type=data.get("usageCategoryOverwrite"),
            customer_tier=customer_tier,
            tier_warning=tier_warning,
            orb_plan_change=orb_plan_change_result,
            entitlement_plan_change=entitlement_plan_change_result,
        )

    # --- Parse grace period value ---
    parsed_value, parse_error = _parse_grace_period_value(set_grace_period)
    if parse_error is not None:
        return OrganizationPaymentConfigUpdateResult(
            success=False,
            message=parse_error,
            organization_id=organization_id,
            customer_tier=customer_tier,
            tier_warning=tier_warning,
        )

    assert parsed_value is not None

    # --- Fetch current payment config (needed for both cancel and set paths) ---
    try:
        current_config = _get_organization_payment_config(
            organization_id=organization_id,
            config_api_root=resolved_api_root,
            client_id=client_id,
            client_secret=client_secret,
            bearer_token=bearer_token,
        )
    except PaymentConfigAPIError as e:
        return OrganizationPaymentConfigUpdateResult(
            success=False,
            message=f"Failed to fetch current config: {e}",
            organization_id=organization_id,
            customer_tier=customer_tier,
            tier_warning=tier_warning,
        )

    current_status = current_config["paymentStatus"]

    if parsed_value == "cancel":
        # Only allow cancel when org is actually in grace_period (or manual with
        # an active grace period end date).
        if current_status not in ("grace_period", "manual"):
            return OrganizationPaymentConfigUpdateResult(
                success=False,
                message=f"Cannot cancel grace period: organization is in "
                f"'{current_status}' status, not 'grace_period'.",
                organization_id=organization_id,
                payment_status=current_status,
                customer_tier=customer_tier,
                tier_warning=tier_warning,
            )

        # Cancel grace period by setting status to manual
        try:
            data = _update_organization_payment_config(
                organization_id=organization_id,
                payment_status="manual",
                config_api_root=resolved_api_root,
                client_id=client_id,
                client_secret=client_secret,
                bearer_token=bearer_token,
                new_grace_period_reason=(
                    set_grace_period_reason or "Grace period canceled via MCP tool"
                ),
            )
        except PaymentConfigAPIError as e:
            return OrganizationPaymentConfigUpdateResult(
                success=False,
                message=str(e),
                organization_id=organization_id,
                customer_tier=customer_tier,
                tier_warning=tier_warning,
            )

        return OrganizationPaymentConfigUpdateResult(
            success=True,
            message=f"Grace period canceled for org {organization_id}. "
            f"New status: {data['paymentStatus']}.",
            organization_id=organization_id,
            payment_status=data["paymentStatus"],
            grace_period_end_at=data.get("gracePeriodEndAt"),
            permanent_waiver_type=data.get("usageCategoryOverwrite"),
            customer_tier=customer_tier,
            tier_warning=tier_warning,
        )

    # --- Setting/extending grace period ---
    if not set_grace_period_reason:
        return OrganizationPaymentConfigUpdateResult(
            success=False,
            message="`set_grace_period_reason` is required when setting or "
            "extending a grace period.",
            organization_id=organization_id,
            customer_tier=customer_tier,
            tier_warning=tier_warning,
        )

    # The API only allows setting grace_period from manual status.
    # If not already in manual, transition to manual first.
    transitioned_to_manual = False
    if current_status != "manual":
        logger.info(
            "Org %s is in '%s' status; transitioning to 'manual' first.",
            organization_id,
            current_status,
        )
        try:
            _update_organization_payment_config(
                organization_id=organization_id,
                payment_status="manual",
                config_api_root=resolved_api_root,
                client_id=client_id,
                client_secret=client_secret,
                bearer_token=bearer_token,
            )
            transitioned_to_manual = True
        except PaymentConfigAPIError as e:
            return OrganizationPaymentConfigUpdateResult(
                success=False,
                message=f"Failed to transition to 'manual' from '{current_status}': {e}",
                organization_id=organization_id,
                customer_tier=customer_tier,
                tier_warning=tier_warning,
            )

    # Now set the grace period
    try:
        data = _update_organization_payment_config(
            organization_id=organization_id,
            payment_status="grace_period",
            config_api_root=resolved_api_root,
            client_id=client_id,
            client_secret=client_secret,
            bearer_token=bearer_token,
            grace_period_end_at=parsed_value,
            new_grace_period_reason=set_grace_period_reason,
        )
    except PaymentConfigAPIError as e:
        if transitioned_to_manual:
            msg = (
                f"Failed to set grace period after transitioning to 'manual' "
                f"from '{current_status}'. The organization is now in 'manual' "
                f"status. Original error: {e}"
            )
        else:
            msg = str(e)
        return OrganizationPaymentConfigUpdateResult(
            success=False,
            message=msg,
            organization_id=organization_id,
            payment_status="manual" if transitioned_to_manual else None,
            customer_tier=customer_tier,
            tier_warning=tier_warning,
        )

    return OrganizationPaymentConfigUpdateResult(
        success=True,
        message=f"Grace period set for org {organization_id}. "
        f"New status: {data['paymentStatus']}.",
        organization_id=organization_id,
        payment_status=data["paymentStatus"],
        grace_period_end_at=data.get("gracePeriodEndAt"),
        permanent_waiver_type=data.get("usageCategoryOverwrite"),
        customer_tier=customer_tier,
        tier_warning=tier_warning,
    )


class TierLookupEntry(BaseModel):
    """A single resolved tier entry for an org, workspace, or connection."""

    input_id: str = Field(description="The original ID that was looked up")
    input_type: str = Field(
        description="Type of the input ID: 'organization', 'workspace', or 'connection'"
    )
    organization_id: str | None = Field(
        default=None, description="Resolved organization UUID"
    )
    workspace_id: str | None = Field(
        default=None,
        description="Workspace UUID (if input was workspace or connection)",
    )
    connection_id: str | None = Field(
        default=None, description="Connection UUID (if input was connection)"
    )
    customer_tier: CustomerTier = Field(
        description="Resolved tier: TIER_0, TIER_1, or TIER_2"
    )
    dataplane_name: str | None = Field(
        default=None, description="Dataplane region name (e.g., 'US', 'EU')"
    )
    is_eu: bool = Field(
        default=False, description="Whether the entity is in the EU region"
    )
    resolved: bool = Field(
        default=True, description="Whether the ID was successfully resolved"
    )


class TierLookupResult(BaseModel):
    """Result of a customer tier lookup across multiple IDs."""

    entries: list[TierLookupEntry] = Field(
        description="Individual tier lookup results for each input ID"
    )
    summary: TierSummary = Field(
        description="Tier distribution summary across all resolved entries"
    )
    summary_text: str = Field(description="Human-readable tier distribution summary")


class TierCacheRefreshResult(BaseModel):
    """Result of refreshing the tier cache."""

    stats: TierCacheStats = Field(description="Cache statistics after refresh")
    message: str = Field(description="Human-readable result message")


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def lookup_customer_tiers(
    organization_ids: Annotated[
        list[str] | None,
        Field(
            description=(
                "List of organization UUIDs to look up tiers for. "
                "Example: ['664c690e-5263-49ba-b01f-4a6759b3330a']"
            ),
            default=None,
        ),
    ] = None,
    workspace_ids: Annotated[
        list[str] | None,
        Field(
            description=(
                "List of workspace UUIDs to look up tiers for. "
                "Each workspace will be resolved to its organization and tier. "
                "Example: ['266ebdfe-0d7b-4540-9817-de7e4505ba61']"
            ),
            default=None,
        ),
    ] = None,
    connection_ids: Annotated[
        list[str] | None,
        Field(
            description=(
                "List of connection UUIDs to look up tiers for. "
                "Each connection will be resolved to its workspace, organization, and tier."
            ),
            default=None,
        ),
    ] = None,
) -> TierLookupResult:
    """Look up customer tier classification for organizations, workspaces, and/or connections.

    Accepts mixed lists of organization IDs, workspace IDs, and connection IDs.
    Resolves each to its organization and maps to a customer tier (TIER_0, TIER_1, or TIER_2).

    Tier 0 and Tier 1 orgs are explicitly tracked in Salesforce and cached from the GCS export.
    Any org not in the cache defaults to TIER_2.

    Returns enriched entries with tier, region (EU/US), and a summary of the distribution.
    """
    entries: list[TierLookupEntry] = []

    # Resolve organization IDs directly
    org_ids = organization_ids or []
    if org_ids:
        org_results = get_org_tiers(org_ids)
        for result in org_results:
            entries.append(
                TierLookupEntry(
                    input_id=result.organization_id,
                    input_type="organization",
                    organization_id=result.organization_id,
                    customer_tier=result.customer_tier,
                    resolved=True,
                )
            )

    # Resolve workspace IDs -> org -> tier
    ws_ids = workspace_ids or []
    if ws_ids:
        ws_results = resolve_workspaces(ws_ids)
        for result in ws_results:
            entries.append(
                TierLookupEntry(
                    input_id=result.workspace_id,
                    input_type="workspace",
                    organization_id=result.organization_id,
                    workspace_id=result.workspace_id,
                    customer_tier=result.customer_tier,
                    dataplane_name=result.dataplane_name,
                    is_eu=result.is_eu,
                    resolved=result.resolved,
                )
            )

    # Resolve connection IDs -> workspace -> org -> tier
    conn_ids = connection_ids or []
    if conn_ids:
        conn_details = query_connection_workspace_details(conn_ids)
        conn_map: dict[str, dict[str, Any]] = {
            str(row["connection_id"]): row for row in conn_details
        }

        for conn_id in conn_ids:
            row = conn_map.get(conn_id)
            if row is None:
                entries.append(
                    TierLookupEntry(
                        input_id=conn_id,
                        input_type="connection",
                        connection_id=conn_id,
                        customer_tier="TIER_2",
                        resolved=False,
                    )
                )
                continue

            org_id = str(row["organization_id"])
            dataplane_name = row.get("dataplane_name") or "US"
            org_result = get_org_tier(org_id)

            entries.append(
                TierLookupEntry(
                    input_id=conn_id,
                    input_type="connection",
                    organization_id=org_id,
                    workspace_id=str(row["workspace_id"]),
                    connection_id=conn_id,
                    customer_tier=org_result.customer_tier,
                    dataplane_name=dataplane_name,
                    is_eu=dataplane_name == "EU",
                    resolved=True,
                )
            )

    # Build summary from enriched entries
    summary_rows = [{"customer_tier": e.customer_tier} for e in entries if e.resolved]
    summary = build_tier_summary(summary_rows)

    return TierLookupResult(
        entries=entries,
        summary=summary,
        summary_text=str(summary),
    )


@mcp_tool(
    read_only=False,
    idempotent=True,
)
def refresh_customer_tier_cache() -> TierCacheRefreshResult:
    """Force-refresh the customer tier cache from the GCS export.

    The tier cache is automatically refreshed every 24 hours. Use this tool to
    manually trigger a refresh if you need the latest tier data immediately
    (e.g., after a Salesforce update).

    Returns cache statistics after the refresh.
    """
    stats = refresh_tier_cache()
    return TierCacheRefreshResult(
        stats=stats,
        message=(
            f"Tier cache refreshed: {stats.tier_cache_size} orgs cached, "
            f"{stats.workspace_cache_size} workspaces cached."
        ),
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def get_customer_tier_cache_stats() -> TierCacheStats:
    """Get current statistics about the customer tier cache.

    Returns cache size, age, and file paths for both the tier cache
    (org -> tier) and workspace cache (workspace -> org + region).

    Useful for checking cache freshness and diagnosing issues.
    """
    return get_cache_stats()


def register_organization_admin_tools(app: FastMCP) -> None:
    """Register organization_admin tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
