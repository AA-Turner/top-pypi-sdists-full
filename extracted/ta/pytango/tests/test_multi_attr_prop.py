# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import pytest


from tango import (
    Attribute,
    MultiAttrProp,
    DevEncoded,
)
from tango.server import Device
from tango.server import command, attribute
from tango.test_utils import (
    DeviceTestContext,
)


class SimpleDevice(Device):
    @attribute(dtype=bool)
    def attr_bool(self):
        pass

    @attribute(dtype=str)
    def attr_str(self):
        pass

    @attribute(dtype=DevEncoded)
    def attr_enc(self):
        pass

    def check_multi_attr(self, attr_name):
        attr = self.get_device_attr().get_attr_by_name(attr_name)
        assert isinstance(attr, Attribute)

        prop = attr.get_properties()
        assert isinstance(prop, MultiAttrProp)

        prop = MultiAttrProp()
        ret = attr.get_properties(prop)
        assert isinstance(prop, MultiAttrProp)
        assert prop is ret

        with pytest.raises(
            TypeError, match="attr_cfg must be an instance of MultiAttrProp"
        ):
            attr.get_properties([])

        assert prop.label == attr_name
        assert prop.unit == ""

        prop.unit = "kgm^2/s"

        attr.set_properties(prop)

        with pytest.raises(
            TypeError, match="attr_cfg must be an instance of MultiAttrProp"
        ):
            attr.set_properties([])

    @command
    def check_attr_str(self):
        self.check_multi_attr("attr_str")

    @command
    def check_attr_enc(self):
        self.check_multi_attr("attr_enc")

    @command
    def check_attr_bool(self):
        self.check_multi_attr("attr_bool")


def test_stuff():
    with DeviceTestContext(SimpleDevice) as proxy:
        proxy.check_attr_str()
        info = proxy.attribute_query("attr_str")
        assert info.unit == "kgm^2/s"

        proxy.check_attr_enc()
        info = proxy.attribute_query("attr_enc")
        assert info.unit == "kgm^2/s"

        proxy.check_attr_bool()
        info = proxy.attribute_query("attr_bool")
        assert info.unit == "kgm^2/s"
