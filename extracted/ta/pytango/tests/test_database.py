# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import numpy as np
import pytest

from tango import Database
from tango.server import Device, attribute
from tango.test_utils import MultiDeviceTestContext, assert_close


class DeviceToTest(Device):
    @attribute(dtype=str)
    def attr1(self):
        return "attr1"

    @attribute(dtype=str)
    def attr2(self):
        return "attr2"


device_name = "device/test/1"

devices_info = ({"class": DeviceToTest, "devices": [{"name": device_name}]},)


@pytest.fixture()
def test_database():
    with MultiDeviceTestContext(devices_info) as context:
        yield Database(context.db)


def test_put_remove_attribute_properties(test_database):
    attr1_properties = {"attr1": {"value1": ["1"], "value2": ["2"], "value3": ["3"]}}
    attr2_properties = {"attr2": {"value1": ["4"], "value2": ["5"], "value3": ["6"]}}

    test_database.put_device_attribute_property(
        device_name, attr1_properties | attr2_properties
    )

    assert_close(
        test_database.get_device_attribute_property(device_name, "attr1"),
        attr1_properties,
    )
    assert_close(
        test_database.get_device_attribute_property(device_name, "attr2"),
        attr2_properties,
    )

    attr1_prop_to_delete = {"attr1": ["value1"]}
    attr2_prop_to_delete = {"attr2": ["value2"]}

    test_database.delete_device_attribute_property(
        device_name, attr1_prop_to_delete | attr2_prop_to_delete
    )

    [attr1_properties["attr1"].pop(k, None) for k in attr1_prop_to_delete["attr1"]]
    [attr2_properties["attr2"].pop(k, None) for k in attr2_prop_to_delete["attr2"]]

    assert_close(
        test_database.get_device_attribute_property(device_name, "attr1"),
        attr1_properties,
    )
    assert_close(
        test_database.get_device_attribute_property(device_name, "attr2"),
        attr2_properties,
    )


class BadReprObj:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"don't use the repr! {self.value}"


def test_put_get_attribute_properties_string_conversion(test_database):
    attr_properties = {
        "attr": {
            "value0": ["zero"],
            "value1": ["o", "n", "e"],
            "value2": [2],
            "value3": [3.0],
            "value4": [np.float64(4.0)],
            "value5": [BadReprObj(5)],
            "value6": 6,
            "value7": 7.0,
            "value8": np.float64(8.0),
            "value9": BadReprObj(9),
            "value10": True,
        }
    }
    expected_string_properties = {
        "attr": {
            "value0": ["zero"],
            "value1": ["o", "n", "e"],
            "value2": ["2"],
            "value3": ["3.0"],
            "value4": ["4.0"],
            "value5": ["5"],
            "value6": ["6"],
            "value7": ["7.0"],
            "value8": ["8.0"],
            "value9": ["9"],
            "value10": ["True"],
        }
    }

    test_database.put_device_attribute_property(device_name, attr_properties)

    assert_close(
        test_database.get_device_attribute_property(device_name, "attr"),
        expected_string_properties,
    )
