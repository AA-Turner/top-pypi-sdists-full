"""Version list panel: scrollable table of published versions with pin detail."""

from __future__ import annotations

from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import (
    H2,
    H3,
    Button,
    CardContent,
    CardHeader,
    Column,
    DataTable,
    DataTableColumn,
    Div,
    Grid,
    Link,
    Muted,
    Row,
    Small,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import EVENT, RESULT, STATE

from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
    fail_tool_call,
    finish_tool_call,
    start_tool_call,
)
from airbyte_ops_webapp.pages.connector_version_manager._mcp_tools import (
    load_version_pins,
)
from airbyte_ops_webapp.theme import (
    BUTTON_INFO_CLASS,
    BUTTON_OUTLINE_CLASS,
    PANEL_CARD_CLASS,
    _card_style,
)

# ---------------------------------------------------------------------------
# Pin-load success actions
# ---------------------------------------------------------------------------

_PIN_LOAD_SUCCESS = [
    *finish_tool_call(),
    SetState("version_pins", RESULT.version_pins),
    SetState("version_pins_total", RESULT.version_pins_total),
    SetState("version_pins_offset", RESULT.version_pins_offset),
    SetState("selected_version_id", RESULT.selected_version_id),
    SetState("selected_version_tag", RESULT.selected_version_tag),
    SetState("selected_pin_index", -1),
    SetState(
        "selected_pin",
        {
            "scope_type": "",
            "scope_id": "",
            "scope_url": "",
            "origin_type": "",
            "origin_name": "",
            "description": "",
            "created_at": "",
            "created_at_display": "",
            "expires_at": "",
            "expires_at_display": "",
            "reference_url": "",
        },
    ),
]


def _version_table_style() -> dict[str, str]:
    return {
        "maxHeight": "28rem",
        "overflowY": "auto",
        "paddingRight": "0.25rem",
    }


# ---------------------------------------------------------------------------
# Public render
# ---------------------------------------------------------------------------


def render_version_list() -> None:
    """Left-column scrollable DataTable of published versions with pin detail."""
    with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
        with CardHeader():
            H2("Version List")
        with CardContent(), Column(gap=3):
            Text("Click a version row to view its pins.")
            with Div(style=_version_table_style()):
                DataTable(
                    columns=[
                        DataTableColumn(
                            key="docker_image_tag",
                            header="Version",
                            sortable=True,
                        ),
                        DataTableColumn(
                            key="last_published_display",
                            header="Published",
                            sortable=True,
                        ),
                    ],
                    rows=STATE.versions,
                    pageSize=20,
                    on_row_click=[
                        SetState("selected_version_tag", EVENT.docker_image_tag),
                        SetState("selected_version_id", EVENT.version_id),
                        SetState("version_pins", []),
                        SetState("version_pins_total", 0),
                        SetState("selected_pin_index", -1),
                        *start_tool_call("Loading pins\u2026"),
                        CallTool(
                            load_version_pins,
                            arguments={
                                "version_id": EVENT.version_id,
                                "version_tag": EVENT.docker_image_tag,
                                "auth_bearer_token": STATE.auth_bearer_token,
                            },
                            on_success=_PIN_LOAD_SUCCESS,
                            on_error=fail_tool_call("Failed to load version pins."),
                        ),
                    ],
                )

            # --- Pin detail for the selected version ---
            with If(STATE.selected_version_tag):
                _render_version_pin_detail()


# ---------------------------------------------------------------------------
# Pin detail sub-sections
# ---------------------------------------------------------------------------


def _render_version_pin_detail() -> None:
    """Pin detail section displayed below the version table."""
    with Column(gap=3, style={"marginTop": "1rem"}):
        with Row(align="center", gap=2):
            H3(
                STATE.selected_version_tag
                + " \u2014 "
                + STATE.version_pins_total.number()
                + " pin(s)"
            )
        _render_pin_table()
        _render_selected_pin_audit()
        _render_pin_action_buttons()


def _render_pin_table() -> None:
    """Pin list table for the selected version."""
    with If(STATE.version_pins_total):
        DataTable(
            columns=[
                DataTableColumn(key="scope_type", header="Scope"),
                DataTableColumn(key="scope_id", header="Scope ID"),
                DataTableColumn(key="origin_name", header="Set By"),
                DataTableColumn(key="created_at_display", header="Date"),
            ],
            rows=STATE.version_pins,
            pageSize=10,
            on_row_click=[
                SetState("selected_pin", EVENT),
            ],
        )
    with If(STATE.version_pins_total.__eq__(0)):
        Muted("No pins for this version.")


def _render_selected_pin_audit() -> None:
    """Audit detail for the pin row the user clicked."""
    with (
        If(STATE.selected_pin.scope_id),
        Div(
            style={
                "padding": "0.75rem",
                "borderRadius": "0.375rem",
                "border": "1px solid rgba(255,255,255,0.1)",
                "marginTop": "0.5rem",
            }
        ),
        Column(gap=2),
    ):
        with Grid(columns=2, gap=2):
            with Column(gap=1):
                Small("Origin")
                Text(content=STATE.selected_pin.origin_type)
            with Column(gap=1):
                Small("Set by")
                Text(content=STATE.selected_pin.origin_name)
        with Grid(columns=2, gap=2):
            with Column(gap=1):
                Small("Date")
                Text(content=STATE.selected_pin.created_at_display)
            with Column(gap=1):
                Small("Expiry")
                Text(content=STATE.selected_pin.expires_at_display)
        with Column(gap=1):
            Small("Reason")
            Text(content=STATE.selected_pin.description)
        with If(STATE.selected_pin.reference_url), Column(gap=1):
            Small("Reference")
            Link(
                content=STATE.selected_pin.reference_url,
                href=STATE.selected_pin.reference_url,
                target="_blank",
            )
        with If(STATE.selected_pin.scope_url), Column(gap=1):
            Small("Scope link")
            Link(
                content="View in Airbyte Cloud \u2197",
                href=STATE.selected_pin.scope_url,
                target="_blank",
            )
        with Row(gap=2, style={"marginTop": "0.5rem"}):
            Button(
                "Unset Pin",
                variant="outline",
                size="sm",
                css_class=BUTTON_OUTLINE_CLASS,
                on_click=[
                    SetState("pin_modal_open", True),
                    SetState("action", "unset"),
                    SetState("scope_type", STATE.selected_pin.scope_type),
                    SetState("scope_id", STATE.selected_pin.scope_id),
                    SetState("target_version", STATE.selected_version_tag),
                ],
            )


def _render_pin_action_buttons() -> None:
    """Bottom action row: Load More | Locate Pin | Create New Pin."""
    with Row(gap=2, style={"marginTop": "0.5rem"}):
        with If(STATE.version_pins_total):
            Button(
                "Load More Pins",
                variant="outline",
                size="sm",
                css_class=BUTTON_OUTLINE_CLASS,
                on_click=[
                    *start_tool_call("Loading more pins\u2026"),
                    CallTool(
                        load_version_pins,
                        arguments={
                            "version_id": STATE.selected_version_id,
                            "version_tag": STATE.selected_version_tag,
                            "auth_bearer_token": STATE.auth_bearer_token,
                            "offset": STATE.version_pins_offset,
                        },
                        on_success=[
                            *finish_tool_call(),
                            SetState("version_pins", RESULT.version_pins),
                            SetState("version_pins_total", RESULT.version_pins_total),
                            SetState("version_pins_offset", RESULT.version_pins_offset),
                        ],
                        on_error=fail_tool_call("Failed to load more pins."),
                    ),
                ],
            )
        with If(STATE.version_pins_total):
            Button(
                "Locate Pin",
                variant="outline",
                size="sm",
                css_class=BUTTON_OUTLINE_CLASS,
            )
        Button(
            "Create New Pin",
            variant="default",
            size="sm",
            css_class=BUTTON_INFO_CLASS,
            on_click=[
                SetState("pin_modal_open", True),
                SetState("action", "set"),
                SetState("target_version", STATE.selected_version_tag),
            ],
        )
