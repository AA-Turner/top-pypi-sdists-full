# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

import atexit
import contextlib
import enum
import importlib.util
import inspect
import logging
import re
import socket
import sys
import threading
import typing
import warnings
from collections import namedtuple
from contextvars import ContextVar
from dataclasses import dataclass

from tango._tango import ApiUtil, LockerLanguage, _telemetry, is_omni_thread
from tango.constants import TELEMETRY_SUPPORTED
from tango.release import Release

from ._warnings import PyTangoUserWarning, warn_once


def _truthy_env_var(name) -> bool:
    value = ApiUtil.get_env_var(name)
    return bool(value and value.lower() in {"on", "1", "true", "yes", "y"})


def _module_available(module_name: str) -> bool:
    try:
        return importlib.util.find_spec(module_name) is not None
    except (ImportError, ValueError):
        return False


class TelemetryExporter(enum.IntEnum):
    """
    An enumeration representing the telemetry exporter types.

    .. versionadded:: 10.3.0
    """

    GRPC = 0
    HTTP = 1
    CONSOLE = 2


class TelemetryType(enum.IntEnum):
    """
    An enumeration representing the telemetry signal types.

    .. versionadded:: 10.3.0
    """

    TRACING = 0
    LOGGING = 1
    NONE = 2


class TelemetryTopic(enum.IntEnum):
    """
    An enumeration representing the telemetry topics.

    .. note::
      As of version 10.3.0, the only usable topic is ALL.
      The DATABASE, EVENTS and POLLING topics are not implemented.
      The USER topic leads to inconsistent results due to an
      `issue in cppTango <https://gitlab.com/tango-controls/cppTango/-/work_items/1645>`__
      A fix is expected in version 10.4.0,
      which will also bring in a new set of topics.

    .. versionadded:: 10.3.0
    """

    DATABASE = 0
    EVENTS = 1
    POLLING = 2
    USER = 3
    ALL = 4


@dataclass(frozen=True)
class TelemetryEndpoint:
    exporter: TelemetryExporter
    endpoint: str


class TracerProviderFactory(typing.Protocol):
    def __call__(
        self,
        service_name: str,
        service_instance_id: None | str = None,
        extra_resource_attributes: None | dict[str, str] = None,
        endpoints: None | tuple[TelemetryEndpoint, ...] = None,
    ): ...


@dataclass(frozen=True)
class _TelemetryEnvConfig:
    enabled: bool
    tracing_endpoints: tuple[TelemetryEndpoint, ...]
    logging_endpoints: tuple[TelemetryEndpoint, ...]
    types: tuple[TelemetryType, ...]
    topics: tuple[TelemetryTopic, ...]
    tracing_enabled: bool
    logging_enabled: bool


@dataclass(frozen=True)
class _TelemetryHandlers:
    get_current_otel_context: typing.Any = None
    span_from_cpptango: typing.Any = None
    context_from_cpptango: typing.Any = None
    span_to_cpptango: typing.Any = None
    tracer_provider_factory: typing.Any = None
    create_device_tracer: typing.Any = None


_DummySpanContext = namedtuple(
    "_DummySpanContext",
    ["trace_id", "span_id", "is_remote", "trace_flags", "trace_state", "is_valid"],
)


class _DummySpan:
    def set_attributes(self, *args, **kwargs):
        pass

    def set_attribute(self, *args, **kwargs):
        pass

    def add_event(self, *args, **kwargs):
        pass

    def add_link(self, *args, **kwargs):
        pass

    def update_name(self, *args, **kwargs):
        pass

    def is_recording(self):
        return False

    def set_status(self, *args, **kwargs):
        pass

    def record_exception(self, *args, **kwargs):
        pass

    def end(self, *args, **kwargs):
        pass

    def get_span_context(self):
        return _DummySpanContext(0, 0, False, 0, {}, False)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.end()


class _DummyTracer:
    def start_span(self, *args, **kwargs):
        pass

    @contextlib.contextmanager
    def start_as_current_span(self, *args, **kwargs):
        yield _DummySpan()


class _DummyTracerProvider:
    def get_tracer(self, *args, **kwargs):
        return _DummyTracer()


def _dummy_get_current_otel_context():
    return {}


@contextlib.contextmanager
def _dummy_span_from_cpptango(device, fn):
    yield _DummySpan()


@contextlib.contextmanager
def _dummy_context_from_cpptango():
    yield


@contextlib.contextmanager
def _dummy_span_to_cpptango(name: str, context=None, topic: str = ""):
    yield


def _dummy_telemetry_tracer_provider_factory(
    service_name,
    service_instance_id=None,
    extra_resource_attributes=None,
    endpoints=None,
):
    return _DummyTracerProvider()


def _dummy_create_device_telemetry_tracer(tracer_provider) -> _DummyTracer:
    return _DummyTracer()


_dummy_telemetry_handlers = _TelemetryHandlers(
    get_current_otel_context=_dummy_get_current_otel_context,
    span_from_cpptango=_dummy_span_from_cpptango,
    context_from_cpptango=_dummy_context_from_cpptango,
    span_to_cpptango=_dummy_span_to_cpptango,
    tracer_provider_factory=_dummy_telemetry_tracer_provider_factory,
    create_device_tracer=_dummy_create_device_telemetry_tracer,
)


def _telemetry_exporter_to_wire(exporter) -> str:
    if isinstance(exporter, str):
        return exporter.lower()
    return exporter.name.lower()


def _telemetry_endpoint_to_wire(
    endpoint: TelemetryEndpoint,
):
    return [_telemetry_exporter_to_wire(endpoint.exporter), endpoint.endpoint]


def _telemetry_endpoints_to_wire(endpoints):
    wire = []
    for endpoint in endpoints:
        wire.extend(_telemetry_endpoint_to_wire(endpoint))
    return wire


def _telemetry_endpoint_from_wire(exporter: str, endpoint: str) -> TelemetryEndpoint:
    return TelemetryEndpoint(TelemetryExporter[exporter.upper()], endpoint)


def _telemetry_endpoints_from_wire(endpoint_pairs) -> tuple[TelemetryEndpoint, ...]:
    if len(endpoint_pairs) % 2 != 0:
        raise ValueError("telemetry endpoint data must contain exporter/endpoint pairs")
    return tuple(
        _telemetry_endpoint_from_wire(endpoint_pairs[index], endpoint_pairs[index + 1])
        for index in range(0, len(endpoint_pairs), 2)
    )


_trace_api = None
_telemetry_runtime_available = False
_telemetry_sdk_available = False
_telemetry_http_exporter_available = False
_telemetry_grpc_exporter_available = False
_real_telemetry_handlers = _TelemetryHandlers()


def _call_tracer_provider_factory(
    factory,
    service_name,
    service_instance_id=None,
    extra_resource_attributes=None,
    endpoints=None,
):
    signature = inspect.signature(factory)
    parameters = signature.parameters.values()
    accepts_endpoints = "endpoints" in signature.parameters or any(
        parameter.kind == inspect.Parameter.VAR_KEYWORD for parameter in parameters
    )
    if accepts_endpoints:
        return factory(
            service_name,
            service_instance_id,
            extra_resource_attributes,
            endpoints=endpoints,
        )
    # fallback to v10.0.0 signature, before endpoints were added
    return factory(service_name, service_instance_id, extra_resource_attributes)


def _warn_if_deprecated_telemetry_env_vars_used() -> None:
    deprecated_env_vars = (
        ("TANGO_TELEMETRY_TRACES_EXPORTER", "TANGO_TELEMETRY_TRACING_EXPORTERS"),
        ("TANGO_TELEMETRY_TRACES_ENDPOINT", "TANGO_TELEMETRY_TRACING_ENDPOINTS"),
        ("TANGO_TELEMETRY_LOGS_EXPORTER", "TANGO_TELEMETRY_LOGGING_EXPORTERS"),
        ("TANGO_TELEMETRY_LOGS_ENDPOINT", "TANGO_TELEMETRY_LOGGING_ENDPOINTS"),
    )
    for name, replacement_name in deprecated_env_vars:
        _warn_if_deprecated_env_var_used(name, replacement_name)


def _warn_if_deprecated_env_var_used(name: str, replacement_name: str) -> None:
    if ApiUtil.get_env_var(name) is None:
        return
    warn_once(
        f"{name} is deprecated; use {replacement_name} instead.",
        key=f"deprecated-env:{name}",
        category=DeprecationWarning,
        stacklevel=2,
    )


def _parse_telemetry_endpoints_from_env(
    enabled: bool,
    *,
    exporters_env_var: str,
    endpoints_env_var: str,
) -> tuple[TelemetryEndpoint, ...]:
    exporters_value = ApiUtil.get_env_var(exporters_env_var)
    endpoints_value = ApiUtil.get_env_var(endpoints_env_var)

    if exporters_value:
        exporter_names = [item.strip().lower() for item in exporters_value.split(",") if item.strip()]
    else:
        exporter_names = ["console" if enabled else "none"]

    endpoints = [item.strip() for item in endpoints_value.split(",")] if endpoints_value else []

    parsed_endpoints = []
    if len(endpoints) > len(exporter_names):
        warnings.warn(
            f"Ignoring extra endpoint values from {endpoints_env_var}: "
            f"expected at most {len(exporter_names)}, got {len(endpoints)}.",
            stacklevel=1,
        )
        endpoints = endpoints[: len(exporter_names)]

    while len(endpoints) < len(exporter_names):
        endpoints.append("")

    for exporter_name, endpoint in zip(exporter_names, endpoints, strict=True):
        if exporter_name not in {"console", "grpc", "http", "none"}:
            warnings.warn(
                f"Unknown value '{exporter_name}' for {exporters_env_var}. Options are: "
                f"'console', 'grpc', 'http' and 'none'. Defaulting to 'console'.",
                stacklevel=1,
            )
            exporter_name = "console"
        if exporter_name == "none":
            continue
        parsed_endpoints.append(TelemetryEndpoint(TelemetryExporter[exporter_name.upper()], endpoint))

    return tuple(parsed_endpoints)


def _parse_telemetry_enum_values_from_env(
    env_var_name: str,
    enum_type,
) -> tuple:
    values = ApiUtil.get_env_var(env_var_name)
    if not values:
        return ()

    parsed_values = []
    for item in values.split(","):
        name = item.strip().upper()
        if not name:
            continue
        try:
            parsed_values.append(enum_type[name])
        except KeyError:
            warnings.warn(f"Unknown value '{item.strip()}' for {env_var_name}. Ignoring it.", stacklevel=1)
    return tuple(parsed_values)


def _get_env_telemetry_config() -> _TelemetryEnvConfig:
    _warn_if_deprecated_telemetry_env_vars_used()
    enabled = _truthy_env_var("TANGO_TELEMETRY_ENABLE")
    telemetry_types = _parse_telemetry_enum_values_from_env(
        "TANGO_TELEMETRY_TYPES",
        TelemetryType,
    )
    tracing_enabled = not telemetry_types
    logging_enabled = not telemetry_types
    if telemetry_types and TelemetryType.NONE not in telemetry_types:
        tracing_enabled = TelemetryType.TRACING in telemetry_types
        logging_enabled = TelemetryType.LOGGING in telemetry_types

    return _TelemetryEnvConfig(
        enabled=enabled,
        tracing_endpoints=_parse_telemetry_endpoints_from_env(
            enabled,
            exporters_env_var="TANGO_TELEMETRY_TRACING_EXPORTERS",
            endpoints_env_var="TANGO_TELEMETRY_TRACING_ENDPOINTS",
        ),
        logging_endpoints=_parse_telemetry_endpoints_from_env(
            enabled,
            exporters_env_var="TANGO_TELEMETRY_LOGGING_EXPORTERS",
            endpoints_env_var="TANGO_TELEMETRY_LOGGING_ENDPOINTS",
        ),
        types=telemetry_types,
        topics=_parse_telemetry_enum_values_from_env(
            "TANGO_TELEMETRY_TOPICS",
            TelemetryTopic,
        ),
        tracing_enabled=tracing_enabled,
        logging_enabled=logging_enabled,
    )


_env_telemetry_config = _get_env_telemetry_config()


try:
    _telemetry_disabled_via_env_var = _truthy_env_var("PYTANGO_DISABLE_TELEMETRY_PATCHING")
    if not _telemetry_disabled_via_env_var and TELEMETRY_SUPPORTED:
        from opentelemetry import context as context_api
        from opentelemetry import trace as trace_api
        from opentelemetry.trace.propagation.tracecontext import (
            TraceContextTextMapPropagator,
        )

        _trace_api = trace_api
        _telemetry_runtime_available = True

        try:
            from opentelemetry.sdk.resources import (
                HOST_NAME,
                SERVICE_INSTANCE_ID,
                SERVICE_NAME,
                SERVICE_NAMESPACE,
                Resource,
            )
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import (
                BatchSpanProcessor,
                ConsoleSpanExporter,
                SimpleSpanProcessor,
            )

            _telemetry_http_exporter_available = _module_available(
                "opentelemetry.exporter.otlp.proto.http.trace_exporter"
            )
            _telemetry_grpc_exporter_available = _module_available(
                "opentelemetry.exporter.otlp.proto.grpc.trace_exporter"
            )

            _telemetry_sdk_available = True
        except ImportError:
            _telemetry_sdk_available = False

        def _real_get_current_otel_context() -> context_api.Context:
            return context_api.get_current()

        _current_telemetry_tracer = ContextVar("current_telemetry_tracer")

        @contextlib.contextmanager
        def _real_span_from_cpptango(device, fn) -> typing.Iterator[trace_api.Span]:
            fn = inspect.unwrap(fn)
            if not hasattr(fn, "__code__") and hasattr(fn, "__call__"):  # noqa: B004
                fn = fn.__call__
            name = getattr(fn, "__qualname__", getattr(fn, "__name__", "unknown"))
            code = getattr(fn, "__code__", None)
            filepath = getattr(code, "co_filename", "unknown")
            lineno = getattr(code, "co_firstlineno", 0)

            carrier = _telemetry.get_trace_context()
            ctx = TraceContextTextMapPropagator().extract(carrier=carrier)
            device_tracer = device.get_telemetry_tracer()
            token = _current_telemetry_tracer.set(device_tracer)
            try:
                with device_tracer.start_as_current_span(name, context=ctx, kind=trace_api.SpanKind.SERVER) as span:
                    span.set_attribute("code.filepath", filepath)
                    span.set_attribute("code.lineno", lineno)
                    current_thread = threading.current_thread()
                    span.set_attribute("thread.id", hex(current_thread.ident))
                    span.set_attribute("thread.name", current_thread.name)
                    _add_client_ident_info(device, span)
                    yield span
            finally:
                _current_telemetry_tracer.reset(token)

        @contextlib.contextmanager
        def _real_context_from_cpptango():
            carrier = _telemetry.get_trace_context()
            ctx = TraceContextTextMapPropagator().extract(carrier=carrier)
            token = context_api.attach(ctx)
            try:
                yield
            finally:
                context_api.detach(token)

        _PID_PATTERN = re.compile(r"\bPID=(\d+)\b", re.IGNORECASE)

        def _add_client_ident_info(device, span):
            if not is_omni_thread():
                return
            ident = device.get_client_ident()
            if not ident:
                return
            if ident.client_lang in {LockerLanguage.JAVA, LockerLanguage.JAVA_6}:
                span.set_attribute(
                    "tango.client_ident.java_ident",
                    f"{ident.java_ident[0]:x}{ident.java_ident[1]:x}",
                )
                span.set_attribute("tango.client_ident.java_main_class", ident.java_main_class)
                match = _PID_PATTERN.search(ident.java_main_class)
                client_pid = int(match.group(1)) if match else 0
            else:
                client_pid = ident.client_pid
            span.set_attribute("tango.client_ident.location", ident.client_ip)
            span.set_attribute("tango.client_ident.pid", client_pid)
            span.set_attribute("tango.client_ident.lang", str(ident.client_lang))

        @contextlib.contextmanager
        def _real_span_to_cpptango(name: str, context=None, topic: str = ""):
            carrier = {}
            TraceContextTextMapPropagator().inject(carrier, context=context)
            traceparent = carrier.get("traceparent", "")
            tracestate = carrier.get("tracestate", "")
            with _telemetry.TraceContextScope(name, traceparent, tracestate, topic):
                yield

        def _create_span_processor_for_endpoint(endpoint: TelemetryEndpoint):
            global _telemetry_grpc_exporter_available
            global _telemetry_http_exporter_available
            endpoint_value = endpoint.endpoint
            exporter_type = endpoint.exporter
            if exporter_type == TelemetryExporter.GRPC:
                if not _telemetry_grpc_exporter_available:
                    return None

                try:
                    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
                        OTLPSpanExporter as OTLPGrpcSpanExporter,
                    )
                except ImportError:
                    _telemetry_grpc_exporter_available = False
                    warn_once(
                        "OpenTelemetry OTLP gRPC trace exporter package is not "
                        "available. Install opentelemetry-exporter-otlp-proto-grpc "
                        "to emit spans to gRPC tracing endpoints.",
                        key="telemetry-missing-exporter:grpc",
                        category=PyTangoUserWarning,
                        stacklevel=2,
                    )
                    return None

                endpoint_value = endpoint_value.lower()
                if endpoint_value.startswith("grpc://"):
                    endpoint_value = endpoint_value.replace("grpc://", "http://")
                exporter = OTLPGrpcSpanExporter(endpoint=endpoint_value)
            elif exporter_type == TelemetryExporter.HTTP:
                if not _telemetry_http_exporter_available:
                    return None

                try:
                    from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
                        OTLPSpanExporter as OTLPHttpSpanExporter,
                    )
                except ImportError:
                    _telemetry_http_exporter_available = False
                    warn_once(
                        "OpenTelemetry OTLP HTTP trace exporter package is not "
                        "available. Install opentelemetry-exporter-otlp-proto-http "
                        "to emit spans to HTTP tracing endpoints.",
                        key="telemetry-missing-exporter:http",
                        category=PyTangoUserWarning,
                        stacklevel=2,
                    )
                    return None

                exporter = OTLPHttpSpanExporter(endpoint=endpoint_value)
            elif exporter_type == TelemetryExporter.CONSOLE:
                io_out = sys.stderr if endpoint_value.lower() == "cerr" else sys.stdout
                exporter = ConsoleSpanExporter(out=io_out)
            else:
                raise ValueError(f"Unknown exporter type in {endpoint!r}")
            return _create_span_processor_for_exporter(exporter)

        def _create_span_processor_for_exporter(exporter):
            processor_type = ApiUtil.get_env_var("PYTANGO_TELEMETRY_SPAN_PROCESSOR_TYPE")
            if processor_type and processor_type.lower() == "simple":
                processor_class = SimpleSpanProcessor
            elif processor_type and processor_type.lower() == "batch":
                processor_class = BatchSpanProcessor
            elif isinstance(exporter, ConsoleSpanExporter):
                processor_class = SimpleSpanProcessor
            else:
                processor_class = BatchSpanProcessor
            return processor_class(exporter)

        def _real_default_telemetry_tracer_provider_factory(
            service_name: str,
            service_instance_id: None | str = None,
            extra_resource_attributes: None | dict[str, str] = None,
            endpoints: None | tuple[TelemetryEndpoint, ...] = None,
        ) -> trace_api.TracerProvider:
            if not _telemetry_sdk_available:
                return trace_api.NoOpTracerProvider()

            resource_attributes = {
                HOST_NAME: socket.getfqdn(),
                SERVICE_NAMESPACE: "tango",
                SERVICE_NAME: service_name,
            }
            if service_instance_id:
                resource_attributes[SERVICE_INSTANCE_ID] = service_instance_id
            if extra_resource_attributes:
                resource_attributes.update(extra_resource_attributes)

            processors = []
            for endpoint in endpoints or ():
                processor = _create_span_processor_for_endpoint(endpoint)
                if processor is not None:
                    processors.append(processor)

            if not processors:
                return trace_api.NoOpTracerProvider()

            tracer_provider = TracerProvider(resource=Resource.create(resource_attributes))
            for processor in processors:
                tracer_provider.add_span_processor(processor)
            return tracer_provider

        def _real_create_device_telemetry_tracer(
            tracer_provider: trace_api.TracerProvider,
        ) -> trace_api.Tracer:
            return trace_api.get_tracer(
                instrumenting_module_name="tango.python.server",
                instrumenting_library_version=Release.version,
                tracer_provider=tracer_provider,
            )

        @atexit.register
        def _shutdown_telemetry():
            _telemetry.cleanup_default_telemetry_interface()

        def _set_telemetry_sdk_log_level():
            level_str = ApiUtil.get_env_var("PYTANGO_TELEMETRY_SDK_LOG_LEVEL")
            if level_str:
                level_int = logging.getLevelNamesMapping()[level_str.upper()]
                names_csv = ApiUtil.get_env_var("PYTANGO_TELEMETRY_SDK_LOGGER_NAMES")
                if names_csv:
                    names = names_csv.split(",")
                else:
                    names = [
                        "opentelemetry.sdk.trace.export",
                        "opentelemetry.sdk._shared_internal",
                        "opentelemetry.exporter.otlp.proto.grpc.exporter",
                        "opentelemetry.exporter.otlp.proto.http._log_exporter",
                        "opentelemetry.exporter.otlp.proto.http.log_exporter",
                        "opentelemetry.exporter.otlp.proto.http.metric_exporter",
                        "opentelemetry.exporter.otlp.proto.http.trace_exporter",
                    ]
                for name in names:
                    logging.getLogger(name).setLevel(level_int)
                _telemetry.set_log_level(level_str)

        _set_telemetry_sdk_log_level()
        _real_telemetry_handlers = _TelemetryHandlers(
            get_current_otel_context=_real_get_current_otel_context,
            span_from_cpptango=_real_span_from_cpptango,
            context_from_cpptango=_real_context_from_cpptango,
            span_to_cpptango=_real_span_to_cpptango,
            tracer_provider_factory=_real_default_telemetry_tracer_provider_factory,
            create_device_tracer=_real_create_device_telemetry_tracer,
        )

except ImportError:
    pass
except Exception as exc:
    warnings.warn(
        f"Error setting up telemetry. Telemetry context may not be passed on "
        f"and traces may not be emitted. Possibly a PyTango bug.\n"
        f"Error: {exc!r}",
        stacklevel=1,
    )


class _TelemetryRuntimeManager:
    def __init__(
        self,
        runtime_available: bool,
        sdk_available: bool,
        real_handlers: _TelemetryHandlers,
        dummy_handlers: _TelemetryHandlers,
        telemetry_active: bool,
        client_tracing_endpoints,
        client_tracing_enabled,
    ):
        self._real_handlers = real_handlers
        self._dummy_handlers = dummy_handlers
        self._runtime_available = runtime_available
        self._sdk_available = sdk_available
        self._telemetry_active = telemetry_active
        self._using_real_handlers = False
        self._real_custom_factory = None
        self._client_tracing_endpoints = client_tracing_endpoints or ()
        self._client_tracing_enabled = client_tracing_enabled
        self._client_tracer = None
        self._skip_kernel_spans = None

    def runtime_available(self) -> bool:
        return self._runtime_available

    def skip_kernel_spans(self) -> bool:
        if self._skip_kernel_spans is None:
            self._skip_kernel_spans = not _truthy_env_var("PYTANGO_TELEMETRY_EMIT_KERNEL_SPANS")
        return self._skip_kernel_spans

    def reset_client_tracer(self):
        self._client_tracer = None

    def warn_if_telemetry_requested(self, endpoints: tuple[TelemetryEndpoint, ...]) -> tuple[bool, str]:
        if _truthy_env_var("PYTANGO_DISABLE_TELEMETRY_PATCHING"):
            return False, ""
        if not self._runtime_available:
            message = (
                "OpenTelemetry API packages are not available: telemetry context "
                "cannot be propagated and Python telemetry spans will not be "
                "emitted. Install opentelemetry-api to enable context "
                "propagation, plus opentelemetry-sdk and an OTLP exporter "
                "package to emit spans."
            )
            warn_now = warn_once(
                message,
                key="telemetry-missing-api",
                category=PyTangoUserWarning,
                stacklevel=2,
            )
            return warn_now, message
        if not self._sdk_available:
            message = (
                "OpenTelemetry SDK packages are not available: telemetry can be "
                "enabled in cppTango, but Python telemetry spans will not be "
                "emitted. Install opentelemetry-sdk and an OTLP exporter "
                "package to emit spans."
            )
            warn_now = warn_once(
                message,
                key="telemetry-missing-sdk",
                category=PyTangoUserWarning,
                stacklevel=2,
            )
            return warn_now, message
        unavailable_exporters = []
        if not _telemetry_http_exporter_available and any(
            endpoint.exporter == TelemetryExporter.HTTP for endpoint in endpoints
        ):
            unavailable_exporters.append(TelemetryExporter.HTTP)
        if not _telemetry_grpc_exporter_available and any(
            endpoint.exporter == TelemetryExporter.GRPC for endpoint in endpoints
        ):
            unavailable_exporters.append(TelemetryExporter.GRPC)
        if unavailable_exporters:
            exporter_messages = {
                TelemetryExporter.HTTP: ("OpenTelemetry OTLP HTTP trace exporter package is not available"),
                TelemetryExporter.GRPC: ("OpenTelemetry OTLP gRPC trace exporter package is not available"),
            }
            package_messages = {
                TelemetryExporter.HTTP: (
                    "Install opentelemetry-exporter-otlp-proto-http to emit spans to HTTP tracing endpoints."
                ),
                TelemetryExporter.GRPC: (
                    "Install opentelemetry-exporter-otlp-proto-grpc to emit spans to gRPC tracing endpoints."
                ),
            }
            messages = [exporter_messages[exporter] for exporter in unavailable_exporters]
            packages = [package_messages[exporter] for exporter in unavailable_exporters]
            message = f"{'; '.join(messages)}. {' '.join(packages)}"
            warn_key_suffix = ",".join(exporter.name.lower() for exporter in unavailable_exporters)
            warn_now = warn_once(
                message,
                key=f"telemetry-missing-exporter:{warn_key_suffix}",
                category=PyTangoUserWarning,
                stacklevel=2,
            )
            return warn_now, message
        return False, ""

    def switch_handlers(self, use_real: bool):
        use_real = use_real and self._runtime_available
        self._using_real_handlers = use_real
        self.reset_client_tracer()

    def set_custom_factory(self, provider_factory):
        self._real_custom_factory = provider_factory
        self.reset_client_tracer()

    def get_factory(self):
        if self._using_real_handlers:
            return self._real_custom_factory or self._real_handlers.tracer_provider_factory
        return self._dummy_handlers.tracer_provider_factory

    def get_client_tracing_endpoints(self) -> tuple[TelemetryEndpoint, ...]:
        return self._client_tracing_endpoints

    def refresh_from_env(self):
        config = _get_env_telemetry_config()
        enabled = self._runtime_available and config.enabled
        config_changed = (
            enabled != self._telemetry_active
            or config.tracing_endpoints != self._client_tracing_endpoints
            or config.tracing_enabled != self._client_tracing_enabled
        )
        if config_changed and config.enabled:
            self.warn_if_telemetry_requested(config.tracing_endpoints)
        if config_changed:
            self._telemetry_active = enabled
            self._client_tracing_endpoints = config.tracing_endpoints
            self._client_tracing_enabled = config.tracing_enabled
            self.reset_client_tracer()

    def can_propagate_context(self):
        return self._runtime_available and self._telemetry_active

    def should_emit_client_spans(self):
        return self.can_propagate_context() and self._client_tracing_enabled

    def get_current_otel_context(self):
        if self.can_propagate_context():
            return self._real_handlers.get_current_otel_context()
        return self._dummy_handlers.get_current_otel_context()

    def span_from_cpptango(self, device, fn):
        if self._runtime_available and device._is_telemetry_enabled():
            return self._real_handlers.span_from_cpptango(device, fn)
        return self._dummy_handlers.span_from_cpptango(device, fn)

    def context_from_cpptango(self):
        if self.can_propagate_context():
            return self._real_handlers.context_from_cpptango()
        return self._dummy_handlers.context_from_cpptango()

    def span_to_cpptango(self, name: str, context=None, topic: str = ""):
        if self.can_propagate_context():
            return self._real_handlers.span_to_cpptango(name, context=context, topic=topic)
        return self._dummy_handlers.span_to_cpptango(name, context=context, topic=topic)

    def create_device_telemetry_tracer(self, tracer_provider):
        if self._using_real_handlers:
            return self._real_handlers.create_device_tracer(tracer_provider)
        return self._dummy_handlers.create_device_tracer(tracer_provider)

    def using_real_handlers(self):
        return self._using_real_handlers

    def get_or_create_client_tracer(self):
        if self._client_tracer is None and self._runtime_available:
            self.warn_if_telemetry_requested(self._client_tracing_endpoints)
            self._client_tracer = self._create_client_tracer()
        return self._client_tracer

    def _create_client_tracer(self):
        service_name = ApiUtil.get_env_var("PYTANGO_TELEMETRY_CLIENT_SERVICE_NAME")
        if not service_name:
            service_name = "pytango.client"
        tracer_provider = _call_tracer_provider_factory(
            self.get_factory(),
            service_name,
            endpoints=self._client_tracing_endpoints,
        )
        return _trace_api.get_tracer(
            instrumenting_module_name="tango.python.client",
            instrumenting_library_version=Release.version,
            tracer_provider=tracer_provider,
        )


_telemetry_runtime = _TelemetryRuntimeManager(
    runtime_available=_telemetry_runtime_available,
    sdk_available=_telemetry_sdk_available,
    real_handlers=_real_telemetry_handlers,
    dummy_handlers=_dummy_telemetry_handlers,
    telemetry_active=_env_telemetry_config.enabled,
    client_tracing_endpoints=_env_telemetry_config.tracing_endpoints,
    client_tracing_enabled=_env_telemetry_config.tracing_enabled,
)
_telemetry_runtime.switch_handlers(use_real=_telemetry_runtime_available)


def set_telemetry_tracer_provider_factory(provider_factory: TracerProviderFactory):
    """
    Change the factory that will be used to create tracer providers.

    .. versionadded:: 10.3.0
    """

    _telemetry_runtime.set_custom_factory(provider_factory)


def _wrap_tracer_provider_factory_with_client_env_defaults(
    provider_factory: TracerProviderFactory,
) -> TracerProviderFactory:
    def wrapped_factory(
        service_name: str,
        service_instance_id: None | str = None,
        extra_resource_attributes: None | dict[str, str] = None,
        endpoints: None | tuple[TelemetryEndpoint, ...] = None,
    ):
        _telemetry_runtime.refresh_from_env()
        if endpoints is None:
            endpoints = _telemetry_runtime.get_client_tracing_endpoints()
        return _call_tracer_provider_factory(
            provider_factory,
            service_name,
            service_instance_id,
            extra_resource_attributes,
            endpoints=endpoints,
        )

    return wrapped_factory


def get_telemetry_tracer_provider_factory() -> TracerProviderFactory:
    """
    Get the factory that will be used to create tracer providers.

    If ``endpoints`` is omitted when calling the returned factory,
    the current client tracing endpoints derived from the environment
    variables are used.

    .. versionadded:: 10.3.0
    """
    return _wrap_tracer_provider_factory_with_client_env_defaults(_telemetry_runtime.get_factory())
