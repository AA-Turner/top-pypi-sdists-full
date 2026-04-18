"""OpenTelemetry integration for Plato agents and worlds.

Provides tracing utilities using OpenTelemetry SDK. Traces are sent directly
to the Chronos OTLP endpoint.

Usage:
    from plato.otel import init_tracing, get_tracer, shutdown_tracing

    # Initialize tracing (sends to Chronos OTLP endpoint)
    init_tracing(
        service_name="my-world",
        session_id="session-123",
        otlp_endpoint="http://chronos/api/otel",
    )

    # Create spans
    tracer = get_tracer()
    with tracer.start_as_current_span("my-operation") as span:
        span.set_attribute("key", "value")
        # ... do work ...

    # Cleanup
    shutdown_tracing()

ATIF helpers:
    from plato.otel import emit_step, session_span

    tracer = get_tracer()
    with session_span(tracer, "my-agent", "1.0.0", model_name="gpt-4") as span:
        emit_step(tracer, step_id=1, source="agent", message="Hello")
"""

from __future__ import annotations

import contextvars
import json
import logging
import os
import traceback
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Literal

from opentelemetry import context as context_api
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.trace import NonRecordingSpan, Span, SpanContext, TraceFlags, Tracer

logger = logging.getLogger(__name__)

# Silence noisy OpenTelemetry exporter logs
logging.getLogger("opentelemetry.exporter.otlp.proto.http.trace_exporter").setLevel(logging.CRITICAL)
logging.getLogger("opentelemetry.exporter.otlp").setLevel(logging.CRITICAL)

# Global state
_tracer_provider = None
_initialized = False
_log_handler = None


class OTelSpanLogHandler(logging.Handler):
    """Logging handler that creates OTel spans for log messages."""

    def __init__(self, tracer: Tracer, level: int = logging.INFO):
        super().__init__(level)
        self.tracer = tracer

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record as an OTel span."""
        try:
            message = record.getMessage()
            if record.exc_info:
                exc_type = record.exc_info[0].__name__ if record.exc_info[0] else "Exception"
                exc_text = "".join(traceback.format_exception(*record.exc_info)).strip()
            else:
                exc_type = None
                exc_text = None
            with self.tracer.start_as_current_span(f"log.{record.levelname.lower()}") as span:
                span.set_attribute("log.level", record.levelname)
                span.set_attribute("log.message", message)
                span.set_attribute("log.logger", record.name)
                span.set_attribute("source", "world")
                content = exc_text or message
                span.set_attribute("content", content[:4000])

                if record.funcName:
                    span.set_attribute("log.function", record.funcName)
                if record.lineno:
                    span.set_attribute("log.lineno", record.lineno)
                if exc_type is not None:
                    span.set_attribute("log.exception_type", exc_type)
                if exc_text is not None:
                    span.set_attribute("log.exception", exc_text[:8000])

                if record.levelno >= logging.ERROR:
                    span.set_attribute("error", True)
        except Exception:
            pass


def init_tracing(
    service_name: str,
    session_id: str,
    otlp_endpoint: str,
    parent_trace_id: str | None = None,
    parent_span_id: str | None = None,
) -> None:
    """Initialize OpenTelemetry tracing.

    Args:
        service_name: Name of the service (e.g., world name or agent name)
        session_id: Chronos session ID (added as resource attribute)
        otlp_endpoint: Chronos OTLP endpoint (e.g., http://chronos/api/otel)
        parent_trace_id: Optional parent trace ID for linking (hex string)
        parent_span_id: Optional parent span ID for linking (hex string)
    """
    global _tracer_provider, _initialized, _log_handler

    if _initialized:
        logger.debug("Tracing already initialized")
        return

    try:
        resource = Resource.create(
            {
                "service.name": service_name,
                "plato.session.id": session_id,
            }
        )

        _tracer_provider = TracerProvider(resource=resource)

        otlp_exporter = OTLPSpanExporter(endpoint=f"{otlp_endpoint.rstrip('/')}/v1/traces")
        _tracer_provider.add_span_processor(SimpleSpanProcessor(otlp_exporter))

        trace.set_tracer_provider(_tracer_provider)

        if parent_trace_id and parent_span_id:
            parent_context = SpanContext(
                trace_id=int(parent_trace_id, 16),
                span_id=int(parent_span_id, 16),
                is_remote=True,
                trace_flags=TraceFlags(0x01),
            )
            parent_span = NonRecordingSpan(parent_context)
            ctx = trace.set_span_in_context(parent_span)
            context_api.attach(ctx)
            logger.debug(f"Using parent context: trace_id={parent_trace_id}, span_id={parent_span_id}")

        tracer = trace.get_tracer(service_name)
        _log_handler = OTelSpanLogHandler(tracer, level=logging.INFO)

        # Attach to root logger to capture ALL logs (including claude-agent-sdk, etc.)
        root_logger = logging.getLogger()
        root_logger.addHandler(_log_handler)

        # Also ensure plato logger is configured
        plato_logger = logging.getLogger("plato")
        plato_logger.setLevel(logging.INFO)

        _initialized = True
        logger.debug(f"Tracing initialized: service={service_name}, session={session_id}")

    except ImportError as e:
        logger.warning(f"OpenTelemetry SDK not installed: {e}")
    except Exception as e:
        logger.error(f"Failed to initialize tracing: {e}")


def shutdown_tracing(timeout_millis: int = 30000) -> None:
    """Shutdown the tracer provider and flush spans.

    Args:
        timeout_millis: Timeout in milliseconds to wait for flush (default 30s)
    """
    global _tracer_provider, _initialized, _log_handler

    if _log_handler:
        try:
            root_logger = logging.getLogger()
            root_logger.removeHandler(_log_handler)
        except Exception:
            pass
        _log_handler = None

    if _tracer_provider:
        try:
            flush_success = _tracer_provider.force_flush(timeout_millis=timeout_millis)
            if not flush_success:
                logger.warning("Span flush timed out")
            _tracer_provider.shutdown()
            logger.debug("Tracing shutdown complete")
        except Exception as e:
            logger.warning(f"Error shutting down tracer: {e}")

    _tracer_provider = None
    _initialized = False


def get_tracer(name: str = "plato") -> Tracer:
    """Get a tracer instance.

    Args:
        name: Tracer name (default: "plato")

    Returns:
        OpenTelemetry Tracer
    """
    return trace.get_tracer(name)


def is_initialized() -> bool:
    """Check if OTel tracing is initialized."""
    return _initialized


def get_current_trace_context() -> dict[str, str]:
    """Capture the current span's trace context for propagation to child sessions.

    Returns a dict with ``trace_id`` and ``span_id`` (hex strings) if a valid
    span is active, or an empty dict otherwise.  Pass the returned values as
    ``parent_trace_id`` / ``parent_span_id`` when launching a child Chronos
    session so its spans appear under this trace.

    Example::

        from plato.otel import get_current_trace_context

        ctx = get_current_trace_context()
        await chronos.launch(
            package="plato-world-cua-benchmark:3.0.15",
            config={**child_config, **ctx},
            parent_session_id=self._session_id,
        )
    """
    current_span = trace.get_current_span()
    span_context = current_span.get_span_context()
    if not span_context.is_valid:
        return {}
    return {
        "parent_trace_id": format(span_context.trace_id, "032x"),
        "parent_span_id": format(span_context.span_id, "016x"),
    }


def instrument(service_name: str = "plato-agent") -> Tracer:
    """Initialize OTel tracing from environment variables.

    Reads the following env vars:
    - OTEL_EXPORTER_OTLP_ENDPOINT: Chronos OTLP endpoint (required for tracing)
    - SESSION_ID: Chronos session ID (default: "local")
    - OTEL_TRACE_ID: Parent trace ID for linking spans (optional)
    - OTEL_PARENT_SPAN_ID: Parent span ID for linking spans (optional)

    If OTEL_EXPORTER_OTLP_ENDPOINT is not set, returns a no-op tracer.

    Args:
        service_name: Name of the service for traces

    Returns:
        OpenTelemetry Tracer
    """
    otel_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    session_id = os.environ.get("SESSION_ID", "local")
    parent_trace_id = os.environ.get("OTEL_TRACE_ID")
    parent_span_id = os.environ.get("OTEL_PARENT_SPAN_ID")

    if not otel_endpoint:
        logger.debug("No OTEL_EXPORTER_OTLP_ENDPOINT set, using no-op tracer")
        return trace.get_tracer(service_name)

    init_tracing(
        service_name=service_name,
        session_id=session_id,
        otlp_endpoint=otel_endpoint,
        parent_trace_id=parent_trace_id,
        parent_span_id=parent_span_id,
    )

    return trace.get_tracer(service_name)


# =============================================================================
# ATIF Step/Session Helpers
# =============================================================================


def _set_step_attributes(
    span: Span,
    *,
    step_id: int,
    source: Literal["system", "user", "agent"],
    message: str,
    model_name: str | None = None,
    reasoning: str | None = None,
    tool_calls: list[dict] | None = None,
    observation: dict | None = None,
    prompt_tokens: int | None = None,
    completion_tokens: int | None = None,
    cache_read_tokens: int | None = None,
    cache_write_tokens: int | None = None,
    reasoning_tokens: int | None = None,
    cost_usd: float | None = None,
    duration_ms: float | None = None,
    screenshot: str | None = None,
    screenshot_format: str | None = None,
) -> None:
    """Populate an ATIF step span with the standard attributes."""
    span.set_attribute("atif.step.id", step_id)
    span.set_attribute("atif.step.source", source)
    span.set_attribute("atif.step.message", message)

    if model_name is not None:
        span.set_attribute("atif.step.model_name", model_name)
    if reasoning is not None:
        span.set_attribute("atif.step.reasoning", reasoning)
    if tool_calls is not None:
        span.set_attribute("atif.step.tool_calls", json.dumps(tool_calls, default=str))
    if observation is not None:
        span.set_attribute("atif.step.observation", json.dumps(observation, default=str))
    if prompt_tokens is not None:
        span.set_attribute("atif.step.prompt_tokens", prompt_tokens)
    if completion_tokens is not None:
        span.set_attribute("atif.step.completion_tokens", completion_tokens)
    if cache_read_tokens is not None:
        span.set_attribute("atif.step.cache_read_tokens", cache_read_tokens)
    if cache_write_tokens is not None:
        span.set_attribute("atif.step.cache_write_tokens", cache_write_tokens)
    if reasoning_tokens is not None:
        span.set_attribute("atif.step.reasoning_tokens", reasoning_tokens)
    if cost_usd is not None:
        span.set_attribute("atif.step.cost_usd", cost_usd)
    if duration_ms is not None:
        span.set_attribute("atif.step.duration_ms", duration_ms)
    if screenshot is not None:
        span.set_attribute("atif.step.screenshot", screenshot)
        span.set_attribute("atif.step.screenshot_format", screenshot_format or "image/png")


@contextmanager
def start_step_span(
    tracer: Tracer,
    step_id: int,
    source: Literal["system", "user", "agent"],
    message: str,
    *,
    model_name: str | None = None,
    reasoning: str | None = None,
    tool_calls: list[dict] | None = None,
    observation: dict | None = None,
    prompt_tokens: int | None = None,
    completion_tokens: int | None = None,
    cache_read_tokens: int | None = None,
    cache_write_tokens: int | None = None,
    reasoning_tokens: int | None = None,
    cost_usd: float | None = None,
    duration_ms: float | None = None,
    screenshot: str | None = None,
    screenshot_format: str | None = None,
) -> Iterator[Span]:
    """Create one live ATIF step span and yield it to the caller.

    Args:
        tracer: OTel tracer instance
        step_id: Sequential step ID (from 1)
        source: "system", "user", or "agent"
        message: Text content of the step
        model_name: LLM model identifier
        reasoning: Chain-of-thought / extended thinking content
        tool_calls: List of tool call dicts with tool_call_id, function_name, arguments
        observation: Observation dict with results list
        prompt_tokens: Input token count
        completion_tokens: Output token count
        cost_usd: Cost in USD
        screenshot: Base64-encoded screenshot image data
        screenshot_format: Image MIME type (e.g., "image/png")
    """
    with tracer.start_as_current_span(f"atif.step.{step_id}") as span:
        _set_step_attributes(
            span,
            step_id=step_id,
            source=source,
            message=message,
            model_name=model_name,
            reasoning=reasoning,
            tool_calls=tool_calls,
            observation=observation,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
            reasoning_tokens=reasoning_tokens,
            cost_usd=cost_usd,
            duration_ms=duration_ms,
            screenshot=screenshot,
            screenshot_format=screenshot_format,
        )
        yield span


def emit_step(
    tracer: Tracer,
    step_id: int,
    source: Literal["system", "user", "agent"],
    message: str,
    *,
    model_name: str | None = None,
    reasoning: str | None = None,
    tool_calls: list[dict] | None = None,
    observation: dict | None = None,
    prompt_tokens: int | None = None,
    completion_tokens: int | None = None,
    cache_read_tokens: int | None = None,
    cache_write_tokens: int | None = None,
    reasoning_tokens: int | None = None,
    cost_usd: float | None = None,
    duration_ms: float | None = None,
    screenshot: str | None = None,
    screenshot_format: str | None = None,
) -> None:
    """Emit one ATIF step as an OTel span."""
    with start_step_span(
        tracer,
        step_id,
        source,
        message,
        model_name=model_name,
        reasoning=reasoning,
        tool_calls=tool_calls,
        observation=observation,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        cache_read_tokens=cache_read_tokens,
        cache_write_tokens=cache_write_tokens,
        reasoning_tokens=reasoning_tokens,
        cost_usd=cost_usd,
        duration_ms=duration_ms,
        screenshot=screenshot,
        screenshot_format=screenshot_format,
    ):
        pass


@dataclass
class _ModelCost:
    """Per-model cost/token totals."""

    cost_usd: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    reasoning_tokens: int = 0


@dataclass
class _CostAccumulator:
    """Aggregates per-step LLM costs/tokens, broken down by model."""

    by_model: dict[str, _ModelCost] = field(default_factory=dict)


_current_cost_accumulator: contextvars.ContextVar[_CostAccumulator | None] = contextvars.ContextVar(
    "plato_cost_accumulator", default=None
)


def record_step_cost(
    cost_usd: float,
    prompt_tokens: int,
    completion_tokens: int,
    reasoning_tokens: int = 0,
    model: str | None = None,
) -> None:
    """Record an LLM step's cost/tokens into the current accumulator, keyed by model.

    No-op when called outside an `aggregate_step_costs()` / `session_span()` /
    world span. Safe to call from any thread that inherits the context where
    the accumulator was entered.
    """
    acc = _current_cost_accumulator.get()
    if acc is None:
        return
    key = model or "unknown"
    bucket = acc.by_model.setdefault(key, _ModelCost())
    bucket.cost_usd += float(cost_usd or 0.0)
    bucket.prompt_tokens += int(prompt_tokens or 0)
    bucket.completion_tokens += int(completion_tokens or 0)
    bucket.reasoning_tokens += int(reasoning_tokens or 0)


@contextmanager
def aggregate_step_costs(
    span: Span,
    tracer: Tracer,
    name: str | None = None,
    version: str | None = None,
) -> Iterator[None]:
    """Aggregate per-step LLM costs into per-model child spans under `span`.

    Installs a contextvar accumulator that `record_step_cost` writes into,
    keyed by model. On context exit, emits one child span per model with
    `atif.agent.{name,model_name,cost_usd,prompt_tokens,completion_tokens,
    reasoning_tokens,version}` so Chronos's `compute_session_costs` (which
    groups by spans carrying `atif.agent.cost_usd`) renders one row per
    model in the trajectory viewer.

    `name`/`version` are propagated as the agent name/version on each
    child span, with the model appended to disambiguate (e.g. `world:gpt-4`).
    """
    accumulator = _CostAccumulator()
    token = _current_cost_accumulator.set(accumulator)
    try:
        yield
    finally:
        _current_cost_accumulator.reset(token)
        for model, bucket in accumulator.by_model.items():
            if bucket.cost_usd <= 0 and bucket.prompt_tokens == 0 and bucket.completion_tokens == 0:
                continue
            child_name = f"atif.cost.{model}"
            with tracer.start_as_current_span(child_name, context=trace.set_span_in_context(span)) as cost_span:
                agent_label = f"{name}:{model}" if name else model
                cost_span.set_attribute("atif.kind", "agent")
                cost_span.set_attribute("atif.agent.name", agent_label)
                cost_span.set_attribute("atif.agent.model_name", model)
                if version is not None:
                    cost_span.set_attribute("atif.agent.version", version)
                if bucket.cost_usd > 0:
                    cost_span.set_attribute("atif.agent.cost_usd", bucket.cost_usd)
                if bucket.prompt_tokens > 0:
                    cost_span.set_attribute("atif.agent.prompt_tokens", bucket.prompt_tokens)
                if bucket.completion_tokens > 0:
                    cost_span.set_attribute("atif.agent.completion_tokens", bucket.completion_tokens)
                if bucket.reasoning_tokens > 0:
                    cost_span.set_attribute("atif.agent.reasoning_tokens", bucket.reasoning_tokens)


@contextmanager
def session_span(
    tracer: Tracer,
    agent_name: str,
    agent_version: str,
    model_name: str | None = None,
    system_prompt: str | None = None,
    mcp_config: str | None = None,
) -> Iterator[Span]:
    """Create root session span with atif.agent.* attributes.

    Optionally emits a system step (step_id=1) with the system prompt and/or
    MCP config so that observability traces always capture what the agent was
    instructed to do.

    Args:
        tracer: OTel tracer instance
        agent_name: Agent name (e.g., "claude-code")
        agent_version: Agent version string
        model_name: Default model used by the agent
        system_prompt: Full system prompt sent to the agent (traced as step 1)
        mcp_config: MCP config content string (traced alongside system prompt)
    """
    display_name = os.environ.get("PLATO_AGENT_DISPLAY_NAME") or agent_name
    with tracer.start_as_current_span("session") as span:
        span.set_attribute("plato.phase", "agent")
        span.set_attribute("atif.version", "0.1.0")
        span.set_attribute("atif.agent.name", display_name)
        span.set_attribute("atif.agent.version", agent_version)
        span.set_attribute("plato.agent.impl_name", agent_name)
        if display_name != agent_name:
            span.set_attribute("plato.agent.display_name", display_name)
        if model_name is not None:
            span.set_attribute("atif.agent.model_name", model_name)

        # Emit system context step if any system info was provided
        system_parts = [
            f"System prompt:\n{system_prompt}" if system_prompt else "",
            f"MCP config:\n{mcp_config}" if mcp_config else "",
        ]
        system_message = "\n\n".join(p for p in system_parts if p)
        if system_message:
            emit_step(tracer, step_id=1, source="system", message=system_message)

        with aggregate_step_costs(span, tracer, name=display_name, version=agent_version):
            yield span
