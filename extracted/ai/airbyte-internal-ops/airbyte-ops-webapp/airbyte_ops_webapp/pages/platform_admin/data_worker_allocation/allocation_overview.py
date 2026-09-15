"""Current Data Worker allocation overview."""

from __future__ import annotations

from prefab_ui.actions import SetState
from prefab_ui.components import (
    Alert,
    Button,
    CardContent,
    Column,
    Grid,
    Muted,
    Text,
)
from prefab_ui.components.control_flow import ForEach, If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.theme import (
    BUTTON_OUTLINE_CLASS,
    AbCard,
    AbCardValue,
    AbFieldLabel,
    AbFieldValue,
    AbSectionTitle,
)


def render_allocation_overview() -> None:
    """Render the organization's current allocation and dataplane rows."""
    with AbCard(), CardContent(), Column(gap=3):
        AbSectionTitle("Current Allocation")
        with (
            If(STATE.allocations_stale),
            Alert(variant="warning", icon="triangle-alert"),
        ):
            Text(
                content=(
                    "These numbers may not match the backend. "
                    "Look up the organization again to confirm."
                )
            )
        with Grid(columns=2, gap=2):
            AbFieldLabel("Organization")
            AbFieldValue(content=STATE.org_info.organization_name)
            AbFieldLabel("Organization ID")
            AbFieldValue(content=STATE.org_info.organization_id)
            AbFieldLabel("Total Capacity")
            AbCardValue(content=STATE.allocations.total_allocated_capacity)
        with If(STATE.allocations.allocations):
            Text("Dataplane Groups", css_class="font-semibold")
            with Column(gap=2), Grid(columns=3, gap=2):
                Text("Region", css_class="text-sm font-semibold")
                Text("Allocated capacity", css_class="text-sm font-semibold")
                Text("")
                with ForEach(STATE.allocations.allocations) as allocation:
                    AbFieldValue(content=allocation.dataplane_group_name)
                    AbFieldValue(content=allocation.allocated_capacity)
                    # Capacity is removed per region, so the button is per row.
                    Button(
                        "Remove",
                        variant="outline",
                        size="sm",
                        css_class=BUTTON_OUTLINE_CLASS,
                        disabled=STATE.is_loading,
                        on_click=[
                            SetState(
                                "remove_dataplane_group_id",
                                allocation.dataplane_group_id,
                            ),
                            SetState(
                                "remove_dataplane_group_name",
                                allocation.dataplane_group_name,
                            ),
                            SetState("remove_amount", ""),
                            SetState("remove_confirm_open", True),
                        ],
                    )
        with If(~STATE.allocations.allocations):
            Muted("No dataplane group allocations.")
