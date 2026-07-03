#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
import functools
import json
import os
import queue
import re
import threading
import uuid
from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Iterable
from contextvars import ContextVar
from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Optional

import google.protobuf.message
import pyspark.sql.connect.proto.base_pb2 as proto_base
from google.protobuf.any_pb2 import Any as AnyProto

from snowflake.connector.cursor import SnowflakeCursor
from snowflake.connector.description import PLATFORM
from snowflake.connector.telemetry import (
    TelemetryClient as PCTelemetryClient,
    TelemetryData as PCTelemetryData,
    TelemetryField as PCTelemetryField,
)
from snowflake.connector.time_util import get_time_millis
from snowflake.snowpark import Session
from snowflake.snowpark._internal.utils import get_os_name, get_python_version
from snowflake.snowpark.version import VERSION as snowpark_version
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.version import VERSION as sas_version


@unique
class TelemetryField(Enum):
    # inherited from snowflake.connector.telemetry.TelemetryField
    KEY_TYPE = PCTelemetryField.KEY_TYPE.value
    KEY_SOURCE = PCTelemetryField.KEY_SOURCE.value

    # constants
    KEY_ERROR_MSG = "error_msg"
    # Message keys for telemetry
    KEY_VERSION = "version"
    KEY_PYTHON_VERSION = "python_version"
    KEY_SNOWPARK_VERSION = "snowpark_version"
    KEY_OS = "operating_system"
    KEY_DATA = "data"
    KEY_START_TIME = "start_time"
    KEY_EVENT_ID = "event_id"


class TelemetryType(Enum):
    TYPE_REQUEST_SUMMARY = "scos_request_summary"
    TYPE_EVENT = "scos_event"
    EVENT_TYPE = "scos_event_type"


class EventType(Enum):
    SERVER_STARTED = "scos_server_started"
    SUBMIT_COMPLETION = "scos_submit_completion"
    WARNING = "scos_warning"
    RESOLUTION_RULE = "scos_resolution_rule"
    NULL_TYPE_FALLBACK = "scos_null_type_fallback"


# global labels
DEFAULT_SOURCE = "SparkConnectForSnowpark"
SCOS_VERSION = ".".join([str(d) for d in sas_version if d is not None])
SNOWPARK_VERSION = ".".join([str(d) for d in snowpark_version if d is not None])
PYTHON_VERSION = get_python_version()
OS = get_os_name()


# list of config keys for which we record values, other config values are not recorded
RECORDED_CONFIG_KEYS = {
    "spark.sql.pyspark.inferNestedDictAsStruct.enabled",
    "spark.sql.pyspark.legacy.inferArrayTypeFromFirstElement.enabled",
    "spark.sql.repl.eagerEval.enabled",
    "spark.sql.crossJoin.enabled",
    "spark.sql.caseSensitive",
    "spark.sql.ansi.enabled",
    "spark.Catalog.databaseFilterInformationSchema",
    "spark.sql.tvf.allowMultipleTableArguments.enabled",
    "spark.sql.repl.eagerEval.maxNumRows",
    "spark.sql.repl.eagerEval.truncate",
    "spark.sql.session.localRelationCacheThreshold",
    "spark.sql.mapKeyDedupPolicy",
    "snowpark.connect.sql.passthrough",
    "snowpark.connect.cte.optimization_enabled",
    "snowpark.connect.iceberg.external_volume",
    "snowpark.connect.iceberg.base_location",
    "snowpark.connect.udtf.compatibility_mode",
    "snowpark.connect.views.duplicate_column_names_handling_mode",
    "snowpark.connect.parquet.useLogicalType",
}

# IO option allowlist for telemetry reporting.
#
# Maps lowercased option key -> allowed values:
#   frozenset(...)  : value is reported only if it matches (case-insensitive)
#   "numeric"       : value is reported only if it parses as a number
#   None            : key is reported but value is always redacted
#
# Keys NOT in this dict are still reported (key only), value = "<redacted>".
# This two-level allowlist prevents accidental leakage even when a user
# mistakenly puts sensitive data into a well-known option key.

_BOOLEAN = frozenset({"true", "false", "0", "1", "yes", "no"})

_COMPRESSION = frozenset(
    {
        "none",
        "auto",
        "gzip",
        "bzip2",
        "snappy",
        "lz4",
        "zstd",
        "deflate",
        "uncompressed",
        "lzo",
    }
)

_ENCODING = frozenset(
    {
        "utf-8",
        "utf-16",
        "utf8",
        "utf16",
        "us-ascii",
        "ascii",
        "iso-8859-1",
        "latin1",
        "windows-1252",
    }
)

_REBASE_MODE = frozenset({"exception", "corrected", "legacy"})

_SEP = frozenset({",", "\t", ";", "|"})
_QUOTE = frozenset({'"', "'", ""})
_ESCAPE = frozenset({"\\", "\\\\"})
_COMMENT = frozenset({"#", "//", "--"})
_LINESEP = frozenset({"\n", "\r", "\r\n"})
_NULL_LIKE = frozenset({"", "null", "none", "nan", "\\n", "\\N"})
_DATE_FORMAT = frozenset(
    {
        "yyyy-mm-dd",
        "yyyy/mm/dd",
        "mm/dd/yyyy",
        "dd/mm/yyyy",
        "dd-mm-yyyy",
        "mm-dd-yyyy",
        "auto",
    }
)
_TIMESTAMP_FORMAT = frozenset(
    {
        "auto",
        "yyyy-mm-dd hh24:mi:ss.ff6",
        "yyyy-mm-dd hh:mm:ss",
        "yyyy-mm-dd hh:mm:ss.sss",
        "yyyy-mm-dd't'hh:mm:ss",
        "yyyy-mm-dd't'hh:mm:ss.sss",
    }
)
_PATH_GLOB_FILTER = frozenset(
    {
        "*.csv",
        "*.json",
        "*.parquet",
        "*.txt",
        "*.xml",
        "*.orc",
        "*.avro",
        "*.gz",
        "*.bz2",
        "*.zst",
        "*.snappy.parquet",
    }
)
_FORMAT = frozenset(
    {
        "csv",
        "json",
        "parquet",
        "text",
        "xml",
        "orc",
        "avro",
        "iceberg",
        "delta",
        "jdbc",
        "table",
        "net.snowflake.spark.snowflake",
    }
)

ALLOWED_IO_OPTION_VALUES: dict[str, frozenset[str] | str | None] = {
    # --- CSV / general boolean options ---
    "header": _BOOLEAN,
    "inferschema": _BOOLEAN,
    "multiline": _BOOLEAN,
    "single": _BOOLEAN,
    "ignoreleadingwhitespace": _BOOLEAN,
    "ignoretrailingwhitespace": _BOOLEAN,
    "escapequotes": _BOOLEAN,
    "quoteall": _BOOLEAN,
    "recursivefilelookup": _BOOLEAN,
    "relaxtypestoinferschema": _BOOLEAN,
    # --- JSON boolean options ---
    "primitivesasstring": _BOOLEAN,
    "prefersdecimal": _BOOLEAN,
    "allowcomments": _BOOLEAN,
    "allowunquotedfieldnames": _BOOLEAN,
    "allowsinglequotes": _BOOLEAN,
    "allownumericleadingzero": _BOOLEAN,
    "allowbackslashescapinganycharacter": _BOOLEAN,
    "allowunquotedcontrolchars": _BOOLEAN,
    "allownonnumericnumbers": _BOOLEAN,
    "dropfieldifallnull": _BOOLEAN,
    "processinbulk": _BOOLEAN,
    "bz2fileparallelloading": _BOOLEAN,
    "jsonfileparallelloading": _BOOLEAN,
    # --- Parquet boolean options ---
    "mergeschema": _BOOLEAN,
    # --- Enum options ---
    "compression": _COMPRESSION,
    "encoding": _ENCODING,
    "charset": _ENCODING,
    "mode": frozenset(
        {
            "permissive",
            "dropmalformed",
            "failfast",
            "append",
            "overwrite",
            "errorifexists",
            "ignore",
        }
    ),
    "overwrite-mode": frozenset({"static", "dynamic"}),
    "datetimerebasemode": _REBASE_MODE,
    "int96rebasemode": _REBASE_MODE,
    # --- Numeric options (value reported only if it parses as a number) ---
    "rowstoinferschema": "numeric",
    "batchsize": "numeric",
    "splitsizemb": "numeric",
    "samplingratio": "numeric",
    "maxcolumns": "numeric",
    "maxcharspercolumn": "numeric",
    "snowflake_max_file_size": "numeric",
    # --- Common string options ---
    "sep": _SEP,
    "quote": _QUOTE,
    "escape": _ESCAPE,
    "comment": _COMMENT,
    "linesep": _LINESEP,
    "nullvalue": _NULL_LIKE,
    "nanvalue": _NULL_LIKE,
    "emptyvalue": _NULL_LIKE,
    "dateformat": _DATE_FORMAT,
    "timestampformat": _TIMESTAMP_FORMAT,
    "columnnameofcorruptrecord": None,
    "pathglobfilter": _PATH_GLOB_FILTER,
    "modifiedbefore": None,
    "modifiedafter": None,
    "partitionby": None,
    "format": _FORMAT,
}

_REDACTED = "<redacted>"


def _sanitize_io_option_value(key: str, value: str) -> str:
    """Return the option value if it passes the allowlist, otherwise '<redacted>'.

    The allowlist in ALLOWED_IO_OPTION_VALUES controls what gets through:
      - frozenset: value must match one of the entries (case-insensitive)
      - "numeric": value must parse as a number
      - None: key is known but its value is always redacted (free-text fields)
      - key absent: unknown option, value is redacted
    """
    normalized_key = str(key).lower()
    raw_value = str(value)
    normalized_value = raw_value.strip()
    allowed = ALLOWED_IO_OPTION_VALUES.get(normalized_key)
    if allowed is None:
        return _REDACTED
    if allowed == "numeric":
        try:
            float(normalized_value)
            return normalized_value
        except (ValueError, TypeError):
            return _REDACTED
    if isinstance(allowed, frozenset):
        raw_lower = raw_value.lower()
        normalized_lower = normalized_value.lower()
        if raw_lower in allowed:
            return raw_value
        if normalized_lower in allowed:
            return normalized_value
    return _REDACTED


# these fields will be redacted when reporting the spark query plan
REDACTED_PLAN_SUFFIXES = [
    # config values can be set using SQL, so we have to redact it
    "sql",
    "pairs.value",
    "local_relation",
    "options",
    # Expression.Literal carries actual user data (inline values, query params)
    "literal",
    # Aggregate.Pivot.PivotValue.values contains user-supplied pivot values
    "pivot_values",
    # SqlCommand.args carries bind parameter values (user data).
    # (SQL.args is already covered by the "sql" suffix redacting the entire SQL node.)
    "sql_command.args",
    # WriteOperationV2.table_properties may contain user-supplied metadata/paths
    "table_properties",
]


# Path-bearing fields are NOT blanket-redacted: a plain path like
# "s3://bucket/data/" or "@stage/file.parquet" is useful debugging context.
# Instead these fields are value-sanitized (see _sanitize_path_value), which
# strips only credential material — presigned-URL signatures, Azure SAS
# tokens, or a password embedded in the URL userinfo.
SANITIZED_PATH_SUFFIXES = [
    "data_source.paths",
    "write_operation.path",
    "write_stream_operation_start.path",
    "write_operation_v2.table_name",
]


@dataclass
class TelemetryMessage:
    """Container for telemetry messages in the processing queue."""

    message: dict
    timestamp: int
    is_warning: bool


def safe(func):
    """
    Decorator to safely execute telemetry functions, catching and logging exceptions
    without affecting the main application flow.
    """

    @functools.wraps(func)
    def wrap(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            # report failed operation to telemetry
            telemetry.send_warning_msg(
                f"Telemetry operation {func} failed due to exception", e
            )

    return wrap


def is_running_on_xp() -> bool:
    """Return True if the code is running on the XP platform (stored procedures or notebooks)."""
    return PLATFORM == "XP"


def extract_telemetry_client(session: Session) -> Optional[PCTelemetryClient]:
    """
    Extract the driver's telemetry client from the Snowpark session. The client will be used
    to send SCOS telemetry to GS.
    """
    server_connection = getattr(session, "_conn", None)
    if not server_connection:
        return None

    snowflake_connection = getattr(server_connection, "_conn", None)
    if not snowflake_connection:
        return None

    return getattr(snowflake_connection, "_telemetry", None)


class TelemetrySink(ABC):
    MAX_BUFFER_ELEMENTS = 20
    MAX_WAIT_MS = 10000  # 10 seconds

    @abstractmethod
    def add_telemetry_data(self, message: dict, timestamp: int) -> None:
        pass

    @abstractmethod
    def flush(self) -> None:
        pass


class NoOpTelemetrySink(TelemetrySink):
    def add_telemetry_data(self, message: dict, timestamp: int) -> None:
        pass

    def flush(self) -> None:
        pass


class ClientTelemetrySink(TelemetrySink):
    def __init__(self, telemetry_client: PCTelemetryClient) -> None:
        self._telemetry_client = telemetry_client
        self._lock = threading.Lock()
        self._reset()

    def add_telemetry_data(self, message: dict, timestamp: int) -> None:
        telemetry_data = PCTelemetryData(message=message, timestamp=timestamp)
        self._telemetry_client.try_add_log_to_batch(telemetry_data)
        with self._lock:
            self._events_since_last_flush += 1
        # flush more often than the underlying telemetry client
        if self._should_flush():
            self.flush()

    def flush(self) -> None:
        with self._lock:
            self._reset()
        self._telemetry_client.send_batch()

    def _should_flush(self) -> bool:
        current_time = get_time_millis()

        return (
            self._events_since_last_flush >= TelemetrySink.MAX_BUFFER_ELEMENTS
            or (current_time - self._last_flush_time) >= TelemetrySink.MAX_WAIT_MS
        )

    def _reset(self):
        self._events_since_last_flush = 0
        self._last_flush_time = get_time_millis()


class QueryTelemetrySink(TelemetrySink):

    MAX_BUFFER_SIZE = 20 * 1024  # 20KB
    TELEMETRY_JOB_ID = "43e72d9b-56d0-4cdb-a615-6b5b5059d6df"

    def __init__(self, session: Session) -> None:
        self._session = session
        self._lock = threading.Lock()
        self._reset()

    def add_telemetry_data(self, message: dict, timestamp: int) -> None:
        telemetry_entry = {"message": message, "timestamp": timestamp}

        # stringify entry, and escape single quotes
        entry_str = json.dumps(telemetry_entry).replace("'", "''")

        with self._lock:
            self._buffer.append(entry_str)
            self._buffer_size += len(entry_str)

        if self._should_flush():
            self.flush()

    def flush(self) -> None:
        with self._lock:
            if not self._buffer:
                return
            # prefix query with a unique identifier for easier tracking
            query = f"select '{self.TELEMETRY_JOB_ID}' as scos_telemetry_export, '[{','.join(self._buffer)}]'"
            self._reset()

        self._session.sql(query).collect_nowait()

    def _reset(self) -> None:
        self._buffer = []
        self._buffer_size = 0
        self._last_export_time = get_time_millis()

    def _should_flush(self):
        current_time = get_time_millis()
        return (
            self._buffer_size >= QueryTelemetrySink.MAX_BUFFER_SIZE
            or len(self._buffer) >= TelemetrySink.MAX_BUFFER_ELEMENTS
            or (current_time - self._last_export_time) >= TelemetrySink.MAX_WAIT_MS
        )


class Telemetry:
    def __init__(self, is_enabled=True) -> None:
        self._sink = NoOpTelemetrySink()  # use no-op sink until initialized
        self._request_summary: ContextVar[dict] = ContextVar(
            "request_summary", default={}
        )
        self._is_enabled = is_enabled
        self._is_initialized = False
        self._lock = threading.Lock()
        self._source = DEFAULT_SOURCE

        # Async processing setup
        self._message_queue = queue.Queue(maxsize=10000)
        self._worker_thread = None

        # Track if any request failed during the session (for job completion telemetry)
        self._any_request_failed = False
        self._last_error_message = None
        self._last_error_type = None

    def __del__(self):
        self.shutdown()

    def _get_static_telemetry_data(self) -> dict:
        """Get static telemetry data with current configuration."""
        return {
            TelemetryField.KEY_SOURCE.value: self._source,
            TelemetryField.KEY_VERSION.value: SCOS_VERSION,
            TelemetryField.KEY_SNOWPARK_VERSION.value: SNOWPARK_VERSION,
            TelemetryField.KEY_PYTHON_VERSION.value: PYTHON_VERSION,
            TelemetryField.KEY_OS.value: OS,
        }

    def _basic_telemetry_data(self) -> dict:
        data = {
            **self._get_static_telemetry_data(),
            TelemetryField.KEY_EVENT_ID.value: str(uuid.uuid4()),
        }
        # Include submit context fields in all server events when present,
        # so any event can be filtered/correlated by workload.
        workload_name = os.getenv("SNOWPARK_SUBMIT_WORKLOAD_NAME")
        if workload_name:
            data["workload_name"] = workload_name
        correlation_id = os.getenv("SNOWPARK_SUBMIT_CORRELATION_ID")
        if correlation_id:
            data["correlation_id"] = correlation_id
        return data

    def initialize(self, session: Session, source: str = None):
        """
        Must be called after the session is created to initialize telemetry.
        Gets the telemetry client from the session's connection and uses it
        to report telemetry data.

        Args:
            session: Snowpark Session to use for telemetry
            source: Optional source identifier for telemetry (e.g., "SparkConnectThinClient").
                    Defaults to "SparkConnectForSnowpark".
        """
        if not self._is_enabled:
            return

        with self._lock:
            if self._is_initialized:
                logger.warning("Telemetry is already initialized")
                return
            self._is_initialized = True

            if source is not None:
                self._source = source

        telemetry_client = extract_telemetry_client(session)
        if is_running_on_xp() or telemetry_client is None:
            # no network connection to GS
            # telemetry will be exported via queries
            self._sink = QueryTelemetrySink(session)
        else:
            self._sink = ClientTelemetrySink(telemetry_client)

        self._start_worker_thread()
        logger.info(f"Telemetry initialized with {type(self._sink)}")

    @safe
    def initialize_request_summary(
        self, request: google.protobuf.message.Message
    ) -> None:
        summary = {
            "client_type": request.client_type,
            "spark_session_id": request.session_id,
            "request_type": request.__class__.__name__,
            "was_successful": True,
            "internal_queries": 0,
            "created_on": get_time_millis(),
        }

        if hasattr(request, "operation_id"):
            summary["spark_operation_id"] = request.operation_id

        self._request_summary.set(summary)

        _set_query_plan(request, summary)

    def _not_in_request(self):
        # we don't want to add things to the summary if it's not initialized
        return "created_on" not in self._request_summary.get()

    @safe
    def report_parsed_sql_plan(self, plan: google.protobuf.message.Message) -> None:
        if self._not_in_request():
            return

        summary = self._request_summary.get()

        if "parsed_sql_plans" not in summary:
            summary["parsed_sql_plans"] = []

        summary["parsed_sql_plans"].append(
            _protobuf_to_json_with_redaction(plan, REDACTED_PLAN_SUFFIXES)
        )

    @safe
    def report_function_usage(self, function_name: str) -> None:
        if self._not_in_request():
            return

        summary = self._request_summary.get()

        if "used_functions" not in summary:
            summary["used_functions"] = defaultdict(int)

        summary["used_functions"][function_name] += 1

    @safe
    def report_request_failure(self, e: Exception) -> None:
        if self._not_in_request():
            return

        summary = self._request_summary.get()

        summary["was_successful"] = False
        summary["error_message"] = str(e)
        summary["error_type"] = type(e).__name__

        if not hasattr(e, "custom_error_code") or (e.custom_error_code is None):
            summary["error_code"] = ErrorCodes.INTERNAL_ERROR
        else:
            summary["error_code"] = e.custom_error_code

        error_location = _error_location(e)
        if error_location:
            summary["error_location"] = error_location

        # Capture the plan node where the error originated. active_plan_id (the context manager
        # in map_relation) tags the exception with _scos_plan_id before resetting the ContextVar,
        # so we read from the exception attribute rather than from get_current_plan_id() which
        # will have already been reset to None by the time we get here.
        error_plan_id = getattr(e, "_scos_plan_id", None)
        if error_plan_id is not None:
            summary["error_plan_id"] = error_plan_id

        # Track session-level failure for job completion telemetry
        self._any_request_failed = True
        self._last_error_message = str(e)[:500]  # Limit length
        self._last_error_type = type(e).__name__

    @safe
    def report_config_set(self, pairs: Iterable) -> None:
        if self._not_in_request():
            return

        summary = self._request_summary.get()

        if "config_set" not in summary:
            summary["config_set"] = []

        for p in pairs:
            summary["config_set"].append(
                {
                    "key": p.key,
                    "value": p.value if p.key in RECORDED_CONFIG_KEYS else "<redacted>",
                }
            )

    @safe
    def report_config_unset(self, keys: Iterable[str]) -> None:
        if self._not_in_request():
            return

        summary = self._request_summary.get()

        if "config_unset" not in summary:
            summary["config_unset"] = []

        summary["config_unset"].extend(keys)

    @safe
    def report_config_get(self, keys: Iterable[str]) -> None:
        if self._not_in_request():
            return

        summary = self._request_summary.get()

        if "config_get" not in summary:
            summary["config_get"] = []

        summary["config_get"].extend(keys)

    @safe
    def report_unknown_config_get(self, key: str) -> None:
        if self._not_in_request():
            return

        summary = self._request_summary.get()

        if "config_get_unknown_keys" not in summary:
            summary["config_get_unknown_keys"] = []

        summary["config_get_unknown_keys"].append(key)

    @safe
    def report_config_op_type(self, op_type: str):
        if self._not_in_request():
            return

        summary = self._request_summary.get()
        summary["config_op_type"] = op_type

    @safe
    def report_query(
        self, result: SnowflakeCursor | dict | Exception, **kwargs
    ) -> None:
        if result is None or isinstance(result, dict) or self._not_in_request():
            return

        # SnowflakeCursor and SQL errors will have sfqid
        # other exceptions will not have it
        # TODO: handle async queries, but filter out telemetry export queries
        qid = getattr(result, "sfqid", None)

        if qid is None:
            logger.warning("Missing query id in result: %s", result)

        is_internal = kwargs.get("_is_internal", False)
        if is_internal:
            self._report_internal_query()
        elif qid:
            self._report_query_id(qid)

    def _report_query_id(self, query_id: str):
        summary = self._request_summary.get()

        if "queries" not in summary:
            summary["queries"] = []

        summary["queries"].append(query_id)

    def _report_internal_query(self):
        summary = self._request_summary.get()

        if "internal_queries" not in summary:
            summary["internal_queries"] = 0

        summary["internal_queries"] += 1

    @safe
    def report_describe_query_cache_lookup(self):
        """Report a describe query cache lookup."""
        if self._not_in_request():
            return

        summary = self._request_summary.get()

        if "describe_cache_lookups" not in summary:
            summary["describe_cache_lookups"] = 0

        summary["describe_cache_lookups"] += 1

    @safe
    def report_describe_query_cache_hit(self):
        """Report a describe query cache hit."""
        if self._not_in_request():
            return

        summary = self._request_summary.get()

        if "describe_cache_hits" not in summary:
            summary["describe_cache_hits"] = 0

        summary["describe_cache_hits"] += 1

    @safe
    def report_describe_query_cache_expired(self, expired_by: float):
        """Report a describe query cache hit."""
        if self._not_in_request():
            return

        summary = self._request_summary.get()

        if "describe_cache_expired" not in summary:
            summary["describe_cache_expired"] = 0

        summary["describe_cache_expired"] += 1

        if "describe_cache_expired_by" not in summary:
            summary["describe_cache_expired_by"] = []

        summary["describe_cache_expired_by"].append(expired_by)

    @safe
    def report_describe_query_cache_clear(self):
        """Report a describe query cache clear."""
        if self._not_in_request():
            return

        summary = self._request_summary.get()

        if "describe_cache_cleared" not in summary:
            summary["describe_cache_cleared"] = 0

        summary["describe_cache_cleared"] += 1

    @safe
    def report_udf_usage(self, udf_name: str):
        if self._not_in_request():
            return

        summary = self._request_summary.get()

        if "udf_usage" not in summary:
            summary["udf_usage"] = defaultdict(int)

        summary["udf_usage"][udf_name] += 1

    def _report_io(
        self, op: str, io_type: str, options: dict[str, str] | None = None
    ) -> None:
        if self._not_in_request():
            return

        summary = self._request_summary.get()

        if "io" not in summary:
            summary["io"] = []

        entry: dict = {"op": op, "type": io_type}

        if options:
            reported_options = {}
            for key, value in options.items():
                lower_key = key.lower()
                reported_options[lower_key] = _sanitize_io_option_value(
                    lower_key, value
                )
            if reported_options:
                # Keep this key name as "safe_options": backend redacts fields named "options".
                entry["safe_options"] = reported_options

        summary["io"].append(entry)

    @safe
    def report_io_read(
        self, io_type: str, options: dict[str, str] | None = None
    ) -> None:
        self._report_io("read", io_type, options)

    @safe
    def report_io_write(
        self, io_type: str, options: dict[str, str] | None = None
    ) -> None:
        self._report_io("write", io_type, options)

    @safe
    def send_server_started_telemetry(self):
        message = {
            **self._basic_telemetry_data(),
            TelemetryField.KEY_TYPE.value: TelemetryType.TYPE_EVENT.value,
            TelemetryType.EVENT_TYPE.value: EventType.SERVER_STARTED.value,
            TelemetryField.KEY_DATA.value: {
                TelemetryField.KEY_START_TIME.value: get_time_millis(),
            },
        }
        self._send(message)

    @safe
    def send_job_completion_telemetry(
        self,
        exit_code: int = 0,
        error: str | None = None,
        error_type: str | None = None,
    ):
        """
        Send telemetry when a server session ends (always emitted, not just for
        snowpark-submit runs). An ``execution_context`` field indicates how the
        server was invoked: "submit" for snowpark-submit jobs, "interactive" otherwise.

        Args:
            exit_code: The exit code of the job (0 for success, non-zero for failure)
            error: Optional error message if the job failed
            error_type: Optional error type/class name
        """
        # Determine execution context from env var set by the snowpark-submit CLI.
        is_submit_job = os.getenv("SNOWPARK_SUBMIT_JOB") == "true"
        execution_context = "submit" if is_submit_job else "interactive"

        # If any request failed during the session, use that info for completion
        if self._any_request_failed:
            exit_code = 1
            error = error or self._last_error_message
            error_type = error_type or self._last_error_type

        data = {
            "execution_context": execution_context,
            "exit_code": exit_code,
            "end_time": get_time_millis(),
        }

        if error:
            data["error"] = error[:500]  # Limit error message length
        if error_type:
            data["error_type"] = error_type

        message = {
            **self._basic_telemetry_data(),
            TelemetryField.KEY_TYPE.value: EventType.SUBMIT_COMPLETION.value,
            TelemetryField.KEY_DATA.value: data,
        }
        self._send(message)

    @safe
    def send_resolution_rule_telemetry(
        self, rule_name: str, rel_type: str, outcome: str
    ) -> None:
        """Emit a custom event when a proto-level resolution rule is exercised.

        outcome is one of "applied", "declined", or "error". This is a custom
        event (not part of request_summary) so we can track how often the
        Catalyst-style resolution rules fire in production.
        """
        data = {
            "rule_name": rule_name,
            "rel_type": rel_type,
            "outcome": outcome,
        }
        summary = self._request_summary.get()
        if spark_session_id := summary.get("spark_session_id"):
            data["spark_session_id"] = spark_session_id
        if operation_id := summary.get("spark_operation_id"):
            data["spark_operation_id"] = operation_id

        message = {
            **self._basic_telemetry_data(),
            TelemetryField.KEY_TYPE.value: TelemetryType.TYPE_EVENT.value,
            TelemetryType.EVENT_TYPE.value: EventType.RESOLUTION_RULE.value,
            TelemetryField.KEY_DATA.value: data,
        }
        self._send(message)

    @safe
    def send_null_type_fallback_telemetry(
        self,
        data: dict[str, Any],
        plan_id: int | None,
        source: str,
    ) -> None:
        """Emitted when a column/argument type resolves to None and falls back to NullType.

        source distinguishes the call site: "map_with_columns" or "map_unresolved_function/in".
        data carries the context-specific fields (differs per call site).
        plan_id and spark_session_id are injected automatically.
        """
        payload = dict(data)
        payload["source"] = source
        if plan_id is not None:
            payload["plan_id"] = plan_id
        summary = self._request_summary.get()
        if spark_session_id := summary.get("spark_session_id"):
            payload["spark_session_id"] = spark_session_id
        if operation_id := summary.get("spark_operation_id"):
            payload["spark_operation_id"] = operation_id

        message = {
            **self._basic_telemetry_data(),
            TelemetryField.KEY_TYPE.value: TelemetryType.TYPE_EVENT.value,
            TelemetryType.EVENT_TYPE.value: EventType.NULL_TYPE_FALLBACK.value,
            TelemetryField.KEY_DATA.value: payload,
        }
        self._send(message)

    @safe
    def send_request_summary_telemetry(self):
        if self._not_in_request():
            self.send_warning_msg(
                "Trying to send request summary telemetry without initializing it"
            )
            return

        summary = self._request_summary.get()
        message = {
            **self._basic_telemetry_data(),
            TelemetryField.KEY_TYPE.value: TelemetryType.TYPE_REQUEST_SUMMARY.value,
            TelemetryField.KEY_DATA.value: summary,
        }
        self._send(message)

    def send_warning_msg(self, msg: str, e: Exception = None) -> None:
        # using this within @safe decorator may result in recursive loop
        try:
            message = self._build_warning_message(msg, e)
            if not message:
                return

            self._send(message, is_warning=True)
        except Exception:
            # if there's an exception here, there's nothing we can really do about it
            pass

    def _build_warning_message(self, warning_msg: str, e: Exception = None) -> dict:
        try:
            data = {"warning_message": warning_msg}
            if e is not None:
                data["exception"] = repr(e)

            # add session and operation id if available
            spark_session_id = self._request_summary.get().get("spark_session_id", None)
            if spark_session_id is not None:
                data["spark_session_id"] = spark_session_id

            spark_operation_id = self._request_summary.get().get(
                "spark_operation_id", None
            )
            if spark_operation_id is not None:
                data["spark_operation_id"] = spark_operation_id

            message = {
                **self._basic_telemetry_data(),
                TelemetryField.KEY_TYPE.value: TelemetryType.TYPE_EVENT.value,
                TelemetryType.EVENT_TYPE.value: EventType.WARNING.value,
                TelemetryField.KEY_DATA.value: data,
            }
            return message
        except Exception:
            return {}

    def _send(self, msg: dict, is_warning: bool = False) -> None:
        """Queue a telemetry message for asynchronous processing."""
        if not self._is_enabled:
            return

        timestamp = get_time_millis()
        try:
            telemetry_msg = TelemetryMessage(
                message=msg, timestamp=timestamp, is_warning=is_warning
            )
            self._message_queue.put_nowait(telemetry_msg)
        except queue.Full:
            # If queue is full, drop the message to avoid blocking
            logger.warning("Telemetry queue is full, dropping message")

    def _start_worker_thread(self) -> None:
        """Start the background worker thread for processing telemetry messages."""
        if self._worker_thread is None:
            self._worker_thread = threading.Thread(
                target=self._worker_loop, daemon=True, name="TelemetryWorker"
            )
            self._worker_thread.start()

    def _worker_loop(self) -> None:
        """Worker thread loop that processes messages from the queue."""
        while True:
            try:
                # block to allow the GIL to switch threads
                telemetry_msg = self._message_queue.get()
                if telemetry_msg is None:
                    # shutdown signal
                    break
                self._sink.add_telemetry_data(
                    telemetry_msg.message, telemetry_msg.timestamp
                )
            except Exception as e:
                if not telemetry_msg.is_warning:
                    self.send_warning_msg("Failed to add telemetry message to sink", e)
            finally:
                self._message_queue.task_done()

        # Flush the sink
        self._sink.flush()

    def shutdown(self) -> None:
        """Shutdown the telemetry worker thread and flush any remaining messages."""
        if not self._worker_thread or not self._worker_thread.is_alive():
            # No worker or already dead, nothing to do
            return

        try:
            self._message_queue.put_nowait(None)
            # Wait for worker thread to finish
            self._worker_thread.join(timeout=3.0)
        except Exception:
            logger.warning(
                "Could not put shutdown message on telemetry queue", exc_info=True
            )


def _error_location(e: Exception) -> dict | None:
    """
    Inspect the exception traceback and extract the file name, line number, and function name
    from the last frame (the one that raised the exception).
    """
    tb = e.__traceback__
    if tb is None:
        return None

    while tb.tb_next is not None:
        tb = tb.tb_next

    # Get just the file name without the path
    full_path = tb.tb_frame.f_code.co_filename
    file_name = full_path.split("/")[-1]

    return {
        "file": file_name,
        "line": tb.tb_lineno,
        "fn": tb.tb_frame.f_code.co_name,
    }


def _is_map_field(field_descriptor) -> bool:
    """
    Check if a protobuf field is a map.

    Uses a try/except guard to handle protobuf version differences where
    the upb C-extension FieldDescriptor may not expose 'label' as a Python
    attribute (observed as AttributeError in protobuf 4.x environments).
    """
    try:
        return (
            field_descriptor.label == field_descriptor.LABEL_REPEATED
            and field_descriptor.message_type is not None
            and field_descriptor.message_type.has_options
            and field_descriptor.message_type.GetOptions().map_entry
        )
    except AttributeError:
        return False


_ANY_UNPACK_REGISTRY: dict[str, type] | None = None


def _get_any_unpack_registry() -> dict[str, type]:
    # Benign race: concurrent threads may both build the registry, but the
    # assignment is idempotent (same dict contents) and atomic under the GIL.
    global _ANY_UNPACK_REGISTRY
    if _ANY_UNPACK_REGISTRY is None:
        from snowflake.snowpark_connect.proto import (
            snowflake_expression_ext_pb2 as sf_expr,
            snowflake_relation_ext_pb2 as sf_rel,
        )

        _ANY_UNPACK_REGISTRY = {
            sf_rel.Extension.DESCRIPTOR.full_name: sf_rel.Extension,
            sf_expr.ExpExtension.DESCRIPTOR.full_name: sf_expr.ExpExtension,
        }
    return _ANY_UNPACK_REGISTRY


def _try_unpack_any(any_msg: "AnyProto") -> google.protobuf.message.Message | None:
    registry = _get_any_unpack_registry()
    type_name = (
        any_msg.type_url.split("/")[-1] if "/" in any_msg.type_url else any_msg.type_url
    )
    msg_class = registry.get(type_name)
    if msg_class is None:
        return None
    try:
        unpacked = msg_class()
        if any_msg.Unpack(unpacked):
            return unpacked
    except Exception as e:
        telemetry.send_warning_msg(
            f"Failed to unpack Any with type_url={any_msg.type_url!r}: {e}"
        )
    return None


# Query-string parameter names that carry credential material in storage URLs.
# Presence of any of these in a path's query string means the whole query is a
# signed/SAS credential and must be stripped. Compared case-insensitively.
_CREDENTIAL_QUERY_KEYS = frozenset(
    {
        # AWS SigV4 presigned URL params
        "x-amz-signature",
        "x-amz-credential",
        "x-amz-security-token",
        "x-amz-algorithm",
        "x-amz-date",
        "x-amz-expires",
        "x-amz-signedheaders",
        "awsaccesskeyid",
        "signature",
        # Azure SAS token params
        "sig",
        "se",
        "sp",
        "spr",
        "sv",
        "ss",
        "srt",
        "st",
        "skoid",
        "sktid",
        "skt",
        "ske",
        "sks",
        "skv",
        # GCS signed URL params
        "x-goog-signature",
        "x-goog-credential",
        "x-goog-algorithm",
        "goog-signature",
        # generic credential-bearing params
        "access_key",
        "accesskey",
        "secret_key",
        "secretkey",
        "token",
        "password",
        "passwd",
        "pwd",
        "credential",
        "credentials",
    }
)

# scheme://user:password@host  ->  the password is credential material.
# Azure paths like abfss://container@account.dfs.core.windows.net/path have an
# '@' but no ':' in the userinfo, so they are left untouched by design.
_URL_USERINFO_PASSWORD_RE = re.compile(r"(://[^/:@?#]*):[^/@?#]+@")


def _query_has_credentials(query: str) -> bool:
    """True if any query-string parameter name looks like a credential."""
    for part in re.split(r"[&;]", query):
        key = part.split("=", 1)[0].strip().lower()
        if key in _CREDENTIAL_QUERY_KEYS:
            return True
    return False


def _sanitize_path_value(value):
    """Strip credential material from a storage path while keeping the path itself.

    A plain path (``s3://bucket/data/``, ``@stage/file.parquet``,
    ``abfss://container@account.dfs.core.windows.net/path``) is returned
    unchanged. Credential material is removed in two cases:
      - a query string carrying a presigned-URL signature or Azure SAS token
        (``...?X-Amz-Signature=...`` / ``...?sig=...``) -> query replaced with
        ``?<redacted>``;
      - a password embedded in URL userinfo (``scheme://user:pass@host``) ->
        the password replaced with ``<redacted>``.
    Non-string values are returned unchanged.
    """
    if not isinstance(value, str) or not value:
        return value

    sanitized = value
    base, sep, query = sanitized.partition("?")
    if sep and _query_has_credentials(query):
        sanitized = f"{base}?<redacted>"

    sanitized = _URL_USERINFO_PASSWORD_RE.sub(r"\1:<redacted>@", sanitized, count=1)
    return sanitized


def _protobuf_to_json_with_redaction(
    message: google.protobuf.message.Message, redacted_suffixes: list[str]
) -> dict:
    """
    Convert a protobuf Message to JSON dict with selective field redaction.

    Args:
        message: The protobuf Message to convert
        redacted_suffixes: List of field path suffixes to redact (e.g. ["jdbc.options"])

    Returns:
        Dictionary representation with specified fields redacted
    """

    MAX_MESSAGE_SIZE = 200 * 1024  # 200KB
    MAX_DEPTH = 100  # guard against RecursionError on pathologically nested plans

    def _convert_field_value(value, field_descriptor, field_path: str, depth: int):
        """Convert a protobuf field value to its JSON representation"""
        # Check if this field should be redacted
        should_redact = any(field_path.endswith(suffix) for suffix in redacted_suffixes)
        if should_redact:
            return "<redacted>"

        # Path-bearing fields are value-sanitized (credentials stripped) rather
        # than blanket-redacted, so plain paths stay visible for debugging.
        should_sanitize_path = any(
            field_path.endswith(suffix) for suffix in SANITIZED_PATH_SUFFIXES
        )

        # Bytes fields (TYPE_BYTES) are opaque binary blobs (pickled functions,
        # Arrow data, packed extension payloads, etc.) that must not be passed
        # to json.dumps as raw bytes.  Redact them instead of encoding.
        if field_descriptor.type == field_descriptor.TYPE_BYTES:
            return "<bytes>"

        # Handle different field types
        if _is_map_field(field_descriptor):
            value_descriptor = field_descriptor.message_type.fields_by_name["value"]
            if value_descriptor.type == value_descriptor.TYPE_MESSAGE:
                return {
                    str(k): _protobuf_to_json_recursive(v, field_path, depth)
                    for k, v in value.items()
                }
            else:
                return dict(value)
        elif field_descriptor.type == field_descriptor.TYPE_MESSAGE:
            if field_descriptor.label == field_descriptor.LABEL_REPEATED:
                # Repeated message field
                return [
                    _protobuf_to_json_recursive(item, field_path, depth)
                    for item in value
                ]
            else:
                # Singular message field
                return _protobuf_to_json_recursive(value, field_path, depth)
        elif field_descriptor.label == field_descriptor.LABEL_REPEATED:
            # Repeated scalar field
            if should_sanitize_path:
                return [_sanitize_path_value(v) for v in value]
            return list(value)
        else:
            # Singular scalar field
            if should_sanitize_path:
                return _sanitize_path_value(value)
            return value

    def _protobuf_to_json_recursive(
        msg: google.protobuf.message.Message, current_path: str = "", depth: int = 0
    ) -> dict:
        """Recursively convert protobuf message to dict"""

        if depth >= MAX_DEPTH:
            return "<too_deep>"

        if not isinstance(msg, google.protobuf.message.Message):
            telemetry.send_warning_msg(f"Expected a protobuf message, got: {type(msg)}")
            return {}

        if isinstance(msg, AnyProto) and msg.type_url:
            unpacked = _try_unpack_any(msg)
            if unpacked is not None:
                return _protobuf_to_json_recursive(unpacked, current_path, depth)

        result = {}

        # Use ListFields() to get all set fields
        for field_descriptor, field_value in msg.ListFields():
            field_name = field_descriptor.name
            field_path = f"{current_path}.{field_name}" if current_path else field_name

            # Convert the field value
            result[field_name] = _convert_field_value(
                field_value, field_descriptor, field_path, depth + 1
            )

        return result

    try:
        size = message.ByteSize()
    except RecursionError:
        # ByteSize() traverses the proto tree in C; when the Python call stack is
        # already near its limit, even a C-level traversal can trigger
        # "RecursionError: maximum recursion depth exceeded while calling a Python object".
        return "<recursion_error>"

    if size > MAX_MESSAGE_SIZE:
        return "<too_big>"

    try:
        return _protobuf_to_json_recursive(message)
    except RecursionError:
        return "<recursion_error>"


def _set_query_plan(request: google.protobuf.message.Message, summary: dict) -> None:
    if isinstance(request, proto_base.ExecutePlanRequest):
        # ExecutePlanRequest has plan at top level
        if hasattr(request, "plan"):
            summary["query_plan"] = _protobuf_to_json_with_redaction(
                request.plan, REDACTED_PLAN_SUFFIXES
            )

    elif isinstance(request, proto_base.AnalyzePlanRequest):
        # AnalyzePlanRequest has plan under oneof analyze
        analyze_type = request.WhichOneof("analyze")
        if not analyze_type:
            return

        summary["analyze_type"] = analyze_type
        analyze_field = getattr(request, analyze_type)
        if hasattr(analyze_field, "plan"):
            summary["query_plan"] = _protobuf_to_json_with_redaction(
                analyze_field.plan, REDACTED_PLAN_SUFFIXES
            )


# global telemetry client
telemetry = Telemetry(is_enabled="SNOWPARK_CONNECT_DISABLE_TELEMETRY" not in os.environ)


class SnowparkConnectNotImplementedError(NotImplementedError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
