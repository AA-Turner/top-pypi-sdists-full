import logging
import traceback
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import simplejson as json
from pythonjsonlogger.json import JsonFormatter

from fluidattacks_core.logging.utils import (
    get_environment_metadata,
    get_job_metadata,
    get_pipeline_environment,
    get_pipeline_metadata,
    get_telemetry_metadata,
)

# Main formats
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
"""
Default date format for logs.
"""


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

            if hasattr(object_, "__dict__"):
                try:
                    return {k: v for k, v in object_.__dict__.items() if not k.startswith("_")}
                except (TypeError, ValueError, RecursionError):
                    return f"<{type(object_).__name__} object>"

            return object_

        super().__init__(*args, **kwargs, json_serializer=json.dumps, json_default=json_default)

    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)

        log_record["timestamp"] = self._get_timestamp(log_record)
        log_record["level"] = log_record.get("level") or record.levelname
        log_record["name"] = record.name
        log_record["file_location"] = f"{record.filename}:{record.lineno}"
        log_record["lineno"] = record.lineno

        self._add_service_fields(log_record)
        self._add_deployment_fields(log_record)

        self._add_default_telemetry_fields(log_record)
        self._add_error_fields(log_record, record)
        self._add_tracing_fields(log_record)
        self._add_extra_fields(log_record)

    def _get_timestamp(self, log_record: dict[str, Any]) -> int:
        if timestamp := log_record.get("timestamp"):
            if isinstance(timestamp, int):
                return timestamp
            if isinstance(timestamp, str) and timestamp.isdigit():
                return int(timestamp)
        return round(datetime.now(tz=UTC).timestamp() * 1000)

    def _add_service_fields(self, log_record: dict[str, Any]) -> None:
        """Add service information to the log record.

        It includes:
        - Version
        - Product name
        """
        batch_info = get_job_metadata().job_queue
        is_in_batch = get_job_metadata().job_id is not None
        product_name = get_environment_metadata().product_id
        service = f"{product_name}" + (f"/{batch_info}" if is_in_batch else "")
        version = get_environment_metadata().version

        log_record["dd.version"] = version
        log_record["service.version"] = version
        log_record["dd.service"] = service
        log_record["service.name"] = service

    def _add_deployment_fields(self, log_record: dict[str, Any]) -> None:
        """Add deployment information to the log record.

        It includes:
        - Environment
        - Pipeline where the log was generated
        """
        env = get_environment_metadata().environment

        log_record["dd.environment"] = env
        log_record["deployment.environment"] = env

        if pipeline := get_pipeline_environment():
            log_record["deployment.pipeline.type"] = pipeline.upper()
            for key, value in get_pipeline_metadata(pipeline).items():
                log_record[f"deployment.pipeline.{key}"] = value

    def _add_default_telemetry_fields(self, log_record: dict[str, Any]) -> None:
        """Add default metadata fields to the log record.

        Added fields via `set_telemetry_metadata` are included in this step.

        """
        for key, value in get_telemetry_metadata().items():
            log_record[key] = value  # noqa: PERF403

    def _add_error_fields(self, log_record: dict[str, Any], record: logging.LogRecord) -> None:
        """Add error fields to the log record.

        It includes:
        - `error.type`
        - `error.message`
        - `error.stack`
        """
        if record.exc_info:
            if exc_type := record.exc_info[0]:
                log_record["error.type"] = exc_type.__name__
            if exc_value := record.exc_info[1]:
                log_record["error.message"] = str(exc_value)
            if exc_tb := record.exc_info[2]:
                log_record["error.stack"] = "".join(traceback.format_tb(exc_tb))

            # Remove duplicated info
            log_record.pop("exc_info", None)

    def _add_tracing_fields(self, log_record: dict[str, Any]) -> None:
        """Add tracing fields (by OpenTelemetry) to the log record.

        It includes:
        - `trace_id`
        - `span_id`
        - `trace_sampled`
        """
        if log_record.get("otelTraceID") is not None:
            log_record["trace_id"] = log_record.pop("otelTraceID")

        if log_record.get("otelSpanID") is not None:
            log_record["span_id"] = log_record.pop("otelSpanID")

        if log_record.get("otelTraceSampled") is not None:
            log_record["trace_sampled"] = log_record.pop("otelTraceSampled")

    def _add_extra_fields(self, log_record: dict[str, Any]) -> None:
        """Add fields from `extra` to the log record.

        It adds fields at the top level, allowing them to override existing fields.
        """
        if log_record.get("extra") is None:
            log_record.pop("extra", None)
        elif isinstance(log_record.get("extra"), dict):
            log_record.update(log_record["extra"])
            log_record.pop("extra", None)
