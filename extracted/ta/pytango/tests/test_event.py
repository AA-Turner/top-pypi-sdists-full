# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
# Imports

import gc
import inspect
import multiprocessing
import os
import sys
import time
from dataclasses import dataclass
from io import StringIO
from threading import Event, Thread

import pytest

from tango import (
    ApiUtil,
    AttrQuality,
    DevEncoded,
    DevFailed,
    DeviceProxy,
    EnsureOmniThread,
    EventData,
    EventReason,
    EventSubMode,
    EventType,
    Except,
    ExtractAs,
    GreenMode,
    PyTangoUserWarning,
    cb_sub_model,
    get_device_proxy,
    is_omni_thread,
)
from tango._internal import warn
from tango.server import Device, attribute, command
from tango.test_utils import DeviceTestContext, assert_close
from tango.utils import EventCallback

MAX_RETRIES = 100
DELAY_PER_RETRY = 0.05
ZMQ_READY_ATTRIBUTE_POLLING_PERIOD = 0.05


async def async_callback(evt, results):
    event_callback(evt, results)


def event_callback(evt, results):
    if evt.err:
        assert evt.attr_value is None
        results.append(evt.errors[0].desc)
    elif hasattr(evt, "ctr"):
        results.append(evt.ctr)
    elif hasattr(evt, "attr_value"):
        results.append(evt.attr_value.value)
    else:
        results.append(evt)


# Test device
class EventDevice(Device):
    _requested_event_type = None
    _base = 0
    _slow_attr_last_read_time = 0.0

    def init_device(self):
        self.set_change_event("attr", implemented=True, detect=False)
        # even if set_alarm_event is not necessary after we did set_change_event,
        # we call it to test that function works
        self.set_alarm_event("attr", implemented=True, detect=False)
        self.set_data_ready_event("attr", implemented=True)
        self.set_archive_event("attr", implemented=True, detect=False)

        self.set_change_event("dev_encoded_attr", implemented=True, detect=False)

    @attribute(polling_period=1000)
    def attr_no_events(self):
        return 1

    @attribute()
    def attr(self) -> int:
        # to avoid sending events at subscription
        if self._requested_event_type is not None:
            self._base += 10
            self._send_events("attr", self._requested_event_type)
        return 0

    @attr.write
    def attr(self, event_type):
        self._base += 10
        self._requested_event_type = event_type
        self._send_events("attr", event_type)

    @attribute(dtype=DevEncoded)
    def dev_encoded_attr(self):
        return "a", "b"

    @attribute(change_event_implemented=True, change_event_detect=False)
    def slow_attr(self) -> int:
        time.sleep(0.1)
        self._slow_attr_last_read_time = time.time()
        time.sleep(0.1)
        return 0

    @attribute
    def slow_attr_last_read_time(self) -> float:
        return self._slow_attr_last_read_time

    @attribute(
        alarm_event_implemented=True,
        alarm_event_detect=False,
        archive_event_implemented=True,
        archive_event_detect=False,
        change_event_implemented=True,
        change_event_detect=False,
        data_ready_event_implemented=True,
    )
    def attr_decorator_with_kwords(self) -> int:
        return 0

    attr_class_with_kwords = attribute(
        alarm_event_implemented=True,
        alarm_event_detect=False,
        archive_event_implemented=True,
        archive_event_detect=False,
        change_event_implemented=True,
        change_event_detect=False,
        data_ready_event_implemented=True,
    )

    def read_attr_class_with_kwords(self) -> int:
        return 0

    @attribute(polling_period=int(ZMQ_READY_ATTRIBUTE_POLLING_PERIOD * 1000))
    def zmq_ready(self) -> int:
        return time.monotonic_ns()

    @command
    def reset(self):
        self._requested_event_type = None
        self._base = 0

    def _send_events(self, attr_name: str, event_type: int):
        # to test fire_xxx_event methods we should have attr object and exception, converted to DevFailed:
        attr = self.get_device_attr().get_attr_by_name(attr_name)
        try:
            raise Exception(f"test exception {self._base + 1}")
        except Exception:
            test_exception = Except.to_dev_failed(*sys.exc_info())

        if event_type == EventType.USER_EVENT:
            self.push_event(attr_name, [], [], self._base + 1)
            self.push_event(attr_name, [], [], self._base + 2, 3.0, AttrQuality.ATTR_WARNING)
            self.push_event(attr_name, [], [], Exception(f"test exception {self._base}"))

        elif event_type == EventType.ARCHIVE_EVENT:
            self.push_archive_event(attr_name, self._base + 1)
            self.push_archive_event(attr_name, self._base + 2, 3.0, AttrQuality.ATTR_WARNING)
            self.push_archive_event(attr_name, Exception(f"test exception {self._base}"))

        elif event_type == EventType.CHANGE_EVENT:
            self.push_change_event(attr_name, self._base + 1)

            self.push_change_event(attr_name, self._base + 2, 3.0, AttrQuality.ATTR_WARNING)

            attr.set_value(self._base + 3)
            attr.fire_change_event()

            self.push_change_event(attr_name, Exception(f"test exception {self._base}"))

            attr.fire_change_event(test_exception)

        elif event_type == EventType.ALARM_EVENT:
            self.push_alarm_event(attr_name, self._base + 1)

            self.push_alarm_event(attr_name, self._base + 2, 3.0, AttrQuality.ATTR_WARNING)

            attr.set_value(self._base + 3)
            attr.fire_alarm_event()

            self.push_alarm_event(attr_name, Exception(f"test exception {self._base}"))

            attr.fire_alarm_event(test_exception)

        elif event_type == EventType.DATA_READY_EVENT:
            self.push_data_ready_event(attr_name, self._base + 1)

    @command
    def send_events(self, event_type: int):
        self._send_events("attr", event_type)

    @command
    def send_slow_event(self):
        self.push_change_event("slow_attr", 42)

    @command
    def send_event_no_data(self, attr_name: str):
        self.push_event(attr_name, [], [])

    @command
    def send_archive_event_no_data(self, attr_name: str):
        self.push_archive_event(attr_name)

    @command
    def send_change_event_no_data(self, attr_name: str):
        self.push_change_event(attr_name)

    @command
    def send_alarm_event_no_data(self, attr_name: str):
        self.push_alarm_event(attr_name)

    @command
    def send_change_event_with_dim_argument(self):
        dim_x_dim_y_unsupported = "dim_x and dim_y arguments are no longer supported"
        now = time.time()

        with pytest.raises(TypeError, match=dim_x_dim_y_unsupported):
            self.push_change_event("attr", 42, 1)

        with pytest.raises(TypeError, match=dim_x_dim_y_unsupported):
            self.push_change_event("attr", 42, 1, 1)

        with pytest.raises(TypeError, match=dim_x_dim_y_unsupported):
            self.push_change_event("attr", 42, dim_x=1)

        with pytest.raises(TypeError, match=dim_x_dim_y_unsupported):
            self.push_change_event("attr", 42, dim_x=1, dim_y=1)

        with pytest.raises(TypeError, match=dim_x_dim_y_unsupported):
            self.push_change_event("attr", 42, now, AttrQuality.ATTR_VALID, 1)

        with pytest.raises(TypeError, match=dim_x_dim_y_unsupported):
            self.push_change_event("attr", 42, now, AttrQuality.ATTR_VALID, 1, 1)

        with pytest.raises(TypeError, match=dim_x_dim_y_unsupported):
            self.push_change_event("dev_encoded_attr", "a", "b", 1)

        with pytest.raises(TypeError, match=dim_x_dim_y_unsupported):
            self.push_change_event("dev_encoded_attr", "a", "b", 1, 1)

        with pytest.raises(TypeError, match=dim_x_dim_y_unsupported):
            self.push_change_event("dev_encoded_attr", "a", "b", dim_x=1)

        with pytest.raises(TypeError, match=dim_x_dim_y_unsupported):
            self.push_change_event("dev_encoded_attr", "a", "b", dim_x=1, dim_y=1)

        # check some valid dev encoded events work
        self.push_change_event("dev_encoded_attr", "a", "b")
        self.push_change_event("dev_encoded_attr", "a", "b", now, AttrQuality.ATTR_VALID)

    @command(dtype_in=str)
    def add_dyn_attr(self, name):
        attr = attribute(name=name, dtype="float", fget=self.read)
        self.add_attribute(attr)

    @command(dtype_in=str)
    def delete_dyn_attr(self, name):
        self.remove_attribute(name)

    def read(self, attr):
        attr.set_value(1.23)


cmd_list = {
    "Init",
    "State",
    "Status",
    "reset",
    "add_dyn_attr",
    "delete_dyn_attr",
    "send_events",
    "send_event_no_data",
    "send_slow_event",
    "send_archive_event_no_data",
    "send_change_event_no_data",
    "send_alarm_event_no_data",
    "send_change_event_with_dim_argument",
}

attr_list = {
    "State",
    "Status",
    "attr",
    "attr_class_with_kwords",
    "attr_decorator_with_kwords",
    "attr_no_events",
    "dev_encoded_attr",
    "slow_attr",
    "slow_attr_last_read_time",
    "zmq_ready",
}

DEVICE_NAME = "test/nodb/eventdevice"


# Device fixture
@pytest.fixture(scope="module")
def event_device_context():
    context = DeviceTestContext(EventDevice, device_name=DEVICE_NAME, host="127.0.0.1", process=True)
    with context:
        yield context


@pytest.fixture(scope="module")
def event_device_with_green_modes(event_device_context, green_mode_device_proxy):
    return green_mode_device_proxy(event_device_context.get_device_access())


@pytest.fixture(scope="module")
def event_device(event_device_context):
    return DeviceProxy(event_device_context.get_device_access())


# Tests
def wait_for_event_condition(proxy, condition, results, *, description, timeout=MAX_RETRIES * DELAY_PER_RETRY):
    deadline = time.monotonic() + timeout
    while True:
        # Let callbacks submitted to Asyncio/Gevent executors make progress.
        proxy.read_attribute("state", wait=True)
        if condition():
            return
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            pytest.fail(f"Timeout after {timeout}s waiting for {description}; received: {results!r}")
        time.sleep(min(DELAY_PER_RETRY, remaining))


def run_event_test(proxy, event_type, cb, expected_res):
    results = []
    callback_errors = []
    initial_callback_finished = Event()
    zmq_data_received = Event()

    def check_initial_event(evt):
        if len(results) == 1 and event_type != EventType.DATA_READY_EVENT:
            assert not evt.err, evt.errors
            assert evt.event_reason == EventReason.SubSuccess
            initial_callback_finished.set()

    if inspect.iscoroutinefunction(cb):

        async def callback(evt):
            try:
                await cb(evt, results)
                check_initial_event(evt)
            except Exception as error:
                callback_errors.append(error)

    else:

        def callback(evt):
            try:
                cb(evt, results)
                check_initial_event(evt)
            except Exception as error:
                callback_errors.append(error)

    zmq_ready_results = []

    def zmq_ready_callback(evt):
        if evt.event_reason == EventReason.Update:
            zmq_data_received.set()
        else:
            zmq_ready_results.append(evt)

    def wait_for_result(condition, description):
        def check():
            if callback_errors:
                raise AssertionError(f"Event callback failed; received: {results!r}") from callback_errors[0]
            return condition()

        wait_for_event_condition(proxy, check, results, description=description)

    proxy.command_inout("reset", wait=True)
    event_ids = []
    try:
        event_ids.append(proxy.subscribe_event("attr", event_type, callback, wait=True))
        event_ids.append(proxy.subscribe_event("zmq_ready", EventType.PERIODIC_EVENT, zmq_ready_callback, wait=True))

        # Data-ready subscriptions do not produce an initial callback.
        if event_type != EventType.DATA_READY_EVENT:
            wait_for_result(initial_callback_finished.is_set, "successful initial callback")
            assert_close(results, expected_res[:1])

        # Wait until we have received something via ZMQ from the second subscription, so we have
        # higher likelihood that the subscriptions have propagated to the PUB socket in the server
        wait_for_event_condition(proxy, zmq_data_received.is_set, zmq_ready_results, description="ZMQ update")

        # Trigger events from command
        proxy.command_inout("send_events", event_type, wait=True)

        # Trigger events from attribute write method
        proxy.write_attribute("attr", event_type, wait=True)

        # Trigger events from attribute read method
        proxy.read_attribute("attr", wait=True)

        wait_for_result(lambda: len(results) >= len(expected_res), f"{len(expected_res)} event results")
        assert_close(results, expected_res)
    finally:
        for event_id in reversed(event_ids):
            proxy.unsubscribe_event(event_id, wait=True)


def test_attribute_with_no_events_cannot_be_subscribed(event_device):
    with pytest.raises(
        DevFailed,
        match=r"Event properties \(abs_change or rel_change\) for attribute attr_no_events are not set",
    ):
        _ = event_device.subscribe_event("attr_no_events", EventType.CHANGE_EVENT, EventCallback())

    with pytest.raises(
        DevFailed,
        match=r"Archive event properties \(archive_abs_change or archive_rel_change or archive_period\) "
        r"for attribute attr_no_events are not set",
    ):
        _ = event_device.subscribe_event("attr_no_events", EventType.ARCHIVE_EVENT, EventCallback())


def test_old_push_event_signatures_no_longer_supported(event_device):
    event_device.send_change_event_with_dim_argument()


def test_change_event(event_device_with_green_modes):
    expected_res = [
        0,
        1,
        2,
        3,
        "Exception: test exception 0\n",
        "Exception: test exception 1\n",
        11,
        12,
        13,
        "Exception: test exception 10\n",
        "Exception: test exception 11\n",
        21,
        22,
        23,
        "Exception: test exception 20\n",
        "Exception: test exception 21\n",
    ]

    if event_device_with_green_modes.get_green_mode() == GreenMode.Asyncio:
        run_event_test(
            event_device_with_green_modes,
            EventType.CHANGE_EVENT,
            async_callback,
            expected_res,
        )
        warn._already_warned_keys.clear()
        with pytest.warns(DeprecationWarning):
            run_event_test(
                event_device_with_green_modes,
                EventType.CHANGE_EVENT,
                event_callback,
                expected_res,
            )
    else:
        run_event_test(
            event_device_with_green_modes,
            EventType.CHANGE_EVENT,
            event_callback,
            expected_res,
        )


def test_alarm_event(event_device):
    expected_res = [
        0,
        1,
        2,
        3,
        "Exception: test exception 0\n",
        "Exception: test exception 1\n",
        11,
        12,
        13,
        "Exception: test exception 10\n",
        "Exception: test exception 11\n",
        21,
        22,
        23,
        "Exception: test exception 20\n",
        "Exception: test exception 21\n",
    ]

    run_event_test(
        event_device,
        EventType.ALARM_EVENT,
        event_callback,
        expected_res,
    )


def test_user_event(event_device):
    expected_res = [
        0,
        1,
        2,
        "Exception: test exception 0\n",
        11,
        12,
        "Exception: test exception 10\n",
        21,
        22,
        "Exception: test exception 20\n",
    ]

    run_event_test(
        event_device,
        EventType.USER_EVENT,
        event_callback,
        expected_res,
    )


def test_archive_event(event_device):
    expected_res = [
        0,
        1,
        2,
        "Exception: test exception 0\n",
        11,
        12,
        "Exception: test exception 10\n",
        21,
        22,
        "Exception: test exception 20\n",
    ]

    run_event_test(
        event_device,
        EventType.ARCHIVE_EVENT,
        event_callback,
        expected_res,
    )


def test_subscribe_data_ready_event(event_device):
    expected_res = [1, 11, 21]
    run_event_test(
        event_device,
        EventType.DATA_READY_EVENT,
        event_callback,
        expected_res,
    )


def test_subscribe_interface_event(event_device):
    events = []

    def check_events(expected_attributes):
        wait_for_event_condition(
            event_device,
            lambda: len(events) >= len(expected_attributes),
            events,
            description=f"{len(expected_attributes)} interface callbacks",
        )
        assert len(events) == len(expected_attributes), events
        for event, attributes in zip(events, expected_attributes, strict=True):
            assert not event.err, event.errors
            assert {cmd.cmd_name for cmd in event.cmd_list} == cmd_list
            assert {att.name for att in event.att_list} == attributes

    eid = event_device.subscribe_event(EventType.INTERFACE_CHANGE_EVENT, events.append, wait=True)
    try:
        check_events([attr_list])

        event_device.command_inout("add_dyn_attr", "bla", wait=True)
        event_device.read_attribute("bla", wait=True)
        check_events([attr_list, attr_list | {"bla"}])

        event_device.command_inout("delete_dyn_attr", "bla", wait=True)
        check_events([attr_list, attr_list | {"bla"}, attr_list])
    finally:
        try:
            if "bla" in event_device.get_command_list():
                event_device.command_inout("delete_dyn_attr", "bla", wait=True)
        finally:
            event_device.unsubscribe_event(eid, wait=True)


def test_push_event_with_event_callback(event_device):
    string = StringIO()
    completed_events = []

    class CompletedEventCallback(EventCallback):
        def push_event(self, evt):
            super().push_event(evt)
            # EventCallback stores the event before writing its output.
            completed_events.append(evt)

    cb = CompletedEventCallback(fd=string)

    # to reduce tests amount here we test only change event
    eid = event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb, wait=True)
    try:
        wait_for_event_condition(
            event_device,
            lambda: bool(completed_events),
            completed_events,
            description="initial EventCallback output",
        )
        event_device.command_inout("send_events", EventType.CHANGE_EVENT, wait=True)
        wait_for_event_condition(
            event_device,
            lambda: len(completed_events) >= 6,
            completed_events,
            description="all six EventCallback outputs",
        )
        # Test the event values and timestamp
        events = cb.get_events()
        assert len(events) == 6
        results = [evt.attr_value.value for evt in events[:4]]
        assert results == [0, 1, 2, 3]
        assert events[2].attr_value.time.totime() == 3.0
        assert events[4].errors[0].desc == "Exception: test exception 0\n"
        assert events[5].errors[0].desc == "Exception: test exception 1\n"
        for evt in events:
            assert evt.device is event_device

        # Check string
        for line in [
            "TEST/NODB/EVENTDEVICE ATTR CHANGE SUBSUCCESS [ATTR_VALID] 0",
            "TEST/NODB/EVENTDEVICE ATTR CHANGE UPDATE [ATTR_VALID] 1",
            "TEST/NODB/EVENTDEVICE ATTR CHANGE UPDATE [ATTR_WARNING] 2",
            "TEST/NODB/EVENTDEVICE ATTR CHANGE UPDATE [ATTR_VALID] 3",
            "TEST/NODB/EVENTDEVICE ATTR CHANGE UPDATE [PyDs_PythonError] Exception: test exception 0",
            "TEST/NODB/EVENTDEVICE ATTR CHANGE UPDATE [PyDs_PythonError] Exception: test exception 1",
        ]:
            assert line in string.getvalue()
    finally:
        event_device.unsubscribe_event(eid, wait=True)


def test_send_events_no_data(event_device):
    event_device.command_inout("send_event_no_data", "state", wait=True)
    event_device.command_inout("send_archive_event_no_data", "State", wait=True)
    event_device.command_inout("send_change_event_no_data", "STaTe", wait=True)
    event_device.command_inout("send_alarm_event_no_data", "state", wait=True)

    event_device.command_inout("send_event_no_data", "status", wait=True)
    event_device.command_inout("send_archive_event_no_data", "Status", wait=True)
    event_device.command_inout("send_change_event_no_data", "STaTus", wait=True)
    event_device.command_inout("send_alarm_event_no_data", "status", wait=True)

    expected_err_msg = (
        "Cannot push event for attribute attr without data. "
        "Pushing event without data parameter is only allowed for State and Status attributes."
    )

    with pytest.raises(DevFailed, match=expected_err_msg):
        event_device.command_inout("send_event_no_data", "attr", wait=True)

    with pytest.raises(DevFailed, match=expected_err_msg):
        event_device.command_inout("send_archive_event_no_data", "attr", wait=True)

    with pytest.raises(DevFailed, match=expected_err_msg):
        event_device.command_inout("send_change_event_no_data", "attr", wait=True)

    with pytest.raises(DevFailed, match=expected_err_msg):
        event_device.command_inout("send_alarm_event_no_data", "attr", wait=True)


def test_main_thread_is_omni_thread():
    assert is_omni_thread()


def test_ensure_omni_thread_main_thread_is_omni_thread():
    with EnsureOmniThread():
        assert is_omni_thread()


def test_user_thread_is_not_omni_thread():
    thread_is_omni = {"result": None}  # use a dict so thread can modify it

    def thread_func():
        thread_is_omni["result"] = is_omni_thread()

    thread = Thread(target=thread_func)
    thread.start()
    thread.join()
    assert thread_is_omni["result"] is False


def test_ensure_omni_thread_user_thread_is_omni_thread():
    thread_is_omni = {"result": None}  # use a dict so thread can modify it

    def thread_func():
        with EnsureOmniThread():
            thread_is_omni["result"] = is_omni_thread()

    thread = Thread(target=thread_func)
    thread.start()
    thread.join()
    assert thread_is_omni["result"] is True


def test_subscribe_change_event_from_user_thread(event_device):
    received_events = []
    worker_errors = []
    subscribed = Event()
    stop = Event()

    def thread_func():
        try:
            with EnsureOmniThread():
                eid = event_device.subscribe_event("attr", EventType.CHANGE_EVENT, received_events.append, wait=True)
                try:
                    subscribed.set()
                    stop.wait()
                finally:
                    try:
                        event_device.unsubscribe_event(eid, wait=True)
                    except Exception as exc:
                        worker_errors.append(exc)
        except Exception as exc:
            worker_errors.append(exc)

    def check_worker():
        if worker_errors:
            raise AssertionError(f"Event subscription worker failed: {worker_errors!r}") from worker_errors[0]

    def subscription_ready():
        check_worker()
        return subscribed.is_set() and bool(received_events)

    def updates_received():
        check_worker()
        return len(received_events) >= 6

    thread = Thread(target=thread_func, daemon=True)
    thread.start()
    try:
        wait_for_event_condition(
            event_device,
            subscription_ready,
            received_events,
            description="worker subscription return and initial callback",
        )
        event_device.command_inout("send_events", EventType.CHANGE_EVENT, wait=True)
        wait_for_event_condition(
            event_device,
            updates_received,
            received_events,
            description="all six worker subscription events",
        )
        results = []
        for evt in received_events:
            event_callback(evt, results)
        assert results == [
            0,
            1,
            2,
            3,
            "Exception: test exception 0\n",
            "Exception: test exception 1\n",
        ]
    finally:
        stop.set()
        # Pump the green executor while the worker finishes unsubscribing.
        wait_for_event_condition(
            event_device,
            lambda: not thread.is_alive(),
            worker_errors,
            description="event subscription worker shutdown",
        )
        thread.join(timeout=0)
        check_worker()


@pytest.mark.parametrize("receiver", ["cb", "no"])
@pytest.mark.parametrize(
    "event_type", [event_type for event_type in EventType.values.values() if event_type != EventType.PERIODIC_EVENT]
)
def test_get_events(event_device, receiver, event_type):
    received_events = []

    def callback(event):
        received_events.append(event)

    eid = event_device.subscribe_event("attr", event_type, 1, wait=True)
    try:
        # DATA_READY_EVENT does not send automatically at the subscription.
        # PERIODIC_EVENT is excluded above because it needs polling.
        if event_type == EventType.DATA_READY_EVENT:
            event_device.send_events(event_type, wait=True)

        def retrieve_events():
            if receiver == "no":
                received_events.extend(event_device.get_events(eid))
            else:
                event_device.get_events(eid, callback)
            return bool(received_events)

        wait_for_event_condition(
            event_device,
            retrieve_events,
            received_events,
            description=f"queued {event_type} event with receiver {receiver}",
        )
        if receiver == "cb":
            for event in received_events:
                event_callback(event, [])
    finally:
        event_device.unsubscribe_event(eid, wait=True)


def test_callback_was_dereferenced(event_device):

    def fcb(_event):
        pass

    initial_refs = len(gc.get_referrers(fcb))
    ids = [event_device.subscribe_event("attr", EventType.CHANGE_EVENT, fcb, wait=True) for _ in range(10)]
    assert initial_refs < len(gc.get_referrers(fcb))

    for id in ids:
        event_device.unsubscribe_event(id, wait=True)

    assert initial_refs == len(gc.get_referrers(fcb))


def test_event_after_unsubscription_crash(event_device):
    callbacks = []
    subscription_ids = []
    callback_errors = []

    class DummyCallback:
        def push_event(self, event):
            pass

    class MainCallback:
        def __init__(self):
            self.device = DeviceProxy(DEVICE_NAME)
            self.eid = self.device.subscribe_event("attr", EventType.CHANGE_EVENT, DummyCallback())
            self.is_first_time = True
            self.finished = Event()

        def unsubscribe(self):
            if self.device is not None:
                self.device.unsubscribe_event(self.eid)
                self.device = None  # remove reference, so it can be deleted

        def push_event(self, _event):
            if self.is_first_time:
                # callback from initial subscription
                self.is_first_time = False
            elif self.device is not None:
                try:
                    # Unsubscribe and release the proxy inside the update callback.
                    self.unsubscribe()
                except Exception as error:
                    callback_errors.append(error)
                finally:
                    self.finished.set()

    def callbacks_finished():
        if callback_errors:
            raise AssertionError("Unsubscription callback failed") from callback_errors[0]
        return all(callback.finished.is_set() for callback in callbacks)

    try:
        for _ in range(50):
            callback = MainCallback()
            callbacks.append(callback)
            subscription_ids.append(event_device.subscribe_event("attr", EventType.CHANGE_EVENT, callback))
            event_device.send_events(EventType.CHANGE_EVENT)

        wait_for_event_condition(
            event_device,
            callbacks_finished,
            callback_errors,
            description="all 50 callbacks to unsubscribe and release their proxies",
        )
    finally:
        for eid in subscription_ids:
            event_device.unsubscribe_event(eid, wait=True)
        # Release inner subscriptions too if setup or a callback failed.
        for callback in callbacks:
            callback.unsubscribe()


def test_events_enabled_by_kwords(event_device):
    """
    In this test we only check, that we can subscribe, i.e., that out kwords were passed to Tango::Attr
    """
    events_to_check = [
        EventType.ALARM_EVENT,
        EventType.ARCHIVE_EVENT,
        EventType.CHANGE_EVENT,
        EventType.DATA_READY_EVENT,
    ]

    for attr_name in ["attr_decorator_with_kwords", "attr_class_with_kwords"]:
        eids = [
            event_device.subscribe_event(attr_name, event_type, lambda event: None, wait=True)
            for event_type in events_to_check
        ]
        for eid in eids:
            event_device.unsubscribe_event(eid)


@dataclass
class SubscriptionModeExpectation:
    sub_mode: EventSubMode
    read_during_subscription: bool
    read_after_subscription: bool
    initial_event_after_subscription: bool
    initial_event_has_data: bool
    exception_on_subscription_failure: bool

    def __str__(self):
        return str(self.sub_mode)


subscription_mode_tests = (
    SubscriptionModeExpectation(
        sub_mode=EventSubMode.Sync,
        read_during_subscription=False,
        read_after_subscription=False,
        initial_event_after_subscription=False,
        initial_event_has_data=False,
        exception_on_subscription_failure=True,
    ),
    SubscriptionModeExpectation(
        sub_mode=EventSubMode.SyncRead,
        read_during_subscription=True,
        read_after_subscription=False,
        initial_event_after_subscription=True,
        initial_event_has_data=True,
        exception_on_subscription_failure=True,
    ),
    SubscriptionModeExpectation(
        sub_mode=EventSubMode.Async,
        read_during_subscription=False,
        read_after_subscription=False,
        initial_event_after_subscription=True,
        initial_event_has_data=False,
        exception_on_subscription_failure=False,
    ),
    SubscriptionModeExpectation(
        sub_mode=EventSubMode.AsyncRead,
        read_during_subscription=False,
        read_after_subscription=True,
        initial_event_after_subscription=True,
        initial_event_has_data=True,
        exception_on_subscription_failure=False,
    ),
    SubscriptionModeExpectation(
        sub_mode=EventSubMode.Stateless,
        read_during_subscription=True,
        read_after_subscription=False,
        initial_event_after_subscription=True,
        initial_event_has_data=True,
        exception_on_subscription_failure=False,
    ),
)


def wait_for_single_event(proxy, events, timeout) -> EventData:
    wait_for_event_condition(proxy, lambda: bool(events), events, description="one event", timeout=timeout)
    assert len(events) == 1, f"Expected exactly one event; received: {events!r}"
    return events[0]


class GatedSlowAttrEventDevice(EventDevice):
    @attribute(change_event_implemented=True, change_event_detect=False)
    def slow_attr(self) -> int:
        self.read_started.set()
        assert self.allow_read.wait(timeout=MAX_RETRIES * DELAY_PER_RETRY), "Subscription did not release the read"
        self.read_finished.set()
        return 0


class GatedDeviceTestContext(DeviceTestContext):
    def __init__(self):
        super().__init__(GatedSlowAttrEventDevice, process=True)
        self.read_started = multiprocessing.Event()
        self.read_finished = multiprocessing.Event()
        self.allow_read = multiprocessing.Event()

    def target(self, runserver, process=False):
        # Transfer the events with the context, then attach them in the child.
        GatedSlowAttrEventDevice.read_started = self.read_started
        GatedSlowAttrEventDevice.read_finished = self.read_finished
        GatedSlowAttrEventDevice.allow_read = self.allow_read
        super().target(runserver, process)


@pytest.mark.parametrize("subscription_mode_tests", subscription_mode_tests, ids=str)
def test_event_subscription_sub_modes(subscription_mode_tests):
    params = subscription_mode_tests
    events = []
    context = GatedDeviceTestContext()

    if not params.read_after_subscription:
        context.allow_read.set()

    with context as event_device:
        eid = None
        try:
            eid = event_device.subscribe_event(
                "slow_attr",
                EventType.CHANGE_EVENT,
                cb=events.append,
                sub_mode=params.sub_mode,
            )
            if params.read_during_subscription:
                assert context.read_finished.is_set(), "Subscription returned before its attribute read"
            elif params.read_after_subscription:
                # The read cannot finish until subscription has returned, even
                # if this thread is descheduled immediately after the call.
                assert not context.read_finished.is_set(), "Attribute read bypassed the gate"
                context.allow_read.set()

            if params.initial_event_after_subscription:
                event = wait_for_single_event(event_device, events, timeout=1.0)
                assert event.event_reason == EventReason.SubSuccess
                if params.initial_event_has_data:
                    assert event.attr_value is not None
                    assert context.read_finished.is_set()
                else:
                    assert event.attr_value is None

            if not (params.read_during_subscription or params.read_after_subscription):
                assert not context.read_started.is_set(), "Subscription unexpectedly read the attribute"

            events.clear()
            event_device.send_slow_event()
            event = wait_for_single_event(event_device, events, timeout=0.5)
            assert event.event_reason == EventReason.Update
            assert event.attr_value is not None
        finally:
            # This must not be a device command: the read can hold its monitor.
            context.allow_read.set()
            if eid is not None:
                event_device.unsubscribe_event(eid, wait=True)


@pytest.mark.parametrize("subscription_mode_tests", subscription_mode_tests, ids=str)
def test_event_subscription_sub_modes_invalid_attribute_fails(subscription_mode_tests):
    params = subscription_mode_tests

    events = []

    with DeviceTestContext(Device, process=True) as event_device:
        if params.exception_on_subscription_failure:
            with pytest.raises(DevFailed, match="API_AttrNotFound"):
                _ = event_device.subscribe_event(
                    "non_existent_attr",
                    EventType.CHANGE_EVENT,
                    cb=events.append,
                    sub_mode=params.sub_mode,
                )
        else:
            eid = event_device.subscribe_event(
                "non_existent_attr",
                EventType.CHANGE_EVENT,
                cb=events.append,
                sub_mode=params.sub_mode,
            )

            try:
                event = wait_for_single_event(event_device, events, timeout=0.5)
                assert event.err
                assert len(event.errors) > 0
                assert event.event_reason == EventReason.SubFail
                assert event.attr_value is None

            finally:
                event_device.unsubscribe_event(eid, wait=True)


def test_subscribe_event_signatures():
    """
    Signatures to be supported:

        subscribe_event(self,            event_type, cb,        sub_mode=EventSubMode.SyncRead, *, __GREEN_KWARGS__) -> int
        subscribe_event(self,            event_type, cb,        stateless=False,                *, __GREEN_KWARGS__) -> int

        subscribe_event(self, attr_name, event_type, cb,        sub_mode=EventSubMode.SyncRead, extract_as=ExtractAs.Numpy, *, __GREEN_KWARGS__) -> int
        subscribe_event(self, attr_name, event_type, queuesize, sub_mode=EventSubMode.SyncRead, extract_as=ExtractAs.Numpy, *, __GREEN_KWARGS__) -> int
        subscribe_event(self, attr_name, event_type, cb,        filters=[], stateless=False,    extract_as=ExtractAs.Numpy, *, __GREEN_KWARGS__) -> int
        subscribe_event(self, attr_name, event_type, queuesize, filters=[], stateless=False,    extract_as=ExtractAs.Numpy, *, __GREEN_KWARGS__) -> int
    """

    last_called_method_and_args = []

    def cb(evnt):
        pass

    cb_with_push_event = EventCallback()

    def subscription_call_mock(method, *args):
        last_called_method_and_args.append((method, *args))
        return len(last_called_method_and_args)

    def check_last_called_method(*method_and_args):
        for called, expected in zip(last_called_method_and_args[-1], method_and_args, strict=True):
            if callable(expected):
                callback = inspect.unwrap(called.push_event)
                assert callback == expected
            else:
                assert called == expected

    # functionality is mocked, so we don't need a real device
    event_device = DeviceProxy("tango://127.0.0.1:0/dummy/test/device#dbase=no")

    with pytest.warns(PyTangoUserWarning):
        event_device.unfreeze_dynamic_interface()

    event_device.__subscribe_event_global_with_stateless_flag = lambda *args: subscription_call_mock(
        "__subscribe_event_global_with_stateless_flag", *args
    )
    event_device.__subscribe_event_global_with_sub_mode = lambda *args: subscription_call_mock(
        "__subscribe_event_global_with_sub_mode", *args
    )
    event_device.__subscribe_event_attrib_with_stateless_flag = lambda *args: subscription_call_mock(
        "__subscribe_event_attrib_with_stateless_flag", *args
    )
    event_device.__subscribe_event_attrib_with_sub_mode = lambda *args: subscription_call_mock(
        "__subscribe_event_attrib_with_sub_mode", *args
    )

    with pytest.raises(TypeError, match="This method is only for Interface Change Events"):
        event_device.subscribe_event(EventType.CHANGE_EVENT)

    with pytest.raises(IndexError, match="Expected parameter 'cb'"):
        event_device.subscribe_event(EventType.INTERFACE_CHANGE_EVENT)

    event_device.subscribe_event(EventType.INTERFACE_CHANGE_EVENT, cb)
    check_last_called_method(
        "__subscribe_event_global_with_sub_mode",
        EventType.INTERFACE_CHANGE_EVENT,
        cb,
        EventSubMode.SyncRead,
    )
    event_device.subscribe_event(EventType.INTERFACE_CHANGE_EVENT, cb=cb)
    check_last_called_method(
        "__subscribe_event_global_with_sub_mode",
        EventType.INTERFACE_CHANGE_EVENT,
        cb,
        EventSubMode.SyncRead,
    )
    event_device.subscribe_event(EventType.INTERFACE_CHANGE_EVENT, cb_with_push_event)
    check_last_called_method(
        "__subscribe_event_global_with_sub_mode",
        EventType.INTERFACE_CHANGE_EVENT,
        cb_with_push_event.push_event,
        EventSubMode.SyncRead,
    )
    event_device.subscribe_event(EventType.INTERFACE_CHANGE_EVENT, cb=cb_with_push_event)
    check_last_called_method(
        "__subscribe_event_global_with_sub_mode",
        EventType.INTERFACE_CHANGE_EVENT,
        cb_with_push_event.push_event,
        EventSubMode.SyncRead,
    )

    with pytest.raises(TypeError, match="Parameter 'cb' must be callable object"):
        event_device.subscribe_event(EventType.INTERFACE_CHANGE_EVENT, cb=None)

    with pytest.raises(TypeError, match="Parameter 'cb' must be callable object"):
        event_device.subscribe_event(EventType.INTERFACE_CHANGE_EVENT, None)

    with pytest.raises(
        IndexError,
        match="Expected parameter 'cb' as either positional arg 2, ",
    ):
        event_device.subscribe_event(EventType.INTERFACE_CHANGE_EVENT)

    event_device.subscribe_event(EventType.INTERFACE_CHANGE_EVENT, cb, EventSubMode.AsyncRead)
    check_last_called_method(
        "__subscribe_event_global_with_sub_mode",
        EventType.INTERFACE_CHANGE_EVENT,
        cb,
        EventSubMode.AsyncRead,
    )
    event_device.subscribe_event(EventType.INTERFACE_CHANGE_EVENT, cb, sub_mode=EventSubMode.AsyncRead)
    check_last_called_method(
        "__subscribe_event_global_with_sub_mode",
        EventType.INTERFACE_CHANGE_EVENT,
        cb,
        EventSubMode.AsyncRead,
    )

    warn._already_warned_keys.clear()
    with pytest.warns(DeprecationWarning, match="The 'stateless' parameter is deprecated"):
        event_device.subscribe_event(EventType.INTERFACE_CHANGE_EVENT, cb, False)

    check_last_called_method(
        "__subscribe_event_global_with_stateless_flag",
        EventType.INTERFACE_CHANGE_EVENT,
        cb,
        False,
    )
    warn._already_warned_keys.clear()
    with pytest.warns(DeprecationWarning, match="The 'stateless' parameter is deprecated"):
        event_device.subscribe_event(EventType.INTERFACE_CHANGE_EVENT, cb, stateless=False)
    check_last_called_method(
        "__subscribe_event_global_with_stateless_flag",
        EventType.INTERFACE_CHANGE_EVENT,
        cb,
        False,
    )

    with pytest.raises(TypeError, match="Invalid type for parameter"):
        event_device.subscribe_event(EventType.INTERFACE_CHANGE_EVENT, cb, None)

    with pytest.raises(TypeError, match="Invalid type for parameter"):
        event_device.subscribe_event(EventType.INTERFACE_CHANGE_EVENT, cb, sub_mode=None)

    with pytest.raises(TypeError, match="Invalid type for parameter"):
        event_device.subscribe_event(EventType.INTERFACE_CHANGE_EVENT, cb, stateless=None)

    with pytest.raises(IndexError, match="Expected parameter 'event_type'"):
        event_device.subscribe_event("attr")

    with pytest.raises(TypeError, match="Invalid type for parameter"):
        event_device.subscribe_event("attr", None)

    with pytest.raises(TypeError, match="Invalid type for parameter"):
        event_device.subscribe_event("attr", event_type=None)

    with pytest.raises(TypeError, match=r"Either parameter 'queuesize' .* or parameter 'cb'"):
        event_device.subscribe_event("attr", EventType.CHANGE_EVENT)

    event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb)
    check_last_called_method(
        "__subscribe_event_attrib_with_sub_mode",
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        EventSubMode.SyncRead,
        ExtractAs.Numpy,
    )
    event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb=cb)
    check_last_called_method(
        "__subscribe_event_attrib_with_sub_mode",
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        EventSubMode.SyncRead,
        ExtractAs.Numpy,
    )
    event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb_with_push_event)
    check_last_called_method(
        "__subscribe_event_attrib_with_sub_mode",
        "attr",
        EventType.CHANGE_EVENT,
        cb_with_push_event.push_event,
        EventSubMode.SyncRead,
        ExtractAs.Numpy,
    )
    event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb=cb_with_push_event)
    check_last_called_method(
        "__subscribe_event_attrib_with_sub_mode",
        "attr",
        EventType.CHANGE_EVENT,
        cb_with_push_event.push_event,
        EventSubMode.SyncRead,
        ExtractAs.Numpy,
    )

    event_device.subscribe_event("attr", EventType.CHANGE_EVENT, 1)
    check_last_called_method(
        "__subscribe_event_attrib_with_sub_mode",
        "attr",
        EventType.CHANGE_EVENT,
        1,
        EventSubMode.SyncRead,
        ExtractAs.Numpy,
    )
    event_device.subscribe_event("attr", EventType.CHANGE_EVENT, queuesize=1)
    check_last_called_method(
        "__subscribe_event_attrib_with_sub_mode",
        "attr",
        EventType.CHANGE_EVENT,
        1,
        EventSubMode.SyncRead,
        ExtractAs.Numpy,
    )

    with pytest.raises(TypeError, match=r"Either parameter 'queuesize' .* or parameter 'cb'"):
        event_device.subscribe_event("attr", EventType.CHANGE_EVENT, None)

    with pytest.raises(TypeError, match="'cb' and 'queuesize' cannot be used together"):
        event_device.subscribe_event(
            "attr",
            EventType.CHANGE_EVENT,
            cb=cb,
            queuesize=1,
        )

    with pytest.raises(TypeError, match="Invalid type for parameter 'cb=None'"):
        event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb=None)

    with pytest.raises(TypeError, match="Invalid type for parameter 'queuesize="):
        event_device.subscribe_event("attr", EventType.CHANGE_EVENT, queuesize=None)

    warn._already_warned_keys.clear()
    with pytest.warns(
        DeprecationWarning,
        match="The 'stateless' and 'filters' parameters are deprecated",
    ):
        event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb, [])
    check_last_called_method(
        "__subscribe_event_attrib_with_stateless_flag",
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        False,
        ExtractAs.Numpy,
        [],
    )
    warn._already_warned_keys.clear()
    with pytest.warns(
        DeprecationWarning,
        match="The 'stateless' and 'filters' parameters are deprecated",
    ):
        event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb, filters=[])
    check_last_called_method(
        "__subscribe_event_attrib_with_stateless_flag",
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        False,
        ExtractAs.Numpy,
        [],
    )

    with pytest.raises(TypeError, match="Invalid type for parameter 'filters="):
        event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb, filters=None)

    event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb, EventSubMode.AsyncRead)
    check_last_called_method(
        "__subscribe_event_attrib_with_sub_mode",
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        EventSubMode.AsyncRead,
        ExtractAs.Numpy,
    )
    event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb, sub_mode=EventSubMode.AsyncRead)
    check_last_called_method(
        "__subscribe_event_attrib_with_sub_mode",
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        EventSubMode.AsyncRead,
        ExtractAs.Numpy,
    )
    with pytest.raises(TypeError, match="Invalid type for parameter 'sub_mode"):
        event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb, sub_mode=None)
    with pytest.raises(TypeError, match="Invalid type for parameter 'stateless"):
        event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb, [], EventSubMode.SyncRead)
    with pytest.raises(TypeError, match="'sub_mode' and 'filters' cannot be used together"):
        event_device.subscribe_event(
            "attr",
            EventType.CHANGE_EVENT,
            cb,
            filters=[],
            sub_mode=EventSubMode.SyncRead,
        )
    with pytest.raises(TypeError, match="'sub_mode' and 'stateless' cannot be used together"):
        event_device.subscribe_event(
            "attr",
            EventType.CHANGE_EVENT,
            cb,
            stateless=False,
            sub_mode=EventSubMode.SyncRead,
        )

    warn._already_warned_keys.clear()
    with pytest.warns(
        DeprecationWarning,
        match="The 'stateless' and 'filters' parameters are deprecated",
    ):
        event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb, [], True)
    check_last_called_method(
        "__subscribe_event_attrib_with_stateless_flag",
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        True,
        ExtractAs.Numpy,
        [],
    )
    warn._already_warned_keys.clear()
    with pytest.warns(
        DeprecationWarning,
        match="The 'stateless' and 'filters' parameters are deprecated",
    ):
        event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb, [], stateless=True)
    check_last_called_method(
        "__subscribe_event_attrib_with_stateless_flag",
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        True,
        ExtractAs.Numpy,
        [],
    )
    warn._already_warned_keys.clear()
    with pytest.warns(
        DeprecationWarning,
        match="The 'stateless' and 'filters' parameters are deprecated",
    ):
        event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb, filters=["a", "b"], stateless=True)
    check_last_called_method(
        "__subscribe_event_attrib_with_stateless_flag",
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        True,
        ExtractAs.Numpy,
        ["a", "b"],
    )
    warn._already_warned_keys.clear()
    with pytest.warns(
        DeprecationWarning,
        match="The 'stateless' and 'filters' parameters are deprecated",
    ):
        event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb, stateless=True)
    check_last_called_method(
        "__subscribe_event_attrib_with_stateless_flag",
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        True,
        ExtractAs.Numpy,
        [],
    )
    with pytest.raises(TypeError, match="Invalid type for parameter 'sub_mode"):
        event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb, False)
    with pytest.raises(TypeError, match="Invalid type for parameter 'stateless"):
        event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb, [], stateless=None)

    event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb, EventSubMode.AsyncRead, ExtractAs.Tuple)
    check_last_called_method(
        "__subscribe_event_attrib_with_sub_mode",
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        EventSubMode.AsyncRead,
        ExtractAs.Tuple,
    )
    event_device.subscribe_event(
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        EventSubMode.AsyncRead,
        extract_as=ExtractAs.Tuple,
    )
    check_last_called_method(
        "__subscribe_event_attrib_with_sub_mode",
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        EventSubMode.AsyncRead,
        ExtractAs.Tuple,
    )
    warn._already_warned_keys.clear()
    with pytest.warns(
        DeprecationWarning,
        match="The 'stateless' and 'filters' parameters are deprecated",
    ):
        event_device.subscribe_event(
            "attr",
            EventType.CHANGE_EVENT,
            cb,
            [],
            True,
            ExtractAs.Tuple,
        )
    check_last_called_method(
        "__subscribe_event_attrib_with_stateless_flag",
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        True,
        ExtractAs.Tuple,
        [],
    )
    warn._already_warned_keys.clear()
    with pytest.warns(
        DeprecationWarning,
        match="The 'stateless' and 'filters' parameters are deprecated",
    ):
        event_device.subscribe_event(
            "attr",
            EventType.CHANGE_EVENT,
            cb,
            [],
            True,
            extract_as=ExtractAs.Tuple,
        )
    check_last_called_method(
        "__subscribe_event_attrib_with_stateless_flag",
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        True,
        ExtractAs.Tuple,
        [],
    )

    with pytest.raises(TypeError, match="Invalid type for parameter 'extract_as' at position 4"):
        event_device.subscribe_event("attr", EventType.CHANGE_EVENT, cb, EventSubMode.SyncRead, None)

    with pytest.raises(TypeError, match="Invalid type for parameter 'extract_as"):
        event_device.subscribe_event(
            "attr",
            EventType.CHANGE_EVENT,
            cb,
            EventSubMode.SyncRead,
            extract_as=None,
        )

    event_device.subscribe_event(
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        EventSubMode.AsyncRead,
        ExtractAs.Tuple,
        green_mode=GreenMode.Synchronous,
    )
    check_last_called_method(
        "__subscribe_event_attrib_with_sub_mode",
        "attr",
        EventType.CHANGE_EVENT,
        cb,
        EventSubMode.AsyncRead,
        ExtractAs.Tuple,
    )

    with pytest.raises(
        TypeError,
        match=r"Got unexpected keyword argument.*submode.*\nAllowed.*sub_mode.*",
    ):
        event_device.subscribe_event(
            "attr",
            EventType.CHANGE_EVENT,
            cb,
            submode=EventSubMode.SyncRead,
            extract_as=None,
        )


_event_type_to_method_name = {
    EventType.ALARM_EVENT: "alarm_event_subscribed",
    EventType.PERIODIC_EVENT: "periodic_event_subscribed",
    EventType.ARCHIVE_EVENT: "archive_event_subscribed",
    EventType.CHANGE_EVENT: "change_event_subscribed",
    EventType.USER_EVENT: "user_event_subscribed",
}


class SimpleEventDevice(Device):
    @attribute(
        alarm_event_implemented=True,
        alarm_event_detect=False,
        archive_event_implemented=True,
        archive_event_detect=False,
        change_event_implemented=True,
        change_event_detect=False,
        data_ready_event_implemented=True,
        polling_period=1000,
    )
    def attr(self) -> tuple[int, int]:
        return [0, 0]

    @command
    def check_is_event_subscribed(self, event_type: int):
        attr = self.get_device_attr().get_attr_by_name("attr")
        assert getattr(attr, _event_type_to_method_name[EventType(event_type)])()
        assert attr.is_event_subscribed(EventType(event_type))

    @command
    def check_is_event_not_subscribed(self, event_type: int):
        attr = self.get_device_attr().get_attr_by_name("attr")
        assert not getattr(attr, _event_type_to_method_name[EventType(event_type)])()
        assert not attr.is_event_subscribed(EventType(event_type))


@pytest.mark.parametrize("event_type_to_test", _event_type_to_method_name.keys())
def test_is_event_subscribed(event_type_to_test):
    with DeviceTestContext(SimpleEventDevice, process=True) as event_device:
        for event_type in _event_type_to_method_name:
            event_device.check_is_event_not_subscribed(event_type)

        eid = event_device.subscribe_event("attr", event_type_to_test, EventCallback())
        for event_type in _event_type_to_method_name:
            if event_type == event_type_to_test:
                event_device.check_is_event_subscribed(event_type)
            else:
                event_device.check_is_event_not_subscribed(event_type)

        event_device.unsubscribe_event(eid)


def test_callback_extract_as(extract_as):
    requested_type, expected_type = extract_as

    events = []

    with DeviceTestContext(SimpleEventDevice, process=True) as event_device:
        eid = event_device.subscribe_event("attr", EventType.CHANGE_EVENT, events.append, extract_as=requested_type)
        try:
            event = wait_for_single_event(event_device, events, timeout=1.0)
            assert not event.err, event.errors
            assert isinstance(event.attr_value.value, expected_type)
        finally:
            event_device.unsubscribe_event(eid, wait=True)


def test_device_proxy_in_server_receives_events(server_green_mode):
    events = []
    if server_green_mode == GreenMode.Asyncio:

        async def callback(event):
            events.append(event)

        class SelfSubscribeDevice(Device):
            green_mode = GreenMode.Asyncio

            @attribute(change_event_implemented=True, change_event_detect=False)
            async def attr(self) -> int:
                return 1

            @command
            async def subscribe(self) -> None:
                self.proxy = await get_device_proxy("test/nodb/1", green_mode=GreenMode.Asyncio)
                self.sub_id = await self.proxy.subscribe_event("attr", EventType.CHANGE_EVENT, callback)

            @command
            async def unsubscribe(self) -> None:
                await self.proxy.unsubscribe_event(self.sub_id)

    else:

        class SelfSubscribeDevice(Device):
            green_mode = server_green_mode

            @attribute(change_event_implemented=True, change_event_detect=False)
            def attr(self) -> int:
                return 1

            @command
            def subscribe(self) -> None:
                self.proxy = get_device_proxy("test/nodb/1", green_mode=server_green_mode)
                self.sub_id = self.proxy.subscribe_event("attr", EventType.CHANGE_EVENT, events.append)

            @command
            def unsubscribe(self) -> None:
                self.proxy.unsubscribe_event(self.sub_id)

    with DeviceTestContext(SelfSubscribeDevice, device_name="test/nodb/1") as device:
        device.subscribe()
        try:
            # Wait outside the server command so its executor can run the callback.
            event = wait_for_single_event(device, events, timeout=1.0)
            assert not event.err, event.errors
            assert event.event_reason == EventReason.SubSuccess
            assert event.attr_value.value == 1
        finally:
            device.unsubscribe()


class CleanupEventDevice(Device):
    @attribute(dtype=int, change_event_implemented=True, change_event_detect=False)
    def sample(self):
        return 0

    @command
    def send_sample(self):
        self.push_change_event("sample", 123)


def cleanup_during_event_callback(device_trl, callback_started_connection):
    proxy = DeviceProxy(device_trl)
    callback_started = Event()

    def callback(event):
        if not event.err and event.attr_value.value == 123:
            callback_started_connection.send(None)
            callback_started.set()
            time.sleep(3)

    proxy.subscribe_event("sample", EventType.CHANGE_EVENT, callback)
    proxy.send_sample()
    assert callback_started.wait(timeout=10)
    ApiUtil.cleanup()
    os._exit(0)  # avoid DeviceProxy clean-up (we aren't testing that)


@pytest.mark.extra_src_test
def test_api_util_cleanup_does_not_deadlock_during_small_event_callback():
    device_context = DeviceTestContext(CleanupEventDevice, process=True)
    with device_context:
        process_context = multiprocessing.get_context("spawn")
        callback_started, callback_started_connection = process_context.Pipe(duplex=False)
        client = process_context.Process(
            target=cleanup_during_event_callback,
            args=(device_context.get_device_access(), callback_started_connection),
        )
        client.start()
        callback_started_connection.close()
        try:
            assert callback_started.poll(timeout=10), "The event callback did not start"
            callback_started.recv()
            client.join(timeout=5)
            assert client.exitcode is not None, "ApiUtil.cleanup() blocked while the callback was active"
            assert client.exitcode == 0, f"Client exited unexpectedly: {client.exitcode}"
        finally:
            callback_started.close()
            if client.is_alive():
                client.terminate()
                client.join(timeout=2)
                if client.is_alive():
                    client.kill()
                    client.join()


def switch_callback_model_during_async_callback(device_trl, callback_started_connection):
    proxy = DeviceProxy(device_trl)
    api_util = ApiUtil.instance()
    api_util.set_asynch_cb_sub_model(cb_sub_model.PUSH_CALLBACK)
    callback_started = Event()
    callback_finished = Event()

    def callback(event):
        assert not event.err
        callback_started_connection.send(None)
        callback_started.set()
        time.sleep(3)
        callback_finished.set()

    proxy.command_inout_asynch("State", callback)
    assert callback_started.wait(timeout=10)
    api_util.set_asynch_cb_sub_model(cb_sub_model.PULL_CALLBACK)
    api_util.set_asynch_cb_sub_model(cb_sub_model.PUSH_CALLBACK)
    assert callback_finished.wait(timeout=5)
    os._exit(0)  # isolate callback-thread shutdown from client teardown


@pytest.mark.extra_src_test
def test_callback_model_switch_does_not_deadlock_during_async_callback():
    device_context = DeviceTestContext(CleanupEventDevice, process=True)
    with device_context:
        process_context = multiprocessing.get_context("spawn")
        callback_started, callback_started_connection = process_context.Pipe(duplex=False)
        client = process_context.Process(
            target=switch_callback_model_during_async_callback,
            args=(device_context.get_device_access(), callback_started_connection),
        )
        client.start()
        callback_started_connection.close()
        try:
            assert callback_started.poll(timeout=10), "The async callback did not start"
            callback_started.recv()
            client.join(timeout=6)
            assert client.exitcode is not None, "Callback-model switching blocked during the callback"
            assert client.exitcode == 0, f"Client exited unexpectedly: {client.exitcode}"
        finally:
            callback_started.close()
            if client.is_alive():
                client.terminate()
                client.join(timeout=2)
                if client.is_alive():
                    client.kill()
                    client.join()


def query_event_queue_during_initial_callback(device_trl, operation):
    proxy = DeviceProxy(device_trl)
    queued_event_id = proxy.subscribe_event("sample", EventType.CHANGE_EVENT, 10)
    callback_entered = Event()

    def callback(event):
        if not event.err:
            callback_entered.set()
            time.sleep(2)

    subscription_errors = []

    def subscribe():
        try:
            proxy.subscribe_event("sample", EventType.CHANGE_EVENT, callback)
        except Exception as error:
            subscription_errors.append(error)

    subscription = Thread(target=subscribe)
    subscription.start()
    assert callback_entered.wait(timeout=10)
    if operation == "event_queue_size":
        proxy.event_queue_size(queued_event_id)
    elif operation == "is_event_queue_empty":
        proxy.is_event_queue_empty(queued_event_id)
    elif operation == "get_last_event_date":
        proxy.get_last_event_date(queued_event_id)
    elif operation == "get_callback_events":
        proxy.get_events(queued_event_id, lambda event: None)
    else:
        proxy.get_events(queued_event_id)
    subscription.join(timeout=5)
    assert not subscription.is_alive()
    assert not subscription_errors, subscription_errors
    os._exit(0)


@pytest.mark.extra_src_test
@pytest.mark.parametrize(
    "operation",
    ["event_queue_size", "get_events", "get_callback_events", "is_event_queue_empty", "get_last_event_date"],
)
def test_event_queue_query_completes_during_initial_callback(operation):
    context = DeviceTestContext(CleanupEventDevice, process=True)
    with context:
        process_context = multiprocessing.get_context("spawn")
        client = process_context.Process(
            target=query_event_queue_during_initial_callback,
            args=(context.get_device_access(), operation),
        )
        client.start()
        try:
            client.join(timeout=8)
            assert client.exitcode is not None, "Queued-event query blocked during initial callback"
            assert client.exitcode == 0, f"Client exited unexpectedly: {client.exitcode}"
        finally:
            if client.is_alive():
                client.terminate()
                client.join(timeout=2)
                if client.is_alive():
                    client.kill()
                    client.join()
