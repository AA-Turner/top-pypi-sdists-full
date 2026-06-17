"""Connector overview pane: rollout status, pin status, context input, and pin modal."""

# ruff: noqa: SIM117

from __future__ import annotations

from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import (
    H2,
    Button,
    CardContent,
    CardHeader,
    Column,
    DataTable,
    DataTableColumn,
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
from prefab_ui.rx import STATE

from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
    context_error_toast_actions,
    context_success_actions,
    fail_context_actions,
    start_tool_call,
)
from airbyte_ops_webapp.pages.connector_version_manager._mcp_tools import (
    load_connector_context,
    search_orgs_workspaces,
)
from airbyte_ops_webapp.pages.connector_version_manager.pin_modal import (
    render_pin_modal,
)
from airbyte_ops_webapp.pages.shared_components.org_lookup_modal import (
    render_org_lookup_modal,
)
from airbyte_ops_webapp.theme import (
    BUTTON_INFO_CLASS,
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
    """Right-pane: version status, rollout info, and pin context."""
    with Column(gap=4):
        _render_version_status_panel()
        _render_rollout_panel()
        _render_pin_panel(state)


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


def _render_pin_panel(state: dict[str, object]) -> None:
    """Standalone panel for connector pin status, context lookup, and pin modal."""
    with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
        with CardHeader():
            H2("Connector Pins")
        with CardContent(), Column(gap=4):
            _render_context_input()
            _render_pin_context_and_versions()
            _render_pin_tables()
            render_pin_modal(state)


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
        )


def _render_context_input() -> None:
    """Context GUID input with refresh and org search buttons."""
    with Row(gap=2, align="end"):
        Input(
            name="context_guid",
            value=STATE.context_guid,
            placeholder="Context GUID: accepts Organization, Workspace, or Actor IDs",
            style={"flex": "1"},
        )
        render_org_lookup_modal(
            search_tool=search_orgs_workspaces,
            target_state_key="context_guid",
            on_select_actions=[
                *start_tool_call("Refreshing connector context…"),
                CallTool(
                    load_connector_context,
                    arguments={
                        "connector_id": STATE.selected_connector_id,
                        "scope_type": STATE.scope_type,
                        "scope_id": STATE.scope_id,
                        "actor_workspace_id": STATE.actor_workspace_id,
                        "context_guid": STATE.context_guid,
                        "auth_bearer_token": STATE.auth_bearer_token,
                    },
                    on_success=[
                        *context_success_actions(),
                        *context_error_toast_actions(),
                    ],
                    on_error=fail_context_actions(),
                ),
            ],
        )
    Button(
        "Refresh context",
        variant="info",
        css_class=BUTTON_INFO_CLASS,
        disabled=STATE.is_loading,
        on_click=[
            *start_tool_call("Refreshing connector context\u2026"),
            CallTool(
                load_connector_context,
                arguments={
                    "connector_id": STATE.selected_connector_id,
                    "scope_type": STATE.scope_type,
                    "scope_id": STATE.scope_id,
                    "actor_workspace_id": STATE.actor_workspace_id,
                    "context_guid": STATE.context_guid,
                    "auth_bearer_token": STATE.auth_bearer_token,
                },
                on_success=[
                    *context_success_actions(),
                    *context_error_toast_actions(),
                ],
                on_error=fail_context_actions(),
            ),
        ],
    )


def _render_pin_context_and_versions() -> None:
    """Resolved context indicator and active/latest/pinned-scope summary."""
    with Row(gap=2):
        Markdown("**Resolved context**")
        with If(STATE.resolved_context_label):
            with Row(align="center", gap=1):
                Text("✅")
                Text(content=STATE.resolved_context_label)
    with Grid(columns=3, gap=3):
        with Column(gap=1):
            Small("Active")
            Text(
                content=STATE.current_state.active_version,
                css_class="airbyte-stat-value",
            )
        with Column(gap=1):
            Small("Latest")
            Text(
                content=STATE.current_state.latest_version,
                css_class="airbyte-stat-value",
            )
        with Column(gap=1):
            Small("Pinned scope")
            Text(
                content=STATE.current_state.active_scope,
                css_class="airbyte-stat-value",
            )


def _render_pin_tables() -> None:
    """Inherited and descendant pin configuration tables."""
    Markdown("**Inherited pins**")
    DataTable(
        columns=[
            DataTableColumn(key="scope_type", header="Scope"),
            DataTableColumn(key="scope_id", header="Scope ID"),
            DataTableColumn(key="value_name", header="Version"),
        ],
        rows=STATE.ancestor_configs,
        pageSize=3,
    )
    Markdown("**Pins below this context**")
    DataTable(
        columns=[
            DataTableColumn(key="scope_type", header="Scope"),
            DataTableColumn(key="scope_id", header="Scope ID"),
            DataTableColumn(key="value_name", header="Version"),
        ],
        rows=STATE.descendant_configs,
        pageSize=3,
    )
