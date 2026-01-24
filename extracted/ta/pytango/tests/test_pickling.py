# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import pickle
from enum import Enum

import pytest

from tango import (
    ArchiveEventInfo,
    AttrDataFormat,
    AttributeAlarmInfo,
    AttributeEventInfo,
    AttributeInfo,
    AttributeInfoEx,
    AttrMemorizedType,
    AttrWriteType,
    ChangeEventInfo,
    DevError,
    DeviceAttributeConfig,
    DevLong,
    DispLevel,
    ErrSeverity,
    PeriodicEventInfo,
)


class StructType(Enum):
    CHANGE_EVENT_INFO = 0
    PERIOD_EVENT_INFO = 1
    ARCHIVE_EVENT_INFO = 2
    ATTRIBUTE_EVENT_INFO = 3
    ATTRIBUTE_ALARM = 4
    DEVICE_ATTRIBUTE_CONFIG = 5
    ATTRIBUTE_INFO = 6
    ATTRIBUTE_INFO_EX = 7
    DEV_ERROR = 8


def get_struct(struct_type):
    if struct_type == StructType.CHANGE_EVENT_INFO:
        structure = ChangeEventInfo()
    elif struct_type == StructType.PERIOD_EVENT_INFO:
        structure = PeriodicEventInfo()
    elif struct_type == StructType.ARCHIVE_EVENT_INFO:
        structure = ArchiveEventInfo()
    elif struct_type == StructType.ATTRIBUTE_EVENT_INFO:
        structure = AttributeEventInfo()
        structure.ch_event = get_struct(StructType.CHANGE_EVENT_INFO)
        structure.per_event = get_struct(StructType.PERIOD_EVENT_INFO)
        structure.arch_event = get_struct(StructType.ARCHIVE_EVENT_INFO)
        return structure
    elif struct_type == StructType.ATTRIBUTE_ALARM:
        structure = AttributeAlarmInfo()
    elif struct_type == StructType.DEVICE_ATTRIBUTE_CONFIG:
        structure = DeviceAttributeConfig()
    elif struct_type == StructType.ATTRIBUTE_INFO:
        structure = AttributeInfo()
    elif struct_type == StructType.ATTRIBUTE_INFO_EX:
        structure = AttributeInfoEx()
        structure.memorized = AttrMemorizedType.MEMORIZED_WRITE_INIT
        structure.enum_labels = ["A", "BB", "CCC"]
        structure.alarms = get_struct(StructType.ATTRIBUTE_ALARM)
        structure.events = get_struct(StructType.ATTRIBUTE_EVENT_INFO)
        structure.sys_extensions = ["ext4", "ext5", "ext6"]
    elif struct_type == StructType.DEV_ERROR:
        structure = DevError()
    else:
        raise RuntimeError("Unknown info type")

    for member in dir(structure):
        if not member.startswith("_") and isinstance(getattr(structure, member), str):
            setattr(structure, member, member)

    if struct_type in [
        StructType.DEVICE_ATTRIBUTE_CONFIG,
        StructType.ATTRIBUTE_INFO,
        StructType.ATTRIBUTE_INFO_EX,
    ]:
        structure.writable = AttrWriteType.READ_WRITE
        structure.data_format = AttrDataFormat.SPECTRUM
        structure.data_type = DevLong
        structure.max_dim_x = 1
        structure.max_dim_y = 2

    if struct_type in [StructType.ATTRIBUTE_INFO, StructType.ATTRIBUTE_INFO_EX]:
        structure.disp_level = DispLevel.EXPERT

    if struct_type == StructType.DEV_ERROR:
        structure.severity = ErrSeverity.WARN
    else:
        structure.extensions = ["ext1", "ext2", "ext3"]

    return structure


def assert_struct(unpickled, struct_type=None):

    if struct_type == StructType.ATTRIBUTE_EVENT_INFO:
        assert_struct(unpickled.ch_event)
        assert_struct(unpickled.per_event)
        assert_struct(unpickled.arch_event)
        return

    for member in dir(unpickled):
        if not member.startswith("_") and isinstance(getattr(unpickled, member), str):
            assert (
                getattr(unpickled, member) == member
            ), f"Mismatch in {member} field after unpickling."

    if struct_type in [
        StructType.DEVICE_ATTRIBUTE_CONFIG,
        StructType.ATTRIBUTE_INFO,
        StructType.ATTRIBUTE_INFO_EX,
    ]:
        assert (
            unpickled.writable == AttrWriteType.READ_WRITE
        ), "Mismatch in writable field after unpickling."
        assert (
            unpickled.data_format == AttrDataFormat.SPECTRUM
        ), "Mismatch in data_format field after unpickling."
        assert (
            unpickled.data_type == DevLong
        ), "Mismatch in data_type field after unpickling."
        assert unpickled.max_dim_x == 1, "Mismatch in max_dim_x field after unpickling."
        assert unpickled.max_dim_y == 2, "Mismatch in max_dim_y field after unpickling."

    if struct_type in [StructType.ATTRIBUTE_INFO, StructType.ATTRIBUTE_INFO_EX]:
        assert (
            unpickled.disp_level == DispLevel.EXPERT
        ), "Mismatch in disp_level field after unpickling."

    if struct_type == StructType.ATTRIBUTE_INFO_EX:
        assert (
            unpickled.memorized == AttrMemorizedType.MEMORIZED_WRITE_INIT
        ), "Mismatch in memorized field after unpickling."
        assert unpickled.enum_labels == [
            "A",
            "BB",
            "CCC",
        ], "Mismatch in enum_labels field after unpickling."
        assert_struct(unpickled.alarms, StructType.ATTRIBUTE_ALARM)
        assert_struct(unpickled.events, StructType.ATTRIBUTE_EVENT_INFO)
        assert unpickled.sys_extensions == [
            "ext4",
            "ext5",
            "ext6",
        ], "Mismatch in sys_extensions field after unpickling."

    if struct_type == StructType.DEV_ERROR:
        assert unpickled.severity == ErrSeverity.WARN
    else:
        assert unpickled.extensions == [
            "ext1",
            "ext2",
            "ext3",
        ], "Mismatch in 'extensions' field after unpickling."


@pytest.mark.parametrize("structure_type", StructType)
def test_structure_pickle(structure_type):
    # Step 1: Create an instance of structure
    original = get_struct(structure_type)

    # Step 2: Pickle the structure instance
    try:
        pickled_data = pickle.dumps(original)
    except Exception as e:
        pytest.fail(f"Pickling failed with exception: {e}")

    # Step 3: Unpickle the data back to a structure instance
    try:
        unpickled = pickle.loads(pickled_data)
    except Exception as e:
        pytest.fail(f"Unpickling failed with exception: {e}")

    # Step 4: Assert that all fields are equal
    assert_struct(unpickled, structure_type)
