"""Add and remove Data Worker capacity actions."""

from __future__ import annotations

from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import (
    Button,
    CardContent,
    Column,
    Dialog,
    Grid,
    Input,
    Row,
    Text,
)
from prefab_ui.rx import STATE

from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation._helpers import (
    apply_fail_actions,
    apply_success_actions,
    start_tool_call,
)
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation._mcp_tools import (
    add_capacity,
    remove_capacity,
)
from airbyte_ops_webapp.theme import (
    BUTTON_INFO_CLASS,
    AbCard,
    AbFieldLabel,
    AbFieldValue,
    AbSectionTitle,
)


def render_allocation_actions() -> None:
    """Render the add-capacity form and both confirmation dialogs."""
    with AbCard(), CardContent(), Column(gap=3):
        AbSectionTitle("Add Capacity")
        Text("Add Data Worker capacity to the selected organization.")
        Input(
            name="add_amount",
            value=STATE.add_amount,
            placeholder="Capacity amount",
        )
        with Row(justify="end"):
            _render_confirm_dialog()
    # Opened from a row button, so it has no trigger in this card.
    _render_remove_confirm_dialog()


def _render_confirm_dialog() -> None:
    with Dialog(
        title="Confirm Capacity Change",
        description="Review the pending capacity addition before confirming.",
        name="add_confirm_open",
    ):
        Button(
            "Apply",
            variant="info",
            css_class=BUTTON_INFO_CLASS,
            disabled=STATE.is_loading,
        )
        with Column(gap=4):
            Text("You are about to add Data Worker capacity to this organization.")
            with Grid(columns=2, gap=2):
                AbFieldLabel("Organization")
                AbFieldValue(content=STATE.org_info.organization_name)
                AbFieldLabel("Amount")
                AbFieldValue(content=STATE.add_amount)
            with Row(justify="end"):
                Button(
                    "Confirm & Apply",
                    variant="info",
                    css_class=BUTTON_INFO_CLASS,
                    disabled=STATE.is_loading,
                    on_click=[
                        SetState("add_confirm_open", False),
                        *start_tool_call("Adding Data Worker capacity…"),
                        CallTool(
                            add_capacity,
                            arguments={
                                "organization_id": STATE.allocations.organization_id,
                                "amount": STATE.add_amount,
                                "organization_name": STATE.org_info.organization_name,
                                "auth_bearer_token": STATE.auth_bearer_token,
                            },
                            on_success=apply_success_actions(),
                            on_error=apply_fail_actions(),
                        ),
                    ],
                )


def _render_remove_confirm_dialog() -> None:
    with Dialog(
        title="Remove Capacity",
        description="Choose how much capacity to take back from this region.",
        name="remove_confirm_open",
    ):
        # Hidden trigger; the row button opens this via state.
        Button("", css_class="hidden")
        with Column(gap=4):
            with Grid(columns=2, gap=2):
                AbFieldLabel("Organization")
                AbFieldValue(content=STATE.org_info.organization_name)
                AbFieldLabel("Region")
                AbFieldValue(content=STATE.remove_dataplane_group_name)
            Input(
                name="remove_amount",
                value=STATE.remove_amount,
                placeholder="Capacity amount",
            )
            with Row(justify="end"):
                Button(
                    "Confirm & Remove",
                    variant="info",
                    css_class=BUTTON_INFO_CLASS,
                    disabled=STATE.is_loading,
                    on_click=[
                        SetState("remove_confirm_open", False),
                        *start_tool_call("Removing Data Worker capacity…"),
                        CallTool(
                            remove_capacity,
                            arguments={
                                "organization_id": STATE.allocations.organization_id,
                                "dataplane_group_id": STATE.remove_dataplane_group_id,
                                "amount": STATE.remove_amount,
                                "region_name": STATE.remove_dataplane_group_name,
                                "auth_bearer_token": STATE.auth_bearer_token,
                            },
                            on_success=apply_success_actions(),
                            on_error=apply_fail_actions(),
                        ),
                    ],
                )
