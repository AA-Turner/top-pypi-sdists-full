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
    Form,
    Input,
    Muted,
    Row,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import EVENT, RESULT, STATE
from pydantic import BaseModel, ConfigDict, Field

from airbyte_ops_webapp.pages.shared_components.org_search import OrgSearchRow


class OrgLookupModalState(BaseModel):
    """Prefab state fields owned by the shared org lookup modal.

    Page state models mix these fields in so every page that embeds the modal
    declares the same keys once, via a typed model.
    """

    model_config = ConfigDict(frozen=True)

    org_search_modal_open: bool = False
    org_search_query: str = ""
    org_search_results: list[OrgSearchRow] = Field(default_factory=list)
    org_search_error: str = ""
    org_search_selected_id: str = ""
    org_search_selected_label: str = ""


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
    result_id_field: str = "entity_id",
    result_label_field: str = "display_label",
    target_label_key: str | None = None,
    search_error_actions: list[Any] | None = None,
) -> None:
    """Render a 🔍 button that opens a modal for searching organizations/workspaces.

    The modal contains a search input, results table, and Cancel/Select buttons.
    When the user clicks a row, the entity ID is stored in state. Clicking
    "Select" writes the chosen ID back to `target_state_key` and fires any
    `on_select_actions` (e.g. to auto-submit the parent form).

    `result_id_field` selects which result-row field is written back as the
    chosen ID — default `entity_id` (the clicked entity), or e.g.
    `organization_id` to always resolve a workspace hit up to its organization.
    `result_label_field` selects which row field is shown as the selected label
    — default `display_label` (the clicked entity's label), or e.g.
    `organization_label` so a workspace hit shows its parent org's label,
    matching an `organization_id` `result_id_field`.
    When `target_label_key` is set, the chosen label is also written there on
    Select, so callers can show the selected context.
    `search_error_actions` are appended to the search tool call's `on_error`
    so a page can add its own error feedback (e.g. a page-level toast) in
    addition to the modal's inline error text.
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
                search_error_actions=search_error_actions or [],
            )
            _render_search_results(
                search_results_key=search_results_key,
                search_error_key=search_error_key,
                target_state_key=target_state_key,
                dialog_state_key=dialog_state_key,
                selected_id_key=selected_id_key,
                selected_label_key=selected_label_key,
                on_select_actions=on_select_actions or [],
                result_id_field=result_id_field,
                result_label_field=result_label_field,
                target_label_key=target_label_key,
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
    search_error_actions: list[Any],
) -> None:
    """Search input row with a Search button.

    Wrapping the input and button in a `Form` makes pressing Enter in the input
    submit the search (native HTML form submission), matching the Search
    button. The button is `button_type="submit"` so a click also submits the
    form, and the search actions live on the form's `on_submit` so both paths
    share a single definition.
    """
    search_actions = [
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
                *search_error_actions,
            ],
        ),
    ]
    with Form(on_submit=search_actions), Row(gap=2, align="end"):
        Input(
            name=search_query_key,
            value=getattr(STATE, search_query_key),
            placeholder="Type org name, email, or workspace name…",
            style={"flex": "1"},
        )
        Button(
            "Search",
            variant="info",
            button_type="submit",
            css_class="bg-[#5D51D5] text-white border-[#5D51D5] hover:bg-[#4D43BE]",
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
    result_id_field: str = "entity_id",
    result_label_field: str = "display_label",
    target_label_key: str | None = None,
) -> None:
    """Results table with clickable rows."""
    with If(getattr(STATE, search_error_key)):
        Text(
            content=getattr(STATE, search_error_key),
            style={"color": "#B42318", "fontSize": "0.875rem"},
        )
    with If(getattr(STATE, search_results_key)):
        Muted("Click a row to select, then press Select.")
        with Column(css_class="max-h-[50vh] overflow-auto"):
            DataTable(
                columns=[
                    DataTableColumn(key="entity_type", header="Type"),
                    DataTableColumn(key="entity_name", header="Name"),
                    DataTableColumn(key="entity_id", header="ID"),
                ],
                rows=getattr(STATE, search_results_key),
                on_row_click=[
                    SetState(selected_id_key, getattr(EVENT, result_id_field)),
                    SetState(selected_label_key, getattr(EVENT, result_label_field)),
                ],
            )
    with If(getattr(STATE, selected_id_key)):
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
                    *(
                        [SetState(target_label_key, getattr(STATE, selected_label_key))]
                        if target_label_key
                        else []
                    ),
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

    Merge these into the page's initial state dict. Backed by
    `OrgLookupModalState` so the keys stay in sync with the typed model that
    page state models mix in.
    """
    return OrgLookupModalState().model_dump(mode="json")
