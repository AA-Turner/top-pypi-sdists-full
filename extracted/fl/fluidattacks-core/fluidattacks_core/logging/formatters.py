import logging
import traceback
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import simplejson as json  # type: ignore[import-untyped]
from pythonjsonlogger.json import JsonFormatter

from fluidattacks_core.logging.utils import get_environment_metadata, get_job_metadata

# Main formats
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
"""
Default date format for logs.
"""

_JOB_METADATA = get_job_metadata()
_ENVIRONMENT_METADATA = get_environment_metadata()


class ColorfulFormatter(logging.Formatter):
    grey: str = "\x1b[38;1m"
    yellow: str = "\x1b[33;1m"
    red: str = "\x1b[31;1m"
    reset: str = "\x1b[0m"
    msg_format: str = "{asctime} [{levelname}] [{name}] {message}"

    FORMATS = {  # noqa: RUF012
        logging.DEBUG: grey + msg_format + reset,
        logging.INFO: msg_format,
        logging.WARNING: yellow + msg_format + reset,
        logging.ERROR: red + msg_format + reset,
        logging.CRITICAL: red + msg_format + reset,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(
            log_fmt,
            datefmt=self.datefmt,
            style="{",
        )
        return formatter.format(record)


class CustomJsonFormatter(JsonFormatter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        def json_default(object_: object) -> Any:
            if isinstance(object_, set):
                return list(object_)
            if isinstance(object_, datetime):
                return object_.astimezone(tz=UTC).isoformat()
            if isinstance(object_, float):
                return Decimal(str(object_))

            return object_

        super().__init__(*args, **kwargs, json_serializer=json.dumps, json_default=json_default)

    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)
        log_timestamp = None
        if timestamp := log_record.get("timestamp"):
            if isinstance(timestamp, int):
                log_timestamp = timestamp
            elif isinstance(timestamp, str) and timestamp.isdigit():
                log_timestamp = int(timestamp)

        env = get_environment_metadata().environment
        version = get_environment_metadata().version
        service = f"{get_environment_metadata().product_id}" + (
            f"/{get_job_metadata().job_queue}" if get_job_metadata().job_id is not None else ""
        )

        log_record["timestamp"] = log_timestamp or round(datetime.now(tz=UTC).timestamp() * 1000)
        log_record["level"] = log_record.get("level") or record.levelname
        log_record["name"] = record.name
        log_record["file_location"] = f"{record.filename}:{record.lineno}"
        log_record["lineno"] = record.lineno

        log_record["deployment.environment"] = env
        log_record["service.version"] = version
        log_record["service.name"] = service

        log_record["dd.environment"] = env
        log_record["dd.version"] = version
        log_record["dd.service"] = service

        self._add_error_fields(log_record, record)
        self._add_opentelemetry_fields(log_record)
        self._add_extra_fields(log_record)

    def _add_error_fields(self, log_record: dict[str, Any], record: logging.LogRecord) -> None:
        """Add error fields: `error.type`, `error.message`, `error.stack`."""
        if record.exc_info:
            if exc_type := record.exc_info[0]:
                log_record["error.type"] = exc_type.__name__
            if exc_value := record.exc_info[1]:
                log_record["error.message"] = str(exc_value)
            if exc_tb := record.exc_info[2]:
                log_record["error.stack"] = "".join(traceback.format_tb(exc_tb))

            # Remove duplicated info
            log_record.pop("exc_info", None)

    def _add_opentelemetry_fields(self, log_record: dict[str, Any]) -> None:
        """Add OpenTelemetry fields: `trace_id`, `span_id`, `trace_sampled`."""
        if log_record.get("otelTraceID") is not None:
            log_record["trace_id"] = log_record.pop("otelTraceID")

        if log_record.get("otelSpanID") is not None:
            log_record["span_id"] = log_record.pop("otelSpanID")

        if log_record.get("otelTraceSampled") is not None:
            log_record["trace_sampled"] = log_record.pop("otelTraceSampled")

    def _add_extra_fields(self, log_record: dict[str, Any]) -> None:
        """Add extra fields or override existing fields."""
        if log_record.get("extra") is None:
            log_record.pop("extra", None)
        elif isinstance(log_record.get("extra"), dict):
            log_record.update(log_record["extra"])
            log_record.pop("extra", None)
