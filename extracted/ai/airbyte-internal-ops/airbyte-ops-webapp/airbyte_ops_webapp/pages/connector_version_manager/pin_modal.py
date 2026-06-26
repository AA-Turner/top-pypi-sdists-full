"""Pin modal dialog: replaces the old bottom "Configure pin" form."""

from __future__ import annotations

from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import (
    Button,
    Column,
    Dialog,
    Div,
    Grid,
    Input,
    Link,
    Markdown,
    Row,
    Text,
    Textarea,
)
from prefab_ui.components.control_flow import Else, If
from prefab_ui.rx import RESULT, STATE

from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
    APPLY_ERROR,
    fail_tool_call,
    finish_tool_call,
    start_tool_call,
)
from airbyte_ops_webapp.pages.connector_version_manager._mcp_tools import (
    apply_override,
    resolve_scope_guid,
)
from airbyte_ops_webapp.theme import (
    AIRBYTE_SECONDARY,
    BUTTON_DESTRUCTIVE_CLASS,
    CODE_BLOCK_CLASS,
    SUCCESS_CARD_CLASS,
    _card_style,
    _code_surface_style,
)


def render_pin_modal(state: dict[str, object]) -> None:
    """Render the "Set Connector Pin" modal dialog.

    Triggered by a button in the version list or overview pane.
    Contains scope inputs, justification fields, confirmation, and apply.
    """
    with Dialog(
        title="Set Connector Pin",
        description="Configure and apply a connector version override.",
        name="pin_modal_open",
    ):
        Div(style={"display": "none"})

        with Column(gap=4):
            _render_connector_info()
            _render_scope_section()
            _render_justification_section()
            _render_apply_section()
            _render_result_section()


def _render_connector_info() -> None:
    with Grid(columns=2, gap=3):
        with Column(gap=1):
            Markdown("**Connector**")
            Text(content=STATE.selected_connector.name)
        with Column(gap=1):
            Markdown("**Version**")
            Text(content=STATE.target_version)


def _render_scope_section() -> None:
    Markdown("**Scope**")
    with Row(gap=2, align="end"):
        with Column(gap=0, style={"flex": "1"}):
            Input(
                name="context_guid",
                placeholder="Context GUID: accepts Organization, Workspace, or Actor IDs",
            )
        Button(
            "Resolve",
            variant="outline",
            size="sm",
            on_click=[
                SetState("resolved_context_label", ""),
                SetState("scope_type", ""),
                SetState("scope_url", ""),
                SetState("context_error", ""),
                CallTool(
                    resolve_scope_guid,
                    arguments={
                        "connector_id": STATE.selected_connector.id,
                        "context_guid": STATE.context_guid,
                        "auth_bearer_token": STATE.auth_bearer_token,
                    },
                    on_success=[
                        SetState("scope_type", RESULT.scope_type),
                        SetState("scope_id", RESULT.scope_id),
                        SetState("scope_url", RESULT.scope_url),
                        SetState(
                            "resolved_context_label",
                            RESULT.resolved_context_label,
                        ),
                        SetState("context_error", RESULT.context_error),
                        SetState(
                            "actor_workspace_id",
                            RESULT.actor_workspace_id,
                        ),
                    ],
                    on_error=[
                        SetState("context_error", "Scope lookup failed."),
                        *fail_tool_call("Scope lookup failed."),
                    ],
                ),
            ],
        )
    _render_scope_resolution_display()


def _render_scope_resolution_display() -> None:
    """Show resolved scope info or error below the GUID input."""
    with If(STATE.context_error):
        Text(
            content=STATE.context_error,
            style={"color": "#dc2626", "fontSize": "0.85rem"},
        )
    with If(STATE.scope_url):
        Link(
            content=STATE.resolved_context_label,
            href=STATE.scope_url,
            target="_blank",
            style={"fontSize": "0.85rem"},
        )
    with Else(), If(STATE.resolved_context_label):
        Text(
            content=STATE.resolved_context_label,
            style={"fontSize": "0.85rem", "color": "#6b7280"},
        )


def _render_justification_section() -> None:
    Markdown("**Justification**")
    Textarea(
        name="override_reason",
        value=STATE.override_reason,
        placeholder="Required justification for set/unset operation",
        rows=3,
    )
    Text("Related PR/Issue URL", style={"fontSize": "0.85rem", "fontWeight": "500"})
    Input(
        name="reference_url",
        value=STATE.reference_url,
        placeholder="GitHub issue URL for audit context",
    )


def _render_apply_section() -> None:
    """Confirmation + Apply button."""
    with Row(justify="end", gap=2):
        Button(
            "Apply Pin Change",
            variant="destructive",
            css_class=BUTTON_DESTRUCTIVE_CLASS,
            disabled=STATE.is_loading,
            on_click=[
                *start_tool_call("Applying change…"),
                CallTool(
                    apply_override,
                    arguments={
                        "connector_id": STATE.selected_connector.id,
                        "connector_name": STATE.selected_connector.name,
                        "connector_type": (STATE.selected_connector.connector_type),
                        "scope_type": STATE.scope_type,
                        "scope_id": STATE.scope_id,
                        "actor_workspace_id": STATE.actor_workspace_id,
                        "action": "set",
                        "version": STATE.target_version,
                        "override_reason": STATE.override_reason,
                        "reference_url": STATE.reference_url,
                        "user_email": STATE.oauth_user_email,
                        "auth_bearer_token": STATE.auth_bearer_token,
                        "customer_tier_filter": STATE.customer_tier_filter,
                        "force": False,
                    },
                    on_success=[
                        *finish_tool_call(),
                        SetState("apply_result_json", RESULT.apply_result_json),
                        SetState("apply_message", RESULT.apply_message),
                        SetState("apply_success", RESULT.apply_success),
                    ],
                    on_error=fail_tool_call(APPLY_ERROR),
                ),
            ],
        )


def _render_result_section() -> None:
    with (
        If(STATE.apply_message),
        Div(
            css_class=SUCCESS_CARD_CLASS,
            style=_card_style(accent=AIRBYTE_SECONDARY),
        ),
        Column(gap=2),
    ):
        Markdown(STATE.apply_message)
        with Div(style=_code_surface_style()):
            Text(STATE.apply_result_json, css_class=CODE_BLOCK_CLASS)
