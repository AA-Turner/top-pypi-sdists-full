# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.
"""

__all__ = ("init",)

__docformat__ = "restructuredtext"

import numpy

from tango.attribute_proxy import attribute_proxy_init
from tango.base_types import base_types_init
from tango.encoded_attribute import encoded_attribute_init
from tango.connection import connection_init
from tango.db import db_init
from tango.device_attribute import device_attribute_init
from tango.device_class import device_class_init
from tango.device_proxy import device_proxy_init
from tango.device_server import device_server_init
from tango.group import group_init
from tango.group_reply import group_reply_init
from tango.pytango_pprint import pytango_pprint_init
from tango.pyutil import pyutil_init
from tango.time_val import time_val_init
from tango.auto_monitor import auto_monitor_init
from tango._tango import constants
from tango._tango import _get_tango_lib_release

__INITIALIZED = False


def init_constants():
    import sys
    import platform

    tg_ver = tuple(map(int, constants.TgLibVers.split(".")))
    tg_ver_str = "0x%02d%02d%02d00" % (tg_ver[0], tg_ver[1], tg_ver[2])
    constants.TANGO_VERSION_HEX = int(tg_ver_str, 16)

    PYBIND11_VERSION = ".".join(
        map(
            str,
            (
                constants.PYBIND11_VERSION_MAJOR,
                constants.PYBIND11_VERSION_MINOR,
                constants.PYBIND11_VERSION_PATCH,
            ),
        )
    )
    constants.PYBIND11_VERSION = PYBIND11_VERSION

    class Compile:
        PY_VERSION = constants.PY_VERSION
        TANGO_VERSION = constants.TANGO_VERSION
        PYBIND11_VERSION = constants.PYBIND11_VERSION
        NUMPY_VERSION = constants.NUMPY_VERSION
        # UNAME = tuple(map(str, json.loads(constants.UNAME)))

    tg_rt_ver_nb = _get_tango_lib_release()
    tg_rt_major_ver = tg_rt_ver_nb // 100
    tg_rt_minor_ver = tg_rt_ver_nb // 10 % 10
    tg_rt_patch_ver = tg_rt_ver_nb % 10
    tg_rt_ver = ".".join(map(str, (tg_rt_major_ver, tg_rt_minor_ver, tg_rt_patch_ver)))

    class Runtime:
        PY_VERSION = ".".join(map(str, sys.version_info[:3]))
        TANGO_VERSION = tg_rt_ver
        NUMPY_VERSION = numpy.__version__
        UNAME = platform.uname()

    constants.Compile = Compile
    constants.Runtime = Runtime


def init():
    global __INITIALIZED
    if __INITIALIZED:
        return

    init_constants()
    base_types_init()
    encoded_attribute_init()
    connection_init()
    db_init()
    device_attribute_init()
    device_class_init()
    device_proxy_init()
    device_server_init()
    group_init()
    group_reply_init()
    pytango_pprint_init()
    pyutil_init()
    time_val_init()
    auto_monitor_init()

    # must come last: depends on device_proxy.init()
    attribute_proxy_init()

    __INITIALIZED = True
