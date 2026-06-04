# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
High Level API for writting Tango clients

This is an experimental module. Not part of the official API.
"""

import functools
import weakref
from typing import ClassVar

try:
    from warnings import deprecated
except ImportError:
    from typing_extensions import deprecated

import tango
from tango import CmdArgType
from tango import DeviceProxy as _DeviceProxy
from tango.codec import dumps as _dumps
from tango.codec import loads

_FMT = "pickle"

dumps = functools.partial(_dumps, _FMT)


@deprecated(
    "Device alias was an experimental API - scheduled for removal in PyTango 11.0.0. Use tango.DeviceProxy instead."
)
class Device(_DeviceProxy):
    pass


def _command(device, cmd_info, *args, **kwargs):
    name = cmd_info.cmd_name
    if cmd_info.in_type == CmdArgType.DevEncoded:
        result = device.command_inout(name, dumps((args, kwargs)))
    else:
        result = device.command_inout(name, *args, **kwargs)
    if cmd_info.out_type == CmdArgType.DevEncoded:
        result = loads(*result)
    return result


class _DeviceHelper:
    __CMD_FILTER: ClassVar[set[str]] = {"init", "state", "status"}
    __ATTR_FILTER: ClassVar[set[str]] = {"state", "status"}

    __attr_cache = None
    __cmd_cache = None

    def __init__(self, dev_name, *args, **kwargs):
        self.dev_name = dev_name
        self.device = Device(dev_name, *args, **kwargs)
        self.slots = weakref.WeakKeyDictionary()

    def connect(self, signal, slot, event_type=tango.EventType.CHANGE_EVENT):
        i = self.device.subscribe_event(signal, event_type, slot)
        self.slots[slot] = i
        return i

    def disconnect(self, signal, slot):
        i = self.slots.pop(slot)
        self.device.unsubscribe_event(i)

    def get_attr_cache(self, refresh=False):
        cache = self.__attr_cache
        if not cache:
            refresh = True
        if refresh:
            cache = {}
            dev = self.device
            try:
                for attr_info in dev.attribute_list_query_ex():
                    attr_name = attr_info.name
                    if attr_name.lower() in self.__ATTR_FILTER:
                        continue
                    cache[attr_name] = attr_info
            except tango.DevFailed:
                pass
            self.__attr_cache = cache
        return cache

    def get_attr_info(self, name):
        cache = self.get_attr_cache()
        result = cache.get(name)
        if result:
            return result
        else:
            cache = self.get_attr_cache(refresh=True)
            return cache.get(name)

    def get_cmd_cache(self, refresh=False):
        cache = self.__cmd_cache
        if not cache:
            refresh = True
        if refresh:
            cache = {}
            dev = self.device
            try:
                for cmd_info in dev.command_list_query():
                    cmd_name = cmd_info.cmd_name
                    if cmd_name.lower() in self.__CMD_FILTER:
                        continue
                    cmd_func = functools.partial(_command, dev, cmd_info)
                    cmd_func.__name__ = cmd_name
                    cmd_func.__doc__ = cmd_info.in_type_desc
                    cmd_info.func = cmd_func
                    cache[cmd_name] = cmd_info
            except tango.DevFailed:
                pass
            self.__cmd_cache = cache
        return cache

    def get_cmd_info(self, name):
        cache = self.get_cmd_cache()
        result = cache.get(name)
        if result:
            return result
        else:
            cache = self.get_cmd_cache(refresh=True)
            return cache.get(name)

    def is_cmd(self, name):
        return name.lower() in self.get_cmd_cache()

    def members(self):
        result = self.get_attr_cache().keys()
        result.extend(self.get_cmd_cache().keys())
        return result

    def get(self, name):
        dev = self.device
        result = self.get_attr_info(name)
        if result:
            result = dev.read_attribute(name)
            value = result.value
            return loads(*value) if result.type == tango.DevEncoded else value
        result = self.get_cmd_info(name)
        if result is None:
            raise KeyError(f"Unknown {name}")
        return result

    def set(self, name, value):
        result = self.get_attr_info(name)
        if result is None:
            raise KeyError(f"Unknown attribute {name}")
        if result.data_type == tango.DevEncoded:
            self.device.write_attribute(name, dumps(value))
        else:
            self.device.write_attribute(name, value)

    def get_info(self):
        try:
            return self.__info
        except AttributeError:
            pass
        try:
            info = self.device.info()
            self.__dict__["__info"] = info
            return info
        except tango.DevFailed:
            return None

    def __getitem__(self, name):
        if self.get_attr_info(name) is None:
            raise KeyError(f"Unknown attribute {name}")
        return self.device[name]

    def __setitem__(self, name, value):
        if self.get_attr_info(name) is None:
            raise KeyError(f"Unknown attribute {name}")
        self.device[name] = value

    def __str__(self):
        return self.dstr()

    def __repr__(self):
        return str(self)

    def dstr(self):
        info = self.get_info()
        klass = "Device"
        if info:
            klass = info.dev_class
        return f"{klass}({self.dev_name})"


@deprecated("Object class was an experimental API - scheduled for removal in PyTango 11.0.0")
class Object:
    """Tango object"""

    def __init__(self, dev_name, *args, **kwargs):
        helper = _DeviceHelper(dev_name, *args, **kwargs)
        self.__dict__["_helper"] = helper

    def __getattr__(self, name):
        try:
            r = self._helper.get(name)
        except KeyError as ke:
            raise AttributeError(f"Unknown {name}") from ke
        if isinstance(r, tango.CommandInfo):
            self.__dict__[name] = r.func
            return r.func
        return r

    def __setattr__(self, name, value):
        try:
            return self._helper.set(name, value)
        except KeyError as ke:
            raise AttributeError(f"Unknown {name}") from ke

    def __getitem__(self, name):
        return self._helper[name]

    def __setitem__(self, name, value):
        self._helper[name] = value

    def __str__(self):
        return str(self._helper)

    def __repr__(self):
        return repr(self._helper)

    def __dir__(self):
        return self._helper.members()


@deprecated("get_object_proxy function was an experimental API - scheduled for removal in PyTango 11.0.0")
def get_object_proxy(obj):
    """Experimental function. Not part of the official API"""
    return obj._helper.device


@deprecated("get_object_db function was an experimental API - scheduled for removal in PyTango 11.0.0")
def get_object_db(obj):
    """Experimental function. Not part of the official API"""
    return get_object_proxy(obj).get_device_db()


@deprecated("get_object_name function was an experimental API - scheduled for removal in PyTango 11.0.0")
def get_object_name(obj):
    """Experimental function. Not part of the official API"""
    return get_object_proxy(obj).get_name()


@deprecated("get_object_info function was an experimental API - scheduled for removal in PyTango 11.0.0")
def get_object_info(obj):
    """Experimental function. Not part of the official API"""
    return get_object_proxy(obj).info()


@deprecated("get_attributes_config function was an experimental API - scheduled for removal in PyTango 11.0.0")
def get_attributes_config(obj, refresh=False):
    """Experimental function. Not part of the official API"""
    return obj._helper.get_attr_cache(refresh=refresh)


@deprecated("get_commands_config function was an experimental API - scheduled for removal in PyTango 11.0.0")
def get_commands_config(obj, refresh=False):
    """Experimental function. Not part of the official API"""
    return obj._helper.get_cmd_cache(refresh=refresh)


@deprecated("connect function was an experimental API - scheduled for removal in PyTango 11.0.0")
def connect(obj, signal, slot, event_type=tango.EventType.CHANGE_EVENT):
    """Experimental function. Not part of the official API"""
    return obj._helper.connect(signal, slot, event_type=event_type)


@deprecated("disconnect function was an experimental API - scheduled for removal in PyTango 11.0.0")
def disconnect(obj, signal, slot):
    """Experimental function. Not part of the official API"""
    return obj._helper.disconnect(signal, slot)
