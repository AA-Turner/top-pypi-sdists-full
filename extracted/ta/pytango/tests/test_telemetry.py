# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

import contextlib
import inspect
import os
import typing
from collections import defaultdict

try:
    from opentelemetry import trace as trace_api
    from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )
    from opentelemetry.sdk.resources import (
        SERVICE_INSTANCE_ID,
        SERVICE_NAME,
        Resource,
    )

    opentelemetry_packages_available = True
except ImportError:
    opentelemetry_packages_available = False

import pytest

from tango import DevState, DeviceProxy, GreenMode, constants
from tango.asyncio import DeviceProxy as AsyncioDeviceProxy
from tango.server import Device, attribute, command
from tango.utils import (
    _telemetry_active,
    get_telemetry_tracer_provider_factory,
    set_telemetry_tracer_provider_factory,
)
from tango.test_utils import DeviceTestContext


@pytest.fixture()
def exporters():
    """Switch to in-memory exporters for Python telemetry"""
    in_mem_exporters: dict[str, InMemorySpanExporter] = {}

    def in_memory_tracer_provider(
        service_name,
        service_instance_id=None,
        extra_resource_attributes=None,
    ):
        resource_attributes = {SERVICE_NAME: service_name}
        if service_instance_id:
            resource_attributes[SERVICE_INSTANCE_ID] = service_instance_id
        tracer_provider = TracerProvider(resource=Resource.create(resource_attributes))
        exporter = InMemorySpanExporter()
        in_mem_exporters[service_name] = exporter
        processor = SimpleSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)
        return tracer_provider

    old_factory = get_telemetry_tracer_provider_factory()
    set_telemetry_tracer_provider_factory(in_memory_tracer_provider)
    yield in_mem_exporters
    set_telemetry_tracer_provider_factory(old_factory)


class CapturedTelemetry:
    def __init__(self, exporters):
        self._exporters = exporters
        self._device_class_name = ""
        self._client_spans: dict[str, list["ReadableSpan"]] = defaultdict(list)
        self._device_spans: dict[str, list["ReadableSpan"]] = defaultdict(list)

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
            print(f"No client for spans. {self._exporters=}")
        device = self._exporters.get(self._device_class_name)
        if device:
            device_spans = device.get_finished_spans()
            device.clear()
        else:
            device_spans = []
            print("No device for spans")
        self._client_spans[stage] = client_spans
        self._device_spans[stage] = device_spans


def print_json(spans):
    """Utility that is useful when debugging tests"""
    print(f"===== Printing {len(spans)} spans... ========")
    for span in spans:
        print(span.to_json())
        print("-----------------------")
    print(f"===== Done printing {len(spans)} spans ========")


@pytest.fixture()
def simple_device(server_green_mode):
    # Note: Telemetry spans are not emitted for BaseDevice methods by default,
    # so we override init_device, delete_device and dev_state in our test device.
    # This lets us verify that user methods will generate spans.

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
            green_mode = server_green_mode

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
    telemetry: CapturedTelemetry, device_class: typing.Type[Device], **kwargs
) -> typing.Generator[DeviceProxy, None, None]:
    """Context manager that records the telemetry spans around DeviceTestContext.

    This lets us capture the spans created at various stages:
      - on device startup
      - while the device is running (if test function accesses device via proxy)
      - on device shutdown
    """
    telemetry.set_device_class_name(device_class.__name__)
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


def test_telemetry_available_constant_exists():
    assert isinstance(constants.TELEMETRY_SUPPORTED, bool)


@pytest.mark.skipif(not _telemetry_active, reason="Telemetry not active")
def test_telemetry_packages_available_if_telemetry_active():
    assert opentelemetry_packages_available


@pytest.mark.skipif(not _telemetry_active, reason="Telemetry not active")
def test_init_device_and_basic_span_details(exporters, simple_device):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device):
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

    device_span = telemetry.device_startup_spans[0]
    assert device_span.name == "simple_device.<locals>.TestDevice.init_device"
    assert device_span.resource.attributes[SERVICE_NAME] == "TestDevice"
    assert (
        device_span.resource.attributes[SERVICE_INSTANCE_ID] == "test/nodb/testdevice"
    )
    assert device_span.attributes["code.filepath"] == __file__
    assert "code.lineno" in device_span.attributes
    assert "thread.id" in device_span.attributes
    assert "thread.name" in device_span.attributes


@pytest.mark.skipif(not _telemetry_active, reason="Telemetry not active")
def test_delete_device(exporters, simple_device):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device):
        pass

    assert len(telemetry.client_shutdown_spans) == 1
    assert len(telemetry.device_shutdown_spans) == 1

    client_span = telemetry.client_shutdown_spans[0]
    assert client_span.name == "span_recording_device_test_context"

    device_span = telemetry.device_shutdown_spans[0]
    assert device_span.name == "simple_device.<locals>.TestDevice.delete_device"


@pytest.mark.skipif(not _telemetry_active, reason="Telemetry not active")
def test_state(exporters, simple_device):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device) as proxy:
        proxy.State()
        state_lineno = inspect.currentframe().f_lineno - 1

    assert_single_client_and_device_running_span_and_share_trace_id(telemetry)

    client_span = telemetry.client_running_spans[0]
    assert client_span.name == "test_state"
    assert client_span.attributes["code.lineno"] == state_lineno

    device_span = telemetry.device_running_spans[0]
    assert device_span.name == "simple_device.<locals>.TestDevice.dev_state"


@pytest.mark.skipif(not _telemetry_active, reason="Telemetry not active")
def test_static_command(exporters, simple_device):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device) as proxy:
        device_lineno = proxy.lineno_command()
        client_lineno = inspect.currentframe().f_lineno - 1

    assert_single_client_and_device_running_span_and_share_trace_id(telemetry)

    client_span = telemetry.client_running_spans[0]
    assert client_span.name == "test_static_command"
    assert client_span.attributes["code.lineno"] == client_lineno

    device_span = telemetry.device_running_spans[0]
    assert device_span.name == "simple_device.<locals>.TestDevice.lineno_command"
    assert device_span.attributes["code.lineno"] == device_lineno


@pytest.mark.skipif(not _telemetry_active, reason="Telemetry not active")
def test_static_attribute(exporters, simple_device, green_mode_device_proxy):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device) as proxy:
        gm_proxy = green_mode_device_proxy(proxy.dev_name())  # emits some spans
        telemetry.ignore_recent_spans()
        device_lineno = gm_proxy.read_attribute("lineno_attribute", wait=True).value
        client_lineno = inspect.currentframe().f_lineno - 1

    assert_single_client_and_device_running_span_and_share_trace_id(telemetry)

    client_span = telemetry.client_running_spans[0]
    assert client_span.name == "test_static_attribute"
    assert client_span.attributes["code.lineno"] == client_lineno

    device_span = telemetry.device_running_spans[0]
    assert device_span.name == "simple_device.<locals>.TestDevice.lineno_attribute"
    assert device_span.attributes["code.lineno"] == device_lineno


def assert_single_client_and_device_running_span_and_share_trace_id(telemetry):
    assert len(telemetry.client_running_spans) == 1
    assert len(telemetry.device_running_spans) == 1

    client_id = telemetry.client_running_spans[0].context.trace_id
    device_id = telemetry.device_running_spans[0].context.trace_id
    assert client_id == device_id


@pytest.mark.skipif(not _telemetry_active, reason="Telemetry not active")
@pytest.mark.asyncio
async def test_static_attribute_asyncio(exporters, simple_device):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device) as proxy:
        aproxy = await AsyncioDeviceProxy(proxy.dev_name())  # emits some spans
        telemetry.ignore_recent_spans()
        _ = await aproxy.lineno_attribute
        client_lineno = inspect.currentframe().f_lineno - 1

    assert_single_client_and_device_running_span_and_share_trace_id(telemetry)

    client_span = telemetry.client_running_spans[0]
    assert client_span.name == "test_static_attribute_asyncio"
    assert client_span.attributes["code.lineno"] == client_lineno


@pytest.mark.skipif(not _telemetry_active, reason="Telemetry not active")
def test_client_ident_included_for_device(exporters, simple_device):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, simple_device) as proxy:
        proxy.State()

    device_span = telemetry.device_running_spans[0]
    assert "collocated" in device_span.attributes["tango.client_ident.location"]
    assert device_span.attributes["tango.client_ident.pid"] == os.getpid()
    assert device_span.attributes["tango.client_ident.lang"].startswith("CPP")


@pytest.mark.skipif(not _telemetry_active, reason="Telemetry not active")
def test_user_span_traceid_propagates_to_tango(
    exporters, simple_device, green_mode_device_proxy
):
    factory = get_telemetry_tracer_provider_factory()
    user_provider = factory("user")
    user_tracer = trace_api.get_tracer("user.tracer", tracer_provider=user_provider)

    telemetry = CapturedTelemetry(exporters)
    with user_tracer.start_as_current_span("user.span"):
        with span_recording_device_test_context(telemetry, simple_device) as proxy:
            gm_proxy = green_mode_device_proxy(proxy.dev_name())  # emits some spans
            telemetry.ignore_recent_spans()
            _ = gm_proxy.command_inout("State", wait=True)

    user_spans = exporters["user"].get_finished_spans()
    assert len(user_spans) == 1
    assert len(telemetry.client_running_spans) == 1
    assert len(telemetry.device_running_spans) == 1

    user_trace_id = user_spans[0].context.trace_id
    client_trace_id = telemetry.client_running_spans[0].context.trace_id
    device_trace_id = telemetry.device_running_spans[0].context.trace_id
    assert client_trace_id == user_trace_id
    assert device_trace_id == user_trace_id


@pytest.mark.skipif(not _telemetry_active, reason="Telemetry not active")
def test_base_device_kernel_tracing_disabled_by_default(exporters):
    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, Device):
        pass

    assert len(telemetry.device_startup_spans) == 0
    assert len(telemetry.device_shutdown_spans) == 0


@pytest.mark.skipif(not _telemetry_active, reason="Telemetry not active")
def test_base_device_traces_if_kernel_tracing_enabled(exporters, simple_device):
    class TestDevice(simple_device):
        def create_telemetry_tracer_provider(self, *args, **kwargs):
            # we override create_telemetry_tracer_provider because it gets called
            # just before init_device
            self.set_kernel_tracing_enabled(True)
            return super().create_telemetry_tracer_provider(*args, **kwargs)

    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, TestDevice):
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


@pytest.mark.skipif(not _telemetry_active, reason="Telemetry not active")
def test_no_device_traces_if_device_tracing_disabled(exporters, simple_device):
    class TestDevice(simple_device):
        def create_telemetry_tracer_provider(self, *args, **kwargs):
            # we override create_telemetry_tracer_provider because it gets called
            # just before init_device
            self.set_telemetry_enabled(False)
            return super().create_telemetry_tracer_provider(*args, **kwargs)

    telemetry = CapturedTelemetry(exporters)
    with span_recording_device_test_context(telemetry, TestDevice) as proxy:
        _ = proxy.lineno_attribute

    assert len(telemetry.device_startup_spans) == 0
    assert len(telemetry.device_running_spans) == 0
    assert len(telemetry.device_shutdown_spans) == 0
