# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import re
import os
import textwrap
import time
import enum

import psutil

import numpy as np

try:
    import numpy.typing as npt
except ImportError:
    npt = None

import pytest

import tango.asyncio
import tango.constants
from tango import (
    AttrData,
    Attr,
    AttrDataFormat,
    AttrQuality,
    AttReqType,
    AttrWriteType,
    Attribute,
    CmdArgType,
    DevBoolean,
    DevLong,
    DevDouble,
    DevFailed,
    DevEncoded,
    DevEnum,
    DevState,
    DevVoid,
    Device_4Impl,
    Device_5Impl,
    Device_6Impl,
    DeviceClass,
    ExtractAs,
    GreenMode,
    LatestDeviceImpl,
    MultiClassAttribute,
    READ_WRITE,
    SCALAR,
    SPECTRUM,
    EncodedAttribute,
    PyTangoUserWarning,  # noqa
    Util,
    WAttribute,
)
from tango.green import get_executor
from tango.pyutil import TimedAttrData
from tango.server import Device
from tango.server import command, attribute
from tango.test_utils import (
    DeviceTestContext,
    GoodEnum,
    general_decorator,
    general_asyncio_decorator,  # noqa
    assert_close,
    check_attr_type,
    check_read_attr,
    make_nd_value,
    convert_dtype_to_typing_hint,
    UTF8_STRING,
)
from tango.utils import (
    FROM_TANGO_TO_NUMPY_TYPE,
    TO_TANGO_TYPE,
    get_enum_labels,
    is_pure_str,
    get_tango_type_format,
)


@pytest.mark.parametrize("return_time_quality", [True, False])
def test_read_write_attribute_all_types(attribute_typed_values, return_time_quality):
    dtype, values, expected = attribute_typed_values

    class TestDevice(Device):
        _is_allowed = None

        @attribute(
            dtype=dtype, max_dim_x=3, max_dim_y=3, access=AttrWriteType.READ_WRITE
        )
        def attr(self):
            if return_time_quality:
                return self.attr_value, time.time(), AttrQuality.ATTR_VALID
            else:
                return self.attr_value

        @attr.write
        def attr(self, value):
            self.attr_value = value

    with DeviceTestContext(TestDevice) as proxy:
        for value in values:
            proxy.attr = value
            assert_close(proxy.attr, expected(value))


def test_read_write_attribute_with_green_modes(server_green_mode):
    if server_green_mode == GreenMode.Asyncio:

        class TestDevice(Device):
            green_mode = server_green_mode
            _is_allowed = None
            attr_value = None

            @attribute(dtype=int, access=AttrWriteType.READ_WRITE)
            async def attr(self):
                return self.attr_value

            @attr.write
            async def attr(self, value):
                self.attr_value = value

            async def is_attr_allowed(self, req_type):
                assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
                return self._is_allowed

            @command(dtype_in=bool)
            async def make_allowed(self, yesno):
                self._is_allowed = yesno

    else:

        class TestDevice(Device):
            green_mode = server_green_mode
            _is_allowed = None
            attr_value = None

            @attribute(dtype=int, access=AttrWriteType.READ_WRITE)
            def attr(self):
                return self.attr_value

            @attr.write
            def attr(self, value):
                self.attr_value = value

            def is_attr_allowed(self, req_type):
                assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
                return self._is_allowed

            @command(dtype_in=bool)
            def make_allowed(self, yesno):
                self._is_allowed = yesno

    with DeviceTestContext(TestDevice) as proxy:
        proxy.make_allowed(True)
        proxy.attr = 1
        assert proxy.attr == 1

        proxy.make_allowed(False)
        with pytest.raises(DevFailed):
            proxy.attr = 1
        with pytest.raises(DevFailed):
            _ = proxy.attr


def test_wrong_encoding_string():
    class TestDevice(Device):
        @attribute(dtype=str)
        def wrong_string(self):
            return "�"

    with DeviceTestContext(TestDevice) as proxy:
        with pytest.raises(DevFailed, match="UnicodeError"):
            _ = proxy.wrong_string


@pytest.mark.parametrize("return_time_quality", [True, False])
def test_attribute_declared_with_typing(attribute_typed_values, return_time_quality):
    dtype, values, expected = attribute_typed_values
    tuple_hint, list_hint, check_x_dim, check_y_dim = convert_dtype_to_typing_hint(
        dtype
    )

    if return_time_quality:
        tuple_hint = tuple[tuple_hint, float, AttrQuality]
        list_hint = list[list_hint, float, AttrQuality]

    class TestDevice(Device):
        attr_value = None

        hint_with_tuple: tuple_hint = attribute(
            access=AttrWriteType.READ_WRITE, fget="read_attr", fset="write_attr"
        )

        user_size_priority_over_hint: tuple_hint = attribute(
            max_dim_x=5,
            max_dim_y=5,
            access=AttrWriteType.READ_WRITE,
            fget="read_attr",
            fset="write_attr",
        )

        hint_with_list: list_hint = attribute(
            max_dim_x=5,
            max_dim_y=5,
            access=AttrWriteType.READ_WRITE,
            fget="read_attr",
            fset="write_attr",
        )

        def read_attr(self):
            if return_time_quality:
                return self.attr_value, time.time(), AttrQuality.ATTR_VALID
            return self.attr_value

        def write_attr(self, value):
            self.attr_value = value

        @attribute(access=AttrWriteType.READ_WRITE)
        def attribute_tuple_hint(self) -> tuple_hint:
            if return_time_quality:
                return self.attr_value, time.time(), AttrQuality.ATTR_VALID
            return self.attr_value

        @attribute_tuple_hint.write
        def attribute_tuple_hint(self, value):
            self.attr_value = value

        @attribute(access=AttrWriteType.READ_WRITE)
        @general_decorator
        def attribute_with_decorated_read_method(self) -> tuple_hint:
            if return_time_quality:
                return self.attr_value, time.time(), AttrQuality.ATTR_VALID
            return self.attr_value

        @attribute_with_decorated_read_method.write
        def attribute_with_decorated_read_method(self, value):
            self.attr_value = value

        @attribute(access=AttrWriteType.READ_WRITE)
        def attribute_tuple_hint_in_write(self):
            if return_time_quality:
                return self.attr_value, time.time(), AttrQuality.ATTR_VALID
            return self.attr_value

        @attribute_tuple_hint_in_write.write
        def attribute_tuple_hint_in_write(self, value: tuple_hint):
            self.attr_value = value

        @attribute(access=AttrWriteType.READ_WRITE)
        def attribute_hint_in_decorated_write_method(self):
            if return_time_quality:
                return self.attr_value, time.time(), AttrQuality.ATTR_VALID
            return self.attr_value

        @attribute_hint_in_decorated_write_method.write
        @general_decorator
        def attribute_hint_in_decorated_write_method(self, value: tuple_hint):
            self.attr_value = value

        @attribute(access=AttrWriteType.READ_WRITE, max_dim_x=5, max_dim_y=5)
        def attribute_user_size_priority_over_hint(self) -> tuple_hint:
            if return_time_quality:
                return self.attr_value, time.time(), AttrQuality.ATTR_VALID
            return self.attr_value

        @attribute_user_size_priority_over_hint.write
        def attribute_user_size_priority_over_hint(self, value):
            self.attr_value = value

        @attribute(access=AttrWriteType.READ_WRITE, max_dim_x=5, max_dim_y=5)
        def attribute_list_hint(self) -> list_hint:
            if return_time_quality:
                return self.attr_value, time.time(), AttrQuality.ATTR_VALID
            return self.attr_value

        @attribute_list_hint.write
        def attribute_list_hint(self, value: tuple_hint):
            self.attr_value = value

        @command()
        def reset(self):
            self.attr_value = None

    def check_attribute_with_size(proxy, attr, value, size_x, size_y):
        setattr(proxy, attr, value)
        assert_close(getattr(proxy, attr), expected(value))
        conf = proxy.get_attribute_config(attr)
        if check_x_dim:
            assert conf.max_dim_x == size_x
        if check_y_dim:
            assert conf.max_dim_y == size_y
        proxy.reset()

    with DeviceTestContext(TestDevice) as proxy:
        for value in values:
            check_attribute_with_size(proxy, "hint_with_tuple", value, 3, 4)
            check_attribute_with_size(
                proxy, "user_size_priority_over_hint", value, 5, 5
            )
            check_attribute_with_size(proxy, "hint_with_list", value, 5, 5)
            check_attribute_with_size(proxy, "attribute_tuple_hint", value, 3, 4)
            check_attribute_with_size(
                proxy, "attribute_with_decorated_read_method", value, 3, 4
            )
            check_attribute_with_size(
                proxy, "attribute_tuple_hint_in_write", value, 3, 4
            )
            check_attribute_with_size(
                proxy, "attribute_hint_in_decorated_write_method", value, 3, 4
            )
            check_attribute_with_size(
                proxy, "attribute_user_size_priority_over_hint", value, 5, 5
            )
            check_attribute_with_size(proxy, "attribute_list_hint", value, 5, 5)


def test_attribute_self_typed_with_not_defined_name():
    _value = [None]

    def non_bound_read(device: "TestDevice") -> int:
        return _value[0]

    def non_bound_read_no_return_hint(device: "TestDevice"):
        return _value[0]

    def non_bound_write(device: "TestDevice", val_in: int):
        _value[0] = val_in

    class TestDevice(Device):
        _value = None

        assignment_attr: int = attribute(
            access=AttrWriteType.READ_WRITE, fget="read_attr", fset="write_attr"
        )

        non_bound_attr: int = attribute(
            access=AttrWriteType.READ_WRITE, fget=non_bound_read, fset=non_bound_write
        )

        non_bound_attr_in_write: int = attribute(
            access=AttrWriteType.READ_WRITE,
            fget=non_bound_read_no_return_hint,
            fset=non_bound_write,
        )

        def read_attr(self: "TestDevice"):
            return self._value

        def write_attr(self: "TestDevice", val_in):
            self._value = val_in

        @attribute
        def decorator_attr(self: "TestDevice") -> int:
            return self._value

        @decorator_attr.write
        def set_value(self: "TestDevice", val_in: int):
            self._value = val_in

        @attribute
        def decorator_attr_def_in_write(self: "TestDevice"):
            return self._value

        @decorator_attr_def_in_write.write
        def set_value_2(self: "TestDevice", val_in: int):
            self._value = val_in

    with DeviceTestContext(TestDevice) as proxy:
        proxy.assignment_attr = 1
        assert 1 == proxy.assignment_attr
        proxy.decorator_attr = 2
        assert 2 == proxy.decorator_attr
        proxy.decorator_attr_def_in_write = 3
        assert 3 == proxy.decorator_attr_def_in_write

        proxy.non_bound_attr = 1
        assert 1 == proxy.non_bound_attr
        proxy.non_bound_attr_in_write = 2
        assert 2 == proxy.non_bound_attr_in_write


def test_read_write_attribute_with_unbound_functions():
    v = {"attr": None}
    is_allowed = None

    def read_attr(device):
        assert isinstance(device, TestDevice)
        return v["attr"]

    def write_attr(device, val):
        assert isinstance(device, TestDevice)
        v["attr"] = val

    def is_attr_allowed(device, req_type):
        assert isinstance(device, TestDevice)
        assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
        return is_allowed

    class TestDevice(Device):

        attr = attribute(
            fget=read_attr,
            fset=write_attr,
            fisallowed=is_attr_allowed,
            dtype=int,
            access=AttrWriteType.READ_WRITE,
        )

    with DeviceTestContext(TestDevice) as proxy:
        is_allowed = True
        proxy.attr = 123
        assert proxy.attr == 123

        is_allowed = False
        with pytest.raises(DevFailed):
            proxy.attr = 123
        with pytest.raises(DevFailed):
            _ = proxy.attr


def test_read_write_attribute_decorated_methods(server_green_mode):
    if server_green_mode == GreenMode.Asyncio:

        class BaseTestDevice(Device):
            @command(dtype_in=bool)
            async def make_allowed(self, yesno):
                self.is_allowed = yesno

    else:

        class BaseTestDevice(Device):
            @command(dtype_in=bool)
            def make_allowed(self, yesno):
                self.is_allowed = yesno

    class TestDevice(BaseTestDevice):
        green_mode = server_green_mode

        attr_value = None
        is_allowed = None

        attr = attribute(dtype=int, access=AttrWriteType.READ_WRITE)

        sync_code = textwrap.dedent(
            """
        @general_decorator
        def read_attr(self):
            return self.attr_value

        @general_decorator
        def write_attr(self, value):
            self.attr_value = value

        @general_decorator
        def is_attr_allowed(self, req_type):
            assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
            return self.is_allowed
        """
        )

        if server_green_mode == GreenMode.Asyncio:
            exec(
                sync_code.replace("def", "async def").replace(
                    "general_decorator", "general_asyncio_decorator"
                )
            )
        else:
            exec(sync_code)

    with DeviceTestContext(TestDevice) as proxy:
        proxy.make_allowed(True)
        proxy.attr = 123
        assert proxy.attr == 123

        proxy.make_allowed(False)
        with pytest.raises(DevFailed):
            proxy.attr = 123
        with pytest.raises(DevFailed):
            _ = proxy.attr


def test_read_write_wvalue_attribute(attribute_typed_values):
    dtype, values, expected = attribute_typed_values

    class TestDevice(Device):
        value = None

        attr = attribute(
            dtype=dtype, max_dim_x=3, max_dim_y=3, access=AttrWriteType.READ_WRITE
        )

        def read_attr(self):
            return self.value

        def write_attr(self, value):
            self.value = value
            w_attr = self.get_device_attr().get_w_attr_by_name("attr")
            w_attr.set_write_value(value)

    with DeviceTestContext(TestDevice) as proxy:
        for value in values:
            proxy.attr = value
            assert_close(proxy.attr, expected(proxy.read_attribute("attr").w_value))


def test_get_set_attribute_value_warning_and_alarm_thresholds():

    class TestDevice(Device):

        @attribute(
            dtype=int,
            min_value=-21,
            min_alarm=-11,
            min_warning=-1,
            max_warning=1,
            max_alarm=11,
            max_value=21,
        )
        def attr(self):
            return 0

        @attr.setter
        def attr(self, value):
            pass

        @command()
        def check_limits(self):
            multi_attr = self.get_device_attr()
            attr = multi_attr.get_attr_by_name("attr")

            assert attr.get_min_alarm() == -11
            assert attr.get_max_alarm() == 11
            attr.set_min_alarm(-12)
            attr.set_max_alarm(12)
            assert attr.get_min_alarm() == -12
            assert attr.get_max_alarm() == 12

            assert attr.get_min_warning() == -1
            assert attr.get_max_warning() == 1
            attr.set_min_warning(-2)
            attr.set_max_warning(2)
            assert attr.get_min_warning() == -2
            assert attr.get_max_warning() == 2

            w_attr = multi_attr.get_w_attr_by_name("attr")
            assert w_attr.get_min_value() == -21
            assert w_attr.get_max_value() == 21
            w_attr.set_min_value(-22)
            w_attr.set_max_value(22)
            assert w_attr.get_min_value() == -22
            assert w_attr.get_max_value() == 22

    with DeviceTestContext(TestDevice) as proxy:
        proxy.check_limits()


@pytest.mark.parametrize(
    "input_values",
    [[[], []], [np.empty((0)), np.empty((0, 0))], [np.array([]), np.array([])]],
    ids=["list", "np.empty", "np.array"],
)
def test_write_read_empty_spectrum_image_attribute(extract_as, base_type, input_values):
    requested_type, expected_type = extract_as
    spectrum_value, image_value = input_values

    if requested_type == ExtractAs.Numpy and base_type is str:
        expected_type = tuple

    if (
        requested_type in [ExtractAs.ByteArray, ExtractAs.Bytes, ExtractAs.String]
        and base_type is str
    ):
        pytest.xfail(
            "Conversion from (str,) to ByteArray, Bytes and String not supported. May be fixed in future"
        )

    class TestDevice(Device):
        attr_spectrum_value = spectrum_value
        attr_image_value = image_value

        @attribute(dtype=(base_type,), max_dim_x=3, access=AttrWriteType.READ_WRITE)
        def attr_spectrum(self):
            return self.attr_spectrum_value

        @attr_spectrum.write
        def attr_spectrum(self, value):
            self.attr_spectrum_value = value

        @attribute(
            dtype=((base_type,),),
            max_dim_x=3,
            max_dim_y=3,
            access=AttrWriteType.READ_WRITE,
        )
        def attr_image(self):
            return self.attr_image_value

        @attr_image.write
        def attr_image(self, value):
            self.attr_image_value = value

        @command()
        def check_attr_is_empty_list(self):
            if base_type in [int, float, bool]:
                expected_numpy_type = FROM_TANGO_TO_NUMPY_TYPE[TO_TANGO_TYPE[base_type]]
                assert self.attr_spectrum_value.dtype == np.dtype(expected_numpy_type)
                assert self.attr_image_value.dtype == np.dtype(expected_numpy_type)
            else:
                assert isinstance(self.attr_spectrum_value, list)
                assert isinstance(self.attr_image_value, list)
            assert len(self.attr_spectrum_value) == 0
            assert len(self.attr_image_value) == 0

    with DeviceTestContext(TestDevice) as proxy:
        # first we read init value
        attr_read = proxy.read_attribute("attr_spectrum", extract_as=requested_type)
        assert isinstance(attr_read.value, expected_type)
        assert len(attr_read.value) == 0
        attr_read = proxy.read_attribute("attr_image", extract_as=requested_type)
        assert isinstance(attr_read.value, expected_type)
        assert len(attr_read.value) == 0
        # then we write empty list and check if it was really written
        proxy.attr_spectrum = spectrum_value
        proxy.attr_image = image_value
        proxy.check_attr_is_empty_list()
        # and finally, we read it again and check the value and wvalue
        attr_read = proxy.read_attribute("attr_spectrum", extract_as=requested_type)
        assert isinstance(attr_read.value, expected_type)
        assert len(attr_read.value) == 0
        assert isinstance(attr_read.w_value, expected_type)
        assert len(attr_read.w_value) == 0
        attr_read = proxy.read_attribute("attr_image", extract_as=requested_type)
        assert isinstance(attr_read.value, expected_type)
        assert len(attr_read.value) == 0
        assert isinstance(attr_read.w_value, expected_type)
        assert len(attr_read.w_value) == 0


@pytest.mark.parametrize(
    "device_impl_class", [Device_4Impl, Device_5Impl, Device_6Impl, LatestDeviceImpl]
)
def test_write_read_empty_spectrum_attribute_classic_api(
    device_impl_class, extract_as, base_type
):
    requested_type, expected_type = extract_as

    if requested_type == ExtractAs.Numpy and base_type is str:
        expected_type = tuple

    if (
        requested_type in [ExtractAs.ByteArray, ExtractAs.Bytes, ExtractAs.String]
        and base_type is str
    ):
        pytest.xfail(
            "Conversion from (str,) to ByteArray, Bytes and String not supported. May be fixed in future"
        )

    class ClassicAPIClass(DeviceClass):
        cmd_list = {"check_attr_is_empty_list": [[DevVoid, "none"], [DevVoid, "none"]]}
        attr_list = {
            "attr": [[TO_TANGO_TYPE[base_type], SPECTRUM, AttrWriteType.READ_WRITE, 10]]
        }

        def __init__(self, name):
            super().__init__(name)
            self.set_type("TestDevice")

    class ClassicAPIDeviceImpl(device_impl_class):
        attr_value = []

        def read_attr(self, attr):
            attr.set_value(self.attr_value)

        def write_attr(self, attr):
            w_value = attr.get_write_value()
            self.attr_value = w_value

        def check_attr_is_empty_list(self):
            if base_type in [int, float, bool]:
                expected_numpy_type = FROM_TANGO_TO_NUMPY_TYPE[TO_TANGO_TYPE[base_type]]
                assert self.attr_value.dtype == np.dtype(expected_numpy_type)
            else:
                assert isinstance(self.attr_value, list)
            assert len(self.attr_value) == 0

    with DeviceTestContext(ClassicAPIDeviceImpl, ClassicAPIClass) as proxy:
        # first we read init value
        attr_read = proxy.read_attribute("attr", extract_as=requested_type)
        assert isinstance(attr_read.value, expected_type)
        assert len(attr_read.value) == 0
        # then we write empty list and check if it was really written
        proxy.attr = []
        proxy.check_attr_is_empty_list()
        # and finally, we read it again and check the value and wvalue
        attr_read = proxy.read_attribute("attr", extract_as=requested_type)
        assert isinstance(attr_read.value, expected_type)
        assert len(attr_read.value) == 0
        assert isinstance(attr_read.w_value, expected_type)
        assert len(attr_read.w_value) == 0


@pytest.mark.parametrize("dtype", ["state", DevState, CmdArgType.DevState])
def test_ensure_devstate_is_pytango_enum(attr_data_format, dtype):
    if attr_data_format == AttrDataFormat.SCALAR:
        value = DevState.ON
    elif attr_data_format == AttrDataFormat.SPECTRUM:
        dtype = (dtype,)
        value = (DevState.ON, DevState.RUNNING)
    else:
        dtype = ((dtype,),)
        value = ((DevState.ON, DevState.RUNNING), (DevState.UNKNOWN, DevState.MOVING))

    class TestDevice(Device):
        @attribute(dtype=dtype, access=AttrWriteType.READ, max_dim_x=3, max_dim_y=3)
        def any_name_for_state_attribute(self):
            return value

    with DeviceTestContext(TestDevice) as proxy:
        states = proxy.any_name_for_state_attribute
        assert states == value
        if attr_data_format == AttrDataFormat.SCALAR:
            assert states is value
        check_attr_type(states, attr_data_format, DevState)


def test_read_write_attribute_enum(attr_data_format):
    values = [member.value for member in GoodEnum]
    enum_labels = get_enum_labels(GoodEnum)

    if attr_data_format == AttrDataFormat.SCALAR:
        good_type = GoodEnum
        good_type_str = "DevEnum"
    elif attr_data_format == AttrDataFormat.SPECTRUM:
        good_type = (GoodEnum,)
        good_type_str = ("DevEnum",)
    else:
        good_type = ((GoodEnum,),)
        good_type_str = (("DevEnum",),)

    class TestDevice(Device):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if attr_data_format == AttrDataFormat.SCALAR:
                self.attr_from_enum_value = 0
                self.attr_from_labels_value = 0
            elif attr_data_format == AttrDataFormat.SPECTRUM:
                self.attr_from_enum_value = (0,)
                self.attr_from_labels_value = (0,)
            else:
                self.attr_from_enum_value = ((0,),)
                self.attr_from_labels_value = ((0,),)

        attr_from_enum = attribute(
            dtype=good_type, max_dim_x=3, max_dim_y=3, access=AttrWriteType.READ_WRITE
        )

        attr_from_labels = attribute(
            dtype=good_type_str,
            max_dim_x=3,
            max_dim_y=3,
            enum_labels=enum_labels,
            access=AttrWriteType.READ_WRITE,
        )

        def read_attr_from_enum(self):
            return self.attr_from_enum_value

        def write_attr_from_enum(self, value):
            self.attr_from_enum_value = value

        def read_attr_from_labels(self):
            return self.attr_from_labels_value

        def write_attr_from_labels(self, value):
            self.attr_from_labels_value = value

    with DeviceTestContext(TestDevice) as proxy:
        # test assigning values (ints)
        for value, label in zip(values, enum_labels):
            nd_value = make_nd_value(value, attr_data_format)
            proxy.attr_from_enum = nd_value
            read_attr = proxy.attr_from_enum
            assert read_attr == nd_value
            check_attr_type(read_attr, attr_data_format, enum.IntEnum)
            check_read_attr(read_attr, attr_data_format, value, label)

            proxy.attr_from_labels = nd_value
            read_attr = proxy.attr_from_labels
            assert read_attr == nd_value
            check_attr_type(read_attr, attr_data_format, enum.IntEnum)
            check_read_attr(read_attr, attr_data_format, value, label)

        # test assigning labels (strings)
        for value, label in zip(values, enum_labels):
            nd_label = make_nd_value(label, attr_data_format)
            proxy.attr_from_enum = nd_label
            read_attr = proxy.attr_from_enum
            check_attr_type(read_attr, attr_data_format, enum.IntEnum)
            check_read_attr(read_attr, attr_data_format, value, label)

            proxy.attr_from_labels = nd_label
            read_attr = proxy.attr_from_labels
            check_attr_type(read_attr, attr_data_format, enum.IntEnum)
            check_read_attr(read_attr, attr_data_format, value, label)

        invalid_label = make_nd_value("_DOES_NOT_EXIST_", attr_data_format)
        expected_match = re.escape(f"Valid values: {enum_labels}")
        with pytest.raises(AttributeError, match=expected_match):
            proxy.attr_from_enum = invalid_label
        with pytest.raises(AttributeError, match=expected_match):
            proxy.attr_from_labels = invalid_label

    with pytest.raises(TypeError) as context:

        class BadTestDevice(Device):

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                if attr_data_format == AttrDataFormat.SCALAR:
                    self.attr_value = 0
                elif attr_data_format == AttrDataFormat.SPECTRUM:
                    self.attr_value = (0,)
                else:
                    self.attr_value = ((0,),)

            # enum_labels may not be specified if dtype is an enum.Enum
            @attribute(
                dtype=good_type, max_dim_x=3, max_dim_y=3, enum_labels=enum_labels
            )
            def bad_attr(self):
                return self.attr_value

        BadTestDevice()  # dummy instance for Codacy
    assert "enum_labels" in str(context.value)


@pytest.mark.parametrize("enum_type", [DevState, GoodEnum])
def test_enum_devstate_attribute_declared_with_typing(attr_data_format, enum_type):
    value = DevState.MOVING if enum_type is DevState else GoodEnum.MIDDLE
    expected_type = DevState if enum_type is DevState else enum.IntEnum
    nd_value = make_nd_value(value, attr_data_format)

    if attr_data_format == AttrDataFormat.SCALAR:
        EnumType = enum_type
    elif attr_data_format == AttrDataFormat.SPECTRUM:
        EnumType = tuple[enum_type, enum_type, enum_type]
    else:
        EnumType = tuple[
            tuple[enum_type, enum_type, enum_type],
            tuple[enum_type, enum_type, enum_type],
            tuple[enum_type, enum_type, enum_type],
        ]

    class TestDevice(Device):
        attr: EnumType = attribute(access=AttrWriteType.READ)

        def read_attr(self):
            return nd_value

    with DeviceTestContext(TestDevice) as proxy:
        read_value = proxy.attr
        assert read_value == nd_value
        check_attr_type(read_value, attr_data_format, expected_type)
        if enum_type is GoodEnum:
            check_read_attr(read_value, attr_data_format, value, "MIDDLE")


def test_read_attribute_with_invalid_quality_is_none(attribute_typed_values):
    dtype, values, expected = attribute_typed_values

    class TestDevice(Device):
        @attribute(dtype=dtype, max_dim_x=3, max_dim_y=3)
        def attr(self):
            dummy_time = 123.4
            return values[0], dummy_time, AttrQuality.ATTR_INVALID

    with DeviceTestContext(TestDevice) as proxy:
        reading = proxy.read_attribute("attr")
        assert reading.value is None
        assert reading.quality == AttrQuality.ATTR_INVALID
        high_level_value = proxy.attr
        assert high_level_value is None


def test_read_enum_attribute_with_invalid_quality_is_none():
    class TestDevice(Device):
        @attribute(dtype=GoodEnum)
        def attr(self):
            dummy_time = 123.4
            return GoodEnum.START, dummy_time, AttrQuality.ATTR_INVALID

    with DeviceTestContext(TestDevice) as proxy:
        reading = proxy.read_attribute("attr")
        assert reading.value is None
        assert reading.quality == AttrQuality.ATTR_INVALID
        high_level_value = proxy.attr
        assert high_level_value is None


def test_wrong_attribute_read():
    class TestDevice(Device):

        @attribute(dtype=str)
        def attr_str_err(self):
            return 1.2345

        @attribute(dtype=int)
        def attr_int_err(self):
            return "bla"

        @attribute(dtype=[str])
        def attr_str_list_err(self):
            return ["hello", 55]

    with DeviceTestContext(TestDevice) as proxy:
        with pytest.raises(DevFailed):
            proxy.attr_str_err
        with pytest.raises(DevFailed):
            proxy.attr_int_err
        with pytest.raises(DevFailed):
            proxy.attr_str_list_err


def test_attribute_access_with_default_method_names():

    is_allowed = True

    class TestDevice(Device):

        _read_write_value = ""
        _is_allowed = True

        attr_r = attribute(dtype=str)
        attr_rw = attribute(dtype=str, access=AttrWriteType.READ_WRITE)

        def read_attr_r(self):
            return "readable"

        def read_attr_rw(self):
            print(f"Return value {self._read_write_value}")
            return self._read_write_value

        def write_attr_rw(self, value):
            print(f"Get value {value}")
            self._read_write_value = value

        def is_attr_r_allowed(self, req_type):
            assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
            return is_allowed

        def is_attr_rw_allowed(self, req_type):
            assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
            return is_allowed

    with DeviceTestContext(TestDevice) as proxy:
        with pytest.raises(DevFailed):
            proxy.attr_r = "writable"
        assert proxy.attr_r == "readable"
        proxy.attr_rw = "writable"
        assert proxy.attr_rw == "writable"

        is_allowed = False
        with pytest.raises(DevFailed):
            _ = proxy.attr_r
        with pytest.raises(DevFailed):
            proxy.attr_rw = "writing_not_allowed"
        with pytest.raises(DevFailed):
            _ = proxy.attr_rw


@pytest.fixture(
    ids=["low_level_read", "high_level_read"],
    params=[
        textwrap.dedent(
            """\
                        def read_dyn_attr(self, attr):
                            attr.set_value(self.attr_value)
                            """
        ),
        textwrap.dedent(
            """\
                        def read_dyn_attr(self, attr):
                            return self.attr_value
                            """
        ),
    ],
)
def dynamic_attribute_read_function(request):
    return request.param


def test_read_write_dynamic_attribute(
    dynamic_attribute_read_function, server_green_mode
):
    if server_green_mode == GreenMode.Asyncio:

        class TestDevice(Device):
            green_mode = server_green_mode
            attr_value = None

            @command
            async def add_dyn_attr(self):
                attr = attribute(
                    name="dyn_attr",
                    dtype=int,
                    access=AttrWriteType.READ_WRITE,
                    fget=self.read_dyn_attr,
                    fset=self.write_dyn_attr,
                )
                await self.async_add_attribute(attr)

            @command
            async def delete_dyn_attr(self):
                await self.async_remove_attribute("dyn_attr")

            async def write_dyn_attr(self, attr):
                self.attr_value = attr.get_write_value()

            exec(dynamic_attribute_read_function.replace("def ", "async def "))

    else:

        class TestDevice(Device):
            green_mode = server_green_mode
            attr_value = None

            @command
            def add_dyn_attr(self):
                attr = attribute(
                    name="dyn_attr",
                    dtype=int,
                    access=AttrWriteType.READ_WRITE,
                    fget=self.read_dyn_attr,
                    fset=self.write_dyn_attr,
                )
                self.add_attribute(attr)

            @command
            def delete_dyn_attr(self):
                self.remove_attribute("dyn_attr")

            def write_dyn_attr(self, attr):
                self.attr_value = attr.get_write_value()

            exec(dynamic_attribute_read_function)

    with DeviceTestContext(TestDevice) as proxy:
        proxy.add_dyn_attr()
        proxy.dyn_attr = 123
        assert proxy.dyn_attr == 123
        proxy.delete_dyn_attr()
        assert "dyn_attr" not in proxy.get_attribute_list()


def test_async_add_remove_dynamic_attribute():
    class TestDevice(Device):
        green_mode = GreenMode.Asyncio

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.attr_value = None

        @command
        async def add_dyn_attr(self):
            attr = attribute(
                name="dyn_attr",
                dtype=int,
                access=AttrWriteType.READ_WRITE,
                fget=self.read_dyn_attr,
                fset=self.write_dyn_attr,
            )
            self.add_attribute(attr)

        @command
        async def delete_dyn_attr(self):
            self.remove_attribute("dyn_attr")

        @command
        async def async_add_dyn_attr(self):
            attr = attribute(
                name="dyn_attr",
                dtype=int,
                access=AttrWriteType.READ_WRITE,
                fget=self.read_dyn_attr,
                fset=self.write_dyn_attr,
            )
            await self.async_add_attribute(attr)

        @command
        async def async_delete_dyn_attr(self):
            await self.async_remove_attribute("dyn_attr")

        async def write_dyn_attr(self, attr):
            self.attr_value = attr.get_write_value()

        async def read_dyn_attr(self, attr):
            return self.attr_value

    with DeviceTestContext(TestDevice) as proxy:
        proxy.add_dyn_attr()
        proxy.dyn_attr = 123
        assert proxy.dyn_attr == 123
        proxy.delete_dyn_attr()
        assert "dyn_attr" not in proxy.get_attribute_list()

        proxy.async_add_dyn_attr()
        proxy.dyn_attr = 123
        assert proxy.dyn_attr == 123
        proxy.async_delete_dyn_attr()
        assert "dyn_attr" not in proxy.get_attribute_list()


def test_dynamic_attribute_declared_with_typing(attribute_typed_values):
    dtype, values, expected = attribute_typed_values
    tuple_hint, list_hint, check_x_dim, check_y_dim = convert_dtype_to_typing_hint(
        dtype
    )

    class TestDevice(Device):
        attr_value = None

        def initialize_dynamic_attributes(self):
            attr = attribute(
                name="read_function_tuple_hint",
                access=AttrWriteType.READ_WRITE,
                fget=self.read_attr_with_tuple_hints,
                fset=self.write_attr_no_hints,
            )
            self.add_attribute(attr)

            attr = attribute(
                name="user_size_priority_over_hint",
                max_dim_x=5,
                max_dim_y=5,
                access=AttrWriteType.READ_WRITE,
                fget=self.read_attr_with_tuple_hints,
                fset=self.write_attr_no_hints,
            )
            self.add_attribute(attr)

            attr = attribute(
                name="read_function_list_hint",
                access=AttrWriteType.READ_WRITE,
                max_dim_x=5,
                max_dim_y=5,
                fget=self.read_attr_with_list_hints,
                fset=self.write_attr_no_hints,
            )
            self.add_attribute(attr)

            attr = attribute(
                name="write_function_tuple_hint",
                access=AttrWriteType.READ_WRITE,
                fget=self.read_attr_no_hints,
                fset=self.write_attr_with_tuple_hints,
            )
            self.add_attribute(attr)

            attr = attribute(
                name="write_function_list_hint",
                access=AttrWriteType.READ_WRITE,
                max_dim_x=5,
                max_dim_y=5,
                fget=self.read_attr_no_hints,
                fset=self.write_attr_with_list_hints,
            )
            self.add_attribute(attr)

        def read_attr_no_hints(self, attr):
            return self.attr_value

        def write_attr_no_hints(self, attr):
            self.attr_value = attr.get_write_value()

        def read_attr_with_tuple_hints(self, attr) -> tuple_hint:
            return self.attr_value

        def read_attr_with_list_hints(self, attr) -> list_hint:
            return self.attr_value

        def write_attr_with_tuple_hints(self, attr: tuple_hint):
            self.attr_value = attr.get_write_value()

        def write_attr_with_list_hints(self, attr: list_hint):
            self.attr_value = attr.get_write_value()

        @command()
        def reset(self):
            self.attr_value = None

    def check_attribute_with_size(proxy, attr, value, size_x, size_y):
        setattr(proxy, attr, value)
        assert_close(getattr(proxy, attr), expected(value))
        conf = proxy.get_attribute_config(attr)
        if check_x_dim:
            assert conf.max_dim_x == size_x
        if check_y_dim:
            assert conf.max_dim_y == size_y
        proxy.reset()

    with DeviceTestContext(TestDevice) as proxy:
        for value in values:
            check_attribute_with_size(proxy, "read_function_tuple_hint", value, 3, 4)
            check_attribute_with_size(proxy, "read_function_list_hint", value, 5, 5)
            check_attribute_with_size(
                proxy, "user_size_priority_over_hint", value, 5, 5
            )
            check_attribute_with_size(proxy, "write_function_tuple_hint", value, 3, 4)
            check_attribute_with_size(proxy, "write_function_list_hint", value, 5, 5)


def test_dynamic_attribute_self_typed_with_not_defined_name():
    _value = [None]

    def non_bound_read(device: "TestDevice", attr) -> int:
        return _value[0]

    def non_bound_read_no_return_hint(device: "TestDevice", attr):
        return _value[0]

    def non_bound_write(device: "TestDevice", attr: int):
        _value[0] = attr.get_write_value()

    class TestDevice(Device):
        _value = None

        def initialize_dynamic_attributes(self):
            attr = attribute(
                name="read_with_hint",
                access=AttrWriteType.READ_WRITE,
                fget=self.read_attr,
                fset=self.write_attr,
            )
            self.add_attribute(attr)

            attr = attribute(
                name="read_no_hint",
                access=AttrWriteType.READ_WRITE,
                fget=self.read_attr_no_hint,
                fset=self.write_attr,
            )
            self.add_attribute(attr)

            attr = attribute(
                name="non_bound_read_with_hint",
                access=AttrWriteType.READ_WRITE,
                fget=non_bound_read,
                fset=non_bound_write,
            )
            self.add_attribute(attr)

            attr = attribute(
                name="non_bound_read_no_hint",
                access=AttrWriteType.READ_WRITE,
                fget=non_bound_read_no_return_hint,
                fset=non_bound_write,
            )
            self.add_attribute(attr)

        def read_attr(self: "TestDevice", attr) -> int:
            return self._value

        def read_attr_no_hint(self: "TestDevice", attr):
            return self._value

        def write_attr(self: "TestDevice", attr: int):
            self._value = attr.get_write_value()

    with DeviceTestContext(TestDevice) as proxy:
        proxy.read_with_hint = 1
        assert 1 == proxy.read_with_hint
        proxy.read_no_hint = 2
        assert 2 == proxy.read_no_hint

        proxy.non_bound_read_with_hint = 1
        assert 1 == proxy.non_bound_read_with_hint
        proxy.non_bound_read_no_hint = 2
        assert 2 == proxy.non_bound_read_no_hint


if npt:

    def test_attribute_declared_with_numpy_typing(attribute_numpy_typed_values):
        type_hint, dformat, value, expected = attribute_numpy_typed_values

        class TestDevice(Device):
            attr_value = None

            statement_declaration: type_hint = attribute(
                access=AttrWriteType.READ_WRITE,
                fget="read_attr",
                fset="write_attr",
                dformat=dformat,
                max_dim_x=2,
                max_dim_y=2,
            )

            def read_attr(self):
                return self.attr_value

            def write_attr(self, value):
                self.attr_value = value

            def initialize_dynamic_attributes(self):
                attr = attribute(
                    name="dynamic_declaration",
                    access=AttrWriteType.READ_WRITE,
                    fget=self.read_dynamic_attr,
                    fset=self.write_dynamic_attr,
                    dformat=dformat,
                    max_dim_x=2,
                    max_dim_y=2,
                )
                self.add_attribute(attr)

            def read_dynamic_attr(self, attr):
                return self.attr_value

            def write_dynamic_attr(self, attr):
                self.attr_value = attr.get_write_value()

            @attribute(
                access=AttrWriteType.READ_WRITE,
                dformat=dformat,
                max_dim_x=2,
                max_dim_y=2,
            )
            def decorator_declaration(self) -> type_hint:
                return self.attr_value

            @decorator_declaration.write
            def decorator_declaration_write(self, value: type_hint):
                self.attr_value = value

            @command()
            def reset(self):
                self.attr_value = None

        def check_attribute(proxy, attr, value):
            setattr(proxy, attr, value)
            assert_close(getattr(proxy, attr), expected(value))
            proxy.reset()

        with DeviceTestContext(TestDevice) as proxy:
            check_attribute(proxy, "statement_declaration", value)
            check_attribute(proxy, "decorator_declaration", value)
            check_attribute(proxy, "dynamic_declaration", value)

    def test_attribute_wrong_declared_with_numpy_typing(attribute_wrong_numpy_typed):
        dformat, max_x, max_y, value, error, match = attribute_wrong_numpy_typed

        with pytest.raises(error, match=match):

            class TestDevice(Device):
                attr_value = None

                attr: npt.NDArray[np.int_] = attribute(
                    access=AttrWriteType.READ_WRITE,
                    dformat=dformat,
                    max_dim_x=max_x,
                    max_dim_y=max_y,
                )

                def read_attr(self):
                    return self.attr_value

                def write_attr(self, value):
                    self.attr_value = value

            with DeviceTestContext(TestDevice) as proxy:
                proxy.attr = value
                _ = proxy.attr


def test_read_write_dynamic_attribute_decorated_methods_default_names(
    server_green_mode,
):

    is_allowed = True

    class TestDevice(Device):
        green_mode = server_green_mode

        attr_value = None
        is_allowed = None

        def initialize_dynamic_attributes(self):
            attr = attribute(name="attr", dtype=int, access=AttrWriteType.READ_WRITE)
            self.add_attribute(attr)

        def allowed(self):
            return is_allowed

        sync_code = textwrap.dedent(
            """\
        @general_decorator
        def read_attr(self, attr):
            return self.attr_value

        @general_decorator
        def write_attr(self, attr):
            self.attr_value = attr.get_write_value()

        @general_decorator
        def is_attr_allowed(self, req_type):
            assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
            return self.allowed()
        """
        )

        if server_green_mode != GreenMode.Asyncio:
            exec(sync_code)
        else:
            exec(
                sync_code.replace("def ", "async def ").replace(
                    "general_decorator", "general_asyncio_decorator"
                )
            )

    with DeviceTestContext(TestDevice) as proxy:
        proxy.attr = 123
        assert proxy.attr == 123

        is_allowed = False
        with pytest.raises(DevFailed):
            proxy.attr = 123
        with pytest.raises(DevFailed):
            _ = proxy.attr


def test_read_write_dynamic_attribute_decorated_methods_user_names(server_green_mode):

    is_allowed = True

    class TestDevice(Device):
        green_mode = server_green_mode

        attr_value = None
        is_allowed = None

        def initialize_dynamic_attributes(self):
            attr = attribute(
                name="attr",
                dtype=int,
                access=AttrWriteType.READ_WRITE,
                fget=self.user_read,
                fset=self.user_write,
                fisallowed=self.user_is_allowed,
            )
            self.add_attribute(attr)

        def allowed(self):
            return is_allowed

        sync_code = textwrap.dedent(
            """\
        @general_decorator
        def user_read(self, attr):
            return self.attr_value

        @general_decorator
        def user_write(self, attr):
            self.attr_value = attr.get_write_value()

        @general_decorator
        def user_is_allowed(self, req_type):
            assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
            return self.allowed()
        """
        )

        if server_green_mode != GreenMode.Asyncio:
            exec(sync_code)
        else:
            exec(
                sync_code.replace("def ", "async def ").replace(
                    "general_decorator", "general_asyncio_decorator"
                )
            )

    with DeviceTestContext(TestDevice) as proxy:
        proxy.attr = 123
        assert proxy.attr == 123

        is_allowed = False
        with pytest.raises(DevFailed):
            proxy.attr = 123
        with pytest.raises(DevFailed):
            _ = proxy.attr


def test_read_write_dynamic_attribute_decorated_shared_user_functions():

    is_allowed = True

    class TestDevice(Device):

        attr_values = {"attr1": None, "attr2": None}
        is_allowed = None

        def initialize_dynamic_attributes(self):
            attr = attribute(
                name="attr1",
                dtype=int,
                access=AttrWriteType.READ_WRITE,
                fget=self.user_read,
                fset=self.user_write,
                fisallowed=self.user_is_allowed,
            )
            self.add_attribute(attr)
            attr = attribute(
                name="attr2",
                dtype=int,
                access=AttrWriteType.READ_WRITE,
                fget=self.user_read,
                fset=self.user_write,
                fisallowed=self.user_is_allowed,
            )
            self.add_attribute(attr)

        @general_decorator
        def user_read(self, attr):
            return self.attr_values[attr.get_name()]

        @general_decorator
        def user_write(self, attr):
            self.attr_values[attr.get_name()] = attr.get_write_value()

        @general_decorator
        def user_is_allowed(self, req_type):
            assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
            return is_allowed

    with DeviceTestContext(TestDevice) as proxy:
        proxy.attr1 = 123
        assert proxy.attr1 == 123
        proxy.attr2 = 456
        assert proxy.attr1 == 123
        assert proxy.attr2 == 456

        is_allowed = False
        with pytest.raises(DevFailed):
            proxy.attr1 = 123
        with pytest.raises(DevFailed):
            _ = proxy.attr1
        with pytest.raises(DevFailed):
            proxy.attr2 = 123
        with pytest.raises(DevFailed):
            _ = proxy.attr2


def test_read_write_dynamic_attribute_enum(attr_data_format):
    values = [member.value for member in GoodEnum]
    enum_labels = get_enum_labels(GoodEnum)

    if attr_data_format == AttrDataFormat.SCALAR:
        attr_type = DevEnum
        attr_info = (DevEnum, attr_data_format, READ_WRITE)
    elif attr_data_format == AttrDataFormat.SPECTRUM:
        attr_type = (DevEnum,)
        attr_info = (DevEnum, attr_data_format, READ_WRITE, 10)
    else:
        attr_type = ((DevEnum,),)
        attr_info = (DevEnum, attr_data_format, READ_WRITE, 10, 10)

    class TestDevice(Device):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if attr_data_format == AttrDataFormat.SCALAR:
                self.attr_value = 0
            elif attr_data_format == AttrDataFormat.SPECTRUM:
                self.attr_value = (0,)
            else:
                self.attr_value = ((0,),)

        @command
        def add_dyn_attr_old(self):
            attr = AttrData(
                "dyn_attr",
                None,
                attr_info=[
                    attr_info,
                    {"enum_labels": enum_labels},
                ],
            )
            self.add_attribute(
                attr, r_meth=self.read_dyn_attr, w_meth=self.write_dyn_attr
            )

        @command
        def add_dyn_attr_new(self):
            attr = attribute(
                name="dyn_attr",
                dtype=attr_type,
                enum_labels=enum_labels,
                max_dim_x=3,
                max_dim_y=3,
                access=AttrWriteType.READ_WRITE,
                fget=self.read_dyn_attr,
                fset=self.write_dyn_attr,
            )
            self.add_attribute(attr)

        @command
        def delete_dyn_attr(self):
            self.remove_attribute("dyn_attr")

        def read_dyn_attr(self, attr):
            return self.attr_value

        def write_dyn_attr(self, attr):
            self.attr_value = attr.get_write_value()

    with DeviceTestContext(TestDevice) as proxy:
        for add_attr_cmd in [proxy.add_dyn_attr_old, proxy.add_dyn_attr_new]:
            add_attr_cmd()
            for value, label in zip(values, enum_labels):
                nd_value = make_nd_value(value, attr_data_format)
                proxy.dyn_attr = nd_value
                read_attr = proxy.dyn_attr
                assert read_attr == nd_value
                check_attr_type(read_attr, attr_data_format, enum.IntEnum)
                check_read_attr(read_attr, attr_data_format, value, label)
            proxy.delete_dyn_attr()
            assert "dyn_attr" not in proxy.get_attribute_list()


@pytest.mark.parametrize("enum_type", [DevState, GoodEnum])
def test_enum_devstate_dynamic_attribute_declared_with_typing(
    attr_data_format, enum_type
):
    value = DevState.MOVING if enum_type is DevState else GoodEnum.MIDDLE
    expected_type = DevState if enum_type is DevState else enum.IntEnum
    nd_value = make_nd_value(value, attr_data_format)

    if attr_data_format == AttrDataFormat.SCALAR:
        EnumType = enum_type
    elif attr_data_format == AttrDataFormat.SPECTRUM:
        EnumType = tuple[enum_type, enum_type, enum_type]
    else:
        EnumType = tuple[
            tuple[enum_type, enum_type, enum_type],
            tuple[enum_type, enum_type, enum_type],
        ]

    class TestDevice(Device):
        def initialize_dynamic_attributes(self):
            self.add_attribute(attribute(name="attr", access=AttrWriteType.READ))

        def read_attr(self, attr) -> EnumType:
            return nd_value

    with DeviceTestContext(TestDevice) as proxy:
        read_value = proxy.attr
        assert read_value == nd_value
        check_attr_type(read_value, attr_data_format, expected_type)
        if enum_type is GoodEnum:
            check_read_attr(read_value, attr_data_format, value, "MIDDLE")


def test_read_write_dynamic_attribute_is_allowed_with_async(server_green_mode):
    DYN_ATTRS_END_RANGE = 9

    if server_green_mode == GreenMode.Asyncio:

        class BaseTestDevice(Device):
            @command(dtype_in=bool)
            async def make_allowed(self, yesno):
                for att_num in range(1, DYN_ATTRS_END_RANGE):
                    setattr(self, f"attr{att_num}_allowed", yesno)

    else:

        class BaseTestDevice(Device):
            @command(dtype_in=bool)
            def make_allowed(self, yesno):
                for att_num in range(1, DYN_ATTRS_END_RANGE):
                    setattr(self, f"attr{att_num}_allowed", yesno)

    class TestDevice(BaseTestDevice):
        green_mode = server_green_mode

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for att_num in range(1, DYN_ATTRS_END_RANGE):
                setattr(self, f"attr{att_num}_allowed", True)
            for att_num in range(1, DYN_ATTRS_END_RANGE):
                setattr(self, f"attr{att_num}_value", None)

        def initialize_dynamic_attributes(self):
            # recommended approach: using attribute() and bound methods:
            attr = attribute(
                name="dyn_attr1",
                dtype=int,
                access=AttrWriteType.READ_WRITE,
                fget=self.read_dyn_attr1,
                fset=self.write_dyn_attr1,
                fisallowed=self.is_attr1_allowed,
            )
            self.add_attribute(attr)

            # not recommended: using attribute() with unbound methods:
            attr = attribute(
                name="dyn_attr2",
                dtype=int,
                access=AttrWriteType.READ_WRITE,
                fget=TestDevice.read_dyn_attr2,
                fset=TestDevice.write_dyn_attr2,
                fisallowed=TestDevice.is_attr2_allowed,
            )
            self.add_attribute(attr)

            # possible approach: using attribute() with method name strings:
            attr = attribute(
                name="dyn_attr3",
                dtype=int,
                access=AttrWriteType.READ_WRITE,
                fget="read_dyn_attr3",
                fset="write_dyn_attr3",
                fisallowed="is_attr3_allowed",
            )
            self.add_attribute(attr)

            # old approach: using tango.AttrData with bound methods:
            attr_name = "dyn_attr4"
            data_info = self._get_attr_data_info()
            dev_class = self.get_device_class()
            attr_data = AttrData(attr_name, dev_class.get_name(), data_info)
            self.add_attribute(
                attr_data,
                self.read_dyn_attr4,
                self.write_dyn_attr4,
                self.is_attr4_allowed,
            )

            # old approach: using tango.AttrData with unbound methods:
            attr_name = "dyn_attr5"
            attr_data = AttrData(attr_name, dev_class.get_name(), data_info)
            self.add_attribute(
                attr_data,
                TestDevice.read_dyn_attr5,
                TestDevice.write_dyn_attr5,
                TestDevice.is_attr5_allowed,
            )

            # old approach: using tango.AttrData with default method names
            attr_name = "dyn_attr6"
            attr_data = AttrData(attr_name, dev_class.get_name(), data_info)
            self.add_attribute(attr_data)

            # old approach: using tango.AttrData filled from dictionary
            attr_name = "dyn_attr7"
            d = {
                "name": attr_name,
                "class_name": dev_class.get_name(),
                # not setting access explicitly
                "fread": "read_dyn_attr7",
                "fwrite": "write_dyn_attr7",
                "fisallowed": self.is_attr7_allowed,
            }
            attr_data = AttrData.from_dict(d)
            self.add_attribute(attr_data)

            # not recommened: implicit access level
            attr = attribute(
                name="dyn_attr8",
                fset=self.write_dyn_attr8,
                fisallowed=self.is_attr8_allowed,
            )
            self.add_attribute(attr)

        def _get_attr_data_info(self):
            simple_type, fmt = get_tango_type_format(int)
            data_info = [[simple_type, fmt, READ_WRITE]]
            return data_info

        # the following methods are written in plain text which looks
        # weird. This is done so that it is easy to change for async
        # tests without duplicating all the code.
        read_code = textwrap.dedent(
            """
        def read_dyn_attr(self, attr):
            return self.attr_value
        """
        )

        write_code = textwrap.dedent(
            """
        def write_dyn_attr(self, attr):
            self.attr_value = attr.get_write_value()
        """
        )

        is_allowed_code = textwrap.dedent(
            """
        def is_attr_allowed(self, req_type):
            assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
            return self.attr_allowed
        """
        )

        for attr_num in range(1, DYN_ATTRS_END_RANGE):
            read_method = read_code.replace("read_dyn_attr", f"read_dyn_attr{attr_num}")
            read_method = read_method.replace("attr_value", f"attr{attr_num}_value")
            write_method = write_code.replace(
                "write_dyn_attr", f"write_dyn_attr{attr_num}"
            )
            write_method = write_method.replace("attr_value", f"attr{attr_num}_value")
            if attr_num != 6:
                is_allowed_method = is_allowed_code.replace(
                    "is_attr_allowed", f"is_attr{attr_num}_allowed"
                )
            else:
                # default name differs
                is_allowed_method = is_allowed_code.replace(
                    "is_attr_allowed", f"is_dyn_attr{attr_num}_allowed"
                )
            is_allowed_method = is_allowed_method.replace(
                "self.attr_allowed", f"self.attr{attr_num}_allowed"
            )

            if server_green_mode != GreenMode.Asyncio:
                exec(read_method)
                exec(write_method)
                exec(is_allowed_method)
            else:
                exec(read_method.replace("def ", "async def "))
                exec(write_method.replace("def ", "async def "))
                exec(is_allowed_method.replace("def ", "async def "))

    with DeviceTestContext(TestDevice) as proxy:
        proxy.make_allowed(True)

        for ind in range(1, DYN_ATTRS_END_RANGE):

            setattr(proxy, f"dyn_attr{ind}", ind)

            if ind != 8:
                assert getattr(proxy, f"dyn_attr{ind}") == ind

        proxy.make_allowed(False)

        for ind in range(1, DYN_ATTRS_END_RANGE):

            if ind != 8:
                with pytest.raises(DevFailed):
                    _ = getattr(proxy, f"dyn_attr{ind}")

            with pytest.raises(DevFailed):
                setattr(proxy, f"dyn_attr{ind}", ind)


@pytest.mark.parametrize("use_green_mode", [True, False])
def test_dynamic_attribute_with_green_mode(use_green_mode, server_green_mode):
    class TestDevice(Device):
        green_mode = server_green_mode
        attr_value = 123

        def initialize_dynamic_attributes(self):
            global executor
            executor = get_executor(server_green_mode)
            attr = attribute(
                name="attr_r",
                dtype=int,
                access=AttrWriteType.READ,
                fget=self.user_read,
                read_green_mode=use_green_mode,
            )
            self.add_attribute(attr)
            attr = attribute(
                name="attr_rw",
                dtype=int,
                access=AttrWriteType.READ_WRITE,
                fget=self.user_read,
                fset=self.user_write,
                read_green_mode=use_green_mode,
                write_green_mode=use_green_mode,
            )
            self.add_attribute(attr)
            attr = attribute(
                name="attr_ia",
                dtype=int,
                access=AttrWriteType.READ,
                fget=self.user_read,
                fisallowed=self.user_is_allowed,
                read_green_mode=use_green_mode,
                isallowed_green_mode=use_green_mode,
            )
            self.add_attribute(attr)
            attr = attribute(
                name="attr_rw_always_ok",
                dtype=int,
                access=AttrWriteType.READ_WRITE,
                fget=self.user_read,
                fset=self.user_write,
                green_mode=True,
            )
            self.add_attribute(attr)

        sync_code = textwrap.dedent(
            """
            def user_read(self, attr):
                self.assert_executor_context_correct(attr.get_name())
                return self.attr_value

            def user_write(self, attr):
                self.assert_executor_context_correct(attr.get_name())
                self.attr_value = attr.get_write_value()

            def user_is_allowed(self, req_type):
                self.assert_executor_context_correct()
                assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
                return True

        """
        )

        def assert_executor_context_correct(self, attr_name=""):
            check_required = attr_name != "attr_rw_always_ok"
            if check_required and executor.asynchronous:
                assert executor.in_executor_context() == use_green_mode

        if server_green_mode == GreenMode.Asyncio and use_green_mode:
            exec(sync_code.replace("def", "async def"))
        else:
            exec(sync_code)

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.attr_r == 123
        proxy.attr_rw = 456
        assert proxy.attr_rw == 456
        assert proxy.attr_ia == 456


@pytest.mark.parametrize(
    "device_impl_class", [Device_4Impl, Device_5Impl, Device_6Impl, LatestDeviceImpl]
)
def test_dynamic_attribute_using_classic_api_like_sardana(device_impl_class):
    class ClassicAPIClass(DeviceClass):
        cmd_list = {
            "make_allowed": [[DevBoolean, "allow access"], [DevVoid, "none"]],
        }

        def __init__(self, name):
            super().__init__(name)
            self.set_type("TestDevice")

    class ClassicAPIDeviceImpl(device_impl_class):
        def __init__(self, cl, name):
            super().__init__(cl, name)
            ClassicAPIDeviceImpl.init_device(self)

        def init_device(self):
            self._attr1 = 3.14
            self._is_test_attr_allowed = True
            read = self.__class__._read_attr
            write = self.__class__._write_attr
            is_allowed = self.__class__._is_attr_allowed
            attr_name = "attr1"
            data_info = [[DevDouble, SCALAR, READ_WRITE]]
            dev_class = self.get_device_class()
            attr_data = AttrData(attr_name, dev_class.get_name(), data_info)
            self.add_attribute(attr_data, read, write, is_allowed)

        def _is_attr_allowed(self, req_type):
            assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
            return self._is_test_attr_allowed

        def _read_attr(self, attr):
            attr.set_value(self._attr1)

        def _write_attr(self, attr):
            w_value = attr.get_write_value()
            self._attr1 = w_value

        def make_allowed(self, yesno):
            self._is_test_attr_allowed = yesno

    with DeviceTestContext(ClassicAPIDeviceImpl, ClassicAPIClass) as proxy:
        proxy.make_allowed(True)
        assert proxy.attr1 == 3.14
        proxy.attr1 = 42.0
        assert proxy.attr1 == 42.0

        proxy.make_allowed(False)
        with pytest.raises(DevFailed):
            _ = proxy.attr1
        with pytest.raises(DevFailed):
            proxy.attr1 = 12.0


@pytest.mark.parametrize("read_function_signature", ["low_level", "high_level"])
@pytest.mark.parametrize("patched", [True, False])
def test_dynamic_attribute_with_unbound_functions(read_function_signature, patched):
    value = {"attr": None}
    is_allowed = None

    def low_level_read_function(device, attr):
        assert isinstance(device, TestDevice)
        attr.set_value(value["attr"])

    def high_level_read_function(device, attr):
        assert isinstance(device, TestDevice)
        return value["attr"]

    def write_function(device, attr):
        assert isinstance(device, TestDevice)
        value["attr"] = attr.get_write_value()

    def is_allowed_function(device, req_type):
        assert isinstance(device, TestDevice)
        assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
        return is_allowed

    class TestDevice(Device):

        def initialize_dynamic_attributes(self):
            if read_function_signature == "low_level":
                read_function = low_level_read_function
            elif read_function_signature == "high_level":
                read_function = high_level_read_function

            # trick to run server with non device method: patch __dict__
            if patched:
                self.__dict__["read_dyn_attr1"] = read_function
                self.__dict__["write_dyn_attr1"] = write_function
                self.__dict__["is_dyn_attr1_allowed"] = is_allowed_function
                attr = attribute(
                    name="dyn_attr1", dtype=int, access=AttrWriteType.READ_WRITE
                )
                self.add_attribute(attr)

                setattr(self, "read_dyn_attr2", read_function)
                setattr(self, "write_dyn_attr2", write_function)
                setattr(self, "is_dyn_attr2_allowed", is_allowed_function)
                attr = attribute(
                    name="dyn_attr2", dtype=int, access=AttrWriteType.READ_WRITE
                )
                self.add_attribute(attr)

            else:
                attr = attribute(
                    name="dyn_attr",
                    fget=read_function,
                    fset=write_function,
                    fisallowed=is_allowed_function,
                    dtype=int,
                    access=AttrWriteType.READ_WRITE,
                )
                self.add_attribute(attr)

    with DeviceTestContext(TestDevice) as proxy:
        is_allowed = True
        if patched:
            proxy.dyn_attr1 = 123
            assert proxy.dyn_attr1 == 123

            proxy.dyn_attr2 = 456
            assert proxy.dyn_attr2 == 456
        else:
            proxy.dyn_attr = 789
            assert proxy.dyn_attr == 789

        is_allowed = False
        if patched:
            with pytest.raises(DevFailed):
                proxy.dyn_attr1 = 123

            with pytest.raises(DevFailed):
                _ = proxy.dyn_attr1

            with pytest.raises(DevFailed):
                proxy.dyn_attr2 = 456

            with pytest.raises(DevFailed):
                _ = proxy.dyn_attr2
        else:
            with pytest.raises(DevFailed):
                proxy.dyn_attr = 123

            with pytest.raises(DevFailed):
                _ = proxy.dyn_attr


def test_attribute_decorators(server_green_mode):
    if server_green_mode == GreenMode.Asyncio:

        class BaseTestDevice(Device):
            @command(dtype_in=bool)
            async def make_allowed(self, yesno):
                self.is_allowed = yesno

    else:

        class BaseTestDevice(Device):
            @command(dtype_in=bool)
            def make_allowed(self, yesno):
                self.is_allowed = yesno

    class TestDevice(BaseTestDevice):
        green_mode = server_green_mode
        current_value = None
        voltage_value = None
        is_allowed = None

        current = attribute(label="Current", unit="mA", dtype=float)
        voltage = attribute(label="Voltage", unit="V", dtype=float)

        sync_code = textwrap.dedent(
            """
        @current.getter
        def cur_read(self):
            return self.current_value

        @current.setter
        def cur_write(self, current):
            self.current_value = current

        @current.is_allowed
        def cur_allo(self, req_type):
            return self.is_allowed

        @voltage.read
        def vol_read(self):
            return self.voltage_value

        @voltage.write
        def vol_write(self, voltage):
            self.voltage_value = voltage

        @voltage.is_allowed
        def vol_allo(self, req_type):
            return self.is_allowed
        """
        )

        if server_green_mode == GreenMode.Asyncio:
            exec(sync_code.replace("def ", "async def "))
        else:
            exec(sync_code)

    with DeviceTestContext(TestDevice) as proxy:
        proxy.make_allowed(True)
        proxy.current = 2.0
        assert_close(proxy.current, 2.0)
        proxy.voltage = 3.0
        assert_close(proxy.voltage, 3.0)

        proxy.make_allowed(False)
        with pytest.raises(DevFailed):
            proxy.current = 4.0
        with pytest.raises(DevFailed):
            _ = proxy.current
        with pytest.raises(DevFailed):
            proxy.voltage = 4.0
        with pytest.raises(DevFailed):
            _ = proxy.voltage


def test_attribute_info_description():
    class TestDevice(Device):
        @attribute(description="Description from kwarg has priority")
        def attr_description_kwarg(self) -> float:
            """Docstring has lower priority than description kwarg, so ignored"""
            return 1.5

        @attribute(access=AttrWriteType.READ_WRITE)
        def attr_decorated_docstring_only(self) -> float:
            """Docstring from decorated read method"""
            return 2.5

        @attr_decorated_docstring_only.setter
        def attr_decorated_docstring_only(self, value: float) -> None:
            """Docstring from decorated write method currently ignored"""
            pass

        attr_assignment = attribute()

        def read_attr_assignment(self) -> float:
            """Docstring from read method currently ignored for description"""
            return 3.5

    with DeviceTestContext(TestDevice) as proxy:
        cfg = proxy.get_attribute_config("attr_description_kwarg")
        assert cfg.description == "Description from kwarg has priority"

        cfg = proxy.get_attribute_config("attr_decorated_docstring_only")
        assert cfg.description == "Docstring from decorated read method"

        cfg = proxy.get_attribute_config("attr_assignment")
        assert cfg.description == tango.constants.DescNotSpec


def test_read_only_dynamic_attribute_with_dummy_write_method(
    dynamic_attribute_read_function,
):
    def dummy_write_method():
        return None

    class TestDevice(Device):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.attr_value = 123

        def initialize_dynamic_attributes(self):
            self.add_attribute(
                Attr("dyn_attr", DevLong, AttrWriteType.READ),
                r_meth=self.read_dyn_attr,
                w_meth=dummy_write_method,
            )

        def read_dyn_attr(self, attr):
            return self.attr_value

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.dyn_attr == 123


def test_dynamic_attribute_with_method_in_other_class():
    class Helper:
        value = 0
        is_allowed = True

        def _read_method(self, device, attr):
            assert isinstance(device, TestDevice)
            assert attr.get_name() == "dyn_attr"
            return self.value

        def _write_method(self, device, attr):
            assert isinstance(device, TestDevice)
            assert attr.get_name() == "dyn_attr"
            self.value = attr.get_write_value()

        def _is_allowed_method(self, device, req_type):
            assert isinstance(device, TestDevice)
            assert req_type in (AttReqType.READ_REQ, AttReqType.WRITE_REQ)
            return self.is_allowed

        def read_method(self, device, attr):
            return self._read_method(device, attr)

        def write_method(self, device, attr):
            self._write_method(device, attr)

        def is_allowed_method(self, device, req_type):
            return self._is_allowed_method(device, req_type)

    class TestDevice(Device):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = Helper()

        def initialize_dynamic_attributes(self):
            self.add_attribute(
                Attr("dyn_attr", DevLong, AttrWriteType.READ_WRITE),
                r_meth=self.helper.read_method,
                w_meth=self.helper.write_method,
                is_allo_meth=self.helper.is_allowed_method,
            )

    with DeviceTestContext(TestDevice) as proxy:
        Helper.is_allowed = True
        proxy.dyn_attr = 123
        assert proxy.dyn_attr == 123

        Helper.is_allowed = False
        with pytest.raises(DevFailed):
            proxy.dyn_attr = 456
        with pytest.raises(DevFailed):
            _ = proxy.dyn_attr


def test_polled_attribute(server_green_mode):
    dct = {"PolledAttribute1": 100, "PolledAttribute2": 100000, "PolledAttribute3": 500}

    class TestDevice(Device):
        green_mode = server_green_mode

        @attribute(polling_period=dct["PolledAttribute1"])
        def PolledAttribute1(self):
            return 42.0

        @attribute(polling_period=dct["PolledAttribute2"])
        def PolledAttribute2(self):
            return 43.0

        @attribute(polling_period=dct["PolledAttribute3"])
        def PolledAttribute3(self):
            return 44.0

    with DeviceTestContext(TestDevice) as proxy:
        ans = proxy.polling_status()
        for x in ans:
            lines = x.split("\n")
            attr = lines[0].split("= ")[1]
            poll_period = int(lines[1].split("= ")[1])
            assert dct[attr] == poll_period


@pytest.mark.parametrize("return_type", [tuple, list])
@pytest.mark.parametrize("return_quality", [True, False])
def test_read_write_dev_encoded(dev_encoded_values, return_quality, return_type):

    def check_ans(raw_ans, expected_type):
        assert len(raw_ans) == 2
        assert is_pure_str(raw_ans[0])
        if expected_type is bytes:
            assert isinstance(raw_ans[1], bytes)
            assert raw_ans[1] == UTF8_STRING.encode()
        elif expected_type is str:
            assert is_pure_str(raw_ans[1])
            assert raw_ans[1] == UTF8_STRING
        else:
            assert isinstance(raw_ans[1], bytearray)
            assert raw_ans[1] == bytearray(UTF8_STRING.encode())

    class TestDevice(Device):
        attr_value = None
        command_value = None

        @attribute(dtype=DevEncoded, access=AttrWriteType.READ_WRITE)
        def attr(self):
            if return_quality:
                return return_type(self.attr_value), time.time(), AttrQuality.ATTR_VALID
            else:
                return return_type(self.attr_value)

        @attr.write
        def attr(self, value):
            check_ans(value, bytes)
            self.attr_value = value

        @attribute(dtype=DevEncoded)
        def attr_time_quality_1(self):
            return self.attr_value, 1.0, AttrQuality.ATTR_ALARM

        @attribute(dtype=DevEncoded)
        def attr_time_quality_2(self):
            return *self.attr_value, 2.0, AttrQuality.ATTR_WARNING

        @command(dtype_in=DevEncoded)
        def cmd_in(self, value):
            check_ans(value, bytes)
            self.command_value = value

        @command(dtype_out=DevEncoded)
        def cmd_out(self):
            return self.command_value

        @command(dtype_in=DevEncoded, dtype_out=DevEncoded)
        def cmd_in_out(self, value):
            check_ans(value, bytes)
            return value

    with DeviceTestContext(TestDevice) as proxy:
        proxy.attr = dev_encoded_values
        raw_ans = proxy.read_attribute("attr", extract_as=ExtractAs.Bytes)
        check_ans(raw_ans.value, bytes)
        check_ans(raw_ans.w_value, bytes)

        raw_ans = proxy.read_attribute("attr", extract_as=ExtractAs.String)
        check_ans(raw_ans.value, str)
        check_ans(raw_ans.w_value, str)

        raw_ans = proxy.read_attribute("attr", extract_as=ExtractAs.ByteArray)
        check_ans(raw_ans.value, bytearray)
        check_ans(raw_ans.w_value, bytearray)

        raw_ans = proxy.read_attribute(
            "attr_time_quality_1", extract_as=ExtractAs.Bytes
        )
        check_ans(raw_ans.value, bytes)
        assert raw_ans.quality == AttrQuality.ATTR_ALARM
        assert raw_ans.time.tv_sec == 1

        raw_ans = proxy.read_attribute(
            "attr_time_quality_2", extract_as=ExtractAs.Bytes
        )
        check_ans(raw_ans.value, bytes)
        assert raw_ans.quality == AttrQuality.ATTR_WARNING
        assert raw_ans.time.tv_sec == 2

        proxy.cmd_in(dev_encoded_values)
        raw_ans = proxy.cmd_out()
        check_ans(raw_ans, bytes)

        raw_ans = proxy.cmd_in_out(dev_encoded_values)
        check_ans(raw_ans, bytes)


def test_dev_encoded_wrong_encoding():
    class TestDevice(Device):
        @attribute(dtype=DevEncoded, access=AttrWriteType.READ)
        def attr_bad_encoding(self):
            return "utf-16", UTF8_STRING.encode("utf-16")

        @attribute(dtype=DevEncoded, access=AttrWriteType.READ)
        def attr_bad_string(self):
            return "bad_one", b"\xff"

    with DeviceTestContext(TestDevice) as proxy:
        with pytest.raises(UnicodeDecodeError):
            _ = proxy.read_attribute("attr_bad_encoding", extract_as=ExtractAs.String)

        with pytest.raises(UnicodeDecodeError):
            _ = proxy.read_attribute("attr_bad_string", extract_as=ExtractAs.String)


ENCODED_ATTRIBUTES = (  # encode function, decode function, data
    ("gray8", "gray8", np.array([np.arange(100, dtype=np.byte) for _ in range(5)])),
    ("gray16", "gray16", np.array([np.arange(100, dtype=np.int16) for _ in range(5)])),
    ("rgb24", "decode_24", np.ones((20, 10, 3), dtype=np.uint8)),
    (
        "jpeg_gray8",
        "gray8",
        np.array([np.arange(100, dtype=np.byte) for _ in range(5)]),
    ),
    ("jpeg_rgb24", None, np.ones((10, 10, 3), dtype=np.uint8)),
    ("jpeg_rgb32", "rgb32", np.zeros((10, 10, 3), dtype=np.uint8)),
)


def test_set_value_None():
    none_position = 0

    class TestDevice(Device):
        def init_device(self):
            super().init_device()
            attr = attribute(name="attr")
            self.add_attribute(attr, self._read_attr_that_raises)

            attr = attribute(name="attr_with_data_quality")
            self.add_attribute(attr, self._read_attr_with_date_quality_that_raises)

        def _read_attr_that_raises(self, attr):
            invalid_value = None
            attr.set_value(invalid_value)

        def _read_attr_with_date_quality_that_raises(self, attr):
            invalid_value = [1, 1, AttrQuality.ATTR_VALID]
            invalid_value[none_position] = None
            attr.set_value_date_quality(*invalid_value)

    with DeviceTestContext(TestDevice) as proxy:
        with pytest.raises(DevFailed, match="method cannot be called with None"):
            _ = proxy.attr

        for _ in range(3):
            with pytest.raises(DevFailed, match="method cannot be called with None"):
                _ = proxy.attr_with_data_quality
            none_position += 1


@pytest.mark.parametrize(
    "f_encode, f_decode, data",
    ENCODED_ATTRIBUTES,
    ids=[f_name for f_name, _, _ in ENCODED_ATTRIBUTES],
)
def test_encoded_attribute(f_encode, f_decode, data):
    if f_encode == "jpeg_rgb32":
        pytest.xfail(
            "jpeg_rgb32 needs cppTango built with TANGO_USE_JPEG option, so we skip this test"
        )

    class TestDevice(Device):
        @attribute(dtype=DevEncoded, access=AttrWriteType.READ)
        def attr(self):
            enc = EncodedAttribute()
            getattr(enc, f"encode_{f_encode}")(data)
            return enc

    def decode_24(data_to_decode):
        # first two bytes are width, then two bytes are height and then goes encoded image
        # see implementation of other decode methods, e.g.
        # https://gitlab.com/tango-controls/cppTango/-/blob/main/cppapi/server/encoded_attribute.cpp#L229
        width = int.from_bytes(data_to_decode[:2], byteorder="big")
        height = int.from_bytes(data_to_decode[2:4], byteorder="big")
        decoded_data = np.frombuffer(data_to_decode[4:], dtype=np.uint8)
        return decoded_data.reshape((height, width, 3))

    with DeviceTestContext(TestDevice) as proxy:
        if f_decode == "decode_24":
            ret = proxy.read_attribute("attr", extract_as=ExtractAs.Bytes)
            codec, ret_data = ret.value
            assert_close(decode_24(ret_data), data)
        elif f_decode is not None:
            ret = proxy.read_attribute("attr", extract_as=ExtractAs.Nothing)
            enc = EncodedAttribute()
            assert_close(getattr(enc, f"decode_{f_decode}")(ret), data)
        else:
            # for jpeg24 we test only encode
            pass


@pytest.mark.xfail(reason="Somehow this test became too fragile, need better solution")
def test_dev_encoded_memory_usage():
    LARGE_DATA_SIZE = 10 * 1024 * 1024  # 1 Mb should be enough, but 10 more reliable
    NUM_CYCLES = 5

    def check_ans(raw_ans):
        assert len(raw_ans) == 2
        assert is_pure_str(raw_ans[0])
        assert isinstance(raw_ans[1], bytes)
        assert len(raw_ans[1]) == LARGE_DATA_SIZE
        if raw_ans[0] == "str":
            assert raw_ans[1] == b"a" * LARGE_DATA_SIZE
        elif raw_ans[0] == "bytes":
            assert raw_ans[1] == b"b" * LARGE_DATA_SIZE
        else:
            assert raw_ans[1] == b"c" * LARGE_DATA_SIZE

    class TestDevice(Device):
        attr_str_read = attribute(
            dtype=DevEncoded, access=AttrWriteType.READ, fget="read_str"
        )
        attr_str_write = attribute(
            dtype=DevEncoded, access=AttrWriteType.WRITE, fset="write_str"
        )
        attr_str_read_write = attribute(
            dtype=DevEncoded,
            access=AttrWriteType.READ_WRITE,
            fget="read_str",
            fset="write_str",
        )

        attr_bytes_read = attribute(
            dtype=DevEncoded, access=AttrWriteType.READ, fget="read_bytes"
        )
        attr_bytes_write = attribute(
            dtype=DevEncoded, access=AttrWriteType.WRITE, fset="write_bytes"
        )
        attr_bytes_read_write = attribute(
            dtype=DevEncoded,
            access=AttrWriteType.READ_WRITE,
            fget="read_bytes",
            fset="write_bytes",
        )

        attr_bytearray_read = attribute(
            dtype=DevEncoded, access=AttrWriteType.READ, fget="read_bytearray"
        )
        attr_bytearray_write = attribute(
            dtype=DevEncoded, access=AttrWriteType.WRITE, fset="write_bytearray"
        )
        attr_bytearray_read_write = attribute(
            dtype=DevEncoded,
            access=AttrWriteType.READ_WRITE,
            fget="read_bytearray",
            fset="write_bytearray",
        )

        def read_str(self):
            return "str", "a" * LARGE_DATA_SIZE

        def write_str(self, value):
            check_ans(value)

        def read_bytes(self):
            return "bytes", b"b" * LARGE_DATA_SIZE

        def write_bytes(self, value):
            check_ans(value)

        def read_bytearray(self):
            return "bytearray", bytearray(b"c" * LARGE_DATA_SIZE)

        def write_bytearray(self, value):
            check_ans(value)

        @command(dtype_in=DevEncoded, dtype_out=DevEncoded)
        def cmd_in_out(self, value):
            check_ans(value)
            if value[0] == "str":
                return "str", "a" * LARGE_DATA_SIZE
            elif value[0] == "bytes":
                return "bytes", b"b" * LARGE_DATA_SIZE
            else:
                return "bytearray", bytearray(b"c" * LARGE_DATA_SIZE)

    with DeviceTestContext(TestDevice) as proxy:
        last_memory_usage = []
        for cycle in range(NUM_CYCLES):
            proxy.attr_str_write = "str", "a" * LARGE_DATA_SIZE
            proxy.attr_bytes_write = "bytes", b"b" * LARGE_DATA_SIZE
            proxy.attr_bytearray_write = "bytearray", bytearray(b"c" * LARGE_DATA_SIZE)

            proxy.attr_str_read_write = "str", "a" * LARGE_DATA_SIZE
            proxy.attr_bytes_read_write = "bytes", b"b" * LARGE_DATA_SIZE
            proxy.attr_bytearray_read_write = "bytearray", bytearray(
                b"c" * LARGE_DATA_SIZE
            )

            check_ans(proxy.attr_str_read)
            check_ans(proxy.attr_bytes_read)
            check_ans(proxy.attr_bytearray_read)

            check_ans(proxy.attr_str_read_write)
            check_ans(proxy.attr_bytes_read_write)
            check_ans(proxy.attr_bytearray_read_write)

            check_ans(proxy.cmd_in_out(("str", "a" * LARGE_DATA_SIZE)))
            check_ans(proxy.cmd_in_out(("bytes", b"b" * LARGE_DATA_SIZE)))
            check_ans(
                proxy.cmd_in_out(("bytearray", bytearray(b"c" * LARGE_DATA_SIZE)))
            )

            current_memory_usage = int(psutil.Process(os.getpid()).memory_info().rss)
            last_memory_usage = np.append(last_memory_usage, current_memory_usage)
        assert not np.all(np.diff(last_memory_usage) > 0)


def test_attribute_list():
    class TestDevice(Device):

        _val = 0

        @attribute
        def attr(self) -> int:
            return self._val

        @attr.write
        def set_attr(self, val_in: int):
            self._val = val_in

        @attribute
        def attr2(self) -> str:
            return "a"

        @command()
        def check_attribute_list(self):
            attribute_list = self.get_device_attr().get_attribute_list()
            assert isinstance(attribute_list, tuple)
            assert len(attribute_list) == 4

            assert isinstance(attribute_list[0], WAttribute)
            assert attribute_list[0].get_name() == "attr"

            assert isinstance(attribute_list[1], Attribute)
            assert attribute_list[1].get_name() == "attr2"

        @command()
        def check_attr_list(self):
            u = Util.instance()

            classes = u.get_class_list()
            assert len(classes) == 1
            assert isinstance(classes[0], DeviceClass)
            multi_class_attribute = classes[0].get_class_attr()
            assert isinstance(multi_class_attribute, MultiClassAttribute)

            attr_list = multi_class_attribute.get_attr_list()
            assert isinstance(attr_list, tuple)

            assert len(attr_list) == 2

            assert isinstance(attr_list[0], Attr)
            assert attr_list[0].get_name() == "attr"

            assert isinstance(attr_list[1], Attr)
            assert attr_list[1].get_name() == "attr2"

    with DeviceTestContext(TestDevice) as proxy:
        proxy.check_attribute_list()
        proxy.check_attr_list()


@pytest.mark.parametrize("set_w_value", [False, True])
def test_fill_attr_polling_buffer(attribute_typed_values, set_w_value):
    dtype, values, expected = attribute_typed_values

    start_time = time.time()

    class TestDevice(Device):

        @attribute(
            dtype=dtype, access=AttrWriteType.READ_WRITE, max_dim_x=3, max_dim_y=3
        )
        def attr(self):
            return values[0]

        @attr.write
        def attr(self, new_val):
            pass

        @attribute(dtype=dtype, max_dim_x=3, max_dim_y=3)
        def attr_2(self):
            return values[0]

        @command
        def fill_history(self):
            data = []
            for i, val in enumerate(values):
                t = start_time + i
                w_val = val if set_w_value else None
                data.append(TimedAttrData(val, w_value=w_val, time_stamp=t))

            data.append(
                TimedAttrData(
                    error=RuntimeError("Test"),
                    time_stamp=start_time + len(data),
                )
            )
            self.fill_attr_polling_buffer("attr", data)

            # check how auto-convert to list works
            self.fill_attr_polling_buffer("attr_2", TimedAttrData(values[0]))

    with DeviceTestContext(TestDevice) as proxy:
        # we do not want, that tango core fills up history automatically
        proxy.poll_attribute("attr", 0)
        proxy.poll_attribute("attr_2", 0)
        proxy.fill_history()
        history = proxy.attribute_history("attr", 10)
        assert len(history) == len(values) + 1
        for ind, attr in enumerate(history[:-1]):
            assert_close(attr.value, expected(values[ind]))
            assert attr.quality == AttrQuality.ATTR_VALID
            assert not attr.has_failed
            assert_close(start_time + ind, attr.time.totime())
            if set_w_value:
                assert_close(attr.w_value, expected(values[ind]))

        assert history[-1].has_failed
        assert history[-1].quality == AttrQuality.ATTR_INVALID

        history = proxy.attribute_history("attr_2", 10)
        assert_close(history[0].value, expected(values[0]))


def test_removed_dim_parameters():
    reason = "Note, that dim_x and dim_y arguments are no longer supported"

    class TestDevice(Device):
        def initialize_dynamic_attributes(self):
            attr = attribute(name="attr", fget=self.attr, dtype=int)
            self.add_attribute(attr)

        def attr(self, attr):
            with pytest.raises(TypeError, match=reason):
                attr.set_value_date_quality(1, time.time(), AttrQuality.ATTR_VALID, 1)
            with pytest.raises(TypeError, match=reason):
                attr.set_value_date_quality(
                    1, time.time(), AttrQuality.ATTR_VALID, 1, 1
                )
            with pytest.raises(TypeError, match=reason):
                attr.set_value(1, 1)
            with pytest.raises(TypeError, match=reason):
                attr.set_value(1, 1, 2)

            return 1

    with DeviceTestContext(TestDevice) as proxy:
        _ = proxy.attr
