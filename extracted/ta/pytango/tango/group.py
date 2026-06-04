# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.
"""

__all__ = ("Group", "group_init")

__docformat__ = "restructuredtext"

import collections.abc
from typing import Any, Union

from tango._instrumentation import _trace_client
from tango._tango import (
    DeviceDataList,
    GroupAttrReply,
    GroupCmdReply,
    GroupReply,
)
from tango._tango import (
    __Group as _RealGroup,
)
from tango.device_proxy import (
    DeviceProxy,
)
from tango.device_proxy import (
    __init_device_proxy_internals as init_device_proxy,
)
from tango.utils import (
    _get_command_inout_param,
    _get_device_fqtrl_if_necessary,
    is_non_str_seq,
    is_pure_str,
    seq_2_StdStringVector,
)


def _apply_to(fn, key):
    if isinstance(key, slice):
        if key.step:
            return [fn(x) for x in range(key.start, key.stop, key.step)]
        else:
            return [fn(x) for x in range(key.start, key.stop)]
    else:
        return fn(key)


def _get_one_item(group, key):
    x = group.get_group(key)
    if x is not None:
        return x
    return group.get_device(key)


# I define Group as a proxy to __Group, where group is the actual
# C++ Tango::Group object. Most functions just call the __group object
# and are defined dynamically in __init_proxy_Group, also copying it's
# documentation strings.
# The proxy is useful for add(group). In this case the parameter 'group'
# becomes useless. With the proxy we make that parameter come to live
# again before returning.
# Another function that needs to be adapted to this is get_group because
# we want to return a Group, not a __Group!
# The get_device method also needs to be adapted in order to properly
# initialize the returned proxy with its python attributes.
class Group:
    """A Tango Group represents a hierarchy of tango devices. The hierarchy
    may have more than one level. The main goal is to group devices with
    same attribute(s)/command(s) to be able to do parallel requests."""

    def __init__(self, name):
        if is_pure_str(name):
            name = _RealGroup(name)
        if not isinstance(name, _RealGroup):
            raise TypeError("Constructor expected receives a str")
        self.__group = name

    def add(self, pattern_subgroup: Union[str, list[str], "Group"], timeout_ms: int = -1) -> None:
        """
        add(self, device: str, timeout_ms: int=-1) -> None
        add(self, device_list: list[str], timeout_ms: int=-1) -> None
        add(self, subgroup: Group, timeout_ms: int=-1) -> None

        Attaches any device which name matches one of the specified patterns.

        This method first asks the Tango database the list of device names
        matching one the patterns. Devices are then attached to the group in
        the order in which they are returned by the database.

        Any device already present in the hierarchy (i.e. a device belonging to
        the group or to one of its subgroups), is silently ignored but its
        client side timeout is set to timeout_ms milliseconds if timeout_ms
        is different from -1.

        :param device: a simple device name or a device name pattern (e.g. domain_*/ family/member_*)
        :type device: :py:obj:`str`

        :param device_list: a sequence of these of  a simple device names or
                            a device name patterns (e.g. domain_*/ family/member_*)
        :type device_list: :py:obj:`list`\\[:py:obj:`str`]

        :param subgroup: a Group to be attached as subgroup
        :type subgroup: :py:obj:`~tango.Group`

        :param timeout_ms: If timeout_ms is different from -1, the client
                           side timeouts of all devices matching the
                           specified patterns are set to timeout_ms
                           milliseconds
        :type timeout_ms: :py:obj:`int`

        :throws: :py:obj:`TypeError`, :py:obj:`ArgumentError`
        """
        if isinstance(pattern_subgroup, Group):
            name = pattern_subgroup.__group.get_name()
            self._add(pattern_subgroup.__group, timeout_ms)
            pattern_subgroup.__group = self.get_group(name)
        else:
            self._add(pattern_subgroup, timeout_ms)

    def _add(self, patterns_or_group, timeout_ms=-1):
        if isinstance(patterns_or_group, _RealGroup):
            items = patterns_or_group
        else:
            if is_pure_str(patterns_or_group):
                items = [patterns_or_group]
            elif is_non_str_seq(patterns_or_group):
                items = patterns_or_group
            else:
                raise TypeError("Parameter patterns_or_group: Should be Group, str or a sequence of strings.")

            # If TestContext active, each short TRL is replaced with a fully-qualified
            # TRL, using test server's connection details.  Otherwise, left as-is.
            items = [_get_device_fqtrl_if_necessary(item) for item in items]
            items = seq_2_StdStringVector(items)

        resp = self.__group._add(items, timeout_ms)
        return resp

    def remove(self, patterns: str | list[str], forward: bool = True) -> None:
        """
        Removes any group or device which name matches the specified pattern.

        The pattern parameter can be a group name, a device name or a device
        name pattern (e.g domain_*/family/member_*).

        Since we can have groups with the same name in the hierarchy, a group
        name can be fully qualified to specify which group should be removed.
        Considering the following group:

            ::

                -> gauges
                | -> cell-01
                |     |-> penning
                |     |    |-> ...
                |     |-> pirani
                |          |-> ...
                | -> cell-02
                |     |-> penning
                |     |    |-> ...
                |     |-> pirani
                |          |-> ...
                | -> cell-03
                |     |-> ...
                |
                | -> ...

        A call to gauges->remove("penning") will remove any group named
        "penning" in the hierarchy while gauges->remove("gauges.cell-02.penning")
        will only remove the specified group.

        :param patterns: A string with the pattern or a list of patterns.
        :type patterns: :py:obj:`str` | :py:obj:`list`\\[:py:obj:`str`]

        :param forward: If fwd is set to true (the default), the remove
                        request is also forwarded to subgroups. Otherwise,
                        it is only applied to the local set of elements.
                        For instance, the following code remove any
                        stepper motor in the hierarchy:

                            root_group->remove("*/stepper_motor/*")
        :type forward: :py:obj:`bool`
        """
        if isinstance(patterns, str):
            return self.__group._remove(patterns, forward)
        elif isinstance(patterns, collections.abc.Sequence):
            std_patterns = seq_2_StdStringVector(patterns)
            return self.__group._remove(std_patterns, forward)
        else:
            raise TypeError("Parameter patterns: Should be a str or a sequence of str.")

    def get_device(self, name_or_index: str | int) -> DeviceProxy:
        """
        Returns a reference to the specified device or None if there is no
        device by that name in the group. Or, returns a reference to the
        "idx-th" device in the hierarchy or NULL if the hierarchy contains
        less than "idx" devices.

        The request is systematically forwarded to subgroups (i.e. if no device
        named device_name could be found in the local set of devices, the
        request is forwarded to subgroups).

        This method may throw an exception in case the specified device belongs
        to the group but can't be reached (not registered, down...).

        :param name_or_index: device name of index in group
        :type name_or_index: :py:obj:`str` | :py:obj:`int`

        :rtype: :obj:`~tango.DeviceProxy`

        :throws: :obj:`~tango.DevFailed`
        """
        proxy = self.__group.get_device(name_or_index)
        if proxy is None:
            raise KeyError(f"Group does not have device {name_or_index}")
        init_device_proxy(proxy)
        return proxy

    def get_group(self, group_name: str) -> "Group":
        """
        Returns a reference to the specified group or None if there is no group
        by that name. The group_name can be a fully qualified name.

        Considering the following group:

        ::

            -> gauges
                |-> cell-01
                |    |-> penning
                |    |    |-> ...
                |    |-> pirani
                |    |-> ...
                |-> cell-02
                |    |-> penning
                |    |    |-> ...
                |    |-> pirani
                |    |-> ...
                | -> cell-03
                |    |-> ...
                |
                | -> ...

        A call to gauges.get_group("penning") returns the first group named
        "penning" in the hierarchy (i.e. gauges.cell-01.penning) while
        gauges.get_group("gauges.cell-02.penning'') returns the specified group.

        The request is systematically forwarded to subgroups (i.e. if no group
        named group_name could be found in the local set of elements, the request
        is forwarded to subgroups).

        :param group_name:
        :type group_name: :py:obj:`str`

        :rtype: :obj:`~tango.Group`

        .. versionadded:: 7.0.0
        """
        internal = self.__group.get_group(group_name)
        if internal is None:
            return None
        return Group(internal)

    def __contains__(self, pattern):
        return self.contains(pattern)

    def __getitem__(self, key):
        fn = lambda x: _get_one_item(self, x)
        return _apply_to(fn, key)

    def __delitem__(self, key):
        fn = lambda x: self.remove(x)
        return _apply_to(fn, key)

    def __len__(self):
        return self.get_size()

    def __repr__(self):
        return f"Group({self.get_name()})"

    @_trace_client
    def command_inout(
        self, cmd_name: str, param: Any | DeviceDataList = None, forward: bool = True
    ) -> list[GroupCmdReply]:
        """
        command_inout(self, cmd_name: str, forward: bool=True) -> list[GroupCmdReply]
        command_inout(self, cmd_name: str, param: typing.Any, forward: bool=True) -> list[GroupCmdReply]
        command_inout(self, cmd_name: str, param_list: DeviceDataList, forward: bool=True) -> list[GroupCmdReply]

        Just a shortcut to do:
            self.command_inout_reply(self.command_inout_asynch(...))

        :param cmd_name: Command name
        :type cmd_name: :py:obj:`str`

        :param param: Command parameter
        :type param: :py:obj:`typing.Any`

        :param param_list: Sequence of command parameters
        :type  param_list: :py:obj:`~tango.DeviceDataList`

        :param forward: If it is set to true (the default) request is
                        forwarded to subgroups. Otherwise, it is only applied
                        to the local set of devices
        :type forward: :py:obj:`bool`
        """
        idx = self.command_inout_asynch(cmd_name, param, forward)
        return self.command_inout_reply(idx)

    @_trace_client
    def command_inout_asynch(self, cmd_name: str, param: Any = None, forward: bool = True) -> int:
        """
        Executes a Tango command on each device in the group asynchronously.
        The method sends the request to all devices and returns immediately.
        Pass the returned request id to Group.command_inout_reply() to obtain
        the results.

        :param cmd_name: command name
        :type cmd_name: :py:obj:`str`

        :param param: parameter value
        :type param: :py:obj:`typig.Any`

        :param forward: If it is set to true (the default), the request is forwarded to sub-groups.
                        Otherwise, it is only applied to the local set of devices.
        :type forward: :py:obj:`bool`

        :return: request id. Pass the returned request id to
                 Group.command_inout_reply() to obtain the results.
        :rtype: int
        """
        if param is None:
            idx = self.__group.command_inout_asynch(cmd_name, forget=False, forward=forward)
        else:
            arg_in = _get_command_inout_param(self.__group, cmd_name, param)
            idx = self.__group.command_inout_asynch(cmd_name, arg_in, forget=False, forward=forward)

        return idx

    @_trace_client
    def read_attribute(self, attr_name: str, forward: bool = True) -> list[GroupAttrReply]:
        """
        Just a shortcut to do:
            self.read_attribute_reply(self.read_attribute_asynch(...))

        """
        idx = self.__group.read_attribute_asynch(attr_name, forward)
        return self.__group.read_attribute_reply(idx)

    @_trace_client
    def read_attributes(self, attr_names: list[str], forward: bool = True) -> list[GroupAttrReply]:
        """
        Just a shortcut to do:
            self.read_attributes_reply(self.read_attributes_asynch(...))
        """
        idx = self.__group.read_attributes_asynch(attr_names, forward)
        return self.__group.read_attributes_reply(idx)

    @_trace_client
    def write_attribute(
        self, attr_name: str, value: Any, forward: bool = True, multi: bool = False
    ) -> list[GroupReply]:
        """
        Just a shortcut to do:
            self.write_attribute_reply(self.write_attribute_asynch(...))
        """
        idx = self.__group.write_attribute_asynch(attr_name, value, forward=forward, multi=multi)
        return self.__group.write_attribute_reply(idx)


def group_init():
    proxy_methods = [
        # 'add',  # Needs to be adapted
        # "command_inout_asynch",  # Needs to be adapted
        "command_inout_reply",
        "contains",
        "disable",
        "enable",
        # 'get_device',  # Needs to be adapted
        "get_device_list",
        "get_fully_qualified_name",
        # 'get_group',   # Needs to be adapted
        "get_name",
        "get_size",
        "is_enabled",
        "name_equals",
        "name_matches",
        "ping",
        "read_attribute_asynch",
        "read_attribute_reply",
        "read_attributes_asynch",
        "read_attributes_reply",
        "remove_all",
        "set_timeout_millis",
        "write_attribute_asynch",
        "write_attribute_reply",
    ]

    def proxy_call_define(fname):
        def fn(self, *args, **kwds):
            return getattr(self._Group__group, fname)(*args, **kwds)

        fn.__doc__ = getattr(_RealGroup, fname).__doc__
        fn.__qualname__ = f"Group.{fname}"
        setattr(Group, fname, _trace_client(fn))

    for fname in proxy_methods:
        proxy_call_define(fname)

        # Group.add.__func__.__doc__ = _RealGroup.add.__doc__
        # Group.get_group.__func__.__doc__ = _RealGroup.get_group.__doc__
        # Group.__doc__ = _RealGroup.__doc__
