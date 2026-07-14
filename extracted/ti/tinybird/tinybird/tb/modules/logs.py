# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.
import json
import re
import time
from contextlib import suppress
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

import click
import humanfriendly.tables
from click import Context

from tinybird.tb.client import TinyB
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import echo_json, force_echo
from tinybird.tb.modules.exceptions import CLIException
from tinybird.tb.modules.feedback_manager import FeedbackManager

LOG_SOURCES: Tuple[str, ...] = (
    "tinybird.pipe_stats_rt",
    "tinybird.block_log",
    "tinybird.datasources_ops_log",
    "tinybird.endpoint_errors",
    "tinybird.kafka_ops_log",
    "tinybird.sinks_ops_log",
    "tinybird.jobs_log",
    "tinybird.llm_usage",
)

DEFAULT_LOG_SOURCES: Tuple[str, ...] = (
    "tinybird.datasources_ops_log",
    "tinybird.pipe_stats_rt",
    "tinybird.jobs_log",
)

TIMESTAMP_COLUMNS: Dict[str, str] = {
    "tinybird.pipe_stats_rt": "start_datetime",
    "tinybird.block_log": "timestamp",
    "tinybird.datasources_ops_log": "timestamp",
    "tinybird.endpoint_errors": "start_datetime",
    "tinybird.kafka_ops_log": "timestamp",
    "tinybird.sinks_ops_log": "timestamp",
    "tinybird.jobs_log": "created_at",
    "tinybird.llm_usage": "start_time",
}

RELEVANT_DETAIL_FIELDS: Dict[str, Tuple[str, ...]] = {
    "tinybird.pipe_stats_rt": (
        "pipe_name",
        "method",
        "status_code",
        "Error",
        "error",
        "duration",
        "read_rows",
        "read_bytes",
        "result_rows",
    ),
    "tinybird.block_log": (
        "datasource_name",
        "status",
        "source",
        "rows",
        "bytes",
        "processing_time",
        "processing_error",
        "quarantine_lines",
    ),
    "tinybird.datasources_ops_log": (
        "event_type",
        "datasource_name",
        "result",
        "elapsed_time",
        "rows",
        "error",
        "pipe_name",
    ),
    "tinybird.endpoint_errors": (
        "pipe_name",
        "status_code",
        "error",
        "url",
        "params",
    ),
    "tinybird.kafka_ops_log": (
        "topic",
        "partition",
        "msg_type",
        "lag",
        "processed_messages",
        "committed_messages",
        "msg",
    ),
    "tinybird.sinks_ops_log": (
        "service",
        "pipe_name",
        "result",
        "error",
        "elapsed_time",
        "read_rows",
        "written_rows",
    ),
    "tinybird.jobs_log": (
        "job_id",
        "job_type",
        "status",
        "pipe_name",
        "error",
    ),
    "tinybird.llm_usage": (
        "feature",
        "origin",
        "user_email",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "duration",
        "cost",
    ),
}

LOG_TABLE_COLUMNS: Tuple[str, ...] = ("Timestamp", "Source", "Type", "Resource", "Result", "Duration", "Payload")

PRIMARY_LOG_FIELDS: Dict[str, Dict[str, Tuple[str, ...]]] = {
    "tinybird.pipe_stats_rt": {
        "type": ("method",),
        "resource": ("pipe_name",),
        "result": ("status_code",),
        "duration": ("duration",),
    },
    "tinybird.datasources_ops_log": {
        "type": ("event_type",),
        "resource": ("datasource_name",),
        "result": ("result",),
        "duration": ("elapsed_time",),
    },
    "tinybird.kafka_ops_log": {
        "type": ("msg_type",),
        "resource": ("topic",),
        "result": (),
        "duration": ("time_write",),
    },
    "tinybird.sinks_ops_log": {
        "type": ("service",),
        "resource": ("pipe_name",),
        "result": ("result",),
        "duration": ("elapsed_time",),
    },
    "tinybird.jobs_log": {
        "type": ("job_type",),
        "resource": ("pipe_name",),
        "result": ("status",),
        "duration": (),
    },
}

FALLBACK_PRIMARY_LOG_FIELDS: Dict[str, Tuple[str, ...]] = {
    "type": ("event_type", "msg_type", "method", "job_type", "type"),
    "resource": ("pipe_name", "datasource_name", "topic", "service", "resource"),
    "result": ("result", "status", "status_code", "error"),
    "duration": ("elapsed_time", "duration", "processing_time", "time_write"),
}

_RELATIVE_TIME_RE = re.compile(r"^-?(\d+)([mhdw])$")
_DETAILS_EXCLUDED_FIELDS = {
    "start_datetime",
    "timestamp",
    "created_at",
    "start_time",
    "end_datetime",
    "end_time",
    "date",
    "source",
}
_TEMPORAL_DETAIL_FIELDS = {
    "date",
    "datetime",
    "timestamp",
    "start_datetime",
    "end_datetime",
    "created_at",
    "updated_at",
    "started_at",
    "ended_at",
    "finished_at",
    "start_time",
    "end_time",
    "event_date",
    "query_last_execution",
    "run_validation",
}
_DURATION_DETAIL_FIELDS = {"duration", "elapsed_time", "processing_time"}
_ROW_COUNT_DETAIL_FIELDS = {"rows", "read_rows", "written_rows", "result_rows", "quarantine_lines"}
_BYTE_COUNT_DETAIL_FIELDS = {"bytes", "read_bytes", "result_bytes", "written_bytes"}
_MILLISECOND_DURATION_SOURCES: Set[str] = set()


def _to_iso_utc(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _parse_relative_time(value: str, now: Optional[datetime] = None) -> str:
    now = now or datetime.now(timezone.utc)
    cleaned_value = value.strip()
    match = _RELATIVE_TIME_RE.match(cleaned_value)
    if not match:
        return cleaned_value

    amount = int(match.group(1))
    unit = match.group(2)
    delta_by_unit = {
        "m": timedelta(minutes=amount),
        "h": timedelta(hours=amount),
        "d": timedelta(days=amount),
        "w": timedelta(weeks=amount),
    }
    return _to_iso_utc(now - delta_by_unit[unit])


def _escape_sql_literal(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def _build_source_query(source: str, start_time: str, end_time: str) -> str:
    timestamp_column = TIMESTAMP_COLUMNS[source]
    escaped_start = _escape_sql_literal(start_time)
    escaped_end = _escape_sql_literal(end_time)
    return f"""
    SELECT
      '{source}' AS source,
      {timestamp_column} AS timestamp,
      formatRowNoNewline('JSONEachRow', *) AS data
    FROM {source}
    WHERE {timestamp_column} >= parseDateTimeBestEffort('{escaped_start}')
      AND {timestamp_column} < parseDateTimeBestEffort('{escaped_end}')"""


def _build_query(sources: Sequence[str], start_time: str, end_time: str, limit: int) -> str:
    query_parts = [_build_source_query(source, start_time, end_time) for source in sources]
    source_union = "\n  UNION ALL\n".join(query_parts)
    return f"""
SELECT *
FROM (
{source_union}
)
ORDER BY timestamp DESC
LIMIT {limit}
FORMAT JSON"""


def _parse_sources(raw_sources: Sequence[str]) -> List[str]:
    if not raw_sources:
        return list(DEFAULT_LOG_SOURCES)

    selected_sources: List[str] = []
    for raw_source in raw_sources:
        for source in raw_source.split(","):
            cleaned_source = source.strip()
            if not cleaned_source:
                continue
            if cleaned_source == "*":
                return list(LOG_SOURCES)
            if cleaned_source not in LOG_SOURCES:
                raise CLIException(
                    FeedbackManager.error(
                        message=f"Unknown source '{cleaned_source}'. Valid sources: {', '.join(LOG_SOURCES)}"
                    )
                )
            if cleaned_source not in selected_sources:
                selected_sources.append(cleaned_source)

    if not selected_sources:
        raise CLIException(FeedbackManager.error(message="At least one source is required"))

    return selected_sources


def _format_time(timestamp_value: Any) -> str:
    timestamp = str(timestamp_value)
    try:
        parsed_dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return parsed_dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return timestamp


def _normalize_json_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _normalize_json_value(val) for key, val in value.items()}
    if isinstance(value, list):
        return [_normalize_json_value(item) for item in value]
    if isinstance(value, str):
        stripped = value.strip()
        if stripped and stripped[0] in {"{", "["}:
            with suppress(json.JSONDecodeError):
                return _normalize_json_value(json.loads(stripped))
    return value


def _normalize_json_row(row: Dict[str, Any]) -> Dict[str, Any]:
    normalized_row = dict(row)
    normalized_row["data"] = _normalize_json_value(row.get("data"))
    return normalized_row


def _truncate(value: str, width: int) -> str:
    if width <= 3:
        return value[:width]
    if len(value) <= width:
        return value
    return f"{value[: width - 3]}..."


def _truncate_details(value: str, width: int) -> str:
    if len(value) <= width:
        return value

    items = value.split(", ")
    if not items:
        return value[:width]

    # Keep only whole values that fit in the available width.
    kept: List[str] = []
    for item in items:
        candidate = item if not kept else f"{', '.join(kept)}, {item}"
        if len(candidate) <= width:
            kept.append(item)
            continue
        break

    if not kept:
        return value[:width]

    return ", ".join(kept)


def _format_detail_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, (list, dict)):
        return json.dumps(value, separators=(",", ":"))
    return str(value).strip()


def _format_numeric_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        normalized = int(value) if value.is_integer() else value
        if isinstance(normalized, int):
            return f"{normalized:,}"
        return f"{normalized:,.3f}".rstrip("0").rstrip(".")
    return _format_detail_value(value)


def _as_float(value: Any) -> Optional[float]:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        try:
            return float(stripped)
        except ValueError:
            return None
    return None


def _format_pretty_detail_value(key: str, value: Any, source: str) -> str:
    base_key = key.strip().lower().split(".")[-1]
    numeric_value = _as_float(value)

    if base_key in _DURATION_DETAIL_FIELDS and numeric_value is not None:
        if base_key == "duration" and source in _MILLISECOND_DURATION_SOURCES:
            milliseconds = numeric_value
        else:
            milliseconds = numeric_value * 1000
        return f"{_format_numeric_value(milliseconds)} ms"

    if base_key in _ROW_COUNT_DETAIL_FIELDS and numeric_value is not None:
        row_count = int(numeric_value) if float(numeric_value).is_integer() else numeric_value
        return f"{_format_numeric_value(row_count)} rows"

    if base_key in _BYTE_COUNT_DETAIL_FIELDS and numeric_value is not None:
        byte_count = int(numeric_value) if float(numeric_value).is_integer() else numeric_value
        return f"{_format_numeric_value(byte_count)} bytes"

    return _format_detail_value(value)


def _select_detail_keys(parsed_data: Dict[str, Any], source: str, verbose: bool) -> List[str]:
    visible_keys: List[str] = []
    for key, value in parsed_data.items():
        if value is None or value == "":
            continue
        if not verbose and _is_temporal_detail_field(key):
            continue
        visible_keys.append(key)

    if verbose:
        return visible_keys

    preferred_keys = RELEVANT_DETAIL_FIELDS.get(source, ())
    selected_keys: List[str] = [
        key for key in preferred_keys if key in parsed_data and parsed_data.get(key) not in ("", None)
    ]
    return selected_keys or visible_keys


def _parse_data_object(data: Any) -> Optional[Dict[str, Any]]:
    if isinstance(data, dict):
        return data

    text = str(data)
    try:
        parsed_data = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None

    return parsed_data if isinstance(parsed_data, dict) else None


def _find_matching_key(parsed_data: Dict[str, Any], key: str) -> Optional[str]:
    if key in parsed_data:
        return key

    key_lower = key.lower()
    for parsed_key in parsed_data:
        if parsed_key.lower() == key_lower:
            return parsed_key
    return None


def _extract_primary_column_value(parsed_data: Dict[str, Any], source: str, column: str, used_keys: Set[str]) -> str:
    source_fields = PRIMARY_LOG_FIELDS.get(source, {})
    candidate_keys = source_fields[column] if column in source_fields else FALLBACK_PRIMARY_LOG_FIELDS.get(column, ())

    for key in candidate_keys:
        matching_key = _find_matching_key(parsed_data, key)
        if matching_key is None:
            continue

        value = parsed_data.get(matching_key)
        if value in ("", None):
            continue

        used_keys.add(matching_key)
        if column == "duration":
            return _format_pretty_detail_value(matching_key, value, source=source)
        return _format_detail_value(value)

    return "-"


def _summarize_payload(
    parsed_data: Dict[str, Any], source: str, used_keys: Set[str], expand: bool, verbose: bool
) -> str:
    selected_keys = _select_detail_keys(parsed_data, source=source, verbose=verbose)
    used_lower = {key.lower() for key in used_keys}
    payload_keys = [
        key for key in selected_keys if key.lower() not in used_lower and parsed_data.get(key) not in ("", None)
    ]
    if not payload_keys:
        return "-"

    values = [f"{key}: {_format_pretty_detail_value(key, parsed_data.get(key), source=source)}" for key in payload_keys]
    summary = ", ".join(values)
    return summary if expand else _truncate_details(summary, 120)


def _summarize_details(data: Any, source: str, expand: bool, verbose: bool) -> str:
    text = str(data)
    try:
        parsed_data = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return text if expand else _truncate(text, 120)

    if not isinstance(parsed_data, dict):
        normalized = str(parsed_data)
        return normalized if expand else _truncate(normalized, 120)

    values: List[str] = []
    for key in _select_detail_keys(parsed_data, source=source, verbose=verbose):
        value = parsed_data.get(key)
        formatted_value = _format_pretty_detail_value(key, value, source=source)
        values.append(f"{key}: {formatted_value}" if verbose else formatted_value)

    summary = ", ".join(values) if values else text
    return summary


def _render_logs_table(rows: Sequence[Dict[str, Any]], expand: bool, verbose: bool) -> str:
    rendered_rows: List[Tuple[str, str, str, str, str, str, str]] = []
    for row in rows:
        source = str(row.get("source", ""))
        timestamp = _format_time(row.get("timestamp", ""))
        parsed_data = _parse_data_object(row.get("data", ""))

        if parsed_data is None:
            payload = _format_detail_value(row.get("data", ""))
            payload = payload if expand else _truncate(payload, 120)
            rendered_rows.append((timestamp, source, "-", "-", "-", "-", payload))
            continue

        used_keys: Set[str] = set()
        row_type = _extract_primary_column_value(parsed_data, source, "type", used_keys)
        resource = _extract_primary_column_value(parsed_data, source, "resource", used_keys)
        result = _extract_primary_column_value(parsed_data, source, "result", used_keys)
        duration = _extract_primary_column_value(parsed_data, source, "duration", used_keys)
        payload = _summarize_payload(parsed_data, source, used_keys, expand=expand, verbose=verbose)

        rendered_rows.append((timestamp, source, row_type, resource, result, duration, payload))

    return humanfriendly.tables.format_pretty_table(rendered_rows, column_names=list(LOG_TABLE_COLUMNS))


def _resolve_environment_label(ctx: Context) -> str:
    env = ctx.ensure_object(dict).get("env", "local")
    branch = ctx.ensure_object(dict).get("branch")
    if env == "cloud" and branch:
        return f"branch:{branch}"
    return str(env)


def _is_temporal_detail_field(key: str) -> bool:
    normalized_key = key.strip().lower()
    base_key = normalized_key.split(".")[-1]

    if base_key in _DETAILS_EXCLUDED_FIELDS:
        return True
    if base_key in _TEMPORAL_DETAIL_FIELDS:
        return True
    if base_key.endswith("_at"):
        return True
    if base_key.endswith("_timestamp"):
        return True
    return bool(base_key.endswith("_date"))


@cli.command(name="logs")
@click.option(
    "-s",
    "--start",
    "start_time",
    default="-1h",
    show_default=True,
    help="Start time (relative: -1h, -30m, -1d, -7d or ISO 8601).",
)
@click.option(
    "-e",
    "--end",
    "end_time",
    default=None,
    help="End time (relative or ISO 8601).",
)
@click.option(
    "--source",
    "sources",
    multiple=True,
    help=f"Comma-separated or repeated list of sources. Use '*' for all. Available: {', '.join(LOG_SOURCES)}",
)
@click.option(
    "-n",
    "--limit",
    default=100,
    show_default=True,
    type=click.IntRange(1, 1000),
    help="Maximum rows to return.",
)
@click.option("-x", "--expand", is_flag=True, default=False, help="Show full details without truncation.")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Show all fields in details with property names.")
@click.pass_context
def logs(
    ctx: Context,
    start_time: str,
    end_time: Optional[str],
    sources: Tuple[str, ...],
    limit: int,
    expand: bool,
    verbose: bool,
) -> None:
    """Query Tinybird real-time service logs."""
    output = ctx.ensure_object(dict)["output"]
    if output not in {"human", "json"}:
        force_echo(FeedbackManager.error_invalid_output_format(formats=", ".join(["human", "json"])))
        return

    client: TinyB = ctx.ensure_object(dict)["client"]
    now = datetime.now(timezone.utc)

    resolved_start = _parse_relative_time(start_time, now)
    resolved_end = _parse_relative_time(end_time, now) if end_time else _to_iso_utc(now)
    resolved_sources = _parse_sources(sources)
    environment = _resolve_environment_label(ctx)
    query = _build_query(resolved_sources, resolved_start, resolved_end, limit)

    started = time.monotonic()
    try:
        result = client.query(query)
    except Exception as e:
        raise CLIException(FeedbackManager.error_exception(error=str(e)))

    if isinstance(result, str):
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            raise CLIException(FeedbackManager.error_exception(error=result))

    if not isinstance(result, dict):
        raise CLIException(FeedbackManager.error_exception(error="Unexpected response format while querying logs"))
    if "error" in result:
        raise CLIException(FeedbackManager.error_exception(error=str(result["error"])))

    rows = [row for row in result.get("data", []) if isinstance(row, dict)]
    reported_rows = result.get("rows")
    rows_count = len(rows)
    if isinstance(reported_rows, int) and reported_rows >= 0:
        rows_count = reported_rows
    elif isinstance(reported_rows, str) and reported_rows.isdigit():
        rows_count = int(reported_rows)
    if not rows:
        rows_count = 0
    statistics = result.get("statistics", {})
    elapsed_seconds = statistics.get("elapsed") if isinstance(statistics, dict) else None
    if not isinstance(elapsed_seconds, (float, int)):
        elapsed_seconds = time.monotonic() - started

    payload = {
        "environment": environment,
        "query": {
            "start": resolved_start,
            "end": resolved_end,
            "sources": resolved_sources,
            "limit": limit,
            "verbose": verbose,
        },
        "statistics": statistics if isinstance(statistics, dict) else {},
        "rows": rows_count,
        "data": [_normalize_json_row(row) for row in rows],
    }

    if output == "json":
        echo_json(payload, indent=8)
        return

    if not rows:
        click.echo("No logs found for the specified time range.")
        click.echo(f"\nQueried {len(resolved_sources)} source(s) from {environment} in {elapsed_seconds:.1f}s")
        return

    click.echo(_render_logs_table(rows, expand=expand, verbose=verbose))
    click.echo(
        f"\nFetched {rows_count} logs from {len(resolved_sources)} source(s) in {elapsed_seconds:.1f}s ({environment})"
    )
