#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
SPCS Logger - Adapted from ExecPlatform/src/coprocessor/python/telemetry/py/logger.py
Outputs flat JSON format compatible with SPCS OpenTelemetry collector with proper trace context.
"""

import json
import logging
import sys
import traceback
from typing import Any, Mapping, Sequence


class SPCSLoggerConfig:
    """Configuration for SPCS logger."""

    MESSAGE_SIZE_LIMIT_BYTES = 524288  # 512KB
    ELLIPSIS = "..."

    # Set to True if initialized
    is_initialized = False


def _encode_value_simple(value: Any) -> Any:
    """
    Encode a value to simple JSON format (not OpenTelemetry nested format).
    SPCS expects flat JSON values, not the {stringValue: ...} format.
    """
    if isinstance(value, (bool, str, int, float)):
        return value
    if isinstance(value, Sequence) and not isinstance(value, str):
        return [_encode_value_simple(v) for v in value]
    if isinstance(value, Mapping):
        return {str(k): _encode_value_simple(v) for k, v in value.items()}
    # Stringify anything else
    return str(value)


# Skip Python's built-in LogRecord attributes
_RESERVED_ATTRS = frozenset(
    (
        "asctime",
        "args",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "message",
        "levelname",
        "levelno",
        "lineno",
        "module",
        "msecs",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "thread",
        "threadName",
        "taskName",
    )
)


def _extract_attributes(record: logging.LogRecord) -> dict:
    """Extract log record attributes to flat dict format for SPCS."""
    attributes = {}

    # Extract custom attributes from extra={}
    for k, v in vars(record).items():
        if k not in _RESERVED_ATTRS:
            attributes[k] = _encode_value_simple(v)

    # Add standard code location attributes
    attributes["code.lineno"] = record.lineno
    attributes["code.function"] = record.funcName
    attributes["code.filepath"] = record.pathname

    # Add exception info if present
    if record.exc_info is not None:
        exctype, value, tb = record.exc_info
        if exctype is not None:
            attributes["exception.type"] = exctype.__name__
        if value is not None and value.args:
            attributes["exception.message"] = str(value.args[0])
        if tb is not None:
            attributes["exception.stacktrace"] = "".join(
                traceback.format_exception(*record.exc_info)
            )

    return attributes


def get_snowflake_log_level_name(py_level_name: str) -> str:
    """
    Convert Python log level to Snowflake log level.
    This matches the original UDF logger implementation.
    """
    level = py_level_name.upper()
    if level == "WARNING":
        return "WARN"
    elif level == "CRITICAL":
        return "FATAL"
    elif level == "NOTSET":
        return "TRACE"
    else:
        return level


def get_severity_number(snowflake_level: str) -> int:
    """
    Get OTLP severity number (integer) for a Snowflake log level.

    OTLP Spec: https://opentelemetry.io/docs/specs/otel/logs/data-model/#field-severitynumber
    This returns INTEGER values (not strings like the buggy UDF code).
    """
    if snowflake_level == "TRACE":
        return 1  # SEVERITY_NUMBER_TRACE
    elif snowflake_level == "DEBUG":
        return 5  # SEVERITY_NUMBER_DEBUG
    elif snowflake_level == "INFO":
        return 9  # SEVERITY_NUMBER_INFO
    elif snowflake_level == "WARN":
        return 13  # SEVERITY_NUMBER_WARN
    elif snowflake_level == "ERROR":
        return 17  # SEVERITY_NUMBER_ERROR
    elif snowflake_level == "FATAL":
        return 21  # SEVERITY_NUMBER_FATAL
    else:
        return 0  # SEVERITY_NUMBER_UNSPECIFIED


def _encode_spcs_log_record(record: logging.LogRecord) -> dict:
    """
    Encode a log record to the FLAT JSON format expected by SPCS.

    SPCS OpenTelemetry collector expects:
    {
      "body": "message",
      "severity_text": "INFO",
      "severity_number": 9,          # INTEGER, not string!
      "attributes": {...},
      "scope": {"name": "logger_name"}
    }
    """
    # Format the message
    message = str(record.msg)
    if record.args:
        try:
            message = message % record.args
        except (TypeError, ValueError):
            message = str(record.msg)

    # Truncate message if it exceeds size limit
    message_bytes = message.encode("utf-8", errors="replace")
    if sys.getsizeof(message_bytes) > SPCSLoggerConfig.MESSAGE_SIZE_LIMIT_BYTES:
        truncate_length = SPCSLoggerConfig.MESSAGE_SIZE_LIMIT_BYTES - len(
            SPCSLoggerConfig.ELLIPSIS.encode()
        )
        # Ensure we don't cut in the middle of a UTF-8 multibyte sequence
        while truncate_length > 0 and (message_bytes[truncate_length] & 0xC0) == 0x80:
            truncate_length -= 1
        message_bytes = message_bytes[0:truncate_length]
        message = (
            message_bytes.decode("utf-8", errors="replace") + SPCSLoggerConfig.ELLIPSIS
        )

    # Map to Snowflake log level
    snowflake_level = get_snowflake_log_level_name(record.levelname)

    # Construct the FLAT log record (NOT nested OpenTelemetry structure)
    log_record = {
        "body": message,
        "severity_text": snowflake_level,
        "severity_number": get_severity_number(snowflake_level),  # INTEGER!
        "attributes": _extract_attributes(record),
        "scope": {"name": record.name},
    }

    return log_record


# =============================================================================
# SPCS-SPECIFIC HANDLER
# =============================================================================


class SPCSStreamHandler(logging.StreamHandler):
    """
    Custom handler for SPCS that writes flat JSON format to stdout.

    The SPCS OpenTelemetry collector will:
    1. Capture stdout
    2. Parse JSON if line matches ^{.*}$
    3. Extract body, severity_text, severity_number, attributes, scope, trace_id, span_id fields
    4. Map trace_id/span_id to LogRecord protobuf fields
    5. Backend creates TRACE column from protobuf trace_id/span_id
    6. Route to Event Table
    """

    def __init__(self, stream=None) -> None:
        """
        Initialize the handler.

        Args:
            stream: Output stream (default: sys.stdout)
        """
        super().__init__(stream or sys.stdout)

    def emit(self, record: logging.LogRecord):
        """
        Emit a log record as single-line JSON to stdout.
        """
        try:
            # Encode to SPCS-compatible flat JSON format
            log_record = _encode_spcs_log_record(record)

            # Convert to compact JSON string (single line, no spaces)
            log_json = json.dumps(log_record, separators=(",", ":"))

            # Write to stdout (SPCS captures this)
            self.stream.write(log_json + "\n")
            self.flush()

        except Exception:
            self.handleError(record)


# =============================================================================
# INITIALIZATION FUNCTIONS
# =============================================================================


def setup_spcs_logger(
    log_level: int = logging.INFO,
    logger_name: str = None,
    enable_console_output: bool = False,
) -> logging.Logger:
    """
    Set up the root logger for SPCS with flat JSON formatting.

    Args:
        log_level: Python logging level (e.g., logging.INFO)
        logger_name: Optional logger name (None for root logger)
        enable_console_output: If True, also adds a human-readable console handler to stderr

    Returns:
        Configured logger instance

    Example:
        >>> logger = setup_spcs_logger(logging.INFO, enable_console_output=True)
        >>> logger.info("Hello from SPCS", extra={"user_id": 123, "action": "login"})

        # Output to stdout (captured by SPCS):
        {"body":"Hello from SPCS","severity_text":"INFO","severity_number":9,"attributes":{"user_id":123,"action":"login","code.lineno":42,"code.function":"main","code.filepath":"/app/main.py"},"scope":{"name":"root"}}

        # Output to stderr (if enable_console_output=True):
        2024-01-15 10:30:45,123 - root - INFO - Hello from SPCS
    """
    # Mark as initialized
    SPCSLoggerConfig.is_initialized = True

    # Get logger (root or named)
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    logger.handlers.clear()

    # Add SPCS flat JSON handler (writes JSON to stdout)
    spcs_handler = SPCSStreamHandler(sys.stdout)
    spcs_handler.setLevel(log_level)
    logger.addHandler(spcs_handler)

    # Optionally add human-readable console handler (to stderr to avoid mixing with JSON logs)
    if enable_console_output:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(log_level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
