"""Typed Prefab state for the Data Worker Allocation page."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from airbyte_ops_webapp.pages.shared_components.org_lookup_modal import (
    OrgLookupModalState,
)
from airbyte_ops_webapp.state import OpsPageState


class OrgInfo(BaseModel):
    """Organization identity placeholder."""

    model_config = ConfigDict(frozen=True)

    organization_id: str = ""
    organization_name: str = ""
    email: str = ""


class AllocationItem(BaseModel):
    """Dataplane allocation placeholder."""

    model_config = ConfigDict(frozen=True)

    dataplane_group_id: str = ""
    # Region name, or the UUID again when the name is unavailable.
    dataplane_group_name: str = ""
    allocated_capacity: float = 0.0


class AllocationsPlaceholder(BaseModel):
    """Data Worker allocation placeholder."""

    model_config = ConfigDict(frozen=True)

    organization_id: str = ""
    total_allocated_capacity: float = 0.0
    allocations: list[AllocationItem] = Field(default_factory=list)


class ApplyResult(BaseModel):
    """Capacity-application result placeholder."""

    model_config = ConfigDict(frozen=True)

    success: bool = False
    message: str = ""
    organization_id: str = ""
    total_allocated_capacity: float | None = None
    allocations: list[dict[str, object]] | None = None


class LookupAllocationsResult(BaseModel):
    """Typed output of `lookup_allocations`."""

    model_config = ConfigDict(frozen=True)

    org_info: dict[str, object] | None = None
    allocations: dict[str, object] | None = None
    resolved_org_label: str = ""
    org_loaded: bool = False
    lookup_error: str = ""


class CapacityChangeResult(BaseModel):
    """Typed output of `add_capacity` and `remove_capacity`."""

    model_config = ConfigDict(frozen=True)

    success: bool = False
    message: str = ""
    organization_id: str = ""
    total_allocated_capacity: float | None = None
    allocations: list[dict[str, object]] | None = None
    # True when the change committed but its new totals could not be read.
    stale: bool = False
    # Replacement for the page's `allocations` state; `None` leaves it untouched.
    allocations_view: dict[str, object] | None = None


class DataWorkerAllocationPageState(OpsPageState, OrgLookupModalState):
    """Complete initial Prefab state for Data Worker Allocation."""

    org_query: str = ""
    org_info: OrgInfo = Field(default_factory=OrgInfo)
    allocations: AllocationsPlaceholder = Field(default_factory=AllocationsPlaceholder)
    resolved_org_label: str = ""
    org_loaded: bool = False
    lookup_error: str = ""
    add_amount: str = ""
    add_confirm_open: bool = False
    remove_amount: str = ""
    # Set by the Remove button on a region's row. Adding needs no region
    # because the platform always adds to the default one.
    remove_dataplane_group_id: str = ""
    # Kept so the dialog can name the region instead of showing a UUID.
    remove_dataplane_group_name: str = ""
    remove_confirm_open: bool = False
    apply_result: ApplyResult = Field(default_factory=ApplyResult)
    result_modal_open: bool = False
    # True when the shown allocation may not match the backend.
    allocations_stale: bool = False
