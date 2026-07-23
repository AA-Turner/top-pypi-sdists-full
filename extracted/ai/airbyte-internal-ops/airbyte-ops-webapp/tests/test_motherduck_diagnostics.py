"""Tests for the MotherDuck Diagnostics page data + tool layer.

Covers timestamp parsing, compute-bucket chart rows (labels + native query-type
split), the Summary period/grain options, in-memory Recent Queries filtering
(outcome + native query_type + progressively-disclosed subtype), the lazy tab
tools, and the privacy guarantee that verbatim SQL never leaves the projections.
"""

from __future__ import annotations

import pytest
from airbyte_ops_mcp.motherduck_diagnostics.models import MotherDuckComputeUsageBucket

from airbyte_ops_webapp.pages.motherduck_diagnostics._data import (
    _ERROR_MESSAGE_PREVIEW_LEN,
    ComputeUsageChartRow,
    _abbreviate_user,
    _colorize_hash,
    _compute_usage_rows,
    _display_row,
    _hash_swatch,
    _parse_timestamp,
    _short_start_time,
    _truncate_display,
    build_recent_query_view,
    format_elapsed,
    load_active_connection_rows,
    load_recent_query_rows,
    load_summary_data,
    load_summary_error_rows,
    present_error_type_keys,
)
from airbyte_ops_webapp.pages.motherduck_diagnostics._mcp_tools import (
    filter_recent_queries,
    load_recent_queries_tab,
    load_summary_errors_tab,
    load_summary_tab,
)
from airbyte_ops_webapp.pages.motherduck_diagnostics.page import _QUERY_COLUMNS
from airbyte_ops_webapp.pages.motherduck_diagnostics.sample_data import (
    SAMPLE_RECENT_QUERIES,
)
from airbyte_ops_webapp.state import MOCK_ONLY_ENV_VAR

# Fields the privacy contract forbids in any browser-bound projection. Only the
# treated `query_text_treated` (literals redacted) is allowed to reach the UI.
_FORBIDDEN_KEYS = frozenset({"query_text", "client_query"})


@pytest.fixture
def mock_only(monkeypatch: pytest.MonkeyPatch) -> None:
    """Force mock-only mode so loaders return sample data."""
    monkeypatch.setenv(MOCK_ONLY_ENV_VAR, "1")


def _bucket(
    bucket_start: str,
    grain: str,
    compute_seconds: float,
    query_count: int = 1,
    failed_count: int = 0,
    query_type_compute_seconds: dict[str, float] | None = None,
    error_type_counts: dict[str, int] | None = None,
) -> MotherDuckComputeUsageBucket:
    return MotherDuckComputeUsageBucket(
        bucket_start=bucket_start,
        grain=grain,
        compute_seconds=compute_seconds,
        query_count=query_count,
        failed_count=failed_count,
        query_type_compute_seconds=query_type_compute_seconds or {},
        error_type_counts=error_type_counts or {},
    )


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        pytest.param(0.0, "0.0 ms", id="zero"),
        pytest.param(0.0004123, "0.4 ms", id="sub_ms"),
        pytest.param(0.5324, "532.4 ms", id="under_one_second"),
        pytest.param(0.9999, "999.9 ms", id="just_under_one_second"),
        pytest.param(1.0, "1.0 s", id="exactly_one_second"),
        pytest.param(1.82, "1.8 s", id="over_one_second"),
        pytest.param(73.6, "73.6 s", id="many_seconds"),
        pytest.param(120.0, "120.0 s", id="exactly_two_minutes"),
        pytest.param(120.5, "2.0 m", id="just_over_two_minutes"),
        pytest.param(150.0, "2.5 m", id="minutes"),
    ],
)
def test_format_elapsed(seconds: float, expected: str) -> None:
    assert format_elapsed(seconds) == expected


@pytest.mark.parametrize(
    ("raw", "expected_iso"),
    [
        pytest.param(
            "2026-07-14T09:30:00Z", "2026-07-14T09:30:00+00:00", id="trailing_z"
        ),
        pytest.param(
            "2026-07-14 09:30:00", "2026-07-14T09:30:00+00:00", id="space_separated"
        ),
        pytest.param(
            "2026-07-14T09:30:00+00:00",
            "2026-07-14T09:30:00+00:00",
            id="explicit_offset",
        ),
        pytest.param("   ", None, id="blank"),
        pytest.param("not-a-timestamp", None, id="unparseable"),
    ],
)
def test_parse_timestamp(raw: str, expected_iso: str | None) -> None:
    parsed = _parse_timestamp(raw)
    assert (parsed.isoformat() if parsed is not None else None) == expected_iso


def test_compute_usage_rows_multi_day_hourly_uses_date_labels() -> None:
    # Hourly buckets spanning more than one calendar day include the date.
    buckets = [
        _bucket("2026-07-14T09:00:00+00:00", "hour", 8.0),
        _bucket("2026-07-15T09:00:00+00:00", "hour", 7.0),
    ]
    labels = [row.bucket for row in _compute_usage_rows(buckets)]
    assert labels == ["07-14 09:00", "07-15 09:00"]


def test_compute_usage_rows_single_day_uses_time_labels() -> None:
    buckets = [
        _bucket("2026-07-15T08:00:00+00:00", "hour", 5.0),
        _bucket("2026-07-15T09:00:00+00:00", "hour", 7.0),
    ]
    labels = [row.bucket for row in _compute_usage_rows(buckets)]
    assert labels == ["08:00", "09:00"]


def test_compute_usage_rows_day_grain_uses_date_only_labels() -> None:
    buckets = [
        _bucket("2026-07-14T00:00:00+00:00", "day", 100.0),
        _bucket("2026-07-15T00:00:00+00:00", "day", 120.0),
    ]
    labels = [row.bucket for row in _compute_usage_rows(buckets)]
    assert labels == ["07-14", "07-15"]


def test_compute_usage_rows_splits_native_query_type_series() -> None:
    buckets = [
        _bucket(
            "2026-07-15T09:00:00+00:00",
            "hour",
            compute_seconds=12.0,
            query_count=10,
            failed_count=3,
            query_type_compute_seconds={"QUERY": 6.0, "DML": 4.0, "WEIRD": 2.0},
        ),
    ]
    (row,) = _compute_usage_rows(buckets)
    assert row.succeeded == 7
    assert row.failed == 3
    assert row.qt_QUERY == 6.0
    assert row.qt_DML == 4.0
    # An unknown native type folds into the OTHER series, not its own key.
    assert row.qt_OTHER == 2.0
    assert row.qt_DDL == 0.0


def test_compute_usage_rows_splits_native_error_type_series() -> None:
    buckets = [
        _bucket(
            "2026-07-15T09:00:00+00:00",
            "hour",
            compute_seconds=12.0,
            query_count=10,
            failed_count=5,
            error_type_counts={
                "OutOfMemory": 2,
                "QueryTimeout": 1,
                "WeirdError": 2,
            },
        ),
    ]
    (row,) = _compute_usage_rows(buckets)
    assert row.failed == 5
    assert row.et_OutOfMemory == 2
    assert row.et_QueryTimeout == 1
    # An error type outside KNOWN_ERROR_TYPES folds into the OTHER series.
    assert row.et_OTHER == 2
    assert row.et_PermissionDenied == 0
    # The per-error-type split sums to the bucket's total failed count.
    dumped = row.model_dump()
    et_total = sum(value for name, value in dumped.items() if name.startswith("et_"))
    assert et_total == row.failed


def test_compute_usage_rows_empty() -> None:
    assert _compute_usage_rows([]) == []


def test_error_counts_maps_every_series_key() -> None:
    row = ComputeUsageChartRow(
        bucket="09:00",
        et_OutOfMemory=2,
        et_QueryTimeout=1,
        et_OTHER=3,
    )
    assert row.error_counts() == {
        "OutOfMemory": 2,
        "QueryTimeout": 1,
        "PermissionDenied": 0,
        "Connection": 0,
        "UNKNOWN": 0,
        "OTHER": 3,
    }


def test_present_error_type_keys_hides_absent_types(mock_only: None) -> None:
    # The mock data only ever distributes failures across four error types, so
    # UNKNOWN / OTHER (which never appear) must be omitted from the series set,
    # and the returned keys stay in canonical order.
    keys = present_error_type_keys()
    assert keys == ["OutOfMemory", "QueryTimeout", "PermissionDenied", "Connection"]


@pytest.mark.parametrize(
    ("option", "grain", "window_label", "expected_buckets"),
    [
        pytest.param("24h", "hour", "last 24 hours", 7, id="24h_hourly"),
        pytest.param("48h", "hour", "last 48 hours", 7, id="48h_hourly"),
        pytest.param("7d", "day", "last 7 days", 7, id="7d_daily"),
        pytest.param("14d", "day", "last 14 days", 7, id="14d_daily"),
    ],
)
def test_load_summary_data_options_drive_grain_and_window(
    mock_only: None,
    option: str,
    grain: str,
    window_label: str,
    expected_buckets: int,
) -> None:
    data = load_summary_data(option)
    assert data.window_label == window_label
    assert len(data.compute_usage) == expected_buckets
    if grain == "day":
        assert data.total_compute_seconds == pytest.approx(20540.0)
        assert (data.query_count, data.failed_count) == (6980, 188)
    else:
        assert data.total_compute_seconds == pytest.approx(1315.0)
        assert (data.query_count, data.failed_count) == (450, 16)


def test_load_summary_data_unknown_option_falls_back_to_default(
    mock_only: None,
) -> None:
    assert load_summary_data("bogus").window_label == "last 24 hours"


def test_load_summary_tab_tool_formats_counts_and_window(mock_only: None) -> None:
    payload = load_summary_tab("7d")
    assert payload.summary_total_compute == "20,540"
    assert payload.summary_query_count == "6,980"
    assert payload.summary_failed_count == "188"
    assert payload.summary_window_label == "last 7 days"


@pytest.mark.parametrize(
    "lookback_hours",
    [pytest.param(1, id="1h"), pytest.param(8, id="8h"), pytest.param(72, id="72h")],
)
def test_load_recent_query_rows_mock_ignores_lookback(
    mock_only: None, lookback_hours: int
) -> None:
    data = load_recent_query_rows(lookback_hours=lookback_hours)
    assert len(data.rows) == len(SAMPLE_RECENT_QUERIES)


def test_load_active_connection_rows_mock(mock_only: None) -> None:
    assert len(load_active_connection_rows().rows) == 4


@pytest.mark.parametrize(
    ("query_type", "subtype", "expected"),
    [
        pytest.param("", "", 8, id="all"),
        pytest.param("DML", "", 4, id="dml"),
        pytest.param("QUERY", "SELECT", 3, id="query_select"),
        pytest.param("DDL", "", 1, id="ddl"),
        pytest.param("QUERY", "INSERT", 0, id="query_insert_none"),
    ],
)
def test_build_recent_query_view_combines_filters_in_memory(
    query_type: str, subtype: str, expected: int
) -> None:
    view = build_recent_query_view(
        list(SAMPLE_RECENT_QUERIES),
        query_type=query_type,
        subtype=subtype,
    )
    assert len(view.visible_rows) == expected


def test_build_recent_query_view_has_no_count_fields() -> None:
    # The top-level modality is applied server-side, so the view carries no
    # outcome/speed count fields for the (count-free) mode buttons.
    view = build_recent_query_view(
        list(SAMPLE_RECENT_QUERIES), query_type="", subtype=""
    )
    count_fields = {
        name for name in type(view).model_fields if name.startswith("count")
    }
    assert count_fields == set()


def test_build_recent_query_view_progressive_subtype_disclosure() -> None:
    rows = list(SAMPLE_RECENT_QUERIES)
    # No query type selected -> no subtype chips.
    without_type = build_recent_query_view(rows, query_type="", subtype="")
    assert without_type.subtype_options == []
    # Query-type chips always available (leading "all" chip + one per type).
    type_values = {opt.value for opt in without_type.query_type_options}
    assert type_values == {"", "QUERY", "DML", "DDL"}

    # A stray subtype without a query type is ignored (matches the UI contract),
    # so it does not narrow the visible rows below the full loaded set.
    stray_subtype = build_recent_query_view(rows, query_type="", subtype="INSERT")
    assert len(stray_subtype.visible_rows) == len(rows)

    # Selecting DML discloses only the subtypes present for DML rows.
    with_type = build_recent_query_view(rows, query_type="DML", subtype="")
    subtype_values = {opt.value for opt in with_type.subtype_options if opt.value}
    assert subtype_values == {"INSERT", "COPY", "DELETE"}


@pytest.mark.parametrize(
    ("mode", "expected"),
    [
        pytest.param("all", 8, id="all"),
        pytest.param("failed", 3, id="failed"),
        pytest.param("slow", 4, id="slow_inclusive_of_very_slow"),
        pytest.param("very_slow", 0, id="very_slow"),
        pytest.param("bogus", 8, id="unknown_falls_back_to_all"),
    ],
)
def test_load_recent_query_rows_mode_filters_server_side(
    mock_only: None, mode: str, expected: int
) -> None:
    # Modes narrow the dataset (mock mode mirrors the server-side predicates);
    # `slow` (>= 10s) is inclusive of the `very_slow` (>= 2m) rows.
    assert len(load_recent_query_rows(mode=mode).rows) == expected


def test_recent_queries_tab_tool_returns_rows_without_counts(mock_only: None) -> None:
    payload = load_recent_queries_tab()
    assert len(payload.rows_all) == 8
    # No mode filter applied, so every loaded row is initially visible.
    assert len(payload.visible_rows) == 8
    count_fields = {
        name for name in type(payload).model_fields if name.startswith("count")
    }
    assert count_fields == set()
    assert payload.error == ""


def test_recent_queries_tab_tool_failed_mode_fetches_only_failures(
    mock_only: None,
) -> None:
    payload = load_recent_queries_tab(mode="failed")
    assert len(payload.rows_all) == 3
    assert all(row.status == "Failed" for row in payload.visible_rows)


def test_filter_recent_queries_tool_reslices_loaded_rows(mock_only: None) -> None:
    rows = load_recent_queries_tab().rows_all
    payload = filter_recent_queries(rows, query_type="DDL", subtype="")
    assert len(payload.visible_rows) == 1
    subtype_values = {opt.value for opt in payload.subtype_options if opt.value}
    assert subtype_values == {"CREATE"}


def test_display_row_shows_elapsed_and_wait_and_carries_type() -> None:
    row = _display_row(SAMPLE_RECENT_QUERIES[0])
    assert row.elapsed.endswith((" ms", " s"))
    assert row.wait.endswith((" ms", " s"))
    assert row.execution.endswith((" ms", " s"))
    assert "total_elapsed_seconds" not in type(row).model_fields
    assert row.query_type == "QUERY"
    assert row.detail == "🔍"


def test_display_row_carries_verbatim_error_message_for_failed_queries() -> None:
    # The failed COPY sample carries an OutOfMemory diagnostic; the display row
    # must surface it verbatim (no SQL literal redaction applied to the message).
    failed = next(s for s in SAMPLE_RECENT_QUERIES if not s["succeeded"])
    row = _display_row(failed)
    assert row.status == "Failed"
    assert row.error_message == failed["error_message"]
    assert row.error_message != ""


def test_display_row_omits_error_message_for_succeeded_queries() -> None:
    succeeded = next(s for s in SAMPLE_RECENT_QUERIES if s["succeeded"])
    row = _display_row(succeeded)
    assert row.status == "Succeeded"
    assert row.error_message == ""
    assert row.error_message_display == ""


def test_display_row_truncates_long_error_message_for_table_preview() -> None:
    # The table cell binds `error_message_display`, a bounded preview so one long
    # message can't blow out the column width; `error_message` keeps the full
    # text for the detail modal. Pick the longest sample error to exercise it.
    longest = max(
        (s for s in SAMPLE_RECENT_QUERIES if not s["succeeded"]),
        key=lambda s: len(s["error_message"]),
    )
    assert len(longest["error_message"]) > _ERROR_MESSAGE_PREVIEW_LEN
    row = _display_row(longest)
    assert row.error_message == longest["error_message"]
    assert len(row.error_message_display) <= _ERROR_MESSAGE_PREVIEW_LEN + 1
    assert row.error_message_display.endswith("\u2026")
    assert row.error_message_display[:-1] in longest["error_message"]


@pytest.mark.parametrize(
    "value,max_len,expected",
    [
        pytest.param("short", 10, "short", id="under_limit_unchanged"),
        pytest.param("exactly-10", 10, "exactly-10", id="at_limit_unchanged"),
        pytest.param("0123456789abc", 10, "0123456789\u2026", id="over_limit_ellipsis"),
        pytest.param("trailing    x", 8, "trailing\u2026", id="trailing_ws_stripped"),
        pytest.param("", 10, "", id="empty_unchanged"),
    ],
)
def test_truncate_display(value: str, max_len: int, expected: str) -> None:
    assert _truncate_display(value, max_len) == expected


def test_display_row_status_display_carries_outcome_emoji() -> None:
    succeeded = next(s for s in SAMPLE_RECENT_QUERIES if s["succeeded"])
    failed = next(s for s in SAMPLE_RECENT_QUERIES if not s["succeeded"])
    assert _display_row(succeeded).status_display == "✅ Succeeded"
    assert _display_row(failed).status_display == "❌ Failed"


def test_display_row_never_leaks_verbatim_sql() -> None:
    for sample in SAMPLE_RECENT_QUERIES:
        row = _display_row(sample)
        assert _FORBIDDEN_KEYS.isdisjoint(type(row).model_fields)
        assert row.status in {"Succeeded", "Failed"}


def test_sample_data_contains_no_raw_sql() -> None:
    for row in SAMPLE_RECENT_QUERIES:
        assert _FORBIDDEN_KEYS.isdisjoint(row.keys())


@pytest.mark.parametrize(
    "user_name,expected",
    [
        pytest.param("short", "short", id="short_unchanged"),
        pytest.param("exactly12chr", "exactly12chr", id="len_12_unchanged"),
        pytest.param("abcdefghijklm", "abcdef...klm", id="len_13_abbreviated"),
        pytest.param(
            "user_1234567890@airbyte.io",
            "user_1....io",
            id="email_abbreviated",
        ),
    ],
)
def test_abbreviate_user(user_name: str, expected: str) -> None:
    assert _abbreviate_user(user_name) == expected


def test_short_start_time_formats_parseable_timestamp() -> None:
    assert _short_start_time("2026-07-15T18:25:47.123456+00:00") == "2026-07-15 18:25"


def test_short_start_time_falls_back_for_unparseable() -> None:
    assert _short_start_time("not-a-timestamp") == "not-a-timestamp"[:16]


def test_hash_swatch_is_deterministic_and_blank_for_empty() -> None:
    assert _hash_swatch("") == ""
    assert _hash_swatch("abc12345") == _hash_swatch("abc12345")


def test_colorize_hash_prefixes_swatch_and_keeps_hash() -> None:
    colorized = _colorize_hash("abc12345")
    assert colorized.endswith("abc12345")
    assert colorized != "abc12345"
    assert _colorize_hash("") == ""


def test_display_row_keeps_full_user_but_abbreviates_display() -> None:
    long_user = next(s for s in SAMPLE_RECENT_QUERIES if len(s["user_name"]) > 12)
    row = _display_row(long_user)
    # The full id is retained (for the detail modal) while the table-only display
    # projection is abbreviated.
    assert row.user_name == long_user["user_name"]
    assert row.user_name_display == _abbreviate_user(long_user["user_name"])
    assert "..." in row.user_name_display
    # The short start time is a table-only projection; the full value is kept.
    assert row.start_time == long_user["start_time"]
    assert len(row.start_time_display) <= 16
    # The colorized hash carries the plain hash for the detail modal.
    assert row.query_hash_display.endswith(row.query_hash)


def test_display_row_surfaces_source_identifiers() -> None:
    # A sample whose query scans a source's iceberg data carries the database
    # and its parsed UUID verbatim, with matching non-placeholder display forms.
    with_source = next(s for s in SAMPLE_RECENT_QUERIES if s["database_name"])
    row = _display_row(with_source)
    assert row.database_name == with_source["database_name"]
    assert row.source_id == with_source["source_id"]
    assert row.database_name_display == with_source["database_name"]
    assert row.source_id_display == with_source["source_id"]


def test_display_row_renders_placeholder_for_missing_source() -> None:
    # A query with no source database renders the em-dash placeholder rather
    # than a blank cell, while the raw fields stay empty.
    without_source = next(s for s in SAMPLE_RECENT_QUERIES if not s["database_name"])
    row = _display_row(without_source)
    assert row.database_name == ""
    assert row.source_id == ""
    assert row.database_name_display == "—"
    assert row.source_id_display == "—"


def test_query_columns_show_source_db_but_omit_source_id() -> None:
    # Source DB is shown as the last column (after the error message);
    # Source ID is intentionally omitted from the table as redundant with the
    # database name and is surfaced in the detail modal instead.
    keys = [column.key for column in _QUERY_COLUMNS]
    assert "database_name_display" in keys
    assert "source_id_display" not in keys
    assert keys[-1] == "database_name_display"


def test_query_columns_order_puts_boring_columns_last() -> None:
    keys = [column.key for column in _QUERY_COLUMNS]
    # Detail affordance first; Source DB is the final column, with the error
    # text immediately before it and the query hash before that.
    assert keys[0] == "detail"
    assert keys[-1] == "database_name_display"
    assert keys[-2] == "error_message_display"
    assert keys.index("user_name_display") < keys.index("query_hash_display")
    assert keys.index("query_hash_display") < keys.index("error_message_display")
    assert keys.index("start_time_display") < keys.index("user_name_display")


def test_load_summary_error_rows_returns_only_failed(mock_only: None) -> None:
    result = load_summary_error_rows("24h")
    assert result.error == ""
    assert result.visible_rows
    assert all(row.status == "Failed" for row in result.visible_rows)


def test_load_summary_errors_tab_binds_visible_rows(mock_only: None) -> None:
    result = load_summary_errors_tab("24h")
    assert all(row.status == "Failed" for row in result.visible_rows)
    assert result.window_label
