# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""API client functions for organization payment config management.

This module provides direct HTTP access to the Airbyte Cloud Config API
endpoints for reading and updating organization payment configurations.
"""

from __future__ import annotations

from typing import Any, Literal

import requests

from airbyte_ops_mcp.cloud_admin.api_client import _get_access_token
from airbyte_ops_mcp.cloud_admin.models import OrganizationInfo
from airbyte_ops_mcp.constants import USER_AGENT

# Valid payment statuses from the OpenAPI spec
PaymentStatus = Literal[
    "uninitialized",
    "okay",
    "grace_period",
    "disabled",
    "locked",
    "manual",
]

# Valid usage category overwrite values
UsageCategoryOverwrite = Literal["free", "internal"]


class PaymentConfigAPIError(Exception):
    """Raised when a payment config API call fails."""


def get_organization_info(
    organization_id: str,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> OrganizationInfo | None:
    """Fetch basic organization info by ID.

    Calls `POST /v1/organizations/get` on the Config API.

    Returns an `OrganizationInfo` model, or `None` if the org is not found (404).

    Raises:
        PaymentConfigAPIError: If the API returns a non-200/404 status.
    """
    access_token = _get_access_token(client_id, client_secret, bearer_token)

    endpoint = f"{config_api_root}/organizations/get"
    response = requests.post(
        endpoint,
        json={"organizationId": organization_id},
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if response.status_code == 404:
        return None

    if response.status_code != 200:
        raise PaymentConfigAPIError(
            f"GET organization info failed: {response.status_code} {response.text}"
        )

    return OrganizationInfo.model_validate(response.json())


def get_organization_payment_config(
    organization_id: str,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> dict[str, Any]:
    """Fetch the current payment config for an organization.

    Calls `GET /api/v1/organization_payment_config/{organizationId}`.

    Returns the raw API response dict with keys: `organizationId`,
    `paymentStatus`, `subscriptionStatus`, `paymentProviderId`,
    `gracePeriodEndAt`, `usageCategoryOverwrite`.

    Raises:
        PaymentConfigAPIError: If the API returns a non-200 status.
    """
    access_token = _get_access_token(client_id, client_secret, bearer_token)

    endpoint = f"{config_api_root}/organization_payment_config/{organization_id}"
    response = requests.get(
        endpoint,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise PaymentConfigAPIError(
            f"GET payment config failed: {response.status_code} {response.text}"
        )

    return response.json()


def update_organization_payment_config(
    organization_id: str,
    payment_status: PaymentStatus,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
    payment_provider_id: str | None = None,
    grace_period_end_at: str | None = None,
    new_grace_period_reason: str | None = None,
    usage_category_overwrite: UsageCategoryOverwrite | None = None,
) -> dict[str, Any]:
    """Update the payment config for an organization.

    Calls `POST /api/v1/organization_payment_config`.

    The wrapped controller enforces these constraints:
    - Setting status to `grace_period` is only allowed from `manual` status.
    - `grace_period_end_at` and `new_grace_period_reason` are required when
      setting `grace_period`.
    - Grace period end date cannot be in the past or more than 90 days in the future.
    - Statuses `uninitialized`, `okay`, `disabled` cannot be set via this API.

    Returns the updated `OrganizationPaymentConfigRead` response dict.

    Raises:
        PaymentConfigAPIError: If the API returns a non-200 status.
    """
    access_token = _get_access_token(client_id, client_secret, bearer_token)

    payload: dict[str, Any] = {
        "organizationId": organization_id,
        "paymentStatus": payment_status,
    }
    if payment_provider_id is not None:
        payload["paymentProviderId"] = payment_provider_id
    if grace_period_end_at is not None:
        payload["gracePeriodEndAt"] = grace_period_end_at
    if new_grace_period_reason is not None:
        payload["newGracePeriodReason"] = new_grace_period_reason
    if usage_category_overwrite is not None:
        payload["usageCategoryOverwrite"] = usage_category_overwrite

    endpoint = f"{config_api_root}/organization_payment_config"
    response = requests.post(
        endpoint,
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise PaymentConfigAPIError(
            f"POST payment config update failed: {response.status_code} {response.text}"
        )

    return response.json()
