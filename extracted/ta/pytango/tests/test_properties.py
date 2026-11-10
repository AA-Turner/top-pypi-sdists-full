# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
from typing import Any, ClassVar

import numpy as np

try:
    import numpy.typing as npt
except ImportError:
    npt = None

import pytest

import tango
from tango import (
    DevFailed,
    DevString,
    DevVoid,
    PyTangoUserWarning,  # noqa
)
from tango.server import Device, attribute, class_property, command, device_property
from tango.test_utils import (
    ClassicAPISimpleDeviceClass,
    ClassicAPISimpleDeviceImpl,
    DeviceTestContext,
    MultiDeviceTestContext,
    assert_close,
    convert_dtype_to_typing_hint,
)


def test_device_property_no_default(
    general_typed_values,
):
    dtype, values, expected = general_typed_values
    value = values[1]

    class TestDevice(Device):
        prop_without_db_value = device_property(dtype=dtype)
        prop_with_db_value = device_property(dtype=dtype)

        @command(dtype_out=bool)
        def is_prop_without_db_value_set_to_none(self):
            return self.prop_without_db_value is None

        @command(dtype_out=dtype)
        def get_prop_with_db_value(self):
            return self.prop_with_db_value

    with DeviceTestContext(TestDevice, properties={"prop_with_db_value": value}) as proxy:
        assert proxy.is_prop_without_db_value_set_to_none()
        assert_close(proxy.get_prop_with_db_value(), expected(value))


def test_device_property_with_typing(general_typed_values):
    dtype, values, expected = general_typed_values
    value = values[1]

    tuple_hint, list_hint, _, _ = convert_dtype_to_typing_hint(dtype)

    class TestDevice(Device):
        prop_tuple_hint: tuple_hint = device_property()

        prop_list_hint: list_hint = device_property()

        prop_user_type_has_priority: dict = device_property(dtype=dtype)

        @command(dtype_out=dtype)
        def get_prop_tuple_hint(self):
            return self.prop_tuple_hint

        @command(dtype_out=dtype)
        def get_prop_list_hint(self):
            return self.prop_list_hint

        @command(dtype_out=dtype)
        def get_prop_user_type_has_priority(self):
            return self.prop_user_type_has_priority

    with DeviceTestContext(
        TestDevice,
        properties={
            "prop_tuple_hint": value,
            "prop_list_hint": value,
            "prop_user_type_has_priority": value,
        },
    ) as proxy:
        assert_close(proxy.get_prop_tuple_hint(), expected(value))
        assert_close(proxy.get_prop_list_hint(), expected(value))
        assert_close(proxy.get_prop_user_type_has_priority(), expected(value))


if npt:

    def test_device_property_with_numpy_typing(command_numpy_typed_values):
        type_hint, dformat, value, expected = command_numpy_typed_values
        if type_hint in [np.uint8, npt.NDArray[np.uint8]]:
            pytest.xfail("Does not work for some reason")

        class TestDevice(Device):
            prop: type_hint = device_property()

            @command(dformat_out=dformat)
            def get_prop(self) -> type_hint:
                return self.prop

        with DeviceTestContext(TestDevice, properties={"prop": value}) as proxy:
            assert_close(proxy.get_prop(), expected(value))


@pytest.mark.parametrize("input_type", [str, Any])
def test_device_property_with_default_value(general_typed_values, input_type):
    dtype, values, expected = general_typed_values

    if isinstance(input_type, str) and isinstance(values[0], list):
        default_set = [str(v) for v in values[0]]
    elif isinstance(input_type, str):
        default_set = str(values[0])
    else:
        default_set = values[0]
    default_expected = values[0]
    value = values[1]

    class TestDevice(Device):
        prop_without_db_value = device_property(dtype=dtype, default_value=default_set)
        prop_with_db_value = device_property(dtype=dtype, default_value=default_set)

        @command(dtype_out=dtype)
        def get_prop_without_db_value(self):
            return self.prop_without_db_value

        @command(dtype_out=dtype)
        def get_prop_with_db_value(self):
            return self.prop_with_db_value

    with DeviceTestContext(TestDevice, properties={"prop_with_db_value": value}) as proxy:
        assert_close(proxy.get_prop_without_db_value(), expected(default_expected))
        assert_close(proxy.get_prop_with_db_value(), expected(value))


def test_device_get_device_properties_when_init_device():
    class TestDevice(Device):
        _got_properties = False

        def get_device_properties(self, *args, **kwargs):
            super().get_device_properties(*args, **kwargs)
            self._got_properties = True

        @attribute(dtype=bool)
        def got_properties(self):
            return self._got_properties

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.got_properties


def test_old_api_get_device_properties_before_base_init_without_device_properties():
    class TestDeviceClass(ClassicAPISimpleDeviceClass):
        class_property_list: ClassVar = {"class_prop": [DevString, "", ["cls_default"]]}
        device_property_list: ClassVar = {}
        cmd_list: ClassVar = {"get_class_prop": [[DevVoid, ""], [DevString, ""]]}

    class TestDeviceImpl(ClassicAPISimpleDeviceImpl):
        def __init__(self, cl, name):
            self._base_initialised = False
            self.get_device_properties(self.get_device_class())
            tango.LatestDeviceImpl.__init__(self, cl, name)
            self._base_initialised = True
            self.init_device()

        def get_name(self):
            # Calling the C++ method before DeviceImpl.__init__ is undefined behaviour
            if not self._base_initialised:
                raise RuntimeError("get_name() called before DeviceImpl.__init__")
            return super().get_name()

        def get_class_prop(self):
            return self.class_prop

    with DeviceTestContext(TestDeviceImpl, TestDeviceClass) as proxy:
        assert proxy.get_class_prop() == "cls_default"


def test_single_with_device_property_initialised_from_class_property():

    class TestDevice(Device):
        prop_set_at_class_level_no_default = device_property(dtype=str)
        prop_set_at_class_level_with_default = device_property(dtype=str, default_value="default")
        prop_set_at_device_level_no_default = device_property(dtype=str)
        prop_set_at_device_level_with_default = device_property(dtype=str, default_value="default")

        @command(dtype_out=str)
        def get_prop_set_at_class_level_no_default(self):
            return self.prop_set_at_class_level_no_default

        @command(dtype_out=str)
        def get_prop_set_at_class_level_with_default(self):
            return self.prop_set_at_class_level_with_default

        @command(dtype_out=str)
        def get_prop_set_at_device_level_no_default(self):
            return self.prop_set_at_device_level_no_default

        @command(dtype_out=str)
        def get_prop_set_at_device_level_with_default(self):
            return self.prop_set_at_device_level_with_default

        @command
        def reset_file_database(self):
            tango.Util.instance().get_database().reread_filedatabase()
            tango.Util.instance().reset_filedatabase()

    context = DeviceTestContext(
        TestDevice,
        class_properties={
            "prop_set_at_class_level_no_default": "cls_no_default",
            "prop_set_at_class_level_with_default": "cls_with_default",
            "prop_set_at_device_level_no_default": "cls_no_default",
            "prop_set_at_device_level_with_default": "cls_with_default",
        },
        properties={
            "prop_set_at_device_level_no_default": "dev_no_default",
            "prop_set_at_device_level_with_default": "dev_with_default",
        },
    )
    with context as proxy:
        assert proxy.get_prop_set_at_class_level_no_default() == "cls_no_default"
        assert proxy.get_prop_set_at_class_level_with_default() == "cls_with_default"
        assert proxy.get_prop_set_at_device_level_no_default() == "dev_no_default"
        assert proxy.get_prop_set_at_device_level_with_default() == "dev_with_default"

        tango.Database(context.db).put_class_property(
            TestDevice.__name__,
            {
                "prop_set_at_class_level_no_default": "updated_cls_no_default",
                "prop_set_at_class_level_with_default": "updated_cls_with_default",
                "prop_set_at_device_level_no_default": "updated_cls_no_default",
                "prop_set_at_device_level_with_default": "updated_cls_with_default",
            },
        )
        proxy.reset_file_database()
        proxy.Init()

        assert proxy.get_prop_set_at_class_level_no_default() == "updated_cls_no_default"
        assert proxy.get_prop_set_at_class_level_with_default() == "updated_cls_with_default"
        assert proxy.get_prop_set_at_device_level_no_default() == "dev_no_default"
        assert proxy.get_prop_set_at_device_level_with_default() == "dev_with_default"


def test_single_old_api_with_device_property_initialised_from_class_property():

    class TestDeviceClass(ClassicAPISimpleDeviceClass):
        cmd_list: ClassVar = {
            "get_prop_set_at_class_level_no_default": [[DevVoid, ""], [DevString, ""]],
            "get_prop_set_at_class_level_with_default": [[DevVoid, ""], [DevString, ""]],
            "get_prop_set_at_device_level_no_default": [[DevVoid, ""], [DevString, ""]],
            "get_prop_set_at_device_level_with_default": [[DevVoid, ""], [DevString, ""]],
            "get_prop_both_class_and_device_no_default": [[DevVoid, ""], [DevString, ""]],
            "get_prop_both_class_and_device_with_class_default": [[DevVoid, ""], [DevString, ""]],
            "get_prop_both_class_and_device_with_class_and_device_default": [[DevVoid, ""], [DevString, ""]],
            "get_prop_both_class_and_device_with_device_default": [[DevVoid, ""], [DevString, ""]],
            "get_prop_both_class_and_device_with_none_class_default_repr": [
                [DevVoid, ""],
                [tango.DevString, ""],
            ],
            "reset_file_database": [[DevVoid, ""], [DevVoid, ""]],
        }
        class_property_list: ClassVar = {
            "prop_both_class_and_device_no_default": [DevString, "", []],
            "prop_both_class_and_device_with_class_default": [DevString, "", ["cls_default"]],
            "prop_both_class_and_device_with_class_and_device_default": [DevString, "", ["cls_default"]],
            "prop_both_class_and_device_with_device_default": [DevString, "", []],
            "prop_both_class_and_device_with_none_class_default": [tango.DevLong, "", None],
        }
        device_property_list: ClassVar = {
            "prop_set_at_class_level_no_default": [DevString, "", []],
            "prop_set_at_class_level_with_default": [DevString, "", ["default"]],
            "prop_set_at_device_level_no_default": [DevString, "", []],
            "prop_set_at_device_level_with_default": [DevString, "", ["default"]],
            "prop_both_class_and_device_no_default": [DevString, "", []],
            "prop_both_class_and_device_with_class_default": [DevString, "", None],
            "prop_both_class_and_device_with_class_and_device_default": [DevString, "", ["dev_default"]],
            "prop_both_class_and_device_with_device_default": [DevString, "", ["dev_default"]],
            "prop_both_class_and_device_with_none_class_default": [tango.DevLong, "", []],
        }

    class TestDeviceImpl(ClassicAPISimpleDeviceImpl):
        def get_prop_set_at_class_level_no_default(self):
            return self.prop_set_at_class_level_no_default

        def get_prop_set_at_class_level_with_default(self):
            return self.prop_set_at_class_level_with_default

        def get_prop_set_at_device_level_no_default(self):
            return self.prop_set_at_device_level_no_default

        def get_prop_set_at_device_level_with_default(self):
            return self.prop_set_at_device_level_with_default

        def get_prop_both_class_and_device_no_default(self):
            return self.prop_both_class_and_device_no_default

        def get_prop_both_class_and_device_with_class_default(self):
            return self.prop_both_class_and_device_with_class_default

        def get_prop_both_class_and_device_with_class_and_device_default(self):
            return self.prop_both_class_and_device_with_class_and_device_default

        def get_prop_both_class_and_device_with_device_default(self):
            return self.prop_both_class_and_device_with_device_default

        def get_prop_both_class_and_device_with_none_class_default_repr(self):
            return repr(self.prop_both_class_and_device_with_none_class_default)

        def reset_file_database(self):
            tango.Util.instance().get_database().reread_filedatabase()
            tango.Util.instance().reset_filedatabase()

    context = DeviceTestContext(
        TestDeviceImpl,
        TestDeviceClass,
        class_properties={
            "prop_set_at_class_level_no_default": "cls_no_default",
            "prop_set_at_class_level_with_default": "cls_with_default",
            "prop_set_at_device_level_no_default": "cls_no_default",
            "prop_set_at_device_level_with_default": "cls_with_default",
            "prop_both_class_and_device_no_default": "cls_dev_no_default",
        },
        properties={
            "prop_set_at_device_level_no_default": "dev_no_default",
            "prop_set_at_device_level_with_default": "dev_with_default",
            "prop_both_class_and_device_no_default": "dev_no_default",
        },
    )
    with context as proxy:
        assert proxy.get_prop_set_at_class_level_no_default() == "cls_no_default"
        assert proxy.get_prop_set_at_class_level_with_default() == "cls_with_default"
        assert proxy.get_prop_set_at_device_level_no_default() == "dev_no_default"
        assert proxy.get_prop_set_at_device_level_with_default() == "dev_with_default"

        assert proxy.get_prop_both_class_and_device_no_default() == "dev_no_default"
        assert proxy.get_prop_both_class_and_device_with_class_default() == "cls_default"
        assert proxy.get_prop_both_class_and_device_with_class_and_device_default() == "cls_default"
        assert proxy.get_prop_both_class_and_device_with_device_default() == "dev_default"
        assert proxy.get_prop_both_class_and_device_with_none_class_default_repr() == "[]"

        tango.Database(context.db).put_class_property(
            TestDeviceImpl.__name__,
            {
                "prop_set_at_class_level_no_default": "updated_cls_no_default",
                "prop_set_at_class_level_with_default": "updated_cls_with_default",
                "prop_set_at_device_level_no_default": "updated_cls_no_default",
                "prop_set_at_device_level_with_default": "updated_cls_with_default",
            },
        )
        proxy.reset_file_database()
        proxy.Init()

        assert proxy.get_prop_set_at_class_level_no_default() == "updated_cls_no_default"
        assert proxy.get_prop_set_at_class_level_with_default() == "updated_cls_with_default"
        assert proxy.get_prop_set_at_device_level_no_default() == "dev_no_default"
        assert proxy.get_prop_set_at_device_level_with_default() == "dev_with_default"


def test_multi_with_device_property_initialised_from_class_property():

    class TestDeviceA(Device):
        cls_prop = class_property(dtype=str, default_value="cls_default_a")
        prop_set_at_class_level_no_default = device_property(dtype=str)
        prop_set_at_class_level_with_default = device_property(dtype=str, default_value="default_a")
        prop_set_at_device_level_no_default = device_property(dtype=str)
        prop_set_at_device_level_with_default = device_property(dtype=str, default_value="default_a")

        @command(dtype_out=str)
        def get_prop_set_at_class_level_no_default(self):
            return self.prop_set_at_class_level_no_default

        @command(dtype_out=str)
        def get_prop_set_at_class_level_with_default(self):
            return self.prop_set_at_class_level_with_default

        @command(dtype_out=str)
        def get_prop_set_at_device_level_no_default(self):
            return self.prop_set_at_device_level_no_default

        @command(dtype_out=str)
        def get_prop_set_at_device_level_with_default(self):
            return self.prop_set_at_device_level_with_default

        @command
        def reset_file_database(self):
            tango.Util.instance().get_database().reread_filedatabase()
            tango.Util.instance().reset_filedatabase()

    class TestDeviceB(TestDeviceA):
        cls_prop = class_property(dtype=str, default_value="cls_default_b")
        prop_set_at_class_level_with_default = device_property(dtype=str, default_value="default_b")
        prop_set_at_device_level_with_default = device_property(dtype=str, default_value="default_b")

    devices_info = (
        {
            "class": TestDeviceA,
            "class_properties": {
                "prop_set_at_class_level_no_default": "cls_no_default_a",
                "prop_set_at_class_level_with_default": "cls_with_default_a",
                "prop_set_at_device_level_no_default": "cls_no_default_a",
                "prop_set_at_device_level_with_default": "cls_with_default_a",
            },
            "devices": [
                {
                    "name": "test/device/1",
                    "properties": {
                        "prop_set_at_device_level_no_default": "dev_no_default_1",
                        "prop_set_at_device_level_with_default": "dev_with_default_1",
                    },
                },
                {
                    "name": "test/device/2",
                    "properties": {
                        "prop_set_at_device_level_no_default": "dev_no_default_2",
                        "prop_set_at_device_level_with_default": "dev_with_default_2",
                    },
                },
            ],
        },
        {
            "class": TestDeviceB,
            "class_properties": {
                "prop_set_at_class_level_no_default": "cls_no_default_b",
                "prop_set_at_class_level_with_default": "cls_with_default_b",
                "prop_set_at_device_level_no_default": "cls_no_default_b",
                "prop_set_at_device_level_with_default": "cls_with_default_b",
            },
            "devices": [
                {
                    "name": "test/device/3",
                    "properties": {
                        "prop_set_at_device_level_no_default": "dev_no_default_3",
                        "prop_set_at_device_level_with_default": "dev_with_default_3",
                    },
                }
            ],
        },
    )
    with MultiDeviceTestContext(devices_info) as context:
        devices = [
            (context.get_device("test/device/1"), "a", "1"),
            (context.get_device("test/device/2"), "a", "2"),
            (context.get_device("test/device/3"), "b", "3"),
        ]
        for proxy, class_suffix, device_suffix in devices:
            assert proxy.get_prop_set_at_class_level_no_default() == f"cls_no_default_{class_suffix}"
            assert proxy.get_prop_set_at_class_level_with_default() == f"cls_with_default_{class_suffix}"
            assert proxy.get_prop_set_at_device_level_no_default() == f"dev_no_default_{device_suffix}"
            assert proxy.get_prop_set_at_device_level_with_default() == f"dev_with_default_{device_suffix}"

        db = tango.Database(context.db)
        for device_class, value_suffix in [(TestDeviceA, "a"), (TestDeviceB, "b")]:
            db.put_class_property(
                device_class.__name__,
                {
                    "prop_set_at_class_level_no_default": f"updated_cls_no_default_{value_suffix}",
                    "prop_set_at_class_level_with_default": f"updated_cls_with_default_{value_suffix}",
                    "prop_set_at_device_level_no_default": f"updated_cls_no_default_{value_suffix}",
                    "prop_set_at_device_level_with_default": f"updated_cls_with_default_{value_suffix}",
                },
            )

        devices[0][0].reset_file_database()
        for proxy, class_suffix, device_suffix in devices:
            proxy.Init()
            assert proxy.get_prop_set_at_class_level_no_default() == f"updated_cls_no_default_{class_suffix}"
            assert proxy.get_prop_set_at_class_level_with_default() == f"updated_cls_with_default_{class_suffix}"
            assert proxy.get_prop_set_at_device_level_no_default() == f"dev_no_default_{device_suffix}"
            assert proxy.get_prop_set_at_device_level_with_default() == f"dev_with_default_{device_suffix}"


def test_multi_device_property_array_from_class_database_is_isolated():

    class TestDevice(Device):
        prop = device_property(dtype=(str,))

        @command(dtype_out=(str,))
        def get_prop_values(self):
            return self.prop

        @command(dtype_in=str)
        def append_prop_value(self, value):
            # we don't expect users will append to properties like this,
            # but it still shouldn't affect other instances in the server
            self.prop.append(value)

    devices_info = (
        {
            "class": TestDevice,
            "class_properties": {"prop": ["one", "two"]},
            "devices": [
                {"name": "test/device/1"},
                {"name": "test/device/2"},
            ],
        },
    )
    with MultiDeviceTestContext(devices_info) as context:
        first = context.get_device("test/device/1")
        second = context.get_device("test/device/2")

        first.append_prop_value("three")

        assert list(first.get_prop_values()) == ["one", "two", "three"]
        assert list(second.get_prop_values()) == ["one", "two"]


def test_multi_device_property_array_from_class_default_is_isolated():
    class TestDeviceClass(ClassicAPISimpleDeviceClass):
        cmd_list: ClassVar = {
            "get_prop_values": [[DevVoid, ""], [tango.DevVarStringArray, ""]],
            "append_prop_value": [[DevString, ""], [DevVoid, ""]],
        }
        class_property_list: ClassVar = {
            "prop": [tango.DevVarStringArray, "", ["one", "two"]],
        }
        device_property_list: ClassVar = {
            "prop": [tango.DevVarStringArray, "", []],
        }

    class TestDeviceImpl(ClassicAPISimpleDeviceImpl):
        def get_prop_values(self):
            return self.prop

        def append_prop_value(self, value):
            # we don't expect users will append to properties like this,
            # but it still shouldn't affect other instances in the server
            self.prop.append(value)

    devices_info = (
        {
            "class": (TestDeviceClass, TestDeviceImpl),
            "devices": [
                {"name": "test/device/1"},
                {"name": "test/device/2"},
            ],
        },
    )
    with MultiDeviceTestContext(devices_info) as context:
        first = context.get_device("test/device/1")
        second = context.get_device("test/device/2")

        first.append_prop_value("three")

        assert list(first.get_prop_values()) == ["one", "two", "three"]
        assert list(second.get_prop_values()) == ["one", "two"]


@pytest.mark.parametrize("set_default", [True, False])
def test_mandatory_device_property_with_db_value_succeeds(set_default):

    class TestDevice(Device):
        prop = device_property(dtype=int, mandatory=True)

        @command(dtype_out=int)
        def get_prop(self):
            return self.prop

    if set_default:
        with DeviceTestContext(TestDevice, properties={"prop": 1}) as proxy:
            assert proxy.get_prop() == 1
    else:
        with pytest.raises(DevFailed, match="Device property prop is mandatory"), DeviceTestContext(TestDevice):
            pass


def test_mandatory_device_property_with_class_db_value_succeeds():
    class TestDevice(Device):
        prop = device_property(dtype=int, mandatory=True)

        @command(dtype_out=int)
        def get_prop(self):
            return self.prop

    with DeviceTestContext(TestDevice, class_properties={"prop": 1}) as proxy:
        assert proxy.get_prop() == 1


@pytest.mark.parametrize("d_type", [bool, (bool,)])
def test_wrong_bool_property_raises(d_type):

    class TestDevice(Device):
        prop = device_property(dtype=d_type)

    with (
        pytest.raises(DevFailed, match="Failed to convert property 'prop' of device 'test/nodb/testdevice'"),
        DeviceTestContext(TestDevice, properties={"prop": ["true, true"]}),
    ):
        pass


@pytest.mark.parametrize("d_type", [bool, (bool,)])
def test_wrong_bool_device_property_from_class_db_raises(d_type):
    class TestDevice(Device):
        prop = device_property(dtype=d_type)

    with (
        pytest.raises(DevFailed, match="Failed to convert property 'prop' of class 'TestDevice'"),
        DeviceTestContext(TestDevice, class_properties={"prop": ["invalid, value"]}),
    ):
        pass
