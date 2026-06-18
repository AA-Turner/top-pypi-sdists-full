"""Connector overview pane: rollout status, pin status, context input, and pin modal."""

# ruff: noqa: SIM117

from __future__ import annotations

from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import (
    H2,
    Button,
    CardContent,
    CardHeader,
    Column,
    DataTable,
    DataTableColumn,
    Dialog,
    Div,
    Grid,
    Input,
    Markdown,
    Muted,
    Row,
    Small,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import EVENT, STATE

from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
    fail_tool_call,
    rollout_action_success_actions,
    start_tool_call,
)
from airbyte_ops_webapp.pages.connector_version_manager._mcp_tools import (
    advance_rollout,
    finalize_rollout,
)
from airbyte_ops_webapp.pages.connector_version_manager.pin_modal import (
    render_pin_modal,
)
from airbyte_ops_webapp.theme import (
    BUTTON_DESTRUCTIVE_CLASS,
    BUTTON_INFO_CLASS,
    BUTTON_OUTLINE_CLASS,
    PANEL_CARD_CLASS,
    STATUS_CARD_CLASS,
    _card_style,
)


def render_status_bar() -> None:
    """Compact status bar showing connector name, latest version, and docker repo."""
    with Grid(columns=3, gap=4):
        with (
            Div(css_class=STATUS_CARD_CLASS, style=_card_style()),
            CardContent(),
            Column(gap=1),
        ):
            Small("Selected connector")
            Text(
                content=STATE.selected_connector.name,
                css_class="airbyte-stat-value",
            )
            Text(content=STATE.selected_connector.id)
        with (
            Div(css_class=STATUS_CARD_CLASS, style=_card_style()),
            CardContent(),
            Column(gap=1),
        ):
            Small("Latest version")
            Text(
                content=STATE.selected_connector.latest_version,
                css_class="airbyte-stat-value",
            )
            Muted("Registry latest")
        with (
            Div(css_class=STATUS_CARD_CLASS, style=_card_style()),
            CardContent(),
            Column(gap=1),
        ):
            Small("Docker repository")
            Text(
                content=STATE.selected_connector.docker_repository,
                css_class="airbyte-stat-value",
            )
            Text(content=STATE.selected_connector.connector_type)


def render_connector_overview(state: dict[str, object]) -> None:
    """Right-pane: version status, rollout info, and pin modal."""
    with Column(gap=4):
        _render_version_status_panel()
        _render_rollout_panel()
        render_pin_modal(state)


def _render_version_status_panel() -> None:
    """Reactive panel showing status for the selected version."""
    with If(STATE.selected_version_tag):
        with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
            with CardHeader():
                H2("Version Status")
            with CardContent(), Column(gap=2):
                Text(
                    content=STATE.selected_version_tag,
                    css_class="airbyte-stat-value",
                )
                with If(
                    STATE.selected_version_tag.__eq__(
                        STATE.selected_connector.latest_version
                    )
                ):
                    with Row(gap=1, align="center"):
                        Text("✓")
                        Text("GA (Default) — current latest version")
                    with Row(gap=1):
                        Small("Pins:")
                        Text(content=STATE.version_pins_total.number())
                with If(
                    STATE.selected_version_tag.__ne__(
                        STATE.selected_connector.latest_version
                    )
                ):
                    with Row(gap=1, align="center"):
                        Text("◇")
                        Text("Previous version")
                    with Row(gap=1):
                        Small("Pins:")
                        Text(content=STATE.version_pins_total.number())


def _render_rollout_panel() -> None:
    """Standalone panel for active rollout status."""
    with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
        with CardHeader():
            H2("Rollout Status")
        with CardContent():
            _render_rollout_summary()


def _render_rollout_summary() -> None:
    """Active rollout status summary."""
    with If(STATE.rollout_error):
        Muted(content=STATE.rollout_error)
    with If(STATE.active_rollouts):
        DataTable(
            columns=[
                DataTableColumn(key="state", header="State"),
                DataTableColumn(key="rc_docker_image_tag", header="RC"),
                DataTableColumn(key="initial_docker_image_tag", header="Initial"),
                DataTableColumn(key="updated_at_display", header="Updated"),
            ],
            rows=STATE.active_rollouts,
            pageSize=5,
            on_row_click=[
                SetState(
                    "selected_rollout",
                    {
                        "rollout_id": EVENT.rollout_id,
                        "connector_id": EVENT.connector_id,
                        "connector_name": EVENT.connector_name,
                        "connector_type": EVENT.connector_type,
                        "docker_repository": EVENT.docker_repository,
                        "state": EVENT.state,
                        "rc_docker_image_tag": EVENT.rc_docker_image_tag,
                        "initial_docker_image_tag": EVENT.initial_docker_image_tag,
                        "current_target_rollout_pct": EVENT.current_target_rollout_pct,
                        "final_target_rollout_pct": EVENT.final_target_rollout_pct,
                        "created_at": EVENT.created_at,
                        "updated_at": EVENT.updated_at,
                    },
                ),
                SetState("rollout_action_result", ""),
                SetState("rollout_action_success", False),
            ],
        )
        _render_rollout_actions()
        _render_rollout_modal()


def _render_rollout_actions() -> None:
    """Contextual action buttons for the selected rollout."""
    with If(STATE.selected_rollout.rollout_id):
        with Column(gap=2, style={"marginTop": "0.75rem"}):
            with Row(gap=1, align="center"):
                Small("Selected:")
                Text(
                    content=STATE.selected_rollout.rc_docker_image_tag
                    + " — "
                    + STATE.selected_rollout.state,
                )
            # Only show buttons when rollout is in an actionable state
            with If(
                STATE.selected_rollout.state.__ne__("succeeded")
                .__and__(STATE.selected_rollout.state.__ne__("failed_rolled_back"))
                .__and__(STATE.selected_rollout.state.__ne__("canceled"))
                .__and__(STATE.selected_rollout.state.__ne__("finalizing"))
                .__and__(STATE.selected_rollout.state.__ne__("errored"))
            ):
                with Row(gap=2):
                    Button(
                        "Advance",
                        variant="info",
                        css_class=BUTTON_INFO_CLASS,
                        disabled=STATE.is_loading,
                        on_click=[
                            SetState("rollout_action", "advance"),
                            SetState("rollout_modal_open", True),
                        ],
                    )
                    Button(
                        "Promote",
                        variant="outline",
                        css_class=BUTTON_OUTLINE_CLASS,
                        disabled=STATE.is_loading,
                        on_click=[
                            SetState("rollout_action", "promote"),
                            SetState("rollout_modal_open", True),
                        ],
                    )
                    Button(
                        "Cancel / Rollback",
                        variant="destructive",
                        css_class=BUTTON_DESTRUCTIVE_CLASS,
                        disabled=STATE.is_loading,
                        on_click=[
                            SetState("rollout_action", "cancel"),
                            SetState("rollout_modal_open", True),
                        ],
                    )


def _render_rollout_modal() -> None:
    """Confirmation modal for rollout actions."""
    with Dialog(
        title="Confirm Rollout Action",
        description="Review and confirm the rollout operation.",
        name="rollout_modal_open",
    ):
        # Hidden trigger — the dialog is opened via state, not a trigger button
        Button("", css_class="hidden")

        with Column(gap=4):
            _render_rollout_modal_info()
            _render_rollout_modal_advance_input()
            _render_rollout_modal_actions()
            _render_rollout_modal_result()


def _render_rollout_modal_info() -> None:
    """Show details about the rollout being acted on."""
    with Grid(columns=2, gap=3):
        with Column(gap=1):
            Markdown("**Connector**")
            Text(content=STATE.selected_rollout.connector_name)
        with Column(gap=1):
            Markdown("**RC Version**")
            Text(content=STATE.selected_rollout.rc_docker_image_tag)
    with Grid(columns=2, gap=3):
        with Column(gap=1):
            Markdown("**Current State**")
            Text(content=STATE.selected_rollout.state)
        with Column(gap=1):
            Markdown("**Current %**")
            Text(content=STATE.selected_rollout.current_target_rollout_pct)
    with Row(gap=1):
        Markdown("**Action:**")
        Text(content=STATE.rollout_action)


def _render_rollout_modal_advance_input() -> None:
    """Target percentage input shown only for advance action."""
    with If(STATE.rollout_action.__eq__("advance")):
        with Column(gap=1):
            Markdown("**Target Percentage** (leave blank to auto-increment)")
            Input(
                name="rollout_target_percentage",
                value=STATE.rollout_target_percentage,
                placeholder="e.g. 50",
            )


def _render_rollout_modal_actions() -> None:
    """Apply buttons inside the modal."""
    with Row(justify="end", gap=2):
        # Advance button
        with If(STATE.rollout_action.__eq__("advance")):
            Button(
                "Confirm Advance",
                variant="info",
                css_class=BUTTON_INFO_CLASS,
                disabled=STATE.is_loading,
                on_click=[
                    SetState("rollout_modal_open", False),
                    *start_tool_call("Advancing rollout…"),
                    CallTool(
                        advance_rollout,
                        arguments={
                            "rollout_id": STATE.selected_rollout.rollout_id,
                            "connector_id": STATE.selected_rollout.connector_id,
                            "docker_repository": STATE.selected_rollout.docker_repository,
                            "docker_image_tag": STATE.selected_rollout.rc_docker_image_tag,
                            "target_percentage": STATE.rollout_target_percentage,
                            "auth_bearer_token": STATE.auth_bearer_token,
                            "user_email": STATE.oauth_user_email,
                        },
                        on_success=rollout_action_success_actions(),
                        on_error=fail_tool_call("Advance rollout failed."),
                    ),
                ],
            )
        # Promote button
        with If(STATE.rollout_action.__eq__("promote")):
            Button(
                "Confirm Promote",
                variant="info",
                css_class=BUTTON_INFO_CLASS,
                disabled=STATE.is_loading,
                on_click=[
                    SetState("rollout_modal_open", False),
                    *start_tool_call("Promoting rollout…"),
                    CallTool(
                        finalize_rollout,
                        arguments={
                            "rollout_id": STATE.selected_rollout.rollout_id,
                            "connector_id": STATE.selected_rollout.connector_id,
                            "docker_repository": STATE.selected_rollout.docker_repository,
                            "docker_image_tag": STATE.selected_rollout.rc_docker_image_tag,
                            "state": "succeeded",
                            "auth_bearer_token": STATE.auth_bearer_token,
                            "user_email": STATE.oauth_user_email,
                        },
                        on_success=rollout_action_success_actions(),
                        on_error=fail_tool_call("Promote rollout failed."),
                    ),
                ],
            )
        # Cancel/Rollback button
        with If(STATE.rollout_action.__eq__("cancel")):
            Button(
                "Confirm Cancel / Rollback",
                variant="destructive",
                css_class=BUTTON_DESTRUCTIVE_CLASS,
                disabled=STATE.is_loading,
                on_click=[
                    SetState("rollout_modal_open", False),
                    *start_tool_call("Canceling rollout…"),
                    CallTool(
                        finalize_rollout,
                        arguments={
                            "rollout_id": STATE.selected_rollout.rollout_id,
                            "connector_id": STATE.selected_rollout.connector_id,
                            "docker_repository": STATE.selected_rollout.docker_repository,
                            "docker_image_tag": STATE.selected_rollout.rc_docker_image_tag,
                            "state": "canceled",
                            "auth_bearer_token": STATE.auth_bearer_token,
                            "user_email": STATE.oauth_user_email,
                        },
                        on_success=rollout_action_success_actions(),
                        on_error=fail_tool_call("Cancel rollout failed."),
                    ),
                ],
            )


def _render_rollout_modal_result() -> None:
    """Result message after a rollout action."""
    with If(STATE.rollout_action_result):
        Markdown(content=STATE.rollout_action_result)
