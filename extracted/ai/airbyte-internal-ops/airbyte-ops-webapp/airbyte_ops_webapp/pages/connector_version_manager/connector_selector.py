"""Connector selector with tabbed search (All / Recent Releases / Rollouts)."""

from __future__ import annotations

from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import (
    H2,
    CardContent,
    CardHeader,
    Combobox,
    Div,
    Tab,
    Tabs,
)
from prefab_ui.rx import EVENT, RESULT, STATE

from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
    context_success_actions,
    fail_context_actions,
    render_combobox_options,
    start_tool_call,
)
from airbyte_ops_webapp.pages.connector_version_manager._mcp_tools import (
    load_connector_context,
    load_progressive_rollout_context,
    load_recent_release_context,
)
from airbyte_ops_webapp.theme import COMBOBOX_CLASS, PANEL_CARD_CLASS, _card_style


def render_connector_selector(state: dict[str, object]) -> None:
    """Render the connector selector card with three tabbed comboboxes."""
    with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
        with CardHeader():
            H2("Select a Connector")
        with (
            CardContent(),
            Tabs(
                name="selector_tab",
                value=state["selector_tab"],
                variant="line",
            ),
        ):
            with Tab("All Connectors", value="all-connectors"):
                _render_all_connectors_combobox(state)
            with Tab("Recent Releases", value="recent-releases"):
                _render_recent_releases_combobox(state)
            with Tab("Progressive Rollouts", value="progressive-rollouts"):
                _render_progressive_rollouts_combobox(state)


def _render_all_connectors_combobox(state: dict[str, object]) -> None:
    with Combobox(
        name="selected_connector_id",
        value=state["selected_connector_id"],
        placeholder="Search connector name, ID, or Docker repo",
        css_class=COMBOBOX_CLASS,
        searchPlaceholder="Type source-github, destination-snowflake, etc.",
        onChange=[
            SetState("selected_connector_id", EVENT),
            SetState("recent_release_value", ""),
            SetState("progressive_rollout_value", ""),
            *start_tool_call("Loading connector context…"),
            CallTool(
                load_connector_context,
                arguments={
                    "connector_id": EVENT,
                    "scope_type": STATE.scope_type,
                    "scope_id": STATE.scope_id,
                    "actor_workspace_id": STATE.actor_workspace_id,
                    "context_guid": STATE.context_guid,
                    "auth_bearer_token": STATE.auth_bearer_token,
                },
                on_success=[*context_success_actions()],
                on_error=fail_context_actions(),
            ),
        ],
    ):
        render_combobox_options(state["connector_options"])


def _render_recent_releases_combobox(state: dict[str, object]) -> None:
    with Combobox(
        name="recent_release_value",
        value=state["recent_release_value"],
        placeholder="Choose a recently published release",
        css_class=COMBOBOX_CLASS,
        searchPlaceholder="Type connector or version",
        onChange=[
            SetState("recent_release_value", EVENT),
            SetState("progressive_rollout_value", ""),
            *start_tool_call("Loading recent release context…"),
            CallTool(
                load_recent_release_context,
                arguments={
                    "release_value": EVENT,
                    "scope_type": STATE.scope_type,
                    "scope_id": STATE.scope_id,
                    "actor_workspace_id": STATE.actor_workspace_id,
                    "context_guid": STATE.context_guid,
                    "auth_bearer_token": STATE.auth_bearer_token,
                },
                on_success=[
                    *context_success_actions(),
                    SetState("selected_connector_id", RESULT.selected_connector_id),
                    SetState("target_version", RESULT.target_version),
                ],
                on_error=fail_context_actions(),
            ),
        ],
    ):
        render_combobox_options(state["recent_release_options"])


def _render_progressive_rollouts_combobox(state: dict[str, object]) -> None:
    with Combobox(
        name="progressive_rollout_value",
        value=state["progressive_rollout_value"],
        placeholder="Choose an active rollout",
        css_class=COMBOBOX_CLASS,
        searchPlaceholder="Type connector, version, or state",
        onChange=[
            SetState("progressive_rollout_value", EVENT),
            SetState("recent_release_value", ""),
            *start_tool_call("Loading progressive rollout context…"),
            CallTool(
                load_progressive_rollout_context,
                arguments={
                    "rollout_value": EVENT,
                    "scope_type": STATE.scope_type,
                    "scope_id": STATE.scope_id,
                    "actor_workspace_id": STATE.actor_workspace_id,
                    "context_guid": STATE.context_guid,
                    "auth_bearer_token": STATE.auth_bearer_token,
                },
                on_success=[
                    *context_success_actions(),
                    SetState("selected_connector_id", RESULT.selected_connector_id),
                    SetState("target_version", RESULT.target_version),
                ],
                on_error=fail_context_actions(),
            ),
        ],
    ):
        render_combobox_options(state["progressive_rollout_options"])
