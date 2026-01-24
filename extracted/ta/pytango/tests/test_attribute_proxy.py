# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import sys
import time
from functools import partial

import numpy as np
import pytest

from tango import (
    DevState,
    AttributeProxy,
    GreenMode,
    DevFailed,
    EventType,
    AttrWriteType,
)
from tango.constants import DefaultPollRingDepth
from tango.asyncio import AttributeProxy as asyncio_AttributeProxy
from tango.gevent import AttributeProxy as gevent_AttributeProxy
from tango.futures import AttributeProxy as futures_AttributeProxy

from tango.server import Device, attribute, command

from tango.test_utils import assert_close, DeviceTestContext, MultiDeviceTestContext
from tango.utils import EventCallback, AsyncEventCallback


TEST_VALUES = {
    "scalar_int": (2, 3, 4, 5, 6),
    "spectrum_str": (["c", "d"], ["e", "f"], ["g", "h"], ["i", "j"], ["k", "l"]),
    "image_float": (
        [[15.0, 16.0], [17.0, 18.0]],
        [[19.0, 20.0], [21.0, 22.0]],
        [[23.0, 24.0], [25.0, 26.0]],
        [[27.0, 28.0], [29.0, 30.0]],
        [[31.0, 32.0], [33.0, 34.0]],
    ),
}

ATTRIBUTES_TO_TEST = list(TEST_VALUES.keys())

attribute_proxy_map = {
    GreenMode.Synchronous: AttributeProxy,
    GreenMode.Futures: futures_AttributeProxy,
    GreenMode.Asyncio: partial(asyncio_AttributeProxy, wait=True),
    GreenMode.Gevent: gevent_AttributeProxy,
}

# Tests


class EasyEchoDevice(Device):

    scalar_int_value = 1
    spectrum_str_value = ["a", "b"]
    image_float_value = [[1.0, 2.0], [3.0, 4.0]]

    def init_device(self):
        self.set_state(DevState.ON)

    @attribute(access=AttrWriteType.READ_WRITE)
    def scalar_int(self) -> int:
        return self.scalar_int_value

    @scalar_int.setter
    def set_scalar_int(self, new_value):
        self.scalar_int_value = new_value

    @attribute(access=AttrWriteType.READ_WRITE)
    def spectrum_str(self) -> tuple[str, str]:
        return self.spectrum_str_value

    @spectrum_str.setter
    def set_spectrum_str(self, new_value):
        self.spectrum_str_value = new_value

    @attribute(access=AttrWriteType.READ_WRITE)
    def image_float(self) -> tuple[tuple[float, float], tuple[float, float]]:
        return self.image_float_value

    @image_float.setter
    def set_image_float(self, new_value):
        self.image_float_value = new_value


devices_info = ({"class": EasyEchoDevice, "devices": [{"name": "test/dev/main"}]},)


@pytest.fixture(params=ATTRIBUTES_TO_TEST)
def attribute_proxy(request):
    with MultiDeviceTestContext(devices_info=devices_info):
        proxy = AttributeProxy(f"test/dev/main/{request.param}")
        assert proxy.__repr__() == proxy.__str__() == f"AttributeProxy({request.param})"
        yield proxy


def test_ping(attribute_proxy):
    duration = attribute_proxy.ping(wait=True)
    assert isinstance(duration, int)


def test_state_status(attribute_proxy):
    state = attribute_proxy.state(wait=True)
    assert isinstance(state, DevState)

    status = attribute_proxy.status(wait=True)
    assert status == f"The device is in {state} state."


def test_read_write_attribute(attribute_proxy):
    values = TEST_VALUES[attribute_proxy.name()]
    attribute_proxy.write(values[0], wait=True)
    assert_close(attribute_proxy.read(wait=True).value, values[0])
    assert_close(attribute_proxy.write_read(values[1], wait=True).value, values[1])


def test_attribute_poll(attribute_proxy):
    poll_period = 0.1  # sec
    values = TEST_VALUES[attribute_proxy.name()]
    initial_value = attribute_proxy.read().value
    t_start = time.time()

    _assert_polling_can_be_started(attribute_proxy, poll_period)
    history = _write_values_and_read_via_polling(attribute_proxy, poll_period, values)
    _assert_polling_can_be_stopped(attribute_proxy)
    _assert_reading_times_increase_monotonically(history, t_start)
    _assert_reading_values_valid(history, initial_value, values)


def _assert_polling_can_be_started(attribute_proxy, poll_period_sec):
    poll_period_msec = round(poll_period_sec * 1000)
    assert not attribute_proxy.is_polled()
    attribute_proxy.poll(poll_period_msec)
    assert attribute_proxy.is_polled()
    assert attribute_proxy.get_poll_period() == poll_period_msec


def _assert_polling_can_be_stopped(attribute_proxy):
    attribute_proxy.stop_poll()
    assert not attribute_proxy.is_polled()


def _write_values_and_read_via_polling(attribute_proxy, poll_period_sec, values):
    for value in values:
        attribute_proxy.write(value)
        time.sleep(poll_period_sec)
    assert len(values) <= DefaultPollRingDepth
    history = attribute_proxy.history(DefaultPollRingDepth)
    tolerance_for_slow_ci_runners = 2
    assert len(history) >= len(values) - tolerance_for_slow_ci_runners
    return history


def _assert_reading_times_increase_monotonically(history, t_start):
    t_previous = t_start
    for reading in history:
        t_current = reading.time.totime()
        assert t_current > t_previous
        t_previous = t_current


def _assert_reading_values_valid(history, initial_value, written_values):
    valid_values = _get_comparable_values([initial_value] + list(written_values))
    history_values = _get_comparable_values([reading.value for reading in history])
    last_index = -1
    for history_value in history_values:
        assert history_value in valid_values
        # check that historical values only move forward through the written values
        # i.e. polling buffer may repeat values, but may not return to an earlier value
        index = valid_values.index(history_value)
        assert index >= last_index
        last_index = index


def _get_comparable_values(values):
    comparable_values = []
    for value in values:
        if isinstance(value, tuple):
            value = list(value)
        elif isinstance(value, np.ndarray):
            value = value.tolist()
        comparable_values.append(value)
    return comparable_values


max_reply_attempts = 10
delay = 0.1


def test_read_write_attribute_async(attribute_proxy):
    value = TEST_VALUES[attribute_proxy.name()][0]
    w_id = attribute_proxy.write_asynch(value, wait=True)
    got_reply, attempt = False, 0
    while not got_reply:
        try:
            attribute_proxy.write_reply(w_id, wait=True)
            got_reply = True
        except DevFailed:
            attempt += 1
            if attempt >= max_reply_attempts:
                raise RuntimeError(
                    f"Test failed: cannot get write reply within {max_reply_attempts*delay} sec"
                )
            time.sleep(delay)

    r_id = attribute_proxy.read_asynch(wait=True)
    got_reply, attempt = False, 0
    while not got_reply:
        try:
            ret = attribute_proxy.read_reply(r_id, wait=True)
            got_reply = True
        except DevFailed:
            attempt += 1
            if attempt >= max_reply_attempts:
                raise RuntimeError(
                    f"Test failed: cannot get read reply within {max_reply_attempts*delay} sec"
                )
            time.sleep(delay)

    assert_close(ret.value, value)


class EasyEventDevice(Device):
    def init_device(self):
        self.set_change_event("attr", implemented=True, detect=False)

    @attribute
    def attr(self) -> int:
        return 1

    @command
    def send_event(self):
        self.push_change_event("attr", 2)


@pytest.mark.parametrize("green_mode", GreenMode.values.values(), ids=str)
def test_event(green_mode):
    with DeviceTestContext(EasyEventDevice, device_name="test/device/1", process=True):
        attr_proxy = attribute_proxy_map[green_mode]("test/device/1/attr")
        dev_proxy = attr_proxy.get_device_proxy()
        cb = (
            AsyncEventCallback() if green_mode == GreenMode.Asyncio else EventCallback()
        )
        eid = attr_proxy.subscribe_event(EventType.CHANGE_EVENT, cb, wait=True)
        dev_proxy.command_inout("send_event", wait=True)
        evts = cb.get_events()
        rep = 0
        while len(evts) < 2 and rep < 50:
            if green_mode in {GreenMode.Asyncio, GreenMode.Gevent}:
                # For asyncio and gevent green mode, the event callback is
                # scheduled on the event loop when it arrives.  We have to exercise
                # the event loop so that it gets a chance to invoke the callback.
                # One way to do that is sending a command that we wait for.
                # (For synchronous green mode, the callback will be invoked from
                # another thread so we can just sleep)
                # In a typical asyncio app, we would be awaiting other tasks, so
                # this wouldn't be necessary.
                dev_proxy.command_inout("state", wait=True)
            rep += 1
            evts = cb.get_events()
            time.sleep(0.1)
        if len(evts) < 2:
            pytest.fail(f"Cannot receive events in {green_mode}")
        assert_close([evt.attr_value.value for evt in evts[:2]], [1, 2])
        attr_proxy.unsubscribe_event(eid, wait=True)


@pytest.fixture
def uninitialized_attr_proxy():
    """
    This could happen if there was an exception in the AttributeProxy __init__ method,
    and the user is running through pytest.  pytest will have a reference to the frame
    and try to print out all the objects from the failed test.
    """
    proxy_instance = None
    try:
        AttributeProxy("not/existing/device/attr")
    except DevFailed:
        traceback = sys.exc_info()[2]
        for v in traceback.tb_next.tb_frame.f_locals.values():
            if isinstance(v, AttributeProxy):
                proxy_instance = v

    assert proxy_instance is not None
    yield proxy_instance


def test_pytest_report_on_failed_attribute_proxy_does_not_crash(
    uninitialized_attr_proxy,
):
    safe_repr = repr(uninitialized_attr_proxy)
    assert "AttributeProxy" in safe_repr
    assert "Unknown" in safe_repr

    safe_str = str(uninitialized_attr_proxy)
    assert "AttributeProxy" in safe_str
    assert "Unknown" in safe_str
