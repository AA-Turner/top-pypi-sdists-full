# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""API client functions for Airbyte Cloud entitlement plan management.

This module provides HTTP access to the Airbyte Cloud Config API for updating
organization entitlement plans (Stigg). Used to automate Stigg plan transitions
when setting permanent billing waivers on organizations.

The entitlement plan controls frontend feature gating and trial paywall visibility.
"""

from __future__ import annotations

import logging
from typing import Literal

import requests

from airbyte_ops_mcp.cloud_admin.api_client import _get_access_token
from airbyte_ops_mcp.constants import USER_AGENT

logger = logging.getLogger(__name__)

# Mapping from permanent waiver type to the Stigg entitlement plan name.
# These are the enum values accepted by POST /v1/entitlements/update_plan.
WAIVER_TYPE_TO_ENTITLEMENT_PLAN: dict[str, str] = {
    "free": "PARTNER",
    "internal": "PARTNER",
}
"""Maps permanent waiver type to the target Stigg entitlement plan name."""

# Valid plan names from the OpenAPI spec enum
EntitlementPlanName = Literal[
    "CORE",
    "SME",
    "STANDARD",
    "STANDARD_TRIAL",
    "PRO",
    "UNIFIED_TRIAL",
    "PARTNER",
    "POV",
    "FLEX",
    "EMBEDDED_PAYG",
    "EMBEDDED_ANNUAL_COMMITMENT",
]


class EntitlementAPIError(Exception):
    """Raised when an entitlement plan API call fails."""


def update_entitlement_plan(
    organization_id: str,
    plan_name: EntitlementPlanName | str,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> dict[str, str]:
    """Update an organization's entitlement plan (Stigg).

    Calls `POST /v1/entitlements/update_plan` on the Config API.

    This endpoint controls the Stigg entitlement plan which gates frontend
    features and the trial paywall modal. Changing from `UNIFIED_TRIAL` to
    `PARTNER` removes the trial expired paywall.

    Note: The API uses **snake_case** field names (`organization_id`, `plan_name`),
    not camelCase.

    Args:
        organization_id: The organization UUID.
        plan_name: Target plan name (e.g. `PARTNER`, `STANDARD`).
        config_api_root: Config API base URL (e.g. `https://cloud.airbyte.com/api/v1`).
        client_id: Airbyte Cloud client ID.
        client_secret: Airbyte Cloud client secret.
        bearer_token: Pre-existing bearer token (takes precedence over client creds).

    Returns:
        Dict with `organization_id` and `plan_name` confirming the update.

    Raises:
        EntitlementAPIError: If the API returns a non-200 status.
    """
    access_token = _get_access_token(client_id, client_secret, bearer_token)

    endpoint = f"{config_api_root}/entitlements/update_plan"
    response = requests.post(
        endpoint,
        json={
            "organization_id": organization_id,
            "plan_name": plan_name,
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise EntitlementAPIError(
            f"POST entitlements/update_plan failed: {response.status_code} {response.text}"
        )

    return response.json()
