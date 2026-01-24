import pytest

from tango import (
    LockerLanguage,
    CmdArgType,
    MessBoxType,
    PollObjType,
    PollCmdCode,
    SerialModel,
    AttReqType,
    LockCmdCode,
    EventType,
    AttrSerialModel,
    KeepAliveCmdCode,
    AccessControlType,
    asyn_req_type,
    cb_sub_model,
    AttrQuality,
    AttrWriteType,
    AttrDataFormat,
    DevSource,
    ErrSeverity,
    DevState,
    DispLevel,
    AttrMemorizedType,
    ExtractAs,
    GreenMode,
    LogLevel,
    LogTarget,
    EventSubMode,
    EventReason,
)


@pytest.fixture(
    params=[
        LockerLanguage,
        CmdArgType,
        MessBoxType,
        PollObjType,
        PollCmdCode,
        SerialModel,
        AttReqType,
        LockCmdCode,
        EventType,
        AttrSerialModel,
        KeepAliveCmdCode,
        AccessControlType,
        asyn_req_type,
        cb_sub_model,
        AttrQuality,
        AttrWriteType,
        AttrDataFormat,
        DevSource,
        ErrSeverity,
        DevState,
        DispLevel,
        AttrMemorizedType,
        ExtractAs,
        GreenMode,
        LogLevel,
        LogTarget,
        EventSubMode,
        EventReason,
    ],
)
def enum_class(request):
    return request.param


def test_enum_str_and_int(enum_class):
    for name, value in list(enum_class.names.items()):
        assert str(value) == name
        assert int(value) == value


def test_enum_members_names_values(enum_class):
    members = enum_class.__members__
    members_as_ints = [int(enum_value) for enum_value in members.values()]
    names_to_enums = enum_class.names
    values_to_enums = enum_class.values

    assert names_to_enums == members
    assert list(values_to_enums.keys()) == members_as_ints
    assert list(values_to_enums.values()) == list(members.values())
