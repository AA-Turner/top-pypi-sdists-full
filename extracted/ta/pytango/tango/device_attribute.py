# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.
"""

__all__ = ("device_attribute_init",)

__docformat__ = "restructuredtext"

import copy

from tango import DeviceAttribute, ExtractAs


def __DeviceAttribute__get_data(self):
    return self.get_data_raw().extract()


def __DeviceAttribute__init(self, da=None):
    if da is None:
        DeviceAttribute.__init_orig(self)
    else:
        DeviceAttribute.__init_orig(self, da)
        try:
            self.value = copy.deepcopy(da.value)
        except Exception:
            pass
        try:
            self.w_value = copy.deepcopy(da.w_value)
        except Exception:
            pass
        try:
            self.scalar_w_value = da.scalar_w_value
        except Exception:
            pass
        self.type = da.type
        self.is_empty = da.is_empty
        self.has_failed = da.has_failed


def device_attribute_init():
    DeviceAttribute.__init_orig = DeviceAttribute.__init__
    DeviceAttribute.__init__ = __DeviceAttribute__init
    DeviceAttribute.ExtractAs = ExtractAs
