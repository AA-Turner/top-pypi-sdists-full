# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import time

from tango import (
    AttrConfEventData,
    AttrWriteType,
    DevError,
    DevFailed,
    EventType,
)
from tango.server import Device, attribute, command
from tango.test_utils import DeviceTestContext
from tango.utils import EventCallback

A_BIT = 0.5


class EchoDevice(Device):
    scalar_int_value = 1

    @attribute(access=AttrWriteType.READ_WRITE)
    def scalar_int(self) -> int:
        return self.scalar_int_value

    def write_scalar_int(self, new_value):
        self.scalar_int_value = new_value

    @command(dtype_in=[int])
    def change_min_max(self, values):
        w_attr = self.get_device_attr().get_w_attr_by_name("scalar_int")

        w_attr.set_min_value(values[0])
        w_attr.set_max_value(values[1])


def test_attribute_configuration_event():

    with DeviceTestContext(EchoDevice, process=True) as proxy:
        start_time = time.time()

        cb = EventCallback()

        event_id = proxy.subscribe_event("scalar_int", EventType.ATTR_CONF_EVENT, cb)

        def check_limits(attr_conf_event, min_value, max_value):
            attr_info = attr_conf_event.attr_conf
            assert attr_info.min_value == min_value
            assert attr_info.max_value == max_value

        time.sleep(A_BIT)
        events = cb.get_events()
        assert len(events) == 1
        ev = events[0]
        check_limits(ev, "Not specified", "Not specified")
        assert "scalar_int" in ev.attr_name
        assert ev.event == "attr_conf"
        assert not ev.err
        tv1 = ev.get_date()
        tv2 = ev.reception_date
        assert str(tv1) == str(tv2)
        assert start_time < tv1.totime() < start_time + 2 * A_BIT
        assert ev.errors == ()
        assert ev.device is proxy

        new_limits = [10, 15]
        proxy.change_min_max(new_limits)

        time.sleep(A_BIT)
        assert len(events) == 3
        check_limits(events[1], "10", "Not specified")
        check_limits(events[2], "10", "15")

        proxy.unsubscribe_event(event_id)


def test_attribute_configuration_event_set_errors():

    conf_event = AttrConfEventData()
    conf_event.errors = DevFailed(DevError())
    assert len(conf_event.errors) == 1
