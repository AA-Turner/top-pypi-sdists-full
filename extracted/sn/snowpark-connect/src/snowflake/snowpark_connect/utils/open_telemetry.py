#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
OpenTelemetry context management for Snowpark Connect.
Handles OpenTelemetry initialization, root span creation, and context propagation.
"""

import os
import time

from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

try:
    from opentelemetry import context, trace
    from opentelemetry.trace import Status, StatusCode

    OTEL_AVAILABLE = True

    try:
        from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
            OTLPMetricExporter,
        )
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.metrics import set_meter_provider
        from opentelemetry.sdk.metrics import MeterProvider
        from opentelemetry.sdk.metrics._internal.export import (
            PeriodicExportingMetricReader,
        )
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from snowflake.telemetry.trace import SnowflakeTraceIdGenerator

        OTEL_EXPORTERS_AVAILABLE = True
        logger.debug("OpenTelemetry exporters available")
    except ImportError as e:
        logger.warning(f"OpenTelemetry exporters not available: {e}")
        OTEL_EXPORTERS_AVAILABLE = False

except ImportError as e:
    logger.warning(f"OpenTelemetry basic modules not available: {e}")
    OTEL_AVAILABLE = False
    OTEL_EXPORTERS_AVAILABLE = False
    trace = None
    context = None

# Environment variable configuration
TELEMETRY_ENV_VAR = "SNOWPARK_TELEMETRY_ENABLED"
DEFAULT_TELEMETRY_ENABLED = True

# Span name constants
SNOWPARK_CONNECT_CREATED_ROOT_SPAN = "snowpark_connect_span"

# Global State Variables
_root_span_otel_context = None  # OpenTelemetry context containing root span
_root_span = None  # Main root span for all operations
_root_span_context_token = None  # Token for context activation/deactivation
_tracer_provider = None  # TracerProvider instance for telemetry cleanup
_meter_provider = None  # MeterProvider instance for metrics
_root_span_ended = False  # Flag to ensure span ends only once
_is_inherited_context = False  # Track if using existing Snowflake context


def otel_create_context_wrapper(func):
    """
    Create a wrapper function that transfers OpenTelemetry context to any thread function.

    Args:
        func: Any function to wrap

    Returns:
        function: Either the wrapped function with context transfer or the original function
    """
    if is_telemetry_enabled():
        try:
            current_context = context.get_current()

            def func_with_telemetry_context(*args, **kwargs):
                """Run function with OpenTelemetry context attached"""
                context_token = None
                try:
                    context_token = context.attach(current_context)
                    return func(*args, **kwargs)
                finally:
                    if context_token:
                        context.detach(context_token)

            return func_with_telemetry_context

        except ImportError:
            logger.warning("Failed to import OpenTelemetry context for thread transfer")
            return func
    else:
        return func


# Helper Functions


def _setup_tracer_provider():
    """Set up basic TracerProvider if not already initialized"""
    current_provider = trace.get_tracer_provider()
    provider_type = current_provider.__class__.__name__

    if provider_type not in ["NoOpTracerProvider", "ProxyTracerProvider"]:
        return current_provider

    # Initialize TracerProvider
    resource = Resource.create({"service.name": "snowpark-telemetry"})
    tracer_provider = TracerProvider(
        resource=resource, id_generator=SnowflakeTraceIdGenerator()
    )
    trace.set_tracer_provider(tracer_provider)

    global _tracer_provider
    _tracer_provider = tracer_provider

    return tracer_provider


def _check_existing_telemetry_context():
    """Check if we're running within existing Snowflake telemetry context"""
    if not OTEL_AVAILABLE:
        return False, None

    try:
        current_span = trace.get_current_span()

        if current_span and current_span.is_recording():
            # Check if this is a Snowflake span (not our own root span)
            span_name = getattr(current_span, "name", "unknown")

            # Don't inherit if it's our own sas_spcs span
            if span_name == SNOWPARK_CONNECT_CREATED_ROOT_SPAN:
                return False, None

            existing_context = context.get_current()
            return True, existing_context
        else:
            return False, None
    except Exception as e:
        logger.warning(f"Failed to check existing context: {e}")
        return False, None


def _create_root_span() -> bool:
    """
    Create the main application span for Snowpark Connect operations.

    Returns:
        bool: True if root span was successfully created, False otherwise
    """
    if not is_telemetry_enabled():
        return False

    try:
        tracer = trace.get_tracer("snowpark-connect-telemetry")
        # This span gets triggered for snowpark-submit applications
        span = tracer.start_span(SNOWPARK_CONNECT_CREATED_ROOT_SPAN)

        if span.is_recording():
            span.set_attribute("application.type", "snowpark-connect")
            span.set_attribute("service.name", "snowpark-connect-telemetry")
            span.set_attribute("operation.name", "snowpark_connect_application")

        span_context = trace.set_span_in_context(span)
        activation_token = context.attach(span_context)

        global _root_span, _root_span_context_token
        _root_span = span
        _root_span_context_token = activation_token
        return True

    except Exception as e:
        logger.warning(f"Failed to create root span: {e}")
        return False


def _get_current_otel_context():
    """Capture current OpenTelemetry context for thread transfer"""
    if not OTEL_AVAILABLE:
        return None

    try:
        current_span = trace.get_current_span()
        if current_span:
            current_otel_context = context.get_current()
            return current_otel_context
        else:
            return None
    except Exception as e:
        logger.warning(f"Failed to capture telemetry context: {e}")
        return None


def _setup_exporters_for_spcs():
    """Set up OTLP exporters for SPCS mode"""
    if not OTEL_EXPORTERS_AVAILABLE or not _tracer_provider:
        return False

    try:
        otlp_exporter = OTLPSpanExporter(insecure=True)
        batch_processor = BatchSpanProcessor(otlp_exporter, schedule_delay_millis=1000)
        _tracer_provider.add_span_processor(batch_processor)

        resource = Resource.create({"service.name": "snowpark-telemetry"})
        meter_provider = MeterProvider(
            resource=resource,
            metric_readers=[
                PeriodicExportingMetricReader(
                    OTLPMetricExporter(insecure=True), export_interval_millis=30000
                )
            ],
        )
        set_meter_provider(meter_provider)

        global _meter_provider
        _meter_provider = meter_provider

        return True

    except Exception as e:
        logger.warning(f"Failed to setup exporters: {e}")
        return False


# Main Initialization Functions


def otel_initialize():
    """
    Initialize OpenTelemetry for Snowpark Connect.

    This function:
    1. Checks for existing Snowflake telemetry context (e.g., stored procs/notebooks)
    2. Sets up OTLP exporters if running in SPCS
    3. Creates root span for tracking operations

    Returns:
        bool: True if telemetry was successfully initialized, False otherwise
    """
    if not is_telemetry_enabled():
        return False

    try:
        # First check for existing context BEFORE setting up our own TracerProvider
        # This is important for stored procedures and notebooks that already have Snowflake context
        has_existing_context, existing_context = _check_existing_telemetry_context()

        global _is_inherited_context, _root_span_otel_context

        if has_existing_context:
            # Inherit existing Snowflake context - don't create new span or TracerProvider
            logger.debug("Using existing Snowflake telemetry context")
            _is_inherited_context = True
            _root_span_otel_context = existing_context
            return True

        # No existing context found, set up our own TracerProvider
        _setup_tracer_provider()

        # Set up OTLP exporters if running in SPCS
        from snowflake.snowpark_connect.utils.session import _is_running_in_SPCS

        if _is_running_in_SPCS():
            logger.debug("Running in SPCS, setting up OTLP exporters")
            _setup_exporters_for_spcs()

        # Create root span for tracking operations
        if _create_root_span():
            _root_span_otel_context = _get_current_otel_context()
            return True
        else:
            return False

    except Exception as e:
        logger.warning(f"Telemetry initialization failed: {e}")
        return False


# API Functions


def otel_get_root_span_context():
    """Get the stored root span context for thread transfer"""
    return _root_span_otel_context


def otel_attach_context(otel_context):
    """Attach OpenTelemetry context and return token"""
    if not OTEL_AVAILABLE or not otel_context:
        return None

    try:
        token = context.attach(otel_context)
        return token
    except Exception as e:
        logger.warning(f"Failed to attach context: {e}")
        return None


def otel_detach_context(context_token):
    """Detach OpenTelemetry context using token"""
    if not OTEL_AVAILABLE or not context_token:
        return

    try:
        context.detach(context_token)
    except Exception as e:
        logger.warning(f"Failed to detach context: {e}")


def otel_end_root_span(flush_timeout_millis: int = 5000):
    """
    End the application span with final duration and status

    Args:
        flush_timeout_millis: Maximum time to wait for telemetry flush in milliseconds (default: 5000)
    """
    if not is_telemetry_enabled():
        return False

    global _root_span_ended, _root_span_context_token

    if _root_span_ended or _is_inherited_context:
        # Don't end inherited spans - they're managed by Snowflake
        return False

    if _root_span:
        try:
            if _root_span.is_recording():
                final_duration_ms = int(
                    (time.time() * 1000) - (_root_span.start_time / 1_000_000)
                )
                _root_span.set_attribute("execution.duration_ms", final_duration_ms)
                _root_span.set_status(Status(StatusCode.OK))

            _root_span.end()
            _root_span_ended = True

            # Detach the root context token that was attached during span creation
            if _root_span_context_token is not None:
                try:
                    context.detach(_root_span_context_token)
                    _root_span_context_token = None
                except Exception as detach_error:
                    logger.warning(
                        f"Failed to detach root span context token: {detach_error}"
                    )

            otel_flush_telemetry(timeout_millis=flush_timeout_millis)

            return True
        except Exception as e:
            logger.warning(f"Failed to end root span: {e}")
    return False


# Utility Functions


def is_telemetry_enabled():
    """
    Check if OpenTelemetry telemetry is both available (installed) and enabled.

    This combines multiple checks:
    1. OTEL_AVAILABLE: Whether OpenTelemetry packages are installed
    2. Environment variable: Whether telemetry is enabled via SNOWPARK_TELEMETRY_ENABLED
    3. Runtime environment: Must be running in SPCS or stored procedure/notebook

    Returns:
        bool: True if telemetry can and should be used, False otherwise
    """
    if not OTEL_AVAILABLE:
        return False

    # Check environment variable setting
    env_value = os.getenv(TELEMETRY_ENV_VAR, str(DEFAULT_TELEMETRY_ENABLED)).lower()
    if env_value not in ("true", "1", "yes", "on"):
        return False

    # Only enable telemetry in SPCS or stored procedure/notebook environments
    from snowflake.snowpark_connect.utils.session import (
        _is_running_in_SPCS,
        _is_running_in_stored_procedure_or_notebook,
    )

    return _is_running_in_SPCS() or _is_running_in_stored_procedure_or_notebook()


def otel_get_current_span():
    """
    Get the current OpenTelemetry span if telemetry is enabled.

    Returns:
        Span object if telemetry is enabled and a span is active, None otherwise
    """
    if not is_telemetry_enabled():
        return None
    if trace is None:
        return None
    try:
        return trace.get_current_span()
    except Exception as e:
        logger.warning(f"Failed to get current span: {e}")
        return None


def otel_get_tracer(name: str):
    """
    Get an OpenTelemetry tracer if telemetry is enabled.

    Args:
        name: The tracer name

    Returns:
        Tracer object if telemetry is enabled, None otherwise
    """
    if not is_telemetry_enabled():
        return None
    if trace is None:
        return None
    try:
        return trace.get_tracer(name)
    except Exception as e:
        logger.warning(f"Failed to get tracer: {e}")
        return None


def otel_start_span_as_current(tracer, span_name: str):
    """
    Start a span as current context if telemetry is enabled.

    Args:
        tracer: The tracer object (can be None)
        span_name: Name of the span

    Returns:
        Context manager for the span, or None
    """
    if not is_telemetry_enabled() or tracer is None:
        return None
    try:
        return tracer.start_as_current_span(span_name)
    except Exception as e:
        logger.warning(f"Failed to start span: {e}")
        return None


def otel_create_status(status_code, description: str = ""):
    """
    Create an OpenTelemetry Status object if telemetry is enabled.

    Args:
        status_code: StatusCode enum value
        description: Optional description string

    Returns:
        Status object if telemetry is enabled, None otherwise
    """
    if not is_telemetry_enabled():
        return None
    if trace is None:
        return None
    try:
        from opentelemetry.trace import Status

        return Status(status_code, description)
    except Exception as e:
        logger.warning(f"Failed to create status: {e}")
        return None


def otel_get_status_code():
    """
    Get the StatusCode enum if telemetry is enabled.

    Returns:
        StatusCode enum if available, None otherwise
    """
    if not is_telemetry_enabled():
        return None
    try:
        from opentelemetry.trace import StatusCode

        return StatusCode
    except Exception as e:
        logger.warning(f"Failed to get StatusCode: {e}")
        return None


def otel_flush_telemetry(timeout_millis: int = 5000):
    """
    Force flush telemetry traces and metrics to ensure export

    Args:
        timeout_millis: Maximum time to wait for flush in milliseconds (default: 5000)
    """
    if not is_telemetry_enabled():
        return

    if _tracer_provider:
        try:
            _tracer_provider.force_flush(timeout_millis=timeout_millis)
        except Exception as e:
            logger.warning(f"Failed to force flush traces: {e}")

    if _meter_provider:
        try:
            _meter_provider.force_flush(timeout_millis=timeout_millis)
        except Exception as e:
            logger.warning(f"Failed to force flush metrics: {e}")
