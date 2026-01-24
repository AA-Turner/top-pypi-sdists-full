# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

import pytest
from tango import AttributeConfig, CmdArgType, DevError, DevFailed, Group, ClientAddr
from tango._tango import GroupAttrReply, GroupCmdReply, GroupReply
from tango.pytango_pprint import _SEQUENCE_TYPES, _STRUCT_TYPES
from tango.server import Device, attribute, command
from tango.test_context import DeviceTestContext


STRUCTS_NOT_INSTANTIABLE_FROM_PYTHON = (
    GroupAttrReply,
    GroupCmdReply,
    GroupReply,
)
TESTABLE_TYPES = set(_STRUCT_TYPES).difference(STRUCTS_NOT_INSTANTIABLE_FROM_PYTHON)


class GroupTestDevice(Device):
    @attribute
    def attr(self) -> float:
        return 12.3

    @attr.setter
    def attr(self, val: float) -> None:
        pass

    @attribute
    def attr_fail(self) -> float:
        raise RuntimeError("Fail for test")

    @attr_fail.setter
    def attr_fail(self, val: float) -> None:
        raise RuntimeError("Fail for test")

    @command
    def cmd_fail(self):
        raise RuntimeError("Fail for test")


@pytest.fixture
def group():
    with DeviceTestContext(GroupTestDevice, device_name="test/device/1"):
        group_client = Group("test")
        group_client.add("test/device/1")
        yield group_client


@pytest.mark.parametrize(
    "to_string, requires_newline",
    [
        (str, True),
        (repr, False),
    ],
)
def test_pprint_structs(to_string, requires_newline):
    for struct_type in TESTABLE_TYPES:
        struct = struct_type()
        s = to_string(struct)
        assert struct_type.__name__ in s
        assert ("\n" in s) == requires_newline


@pytest.mark.parametrize(
    "to_string, requires_newline",
    [
        (str, True),
        (repr, False),
    ],
)
def test_pprint_group_structs(to_string, requires_newline, group):
    group_cmd_reply = group.command_inout("State")[0]
    group_attr_reply = group.read_attribute("attr")[0]
    group_reply = group.write_attribute("attr", 45.6)[0]
    group_cmd_failed_reply = group.command_inout("cmd_fail")[0]
    group_attr_failed_reply = group.read_attribute("attr_fail")[0]
    group_failed_reply = group.write_attribute("attr_fail", 45.6)[0]
    for struct in [
        group_cmd_reply,
        group_attr_reply,
        group_reply,
        group_cmd_failed_reply,
        group_attr_failed_reply,
        group_failed_reply,
    ]:
        s = to_string(struct)
        assert type(struct).__name__ in s
        assert ("\n" in s) == requires_newline


@pytest.mark.parametrize(
    "to_string, requires_newline",
    [
        (str, True),
        (repr, False),
    ],
)
def test_pprint_dev_failed_dev_error(to_string, requires_newline):
    dev_failed = DevFailed(DevError(), DevError())
    s = to_string(dev_failed)
    assert "DevFailed" in s
    assert "DevError" in s
    assert ("\n" in s) == requires_newline


@pytest.mark.parametrize("to_string", [str, repr])
def test_pprint_sequences(to_string):
    for seq_type in _SEQUENCE_TYPES:
        struct = seq_type()
        s = to_string(struct)
        assert "[" in s
        assert "]" in s


def test_pprint_data_type_is_cmd_arg_type():
    config = AttributeConfig()
    for dtype_value in CmdArgType.values:
        config.data_type = dtype_value
        s = str(config)
        assert f"data_type = {CmdArgType(dtype_value)!r}" in s


def test_pprint_client_addr():
    addr = ClientAddr("127.0.0.1")
    s = str(addr)
    assert s == "Client identification not available"
    r = repr(addr)
    assert "ClientAddr" in r
    assert "127.0.0.1" in r
