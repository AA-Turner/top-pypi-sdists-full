"""Shared organization lookup modal dialog.

Provides a reusable 🔍 button + modal dialog that searches for organizations
and workspaces by substring. The user selects a result and the organization ID
is written back to the adjacent text input via a configurable state key.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import (
    Button,
    Column,
    DataTable,
    DataTableColumn,
    Dialog,
    Input,
    Muted,
    Row,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import EVENT, RESULT, STATE


def render_org_lookup_modal(
    *,
    search_tool: Callable[..., Any],
    target_state_key: str,
    on_select_actions: list[Any] | None = None,
    dialog_state_key: str = "org_search_modal_open",
    search_query_key: str = "org_search_query",
    search_results_key: str = "org_search_results",
    search_error_key: str = "org_search_error",
    selected_id_key: str = "org_search_selected_id",
    selected_label_key: str = "org_search_selected_label",
) -> None:
    """Render a 🔍 button that opens a modal for searching organizations/workspaces.

    The modal contains a search input, results table, and Cancel/Select buttons.
    When the user clicks a row, the entity ID is stored in state. Clicking
    "Select" writes the chosen ID back to `target_state_key` and fires any
    `on_select_actions` (e.g. to auto-submit the parent form).
    """
    with Dialog(
        title="Search Organizations & Workspaces",
        description="Search by name, email, or slug (case-insensitive substring match).",
        name=dialog_state_key,
    ):
        # Trigger: 🔍 button
        Button(
            "🔍",
            variant="outline",
            style={"minWidth": "2.5rem", "padding": "0.5rem"},
        )

        # Dialog body
        with Column(gap=3):
            _render_search_input(
                search_tool=search_tool,
                search_query_key=search_query_key,
                search_results_key=search_results_key,
                search_error_key=search_error_key,
                selected_id_key=selected_id_key,
                selected_label_key=selected_label_key,
            )
            _render_search_results(
                search_results_key=search_results_key,
                search_error_key=search_error_key,
                target_state_key=target_state_key,
                dialog_state_key=dialog_state_key,
                selected_id_key=selected_id_key,
                selected_label_key=selected_label_key,
                on_select_actions=on_select_actions or [],
            )
            _render_cancel_button(
                dialog_state_key=dialog_state_key,
                selected_id_key=selected_id_key,
                selected_label_key=selected_label_key,
            )


def _render_search_input(
    *,
    search_tool: Callable[..., Any],
    search_query_key: str,
    search_results_key: str,
    search_error_key: str,
    selected_id_key: str,
    selected_label_key: str,
) -> None:
    """Search input row with a Search button."""
    with Row(gap=2, align="end"):
        Input(
            name=search_query_key,
            value=getattr(STATE, search_query_key),
            placeholder="Type org name, email, or workspace name…",
            style={"flex": "1"},
        )
        Button(
            "Search",
            variant="info",
            css_class="bg-[#5D51D5] text-white border-[#5D51D5] hover:bg-[#4D43BE]",
            on_click=[
                SetState(search_error_key, ""),
                SetState(search_results_key, []),
                SetState(selected_id_key, ""),
                SetState(selected_label_key, ""),
                CallTool(
                    search_tool,
                    arguments={
                        "query": getattr(STATE, search_query_key),
                    },
                    on_success=[
                        SetState(search_results_key, RESULT.results),
                        SetState(search_error_key, RESULT.error),
                    ],
                    on_error=[
                        SetState(search_error_key, "Search failed. Please try again."),
                    ],
                ),
            ],
        )


def _render_search_results(
    *,
    search_results_key: str,
    search_error_key: str,
    target_state_key: str,
    dialog_state_key: str,
    selected_id_key: str,
    selected_label_key: str,
    on_select_actions: list[Any],
) -> None:
    """Results table with clickable rows."""
    with If(getattr(STATE, search_error_key)):
        Text(
            content=getattr(STATE, search_error_key),
            style={"color": "#B42318", "fontSize": "0.875rem"},
        )
    with If(getattr(STATE, search_results_key)):
        Muted("Click a row to select, then press Select.")
        DataTable(
            columns=[
                DataTableColumn(key="entity_type", header="Type"),
                DataTableColumn(key="entity_name", header="Name"),
                DataTableColumn(key="entity_id", header="ID"),
            ],
            rows=getattr(STATE, search_results_key),
            pageSize=10,
            on_row_click=[
                SetState(selected_id_key, EVENT.entity_id),
                SetState(selected_label_key, EVENT.display_label),
            ],
        )
    with If(getattr(STATE, selected_label_key)):
        with Row(gap=2, align="center"):
            Text("Selected:", style={"fontWeight": "600", "fontSize": "0.875rem"})
            Text(
                content=getattr(STATE, selected_label_key),
                style={"fontSize": "0.875rem"},
            )
        with Row(justify="end", gap=2):
            Button(
                "Select",
                variant="info",
                css_class="bg-[#5D51D5] text-white border-[#5D51D5] hover:bg-[#4D43BE]",
                on_click=[
                    SetState(target_state_key, getattr(STATE, selected_id_key)),
                    SetState(dialog_state_key, False),
                    SetState(selected_id_key, ""),
                    SetState(selected_label_key, ""),
                    *on_select_actions,
                ],
            )


def _render_cancel_button(
    *,
    dialog_state_key: str,
    selected_id_key: str,
    selected_label_key: str,
) -> None:
    """Cancel button to dismiss the modal without selection."""
    with Row(justify="end"):
        Button(
            "Cancel",
            variant="outline",
            on_click=[
                SetState(dialog_state_key, False),
                SetState(selected_id_key, ""),
                SetState(selected_label_key, ""),
            ],
        )


def org_lookup_modal_state() -> dict[str, object]:
    """Return the initial state entries required by the org lookup modal.

    Merge these into the page's initial state dict.
    """
    return {
        "org_search_modal_open": False,
        "org_search_query": "",
        "org_search_results": [],
        "org_search_error": "",
        "org_search_selected_id": "",
        "org_search_selected_label": "",
    }
