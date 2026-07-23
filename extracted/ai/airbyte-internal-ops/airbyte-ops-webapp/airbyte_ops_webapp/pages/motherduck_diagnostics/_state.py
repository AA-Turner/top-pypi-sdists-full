"""Typed Prefab state model for the MotherDuck Diagnostics page.

`MotherDuckDiagnosticsPageState` is the single source of truth for the page's
initial state. It extends the shared `OpsPageState` (env / deploy / auth) and
adds only the page-specific keys. Building initial state through this model means
a mistyped, missing, or extra initial-state key fails at page-build / type-check
time instead of silently in the browser.

The page is organized as three lazily-loaded top-level tabs (Recent Activity
Summary, Recent Queries, Active Connections); each tab owns a `*_loaded`
sentinel so its data is fetched only on first activation.
"""

from __future__ import annotations

from pydantic import Field

from airbyte_ops_webapp.pages.motherduck_diagnostics.defaults import (
    DEFAULT_LOOKBACK_HOURS,
    DEFAULT_QUERY_MODE,
    DEFAULT_SUMMARY_OPTION,
)
from airbyte_ops_webapp.state import OpsPageState


class MotherDuckDiagnosticsPageState(OpsPageState):
    """Complete initial Prefab state for the MotherDuck Diagnostics page."""

    # Active top-level tab. Each tab loads its data lazily on first activation.
    diagnostics_tab: str = "recent_activity_summary"

    # --- Recent Activity Summary tab ---
    summary_loaded: bool = False
    summary_error: str = ""
    # Selected period/grain option key (`24h`/`48h`/`7d`/`14d`). Changing it
    # re-runs the server-side aggregate and drives every Summary graph + KPI.
    summary_option: str = DEFAULT_SUMMARY_OPTION
    # Human-readable window label for the selected option, e.g. `last 24 hours`.
    summary_window_label: str = ""
    compute_usage_rows: list[dict[str, object]] = Field(default_factory=list)
    # Headline counts are pre-formatted with thousands separators server-side,
    # so they are carried as display strings rather than raw ints.
    summary_total_compute: str = "0"
    summary_query_count: str = "0"
    summary_failed_count: str = "0"
    # Summary "Show errors" drill-down: the failed queries within the selected
    # period, fetched on demand and reset whenever the period changes.
    summary_errors_loaded: bool = False
    summary_errors_loading: bool = False
    summary_errors_error: str = ""
    summary_errors_window_label: str = ""
    summary_error_rows: list[dict[str, object]] = Field(default_factory=list)

    # --- Recent Queries tab ---
    recent_queries_loaded: bool = False
    recent_queries_loading: bool = False
    recent_queries_error: str = ""
    # Lookback window (hours). Changing it re-executes the query tool.
    recent_query_lookback_hours: str = str(DEFAULT_LOOKBACK_HOURS)
    # Top-level modality (all / failed / slow / very slow). Changing it re-runs
    # the query tool server-side so rare errored/slow rows are fetched directly.
    recent_query_mode: str = DEFAULT_QUERY_MODE
    # Local-only refinements. Changing either never re-queries MotherDuck — the
    # filter tool re-slices the already-loaded rows in memory.
    recent_query_type: str = ""
    recent_query_subtype: str = ""
    # The full loaded dataset (privacy-safe rows), fed back to the in-memory
    # filter tool, plus the currently-visible filtered subset the table binds to.
    recent_query_rows_all: list[dict[str, object]] = Field(default_factory=list)
    recent_query_visible_rows: list[dict[str, object]] = Field(default_factory=list)
    # Dynamic filter chips derived from the loaded dataset. Subtype chips are
    # empty until a query type is selected (progressive disclosure).
    recent_query_type_options: list[dict[str, str]] = Field(default_factory=list)
    recent_query_subtype_options: list[dict[str, str]] = Field(default_factory=list)

    # --- Per-query detail modal (treated/redacted query text only) ---
    query_detail_open: bool = False
    query_detail_hash: str = ""
    query_detail_type: str = ""
    query_detail_subtype: str = ""
    # Owning Sonar source (database + parsed source UUID) for the selected query.
    query_detail_database_display: str = ""
    query_detail_source_id_display: str = ""
    query_detail_user: str = ""
    query_detail_start: str = ""
    # The detail modal shows all three timings; the table shows only elapsed+wait.
    query_detail_elapsed: str = ""
    query_detail_wait: str = ""
    query_detail_execution: str = ""
    query_detail_status: str = ""
    query_detail_error: str = ""
    query_detail_error_message: str = ""
    query_detail_text: str = ""

    # --- Active Connections tab ---
    active_connections_loaded: bool = False
    active_connections_error: str = ""
    active_connection_rows: list[dict[str, object]] = Field(default_factory=list)
