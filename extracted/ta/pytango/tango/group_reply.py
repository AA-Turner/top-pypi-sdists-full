# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
"""
This is an internal PyTango module.
"""

__all__ = ("group_reply_init",)

__docformat__ = "restructuredtext"

from tango.pytango_pprint import __indented, __str_error_stack_helper
from tango import GroupReply, GroupCmdReply, GroupAttrReply


def __GroupCmdReply__get_data(self):
    """
    get_data(self) -> any

        Get the actual value stored in the GroupCmdRply, the command
        output value.
        It's the same as self.get_data_raw().extract()

    Parameters : None
    Return     : (any) Whatever is stored there, or None.
    """
    return self.get_data_raw().extract()


def __str_group_reply_helper(self):
    dev_name = self.dev_name()
    obj_name = self.obj_name()
    enabled = self.group_element_enabled()
    has_failed = self.has_failed()
    if not enabled:
        extra_line = ""
    elif has_failed:
        err_str = __str_error_stack_helper(self.get_err_stack())
        err_str = f"[\n{err_str}\n]"
        extra_line = f"err_stack = {err_str}\n"
    elif hasattr(self, "get_data"):
        value = self.get_data()
        if isinstance(value, str):
            value = f'"{value}"'
        else:
            value = str(value)
        extra_line = f"data = {value}\n"
    else:
        extra_line = ""
    details = (
        f'dev_name = "{dev_name}"\n'
        f'obj_name = "{obj_name}"\n'
        f"enabled = {enabled}\n"
        f"has_failed = {has_failed}\n"
        f"{extra_line}"
    )
    return (
        f"{self.__class__.__name__}[\n"
        f"{__indented(details, strip_outer=False)}\n"
        f"]"
    )


def group_reply_init():
    GroupCmdReply.get_data = __GroupCmdReply__get_data
    GroupCmdReply.__str__ = __str_group_reply_helper
    GroupAttrReply.__str__ = __str_group_reply_helper
    GroupReply.__str__ = __str_group_reply_helper
