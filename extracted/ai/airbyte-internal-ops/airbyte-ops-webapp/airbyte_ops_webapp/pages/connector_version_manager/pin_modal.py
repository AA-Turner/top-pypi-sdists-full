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
    Markdown,
    Row,
    Text,
    Textarea,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import RESULT, STATE

from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
    APPLY_ERROR,
    fail_tool_call,
    finish_tool_call,
    start_tool_call,
)
from airbyte_ops_webapp.pages.connector_version_manager._mcp_tools import apply_override
from airbyte_ops_webapp.theme import (
    AIRBYTE_SECONDARY,
    BUTTON_DESTRUCTIVE_CLASS,
    BUTTON_INFO_CLASS,
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
        Button(
            "Set Pin",
            variant="info",
            css_class=BUTTON_INFO_CLASS,
        )

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
    Input(
        name="context_guid",
        value=STATE.context_guid,
        placeholder="Context GUID: accepts Organization, Workspace, or Actor IDs",
    )
    with Grid(columns=2, gap=3), Column(gap=1):
        Text("Scope Type")
        Text(content=STATE.scope_type)


def _render_justification_section() -> None:
    Markdown("**Justification**")
    Textarea(
        name="override_reason",
        value=STATE.override_reason,
        placeholder="Required justification for set/unset operation",
        rows=3,
    )
    Input(
        name="reference_url",
        value=STATE.reference_url,
        placeholder="GitHub issue URL for audit context",
    )
    Input(
        name="approval_comment_url",
        value=STATE.approval_comment_url,
        placeholder="Slack approval record URL",
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
                        "approval_comment_url": STATE.approval_comment_url,
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
