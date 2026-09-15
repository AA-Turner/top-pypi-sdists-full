"""Tool definitions for the Data Worker Allocation page."""

from __future__ import annotations

import logging
import math

from airbyte_ops_mcp.cloud_admin.data_worker_allocation import (
    DataWorkerAllocationAPIError,
    DataWorkerAllocationResponseError,
    add_data_worker_capacity,
    list_data_worker_allocations,
    list_dataplane_groups,
    remove_data_worker_capacity,
)
from airbyte_ops_mcp.cloud_admin.models import DataWorkerAllocationList
from airbyte_ops_mcp.cloud_admin.payment_config import (
    PaymentConfigAPIError,
    get_organization_info,
)
from fastmcp import FastMCPApp

from airbyte_ops_webapp.pages.customer_billing._helpers import (
    auth_available,
    resolved_bearer_token,
    resolved_config_api_root,
)
from airbyte_ops_webapp.pages.customer_billing._mcp_tools import _resolve_org_id
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation._state import (
    CapacityChangeResult,
    LookupAllocationsResult,
)
from airbyte_ops_webapp.pages.shared_components.org_search import (
    OrgSearchResult,
    search_organizations_and_workspaces,
)
from airbyte_ops_webapp.state import mock_only_enabled

logger = logging.getLogger(__name__)

data_worker_allocation_app = FastMCPApp("Data Worker Allocation")


def _named_allocation_rows(
    allocation_list: DataWorkerAllocationList,
    organization_id: str,
    bearer: str | None,
) -> list[dict[str, object]]:
    """Add a region name to each allocation row, falling back to its UUID.

    The allocation endpoints only return region UUIDs, so the names come from a
    second call. Deleted regions aren't listed, and a failed call names nothing.
    """
    names: dict[str, str] = {}
    try:
        group_list = list_dataplane_groups(
            organization_id=organization_id,
            config_api_root=resolved_config_api_root(),
            bearer_token=bearer,
        )
        names = {
            group.dataplane_group_id: group.name
            for group in group_list.dataplane_groups
        }
    except DataWorkerAllocationAPIError:
        logger.warning(
            "Could not get region names for org %s; showing UUIDs",
            organization_id,
            exc_info=True,
        )

    rows: list[dict[str, object]] = []
    for allocation in allocation_list.allocations:
        # Removing capacity leaves a zero row behind, and there is nothing to
        # act on in a region holding nothing.
        if allocation.allocated_capacity == 0:
            continue
        row = allocation.model_dump(mode="json")
        row["dataplane_group_name"] = names.get(
            allocation.dataplane_group_id,
            allocation.dataplane_group_id,
        )
        rows.append(row)
    return rows


@data_worker_allocation_app.tool()
def search_orgs_workspaces(query: str) -> OrgSearchResult:
    """Search organizations and workspaces by name."""
    return search_organizations_and_workspaces(query)


def _mock_lookup_result(query: str) -> LookupAllocationsResult:
    org_id = query.strip() or "00000000-aaaa-bbbb-cccc-111111111111"
    return LookupAllocationsResult(
        org_info={
            "organization_id": org_id,
            "organization_name": "Acme Corp (Demo)",
            "email": "platform-admin@acme-demo.io",
        },
        allocations={
            "organization_id": org_id,
            "total_allocated_capacity": 12.5,
            "allocations": [
                {
                    "dataplane_group_id": "dataplane-group-us-east-1",
                    "dataplane_group_name": "US",
                    "allocated_capacity": 8.0,
                },
                {
                    "dataplane_group_id": "dataplane-group-eu-west-1",
                    "dataplane_group_name": "EU",
                    "allocated_capacity": 4.5,
                },
            ],
        },
        org_loaded=True,
    )


@data_worker_allocation_app.tool()
def lookup_allocations(
    query: str = "",
    auth_bearer_token: str = "",
) -> LookupAllocationsResult:
    """Look up an organization's Data Worker allocations by ID or workspace ID."""
    if not auth_available(auth_bearer_token or None):
        return LookupAllocationsResult(
            lookup_error="Sign in with Airbyte to look up organizations.",
        )
    if mock_only_enabled():
        return _mock_lookup_result(query)

    bearer = resolved_bearer_token(auth_bearer_token or None)
    organization_id, resolved_label, resolution_error = _resolve_org_id(
        query,
        bearer_token_override=bearer,
    )
    if resolution_error or not organization_id:
        return LookupAllocationsResult(
            lookup_error=resolution_error or "Organization not found."
        )

    try:
        org_info = get_organization_info(
            organization_id=organization_id,
            config_api_root=resolved_config_api_root(),
            bearer_token=bearer,
        )
        if org_info is None:
            return LookupAllocationsResult(
                lookup_error=f"Organization {organization_id} was not found."
            )
        allocation_list = list_data_worker_allocations(
            organization_id=organization_id,
            config_api_root=resolved_config_api_root(),
            bearer_token=bearer,
        )
    except (PaymentConfigAPIError, DataWorkerAllocationAPIError) as error:
        return LookupAllocationsResult(lookup_error=str(error))

    allocations = allocation_list.model_dump(mode="json")
    allocations["allocations"] = _named_allocation_rows(
        allocation_list,
        organization_id,
        bearer,
    )
    return LookupAllocationsResult(
        org_info=org_info.model_dump(mode="json"),
        allocations=allocations,
        resolved_org_label=resolved_label or "",
        org_loaded=True,
    )


def _parse_amount(
    amount: str,
    organization_id: str,
) -> tuple[float | None, CapacityChangeResult | None]:
    """Turn the amount field into a positive number, or say why it isn't one."""
    try:
        amount_value = float(amount)
    except (TypeError, ValueError):
        amount_value = math.nan
    if not math.isfinite(amount_value):
        return None, CapacityChangeResult(
            message="Capacity amount must be a positive number.",
            organization_id=organization_id,
        )
    if amount_value <= 0:
        return None, CapacityChangeResult(
            message="Capacity amount must be greater than zero.",
            organization_id=organization_id,
        )
    return amount_value, None


def _committed_but_unreadable(
    organization_id: str,
    message: str,
) -> CapacityChangeResult:
    """Report a committed change whose new totals could not be read back."""
    return CapacityChangeResult(
        success=True,
        message=f"{message} The updated totals could not be read back.",
        organization_id=organization_id,
        stale=True,
    )


def _changed_capacity_result(
    allocation_list: DataWorkerAllocationList,
    organization_id: str,
    bearer: str | None,
    message: str,
) -> CapacityChangeResult:
    """Build the success result shared by adding and removing capacity."""
    return _readable_capacity_result(
        organization_id,
        message,
        allocation_list.total_allocated_capacity,
        _named_allocation_rows(allocation_list, organization_id, bearer),
    )


def _readable_capacity_result(
    organization_id: str,
    message: str,
    total_allocated_capacity: float,
    allocations: list[dict[str, object]],
) -> CapacityChangeResult:
    """Build a success result whose new totals replace the page's overview."""
    return CapacityChangeResult(
        success=True,
        message=message,
        organization_id=organization_id,
        total_allocated_capacity=total_allocated_capacity,
        allocations=allocations,
        allocations_view={
            "organization_id": organization_id,
            "total_allocated_capacity": total_allocated_capacity,
            "allocations": allocations,
        },
    )


@data_worker_allocation_app.tool()
def add_capacity(
    organization_id: str,
    amount: str,
    organization_name: str = "",
    auth_bearer_token: str = "",
) -> CapacityChangeResult:
    """Add Data Worker capacity to an organization's default region."""
    amount_value, amount_error = _parse_amount(amount, organization_id)
    if amount_error is not None:
        return amount_error
    assert amount_value is not None
    if not auth_available(auth_bearer_token or None):
        return CapacityChangeResult(
            message="Sign in with Airbyte to add Data Worker capacity.",
            organization_id=organization_id,
        )
    if mock_only_enabled():
        return _readable_capacity_result(
            organization_id,
            f"[MOCK] Added {amount_value:g} capacity for "
            f"{organization_name or organization_id}.",
            12.5 + amount_value,
            [],
        )

    bearer = resolved_bearer_token(auth_bearer_token or None)
    try:
        allocation_list = add_data_worker_capacity(
            organization_id=organization_id,
            amount=amount_value,
            config_api_root=resolved_config_api_root(),
            bearer_token=bearer,
        )
    except DataWorkerAllocationResponseError:
        return _committed_but_unreadable(
            organization_id, f"Added {amount_value:g} capacity."
        )
    except DataWorkerAllocationAPIError as error:
        return CapacityChangeResult(
            message=str(error),
            organization_id=organization_id,
        )
    return _changed_capacity_result(
        allocation_list,
        organization_id,
        bearer,
        f"Added {amount_value:g} capacity.",
    )


@data_worker_allocation_app.tool()
def remove_capacity(
    organization_id: str,
    dataplane_group_id: str,
    amount: str,
    region_name: str = "",
    auth_bearer_token: str = "",
) -> CapacityChangeResult:
    """Remove Data Worker capacity from one of an organization's regions."""
    amount_value, amount_error = _parse_amount(amount, organization_id)
    if amount_error is not None:
        return amount_error
    assert amount_value is not None
    if not dataplane_group_id.strip():
        return CapacityChangeResult(
            message="Pick the region to remove capacity from.",
            organization_id=organization_id,
        )
    if not auth_available(auth_bearer_token or None):
        return CapacityChangeResult(
            message="Sign in with Airbyte to remove Data Worker capacity.",
            organization_id=organization_id,
        )
    if mock_only_enabled():
        return _readable_capacity_result(
            organization_id,
            f"[MOCK] Removed {amount_value:g} capacity from "
            f"{region_name or dataplane_group_id}.",
            max(0.0, 12.5 - amount_value),
            [],
        )

    bearer = resolved_bearer_token(auth_bearer_token or None)
    try:
        allocation_list = remove_data_worker_capacity(
            organization_id=organization_id,
            dataplane_group_id=dataplane_group_id,
            amount=amount_value,
            config_api_root=resolved_config_api_root(),
            bearer_token=bearer,
        )
    except DataWorkerAllocationResponseError:
        return _committed_but_unreadable(
            organization_id,
            f"Removed {amount_value:g} capacity from "
            f"{region_name or dataplane_group_id}.",
        )
    except DataWorkerAllocationAPIError as error:
        return CapacityChangeResult(
            message=str(error),
            organization_id=organization_id,
        )
    return _changed_capacity_result(
        allocation_list,
        organization_id,
        bearer,
        f"Removed {amount_value:g} capacity from {region_name or dataplane_group_id}.",
    )
