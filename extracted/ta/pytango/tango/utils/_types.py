# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Tango data-type tables and the predicates that query them."""

import collections.abc
import enum
import inspect
import numbers

import numpy as np

from tango import CmdArgType, DevState, StdStringVector

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

_scalar_binary_types = (CmdArgType.DevEncoded,)

_array_binary_types = (CmdArgType.DevVarCharArray,)


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
    }

    for key in dir(CmdArgType):
        if key.startswith("Dev"):
            value = getattr(CmdArgType, key)
            ret[key] = ret[value] = value

    for tango_type, numpy_type in FROM_TANGO_TO_NUMPY_TYPE.items():
        ret[numpy_type] = tango_type

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


def __add_derived_scalar_types(scalar_to_array_map):
    """Let every spelling accepted by TO_TANGO_TYPE index the array map too."""
    for alias, tango_type in TO_TANGO_TYPE.items():
        if tango_type in scalar_to_array_map:
            scalar_to_array_map[alias] = scalar_to_array_map[tango_type]


__add_derived_scalar_types(_scalar_to_array_type)


def is_pure_str(obj):
    """
    Tells if the given object is a python string.

    This means any subclass of str.

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
        while is_non_str_seq(obj) and len(obj):
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
    return isinstance(obj, __int_klasses) and not isinstance(obj, bool)


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

    return tg_type in _scalar_types


is_scalar_type = is_scalar


def is_array(tg_type):
    """Tells if the given tango type is an array type

    :param tg_type: tango type
    :type tg_type: :class:`tango.CmdArgType`

    :return: True if the given tango type is an array type or False otherwise
    :rtype: :py:obj:`bool`
    """
    return tg_type in _array_types


is_array_type = is_array


def __is_type(tg_type, inc_array, scalar_types, array_types):
    """Shared body of the type predicates: array types count only on request."""
    if tg_type in scalar_types:
        return True
    if not inc_array:
        return False
    return tg_type in array_types


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
    return __is_type(tg_type, inc_array, _scalar_numerical_types, _array_numerical_types)


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
    return __is_type(tg_type, inc_array, _scalar_int_types, _array_int_types)


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
    return __is_type(tg_type, inc_array, _scalar_float_types, _array_float_types)


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
    return __is_type(tg_type, inc_array, _scalar_bool_types, _array_bool_types)


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
    return __is_type(tg_type, inc_array, _scalar_str_types, _array_str_types)


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
    return __is_type(tg_type, inc_array, _scalar_binary_types, _array_binary_types)


is_binary_type = is_binary


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
        raise ValueError(f"Invalid tango scalar type: {tg_type}") from None
