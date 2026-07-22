"""MotherDuck Diagnostics page.

Three lazily-loaded top-level tabs over MotherDuck activity:

1. **Recent Activity Summary** — a compute-usage chart split by native query
   type plus a succeeded/failed outcome chart and headline KPIs, all driven by a
   compact period/grain selection control (24h/48h hourly, 7d/14d daily).
2. **Recent Queries** — a query-outcome table over a selectable lookback window
   with outcome, native `query_type`, and (progressively-disclosed) regex
   `query_subtype` filters that refine the loaded rows in memory, plus a
   per-row detail modal showing the redacted query text.
3. **Active Connections** — live server connections (no limits or filters).

Each tab fetches its data only on first activation (mirroring the Connector
Version Manager lazy-tab pattern), via the loader tools in `_mcp_tools`.

No verbatim SQL is surfaced anywhere: list rows are keyed by a short
`query_hash`, native `query_type`, and regex `query_subtype`; the detail modal
shows only the redacted/truncated query text (string literals replaced with `?`).
"""

# ruff: noqa: SIM117

from __future__ import annotations

from fastmcp import FastMCP
from prefab_ui.actions import SetState
from prefab_ui.actions.mcp import CallTool
from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    Button,
    CardContent,
    CardHeader,
    Code,
    Column,
    DataTable,
    DataTableColumn,
    Dialog,
    Div,
    Grid,
    Markdown,
    Metric,
    Muted,
    Row,
    Select,
    SelectOption,
    Tab,
    Tabs,
    Text,
)
from prefab_ui.components.charts import BarChart, ChartSeries
from prefab_ui.components.control_flow import Else, ForEach, If
from prefab_ui.rx import EVENT, RESULT, STATE

from airbyte_ops_webapp.app_shell import build_ops_app
from airbyte_ops_webapp.auth.oauth import hydrate_oauth_action, oauth_config
from airbyte_ops_webapp.pages.motherduck_diagnostics._data import (
    present_error_type_keys,
)
from airbyte_ops_webapp.pages.motherduck_diagnostics._mcp_tools import (
    filter_recent_queries,
    load_active_connections_tab,
    load_recent_queries_tab,
    load_summary_errors_tab,
    load_summary_tab,
    motherduck_diagnostics_app,
)
from airbyte_ops_webapp.pages.motherduck_diagnostics._state import (
    MotherDuckDiagnosticsPageState,
)
from airbyte_ops_webapp.pages.motherduck_diagnostics.agents import (
    MOTHERDUCK_DIAGNOSTICS_AGENTS_CALLOUT,
)
from airbyte_ops_webapp.pages.motherduck_diagnostics.defaults import (
    DEFAULT_LOOKBACK_HOURS,
    KNOWN_ERROR_TYPES,
    LOOKBACK_OPTIONS_HOURS,
    MOTHERDUCK_DIAGNOSTICS_EMOJI,
    MOTHERDUCK_DIAGNOSTICS_TOOL_NAME,
    OTHER_ERROR_TYPE,
    QUERY_MODES,
    SUMMARY_OPTIONS,
)
from airbyte_ops_webapp.pages.shared_components.layout import (
    render_breadcrumb_nav,
    render_environment_banners,
    render_page_hero,
    render_version_footer,
)
from airbyte_ops_webapp.state import OAuthConfigState
from airbyte_ops_webapp.theme import (
    AIRBYTE_PRIMARY,
    PAGE_CLASS,
    AbCard,
    AbErrorCard,
    AbFieldLabel,
    AbPage,
    AbSectionTitle,
    AbStatusCard,
    AbTableScroll,
)

# Failure accent for the query-outcome chart, matching the theme's destructive
# red so failed queries read as an alert against the primary (succeeded) bars.
_FAILED_COLOR = "#B42318"

# Fixed compute-usage stack series keyed by native `QUERY_TYPE` (unknown types
# fold into `qt_OTHER`), so the stacked chart binds to a known, finite set.
_COMPUTE_TYPE_SERIES: list[tuple[str, str, str]] = [
    ("QUERY", "Query", AIRBYTE_PRIMARY),
    ("DML", "DML", "#2E7D6B"),
    ("DDL", "DDL", "#B7791F"),
    ("UNKNOWN", "Unknown", "#6B7280"),
    ("OTHER", "Other", "#9CA3AF"),
]

# Catalog of "Failed queries" stack series keyed by native `ERROR_TYPE` (types
# outside `KNOWN_ERROR_TYPES` fold into `et_OTHER`). Colors span distinct
# warm/alert hues (red → orange → gold → violet → slate → pink) rather than a
# single red family, so adjacent stack segments and legend entries stay visually
# separable. Keys and order mirror `KNOWN_ERROR_TYPES` + the catch-all. This is
# the full catalog; `_render_failed_queries_section` renders only the subset of
# error types actually present in the data (see `present_error_type_keys`).
_ERROR_TYPE_SERIES: list[tuple[str, str, str]] = [
    ("OutOfMemory", "Out of memory", "#B42318"),
    ("QueryTimeout", "Query timeout", "#EA7317"),
    ("PermissionDenied", "Permission denied", "#CA8A04"),
    ("Connection", "Connection", "#7C3AED"),
    ("UNKNOWN", "Unknown", "#64748B"),
    ("OTHER", "Other", "#DB2777"),
]

# Guard against drift between the failed-queries series and the error-type
# constants (and thus the `et_*` chart-row fields) they must bind to.
assert {key for key, _, _ in _ERROR_TYPE_SERIES} == {
    *KNOWN_ERROR_TYPES,
    OTHER_ERROR_TYPE,
}


@motherduck_diagnostics_app.ui(
    name=MOTHERDUCK_DIAGNOSTICS_TOOL_NAME,
    title="MotherDuck Diagnostics",
    description="Compute usage, recent queries, and live connections for MotherDuck.",
)
def motherduck_diagnostics() -> PrefabApp:
    """Open the MotherDuck Diagnostics page."""
    current_oauth_config = oauth_config()
    state = _build_initial_state(current_oauth_config=current_oauth_config)

    with build_ops_app(
        title=f"{MOTHERDUCK_DIAGNOSTICS_EMOJI} MotherDuck Diagnostics",
        state=state,
        oauth_issuer=current_oauth_config.issuer,
    ) as app:
        with AbPage(onMount=hydrate_oauth_action()):
            with Column(gap=5, css_class=PAGE_CLASS):
                render_environment_banners()
                render_breadcrumb_nav(
                    current_page=f"{MOTHERDUCK_DIAGNOSTICS_EMOJI} MotherDuck Diagnostics",
                )
                render_page_hero(
                    title=f"{MOTHERDUCK_DIAGNOSTICS_EMOJI} MotherDuck Diagnostics",
                    description=(
                        "Compute-usage analytics, recent query outcomes, and live "
                        "server connections for MotherDuck. Verbatim SQL is never "
                        "shown — queries are keyed by a short query_hash, native "
                        "query_type, and subtype, and the per-query detail modal "
                        "shows only redacted query text."
                    ),
                    show_auth_controls=True,
                    agents_callout=MOTHERDUCK_DIAGNOSTICS_AGENTS_CALLOUT,
                )
                with Tabs(
                    name="diagnostics_tab",
                    value=state["diagnostics_tab"],
                    variant="line",
                ):
                    with Tab(
                        "Recent Activity Summary", value="recent_activity_summary"
                    ):
                        _render_summary_tab()
                    with Tab("Recent Queries", value="recent_queries"):
                        _render_recent_queries_tab()
                    with Tab("Active Connections", value="active_connections"):
                        _render_active_connections_tab()
                _render_query_detail_modal()
                render_version_footer()

    return app


# ---------------------------------------------------------------------------
# Tab 1: Recent Activity Summary (compute usage + headline KPIs)
# ---------------------------------------------------------------------------


def _summary_success_actions() -> list:
    return [
        SetState("compute_usage_rows", RESULT.compute_usage_rows),
        SetState("summary_total_compute", RESULT.summary_total_compute),
        SetState("summary_query_count", RESULT.summary_query_count),
        SetState("summary_failed_count", RESULT.summary_failed_count),
        SetState("summary_window_label", RESULT.summary_window_label),
        SetState("summary_error", RESULT.error),
        SetState("summary_loaded", True),
    ]


def _summary_error_actions() -> list:
    return [
        SetState("summary_loaded", True),
        SetState("summary_error", "Failed to load recent activity summary."),
    ]


def _reload_summary() -> list:
    """Re-run the Summary aggregate for the currently-selected period/grain.

    Reads `summary_option` from state, so callers must commit the intended
    option key via `SetState` before invoking this.
    """
    return [
        # Changing the period invalidates any drill-down list fetched for the
        # prior window, so collapse it until the user re-requests it.
        SetState("summary_errors_loaded", False),
        SetState("summary_errors_error", ""),
        SetState("summary_error_rows", []),
        CallTool(
            load_summary_tab,
            arguments={"summary_option": STATE.summary_option},
            on_success=_summary_success_actions(),
            on_error=_summary_error_actions(),
        ),
    ]


def _render_summary_tab() -> None:
    with (
        If(STATE.summary_loaded.__eq__(False)),
        Div(
            on_mount=[
                CallTool(
                    load_summary_tab,
                    arguments={"summary_option": STATE.summary_option},
                    on_success=_summary_success_actions(),
                    on_error=_summary_error_actions(),
                ),
            ],
        ),
    ):
        Muted("Loading recent activity summary\u2026")

    with If(STATE.summary_loaded.__eq__(True)):
        with Column(gap=4):
            _render_summary_period_control()
            with If(STATE.summary_error):
                with AbErrorCard(), CardContent(), Column(gap=1):
                    Markdown("**Unable to load diagnostics**")
                    Text(STATE.summary_error)
            with If(STATE.summary_error.__eq__("")):
                Muted(
                    "Aggregated over the " + STATE.summary_window_label + " (UTC).",
                )
                _render_kpi_row()
                _render_compute_usage_section()
                _render_queries_executed_section()
                _render_failed_queries_section()
                _render_summary_errors_section()


def _render_summary_period_control() -> None:
    with Row(gap=2, css_class="items-center flex-wrap"):
        AbFieldLabel("Period")
        for option in SUMMARY_OPTIONS:
            with If(STATE.summary_option.__eq__(option.key)):
                Button(
                    option.label,
                    variant="default",
                    size="sm",
                    on_click=[
                        SetState("summary_option", option.key),
                        *_reload_summary(),
                    ],
                )
            with Else():
                Button(
                    option.label,
                    variant="outline",
                    size="sm",
                    on_click=[
                        SetState("summary_option", option.key),
                        *_reload_summary(),
                    ],
                )


def _render_kpi_row() -> None:
    with Grid(columns=3, gap=3):
        with AbStatusCard(), CardContent():
            Metric(
                label="Compute-seconds",
                value=STATE.summary_total_compute,
                description="Sum of query execution time",
            )
        with AbStatusCard(), CardContent():
            Metric(
                label="Queries",
                value=STATE.summary_query_count,
                description="Total queries in the window",
            )
        with AbStatusCard(), CardContent():
            Metric(
                label="Failed queries",
                value=STATE.summary_failed_count,
                description="Queries that ended with an error",
            )


def _render_compute_usage_section() -> None:
    with AbCard():
        with CardHeader(), Column(gap=1):
            AbSectionTitle("Compute usage")
            AbFieldLabel(
                "Aggregate compute-seconds per bucket, split by MotherDuck's "
                "native query type. This is the proxy for MotherDuck spend.",
            )
        with CardContent():
            BarChart(
                data=STATE.compute_usage_rows,
                series=[
                    ChartSeries(data_key=f"qt_{key}", label=label, color=color)
                    for key, label, color in _COMPUTE_TYPE_SERIES
                ],
                x_axis="bucket",
                height=320,
                stacked=True,
                show_legend=True,
                y_axis_format="compact",
            )


def _render_queries_executed_section() -> None:
    with AbCard():
        with CardHeader(), Column(gap=1):
            AbSectionTitle("Queries executed")
            AbFieldLabel(
                "Succeeded vs. failed queries per bucket over the same window. "
                "Failed queries are stacked in red on top of succeeded ones.",
            )
        with CardContent():
            BarChart(
                data=STATE.compute_usage_rows,
                series=[
                    ChartSeries(
                        data_key="succeeded",
                        label="Succeeded",
                        color=AIRBYTE_PRIMARY,
                    ),
                    ChartSeries(
                        data_key="failed",
                        label="Failed",
                        color=_FAILED_COLOR,
                    ),
                ],
                x_axis="bucket",
                height=320,
                stacked=True,
                show_legend=True,
                y_axis_format="compact",
            )


def _render_failed_queries_section() -> None:
    # Declare a series only for error types actually present in the data (probed
    # over the widest window at build time), so empty types drop out of both the
    # graph and the legend rather than cluttering it with flat zero series.
    present = set(present_error_type_keys())
    series = [
        ChartSeries(data_key=f"et_{key}", label=label, color=color)
        for key, label, color in _ERROR_TYPE_SERIES
        if key in present
    ]
    with AbCard():
        with CardHeader(), Column(gap=1):
            AbSectionTitle("Failed queries")
            AbFieldLabel(
                "Failed queries per bucket over the same window, stacked by "
                "MotherDuck's native error type and charted on their own scale so "
                "error trends are not dwarfed by successful queries. Only error "
                "types present in the data are shown.",
            )
        with CardContent():
            BarChart(
                data=STATE.compute_usage_rows,
                series=series,
                x_axis="bucket",
                height=280,
                stacked=True,
                show_legend=True,
                y_axis_format="compact",
            )


def _load_summary_errors() -> list:
    """Fetch the failed queries within the currently-selected Summary period.

    A period-level drill-down keyed off `summary_option` (Prefab `BarChart` has
    no per-bar selection), fetched `error_only` server-side and rendered in the
    same privacy-safe row view as the Recent Queries table.
    """
    return [
        SetState("summary_errors_loading", True),
        CallTool(
            load_summary_errors_tab,
            arguments={"summary_option": STATE.summary_option},
            on_success=[
                SetState("summary_error_rows", RESULT.visible_rows),
                SetState("summary_errors_window_label", RESULT.window_label),
                SetState("summary_errors_error", RESULT.error),
                SetState("summary_errors_loaded", True),
                SetState("summary_errors_loading", False),
            ],
            on_error=[
                SetState("summary_errors_error", "Failed to load failed queries."),
                SetState("summary_errors_loaded", True),
                SetState("summary_errors_loading", False),
            ],
        ),
    ]


def _render_summary_errors_section() -> None:
    with AbCard():
        with CardHeader(), Column(gap=1):
            AbSectionTitle("Failed query detail")
            AbFieldLabel(
                "Fetch the failed queries within the selected period and list "
                "them below. Click a row for the redacted SQL and error message.",
            )
        with CardContent(), Column(gap=3):
            Button(
                "Show errors",
                variant="outline",
                size="sm",
                on_click=_load_summary_errors(),
            )
            with If(STATE.summary_errors_loading.__eq__(True)):
                Muted("Loading failed queries\u2026")
            with If(STATE.summary_errors_error.__ne__("")):
                with AbErrorCard(), CardContent(), Column(gap=1):
                    Markdown("**Unable to load failed queries**")
                    Text(STATE.summary_errors_error)
            with If(STATE.summary_errors_loaded.__eq__(True)):
                with If(STATE.summary_errors_error.__eq__("")):
                    Muted(
                        "Failed queries in the "
                        + STATE.summary_errors_window_label
                        + " (UTC).",
                    )
                    with AbTableScroll():
                        DataTable(
                            columns=_QUERY_COLUMNS,
                            rows=STATE.summary_error_rows,
                            search=True,
                            on_row_click=_open_detail_actions(),
                        )


# ---------------------------------------------------------------------------
# Tab 2: Recent Queries (lookback + outcome/type/subtype filters + detail modal)
# ---------------------------------------------------------------------------


_QUERY_COLUMNS = [
    DataTableColumn(
        key="detail",
        header="",
        align="center",
        width="3rem",
    ),
    DataTableColumn(key="query_type", header="Type", sortable=True),
    DataTableColumn(key="query_subtype", header="Subtype", sortable=True),
    DataTableColumn(key="status", header="Status", sortable=True),
    DataTableColumn(key="error_type", header="Error Type", sortable=True),
    DataTableColumn(
        key="elapsed",
        header="Elapsed",
        align="right",
        header_class="normal-case",
    ),
    DataTableColumn(
        key="wait",
        header="Wait",
        align="right",
        header_class="normal-case",
    ),
    DataTableColumn(key="start_time_display", header="Start", sortable=True),
    DataTableColumn(key="user_name_display", header="User", sortable=True),
    DataTableColumn(key="query_hash_display", header="Query Hash", sortable=True),
    DataTableColumn(key="error_message", header="Error", sortable=True),
]


def _filter_success_actions() -> list:
    return [
        SetState("recent_query_visible_rows", RESULT.visible_rows),
        SetState("recent_query_type_options", RESULT.query_type_options),
        SetState("recent_query_subtype_options", RESULT.subtype_options),
    ]


def _apply_filter() -> list:
    """Re-slice the already-loaded rows in memory for the current selections.

    Passes the loaded row set (already narrowed server-side by the selected
    modality) plus the selected `query_type` / `subtype` to the in-memory filter
    tool — no MotherDuck query is issued. Callers must commit the changed
    selection via `SetState` before invoking this.
    """
    return [
        CallTool(
            filter_recent_queries,
            arguments={
                "rows": STATE.recent_query_rows_all,
                "query_type": STATE.recent_query_type,
                "subtype": STATE.recent_query_subtype,
            },
            on_success=_filter_success_actions(),
        ),
    ]


def _recent_success_actions() -> list:
    # After (re)loading the dataset, re-slice the visible rows for the *current*
    # query type / subtype selections so a refresh, lookback, or mode change
    # preserves the active refinements instead of snapping to defaults.
    return [
        SetState("recent_query_rows_all", RESULT.rows_all),
        SetState("recent_query_type_options", RESULT.query_type_options),
        SetState("recent_query_subtype_options", RESULT.subtype_options),
        SetState("recent_queries_error", RESULT.error),
        SetState("recent_queries_loaded", True),
        SetState("recent_queries_loading", False),
        *_apply_filter(),
    ]


def _recent_error_actions() -> list:
    return [
        SetState("recent_queries_loaded", True),
        SetState("recent_queries_loading", False),
        SetState("recent_queries_error", "Failed to load recent queries."),
    ]


def _reload_recent_queries() -> list:
    """Actions that re-execute the recent-queries tool for the current lookback.

    Reloading fetches a fresh dataset but preserves the active outcome / speed /
    query type / subtype selections — `_recent_success_actions` re-applies them
    to the reloaded rows. Reads the lookback from state, so callers must ensure
    `recent_query_lookback_hours` already holds the intended value (the refresh
    button re-runs the current selection; the lookback `Select` commits the new
    value via `SetState` before invoking this).
    """
    return [
        SetState("recent_queries_loading", True),
        CallTool(
            load_recent_queries_tab,
            arguments={
                "lookback_hours": STATE.recent_query_lookback_hours,
                "mode": STATE.recent_query_mode,
            },
            on_success=_recent_success_actions(),
            on_error=_recent_error_actions(),
        ),
    ]


def _render_recent_queries_tab() -> None:
    with (
        If(STATE.recent_queries_loaded.__eq__(False)),
        Div(
            on_mount=[
                CallTool(
                    load_recent_queries_tab,
                    arguments={
                        "lookback_hours": STATE.recent_query_lookback_hours,
                        "mode": STATE.recent_query_mode,
                    },
                    on_success=_recent_success_actions(),
                    on_error=_recent_error_actions(),
                ),
            ],
        ),
    ):
        Muted("Loading recent queries\u2026")

    with If(STATE.recent_queries_loaded.__eq__(True)):
        with AbCard():
            with CardHeader(), Column(gap=2):
                AbSectionTitle("Recent queries")
                AbFieldLabel(
                    "QUERY_HISTORY over the selected lookback window (includes "
                    "completed and errored queries). Filters refine the loaded "
                    "rows in memory — only a lookback change or refresh re-runs "
                    "the query. Click a row for the redacted query text. No "
                    "verbatim SQL — query_hash, type + subtype only.",
                )
                _render_recent_queries_controls()
            with CardContent(), Column(gap=3):
                with If(STATE.recent_queries_error):
                    with AbErrorCard(), CardContent(), Column(gap=1):
                        Markdown("**Unable to load recent queries**")
                        Text(STATE.recent_queries_error)
                _render_recent_queries_table()


def _render_recent_queries_controls() -> None:
    with Column(gap=2):
        with Row(gap=3, css_class="items-center flex-wrap justify-between"):
            with Row(gap=3, css_class="items-center flex-wrap"):
                with Row(gap=2, css_class="items-center"):
                    AbFieldLabel("Lookback")
                    with Select(
                        name="recent_query_lookback_hours",
                        value=str(DEFAULT_LOOKBACK_HOURS),
                        size="sm",
                        css_class="w-24",
                        onChange=[
                            SetState("recent_query_lookback_hours", EVENT),
                            *_reload_recent_queries(),
                        ],
                    ):
                        for hours in LOOKBACK_OPTIONS_HOURS:
                            SelectOption(value=str(hours), label=f"{hours}h")
                with Row(gap=2, css_class="items-center"):
                    AbFieldLabel("Show")
                    _render_mode_filters()
            with Row(gap=2, css_class="items-center"):
                with If(STATE.recent_queries_loading):
                    Muted("Refreshing\u2026")
                _render_refresh_button()
        _render_query_type_filters()
        _render_subtype_filters()


def _render_refresh_button() -> None:
    Button(
        label="",
        icon="refresh-cw",
        variant="outline",
        size="icon-sm",
        on_click=_reload_recent_queries(),
    )


def _render_mode_filters() -> None:
    # Top-level modality: all / failed / slow (inclusive of very slow) / very
    # slow. Selecting one re-runs the query server-side (rare errored/slow rows
    # would otherwise be sampled out of the newest capped set), so these carry no
    # count estimates. The query type / subtype chips then refine in memory.
    with Row(gap=2, css_class="flex-wrap"):
        for mode in QUERY_MODES:
            with If(STATE.recent_query_mode.__eq__(mode.key)):
                Button(
                    mode.label,
                    variant="default",
                    size="sm",
                    on_click=[
                        SetState("recent_query_mode", mode.key),
                        *_reload_recent_queries(),
                    ],
                )
            with Else():
                Button(
                    mode.label,
                    variant="outline",
                    size="sm",
                    on_click=[
                        SetState("recent_query_mode", mode.key),
                        *_reload_recent_queries(),
                    ],
                )


def _render_query_type_filters() -> None:
    with Row(gap=2, css_class="items-center flex-wrap"):
        AbFieldLabel("Query type")
        with ForEach(STATE.recent_query_type_options) as option:
            with If(STATE.recent_query_type.__eq__(option.value)):
                Button(
                    option.label,
                    variant="default",
                    size="sm",
                    on_click=[
                        SetState("recent_query_type", option.value),
                        SetState("recent_query_subtype", ""),
                        *_apply_filter(),
                    ],
                )
            with Else():
                Button(
                    option.label,
                    variant="outline",
                    size="sm",
                    on_click=[
                        SetState("recent_query_type", option.value),
                        SetState("recent_query_subtype", ""),
                        *_apply_filter(),
                    ],
                )


def _render_subtype_filters() -> None:
    # Subtype chips appear only after a query type is selected (progressive
    # disclosure); clearing the query type empties the options and hides them.
    with If(STATE.recent_query_type.__ne__("")):
        with Row(gap=2, css_class="items-center flex-wrap"):
            AbFieldLabel("Subtype")
            with ForEach(STATE.recent_query_subtype_options) as option:
                with If(STATE.recent_query_subtype.__eq__(option.value)):
                    Button(
                        option.label,
                        variant="default",
                        size="sm",
                        on_click=[
                            SetState("recent_query_subtype", option.value),
                            *_apply_filter(),
                        ],
                    )
                with Else():
                    Button(
                        option.label,
                        variant="outline",
                        size="sm",
                        on_click=[
                            SetState("recent_query_subtype", option.value),
                            *_apply_filter(),
                        ],
                    )


def _open_detail_actions() -> list:
    """Populate the detail modal from the clicked row, then open it.

    The row carries only privacy-safe fields (including the already-redacted
    query text), so no verbatim SQL reaches this state.
    """
    return [
        SetState("query_detail_hash", EVENT.query_hash_display),
        SetState("query_detail_type", EVENT.query_type),
        SetState("query_detail_subtype", EVENT.query_subtype),
        SetState("query_detail_user", EVENT.user_name),
        SetState("query_detail_start", EVENT.start_time),
        SetState("query_detail_elapsed", EVENT.elapsed),
        SetState("query_detail_wait", EVENT.wait),
        SetState("query_detail_execution", EVENT.execution),
        SetState("query_detail_status", EVENT.status_display),
        SetState("query_detail_error", EVENT.error_type),
        SetState("query_detail_error_message", EVENT.error_message),
        SetState("query_detail_text", EVENT.query_text_treated),
        SetState("query_detail_open", True),
    ]


def _render_recent_queries_table() -> None:
    with AbTableScroll():
        DataTable(
            columns=_QUERY_COLUMNS,
            rows=STATE.recent_query_visible_rows,
            search=True,
            on_row_click=_open_detail_actions(),
        )


def _detail_row(label: str, value) -> None:
    with Row(gap=2, css_class="items-baseline"):
        AbFieldLabel(label)
        Text(value)


def _render_query_detail_modal() -> None:
    with Dialog(
        title="Query detail",
        description="Redacted query text and metadata (no verbatim SQL).",
        name="query_detail_open",
    ):
        Div(css_class="hidden")
        with Column(gap=3):
            with Grid(columns=2, gap=2):
                # Left column: query identity. Right column: timing breakdown
                # (start, then total, then its execution/wait components).
                with Column(gap=2):
                    _detail_row("Query hash", STATE.query_detail_hash)
                    _detail_row("Query type", STATE.query_detail_type)
                    _detail_row("Subtype", STATE.query_detail_subtype)
                    _detail_row("User", STATE.query_detail_user)
                with Column(gap=2):
                    _detail_row("Start", STATE.query_detail_start)
                    _detail_row("Total elapsed", STATE.query_detail_elapsed)
                    _detail_row("Execution", STATE.query_detail_execution)
                    _detail_row("Wait", STATE.query_detail_wait)
            AbFieldLabel(
                "Redacted SQL — string literals replaced with ?, truncated to "
                "1000 characters."
            )
            Code(
                content=STATE.query_detail_text,
                language="sql",
                css_class="whitespace-pre-wrap break-words",
            )
            _detail_row("Status", STATE.query_detail_status)
            _detail_row("Error type", STATE.query_detail_error)
            with If(STATE.query_detail_error_message.__ne__("")):
                AbFieldLabel("Error message")
                # A code-block look (matching the SQL block) but plain text: the
                # renderer's `Code` always syntax-highlights (unknown languages
                # fall back to auto-detection), so the verbatim error message is
                # rendered in a styled `Div` instead.
                with Div(
                    css_class=(
                        "rounded-md bg-muted p-4 text-sm overflow-x-auto "
                        "font-mono whitespace-pre-wrap break-words"
                    ),
                ):
                    Text(STATE.query_detail_error_message)


# ---------------------------------------------------------------------------
# Tab 3: Active Connections (no limits or filters)
# ---------------------------------------------------------------------------


_CONNECTION_COLUMNS = [
    DataTableColumn(key="client_connection_id", header="Connection", sortable=True),
    DataTableColumn(key="client_user_agent", header="User Agent", sortable=True),
    DataTableColumn(key="server_transaction_stage", header="Txn Stage", sortable=True),
    DataTableColumn(
        key="server_query_elapsed_time",
        header="Elapsed",
        sortable=True,
        align="right",
        header_class="[&>button]:justify-end",
    ),
]


def _render_active_connections_tab() -> None:
    with (
        If(STATE.active_connections_loaded.__eq__(False)),
        Div(
            on_mount=[
                CallTool(
                    load_active_connections_tab,
                    on_success=[
                        SetState("active_connection_rows", RESULT.rows),
                        SetState("active_connections_error", RESULT.error),
                        SetState("active_connections_loaded", True),
                    ],
                    on_error=[
                        SetState("active_connections_loaded", True),
                        SetState(
                            "active_connections_error",
                            "Failed to load active connections.",
                        ),
                    ],
                ),
            ],
        ),
    ):
        Muted("Loading active connections\u2026")

    with If(STATE.active_connections_loaded.__eq__(True)):
        with AbCard():
            with CardHeader(), Column(gap=1):
                AbSectionTitle("Active connections")
                AbFieldLabel(
                    "Live server connections from md_active_server_connections(). "
                    "No raw client_query text is displayed.",
                )
            with CardContent(), Column(gap=3):
                with If(STATE.active_connections_error):
                    with AbErrorCard(), CardContent(), Column(gap=1):
                        Markdown("**Unable to load active connections**")
                        Text(STATE.active_connections_error)
                with AbTableScroll():
                    DataTable(
                        columns=_CONNECTION_COLUMNS,
                        rows=STATE.active_connection_rows,
                        search=True,
                    )


# ---------------------------------------------------------------------------
# State initialization + registration
# ---------------------------------------------------------------------------


def _build_initial_state(
    *,
    current_oauth_config: OAuthConfigState,
) -> dict[str, object]:
    return MotherDuckDiagnosticsPageState.from_env(
        oauth_config=current_oauth_config
    ).to_prefab_state()


def register_motherduck_diagnostics_app(mcp: FastMCP) -> None:
    """Register the MotherDuck Diagnostics app with the MCP server."""
    mcp.add_provider(motherduck_diagnostics_app)
