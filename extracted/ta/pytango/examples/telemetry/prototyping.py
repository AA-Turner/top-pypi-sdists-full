# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

import threading
import time

from tango import (
    AttrWriteType,
    AttributeProxy,
    Database,
    DeviceProxy,
    EnsureOmniThread,
    EventType,
    InfoIt,
    Group,
)
from tango.test_context import MultiDeviceTestContext
from tango.server import Device, attribute, command, device_property
from tango.utils import EventCallback

# <<<<<< If user wants to trace their own things -------
# Dependencies:
# pip or conda install the following libraries:
#   opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc

# API
from opentelemetry import trace as trace_api

# SDK
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import (
    SERVICE_NAME,
    SERVICE_NAMESPACE,
    Resource,
)
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource.create({SERVICE_NAMESPACE: "org.institute", SERVICE_NAME: "my.app"})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace_api.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace_api.get_tracer("user.tracer")
# ---- end of user's own tracing. >>>>>>

# import to pass context to a user thread:
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


class Leader(Device):
    FollowerTRLs = device_property(dtype=(str,))

    @command(dtype_in=int)
    @InfoIt(show_args=True)
    def TurnFollowerOn(self, follower_id):
        self.debug_stream(f"Turning follower {follower_id} on...")
        follower_trl = self.FollowerTRLs[follower_id - 1]
        follower_device = DeviceProxy(follower_trl)
        follower_device.isOn = True

    @command(dtype_in=int)
    def TurnFollowerOff(self, follower_id):
        device_tracer = self.get_telemetry_tracer()
        with device_tracer.start_as_current_span("test.leader.span") as span:
            span.set_attribute("follower_id", follower_id)
            follower_trl = self.FollowerTRLs[follower_id - 1]
            follower_device = DeviceProxy(follower_trl)
            follower_device.isOn = False

    @command(dtype_in=bool, dtype_out=bool)
    def SetDeviceTracing(self, enable):
        self.set_telemetry_enabled(enable)
        return self.is_telemetry_enabled()

    @command(dtype_in=bool, dtype_out=bool)
    def SetKernelTracing(self, enable):
        self.set_kernel_tracing_enabled(enable)
        return self.is_kernel_tracing_enabled()

    @command(dtype_in=int)
    @InfoIt(show_args=True)
    def PollFollowerOnOff(self, follower_id):
        follower_trl = self.FollowerTRLs[follower_id - 1]
        follower_device = DeviceProxy(follower_trl)
        user_test_polling_and_events(follower_device)


class Follower(Device):
    def init_device(self):
        super().init_device()
        self._is_on = False

        attr = attribute(
            name="dynamicAttribute",
            access=AttrWriteType.READ,
            fget=self.read_dyn_attr,
        )
        self.add_attribute(attr)
        cmd = command(
            dtype_in=int,
            f=self.DynamicCommand,
        )
        self.add_command(cmd)

    isOn = attribute(access=AttrWriteType.READ_WRITE)

    @InfoIt(show_ret=True)
    def read_isOn(self) -> bool:
        return self._is_on

    @InfoIt(show_args=True)
    def write_isOn(self, value: bool) -> None:
        self._is_on = value

    def read_dyn_attr(self, arg) -> int:
        print(f"Follower.dynamicAttribute")
        return 123

    def DynamicCommand(self, arg):
        print(f"Follower.DynamicCommand({arg})")

    def delete_device(self):
        # just to show trace emitted for user code
        pass

    def dev_state(self):
        # just to show trace emitted for user code
        return super().dev_state()


devices_info = [
    {
        "class": Leader,
        "devices": (
            {
                "name": "device/leader/1",
                "properties": {
                    "FollowerTRLs": ["device/follower/1", "device/follower/2"],
                },
            },
        ),
    },
    {
        "class": Follower,
        "devices": [
            {"name": "device/follower/1", "properties": {}},
            {"name": "device/follower/2", "properties": {}},
        ],
    },
]


def call_from_thread_with_context(follower: DeviceProxy):
    carrier = {}
    TraceContextTextMapPropagator().inject(carrier)
    print(f"call_from_thread_with_context {carrier=}")
    thread = threading.Thread(target=thread_worker, args=(carrier, follower))
    thread.start()
    time.sleep(0.001)


def thread_worker(carrier, follower):
    with EnsureOmniThread():
        print(f"worker started for: {follower}")
        ctx = TraceContextTextMapPropagator().extract(carrier=carrier)
        with tracer.start_as_current_span("thread.worker.call", context=ctx):
            user_turn_follower_off_directly(follower)


def user_turn_follower_off_directly(follower: DeviceProxy):
    print(f"user_turn_follower_off_directly: {follower}")
    follower.isOn = False


def user_test_polling_and_events(follower: DeviceProxy):
    print(f"user_toggle_polling {follower.is_attribute_polled('isOn')=}")
    follower.poll_attribute("isOn", 10)
    print(f"user_toggle_polling {follower.is_attribute_polled('isOn')=}")
    user_test_events(follower)
    follower.stop_poll_attribute("isOn")
    print(f"user_toggle_polling {follower.is_attribute_polled('isOn')=}")


def user_test_events(follower: DeviceProxy):
    eid = follower.subscribe_event("isOn", EventType.CHANGE_EVENT, EventCallback())
    follower.isOn = False
    time.sleep(0.01)
    follower.isOn = True
    time.sleep(0.01)
    follower.unsubscribe_event(eid)


def main():
    with MultiDeviceTestContext(devices_info, process=False, timeout=600, debug=3):
        leader = DeviceProxy("device/leader/1")
        follower_1 = DeviceProxy("device/follower/1")
        follower_2 = DeviceProxy("device/follower/2")
        # user could create their own span, e.g.:
        with tracer.start_as_current_span(
            "my.app.main", kind=trace_api.SpanKind.CLIENT
        ):
            for loop in range(2):
                with tracer.start_as_current_span(
                    "my.app.main.inner-loop", kind=trace_api.SpanKind.CLIENT
                ) as span:
                    span.set_attribute("operation.value", loop)

                    # tell leader to enable both followers
                    leader.command_inout("TurnFollowerOn", 1)
                    leader.command_inout("TurnFollowerOn", 2)

                    # check initial state: both followers are on
                    _ = follower_1.read_attribute("isOn").value
                    _ = follower_2.isOn

                    # turn off, using low-level and high-level API
                    follower_1.write_attribute("isOn", 0)
                    user_turn_follower_off_directly(follower_2)

                    call_from_thread_with_context(follower_2)

                    leader.TurnFollowerOff(1)  # FIXME

                    with tracer.start_as_current_span(
                        "test.deviceproxy.other", kind=trace_api.SpanKind.CLIENT
                    ):
                        # read multiple attributes, and check config
                        _ = follower_2.read_attributes(["isOn", "state"])
                        _ = follower_1.get_attribute_config("isOn")
                        _ = follower_1.read_attribute("dynamicAttribute")
                        _ = follower_1.command_inout("DynamicCommand", 22)

                    with tracer.start_as_current_span(
                        "test.polling-and-events", kind=trace_api.SpanKind.CLIENT
                    ):
                        leader.PollFollowerOnOff(1)
                        # polling changes not within device context aren't traced yet
                        follower_1.poll_attribute("isOn", 1000)
                        follower_1.stop_poll_attribute("isOn")

                    with tracer.start_as_current_span(
                        "test.attributeproxy", kind=trace_api.SpanKind.CLIENT
                    ):
                        follower_1_is_on = AttributeProxy("device/follower/1/isOn")
                        _ = follower_1_is_on.ping()
                        reading = follower_1_is_on.read()
                        print(f"AttributeProxy reading: {reading.value}")

                    with tracer.start_as_current_span(
                        "test.group", kind=trace_api.SpanKind.CLIENT
                    ):
                        group = Group("add-one-at-a-time")
                        group.add("device/follower/1")
                        group.add("device/follower/2")
                        group.ping()
                        reply = group.read_attribute("isOn")
                        print(
                            f"Group reading: 1:{reply[0].get_data().value}, 2:{reply[1].get_data().value}"
                        )

                    with tracer.start_as_current_span(
                        "test.database", kind=trace_api.SpanKind.CLIENT
                    ):
                        db = Database()
                        _ = db.get_server_list()
                        _ = db.put_device_property("sys/tg_test/1", {"foo": "bar"})
                        prop_val = db.get_device_property("sys/tg_test/1", "foo")
                        print(f"got property foo: {prop_val}")
                        _ = db.delete_device_property("sys/tg_test/1", "foo")


if __name__ == "__main__":
    main()

    # instead of running main, can run as Tango server providing the two classes:
    # tango.server.run([Leader, Follower])

"""
Examples:

*** Change code above to use main() instead of tango.server.run(...)

# Run example with telemetry on, traces go to stdout
$ TANGO_TELEMETRY_ENABLE=on python prototyping.py

# Run example with telemetry on, traces to to local collector via gRPC
$ TANGO_TELEMETRY_ENABLE=on TANGO_TELEMETRY_TRACES_EXPORTER=grpc python

*** Change code above to use tango.server.run(...) instead of main()

# Python client with telemetry on, traces go to stdout
#  (create your own DeviceProxy)
$ TANGO_TELEMETRY_ENABLE=on python

# Python client with telemetry on, traces to to local collector via gRPC
# (create your own DeviceProxy)
$ TANGO_TELEMETRY_ENABLE=on TANGO_TELEMETRY_TRACES_EXPORTER=grpc python

# Run Leader device server, telemetry disabled
$ python prototyping.py Leader --host=127.0.0.1 -v3

# Run Leader device server, telemetry on, traces and logs to local collector via gRPC
$ TANGO_TELEMETRY_ENABLE=on TANGO_TELEMETRY_TRACES_EXPORTER=grpc TANGO_TELEMETRY_LOGS_EXPORTER=grpc python prototyping.py Leader --host=127.0.0.1 -v3

# Run Follower device server, telemetry on, traces and logs to local collector via gRPC
# Also include additional process info in the traces using experimental OpenTelemetry
# resource detector.
$ TANGO_TELEMETRY_ENABLE=on TANGO_TELEMETRY_TRACES_EXPORTER=grpc TANGO_TELEMETRY_LOGS_EXPORTER=grpc OTEL_EXPERIMENTAL_RESOURCE_DETECTORS=process python prototyping.py Follower --host=127.0.0.1 -v3

"""
