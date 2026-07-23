"""Data access for the MotherDuck Diagnostics page.

Loads compute usage, recent queries, and active connections either from live
MotherDuck (via the shared `airbyte_ops_mcp.motherduck_diagnostics` query
functions) or, when the app runs in mock-only mode, from `sample_data`.

Each top-level page tab has its own granular loader so the page can fetch data
lazily, one tab at a time:

- `load_summary_data` — server-side aggregate compute usage plus headline counts
  for a selected period/grain option.
- `load_recent_query_rows` — recent query rows for a lookback window.
- `load_active_connection_rows` — live server connections.

Privacy contract: normal list rows never carry verbatim SQL. Live query rows are
fetched with a `QueryTextTreatment` that redacts string literals to `?` and
truncates to 1000 characters, so the only query text that can reach the browser
(surfaced solely in the per-query detail modal) is the treated form. The
Summary aggregate reads no query text at all — it groups by MotherDuck's native
`QUERY_TYPE` server-side. Full raw SQL never reaches browser state.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from airbyte_ops_mcp.motherduck_diagnostics.models import (
    MotherDuckComputeUsageBucket,
    MotherDuckConnectionFilters,
    MotherDuckConnectionInfo,
    MotherDuckQueryFilters,
    MotherDuckQueryRecord,
    QueryTextTreatment,
)
from airbyte_ops_mcp.motherduck_diagnostics.queries import (
    query_active_connections,
    query_compute_usage_summary,
    query_motherduck_queries,
)
from pydantic import BaseModel, Field

from airbyte_ops_webapp.pages.motherduck_diagnostics.defaults import (
    DEFAULT_LOOKBACK_HOURS,
    DEFAULT_QUERY_MODE,
    DEFAULT_SUMMARY_OPTION,
    KNOWN_ERROR_TYPES,
    KNOWN_QUERY_TYPES,
    OTHER_ERROR_TYPE,
    OTHER_QUERY_TYPE,
    QUERY_MODE_FAILED,
    QUERY_MODES_BY_KEY,
    SUMMARY_OPTIONS_BY_KEY,
    WIDEST_SUMMARY_OPTION,
    QueryMode,
    SummaryOption,
)
from airbyte_ops_webapp.pages.motherduck_diagnostics.sample_data import (
    SAMPLE_ACTIVE_CONNECTIONS,
    SAMPLE_COMPUTE_BUCKETS_DAILY,
    SAMPLE_COMPUTE_BUCKETS_HOURLY,
    SAMPLE_RECENT_QUERIES,
    QueryRow,
)
from airbyte_ops_webapp.state import mock_only_enabled

# Cap on the number of detailed rows the Recent Queries tab pulls within its
# lookback window. This bounds the in-browser result set; the underlying query
# tool itself imposes no maximum.
_RECENT_QUERY_LIMIT = 999
_HASH_PREFIX_LEN = 8
# Error messages can be arbitrarily long; the table cell shows a truncated
# preview (full text remains in the detail modal) so one row can't blow out the
# table width. The column also has a CSS `max_width` cap as a second guard.
_ERROR_MESSAGE_PREVIEW_LEN = 80

# Detail-modal query-text treatment: redact string literals and truncate. This
# is the only query text allowed to reach the browser.
_DETAIL_TEXT_TREATMENT = QueryTextTreatment(
    char_limit=1000, redact_string_constants=True
)


class FilterChipOption(BaseModel):
    """A single filter-chip option: a bound `value` and its display `label`."""

    value: str
    label: str


class RecentQueryDisplayRow(BaseModel):
    """A `DataTable`-bound Recent Queries row (privacy-safe display projection).

    Every field is a pre-rendered string safe for the browser. The table shows
    `elapsed` (total wall-clock) and `wait` (queue time) side by side so the
    reader can mentally subtract to gauge compute time; `execution` (pure
    compute) is carried too for the detail modal, which shows all three. `status`
    is a human-readable outcome and `query_text_treated` is the
    redacted/truncated form (never verbatim SQL).
    """

    query_hash: str
    query_hash_display: str
    query_type: str
    query_subtype: str
    user_name: str
    user_name_display: str
    start_time: str
    start_time_display: str
    elapsed: str
    wait: str
    execution: str
    status: str
    status_display: str
    error_type: str
    error_message: str
    error_message_display: str
    detail: str
    query_text_treated: str
    # Owning Sonar source, parsed from the query's `iceberg_scan` S3 path. The
    # raw fields feed the detail modal; the `*_display` forms render `—` when
    # absent so an empty value reads as "not applicable", not a blank cell.
    database_name: str
    database_name_display: str
    source_id: str
    source_id_display: str


class ConnectionDisplayRow(BaseModel):
    """A `DataTable`-bound Active Connections row (no `client_query` text)."""

    client_connection_id: str
    client_user_agent: str
    server_transaction_stage: str
    server_query_elapsed_time: str
    database_name_display: str = "—"


class ComputeUsageChartRow(BaseModel):
    """A stacked-bar row for the Summary compute-usage chart.

    One row per aggregation bucket. `bucket` is the display label; `succeeded` /
    `failed` back the outcome chart; each `qt_*` field is the summed
    compute-seconds for one native `QUERY_TYPE` stack series. Native types
    outside `KNOWN_QUERY_TYPES` fold into `qt_OTHER`, so the series set is fixed
    and finite (it mirrors `KNOWN_QUERY_TYPES` + `OTHER_QUERY_TYPE`) rather than
    dynamic — hence a typed model rather than a dynamic-key `dict`. The `et_*`
    fields back the stacked "Failed queries" chart: each holds the bucket's
    failed count for one native `ERROR_TYPE`, with the same fixed/finite series
    scheme (`KNOWN_ERROR_TYPES` + `OTHER_ERROR_TYPE`).
    """

    bucket: str
    compute_seconds: float = 0.0
    succeeded: int = 0
    failed: int = 0
    # The `qt_*` field names must match the native uppercase `QUERY_TYPE` values
    # (via `qt_{QUERY_TYPE}`) so the stacked chart's `ChartSeries` data keys bind
    # directly, hence the mixed-case names.
    qt_QUERY: float = 0.0  # noqa: N815
    qt_DML: float = 0.0  # noqa: N815
    qt_DDL: float = 0.0  # noqa: N815
    qt_UNKNOWN: float = 0.0  # noqa: N815
    qt_OTHER: float = 0.0  # noqa: N815
    # The `et_*` field names mirror `KNOWN_ERROR_TYPES` (+ `OTHER_ERROR_TYPE`)
    # via `et_{ERROR_TYPE}` so the stacked "Failed queries" chart binds its
    # per-error-type `ChartSeries` directly; each holds that bucket's failed
    # count for one native `ERROR_TYPE`.
    et_OutOfMemory: int = 0  # noqa: N815
    et_QueryTimeout: int = 0  # noqa: N815
    et_PermissionDenied: int = 0  # noqa: N815
    et_Connection: int = 0  # noqa: N815
    et_UNKNOWN: int = 0  # noqa: N815
    et_OTHER: int = 0  # noqa: N815

    def error_counts(self) -> dict[str, int]:
        """Return this bucket's failed counts keyed by native error type.

        Keys mirror `KNOWN_ERROR_TYPES` + `OTHER_ERROR_TYPE`; used to decide
        which `et_*` stack series carry data (and can therefore be rendered)
        without reflective `et_*` field access.
        """
        return {
            "OutOfMemory": self.et_OutOfMemory,
            "QueryTimeout": self.et_QueryTimeout,
            "PermissionDenied": self.et_PermissionDenied,
            "Connection": self.et_Connection,
            "UNKNOWN": self.et_UNKNOWN,
            "OTHER": self.et_OTHER,
        }


# Guard against drift between the fixed `qt_*` model fields and the query-type
# constants they mirror.
assert {
    f"qt_{query_type}" for query_type in (*KNOWN_QUERY_TYPES, OTHER_QUERY_TYPE)
} == {name for name in ComputeUsageChartRow.model_fields if name.startswith("qt_")}

# Guard against drift between the fixed `et_*` model fields and the error-type
# constants they mirror. The `error_counts()` map must expose the same keys.
assert {
    f"et_{error_type}" for error_type in (*KNOWN_ERROR_TYPES, OTHER_ERROR_TYPE)
} == {name for name in ComputeUsageChartRow.model_fields if name.startswith("et_")}
assert set(ComputeUsageChartRow(bucket="").error_counts()) == {
    *KNOWN_ERROR_TYPES,
    OTHER_ERROR_TYPE,
}


@dataclass(frozen=True)
class SummaryData:
    """Recent Activity Summary tab payload for a selected period/grain option."""

    compute_usage: list[ComputeUsageChartRow] = field(default_factory=list)
    total_compute_seconds: float = 0.0
    query_count: int = 0
    failed_count: int = 0
    window_label: str = ""
    error: str = ""


@dataclass(frozen=True)
class RecentQueriesData:
    """Recent Queries tab payload (a single dataset the UI filters locally)."""

    rows: list[QueryRow] = field(default_factory=list)
    error: str = ""


@dataclass(frozen=True)
class ActiveConnectionsData:
    """Active Connections tab payload."""

    rows: list[ConnectionDisplayRow] = field(default_factory=list)
    error: str = ""


# ---------------------------------------------------------------------------
# Timestamp parsing + compute-bucket chart rows
# ---------------------------------------------------------------------------


def _parse_timestamp(start_time: str) -> datetime | None:
    """Parse a MotherDuck timestamp string, or return `None` if unparseable.

    Handles both `T`- and space-separated forms and normalizes a trailing `Z`
    (UTC designator) to a `+00:00` offset that `datetime.fromisoformat`
    accepts on all supported Python versions. Offset-naive results are assumed
    to be UTC and made timezone-aware, so that mixing naive and aware records in
    one dataset can never raise `TypeError` when their buckets are sorted.
    """
    text = start_time.strip()
    if not text:
        return None
    text = text.replace(" ", "T", 1)
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed


def _bucket_label_format(
    buckets: list[MotherDuckComputeUsageBucket],
    parsed: list[datetime | None],
) -> str:
    """Pick the display label format shared by every bucket in the window.

    Day-grain buckets render date-only (`%m-%d`); hourly buckets render `HH:00`,
    adding the date when the window spans more than one calendar day.
    """
    is_day = all(bucket.grain == "day" for bucket in buckets) and len(buckets) > 0
    dates = {value.date() for value in parsed if value is not None}
    if is_day:
        return "%m-%d"
    if len(dates) > 1:
        return "%m-%d %H:00"
    return "%H:00"


def _compute_usage_rows(
    buckets: list[MotherDuckComputeUsageBucket],
) -> list[ComputeUsageChartRow]:
    """Format server-aggregated compute buckets into labeled chart rows.

    The buckets already arrive rolled-up and chronologically ordered from the
    SQL `GROUP BY`; this turns each `bucket_start` timestamp into a display
    label (date-only for a day grain, otherwise `HH:00`, adding the date when
    the hourly buckets span more than one calendar day) and folds the native
    `query_type` compute split into a fixed set of `qt_*` series keys (unknown
    types collapse into `qt_OTHER`) so the stacked compute chart can bind to a
    finite, known series set. The native `error_type` failure split is folded the
    same way into `et_*` series keys (error types outside `KNOWN_ERROR_TYPES`
    collapse into `et_OTHER`) for the stacked "Failed queries" chart.
    """
    parsed = [_parse_timestamp(bucket.bucket_start) for bucket in buckets]
    label_format = _bucket_label_format(buckets, parsed)

    rows: list[ComputeUsageChartRow] = []
    for bucket, value in zip(buckets, parsed, strict=True):
        label = (
            value.strftime(label_format) if value is not None else bucket.bucket_start
        )
        succeeded = max(bucket.query_count - bucket.failed_count, 0)
        qt_seconds = {
            f"qt_{query_type}": 0.0
            for query_type in (*KNOWN_QUERY_TYPES, OTHER_QUERY_TYPE)
        }
        for query_type, seconds in bucket.query_type_compute_seconds.items():
            key = query_type if query_type in KNOWN_QUERY_TYPES else OTHER_QUERY_TYPE
            qt_seconds[f"qt_{key}"] += seconds
        et_counts = {
            f"et_{error_type}": 0
            for error_type in (*KNOWN_ERROR_TYPES, OTHER_ERROR_TYPE)
        }
        for error_type, count in bucket.error_type_counts.items():
            key = error_type if error_type in KNOWN_ERROR_TYPES else OTHER_ERROR_TYPE
            et_counts[f"et_{key}"] += count
        rows.append(
            ComputeUsageChartRow(
                bucket=label,
                compute_seconds=bucket.compute_seconds,
                succeeded=succeeded,
                failed=bucket.failed_count,
                **qt_seconds,
                **et_counts,
            )
        )
    return rows


def format_elapsed(seconds: float) -> str:
    """Format an elapsed duration with a scale-appropriate unit.

    Sub-second durations render in milliseconds (`532.4 ms`); durations from one
    second up to and including two minutes render in seconds (`1.8 s`); anything
    greater than 120 seconds renders in minutes (`2.5 m`). Each scale uses a
    single decimal place, and the unit is rendered inline with the value.
    """
    if seconds < 1.0:
        return f"{seconds * 1000:.1f} ms"
    if seconds > 120.0:
        return f"{seconds / 60:.1f} m"
    return f"{seconds:.1f} s"


# ---------------------------------------------------------------------------
# Privacy-safe row projections (never include raw query / client_query text)
# ---------------------------------------------------------------------------


def _query_row(record: MotherDuckQueryRecord) -> QueryRow:
    """Project a query record to the privacy-safe row.

    Carries the native `query_type`, the regex-derived `query_subtype`, and the
    already-treated (redacted + truncated) `query_text` — never verbatim SQL.
    """
    query_hash = (record.query_hash or "")[:_HASH_PREFIX_LEN]
    succeeded = record.error_message is None and record.error_type is None
    return {
        "query_hash": query_hash,
        "query_type": (record.query_type or "UNKNOWN"),
        "query_subtype": record.query_subtype,
        "user_name": record.user_name,
        "start_time": record.start_time,
        "total_elapsed_seconds": record.total_elapsed_seconds or 0.0,
        "execution_seconds": record.execution_time_seconds or 0.0,
        "wait_seconds": record.wait_time_seconds or 0.0,
        "succeeded": succeeded,
        "error_type": record.error_type or "",
        "error_message": record.error_message or "",
        "query_text_treated": record.query_text or "",
        "database_name": record.database_name or "",
        "source_id": record.source_id or "",
    }


# Placeholder rendered for an absent (blank) safe identifier, so an empty cell
# reads as "not applicable" rather than looking like missing data.
_EMPTY_DISPLAY = "—"


def _or_placeholder(value: str) -> str:
    """Return `value`, or the em-dash placeholder when it is blank."""
    return value or _EMPTY_DISPLAY


def _truncate_display(value: str, max_len: int) -> str:
    """Return `value` truncated to `max_len` characters with a trailing `…`.

    Values at or under `max_len` are returned unchanged. Used for table cells
    (e.g. the Error column) whose full text lives in the detail modal.
    """
    if len(value) <= max_len:
        return value
    return value[:max_len].rstrip() + "…"


def _mask_connection_id(connection_id: str) -> str:
    """Shorten a connection UUID to a `abcd…wxyz` display form."""
    if len(connection_id) <= 9:
        return connection_id
    return f"{connection_id[:4]}…{connection_id[-4:]}"


def _connection_row(info: MotherDuckConnectionInfo) -> ConnectionDisplayRow:
    """Project a connection to the privacy-safe row (no client_query text)."""
    return ConnectionDisplayRow(
        client_connection_id=_mask_connection_id(info.client_connection_id),
        client_user_agent=info.client_user_agent or "",
        server_transaction_stage=info.server_transaction_stage or "",
        server_query_elapsed_time=(
            info.server_query_elapsed_time or info.server_transaction_elapsed_time or ""
        ),
        database_name_display=_or_placeholder(info.database_name or ""),
    )


# ---------------------------------------------------------------------------
# Local, in-memory Recent Queries filtering (no MotherDuck round-trip)
# ---------------------------------------------------------------------------


# A fixed palette of visually distinct swatches. A query hash always maps to the
# same swatch, so identical hashes are obvious at a glance even when the 8-char
# prefixes are hard to eyeball; different hashes usually (not always, given the
# small palette) differ in swatch.
_HASH_SWATCHES = (
    "\U0001f7e5",
    "\U0001f7e7",
    "\U0001f7e8",
    "\U0001f7e9",
    "\U0001f7e6",
    "\U0001f7ea",
    "\U0001f7eb",
    "\u2b1b",
    "\u2b1c",
)


def _hash_swatch(query_hash: str) -> str:
    """Return a deterministic color swatch for `query_hash` (empty if blank)."""
    if not query_hash:
        return ""
    index = hashlib.md5(query_hash.encode()).digest()[0] % len(_HASH_SWATCHES)
    return _HASH_SWATCHES[index]


def _colorize_hash(query_hash: str) -> str:
    """Prefix `query_hash` with its swatch so same-hash rows read alike."""
    swatch = _hash_swatch(query_hash)
    return f"{swatch} {query_hash}" if swatch else query_hash


def _abbreviate_user(user_name: str) -> str:
    """Abbreviate a long user id to `{first-6}...{last-3}` (table view only)."""
    if len(user_name) > 12:
        return f"{user_name[:6]}...{user_name[-3:]}"
    return user_name


def _short_start_time(start_time: str) -> str:
    """Render a start timestamp as `YYYY-MM-DD HH:mm` (table view only)."""
    parsed = _parse_timestamp(start_time)
    if parsed is not None:
        return parsed.strftime("%Y-%m-%d %H:%M")
    return start_time[:16]


def _display_row(row: QueryRow) -> RecentQueryDisplayRow:
    """Project a query row to a display model for a state-bound `DataTable`.

    Only whitelisted, privacy-safe fields are emitted (the query text is the
    treated form only). `status` is a human-readable string because
    state-serialized rows cannot carry `Badge` components; `elapsed` is
    pre-formatted with its unit inline; `detail` is a magnifier affordance whose
    row-click opens the detail modal.
    """
    return RecentQueryDisplayRow(
        query_hash=row["query_hash"],
        query_hash_display=_colorize_hash(row["query_hash"]),
        query_type=row["query_type"],
        query_subtype=row["query_subtype"],
        user_name=row["user_name"],
        user_name_display=_abbreviate_user(row["user_name"]),
        start_time=row["start_time"],
        start_time_display=_short_start_time(row["start_time"]),
        elapsed=format_elapsed(row["total_elapsed_seconds"]),
        wait=format_elapsed(row["wait_seconds"]),
        execution=format_elapsed(row["execution_seconds"]),
        status="Succeeded" if row["succeeded"] else "Failed",
        status_display="✅ Succeeded" if row["succeeded"] else "❌ Failed",
        error_type=row["error_type"] or "—",
        error_message=row["error_message"],
        error_message_display=_truncate_display(
            row["error_message"], _ERROR_MESSAGE_PREVIEW_LEN
        ),
        detail="🔍",
        query_text_treated=row["query_text_treated"],
        database_name=row["database_name"],
        database_name_display=_or_placeholder(row["database_name"]),
        source_id=row["source_id"],
        source_id_display=_or_placeholder(row["source_id"]),
    )


class RecentQueryView(BaseModel):
    """The visible Recent Queries subset plus the filter chips for the UI.

    The dataset has already been narrowed server-side by the selected top-level
    mode (all / failed / slow / very slow); this view only applies the in-memory
    native `query_type` and regex `query_subtype` refinements and derives their
    chips. The chips carry per-value counts, but the top-level mode buttons do
    not (rare rows make a count over a capped sample misleading).
    """

    visible_rows: list[RecentQueryDisplayRow] = Field(default_factory=list)
    query_type_options: list[FilterChipOption] = Field(default_factory=list)
    subtype_options: list[FilterChipOption] = Field(default_factory=list)


def _distinct_options(
    values: list[str],
    *,
    all_label: str,
    total: int,
) -> list[FilterChipOption]:
    """Build filter-chip options (a leading "all" chip + one per distinct value).

    Each chip carries its own count so the label reads `Name (count)`.
    """
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    options = [FilterChipOption(value="", label=f"{all_label} ({total})")]
    for value in sorted(counts):
        options.append(
            FilterChipOption(value=value, label=f"{value} ({counts[value]})")
        )
    return options


def build_recent_query_view(
    rows: list[QueryRow],
    *,
    query_type: str,
    subtype: str,
) -> RecentQueryView:
    """Refine the mode's already-fetched rows in memory and derive the chips.

    The top-level modality (all / failed / slow / very slow) has already been
    applied server-side, so this only combines the native `query_type` and regex
    `query_subtype` selections with an `AND` — no MotherDuck round-trip happens
    for a `query_type` / `subtype` change. Subtype chips are populated only when a
    `query_type` is selected (progressive disclosure), and only for subtypes
    actually present among rows of that type.
    """
    # Subtype only refines within a selected query type (progressive disclosure);
    # ignore it when no query type is chosen so the tool matches the UI contract.
    effective_subtype = subtype if query_type else ""
    visible = [
        row
        for row in rows
        if (not query_type or row["query_type"] == query_type)
        and (not effective_subtype or row["query_subtype"] == effective_subtype)
    ]
    query_type_options = _distinct_options(
        [row["query_type"] for row in rows],
        all_label="All types",
        total=len(rows),
    )
    subtype_options: list[FilterChipOption] = []
    if query_type:
        typed = [row for row in rows if row["query_type"] == query_type]
        subtype_options = _distinct_options(
            [row["query_subtype"] for row in typed],
            all_label="All subtypes",
            total=len(typed),
        )
    return RecentQueryView(
        visible_rows=[_display_row(row) for row in visible],
        query_type_options=query_type_options,
        subtype_options=subtype_options,
    )


# ---------------------------------------------------------------------------
# Per-tab loaders (live MotherDuck or sample data in mock-only mode)
# ---------------------------------------------------------------------------


def _summary_option(summary_option: str) -> SummaryOption:
    """Resolve a browser-provided key to a safe `SummaryOption` (default 24h)."""
    return SUMMARY_OPTIONS_BY_KEY.get(
        summary_option, SUMMARY_OPTIONS_BY_KEY[DEFAULT_SUMMARY_OPTION]
    )


def load_summary_data(summary_option: str = DEFAULT_SUMMARY_OPTION) -> SummaryData:
    """Load compute usage plus headline counts for the selected Summary option.

    The `summary_option` key selects a coupled lookback window and grain; the
    aggregate is grouped server-side by that grain and by native `QUERY_TYPE`.
    """
    option = _summary_option(summary_option)

    if mock_only_enabled():
        buckets = (
            SAMPLE_COMPUTE_BUCKETS_DAILY
            if option.grain == "day"
            else SAMPLE_COMPUTE_BUCKETS_HOURLY
        )
        return SummaryData(
            compute_usage=_compute_usage_rows(buckets),
            total_compute_seconds=sum(bucket.compute_seconds for bucket in buckets),
            query_count=sum(bucket.query_count for bucket in buckets),
            failed_count=sum(bucket.failed_count for bucket in buckets),
            window_label=option.window_label,
        )

    min_start_time = (
        datetime.now(UTC) - timedelta(hours=option.period_hours)
    ).isoformat()
    try:
        summary = query_compute_usage_summary(
            MotherDuckQueryFilters(min_start_time=min_start_time),
            realtime=False,
            grain=option.grain,
        )
    except RuntimeError as exc:
        return SummaryData(window_label=option.window_label, error=str(exc))

    return SummaryData(
        compute_usage=_compute_usage_rows(summary.buckets),
        total_compute_seconds=summary.total_compute_seconds,
        query_count=summary.total_query_count,
        failed_count=summary.total_failed_count,
        window_label=option.window_label,
    )


def present_error_type_keys() -> list[str]:
    """Return the error-type keys that carry at least one failure to chart.

    Called at page-build time so the stacked "Failed queries" chart declares a
    `ChartSeries` only for error types actually present, hiding empty types from
    the graph and legend. The probe scans the *widest* selectable window
    (`WIDEST_SUMMARY_OPTION`), a superset of every period the user can pick, so
    switching Period (which only re-runs the data tool, not the static series)
    can never surface a type without a series. On a load error the full set is
    returned so a transient probe failure never drops a real series.
    """
    data = load_summary_data(WIDEST_SUMMARY_OPTION)
    if data.error:
        return [*KNOWN_ERROR_TYPES, OTHER_ERROR_TYPE]

    totals = dict.fromkeys((*KNOWN_ERROR_TYPES, OTHER_ERROR_TYPE), 0)
    for row in data.compute_usage:
        for key, count in row.error_counts().items():
            totals[key] += count
    return [key for key in (*KNOWN_ERROR_TYPES, OTHER_ERROR_TYPE) if totals[key] > 0]


def _query_mode(mode: str) -> QueryMode:
    """Resolve a browser-provided key to a safe `QueryMode` (default all)."""
    return QUERY_MODES_BY_KEY.get(mode, QUERY_MODES_BY_KEY[DEFAULT_QUERY_MODE])


def _mock_rows_for_mode(mode: QueryMode) -> list[QueryRow]:
    """Apply the selected modality to the fixed sample rows (mock-only mode)."""
    rows = list(SAMPLE_RECENT_QUERIES)
    if mode.error_only:
        rows = [row for row in rows if not row["succeeded"]]
    if mode.min_total_elapsed_seconds is not None:
        rows = [
            row
            for row in rows
            if row["total_elapsed_seconds"] >= mode.min_total_elapsed_seconds
        ]
    return rows


def load_recent_query_rows(
    lookback_hours: int = DEFAULT_LOOKBACK_HOURS,
    mode: str = DEFAULT_QUERY_MODE,
) -> RecentQueriesData:
    """Load recent query rows for a lookback window and top-level modality.

    At most `_RECENT_QUERY_LIMIT` rows are fetched; the in-memory `query_type` /
    `query_subtype` chips then re-slice that loaded set without re-querying
    MotherDuck. `lookback_hours` is applied server-side as a `min_start_time`
    filter against `QUERY_HISTORY` (`realtime=False`), which — unlike the realtime
    `RECENT_QUERIES` view — reliably carries completed and errored queries. The
    `mode` maps to server-side `MotherDuckQueryFilters` (`error_only` for failed,
    `min_total_elapsed_seconds` for slow/very slow) so rare errored/slow rows are
    fetched directly rather than sampled out of the newest capped set. Query text
    is fetched already-treated (literals redacted, truncated) so only the safe
    form can reach the browser. In mock-only mode the fixed sample rows are
    filtered to the selected mode regardless of the requested window.
    """
    query_mode = _query_mode(mode)

    if mock_only_enabled():
        return RecentQueriesData(rows=_mock_rows_for_mode(query_mode))

    lookback = max(1, lookback_hours)
    min_start_time = (datetime.now(UTC) - timedelta(hours=lookback)).isoformat()
    try:
        recent = query_motherduck_queries(
            MotherDuckQueryFilters(
                min_start_time=min_start_time,
                error_only=query_mode.error_only,
                min_total_elapsed_seconds=query_mode.min_total_elapsed_seconds,
            ),
            realtime=False,
            limit=_RECENT_QUERY_LIMIT,
            include_query_text=_DETAIL_TEXT_TREATMENT,
        )
    except RuntimeError as exc:
        return RecentQueriesData(error=str(exc))
    return RecentQueriesData(rows=[_query_row(record) for record in recent.queries])


class SummaryErrorRows(BaseModel):
    """Failed queries within a selected Summary period, for the drill-down list.

    Backs the Summary tab's *Show errors* control: the same privacy-safe display
    rows as the Recent Queries table, but fetched `error_only` and scoped to the
    selected Summary window (`window_label`) — a period-level drill-down, since
    Prefab `BarChart` exposes no per-bar selection to key off a single bucket.
    """

    visible_rows: list[RecentQueryDisplayRow] = Field(default_factory=list)
    window_label: str = ""
    error: str = ""


def load_summary_error_rows(
    summary_option: str = DEFAULT_SUMMARY_OPTION,
) -> SummaryErrorRows:
    """Load the failed queries within the selected Summary period/grain window.

    Resolves `summary_option` to its coupled lookback window and fetches only
    failed rows (`QUERY_MODE_FAILED`, applied server-side) for that window, so the
    list mirrors the selected Summary period rather than the Recent Queries tab's
    independent lookback.
    """
    option = _summary_option(summary_option)
    data = load_recent_query_rows(
        lookback_hours=option.period_hours, mode=QUERY_MODE_FAILED
    )
    view = build_recent_query_view(data.rows, query_type="", subtype="")
    return SummaryErrorRows(
        visible_rows=view.visible_rows,
        window_label=option.window_label,
        error=data.error,
    )


def load_active_connection_rows() -> ActiveConnectionsData:
    """Load live server connections for the Active Connections tab."""
    if mock_only_enabled():
        return ActiveConnectionsData(
            rows=[
                ConnectionDisplayRow(
                    client_connection_id=row["client_connection_id"],
                    client_user_agent=row["client_user_agent"],
                    server_transaction_stage=row["server_transaction_stage"],
                    server_query_elapsed_time=row["server_query_elapsed_time"],
                    database_name_display=_or_placeholder(row["database_name"]),
                )
                for row in SAMPLE_ACTIVE_CONNECTIONS
            ]
        )

    try:
        connections = query_active_connections(
            MotherDuckConnectionFilters(),
            include_query_text=False,
        )
    except RuntimeError as exc:
        return ActiveConnectionsData(error=str(exc))
    return ActiveConnectionsData(
        rows=[_connection_row(info) for info in connections.connections]
    )
