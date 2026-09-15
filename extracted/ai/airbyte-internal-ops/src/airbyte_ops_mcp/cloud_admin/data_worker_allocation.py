# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""API client functions for Data Worker allocation management."""

from __future__ import annotations

import requests
from pydantic import ValidationError

from airbyte_ops_mcp.cloud_admin.api_client import _get_access_token
from airbyte_ops_mcp.cloud_admin.models import (
    DataplaneGroupList,
    DataWorkerAllocationList,
)
from airbyte_ops_mcp.constants import USER_AGENT


class DataWorkerAllocationAPIError(Exception):
    """Raised when a Data Worker allocation API call fails."""


class DataWorkerAllocationResponseError(DataWorkerAllocationAPIError):
    """Raised when the call succeeded but its response could not be read."""


def _post_allocation_request(
    *,
    path: str,
    payload: dict[str, object],
    operation: str,
    config_api_root: str,
    client_id: str | None,
    client_secret: str | None,
    bearer_token: str | None,
) -> DataWorkerAllocationList:
    try:
        access_token = _get_access_token(client_id, client_secret, bearer_token)
        response = requests.post(
            f"{config_api_root}/{path}",
            json=payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": USER_AGENT,
                "Content-Type": "application/json",
            },
            timeout=30,
        )
    except requests.RequestException as error:
        raise DataWorkerAllocationAPIError(f"{operation} failed: {error}") from error

    if response.status_code != 200:
        raise DataWorkerAllocationAPIError(
            f"{operation} failed: {response.status_code} {response.text}"
        )

    # A 200 means a capacity change already committed, so an unreadable body
    # is not a failed call.
    try:
        return DataWorkerAllocationList.model_validate(response.json())
    except (ValidationError, ValueError) as error:
        raise DataWorkerAllocationResponseError(
            f"{operation} returned an unreadable response: {error}"
        ) from error


def list_data_worker_allocations(
    organization_id: str,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> DataWorkerAllocationList:
    """List the Data Worker allocations for an organization."""
    return _post_allocation_request(
        path="data_worker_allocation/list",
        payload={"organization_id": organization_id},
        operation="POST data worker allocation list",
        config_api_root=config_api_root,
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
    )


def list_dataplane_groups(
    organization_id: str,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> DataplaneGroupList:
    """List the regions an organization can hold Data Worker capacity in.

    Deleted regions are left out, so an organization can still hold capacity in
    a region that is missing from this list.
    """
    try:
        access_token = _get_access_token(client_id, client_secret, bearer_token)
        response = requests.post(
            f"{config_api_root}/dataplane_group/list",
            json={"organization_id": organization_id},
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": USER_AGENT,
                "Content-Type": "application/json",
            },
            timeout=30,
        )
        if response.status_code != 200:
            raise DataWorkerAllocationAPIError(
                f"POST dataplane group list failed: "
                f"{response.status_code} {response.text}"
            )
        return DataplaneGroupList.model_validate(response.json())
    except (requests.RequestException, ValidationError, ValueError) as error:
        raise DataWorkerAllocationAPIError(
            f"POST dataplane group list failed: {error}"
        ) from error


def add_data_worker_capacity(
    organization_id: str,
    amount: float,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> DataWorkerAllocationList:
    """Add Data Worker capacity to an organization's allocation."""
    return _post_allocation_request(
        path="data_worker_allocation/add_capacity",
        payload={"organization_id": organization_id, "amount": amount},
        operation="POST data worker capacity",
        config_api_root=config_api_root,
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
    )


def remove_data_worker_capacity(
    organization_id: str,
    dataplane_group_id: str,
    amount: float,
    config_api_root: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    bearer_token: str | None = None,
) -> DataWorkerAllocationList:
    """Remove Data Worker capacity from one of an organization's regions.

    The region has to be named because capacity is held per region. The amount
    cannot be more than that region currently holds.
    """
    return _post_allocation_request(
        path="data_worker_allocation/remove_capacity",
        payload={
            "organization_id": organization_id,
            "dataplane_group_id": dataplane_group_id,
            "amount": amount,
        },
        operation="POST data worker remove capacity",
        config_api_root=config_api_root,
        client_id=client_id,
        client_secret=client_secret,
        bearer_token=bearer_token,
    )
