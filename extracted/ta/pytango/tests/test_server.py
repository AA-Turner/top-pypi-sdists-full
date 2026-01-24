# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import asyncio
import inspect
import multiprocessing
import os
import sys
import textwrap
import threading
import time

import numpy as np

try:
    import numpy.typing as npt
except ImportError:
    npt = None

import pytest

from collections.abc import Callable

import tango.asyncio
import tango.constants
from tango import (
    AttrData,
    Attr,
    AttrDataFormat,
    AttReqType,
    AttrWriteType,
    CmdArgType,
    DevFailed,
    DevState,
    DeviceClass,
    DeviceProxy,
    EventType,
    GreenMode,
    LatestDeviceImpl,
    EnsureOmniThread,
    LockerLanguage,
)
from tango.server import __to_callback, BaseDevice, Device
from tango.pyutil import parse_args
from tango.server import command, attribute, class_property, device_property
from tango.test_utils import (
    DeviceTestContext,
    MultiDeviceTestContext,
    GoodEnum,
    BadEnumNonZero,
    BadEnumSkipValues,
    BadEnumDuplicates,
    DEVICE_SERVER_ARGUMENTS,
    wait_for_proxy,
)
from tango.utils import (
    EnumTypeError,
    get_enum_labels,
    get_latest_device_class,
    is_pure_str,
    get_tango_type_format,
    parse_type_hint,
)


# Constants
TIMEOUT = 10.0

# Test implementation classes

WRONG_HINTS = (  # hint_caller, type_hint, error_reason
    ("property", tuple[tuple[int]], "Property does not support IMAGE type"),
    (
        "property",
        tuple[tuple[int, float], float],
        "Property does not support IMAGE type",
    ),
    ("property", tuple[int, float], "PyTango does not support mixed types"),
    ("attribute", tuple[int, float], "PyTango does not support mixed types"),
    (
        "attribute",
        tuple[tuple[int, float], float],
        "PyTango does not support mixed types",
    ),
    (
        "attribute",
        tuple[tuple[int, int], list[int, int]],
        "PyTango does not support mixed types",
    ),
    ("attribute", Callable[[int], None], "Cannot translate"),
)


@pytest.mark.parametrize("hint_caller, type_hint, error_reason", WRONG_HINTS)
def test_uncorrect_typing_hints(hint_caller, type_hint, error_reason):
    with pytest.raises(RuntimeError, match=error_reason):
        dtype, dformat, max_x, max_y = parse_type_hint(type_hint, caller=hint_caller)
        get_tango_type_format(dtype, dformat, hint_caller)


@pytest.fixture(params=[GoodEnum])
def good_enum(request):
    return request.param


@pytest.fixture(params=[BadEnumNonZero, BadEnumSkipValues, BadEnumDuplicates])
def bad_enum(request):
    return request.param


# test utilities for servers


def test_get_enum_labels_success(good_enum):
    expected_labels = ["START", "MIDDLE", "END"]
    assert get_enum_labels(good_enum) == expected_labels


def test_get_enum_labels_fail(bad_enum):
    with pytest.raises(EnumTypeError):
        get_enum_labels(bad_enum)


def test_device_classes_use_latest_implementation():
    assert issubclass(LatestDeviceImpl, get_latest_device_class())
    assert issubclass(BaseDevice, LatestDeviceImpl)
    assert issubclass(Device, BaseDevice)


# Test state/status


def test_empty_device(server_green_mode):
    class TestDevice(Device):
        green_mode = server_green_mode

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.state() == DevState.UNKNOWN
        assert proxy.status() == "The device is in UNKNOWN state."


@pytest.mark.parametrize("description_source", ["doc", "description"])
def test_set_desc_status_state_at_init(description_source):
    class TestDevice(Device):
        if description_source == "doc":
            __doc__ = "Test name"
        else:
            # device_class_description has priority
            __doc__ = "Test name 2"
            DEVICE_CLASS_DESCRIPTION = "Test name"
        DEVICE_CLASS_INITIAL_STATUS = "Test status"
        DEVICE_CLASS_INITIAL_STATE = DevState.ON

    class ChildDevice(TestDevice):
        pass

    class SecondChildDevice(TestDevice):
        DEVICE_CLASS_DESCRIPTION = "Test name 2"
        DEVICE_CLASS_INITIAL_STATUS = "Test status 2"
        DEVICE_CLASS_INITIAL_STATE = DevState.OFF

    devices_info = (
        {"class": TestDevice, "devices": [{"name": "test/dev/main"}]},
        {"class": ChildDevice, "devices": [{"name": "test/dev/child1"}]},
        {"class": SecondChildDevice, "devices": [{"name": "test/dev/child2"}]},
    )

    with MultiDeviceTestContext(devices_info) as context:
        for proxy in [
            context.get_device("test/dev/main"),
            context.get_device("test/dev/child1"),
        ]:
            assert proxy.state() == DevState.ON
            assert proxy.status() == "Test status"
            if (
                description_source == "description"
            ):  # note, that docsrting is not inherited!
                assert proxy.description() == "Test name"

        proxy = context.get_device("test/dev/child2")
        assert proxy.state() == DevState.OFF
        assert proxy.status() == "Test status 2"
        assert proxy.description() == "Test name 2"


@pytest.mark.parametrize("force_user_status", [False, True])
def test_set_state_status(state, server_green_mode, force_user_status):
    if force_user_status:
        status = "\n".join(
            (
                "This is a multiline status",
                "with special characters such as",
                "Café à la crème",
            )
        )
    else:
        status = f"The device is in {state} state."

    if server_green_mode == GreenMode.Asyncio:

        class TestDevice(Device):
            green_mode = server_green_mode

            async def init_device(self):
                self.set_state(state)
                if force_user_status:
                    self.set_status(status)

    else:

        class TestDevice(Device):
            green_mode = server_green_mode

            def init_device(self):
                self.set_state(state)
                if force_user_status:
                    self.set_status(status)

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.state() == state
        assert proxy.status() == status


def test_user_dev_state_status(server_green_mode):
    state = DevState.MOVING
    status = "Device is MOVING"

    if server_green_mode == GreenMode.Asyncio:

        class TestDevice(Device):
            green_mode = server_green_mode

            async def dev_state(self):
                return state

            async def dev_status(self):
                return status

    else:

        class TestDevice(Device):
            green_mode = server_green_mode

            def dev_state(self):
                return state

            def dev_status(self):
                return status

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.state() == state
        assert proxy.status() == status


def test_attr_quality_checked_with_state(server_green_mode):
    if server_green_mode == GreenMode.Asyncio:

        class BaseTestDevice(Device):
            @command(dtype_out=bool)
            async def check_sub_function_was_called(self):
                return (
                    self.read_attr_hardware_was_called
                    and self.always_executed_hook_was_called
                )

    else:

        class BaseTestDevice(Device):
            @command(dtype_out=bool)
            def check_sub_function_was_called(self):
                return (
                    self.read_attr_hardware_was_called
                    and self.always_executed_hook_was_called
                )

    class TestDevice(BaseTestDevice):
        green_mode = server_green_mode

        read_attr_hardware_was_called = False
        always_executed_hook_was_called = False

        sync_code = textwrap.dedent(
            """
            def init_device(self):
                Device.init_device(self)
                self.set_state(DevState.ON)

            def read_attr_hardware(self, attr_list):
                self.read_attr_hardware_was_called = True
                return Device.read_attr_hardware(self, attr_list)

            def always_executed_hook(self):
                self.always_executed_hook_was_called = True

            @attribute(max_alarm=0)
            def test_attribute(self):
                return 42
                """
        )

        if server_green_mode == GreenMode.Asyncio:
            exec(
                sync_code.replace("def", "async def").replace("Device", "await Device")
            )
        else:
            exec(sync_code)

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.state() == DevState.ALARM
        assert proxy.check_sub_function_was_called()


def test_device_get_attr_config(server_green_mode):
    class TestDevice(Device):
        # green mode matters to check deadlocks in async modes
        green_mode = server_green_mode

        sync_code = textwrap.dedent(
            """
        @attribute(dtype=bool)
        def attr_config_ok(self):
            # testing that call to get_attribute_config for all types of
            # input arguments gives same result and doesn't raise an exception
            ac1 = self.get_attribute_config("attr_config_ok")
            ac2 = self.get_attribute_config(["attr_config_ok"])
            return repr(ac1) == repr(ac2)
        """
        )

        if server_green_mode == GreenMode.Asyncio:
            exec(sync_code.replace("def", "async def"))
        else:
            exec(sync_code)

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.attr_config_ok


def test_device_set_attr_config(server_green_mode):
    class TestDevice(Device):
        # green mode matters to check deadlocks in async modes
        green_mode = server_green_mode

        sync_code = textwrap.dedent(
            """
        @attribute(dtype=int)
        def attr(self):
            attr_config = self.get_attribute_config("attr")
            attr_config[0].min_value = "-7"
            attr_config[0].min_alarm = "-6"

            attr_config[0].max_alarm = "6"
            attr_config[0].max_value = "7"

            self.set_attribute_config(attr_config)
            assert repr(attr_config) == repr(self.get_attribute_config("attr"))

            with pytest.raises(AttributeError, match="object has no attribute 'lala'"):
                attr_config[0].lala = "7"

            attr_config = self.get_attribute_config_3("attr")
            attr_config[0].min_value = "-5"
            attr_config[0].att_alarm.min_alarm = "-4"
            attr_config[0].att_alarm.min_warning = "-3"

            attr_config[0].att_alarm.max_warning = "3"
            attr_config[0].att_alarm.max_alarm = "4"
            attr_config[0].max_value = "5"

            self.set_attribute_config_3(attr_config)
            assert repr(attr_config) == repr(self.get_attribute_config_3("attr"))

            with pytest.raises(AttributeError, match="object has no attribute 'lala'"):
                attr_config[0].lala = "7"

            attr = self.get_device_attr().get_attr_by_name("attr")

            val = -2
            for f in ["min_alarm", "min_warning", "max_warning", "max_alarm"]:
                getattr(attr, f"set_{f}")(val)
                assert val == getattr(attr, f"get_{f}")()
                val += 1

            return 1
            """
        )

        if server_green_mode == GreenMode.Asyncio:
            exec(sync_code.replace("def", "async def"))
        else:
            exec(sync_code)

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.attr == 1


def test_default_units():
    # testing that, by default tango.constants.UnitNotSpec is set
    # when no unit is specified. For bool, int, float and str dtypes
    class TestDevice(Device):

        @attribute(dtype=bool)
        def attr_bool_ok(self):
            return True

        @attribute(dtype=int)
        def attr_int_ok(self):
            return 1

        @attribute(dtype=float)
        def attr_float_ok(self):
            return 1.0

        @attribute(dtype=str)
        def attr_str_ok(self):
            return "True"

    def assert_attr_bool_ok(dev_proxy):
        config = dev_proxy.get_attribute_config("attr_bool_ok")
        assert config.unit == tango.constants.UnitNotSpec

    def assert_attr_int_ok(dev_proxy):
        config = dev_proxy.get_attribute_config("attr_int_ok")
        assert config.unit == tango.constants.UnitNotSpec

    def assert_attr_float_ok(dev_proxy):
        config = dev_proxy.get_attribute_config("attr_float_ok")
        assert config.unit == tango.constants.UnitNotSpec

    def assert_attr_str_ok(dev_proxy):
        config = dev_proxy.get_attribute_config("attr_str_ok")
        assert config.unit == tango.constants.UnitNotSpec

    with DeviceTestContext(TestDevice) as proxy:
        assert_attr_bool_ok(proxy)
        assert_attr_int_ok(proxy)
        assert_attr_float_ok(proxy)
        assert_attr_str_ok(proxy)


def test_custom_units():
    class TestDevice(Device):

        @attribute(dtype=bool, unit="mA")
        def custom_unit_ok(self):
            return True

    def assert_custom_unit_ok(dev_proxy):
        config = dev_proxy.get_attribute_config("custom_unit_ok")
        assert config.unit == "mA"

    with DeviceTestContext(TestDevice) as proxy:
        assert_custom_unit_ok(proxy)


# Test inheritance


def test_inheritance_overrides_a_property():

    class A(Device):

        dev_prop1 = device_property(dtype=str, default_value="hello_dev1")
        dev_prop2 = device_property(dtype=str, default_value="hello_dev2")
        class_prop1 = class_property(dtype=str, default_value="hello_class1")
        class_prop2 = class_property(dtype=str, default_value="hello_class2")

        @command(dtype_out=str)
        def get_dev_prop1(self):
            return self.dev_prop1

        @command(dtype_out=str)
        def get_dev_prop2(self):
            return self.dev_prop2

        @command(dtype_out=str)
        def get_class_prop1(self):
            return self.class_prop1

        @command(dtype_out=str)
        def get_class_prop2(self):
            return self.class_prop2

    class B(A):
        dev_prop2 = device_property(dtype=str, default_value="goodbye_dev2")
        class_prop2 = class_property(dtype=str, default_value="goodbye_class2")

    devices_info = (
        {"class": A, "devices": [{"name": "test/dev/a"}]},
        {"class": B, "devices": [{"name": "test/dev/b"}]},
    )

    with MultiDeviceTestContext(devices_info) as context:
        proxy_a = context.get_device("test/dev/a")
        proxy_b = context.get_device("test/dev/b")

        assert proxy_a.get_dev_prop1() == "hello_dev1"
        assert proxy_a.get_dev_prop2() == "hello_dev2"
        assert proxy_a.get_class_prop1() == "hello_class1"
        assert proxy_a.get_class_prop2() == "hello_class2"

        assert proxy_b.get_dev_prop1() == "hello_dev1"
        assert proxy_b.get_dev_prop2() == "goodbye_dev2"
        assert proxy_b.get_class_prop1() == "hello_class1"
        assert proxy_b.get_class_prop2() == "goodbye_class2"


def test_inheritance_override_dev_status():
    class A(Device):

        def dev_status(self):
            return ")`'-.,_"

    class B(A):
        def dev_status(self):
            return 3 * A.dev_status(self)

    with DeviceTestContext(B) as proxy:
        assert proxy.status() == ")`'-.,_)`'-.,_)`'-.,_"


def test_inheritance_init_device():

    class A(Device):
        initialised_count_a = 0

        def init_device(self):
            super().init_device()
            self.initialised_count_a += 1

        @command(dtype_out=int)
        def get_is_initialised_a(self):
            return self.initialised_count_a

    class B(A):
        initialised_count_b = 0

        def init_device(self):
            super().init_device()
            self.initialised_count_b += 1

        @command(dtype_out=int)
        def get_is_initialised_b(self):
            return self.initialised_count_b

    with DeviceTestContext(B) as proxy:
        assert proxy.get_is_initialised_a() == 1
        assert proxy.get_is_initialised_b() == 1


def test_inheritance_with_decorated_attributes():
    is_allowed = True

    class A(Device):

        @attribute(access=AttrWriteType.READ_WRITE)
        def decorated_a(self):
            return self.decorated_a_value

        @decorated_a.setter
        def decorated_a(self, value):
            self.decorated_a_value = value

        @decorated_a.is_allowed
        def decorated_a(self, req_type):
            assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
            return is_allowed

    class B(A):
        @attribute(access=AttrWriteType.READ_WRITE)
        def decorated_b(self):
            return self.decorated_b_value

        @decorated_b.setter
        def decorated_b(self, value):
            self.decorated_b_value = value

        @decorated_b.is_allowed
        def decorated_b(self, req_type):
            assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
            return is_allowed

    with DeviceTestContext(B) as proxy:
        is_allowed = True

        proxy.decorated_a = 1.23
        assert proxy.decorated_a == 1.23
        proxy.decorated_b = 4.5
        assert proxy.decorated_b == 4.5

        is_allowed = False
        with pytest.raises(DevFailed):
            proxy.decorated_a = 1.0
        with pytest.raises(DevFailed):
            _ = proxy.decorated_a
        with pytest.raises(DevFailed):
            proxy.decorated_b = 1.0
        with pytest.raises(DevFailed):
            _ = proxy.decorated_b


def test_inheritance_with_undecorated_attributes():
    is_allowed = True

    class A(Device):

        attr_a = attribute(access=AttrWriteType.READ_WRITE)

        def _check_is_allowed(self):
            return is_allowed

        def read_attr_a(self):
            return self.attr_a_value

        def write_attr_a(self, value):
            self.attr_a_value = value

        def is_attr_a_allowed(self, req_type):
            assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
            return self._check_is_allowed()

    class B(A):
        attr_b = attribute(access=AttrWriteType.READ_WRITE)

        def read_attr_b(self):
            return self.attr_b_value

        def write_attr_b(self, value):
            self.attr_b_value = value

        def is_attr_b_allowed(self, req_type):
            assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
            return self._check_is_allowed()

    with DeviceTestContext(B) as proxy:
        is_allowed = True

        proxy.attr_a = 2.5
        assert proxy.attr_a == 2.5
        proxy.attr_b = 5.75
        assert proxy.attr_b == 5.75

        is_allowed = False
        with pytest.raises(DevFailed):
            proxy.attr_a = 1.0
        with pytest.raises(DevFailed):
            _ = proxy.attr_a
        with pytest.raises(DevFailed):
            proxy.attr_b = 1.0
        with pytest.raises(DevFailed):
            _ = proxy.attr_b


def test_inheritance_with_undecorated_attribute_and_bound_methods():

    class A(Device):

        is_allowed = True

        attr_a = attribute(
            access=AttrWriteType.READ_WRITE,
            fget="get_attr_a",
            fset="set_attr_a",
            fisallowed="isallowed_attr_a",
        )

        def get_attr_a(self):
            return self.attr_value

        def set_attr_a(self, value):
            self.attr_value = value

        def isallowed_attr_a(self, req_type):
            assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
            return self.is_allowed

        @command(dtype_in=bool)
        def make_allowed(self, yesno):
            self.is_allowed = yesno

    class B(A):
        attr_b = attribute(
            access=AttrWriteType.READ_WRITE,
            fget="get_attr_b",
            fset="set_attr_b",
            fisallowed="isallowed_attr_b",
        )

        def get_attr_b(self):
            return self.attr_value

        def set_attr_b(self, value):
            self.attr_value = value

        def isallowed_attr_b(self, req_type):
            assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
            return self.is_allowed

    with DeviceTestContext(B) as proxy:
        proxy.attr_a = 3.75
        assert proxy.attr_a == 3.75
        proxy.attr_b = 6.0
        assert proxy.attr_b == 6.0

        proxy.make_allowed(False)
        with pytest.raises(DevFailed):
            proxy.attr_a = 1.0
        with pytest.raises(DevFailed):
            _ = proxy.attr_a
        with pytest.raises(DevFailed):
            proxy.attr_b = 1.0
        with pytest.raises(DevFailed):
            _ = proxy.attr_b


def test_inheritance_with_undecorated_attributes_and_unbound_functions():
    is_allowed = True
    values = {"a": 0.0, "b": 0.0}

    def read_attr_a(device):
        assert isinstance(device, B)
        return values["a"]

    def write_attr_a(device, value):
        assert isinstance(device, B)
        values["a"] = value

    def is_attr_a_allowed(device, req_type):
        assert isinstance(device, B)
        assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
        return is_allowed

    class A(Device):

        attr_a = attribute(
            access=AttrWriteType.READ_WRITE,
            fget=read_attr_a,
            fset=write_attr_a,
            fisallowed=is_attr_a_allowed,
        )

    def read_attr_b(device):
        assert isinstance(device, B)
        return values["b"]

    def write_attr_b(device, value):
        assert isinstance(device, B)
        values["b"] = value

    def is_attr_b_allowed(device, req_type):
        assert isinstance(device, B)
        assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
        return is_allowed

    class B(A):
        attr_b = attribute(
            access=AttrWriteType.READ_WRITE,
            fget=read_attr_b,
            fset=write_attr_b,
            fisallowed=is_attr_b_allowed,
        )

    with DeviceTestContext(B) as proxy:
        is_allowed = True

        proxy.attr_a = 2.5
        assert proxy.attr_a == 2.5
        proxy.attr_b = 5.75
        assert proxy.attr_b == 5.75

        is_allowed = False
        with pytest.raises(DevFailed):
            proxy.attr_a = 1.0
        with pytest.raises(DevFailed):
            _ = proxy.attr_a
        with pytest.raises(DevFailed):
            proxy.attr_b = 1.0
        with pytest.raises(DevFailed):
            _ = proxy.attr_b


def test_inheritance_command_is_allowed_by_naming_convention():

    class A(Device):

        @command(dtype_out=str)
        def cmd(self):
            return "ok"

        def is_cmd_allowed(self):
            return is_allowed

    class B(A):
        pass

    with DeviceTestContext(B) as proxy:
        is_allowed = True
        assert proxy.cmd() == "ok"
        is_allowed = False
        with pytest.raises(DevFailed):
            proxy.cmd()


def test_inheritance_command_is_allowed_by_kwarg_method():

    class A(Device):

        @command(dtype_out=str, fisallowed="fisallowed_kwarg_method")
        def cmd(self):
            return "ok 1"

        def fisallowed_kwarg_method(self):
            return is_allowed

    class B(A):
        pass

    with DeviceTestContext(B) as proxy:
        is_allowed = True
        assert proxy.cmd() == "ok 1"
        is_allowed = False
        with pytest.raises(DevFailed):
            proxy.cmd()


def test_inheritance_command_is_allowed_by_kwarg_unbound_function():
    is_allowed = True

    def fisallowed_function(self):
        return is_allowed

    class A(Device):
        @command(dtype_out=str, fisallowed=fisallowed_function)
        def cmd(self):
            return "ok"

    class B(A):
        pass

    with DeviceTestContext(B) as proxy:
        is_allowed = True
        assert proxy.cmd() == "ok"
        is_allowed = False
        with pytest.raises(DevFailed):
            proxy.cmd()


# Test Exception propagation
def test_exception_propagation(server_green_mode):
    if server_green_mode == GreenMode.Asyncio:

        class TestDevice(Device):
            green_mode = server_green_mode

            @attribute
            async def attr(self):
                1 / 0  # pylint: disable=pointless-statement

            @command
            async def cmd(self):
                1 / 0  # pylint: disable=pointless-statement

    else:

        class TestDevice(Device):
            green_mode = server_green_mode

            @attribute
            def attr(self):
                1 / 0  # pylint: disable=pointless-statement

            @command
            def cmd(self):
                1 / 0  # pylint: disable=pointless-statement

    with DeviceTestContext(TestDevice) as proxy:
        with pytest.raises(DevFailed) as record:
            proxy.attr  # pylint: disable=pointless-statement
        assert "ZeroDivisionError" in record.value.args[0].desc

        with pytest.raises(DevFailed) as record:
            proxy.cmd()
        assert "ZeroDivisionError" in record.value.args[0].desc


def _avoid_double_colon_node_ids(val):
    """Return node IDs without a double colon.

    IDs with "::" can't be used to launch a test from the command line, as pytest
    considers this sequence as a module/test name separator.  Add something extra
    to keep them usable for single test command line execution (e.g., under Windows CI).
    """
    if is_pure_str(val) and "::" in val:
        return str(val).replace("::", ":_:")


@pytest.fixture(params=["linux", "win"])
def os_system(request):
    original_platform = sys.platform
    sys.platform = request.param
    yield
    sys.platform = original_platform


@pytest.mark.parametrize(
    "applicable_os, test_input, expected_output",
    DEVICE_SERVER_ARGUMENTS,
    ids=_avoid_double_colon_node_ids,
)
def test_arguments(applicable_os, test_input, expected_output, os_system):
    try:
        assert set(parse_args(test_input.split())) == set(expected_output)
    except SystemExit:
        assert sys.platform not in applicable_os


# Test Server init hook


def test_server_init_hook_called(server_green_mode):
    if server_green_mode == GreenMode.Asyncio:

        class TestDevice(Device):
            green_mode = server_green_mode
            server_init_hook_called = False

            async def server_init_hook(self):
                await asyncio.sleep(0.01)
                TestDevice.server_init_hook_called = True

    else:

        class TestDevice(Device):
            green_mode = server_green_mode
            server_init_hook_called = False

            def server_init_hook(self):
                TestDevice.server_init_hook_called = True

    with DeviceTestContext(TestDevice):
        assert TestDevice.server_init_hook_called


def test_server_init_hook_change_state():

    class TestDevice(Device):
        def server_init_hook(self):
            self.set_state(DevState.ON)

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.state() == DevState.ON


def test_asyncio_server_init_hook_change_state():
    class TestDevice(Device):
        green_mode = GreenMode.Asyncio

        async def server_init_hook(self):
            await asyncio.sleep(0.01)
            self.set_state(DevState.ON)

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.state() == DevState.ON


def test_server_init_hook_called_after_init():
    class TestDevice(Device):
        def init_device(self):
            self.set_state(DevState.INIT)

        def server_init_hook(self):
            self.set_state(DevState.ON)

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.state() == DevState.ON


def test_async_server_init_hook_called_after_init():
    class TestDevice(Device):
        green_mode = GreenMode.Asyncio

        async def init_device(self):
            await asyncio.sleep(0.01)
            self.set_state(DevState.INIT)

        async def server_init_hook(self):
            await asyncio.sleep(0.01)
            self.set_state(DevState.ON)

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.state() == DevState.ON


def test_server_init_hook_exception():
    class TestDevice(Device):

        def server_init_hook(self):
            self.set_state(DevState.ON)
            raise RuntimeError("Force exception for test")

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.state() == DevState.FAULT


def test_asyncio_server_init_hook_exception():
    class TestDevice(Device):
        green_mode = GreenMode.Asyncio

        async def server_init_hook(self):
            await asyncio.sleep(0.01)
            raise RuntimeError("Force exception for test")

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.state() == DevState.FAULT


def test_server_init_hook_with_low_level_api_called():
    class ClassicAPISimpleDeviceImpl(LatestDeviceImpl):
        has_been_called = False

        def server_init_hook(self):
            self.set_state(DevState.ON)
            ClassicAPISimpleDeviceImpl.has_been_called = True

    class ClassicAPISimpleDeviceClass(DeviceClass):
        pass

    with DeviceTestContext(ClassicAPISimpleDeviceImpl, ClassicAPISimpleDeviceClass):
        assert ClassicAPISimpleDeviceImpl.has_been_called


def test_server_init_hook_with_low_level_api_change_state():
    class ClassicAPISimpleDeviceImpl(LatestDeviceImpl):

        def server_init_hook(self):
            self.set_state(DevState.ON)

    class ClassicAPISimpleDeviceClass(DeviceClass):
        pass

    with DeviceTestContext(
        ClassicAPISimpleDeviceImpl, ClassicAPISimpleDeviceClass
    ) as proxy:
        assert proxy.state() == DevState.ON


def test_server_init_hook_with_low_level_api_called_after_init():
    class ClassicAPISimpleDeviceImpl(LatestDeviceImpl):
        def init_device(self):
            self.set_state(DevState.INIT)

        def server_init_hook(self):
            self.set_state(DevState.ON)

    class ClassicAPISimpleDeviceClass(DeviceClass):
        pass

    with DeviceTestContext(
        ClassicAPISimpleDeviceImpl, ClassicAPISimpleDeviceClass
    ) as proxy:
        assert proxy.state() == DevState.ON


def test_server_init_hook_with_low_level_api_exception():
    class ClassicAPISimpleDeviceImpl(LatestDeviceImpl):

        def server_init_hook(self):
            self.set_state(DevState.ON)
            raise RuntimeError("Force exception for test")

    class ClassicAPISimpleDeviceClass(DeviceClass):
        pass

    with DeviceTestContext(
        ClassicAPISimpleDeviceImpl, ClassicAPISimpleDeviceClass
    ) as proxy:
        assert proxy.state() == DevState.FAULT


def test_server_init_multiple_devices():
    event_list = []

    class DeviceOne(Device):
        def server_init_hook(self):
            event_list.append("DeviceOne")

    class DeviceTwo(Device):
        def server_init_hook(self):
            event_list.append("DeviceTwo")

    devices_info = (
        {"class": DeviceOne, "devices": [{"name": "test/device1/1"}]},
        {
            "class": DeviceTwo,
            "devices": [{"name": "test/device2/1"}, {"name": "test/device3/1"}],
        },
    )

    with MultiDeviceTestContext(devices_info):
        assert len(event_list) == 3
        assert "DeviceOne" in event_list
        assert "DeviceTwo" in event_list


def test_server_init_hook_subscribe_event_multiple_devices():
    pytest.xfail("This test is unreliable - to be fixed soon")

    event_queue = multiprocessing.Queue()

    class DeviceOne(Device):
        @attribute(dtype=int)
        def some_attribute(self):
            return 42

        def init_device(self):
            super().init_device()
            self.set_change_event("some_attribute", implemented=True, detect=False)

        @command
        def push_event_cmd(self):
            self.push_change_event("some_attribute", 43)

    class DeviceTwo(Device):
        def event_handler(self, data):
            event_queue.put(data.attr_value.value)

        def server_init_hook(self):
            self.dev1_proxy = DeviceProxy("test/device1/1")
            self.dev1_proxy.subscribe_event(
                "some_attribute", EventType.CHANGE_EVENT, self.event_handler
            )

    devices_info = (
        {"class": DeviceOne, "devices": [{"name": "test/device1/1"}]},
        {
            "class": DeviceTwo,
            "devices": [{"name": "test/device2/1"}, {"name": "test/device3/1"}],
        },
    )

    with MultiDeviceTestContext(devices_info) as context:
        proxy = context.get_device("test/device1/1")

        # synchronous event
        assert 42 == event_queue.get(timeout=TIMEOUT)
        assert 42 == event_queue.get(timeout=TIMEOUT)
        assert event_queue.empty()

        # asynchronous event pushed from user code
        proxy.push_event_cmd()
        assert 43 == event_queue.get(timeout=TIMEOUT)
        assert 43 == event_queue.get(timeout=TIMEOUT)
        assert event_queue.empty()


def test_deprecation_warning_for_sync_attr_com_methods_in_asyncio_device():
    class TestDevice(Device):
        green_mode = GreenMode.Asyncio
        attr_value = 1

        # static attributes and commands

        @attribute(access=AttrWriteType.READ_WRITE)
        async def attr_all_methods_async(self) -> int:
            return self.attr_value

        @attr_all_methods_async.write
        async def attr_all_methods_async(self, value):
            self.attr_value = value

        @attr_all_methods_async.is_allowed
        async def attr_all_methods_async(self, req_type):
            return True

        @attribute(access=AttrWriteType.READ_WRITE)
        def attr_sync_read_write(self) -> int:
            return self.attr_value

        @attr_sync_read_write.write
        def set_attr_sync_read_write(self, value):
            self.attr_value = value

        @attribute
        async def attr_sync_is_allowed(self) -> int:
            return self.attr_value

        @attr_sync_is_allowed.is_allowed
        def is_attr_sync_is_allowed(self, req_type):
            return True

        @command(dtype_out=int)
        async def cmd_all_methods_async(self, val_in: int) -> int:
            return val_in

        async def is_cmd_all_methods_async_allowed(self):
            return True

        @command(dtype_out=int)
        def cmd_sync_func(self, val_in: int) -> int:
            return val_in

        @command(dtype_out=int)
        async def cmd_sync_is_allowed(self, val_in: int) -> int:
            return val_in

        def is_cmd_sync_is_allowed_allowed(self):
            return True

        # dynamic attributes and commands

        @command
        async def add_dynamic_cmd_attr(self):
            attr = attribute(
                name="dyn_attr_all_methods_async",
                access=AttrWriteType.READ_WRITE,
                fget=self.dyn_attr_all_methods_async,
                fset=self.dyn_set_attr_all_methods_async,
                fisallowed=self.is_dyn_attr_all_methods_async_allowed,
            )
            self.add_attribute(attr)

            attr = attribute(
                name="dyn_attr_sync_read_write",
                access=AttrWriteType.READ_WRITE,
                fget=self.dyn_attr_sync_read_write,
                fset=self.dyn_set_attr_sync_read_write,
            )
            self.add_attribute(attr)

            attr = attribute(
                name="dyn_attr_sync_is_allowed",
                access=AttrWriteType.READ,
                fget=self.dyn_attr_sync_is_allowed,
                fisallowed=self.is_dyn_attr_sync_is_allowed,
            )
            self.add_attribute(attr)

            cmd = command(
                f=self.dyn_cmd_all_methods_async,
                fisallowed=self.is_dyn_cmd_all_methods_async_allowed,
            )
            self.add_command(cmd)

            cmd = command(f=self.dyn_cmd_sync_func)
            self.add_command(cmd)

            cmd = command(
                f=self.dyn_cmd_sync_is_allowed,
                fisallowed=self.is_dyn_cmd_sync_is_allowed_allowed,
            )
            self.add_command(cmd)

        async def dyn_attr_all_methods_async(self, attr) -> int:
            return self.attr_value

        async def dyn_set_attr_all_methods_async(self, attr):
            self.attr_value = attr.get_write_value()

        async def is_dyn_attr_all_methods_async_allowed(self, req_type):
            return True

        def dyn_attr_sync_read_write(self, attr) -> int:
            return self.attr_value

        def dyn_set_attr_sync_read_write(self, attr):
            self.attr_value = attr.get_write_value()

        async def dyn_attr_sync_is_allowed(self, attr) -> int:
            return self.attr_value

        def is_dyn_attr_sync_is_allowed(self, req_type):
            return True

        async def dyn_cmd_all_methods_async(self, val_in: int) -> int:
            return val_in

        async def is_dyn_cmd_all_methods_async_allowed(self):
            return True

        def dyn_cmd_sync_func(self, val_in: int) -> int:
            return val_in

        async def dyn_cmd_sync_is_allowed(self, val_in: int) -> int:
            return val_in

        def is_dyn_cmd_sync_is_allowed_allowed(self):
            return True

    with DeviceTestContext(TestDevice) as proxy:
        proxy.add_dynamic_cmd_attr()

        proxy.attr_all_methods_async = 123
        assert proxy.attr_all_methods_async == 123

        proxy.dyn_attr_all_methods_async = 456
        assert proxy.dyn_attr_all_methods_async == 456

        with pytest.warns(DeprecationWarning):
            proxy.attr_sync_read_write = 123

        with pytest.warns(DeprecationWarning):
            assert proxy.attr_sync_read_write == 123

        with pytest.warns(DeprecationWarning):
            assert proxy.attr_sync_is_allowed == 123

        with pytest.warns(DeprecationWarning):
            proxy.dyn_attr_sync_read_write = 456

        with pytest.warns(DeprecationWarning):
            assert proxy.dyn_attr_sync_read_write == 456

        with pytest.warns(DeprecationWarning):
            assert proxy.dyn_attr_sync_is_allowed == 456

        assert proxy.cmd_all_methods_async(123) == 123

        with pytest.warns(DeprecationWarning):
            assert proxy.cmd_sync_func(123) == 123

        with pytest.warns(DeprecationWarning):
            assert proxy.cmd_sync_is_allowed(123) == 123

        assert proxy.dyn_cmd_all_methods_async(123) == 123

        with pytest.warns(DeprecationWarning):
            assert proxy.dyn_cmd_sync_func(123) == 123

        with pytest.warns(DeprecationWarning):
            assert proxy.dyn_cmd_sync_is_allowed(123) == 123


@pytest.mark.parametrize(
    "method",
    [
        "init_device",
        "delete_device",
        "dev_state",
        "dev_status",
        "read_attr_hardware",
        "always_executed_hook",
    ],
)
def test_deprecation_warning_for_standard_methods_in_asyncio_device(method):
    class TestDevice(Device):
        green_mode = GreenMode.Asyncio

        @attribute
        async def attr(self) -> int:
            return 1

        async_code = textwrap.dedent(
            """
            async def init_device(self):
                pass

            async def delete_device(self):
                pass

            async def dev_state(self):
                return DevState.ON

            async def dev_status(self):
                return "All good"

            async def read_attr_hardware(self, attr_list):
                pass

            async def always_executed_hook(self):
                 pass
             """
        )

        exec(async_code.replace(f"async def {method}", f"def {method}"))

    with pytest.warns(DeprecationWarning, match=method):
        with DeviceTestContext(TestDevice) as proxy:
            _ = proxy.state()
            _ = proxy.status()
            _ = proxy.attr


@pytest.mark.skip(
    reason="This test fails because the first attempt to solve this problem caused a regression and the MR was reverted"
)
def test_no_sync_attribute_locks(server_green_mode):
    """
    Without AttributeMonitor locks, reading attributes while
    simultaneously pushing change events would crash the device
    in NO_SYNC modes: Asyncio and Gevent.
    """

    class BaseTestDevice(Device):
        def __init__(self, *args):
            super().__init__(*args)
            self._last_data = 0.0
            self._publisher = threading.Thread(
                target=self._publisher_thread, name="publisher"
            )
            self._publisher.daemon = True
            self._running = False
            self.set_change_event("H22", implemented=True, detect=False)

        def _publisher_thread(self):
            with EnsureOmniThread():
                while self._running:
                    self._last_data = np.random.rand()
                    super().push_change_event("H22", self._last_data)

    if server_green_mode == GreenMode.Asyncio:

        class TestDevice(BaseTestDevice):
            green_mode = server_green_mode

            @command
            async def Start(self):
                self._running = True
                self._publisher.start()

            @command
            async def Stop(self):
                self._running = False

            @attribute(dtype=float)
            async def H22(self):
                return self._last_data

    else:

        class TestDevice(BaseTestDevice):
            green_mode = server_green_mode

            @command
            def Start(self):
                self._running = True
                self._publisher.start()

            @command
            def Stop(self):
                self._running = False

            @attribute(dtype=float)
            def H22(self):
                return self._last_data

    with DeviceTestContext(TestDevice) as proxy:
        proxy.Start()
        # This loop should be enough to crash the device
        # with previous unpatched code in 99% of the cases
        for _ in range(15):
            proxy.H22
        proxy.Stop()


def test_read_slow_and_fast_attributes_with_asyncio():
    class MyDevice(Device):
        green_mode = GreenMode.Asyncio

        @attribute(dtype=str)
        async def slow(self):
            await asyncio.sleep(1)
            return "slow"

        @attribute(dtype=str)
        async def fast(self):
            return "fast"

    context = DeviceTestContext(MyDevice)
    context.start()
    access = context.get_device_access()
    read_order = []

    def read_slow_attribute():
        proxy = DeviceProxy(access)
        read_order.append(proxy.slow)

    def read_fast_attribute():
        proxy = DeviceProxy(access)
        read_order.append(proxy.fast)

    slow_thread = threading.Thread(target=read_slow_attribute)
    fast_thread = threading.Thread(target=read_fast_attribute)
    slow_thread.start()
    time.sleep(0.5)
    fast_thread.start()

    slow_thread.join()
    fast_thread.join()
    context.stop()

    assert read_order == ["fast", "slow"]


def test_get_version_info_classic_api():
    version_info = dict()

    class ClassicAPIDeviceImpl(LatestDeviceImpl):
        def __init__(self, cl, name):
            super().__init__(cl, name)
            ClassicAPIDeviceImpl.init_device(self)

        def init_device(self):
            version_info.update(self.get_version_info())

    class ClassicAPIClass(DeviceClass):
        pass

    with DeviceTestContext(ClassicAPIDeviceImpl, ClassicAPIClass) as proxy:
        assert "PyTango" in version_info
        assert "NumPy" in version_info
        assert proxy.info().version_info == version_info


def test_get_version_info_high_level_api():
    version_info = dict()

    class TestDevice(Device):
        def init_device(self):
            version_info.update(self.get_version_info())

    with DeviceTestContext(TestDevice) as proxy:
        assert "PyTango" in version_info
        assert "NumPy" in version_info
        assert proxy.info().version_info == version_info


def test_add_version_info_classic_api():
    class ClassicAPIDeviceImpl(LatestDeviceImpl):
        def __init__(self, cl, name):
            super().__init__(cl, name)
            ClassicAPIDeviceImpl.init_device(self)

        def init_device(self):
            self.add_version_info("device_version", "1.0.0")

    class ClassicAPIClass(DeviceClass):
        pass

    with DeviceTestContext(ClassicAPIDeviceImpl, ClassicAPIClass) as proxy:
        assert proxy.info().version_info["device_version"] == "1.0.0"


def test_add_version_info_high_level_api():
    class TestDevice(Device):
        def init_device(self):
            self.add_version_info("device_version", "1.0.0")

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.info().version_info["device_version"] == "1.0.0"


@pytest.mark.extra_src_test
def test_restart_server_command_cpp_and_py(mixed_tango_test_server):
    process, proxy_when_ready = mixed_tango_test_server

    proxy = proxy_when_ready()
    assert proxy.state() == DevState.ON

    proxy.command_inout("RestartServer")

    # after restart the proxy is unavailable for a short time, so we wait again
    proxy = proxy_when_ready()
    time.sleep(0.1)  # give TangoTest some extra time to start

    assert proxy.state() == DevState.ON

    # terminate early so we can verify that there is a clean exit
    process.terminate()
    process.join(timeout=3.0)  # Allow TangoTest time to stop DataGenerator

    assert not process.is_alive()
    assert process.exitcode == 0


def test_restart_simple_server_does_not_crash(server_green_mode):

    class TestDevice(Device):
        pass

    devices_info = ({"class": TestDevice, "devices": [{"name": "device/test/1"}]},)
    with MultiDeviceTestContext(devices_info) as context:
        proxy = context.get_device(context.server_name)
        assert proxy.state() == DevState.ON
        proxy.command_inout("RestartServer")
        time.sleep(0.1)
        new_proxy = wait_for_proxy(context.server_name)
        assert new_proxy.state() == DevState.ON
        assert proxy.state() == DevState.ON


def test_attr_data_default_fwd_properties():

    attr_name = "some_attr"
    class_name = "some_class"
    label_value = "abcd"

    d = {
        "name": attr_name,
        "class_name": class_name,
        "forwarded": True,
        "label": label_value,
    }
    AttrData.from_dict(d)
    # can't query "label" as that is in a private section in cppTango's UserDefaultFwdAttrProp
    pass


def test_attr_data_default_properties():

    attr_name = "some_attr"
    class_name = "some_class"

    d = {
        "name": attr_name,
        "class_name": class_name,
        "forwarded": False,
        "delta_time": 1234,
    }

    attr_data = AttrData.from_dict(d)
    assert attr_data.att_prop.delta_t == "1234"


def test_attr_data_default_properties_throws_on_unknown():

    attr_name = "some_attr"
    class_name = "some_class"

    d = {
        "name": attr_name,
        "class_name": class_name,
        "forwarded": False,
        "memorized": True,
        "I DONT EXIST": None,
    }

    with pytest.raises(DevFailed, match="Wrong definition of attribute"):
        AttrData.from_dict(d)


def test_attr_data_enum_labels():

    attr_name = "some_attr"
    class_name = "some_class"
    label_value_1 = "abcd"
    label_value_2 = "efgh"

    d = {
        "name": attr_name,
        "class_name": class_name,
    }
    attr_data = AttrData.from_dict(d)

    attr_data.set_enum_labels_to_attr_prop([label_value_1])
    assert attr_data.att_prop is not None
    assert attr_data.att_prop.enum_labels == label_value_1

    # set different enum values
    attr_data.set_enum_labels_to_attr_prop([label_value_2])
    assert attr_data.att_prop.enum_labels == label_value_2


def test_attr_data_to_attr():

    attr_name = "some_attr"
    class_name = "some class"
    poll_period = 123

    d = {
        "name": attr_name,
        "class_name": class_name,
        "klass": Attr,
        "memorized": True,
        "fread": "read_method",
        "fwrite": "write_method",
        "polling_period": poll_period,
    }

    attr_data = AttrData.from_dict(d)

    assert attr_data.attr_args is None
    assert attr_data.attr_class is not None

    attr = attr_data.to_attr()

    assert attr.get_memorized()
    assert attr.get_polling_period() == poll_period

    # attr_args != None case
    attr_data.attr_args = [
        attr_data.attr_name,
        attr_data.attr_type,
        attr_data.attr_write,
    ]

    attr = attr_data.to_attr()

    assert attr.get_memorized()
    assert attr.get_polling_period() == poll_period


@pytest.mark.parametrize(
    "attr_info,exception_message",
    [
        ("some string", "Wrong data type for value for describing attribute"),
        ([], "Wrong number of argument for describing attribute"),
        ([1, 2, 3], "Wrong number of argument for describing attribute"),
        ([[1]], "Wrong data type for describing mandatory information"),
        ([[1, 2, 3, 4, 5, 6]], "Wrong data type for describing mandatory information"),
        (
            [["abcd", "abcd", "abcd"]],
            "Wrong data type in attribute argument for attribute",
        ),
        (
            [[CmdArgType.DevDouble, "abcd", "abcd"]],
            "Wrong data format in attribute argument for attribute",
        ),
        (
            [[CmdArgType.DevDouble, AttrDataFormat.SCALAR, "abcd", "abcd"]],
            "Sequence describing mandatory attribute parameters for scalar attribute must have 3 elements",
        ),
        (
            [[CmdArgType.DevDouble, AttrDataFormat.SPECTRUM, "abcd"]],
            "Sequence describing mandatory attribute parameters for spectrum attribute must have 4 elements",
        ),
        (
            [[CmdArgType.DevDouble, AttrDataFormat.SPECTRUM, "abcd", "abcd"]],
            "mandatory dim_x attribute parameter for spectrum attribute must be an integer",
        ),
        (
            [[CmdArgType.DevDouble, AttrDataFormat.IMAGE, "abcd", "abcd"]],
            "Sequence describing mandatory attribute parameters for image attribute must have 5 elements",
        ),
        (
            [[CmdArgType.DevDouble, AttrDataFormat.IMAGE, "abcd", "abcd", "abcd"]],
            "mandatory dim_x attribute parameter for image attribute must be an integer",
        ),
        (
            [[CmdArgType.DevDouble, AttrDataFormat.IMAGE, "abcd", 1, "abcd"]],
            "mandatory dim_y attribute parameter for image attribute must be an integer",
        ),
        (
            [[CmdArgType.DevDouble, AttrDataFormat.SCALAR, "abcd"]],
            "Wrong data write type in attribute argument",
        ),
        (
            [
                [CmdArgType.DevDouble, AttrDataFormat.SCALAR, AttrWriteType.READ],
                {"display level": "unknown"},
            ],
            "Wrong display level",
        ),
        (
            [
                [CmdArgType.DevDouble, AttrDataFormat.SCALAR, AttrWriteType.READ],
                {"polling period": "unknown"},
            ],
            "Wrong polling period",
        ),
        (
            [
                [CmdArgType.DevDouble, AttrDataFormat.SCALAR, AttrWriteType.READ],
                {"memorized": "unknown"},
            ],
            "Wrong memorized value",
        ),
        (
            [[CmdArgType.DevEnum, AttrDataFormat.SCALAR, AttrWriteType.READ], {}],
            "Missing 'enum_labels' key in attr_list definition",
        ),
    ],
)
def test_from_attr_info_exceptions(attr_info, exception_message):

    attr_name = "some_attr"
    class_name = "some_class"

    with pytest.raises(DevFailed, match=exception_message):
        AttrData(attr_name, class_name, attr_info=attr_info)


def test_from_attr_info_hw_memorized():

    attr_name = "some_attr"
    class_name = "some_class"

    attr_info = [
        [CmdArgType.DevDouble, AttrDataFormat.SCALAR, AttrWriteType.READ],
        {"memorized": "TRUE"},
    ]
    attr_data = AttrData(attr_name, class_name, attr_info=attr_info)
    assert attr_data.memorized
    assert attr_data.hw_memorized


def test_from_attr_info_memorized():

    attr_name = "some_attr"
    class_name = "some_class"

    attr_info = [
        [CmdArgType.DevDouble, AttrDataFormat.SCALAR, AttrWriteType.READ],
        {"memorized": "true_without_hard_applied"},
    ]
    attr_data = AttrData(attr_name, class_name, attr_info=attr_info)
    assert attr_data.memorized
    assert not attr_data.hw_memorized


# The following devices and fixture used to force rare segfault, when Device used as fixture
class BaseFixtureDevice(Device):
    def init_device(self):
        self.driver = self.create_driver()

    @command
    def cmd(self):
        raise RuntimeError("Bad command")

    def update_callback(self, data):
        pass


@pytest.fixture
def mocked_driver():
    return {}


@pytest.fixture
def TestFixtureDevice(mocked_driver):
    class D(BaseFixtureDevice):
        def create_driver(self):
            mocked_driver["callback"] = self.update_callback
            return mocked_driver

    return D


def test_device_repr_does_not_segfault_with_pytest(mocked_driver, TestFixtureDevice):
    with DeviceTestContext(TestFixtureDevice) as dp:
        with pytest.raises(DevFailed):
            dp.cmd()


def test_client_ident(server_green_mode):

    class MyDevice(Device):

        green_mode = server_green_mode

        if server_green_mode == GreenMode.Asyncio:

            @command()
            async def test_client_ident(self):
                self.assert_client_ident_is_none_for_non_sync_servers()

        elif server_green_mode == GreenMode.Gevent:

            @command()
            def test_client_ident(self):
                self.assert_client_ident_is_none_for_non_sync_servers()

        else:

            @command()
            def test_client_ident(self):
                self.assert_client_ident_valid()

        def assert_client_ident_valid(self):
            data = self.get_client_ident()
            assert data.client_ident
            assert data.client_lang == LockerLanguage.CPP_6
            assert data.client_pid == os.getpid()
            assert data.client_ip == "collocated client (c++ to c++ call)"
            data2 = self.get_client_ident()
            assert data2 == data

        def assert_client_ident_is_none_for_non_sync_servers(self):
            assert self.get_client_ident() is None

    with DeviceTestContext(MyDevice) as dev:
        dev.test_client_ident()


@pytest.mark.asyncio
async def test___to_callback():

    def callback1():
        return "called"

    def callback2(a, b):
        return f"called {a=}, {b=}"

    def callback3(a, b, c=0):
        return f"called {a=}, {b=}, {c=}"

    cb = __to_callback(None, "None-becomes-callable", GreenMode.Synchronous)
    assert callable(cb)

    cb = __to_callback(callback1, "callable", GreenMode.Synchronous)
    assert callable(cb)
    assert cb() == "called"

    cb = __to_callback([callback1], "seq-length-1", GreenMode.Synchronous)
    assert callable(cb)
    assert cb() == "called"

    args = (1, 2)
    cb = __to_callback([callback2, args], "seq-length-2", GreenMode.Synchronous)
    assert callable(cb)
    assert cb() == "called a=1, b=2"

    kwargs = {"c": 3}
    cb = __to_callback([callback3, args, kwargs], "seq-length-3", GreenMode.Synchronous)
    assert callable(cb)
    assert cb() == "called a=1, b=2, c=3"

    with pytest.raises(TypeError):
        _ = __to_callback({}, "wrong-type", GreenMode.Synchronous)

    with pytest.raises(TypeError):
        _ = __to_callback([], "seq-length-0", GreenMode.Synchronous)

    with pytest.raises(TypeError):
        _ = __to_callback(["invalid"], "seq-length-1-bad-type", GreenMode.Synchronous)

    with pytest.raises(TypeError):
        _ = __to_callback([callback1, [], {}, 4], "seq-length-4", GreenMode.Synchronous)

    cb = __to_callback(callback1, "sync-func-becomes-coroutine", GreenMode.Asyncio)
    assert inspect.iscoroutinefunction(cb)
    result = await cb()
    assert result == "called"

    cb = __to_callback(asyncio.sleep, "coroutine-unchanged", GreenMode.Asyncio)
    assert cb is asyncio.sleep


def test_no_crash_when_error_in_delete_device(capfd):

    class TestDevice(Device):
        def delete_device(self):
            raise RuntimeError("Don't crash please")

    with DeviceTestContext(TestDevice) as dev:
        dev.ping()

    _, err = capfd.readouterr()

    assert "delete_device() raised a DevFailed exception" in err
    assert "RuntimeError: Don't crash please" in err


def test_polling_configuration():
    class TestDevice(Device):

        def init_device(self):
            # check polling from attribute/command definition
            assert self.is_attribute_polled("attr")
            assert self.get_attribute_poll_period("attr") == 1000
            assert self.is_command_polled("cmd")
            assert self.get_command_poll_period("cmd") == 2000

            # check polling can be changed
            self.poll_attribute("attr", 1100)
            assert self.is_attribute_polled("attr")
            assert self.get_attribute_poll_period("attr") == 1100
            self.poll_command("cmd", 2100)
            assert self.is_command_polled("cmd")
            assert self.get_command_poll_period("cmd") == 2100

            # check polling can be stopped
            self.stop_poll_attribute("attr")
            assert not self.is_attribute_polled("attr")
            self.stop_poll_command("cmd")
            assert not self.is_command_polled("cmd")

            # restart polling for client to check
            self.poll_attribute("attr", 1200)
            self.poll_command("cmd", 2200)

        @attribute(polling_period=1000)
        def attr(self) -> int:
            return 55

        @command(polling_period=2000)
        def cmd(self):
            pass

    with DeviceTestContext(TestDevice) as proxy:
        # check polling enabled
        assert proxy.is_attribute_polled("attr")
        assert proxy.get_attribute_poll_period("attr") == 1200
        assert proxy.is_command_polled("cmd")
        assert proxy.get_command_poll_period("cmd") == 2200
        # check polling can be stopped
        proxy.stop_poll_attribute("attr")
        assert not proxy.is_attribute_polled("attr")
        proxy.stop_poll_command("cmd")
        assert not proxy.is_command_polled("cmd")
