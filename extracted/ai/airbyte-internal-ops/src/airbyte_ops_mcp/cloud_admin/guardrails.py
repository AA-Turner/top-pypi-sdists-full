"""Shared authorization and customer-tier guardrails for admin operations."""

from __future__ import annotations

import logging

from airbyte_ops_mcp.approval_resolution import ApprovalStatus, check_approval_status
from airbyte_ops_mcp.cloud_admin.auth import (
    CloudAuthError,
    require_internal_admin_flag_only,
)
from airbyte_ops_mcp.tier_cache import TierFilter, TierSourceHealth

logger = logging.getLogger(__name__)


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
    """Check whether `actual_tier` matches `requested_filter`."""
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
            "or use 'ALL' to proceed with a warning."
        )
    return True, None


def validate_admin_and_authorization(
    *,
    issue_url: str | None,
    approval_comment_url: str | None,
    user_email: str | None = None,
) -> tuple[str | None, str | None]:
    """Run internal-admin and approval-parameter checks."""
    try:
        require_internal_admin_flag_only()
    except CloudAuthError as e:
        return None, f"Admin authentication failed: {e}"

    approval = check_approval_status(
        approval_comment_url=approval_comment_url,
        user_email=user_email,
    )
    if approval.status == ApprovalStatus.APPROVED:
        return approval.admin_email, None

    if approval.status == ApprovalStatus.NEEDS_APPROVAL:
        validation_errors: list[str] = []
        if not issue_url:
            validation_errors.append(
                "issue_url is required for authorization (GitHub issue URL)"
            )
        elif not issue_url.startswith("https://github.com/"):
            validation_errors.append(
                "issue_url must be a valid GitHub URL "
                f"(https://github.com/...), got: {issue_url}"
            )
        validation_errors.append(approval.reason or "Approval URL is required")
        return None, "Authorization validation failed: " + "; ".join(validation_errors)

    return None, approval.reason or "Approval check failed"
