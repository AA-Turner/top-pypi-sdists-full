# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Deriving a tango type and format from a python value or type hint."""

import enum
import inspect
import typing

import numpy as np

from tango import AttrDataFormat, AttrQuality, CmdArgType, DevState

from ._types import (
    TO_TANGO_TYPE,
    __int_klasses,
    __number_klasses,
    is_devstate,
    is_devstate_seq,
    is_enum,
    is_enum_seq,
    is_non_str_seq,
    is_pure_str,
)

try:
    # numpy >= 2.0 exposes numpy.typing as soon as numpy is imported, but older
    # versions require the submodule to be imported explicitly.
    import numpy.typing

    _np_NDArray = np.typing.NDArray
except (ImportError, AttributeError):
    # numpy < 1.20 has no numpy.typing, numpy 1.20 has no NDArray in it.
    # Use a sentinel that never compares equal to a real typing origin.
    _np_NDArray = object()


def set_complex_value(attr, value):
    if not isinstance(value, tuple):
        attr.set_value(value)
    else:
        n_vals = len(value)
        if (n_vals > 2 and isinstance(value[2], AttrQuality)) or (
            n_vals > 3 and attr.get_data_type() == CmdArgType.DevEncoded and isinstance(value[3], AttrQuality)
        ):
            attr.set_value_date_quality(*value)
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
            raise TypeError(f"cannot translate numpy array with {obj.ndim} dimensions to tango type")
        return TO_TANGO_TYPE[dtype], AttrDataFormat(ndim)
    except AttributeError:
        return __get_tango_type(obj)


def get_attribute_type_format(dtype, dformat, enum_labels):
    if is_devstate(dtype) or is_devstate_seq(dtype):
        _dtype = dtype
        dtype = CmdArgType.DevState

        while is_devstate_seq(_dtype):
            _dtype = _dtype[0]
            dtype = (dtype,)
    elif is_enum(dtype) or is_enum_seq(dtype):
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
                        raise TypeError("Image attribute type must be specified as ((<dtype>,),)")
            elif caller == "attribute":
                raise TypeError("Spectrum attribute type must be specified as (<dtype>,)")

    try:
        tango_type = TO_TANGO_TYPE[dtype]
    except KeyError:
        if isinstance(dtype, str):
            raise RuntimeError(
                f"Cannot translate {dtype!r} to TANGO type. See documentation for the allowed types. "
                'If you are declaring type with type hints and using "from __future__ import annotations", '
                "please read documentation to learn about limitations"
            ) from None
        else:
            raise RuntimeError(
                f"Cannot translate {dtype!r} to TANGO type. See documentation for the allowed types"
            ) from None

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
        if typing.get_origin(sub_type) in [list, tuple] and not __check_types_uniformity(sub_type):
            return False
    return True


def eval_in_fallback_frames(dtype_str, try_depth):
    """
    Tries to eval a string at `try_depth` frames back from the caller.
    """

    def get_frame_at_depth(depth):
        # f_back.f_back reaches the caller of eval_in_fallback_frames; depth
        # further steps reach the frame to evaluate in.
        current_frame = inspect.currentframe().f_back.f_back
        for _ in range(depth):
            if current_frame:
                current_frame = current_frame.f_back
            else:
                # Stack is not deep enough
                return None
        return current_frame

    frame_to_try = None
    try:
        frame_to_try = get_frame_at_depth(try_depth)
        if frame_to_try is None:
            raise IndexError()
        return eval(dtype_str, frame_to_try.f_globals, frame_to_try.f_locals)
    finally:
        # Ensure all created frame references are deleted
        if frame_to_try:
            del frame_to_try


def parse_type_hint(annotation, caller):
    dtype = annotation
    if isinstance(dtype, str):
        depth = 1
        while depth <= 6:  # user code should be before 6th frame
            try:
                dtype = eval_in_fallback_frames(dtype, depth)
                break
            except NameError:
                depth += 1
            except IndexError:
                break

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
        if n_elements == 3 and typing.get_args(dtype)[1] is float and typing.get_args(dtype)[2] == AttrQuality:
            dtype = typing.get_args(dtype)[0]
    origin = typing.get_origin(dtype)
    if origin is np.ndarray or origin is _np_NDArray:
        # numpy < 2.5: ndarray[Any, dtype[T]]; numpy >= 2.5: NDArray is a TypeAliasType; scalar type is the sole arg
        dtype = typing.get_args(typing.get_args(dtype)[1])[0] if origin is np.ndarray else typing.get_args(dtype)[0]
        dformat = None
        if caller in ["property", "command"]:
            dtype = (dtype,)
    if typing.get_origin(dtype) in [list, tuple]:
        if not __has_ellipsis_in_types(dtype):
            max_x = len(typing.get_args(dtype))
        types_are_uniform = __check_types_uniformity(dtype)
        dtype = typing.get_args(dtype)[0]
        dformat = AttrDataFormat.IMAGE if typing.get_origin(dtype) in [list, tuple] else AttrDataFormat.SPECTRUM

        if caller in ["property", "command"] and dformat == AttrDataFormat.IMAGE:
            raise RuntimeError(f"{caller.capitalize()} does not support IMAGE type")

        if not types_are_uniform:
            if caller in ["property", "command"]:
                raise RuntimeError(f"PyTango does not support mixed types in SPECTRUM {caller}")
            else:
                if dformat == AttrDataFormat.IMAGE:
                    raise RuntimeError("PyTango does not support mixed types in IMAGE attributes")
                else:
                    raise RuntimeError("PyTango does not support mixed types in SPECTRUM attributes")

        if caller == "attribute" and dformat == AttrDataFormat.IMAGE:
            max_y = max_x
            max_x = len(typing.get_args(dtype)) if not __has_ellipsis_in_types(dtype) else None
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
        raise EnumTypeError(f"Input class '{enum_cls}' must be unique - {exc}") from None

    # Check the values start at 0, and increment by 1, since that is
    # assumed by tango's DEV_ENUM implementation.
    values = [member.value for member in enum_cls]
    if not values:
        raise EnumTypeError(f"Input class '{enum_cls}' has no members!")
    for expected_value, value in enumerate(values):
        if value != expected_value:
            raise EnumTypeError(f"Enum values for '{enum_cls}' must start at 0 and increment by 1.  Values: {values}")

    return [member.name for member in enum_cls]
