# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.
"""

__all__ = ("pytango_pprint_init",)

__docformat__ = "restructuredtext"

import json
import textwrap

from tango import (
    StdStringVector,
    StdLongVector,
    CommandInfoList,
    AttributeInfoList,
    AttributeInfoListEx,
    DeviceDataHistoryList,
    GroupReplyList,
    GroupAttrReplyList,
    GroupCmdReplyList,
    DbData,
    DbDevInfos,
    DbDevExportInfos,
    DbDevImportInfos,
    DbHistoryList,
    LockerInfo,
    DevCommandInfo,
    AttributeDimension,
    CommandInfo,
    DeviceInfo,
    DeviceAttributeConfig,
    AttributeInfo,
    AttributeAlarmInfo,
    ChangeEventInfo,
    PeriodicEventInfo,
    ArchiveEventInfo,
    AttributeEventInfo,
    AttributeInfoEx,
    DeviceAttribute,
    DeviceAttributeHistory,
    DeviceData,
    DeviceDataHistory,
    DbDatum,
    DbDevInfo,
    DbDevImportInfo,
    DbDevExportInfo,
    DbServerInfo,
    GroupReply,
    GroupAttrReply,
    GroupCmdReply,
    DevError,
    EventData,
    AttrConfEventData,
    DataReadyEventData,
    TimeVal,
    DevFailed,
    CmdArgType,
    MultiAttrProp,
    ClientAddr,
)

from tango._tango import (
    AttributeConfig,
    AttributeConfig_2,
    AttributeConfig_3,
    AttributeConfig_5,
    AttributeAlarm,
    EventProperties,
    ChangeEventProp,
    PeriodicEventProp,
    ArchiveEventProp,
)
import collections.abc


_INDENT_LEVEL = 4
_INDENT = " " * _INDENT_LEVEL
_STRUCT_TYPES = (
    LockerInfo,
    DevCommandInfo,
    AttributeDimension,
    CommandInfo,
    DeviceInfo,
    DeviceAttributeConfig,
    AttributeInfo,
    AttributeAlarmInfo,
    ChangeEventInfo,
    PeriodicEventInfo,
    ArchiveEventInfo,
    AttributeEventInfo,
    AttributeInfoEx,
    DeviceAttribute,
    DeviceAttributeHistory,
    DeviceData,
    DeviceDataHistory,
    DbDatum,
    DbDevInfo,
    DbDevImportInfo,
    DbDevExportInfo,
    DbServerInfo,
    DevError,
    EventData,
    AttrConfEventData,
    DataReadyEventData,
    AttributeConfig,
    AttributeConfig_2,
    AttributeConfig_3,
    AttributeConfig_5,
    ChangeEventProp,
    PeriodicEventProp,
    ArchiveEventProp,
    AttributeAlarm,
    EventProperties,
    MultiAttrProp,
)
_SEQUENCE_TYPES = (
    StdStringVector,
    StdLongVector,
    CommandInfoList,
    AttributeInfoList,
    AttributeInfoListEx,
    DeviceDataHistoryList,
    GroupReplyList,
    GroupAttrReplyList,
    GroupCmdReplyList,
    DbData,
    DbDevInfos,
    DbDevExportInfos,
    DbDevImportInfos,
    DbHistoryList,
)


def __inc_param(obj, name):
    ret = not name.startswith("_")
    ret &= name not in ("except_flags",)
    ret &= not isinstance(getattr(obj, name), collections.abc.Callable)
    return ret


def __nested_json_like_repr(value) -> str:
    if isinstance(value, str):
        return f'"{value}"'
    elif type(value) in _STRUCT_TYPES:
        return str(value)
    elif isinstance(value, dict):
        try:
            return json.dumps(value, indent=_INDENT_LEVEL, sort_keys=True)
        except TypeError:
            return repr(value)
    else:
        return repr(value)


def __single_param(obj, param_name, f=repr, fmt="%s = %s"):
    param_value = getattr(obj, param_name)
    if param_name == "data_type":
        param_value = CmdArgType.values.get(param_value, param_value)
    return fmt % (param_name, f(param_value))


def __struct_params_s(obj, separator=", ", f=repr, fmt="%s = %s"):
    """method wrapper for printing all elements of a struct"""
    s = separator.join(
        [__single_param(obj, n, f, fmt) for n in dir(obj) if __inc_param(obj, n)]
    )
    return s


def __struct_params_repr(obj):
    """method wrapper for representing all elements of a struct"""
    return __struct_params_s(obj)


def __struct_params_str(obj, fmt, f=repr):
    """method wrapper for printing all elements of a struct."""
    return __struct_params_s(obj, "\n", f=f, fmt=fmt)


def __repr__Struct(self):
    """repr method for struct"""
    return f"{self.__class__.__name__}({__struct_params_repr(self)})"


def __str__Struct(self):
    """str method for struct"""
    fmt = "%s = %s"
    details = __struct_params_str(self, fmt, __nested_json_like_repr)
    details = __indented(details, strip_outer=False)
    result = f"{self.__class__.__name__}[\n{details}\n]"
    return result


def __registerSeqStr():
    """helper function to make internal sequences printable"""
    _SeqStr = lambda self: (self and f"[{', '.join(map(repr, self))}]") or "[]"
    _SeqRepr = lambda self: (self and f"[{', '.join(map(repr, self))}]") or "[]"

    for seq in _SEQUENCE_TYPES:
        seq.__str__ = _SeqStr
        seq.__repr__ = _SeqRepr


def __str__DevFailed(self):
    if isinstance(self.args, collections.abc.Sequence):
        seq_str = __str_error_stack_helper(self.args)
        return f"DevFailed[\n{seq_str}\n]"
    return f"DevFailed[{self.args}]"


def __str_error_stack_helper(errors):
    err_str = ",\n".join(str(err).strip() for err in errors)
    err_str = __indented(err_str, strip_outer=False)
    return err_str


def __repr__DevFailed(self):
    return f"DevFailed(args = {repr(self.args)})"


def __str__DevError(self):
    details = (
        f"desc = {__indented(self.desc)}\n"
        f"origin = {__indented(self.origin)}\n"
        f"reason = {self.reason}\n"
        f"severity = {self.severity}\n"
    )
    details = __indented(details, strip_outer=False)
    s = f"DevError[\n{details}\n]"
    return s


def __indented(text, strip_outer=True):
    indented = textwrap.indent(text.strip(), _INDENT)
    if strip_outer:
        return indented.strip()
    else:
        return indented


def __registerStructStr():
    """helper method to register str and repr methods for structures"""

    for struct in _STRUCT_TYPES:
        struct.__str__ = __str__Struct
        struct.__repr__ = __repr__Struct

    # special case for structs that already have a str representation
    TimeVal.__repr__ = __repr__Struct
    GroupReply.__repr__ = __repr__Struct
    GroupAttrReply.__repr__ = __repr__Struct
    GroupCmdReply.__repr__ = __repr__Struct
    ClientAddr.__repr__ = __repr__Struct

    # special case for DevFailed: we want a better pretty print
    # also, because it is an Exception it has the message attribute which
    # generates a Deprecation warning in python 2.6
    DevFailed.__str__ = __str__DevFailed
    DevFailed.__repr__ = __repr__DevFailed

    DevError.__str__ = __str__DevError


def pytango_pprint_init():
    __registerSeqStr()
    __registerStructStr()
