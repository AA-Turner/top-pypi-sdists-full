"""Tool definitions for the Customer Billing page."""

from __future__ import annotations

import logging
import re
from datetime import UTC, date, datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from airbyte_ops_mcp.cloud_admin.entitlements import (
    WAIVER_TYPE_TO_ENTITLEMENT_PLAN,
    EntitlementAPIError,
    update_entitlement_plan,
)
from airbyte_ops_mcp.cloud_admin.models import (
    OrbSubscriptionInfo,
    OrganizationInfo,
    OrganizationPaymentConfigInfo,
)
from airbyte_ops_mcp.cloud_admin.orb_billing import (
    OrbAPIError,
    _get_orb_api_key,
    _resolve_plan_id,
    extract_subscription_summary,
    get_active_subscription,
    schedule_plan_change,
)
from airbyte_ops_mcp.cloud_admin.payment_config import (
    PaymentConfigAPIError,
    get_organization_info,
)
from airbyte_ops_mcp.cloud_admin.payment_config import (
    get_organization_payment_config as _get_payment_config,
)
from airbyte_ops_mcp.cloud_admin.payment_config import (
    update_organization_payment_config as _update_payment_config,
)
from airbyte_ops_mcp.gcp_auth import get_gcp_credentials_for_bigquery_ro
from airbyte_ops_mcp.tier_cache import get_org_tier, resolve_workspace
from fastmcp import FastMCPApp

from airbyte_ops_webapp.pages.customer_billing._helpers import (
    auth_available,
    resolved_bearer_token,
    resolved_config_api_root,
)
from airbyte_ops_webapp.pages.shared_components.org_search import (
    search_organizations_and_workspaces,
)
from airbyte_ops_webapp.state import mock_only_enabled

logger = logging.getLogger(__name__)

customer_billing_app = FastMCPApp("Customer Billing")

_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DAYS_PATTERN = re.compile(r"^\d+$")
_PACIFIC = ZoneInfo("America/Los_Angeles")
_API_NONSETTABLE_STATUSES = ("uninitialized", "okay", "disabled")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


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
    active subscription is found.
    """
    orb_api_key = _get_orb_api_key()
    if not orb_api_key:
        return None

    try:
        active_sub = get_active_subscription(organization_id, orb_api_key)
    except (OrbAPIError, OSError):
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


def _format_grace_period_end(target_date: date) -> str:
    """Build a backend-compatible datetime string for 11:59 PM Pacific on `target_date`."""
    end_pacific = datetime(
        target_date.year,
        target_date.month,
        target_date.day,
        23,
        59,
        59,
        tzinfo=_PACIFIC,
    )
    end_utc = end_pacific.astimezone(UTC)
    return end_utc.strftime("%Y-%m-%dT%H:%M:%S.000+0000")


def _parse_grace_period_value(value: str) -> tuple[str | None, str | None]:
    """Parse `set_grace_period` into an ISO 8601 datetime string or an action keyword.

    Returns `(iso_datetime_or_action, error_message)`.
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
        f"Invalid grace period value: '{value}'. "
        "Expected a date (YYYY-MM-DD), an integer number of days, or 'cancel'."
    )


def _validate_organization_name(
    organization_id: str,
    organization_name: str | None,
    org_info: OrganizationInfo,
) -> tuple[bool, str | None]:
    """Validate `organization_name` against the org record.

    Accepts the org's literal name, email, or email domain.
    Returns `(ok, error_message)`.
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
        f"To confirm, resend with organization_name set to one of: "
        f"{', '.join(identifier_parts)}."
    )

    if organization_name is None:
        return (
            False,
            f"organization_name is required to confirm the target organization. {hint_message}",
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


def _resolve_org_id(
    query: str,
    bearer_token_override: str | None = None,
) -> tuple[str | None, str | None, str | None]:
    """Resolve a query to an organization ID.

    Accepts an org UUID or workspace UUID.
    Returns `(org_id, resolved_label, error_message)`.
    """
    query = query.strip()
    if not query:
        return (
            None,
            None,
            "Please enter an organization ID or workspace ID.",
        )

    # Heuristic: UUID-shaped → try as org ID first, then workspace ID
    _uuid_like = re.compile(
        r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
    )

    if _uuid_like.match(query):
        # Try as org ID first by calling get_organization_info
        bearer = resolved_bearer_token(bearer_token_override)
        api_root = resolved_config_api_root()
        try:
            org_info = get_organization_info(
                organization_id=query,
                config_api_root=api_root,
                bearer_token=bearer,
            )
            if org_info is not None:
                return query, None, None
        except PaymentConfigAPIError:
            logger.debug(
                "UUID %s not found as org ID, falling back to workspace resolution",
                query,
            )

        # Not found as org — try as workspace ID
        ws_result = resolve_workspace(query)
        if ws_result.resolved and ws_result.organization_id:
            label = f"Resolved from workspace {query} → org {ws_result.organization_id}"
            return ws_result.organization_id, label, None

        return (
            None,
            None,
            f"Could not resolve '{query}' as an organization or workspace ID.",
        )

    return (
        None,
        None,
        f"Invalid input: '{query}'. Please enter a valid organization ID or workspace ID (UUID format).",
    )


# ---------------------------------------------------------------------------
# MCP tools (called by Prefab UI via CallTool)
# ---------------------------------------------------------------------------


_MOCK_ORG_ID = "00000000-aaaa-bbbb-cccc-111111111111"


def _mock_lookup_result(query: str) -> dict[str, Any]:
    """Return mock lookup data for demo/mock mode."""
    org_id = query.strip() or _MOCK_ORG_ID
    return {
        "org_info": {
            "organization_id": org_id,
            "organization_name": "Acme Corp (Demo)",
            "email": "billing@acme-demo.io",
        },
        "payment_config": {
            "organization_id": org_id,
            "payment_status": "grace_period",
            "subscription_status": "subscribed",
            "payment_provider_id": "cus_mock_stripe_123",
            "grace_period_end_at": "2026-07-15T06:59:59.000+0000",
            "usage_category_overwrite": "",
            "customer_tier": "TIER_2",
            "tier_warning": None,
            "orb_subscription": {
                "subscription_id": "sub_mock_orb_456",
                "status": "active",
                "plan_name": "Cloud Team (Demo)",
                "plan_id": "plan_mock_789",
                "external_plan_id": "cloud_team_v2",
                "start_date": "2025-01-01",
                "end_date": None,
                "orb_customer_id": "orb_cust_mock_012",
            },
        },
        "resolved_org_label": "",
        "org_loaded": True,
        "lookup_error": "",
    }


def _mock_apply_result(organization_id: str, action: str) -> dict[str, Any]:
    """Return mock apply result for demo/mock mode."""
    return {
        "success": True,
        "message": f"[MOCK] {action} applied for org {organization_id}.",
        "organization_id": organization_id,
        "payment_status": "grace_period",
        "grace_period_end_at": "2026-07-15T06:59:59.000+0000",
        "permanent_waiver_type": None,
        "customer_tier": "TIER_2",
        "tier_warning": None,
        "orb_plan_change": None,
        "entitlement_plan_change": None,
    }


@customer_billing_app.tool()
def lookup_organization(
    query: str = "",
    auth_bearer_token: str = "",
    google_access_token: str = "",
) -> dict[str, Any]:
    """Look up an organization's payment configuration by ID or workspace ID."""
    if not auth_available(auth_bearer_token or None):
        return {
            "org_info": None,
            "payment_config": None,
            "resolved_org_label": "",
            "org_loaded": False,
            "lookup_error": "Sign in with Airbyte to look up organizations.",
        }

    if mock_only_enabled():
        return _mock_lookup_result(query)

    bearer = resolved_bearer_token(auth_bearer_token or None)
    api_root = resolved_config_api_root()

    # Resolve query to org ID
    org_id, resolved_label, resolve_error = _resolve_org_id(
        query, bearer_token_override=auth_bearer_token or None
    )
    if resolve_error is not None:
        return {
            "org_info": None,
            "payment_config": None,
            "resolved_org_label": "",
            "org_loaded": False,
            "lookup_error": resolve_error,
        }
    assert org_id is not None

    # Fetch org info
    try:
        org_info = get_organization_info(
            organization_id=org_id,
            config_api_root=api_root,
            bearer_token=bearer,
        )
    except PaymentConfigAPIError as e:
        return {
            "org_info": None,
            "payment_config": None,
            "resolved_org_label": resolved_label or "",
            "org_loaded": False,
            "lookup_error": f"Failed to fetch organization info: {e}",
        }

    if org_info is None:
        return {
            "org_info": None,
            "payment_config": None,
            "resolved_org_label": resolved_label or "",
            "org_loaded": False,
            "lookup_error": f"Organization {org_id} not found.",
        }

    # Fetch payment config
    try:
        raw_config = _get_payment_config(
            organization_id=org_id,
            config_api_root=api_root,
            bearer_token=bearer,
        )
    except PaymentConfigAPIError as e:
        return {
            "org_info": org_info.model_dump(mode="json", by_alias=False),
            "payment_config": None,
            "resolved_org_label": resolved_label or "",
            "org_loaded": False,
            "lookup_error": f"Failed to fetch payment config: {e}",
        }

    # Enrich with tier info (use Google token for BigQuery if available)
    bq_credentials = get_gcp_credentials_for_bigquery_ro(
        access_token_override=google_access_token
    )
    tier_result = get_org_tier(org_id, credentials=bq_credentials)
    tier_warning = _build_tier_warning(tier_result.customer_tier)

    # Enrich with Orb subscription info (best-effort)
    orb_subscription = _fetch_orb_subscription_info(org_id)

    payment_config = OrganizationPaymentConfigInfo(
        organization_id=raw_config["organizationId"],
        payment_status=raw_config["paymentStatus"],
        subscription_status=raw_config["subscriptionStatus"],
        payment_provider_id=raw_config.get("paymentProviderId"),
        grace_period_end_at=raw_config.get("gracePeriodEndAt"),
        usage_category_overwrite=raw_config.get("usageCategoryOverwrite"),
        customer_tier=tier_result.customer_tier,
        tier_warning=tier_warning,
        orb_subscription=orb_subscription,
    )

    return {
        "org_info": org_info.model_dump(mode="json", by_alias=False),
        "payment_config": payment_config.model_dump(mode="json"),
        "resolved_org_label": resolved_label or "",
        "org_loaded": True,
        "lookup_error": "",
    }


@customer_billing_app.tool()
def apply_grace_period(
    organization_id: str,
    grace_period_value: str,
    reason: str = "",
    approval_comment_url: str = "",
    organization_name: str = "",
    auth_bearer_token: str = "",
    google_access_token: str = "",
) -> dict[str, Any]:
    """Set, extend, or cancel a grace period for an organization."""
    if not auth_available(auth_bearer_token or None):
        return _error_result(
            organization_id, "Sign in with Airbyte to apply grace periods."
        )

    if mock_only_enabled():
        return _mock_apply_result(
            organization_id, f"Grace period ({grace_period_value})"
        )

    bearer = resolved_bearer_token(auth_bearer_token or None)
    api_root = resolved_config_api_root()

    if not reason.strip() and grace_period_value.strip().lower() != "cancel":
        return _error_result(
            organization_id, "Reason is required when setting a grace period."
        )

    if not approval_comment_url.strip():
        return _error_result(organization_id, "Approval URL is required.")

    # Validate org name
    try:
        org_info = get_organization_info(
            organization_id=organization_id,
            config_api_root=api_root,
            bearer_token=bearer,
        )
    except PaymentConfigAPIError as e:
        return _error_result(organization_id, f"Failed to fetch organization info: {e}")

    if org_info is None:
        return _error_result(
            organization_id, f"Organization {organization_id} not found."
        )

    name_ok, name_error = _validate_organization_name(
        organization_id, organization_name or None, org_info
    )
    if not name_ok:
        return _error_result(
            organization_id, name_error or "Organization name validation failed."
        )

    # Enrich with tier info
    bq_credentials = get_gcp_credentials_for_bigquery_ro(
        access_token_override=google_access_token
    )
    tier_result = get_org_tier(organization_id, credentials=bq_credentials)
    customer_tier = tier_result.customer_tier
    tier_warning = _build_tier_warning(customer_tier)

    # Parse grace period value
    parsed_value, parse_error = _parse_grace_period_value(grace_period_value)
    if parse_error is not None:
        return _error_result(organization_id, parse_error)
    assert parsed_value is not None

    # Fetch current config
    try:
        current_config = _get_payment_config(
            organization_id=organization_id,
            config_api_root=api_root,
            bearer_token=bearer,
        )
    except PaymentConfigAPIError as e:
        return _error_result(organization_id, f"Failed to fetch current config: {e}")

    current_status = current_config["paymentStatus"]

    if parsed_value == "cancel":
        if current_status not in ("grace_period", "manual"):
            return _error_result(
                organization_id,
                f"Cannot cancel grace period: organization is in '{current_status}' status.",
            )
        try:
            data = _update_payment_config(
                organization_id=organization_id,
                payment_status="manual",
                config_api_root=api_root,
                bearer_token=bearer,
                new_grace_period_reason=reason
                or "Grace period canceled via Ops Webapp",
            )
        except PaymentConfigAPIError as e:
            return _error_result(organization_id, str(e))

        return _success_result(
            organization_id=organization_id,
            message=f"Grace period canceled. New status: {data['paymentStatus']}.",
            data=data,
            customer_tier=customer_tier,
            tier_warning=tier_warning,
        )

    # Setting/extending grace period
    if current_status != "manual":
        try:
            _update_payment_config(
                organization_id=organization_id,
                payment_status="manual",
                config_api_root=api_root,
                bearer_token=bearer,
            )
        except PaymentConfigAPIError as e:
            return _error_result(
                organization_id,
                f"Failed to transition to 'manual' from '{current_status}': {e}",
            )

    try:
        data = _update_payment_config(
            organization_id=organization_id,
            payment_status="grace_period",
            config_api_root=api_root,
            bearer_token=bearer,
            grace_period_end_at=parsed_value,
            new_grace_period_reason=reason,
        )
    except PaymentConfigAPIError as e:
        return _error_result(organization_id, f"Failed to set grace period: {e}")

    return _success_result(
        organization_id=organization_id,
        message=f"Grace period set. New status: {data['paymentStatus']}.",
        data=data,
        customer_tier=customer_tier,
        tier_warning=tier_warning,
    )


@customer_billing_app.tool()
def apply_permanent_waiver(
    organization_id: str,
    waiver_type: str,
    reason: str = "",
    approval_comment_url: str = "",
    organization_name: str = "",
    auth_bearer_token: str = "",
    google_access_token: str = "",
) -> dict[str, Any]:
    """Set or remove a permanent billing waiver for an organization."""
    if not auth_available(auth_bearer_token or None):
        return _error_result(
            organization_id, "Sign in with Airbyte to apply permanent waivers."
        )

    if mock_only_enabled():
        return _mock_apply_result(organization_id, f"Permanent waiver ({waiver_type})")

    bearer = resolved_bearer_token(auth_bearer_token or None)
    api_root = resolved_config_api_root()

    if waiver_type not in ("free", "internal", "none"):
        return _error_result(
            organization_id,
            f"Invalid waiver type: '{waiver_type}'. Must be 'free', 'internal', or 'none'.",
        )

    if not reason.strip():
        return _error_result(organization_id, "Reason is required.")

    if not approval_comment_url.strip():
        return _error_result(organization_id, "Approval URL is required.")

    # Validate ORB_API_KEY for free/internal waivers
    if waiver_type in ("free", "internal") and not _get_orb_api_key():
        return _error_result(
            organization_id,
            "ORB_API_KEY is not configured. Required for waiver type changes.",
        )

    # Validate org name
    try:
        org_info = get_organization_info(
            organization_id=organization_id,
            config_api_root=api_root,
            bearer_token=bearer,
        )
    except PaymentConfigAPIError as e:
        return _error_result(organization_id, f"Failed to fetch organization info: {e}")

    if org_info is None:
        return _error_result(
            organization_id, f"Organization {organization_id} not found."
        )

    name_ok, name_error = _validate_organization_name(
        organization_id, organization_name or None, org_info
    )
    if not name_ok:
        return _error_result(
            organization_id, name_error or "Organization name validation failed."
        )

    # Tier info
    bq_credentials = get_gcp_credentials_for_bigquery_ro(
        access_token_override=google_access_token
    )
    tier_result = get_org_tier(organization_id, credentials=bq_credentials)
    customer_tier = tier_result.customer_tier
    tier_warning = _build_tier_warning(customer_tier)

    # Fetch current config
    try:
        current_config = _get_payment_config(
            organization_id=organization_id,
            config_api_root=api_root,
            bearer_token=bearer,
        )
    except PaymentConfigAPIError as e:
        return _error_result(organization_id, f"Failed to fetch current config: {e}")

    current_status = current_config["paymentStatus"]
    target_status = current_status

    # Transition to manual if needed
    if current_status in _API_NONSETTABLE_STATUSES:
        try:
            _update_payment_config(
                organization_id=organization_id,
                payment_status="manual",
                config_api_root=api_root,
                bearer_token=bearer,
                new_grace_period_reason=f"Transitioned to manual for permanent waiver: {reason}",
            )
            target_status = "manual"
        except PaymentConfigAPIError as e:
            return _error_result(
                organization_id,
                f"Failed to transition from '{current_status}' to 'manual': {e}",
            )

    # Apply usage category overwrite
    try:
        data = _update_payment_config(
            organization_id=organization_id,
            payment_status=target_status,
            config_api_root=api_root,
            bearer_token=bearer,
            usage_category_overwrite=waiver_type if waiver_type != "none" else "",
        )
    except PaymentConfigAPIError as e:
        return _error_result(organization_id, f"Failed to set permanent waiver: {e}")

    parts = [f"Permanent waiver set to '{waiver_type}' for org {organization_id}."]
    if current_status in _API_NONSETTABLE_STATUSES:
        parts.append(f"Status transitioned from '{current_status}' to 'manual'.")

    # Orb plan change
    orb_plan_change: str | None = None
    if waiver_type in ("free", "internal"):
        orb_api_key = _get_orb_api_key()
        if orb_api_key:
            try:
                active_sub = get_active_subscription(organization_id, orb_api_key)
                if active_sub is None:
                    orb_plan_change = "Skipped: no active Orb subscription"
                    parts.append("Orb plan change skipped: no active subscription.")
                else:
                    target_plan_id = _resolve_plan_id(waiver_type)
                    current_plan_id = (active_sub.get("plan") or {}).get("id")
                    current_plan_name = (active_sub.get("plan") or {}).get(
                        "name", current_plan_id or "unknown"
                    )
                    if current_plan_id == target_plan_id:
                        orb_plan_change = f"Already on plan '{current_plan_name}'"
                        parts.append(f"Orb plan already set to '{current_plan_name}'.")
                    else:
                        schedule_plan_change(
                            subscription_id=active_sub["id"],
                            plan_id=target_plan_id,
                            api_key=orb_api_key,
                        )
                        orb_plan_change = (
                            f"Changed from '{current_plan_name}' to '{target_plan_id}'"
                        )
                        parts.append(f"Orb plan changed to '{target_plan_id}'.")
            except (OrbAPIError, OSError) as e:
                parts.append(f"Orb plan change failed: {e}")
                orb_plan_change = f"Failed: {e}"

    # Stigg entitlement update
    entitlement_change: str | None = None
    target_entitlement_plan = WAIVER_TYPE_TO_ENTITLEMENT_PLAN.get(waiver_type)
    if target_entitlement_plan:
        try:
            update_entitlement_plan(
                organization_id=organization_id,
                plan_name=target_entitlement_plan,
                config_api_root=api_root,
                bearer_token=bearer,
            )
            entitlement_change = f"Changed to {target_entitlement_plan}"
            parts.append(f"Entitlement plan updated to '{target_entitlement_plan}'.")
        except EntitlementAPIError as e:
            parts.append(f"Entitlement plan update failed: {e}")
            entitlement_change = f"Failed: {e}"

    return {
        "success": True,
        "message": " ".join(parts),
        "organization_id": organization_id,
        "payment_status": data["paymentStatus"],
        "grace_period_end_at": data.get("gracePeriodEndAt"),
        "permanent_waiver_type": data.get("usageCategoryOverwrite"),
        "customer_tier": customer_tier,
        "tier_warning": tier_warning,
        "orb_plan_change": orb_plan_change,
        "entitlement_plan_change": entitlement_change,
    }


# ---------------------------------------------------------------------------
# Result helpers
# ---------------------------------------------------------------------------


def _error_result(organization_id: str, message: str) -> dict[str, Any]:
    """Build a failure result dict."""
    return {
        "success": False,
        "message": message,
        "organization_id": organization_id,
        "payment_status": None,
        "grace_period_end_at": None,
        "permanent_waiver_type": None,
        "customer_tier": None,
        "tier_warning": None,
        "orb_plan_change": None,
        "entitlement_plan_change": None,
    }


def _success_result(
    *,
    organization_id: str,
    message: str,
    data: dict[str, Any],
    customer_tier: str,
    tier_warning: str | None,
) -> dict[str, Any]:
    """Build a success result dict from raw Config API response data."""
    return {
        "success": True,
        "message": message,
        "organization_id": organization_id,
        "payment_status": data["paymentStatus"],
        "grace_period_end_at": data.get("gracePeriodEndAt"),
        "permanent_waiver_type": data.get("usageCategoryOverwrite"),
        "customer_tier": customer_tier,
        "tier_warning": tier_warning,
        "orb_plan_change": None,
        "entitlement_plan_change": None,
    }


@customer_billing_app.tool()
def search_orgs_workspaces(
    query: str = "",
) -> dict[str, Any]:
    """Search organizations and workspaces by name (case-insensitive substring)."""
    return search_organizations_and_workspaces(query=query)
