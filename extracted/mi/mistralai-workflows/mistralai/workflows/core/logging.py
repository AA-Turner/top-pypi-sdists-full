"""
Monitoring and logging configuration utilities.

This module provides structured logging setup using structlog.
"""

import json
import logging
from enum import StrEnum
from typing import Any, TypedDict

import structlog
import temporalio.activity
import temporalio.workflow
from opentelemetry import trace
from pydantic import BaseModel
from structlog.typing import EventDict, Processor

from mistralai.workflows.core._events.event_utils import try_get_lineage_workflow_exec_id
from mistralai.workflows.worker_client.errors import SDKError


class ErrorContext(TypedDict, total=False):
    error_type: str
    error_message: str
    http_status: int | None
    api_error_body: str | None
    api_error_code: str
    api_error_message: str


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

    root_id, parent_id = try_get_lineage_workflow_exec_id()
    if root_id is not None:
        event_dict.setdefault("workflow.root_execution_id", root_id)
    if parent_id is not None:
        event_dict.setdefault("workflow.parent_execution_id", parent_id)
    return event_dict


def _add_otel_trace_processor(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    span = trace.get_current_span()
    if span:
        ctx = span.get_span_context()
        if ctx.is_valid:
            event_dict["otel.trace_id"] = format(ctx.trace_id, "032x")
            event_dict["otel.span_id"] = format(ctx.span_id, "016x")

    return event_dict


_shared_processors: list[Processor] = []


def _build_shared_processors(inject_otel_trace: bool) -> list[Processor]:
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        _add_temporal_context_processor,
    ]

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
    return processors


def _build_formatter(renderer: Processor) -> structlog.stdlib.ProcessorFormatter:
    return structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=_shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.format_exc_info,
            renderer,
        ],
    )


def build_json_log_formatter() -> structlog.stdlib.ProcessorFormatter:
    """structlog formatter that always renders log records as JSON.

    Attached to the OTLP log handler so exported log bodies are JSON regardless of the
    console ``log_format`` chosen by the user. This is pure structlog (no OpenTelemetry);
    relies on ``setup_logging`` having populated the shared processor chain first.
    """
    return _build_formatter(structlog.processors.JSONRenderer())


def setup_logging(
    log_level: LogLevel = LogLevel.INFO,
    log_format: LogFormat = LogFormat.CONSOLE,
    app_version: str = "0.0.0",
    inject_otel_trace: bool = False,
    extra_config: list[LoggerConfig] | None = None,
) -> None:
    global _shared_processors
    _shared_processors = _build_shared_processors(inject_otel_trace)

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            *_shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    console_renderer: Processor = (
        structlog.processors.JSONRenderer() if log_format == LogFormat.JSON else structlog.dev.ConsoleRenderer()
    )
    handler = logging.StreamHandler()
    handler.setFormatter(_build_formatter(console_renderer))

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(_get_log_level_value(log_level))

    if extra_config:
        for logger_config in extra_config:
            logger = logging.getLogger(logger_config.name)
            logger.setLevel(_get_log_level_value(logger_config.level))


def extract_error_context(exc: Exception) -> ErrorContext:
    ctx: ErrorContext = {
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
