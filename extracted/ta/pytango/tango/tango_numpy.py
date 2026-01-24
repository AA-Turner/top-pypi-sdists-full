# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.
"""

__all__ = ("NumpyType", "numpy_type", "numpy_spectrum", "numpy_image")

__docformat__ = "restructuredtext"

import collections.abc
import numpy

from tango import Except, Attribute, AttributeInfo
from tango import CmdArgType as ArgType

from tango.attribute_proxy import AttributeProxy


def _numpy_invalid(*args, **kwds):
    Except.throw_exception(
        "PyTango_InvalidConversion",
        "There's no registered conversor to numpy.",
        "NumpyType.tango_to_numpy",
    )


class NumpyType:
    DevShort = numpy.int16
    DevLong = numpy.int32
    DevDouble = numpy.float64
    DevFloat = numpy.float32
    DevBoolean = numpy.bool_
    DevUShort = numpy.uint16
    DevULong = numpy.uint32
    DevUChar = numpy.ubyte
    DevLong64 = numpy.int64
    DevULong64 = numpy.uint64

    mapping = {
        ArgType.DevShort: DevShort,
        ArgType.DevLong: DevLong,
        ArgType.DevDouble: DevDouble,
        ArgType.DevFloat: DevFloat,
        ArgType.DevBoolean: DevBoolean,
        ArgType.DevUShort: DevUShort,
        ArgType.DevULong: DevULong,
        ArgType.DevUChar: DevUChar,
        ArgType.DevLong64: DevLong64,
        ArgType.DevULong: DevULong64,
    }

    @staticmethod
    def tango_to_numpy(param):
        if isinstance(param, ArgType):
            tg_type = param
        if isinstance(param, AttributeInfo):  # or AttributeInfoEx
            tg_type = param.data_type
        elif isinstance(param, Attribute):
            tg_type = param.get_data_type()
        elif isinstance(param, AttributeProxy):
            tg_type = param.get_config().data_type
        else:
            tg_type = param
        try:
            return NumpyType.mapping[tg_type]
        except Exception:
            _numpy_invalid()

    @staticmethod
    def spectrum(tg_type, dim_x):
        """
        numpy_spectrum(self, tg_type, dim_x, dim_y) -> numpy.array
        numpy_spectrum(self, tg_type, sequence) -> numpy.array

                Get a square numpy array to be used with tango.
                One version gets dim_x and creates an object with
                this size. The other version expects any sequence to
                convert.

            Parameters:
                - tg_type : (ArgType): The tango type. For convenience, it
                            can also extract this information from an
                            Attribute, AttributeInfo or AttributeProxy
                            object.
                - dim_x : (int)
                - sequence:
        """
        np_type = NumpyType.tango_to_numpy(tg_type)
        if isinstance(dim_x, collections.abc.Sequence):
            return numpy.array(dim_x, dtype=np_type)
        else:
            return numpy.ndarray(shape=(dim_x,), dtype=np_type)

    @staticmethod
    def image(tg_type, dim_x, dim_y=None):
        """
        numpy_image(self, tg_type, dim_x, dim_y) -> numpy.array
        numpy_image(self, tg_type, sequence) -> numpy.array

                Get a square numpy array to be used with tango.
                One version gets dim_x and dim_y and creates an object with
                this size. The other version expects a square sequence of
                sequences to convert.

            Parameters:
                - tg_type : (ArgType): The tango type. For convenience, it
                            can also extract this information from an
                            Attribute, AttributeInfo or AttributeProxy
                            object.
                - dim_x : (int)
                - dim_y : (int)
                - sequence:
        """
        np_type = NumpyType.tango_to_numpy(tg_type)
        if dim_y is None:
            return numpy.array(dim_x, dtype=np_type)
        else:
            return numpy.ndarray(
                shape=(
                    dim_y,
                    dim_x,
                ),
                dtype=np_type,
            )


numpy_spectrum = NumpyType.spectrum
numpy_image = NumpyType.image
numpy_type = NumpyType.tango_to_numpy
