"""
Monitoring and logging configuration utilities.

This module provides structured logging setup using structlog.
"""

import base64
import json
import logging
import os
import re
from enum import StrEnum
from typing import Any, TypedDict
from urllib.parse import quote, quote_plus

import httpx
import structlog
import temporalio.activity
import temporalio.workflow
from mistralai.client.errors import MistralError
from mistralai.extra.observability import DEFAULT_TOKEN_PATTERNS, RegexRedactionPolicy
from opentelemetry import trace
from pydantic import BaseModel, ValidationError
from structlog.typing import EventDict, Processor
from temporalio.service import RPCError

from mistralai.workflows.core._events.event_utils import try_get_lineage_workflow_exec_id
from mistralai.workflows.core._logger import _to_stdlib_call
from mistralai.workflows.worker_client.errors import SDKError


class ErrorContext(TypedDict, total=False):
    error_type: str
    error_chain: list[str]
    http_status: int | None
    api_error_code: str
    missing_module: str
    os_error_code: int
    rpc_status: str
    validation_error_count: int
    validation_error_types: list[str]


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


_CREDENTIAL_KEY = re.compile(
    r"api[_.-]?key|access[_.-]?key|private[_.-]?(?:key|access)|"
    r"token|password|secret|authorization|cookie|credential",
    re.IGNORECASE,
)
_USAGE_KEYS = frozenset(
    {
        "input_tokens",
        "output_tokens",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "max_tokens",
        "cached_tokens",
        "token_workflow_usage",
        "token_usage_source",
    }
)
_REDACTED = "[REDACTED]"
_LOG_PATTERNS = (
    *DEFAULT_TOKEN_PATTERNS,
    re.compile(r"(?i)(?:Bearer|Basic)\s+[A-Za-z0-9._~+/=-]+"),
    re.compile(r"(?i)(?<=://)[^/\s@]+@"),
    re.compile(r"(?i)(?<=[?&])(?:sig|signature|x-amz-signature|x-goog-signature|access_token)=[^&\s]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL),
)
_LOG_POLICY = RegexRedactionPolicy(patterns=_LOG_PATTERNS)
# Pattern scanning costs ~0.1 µs per character and runs on the workflow thread, so a
# multi-megabyte value logged from a workflow would trip Temporal's 2 s deadlock detector.
# Known credential values are still removed from strings of any size.
_PATTERN_SCAN_MAX_CHARS = 64 * 1024


def _redact_log_event(_logger: Any, _method_name: str, event_dict: EventDict) -> EventDict:
    # Run after exception formatting and before both console and OTLP rendering.
    try:
        # These SDK/CI switches control credential handling, but contain no credentials.
        non_credentials = {
            "TOKENIZERS_PARALLELISM",
            "HF_HUB_DISABLE_IMPLICIT_TOKEN",
            "BUILDKITE_USE_GITHUB_APP_GIT_CREDENTIALS",
            "BUILDKITE_USE_REPOSITORY_PROVIDER_GIT_CREDENTIALS",
        }
        secrets = [
            value
            for name, value in os.environ.items()
            if value
            and name not in non_credentials
            and name.lower() not in _USAGE_KEYS
            and _CREDENTIAL_KEY.search(name)
        ]
        for name in ("MISTRAL_API_HEADERS", "OTEL_EXPORTER_OTLP_HEADERS"):
            raw = os.environ.get(name, "")
            if not raw:
                continue
            try:
                headers = json.loads(raw)
            except json.JSONDecodeError:
                headers = dict(pair.split("=", 1) for pair in raw.split(",") if "=" in pair)
            if isinstance(headers, dict):
                secrets.extend(str(value) for key, value in headers.items() if _CREDENTIAL_KEY.search(key))
        needles: set[str] = set()
        for secret in secrets:
            needles.update(
                (
                    secret,
                    quote(secret, safe=""),
                    quote(secret),
                    quote_plus(secret),
                    json.dumps(secret)[1:-1],
                    base64.b64encode(secret.encode()).decode(),
                    base64.urlsafe_b64encode(secret.encode()).decode(),
                )
            )
        ordered = sorted(needles, key=len, reverse=True)

        def redact(value: Any) -> Any:
            if isinstance(value, str):
                for needle in ordered:
                    # Short credentials remain masked without erasing substrings in ordinary words.
                    value = (
                        re.sub(rf"(?<!\w){re.escape(needle)}(?!\w)", _REDACTED, value)
                        if len(needle) < 8
                        else value.replace(needle, _REDACTED)
                    )
                if len(value) > _PATTERN_SCAN_MAX_CHARS:
                    return value
                return _LOG_POLICY.redact_span_name(value)
            if isinstance(value, dict):
                return {
                    redact(str(key)): _REDACTED
                    if _CREDENTIAL_KEY.search(str(key)) and str(key).lower() not in _USAGE_KEYS
                    else redact(item)
                    for key, item in value.items()
                }
            if isinstance(value, (tuple, list)):
                return [redact(item) for item in value]
            if value is None or isinstance(value, (bool, int, float)):
                return value
            return redact(str(value))

        redacted: EventDict = redact(event_dict)
        return redacted
    except Exception:
        return {"event": "Log redaction failed; event omitted", "level": "error"}


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


class _HostEventMessage(str):
    """The text of an SDK event logged in host mode, carrying the event's fields for SDK formatters.

    It is the record's ``msg``: host handlers and exporters get a plain string from ``getMessage()``
    and the record has no extra attribute, so a host's own OTel handler exports nothing new.
    """

    fields: dict[str, Any]


def _to_host_stdlib_call(logger: Any, method_name: str, event_dict: EventDict) -> tuple[tuple[str], dict[str, Any]]:
    """Hand the event to the stdlib logger as text, keeping its fields in the message for SDK formatters."""
    fields = {key: value for key, value in event_dict.items() if key not in ("exc_info", "stack_info")}
    (text,), kwargs = _to_stdlib_call(logger, method_name, event_dict)
    if getattr(type(logger).findCaller, "__module__", None) == "structlog.stdlib":
        # structlog's stdlib logger class skips its own frames to find the caller; other loggers,
        # including application classes that override findCaller, need the stacklevel offset.
        del kwargs["stacklevel"]
    message = _HostEventMessage(text)
    message.fields = fields
    return (message,), kwargs


def _restore_host_event_fields(_logger: Any, _method_name: str, event_dict: EventDict) -> EventDict:
    """Give SDK formatters (the OTLP JSON one) the fields of an event logged in host mode, not its text."""
    message = getattr(event_dict.get("_record"), "msg", None)
    if not isinstance(message, _HostEventMessage):
        return event_dict
    restored = {**event_dict, **message.fields}
    # The record's stack was taken at the call; StackInfoRenderer would take a new one here.
    if stack := restored.pop("stack_info", None):
        restored["stack"] = stack
    return restored


def _build_formatter(
    renderer: Processor,
    redactor: Processor | None = None,
    *,
    redact_credentials: bool = True,
) -> structlog.stdlib.ProcessorFormatter:
    return structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=[_restore_host_event_fields, *_shared_processors],
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.format_exc_info,
            *([_redact_log_event] if redact_credentials else []),
            *([redactor] if redactor is not None else []),
            renderer,
        ],
    )


def build_json_log_formatter(
    redactor: Processor | None = None, *, redact_credentials: bool = True
) -> structlog.stdlib.ProcessorFormatter:
    """structlog formatter that always renders log records as JSON.

    Attached to the OTLP log handler so exported log bodies are JSON regardless of the
    console ``log_format`` chosen by the user. This is pure structlog (no OpenTelemetry);
    relies on ``setup_logging`` having populated the shared processor chain first.

    ``redactor`` runs on the event dict right before rendering, after exceptions are
    formatted, so it sees the final fields and the body stays valid JSON.
    ``redact_credentials=False`` skips the built-in credential masking, for callers that
    explicitly opted out of log redaction (``OTEL_REDACTION=none``).
    """
    return _build_formatter(structlog.processors.JSONRenderer(), redactor, redact_credentials=redact_credentials)


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


def route_logs_to_host_logging(inject_otel_trace: bool = False) -> None:
    """Send structlog events through the host's stdlib logging as text, leaving the root logger as it is.

    For a process that set up stdlib logging itself but not structlog: its handlers, levels and
    formatters stay, and the SDK's events reach them through the stdlib logger they name, as one
    text line with the exception and call site on the record (as before ``setup_logging``). The
    event's fields also ride in the record's message, so the OTLP log export still gets them as JSON fields.
    The host can still configure structlog later; no logger keeps this configuration cached.
    """
    global _shared_processors
    _shared_processors = _build_shared_processors(inject_otel_trace)

    # LoggerFactory() sets the global logger class; restore the host's so its loggers keep their methods.
    # Known gap: async methods such as ainfo() report a structlog frame as their file, function, line and
    # stack. Nothing in the SDK calls them, and fixing it would multiply this change roughly tenfold.
    host_logger_class = logging.getLoggerClass()
    factory = structlog.stdlib.LoggerFactory()
    logging.setLoggerClass(host_logger_class)

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.PositionalArgumentsFormatter(),
            _add_temporal_context_processor,
            *([_add_otel_trace_processor] if inject_otel_trace else []),
            _to_host_stdlib_call,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=factory,
        cache_logger_on_first_use=False,
    )


def extract_error_context(exc: BaseException) -> ErrorContext:
    """Extract useful exception diagnostics without exception messages or input values."""
    ctx: ErrorContext = {"error_type": type(exc).__name__}
    error_chain: list[str] = []
    seen: set[int] = set()
    http_diagnostics_captured = False
    current: BaseException | None = exc
    while current is not None:
        if id(current) in seen:
            break
        seen.add(id(current))
        error_chain.append(type(current).__name__)

        if isinstance(current, ValidationError) and "validation_error_count" not in ctx:
            errors = current.errors(include_url=False, include_context=False, include_input=False)
            ctx["validation_error_count"] = len(errors)
            ctx["validation_error_types"] = sorted({str(error["type"]) for error in errors})

        if isinstance(current, ModuleNotFoundError) and current.name is not None:
            ctx["missing_module"] = current.name

        if isinstance(current, OSError) and current.errno is not None:
            ctx["os_error_code"] = current.errno

        if isinstance(current, RPCError):
            ctx["rpc_status"] = current.status.name

        if not http_diagnostics_captured and isinstance(current, httpx.HTTPStatusError):
            http_diagnostics_captured = True
            ctx["http_status"] = current.response.status_code

        if not http_diagnostics_captured and isinstance(current, (SDKError, MistralError)):
            http_diagnostics_captured = True
            if (status_code := getattr(current, "status_code", None)) is not None:
                ctx["http_status"] = status_code
            body = getattr(current, "body", None)
            if body:
                try:
                    parsed = json.loads(body)
                    if isinstance(parsed, dict) and isinstance(parsed.get("code"), str):
                        ctx["api_error_code"] = parsed["code"]
                except (json.JSONDecodeError, TypeError):
                    pass

        if current.__cause__ is not None:
            current = current.__cause__
        elif not current.__suppress_context__:
            current = current.__context__
        else:
            break

    if len(error_chain) > 1:
        ctx["error_chain"] = error_chain
    return ctx
