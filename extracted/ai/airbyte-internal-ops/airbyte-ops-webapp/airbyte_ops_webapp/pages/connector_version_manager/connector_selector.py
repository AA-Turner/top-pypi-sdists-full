"""Connector version selector with tabbed DataTable interface.

Tabs (in order): Active Rollouts, Recent Releases, Pinned Versions,
Yanked Versions, Default Versions, Organization Pins.  The connector-centric
tabs each select both a connector AND a version in one click, populating the
rollout status and pin detail sections below.  Organization Pins is namespaced
separately (`org_pin_*` state) and drives its own two-step org → version → pins
view rather than the shared connector-centric detail panels.
"""

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
    Div,
    Muted,
    Row,
    Tab,
    Tabs,
    Text,
)
from prefab_ui.components.control_flow import Else, If
from prefab_ui.rx import EVENT, RESULT, STATE

from airbyte_ops_webapp.pages.connector_version_manager._helpers import (
    EMPTY_PIN_STATE,
    EMPTY_ROLLOUT_STATE,
    context_success_actions,
    fail_context_actions,
    fail_tool_call,
    start_tool_call,
)
from airbyte_ops_webapp.pages.connector_version_manager._mcp_tools import (
    load_active_rollouts_tab,
    load_connector_version_context,
    load_org_pin_versions,
    load_org_pins,
    load_pinned_versions_tab,
    load_recent_releases_tab,
    load_yanked_versions_tab,
    search_orgs_workspaces,
)
from airbyte_ops_webapp.pages.shared_components.org_lookup_modal import (
    render_org_lookup_modal,
)
from airbyte_ops_webapp.theme import AbCard, AbStatValue

# Fixed-height scrollable container for all 5 selector tabs (~8-9 visible rows).
# `overflow: auto` scrolls both axes so wide tables scroll horizontally (rather
# than bleeding out) while the sticky header pins to this wrapper on vertical
# scroll.
_TAB_LIST_CLASS = "max-h-[480px] overflow-auto"


def render_connector_selector(state: dict[str, object]) -> None:
    """Render the connector version selector with four DataTable tabs."""
    with AbCard():
        with CardHeader():
            H2("Select a Connector Version")
        with (
            CardContent(),
            Tabs(
                name="selector_tab",
                value=state["selector_tab"],
                variant="line",
            ),
        ):
            with Tab("Active Rollouts", value="active-rollouts"):
                _render_lazy_tab(
                    state_key="progressive_rollout_rows",
                    tool=load_active_rollouts_tab,
                    loading_label="Loading active rollouts\u2026",
                    empty_label="No active progressive rollouts.",
                    render_fn=_render_active_rollouts_table,
                )
            with Tab("Recent Releases", value="recent-releases"):
                _render_lazy_tab(
                    state_key="recent_release_rows",
                    tool=load_recent_releases_tab,
                    loading_label="Loading recent releases\u2026",
                    empty_label="No recent releases found.",
                    render_fn=_render_recent_releases_table,
                )
            with Tab("Pinned Versions", value="pinned-versions"):
                _render_lazy_tab(
                    state_key="pinned_version_rows",
                    tool=load_pinned_versions_tab,
                    loading_label="Loading pinned versions\u2026",
                    empty_label="No pinned versions found.",
                    render_fn=_render_pinned_versions_table,
                )
            with Tab("Yanked Versions", value="yanked-versions"):
                _render_lazy_tab(
                    state_key="yanked_version_rows",
                    tool=load_yanked_versions_tab,
                    loading_label="Loading yanked versions\u2026",
                    empty_label="No yanked versions found.",
                    render_fn=_render_yanked_versions_table,
                )
            with Tab("Default Versions", value="latest-versions"):
                _render_latest_versions_tab()
            with Tab("Organization Pins", value="organization-pins"):
                _render_organization_pins_tab()


# ---------------------------------------------------------------------------
# Tab 5: Default Versions (one row per connector, latest GA default only)
# ---------------------------------------------------------------------------


def _render_latest_versions_tab() -> None:
    with If(STATE.latest_version_rows), Div(css_class=_TAB_LIST_CLASS):
        DataTable(
            columns=[
                DataTableColumn(
                    key="name",
                    header="Connector",
                    sortable=True,
                ),
                DataTableColumn(
                    key="connector_type",
                    header="Type",
                    sortable=True,
                ),
                DataTableColumn(
                    key="latest_version",
                    header="Default Version",
                    sortable=True,
                ),
            ],
            rows=STATE.latest_version_rows,
            search=True,
            on_row_click=_row_click_actions(
                connector_id_key="id",
                version_tag_key="latest_version",
            ),
        )
    with If(STATE.latest_version_rows.length().__eq__(0)):
        Muted("No connectors found.")


# ---------------------------------------------------------------------------
# Lazy tab loader
# ---------------------------------------------------------------------------


def _render_lazy_tab(
    *,
    state_key: str,
    tool: object,
    loading_label: str,
    empty_label: str,
    render_fn: object,
) -> None:
    """Render a lazy-loaded tab that fetches data on first activation.

    A hidden `Div` with `on_mount` fires the load tool the first time the
    tab content renders. Once rows arrive the trigger unmounts and the
    DataTable (via `render_fn`) takes over.  A boolean sentinel flag
    (`{state_key}_loaded`) distinguishes "loaded but empty" (`True`) from
    "never loaded" (`False`).
    """
    rows_ref = getattr(STATE, state_key)
    loaded_flag_ref = getattr(STATE, f"{state_key}_loaded")

    # First activation: trigger the load tool
    with (
        If(loaded_flag_ref.__eq__(False)),
        Div(
            on_mount=[
                CallTool(
                    tool,
                    on_success=[
                        SetState(state_key, RESULT.rows),
                        SetState(f"{state_key}_loaded", True),
                    ],
                    on_error=[
                        SetState(f"{state_key}_loaded", True),
                        *fail_tool_call(f"Failed to load {state_key}."),
                    ],
                ),
            ],
        ),
    ):
        Muted(loading_label)

    # After loading: show table or empty message
    with If(loaded_flag_ref.__eq__(True)):
        with If(rows_ref):
            render_fn()  # type: ignore[operator]
        with If(rows_ref.length().__eq__(0)):
            Muted(empty_label)


# ---------------------------------------------------------------------------
# Tab 2: Recent Releases (all versions published in last 30 days, max 50)
# (Previously tab 2, unchanged)
# ---------------------------------------------------------------------------


def _render_recent_releases_table() -> None:
    with Div(css_class=_TAB_LIST_CLASS):
        DataTable(
            columns=[
                DataTableColumn(
                    key="connector_name",
                    header="Connector",
                    sortable=True,
                ),
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
            rows=STATE.recent_release_rows,
            search=True,
            on_row_click=_row_click_actions(
                connector_id_key="connector_id",
                version_tag_key="docker_image_tag",
            ),
        )


# ---------------------------------------------------------------------------
# Tab 1: Active Rollouts (same content as Progressive Rollouts dashboard)
# ---------------------------------------------------------------------------


def _render_active_rollouts_table() -> None:
    AbStatValue(
        content=STATE.progressive_rollout_rows.length().number() + " active rollout(s)",
    )
    with Div(css_class=_TAB_LIST_CLASS):
        DataTable(
            columns=[
                DataTableColumn(
                    key="connector_name",
                    header="Connector",
                    sortable=True,
                ),
                DataTableColumn(
                    key="rc_docker_image_tag",
                    header="Version",
                    sortable=True,
                ),
                DataTableColumn(
                    key="tier_2_display",
                    header="Tier 2",
                    sortable=True,
                ),
                DataTableColumn(
                    key="tier_1_display",
                    header="Tier 1",
                    sortable=True,
                ),
                DataTableColumn(
                    key="tier_0_display",
                    header="Tier 0",
                    sortable=True,
                ),
                DataTableColumn(
                    key="state",
                    header="State",
                    sortable=True,
                ),
                DataTableColumn(
                    key="autopilot_display",
                    header="Autopilot",
                    sortable=True,
                ),
                DataTableColumn(
                    key="rc_pin_count_display",
                    header="Version Pins",
                    sortable=True,
                    format="number",
                    align="right",
                    header_class="[&>button]:justify-end",
                ),
            ],
            rows=STATE.progressive_rollout_rows,
            search=True,
            on_row_click=_row_click_actions(
                connector_id_key="connector_id",
                version_tag_key="rc_docker_image_tag",
            ),
        )


# ---------------------------------------------------------------------------
# Tab 3: Pinned Versions (cross-connector, versions with ≥1 pin)
# ---------------------------------------------------------------------------


def _render_pinned_versions_table() -> None:
    _render_pin_origin_filter_chips()
    with Div(css_class=_TAB_LIST_CLASS):
        DataTable(
            columns=[
                DataTableColumn(
                    key="connector_name",
                    header="Connector",
                    sortable=True,
                ),
                DataTableColumn(
                    key="docker_image_tag",
                    header="Version",
                    sortable=True,
                ),
                DataTableColumn(
                    key="breaking_change_pins_display",
                    header="Breaking Change Pins",
                    sortable=True,
                    format="number",
                    align="right",
                    header_class="[&>button]:justify-end",
                ),
                DataTableColumn(
                    key="rollout_pins_display",
                    header="Rollout Pins",
                    sortable=True,
                    format="number",
                    align="right",
                    header_class="[&>button]:justify-end",
                ),
                DataTableColumn(
                    key="actor_pins_display",
                    header="Actor Pins",
                    sortable=True,
                    format="number",
                    align="right",
                    header_class="[&>button]:justify-end",
                ),
                DataTableColumn(
                    key="workspace_pins_display",
                    header="Workspace Pins",
                    sortable=True,
                    format="number",
                    align="right",
                    header_class="[&>button]:justify-end",
                ),
                DataTableColumn(
                    key="org_pins_display",
                    header="Organization Pins",
                    sortable=True,
                    format="number",
                    align="right",
                    header_class="[&>button]:justify-end",
                ),
                DataTableColumn(
                    key="custom_pin_count_display",
                    header="Total Custom Pins",
                    sortable=True,
                    format="number",
                    align="right",
                    header_class="[&>button]:justify-end",
                ),
            ],
            rows=STATE.pinned_version_rows,
            search=True,
            on_row_click=_row_click_actions(
                connector_id_key="connector_id",
                version_tag_key="docker_image_tag",
            ),
        )


# ---------------------------------------------------------------------------
# Tab 4: Yanked Versions (cross-connector, active `version-yank.yml` markers)
# ---------------------------------------------------------------------------


def _render_yanked_versions_table() -> None:
    with Div(css_class=_TAB_LIST_CLASS):
        DataTable(
            columns=[
                DataTableColumn(
                    key="connector_name",
                    header="Connector",
                    sortable=True,
                ),
                DataTableColumn(
                    key="docker_image_tag",
                    header="Version",
                    sortable=True,
                ),
                DataTableColumn(
                    key="yanked_at_display",
                    header="Yanked",
                    sortable=True,
                ),
                DataTableColumn(
                    key="reason",
                    header="Reason",
                    sortable=True,
                ),
            ],
            rows=STATE.yanked_version_rows,
            search=True,
            on_row_click=_row_click_actions(
                connector_id_key="connector_id",
                version_tag_key="docker_image_tag",
            ),
        )


# Filter chip definitions: (label, origin_filter value)
_PIN_FILTER_CHIPS: list[tuple[str, str]] = [
    ("All", "all"),
    ("Rollouts", "rollout"),
    ("Custom Pins", "custom"),
    ("Breaking Changes", "breaking_change"),
]


def _filter_chip_actions(origin_filter: str) -> list:
    """Build click actions for a pin origin filter chip."""
    return [
        SetState("pin_origin_filter", origin_filter),
        CallTool(
            load_pinned_versions_tab,
            arguments={"origin_filter": origin_filter},
            on_success=[
                SetState("pinned_version_rows", RESULT.rows),
            ],
            on_error=fail_tool_call("Failed to filter pinned versions."),
        ),
    ]


def _render_pin_origin_filter_chips() -> None:
    """Render origin-type filter chips above the Pinned Versions table."""
    with Row(gap=2, css_class="mb-3"):
        for label, filter_value in _PIN_FILTER_CHIPS:
            actions = _filter_chip_actions(filter_value)
            with If(STATE.pin_origin_filter.__eq__(filter_value)):
                Button(label, variant="default", size="sm", on_click=actions)
            with Else():
                Button(label, variant="outline", size="sm", on_click=actions)


# ---------------------------------------------------------------------------
# Tab 6: Organization Pins (two-step: pick an org, then its pinned versions)
# ---------------------------------------------------------------------------


def _org_pin_reset_actions() -> list:
    """Reset the namespaced org-pin state when the org changes or is cleared."""
    return [
        SetState("org_pin_version_rows", []),
        SetState("org_pin_version_rows_loaded", False),
        SetState("org_pin_error", ""),
        SetState("org_pin_selected_version_id", ""),
        SetState("org_pin_selected_version_tag", ""),
        SetState("org_pin_rows", []),
        SetState("org_pin_rows_loaded", False),
        SetState("org_pin_rows_error", ""),
    ]


def _render_organization_pins_tab() -> None:
    """Render the two-step Organization Pins tab."""
    _render_org_pin_selector()
    with If(STATE.org_pin_context_id):
        _render_org_pin_versions_section()
        with If(STATE.org_pin_selected_version_id):
            _render_org_pin_detail_section()
    with Else():
        Muted("Select an organization to view its connector version pins.")


def _render_org_pin_selector() -> None:
    """Org search/select row + selected-org label and Clear button."""
    with Row(gap=2, align="center", css_class="mb-3"):
        # Namespaced modal state keys so this tab's org search never collides
        # with the pin-context-pane org search (which uses the default keys).
        render_org_lookup_modal(
            search_tool=search_orgs_workspaces,
            target_state_key="org_pin_context_id",
            target_label_key="org_pin_context_label",
            result_id_field="organization_id",
            result_label_field="organization_label",
            dialog_state_key="org_pin_search_modal_open",
            search_query_key="org_pin_search_query",
            search_results_key="org_pin_search_results",
            search_error_key="org_pin_search_error",
            selected_id_key="org_pin_search_selected_id",
            selected_label_key="org_pin_search_selected_label",
            on_select_actions=_org_pin_reset_actions(),
            search_error_actions=fail_tool_call("Organization search failed."),
        )
        with If(STATE.org_pin_context_id), Row(gap=2, align="center"):
            Text("Organization:", css_class="font-semibold")
            Text(content=STATE.org_pin_context_label)
            Button(
                "Clear",
                variant="outline",
                size="sm",
                on_click=[
                    SetState("org_pin_context_id", ""),
                    SetState("org_pin_context_label", ""),
                    *_org_pin_reset_actions(),
                ],
            )
        with Else():
            Muted("No organization selected.")


def _render_org_pin_versions_section() -> None:
    """Lazy-load and render the versions-with-pins table for the selected org."""
    with (
        If(STATE.org_pin_version_rows_loaded.__eq__(False)),
        Div(
            on_mount=[
                CallTool(
                    load_org_pin_versions,
                    arguments={"organization_id": STATE.org_pin_context_id},
                    on_success=[
                        SetState("org_pin_version_rows", RESULT.rows),
                        SetState("org_pin_version_rows_loaded", True),
                    ],
                    on_error=[
                        SetState("org_pin_version_rows_loaded", True),
                        SetState(
                            "org_pin_error",
                            "Failed to load organization pins.",
                        ),
                        *fail_tool_call("Failed to load organization pins."),
                    ],
                ),
            ],
        ),
    ):
        Muted("Loading organization pins\u2026")
    with If(STATE.org_pin_error):
        Muted(content=STATE.org_pin_error)
    with If(STATE.org_pin_version_rows_loaded.__eq__(True)):
        with If(STATE.org_pin_version_rows):
            _render_org_pin_versions_table()
        with (
            If(STATE.org_pin_error.__eq__("")),
            If(STATE.org_pin_version_rows.length().__eq__(0)),
        ):
            Muted("No connector version pins found under this organization.")


def _render_org_pin_versions_table() -> None:
    with Div(css_class=_TAB_LIST_CLASS):
        DataTable(
            columns=[
                DataTableColumn(
                    key="connector_name", header="Connector", sortable=True
                ),
                DataTableColumn(
                    key="docker_image_tag", header="Version", sortable=True
                ),
                DataTableColumn(
                    key="has_active_rollout_display",
                    header="Live Rollout",
                    sortable=True,
                ),
                DataTableColumn(
                    key="breaking_change_pins_display",
                    header="Breaking Change Pins",
                    sortable=True,
                    format="number",
                    align="right",
                    header_class="[&>button]:justify-end",
                ),
                DataTableColumn(
                    key="rollout_pins_display",
                    header="Rollout Pins",
                    sortable=True,
                    format="number",
                    align="right",
                    header_class="[&>button]:justify-end",
                ),
                DataTableColumn(
                    key="actor_pins_display",
                    header="Actor Pins",
                    sortable=True,
                    format="number",
                    align="right",
                    header_class="[&>button]:justify-end",
                ),
                DataTableColumn(
                    key="workspace_pins_display",
                    header="Workspace Pins",
                    sortable=True,
                    format="number",
                    align="right",
                    header_class="[&>button]:justify-end",
                ),
                DataTableColumn(
                    key="org_pins_display",
                    header="Organization Pins",
                    sortable=True,
                    format="number",
                    align="right",
                    header_class="[&>button]:justify-end",
                ),
            ],
            rows=STATE.org_pin_version_rows,
            search=True,
            on_row_click=_org_pin_version_click_actions(),
        )


def _org_pin_version_click_actions() -> list:
    """Load the org-scoped pins for the clicked version."""
    return [
        SetState("org_pin_selected_version_id", EVENT.version_id),
        SetState("org_pin_selected_version_tag", EVENT.docker_image_tag),
        SetState("org_pin_rows", []),
        SetState("org_pin_rows_loaded", False),
        SetState("org_pin_rows_error", ""),
        CallTool(
            load_org_pins,
            arguments={
                "organization_id": STATE.org_pin_context_id,
                "pinned_version_id": EVENT.version_id,
            },
            on_success=[
                SetState("org_pin_rows", RESULT.rows),
                SetState("org_pin_rows_loaded", True),
            ],
            on_error=[
                SetState("org_pin_rows_loaded", True),
                SetState(
                    "org_pin_rows_error",
                    "Failed to load pins for this version.",
                ),
                *fail_tool_call("Failed to load pins for this version."),
            ],
        ),
    ]


def _render_org_pin_detail_section() -> None:
    """Render the individual pins for the selected version under the org."""
    with Column(gap=2, css_class="mt-4"):
        with Row(gap=2, align="center"):
            Text("Pins for version", css_class="font-semibold")
            Text(content=STATE.org_pin_selected_version_tag)
        with If(STATE.org_pin_rows_error):
            Muted(content=STATE.org_pin_rows_error)
        with If(STATE.org_pin_rows_loaded.__eq__(False)):
            Muted("Loading pins\u2026")
        with If(STATE.org_pin_rows_loaded.__eq__(True)):
            with If(STATE.org_pin_rows):
                _render_org_pin_detail_table()
            with (
                If(STATE.org_pin_rows_error.__eq__("")),
                If(STATE.org_pin_rows.length().__eq__(0)),
            ):
                Muted("No pins found for this version under this organization.")


def _render_org_pin_detail_table() -> None:
    with Div(css_class=_TAB_LIST_CLASS):
        DataTable(
            columns=[
                DataTableColumn(
                    key="connector_name", header="Connector", sortable=True
                ),
                DataTableColumn(
                    key="pinned_version_tag", header="Version", sortable=True
                ),
                DataTableColumn(key="scope_display", header="Scope", sortable=True),
                DataTableColumn(
                    key="scope_name_display", header="Scope Name", sortable=True
                ),
                DataTableColumn(
                    key="pin_type_display", header="Pin Type", sortable=True
                ),
                DataTableColumn(key="set_by_display", header="Set By", sortable=True),
                DataTableColumn(
                    key="created_at_display", header="Created", sortable=True
                ),
                DataTableColumn(
                    key="expires_at_display", header="Expires", sortable=True
                ),
            ],
            rows=STATE.org_pin_rows,
            search=True,
        )


# ---------------------------------------------------------------------------
# Shared row-click action builder
# ---------------------------------------------------------------------------


def _version_context_success_actions() -> list:
    """Combined success actions for connector context + pin loading."""
    return [
        *context_success_actions(),
        SetState("selected_connector_id", RESULT.selected_connector_id),
        SetState("target_version", RESULT.target_version),
        # Pin detail state
        SetState("version_pins", RESULT.version_pins),
        SetState("version_pins_total", RESULT.version_pins_total),
        SetState("version_pins_offset", RESULT.version_pins_offset),
        SetState("selected_version_id", RESULT.selected_version_id),
        SetState("selected_version_tag", RESULT.selected_version_tag),
        SetState("selected_version_release_date", RESULT.selected_version_release_date),
        SetState("latest_version_release_date", RESULT.latest_version_release_date),
        SetState("selected_version_display", RESULT.selected_version_display),
        SetState("default_version_display", RESULT.default_version_display),
        # Selected-version yank detail
        SetState("selected_version_yanked", RESULT.selected_version_yanked),
        SetState(
            "selected_version_yank_yanked_at", RESULT.selected_version_yank_yanked_at
        ),
        SetState(
            "selected_version_yank_yanked_at_display",
            RESULT.selected_version_yank_yanked_at_display,
        ),
        SetState("selected_version_yank_reason", RESULT.selected_version_yank_reason),
        SetState(
            "selected_version_yank_approval_url",
            RESULT.selected_version_yank_approval_url,
        ),
        SetState("selected_version_yank_raw", RESULT.selected_version_yank_raw),
        SetState("selected_pin_index", -1),
        SetState("selected_pin_checks", []),
        SetState("selected_pin", EMPTY_PIN_STATE),
        # Clear loading gate last so UI sees complete data in one frame.
        SetState("context_loading", False),
    ]


def _row_click_actions(
    *,
    connector_id_key: str,
    version_tag_key: str,
) -> list:
    """Build on_row_click actions for any tab's DataTable.

    Uses EVENT attribute access via getattr-style keys to read the correct
    fields from the clicked row dict.
    """
    connector_id_ref = getattr(EVENT, connector_id_key)
    version_tag_ref = getattr(EVENT, version_tag_key)

    return [
        # Immediately invalidate stale content in lower sections.
        SetState("context_loading", True),
        SetState("context_error", ""),
        SetState("active_rollouts", []),
        SetState("version_pins", []),
        SetState("version_pins_total", 0),
        SetState("selected_pin_index", -1),
        SetState("selected_pin_checks", []),
        SetState("selected_pin", EMPTY_PIN_STATE),
        SetState("selected_rollout", EMPTY_ROLLOUT_STATE),
        SetState("selected_version_release_date", ""),
        SetState("latest_version_release_date", ""),
        SetState("selected_version_display", ""),
        SetState("default_version_display", ""),
        # Invalidate stale yank detail for the previously-selected version.
        SetState("selected_version_yanked", False),
        SetState("selected_version_yank_yanked_at", ""),
        SetState("selected_version_yank_yanked_at_display", ""),
        SetState("selected_version_yank_reason", ""),
        SetState("selected_version_yank_approval_url", ""),
        SetState("selected_version_yank_raw", ""),
        # Set selected version / connector refs for context call.
        SetState("selected_connector_id", connector_id_ref),
        SetState("target_version", version_tag_ref),
        SetState("selected_version_tag", version_tag_ref),
        *start_tool_call("Loading connector version context…"),
        CallTool(
            load_connector_version_context,
            arguments={
                "connector_id": connector_id_ref,
                "version_tag": version_tag_ref,
                "scope_type": STATE.scope_type,
                "scope_id": STATE.scope_id,
                "actor_workspace_id": STATE.actor_workspace_id,
                "context_guid": STATE.context_guid,
                "auth_bearer_token": STATE.auth_bearer_token,
            },
            on_success=_version_context_success_actions(),
            on_error=fail_context_actions(),
        ),
    ]
