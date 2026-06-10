# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""API client functions for Orb billing subscription management.

This module provides HTTP access to the Orb API for listing subscriptions
and scheduling plan changes. Used to automate Orb plan transitions when
setting permanent billing waivers on organizations.

Orb API docs: https://docs.withorb.com/api-reference
"""

from __future__ import annotations

import logging
import os
from typing import Any

import requests

from airbyte_ops_mcp.constants import USER_AGENT

logger = logging.getLogger(__name__)

ORB_API_BASE_URL = "https://api.withorb.com/v1"
"""Base URL for the Orb REST API."""

ENV_ORB_API_KEY = "ORB_API_KEY"
"""Environment variable name for the Orb API key."""

# Mapping from permanent waiver type to the Orb plan_id.
# These can be overridden via environment variables for flexibility.
ENV_ORB_PARTNER_PLAN_ID = "ORB_PARTNER_PLAN_ID"
ENV_ORB_INTERNAL_PLAN_ID = "ORB_INTERNAL_PLAN_ID"

DEFAULT_ORB_PARTNER_PLAN_ID = "VwkusX467BUccNtf"
"""Orb internal plan ID for 'Airbyte Partner'."""

DEFAULT_ORB_INTERNAL_PLAN_ID = "KVa2sbZUrjyJ9NZr"
"""Orb internal plan ID for 'Airbyte Internal'."""

WAIVER_TYPE_TO_ORB_PLAN: dict[str, str] = {
    "free": DEFAULT_ORB_PARTNER_PLAN_ID,
    "internal": DEFAULT_ORB_INTERNAL_PLAN_ID,
}
"""Maps `set_permanent_waiver_type` values to Orb `plan_id` values."""


class OrbAPIError(Exception):
    """Raised when an Orb API call fails."""


def _get_orb_api_key() -> str | None:
    """Resolve the Orb API key from the environment."""
    return os.environ.get(ENV_ORB_API_KEY)


def _resolve_plan_id(waiver_type: str) -> str:
    """Resolve the Orb `plan_id` for a given waiver type.

    Checks environment variable overrides first, then falls back to defaults.
    """
    if waiver_type == "free":
        return os.environ.get(ENV_ORB_PARTNER_PLAN_ID, DEFAULT_ORB_PARTNER_PLAN_ID)
    if waiver_type == "internal":
        return os.environ.get(ENV_ORB_INTERNAL_PLAN_ID, DEFAULT_ORB_INTERNAL_PLAN_ID)
    msg = f"No Orb plan mapping for waiver type: {waiver_type!r}"
    raise ValueError(msg)


def _orb_headers(api_key: str) -> dict[str, str]:
    """Build common HTTP headers for Orb API requests."""
    return {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
    }


def list_subscriptions_for_org(
    organization_id: str,
    api_key: str,
) -> list[dict[str, Any]]:
    """List Orb subscriptions for an organization using its ID as `external_customer_id`.

    Returns the raw list of subscription dicts from the Orb API.
    Only returns the first page (up to 100 results); orgs typically have
    a single active subscription.

    Raises:
        OrbAPIError: If the API returns a non-200 status.
    """
    endpoint = f"{ORB_API_BASE_URL}/subscriptions"
    response = requests.get(
        endpoint,
        params={"external_customer_id": organization_id, "limit": 100},
        headers=_orb_headers(api_key),
        timeout=30,
    )
    if response.status_code != 200:
        raise OrbAPIError(
            f"Orb list subscriptions failed: {response.status_code} {response.text}"
        )
    data = response.json()
    return data.get("data", [])


def get_active_subscription(
    organization_id: str,
    api_key: str,
) -> dict[str, Any] | None:
    """Find the active Orb subscription for an organization.

    Returns the first subscription with `status == "active"`, or `None` if
    no active subscription exists.
    """
    subscriptions = list_subscriptions_for_org(organization_id, api_key)
    for sub in subscriptions:
        if sub.get("status") == "active":
            return sub
    return None


def schedule_plan_change(
    subscription_id: str,
    plan_id: str,
    api_key: str,
) -> dict[str, Any]:
    """Schedule an immediate plan change on an Orb subscription.

    Calls `POST /subscriptions/{subscription_id}/schedule_plan_change` with
    `change_option=immediate`.

    Returns the mutated subscription dict from the Orb API.

    Raises:
        OrbAPIError: If the API returns a non-200 status.
    """
    endpoint = (
        f"{ORB_API_BASE_URL}/subscriptions/{subscription_id}/schedule_plan_change"
    )
    payload = {
        "change_option": "immediate",
        "plan_id": plan_id,
    }
    response = requests.post(
        endpoint,
        json=payload,
        headers=_orb_headers(api_key),
        timeout=30,
    )
    if response.status_code != 200:
        raise OrbAPIError(
            f"Orb schedule plan change failed: {response.status_code} {response.text}"
        )
    return response.json()


def extract_subscription_summary(subscription: dict[str, Any]) -> dict[str, Any]:
    """Extract a human-readable summary from a raw Orb subscription dict.

    Returns a flat dict with the most useful fields for display.
    """
    plan = subscription.get("plan") or {}
    customer = subscription.get("customer") or {}
    return {
        "subscription_id": subscription.get("id"),
        "status": subscription.get("status"),
        "plan_id": plan.get("id"),
        "plan_name": plan.get("name"),
        "external_plan_id": plan.get("external_plan_id"),
        "start_date": subscription.get("start_date"),
        "end_date": subscription.get("end_date"),
        "orb_customer_id": customer.get("id"),
        "external_customer_id": customer.get("external_customer_id"),
    }
