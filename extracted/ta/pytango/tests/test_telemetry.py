# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

import contextlib
import enum
import importlib
import inspect
import logging
import os
import sys
import typing
import warnings
from collections import defaultdict

try:
    from opentelemetry import trace as trace_api
    from opentelemetry.sdk.resources import (
        SERVICE_INSTANCE_ID,
        SERVICE_NAME,
        Resource,
    )
    from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    opentelemetry_packages_available = True
except ImportError:
    opentelemetry_packages_available = False

import pytest

import tango
import tango._instrumentation
import tango._warnings
import tango.device_server
import tango.server
from tango import DevFailed, DeviceProxy, DevState, GreenMode, constants
from tango._warnings import PyTangoUserWarning
from tango.asyncio import DeviceProxy as AsyncioDeviceProxy
from tango.server import Device, attribute, command
from tango.telemetry import (
    TelemetryEndpoint,
    TelemetryExporter,
    get_telemetry_tracer_provider_factory,
    set_telemetry_tracer_provider_factory,
)
from tango.test_context import DeviceTestContext, MultiDeviceTestContext

# check if most tests can be run, or should be skipped
skip_reasons = []

if not tango.constants.TELEMETRY_SUPPORTED:
    skip_reasons.append("Telemetry support is not compiled into cppTango/PyTango.")
if not opentelemetry_packages_available:
    skip_reasons.append("OpenTelemetry is not installed.")

telemetry_unavailable = any(skip_reasons)
skip_message = " ".join(skip_reasons)

# TODO: update when cpptango version that fixes user topics and tracing is known, likely 10.4.0
# https://gitlab.com/tango-controls/cppTango/-/work_items/1645
user_topics_and_tracing_fixed = tango.constants.TANGO_VERSION_NB >= 990000


@pytest.fixture()
def exporters():
    """Switch to in-memory exporters for Python telemetry"""
    in_mem_exporters: dict[str, InMemorySpanExporter] = {}

    old_factory = get_telemetry_tracer_provider_factory()
    _set_in_memory_tracer_provider(in_mem_exporters)
    yield in_mem_exporters
    set_telemetry_tracer_provider_factory(old_factory)


def _set_in_memory_tracer_provider(in_mem_exporters):
    from tango._telemetry import _create_span_processor_for_endpoint

    def in_memory_tracer_provider(
        service_name,
        service_instance_id=None,
        extra_resource_attributes=None,
        endpoints=None,
    ):
        resource_attributes = {SERVICE_NAME: service_name}
        if service_instance_id:
            resource_attributes[SERVICE_INSTANCE_ID] = service_instance_id
        tracer_provider = TracerProvider(resource=Resource.create(resource_attributes))
        exporter = InMemorySpanExporter()
        in_mem_exporters[service_name] = exporter
        processor = SimpleSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)
        logging.debug(f"exporters.in_memory_tracer_provider: {service_name=}")
        for endpoint in endpoints:
            processor = _create_span_processor_for_endpoint(endpoint)
            tracer_provider.add_span_processor(processor)
        return tracer_provider

    tango.telemetry.set_telemetry_tracer_provider_factory(in_memory_tracer_provider)


@pytest.fixture(autouse=True)
def telemetry_enabled_env(monkeypatch, request):
    # enable telemetry for all tests (currently, the only way to ensure client-only spans are emitted)
    monkeypatch.setenv("TANGO_TELEMETRY_ENABLE", "on")


@pytest.fixture
def maybe_telemetry_user_topic_env(monkeypatch, request):
    if user_topics_and_tracing_fixed:
        # set user topic (currently, the only way to ensure client topics)
        monkeypatch.setenv("TANGO_TELEMETRY_TOPICS", "user")


@pytest.fixture
def emit_kernel_spans(monkeypatch):
    monkeypatch.setattr(tango._telemetry._telemetry_runtime, "_skip_kernel_spans", False)


@pytest.fixture
def custom_tracer():
    factory = get_telemetry_tracer_provider_factory()
    custom_provider = factory("custom")
    custom_tracer = trace_api.get_tracer("custom.tracer", tracer_provider=custom_provider)
    return custom_tracer


class CapturedTelemetry:
    def __init__(self, exporters):
        self._exporters = exporters
        self._device_class_name = ""
        self._client_spans: dict[str, list[ReadableSpan]] = defaultdict(list)
        self._device_spans: dict[str, list[ReadableSpan]] = defaultdict(list)

    def set_device_class_name(self, name):
        self._device_class_name = name

    @property
    def client_startup_spans(self) -> list["ReadableSpan"]:
        return self._client_spans["startup"]

    @property
    def device_startup_spans(self) -> list["ReadableSpan"]:
        return self._device_spans["startup"]

    @property
    def client_running_spans(self) -> list["ReadableSpan"]:
        return self._client_spans["running"]

    @property
    def device_running_spans(self) -> list["ReadableSpan"]:
        return self._device_spans["running"]

    @property
    def client_shutdown_spans(self) -> list["ReadableSpan"]:
        return self._client_spans["shutdown"]

    @property
    def device_shutdown_spans(self) -> list["ReadableSpan"]:
        return self._device_spans["shutdown"]

    def startup_done(self):
        self._stage_done("startup")

    def running_done(self):
        self._stage_done("running")

    def shutdown_done(self):
        self._stage_done("shutdown")

    def ignore_recent_spans(self):
        self._stage_done("ignore")

    def _stage_done(self, stage):
        client = self._exporters.get("pytango.client")
        if client:
            client_spans = client.get_finished_spans()
            client.clear()
        else:
            client_spans = []
        device = self._exporters.get(self._device_class_name)
        if device:
            device_spans = device.get_finished_spans()
            device.clear()
        else:
            device_spans = []
        logging.debug(f"CapturedTelemetry._stage_done {stage=}")
        for client_span in client_spans:
            logging.debug(f"CapturedTelemetry  {client_span.name=}")
        for device_span in device_spans:
            logging.debug(f"CapturedTelemetry  {device_span.name=}")
        self._client_spans[stage] = client_spans
        self._device_spans[stage] = device_spans


def print_json(spans):
    """Utility that is useful when debugging tests"""
    print(f"===== Printing {len(spans)} spans... ========")
    for span in spans:
        print(span.to_json())
        print("-----------------------")
    print(f"===== Done printing {len(spans)} spans ========")


def _reload_telemetry_modules():
    internal = importlib.reload(tango._telemetry)
    public = importlib.reload(tango.telemetry)
    return internal, public


@contextlib.contextmanager
def _opentelemetry_imports_unavailable(monkeypatch, *, missing="api"):
    original_import = __import__
    original_find_spec = importlib.util.find_spec
    if missing == "api":
        blocked_prefixes = ("opentelemetry",)
    elif missing == "sdk":
        blocked_prefixes = (
            "opentelemetry.sdk",
            "opentelemetry.exporter",
        )
    elif missing == "http_exporter":
        blocked_prefixes = ("opentelemetry.exporter.otlp.proto.http",)
    elif missing == "grpc_exporter":
        blocked_prefixes = ("opentelemetry.exporter.otlp.proto.grpc",)
    else:
        raise ValueError(f"Unsupported missing import mode: {missing!r}")

    original_modules = {
        name: module
        for name, module in sys.modules.items()
        if any(name == prefix or name.startswith(f"{prefix}.") for prefix in blocked_prefixes)
    }

    for name in list(original_modules):
        monkeypatch.delitem(sys.modules, name, raising=False)

    def raising_import(name, globals=None, locals=None, fromlist=(), level=0):
        if any(name == prefix or name.startswith(f"{prefix}.") for prefix in blocked_prefixes):
            raise ImportError("mocked missing opentelemetry")
        return original_import(name, globals, locals, fromlist, level)

    def missing_find_spec(name, package=None):
        if any(name == prefix or name.startswith(f"{prefix}.") for prefix in blocked_prefixes):
            return None
        return original_find_spec(name, package)

    monkeypatch.setattr("builtins.__import__", raising_import)
    monkeypatch.setattr(importlib.util, "find_spec", missing_find_spec)
    try:
        yield
    finally:
        for name in list(sys.modules):
            if any(name == prefix or name.startswith(f"{prefix}.") for prefix in blocked_prefixes):
                sys.modules.pop(name, None)
        sys.modules.update(original_modules)


@contextlib.contextmanager
def _isolated_telemetry_warning_state():
    tango._warnings._already_warned_keys.clear()
    try:
        yield
    finally:
        tango._warnings._already_warned_keys.clear()


def _reload_telemetry_runtime_references(monkeypatch):
    telemetry_runtime = tango._telemetry._telemetry_runtime
    monkeypatch.setattr(tango._instrumentation, "_telemetry_runtime", telemetry_runtime)
    monkeypatch.setattr(tango.server, "_telemetry_runtime", telemetry_runtime)
    monkeypatch.setattr(tango.device_server, "_telemetry_runtime", telemetry_runtime)


@pytest.fixture()
def simple_device():
    # Note: Telemetry spans are not emitted for BaseDevice methods by default,
    # so we override init_device, delete_device and dev_state in our test device.
    # This lets us verify that user methods will generate spans.

    class TestDevice(Device):
        def init_device(self):
            super().init_device()

        def delete_device(self):
            super().delete_device()

        def dev_state(self):
            return DevState.RUNNING

        @attribute
        def lineno_attribute(self) -> int:
            return inspect.currentframe().f_lineno - 2

        @command
        def lineno_command(self) -> int:
            return inspect.currentframe().f_lineno - 2

    return TestDevice


@pytest.fixture()
def simple_device_gm(server_green_mode):
    # Same as simple_device, but this here we support all green modes

    if server_green_mode == GreenMode.Asyncio:

        class TestDevice(Device):
            green_mode = server_green_mode

            async def init_device(self):
                await super().init_device()

            async def delete_device(self):
                await super().delete_device()

            async def dev_state(self):
                return DevState.RUNNING

            @attribute
            async def lineno_attribute(self) -> int:
                return inspect.currentframe().f_lineno - 2

            @command
            async def lineno_command(self) -> int:
                return inspect.currentframe().f_lineno - 2

    else:

        class TestDevice(Device):
            def init_device(self):
                super().init_device()

            def delete_device(self):
                super().delete_device()

            def dev_state(self):
                return DevState.RUNNING

            @attribute
            def lineno_attribute(self) -> int:
                return inspect.currentframe().f_lineno - 2

            @command
            def lineno_command(self) -> int:
                return inspect.currentframe().f_lineno - 2

    return TestDevice


@contextlib.contextmanager
def span_recording_device_test_context(
    telemetry: CapturedTelemetry, device_class: type[Device], **kwargs
) -> typing.Generator[DeviceProxy, None, None]:
    """Context manager that records the telemetry spans around DeviceTestContext.

    This lets us capture the spans created at various stages:
      - on device startup
      - while the device is running (if test function accesses device via proxy)
      - on device shutdown
    """
    telemetry.set_device_class_name(device_class.__name__)
    # ensure telemetry is enabled and topic set, unless explicitly provided in properties
    default_topics = "user" if user_topics_and_tracing_fixed else "all"
    if "properties" not in kwargs:
        kwargs["properties"] = {
            "telemetry_enable": "1",
            "telemetry_topics": default_topics,
        }
    else:
        if "telemetry_enable" not in kwargs["properties"]:
            kwargs["properties"]["telemetry_enable"] = "1"
        if "telemetry_topics" not in kwargs["properties"]:
            kwargs["properties"]["telemetry_topics"] = default_topics
    context = DeviceTestContext(device_class, **kwargs)
    context.start()
    try:
        telemetry.startup_done()
        yield context.device
        telemetry.running_done()
    finally:
        context.stop()
        context.join()
    telemetry.shutdown_done()


def test_telemetry_available_constant():
    assert isinstance(constants.TELEMETRY_SUPPORTED, bool)
    assert isinstance(tango._tango._telemetry.TELEMETRY_ENABLED, bool)
    assert constants.TELEMETRY_SUPPORTED == tango._tango._telemetry.TELEMETRY_ENABLED


@pytest.mark.skipif(
    constants.TELEMETRY_SUPPORTED,
    reason="Telemetry support is compiled into cppTango",
)
def test_device_impl_no_op_telemetry_methods_exist_and_are_callable():
    class TestDevice(Device):
        @command(dtype_out=(str,))
        def run_no_op_telemetry_methods(self):
            telemetry_enabled = self._is_telemetry_enabled()
            topic_enabled = self._check_telemetry_topic("all")
            tracing_enabled = self._is_telemetry_tracing_enabled()
            tracing_endpoints = self._get_telemetry_tracing_endpoints()
            return [
                f"telemetry_enabled={telemetry_enabled}",
                f"topic_enabled={topic_enabled}",
                f"tracing_enabled={tracing_enabled}",
                f"tracing_endpoints={tracing_endpoints}",
            ]

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.run_no_op_telemetry_methods() == [
            "telemetry_enabled=False",
            "topic_enabled=False",
            "tracing_enabled=False",
            "tracing_endpoints=[]",
        ]


def test_device_proxy_telemetry_methods_are_exposed():
    method_names = (
        "is_telemetry_enabled",
        "start_telemetry",
        "stop_telemetry",
        "get_telemetry_topics",
        "set_telemetry_topics",
        "get_telemetry_tracing",
        "set_telemetry_tracing",
        "get_telemetry_tracing_endpoints",
        "set_telemetry_tracing_endpoints",
        "add_telemetry_tracing_endpoint",
        "remove_telemetry_tracing_endpoint",
        "get_telemetry_logging",
        "set_telemetry_logging",
        "get_telemetry_logging_endpoints",
        "set_telemetry_logging_endpoints",
        "add_telemetry_logging_endpoint",
        "remove_telemetry_logging_endpoint",
    )

    for method_name in method_names:
        assert hasattr(DeviceProxy, method_name)


def test_telemetry_enums_are_exposed():
    assert issubclass(tango.telemetry.TelemetryExporter, enum.IntEnum)
    assert issubclass(tango.telemetry.TelemetryType, enum.IntEnum)
    assert issubclass(tango.telemetry.TelemetryTopic, enum.IntEnum)
    # Check some of the members are exposed
    assert hasattr(tango.telemetry.TelemetryExporter, "HTTP")
    assert hasattr(tango.telemetry.TelemetryType, "TRACING")
    assert hasattr(tango.telemetry.TelemetryTopic, "USER")


def _enum_members(enum_type):
    return {name: member.value for name, member in enum_type.__members__.items()}


@pytest.mark.skipif(
    not constants.TELEMETRY_SUPPORTED,
    reason="cppTango telemetry enums are not compiled in",
)
def test_telemetry_enum_fallback_values_match_cpptango():
    from tango._tango import _telemetry as cpptango_telemetry

    assert {
        "TelemetryExporter": _enum_members(tango.telemetry.TelemetryExporter),
        "TelemetryType": _enum_members(tango.telemetry.TelemetryType),
        "TelemetryTopic": _enum_members(tango.telemetry.TelemetryTopic),
    } == cpptango_telemetry._ENUM_MEMBERS


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_new_env_var_names(monkeypatch):
    with monkeypatch.context() as env:
        env.setenv("TANGO_TELEMETRY_ENABLE", "on")
        env.setenv("TANGO_TELEMETRY_TRACING_EXPORTERS", "console,http")
        env.setenv(
            "TANGO_TELEMETRY_TRACING_ENDPOINTS",
            "cout,https://traces.example/v1/traces",
        )
        env.setenv("TANGO_TELEMETRY_LOGGING_EXPORTERS", "grpc,console")
        env.setenv(
            "TANGO_TELEMETRY_LOGGING_ENDPOINTS",
            "grpc://logs.example:4317,cerr",
        )
        env.setenv("TANGO_TELEMETRY_TYPES", "tracing, logging")
        env.setenv("TANGO_TELEMETRY_TOPICS", " user , polling ")

        telemetry_internal, telemetry_public = _reload_telemetry_modules()
        config = telemetry_internal._get_env_telemetry_config()
        expected_tracing_endpoints = (
            telemetry_public.TelemetryEndpoint(telemetry_public.TelemetryExporter.CONSOLE, "cout"),
            telemetry_public.TelemetryEndpoint(
                telemetry_public.TelemetryExporter.HTTP,
                "https://traces.example/v1/traces",
            ),
        )
        expected_logging_endpoints = (
            telemetry_public.TelemetryEndpoint(telemetry_public.TelemetryExporter.GRPC, "grpc://logs.example:4317"),
            telemetry_public.TelemetryEndpoint(telemetry_public.TelemetryExporter.CONSOLE, "cerr"),
        )
        expected_types = (
            telemetry_public.TelemetryType.TRACING,
            telemetry_public.TelemetryType.LOGGING,
        )
        expected_topics = (
            telemetry_public.TelemetryTopic.USER,
            telemetry_public.TelemetryTopic.POLLING,
        )

    assert config.tracing_endpoints == expected_tracing_endpoints
    assert config.logging_endpoints == expected_logging_endpoints
    assert config.enabled is True
    assert config.types == expected_types
    assert config.topics == expected_topics
    assert config.tracing_enabled is True
    assert config.logging_enabled is True
    assert telemetry_internal._telemetry_runtime._client_tracing_endpoints == (expected_tracing_endpoints)

    _reload_telemetry_modules()


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_public_factory_uses_client_env_endpoints_by_default(monkeypatch):
    with monkeypatch.context() as env:
        env.setenv("TANGO_TELEMETRY_ENABLE", "on")
        env.setenv("TANGO_TELEMETRY_TRACING_EXPORTERS", "console,http")
        env.setenv(
            "TANGO_TELEMETRY_TRACING_ENDPOINTS",
            "cout,https://traces.example/v1/traces",
        )

        _, telemetry_public = _reload_telemetry_modules()
        expected_endpoints = (
            telemetry_public.TelemetryEndpoint(telemetry_public.TelemetryExporter.CONSOLE, "cout"),
            telemetry_public.TelemetryEndpoint(
                telemetry_public.TelemetryExporter.HTTP,
                "https://traces.example/v1/traces",
            ),
        )
        observed_calls = []

        def recording_factory(
            service_name,
            service_instance_id=None,
            extra_resource_attributes=None,
            endpoints=None,
        ):
            observed_calls.append(
                (
                    service_name,
                    service_instance_id,
                    extra_resource_attributes,
                    endpoints,
                )
            )
            return object()

        telemetry_public.set_telemetry_tracer_provider_factory(recording_factory)
        factory = telemetry_public.get_telemetry_tracer_provider_factory()
        factory("my.app")

    assert observed_calls == [("my.app", None, None, expected_endpoints)]

    _reload_telemetry_modules()


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
@pytest.mark.parametrize(
    ("deprecated_name", "replacement_name", "deprecated_value"),
    [
        (
            "TANGO_TELEMETRY_TRACES_EXPORTER",
            "TANGO_TELEMETRY_TRACING_EXPORTERS",
            "http",
        ),
        (
            "TANGO_TELEMETRY_TRACES_ENDPOINT",
            "TANGO_TELEMETRY_TRACING_ENDPOINTS",
            "https://traces.example/v1/traces",
        ),
        (
            "TANGO_TELEMETRY_LOGS_EXPORTER",
            "TANGO_TELEMETRY_LOGGING_EXPORTERS",
            "grpc",
        ),
        (
            "TANGO_TELEMETRY_LOGS_ENDPOINT",
            "TANGO_TELEMETRY_LOGGING_ENDPOINTS",
            "grpc://logs.example:4317",
        ),
    ],
)
def test_old_env_var_names_warn_but_do_not_configure(monkeypatch, deprecated_name, replacement_name, deprecated_value):

    with monkeypatch.context() as env:
        env.setenv("TANGO_TELEMETRY_ENABLE", "on")
        env.setenv(deprecated_name, deprecated_value)

        with pytest.warns(
            DeprecationWarning,
            match=rf"{deprecated_name} is deprecated; use {replacement_name} instead\.",
        ):
            telemetry_internal, telemetry_public = _reload_telemetry_modules()
            config = telemetry_internal._get_env_telemetry_config()

    expected_default_endpoints = (telemetry_public.TelemetryEndpoint(telemetry_public.TelemetryExporter.CONSOLE, ""),)
    assert config.tracing_endpoints == expected_default_endpoints
    assert config.logging_endpoints == expected_default_endpoints
    assert config.enabled is True
    assert config.tracing_enabled is True
    assert config.logging_enabled is True
    assert telemetry_internal._telemetry_runtime._client_tracing_endpoints == (expected_default_endpoints)

    _reload_telemetry_modules()


def test_no_warning_at_import_time(monkeypatch):
    with (
        _isolated_telemetry_warning_state(),
        _opentelemetry_imports_unavailable(monkeypatch),
        warnings.catch_warnings(record=True) as recorded,
    ):
        warnings.simplefilter("always")
        _reload_telemetry_modules()

    assert recorded == []
    _reload_telemetry_modules()


@pytest.mark.parametrize("missing", ["sdk", "http_exporter"])
def test_no_warning_at_import_time_when_otel_dependency_unavailable_and_env_configured(monkeypatch, missing):
    with _isolated_telemetry_warning_state():
        monkeypatch.setenv("TANGO_TELEMETRY_ENABLE", "on")
        monkeypatch.setenv("TANGO_TELEMETRY_TRACING_EXPORTERS", "http")
        monkeypatch.setenv(
            "TANGO_TELEMETRY_TRACING_ENDPOINTS",
            "http://localhost:4317/v1/traces",
        )
        with (
            _opentelemetry_imports_unavailable(monkeypatch, missing=missing),
            warnings.catch_warnings(record=True) as recorded,
        ):
            warnings.simplefilter("always")
            _reload_telemetry_modules()

    assert recorded == []
    _reload_telemetry_modules()


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
@pytest.mark.parametrize(
    ("missing", "match"),
    [
        ("api", "OpenTelemetry API packages are not available"),
        ("sdk", "OpenTelemetry SDK packages are not available"),
    ],
)
def test_warning_when_otel_dependency_unavailable_device(monkeypatch, missing, match):
    with _isolated_telemetry_warning_state():
        monkeypatch.setenv("TANGO_TELEMETRY_ENABLE", "off")
        with _opentelemetry_imports_unavailable(monkeypatch, missing=missing):
            _reload_telemetry_modules()
            _reload_telemetry_runtime_references(monkeypatch)

            with DeviceTestContext(Device) as proxy, pytest.warns(PyTangoUserWarning, match=match):
                proxy.start_telemetry()
    _reload_telemetry_modules()


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
@pytest.mark.parametrize(
    ("missing", "match", "env"),
    [
        (
            "api",
            "OpenTelemetry API packages are not available",
            {},
        ),
        (
            "sdk",
            "OpenTelemetry SDK packages are not available",
            {},
        ),
        (
            "http_exporter",
            "OpenTelemetry OTLP HTTP trace exporter package is not available",
            {
                "TANGO_TELEMETRY_TRACING_EXPORTERS": "http",
                "TANGO_TELEMETRY_TRACING_ENDPOINTS": "http://localhost:4317/v1/traces",
            },
        ),
    ],
)
def test_warning_when_otel_dependency_unavailable_client(monkeypatch, missing, match, env):
    with _isolated_telemetry_warning_state():
        monkeypatch.setenv("TANGO_TELEMETRY_ENABLE", "on")
        for key, value in env.items():
            monkeypatch.setenv(key, value)
        with _opentelemetry_imports_unavailable(monkeypatch, missing=missing):
            _reload_telemetry_modules()
            _reload_telemetry_runtime_references(monkeypatch)

            with pytest.warns(PyTangoUserWarning, match=match):
                _ = DeviceProxy("tango://127.0.0.1:12345/non/existent/device#dbase=no")
    _reload_telemetry_modules()


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_refresh_from_env_warns_for_new_http_endpoints_only_when_config_changes(
    monkeypatch,
):
    with _isolated_telemetry_warning_state():
        monkeypatch.setenv("TANGO_TELEMETRY_ENABLE", "on")
        monkeypatch.setenv("TANGO_TELEMETRY_TRACING_EXPORTERS", "console")
        with _opentelemetry_imports_unavailable(monkeypatch, missing="http_exporter"):
            _reload_telemetry_modules()
            _reload_telemetry_runtime_references(monkeypatch)

            monkeypatch.setenv("TANGO_TELEMETRY_TRACING_EXPORTERS", "http")
            monkeypatch.setenv(
                "TANGO_TELEMETRY_TRACING_ENDPOINTS",
                "http://localhost:4317/v1/traces",
            )

            with pytest.warns(
                PyTangoUserWarning,
                match="OpenTelemetry OTLP HTTP trace exporter package is not available",
            ):
                tango._telemetry._telemetry_runtime.refresh_from_env()

            with warnings.catch_warnings(record=True) as recorded:
                warnings.simplefilter("always")
                tango._telemetry._telemetry_runtime.refresh_from_env()

    assert recorded == []
    _reload_telemetry_modules()


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_lazy_exporter_import_failure_warns(monkeypatch):
    with _isolated_telemetry_warning_state():
        monkeypatch.setenv("TANGO_TELEMETRY_ENABLE", "on")
        monkeypatch.setenv("TANGO_TELEMETRY_TRACING_EXPORTERS", "http")
        monkeypatch.setenv(
            "TANGO_TELEMETRY_TRACING_ENDPOINTS",
            "http://localhost:4317/v1/traces",
        )
        with _opentelemetry_imports_unavailable(monkeypatch, missing="http_exporter"):
            missing_find_spec = importlib.util.find_spec

            def available_find_spec(name, package=None):
                if name == "opentelemetry.exporter.otlp.proto.http.trace_exporter":
                    return importlib.machinery.ModuleSpec(name, loader=None)
                return missing_find_spec(name, package)

            monkeypatch.setattr(importlib.util, "find_spec", available_find_spec)
            _reload_telemetry_modules()

            with pytest.warns(
                PyTangoUserWarning,
                match="OpenTelemetry OTLP HTTP trace exporter package is not available",
            ):
                tango._telemetry.get_telemetry_tracer_provider_factory()("test")

            assert not tango._telemetry._telemetry_http_exporter_available
    _reload_telemetry_modules()


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_repeated_enable_does_not_spam_warnings(monkeypatch):
    class WarnRecordingDevice(Device):
        warn_messages: typing.ClassVar[list] = []

        def warn_stream(self, msg, *args, **kwargs):
            WarnRecordingDevice.warn_messages.append(msg)

    with _isolated_telemetry_warning_state():
        monkeypatch.setenv("TANGO_TELEMETRY_ENABLE", "off")
        with _opentelemetry_imports_unavailable(monkeypatch, missing="api"):
            _reload_telemetry_modules()
            _reload_telemetry_runtime_references(monkeypatch)

            with (
                DeviceTestContext(WarnRecordingDevice) as proxy,
                warnings.catch_warnings(record=True) as recorded,
            ):
                warnings.simplefilter("always")
                proxy.start_telemetry()
                proxy.stop_telemetry()
                proxy.start_telemetry()

    assert len(recorded) == 1
    assert issubclass(recorded[0].category, PyTangoUserWarning)
    assert len(WarnRecordingDevice.warn_messages) == 1
    assert "OpenTelemetry API packages are not available" in WarnRecordingDevice.warn_messages[0]
    _reload_telemetry_modules()


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_init_device_and_basic_span_details(exporters, simple_device_gm, emit_kernel_spans):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device_gm):
        pass

    assert len(telemetry.client_startup_spans) > 0
    assert len(telemetry.device_startup_spans) > 0

    client_span = telemetry.client_startup_spans[0]
    assert client_span.name == "span_recording_device_test_context"
    assert client_span.resource.attributes[SERVICE_NAME] == "pytango.client"
    assert client_span.attributes["code.filepath"] == __file__
    assert "code.lineno" in client_span.attributes
    assert "thread.id" in client_span.attributes
    assert "thread.name" in client_span.attributes

    span_index = 0 if user_topics_and_tracing_fixed else 1
    device_span = telemetry.device_startup_spans[span_index]
    assert device_span.name == "simple_device_gm.<locals>.TestDevice.init_device"
    assert device_span.resource.attributes[SERVICE_NAME] == "TestDevice"
    assert device_span.resource.attributes[SERVICE_INSTANCE_ID] == "test/nodb/testdevice"
    assert device_span.attributes["code.filepath"] == __file__
    assert "code.lineno" in device_span.attributes
    assert "thread.id" in device_span.attributes
    assert "thread.name" in device_span.attributes


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_delete_device(exporters, simple_device_gm):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device_gm):
        pass

    assert len(telemetry.client_shutdown_spans) == 1
    assert len(telemetry.device_shutdown_spans) >= 1

    client_span = telemetry.client_shutdown_spans[0]
    assert client_span.name == "span_recording_device_test_context"

    device_span = telemetry.device_shutdown_spans[-1]
    assert device_span.name == "simple_device_gm.<locals>.TestDevice.delete_device"


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_state(exporters, simple_device_gm, maybe_telemetry_user_topic_env):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device_gm) as proxy:
        proxy.State()
        state_lineno = inspect.currentframe().f_lineno - 1

    assert_single_client_span_and_device_running_spans_share_trace_id(telemetry)

    client_span = telemetry.client_running_spans[0]
    assert client_span.name == "test_state"
    assert client_span.attributes["code.lineno"] == state_lineno

    device_span = telemetry.device_running_spans[-1]
    assert device_span.name == "simple_device_gm.<locals>.TestDevice.dev_state"


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_static_command(exporters, simple_device_gm, maybe_telemetry_user_topic_env):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device_gm) as proxy:
        device_lineno = proxy.lineno_command()
        client_lineno = inspect.currentframe().f_lineno - 1

    assert_single_client_span_and_device_running_spans_share_trace_id(telemetry)

    client_span = telemetry.client_running_spans[0]
    assert client_span.name == "test_static_command"
    assert client_span.attributes["code.lineno"] == client_lineno

    device_span = telemetry.device_running_spans[-1]
    assert device_span.name == "simple_device_gm.<locals>.TestDevice.lineno_command"
    assert device_span.attributes["code.lineno"] == device_lineno


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_static_attribute(exporters, simple_device_gm, green_mode_device_proxy, maybe_telemetry_user_topic_env):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device_gm) as proxy:
        gm_proxy = green_mode_device_proxy(proxy.dev_name())  # emits some spans
        telemetry.ignore_recent_spans()
        device_lineno = gm_proxy.read_attribute("lineno_attribute", wait=True).value
        client_lineno = inspect.currentframe().f_lineno - 1

    assert_single_client_span_and_device_running_spans_share_trace_id(telemetry)

    client_span = telemetry.client_running_spans[0]
    assert client_span.name == "test_static_attribute"
    assert client_span.attributes["code.lineno"] == client_lineno

    device_span = telemetry.device_running_spans[-1]
    assert device_span.name == "simple_device_gm.<locals>.TestDevice.lineno_attribute"
    assert device_span.attributes["code.lineno"] == device_lineno


def assert_single_client_span_and_device_running_spans_share_trace_id(telemetry):
    assert len(telemetry.client_running_spans) == 1
    assert len(telemetry.device_running_spans) >= 1

    client_id = telemetry.client_running_spans[0].context.trace_id
    devices_ids = [span.context.trace_id for span in telemetry.device_running_spans]
    assert all(client_id == device_id for device_id in devices_ids)


def _trace_id_from_traceparent(traceparent: str) -> str:
    return traceparent.split("-")[1]


def _span_id_hex(span_id: int) -> str:
    return format(span_id, "016x")


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
@pytest.mark.asyncio
async def test_static_attribute_asyncio(exporters, simple_device_gm, maybe_telemetry_user_topic_env):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device_gm) as proxy:
        aproxy = await AsyncioDeviceProxy(proxy.dev_name())  # emits some spans
        telemetry.ignore_recent_spans()
        _ = await aproxy.lineno_attribute
        client_lineno = inspect.currentframe().f_lineno - 1

    assert_single_client_span_and_device_running_spans_share_trace_id(telemetry)

    client_span = telemetry.client_running_spans[0]
    assert client_span.name == "test_static_attribute_asyncio"
    assert client_span.attributes["code.lineno"] == client_lineno


@pytest.mark.skipif(
    telemetry_unavailable or not user_topics_and_tracing_fixed,
    reason=(skip_message if telemetry_unavailable else "User topics don't work with this cppTango version"),
)
def test_user_topic_spans_have_expected_parent_chain(exporters, maybe_telemetry_user_topic_env, custom_tracer):
    class TestDevice(Device):
        def dev_state(self):
            return DevState.RUNNING

    telemetry = CapturedTelemetry(exporters)
    with (
        custom_tracer.start_as_current_span("custom.span") as custom_span,
        span_recording_device_test_context(telemetry, TestDevice, properties={"telemetry_topics": "user"}) as proxy,
    ):
        proxy.State()

    custom_spans = exporters["custom"].get_finished_spans()
    assert len(custom_spans) == 1
    assert len(telemetry.client_running_spans) == 1
    assert len(telemetry.device_running_spans) == 1

    client_span = telemetry.client_running_spans[0]
    device_span = telemetry.device_running_spans[0]

    assert client_span.parent is not None
    assert device_span.parent is not None
    assert client_span.parent.trace_id == custom_span.get_span_context().trace_id
    assert device_span.parent.trace_id == client_span.context.trace_id
    assert _span_id_hex(client_span.parent.span_id) == _span_id_hex(custom_span.get_span_context().span_id)
    assert _span_id_hex(device_span.parent.span_id) == _span_id_hex(client_span.context.span_id)


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_client_ident_included_for_device(exporters, simple_device_gm):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device_gm) as proxy:
        proxy.State()

    device_span = telemetry.device_running_spans[0]
    assert "collocated" in device_span.attributes["tango.client_ident.location"]
    assert device_span.attributes["tango.client_ident.pid"] == os.getpid()
    assert device_span.attributes["tango.client_ident.lang"].startswith("CPP")


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_custom_span_traceid_propagates_to_tango(exporters, simple_device, custom_tracer):
    telemetry = CapturedTelemetry(exporters)
    with (
        custom_tracer.start_as_current_span("custom.span"),
        span_recording_device_test_context(telemetry, simple_device) as proxy,
    ):
        _ = proxy.State()

    custom_spans = exporters["custom"].get_finished_spans()
    assert len(custom_spans) == 1
    assert len(telemetry.client_running_spans) == 1
    assert len(telemetry.device_running_spans) >= 1

    custom_trace_id = custom_spans[0].context.trace_id
    client_trace_id = telemetry.client_running_spans[0].context.trace_id
    device_trace_id = telemetry.device_running_spans[-1].context.trace_id
    assert client_trace_id == custom_trace_id
    assert device_trace_id == custom_trace_id


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_base_device_spans_require_all_topic(exporters, emit_kernel_spans):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(
        telemetry, Device, properties={"telemetry_topics": "user,database,polling"}
    ):
        pass

    assert len(telemetry.device_startup_spans) == 0
    assert len(telemetry.device_shutdown_spans) == 0


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_base_device_traces_with_all_topic(exporters, simple_device, emit_kernel_spans):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device, properties={"telemetry_topics": "all"}):
        pass

    startup_spans = telemetry.device_startup_spans
    shutdown_spans = telemetry.device_shutdown_spans
    assert len(startup_spans) == 3
    assert startup_spans[0].name == "BaseDevice.init_device"
    assert startup_spans[1].name == "simple_device.<locals>.TestDevice.init_device"
    assert startup_spans[2].name == "BaseDevice.server_init_hook"
    assert len(shutdown_spans) == 2
    assert shutdown_spans[0].name == "BaseDevice.delete_device"
    assert shutdown_spans[1].name == "simple_device.<locals>.TestDevice.delete_device"


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_kernel_spans_are_skipped_by_default(exporters, simple_device):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device, properties={"telemetry_topics": "all"}):
        pass

    startup_span_names = [span.name for span in telemetry.device_startup_spans]
    shutdown_span_names = [span.name for span in telemetry.device_shutdown_spans]
    assert startup_span_names == ["simple_device.<locals>.TestDevice.init_device"]
    assert shutdown_span_names == ["simple_device.<locals>.TestDevice.delete_device"]


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_kernel_spans_can_be_enabled_via_env_var(monkeypatch, exporters, simple_device):
    try:
        monkeypatch.setenv("PYTANGO_TELEMETRY_EMIT_KERNEL_SPANS", "on")
        telemetry_internal, _ = _reload_telemetry_modules()
        _reload_telemetry_runtime_references(monkeypatch)
        _set_in_memory_tracer_provider(exporters)
        assert telemetry_internal._telemetry_runtime._skip_kernel_spans is None

        telemetry = CapturedTelemetry(exporters)
        with span_recording_device_test_context(telemetry, simple_device, properties={"telemetry_topics": "all"}):
            pass

        assert telemetry_internal._telemetry_runtime._skip_kernel_spans is False
        startup_span_names = [span.name for span in telemetry.device_startup_spans]
        shutdown_span_names = [span.name for span in telemetry.device_shutdown_spans]
        assert startup_span_names == [
            "BaseDevice.init_device",
            "simple_device.<locals>.TestDevice.init_device",
            "BaseDevice.server_init_hook",
        ]
        assert shutdown_span_names == [
            "BaseDevice.delete_device",
            "simple_device.<locals>.TestDevice.delete_device",
        ]
    finally:
        monkeypatch.delenv("PYTANGO_TELEMETRY_EMIT_KERNEL_SPANS", raising=False)
        _reload_telemetry_modules()
        _reload_telemetry_runtime_references(monkeypatch)


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_disable_tracing_stops_spans(exporters, simple_device):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device) as proxy:
        _ = proxy.lineno_command()
        telemetry.running_done()
        device_spans = telemetry.device_running_spans
        assert len(device_spans) >= 1
        assert device_spans[-1].name == "simple_device.<locals>.TestDevice.lineno_command"

        proxy.set_telemetry_tracing(False)
        assert not proxy.get_telemetry_tracing()

        _ = proxy.lineno_command()
        telemetry.running_done()
        device_spans = telemetry.device_running_spans
        assert len(device_spans) == 0


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_reenable_tracing_resumes_spans(exporters, simple_device):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device) as proxy:
        telemetry.ignore_recent_spans()
        proxy.set_telemetry_tracing(False)
        _ = proxy.lineno_command()
        telemetry.running_done()
        assert len(telemetry.device_running_spans) == 0

        proxy.set_telemetry_tracing(True)
        assert proxy.get_telemetry_tracing()

        telemetry.ignore_recent_spans()
        _ = proxy.lineno_command()
        telemetry.running_done()
        device_spans = telemetry.device_running_spans
        assert len(device_spans) >= 1
        assert device_spans[-1].name == "simple_device.<locals>.TestDevice.lineno_command"


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_topics_filter_spans(exporters, simple_device, green_mode_device_proxy, emit_kernel_spans):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device, properties={"telemetry_topics": "all"}) as proxy:
        gm_proxy = green_mode_device_proxy(proxy.dev_name())
        telemetry.ignore_recent_spans()
        gm_proxy.set_telemetry_topics(["user"], wait=True)
        gm_proxy.command_inout("Init", wait=True)
        telemetry.running_done()
        user_topics_spans = telemetry.device_running_spans
        if user_topics_and_tracing_fixed:
            assert user_topics_spans
        assert not any(span.name.startswith("BaseDevice.") for span in user_topics_spans)

        telemetry.ignore_recent_spans()
        gm_proxy.set_telemetry_topics(["all"], wait=True)
        gm_proxy.command_inout("Init", wait=True)
        telemetry.running_done()
        all_topics_spans = telemetry.device_running_spans
        assert any(span.name.startswith("BaseDevice.") for span in all_topics_spans)
        assert any(span.name == "simple_device.<locals>.TestDevice.init_device" for span in all_topics_spans)


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_no_device_traces_if_device_tracing_disabled(exporters, simple_device):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(
        telemetry,
        simple_device,
        properties={"telemetry_enable": "0"},
    ) as proxy:
        _ = proxy.lineno_attribute

    assert len(telemetry.device_startup_spans) == 0
    assert len(telemetry.device_running_spans) == 0
    assert len(telemetry.device_shutdown_spans) == 0


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_device_tracing_can_be_enabled_if_env_initially_disabled(exporters, simple_device, monkeypatch):
    monkeypatch.setenv("TANGO_TELEMETRY_ENABLE", "off")

    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device, properties={"telemetry_enable": "0"}) as proxy:
        proxy.start_telemetry()
        _ = proxy.State()

    assert len(telemetry.device_startup_spans) == 0
    assert len(telemetry.device_running_spans) >= 1
    assert len(telemetry.device_shutdown_spans) >= 1


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_client_tracing_disabled_when_telemetry_types_logging(exporters, simple_device, monkeypatch):
    monkeypatch.setenv("TANGO_TELEMETRY_TYPES", "logging")

    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device) as proxy:
        proxy.command_inout("State")

    assert len(telemetry.client_running_spans) == 0
    assert len(telemetry.device_running_spans) == 0


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_client_context_propagates_when_client_tracing_disabled(exporters, monkeypatch, custom_tracer):
    monkeypatch.setenv("TANGO_TELEMETRY_TYPES", "none")  # i.e., tracing disabled

    class TestDevice(Device):
        @command(dtype_out=str)
        def current_traceparent(self):
            return tango._tango._telemetry.get_trace_context()["traceparent"]

    telemetry = CapturedTelemetry(exporters)
    with (
        custom_tracer.start_as_current_span("custom.span") as custom_span,
        span_recording_device_test_context(telemetry, TestDevice) as proxy,
    ):
        proxy.set_telemetry_tracing(True)
        telemetry.ignore_recent_spans()
        traceparent = proxy.command_inout("current_traceparent")

    assert len(telemetry.client_running_spans) == 0
    assert _trace_id_from_traceparent(traceparent) == format(custom_span.get_span_context().trace_id, "032x")


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_client_tracing_disabled_when_telemetry_types_none(exporters, simple_device, monkeypatch):
    monkeypatch.setenv("TANGO_TELEMETRY_TYPES", "none")

    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device) as proxy:
        proxy.command_inout("State")

    assert len(telemetry.client_running_spans) == 0
    assert len(telemetry.device_running_spans) == 0


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_client_tracing_enabled_when_telemetry_types_tracing(exporters, simple_device, monkeypatch):
    monkeypatch.setenv("TANGO_TELEMETRY_TYPES", "tracing")

    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device) as proxy:
        proxy.command_inout("State")

    assert_single_client_span_and_device_running_spans_share_trace_id(telemetry)


@pytest.fixture
def dual_traceparent_devices_info():
    class DownstreamDevice(Device):
        @command(dtype_out=str)
        def current_traceparent(self):
            return tango._tango._telemetry.get_trace_context()["traceparent"]

    class UpstreamDevice(Device):
        @command(dtype_out=str)
        def relay_traceparent(self):
            proxy = DeviceProxy("test/downstream/1")
            return proxy.command_inout("current_traceparent")

    return (
        {
            "class": DownstreamDevice,
            "devices": [{"name": "test/downstream/1", "properties": {"telemetry_enable": "1"}}],
        },
        {
            "class": UpstreamDevice,
            "devices": [{"name": "test/upstream/1", "properties": {"telemetry_enable": "1"}}],
        },
    )


@pytest.mark.skipif(
    telemetry_unavailable or not user_topics_and_tracing_fixed,
    reason=(
        skip_message
        if telemetry_unavailable
        else "Propagation with tracing disabled doesn't work with this cppTango version"
    ),
)
def test_server_context_propagates_when_server_tracing_is_disabled(dual_traceparent_devices_info, custom_tracer):
    with MultiDeviceTestContext(dual_traceparent_devices_info) as context:
        upstream = context.get_device("test/upstream/1")
        upstream.set_telemetry_tracing(False)

        with custom_tracer.start_as_current_span("custom.span") as custom_span:
            traceparent = upstream.command_inout("relay_traceparent")

    assert _trace_id_from_traceparent(traceparent) == format(custom_span.get_span_context().trace_id, "032x")


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_server_context_propagates_to_nested_client_call_with_no_tracing_endpoints(
    dual_traceparent_devices_info, custom_tracer
):
    with MultiDeviceTestContext(dual_traceparent_devices_info) as context:
        upstream = context.get_device("test/upstream/1")
        upstream.set_telemetry_tracing_endpoints([])

        with custom_tracer.start_as_current_span("custom.span") as custom_span:
            traceparent = upstream.command_inout("relay_traceparent")

    assert _trace_id_from_traceparent(traceparent) == format(custom_span.get_span_context().trace_id, "032x")


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_server_context_propagates_to_nested_client_call_when_python_server_span_is_suppressed(
    dual_traceparent_devices_info, custom_tracer
):
    with MultiDeviceTestContext(dual_traceparent_devices_info) as context:
        upstream = context.get_device("test/upstream/1")
        upstream.set_telemetry_topics(["database"])

        with custom_tracer.start_as_current_span("custom.span") as custom_span:
            traceparent = upstream.command_inout("relay_traceparent")

    assert _trace_id_from_traceparent(traceparent) == format(custom_span.get_span_context().trace_id, "032x")


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_repeated_enable_disable_enable_cycles_refresh_provider(exporters, simple_device):
    provider_ids = []

    class TestDevice(simple_device):
        def create_telemetry_tracer_provider(self, class_name, device_name):
            provider = super().create_telemetry_tracer_provider(class_name, device_name)
            provider_ids.append(id(provider))
            return provider

    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, TestDevice) as proxy:
        for _ in range(2):
            proxy.set_telemetry_tracing(False)
            proxy.set_telemetry_tracing(True)
    assert len(provider_ids) >= 3
    unique_providers = set(provider_ids[-3:])
    assert len(unique_providers) == 3


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_enable_telemetry_at_runtime(exporters, simple_device, green_mode_device_proxy):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(
        telemetry,
        simple_device,
        properties={"telemetry_enable": "0"},
    ) as proxy:
        gm_proxy = green_mode_device_proxy(proxy.dev_name())
        assert not gm_proxy.is_telemetry_enabled(wait=True)

        _ = gm_proxy.lineno_command(wait=True)
        telemetry.running_done()
        assert len(telemetry.device_running_spans) == 0

        gm_proxy.start_telemetry(wait=True)
        assert gm_proxy.is_telemetry_enabled(wait=True)

        telemetry.ignore_recent_spans()
        device_lineno = gm_proxy.lineno_command(wait=True)
        telemetry.running_done()
        device_spans = telemetry.device_running_spans
        assert len(device_spans) >= 1
        assert device_spans[-1].attributes["code.lineno"] == device_lineno


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_disable_telemetry_at_runtime(exporters, simple_device):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device, properties={"telemetry_enable": "1"}) as proxy:
        assert proxy.is_telemetry_enabled()
        telemetry.ignore_recent_spans()

        _ = proxy.lineno_command()
        telemetry.running_done()
        device_spans = telemetry.device_running_spans
        assert len(device_spans) >= 1
        assert device_spans[-1].name == "simple_device.<locals>.TestDevice.lineno_command"

        telemetry.ignore_recent_spans()
        proxy.stop_telemetry()
        assert not proxy.is_telemetry_enabled()

        _ = proxy.lineno_command()
        telemetry.running_done()
        assert len(telemetry.device_running_spans) == 0


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_endpoint_change_recreates_provider(simple_device, green_mode_device_proxy):
    factory_endpoint_configs = []
    cout = TelemetryEndpoint(TelemetryExporter.CONSOLE, "cout")
    cerr = TelemetryEndpoint(TelemetryExporter.CONSOLE, "cerr")

    old_factory = get_telemetry_tracer_provider_factory()

    def recording_factory(
        service_name,
        service_instance_id=None,
        extra_resource_attributes=None,
        endpoints=None,
    ):
        factory_endpoint_configs.append(tuple(endpoints or ()))
        return old_factory(
            service_name,
            service_instance_id,
            extra_resource_attributes,
            endpoints=endpoints,
        )

    set_telemetry_tracer_provider_factory(recording_factory)
    try:
        with DeviceTestContext(simple_device, properties={"telemetry_enable": "1"}) as proxy:
            gm_proxy = green_mode_device_proxy(proxy.dev_name())
            gm_proxy.set_telemetry_tracing_endpoints([cout], wait=True)
            gm_proxy.set_telemetry_tracing_endpoints([cerr], wait=True)
            gm_proxy.set_telemetry_tracing_endpoints([], wait=True)
            gm_proxy.set_telemetry_tracing_endpoints([cout, cerr], wait=True)
    finally:
        set_telemetry_tracer_provider_factory(old_factory)

    assert factory_endpoint_configs[-4:] == [(cout,), (cerr,), (), (cout, cerr)]


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_toggle_telemetry_logging_flag(simple_device, green_mode_device_proxy):
    with DeviceTestContext(simple_device, properties={"telemetry_enable": "1"}) as proxy:
        gm_proxy = green_mode_device_proxy(proxy.dev_name())
        gm_proxy.set_telemetry_logging(True, wait=True)
        assert gm_proxy.get_telemetry_logging(wait=True)
        gm_proxy.set_telemetry_logging(False, wait=True)
        assert not gm_proxy.get_telemetry_logging(wait=True)
        gm_proxy.set_telemetry_logging(True, wait=True)
        assert gm_proxy.get_telemetry_logging(wait=True)


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_toggle_telemetry_tracing_flag(simple_device, green_mode_device_proxy):
    with DeviceTestContext(simple_device, properties={"telemetry_enable": "1"}) as proxy:
        gm_proxy = green_mode_device_proxy(proxy.dev_name())
        gm_proxy.set_telemetry_tracing(True, wait=True)
        assert gm_proxy.get_telemetry_tracing(wait=True)
        gm_proxy.set_telemetry_tracing(False, wait=True)
        assert not gm_proxy.get_telemetry_tracing(wait=True)
        gm_proxy.set_telemetry_tracing(True, wait=True)
        assert gm_proxy.get_telemetry_tracing(wait=True)


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_get_and_set_telemetry_logging_endpoints(simple_device, green_mode_device_proxy):
    cout = TelemetryEndpoint(TelemetryExporter.CONSOLE, "cout")
    cerr = TelemetryEndpoint(TelemetryExporter.CONSOLE, "cerr")

    with DeviceTestContext(simple_device, properties={"telemetry_enable": "1"}) as proxy:
        gm_proxy = green_mode_device_proxy(proxy.dev_name())
        gm_proxy.set_telemetry_logging_endpoints([cout], wait=True)
        assert gm_proxy.get_telemetry_logging_endpoints(wait=True) == (cout,)
        gm_proxy.add_telemetry_logging_endpoint(cerr, wait=True)
        assert gm_proxy.get_telemetry_logging_endpoints(wait=True) == (cout, cerr)
        gm_proxy.remove_telemetry_logging_endpoint(cout, wait=True)
        assert gm_proxy.get_telemetry_logging_endpoints(wait=True) == (cerr,)


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_get_and_set_telemetry_tracing_endpoints(simple_device, green_mode_device_proxy):
    cout = TelemetryEndpoint(TelemetryExporter.CONSOLE, "cout")
    cerr = TelemetryEndpoint(TelemetryExporter.CONSOLE, "cerr")

    with DeviceTestContext(simple_device, properties={"telemetry_enable": "1"}) as proxy:
        gm_proxy = green_mode_device_proxy(proxy.dev_name())
        gm_proxy.set_telemetry_tracing_endpoints([cout], wait=True)
        assert gm_proxy.get_telemetry_tracing_endpoints(wait=True) == (cout,)
        gm_proxy.add_telemetry_tracing_endpoint(cerr, wait=True)
        assert gm_proxy.get_telemetry_tracing_endpoints(wait=True) == (cout, cerr)
        gm_proxy.remove_telemetry_tracing_endpoint(cout, wait=True)
        assert gm_proxy.get_telemetry_tracing_endpoints(wait=True) == (cerr,)


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_telemetry_topics_are_normalized_and_checked_via_device_impl():
    class TestDevice(Device):
        @command(dtype_in=str, dtype_out=bool)
        def has_topic(self, topic):
            return self._check_telemetry_topic(topic)

    with DeviceTestContext(TestDevice, properties={"telemetry_enable": "1"}) as proxy:
        proxy.set_telemetry_topics([" USER ", " Polling "])
        topics = proxy.get_telemetry_topics()
        assert isinstance(topics, tuple)
        assert set(topics) == {"user", "polling"}
        assert proxy.has_topic("user")
        assert proxy.has_topic("polling")
        assert not proxy.has_topic("database")


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_invalid_telemetry_topics_raise():
    with DeviceTestContext(Device, properties={"telemetry_enable": "1"}) as proxy, pytest.raises(DevFailed):
        proxy.set_telemetry_topics(["INVALID"])


@pytest.mark.skipif(telemetry_unavailable, reason=skip_message)
def test_device_impl_tracing_endpoint_hooks_receive_typed_endpoints():
    expected = TelemetryEndpoint(TelemetryExporter.CONSOLE, "cout")
    added = TelemetryEndpoint(TelemetryExporter.CONSOLE, "cerr")
    call_count = 0

    class TestDevice(Device):
        def _telemetry_reconfigured(self):
            nonlocal call_count
            call_count += 1

    with DeviceTestContext(TestDevice, properties={"telemetry_enable": "1"}) as proxy:
        proxy.set_telemetry_tracing_endpoints([expected])
        proxy.add_telemetry_tracing_endpoint(added)
        proxy.remove_telemetry_tracing_endpoint(expected)

    assert call_count == 3
