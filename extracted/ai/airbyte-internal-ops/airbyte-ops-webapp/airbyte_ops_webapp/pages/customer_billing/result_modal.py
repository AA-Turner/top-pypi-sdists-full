"""Result modal dialog for the Payment & Billing Manager page."""

from __future__ import annotations

from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import (
    Button,
    Column,
    Dialog,
    Grid,
    Markdown,
    Row,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.pages.customer_billing._helpers import (
    lookup_success_actions,
    start_tool_call,
)
from airbyte_ops_webapp.pages.customer_billing._mcp_tools import (
    lookup_organization,
)
from airbyte_ops_webapp.theme import BUTTON_INFO_CLASS


def render_result_modal() -> None:
    """Render the result/confirmation modal dialog.

    Shown after an Apply action completes (success or error).
    Dismissed by clicking "Done", which also triggers a refresh of billing state.
    """
    with Dialog(
        title="",
        description="",
        name="result_modal_open",
    ):
        # Hidden trigger — the dialog is opened via state, not a trigger button
        Button("", css_class="hidden")

        with Column(gap=4):
            _render_success_content()
            _render_error_content()
            _render_done_button()


def _render_success_content() -> None:
    """Content shown when the apply operation succeeded."""
    with If(STATE.apply_result.success), Column(gap=3):
        Markdown("**Payment Configuration Updated**")
        _render_result_field("Organization", STATE.org_info.organization_name)
        _render_result_field("Action", STATE.apply_result.message)
        _render_result_field("Payment Status", STATE.apply_result.payment_status)
        with If(STATE.apply_result.grace_period_end_at):
            _render_result_field(
                "Grace Period Ends", STATE.apply_result.grace_period_end_at
            )
        with If(STATE.apply_result.permanent_waiver_type):
            _render_result_field(
                "Waiver Type", STATE.apply_result.permanent_waiver_type
            )
        with If(STATE.apply_result.orb_plan_change):
            _render_result_field("Orb Plan Change", STATE.apply_result.orb_plan_change)
        with If(STATE.apply_result.entitlement_plan_change):
            _render_result_field(
                "Stigg Entitlement",
                STATE.apply_result.entitlement_plan_change,
            )
        with If(STATE.apply_result.customer_tier):
            _render_result_field("Tier", STATE.apply_result.customer_tier)
        with If(STATE.apply_result.tier_warning):
            Text(
                content=STATE.apply_result.tier_warning,
                style={"color": "#B42318", "fontWeight": "600", "fontSize": "0.875rem"},
            )


def _render_error_content() -> None:
    """Content shown when the apply operation failed."""
    with If(~STATE.apply_result.success), Column(gap=3):
        Markdown("**Update Failed**")
        Text(
            content=STATE.apply_result.message,
            style={"fontSize": "0.875rem"},
        )


def _render_result_field(label: str, value: object) -> None:
    """Render a single label-value row in the modal."""
    with Grid(columns=2, gap=2):
        Text(
            label,
            style={"fontSize": "0.875rem", "opacity": "0.7"},
        )
        Text(
            content=value,
            style={"fontSize": "0.875rem", "fontWeight": "500"},
        )


def _render_done_button() -> None:
    """Done button that dismisses the modal and refreshes billing state."""
    with Row(justify="end"):
        Button(
            "Done",
            variant="info",
            css_class=BUTTON_INFO_CLASS,
            on_click=[
                SetState("result_modal_open", False),
                # Refresh the billing state by re-running the lookup
                *start_tool_call("Refreshing billing state…"),
                CallTool(
                    lookup_organization,
                    arguments={
                        "query": STATE.payment_config.organization_id,
                        "auth_bearer_token": STATE.auth_bearer_token,
                    },
                    on_success=lookup_success_actions(),
                    on_error=[
                        SetState("is_loading", False),
                        SetState("loading_message", ""),
                    ],
                ),
            ],
        )
