# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""API client functions for organization `is_agentic` flag management."""

from __future__ import annotations

import requests

from airbyte_ops_mcp.cloud_admin.api_client import _get_access_token
from airbyte_ops_mcp.cloud_admin.models import OrganizationInfo
from airbyte_ops_mcp.constants import USER_AGENT


class OrganizationAgenticFlagAPIError(Exception):
    """Raised when an organization `is_agentic` flag API call fails."""


def get_organization_info(
    organization_id: str,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> OrganizationInfo | None:
    """Fetch basic organization info by ID.

    Calls `POST /v1/organizations/get` on the Config API.
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
        raise OrganizationAgenticFlagAPIError(
            f"GET organization info failed: {response.status_code} {response.text}"
        )

    return OrganizationInfo.model_validate(response.json())


def set_organization_agentic_status(
    organization_id: str,
    is_agentic: bool,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> OrganizationInfo:
    """Set the organization agentic status through the Config API."""
    access_token = _get_access_token(client_id, client_secret, bearer_token)

    endpoint = f"{config_api_root}/organizations/agentic_status"
    response = requests.post(
        endpoint,
        json={"organizationId": organization_id, "isAgentic": is_agentic},
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise OrganizationAgenticFlagAPIError(
            f"Set organization agentic status failed: {response.status_code} {response.text}"
        )

    return OrganizationInfo.model_validate(response.json())
