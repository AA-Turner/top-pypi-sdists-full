"""Lazy tab-loading tools for the MotherDuck Diagnostics page.

This module owns the `FastMCPApp` that the page's `.ui()` provider attaches to,
plus one loader tool per top-level tab so each tab fetches its data only on
first activation (and, for Recent Queries, on explicit lookback change or
refresh). These tools are an internal presentation layer for Prefab reactive
bindings, but — per the repo's typed-result guidance — they still return typed
Pydantic models rather than plain dicts. FastMCP serializes each model to the
same JSON the `RESULT.*` / `SetState` bindings read, so typing them is
transparent to the UI while giving the loaders a schema and validation.

Live query rows are fetched already-treated (string literals redacted,
truncated) so the only query text that can reach the browser is the safe form
surfaced in the detail modal; the Summary aggregate reads no query text at all.
The top-level modality (all / failed / slow / very slow) re-queries MotherDuck
server-side (`load_recent_queries_tab`), since those rare rows would otherwise be
sampled out of the newest capped set; the native `query_type` / regex
`query_subtype` chips then refine that dataset entirely in memory
(`filter_recent_queries`) without re-querying.
"""

from __future__ import annotations

from fastmcp import FastMCPApp
from pydantic import BaseModel, Field

from airbyte_ops_webapp.pages.motherduck_diagnostics._data import (
    ComputeUsageChartRow,
    ConnectionDisplayRow,
    RecentQueryView,
    SummaryErrorRows,
    build_recent_query_view,
    load_active_connection_rows,
    load_recent_query_rows,
    load_summary_data,
    load_summary_error_rows,
)
from airbyte_ops_webapp.pages.motherduck_diagnostics.defaults import (
    DEFAULT_LOOKBACK_HOURS,
    DEFAULT_QUERY_MODE,
    DEFAULT_SUMMARY_OPTION,
)
from airbyte_ops_webapp.pages.motherduck_diagnostics.sample_data import QueryRow

motherduck_diagnostics_app = FastMCPApp("MotherDuck Diagnostics")


class SummaryTabResult(BaseModel):
    """Recent Activity Summary tab payload for a selected period/grain option.

    The compute-usage rows are typed `ComputeUsageChartRow` models: each row's
    `qt_*` stack series come from a fixed, finite key set (`KNOWN_QUERY_TYPES` +
    `OTHER_QUERY_TYPE`), so there is no dynamic-key dict here.
    """

    compute_usage_rows: list[ComputeUsageChartRow] = Field(default_factory=list)
    summary_total_compute: str = "0"
    summary_query_count: str = "0"
    summary_failed_count: str = "0"
    summary_window_label: str = ""
    error: str = ""


class RecentQueriesTabResult(RecentQueryView):
    """Initial Recent Queries payload: the mode's dataset plus the default view.

    Extends `RecentQueryView` (the in-memory-filtered visible subset and the
    filter chips) with `rows_all` — the full privacy-safe dataset for the
    selected mode, fed back into `filter_recent_queries` for subsequent in-memory
    `query_type` / `subtype` filtering.
    """

    rows_all: list[QueryRow] = Field(default_factory=list)
    error: str = ""


class ActiveConnectionsTabResult(BaseModel):
    """Active Connections tab payload (live server connections, no filters)."""

    rows: list[ConnectionDisplayRow] = Field(default_factory=list)
    error: str = ""


@motherduck_diagnostics_app.tool()
def load_summary_tab(
    summary_option: str = DEFAULT_SUMMARY_OPTION,
) -> SummaryTabResult:
    """Load the Recent Activity Summary tab for a selected period/grain option.

    The `summary_option` key (`24h`/`48h`/`7d`/`14d`) selects a coupled lookback
    window and grain; every returned graph row and headline count reflects that
    server-side aggregate.
    """
    data = load_summary_data(summary_option)
    return SummaryTabResult(
        compute_usage_rows=data.compute_usage,
        summary_total_compute=f"{data.total_compute_seconds:,.0f}",
        summary_query_count=f"{data.query_count:,}",
        summary_failed_count=f"{data.failed_count:,}",
        summary_window_label=data.window_label,
        error=data.error,
    )


@motherduck_diagnostics_app.tool()
def load_summary_errors_tab(
    summary_option: str = DEFAULT_SUMMARY_OPTION,
) -> SummaryErrorRows:
    """Load the failed queries within the selected Summary period/grain window.

    Backs the Summary tab's *Show errors* drill-down: fetches only failed rows
    (`error_only`, server-side) scoped to the same lookback window the selected
    `summary_option` drives, so the list matches the Summary charts above it.
    """
    return load_summary_error_rows(summary_option)


@motherduck_diagnostics_app.tool()
def load_recent_queries_tab(
    lookback_hours: int = DEFAULT_LOOKBACK_HOURS,
    mode: str = DEFAULT_QUERY_MODE,
) -> RecentQueriesTabResult:
    """Load Recent Queries for a lookback window and top-level modality.

    Fetches the query dataset for the selected `mode` (all / failed / slow / very
    slow, applied server-side) and returns both the full privacy-safe row set
    (fed back to `filter_recent_queries` for in-memory `query_type` / `subtype`
    filtering) and the initial visible subset. A lookback change, mode change, or
    explicit refresh calls this tool again.
    """
    data = load_recent_query_rows(lookback_hours=lookback_hours, mode=mode)
    rows: list[QueryRow] = data.rows
    view = build_recent_query_view(rows, query_type="", subtype="")
    return RecentQueriesTabResult(
        rows_all=[dict(row) for row in rows],
        visible_rows=view.visible_rows,
        query_type_options=view.query_type_options,
        subtype_options=view.subtype_options,
        error=data.error,
    )


@motherduck_diagnostics_app.tool()
def filter_recent_queries(
    rows: list[QueryRow],
    query_type: str = "",
    subtype: str = "",
) -> RecentQueryView:
    """Re-filter the mode's already-loaded rows in memory (no MotherDuck).

    Receives the rows already fetched for the current lookback and modality plus
    the selected native `query_type` / regex `query_subtype`, then returns the
    combined visible subset plus the (progressively-disclosed) subtype chips. No
    MotherDuck query is issued.
    """
    return build_recent_query_view(rows, query_type=query_type, subtype=subtype)


@motherduck_diagnostics_app.tool()
def load_active_connections_tab() -> ActiveConnectionsTabResult:
    """Load the Active Connections tab (live server connections, no filters)."""
    data = load_active_connection_rows()
    return ActiveConnectionsTabResult(rows=data.rows, error=data.error)
