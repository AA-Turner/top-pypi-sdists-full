"""Connector Version Manager page-specific UI components."""

from prefab_ui.components import (
    H2,
    CardContent,
    CardHeader,
    Column,
    DataTable,
    DataTableColumn,
    Div,
    Grid,
    Markdown,
    Muted,
    Row,
    Small,
    Text,
)
from prefab_ui.components.control_flow import If
from prefab_ui.rx import STATE

from airbyte_ops_webapp.theme import PANEL_CARD_CLASS, STATUS_CARD_CLASS, _card_style


def _version_table_container_style() -> dict[str, str]:
    return {
        "maxHeight": "20rem",
        "overflowY": "auto",
        "paddingRight": "0.25rem",
    }


def render_status_cards() -> None:
    with Grid(columns=3, gap=4):
        with (
            Div(css_class=STATUS_CARD_CLASS, style=_card_style()),
            CardContent(),
            Column(gap=1),
        ):
            Small("Selected connector")
            Text(content=STATE.selected_connector.name, css_class="airbyte-stat-value")
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


def render_recent_releases_and_rollout_context() -> None:
    with Grid(columns=[1, 1], gap=4):
        with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
            with CardHeader():
                H2("Recent releases")
            with CardContent(), Column(gap=3):
                Text("Latest published versions for the selected connector.")
                with Div(style=_version_table_container_style()):
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
                    )
        with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
            with CardHeader():
                H2("Active rollout")
            with CardContent(), Column(gap=3):
                Text("Active progressive rollouts for the selected connector.")
                with If(STATE.rollout_error):
                    Text(content=STATE.rollout_error)
                DataTable(
                    columns=[
                        DataTableColumn(key="state", header="State"),
                        DataTableColumn(key="rc_docker_image_tag", header="RC"),
                        DataTableColumn(
                            key="initial_docker_image_tag",
                            header="Initial",
                        ),
                        DataTableColumn(
                            key="current_target_rollout_pct",
                            header="Target %",
                        ),
                        DataTableColumn(key="updated_at", header="Updated"),
                    ],
                    rows=STATE.active_rollouts,
                    pageSize=5,
                )


def render_pin_status() -> None:
    with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
        with CardHeader():
            H2("Pin status")
        with CardContent(), Column(gap=3):
            with Row(gap=2):
                Markdown("**Resolved context**")
                with If(STATE.resolved_context_label):  # noqa: SIM117
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
