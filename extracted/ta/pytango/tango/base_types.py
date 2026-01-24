# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.
"""

__all__ = ("base_types_init",)

__docformat__ = "restructuredtext"

from tango import (
    StdStringVector,
    StdLongVector,
    StdDoubleVector,
    CommandInfoList,
    AttributeInfoList,
    AttributeInfoListEx,
    DbData,
    DbDevInfos,
    DbDevExportInfos,
    DbDevImportInfos,
    DbHistoryList,
    DeviceDataHistoryList,
)


def __StdVector__add(self, seq):
    ret = seq.__class__(self)
    ret.extend(seq)
    return ret


def __StdVector__mul(self, n):
    ret = self.__class__()
    for _ in range(n):
        ret.extend(self)
    return ret


def __StdVector__imul(self, n):
    ret = self.__class__()
    for _ in range(n):
        ret.extend(self)
    return ret


def __fillVectorClass(klass):
    klass.__add__ = __StdVector__add
    klass.__mul__ = __StdVector__mul
    klass.__imul__ = __StdVector__imul


def base_types_init():
    v_klasses = (
        StdStringVector,
        StdLongVector,
        StdDoubleVector,
        CommandInfoList,
        AttributeInfoList,
        AttributeInfoListEx,
        DbData,
        DbDevInfos,
        DbDevExportInfos,
        DbDevImportInfos,
        DbHistoryList,
        DeviceDataHistoryList,
    )

    for v_klass in v_klasses:
        __fillVectorClass(v_klass)

    # Doc string for vectors is easier to add already in Python

    AttributeInfoList.__doc__ = """
    List of AttributeInfo objects, containing available information for the attributes"""

    AttributeInfoListEx.__doc__ = """
    List of AttributeInfoEx objects, containing available information for the attributes"""
