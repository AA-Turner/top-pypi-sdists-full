# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Version, environment and interpreter-level helpers."""

import contextlib
import os
import sys
from argparse import HelpFormatter

from packaging.version import Version

from tango import Database, DevFailed, _tango
from tango.constants import TgLibVers
from tango.release import Release

__device_classes = None


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
            raise Exception(msg) from None
        except Exception:
            msg = f"Error importing package {package_name} required by {software_name}"
            raise Exception(msg) from None

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

    .. versionadded:: 8.1.4
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

    .. versionadded:: 8.1.4
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


def get_home():
    """
    Find user's home directory if possible. Otherwise raise error.

    :return: user's home directory
    :rtype: :py:obj:`str`

    .. versionadded:: 7.1.4
    """
    path = ""
    with contextlib.suppress(Exception):
        path = os.path.expanduser("~")
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


def from_version_str_to_hex_str(version_str):
    v = list(map(int, version_str.split(".")))
    return f"0x{v[0]:02x}{v[1]:02x}{v[2]:02x}00"


def from_version_str_to_int(version_str):
    return int(from_version_str_to_hex_str(version_str), 16)


def info():
    # Compile and Runtime are set by `tango.pytango_init.init`
    from tango.constants import Compile, Runtime

    msg = f"""\
PyTango {Release.version_long} {Release.version_info}
PyTango compiled with:
    Python   : {Compile.PY_VERSION}
    Numpy    : {Compile.NUMPY_VERSION}
    Tango    : {Compile.TANGO_VERSION}
    pybind11 : {Compile.PYBIND11_VERSION}

PyTango runtime is:
    Python   : {Runtime.PY_VERSION}
    Numpy    : {Runtime.NUMPY_VERSION}
    Tango    : {Runtime.TANGO_VERSION}

PyTango running on:
{Runtime.UNAME}
"""
    return msg


class PyTangoHelpFormatter(HelpFormatter):
    def _format_usage(self, usage, actions, groups, prefix):
        usage = super()._format_usage(usage, actions, groups, prefix)
        try:
            db = Database()
            servers_list = db.get_instance_name_list(self._prog)
            if servers_list.size():
                usage += f"Instance names defined in database for server {self._prog}:\n"
                for server in servers_list:
                    usage += "\t" + str(server) + "\n"
            else:
                usage += f"Warning! No defined instance in database for server {self._prog} found!\n"
        except DevFailed:
            pass

        return usage
