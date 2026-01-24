# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import numpy as np

try:
    import numpy.typing as npt
except ImportError:
    npt = None

import pytest

from typing import Any
from tango import (
    DevFailed,
    PyTangoUserWarning,  # noqa
)
from tango.server import Device
from tango.server import command, device_property, attribute
from tango.test_utils import DeviceTestContext

from tango.test_utils import (
    assert_close,
    convert_dtype_to_typing_hint,
)


def test_device_property_no_default(
    general_typed_values,
):
    dtype, values, expected = general_typed_values
    patched_dtype = dtype if dtype != (bool,) else (int,)
    value = values[1]

    class TestDevice(Device):

        prop_without_db_value = device_property(dtype=dtype)
        prop_with_db_value = device_property(dtype=dtype)

        @command(dtype_out=bool)
        def is_prop_without_db_value_set_to_none(self):
            return self.prop_without_db_value is None

        @command(dtype_out=patched_dtype)
        def get_prop_with_db_value(self):
            return self.prop_with_db_value

    with DeviceTestContext(
        TestDevice, properties={"prop_with_db_value": value}
    ) as proxy:
        assert proxy.is_prop_without_db_value_set_to_none()
        assert_close(proxy.get_prop_with_db_value(), expected(value))


def test_device_property_with_typing(general_typed_values):
    dtype, values, expected = general_typed_values
    patched_dtype = dtype if dtype != (bool,) else (int,)
    value = values[1]

    tuple_hint, list_hint, _, _ = convert_dtype_to_typing_hint(dtype)

    class TestDevice(Device):
        prop_tuple_hint: tuple_hint = device_property()

        prop_list_hint: list_hint = device_property()

        prop_user_type_has_priority: dict = device_property(dtype=dtype)

        @command(dtype_out=patched_dtype)
        def get_prop_tuple_hint(self):
            return self.prop_tuple_hint

        @command(dtype_out=patched_dtype)
        def get_prop_list_hint(self):
            return self.prop_list_hint

        @command(dtype_out=patched_dtype)
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
    patched_dtype = dtype if dtype != (bool,) else (int,)

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

        @command(dtype_out=patched_dtype)
        def get_prop_without_db_value(self):
            return self.prop_without_db_value

        @command(dtype_out=patched_dtype)
        def get_prop_with_db_value(self):
            return self.prop_with_db_value

    with DeviceTestContext(
        TestDevice, properties={"prop_with_db_value": value}
    ) as proxy:
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
        with pytest.raises(DevFailed) as context:
            with DeviceTestContext(TestDevice):
                pass
        assert "Device property prop is mandatory" in str(context.value)
