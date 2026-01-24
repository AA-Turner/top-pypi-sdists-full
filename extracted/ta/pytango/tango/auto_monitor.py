# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.
"""

__all__ = ("auto_monitor_init",)

__docformat__ = "restructuredtext"

from tango import AutoTangoMonitor, AutoTangoAllowThreads


def __AutoTangoMonitor__enter__(self):
    self._acquire()
    return self


def __AutoTangoMonitor__exit__(self, *args, **kwargs):
    self._release()


def __init_AutoTangoMonitor():
    AutoTangoMonitor.__enter__ = __AutoTangoMonitor__enter__
    AutoTangoMonitor.__exit__ = __AutoTangoMonitor__exit__


def __AutoTangoAllowThreads__enter__(self):
    return self


def __AutoTangoAllowThreads__exit__(self, *args, **kwargs):
    self._acquire()


def __init_AutoTangoAllowThreads():
    AutoTangoAllowThreads.__enter__ = __AutoTangoAllowThreads__enter__
    AutoTangoAllowThreads.__exit__ = __AutoTangoAllowThreads__exit__


def auto_monitor_init(doc=True):
    __init_AutoTangoMonitor()
    __init_AutoTangoAllowThreads()
