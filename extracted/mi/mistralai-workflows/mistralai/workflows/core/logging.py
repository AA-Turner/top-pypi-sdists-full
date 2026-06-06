"""
Monitoring and logging configuration utilities.

This module provides structured logging setup using structlog.
"""

import json
import logging
from enum import StrEnum
from typing import Any

import structlog
import temporalio.activity
import temporalio.workflow
from opentelemetry import trace
from pydantic import BaseModel
from structlog.typing import EventDict, Processor

from mistralai.workflows.worker_client.errors import SDKError


class Env(StrEnum):
    DEV = "development"
    STAGING = "staging"
    PROD = "production"


class LogFormat(StrEnum):
    JSON = "json"
    CONSOLE = "console"


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggerConfig(BaseModel):
    name: str
    level: LogLevel


def _get_log_level_value(level: LogLevel) -> int:
    level_map = {
        LogLevel.DEBUG: logging.DEBUG,
        LogLevel.INFO: logging.INFO,
        LogLevel.WARNING: logging.WARNING,
        LogLevel.ERROR: logging.ERROR,
        LogLevel.CRITICAL: logging.CRITICAL,
    }
    return level_map[level]


def _try_get_workflow_info() -> temporalio.workflow.Info | None:
    try:
        return temporalio.workflow.info()
    except Exception:
        return None


def _try_get_activity_info() -> temporalio.activity.Info | None:
    try:
        return temporalio.activity.info()
    except Exception:
        return None


def _add_temporal_context_processor(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    del logger, method_name
    workflow_id: str | None
    run_id: str | None

    if (workflow_info := _try_get_workflow_info()) is not None:
        workflow_id = getattr(workflow_info, "workflow_id", None)
        run_id = getattr(workflow_info, "run_id", None)
    elif (activity_info := _try_get_activity_info()) is not None:
        workflow_id = getattr(activity_info, "workflow_id", None)
        run_id = getattr(activity_info, "workflow_run_id", None)
    else:
        return event_dict

    if workflow_id is None or run_id is None:
        return event_dict

    event_dict.setdefault("workflow.execution_id", workflow_id)
    event_dict.setdefault("workflow.run_id", run_id)
    return event_dict


def _add_otel_trace_processor(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    span = trace.get_current_span()
    if span:
        ctx = span.get_span_context()
        if ctx.is_valid:
            event_dict["otel.trace_id"] = format(ctx.trace_id, "032x")
            event_dict["otel.span_id"] = format(ctx.span_id, "016x")

    return event_dict


def setup_logging(
    log_level: LogLevel = LogLevel.INFO,
    log_format: LogFormat = LogFormat.CONSOLE,
    app_version: str = "0.0.0",
    inject_otel_trace: bool = False,
    extra_config: list[LoggerConfig] | None = None,
) -> None:
    logging.basicConfig(
        format="%(message)s",
        level=_get_log_level_value(log_level),
    )

    if extra_config:
        for logger_config in extra_config:
            logger = logging.getLogger(logger_config.name)
            logger.setLevel(_get_log_level_value(logger_config.level))

    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    processors.append(_add_temporal_context_processor)

    if inject_otel_trace:
        processors.append(_add_otel_trace_processor)

    processors.append(
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.PATHNAME,
                structlog.processors.CallsiteParameter.LINENO,
            }
        )
    )

    if log_format == LogFormat.JSON:
        processors.extend(
            [
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer(),
            ]
        )
    else:
        processors.extend(
            [
                structlog.processors.format_exc_info,
                structlog.dev.ConsoleRenderer(),
            ]
        )

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def extract_error_context(exc: Exception) -> dict:
    ctx: dict = {
        "error_type": type(exc).__name__,
        "error_message": str(exc),
    }
    seen: set[int] = set()
    current: BaseException | None = exc
    while current is not None:
        if id(current) in seen:
            break
        seen.add(id(current))
        if isinstance(current, SDKError):
            ctx["http_status"] = getattr(current, "status_code", None)
            body = getattr(current, "body", None)
            ctx["api_error_body"] = body
            if body:
                try:
                    parsed = json.loads(body)
                    if isinstance(parsed, dict):
                        if "code" in parsed:
                            ctx["api_error_code"] = parsed["code"]
                        if "message" in parsed:
                            ctx["api_error_message"] = parsed["message"]
                except (json.JSONDecodeError, TypeError):
                    pass
            break
        if current.__cause__ is not None:
            current = current.__cause__
        elif not current.__suppress_context__:
            current = current.__context__
        else:
            break
    return ctx
