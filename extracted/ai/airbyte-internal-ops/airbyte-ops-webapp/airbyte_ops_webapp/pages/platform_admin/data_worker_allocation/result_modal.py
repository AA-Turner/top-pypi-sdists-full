"""Result modal for Data Worker capacity changes."""

from __future__ import annotations

from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import Button, Column, Dialog, Grid, Markdown, Row, Text
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation._helpers import (
    lookup_success_actions,
    refresh_fail_actions,
    start_tool_call,
)
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation._mcp_tools import (
    lookup_allocations,
)
from airbyte_ops_webapp.theme import BUTTON_INFO_CLASS, AbFieldLabel, AbFieldValue


def render_result_modal() -> None:
    """Render the result modal shown after applying capacity."""
    with Dialog(title="", description="", name="result_modal_open"):
        Button("", css_class="hidden")
        with Column(gap=4):
            with If(STATE.apply_result.success), Column(gap=3):
                Markdown("**Capacity Updated**")
                _render_result_field("Organization", STATE.org_info.organization_name)
                _render_result_field("Result", STATE.apply_result.message)
                _render_result_field(
                    "New Total Capacity",
                    STATE.apply_result.total_allocated_capacity,
                )
            with If(~STATE.apply_result.success), Column(gap=3):
                Markdown("**Update Failed**")
                Text(content=STATE.apply_result.message)
            with Row(justify="end"):
                Button(
                    "Done",
                    variant="info",
                    css_class=BUTTON_INFO_CLASS,
                    on_click=[
                        SetState("result_modal_open", False),
                        *start_tool_call("Refreshing allocation state…"),
                        CallTool(
                            lookup_allocations,
                            arguments={
                                "query": STATE.allocations.organization_id,
                                "auth_bearer_token": STATE.auth_bearer_token,
                            },
                            on_success=lookup_success_actions(),
                            on_error=refresh_fail_actions(),
                        ),
                    ],
                )


def _render_result_field(label: str, value: object) -> None:
    """Render a result field."""
    with Grid(columns=2, gap=2):
        AbFieldLabel(label)
        AbFieldValue(content=value)
