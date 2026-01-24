# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

import time

try:
    import numpy.typing as npt
except ImportError:
    npt = None

from tango import (
    AttrDataFormat,
    AttrQuality,
    AttrWriteType,
    DevState,
)
from tango.server import Device
from tango.server import command, attribute
from tango.test_utils import (
    DeviceTestContext,
    assert_close,
    check_attr_type,
)


def test_scalar_attribute_declared_with_typing():

    class TestDevice(Device):
        attr_value = None

        hint_scalar: int = attribute(
            access=AttrWriteType.READ_WRITE, fget="read_attr", fset="write_attr"
        )

        hint_scalar_quality: tuple[int, float, AttrQuality] = attribute(
            access=AttrWriteType.READ_WRITE, fget="read_attr", fset="write_attr"
        )

        hint_with_tuple_spectrum: tuple[int, int, int] = attribute(
            access=AttrWriteType.READ_WRITE, fget="read_attr", fset="write_attr"
        )

        hint_with_tuple_quality_spectrum: tuple[
            tuple[int, int, int], float, AttrQuality
        ] = attribute(
            access=AttrWriteType.READ_WRITE,
            fget="read_attr_with_quality",
            fset="write_attr",
        )

        hint_with_list_spectrum: list[int] = attribute(
            access=AttrWriteType.READ_WRITE,
            max_dim_x=3,
            max_dim_y=3,
            fget="read_attr",
            fset="write_attr",
        )

        hint_with_tuple_image: tuple[
            tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]
        ] = attribute(
            access=AttrWriteType.READ_WRITE, fget="read_attr", fset="write_attr"
        )

        hint_with_tuple_quality_image: tuple[
            tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]],
            float,
            AttrQuality,
        ] = attribute(
            access=AttrWriteType.READ_WRITE,
            fget="read_attr_with_quality",
            fset="write_attr",
        )

        def read_attr(self):
            return self.attr_value

        def read_attr_with_quality(self):
            return self.attr_value, time.time(), AttrQuality.ATTR_VALID

        def write_attr(self, value):
            self.attr_value = value

        @attribute(access=AttrWriteType.READ_WRITE)
        def attribute_hint(self) -> int:
            return self.attr_value

        @attribute_hint.write
        def attribute_hint(self, value):
            self.attr_value = value

        @attribute(access=AttrWriteType.READ_WRITE)
        def attribute_hint_quality(self) -> tuple[int, float, AttrQuality]:
            return self.attr_value

        @attribute_hint_quality.write
        def attribute_hint_quality(self, value):
            self.attr_value = value

        @command()
        def reset(self):
            self.attr_value = None

    def check_attribute_with_size(proxy, attr, value):
        setattr(proxy, attr, value)
        assert_close(getattr(proxy, attr), value)
        proxy.reset()

    with DeviceTestContext(TestDevice) as proxy:
        check_attribute_with_size(proxy, "hint_scalar", 1)
        check_attribute_with_size(proxy, "hint_scalar_quality", 2)
        check_attribute_with_size(proxy, "hint_with_tuple_spectrum", [1, 2, 3])
        check_attribute_with_size(proxy, "hint_with_tuple_quality_spectrum", [1, 2, 3])
        check_attribute_with_size(proxy, "hint_with_list_spectrum", [1, 2, 3])
        check_attribute_with_size(
            proxy, "hint_with_tuple_image", [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        )
        check_attribute_with_size(
            proxy, "hint_with_tuple_quality_image", [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        )
        check_attribute_with_size(proxy, "attribute_hint", 1)
        check_attribute_with_size(proxy, "attribute_hint_quality", 2)


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


if npt:

    def test_attribute_declared_with_numpy_typing():

        class TestDevice(Device):
            attr_value = None

            statement_declaration: npt.NDArray[int] = attribute(
                access=AttrWriteType.READ_WRITE,
                fget="read_attr",
                fset="write_attr",
                dformat=AttrDataFormat.SPECTRUM,
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
                    dformat=AttrDataFormat.SPECTRUM,
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
                dformat=AttrDataFormat.SPECTRUM,
                max_dim_x=2,
                max_dim_y=2,
            )
            def decorator_declaration(self) -> npt.NDArray[int]:
                return self.attr_value

            @decorator_declaration.write
            def decorator_declaration_write(self, value: npt.NDArray[int]):
                self.attr_value = value

            @command()
            def reset(self):
                self.attr_value = None

        def check_attribute(proxy, attr, value):
            setattr(proxy, attr, value)
            assert_close(getattr(proxy, attr), value)
            proxy.reset()

        with DeviceTestContext(TestDevice) as proxy:
            check_attribute(proxy, "statement_declaration", [1, 2])
            check_attribute(proxy, "decorator_declaration", [3, 4])
            check_attribute(proxy, "dynamic_declaration", [5, 6])


def test_devstate_attribute_declared_with_typing():

    class TestDevice(Device):

        @attribute()
        def state_attr(self) -> DevState:
            return DevState.MOVING

    with DeviceTestContext(TestDevice) as proxy:
        state_value = proxy.state_attr
        assert state_value == DevState.MOVING
        check_attr_type(state_value, AttrDataFormat.SCALAR, DevState)
