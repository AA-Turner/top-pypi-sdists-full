"""Connector Version Manager page-specific UI components."""

from prefab_ui.components import (
    H2,
    H3,
    CardContent,
    CardHeader,
    Column,
    DataTable,
    DataTableColumn,
    Div,
    Grid,
    Markdown,
    Muted,
    Small,
    Text,
)
from prefab_ui.rx import STATE

from airbyte_ops_webapp.theme import PANEL_CARD_CLASS, STATUS_CARD_CLASS, _card_style


def render_status_cards() -> None:
    with Grid(columns=3, gap=4):
        with (
            Div(css_class=STATUS_CARD_CLASS, style=_card_style()),
            CardContent(),
            Column(gap=1),
        ):
            Small("Selected connector")
            H3(STATE.selected_connector.name)
            Muted(STATE.selected_connector.id)
        with (
            Div(css_class=STATUS_CARD_CLASS, style=_card_style()),
            CardContent(),
            Column(gap=1),
        ):
            Small("Latest version")
            H3(STATE.selected_connector.latest_version)
            Muted("Registry latest")
        with (
            Div(css_class=STATUS_CARD_CLASS, style=_card_style()),
            CardContent(),
            Column(gap=1),
        ):
            Small("Docker repository")
            H3(STATE.selected_connector.docker_repository)
            Muted(STATE.selected_connector.connector_type)


def render_recent_releases_and_rollout_context() -> None:
    with Grid(columns=[1, 1], gap=4):
        with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
            with CardHeader():
                H2("Recent releases")
            with CardContent(), Column(gap=3):
                Text("Latest published versions for the selected connector.")
                DataTable(
                    columns=[
                        DataTableColumn(
                            key="docker_image_tag",
                            header="Version",
                            sortable=True,
                        ),
                        DataTableColumn(
                            key="last_published",
                            header="Published",
                            sortable=True,
                        ),
                        DataTableColumn(key="release_stage", header="Stage"),
                    ],
                    rows=STATE.versions,
                    paginated=True,
                    pageSize=5,
                )
        with Div(css_class=PANEL_CARD_CLASS, style=_card_style()):
            with CardHeader():
                H2("Rollout context")
            with CardContent(), Column(gap=3):
                Markdown("**Active version state**")
                with Grid(columns=3, gap=3):
                    with Column(gap=1):
                        Small("Active")
                        H3(STATE.current_state.active_version)
                    with Column(gap=1):
                        Small("Latest")
                        H3(STATE.current_state.latest_version)
                    with Column(gap=1):
                        Small("Pinned scope")
                        H3(STATE.current_state.active_scope)
                Markdown("**Parent pins**")
                DataTable(
                    columns=[
                        DataTableColumn(key="scope_type", header="Scope"),
                        DataTableColumn(key="scope_id", header="Scope ID"),
                        DataTableColumn(key="value_name", header="Version"),
                    ],
                    rows=STATE.ancestor_configs,
                    paginated=True,
                    pageSize=3,
                )
                Markdown("**Child pins**")
                DataTable(
                    columns=[
                        DataTableColumn(key="scope_type", header="Scope"),
                        DataTableColumn(key="scope_id", header="Scope ID"),
                        DataTableColumn(key="value_name", header="Version"),
                    ],
                    rows=STATE.descendant_configs,
                    paginated=True,
                    pageSize=3,
                )
