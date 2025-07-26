# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.
"""


import atexit
import collections.abc
import contextlib
import logging
import os
import re
import socket
import sys
import types
import numbers
import inspect
import enum
import threading
import warnings
import functools
import weakref

import typing
import numpy as np

from argparse import HelpFormatter
from collections import namedtuple
from contextvars import ContextVar
from urllib.parse import urlparse, urlunparse

from packaging.version import Version

from tango._tango import (
    AttrQuality,
    StdStringVector,
    StdDoubleVector,
    DbData,
    DbDatum,
    DbDevInfos,
    DbDevExportInfos,
    CmdArgType,
    AttrDataFormat,
    EventData,
    AttrConfEventData,
    DataReadyEventData,
    DevFailed,
    DevState,
    PipeEventData,
    DevIntrChangeEventData,
    Database,
    EncodedAttribute,
    ApiUtil,
    EnsureOmniThread,
    DeviceData,
    DeviceDataList,
    DeviceProxy,
    __Group,
)

from tango import _tango
from tango._tango import _telemetry, Except
from tango.constants import (
    AlrmValueNotSpec,
    StatusNotSet,
    TgLibVers,
    TELEMETRY_SUPPORTED,
)
from tango.release import Release

__all__ = (
    "requires_pytango",
    "requires_tango",
    "is_pure_str",
    "is_seq",
    "is_non_str_seq",
    "is_integer",
    "is_number",
    "is_scalar_type",
    "is_array_type",
    "is_numerical_type",
    "is_int_type",
    "is_float_type",
    "is_bool_type",
    "is_binary_type",
    "is_str_type",
    "obj_2_str",
    "seqStr_2_obj",
    "scalar_to_array_type",
    "document_method",
    "document_static_method",
    "document_enum",
    "CaselessList",
    "CaselessDict",
    "EventCallback",
    "AsyncEventCallback",
    "get_home",
    "from_version_str_to_hex_str",
    "from_version_str_to_int",
    "seq_2_StdStringVector",
    "StdStringVector_2_seq",
    "dir2",
    "TO_TANGO_TYPE",
    "ensure_binary",
    "_get_device_fqtrl_if_necessary",
    "_get_test_context_tango_host_fqtrl",
    "_set_test_context_tango_host_fqtrl",
    "_clear_test_context_tango_host_fqtrl",
    "InvalidTangoHostTrlError",
    "PyTangoUserWarning",
    "parse_type_hint",
    "PyTangoThreadPoolExecutor",
    "set_telemetry_tracer_provider_factory",
    "get_telemetry_tracer_provider_factory",
    "_create_device_telemetry_tracer",
    "_get_non_tango_source_location",
    "_span_to_cpptango",
    "_telemetry_active",
    "_trace_client",
    "_DummyTracer",
    "_get_command_inout_param",
)

__docformat__ = "restructuredtext"

# Types

__str_klasses = (str,)
__int_klasses = (int, np.integer)
__number_klasses = (numbers.Number, np.number)
__seq_klasses = (collections.abc.Sequence, bytearray, StdStringVector, np.ndarray)

_scalar_int_types = (
    CmdArgType.DevShort,
    CmdArgType.DevUShort,
    CmdArgType.DevLong,
    CmdArgType.DevULong,
    CmdArgType.DevLong64,
    CmdArgType.DevULong64,
)

_scalar_float_types = (
    CmdArgType.DevFloat,
    CmdArgType.DevDouble,
)

_scalar_numerical_types = _scalar_int_types + _scalar_float_types

_scalar_str_types = (
    CmdArgType.DevString,
    CmdArgType.ConstDevString,
)

_scalar_bool_types = (CmdArgType.DevBoolean,)

_scalar_types = (
    _scalar_numerical_types
    + _scalar_str_types
    + _scalar_bool_types
    + (
        CmdArgType.DevEncoded,
        CmdArgType.DevUChar,
    )
)

_array_int_types = (
    CmdArgType.DevVarShortArray,
    CmdArgType.DevVarUShortArray,
    CmdArgType.DevVarLongArray,
    CmdArgType.DevVarULongArray,
    CmdArgType.DevVarLong64Array,
    CmdArgType.DevVarULong64Array,
)

_array_float_types = (CmdArgType.DevVarFloatArray, CmdArgType.DevVarDoubleArray)

_array_numerical_types = _array_int_types + _array_float_types

_array_str_types = (CmdArgType.DevVarStringArray,)

_array_bool_types = (CmdArgType.DevVarBooleanArray,)

_array_types = (
    _array_numerical_types
    + _array_bool_types
    + _array_str_types
    + (
        CmdArgType.DevVarCharArray,
        CmdArgType.DevVarDoubleStringArray,
        CmdArgType.DevVarLongStringArray,
    )
)

_binary_types = (
    CmdArgType.DevEncoded,
    CmdArgType.DevVarCharArray,
)


FROM_TANGO_TO_NUMPY_TYPE = {
    CmdArgType.DevBoolean: np.bool_,
    CmdArgType.DevUChar: np.ubyte,
    CmdArgType.DevShort: np.short,
    CmdArgType.DevUShort: np.ushort,
    CmdArgType.DevLong: np.int32,
    CmdArgType.DevULong: np.uint32,
    CmdArgType.DevLong64: np.int64,
    CmdArgType.DevULong64: np.uint64,
    CmdArgType.DevString: str,
    CmdArgType.DevDouble: np.float64,
    CmdArgType.DevFloat: np.float32,
}


def __build_to_tango_type():
    ret = {
        int: CmdArgType.DevLong64,
        str: CmdArgType.DevString,
        bool: CmdArgType.DevBoolean,
        bytearray: CmdArgType.DevEncoded,
        float: CmdArgType.DevDouble,
        chr: CmdArgType.DevUChar,
        None: CmdArgType.DevVoid,
        "int": CmdArgType.DevLong64,
        "int16": CmdArgType.DevShort,
        "int32": CmdArgType.DevLong,
        "int64": CmdArgType.DevLong64,
        "uint": CmdArgType.DevULong64,
        "uint16": CmdArgType.DevUShort,
        "uint32": CmdArgType.DevULong,
        "uint64": CmdArgType.DevULong64,
        "str": CmdArgType.DevString,
        "string": CmdArgType.DevString,
        "text": CmdArgType.DevString,
        "bool": CmdArgType.DevBoolean,
        "boolean": CmdArgType.DevBoolean,
        "bytes": CmdArgType.DevEncoded,
        "bytearray": CmdArgType.DevEncoded,
        "float": CmdArgType.DevDouble,
        "float32": CmdArgType.DevFloat,
        "float64": CmdArgType.DevDouble,
        "double": CmdArgType.DevDouble,
        "byte": CmdArgType.DevUChar,
        "chr": CmdArgType.DevUChar,
        "char": CmdArgType.DevUChar,
        "None": CmdArgType.DevVoid,
        "state": CmdArgType.DevState,
        "enum": CmdArgType.DevEnum,
        "blob": CmdArgType.DevPipeBlob,
    }

    for key in dir(CmdArgType):
        if key.startswith("Dev"):
            value = getattr(CmdArgType, key)
            ret[key] = ret[value] = value

        for key, value in FROM_TANGO_TO_NUMPY_TYPE.items():
            ret[value] = key
    return ret


TO_TANGO_TYPE = __build_to_tango_type()

_scalar_to_array_type = {
    CmdArgType.DevBoolean: CmdArgType.DevVarBooleanArray,
    CmdArgType.DevUChar: CmdArgType.DevVarCharArray,
    CmdArgType.DevShort: CmdArgType.DevVarShortArray,
    CmdArgType.DevUShort: CmdArgType.DevVarUShortArray,
    CmdArgType.DevLong: CmdArgType.DevVarLongArray,
    CmdArgType.DevULong: CmdArgType.DevVarULongArray,
    CmdArgType.DevLong64: CmdArgType.DevVarLong64Array,
    CmdArgType.DevULong64: CmdArgType.DevVarULong64Array,
    CmdArgType.DevFloat: CmdArgType.DevVarFloatArray,
    CmdArgType.DevDouble: CmdArgType.DevVarDoubleArray,
    CmdArgType.DevString: CmdArgType.DevVarStringArray,
    CmdArgType.ConstDevString: CmdArgType.DevVarStringArray,
}

# add derived scalar types to scalar to array map
for k, v in TO_TANGO_TYPE.items():
    if v in _scalar_to_array_type:
        _scalar_to_array_type[k] = _scalar_to_array_type[v]

__NO_STR_VALUE = AlrmValueNotSpec, StatusNotSet

__device_classes = None

bool_ = lambda value_str: value_str.lower() == "true"


def __import(name):
    __import__(name)
    return sys.modules[name]


def __requires(package_name, min_version=None, conflicts=(), software_name="Software"):
    package_name_l = package_name.lower()
    if package_name_l == "pytango":
        curr_version = Version(Release.version)
    elif package_name_l == "tango":
        curr_version = Version(TgLibVers)
    else:
        try:
            package = __import(package_name)
            curr_version = Version(package.__version__)
        except ImportError:
            msg = f"Could not find package {package_name} required by {software_name}"
            raise Exception(msg)
        except Exception:
            msg = f"Error importing package {package_name} required by {software_name}"
            raise Exception(msg)

    if min_version is not None:
        min_version = Version(min_version)
        if min_version > curr_version:
            msg = f"{software_name} requires {package_name} {min_version} but {curr_version} installed"
            raise Exception(msg)

    conflicts = map(Version, conflicts)
    if curr_version in conflicts:
        msg = f"{software_name} cannot run with {package_name} {curr_version}"
        raise Exception(msg)
    return True


def requires_pytango(min_version=None, conflicts=(), software_name="Software"):
    """
    Determines if the required PyTango version for the running
    software is present. If not an exception is thrown.
    Example usage::

        from tango import requires_pytango

        requires_pytango('7.1', conflicts=['8.1.1'], software_name='MyDS')

    :param min_version:
        minimum PyTango version [default: None, meaning no minimum
        required]. If a string is given, it must be in the valid
        version number format
        (see: :class:`~packaging.version.Version`)
    :type min_version:
        None, str, :class:`~packaging.version.Version`
    :param conflicts:
        a sequence of PyTango versions which conflict with the
        software using it
    :type conflicts:
        seq<str|Version>
    :param software_name:
        software name using tango. Used in the exception message
    :type software_name: str

    :raises Exception: if the required PyTango version is not met

    New in PyTango 8.1.4
    """
    return __requires(
        "pytango",
        min_version=min_version,
        conflicts=conflicts,
        software_name=software_name,
    )


def requires_tango(min_version=None, conflicts=(), software_name="Software"):
    """
    Determines if the required cppTango version for the running
    software is present. If not an exception is thrown.
    Example usage::

        from tango import requires_tango

        requires_tango('7.1', conflicts=['8.1.1'], software_name='MyDS')

    :param min_version:
        minimum Tango version [default: None, meaning no minimum
        required]. If a string is given, it must be in the valid
        version number format
        (see: :class:`~packaging.version.Version`)
    :type min_version:
        None, str, :class:`~packaging.version.Version`
    :param conflicts:
        a sequence of Tango versions which conflict with the
        software using it
    :type conflicts:
        seq<str|Version>
    :param software_name:
        software name using Tango. Used in the exception message
    :type software_name: str

    :raises Exception: if the required Tango version is not met

    New in PyTango 8.1.4
    """
    return __requires(
        "Tango",
        min_version=min_version,
        conflicts=conflicts,
        software_name=software_name,
    )


def get_tango_device_classes():
    global __device_classes
    if __device_classes is None:
        __device_classes = [_tango.DeviceImpl]
        i = 2
        while True:
            dc = f"Device_{i}Impl"
            try:
                __device_classes.append(getattr(_tango, dc))
                i = i + 1
            except AttributeError:
                break
    return __device_classes


def get_latest_device_class():
    return get_tango_device_classes()[-1]


def set_complex_value(attr, value):
    is_tuple = isinstance(value, tuple)
    dtype, fmt = attr.get_data_type(), attr.get_data_format()
    if dtype == CmdArgType.DevEncoded:
        if is_tuple and len(value) == 4:
            attr.set_value_date_quality(*value)
        elif is_tuple and len(value) == 3 and is_non_str_seq(value[0]):
            attr.set_value_date_quality(value[0][0], value[0][1], *value[1:])
        elif isinstance(value, EncodedAttribute):
            attr.set_value(value)
        else:
            attr.set_value(*value)
    else:
        if is_tuple:
            if len(value) == 3:
                if fmt == AttrDataFormat.SCALAR:
                    attr.set_value_date_quality(*value)
                elif fmt == AttrDataFormat.SPECTRUM:
                    if is_seq(value[0]):
                        attr.set_value_date_quality(*value)
                    else:
                        attr.set_value(value)
                else:
                    if is_seq(value[0]) and is_seq(value[0][0]):
                        attr.set_value_date_quality(*value)
                    else:
                        attr.set_value(value)
            else:
                attr.set_value(value)
        else:
            attr.set_value(value)


def __get_tango_type(obj):
    if is_non_str_seq(obj):
        tg_type, tg_format = get_tango_type(obj[0])
        tg_format = AttrDataFormat(int(tg_format) + 1)
        return tg_type, tg_format
    elif is_pure_str(obj):
        r = CmdArgType.DevString
    elif isinstance(obj, DevState):
        r = CmdArgType.DevState
    elif isinstance(obj, bool):
        r = CmdArgType.DevBoolean
    elif isinstance(obj, __int_klasses):
        r = CmdArgType.DevLong64
    elif isinstance(obj, __number_klasses):
        r = CmdArgType.DevDouble
    else:
        raise TypeError(f"Unsupported type {type(obj)}")
    return r, AttrDataFormat.SCALAR


def get_tango_type(obj):
    try:
        ndim, dtype = obj.ndim, str(obj.dtype)
        if ndim > 2:
            raise TypeError(
                f"cannot translate numpy array with {obj.ndim} "
                f"dimensions to tango type"
            )
        return TO_TANGO_TYPE[dtype], AttrDataFormat(ndim)
    except AttributeError:
        return __get_tango_type(obj)


def get_attribute_type_format(dtype, dformat, enum_labels):
    if is_enum(dtype) or is_enum_seq(dtype):
        if enum_labels:
            raise TypeError(
                "For dtype of enum.Enum, (enum.Enum,) or ((enum.Enum,),) the enum_labels must not "
                f"be specified - dtype: {dtype}, enum_labels: {enum_labels}."
            )
        _dtype = dtype
        dtype = CmdArgType.DevEnum

        while is_enum_seq(_dtype):
            _dtype = _dtype[0]
            dtype = (dtype,)

        enum_labels = get_enum_labels(_dtype)

    elif is_devstate(dtype) or is_devstate_seq(dtype):
        _dtype = dtype
        dtype = CmdArgType.DevState

        while is_devstate_seq(_dtype):
            _dtype = _dtype[0]
            dtype = (dtype,)

    return *get_tango_type_format(dtype, dformat, "attribute"), enum_labels


def get_tango_type_format(dtype, dformat=None, caller=None):
    if dformat is None:
        dformat = AttrDataFormat.SCALAR
        if is_non_str_seq(dtype):
            if len(dtype):
                dtype = dtype[0]
                dformat = AttrDataFormat.SPECTRUM
                if is_non_str_seq(dtype):
                    if len(dtype):
                        dtype = dtype[0]
                        dformat = AttrDataFormat.IMAGE
                    elif caller == "attribute":
                        raise TypeError(
                            "Image attribute type must be specified as ((<dtype>,),)"
                        )
            elif caller == "attribute":
                raise TypeError(
                    "Spectrum attribute type must be specified as (<dtype>,)"
                )

    try:
        tango_type = TO_TANGO_TYPE[dtype]
    except KeyError:
        raise RuntimeError(
            f"Cannot translate {dtype} to TANGO type. See documentation for the allowed types"
        )

    return tango_type, dformat


def __has_ellipsis_in_types(dtype):
    try:
        list(typing.get_args(dtype)).remove(Ellipsis)
        return True
    except ValueError:
        pass

    return False


def __check_types_uniformity(dtype):
    all_types = list(set(typing.get_args(dtype)))
    if Ellipsis in all_types:
        all_types.remove(Ellipsis)
    if len(all_types) > 1:
        return False
    for sub_type in typing.get_args(dtype):
        if typing.get_origin(sub_type) in [list, tuple]:
            if not __check_types_uniformity(sub_type):
                return False
    return True


def parse_type_hint(annotation, caller):
    dtype = annotation
    dformat = AttrDataFormat.SCALAR
    max_x, max_y = None, None
    if typing.get_origin(dtype) in [list, tuple]:
        n_elements = len(typing.get_args(dtype))
        if (
            n_elements in [2, 4]
            and typing.get_args(dtype)[0] is str
            and typing.get_args(dtype)[1] in [bytes, bytearray]
        ):
            return "DevEncoded", dformat, max_x, max_y
        if (
            n_elements in [2, 4]
            and typing.get_args(dtype)[0] in [tuple[int], list[int]]
            and typing.get_args(dtype)[1] in [tuple[str], list[str]]
        ):
            return "DevVarLongStringArray", dformat, max_x, max_y
        if (
            n_elements in [2, 4]
            and typing.get_args(dtype)[0] in [tuple[float], list[float]]
            and typing.get_args(dtype)[1] in [tuple[str], list[str]]
        ):
            return "DevVarDoubleStringArray", dformat, max_x, max_y
        if (
            n_elements == 3
            and typing.get_args(dtype)[1] is float
            and typing.get_args(dtype)[2] == AttrQuality
        ):
            dtype = typing.get_args(dtype)[0]
    if typing.get_origin(dtype) == np.ndarray:
        dtype = typing.get_args(typing.get_args(dtype)[1])[0]
        dformat = None
        if caller in ["property", "command"]:
            dtype = (dtype,)
    if typing.get_origin(dtype) in [list, tuple]:
        if not __has_ellipsis_in_types(dtype):
            max_x = len(typing.get_args(dtype))
        types_are_uniform = __check_types_uniformity(dtype)
        dtype = typing.get_args(dtype)[0]
        dformat = (
            AttrDataFormat.IMAGE
            if typing.get_origin(dtype) in [list, tuple]
            else AttrDataFormat.SPECTRUM
        )

        if caller in ["property", "command"] and dformat == AttrDataFormat.IMAGE:
            raise RuntimeError(f"{caller.capitalize()} does not support IMAGE type")

        if not types_are_uniform:
            if caller in ["property", "command"]:
                raise RuntimeError(
                    f"PyTango does not support mixed types in SPECTRUM {caller}"
                )
            else:
                if dformat == AttrDataFormat.IMAGE:
                    raise RuntimeError(
                        "PyTango does not support mixed types in IMAGE attributes"
                    )
                else:
                    raise RuntimeError(
                        "PyTango does not support mixed types in SPECTRUM attributes"
                    )

        if caller == "attribute":
            if dformat == AttrDataFormat.IMAGE:
                max_y = max_x
                if not __has_ellipsis_in_types(dtype):
                    max_x = len(typing.get_args(dtype))
                else:
                    max_x = None
                dtype = typing.get_args(dtype)[0]
        if caller == "property":
            dtype = (dtype,)

    return dtype, dformat, max_x, max_y


class EnumTypeError(Exception):
    """Invalid Enum class for use with DEV_ENUM."""


def get_enum_labels(enum_cls):
    """
    Return list of enumeration labels from Enum class.

    The list is useful when creating an attribute, for the
    `enum_labels` parameter.  The enumeration values are checked
    to ensure they are unique, start at zero, and increment by one.

    :param enum_cls: the Enum class to be inspected
    :type enum_cls: :py:obj:`enum.Enum`

    :return: List of label strings
    :rtype: :py:obj:`list`

    :raises EnumTypeError: in case the given class is invalid
    """
    if not issubclass(enum_cls, enum.Enum):
        raise EnumTypeError(f"Input class '{enum_cls}' must be derived from enum.Enum")

    # Check there are no duplicate labels
    try:
        enum.unique(enum_cls)
    except ValueError as exc:
        raise EnumTypeError(f"Input class '{enum_cls}' must be unique - {exc}")

    # Check the values start at 0, and increment by 1, since that is
    # assumed by tango's DEV_ENUM implementation.
    values = [member.value for member in enum_cls]
    if not values:
        raise EnumTypeError(f"Input class '{enum_cls}' has no members!")
    expected_value = 0
    for value in values:
        if value != expected_value:
            raise EnumTypeError(
                f"Enum values for '{enum_cls}' must start at 0 and "
                f"increment by 1.  Values: {values}"
            )
        expected_value += 1

    return [member.name for member in enum_cls]


def is_pure_str(obj):
    """
    Tells if the given object is a python string.

    In python 2.x this means any subclass of basestring.
    In python 3.x this means any subclass of str.

    :param obj: the object to be inspected
    :type obj: :py:obj:`object`

    :return: True is the given obj is a string or False otherwise
    :rtype: :py:obj:`bool`
    """
    return isinstance(obj, __str_klasses)


def is_seq(obj):
    """
    Tells if the given object is a python sequence.

    It will return True for any collections.Sequence (list, tuple,
    str, bytes, unicode), bytearray and (if numpy is enabled)
    numpy.ndarray

    :param obj: the object to be inspected
    :type obj: :py:obj:`object`

    :return: True is the given obj is a sequence or False otherwise
    :rtype: :py:obj:`bool`
    """
    return isinstance(obj, __seq_klasses)


def is_non_str_seq(obj):
    """
    Tells if the given object is a python sequence (excluding string
    sequences).

    It will return True for any collections.Sequence (list, tuple (and
    bytes in python3)), bytearray and (if numpy is enabled)
    numpy.ndarray

    :param obj: the object to be inspected
    :type obj: :py:obj:`object`

    :return: True is the given obj is a sequence or False otherwise
    :rtype: :py:obj:`bool`
    """
    return is_seq(obj) and not is_pure_str(obj)


def is_devstate(obj):
    return inspect.isclass(obj) and issubclass(obj, DevState)


def is_devstate_seq(obj):
    if is_non_str_seq(obj):
        while is_non_str_seq(obj):
            obj = obj[0]
        return is_devstate(obj)
    return False


def is_enum(obj):
    return inspect.isclass(obj) and issubclass(obj, enum.Enum)


def is_enum_seq(obj):
    if is_non_str_seq(obj):
        while is_non_str_seq(obj) and len(obj):
            obj = obj[0]
        return is_enum(obj)
    return False


def is_integer(obj):
    """
    Tells if the given object is a python integer.

    It will return True for any int, long (in python 2) and
    (if numpy is enabled) numpy.integer

    :param obj: the object to be inspected
    :type obj: :py:obj:`object`

    :return:
        True is the given obj is a python integer or False otherwise
    :rtype: :py:obj:`bool`
    """
    return isinstance(obj, __int_klasses)


def is_number(obj):
    """
    Tells if the given object is a python number.

    It will return True for any numbers.Number and (if numpy is
    enabled) numpy.number

    :param obj: the object to be inspected
    :type obj: :py:obj:`object`

    :return:
        True is the given obj is a python number or False otherwise
    :rtype: :py:obj:`bool`
    """
    return isinstance(obj, __number_klasses)


def is_scalar(tg_type):
    """Tells if the given tango type is a scalar

    :param tg_type: tango type
    :type tg_type: :class:`tango.CmdArgType`

    :return: True if the given tango type is a scalar or False otherwise
    :rtype: :py:obj:`bool`
    """

    global _scalar_types
    return tg_type in _scalar_types


is_scalar_type = is_scalar


def is_array(tg_type):
    """Tells if the given tango type is an array type

    :param tg_type: tango type
    :type tg_type: :class:`tango.CmdArgType`

    :return: True if the given tango type is an array type or False otherwise
    :rtype: :py:obj:`bool`
    """
    global _array_types
    return tg_type in _array_types


is_array_type = is_array


def is_numerical(tg_type, inc_array=False):
    """Tells if the given tango type is numerical

    :param tg_type: tango type
    :type tg_type: :class:`tango.CmdArgType`
    :param inc_array: (optional, default is False) determines if include array
                      in the list of checked types
    :type inc_array: :py:obj:`bool`

    :return: True if the given tango type is a numerical or False otherwise
    :rtype: :py:obj:`bool`
    """
    global _scalar_numerical_types, _array_numerical_types
    if tg_type in _scalar_numerical_types:
        return True
    if not inc_array:
        return False
    return tg_type in _array_numerical_types


is_numerical_type = is_numerical


def is_int(tg_type, inc_array=False):
    """Tells if the given tango type is integer

    :param tg_type: tango type
    :type tg_type: :class:`tango.CmdArgType`
    :param inc_array: (optional, default is False) determines if include array
                      in the list of checked types
    :type inc_array: :py:obj:`bool`

    :return: True if the given tango type is integer or False otherwise
    :rtype: :py:obj:`bool`
    """
    global _scalar_int_types, _array_int_types
    if tg_type in _scalar_int_types:
        return True
    if not inc_array:
        return False
    return tg_type in _array_int_types


is_int_type = is_int


def is_float(tg_type, inc_array=False):
    """Tells if the given tango type is float

    :param tg_type: tango type
    :type tg_type: :class:`tango.CmdArgType`
    :param inc_array: (optional, default is False) determines if include array
                      in the list of checked types
    :type inc_array: :py:obj:`bool`

    :return: True if the given tango type is float or False otherwise
    :rtype: :py:obj:`bool`
    """
    global _scalar_float_types, _array_float_types
    if tg_type in _scalar_float_types:
        return True
    if not inc_array:
        return False
    return tg_type in _array_float_types


is_float_type = is_float


def is_bool(tg_type, inc_array=False):
    """Tells if the given tango type is boolean

    :param tg_type: tango type
    :type tg_type: :class:`tango.CmdArgType`
    :param inc_array: (optional, default is False) determines if include array
                      in the list of checked types
    :type inc_array: :py:obj:`bool`

    :return: True if the given tango type is boolean or False otherwise
    :rtype: :py:obj:`bool`
    """
    global _scalar_bool_types, _array_bool_types
    if tg_type in _scalar_bool_types:
        return True
    if not inc_array:
        return False
    return tg_type in _array_bool_types


is_bool_type = is_bool


def is_str(tg_type, inc_array=False):
    """Tells if the given tango type is string

    :param tg_type: tango type
    :type tg_type: :class:`tango.CmdArgType`
    :param inc_array: (optional, default is False) determines if include array
                      in the list of checked types
    :type inc_array: :py:obj:`bool`

    :return: True if the given tango type is string or False otherwise
    :rtype: :py:obj:`bool`
    """
    global _scalar_str_types, _array_str_types
    if tg_type in _scalar_str_types:
        return True
    if not inc_array:
        return False
    return tg_type in _array_str_types


is_str_type = is_str


def is_binary(tg_type, inc_array=False):
    """Tells if the given tango type is binary

    :param tg_type: tango type
    :type tg_type: :class:`tango.CmdArgType`
    :param inc_array: (optional, default is False) determines if include array
                      in the list of checked types
    :type inc_array: :py:obj:`bool`

    :return: True if the given tango type is binary or False otherwise
    :rtype: :py:obj:`bool`
    """
    global _binary_types
    return tg_type in _binary_types


is_binary_type = is_binary


def seq_2_StdStringVector(seq, vec=None):
    """Converts a python sequence<str> object to a :class:`tango.StdStringVector`

    :param seq: the sequence of strings
    :type seq: sequence<:py:obj:`str`>
    :param vec: (optional, default is None) an :class:`tango.StdStringVector`
                to be filled. If None is given, a new :class:`tango.StdStringVector`
                is created
    :return: a :class:`tango.StdStringVector` filled with the same contents as seq
    :rtype: :class:`tango.StdStringVector`
    """
    if vec is None:
        if isinstance(seq, StdStringVector):
            return seq
        vec = StdStringVector()
    if not isinstance(vec, StdStringVector):
        raise TypeError("vec must be a tango.StdStringVector")
    for e in seq:
        vec.append(str(e))
    return vec


def StdStringVector_2_seq(vec, seq=None):
    """Converts a :class:`tango.StdStringVector` to a python sequence<str>

    :param seq: the :class:`tango.StdStringVector`
    :type seq: :class:`tango.StdStringVector`
    :param vec: (optional, default is None) a python sequence to be filled.
                 If None is given, a new list is created
    :return: a python sequence filled with the same contents as seq
    :rtype: sequence<str>
    """
    if seq is None:
        seq = []
    if not isinstance(vec, StdStringVector):
        raise TypeError("vec must be a tango.StdStringVector")
    for e in vec:
        seq.append(str(e))
    return seq


def seq_2_StdDoubleVector(seq, vec=None):
    """Converts a python sequence<float> object to a :class:`tango.StdDoubleVector`

    :param seq: the sequence of floats
    :type seq: sequence<:py:obj:`float`>
    :param vec: (optional, default is None) an :class:`tango.StdDoubleVector`
                to be filled. If None is given, a new :class:`tango.StdDoubleVector`
                is created
    :return: a :class:`tango.StdDoubleVector` filled with the same contents as seq
    :rtype: :class:`tango.StdDoubleVector`
    """
    if vec is None:
        if isinstance(seq, StdDoubleVector):
            return seq
        vec = StdDoubleVector()
    if not isinstance(vec, StdDoubleVector):
        raise TypeError("vec must be a tango.StdDoubleVector")
    for e in seq:
        vec.append(float(e))
    return vec


def StdDoubleVector_2_seq(vec, seq=None):
    """Converts a :class:`tango.StdDoubleVector` to a python sequence<float>

    :param seq: the :class:`tango.StdDoubleVector`
    :type seq: :class:`tango.StdDoubleVector`
    :param vec: (optional, default is None) a python sequence to be filled.
                 If None is given, a new list is created
    :return: a python sequence filled with the same contents as seq
    :rtype: sequence<float>
    """
    if seq is None:
        seq = []
    if not isinstance(vec, StdDoubleVector):
        raise TypeError("vec must be a tango.StdDoubleVector")
    for e in vec:
        seq.append(float(e))
    return seq


def seq_2_DbDevInfos(seq, vec=None):
    """Converts a python sequence<DbDevInfo> object to a :class:`tango.DbDevInfos`

    :param seq: the sequence of DbDevInfo
    :type seq: sequence<DbDevInfo>
    :param vec: (optional, default is None) an :class:`tango.DbDevInfos`
                to be filled. If None is given, a new :class:`tango.DbDevInfos`
                is created
    :return: a :class:`tango.DbDevInfos` filled with the same contents as seq
    :rtype: :class:`tango.DbDevInfos`
    """
    if vec is None:
        if isinstance(seq, DbDevInfos):
            return seq
        vec = DbDevInfos()
    if not isinstance(vec, DbDevInfos):
        raise TypeError("vec must be a tango.DbDevInfos")
    for e in seq:
        vec.append(e)
    return vec


def seq_2_DbDevExportInfos(seq, vec=None):
    """Converts a python sequence<DbDevExportInfo> object to a :class:`tango.DbDevExportInfos`

    :param seq: the sequence of DbDevExportInfo
    :type seq: sequence<DbDevExportInfo>
    :param vec: (optional, default is None) an :class:`tango.DbDevExportInfos`
                to be filled. If None is given, a new :class:`tango.DbDevExportInfos`
                is created
    :return: a :class:`tango.DbDevExportInfos` filled with the same contents as seq
    :rtype: :class:`tango.DbDevExportInfos`
    """
    if vec is None:
        if isinstance(seq, DbDevExportInfos):
            return seq
        vec = DbDevExportInfos()
    if not isinstance(vec, DbDevExportInfos):
        raise TypeError("vec must be a tango.DbDevExportInfos")
    for e in seq:
        vec.append(e)
    return vec


def seq_2_DbData(seq, vec=None):
    """Converts a python sequence<DbDatum> object to a :class:`tango.DbData`

    :param seq: the sequence of DbDatum
    :type seq: sequence<DbDatum>
    :param vec: (optional, default is None) an :class:`tango.DbData`
                to be filled. If None is given, a new :class:`tango.DbData`
                is created
    :return: a :class:`tango.DbData` filled with the same contents as seq
    :rtype: :class:`tango.DbData`
    """
    if vec is None:
        if isinstance(seq, DbData):
            return seq
        vec = DbData()
    if not isinstance(vec, DbData):
        raise TypeError("vec must be a tango.DbData")
    for e in seq:
        vec.append(e)
    return vec


def DbData_2_dict(db_data, d=None):
    if d is None:
        d = {}
    if not isinstance(db_data, DbData):
        raise TypeError(
            f"db_data must be a tango.DbData. A {type(db_data)} found instead"
        )
    for db_datum in db_data:
        d[db_datum.name] = db_datum.value_string
    return d


def seqStr_2_obj(seq, tg_type, tg_format=None):
    """Translates a sequence<str> to a sequence of objects of give type and format

    :param seq: the sequence
    :type seq: sequence<str>
    :param tg_type: tango type
    :type tg_type: :class:`tango.CmdArgType`
    :param tg_format: (optional, default is None, meaning SCALAR) tango format
    :type tg_format: :class:`tango.AttrDataFormat`

    :return: a new sequence
    """
    if tg_format:
        return _seqStr_2_obj_from_type_format(seq, tg_type, tg_format)
    return _seqStr_2_obj_from_type(seq, tg_type)


def _seqStr_2_obj_from_type(seq, tg_type):
    if is_pure_str(seq):
        seq = (seq,)

    # Scalar cases
    global _scalar_int_types
    if tg_type in _scalar_int_types:
        return int(seq[0])

    global _scalar_float_types
    if tg_type in _scalar_float_types:
        return float(seq[0])

    global _scalar_str_types
    if tg_type in _scalar_str_types:
        return seq[0]

    if tg_type == CmdArgType.DevBoolean:
        return seq[0].lower() == "true"

    # sequence cases
    if tg_type in (CmdArgType.DevVarCharArray, CmdArgType.DevVarStringArray):
        return seq

    global _array_int_types
    if tg_type in _array_int_types:
        argout = []
        for x in seq:
            argout.append(int(x))
        return argout

    global _array_float_types
    if tg_type in _array_float_types:
        argout = []
        for x in seq:
            argout.append(float(x))
        return argout

    if tg_type == CmdArgType.DevVarBooleanArray:
        argout = []
        for x in seq:
            argout.append(x.lower() == "true")
        return argout

    return []


def _seqStr_2_obj_from_type_format(seq, tg_type, tg_format):
    if tg_format == AttrDataFormat.SCALAR:
        return _seqStr_2_obj_from_type(tg_type, seq)
    elif tg_format == AttrDataFormat.SPECTRUM:
        return _seqStr_2_obj_from_type(_scalar_to_array_type[tg_type], seq)
    elif tg_format == AttrDataFormat.IMAGE:
        if tg_type == CmdArgType.DevString:
            return seq

        global _scalar_int_types
        if tg_type in _scalar_int_types:
            argout = []
            for x in seq:
                tmp = []
                for y in x:
                    tmp.append(int(y))
                argout.append(tmp)
            return argout

        global _scalar_float_types
        if tg_type in _scalar_float_types:
            argout = []
            for x in seq:
                tmp = []
                for y in x:
                    tmp.append(float(y))
                argout.append(tmp)
            return argout

    # UNKNOWN_FORMAT
    return _seqStr_2_obj_from_type(tg_type, seq)


def scalar_to_array_type(tg_type):
    """
    Gives the array tango type corresponding to the given tango
    scalar type. Example: giving DevLong will return DevVarLongArray.

    :param tg_type: tango type
    :type tg_type: :class:`tango.CmdArgType`

    :return: the array tango type for the given scalar tango type
    :rtype: :class:`tango.CmdArgType`

    :raises ValueError: in case the given dtype is not a tango scalar type
    """
    try:
        return _scalar_to_array_type[tg_type]
    except KeyError:
        raise ValueError(f"Invalid tango scalar type: {tg_type}")


def str_2_obj(obj_str, tg_type=None):
    """Converts a string into an object according to the given tango type

    :param obj_str: the string to be converted
    :type obj_str: :py:obj:`str`
    :param tg_type: tango type
    :type tg_type: :class:`tango.CmdArgType`
    :return: an object calculated from the given string
    :rtype: :py:obj:`object`
    """
    if tg_type is None:
        return obj_str
    f = str
    if is_scalar_type(tg_type):
        if is_numerical_type(tg_type):
            if obj_str in __NO_STR_VALUE:
                return None
        if is_int_type(tg_type):
            f = int
        elif is_float_type(tg_type):
            f = float
        elif is_bool_type(tg_type):
            f = bool_
    return f(obj_str)


def obj_2_str(obj, tg_type=None):
    """Converts a python object into a string according to the given tango type

    :param obj: the object to be converted
    :type obj: :py:obj:`object`
    :param tg_type: tango type
    :type tg_type: :class:`tango.CmdArgType`
    :return: a string representation of the given object
    :rtype: :py:obj:`str`
    """
    if tg_type is None:
        return obj
    if tg_type in _scalar_types:
        # scalar cases
        if is_pure_str(obj):
            return obj
        elif is_non_str_seq(obj):
            if not len(obj):
                return ""
            obj = obj[0]
        return str(obj)
    # sequence cases
    if obj is None:
        return ""
    return "\n".join([str(i) for i in obj])


def obj_2_property(value):
    if isinstance(value, DbData):
        pass
    elif isinstance(value, DbDatum):
        new_value = DbData()
        new_value.append(value)
        value = new_value
    elif is_non_str_seq(value):
        value = seq_2_DbData(value)
    elif isinstance(value, collections.abc.Mapping):
        new_value = DbData()
        for k, v in value.items():
            if isinstance(v, DbDatum):
                new_value.append(v)
                continue
            db_datum = DbDatum(k)
            if is_non_str_seq(v):
                seq_2_StdStringVector(v, db_datum.value_string)
            else:
                if not is_pure_str(v):
                    v = str(v)
                v = ensure_binary(v, encoding="latin-1")
                db_datum.value_string.append(v)
            new_value.append(db_datum)
        value = new_value
    else:
        raise TypeError(
            "Value must be a tango.DbDatum, tango.DbData, "
            "a sequence<DbDatum> or a dictionary"
        )
    return value


def __get_meth_func(klass, method_name):
    meth = getattr(klass, method_name)
    func = meth
    if hasattr(meth, "__func__"):
        func = meth.__func__
    elif hasattr(meth, "im_func"):
        func = meth.im_func
    return meth, func


def copy_doc(klass, fnname):
    """Copies documentation string of a method from the super class into the
    rewritten method of the given class"""
    base_meth, base_func = __get_meth_func(klass.__base__, fnname)
    meth, func = __get_meth_func(klass, fnname)
    func.__doc__ = base_func.__doc__


def document_method(klass, method_name, d, add=True):
    meth, func = __get_meth_func(klass, method_name)
    if add:
        cpp_doc = meth.__doc__
        if cpp_doc:
            func.__doc__ = f"{d}\n{cpp_doc}"
            return
    func.__doc__ = d

    if func.__name__ != method_name:
        try:
            func.__name__ = method_name
        except AttributeError:
            pass


def document_static_method(klass, method_name, d, add=True):
    meth, func = __get_meth_func(klass, method_name)
    if add:
        cpp_doc = meth.__doc__
        if cpp_doc:
            meth.__doc__ = f"{d}\n{cpp_doc}"
            return
    meth.__doc__ = d


def document_enum(klass, enum_name, desc, append=True):
    # Get the original enum type
    enum_class = getattr(klass, enum_name)

    # fix the docstring
    # is __doc__ is not empty, expand with given desc
    if append and enum_class.__doc__ is not None:
        enum_class.__doc__ += "\n" + desc
    # otherwise make a new one
    else:
        enum_class.__doc__ = desc


class CaselessList(list):
    """A case insensitive lists that has some caseless methods. Only allows
    strings as list members. Most methods that would normally return a list,
    return a CaselessList. (Except list() and lowercopy())
    Sequence Methods implemented are :
    __contains__, remove, count, index, append, extend, insert,
    __getitem__, __setitem__, __getslice__, __setslice__
    __add__, __radd__, __iadd__, __mul__, __rmul__
    Plus Extra methods:
    findentry, copy , lowercopy, list
    Inherited methods :
    __imul__, __len__, __iter__, pop, reverse, sort
    """

    def __init__(self, inlist=[]):
        list.__init__(self)
        for entry in inlist:
            if not isinstance(entry, str):
                raise TypeError(
                    f"Members of this object must be strings. "
                    f'You supplied "{entry}" which is "{type(entry)}"'
                )
            self.append(entry)

    def findentry(self, item):
        """A caseless way of checking if an item is in the list or not.
        It returns None or the entry."""
        if not isinstance(item, str):
            raise TypeError(
                f'Members of this object must be strings. You supplied "{type(item)}"'
            )
        for entry in self:
            if item.lower() == entry.lower():
                return entry
        return None

    def __contains__(self, item):
        """A caseless way of checking if a list has a member in it or not."""
        for entry in self:
            if item.lower() == entry.lower():
                return True
        return False

    def remove(self, item):
        """Remove the first occurence of an item, the caseless way."""
        for entry in self:
            if item.lower() == entry.lower():
                list.remove(self, entry)
                return
        raise ValueError(": list.remove(x): x not in list")

    def copy(self):
        """Return a CaselessList copy of self."""
        return CaselessList(self)

    def list(self):
        """Return a normal list version of self."""
        return list(self)

    def lowercopy(self):
        """Return a lowercase (list) copy of self."""
        return [entry.lower() for entry in self]

    def append(self, item):
        """Adds an item to the list and checks it's a string."""
        if not isinstance(item, str):
            raise TypeError(
                f'Members of this object must be strings. You supplied "{type(item)}"'
            )
        list.append(self, item)

    def extend(self, item):
        """Extend the list with another list. Each member of the list must be
        a string."""
        if not isinstance(item, list):
            raise TypeError(
                f'You can only extend lists with lists. You supplied "{type(item)}"'
            )
        for entry in item:
            if not isinstance(entry, str):
                raise TypeError(
                    f"Members of this object must be strings. "
                    f'You supplied "{type(entry)}"'
                )
            list.append(self, entry)

    def count(self, item):
        """Counts references to 'item' in a caseless manner.
        If item is not a string it will always return 0."""
        if not isinstance(item, str):
            return 0
        count = 0
        for entry in self:
            if item.lower() == entry.lower():
                count += 1
        return count

    def index(self, item, minindex=0, maxindex=None):
        """Provide an index of first occurence of item in the list. (or raise
        a ValueError if item not present)
        If item is not a string, will raise a TypeError.
        minindex and maxindex are also optional arguments
        s.index(x[, i[, j]]) return smallest k such that s[k] == x and i <= k < j
        """
        if maxindex is None:
            maxindex = len(self)
        minindex = max(0, minindex) - 1
        maxindex = min(len(self), maxindex)
        if not isinstance(item, str):
            raise TypeError(
                f'Members of this object must be strings. You supplied "{type(item)}"'
            )
        index = minindex
        while index < maxindex:
            index += 1
            if item.lower() == self[index].lower():
                return index
        raise ValueError(": list.index(x): x not in list")

    def insert(self, i, x):
        """s.insert(i, x) same as s[i:i] = [x]
        Raises TypeError if x isn't a string."""
        if not isinstance(x, str):
            raise TypeError(
                f'Members of this object must be strings. You supplied "{type(x)}"'
            )
        list.insert(self, i, x)

    def __setitem__(self, index, value):
        """For setting values in the list.
        index must be an integer or (extended) slice object. (__setslice__ used
        for simple slices)
        If index is an integer then value must be a string.
        If index is a slice object then value must be a list of strings - with
        the same length as the slice object requires.
        """
        if isinstance(index, int):
            if not isinstance(value, str):
                raise TypeError(
                    f"Members of this object must be strings. "
                    f'You supplied "{type(value)}"'
                )
            list.__setitem__(self, index, value)
        elif isinstance(index, slice):
            if not hasattr(value, "__len__"):
                raise TypeError("Value given to set slice is not a sequence object.")
            for entry in value:
                if not isinstance(entry, str):
                    raise TypeError(
                        f"Members of this object must be strings. "
                        f'You supplied "{type(entry)}"'
                    )
            list.__setitem__(self, index, value)
        else:
            raise TypeError("Indexes must be integers or slice objects.")

    def __setslice__(self, i, j, sequence):
        """Called to implement assignment to self[i:j]."""
        for entry in sequence:
            if not isinstance(entry, str):
                raise TypeError(
                    f"Members of this object must be strings. "
                    f'You supplied "{type(entry)}"'
                )
        list.__setslice__(self, i, j, sequence)

    def __getslice__(self, i, j):
        """Called to implement evaluation of self[i:j].
        Although the manual says this method is deprecated - if I don't define
        it the list one is called.
        (Which returns a list - this returns a CaselessList)"""
        return CaselessList(list.__getslice__(self, i, j))

    def __getitem__(self, index):
        """For fetching indexes.
        If a slice is fetched then the list returned is a CaselessList."""
        if not isinstance(index, slice):
            return list.__getitem__(self, index)
        else:
            return CaselessList(list.__getitem__(self, index))

    def __add__(self, item):
        """To add a list, and return a CaselessList.
        Every element of item must be a string."""
        return CaselessList(list.__add__(self, item))

    def __radd__(self, item):
        """To add a list, and return a CaselessList.
        Every element of item must be a string."""
        return CaselessList(list.__add__(self, item))

    def __iadd__(self, item):
        """To add a list in place."""
        for entry in item:
            self.append(entry)

    def __mul__(self, item):
        """To multiply itself, and return a CaselessList.
        Every element of item must be a string."""
        return CaselessList(list.__mul__(self, item))

    def __rmul__(self, item):
        """To multiply itself, and return a CaselessList.
        Every element of item must be a string."""
        return CaselessList(list.__rmul__(self, item))


class CaselessDict(dict):
    def __init__(self, other=None):
        if other:
            # Doesn't do keyword args
            if isinstance(other, dict):
                for k, v in other.items():
                    dict.__setitem__(self, k.lower(), v)
            else:
                for k, v in other:
                    dict.__setitem__(self, k.lower(), v)

    def __getitem__(self, key):
        return dict.__getitem__(self, key.lower())

    def __setitem__(self, key, value):
        dict.__setitem__(self, key.lower(), value)

    def __contains__(self, key):
        return dict.__contains__(self, key.lower())

    def __delitem__(self, k):
        dict.__delitem__(self, k.lower())

    def has_key(self, key):
        return key.lower() in self

    def get(self, key, def_val=None):
        return dict.get(self, key.lower(), def_val)

    def setdefault(self, key, def_val=None):
        return dict.setdefault(self, key.lower(), def_val)

    def update(self, other):
        for k, v in other.items():
            dict.__setitem__(self, k.lower(), v)

    def fromkeys(self, iterable, value=None):
        d = CaselessDict()
        for k in iterable:
            dict.__setitem__(d, k.lower(), value)
        return d

    def pop(self, key, def_val=None):
        return dict.pop(self, key.lower(), def_val)

    def keys(self):
        return CaselessList(dict.keys(self))


class EventCallback:
    """
    Useful event callback for test purposes

    Usage::

        >>> dev = tango.DeviceProxy(dev_name)
        >>> cb = tango.utils.EventCallback()
        >>> id = dev.subscribe_event("state", tango.EventType.CHANGE_EVENT, cb, [])
        2011-04-06 15:33:18.910474 sys/tg_test/1 STATE CHANGE [ATTR_VALID] ON

    Allowed format keys are:

        - date (event timestamp)
        - reception_date (event reception timestamp)
        - type (event type)
        - dev_name (device name)
        - name (attribute name)
        - value (event value)

    New in PyTango 7.1.4
    """

    def __init__(
        self,
        format="{date} {dev_name} {name} {type} {value}",
        fd=sys.stdout,
        max_buf=100,
    ):
        self._msg = format
        self._fd = fd
        self._evts = []
        self._max_buf = max_buf

    def get_events(self):
        """Returns the list of events received by this callback

        :return: the list of events received by this callback
        :rtype: sequence<obj>
        """
        return self._evts

    def push_event(self, evt):
        """Internal usage only"""
        try:
            self._push_event(evt)
        except Exception as e:
            print(f"Unexpected error in callback for {evt}: {e}", file=self._fd)

    def _push_event(self, evt):
        """Internal usage only"""
        self._append(evt)
        import datetime

        now = datetime.datetime.now()
        try:
            date = self._get_date(evt)
        except Exception:
            date = now
        try:
            reception_date = evt.reception_date.todatetime()
        except Exception:
            reception_date = now
        try:
            evt_type = evt.event.upper()
        except Exception:
            evt_type = "<UNKNOWN>"
        try:
            dev_name = evt.device.dev_name().upper()
        except Exception:
            dev_name = "<UNKNOWN>"
        try:
            attr_name = evt.attr_name.split("/")[-1].upper()
        except Exception:
            attr_name = "<UNKNOWN>"
        try:
            value = self._get_value(evt)
        except Exception as e:
            value = f"Unexpected exception in getting event value: {e}"
        d = {
            "date": date,
            "reception_date": reception_date,
            "type": evt_type,
            "dev_name": dev_name,
            "name": attr_name,
            "value": value,
        }
        print(self._msg.format(**d), file=self._fd)

    def _append(self, evt):
        """Internal usage only"""
        evts = self._evts
        if len(evts) == self._max_buf:
            evts.pop(0)
        evts.append(evt)

    def _get_date(self, evt):
        if isinstance(evt, EventData):
            return evt.attr_value.time.todatetime()
        elif isinstance(evt, PipeEventData):
            return evt.pipe_value.time.todatetime()
        else:
            return evt.get_date().todatetime()

    def _get_value(self, evt):
        """Internal usage only"""
        if evt.err:
            e = evt.errors[0]
            return f"[{e.reason}] {e.desc}"

        if isinstance(evt, EventData):
            return f"[{evt.attr_value.quality}] {evt.attr_value.value}"
        elif isinstance(evt, AttrConfEventData):
            cfg = evt.attr_conf
            return f"label='{cfg.label}'; unit='{cfg.unit}'"
        elif isinstance(evt, DataReadyEventData):
            return ""
        elif isinstance(evt, PipeEventData):
            return evt.pipe_value
        elif isinstance(evt, DevIntrChangeEventData):
            print("utils::_get_value()")
            return


class AsyncEventCallback(EventCallback):
    async def push_event(self, evt):
        """Internal usage only"""
        try:
            self._push_event(evt)
        except Exception as e:
            print(f"Unexpected error in callback for {evt}: {e}", file=self._fd)


def get_home():
    """
    Find user's home directory if possible. Otherwise raise error.

    :return: user's home directory
    :rtype: :py:obj:`str`

    New in PyTango 7.1.4
    """
    path = ""
    try:
        path = os.path.expanduser("~")
    except Exception:
        pass
    if not os.path.isdir(path):
        for evar in ("HOME", "USERPROFILE", "TMP"):
            try:
                path = os.environ[evar]
                if os.path.isdir(path):
                    break
            except Exception:
                pass
    if path:
        return path
    else:
        raise RuntimeError("please define environment variable $HOME")


def _get_env_var(env_var_name):
    """
    Returns the value for the given environment name

    Search order:

        * a real environ var
        * HOME/.tangorc
        * /etc/tangorc

    :param env_var_name: the environment variable name
    :type env_var_name: str
    :return: the value for the given environment name
    :rtype: str

    New in PyTango 7.1.4
    """

    if env_var_name in os.environ:
        return os.environ[env_var_name]

    fname = os.path.join(get_home(), ".tangorc")
    if not os.path.exists(fname):
        if os.name == "posix":
            fname = "/etc/tangorc"
    if not os.path.exists(fname):
        return None

    for line in open(fname):
        strippedline = line.split("#", 1)[0].strip()

        if not strippedline:
            # empty line
            continue

        tup = strippedline.split("=", 1)
        if len(tup) != 2:
            # illegal line!
            continue

        key, val = map(str.strip, tup)
        if key == env_var_name:
            return val


def from_version_str_to_hex_str(version_str):
    v = map(int, version_str.split("."))
    return "0x%02d%02d%02d00" % (v[0], v[1], v[2])


def from_version_str_to_int(version_str):
    return int(from_version_str_to_hex_str(version_str), 16)


def info():
    # Compile and Runtime are set by `tango.pytango_init.init`
    from tango.constants import Compile, Runtime

    msg = f"""\
PyTango {Release.version_long} {Release.version_info}
PyTango compiled with:
    Python : {Compile.PY_VERSION}
    Numpy  : {Compile.NUMPY_VERSION}
    Tango  : {Compile.TANGO_VERSION}
    Boost  : {Compile.BOOST_VERSION}

PyTango runtime is:
    Python : {Runtime.PY_VERSION}
    Numpy  : {Runtime.NUMPY_VERSION}
    Tango  : {Runtime.TANGO_VERSION}

PyTango running on:
{Runtime.UNAME}
"""
    return msg


def get_attrs(obj):
    """Helper for dir2 implementation."""
    if not hasattr(obj, "__dict__"):
        return []  # slots only
    proxy_type = types.MappingProxyType
    if not isinstance(obj.__dict__, (dict, proxy_type)):
        print(type(obj.__dict__), obj)
        raise TypeError(f"{obj.__name__}.__dict__ is not a dictionary")
    return obj.__dict__.keys()


def dir2(obj):
    """Default dir implementation.

    Inspired by gist: katyukha/dirmixin.py
    https://gist.github.com/katyukha/c6e5e2b829e247c9b009
    """
    attrs = set()

    if not hasattr(obj, "__bases__"):
        # obj is an instance
        if not hasattr(obj, "__class__"):
            # slots
            return sorted(get_attrs(obj))
        klass = obj.__class__
        attrs.update(get_attrs(klass))
    else:
        # obj is a class
        klass = obj

    for cls in klass.__bases__:
        attrs.update(get_attrs(cls))
        attrs.update(dir2(cls))
    attrs.update(get_attrs(obj))
    return list(attrs)


def ensure_binary(s, encoding="utf-8", errors="strict"):
    """Coerce **s** to the bytes type.
    For Python 3:
        - `str` -> encoded to `bytes`
        - `bytes` -> `bytes`

    Code taken from https://github.com/benjaminp/six/blob/1.12.0/six.py#L853
    """
    if isinstance(s, str):
        return s.encode(encoding, errors)
    elif isinstance(s, bytes):
        return s
    else:
        raise TypeError(f"not expecting type '{type(s)}'")


class PyTangoHelpFormatter(HelpFormatter):
    def _format_usage(self, usage, actions, groups, prefix):
        usage = super()._format_usage(usage, actions, groups, prefix)
        try:
            db = Database()
            servers_list = db.get_instance_name_list(self._prog)
            if servers_list.size():
                usage += (
                    f"Instance names defined in database for server {self._prog}:\n"
                )
                for server in servers_list:
                    usage += "\t" + str(server) + "\n"
            else:
                usage += f"Warning! No defined instance in database for server {self._prog} found!\n"
        except DevFailed:
            pass

        return usage


__TEST_CONTEXT_HOST_TRL = None


def _set_test_context_tango_host_fqtrl(host_trl):
    """For PyTango internal use only!"""
    # NOTE: we only keep one value so if multiple TestContexts are started in
    # the same process, only the latest one will be used
    if host_trl is not None:
        global __TEST_CONTEXT_HOST_TRL
        __TEST_CONTEXT_HOST_TRL = host_trl


def _clear_test_context_tango_host_fqtrl():
    """For PyTango internal use only!"""
    global __TEST_CONTEXT_HOST_TRL
    __TEST_CONTEXT_HOST_TRL = None


def _get_test_context_tango_host_fqtrl():
    """For PyTango internal use only!"""
    return __TEST_CONTEXT_HOST_TRL


def _get_device_fqtrl_if_necessary(device_trl):
    """For PyTango internal use only!"""
    if __TEST_CONTEXT_HOST_TRL:
        device_trl = _get_device_fqtrl(device_trl, __TEST_CONTEXT_HOST_TRL)
    return device_trl


def _get_device_fqtrl(device_trl, host_trl):
    parsed_device = urlparse(device_trl)
    if not _is_tango_uri_resolved(parsed_device):
        parsed_host = urlparse(host_trl)
        device_trl = _try_resolve_tango_trl(parsed_host, parsed_device)
    return device_trl


def _is_tango_uri_resolved(parsed_device):
    return parsed_device.scheme == "tango"


def _try_resolve_tango_trl(parsed_host, parsed_device):
    if not _is_valid_tango_trl(parsed_host):
        raise InvalidTangoHostTrlError(
            f"Invalid form for Tango host: {parsed_host!r}, device {parsed_device!r}. "
            f"(Override set to: {__TEST_CONTEXT_HOST_TRL})."
        )
    return _resolve_tango_trl(parsed_host, parsed_device)


def _is_valid_tango_trl(parsed_host):
    scheme_ok = parsed_host.scheme == "tango"
    hostname_ok = bool(parsed_host.hostname)
    port_ok = bool(parsed_host.port)
    path_ok = parsed_host.path == ""
    params_ok = parsed_host.params == ""
    query_ok = parsed_host.query == ""
    fragment_ok = parsed_host.fragment in ["", "dbase=no", "dbase=yes"]
    return (
        scheme_ok
        and hostname_ok
        and port_ok
        and path_ok
        and params_ok
        and query_ok
        and fragment_ok
    )


def _resolve_tango_trl(parsed_host, parsed_device):
    return urlunparse(
        [
            parsed_host.scheme,
            parsed_host.netloc,
            parsed_device.path,
            parsed_host.params,
            parsed_host.query,
            parsed_host.fragment,
        ]
    )


class InvalidTangoHostTrlError(ValueError):
    """Invalid Tango Resource Locator format for TANGO_HOST-like variable."""


class PyTangoUserWarning(UserWarning):
    # a custom category for all PyTango's warnings to give users the option of filtering PyTango's warnings
    pass


def _is_coroutine_function(obj):
    while isinstance(obj, functools.partial):
        obj = obj.func

    return inspect.iscoroutinefunction(obj) or (
        callable(obj) and inspect.iscoroutinefunction(obj.__call__)
    )


def _truthy_env_var(name) -> bool:
    value = ApiUtil.get_env_var(name)
    if value and value.lower() in {"on", "1", "true", "yes", "y"}:
        return True
    return False


_coverage_run_active = False

try:
    import coverage

    if coverage.Coverage.current():
        if _truthy_env_var("PYTANGO_DISABLE_COVERAGE_TRACE_PATCHING"):
            warnings.warn(
                "Coverage run detected, but PYTANGO_DISABLE_COVERAGE_TRACE_PATCHING "
                "environment variable is set. Reported coverage may be inaccurate.",
                category=PyTangoUserWarning,
            )
        else:
            if getattr(threading, "_trace_hook", None):
                _coverage_run_active = True
                warnings.warn(
                    "Coverage run detected: tango.server.Device methods "
                    "will be patched for tracing.",
                    category=PyTangoUserWarning,
                )
            else:
                warnings.warn(
                    "Coverage run detected, but unable to get threading._trace_hook. "
                    "Reported coverage may be inaccurate.",
                    category=PyTangoUserWarning,
                )

except Exception:
    pass

_traced_debug_run_active = False
pydevd = None

try:
    _disabled_via_env_var = _truthy_env_var("PYTANGO_DISABLE_DEBUG_TRACE_PATCHING")
    if not _disabled_via_env_var:
        _forced_via_env_var = _truthy_env_var("PYTANGO_FORCE_DEBUG_TRACE_PATCHING")
        if sys.version_info < (3, 12) or _forced_via_env_var:
            if "PYDEVD_DISABLE_FILE_VALIDATION" not in os.environ:
                os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"
            import pydevd

            _debugger = pydevd.get_global_debugger()
        else:
            # we assume debugger using sys.monitoring hooks so it doesn't need patching
            _debugger = None

        if _debugger is not None:
            if _coverage_run_active:
                warnings.warn(
                    "Debugger detected, but coverage run also detected. "
                    "Patching only for coverage, not for debugger.",
                    category=PyTangoUserWarning,
                )
            else:
                _traced_debug_run_active = True
                warnings.warn(
                    "Debugger detected: tango.server.Device methods "
                    "will be patched for tracing.",
                    category=PyTangoUserWarning,
                )
except Exception:
    pass


_telemetry_active = False
try:
    _globally_enabled_via_env_var = _truthy_env_var("TANGO_TELEMETRY_ENABLE")
    _locally_disabled_via_env_var = _truthy_env_var(
        "PYTANGO_DISABLE_TELEMETRY_PATCHING"
    )
    if (
        _globally_enabled_via_env_var
        and not _locally_disabled_via_env_var
        and TELEMETRY_SUPPORTED
    ):
        from opentelemetry import trace as trace_api
        from opentelemetry.trace.propagation.tracecontext import (
            TraceContextTextMapPropagator,
        )

        _traces_exporter_type = ApiUtil.get_env_var("TANGO_TELEMETRY_TRACES_EXPORTER")
        if not _traces_exporter_type:
            _traces_exporter_type = "console"
        _traces_exporter_endpoint = ApiUtil.get_env_var(
            "TANGO_TELEMETRY_TRACES_ENDPOINT"
        )

        _telemetry_sdk_available = False
        try:
            _traces_exporter_kwargs = {}
            if _traces_exporter_type.lower() == "grpc":
                from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
                    OTLPSpanExporter as SpanExporter,
                )

                if _traces_exporter_endpoint:
                    _traces_exporter_endpoint = _traces_exporter_endpoint.lower()
                    if _traces_exporter_endpoint.startswith("grpc://"):
                        # cppTango requires endpoints starting "grpc://" for gRPC, even
                        # though this is a non-standard scheme.  We convert to
                        # the more standard http:// for the OTel exporter library.
                        _traces_exporter_endpoint = _traces_exporter_endpoint.replace(
                            "grpc://", "http://"
                        )
                    _traces_exporter_kwargs = {"endpoint": _traces_exporter_endpoint}
            elif _traces_exporter_type.lower() == "http":
                from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
                    OTLPSpanExporter as SpanExporter,
                )

                if _traces_exporter_endpoint:
                    _traces_exporter_kwargs = {"endpoint": _traces_exporter_endpoint}
            elif _traces_exporter_type.lower() == "none":
                SpanExporter = None
            else:
                from opentelemetry.sdk.trace.export import (
                    ConsoleSpanExporter as SpanExporter,
                )

                if _traces_exporter_endpoint:
                    if _traces_exporter_endpoint.lower() == "cerr":
                        _traces_exporter_kwargs = {"out": sys.stderr}
                    else:
                        _traces_exporter_kwargs = {"out": sys.stdout}

                if _traces_exporter_type.lower() != "console":
                    warnings.warn(
                        f"Unknown value '{_traces_exporter_type}' for "
                        f"TANGO_TELEMETRY_TRACES_EXPORTER. Options are: "
                        f"'console', 'grpc', 'http' and 'none'. Defaulting to 'console'."
                    )
                    _traces_exporter_type = "console"

            from opentelemetry.sdk.resources import (
                HOST_NAME,
                SERVICE_INSTANCE_ID,
                SERVICE_NAME,
                SERVICE_NAMESPACE,
                Resource,
            )
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import (
                BatchSpanProcessor,
                SimpleSpanProcessor,
            )

            _telemetry_sdk_available = True
        except ImportError:
            warnings.warn(
                "OpenTelemetry SDK packages not available: "
                "no telemetry traces will be emitted from this device/client.\n"
                "To emit telemetry, install the SDK packages: "
                "opentelemetry-sdk and either:\n"
                "  opentelemetry-exporter-otlp-proto-grpc (for traces via gRPC), or\n"
                "  opentelemetry-exporter-otlp-proto-http (for traces via HTTP).\n"
                "This warning can be disabled.\n"
                "  Either set environment variable PYTANGO_DISABLE_TELEMETRY_PATCHING=on"
                " to disable PyTango's usage of telemetry.\n"
                "  Or, set the environment variable TANGO_TELEMETRY_ENABLE=off to "
                "disable all telemetry in cppTango and PyTango.",
                category=PyTangoUserWarning,
            )

        @contextlib.contextmanager
        def _span_from_cpptango(
            device: "tango.server.Device", fn: callable  # noqa: F821
        ) -> typing.Iterator[trace_api.Span]:
            fn = inspect.unwrap(fn)
            name = getattr(fn, "__qualname__", getattr(fn, "__name__", "unknown"))
            carrier = _telemetry.get_trace_context()
            ctx = TraceContextTextMapPropagator().extract(carrier=carrier)
            device_tracer = device.get_telemetry_tracer()
            token = _current_telemetry_tracer.set(device_tracer)
            try:
                with device_tracer.start_as_current_span(
                    name, context=ctx, kind=trace_api.SpanKind.SERVER
                ) as span:
                    span.set_attribute("code.filepath", fn.__code__.co_filename)
                    span.set_attribute("code.lineno", fn.__code__.co_firstlineno)
                    current_thread = threading.current_thread()
                    span.set_attribute("thread.id", hex(current_thread.ident))
                    span.set_attribute("thread.name", current_thread.name)
                    yield span
            finally:
                _current_telemetry_tracer.reset(token)

        @contextlib.contextmanager
        def _span_to_cpptango(name: str):
            # use propagator to get W3C strings from active Python OpenTelemetry context
            carrier = {}
            TraceContextTextMapPropagator().inject(carrier)
            traceparent = carrier.get("traceparent", "")
            tracestate = carrier.get("tracestate", "")
            # create C++ TraceContextScope and set context from Python context
            with _telemetry.TraceContextScope(name, traceparent, tracestate):
                yield

        def _default_telemetry_tracer_provider_factory(
            service_name: str,
            service_instance_id: typing.Union[None, str] = None,
            extra_resource_attributes: typing.Union[None, dict[str, str]] = None,
        ) -> trace_api.TracerProvider:
            """Create default telemetry TracerProvider for a device.

            A TraceProvider is not used directly, but rather used to create a Tracer.

            See also OpenTelemetry's OTEL_EXPERIMENTAL_RESOURCE_DETECTORS environment
            variable, and other resource detectors. It may be possible to add additional
            information just using this environment variable.
            """
            if _telemetry_sdk_available and SpanExporter is not None:
                resource_attributes = {
                    HOST_NAME: socket.getfqdn(),
                    SERVICE_NAMESPACE: "tango",
                    SERVICE_NAME: service_name,
                }
                if service_instance_id:
                    resource_attributes[SERVICE_INSTANCE_ID] = service_instance_id
                if extra_resource_attributes:
                    resource_attributes.update(extra_resource_attributes)
                tracer_provider = TracerProvider(
                    resource=Resource.create(resource_attributes)
                )
                exporter = SpanExporter(**_traces_exporter_kwargs)
                processor = _create_span_processor(exporter)
                tracer_provider.add_span_processor(processor)
            else:
                tracer_provider = trace_api.NoOpTracerProvider()
            return tracer_provider

        def _create_span_processor(exporter):
            processor_type = ApiUtil.get_env_var(
                "PYTANGO_TELEMETRY_SPAN_PROCESSOR_TYPE"
            )
            if processor_type and processor_type.lower() == "simple":
                processor_class = SimpleSpanProcessor
            elif processor_type and processor_type.lower() == "batch":
                processor_class = BatchSpanProcessor
            else:
                if _traces_exporter_type.lower() == "console":
                    processor_class = SimpleSpanProcessor
                else:
                    processor_class = BatchSpanProcessor
            processor = processor_class(exporter)
            return processor

        def _create_device_telemetry_tracer(
            tracer_provider: trace_api.TracerProvider,
        ) -> trace_api.Tracer:
            """Create a standard telemetry Tracer for a device."""
            # See the following link for details on tracer naming:
            #   https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/trace/api.md#get-a-tracer
            # cppTango uses "tango.cpp".  We use "tango.python.server"
            device_tracer = trace_api.get_tracer(
                instrumenting_module_name="tango.python.server",
                instrumenting_library_version=Release.version,
                tracer_provider=tracer_provider,
            )
            return device_tracer

        def _create_client_telemetry_tracer() -> trace_api.Tracer:
            service_name = ApiUtil.get_env_var("PYTANGO_TELEMETRY_CLIENT_SERVICE_NAME")
            if not service_name:
                service_name = "pytango.client"
            tracer_provider_factory = get_telemetry_tracer_provider_factory()
            tracer_provider = tracer_provider_factory(service_name)
            # See comment in _create_device_telemetry_tracer about naming.
            # We differentiate between client and server tracers.
            tracer = trace_api.get_tracer(
                instrumenting_module_name="tango.python.client",
                instrumenting_library_version=Release.version,
                tracer_provider=tracer_provider,
            )
            return tracer

        @atexit.register
        def _shutdown_telemetry():
            _telemetry.cleanup_default_telemetry_interface()

        def _set_telemetry_sdk_log_level():
            level_str = ApiUtil.get_env_var("PYTANGO_TELEMETRY_SDK_LOG_LEVEL")
            if level_str:
                level_int = logging.getLevelNamesMapping()[level_str.upper()]
                names_csv = ApiUtil.get_env_var("PYTANGO_TELEMETRY_SDK_LOGGER_NAMES")
                if names_csv:
                    names = names_csv.split(",")
                else:
                    names = [
                        "opentelemetry.sdk.trace.export",
                        "opentelemetry.sdk._shared_internal",
                    ]
                for name in names:
                    logging.getLogger(name).setLevel(level_int)
                _telemetry.set_log_level(level_str)

        _set_telemetry_sdk_log_level()

        _telemetry_client_tracer: typing.Union[None, trace_api.Tracer] = None
        _telemetry_active = True
except ImportError:
    warnings.warn(
        "\nOpenTelemetry packages not available: \n"
        "telemetry context will not be passed to other Tango devices, "
        "and no telemetry will be emitted from this device/client.\n"
        "To pass through telemetry context, install the API packages: "
        "opentelemetry-api\n"
        "To emit telemetry, install the SDK packages: "
        "opentelemetry-sdk and either:\n"
        "  opentelemetry-exporter-otlp-proto-grpc (for traces via gRPC), or\n"
        "  opentelemetry-exporter-otlp-proto-http (for traces via HTTP).\n"
        "This warning can be disabled:\n"
        "  Either set environment variable PYTANGO_DISABLE_TELEMETRY_PATCHING=on "
        "to disable PyTango's usage of telemetry.\n"
        "  Or, set the environment variable TANGO_TELEMETRY_ENABLE=off to disable "
        "all telemetry in cppTango and PyTango.",
        category=PyTangoUserWarning,
    )
except Exception as exc:
    warnings.warn(
        f"Error setting up telemetry. Telemetry context may not be passed on "
        f"and traces may not be emitted. Possibly a PyTango bug.\n"
        f"Error: {exc!r}"
    )


_DummySpanContext = namedtuple(
    "_DummySpanContext",
    ["trace_id", "span_id", "is_remote", "trace_flags", "trace_state", "is_valid"],
)


class _DummySpan:
    def set_attributes(self, *args, **kwargs):
        pass

    def set_attribute(self, *args, **kwargs):
        pass

    def add_event(self, *args, **kwargs):
        pass

    def add_link(self, *args, **kwargs):
        pass

    def update_name(self, *args, **kwargs):
        pass

    def is_recording(self):
        return False

    def set_status(self, *args, **kwargs):
        pass

    def record_exception(self, *args, **kwargs):
        pass

    def end(self, *args, **kwargs):
        pass

    def get_span_context(self):
        return _DummySpanContext(0, 0, False, 0, {}, False)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.end()


class _DummyTracer:
    def start_span(self, *args, **kwargs):
        pass

    @contextlib.contextmanager
    def start_as_current_span(self, *args, **kwargs):
        yield _DummySpan()


class _DummyTracerProvider:
    def get_tracer(self, *args, **kwargs):
        return _DummyTracer()


if not _telemetry_active:
    # define dummy handlers

    @contextlib.contextmanager
    def _span_to_cpptango():
        yield

    def _default_telemetry_tracer_provider_factory(
        service_name, service_instance_id=None, extra_resource_attributes=None
    ):
        return _DummyTracerProvider()

    def _create_device_telemetry_tracer(tracer_provider) -> _DummyTracer:
        return _DummyTracer()

    _telemetry_client_tracer = None

_current_telemetry_tracer = ContextVar("current_telemetry_tracer")

_current_telemetry_tracer_provider_factory = _default_telemetry_tracer_provider_factory


class _TracerProviderFactory(typing.Protocol):
    def __call__(
        self,
        service_name: str,
        service_instance_id: typing.Union[None, str] = None,
        extra_resource_attributes: typing.Union[None, dict[str, str]] = None,
    ) -> "opentelemetry.trace.TracerProvider":  # noqa: F821
        ...


def set_telemetry_tracer_provider_factory(provider_factory: _TracerProviderFactory):
    """Change the factory that will be used to create tracer providers.

    The factory is called when a tracer provider needs to be created.
    I.e., once for client access, and once for each device.
    """
    global _current_telemetry_tracer_provider_factory
    _current_telemetry_tracer_provider_factory = provider_factory


def get_telemetry_tracer_provider_factory() -> _TracerProviderFactory:
    """Get the factory that will be used to create tracer providers."""
    return _current_telemetry_tracer_provider_factory


_force_tracing = _traced_debug_run_active or _coverage_run_active or _telemetry_active


def _forcefully_traced_method(fn, is_kernel_method=False):
    # late import to avoid circular reference
    from tango.server import BaseDevice

    unwrapped_fn = inspect.unwrap(fn)

    def _get_device_telemetry_required(*args):
        device = None
        telemetry_required = False
        if _telemetry_active and args:
            first = args[0]
            if isinstance(first, BaseDevice):
                device = first
            else:
                fn_self = getattr(unwrapped_fn, "__self__", None)
                if isinstance(fn_self, BaseDevice):
                    device = fn_self
            if device is not None:
                telemetry_required = device.is_telemetry_enabled() and (
                    not is_kernel_method or device.is_kernel_tracing_enabled()
                )
        return device, telemetry_required

    def _set_sys_tracer_and_get_original():
        original_sys_tracer = "EMPTY"

        if _coverage_run_active:
            original_sys_tracer = sys.gettrace()
            threading_trace_hook = getattr(threading, "_trace_hook", None)
            if threading_trace_hook:
                sys.settrace(threading_trace_hook)
        elif _traced_debug_run_active and pydevd is not None:
            pydevd.settrace(suspend=False, trace_only_current_thread=True)

        return original_sys_tracer

    @functools.wraps(fn)
    def trace_wrapper(*args, **kwargs):
        device, telemetry_required = _get_device_telemetry_required(*args)
        original_sys_tracer = _set_sys_tracer_and_get_original()
        try:
            if telemetry_required and device is not None:
                with _span_from_cpptango(device, fn):
                    ret = fn(*args, **kwargs)
            else:
                ret = fn(*args, **kwargs)
        finally:
            if original_sys_tracer != "EMPTY":
                sys.settrace(original_sys_tracer)
        return ret

    @functools.wraps(fn)
    async def async_trace_wrapper(*args, **kwargs):
        device, telemetry_required = _get_device_telemetry_required(*args)
        original_sys_tracer = _set_sys_tracer_and_get_original()
        try:
            if telemetry_required and device is not None:
                with _span_from_cpptango(device, fn):
                    ret = await fn(*args, **kwargs)
            else:
                ret = await fn(*args, **kwargs)
        finally:
            if original_sys_tracer != "EMPTY":
                sys.settrace(original_sys_tracer)
        return ret

    if _is_coroutine_function(fn):
        return async_trace_wrapper
    else:
        return trace_wrapper


def _trace_client(fn):
    """Wrapper/decorator to trace a client function for telemetry."""

    if _telemetry_active:
        # Change function names like "__DeviceProxy__subscribe_event" to
        # "DeviceProxy.subscribe_event" for better readability
        fn_name = getattr(fn, "__qualname__", getattr(fn, "__name__", "unknown"))
        match = re.match(r"__(?P<prefix>\w+?)__(?P<suffix>.*)", fn_name)
        if match:
            fn_name = f"{match.group('prefix')}.{match.group('suffix')}"

        @functools.wraps(fn)
        def client_trace_wrapper(*args, **kwargs):
            global _telemetry_client_tracer
            if _telemetry_client_tracer is None:
                _telemetry_client_tracer = _create_client_telemetry_tracer()
            tracer = _current_telemetry_tracer.get(_telemetry_client_tracer)
            filename, lineno, qualname = _get_non_tango_source_location()
            with tracer.start_as_current_span(
                qualname, kind=trace_api.SpanKind.CLIENT
            ) as span:
                span.set_attribute("code.filepath", filename)
                span.set_attribute("code.lineno", lineno)
                current_thread = threading.current_thread()
                span.set_attribute("thread.id", hex(current_thread.ident))
                span.set_attribute("thread.name", current_thread.name)
                with _span_to_cpptango(fn_name):
                    return fn(*args, **kwargs)

    else:
        client_trace_wrapper = fn

    return client_trace_wrapper


_SourceLocation = namedtuple("_SourceLocation", ("filepath", "lineno", "qualname"))


def _get_non_tango_source_location(
    source: typing.Union[callable, None] = None
) -> _SourceLocation:
    """Provides non-PyTango source caller for logging and tracing functions.

    :param source:
        (optional) Method or function, which will be unwrapped of decorated wrappers
        and inspected for location. If not provided - current stack will be used to
        deduce the location.
    :type source: Callable

    :return:
        Named tuple (filepath, lineno, qualname)
    :rtype :_SourceLocation:
    """
    try:
        if source:
            # If source is a wrapped function - unwrap it to inner function
            source = inspect.unwrap(source)
            # Find callable code location
            code = getattr(source, "__code__", None)
            if code:
                filepath = code.co_filename
                lineno = code.co_firstlineno
                qualname = getattr(
                    code, "co_qualname", getattr(code, "co_name", str(source))
                )
                return _SourceLocation(filepath, lineno, qualname)
        else:
            caller, module = _get_first_non_tango_caller_and_module()
            if caller:
                code = caller.f_code
                filepath = code.co_filename
                lineno = caller.f_lineno
                qualname = getattr(
                    code,
                    "co_qualname",
                    getattr(code, "co_name", "unknown"),
                )
                if qualname == "<module>" and module in ("__main__", "__mp_main__"):
                    qualname = module
                return _SourceLocation(filepath, lineno, qualname)
        return _SourceLocation("(unknown)", 0, str(source))
    except Exception:
        return _SourceLocation("(unknown)", 0, str(source))


# Search the call stack until we are out of the 'tango' module. We cannot
# have a fixed number here because loggers/streams/tracing is used in many places
# inside pytango with varying call stack depth.
#
# There are different option below which trade compatibility for speed (fastest first).
if hasattr(sys, "_getframemodulename") and hasattr(sys, "_getframe"):

    def _get_first_non_tango_caller_and_module():
        depth = 2
        caller = None
        while True:
            module = sys._getframemodulename(depth)  # added in Python 3.12
            if module != "tango" and not module.startswith("tango."):
                caller = sys._getframe(depth)
                break
            elif module is None:
                break  # stack exhausted
            depth += 1
        if caller:
            return caller, module
        else:
            return None, ""

elif hasattr(sys, "_getframe"):

    def _get_first_non_tango_caller_and_module():
        depth = 2
        caller = None
        module = ""
        try:
            while True:
                caller = sys._getframe(depth)
                module = caller.f_globals["__name__"]
                if module != "tango" and not module.startswith("tango."):
                    break
                depth += 1
        except ValueError:
            pass  # stack exhausted
        if caller:
            return caller, module
        else:
            return None, ""

else:
    # use inspect (the slowest approach, most portable)
    def _get_first_non_tango_caller_and_module():
        for caller, _, _, _, _, _ in inspect.stack(0):
            module = caller.f_globals["__name__"]
            if module != "tango" and not module.startswith("tango."):
                return caller, module
        return None, ""


# Since cppTango based on omniThreads, we have to slightly modify ThreadPoolExecutor,
# to use threads with ensured dummy omniORB ID
#
# The `_adjust_thread_count` method below is a slightly modified version of the code from
# https://github.com/python/cpython/blob/3.12/Lib/concurrent/futures/thread.py

# Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
# 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022,
# 2023 Python Software Foundation;
# All Rights Reserved

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures.thread import _worker, _threads_queues


class PyTangoThreadPoolExecutor(ThreadPoolExecutor):
    """
    Based on concurrent.futures.ThreadPoolExecutor, but additionally ensures dummy omniORB runs for every running thread.
    """

    def _adjust_thread_count(self):
        # if idle threads are available, don't spin new threads
        if self._idle_semaphore.acquire(timeout=0):
            return

        # When the executor gets lost, the weakref callback will wake up
        # the worker threads.
        def weakref_cb(_, q=self._work_queue):
            q.put(None)

        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            thread_name = "%s_%d" % (self._thread_name_prefix or self, num_threads)
            t = threading.Thread(
                name=thread_name,
                target=_thread_pool_executor_worker,
                args=(
                    weakref.ref(self, weakref_cb),
                    self._work_queue,
                    self._initializer,
                    self._initargs,
                ),
            )
            t.start()
            self._threads.add(t)
            _threads_queues[t] = self._work_queue


def _thread_pool_executor_worker(executor_reference, work_queue, initializer, initargs):
    with EnsureOmniThread():
        _worker(executor_reference, work_queue, initializer, initargs)


def _get_command_inout_param(self, cmd_name, cmd_param=None):
    if cmd_param is None:
        return DeviceData()

    if isinstance(cmd_param, DeviceData):
        return cmd_param

    if isinstance(self, DeviceProxy):
        # This is not part of 'Connection' interface, but
        # DeviceProxy only.
        info = self.command_query(cmd_name)
        param = DeviceData()
        try:
            param.insert(info.in_type, cmd_param)
        except TypeError as err:
            raise TypeError(
                f"Invalid input argument for command {cmd_name}: "
                f"{cmd_param!r} cannot be converted to type {info.in_type}"
            ) from err
        return param
    elif isinstance(self, __Group):

        if self.get_size() == 0:
            return DeviceData()

        if isinstance(cmd_param, DeviceDataList):
            return cmd_param

        last_cause = None
        try:
            types = set()
            typ = None
            for idx in range(1, self.get_size() + 1):
                dev = self.get_device(idx)
                try:
                    typ = dev.command_query(cmd_name).in_type
                    types.add(typ)
                except DevFailed as df:
                    last_cause = df
            if not types:
                if last_cause:
                    Except.re_throw_exception(
                        last_cause,
                        "PyAPI_GroupCommandArgInTypeUnknown",
                        "Cannot fetch at least one command type in group.",
                        "Group.command_inout_asynch",
                    )
                else:
                    Except.throw_exception(
                        "PyAPI_GroupCommandArgInTypeUnknown",
                        "Cannot fetch at least one command type in group. Unknown cause.",
                        "Group.command_inout_asynch",
                    )
            elif len(types) > 1:
                raise TypeError(
                    "Cannot execute command with more than one type in group, types are:\n"
                    f"{types}"
                )
        finally:
            del last_cause

        param = DeviceData()
        try:
            param.insert(typ, cmd_param)
        except TypeError as err:
            raise TypeError(
                f"Invalid input argument for command {cmd_name}: "
                f"{cmd_param!r} cannot be converted to type {typ}"
            ) from err
        return param

    elif isinstance(self, Database):
        # I just try to guess types DevString and DevVarStringArray
        # as they are used for Database
        param = DeviceData()
        if isinstance(cmd_param, str):
            param.insert(CmdArgType.DevString, cmd_param)
            return param
        elif isinstance(cmd_param, collections.abc.Sequence) and all(
            [isinstance(x, str) for x in cmd_param]
        ):
            param.insert(CmdArgType.DevVarStringArray, cmd_param)
            return param
        else:
            raise TypeError(
                "command_inout() parameter must be a DeviceData object or a string or a sequence of strings"
            )
    else:
        raise TypeError("command_inout() parameter must be a DeviceData object.")
