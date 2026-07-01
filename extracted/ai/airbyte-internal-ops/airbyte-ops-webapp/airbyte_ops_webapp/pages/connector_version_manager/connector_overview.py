"""Connector Status section and rollout action confirmation modals."""

# ruff: noqa: SIM117

from __future__ import annotations

from prefab_ui.actions import Fetch, SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import (
    H2,
    H3,
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
from prefab_ui.rx import RESULT, STATE

from airbyte_ops_webapp.auth.oauth import OAUTH_SESSION_PATH
from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
    fail_tool_call,
    rollout_action_success_actions,
    start_tool_call,
)
from airbyte_ops_webapp.pages.connector_version_manager._mcp_tools import (
    advance_rollout,
    finalize_rollout,
    promote_to_next_stage,
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


def _refresh_token_then(on_success: list) -> Fetch:
    """Fetch a fresh OAuth token, then execute chained actions on success."""
    return Fetch.get(
        OAUTH_SESSION_PATH,
        on_success=[
            SetState("auth_bearer_token", RESULT.auth_bearer_token),
            SetState("oauth_user_email", RESULT.oauth_user_email),
            *on_success,
        ],
        on_error=fail_tool_call(
            "Session expired. Please sign in again to perform this action."
        ),
    )


def render_rollout_status_section() -> None:
    """Connector Version Status section (1/3 width, pivoted key-value layout).

    Shows connector name, UUID, version comparison, and rollout status
    with labels on the left and values on the right.
    """
    with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
        with CardHeader():
            H2("Connector Version Status", css_class="text-lg")
        with CardContent(), Column(gap=3):
            # Loading state while connector context is being fetched
            with If(STATE.context_loading.__eq__(True)):
                Muted("Loading connector status…")

            # Populated state
            with If(STATE.context_loading.__eq__(False)):
                _render_connector_identity_rows()
                _render_version_comparison_rows()

                # Case A: No active rollouts
                with If(STATE.active_rollouts.length().__eq__(0)):
                    Muted("No progressive rollouts active.")

                # Case B: Active rollout exists — show consolidated view
                with If(STATE.active_rollouts.length()):
                    _render_active_rollout_detail()

    # Rollout confirmation modal (shared for all actions)
    _render_rollout_confirmation_modal()


def _pivoted_row(label: str, value: object) -> None:
    """Render a single label-value row for the pivoted connector status layout."""
    with Row(justify="between", align="baseline", gap=2):
        Span(label, style=_OVERVIEW_LABEL_STYLE)
        Text(content=value, style={"fontSize": "0.85rem", "textAlign": "right"})


def _render_connector_identity_rows() -> None:
    """Pivoted rows for connector name and UUID."""
    _pivoted_row("Connector", STATE.selected_connector.name)
    with Row(justify="between", align="baseline", gap=2):
        Span("Connector ID", style=_OVERVIEW_LABEL_STYLE)
        Muted(
            content=STATE.selected_connector.id,
            style={
                "fontSize": "0.75rem",
                "textAlign": "right",
                "wordBreak": "break-all",
            },
        )


def _render_version_comparison_rows() -> None:
    """Pivoted rows comparing selected version against the default version."""
    _pivoted_row("Selected Version", STATE.selected_version_tag)
    _pivoted_row("Selected Version Release Date", STATE.selected_version_release_date)
    _pivoted_row("Default Version", STATE.selected_connector.latest_version)
    _pivoted_row("Default Version Release Date", STATE.latest_version_release_date)


def _render_active_rollout_detail() -> None:
    """Consolidated rollout detail from `STATE.rollout_summary`."""
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
        H3("Rollout Status", css_class="text-sm mb-1")
        _pivoted_row("RC", STATE.rollout_summary.rc_version)
        _pivoted_row("Tiers", STATE.rollout_summary.tier_summary)
        _pivoted_row("Autopilot", STATE.rollout_summary.autopilot)
        _pivoted_row("Updated", STATE.rollout_summary.updated_at)
        _pivoted_row("Pins on RC", STATE.rollout_summary.total_rc_pins)

        # Action buttons
        _render_rollout_action_buttons()


def _render_rollout_action_buttons() -> None:
    """Advance Rollout %, Promote to Next Stage, Promote to Default GA, Cancel."""
    with Column(gap=2, css_class="mt-2"):
        # Row 1: Advance and Cancel
        with Row(gap=2, css_class="flex-wrap"):
            Button(
                "Advance Rollout %",
                variant="info",
                css_class=BUTTON_INFO_CLASS,
                disabled=STATE.is_loading,
                on_click=[
                    SetState("rollout_action", "advance"),
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
                    SetState("rollout_modal_open", True),
                ],
            )

        # Row 2: Promote to Next Stage and Promote to Default GA
        with Row(gap=2, css_class="flex-wrap"):
            Button(
                "Promote to Next Stage",
                variant="outline",
                css_class=BUTTON_OUTLINE_CLASS,
                disabled=STATE.is_loading.__or__(
                    STATE.rollout_summary.has_next_stage.__eq__(False)
                ),
                on_click=[
                    SetState("rollout_action", "promote_next_stage"),
                    SetState("rollout_modal_open", True),
                ],
            )
            Button(
                "Promote to Default GA",
                variant="outline",
                css_class=BUTTON_OUTLINE_CLASS,
                disabled=STATE.is_loading,
                on_click=[
                    SetState("rollout_action", "promote_ga"),
                    SetState("rollout_modal_open", True),
                ],
            )


# ---------------------------------------------------------------------------
# Confirmation modals
# ---------------------------------------------------------------------------


def _render_rollout_confirmation_modal() -> None:
    """Confirmation dialog for rollout actions."""
    with Dialog(
        title="Confirm Rollout Action",
        description="Please confirm the rollout action below.",
        name="rollout_modal_open",
    ):
        Button("", css_class="hidden")

        # --- Advance Rollout % ---
        with If(STATE.rollout_action.__eq__("advance")):
            with Column(gap=4):
                Markdown(
                    content="**Advance rollout percentage?**\n\n"
                    "RC: "
                    + STATE.rollout_summary.rc_docker_image_tag
                    + " — Current tier: "
                    + STATE.rollout_summary.advance_tier
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
                            _refresh_token_then(
                                [
                                    CallTool(
                                        advance_rollout,
                                        arguments={
                                            "rollout_id": STATE.rollout_summary.advance_rollout_id,
                                            "connector_id": STATE.rollout_summary.connector_id,
                                            "docker_repository": STATE.rollout_summary.docker_repository,
                                            "docker_image_tag": STATE.rollout_summary.rc_docker_image_tag,
                                            "target_percentage": STATE.rollout_target_percentage,
                                            "auth_bearer_token": STATE.auth_bearer_token,
                                            "user_email": STATE.oauth_user_email,
                                        },
                                        on_success=rollout_action_success_actions(),
                                        on_error=fail_tool_call(
                                            "Advance rollout failed."
                                        ),
                                    ),
                                ]
                            ),
                        ],
                    )

        # --- Promote to Next Stage ---
        with If(STATE.rollout_action.__eq__("promote_next_stage")):
            with Column(gap=4):
                Markdown(
                    content="**Promote to next stage?**\n\n"
                    "This will start a new rollout at the next tier for "
                    + STATE.rollout_summary.rc_docker_image_tag
                    + "."
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
                            *start_tool_call("Promoting to next stage…"),
                            _refresh_token_then(
                                [
                                    CallTool(
                                        promote_to_next_stage,
                                        arguments={
                                            "connector_id": STATE.rollout_summary.connector_id,
                                            "docker_repository": STATE.rollout_summary.docker_repository,
                                            "docker_image_tag": STATE.rollout_summary.rc_docker_image_tag,
                                            "next_tier": STATE.rollout_summary.next_tier,
                                            "auth_bearer_token": STATE.auth_bearer_token,
                                            "user_email": STATE.oauth_user_email,
                                        },
                                        on_success=rollout_action_success_actions(),
                                        on_error=fail_tool_call(
                                            "Promote to next stage failed."
                                        ),
                                    ),
                                ]
                            ),
                        ],
                    )

        # --- Promote to Default GA ---
        with If(STATE.rollout_action.__eq__("promote_ga")):
            with Column(gap=4):
                Markdown(
                    content="**Promote RC to GA?**\n\n"
                    "This will make "
                    + STATE.rollout_summary.rc_docker_image_tag
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
                            *start_tool_call("Promoting rollout to GA…"),
                            _refresh_token_then(
                                [
                                    CallTool(
                                        finalize_rollout,
                                        arguments={
                                            "rollout_id": STATE.rollout_summary.promote_rollout_id,
                                            "connector_id": STATE.rollout_summary.connector_id,
                                            "docker_repository": STATE.rollout_summary.docker_repository,
                                            "docker_image_tag": STATE.rollout_summary.rc_docker_image_tag,
                                            "state": "succeeded",
                                            "auth_bearer_token": STATE.auth_bearer_token,
                                            "user_email": STATE.oauth_user_email,
                                        },
                                        on_success=rollout_action_success_actions(),
                                        on_error=fail_tool_call(
                                            "Promote rollout failed."
                                        ),
                                    ),
                                ]
                            ),
                        ],
                    )

        # --- Cancel Rollout ---
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
                            _refresh_token_then(
                                [
                                    CallTool(
                                        finalize_rollout,
                                        arguments={
                                            "rollout_id": STATE.rollout_summary.promote_rollout_id,
                                            "connector_id": STATE.rollout_summary.connector_id,
                                            "docker_repository": STATE.rollout_summary.docker_repository,
                                            "docker_image_tag": STATE.rollout_summary.rc_docker_image_tag,
                                            "state": "canceled",
                                            "auth_bearer_token": STATE.auth_bearer_token,
                                            "user_email": STATE.oauth_user_email,
                                        },
                                        on_success=rollout_action_success_actions(),
                                        on_error=fail_tool_call(
                                            "Cancel rollout failed."
                                        ),
                                    ),
                                ]
                            ),
                        ],
                    )
