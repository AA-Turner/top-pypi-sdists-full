"""Connector Status section and rollout action confirmation modals."""

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
    Dialog,
    Div,
    Input,
    Markdown,
    Muted,
    Row,
    Span,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
    fail_tool_call,
    rollout_action_success_actions,
    start_tool_call,
)
from airbyte_ops_webapp.pages.connector_version_manager._mcp_tools import (
    advance_rollout,
    finalize_rollout,
)
from airbyte_ops_webapp.theme import (
    BUTTON_DESTRUCTIVE_CLASS,
    BUTTON_INFO_CLASS,
    BUTTON_OUTLINE_CLASS,
    PANEL_CARD_CLASS,
    _card_style,
)

_OVERVIEW_LABEL_STYLE: dict[str, str] = {
    "display": "block",
    "fontSize": "0.7rem",
    "fontWeight": "600",
    "color": "#9ca3af",
    "textTransform": "uppercase",
    "letterSpacing": "0.03em",
}


def _select_active_rollout() -> SetState:
    """Build a `SetState` that snapshots `active_rollouts[0]` into `selected_rollout`."""
    return SetState(
        "selected_rollout",
        {
            "rollout_id": STATE.active_rollouts[0].rollout_id,
            "connector_id": STATE.active_rollouts[0].connector_id,
            "connector_name": STATE.active_rollouts[0].connector_name,
            "connector_type": STATE.active_rollouts[0].connector_type,
            "docker_repository": STATE.active_rollouts[0].docker_repository,
            "state": STATE.active_rollouts[0].state,
            "rc_docker_image_tag": STATE.active_rollouts[0].rc_docker_image_tag,
            "initial_docker_image_tag": STATE.active_rollouts[
                0
            ].initial_docker_image_tag,
            "current_target_rollout_pct": STATE.active_rollouts[
                0
            ].current_target_rollout_pct,
            "final_target_rollout_pct": STATE.active_rollouts[
                0
            ].final_target_rollout_pct,
            "created_at": STATE.active_rollouts[0].created_at,
            "updated_at": STATE.active_rollouts[0].updated_at,
        },
    )


def render_rollout_status_section() -> None:
    """Connector Status section (1/3 width, pivoted key-value layout).

    Shows connector name, UUID, and rollout status with labels on the
    left and values on the right.
    """
    with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
        with CardHeader():
            H2("Connector Status", css_class="text-lg")
        with CardContent(), Column(gap=3):
            # Loading state while connector context is being fetched
            with If(STATE.context_loading.__eq__(True)):
                Muted("Loading connector status…")

            # Populated state
            with If(STATE.context_loading.__eq__(False)):
                _render_connector_identity_rows()

                # Case A: No active rollouts
                with If(STATE.active_rollouts.length().__eq__(0)):
                    Muted("No progressive rollouts active.")

                # Case B: Active rollout exists
                with If(STATE.active_rollouts.length()):
                    _render_active_rollout_detail()


def _pivoted_row(label: str, value: object) -> None:
    """Render a single label-value row for the pivoted connector status layout."""
    with Row(justify="between", align="baseline", gap=2):
        Span(label, style=_OVERVIEW_LABEL_STYLE)
        Text(content=value, style={"fontSize": "0.85rem", "textAlign": "right"})


def _render_connector_identity_rows() -> None:
    """Pivoted rows for connector name and UUID."""
    _pivoted_row("Connector", STATE.selected_connector.name)
    with Row(justify="between", align="baseline", gap=2):
        Span("ID", style=_OVERVIEW_LABEL_STYLE)
        Muted(
            content=STATE.selected_connector.id,
            style={
                "fontSize": "0.75rem",
                "textAlign": "right",
                "wordBreak": "break-all",
            },
        )


def _render_active_rollout_detail() -> None:
    """Pivoted detail rows for the first active rollout."""
    with (
        Div(
            style={
                "padding": "0.75rem",
                "borderRadius": "0.375rem",
                "border": "1px solid rgba(255,255,255,0.1)",
            }
        ),
        Column(gap=0),
    ):
        _pivoted_row("State", STATE.active_rollouts[0].state)
        _pivoted_row("RC", STATE.active_rollouts[0].rc_docker_image_tag)
        _pivoted_row("Autopilot", STATE.active_rollouts[0].autopilot_display)
        _pivoted_row("Updated", STATE.active_rollouts[0].updated_at_display)
        _pivoted_row("Pins on RC", STATE.active_rollouts[0].rc_pin_count_display)

        # Action buttons (only for actionable states)
        _render_rollout_action_buttons()

    # Rollout confirmation modal (shared for advance/promote/cancel)
    _render_advance_confirmation_modal()


def _render_rollout_action_buttons() -> None:
    """Advance, Promote, and Cancel action buttons."""
    with Row(gap=2, css_class="mt-2"):
        Button(
            "Advance Rollout",
            variant="info",
            css_class=BUTTON_INFO_CLASS,
            disabled=STATE.is_loading,
            on_click=[
                SetState("rollout_action", "advance"),
                _select_active_rollout(),
                SetState("rollout_modal_open", True),
            ],
        )
        Button(
            "Promote to GA",
            variant="outline",
            css_class=BUTTON_OUTLINE_CLASS,
            disabled=STATE.is_loading,
            on_click=[
                SetState("rollout_action", "promote"),
                _select_active_rollout(),
                SetState("rollout_modal_open", True),
            ],
        )
        Button(
            "Cancel Rollout",
            variant="destructive",
            css_class=BUTTON_DESTRUCTIVE_CLASS,
            disabled=STATE.is_loading,
            on_click=[
                SetState("rollout_action", "cancel"),
                _select_active_rollout(),
                SetState("rollout_modal_open", True),
            ],
        )


# ---------------------------------------------------------------------------
# Confirmation modals
# ---------------------------------------------------------------------------


def _render_advance_confirmation_modal() -> None:
    """Confirmation dialog for rollout actions (advance, promote, cancel)."""
    with Dialog(
        title="Confirm Rollout Action",
        description="Please confirm the rollout action below.",
        name="rollout_modal_open",
    ):
        Button("", css_class="hidden")

        with If(STATE.rollout_action.__eq__("advance")):
            with Column(gap=4):
                Markdown(
                    content="**Advance rollout to next stage?**\n\n"
                    "RC: " + STATE.selected_rollout.rc_docker_image_tag
                )
                with Column(gap=1):
                    Markdown("**Target Percentage** (leave blank to auto-increment)")
                    Input(
                        name="rollout_target_percentage",
                        value=STATE.rollout_target_percentage,
                        placeholder="e.g. 50",
                    )
                with Row(justify="end", gap=2):
                    Button(
                        "Cancel",
                        variant="outline",
                        css_class=BUTTON_OUTLINE_CLASS,
                        on_click=[SetState("rollout_modal_open", False)],
                    )
                    Button(
                        "Confirm",
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

        with If(STATE.rollout_action.__eq__("promote")):
            with Column(gap=4):
                Markdown(
                    content="**Promote RC to GA?**\n\n"
                    "This will make "
                    + STATE.selected_rollout.rc_docker_image_tag
                    + " the new default version for all users."
                )
                with Row(justify="end", gap=2):
                    Button(
                        "Cancel",
                        variant="outline",
                        css_class=BUTTON_OUTLINE_CLASS,
                        on_click=[SetState("rollout_modal_open", False)],
                    )
                    Button(
                        "Confirm",
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

        with If(STATE.rollout_action.__eq__("cancel")):
            with Column(gap=4):
                Markdown(
                    content="**Cancel rollout?**\n\n"
                    "This will stop the progressive rollout and "
                    "roll back affected users."
                )
                with Row(justify="end", gap=2):
                    Button(
                        "Cancel",
                        variant="outline",
                        css_class=BUTTON_OUTLINE_CLASS,
                        on_click=[SetState("rollout_modal_open", False)],
                    )
                    Button(
                        "Confirm",
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
