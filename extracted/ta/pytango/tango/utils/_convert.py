# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Conversion between python values, tango vectors and their string forms."""

from tango import AttrDataFormat, CmdArgType, StdDoubleVector, StdStringVector
from tango.constants import AlrmValueNotSpec, StatusNotSet

from ._types import (
    _array_float_types,
    _array_int_types,
    _scalar_float_types,
    _scalar_int_types,
    _scalar_str_types,
    _scalar_types,
    is_bool_type,
    is_float_type,
    is_int_type,
    is_non_str_seq,
    is_numerical_type,
    is_pure_str,
    is_scalar_type,
    scalar_to_array_type,
)

__NO_STR_VALUE = AlrmValueNotSpec, StatusNotSet


def strtobool(val):
    """Convert a string representation of truth to True or False.
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError(f"invalid truth value {val}")


def __seq_2_vector(seq, vec, vector_type, coerce):
    """Fill a tango vector from a python sequence, coercing each element."""
    if vec is None:
        if isinstance(seq, vector_type):
            return seq
        vec = vector_type()
    if not isinstance(vec, vector_type):
        raise TypeError(f"vec must be a tango.{vector_type.__name__}")
    for e in seq:
        vec.append(coerce(e))
    return vec


def __vector_2_seq(vec, seq, vector_type, coerce):
    """Fill a python sequence from a tango vector, coercing each element."""
    if seq is None:
        seq = []
    if not isinstance(vec, vector_type):
        raise TypeError(f"vec must be a tango.{vector_type.__name__}")
    for e in vec:
        seq.append(coerce(e))
    return seq


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
    return __seq_2_vector(seq, vec, StdStringVector, str)


def StdStringVector_2_seq(vec, seq=None):
    """Converts a :class:`tango.StdStringVector` to a python sequence<str>

    :param seq: the :class:`tango.StdStringVector`
    :type seq: :class:`tango.StdStringVector`
    :param vec: (optional, default is None) a python sequence to be filled.
                 If None is given, a new list is created
    :return: a python sequence filled with the same contents as seq
    :rtype: sequence<str>
    """
    return __vector_2_seq(vec, seq, StdStringVector, str)


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
    return __seq_2_vector(seq, vec, StdDoubleVector, float)


def StdDoubleVector_2_seq(vec, seq=None):
    """Converts a :class:`tango.StdDoubleVector` to a python sequence<float>

    :param seq: the :class:`tango.StdDoubleVector`
    :type seq: :class:`tango.StdDoubleVector`
    :param vec: (optional, default is None) a python sequence to be filled.
                 If None is given, a new list is created
    :return: a python sequence filled with the same contents as seq
    :rtype: sequence<float>
    """
    return __vector_2_seq(vec, seq, StdDoubleVector, float)


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
    # AttrDataFormat.SCALAR is 0, so None is the only "not given" value.
    if tg_format is not None:
        return _seqStr_2_obj_from_type_format(seq, tg_type, tg_format)
    return _seqStr_2_obj_from_type(seq, tg_type)


def _seqStr_2_obj_from_type(seq, tg_type):
    if is_pure_str(seq):
        seq = (seq,)

    # Scalar cases
    if tg_type in _scalar_int_types:
        return int(seq[0])

    if tg_type in _scalar_float_types:
        return float(seq[0])

    if tg_type in _scalar_str_types:
        return seq[0]

    if tg_type == CmdArgType.DevBoolean:
        return strtobool(seq[0])

    # sequence cases
    if tg_type in (CmdArgType.DevVarCharArray, CmdArgType.DevVarStringArray):
        return seq

    if tg_type in _array_int_types:
        return [int(x) for x in seq]

    if tg_type in _array_float_types:
        return [float(x) for x in seq]

    if tg_type == CmdArgType.DevVarBooleanArray:
        return [strtobool(x) for x in seq]

    return []


def _seqStr_2_obj_from_type_format(seq, tg_type, tg_format):
    if tg_format == AttrDataFormat.SCALAR:
        return _seqStr_2_obj_from_type(seq, tg_type)
    elif tg_format == AttrDataFormat.SPECTRUM:
        return _seqStr_2_obj_from_type(seq, scalar_to_array_type(tg_type))
    elif tg_format == AttrDataFormat.IMAGE:
        array_type = scalar_to_array_type(tg_type)
        return [_seqStr_2_obj_from_type(row, array_type) for row in seq]

    # UNKNOWN_FORMAT
    return _seqStr_2_obj_from_type(seq, tg_type)


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
        if is_numerical_type(tg_type) and obj_str in __NO_STR_VALUE:
            return None
        if is_int_type(tg_type):
            f = int
        elif is_float_type(tg_type):
            f = float
        elif is_bool_type(tg_type):
            f = strtobool
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
