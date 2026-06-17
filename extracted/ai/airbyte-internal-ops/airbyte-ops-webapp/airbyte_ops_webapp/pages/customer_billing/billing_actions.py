"""Billing actions panel: tabbed Grace Period / Permanent Waiver forms."""

from __future__ import annotations

from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import (
    Button,
    CardContent,
    Column,
    Dialog,
    Div,
    Grid,
    Input,
    Row,
    Select,
    Tab,
    Tabs,
    Text,
    Textarea,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import EVENT, STATE

from airbyte_ops_webapp.pages.customer_billing._helpers import (
    apply_fail_actions,
    apply_success_actions,
    render_select_options,
    start_tool_call,
)
from airbyte_ops_webapp.pages.customer_billing._mcp_tools import (
    apply_grace_period,
    apply_permanent_waiver,
)
from airbyte_ops_webapp.theme import (
    BUTTON_DESTRUCTIVE_CLASS,
    PANEL_CARD_CLASS,
    _card_style,
)


def render_billing_actions() -> None:
    """Render the right-panel tabbed billing actions."""
    with (
        Div(css_class=PANEL_CARD_CLASS, style=_card_style()),
        CardContent(),
        Column(gap=3),
    ):
        Text(
            "Billing Actions",
            style={"fontWeight": "700", "fontSize": "1.125rem"},
        )
        with Tabs(name="billing_action_tab", value="grace_period"):
            with Tab("Grace Period", value="grace_period"):
                _render_grace_period_form()
            with Tab("Permanent Waiver", value="permanent_waiver"):
                _render_permanent_waiver_form()


def _render_grace_period_form() -> None:
    """Grace period set/extend/cancel form."""
    with Column(gap=3):
        with Column(gap=1):
            Text(
                "End date or days", style={"fontSize": "0.875rem", "fontWeight": "500"}
            )
            Input(
                name="grace_period_value",
                value=STATE.grace_period_value,
                placeholder="YYYY-MM-DD, number of days (1-90), or 'cancel'",
            )
        with Column(gap=1):
            Text("Reason", style={"fontSize": "0.875rem", "fontWeight": "500"})
            Textarea(
                name="grace_period_reason",
                value=STATE.grace_period_reason,
                placeholder="e.g. 7-day extension per #ask-finance request",
                rows=2,
            )
        with Column(gap=1):
            Text("Approval URL", style={"fontSize": "0.875rem", "fontWeight": "500"})
            Input(
                name="grace_period_approval_url",
                value=STATE.grace_period_approval_url,
                placeholder="Slack approval record URL",
            )
        with Row(justify="end", gap=2):
            _render_grace_period_confirm_dialog()


def _render_permanent_waiver_form() -> None:
    """Permanent waiver set/remove form."""
    with Column(gap=3):
        with Column(gap=1):
            Text("Waiver Type", style={"fontSize": "0.875rem", "fontWeight": "500"})
            with Select(
                name="waiver_type",
                value="free",
                onChange=SetState("waiver_type", EVENT.target.value),
            ):
                render_select_options(
                    [
                        {"label": "Free (Partner)", "value": "free"},
                        {"label": "Internal", "value": "internal"},
                        {"label": "Remove Waiver", "value": "none"},
                    ]
                )
        with Column(gap=1):
            Text("Reason", style={"fontSize": "0.875rem", "fontWeight": "500"})
            Textarea(
                name="waiver_reason",
                value=STATE.waiver_reason,
                placeholder="e.g. Partner account per SOW",
                rows=2,
            )
        with Column(gap=1):
            Text("Approval URL", style={"fontSize": "0.875rem", "fontWeight": "500"})
            Input(
                name="waiver_approval_url",
                value=STATE.waiver_approval_url,
                placeholder="Slack approval record URL",
            )
        with If(STATE.waiver_type), If(STATE.waiver_type != "none"):
            Text(
                "Also changes Orb plan + Stigg entitlement automatically.",
                style={
                    "fontSize": "0.8125rem",
                    "opacity": "0.6",
                    "fontStyle": "italic",
                },
            )

        with Row(justify="end", gap=2):
            _render_waiver_confirm_dialog()


# ---------------------------------------------------------------------------
# Inline confirmation dialogs (Apply button = Dialog trigger)
# ---------------------------------------------------------------------------


def _render_confirm_field(label: str, value: object) -> None:
    """Render a single label-value row in the confirmation summary."""
    with Grid(columns=2, gap=2):
        Text(label, style={"fontSize": "0.875rem", "opacity": "0.7"})
        Text(
            content=value,
            style={"fontSize": "0.875rem", "fontWeight": "500"},
        )


def _render_grace_period_confirm_dialog() -> None:
    """Apply button that opens a confirmation dialog before firing the tool call."""
    with Dialog(
        title="Confirm Billing Change",
        description="Review the pending action before confirming.",
        name="grace_period_confirm_open",
    ):
        # Trigger: the Apply button itself
        Button(
            "Apply",
            variant="destructive",
            css_class=BUTTON_DESTRUCTIVE_CLASS,
            disabled=STATE.is_loading,
        )

        # Dialog body: confirmation summary + confirm/cancel
        with Column(gap=4):
            Text(
                "You are about to apply a billing change to a production organization.",
                style={"fontSize": "0.875rem", "opacity": "0.8"},
            )
            with Column(gap=2):
                _render_confirm_field("Organization", STATE.org_info.organization_name)
                _render_confirm_field("Action", "Set / Extend / Cancel Grace Period")
                _render_confirm_field("Value", STATE.grace_period_value)
                with If(STATE.grace_period_reason):
                    _render_confirm_field("Reason", STATE.grace_period_reason)

            with Row(justify="end", gap=2):
                Button(
                    "Confirm & Apply",
                    variant="destructive",
                    css_class=BUTTON_DESTRUCTIVE_CLASS,
                    disabled=STATE.is_loading,
                    on_click=[
                        SetState("grace_period_confirm_open", False),
                        *start_tool_call("Applying grace period change…"),
                        CallTool(
                            apply_grace_period,
                            arguments={
                                "organization_id": STATE.payment_config.organization_id,
                                "grace_period_value": STATE.grace_period_value,
                                "reason": STATE.grace_period_reason,
                                "approval_comment_url": STATE.grace_period_approval_url,
                                "organization_name": STATE.org_info.organization_name,
                                "auth_bearer_token": STATE.auth_bearer_token,
                                "google_access_token": STATE.google_access_token,
                            },
                            on_success=apply_success_actions(),
                            on_error=apply_fail_actions(),
                        ),
                    ],
                )


def _render_waiver_confirm_dialog() -> None:
    """Apply button that opens a confirmation dialog before firing the tool call."""
    with Dialog(
        title="Confirm Billing Change",
        description="Review the pending action before confirming.",
        name="waiver_confirm_open",
    ):
        # Trigger: the Apply button itself
        Button(
            "Apply",
            variant="destructive",
            css_class=BUTTON_DESTRUCTIVE_CLASS,
            disabled=STATE.is_loading,
        )

        # Dialog body: confirmation summary + confirm/cancel
        with Column(gap=4):
            Text(
                "You are about to apply a billing change to a production organization.",
                style={"fontSize": "0.875rem", "opacity": "0.8"},
            )
            with Column(gap=2):
                _render_confirm_field("Organization", STATE.org_info.organization_name)
                _render_confirm_field("Action", "Set / Remove Permanent Waiver")
                _render_confirm_field("Waiver Type", STATE.waiver_type)
                with If(STATE.waiver_reason):
                    _render_confirm_field("Reason", STATE.waiver_reason)

            with Row(justify="end", gap=2):
                Button(
                    "Confirm & Apply",
                    variant="destructive",
                    css_class=BUTTON_DESTRUCTIVE_CLASS,
                    disabled=STATE.is_loading,
                    on_click=[
                        SetState("waiver_confirm_open", False),
                        *start_tool_call("Applying permanent waiver…"),
                        CallTool(
                            apply_permanent_waiver,
                            arguments={
                                "organization_id": STATE.payment_config.organization_id,
                                "waiver_type": STATE.waiver_type,
                                "reason": STATE.waiver_reason,
                                "approval_comment_url": STATE.waiver_approval_url,
                                "organization_name": STATE.org_info.organization_name,
                                "auth_bearer_token": STATE.auth_bearer_token,
                                "google_access_token": STATE.google_access_token,
                            },
                            on_success=apply_success_actions(),
                            on_error=apply_fail_actions(),
                        ),
                    ],
                )
