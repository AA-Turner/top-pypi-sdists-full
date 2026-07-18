"""Pin detail panel for the selected connector version."""

from __future__ import annotations

from prefab_ui.actions import SetState, ShowToast
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
    Link,
    Markdown,
    Muted,
    Row,
    Span,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import ERROR, EVENT, RESULT, STATE

from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
    EMPTY_PIN_STATE,
    fail_tool_call,
    finish_tool_call,
    start_tool_call,
)
from airbyte_ops_webapp.pages.connector_version_manager._mcp_tools import (
    load_version_pins,
    remove_selected_pins,
    resolve_scope_guid,
)
from airbyte_ops_webapp.theme import (
    BUTTON_DESTRUCTIVE_CLASS,
    BUTTON_INFO_CLASS,
    BUTTON_OUTLINE_CLASS,
    AbCard,
    AbDetailBox,
    AbDetailValue,
    AbFieldCaption,
    AbScopeBadge,
)

_PIN_LINK_CLASS = "block text-[0.85rem] break-all text-[#818cf8] no-underline"

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
    SetState("selected_pin_checks", []),
    SetState("selected_pin", EMPTY_PIN_STATE),
    SetState("resolved_pin_scope_name", ""),
    SetState("resolved_pin_scope_url", ""),
    SetState("resolved_pin_workspace_name", ""),
    SetState("resolved_pin_workspace_url", ""),
    SetState("resolved_pin_org_name", ""),
    SetState("resolved_pin_org_url", ""),
]

_PIN_REMOVAL_SUCCESS = [
    *finish_tool_call(),
    SetState("version_pins", RESULT.version_pins),
    SetState("version_pins_total", RESULT.version_pins_total),
    SetState("version_pins_offset", RESULT.version_pins_offset),
    SetState("selected_version_id", RESULT.selected_version_id),
    SetState("selected_version_tag", RESULT.selected_version_tag),
    SetState("selected_pin_index", -1),
    SetState("selected_pin_checks", []),
    SetState("selected_pin", EMPTY_PIN_STATE),
    SetState("resolved_pin_scope_name", ""),
    SetState("resolved_pin_scope_url", ""),
    SetState("resolved_pin_workspace_name", ""),
    SetState("resolved_pin_workspace_url", ""),
    SetState("resolved_pin_org_name", ""),
    SetState("resolved_pin_org_url", ""),
    ShowToast(RESULT.remove_message),
]


# ---------------------------------------------------------------------------
# Public render
# ---------------------------------------------------------------------------


def render_pin_detail() -> None:
    """Separate card section showing pin detail for the selected version."""
    with (
        If(STATE.selected_version_tag),
        AbCard(),
    ):
        with CardHeader():
            H2("Version Pins", css_class="text-lg")
        with CardContent():
            # Loading state while connector context is being fetched
            with If(STATE.context_loading.__eq__(True)):
                Muted("Loading version pins…")

            # Populated state
            with If(STATE.context_loading.__eq__(False)):
                # Subheader with pin count for selected version
                Muted(
                    STATE.version_pins_total.number()
                    + " pin(s) for version "
                    + STATE.selected_version_tag,
                    css_class="mb-2",
                )
                _render_pin_table_with_checkboxes()
                _render_pin_action_buttons()


# ---------------------------------------------------------------------------
# Pin detail sub-sections
# ---------------------------------------------------------------------------


def _render_pin_table_with_checkboxes() -> None:
    """Pin list table with row-click selection."""
    with If(STATE.version_pins_total):
        with Div(css_class="max-h-[280px] overflow-auto"):
            DataTable(
                columns=[
                    DataTableColumn(key="scope_type", header="Scope"),
                    DataTableColumn(key="scope_id", header="Scope ID"),
                    DataTableColumn(key="description_display", header="Reason"),
                    DataTableColumn(key="created_at_display", header="Date"),
                    DataTableColumn(key="expires_at_display", header="Expires"),
                ],
                rows=STATE.version_pins,
                on_row_click=[
                    SetState("selected_pin", EVENT),
                    SetState("context_guid", EVENT.scope_id),
                    SetState("resolved_pin_scope_name", ""),
                    SetState("resolved_pin_scope_url", ""),
                    SetState("resolved_pin_workspace_name", ""),
                    SetState("resolved_pin_workspace_url", ""),
                    SetState("resolved_pin_org_name", ""),
                    SetState("resolved_pin_org_url", ""),
                    CallTool(
                        resolve_scope_guid,
                        arguments={
                            "connector_id": STATE.selected_connector.id,
                            "context_guid": EVENT.scope_id,
                            "auth_bearer_token": STATE.auth_bearer_token,
                        },
                        on_success=[
                            SetState("resolved_pin_scope_name", RESULT.scope_name),
                            SetState("resolved_pin_scope_url", RESULT.scope_url),
                            SetState(
                                "resolved_pin_workspace_name", RESULT.workspace_name
                            ),
                            SetState(
                                "resolved_pin_workspace_url", RESULT.workspace_url
                            ),
                            SetState("resolved_pin_org_name", RESULT.organization_name),
                            SetState("resolved_pin_org_url", RESULT.organization_url),
                        ],
                        on_error=fail_tool_call("Failed to resolve pin scope."),
                    ),
                ],
            )
        _render_selected_pin_detail()
    with If(STATE.version_pins_total.__eq__(0)):
        Muted("No pins for this version.")


def _render_selected_pin_detail() -> None:
    """Structured detail panel for the selected pin row."""
    with If(STATE.selected_pin.scope_id), AbDetailBox():
        Span(
            "Pin Details",
            css_class="block font-semibold text-[0.9rem] mb-3 text-[#e5e7eb]",
        )
        # Row 1: Scope badge, Scope Name (link), Scope ID
        with Grid(columns=3, gap=4):
            with Column(gap=0):
                AbFieldCaption("SCOPE", css_class="mb-[2px]")
                AbScopeBadge(content=STATE.selected_pin.scope_type)
            with Column(gap=0):
                AbFieldCaption("SCOPE NAME", css_class="mb-[2px]")
                # Resolved name with link; falls back to scope_name from row
                with If(STATE.resolved_pin_scope_name.__ne__("")):
                    Link(
                        content=STATE.resolved_pin_scope_name,
                        href=STATE.resolved_pin_scope_url,
                        target="_blank",
                        css_class=_PIN_LINK_CLASS,
                    )
                with If(STATE.resolved_pin_scope_name.__eq__("")):
                    with If(STATE.selected_pin.scope_name):
                        AbDetailValue(content=STATE.selected_pin.scope_name)
                    with If(STATE.selected_pin.scope_name.__eq__("")):
                        Muted("Resolving…")
            with Column(gap=0):
                AbFieldCaption("SCOPE ID", css_class="mb-[2px]")
                AbDetailValue(
                    content=STATE.selected_pin.scope_id,
                    css_class="font-mono text-[0.8rem]",
                )

        # Row 2: Parent scopes (organization, workspace) — only for non-org scopes
        _render_parent_scopes()

        # Row 3: Origin, Created, Expires
        with Grid(columns=3, gap=4, css_class="mt-3"):
            with Column(gap=0):
                AbFieldCaption("ORIGIN", css_class="mb-[2px]")
                AbDetailValue(content=STATE.selected_pin.origin_name)
            with Column(gap=0):
                AbFieldCaption("CREATED", css_class="mb-[2px]")
                AbDetailValue(content=STATE.selected_pin.created_at_display)
            with Column(gap=0):
                AbFieldCaption("EXPIRES", css_class="mb-[2px]")
                with If(STATE.selected_pin.expires_at_display):
                    AbDetailValue(content=STATE.selected_pin.expires_at_display)
                with If(STATE.selected_pin.expires_at_display.__eq__("")):
                    AbDetailValue("—", css_class="text-[#6b7280]")

        # Row 4: Reason (full width) — uses description_display which
        # contains synthesized labels for breaking change / rollout pins.
        with (
            If(STATE.selected_pin.description_display),
            Column(
                gap=0,
                css_class="mt-3",
            ),
        ):
            AbFieldCaption("REASON", css_class="mb-[2px]")
            AbDetailValue(content=STATE.selected_pin.description_display)

        # Row 5: Reference URL (full width, if present)
        with (
            If(STATE.selected_pin.reference_url),
            Column(
                gap=0,
                css_class="mt-3",
            ),
        ):
            AbFieldCaption("REFERENCE", css_class="mb-[2px]")
            Link(
                content=STATE.selected_pin.reference_url,
                href=STATE.selected_pin.reference_url,
                target="_blank",
                css_class=_PIN_LINK_CLASS,
            )

        # Row 6: Remove This Pin action
        _render_remove_this_pin_button()


def _render_parent_scopes() -> None:
    """Render parent scope row: organization and/or workspace links.

    - Actor scope: ORGANIZATION + WORKSPACE (both parents)
    - Workspace scope: ORGANIZATION only (workspace is the scope itself)
    - Organization scope: nothing (org is the scope itself)
    """
    # Show org when resolved (for actor and workspace scopes)
    with (
        If(STATE.resolved_pin_org_name.__ne__("")),
        Grid(columns=3, gap=4, css_class="mt-3"),
    ):
        with Column(gap=0):
            AbFieldCaption("ORGANIZATION", css_class="mb-[2px]")
            Link(
                content=STATE.resolved_pin_org_name,
                href=STATE.resolved_pin_org_url,
                target="_blank",
                css_class=_PIN_LINK_CLASS,
            )
        # Show workspace column only for actor scopes
        with If(STATE.resolved_pin_workspace_name.__ne__("")), Column(gap=0):
            AbFieldCaption("WORKSPACE", css_class="mb-[2px]")
            Link(
                content=STATE.resolved_pin_workspace_name,
                href=STATE.resolved_pin_workspace_url,
                target="_blank",
                css_class=_PIN_LINK_CLASS,
            )


def _render_pin_action_buttons() -> None:
    """Bottom action row: left = Add Pins, right = indicator + Load More."""
    with Row(justify="between", gap=2, css_class="mt-2"):
        # Left-aligned action buttons
        with Row(gap=2):
            Button(
                "Add Pins...",
                variant="default",
                size="sm",
                css_class=BUTTON_INFO_CLASS,
                on_click=[
                    SetState("pin_modal_open", True),
                    SetState("action", "set"),
                    SetState("target_version", STATE.selected_version_tag),
                ],
            )

        # Right-aligned: "N of M pins loaded" indicator + Load More button.
        # Derived: shown only while more pins remain to load (loaded < total).
        with (
            If(STATE.version_pins_total.__gt__(STATE.version_pins.length())),
            Row(gap=2, align="center"),
        ):
            Muted(
                STATE.version_pins.length().number()
                + " of "
                + STATE.version_pins_total.number()
                + " pins loaded",
            )
            Button(
                "Load More Pins",
                variant="outline",
                size="sm",
                css_class=BUTTON_OUTLINE_CLASS,
                on_click=[
                    *start_tool_call("Loading more pins…"),
                    CallTool(
                        load_version_pins,
                        arguments={
                            "version_id": STATE.selected_version_id,
                            "version_tag": STATE.selected_version_tag,
                            "auth_bearer_token": STATE.auth_bearer_token,
                            "offset": STATE.version_pins_offset,
                        },
                        on_success=_PIN_LOAD_SUCCESS,
                        on_error=fail_tool_call("Failed to load more pins."),
                    ),
                ],
            )


def _render_remove_this_pin_button() -> None:
    """Remove This Pin button with confirmation modal inside the detail panel.

    Breaking change pins cannot be removed through this interface, so the button
    is rendered as disabled with an explanatory tooltip when `origin_type` is
    `"breaking_change"`.
    """
    # Disabled state for breaking change pins
    with If(STATE.selected_pin.origin_type.__eq__("breaking_change")):
        Button(
            "Remove This Pin",
            variant="destructive",
            size="sm",
            css_class=BUTTON_DESTRUCTIVE_CLASS + " mt-3",
            disabled=True,
            title="Pins for breaking changes cannot be removed through this interface.",
        )

    # Normal removable pin (includes connector rollout pins)
    with (
        If(STATE.selected_pin.origin_type.__ne__("breaking_change")),
        Dialog(
            title="Confirm Pin Removal",
            description="This action cannot be undone.",
            name="remove_pins_modal_open",
        ),
    ):
        Button(
            "Remove This Pin",
            variant="destructive",
            size="sm",
            css_class=BUTTON_DESTRUCTIVE_CLASS + " mt-3",
        )

        with Column(gap=4):
            Markdown(
                content="**Remove this pin?**\n\n"
                "This will unset the version override for scope "
                + STATE.selected_pin.scope_id
                + ". This action cannot be undone."
            )
            with Row(justify="end", gap=2):
                Button(
                    "Cancel",
                    variant="outline",
                    css_class=BUTTON_OUTLINE_CLASS,
                    on_click=[SetState("remove_pins_modal_open", False)],
                )
                Button(
                    "Confirm",
                    variant="destructive",
                    css_class=BUTTON_DESTRUCTIVE_CLASS,
                    disabled=STATE.is_loading,
                    on_click=[
                        SetState("remove_pins_modal_open", False),
                        *start_tool_call("Removing pin…"),
                        CallTool(
                            remove_selected_pins,
                            arguments={
                                "selected_pins": [STATE.selected_pin],
                                "connector_id": STATE.selected_connector.id,
                                "connector_name": STATE.selected_connector.name,
                                "connector_type": (
                                    STATE.selected_connector.connector_type
                                ),
                                "version_id": STATE.selected_version_id,
                                "version_tag": STATE.selected_version_tag,
                                "auth_bearer_token": STATE.auth_bearer_token,
                                "user_email": STATE.oauth_user_email,
                                "customer_tier_filter": "ALL",
                                "google_access_token": STATE.google_access_token,
                            },
                            on_success=_PIN_REMOVAL_SUCCESS,
                            on_error=fail_tool_call(ERROR),
                        ),
                    ],
                )
