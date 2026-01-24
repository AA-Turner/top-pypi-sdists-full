# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import pytest

from tango import (
    AttrWriteType,
    DevFailed,
    DeviceData,
    DeviceDataList,
    DevState,
    Group,
    GroupAttrReply,
    GroupCmdReply,
    GroupReply,
    StdStringVector,
)
from tango.server import Device, attribute, command
from tango.test_context import MultiDeviceTestContext
from tango.utils import TO_TANGO_TYPE

_is_allowed = [True]


class SimpleDevice(Device):
    _attr = None

    def init_device(self):
        self._attr = int(self.get_name()[-1])
        super().init_device()
        self.set_state(DevState.ON)

    @attribute(access=AttrWriteType.READ_WRITE)
    def attr(self) -> int:
        return self._attr

    @attr.setter
    def set_attr(self, new_value):
        self._attr = new_value

    @attr.is_allowed
    def is_allowed(self, req) -> bool:
        return _is_allowed[0]

    @command()
    def indent(self, v_in: int) -> int:
        return v_in

    def is_indent_allowed(self) -> bool:
        return _is_allowed[0]


devices_info = (
    {
        "class": SimpleDevice,
        "devices": [{"name": "test/device/1"}, {"name": "test/device/2"}],
    },
)


@pytest.fixture(scope="module")
def context():
    with MultiDeviceTestContext(devices_info) as ctx:
        yield ctx


def test_wrong_device_name(context):
    group = Group("test_group")
    group.add("test/device/1")

    with pytest.raises(KeyError, match="some/wrong/device"):
        group.get_device("some/wrong/device")

    with pytest.raises(KeyError, match="some/wrong/device"):
        group["some/wrong/device"]


def test_nested_multi_group(context):
    group_singles = Group("add-one-at-a-time")
    group_singles.add("test/device/1")
    group_singles.add("test/device/2")
    group_multiples_list = Group("add-multiple-via-list")
    group_multiples_list.add(["test/device/1", "test/device/2"])
    group_multiples_vector = Group("add-multiple-via-std-vector")
    vector = StdStringVector()
    vector.append("test/device/1")
    vector.append("test/device/2")
    group_multiples_vector.add(vector)
    group_in_group = Group("add-sub-group")
    group_in_group.add(group_singles)

    groups = [
        group_singles,
        group_multiples_list,
        group_multiples_vector,
        group_in_group,
    ]

    device1_fqdn = context.get_device_access("test/device/1")
    device2_fqdn = context.get_device_access("test/device/2")
    for group in groups:
        assert device1_fqdn in group
        assert device2_fqdn in group
        reply = group.read_attribute("attr")
        assert reply[0].dev_name() == device1_fqdn
        assert reply[1].dev_name() == device2_fqdn
        assert not reply[0].has_failed()
        assert not reply[1].has_failed()
        assert reply[0].get_data().value == 1
        assert reply[1].get_data().value == 2

    # patterns are not supported via DeviceTestContext
    with pytest.raises(DevFailed):
        group_multiples_pattern = Group("add-multiple-via-pattern")
        group_multiples_pattern.add("test/device/*")


def test_read_write_attribute(context):

    _is_allowed[0] = True

    group = Group("test_group")
    group.add("test/device/1")
    group.add("test/device/2")

    seq = group.write_attribute("attr", 3)

    for ret in seq:
        assert not ret.has_failed()
        assert isinstance(ret, GroupReply)

    seq = group.read_attribute("attr")

    for ret in seq:
        assert not ret.has_failed()
        assert ret.get_data().value == 3
        # we check, that we can read value for the second time
        assert ret.get_data().value == 3
        assert isinstance(ret, GroupAttrReply)

    # now we check that we can iterate over GroupReplyList for the second time
    for ret in seq:
        assert not ret.has_failed()
        assert ret.get_data().value == 3
        assert ret.get_data().value == 3
        assert isinstance(ret, GroupAttrReply)

    dev = group.get_device(1)
    attr_info = dev.get_attribute_config("attr")
    seq = group.write_attribute(attr_info, 4)

    for ret in seq:
        assert not ret.has_failed()
        assert isinstance(ret, GroupReply)

    seq = group.read_attribute("attr")

    for ret in seq:
        assert not ret.has_failed()
        assert ret.get_data().value == 4

    _is_allowed[0] = False

    for ret in group.write_attribute("attr", 5):
        assert ret.has_failed()
        assert (
            ret.get_err_stack()[0].desc
            == "It is currently not allowed to write attribute attr. The device state is ON"
        )

    for ret in group.read_attribute("attr"):
        assert ret.has_failed()
        assert (
            ret.get_err_stack()[0].desc
            == "It is currently not allowed to read attribute attr"
        )


def test_command(context):

    _is_allowed[0] = True

    group = Group("test_group")
    group.add("test/device/1")
    group.add("test/device/2")

    seq = group.command_inout("indent", 1)

    for ret in seq:
        assert not ret.has_failed()
        assert ret.get_data() == 1
        # we check, that we can read value for the second time
        assert ret.get_data() == 1
        assert isinstance(ret, GroupCmdReply)

    # now we check that we can iterate over GroupReplyList for the second time
    for ret in seq:
        assert not ret.has_failed()
        assert ret.get_data() == 1
        assert ret.get_data() == 1
        assert isinstance(ret, GroupCmdReply)

    param = DeviceData()
    param.insert(TO_TANGO_TYPE[int], 1)

    seq = group.command_inout("indent", param)

    for ret in seq:
        assert not ret.has_failed()
        assert ret.get_data() == 1

    param_list = DeviceDataList()
    param_list.extend([param, param])

    seq = group.command_inout("indent", param_list)

    for ret in seq:
        assert not ret.has_failed()
        assert ret.get_data() == 1

    _is_allowed[0] = False

    for ret in group.command_inout("indent", 2):
        assert ret.has_failed()
        assert (
            ret.get_err_stack()[0].desc
            == "Command indent not allowed when the device is in ON state"
        )
