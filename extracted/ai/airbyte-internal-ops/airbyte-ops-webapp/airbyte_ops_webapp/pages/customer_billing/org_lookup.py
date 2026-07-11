"""Organization lookup card for the Customer Billing page."""

from __future__ import annotations

from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import (
    Alert,
    Button,
    CardContent,
    Column,
    Div,
    Input,
    Row,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.pages.customer_billing._helpers import (
    lookup_fail_actions,
    lookup_success_actions,
    start_tool_call,
)
from airbyte_ops_webapp.pages.customer_billing._mcp_tools import (
    lookup_organization,
    search_orgs_workspaces,
)
from airbyte_ops_webapp.pages.shared_components.org_lookup_modal import (
    render_org_lookup_modal,
)
from airbyte_ops_webapp.theme import BUTTON_INFO_CLASS, PANEL_CARD_CLASS, _card_style


def render_org_lookup() -> None:
    """Render the organization lookup card."""
    with (
        Div(css_class=PANEL_CARD_CLASS, style=_card_style()),
        CardContent(),
        Column(gap=3),
    ):
        Text(
            "Look Up Organization", style={"fontWeight": "700", "fontSize": "1.125rem"}
        )
        with Row(gap=2, align="end"):
            Input(
                name="org_query",
                value=STATE.org_query,
                placeholder="Organization ID or Workspace ID",
                style={"flex": "1"},
            )
            render_org_lookup_modal(
                search_tool=search_orgs_workspaces,
                target_state_key="org_query",
                on_select_actions=[
                    *start_tool_call("Looking up organization…"),
                    SetState("org_loaded", False),
                    CallTool(
                        lookup_organization,
                        arguments={
                            "query": STATE.org_query,
                            "auth_bearer_token": STATE.auth_bearer_token,
                            "google_access_token": STATE.google_access_token,
                        },
                        on_success=lookup_success_actions(),
                        on_error=lookup_fail_actions(),
                    ),
                ],
            )
            Button(
                "Look Up",
                variant="info",
                css_class=BUTTON_INFO_CLASS,
                disabled=STATE.is_loading,
                on_click=[
                    *start_tool_call("Looking up organization…"),
                    SetState("org_loaded", False),
                    CallTool(
                        lookup_organization,
                        arguments={
                            "query": STATE.org_query,
                            "auth_bearer_token": STATE.auth_bearer_token,
                            "google_access_token": STATE.google_access_token,
                        },
                        on_success=lookup_success_actions(),
                        on_error=lookup_fail_actions(),
                    ),
                ],
            )
        with If(STATE.resolved_org_label), Alert(variant="info", icon="info"):
            Text(content=STATE.resolved_org_label)
        with If(STATE.lookup_error), Alert(variant="warning", icon="triangle-alert"):
            Text(content=STATE.lookup_error)
