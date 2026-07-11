"""Reusable pin context pane: context input, resolved summary, and pin tables.

Rendered inline (below a selected pin row) and inside the Locate Pin modal.
"""

from __future__ import annotations

from typing import Any

from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import (
    Button,
    Column,
    DataTable,
    DataTableColumn,
    Dialog,
    Grid,
    Input,
    Markdown,
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
from airbyte_ops_webapp.pages.shared_components.org_lookup_modal import (
    render_org_lookup_modal,
)
from airbyte_ops_webapp.theme import BUTTON_INFO_CLASS

# ---------------------------------------------------------------------------
# Shared context-refresh actions (used by both inline and modal)
# ---------------------------------------------------------------------------


def _context_refresh_actions() -> list[Any]:
    """Actions to refresh connector context from current state."""
    return [
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
    ]


# ---------------------------------------------------------------------------
# Reusable pane
# ---------------------------------------------------------------------------


def render_pin_context_pane(*, show_input: bool = True) -> None:
    """Render the pin context pane: context input, resolved summary, and pin tables.

    Set `show_input` to `False` to omit the GUID input row (e.g. when the
    context is auto-populated from a pin row click).
    """
    with Column(gap=3):
        if show_input:
            _render_context_input()
        _render_resolved_context()
        _render_pin_tables()


def _render_context_input() -> None:
    """Context GUID input with refresh and org-search buttons."""
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
            on_select_actions=_context_refresh_actions(),
        )
    Button(
        "Refresh context",
        variant="info",
        css_class=BUTTON_INFO_CLASS,
        disabled=STATE.is_loading,
        on_click=_context_refresh_actions(),
    )


def _render_resolved_context() -> None:
    """Resolved context indicator and active/latest/pinned-scope summary."""
    with Row(gap=2):
        Markdown("**Resolved context**")
        with If(STATE.resolved_context_label), Row(align="center", gap=1):
            Text("\u2705")
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
    )
    Markdown("**Pins below this context**")
    DataTable(
        columns=[
            DataTableColumn(key="scope_type", header="Scope"),
            DataTableColumn(key="scope_id", header="Scope ID"),
            DataTableColumn(key="value_name", header="Version"),
        ],
        rows=STATE.descendant_configs,
    )


# ---------------------------------------------------------------------------
# Locate Pin modal
# ---------------------------------------------------------------------------


def render_locate_pin_modal() -> None:
    """Render the Locate Pin modal dialog.

    The user enters a context GUID (Organization, Workspace, or Actor ID),
    clicks Refresh, and sees the resolved pin context inline.
    """
    with Dialog(
        title="Locate Pin",
        description="Look up pin context for any Organization, Workspace, or Actor.",
        name="locate_pin_modal_open",
    ):
        Button(
            "Locate Pin",
            variant="outline",
            size="sm",
            css_class="border-white/20 text-white hover:bg-white/10",
        )

        render_pin_context_pane(show_input=True)
