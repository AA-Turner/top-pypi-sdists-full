# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Define python methods for DeviceProxy object."""

from __future__ import annotations

import collections
import collections.abc
import contextlib
import enum
import functools
import textwrap
import threading
import time
import warnings
from collections.abc import Callable, Sequence
from typing import Any

from tango._instrumentation import _forcefully_traced_method, _trace_client
from tango._tango import (
    AttributeInfo,
    AttributeInfoEx,
    AttributeInfoList,
    AttributeInfoListEx,
    CmdArgType,
    CommandInfo,
    CommandInfoList,
    DbData,
    DbDatum,
    DevFailed,
    DeviceAttribute,
    DeviceProxy,
    DevState,
    EventSubMode,
    EventType,
    Except,
    ExtractAs,
    GreenMode,
    StdStringVector,
    __EventCallBack,
    constants,
)
from tango._telemetry import (
    _telemetry_endpoint_to_wire,
    _telemetry_endpoints_from_wire,
    _telemetry_endpoints_to_wire,
)
from tango._warnings import PyTangoUserWarning, warn_once
from tango.green import get_green_mode, green, green_callback
from tango.telemetry import TelemetryEndpoint
from tango.utils import (
    StdStringVector_2_seq,
    _check_only_allowed_kwargs,
    _get_device_fqtrl_if_necessary,
    _get_new_CallbackAutoDie,
    dir2,
    get_property_from_db,
    is_integer,
    is_non_str_seq,
    is_pure_str,
    parameter_2_dbdata,
    seq_2_StdStringVector,
)

__all__ = ("device_proxy_init", "get_device_proxy")

__docformat__ = "restructuredtext"

_UNSUBSCRIBE_LIFETIME = 60


@green(consume_green_mode=False)
@_trace_client
def get_device_proxy(*args, green_mode=None, executor=None, threadpool=None, asyncio_executor=None):
    """
    get_device_proxy(self, dev_name: str, green_mode: GreenMode=None, wait: bool=True, timeout: float=True) -> DeviceProxy
    get_device_proxy(self, dev_name: str, need_check_acc: bool, green_mode: GreenMode=None, wait: bool=True, timeout: float=None) -> DeviceProxy

    Returns a new :class:`~tango.DeviceProxy`.
    There is no difference between using this function and the direct
    :class:`~tango.DeviceProxy` constructor if you use the default kwargs.

    The added value of this function becomes evident when you choose a green_mode
    to be *Futures* or *Gevent* or *Asyncio*. The DeviceProxy constructor internally
    makes some network calls which makes it *slow*. By using one of the *green modes* as
    green_mode you are allowing other python code to be executed in a cooperative way.

    .. note::
        The timeout parameter has no relation with the tango device client side
        timeout (gettable by :meth:`~tango.DeviceProxy.get_timeout_millis` and
        settable through :meth:`~tango.DeviceProxy.set_timeout_millis`)

    :param dev_name: the device name or alias
    :type dev_name: :py:obj:`str`
    :param need_check_acc: (optional, default is True)
                           Determines if at creation time of DeviceProxy it should check
                           for channel access (rarely used)
    :type need_check_acc: :py:obj:`bool`
    :param green_mode: determines the mode of execution of the device (including
                      the way it is created). Defaults to the current global
                      green_mode (check :func:`~tango.get_green_mode` and
                      :func:`~tango.set_green_mode`)
    :type green_mode: :py:obj:`~tango.GreenMode`
    :param wait: whether or not to wait for result. If green_mode
                 Ignored when green_mode is Synchronous (always waits).
    :type wait: :py:obj:`bool`
    :param timeout: The number of seconds to wait for the result.
                    If None, then there is no limit on the wait time.
                    Ignored when green_mode is Synchronous or wait is False.
    :type timeout: :py:obj:`float`

    :returns:
        if green_mode is Synchronous or wait is True:
            :class:`~tango.DeviceProxy`
        elif green_mode is Futures:
            :class:`concurrent.futures.Future`
        elif green_mode is Gevent:
            :class:`gevent.event.AsynchResult`
        elif green_mode is Asyncio:
            :class:`asyncio.Future`
    :throws: :obj:`~tango.DevFailed` if green_mode is Synchronous or wait is True
                and there is an error creating the device.
             :obj:`concurrent.futures.TimeoutError` if green_mode is Futures,
                wait is False, timeout is not None and the time to create the device
                has expired.
             :obj:`gevent.timeout.Timeout` if green_mode is Gevent, wait is False,
                timeout is not None and the time to create the device has expired.
             :obj:`asyncio.TimeoutError` if green_mode is Asyncio,
                wait is False, timeout is not None and the time to create the device
                has expired.

    .. versionadded:: 8.1.0
    """
    return DeviceProxy(
        *args,
        green_mode=green_mode,
        executor=executor,
        threadpool=threadpool,
        asyncio_executor=asyncio_executor,
    )


class __TangoInfo:
    """Helper class for copying DeviceInfo, or when DeviceProxy.info() fails."""

    def __init__(
        self,
        dev_class,
        dev_type,
        doc_url,
        server_host,
        server_id,
        server_version,
    ):
        self.dev_class = str(dev_class)
        self.dev_type = str(dev_type)
        self.doc_url = str(doc_url)
        self.server_host = str(server_host)
        self.server_id = str(server_id)
        self.server_version = int(server_version)

    @classmethod
    def from_defaults(cls):
        return cls(
            dev_class="Device",
            dev_type="Device",
            doc_url="Doc URL = https://www.tango-controls.org/developers/dsc",
            server_host="Unknown",
            server_id="Unknown",
            server_version=1,
        )

    @classmethod
    def from_copy(cls, info):
        return cls(
            dev_class=info.dev_class,
            dev_type=info.dev_type,
            doc_url=info.doc_url,
            server_host=info.server_host,
            server_id=info.server_id,
            server_version=info.server_version,
        )


# -------------------------------------------------------------------------------
# Pythonic API: transform tango commands into methods and tango attributes into
# class members
# -------------------------------------------------------------------------------


def __check_read_attribute(dev_attr):
    if dev_attr.has_failed:
        raise DevFailed(*dev_attr.get_err_stack())
    return dev_attr


def __init_device_proxy_internals(proxy):
    if proxy.__dict__.get("_initialized", False):
        return
    executors = dict.fromkeys(GreenMode.values.values())
    proxy.__dict__["_green_mode"] = None
    proxy.__dict__["_cache_attr_info"] = True
    proxy.__dict__["_dynamic_interface_frozen"] = True
    proxy.__dict__["_initialized"] = True
    proxy.__dict__["_executors"] = executors
    proxy.__dict__["_pending_unsubscribe"] = {}


def __DeviceProxy__get_cmd_cache(self):
    try:
        ret = self.__dict__["__cmd_cache"]
    except KeyError:
        self.__dict__["__cmd_cache"] = ret = {}
    return ret


def __DeviceProxy__get_attr_cache(self):
    try:
        ret = self.__dict__["__attr_cache"]
    except KeyError:
        self.__dict__["__attr_cache"] = ret = {}
    return ret


def __DeviceProxy____init__(self, *args, green_mode=None, executor=None, threadpool=None, asyncio_executor=None):
    __init_device_proxy_internals(self)
    self.__dict__["_initialized"] = False
    self.__dict__["_cache_attr_info"] = True
    self.__dict__["_green_mode"] = green_mode
    self.__dict__["_executors"][GreenMode.Futures] = executor
    self.__dict__["_executors"][GreenMode.Gevent] = threadpool
    self.__dict__["_executors"][GreenMode.Asyncio] = asyncio_executor

    # If TestContext active, short TRL is replaced with fully-qualified
    # TRL, using test server's connection details.  Otherwise, left as-is.
    device_name = args[0]
    new_device_name = _get_device_fqtrl_if_necessary(device_name)
    new_args = [new_device_name, *args[1:]]
    try:
        DeviceProxy.__init_orig__(self, *new_args)
    except DevFailed as orig_err:
        if new_device_name != device_name:
            # If device was not found, it could be an attempt to access a real device
            # with short name while running TestContext.  I.e., we need to use the
            # short name so that the real TANGO_HOST will be tried.
            try:
                DeviceProxy.__init_orig__(self, *args)
            except DevFailed as retry_exc:
                Except.re_throw_exception(
                    retry_exc,
                    "PyAPI_DeviceProxyInitFailed",
                    f"Failed to create DeviceProxy "
                    f"(tried {new_device_name!r} => {orig_err.args[0].reason}, and "
                    f"{device_name!r} => {retry_exc.args[0].reason})",
                    "__DeviceProxy__init__",
                )
        else:
            raise

    self.__dict__["_initialized"] = True


def __DeviceProxy__get_green_mode(self):
    """Returns the green mode in use by this DeviceProxy.

    :returns: the green mode in use by this DeviceProxy.
    :rtype: GreenMode

    .. seealso::
        :func:`tango.get_green_mode`
        :func:`tango.set_green_mode`

    .. versionadded:: 8.1.0
    """
    gm = self._green_mode
    if gm is None:
        gm = get_green_mode()
    return gm


def __DeviceProxy__set_green_mode(self, green_mode=None):
    """Sets the green mode to be used by this DeviceProxy
    Setting it to None means use the global PyTango green mode
    (see :func:`tango.get_green_mode`).

    :param green_mode: the new green mode
    :type green_mode: GreenMode

    .. versionadded:: 8.1.0
    """
    self._green_mode = green_mode


def __DeviceProxy__refresh_cmd_cache(self):
    cmd_list = self.command_list_query()
    cmd_cache = {}
    for cmd in cmd_list:
        n = cmd.cmd_name.lower()
        doc = f"{cmd.cmd_name}({cmd.in_type}) -> {cmd.out_type}\n\n"
        doc += f" -  in ({cmd.in_type}): {cmd.in_type_desc}\n"
        doc += f" - out ({cmd.out_type}): {cmd.out_type_desc}\n"
        cmd_cache[n] = cmd, doc
    self.__dict__["__cmd_cache"] = cmd_cache


def __DeviceProxy__refresh_attr_cache(self):
    attr_infos = self.attribute_list_query_ex()
    attr_cache = {}
    for attr_info in attr_infos:
        name = attr_info.name.lower()
        enum_class = __make_enum_class(attr_info)
        attr_cache[name] = attr_info, enum_class
    self.__dict__["__attr_cache"] = attr_cache


def __DeviceProxy__freeze_dynamic_interface(self):
    """Prevent unknown attributes to be set on this DeviceProxy instance.

    An exception will be raised if the Python attribute set on this DeviceProxy
    instance does not already exist.  This prevents accidentally writing to
    a non-existent Tango attribute when using the high-level API.

    This is the default behaviour since PyTango 9.3.4.

    See also :meth:`tango.DeviceProxy.unfreeze_dynamic_interface`.

    .. versionadded:: 9.4.0
    """
    self._dynamic_interface_frozen = True


def __DeviceProxy__unfreeze_dynamic_interface(self):
    """Allow new attributes to be set on this DeviceProxy instance.

    An exception will not be raised if the Python attribute set on this DeviceProxy
    instance does not exist.  Instead, the new Python attribute will be added to
    the DeviceProxy instance's dictionary of attributes.  This may be useful, but
    a user will not get an error if they accidentally write to a non-existent Tango
    attribute when using the high-level API.

    See also :meth:`tango.DeviceProxy.freeze_dynamic_interface`.

    .. versionadded:: 9.4.0
    """
    warnings.warn(
        f"Dynamic interface unfrozen on DeviceProxy instance {self} id=0x{id(self):x} - "
        f"arbitrary Python attributes can be set without raising an exception.",
        category=PyTangoUserWarning,
        stacklevel=1,
    )
    self._dynamic_interface_frozen = False


def __DeviceProxy__is_dynamic_interface_frozen(self):
    """Indicates if the dynamic interface for this DeviceProxy instance is frozen.

    See also :meth:`tango.DeviceProxy.freeze_dynamic_interface` and
    :meth:`tango.DeviceProxy.unfreeze_dynamic_interface`.

    :returns: True if the dynamic interface this DeviceProxy is frozen.
    :rtype: bool

    .. versionadded:: 9.4.0
    """
    return self._dynamic_interface_frozen


def __DeviceProxy__set_attribute_config_cache(self, enabled: bool) -> None:
    """Enable or disable the attribute configuration caching.

    For more details, see :ref:`attribute-configuration-caching`.

    See also :meth:`tango.DeviceProxy.is_attribute_config_cache_enabled`
    and :meth:`tango.DeviceProxy.invalidate_attribute_config_cache`.

    .. versionadded:: 10.3.0
    """
    self._cache_attr_info = enabled


def __DeviceProxy__is_attribute_config_cache_enabled(self) -> bool:
    """Returns whether the attribute configuration is cached or not.

    For more details, see :ref:`attribute-configuration-caching`.

    See also :meth:`tango.DeviceProxy.enable_attribute_config_cache`
    and :meth:`tango.DeviceProxy.invalidate_attribute_config_cache`.

    .. versionadded:: 10.3.0
    """

    return self._cache_attr_info


def __DeviceProxy__invalidate_attribute_config_cache(self) -> None:
    """Invalidates attribute configuration cache

    For more details, see :ref:`attribute-configuration-caching`.

    See also :meth:`tango.DeviceProxy.enable_attribute_config_cache`
    and :meth:`tango.DeviceProxy.is_attribute_config_cache_enabled`.

    .. versionadded:: 10.3.0
    """
    self.__dict__["__attr_cache"] = {}


def __get_command_func(dp, cmd_info, name):
    _, doc = cmd_info

    def f(*args, **kwds):
        return dp.command_inout(name, *args, **kwds)

    f.__doc__ = doc
    return f


def __make_enum_class(attr_info):
    enum_class = None
    if attr_info.data_type == CmdArgType.DevEnum:
        if attr_info.enum_labels:
            enum_class = enum.IntEnum(attr_info.name, " ".join(attr_info.enum_labels), start=0)
    elif attr_info.data_type == CmdArgType.DevState:
        enum_class = DevState
    return enum_class


def __get_enum_value(attr_value, enum_class):

    if is_non_str_seq(attr_value):
        ret = []
        for value in attr_value:
            if is_non_str_seq(value):
                ret.append(tuple([enum_class(v) for v in value]))
            else:
                ret.append(enum_class(value))
        return tuple(ret)

    return enum_class(attr_value)


async def __async_get_attribute_value(self, name, enum_class):
    reading = await self.read_attribute(name)
    if reading.value is not None and reading.type in [
        CmdArgType.DevState,
        CmdArgType.DevEnum,
    ]:
        if not self._cache_attr_info:
            if reading.type == CmdArgType.DevEnum:
                config = await self.get_attribute_config(name)
                enum_class = __make_enum_class(config)
            elif reading.type == CmdArgType.DevState:
                enum_class = DevState
        return __get_enum_value(reading.value, enum_class)
    else:
        return reading.value


def __sync_get_attribute_value(self, name, enum_class):
    reading = self.read_attribute(name)
    if reading.value is not None and reading.type in [
        CmdArgType.DevState,
        CmdArgType.DevEnum,
    ]:
        if not self._cache_attr_info:
            if reading.type == CmdArgType.DevEnum:
                enum_class = __make_enum_class(self.get_attribute_config(name))
            elif reading.type == CmdArgType.DevState:
                enum_class = DevState
        return __get_enum_value(reading.value, enum_class)
    else:
        return reading.value


def __get_attribute_value(self, name, enum_class):
    if self.get_green_mode() == GreenMode.Asyncio:
        return __async_get_attribute_value(self, name, enum_class)
    else:
        return __sync_get_attribute_value(self, name, enum_class)


def __convert_str_to_enum(value, enum_class, attr_name):
    try:
        return enum_class[value]
    except KeyError:
        raise AttributeError(
            f"Invalid enum value {value} for attribute {attr_name}. Valid values: {list(enum_class.__members__)}"
        ) from None


def __get_value_to_write(value, enum_class, attr_name):
    if enum_class is not None:
        if is_non_str_seq(value):
            org_value = value
            value = []
            for val in org_value:
                if is_non_str_seq(val):
                    value.append(
                        [(__convert_str_to_enum(v, enum_class, attr_name) if is_pure_str(v) else v) for v in val]
                    )
                else:
                    value.append(__convert_str_to_enum(val, enum_class, attr_name) if is_pure_str(val) else val)
        elif is_pure_str(value):
            value = __convert_str_to_enum(value, enum_class, attr_name)

    return value


def __get_attr_info_and_enum(self, attr_name):
    attr_info, enum_class = None, None

    if self._cache_attr_info:
        cached_info = self.__get_attr_cache().get(attr_name.lower())
        if cached_info is not None:
            attr_info, enum_class = cached_info

    if attr_info is None:
        attr_info = self.get_attribute_config(attr_name)
        enum_class = __make_enum_class(attr_info)
    return attr_info, enum_class


def __set_attribute_value(self, attr_name, value):
    attr_info, enum_class = __get_attr_info_and_enum(self, attr_name)
    try:
        value_to_write = __get_value_to_write(value, enum_class, attr_name)
        return self.write_attribute(attr_info, value_to_write)
    except (AttributeError, TypeError):
        new_attr_info = None
        new_enum_class = None
        if self._cache_attr_info:
            # attribute config may have changed on the server, so try updating the cache
            self.__refresh_attr_cache()
            cached_info = self.__get_attr_cache().get(attr_name.lower())
            if cached_info is not None:
                new_attr_info, new_enum_class = cached_info
        nothing_new = new_attr_info is None or new_attr_info == attr_info
        if nothing_new:
            raise
    # try once more with the new config
    value_to_write = __get_value_to_write(value, new_enum_class, attr_name)
    return self.write_attribute(new_attr_info, value_to_write)


def __DeviceProxy__getattr(self, name):
    cause = None
    try:
        # trait_names is a feature of IPython. Hopefully they will solve
        # ticket http://ipython.scipy.org/ipython/ipython/ticket/229 someday
        # and the ugly trait_names could be removed.
        if name.startswith("_") or name == "trait_names":
            raise AttributeError(name) from cause

        name_l = name.lower()

        cmd_info = self.__get_cmd_cache().get(name_l)
        if cmd_info:
            return __get_command_func(self, cmd_info, name)

        cached_info = self.__get_attr_cache().get(name_l)
        if cached_info is not None:
            _, enum_class = cached_info
            try:
                return __get_attribute_value(self, name, enum_class)
            except DevFailed as err:
                # it could be, that attribute was deleted and we have to re-create attribute cache
                if err.args[0].reason != "API_AttrNotFound":
                    raise

        try:
            self.__refresh_cmd_cache()
        except Exception as e:
            if cause is None:
                cause = e

        cmd_info = self.__get_cmd_cache().get(name_l)
        if cmd_info:
            return __get_command_func(self, cmd_info, name)

        try:
            self.__refresh_attr_cache()
        except Exception as e:
            if cause is None:
                cause = e

        cached_info = self.__get_attr_cache().get(name_l)
        if cached_info is not None:
            _, enum_class = cached_info
            return __get_attribute_value(self, name, enum_class)

        raise AttributeError(name) from cause
    finally:
        del cause


def __DeviceProxy__setattr(self, name, value):
    cause = None
    try:
        name_l = name.lower()

        if name_l in self.__get_cmd_cache():
            raise TypeError("Cannot set the value of a command") from cause

        if name_l in self.__get_attr_cache():
            return __set_attribute_value(self, name, value)

        try:
            self.__refresh_cmd_cache()
        except Exception as e:
            if cause is None:
                cause = e

        if name_l in self.__get_cmd_cache():
            raise TypeError("Cannot set the value of a command") from cause

        try:
            self.__refresh_attr_cache()
        except Exception as e:
            if cause is None:
                cause = e

        if name_l in self.__get_attr_cache():
            return __set_attribute_value(self, name, value)

        try:
            if name in self.__dict__ or not self.is_dynamic_interface_frozen():
                return super(DeviceProxy, self).__setattr__(name, value)
            else:
                raise AttributeError(
                    f"Tried to set non-existent attr {name!r} to {value!r}.\n"
                    f"The DeviceProxy object interface is frozen and cannot be modified - "
                    f"see tango.DeviceProxy.freeze_dynamic_interface for details."
                )
        except Exception as e:
            raise e from cause
    finally:
        del cause


def __DeviceProxy__dir(self):
    """Return the attribute list including tango objects."""
    extra_entries = set()
    # Add commands
    with contextlib.suppress(Exception):
        extra_entries.update(self.get_command_list())
    # Add attributes
    with contextlib.suppress(Exception):
        extra_entries.update(self.get_attribute_list())
    # Merge with default dir implementation
    extra_entries.update([x.lower() for x in extra_entries])
    entries = extra_entries.union(dir2(self))
    return sorted(entries)


def __DeviceProxy__getitem(self, key):
    return self.read_attribute(key)


def __DeviceProxy__setitem(self, key, value):
    return self.write_attribute(key, value)


def __DeviceProxy__contains(self, key):
    return key.lower() in map(str.lower, self.get_attribute_list())


def __DeviceProxy__read_attribute(self, attr_name: str, extract_as: ExtractAs = ExtractAs.Numpy) -> DeviceAttribute:
    """
    Read a single attribute.

    :param attr_name: The name of the attribute to read.
    :type attr_name: :py:obj:`str`

    :param extract_as: Defaults to numpy.
    :type extract_as: :obj:`~tango.ExtractAs`

    __GREEN_KWARGS_DESCRIPTION__

    :return: DeviceAttribute object with read attribute value.
    :rtype: :obj:`~tango.DeviceAttribute`

    :throws: :py:obj:`~tango.ConnectionFailed`: Raised in case of a connection failure \n
             :py:obj:`~tango.CommunicationFailed`: Raised in case of a communication failure. \n
             :py:obj:`~tango.DevFailed`: Raised in case of a device failure

    __GREEN_RAISES__

    .. versionchanged:: 7.1.4
        For DevEncoded attributes, before it was returning a DeviceAttribute.value
        as a tuple **(format<str>, data<str>)** no matter what was the *extract_as*
        value was. Since 7.1.4, it returns a **(format<str>, data<buffer>)**
        unless *extract_as* is String, in which case it returns
        **(format<str>, data<str>)**.

    .. versionchanged:: 8.0.0
        For DevEncoded attributes, now returns a DeviceAttribute.value
        as a tuple **(format<str>, data<bytes>)** unless *extract_as* is String,
        in which case it returns **(format<str>, data<str>)**. Careful, if
        using python >= 3 data<str> is decoded using default python
        *utf-8* encoding. This means that PyTango assumes tango DS was written
        encapsulating string into *utf-8* which is the default python encoding.

    .. versionadded:: 8.1.0
        *green_mode* parameter.
        *wait* parameter.
        *timeout* parameter.

    .. versionchanged:: 9.4.0
        For spectrum and image attributes with an empty sequence, no longer
        returns DeviceAttribute.value and DeviceAttribute.w_value as
        :obj:`None`.  Instead, DevString and DevEnum types get an empty :obj:`tuple`,
        while other types get an empty :obj:`numpy.ndarray`.  Using *extract_as* can
        change the sequence type, but it still won't be :obj:`None`.
    """
    return __check_read_attribute(self._read_attribute(attr_name, extract_as))


def __read_attributes_asynch__(self, attr_names, cb, extract_as):
    if cb is None:
        return self.__read_attributes_asynch(attr_names)

    cb2 = _get_new_CallbackAutoDie()
    if isinstance(cb, collections.abc.Callable):
        cb2.attr_read = _forcefully_traced_method(cb)
    else:
        cb2.attr_read = _forcefully_traced_method(cb.attr_read)
    return self.__read_attributes_asynch(attr_names, cb2, extract_as)


def __DeviceProxy__read_attributes_asynch(
    self,
    attr_names: Sequence[str],
    cb: Callable | None = None,
    extract_as: ExtractAs = ExtractAs.Numpy,
) -> int | None:
    """
    read_attributes_asynch(self, attr_names: Sequence[str], __GREEN_KWARGS__) -> int
    read_attributes_asynch(self, attr_names: Sequence[str], cb: typing.Callable, extract_as: ExtractAs=Numpy, __GREEN_KWARGS__) -> None

    Read asynchronously an attribute list.

    .. important::
        by default, TANGO is initialized with the **polling** model. If you want
        to use the **push** model (the one with the callback parameter), you
        need to change the global TANGO model to PUSH_CALLBACK.
        You can do this with the :meth:`tango.ApiUtil.set_asynch_cb_sub_model`

    :param attr_names: A list of attributes to read. See read_attributes.
    :type attr_names: :py:obj:`typing.Sequence`\\[:py:obj:`str`]

    :param cb: push model: as soon as attributes read, core calls cb with read results.
        This callback object should be an instance of a user class with an attr_read() method.
        It can also be any callable object.
    :type cb: :py:obj:`typing.Optional`\\[:py:obj:`typing.Callable`]

    :param extract_as: Defaults to numpy.
    :type extract_as: :obj:`~tango.ExtractAs`

    __GREEN_KWARGS_DESCRIPTION__

    :returns: an asynchronous call identifier which is needed to get attributes value if poll model, None if push model
    :rtype: :py:obj:`int` | :py:obj:`None`

    :throws: :py:obj:`~tango.ConnectionFailed`
    __GREEN_RAISES__

    .. important::
        Multiple asynchronous calls are not guaranteed to be executed by the device
        server in the same order they are invoked by the client.  E.g., a call
        to ``write_attributes_asynch([("a", 1)])`` followed immediately with a call to
        ``read_attributes_asynch(["a"])`` could result in the device reading the
        attribute ``a`` before writing to it.

    .. versionadded:: 7.0.0
    """

    return __read_attributes_asynch__(self, attr_names, cb, extract_as)


def __DeviceProxy__read_attribute_asynch(
    self, attr_name: str, cb: Callable | None = None, extract_as: ExtractAs = ExtractAs.Numpy
) -> int | None:
    """
    read_attribute_asynch(self, attr_name: str, __GREEN_KWARGS__) -> int
    read_attribute_asynch(self, attr_name: str, cb: typing.Callable, extract_as: ExtractAs=Numpy, __GREEN_KWARGS__) -> None

    Read asynchronously the specified attributes.

    .. important::
        by default, TANGO is initialized with the **polling** model. If you want
        to use the **push** model (the one with the callback parameter), you
        need to change the global TANGO model to PUSH_CALLBACK.
        You can do this with the :meth:`tango.ApiUtil.set_asynch_cb_sub_model`

    :param attr_name: an attribute to read
    :type attr_name: :py:obj:`str`

    :param cb: push model: as soon as attributes read, core calls cb with read results.
        This callback object should be an instance of a user class with an attr_read() method.
        It can also be any callable object.
    :type cb: :py:obj:`typing.Optional`\\[:py:obj:`typing.Callable`]

    :param extract_as: Defaults to ExtractAs.Numpy
    :type extract_as: ExtractAs

    __GREEN_KWARGS_DESCRIPTION__

    :returns: an asynchronous call identifier which is needed to get attribute value if poll model, None if push model
    :rtype: :py:obj:`int` | :py:obj:`None`

    :throws: :py:obj:`~tango.ConnectionFailed`

    __GREEN_RAISES__

    .. important::
        Multiple asynchronous calls are not guaranteed to be executed by the device
        server in the same order they are invoked by the client.  E.g., a call
        to the method ``write_attribute_asynch("a", 1)`` followed immediately with
        a call to ``read_attribute_asynch("a")`` could result in the device reading the
        attribute ``a`` before writing to it.

    .. versionadded:: 7.0.0
    """
    return __read_attributes_asynch__(self, [attr_name], cb, extract_as)


def __read_attributes_reply__(self, *args, **kwargs):
    if "poll_timeout" in kwargs:
        kwargs["timeout"] = kwargs.pop("poll_timeout")

    return self.__read_attributes_reply(*args, **kwargs)


def __DeviceProxy__read_attributes_reply(self, *args, **kwargs) -> list[DeviceAttribute]:
    """
    read_attributes_reply(self, id: int, extract_as: ExtractAs=ExtractAs.Numpy, __GREEN_KWARGS__) -> list[DeviceAttribute]
    read_attributes_reply(self, id: int, poll_timeout: int, extract_as: ExtractAs=ExtractAs.Numpy, __GREEN_KWARGS__) -> list[DeviceAttribute]

    Get the answer of an asynchronous read_attributes call, if it has arrived (polling model).

    If the reply is ready, but an attribute raised an exception while reading, it will
    still be included in the returned list.  However, the has_error field for that item
    will be set to True.

    .. versionchanged:: 10.0.0 To eliminate confusion between different timeout parameters,
        the core (cppTango) timeout (previously the optional second positional argument) has
        been renamed to "poll_timeout". Conversely, the pyTango executor timeout remains as the
        keyword argument "timeout". These parameters have distinct meanings and units:

        - The cppTango "poll_timeout" is measured in milliseconds and blocks the call until
          a reply is received. If the reply is not received within the specified poll_timeout
          duration, an exception is thrown. Setting poll_timeout to 0 causes the call to
          wait indefinitely until a reply is received.
        - The pyTango "timeout" is measured in seconds and is applicable only in asynchronous
          GreenModes (Asyncio, Futures, Gevent), and only when "wait" is set to True. The specific
          behavior when a reply is not received within the specified timeout period varies
          depending on the GreenMode.

    :param id: the asynchronous call identifier
    :type id: :py:obj:`int`

    :param poll_timeout: cppTango core timeout in ms: \n
                         - If the reply has not yet arrived, the call will wait for the time specified (in ms). \n
                         - If after timeout, the reply is still not there, an exception is thrown. \n
                         - If timeout set to 0, the call waits until the reply arrives. \n
                         - If the argument is not provided, then there is no timeout check, and an
                           exception is raised immediately if the reply is not ready.
    :type poll_timeout: :py:obj:`int`, optional

    :param extract_as: Defaults to numpy.
    :type extract_as: ExtractAs

    __GREEN_KWARGS_DESCRIPTION__

    :returns: Could be: \n
                  - If the reply is arrived and if it is a valid reply,
                    it is returned to the caller in a list of DeviceAttribute. \n
                  - If the reply is an exception, it is re-thrown by this call. \n
                  - If the reply is not yet arrived, the call will wait (blocking the process)
                    for the time specified in timeout. If after timeout milliseconds, the reply is still not there, an
                    exception is thrown. If timeout is set to 0, the call waits
                    until the reply arrived.
    :rtype: :py:obj:`list`\\[:py:obj:`~tango.DeviceAttribute`]

    :throws: :py:obj:`~tango.AsynCall`, :py:obj:`~tango.AsynReplyNotArrived`,
             :py:obj:`~tango.ConnectionFailed`, :py:obj:`~tango.CommunicationFailed`,
             :py:obj:`~tango.DevFailed`
    __GREEN_RAISES__

    .. versionadded:: 7.0.0

    """
    _check_only_allowed_kwargs(kwargs, {"id", "poll_timeout", "extract_as"})

    return __read_attributes_reply__(self, *args, **kwargs)


def __DeviceProxy__read_attribute_reply(self, *args, **kwargs) -> DeviceAttribute:
    """
    read_attribute_reply(self, id: int, extract_as: ExtractAs=ExtractAs.Numpy, __GREEN_KWARGS__) -> DeviceAttribute
    read_attribute_reply(self, id: int, poll_timeout: int, extract_as: ExtractAs=ExtractAs.Numpy, __GREEN_KWARGS__) -> DeviceAttribute

    Get the answer of an asynchronous read_attribute call, if it has arrived (polling model).

    If the reply is ready, but the attribute raised an exception while reading, an
    exception will be raised by this function (DevFailed, with reason API_AttrValueNotSet).

    .. versionchanged:: 10.0.0 To eliminate confusion between different timeout parameters,
        the core (cppTango) timeout (previously the optional second positional argument) has
        been renamed to "poll_timeout". Conversely, the pyTango executor timeout remains as the
        keyword argument "timeout". These parameters have distinct meanings and units:

        - The cppTango "poll_timeout" is measured in milliseconds and blocks the call until
          a reply is received. If the reply is not received within the specified poll_timeout
          duration, an exception is thrown. Setting poll_timeout to 0 causes the call to
          wait indefinitely until a reply is received.
        - The pyTango "timeout" is measured in seconds and is applicable only in asynchronous
          GreenModes (Asyncio, Futures, Gevent), and only when "wait" is set to True. The specific
          behavior when a reply is not received within the specified timeout period varies
          depending on the GreenMode.

    :param id: the asynchronous call identifier
    :type id: :py:obj:`int`

    :param poll_timeout: cppTango core timeout in ms: \n
                         - If the reply has not yet arrived, the call will wait for the time specified (in ms). \n
                         - If after timeout, the reply is still not there, an exception is thrown. \n
                         - If timeout set to 0, the call waits until the reply arrives. \n
                         - If the argument is not provided, then there is no timeout check, and an
                           exception is raised immediately if the reply is not ready.
    :type poll_timeout: :py:obj:`int`, optional

    :param extract_as: Defaults to numpy.
    :type extract_as: ExtractAs

    __GREEN_KWARGS_DESCRIPTION__

    :returns: Could be: \n
                  - If the reply is arrived and if it is a valid reply,
                    it is returned to the caller in a DeviceAttribute. \n
                  - If the reply is an exception, it is re-thrown by this call. \n
                  - If the reply is not yet arrived, the call will wait (blocking the process)
                    for the time specified in timeout. If after timeout milliseconds, the reply is still not there, an
                    exception is thrown. If timeout is set to 0, the call waits
                    until the reply arrived.

    :rtype: :obj:`tango.DeviceAttribute`

    :throws: :py:obj:`tango.AsynCall`, :py:obj:`tango.AsynReplyNotArrived`,
             :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`

    .. versionadded:: 7.0.0
    """
    _check_only_allowed_kwargs(kwargs, {"id", "poll_timeout", "extract_as"})

    attr = __read_attributes_reply__(self, *args, **kwargs)[0]
    return __check_read_attribute(attr)


def __DeviceProxy__write_attributes_asynch(
    self,
    attr_values: Sequence[tuple[str | AttributeInfoEx, Any]],
    cb: Callable | None = None,
) -> int | None:
    """
    Write asynchronously the specified attributes.

    .. important::
        by default, TANGO is initialized with the **polling** model. If you want
        to use the **push** model (the one with the callback parameter), you
        need to change the global TANGO model to PUSH_CALLBACK.
        You can do this with the :meth:`tango.ApiUtil.set_asynch_cb_sub_model`

    :param values: pairs of (attr_name, value) to write (see Note below)
    :type values: :py:obj:`typing.Sequence`\\[:py:obj:`tuple`\\[:py:obj:`str`
                  | :py:obj:`~tango.AttributeInfoEx`, :py:obj:`typing.Any`]]

    :param cb: push model: as soon as attributes written, core calls cb with write results.
        This callback object should be an instance of a user class with an attr_written() method.
        It can also be any callable object.
    :type cb: :py:obj:`typing.Optional`[:py:obj:`typing.Callable`]

    __GREEN_KWARGS_DESCRIPTION__

    :returns: an asynchronous call identifier which is needed to get the server reply if poll model, None if push model
    :rtype: :py:obj:`int` | :py:obj:`None`

    :throws: :py:obj:`~tango.ConnectionFailed`

    __GREEN_RAISES__

    .. important::
        Multiple asynchronous calls are not guaranteed to be executed by the device
        server in the same order they are invoked by the client.  E.g., a call
        to ``write_attributes_asynch([("a", 1)])`` followed immediately with a call to
        ``read_attributes_asynch(["a"])`` could result in the device reading the
        attribute ``a`` before writing to it.

    .. note::
        For each pair of values there are two possibilities for the
        attr parameter: if you give attribute name, then PyTango must
        fetch attribute info for this attribute from server by additional synchronous(!)
        IO, since we must know to which c++ data type cast each python value.
        If you would like to avoid this IO you must give AttributeInfoEx instead of
        attribute name for each(!) pair of values.

    .. versionchanged:: 10.1.0 Added support for AttributeInfoEx for attr_values parameter.

    """

    if cb is None:
        return self.__write_attributes_asynch(attr_values)

    cb2 = _get_new_CallbackAutoDie()
    if isinstance(cb, collections.abc.Callable):
        cb2.attr_written = _forcefully_traced_method(cb)
    else:
        cb2.attr_written = _forcefully_traced_method(cb.attr_written)
    return self.__write_attributes_asynch(attr_values, cb2)


def __DeviceProxy__write_attribute_asynch(
    self, attr: str | AttributeInfoEx, value: Any, cb: Callable | None = None
) -> int | None:
    """
    Write asynchronously the specified attribute.

    .. important::
        by default, TANGO is initialized with the **polling** model. If you want
        to use the **push** model (the one with the callback parameter), you
        need to change the global TANGO model to PUSH_CALLBACK.
        You can do this with the :meth:`tango.ApiUtil.set_asynch_cb_sub_model`

    :param attr: an attribute name to write or AttributeInfoEx object (see Note below)
    :type attr: :py:obj:`str` | :obj:`~tango.AttributeInfoEx`

    :param value: value to write
    :type value: :py:obj:`typing.Any`

    :param cb: push model: as soon as attribute written, core calls cb with write results.
                           This callback object should be an instance of a user class with an attr_written() method.
                           It can also be any callable object.
    :type cb: :py:obj:`typing.Optional`\\[:py:obj:`typing.Callable`]

    __GREEN_KWARGS_DESCRIPTION__

    :returns: an asynchronous call identifier which is needed to get the server reply if poll model, None if push model
    :rtype: :py:obj:`int` | :py:obj:`None`

    :throws: :py:obj:`tango.ConnectionFailed`

    __GREEN_RAISES__

    .. important::
        Multiple asynchronous calls are not guaranteed to be executed by the device
        server in the same order they are invoked by the client.  E.g., a call
        to the method ``write_attribute_asynch("a", 1)`` followed immediately with
        a call to ``read_attribute_asynch("a")`` could result in the device reading the
        attribute ``a`` before writing to it.

    .. note::
        There are two possibilities for the attr parameter: if you give attribute name,
        then PyTango will do additional synchronous(!) IO to fetch AttributeInfoEx object from device server,
        since we must know to which c++ data type cast python value. If you would like to avoid this IO you
        can give AttributeInfoEx instead of attribute name.

    .. versionchanged:: 10.1.0

        - attr_name parameter was renamed to attr
        - added support for AttributeInfoEx for attr parameter

    """
    if cb is None:
        return self.__write_attribute_asynch(attr, value)

    cb2 = _get_new_CallbackAutoDie()
    if isinstance(cb, collections.abc.Callable):
        cb2.attr_written = _forcefully_traced_method(cb)
    else:
        cb2.attr_written = _forcefully_traced_method(cb.attr_written)
    return self.__write_attribute_asynch(attr, value, cb2)


def __write_attributes_reply__(self, *args, **kwargs):
    if "poll_timeout" in kwargs:
        kwargs["timeout"] = kwargs.pop("poll_timeout")

    return self.__write_attributes_reply(*args, **kwargs)


def __DeviceProxy__write_attributes_reply(self, *args, **kwargs) -> None:
    """

    write_attributes_reply(self, id: int, __GREEN_KWARGS__) -> None
    write_attributes_reply(self, id: int, poll_timeout: int, __GREEN_KWARGS__) -> None

    Check if the answer of an asynchronous write_attributes is arrived
    (polling model). If the reply is arrived and if it is a valid reply,
    the call returned. If the reply is an exception, it is re-thrown by
    this call. An exception is also thrown in case of the reply is not
    yet arrived.

    .. versionchanged:: 10.0.0 To eliminate confusion between different timeout parameters,
                        the core (cppTango) timeout (previously the optional second positional argument) has
                        been renamed to "poll_timeout". Conversely, the pyTango executor timeout remains as
                        the keyword argument "timeout". These parameters have distinct meanings and units:

                        - The cppTango "poll_timeout" is measured in milliseconds and blocks the call
                          until a reply is received. If the reply is not received within the
                          specified poll_timeout duration, an exception is thrown. Setting poll_timeout
                          to 0 causes the call to wait indefinitely until a reply is received.
                        - The pyTango "timeout" is measured in seconds and is applicable only in
                          asynchronous GreenModes (Asyncio, Futures, Gevent), and only when "wait"
                          is set to True. The specific behavior when a reply is not received within
                          the specified timeout period varies depending on the GreenMode.

    :param id: the asynchronous call identifier
    :type id: :py:obj:`int`

    :param poll_timeout: cppTango core timeout in ms: \n
                         - If the reply has not yet arrived, the call will wait for the time specified (in ms). \n
                         - If after timeout, the reply is still not there, an exception is thrown. \n
                         - If timeout set to 0, the call waits until the reply arrives. \n
                         - If the argument is not provided, then there is no timeout check, and an
                           exception is raised immediately if the reply is not ready.
    :type poll_timeout: :py:obj:`int`, optional

    :param extract_as: Defaults to numpy.
    :type extract_as: ExtractAs

    __GREEN_KWARGS_DESCRIPTION__

    :throws: :py:obj:`tango.AsynCall`, :py:obj:`tango.AsynReplyNotArrived`,
             :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`
    __GREEN_RAISES__

    .. versionadded:: 7.0.0

    """
    _check_only_allowed_kwargs(kwargs, {"id", "poll_timeout"})

    return __write_attributes_reply__(self, *args, **kwargs)


def __DeviceProxy__write_attribute_reply(self, *args, **kwargs) -> None:
    """
    write_attribute_reply(self, id: int, __GREEN_KWARGS__) -> None
    write_attribute_reply(self, id: int, poll_timeout: int, __GREEN_KWARGS__) -> None

    Check if the answer of an asynchronous write_attributes is arrived
    (polling model). If the reply is arrived and if it is a valid reply,
    the call returned. If the reply is an exception, it is re-thrown by
    this call. An exception is also thrown in case of the reply is not
    yet arrived.

    .. versionchanged:: 10.0.0 To eliminate confusion between different timeout parameters,
                        the core (cppTango) timeout (previously the optional second positional argument) has
                        been renamed to "poll_timeout". Conversely, the pyTango executor timeout remains as the
                        keyword argument "timeout". These parameters have distinct meanings and units:

                        - The cppTango "poll_timeout" is measured in milliseconds and blocks the call until a
                          reply is received. If the reply is not received within the specified poll_timeout duration,
                          an exception is thrown. Setting poll_timeout to 0 causes the call to wait
                          indefinitely until a reply is received.
                        - The pyTango "timeout" is measured in seconds and is applicable only in asynchronous
                          GreenModes (Asyncio, Futures, Gevent), and only when "wait" is set to True.
                          The specific behavior when a reply is not received within the specified
                          timeout period varies depending on the GreenMode.

    :param id: the asynchronous call identifier
    :type id: :py:obj:`int`

    :param poll_timeout: cppTango core timeout in ms: \n
                         - If the reply has not yet arrived, the call will wait for the time specified (in ms). \n
                         - If after timeout, the reply is still not there, an exception is thrown. \n
                         - If timeout set to 0, the call waits until the reply arrives. \n
                         - If the argument is not provided, then there is no timeout check, and an
                           exception is raised immediately if the reply is not ready.
    :type poll_timeout: :py:obj:`int`, optional

    :param extract_as: Defaults to numpy.
    :type extract_as: ExtractAs

    __GREEN_KWARGS_DESCRIPTION__

    :returns: None
    :rtype: :py:obj:`None`

    :throws: :py:obj:`tango.AsynCall`, :py:obj:`tango.AsynReplyNotArrived`,
             :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`

     .. versionadded:: 7.0.0
    """
    _check_only_allowed_kwargs(kwargs, {"id", "poll_timeout"})

    return __write_attributes_reply__(self, *args, **kwargs)


def __DeviceProxy__write_read_attribute(
    self,
    attr: str | AttributeInfoEx,
    value: Any,
    extract_as: ExtractAs = ExtractAs.Numpy,
) -> DeviceAttribute:
    """

    Write then read a single attribute in a single network call.
    By default (serialisation by device), the execution of this call in
    the server can't be interrupted by other clients.

    :param attr: The name or AttributeInfoEx structure of the attribute to write.
    :type attr: :py:obj:`str` | :obj:`~tango.AttributeInfoEx`

    :param value: The value to write to the attribute.
    :type value: :py:obj:`typing.Any`

    __GREEN_KWARGS_DESCRIPTION__

    :returns: A DeviceAttribute object with readout value.
    :rtype: :obj:`tango.DeviceAttribute`

    :throws:
        :py:obj:`tango.ConnectionFailed`: Raised in case of a connection failure. \n
        :py:obj:`tango.CommunicationFailed`: Raised in case of a communication failure. \n
        :py:obj:`tango.DeviceUnlocked`: Raised in case of an unlocked device. \n
        :py:obj:`tango.WrongData`: Raised in case of a wrong data format. \n
        :py:obj:`tango.DevFailed`: Raised in case of a device failure. \n
        :py:obj:`TypeError`: Raised in case of an incorrect type of input arguments.

    __GREEN_RAISES__

    .. note::
        There are two possibilities for the attr parameter: if you give attribute name,
        then PyTango will do additional IO to fetch AttributeInfoEx object from device server,
        since we must know to which c++ data type cast python value. If you would like to avoid this IO you
        can give AttributeInfoEx instead of attribute name.

    .. versionadded:: 7.0.0

    .. versionadded:: 8.1.0
        *green_mode* parameter.
        *wait* parameter.
        *timeout* parameter.

    .. versionchanged:: 10.1.0

        - attr_name parameter was renamed to attr
        - added support for AttributeInfoEx for attr parameter

    """
    result = self._write_read_attribute(attr, value, extract_as)
    return __check_read_attribute(result)


def __DeviceProxy__write_read_attributes(
    self,
    attr_values: Sequence[tuple[str | AttributeInfoEx, Any]],
    attr_read_names: Sequence[str],
    extract_as: ExtractAs = ExtractAs.Numpy,
) -> DeviceAttribute:
    """
    Write then read attribute(s) in a single network call. By
    default (serialisation by device), the execution of this
    call in the server can't be interrupted by other clients.
    On the server side, attribute(s) are first written and
    if no exception has been thrown during the write phase,
    attributes will be read.

    :param attr_values: A list of pairs (attr, value). See write_attribute
    :type attr_values: :py:obj:`typing.Sequence`\\[:py:obj:`tuple`\\[:py:obj:`str` |
                       :py:obj:`AttributeInfoEx`, :py:obj:`typing.Any`]]

    :param attr_read_names: A list of attributes to read.
    :type attr_read_names: :py:obj:`typing.Sequence`\\[:py:obj:`str`]

    :param extract_as: Defaults to numpy.
    :type extract_as: ExtractAs

    __GREEN_KWARGS_DESCRIPTION__

    :returns: A sequence DeviceAttribute object with readout values.
    :rtype: :py:obj:`list`\\[:obj:`tango.DeviceAttribute`]

    :throws:
        :py:obj:`tango.ConnectionFailed`: Raised in case of a connection failure. \n
        :py:obj:`tango.CommunicationFailed`: Raised in case of a communication failure. \n
        :py:obj:`tango.DeviceUnlocked`: Raised in case of an unlocked device. \n
        :py:obj:`tango.WrongData`: Raised in case of a wrong data format. \n
        :py:obj:`tango.DevFailed`: Raised in case of a device failure. \n
        :py:obj:`TypeError`: Raised in case of an incorrect type of input arguments.

    __GREEN_RAISES__

    .. versionadded:: 9.2.0

    .. note::
        For each pair of values there are two possibilities for the
        attr parameter: if you give attribute name, then PyTango must
        fetch attribute info for this attribute from server by additional synchronous(!)
        IO, since we must know to which c++ data type cast each python value.
        If you would like to avoid this IO you must give AttributeInfoEx instead of
        attribute name for each(!) pair of values.

    .. versionchanged:: 10.1.0

        - name_val parameter was renamed to attr_values
        - added support for AttributeInfoEx for attr_values parameter.


    """
    return self._write_read_attributes(attr_values, attr_read_names, extract_as)


def __DeviceProxy__get_property(
    self,
    propname: (
        str
        | DbDatum
        | DbData
        | list[str | bytes | DbDatum]
        | dict[str, DbDatum]
        | dict[str, list[str]]
        | dict[str, object]
    ),
    value=None,
) -> dict[str, list[str]]:
    """

    Get a (list) property(ies) for an attribute.

    :param propname: Can be one of the following: \n
                    1. :py:obj:`str` [in] - Single property data to be fetched. \n
                    2. :py:obj:`~tango.DbDatum` [in] - Single property data to be fetched. \n
                    3. :py:obj:`~tango.DbData` [in] - Several property data to be fetched. \n
                    4. :py:obj:`list`\\[:py:obj:`str` | :py:obj:`bytes` ] [in] - Several property data to be fetched. \n
                    5. :py:obj:`list`\\[:py:obj:`tango.DbDatum`] [in] - Several property data to be fetched. \n
                    6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] [in] - Keys are property names
                       to be fetched (values are ignored). \n
                    7. :py:obj:`dict`\\[:py:obj:`str`, :obj:`tango.DbDatum`] [in] - Several `DbDatum.name` are
                       property names to be fetched (keys are ignored). \n

    :param value: Optional. For propname overloads with :py:obj:`str` and :py:obj:`list`\\[:py:obj:`str`]
                  will be filed with the property values, if provided.
    :type value: :obj:`tango.DbData`, optional

    __GREEN_KWARGS_DESCRIPTION__

    :returns: A :obj:`dict` object, which keys are the property names the value
              associated with each key being a sequence of strings being the
              property value.

    :throws:
        :py:obj:`TypeError`: Raised in case of propname has the wrong type. \n
        :py:obj:`tango.NonDbDevice`: Raised in case of a non-database device error. \n
        :py:obj:`tango.ConnectionFailed`: Raised on connection failure with the database. \n
        :py:obj:`tango.CommunicationFailed`: Raised on communication failure with the database. \n
        :py:obj:`tango.DevFailed`: Raised on a device failure from the database device.`

    __GREEN_RAISES__

    .. versionadded:: 10.1.0: overloads with :obj:`dict` as propname parameter

    .. versionchanged:: 10.1.0: raises if propname has an invalid type instead of returning None
    """

    return get_property_from_db(self, propname, value)


def __DeviceProxy__put_property(
    self,
    value: (
        str
        | DbDatum
        | DbData
        | list[str | bytes | DbDatum]
        | dict[str, DbDatum]
        | dict[str, list[str]]
        | dict[str, object]
    ),
) -> None:
    """
    Insert or update a list of properties for this attribute.

    :param value: Can be one of the following: \n
                    1. :py:obj:`str` - Single property data to be inserted. \n
                    2. :py:obj:`~tango.DbDatum` - Single property data to be inserted. \n
                    3. :py:obj:`~tango.DbData` - Several property data to be inserted. \n
                    4. :py:obj:`list`\\[:py:obj:`str` | :py:obj:`bytes` | :py:obj:`~tango.DbDatum`] -
                       Several property data to be inserted. \n
                    5. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`~tango.DbDatum`] -
                       DbDatum is property to be inserted (keys are ignored). \n
                    6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`list`\\[:py:obj:`str`]] - Keys are property names,
                       and value has data to be inserted. \n
                    7. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] - Keys are property names,
                       and `str(obj)` is property value.

    __GREEN_KWARGS_DESCRIPTION__

    :throws:
        :py:obj:`TypeError`: Raised in case of value has the wrong type. \n
        :py:obj:`tango.NonDbDevice`: Raised in case of a non-database device error. \n
        :py:obj:`tango.ConnectionFailed`: Raised on connection failure with the database. \n
        :py:obj:`tango.CommunicationFailed`: Raised on communication failure with the database. \n
        :py:obj:`tango.DevFailed`: Raised on a device failure from the database device.`

    __GREEN_RAISES__
    """
    value = parameter_2_dbdata(value, "value")
    return self._put_property(value)


def __DeviceProxy__delete_property(
    self,
    value: (
        str
        | DbDatum
        | DbData
        | list[str | bytes | DbDatum]
        | dict[str, DbDatum]
        | dict[str, list[str]]
        | dict[str, object]
    ),
) -> None:
    """
    Delete the given properties for this attribute.

    :param value: Can be one of the following: \n
        1. :py:obj:`str` [in] - Single property data to be deleted. \n
        2. :py:obj:`~tango.DbDatum` [in] - Single property data to be deleted. \n
        3. :py:obj:`~tango.DbData` [in] - Several property data to be deleted. \n
        4. :py:obj:`list`\\[:py:obj:`str`] [in] - Several property data to be deleted. \n
        5. :py:obj:`list`\\[:py:obj:`tango.DbDatum`] [in] - Several property data to be deleted. \n
        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] [in] - Keys are property names
           to be deleted (values are ignored). \n
        7. :py:obj:`dict`\\[:py:obj:`str`, :obj:`tango.DbDatum`] [in] - Several `DbDatum.name` are
           property names to be deleted (keys are ignored). \n

    __GREEN_KWARGS_DESCRIPTION__

    :throws:
        :py:obj:`TypeError`: Raised in case of value has the wrong type. \n
        :py:obj:`tango.NonDbDevice`: Raised in case of a non-database device error. \n
        :py:obj:`tango.ConnectionFailed`: Raised on connection failure with the database. \n
        :py:obj:`tango.CommunicationFailed`: Raised on communication failure with the database. \n
        :py:obj:`tango.DevFailed`: Raised on a device failure from the database device.`

    __GREEN_RAISES__

    """
    new_value = parameter_2_dbdata(value, "value")
    return self._delete_property(new_value)


def __DeviceProxy__get_property_list(self, filter: str, array: list[object] | None = None) -> list[str]:
    """
    get_property_list(self, filter, array=None, __GREEN_KWARGS__) -> obj

    Get the list of property names for the device. The parameter
    filter allows the user to filter the returned name list. The
    wildcard character is '*'. Only one wildcard character is
    allowed in the filter parameter.

    :param filter: The filter wildcard.
    :type filter: :py:obj:`str`

    :param array: Optional. An array to be filled with the property names.
                  If `None`, a new list will be created internally with the values.
                  Defaults to `None`.
    :type array: :py:obj:`list`\\[:py:obj:`object`]

    __GREEN_KWARGS_DESCRIPTION__

    :returns: The given array filled with the property names, or a new list if `array` is `None`.
    :rtype: sequence obj

    :throws:
        :py:obj:`tango.NonDbDevice`: Raised in case of a non-database device error. \n
        :py:obj:`tango.WrongNameSyntax`: Raised in case of incorrect syntax in the name. \n
        :py:obj:`tango.ConnectionFailed`: Raised in case of a connection failure with the database. \n
        :py:obj:`tango.CommunicationFailed`: Raised in case of a communication failure with the database. \n
        :py:obj:`tango.DevFailed`: Raised in case of a device failure from the database device. \n
        :py:obj:`TypeError`: Raised in case of an incorrect type of input arguments.

    __GREEN_RAISES__

    :versionadded:: 7.0.0
    """

    if array is None:
        new_array = StdStringVector()
        self._get_property_list(filter, new_array)
        return new_array

    if isinstance(array, StdStringVector):
        self._get_property_list(filter, array)
        return array
    elif isinstance(array, collections.abc.Sequence):
        new_array = StdStringVector()
        self._get_property_list(filter, new_array)
        StdStringVector_2_seq(new_array, array)
        return array

    raise TypeError("array must be a mutable sequence<string>")


def __DeviceProxy__get_attribute_config(self, names: str | list[str]) -> AttributeInfoEx | AttributeInfoList:
    """
    get_attribute_config(self, name: str, __GREEN_KWARGS__) -> AttributeInfoEx
    get_attribute_config(self, names: list[str], __GREEN_KWARGS__) -> AttributeInfoList

    Return the attribute configuration for a single or a list of attribute(s). To get all the
    attributes pass a sequence containing the constant :obj:`tango.constants.AllAttr`

    .. deprecated:: use get_attribute_config_ex instead


    :param name: Attribute name.
    :type name: :py:obj:`str`

    :param names: Attribute names.
    :type names: :py:obj:`list`\\[:py:obj:`str`]

    __GREEN_KWARGS_DESCRIPTION__

    :returns: An `AttributeInfoEx` or `AttributeInfoList` object containing the attribute(s) information.
    :rtype: :obj:`tango.AttributeInfoEx` | :obj:`tango.AttributeInfoList`

    :throws:
        :py:obj:`tango.ConnectionFailed`: Raised in case of a connection failure. \n
        :py:obj:`tango.CommunicationFailed`: Raised in case of a communication failure. \n
        :py:obj:`tango.DevFailed`: Raised in case of a device failure. \n
        :py:obj:`TypeError`: Raised in case of an incorrect type of input arguments.

    __GREEN_RAISES__
    """
    if isinstance(names, StdStringVector) or is_pure_str(names):
        return self._get_attribute_config(names)
    elif isinstance(names, collections.abc.Sequence):
        v = seq_2_StdStringVector(names)
        return self._get_attribute_config(v)

    raise TypeError("value must be a string or a sequence<string>")


def __DeviceProxy__get_attribute_config_ex(self, names: str | list[str]) -> AttributeInfoListEx:
    """
    Return the extended attribute configuration for a single attribute or for the list of
    specified attributes. To get all the attributes pass a sequence
    containing the constant tango.constants.AllAttr.

    :param names: Attribute name or attribute names. Can be a single string (for one attribute) or a sequence of
                  strings (for multiple attributes).
    :type names: :py:obj:`str` | :py:obj:`list`\\[:py:obj:`str`]

    __GREEN_KWARGS_DESCRIPTION__

    :returns: An `AttributeInfoListEx` object containing the attribute information.
    :rtype: :obj:`~tango.AttributeInfoListEx`

    :throws:
        :py:obj:`~tango.ConnectionFailed`: Raised in case of a connection failure. \n
        :py:obj:`~tango.CommunicationFailed`: Raised in case of a communication failure. \n
        :py:obj:`~tango.DevFailed`: Raised in case of a device failure.

    __GREEN_RAISES__
    """
    if isinstance(names, StdStringVector):
        return self._get_attribute_config_ex(names)
    elif is_pure_str(names):
        v = StdStringVector()
        v.append(names)
        return self._get_attribute_config_ex(v)
    elif isinstance(names, collections.abc.Sequence):
        v = seq_2_StdStringVector(names)
        return self._get_attribute_config_ex(v)

    raise TypeError("value must be a string or a sequence<string>")


def __DeviceProxy__get_command_config(self, value=(constants.AllCmd,)) -> CommandInfoList | CommandInfo:
    """
    get_command_config(self, __GREEN_KWARGS__) -> CommandInfoList
    get_command_config(self, name: str, __GREEN_KWARGS__) -> CommandInfo
    get_command_config(self, names: Sequence[str], __GREEN_KWARGS__) -> CommandInfoList

    Return the command configuration for single/list/all command(s).

    :param name: Command name. Used when querying information for a single command.
    :type name: :py:obj:`str`, optional

    :param names: Command names. Used when querying information for multiple commands.
                  This parameter should not be used simultaneously with 'name'.
    :type names: :py:obj:`typing.Sequence`\\[:py:obj:`str`], optional

    __GREEN_KWARGS_DESCRIPTION__

    :returns: A `CommandInfoList` object containing the commands information if multiple command names are provided,
              or a `CommandInfo` object if a single command name is provided.
    :rtype: :py:obj:`~tango.CommandInfoList` | :py:obj:`~tango.CommandInfo`

    :throws:
        :py:obj:`tango.ConnectionFailed`: Raised in case of a connection failure. \n
        :py:obj:`tango.CommunicationFailed`: Raised in case of a communication failure. \n
        :py:obj:`tango.DevFailed`: Raised in case of a device failure. \n
        :py:obj:`TypeError`: Raised in case of an incorrect type of input arguments.

    __GREEN_RAISES__
    """
    if isinstance(value, StdStringVector) or is_pure_str(value):
        return self._get_command_config(value)
    elif isinstance(value, collections.abc.Sequence):
        v = seq_2_StdStringVector(value)
        return self._get_command_config(v)

    raise TypeError("value must be a string or a sequence<string>")


def __DeviceProxy__set_attribute_config(
    self,
    value: AttributeInfo | AttributeInfoEx | Sequence[AttributeInfo] | Sequence[AttributeInfoEx],
) -> None:
    """
    set_attribute_config(self, attr_info: AttributeInfo | Sequence[AttributeInfo], __GREEN_KWARGS__) -> None
    set_attribute_config(self, attr_info_ex: AttributeInfoEx | Sequence[AttributeInfoEx], __GREEN_KWARGS__) -> None

    Change the attribute configuration/extended attribute configuration for the specified attribute(s)

    :param attr_info: Attribute information. This parameter is used when providing basic attribute(s) information.
    :type attr_info: :py:obj:`tango.AttributeInfo` | :py:obj:`typing.Sequence`\\[:py:obj:`~tango.AttributeInfo`]]

    :param attr_info_ex: Extended attribute information.
                         This parameter is used when providing extended attribute information.
                         It should not be used simultaneously with 'attr_info'.
    :type attr_info_ex: :py:obj:`~tango.AttributeInfoEx` |
                        :py:obj:`typing.Sequence`\\[:py:obj:`~tango.AttributeInfoEx`]]

    __GREEN_KWARGS_DESCRIPTION__

    :returns: None

    :throws:
        :py:obj:`tango.ConnectionFailed`: Raised in case of a connection failure. \n
        :py:obj:`tango.CommunicationFailed`: Raised in case of a communication failure. \n
        :py:obj:`tango.DevFailed`: Raised in case of a device failure. \n
        :py:obj:`TypeError`: Raised in case of an incorrect type of input arguments.

    __GREEN_RAISES__

    """
    if isinstance(value, AttributeInfoEx):
        v = AttributeInfoListEx()
        v.append(value)
    elif isinstance(value, AttributeInfo):
        v = AttributeInfoList()
        v.append(value)
    elif isinstance(value, (AttributeInfoList, AttributeInfoListEx)):
        v = value
    elif isinstance(value, collections.abc.Sequence):
        if not len(value):
            return
        if isinstance(value[0], AttributeInfoEx):
            v = AttributeInfoListEx()
        elif isinstance(value[0], AttributeInfo):
            v = AttributeInfoList()
        else:
            raise TypeError(
                "Value must be a AttributeInfo, AttributeInfoEx, sequence<AttributeInfo> or sequence<AttributeInfoEx"
            )
        for i in value:
            v.append(i)
    else:
        raise TypeError(
            "Value must be a AttributeInfo, AttributeInfoEx, sequence<AttributeInfo> or sequence<AttributeInfoEx"
        )

    return self._set_attribute_config(v)


def __DeviceProxy__get_event_map_lock(self):
    """
    Internal helper method"""
    if "_subscribed_events_lock" not in self.__dict__:
        # do it like this instead of self._subscribed_events = dict() to avoid
        # calling __setattr__ which requests list of tango attributes from device
        self.__dict__["_subscribed_events_lock"] = threading.Lock()
    return self._subscribed_events_lock


def __DeviceProxy__get_event_map(self):
    """
    Internal helper method"""
    if "_subscribed_events" not in self.__dict__:
        # do it like this instead of self._subscribed_events = {} to avoid
        # calling __setattr__ which requests list of tango attributes from device
        self.__dict__["_subscribed_events"] = {}
    return self._subscribed_events


def __DeviceProxy__subscribe_event(self, *args, **kwargs) -> int:
    """
    subscribe_event(self, attr_name: str, event_type: EventType, cb: typing.Callable, sub_mode: EventSubMode=EventSubMode.SyncRead, extract_as: ExtractAs=ExtractAs.Numpy, *, __GREEN_KWARGS__) -> int
    subscribe_event(self, attr_name: str, event_type: EventType, queuesize: int, sub_mode: EventSubMode=EventSubMode.SyncRead, extract_as: ExtractAs=ExtractAs.Numpy, *, __GREEN_KWARGS__) -> int
    subscribe_event(self, event_type: EventType, cb: typing.Callable, sub_mode: EventSubMode=EventSubMode.SyncRead, *, __GREEN_KWARGS__) -> int

    .. note::
        This function is heavily overloaded, and includes three additional signatures that
        have been deprecated (see warning below).

    The client call to subscribe for event reception.  There are two main categories:

    * Subscribe to events for a specific attribute, like change events, providing
      either:

      * a callback function for immediate notification (*push* callback model), or
      * a queue length, allowing events to be processed later (*pull* callback model).

    * Subscribe to device-level events (not linked to a specific attribute), like
      interface-changed events. These require a callback function (*push* callback model).

    More details of the *push* and *pull* callback models are provided in the
    :external+tangodoc:ref:`cppTango Events API docs <events-tangoclient-api>`.

    A common example, subscribing to change events on the "voltage"  attribute
    with a callback, is shown below.

    .. code-block:: python

        from tango import DeviceProxy, EventData, EventType

        def on_change_event(evt: EventData):
            if evt.err:
                e = evt.errors[0]
                print(f"Event error: [{e.reason}] {e.desc}")
            else:
                print(f"Event received: [{evt.attr_value.quality}] {evt.attr_value.value}")

        # subscribe
        dp = DeviceProxy("my/power_supply/1")
        eid = dp.subscribe_event("voltage", EventType.CHANGE_EVENT, on_change_event)
        ...
        # when done with subscription
        dp.unsubscribe_event(eid)

    :param attr_name: The device attribute name which will be sent as an event, e.g., "current".
    :type attr_name: :py:obj:`str`

    :param event_type: The event reason, which must be one of the enumerated values in `EventType`. This includes:

        * `EventType.CHANGE_EVENT`
        * `EventType.ALARM_EVENT`
        * `EventType.PERIODIC_EVENT`
        * `EventType.ARCHIVE_EVENT`
        * `EventType.USER_EVENT`
        * `EventType.DATA_READY_EVENT`
        * `EventType.ATTR_CONF_EVENT`
        * `EventType.INTERFACE_CHANGE_EVENT`
    :type event_type: :py:obj:`~tango.EventType`

    :param cb:
        Any callable object or an object with a callable ``push_event`` method
        (i.e., use the *push* callback model).
        The callable has the signature ``def cb(event)`` (or ``async def cb(event)``
        for asyncio green mode DeviceProxy objects).  The ``event`` parameter's data
        type depends on the type of event subscribed to. In most cases it is
        :obj:`tango.EventData`.  Special cases are `EventType.DATA_READY`,
        `EventType.ATTR_CONF_EVENT`, and `EventType.INTERFACE_CHANGE_EVENT` -
        see :ref:`event-arrived-structures`.

    :type cb: :py:obj:`typing.Callable`

    :param queuesize:
        The size of the event reception buffer (i.e., use the *pull* callback model).
        The event reception buffer is implemented as a round-robin buffer.
        This way the client can set up different ways to receive events:

        * Event reception buffer size = 1 : The client is interested only in the value of the last event received.
          All other events that have been received since the last reading are discarded.
        * Event reception buffer size > 1 : The client has chosen to keep an event history of a given size.
          When more events arrive since the last reading, older events will be discarded.
        * Event reception buffer size = tango.constants.ALL_EVENTS : The client buffers all received events.
          The buffer size is unlimited and only restricted by the available memory for the client.
    :type queuesize: :py:obj:`int`

    :param sub_mode: The event subscription mode.
    :type sub_mode: :obj:`~tango.EventSubMode`

    :param extract_as: In which format to return the attribute values. Default: ExtractAs.NumPy
    :type extract_as: ExtractAs

    __GREEN_KWARGS_DESCRIPTION__

    :returns: An event id which has to be specified when unsubscribing from this event.
    :rtype: :py:obj:`int`

    :throws:
        :obj:`tango.EventSystemFailed`: Raised in case of a failure in the event system. \n
        :obj:`tango.DevFailed`: Raised in case of general communication failures. \n
        :obj:`TypeError`: Raised in case of an incorrect type of input arguments.

    __GREEN_RAISES__

    .. deprecated:: PyTango 10.1.0

        The following signatures, which use the ``filters`` and/or ``stateless``
        parameters, are deprecated. The version for removal has not been decided, but
        the earliest is version 11.0.0.

        * *subscribe_event(self, attr_name, event_type, cb, filters=[], stateless=False, extract_as=ExtractAs.Numpy, __GREEN_KWARGS__) -> int*
        * *subscribe_event(self, attr_name, event_type, queuesize, filters=[], stateless=False, extract_as=ExtractAs.Numpy, __GREEN_KWARGS__) -> int*
        * *subscribe_event(self, event_type, cb, stateless=False, *, __GREEN_KWARGS__) -> int*

        ``filters`` (*sequence<str>*)
            The filters apply to the original Notifd-based event system, not the
            current ZeroMQ-based event system (added in Tango 8). Notifd support is
            scheduled for removal in Tango 11.

            A variable length list of name-value pairs which define additional filters
            for events. Provide an empty list, if this feature is not needed
            (typically, for all Tango servers from version 8).

            Filters cannot be used with the `sub_mode` parameter.

        ``stateless`` (*bool*)
            Instead of setting ``stateless=True`` use ``sub_mode=EventSubMode.Stateless``.

            When this flag is set to false, an exception will be thrown if the event
            subscription encounters a problem. With the stateless flag set to true,
            the event subscription will not raise an exception, even if the corresponding
            device is not running, or the attribute doesn't exist.
            A keep-alive thread will attempt to subscribe for the specified event
            every 10 seconds, executing a callback with the corresponding exception at
            every retry.

            The ``stateless`` flag cannot be used with the `sub_mode` parameter.

    .. versionadded:: 10.1.0
        Three new signatures using the *sub_mode* parameter.

    .. versionchanged:: 10.1.0
        All parameters can now be passed as keyword arguments.
    """
    _check_only_allowed_kwargs(
        kwargs,
        {
            "attr_name",
            "event_type",
            "queuesize",
            "sub_mode",
            "extract_as",
            "cb",
            "filters",
            "stateless",
            "green_mode",
        },
    )

    if (args and isinstance(args[0], EventType)) or kwargs.get("event_type") == EventType.INTERFACE_CHANGE_EVENT:
        return __DeviceProxy__subscribe_event_global(self, *args, **kwargs)
    # The first argument is the attribute name
    else:
        return __DeviceProxy__subscribe_event_attrib(self, *args, **kwargs)


def __DeviceProxy__subscribe_event_global(self, *args, **kwargs):
    """
    Various signatures to resolve:
    index:                0             1     2
    subscribe_event(self, event_type,   cb,   stateless=False,                  *, green_mode=None) -> int
    subscribe_event(self, event_type,   cb,   sub_mode=EventSubMode.SyncRead,   *, green_mode=None) -> int
    """

    event_type, _ = _get_and_check_param(
        args,
        kwargs,
        "event_type",
        0,
        type_check=lambda x: isinstance(x, EventType),
    )

    if event_type != EventType.INTERFACE_CHANGE_EVENT:
        raise TypeError("This method is only for Interface Change Events")

    user_cb, _ = _get_and_check_param(
        args,
        kwargs,
        "cb",
        1,
        type_check=_is_callable_for_event,
        type_error_message="Parameter 'cb' must be callable object or an object with a 'push_event' method.",
    )

    sub_mode = EventSubMode.SyncRead
    stateless = None

    try:
        sub_mode, _ = _get_and_check_param(
            args,
            kwargs,
            "sub_mode",
            2,
            type_check=lambda x: isinstance(x, EventSubMode),
        )
    except (IndexError, PositionalArgTypeError):
        with contextlib.suppress(IndexError):
            stateless, _ = _get_and_check_param(
                args,
                kwargs,
                "stateless",
                2,
                type_check=lambda x: isinstance(x, bool),
                type_error_message=" must be either EventSubMode (sub_mode) or bool (stateless) type.",
            )

    green_mode = kwargs.get("green_mode")

    cbfn = __EventCallBack()
    cbfn.push_event = green_callback(_callable_for_event(user_cb), obj=self, green_mode=green_mode)

    if stateless is not None:
        warn_once(
            "The 'stateless' parameter is deprecated. "
            "The version for removal has not been decided, but the earliest is version 11.0.0. "
            "Please, update calls to use the 'sub_mode' parameter instead.",
            key="deprecated:tango.device_proxy:stateless_parameter",
            category=DeprecationWarning,
        )
        event_id = self.__subscribe_event_global_with_stateless_flag(event_type, cbfn, stateless)
    else:
        event_id = self.__subscribe_event_global_with_sub_mode(event_type, cbfn, sub_mode)

    _add_event_to_map(self, event_id, cbfn, event_type, "dummy")
    return event_id


def __DeviceProxy__subscribe_event_attrib(self, *args, **kwargs):
    """
    Various signatures to resolve:
              index:          0          1           2          3                               4
        subscribe_event(self, attr_name, event_type, cb,        sub_mode=EventSubMode.SyncRead, extract_as=ExtractAs.Numpy,                             *,  green_mode=None) -> int
        subscribe_event(self, attr_name, event_type, queuesize, sub_mode=EventSubMode.SyncRead, extract_as=ExtractAs.Numpy,                             *,  green_mode=None) -> int

    DEPRECATED, but still valid:
              index:          0          1           2          3                               4                           5
        subscribe_event(self, attr_name, event_type, cb,        filters=[],                     stateless=False,            extract_as=ExtractAs.Numpy, *, green_mode=None) -> int
        subscribe_event(self, attr_name, event_type, queuesize, filters=[],                     stateless=False,            extract_as=ExtractAs.Numpy, *, green_mode=None) -> int

    """

    attr_name, _ = _get_and_check_param(
        args,
        kwargs,
        "attr_name",
        0,
        type_check=is_pure_str,
    )

    event_type, _ = _get_and_check_param(
        args,
        kwargs,
        "event_type",
        1,
        type_check=lambda x: isinstance(x, EventType),
    )

    if "cb" in kwargs and "queuesize" in kwargs:
        raise TypeError(f"Parameters 'cb' and 'queuesize' cannot be used together'. {args=}, {kwargs=}")
    user_cb = None
    queuesize = None
    try:
        user_cb, _ = _get_and_check_param(
            args,
            kwargs,
            "cb",
            2,
            type_check=_is_callable_for_event,
            type_error_message="Parameter 'cb' must be callable object or an object with a 'push_event' method",
        )
    except (IndexError, PositionalArgTypeError):
        try:
            queuesize, _ = _get_and_check_param(args, kwargs, "queuesize", 2, type_check=is_integer)
        except (IndexError, PositionalArgTypeError):
            raise TypeError(
                f"Either parameter 'queuesize' must be an integer, or parameter 'cb' "
                f"must be callable object or an object with a 'push_event' method. "
                f"{args=}, {kwargs=}."
            ) from None

    if "sub_mode" in kwargs and "filters" in kwargs:
        raise TypeError(f"Parameters 'sub_mode' and 'filters' cannot be used together. {args=}, {kwargs=}")
    if "sub_mode" in kwargs and "stateless" in kwargs:
        raise TypeError(f"Parameters 'sub_mode' and 'stateless' cannot be used together. {args=}, {kwargs=}")
    sub_mode = None
    filters = None
    sub_mode_from_caller = False
    filters_from_caller = False
    arg_shift = 0
    try:
        sub_mode, _ = _get_and_check_param(
            args,
            kwargs,
            "sub_mode",
            3,
            type_check=lambda x: isinstance(x, EventSubMode),
            type_error_message="Parameter 'sub_mode' must be of type EventSubMode",
        )
        sub_mode_from_caller = True
    except (IndexError, PositionalArgTypeError) as sub_mode_exc:
        try:
            filters, _ = _get_and_check_param(
                args,
                kwargs,
                "filters",
                3,
                type_check=is_non_str_seq,
                type_error_message="Parameter 'filters' must be sequence of str",
            )
            filters_from_caller = True
            if "filters" not in kwargs:
                arg_shift = 1
        except (IndexError, PositionalArgTypeError) as filters_exc:
            if isinstance(sub_mode_exc, PositionalArgTypeError):
                raise sub_mode_exc from None
            elif isinstance(filters_exc, PositionalArgTypeError):
                raise filters_exc from None
            # fallback to defaults
            sub_mode = EventSubMode.SyncRead
            filters = []

    stateless = None
    stateless_from_caller = False
    if not sub_mode_from_caller:
        stateless, used_default = _get_and_check_param(
            args,
            kwargs,
            "stateless",
            4,
            default=False,
            type_check=lambda x: isinstance(x, bool),
            type_error_message="Parameter 'stateless' must be of type bool",
        )
        stateless_from_caller = not used_default

    extract_as, _ = _get_and_check_param(
        args,
        kwargs,
        "extract_as",
        4 + arg_shift,
        type_check=lambda x: isinstance(x, ExtractAs),
        default=ExtractAs.Numpy,
        type_error_message="Parameter 'extract_as' must be of type ExtractAs",
    )

    green_mode = kwargs.get("green_mode")

    # at least one of "cb" or "queuesize" must be provided
    if user_cb:
        cb_or_queuesize = __EventCallBack()
        cb_or_queuesize.push_event = green_callback(_callable_for_event(user_cb), obj=self, green_mode=green_mode)
    elif queuesize is not None:
        cb_or_queuesize = queuesize
    else:
        raise TypeError(
            f"Either parameter 'queuesize' must be an integer, or parameter 'cb' "
            f"must be callable object or an object with a 'push_event' method. "
            f"{args=}, {kwargs=}."
        )

    if sub_mode_from_caller:
        use_sub_mode = True
    elif filters_from_caller or stateless_from_caller:
        use_sub_mode = False
    else:
        use_sub_mode = True

    if use_sub_mode:
        event_id = self.__subscribe_event_attrib_with_sub_mode(
            attr_name, event_type, cb_or_queuesize, sub_mode, extract_as
        )
    else:
        warn_once(
            "The 'stateless' and 'filters' parameters are deprecated. "
            "The version for removal has not been decided, but the earliest is version 11.0.0. "
            "Please, update calls to use the 'sub_mode' parameter instead.",
            key="deprecated:tango.device_proxy:stateless_and_filters_parameters",
            category=DeprecationWarning,
        )
        event_id = self.__subscribe_event_attrib_with_stateless_flag(
            attr_name, event_type, cb_or_queuesize, stateless, extract_as, filters
        )

    _add_event_to_map(self, event_id, cb_or_queuesize, event_type, attr_name)

    return event_id


class _DummyValue:
    pass


_DUMMY_VALUE = _DummyValue()


class PositionalArgTypeError(TypeError):
    pass


def _get_and_check_param(
    user_args: tuple[Any, ...],
    user_kwargs: dict[str, Any],
    name: str,
    index: int,
    default: Any = _DUMMY_VALUE,
    type_check: Any = None,
    type_error_message: str = "",
) -> tuple[Any, bool]:
    used_default = False
    if name in user_kwargs:
        value = user_kwargs[name]
        if callable(type_check) and not type_check(value):
            raise TypeError(f"Invalid type for parameter '{name}={value}': {type_error_message}")
        return value, used_default

    if len(user_args) > index:
        value = user_args[index]
    else:
        if isinstance(default, _DummyValue):
            raise IndexError(
                f"Expected parameter '{name}' as either positional arg {index + 1}, "
                f"(but only {len(user_args)} provided), or as keyword argument. "
                f"{user_args=}, {user_kwargs=}."
            )
        value = default
        used_default = True

    if callable(type_check) and not type_check(value):
        raise PositionalArgTypeError(
            f"Invalid type for parameter '{name}' at position {index}: {type_error_message}. Received: {type(value)}"
        )

    return value, used_default


def _callable_for_event(fn):
    if isinstance(fn, collections.abc.Callable):
        return fn
    elif hasattr(fn, "push_event") and isinstance(fn.push_event, collections.abc.Callable):
        return fn.push_event
    else:
        return None


def _is_callable_for_event(fn):
    return _callable_for_event(fn) is not None


def _add_event_to_map(self, event_id, cb_or_queuesize, event_type, attr_name):
    with self.__get_event_map_lock():
        se = self.__get_event_map()
        evt_data = se.get(event_id)
        if evt_data is None:
            se[event_id] = (cb_or_queuesize, event_type, attr_name)
            return

        # Raise exception
        desc = textwrap.dedent(
            f"""\
Internal PyTango error:
{self}.subscribe_event({attr_name}, {event_type}) already has key {event_id} assigned to ({evt_data[2]}, {evt_data[1]})
Please report error to PyTango"""
        )
        Except.throw_exception("Py_InternalError", desc, "DeviceProxy.subscribe_event")


def __dummy_event_receiver(_event):
    pass


async def __async_dummy_event_receiver(_event):
    pass


def __DeviceProxy__unsubscribe_event(self, event_id: int) -> None:
    """
    Unsubscribes a client from receiving the event specified by event_id.

    :param event_id: The event identifier returned by `DeviceProxy::subscribe_event()`.
                     Unlike in TangoC++, this implementation checks that the `event_id` has
                     been subscribed to in this `DeviceProxy`.
    :type event_id: :py:obj:`int`

    __GREEN_KWARGS_DESCRIPTION__

    :returns: None

    :throws:
        :obj:`tango.EventSystemFailed`: Raised in case of a failure in the event system. \n
        :obj:`KeyError`: Raised if the specified `event_id` is not found or not subscribed in
                         this :py:obj:`~tango.DeviceProxy`.

    __GREEN_RAISES__
    """
    events_del = set()
    timestamp = time.time()
    se = self.__get_event_map()

    with self.__get_event_map_lock():
        # first delete event callbacks that have expired
        for evt_id, (_, expire_time) in self._pending_unsubscribe.items():
            if expire_time <= timestamp:
                events_del.add(evt_id)
        for evt_id in events_del:
            del self._pending_unsubscribe[evt_id]

        # unsubscribe and put the callback in the pending unsubscribe callbacks
        try:
            evt_info = se[event_id]
        except KeyError:
            raise KeyError("This device proxy does not own this subscription " + str(event_id)) from None

        del se[event_id]

        # if we subscribe callback, we have to keep it alive for sometime,
        # in case there is delayed event comming
        if hasattr(evt_info[0], "push_event"):
            if self.get_green_mode() == GreenMode.Asyncio:
                evt_info[0].push_event = __async_dummy_event_receiver
            else:
                evt_info[0].push_event = __dummy_event_receiver

            self._pending_unsubscribe[event_id] = (
                evt_info[0],
                timestamp + _UNSUBSCRIBE_LIFETIME,
            )

    self.__unsubscribe_event(event_id)


def __DeviceProxy__unsubscribe_event_all(self):
    with self.__get_event_map_lock():
        se = self.__get_event_map()
        event_ids = list(se.keys())
        se.clear()
    for event_id in event_ids:
        self.__unsubscribe_event(event_id)


def __DeviceProxy__get_events(
    self,
    event_id: int,
    callback: Callable | None = None,
    extract_as: ExtractAs = ExtractAs.Numpy,
) -> None:
    """

    The method extracts all waiting events from the event reception buffer.

    If callback is not None, it is executed for every event. During event
    subscription the client must have chosen the pull model for this event.
    The callback will receive a parameter of type EventData,
    AttrConfEventData or DataReadyEventData depending on the type of the
    event (event_type parameter of subscribe_event).

    If callback is None, the method extracts all waiting events from the
    event reception buffer. The returned event_list is a vector of
    EventData, AttrConfEventData or DataReadyEventData pointers, just
    the same data the callback would have received.

    :param event_id: The event identifier returned by the `DeviceProxy.subscribe_event()` method.
    :type event_id: :py:obj:`int`

    :param callback: Any callable object or any object with a "push_event" method.
    :type callback: :py:obj:`typing.Callable`

    :param extract_as: (Description Needed)
    :type extract_as: :py:obj:`~tango.ExtractAs`

    :throws:
        :py:obj:`tango.EventSystemFailed`: Raised in case of a failure in the event system. \n
        :py:obj:`TypeError`: Raised in case of an incorrect type of input arguments. \n
        :py:obj:`ValueError`: Raised in case of an invalid value.

    :see also: :meth:`~tango.DeviceProxy.subscribe_event`

    """
    if callback is None:
        _, event_type, _ = self.__get_event_map().get(event_id, (None, None, None))
        if event_type is None:
            raise ValueError(f"Invalid event_id. You are not subscribed to event {event_id!s}.")
        if event_type in (
            EventType.CHANGE_EVENT,
            EventType.ALARM_EVENT,
            EventType.PERIODIC_EVENT,
            EventType.ARCHIVE_EVENT,
            EventType.USER_EVENT,
        ):
            return self.__get_data_events(event_id, extract_as)
        elif event_type in (EventType.ATTR_CONF_EVENT,):
            return self.__get_attr_conf_events(event_id)
        elif event_type in (EventType.DATA_READY_EVENT,):
            return self.__get_data_ready_events(event_id)
        elif event_type in (EventType.INTERFACE_CHANGE_EVENT,):
            return self.__get_devintr_change_events(event_id, extract_as)
        else:
            raise ValueError("Unknown event_type: " + str(event_type))
    elif isinstance(callback, collections.abc.Callable):
        cb = __EventCallBack()
        cb.push_event = callback
        return self.__get_callback_events(event_id, cb, extract_as)
    elif hasattr(callback, "push_event") and isinstance(callback.push_event, collections.abc.Callable):
        cb = __EventCallBack()
        cb.push_event = callback.push_event
        return self.__get_callback_events(event_id, cb, extract_as)
    else:
        raise TypeError(
            "Parameter 'callback' should be None, a callable object or an object with a 'push_event' method."
        )


def __DeviceProxy___get_info_(self):
    """Protected method that gets device info once and stores it in cache"""
    if "_dev_info" not in self.__dict__:
        try:
            info = self.info()
            info_without_cyclic_reference = __TangoInfo.from_copy(info)
            self.__dict__["_dev_info"] = info_without_cyclic_reference
        except Exception:
            return __TangoInfo.from_defaults()
    return self._dev_info


def __DeviceProxy__str(self):
    is_safe_to_access_proxy = self.__dict__.get("_initialized", False)
    if is_safe_to_access_proxy:
        info = self._get_info_()
        dev_class = info.dev_class
        dev_name = self.dev_name()
    else:
        dev_class = "DeviceProxy<Unknown Device>"
        dev_name = "<object was not fully initialized>"
    return f"{dev_class}({dev_name})"


def __DeviceProxy__read_attributes(
    self, attr_names: Sequence[str], extract_as: ExtractAs = ExtractAs.Numpy
) -> list[DeviceAttribute]:
    """
    Read the list of specified attributes.

    :param attr_names: A list of attributes to read.
    :type attr_names: :py:obj:`typing.Sequence`\\[:py:obj:`str`]

    :param extract_as: In which format to return the attribute values.
    :type extract_as: :py:obj:`~tango.ExtractAs`

    __GREEN_KWARGS_DESCRIPTION__

    :returns: A list of DeviceAttribute objects.
    :rtype: :py:obj:`list`\\[:obj:`tango.DeviceAttribute`]

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DeviceUnlocked`, :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 8.1.0
        *green_mode* parameter.
        *wait* parameter.
        *timeout* parameter.
    """
    return self._read_attributes(attr_names, extract_as)


def __DeviceProxy__write_attribute(self, attr: str | AttributeInfoEx, value: Any) -> None:
    """
    write_attribute(self, attr, value, __GREEN_KWARGS__) -> None

    Write a single attribute.

    :param attr: The name or AttributeInfoEx structure of the attribute to write.
    :type attr: :py:obj:`str` | :py:obj:`tango.AttributeInfoEx`

    :param value: The value to write to the attribute.
    :type value: :py:obj:`typing.Any`

    __GREEN_KWARGS_DESCRIPTION__

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DeviceUnlocked`, :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 8.1.0
        *green_mode* parameter.
        *wait* parameter.
        *timeout* parameter.

    .. versionchanged:: 10.1.0 attr_name parameter was renamed to attr

    """
    return self._write_attribute(attr, value)


def __DeviceProxy__write_attributes(self, attr_values: Sequence[tuple[str | AttributeInfoEx, Any]]) -> None:
    """
    Write the specified attributes.

    :param attr_values: A list of pairs (attr, value). See write_attribute
    :type attr_values: :py:obj:`typing.Sequence`\\[:py:obj:`tuple`\\[:py:obj:`str` |
                       :py:obj:`AttributeInfoEx`, :py:obj:`typing.Any`]]

    __GREEN_KWARGS_DESCRIPTION__

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`, :py:obj:`tango.DeviceUnlocked`,
             :py:obj:`tango.DevFailed`, :py:obj:`tango.NamedDevFailedList`: from device

    __GREEN_RAISES__

    .. versionadded:: 8.1.0
        *green_mode* parameter.
        *wait* parameter.
        *timeout* parameter.

    .. versionchanged:: 10.1.0

        - name_val parameter was renamed to attr_values
        - added support for AttributeInfoEx for attr_values parameter
    """
    return self._write_attributes(attr_values)


def __DeviceProxy__ping(self) -> int:
    """
    A method which sends a ping to the device

    __GREEN_KWARGS_DESCRIPTION__

    :returns: time elapsed in microseconds
    :rtype: :py:obj:`int`

    __GREEN_RAISES__

    """
    return self._ping()


def __DeviceProxy__state(self) -> DevState:
    """
    A method which returns the state of the device.

    __GREEN_KWARGS_DESCRIPTION__

    :returns: A `DevState` constant.
    :rtype: :py:obj:`~tango.DevState`

    __GREEN_RAISES__

    """
    return self._state()


def __DeviceProxy__status(self) -> str:
    """
    A method which returns the status of the device as a string.

    __GREEN_KWARGS_DESCRIPTION__

    :returns: string describing the device status
    :rtype: :py:obj:`str`

    __GREEN_RAISES__

    """
    return self._status()


def __safe_call(fn):

    already_wrapped = hasattr(fn, "__access_wrapped__")
    if already_wrapped:
        return fn

    @functools.wraps(fn)
    def safe_call_wrapper(self, *args, **kwargs):
        if not self._initialized:
            raise RuntimeError("DeviceProxy object was not fully initialized.")
        return fn(self, *args, **kwargs)

    fn.__access_wrapped__ = True

    return safe_call_wrapper


def __DeviceProxy__set_telemetry_logging(self, enabled: bool) -> None:
    """
    Set the enabled state of telemetry logging for the device.

    :param enabled: True to enable telemetry logging, False to disable it.
    :type enabled: :py:obj:`bool`

    __GREEN_KWARGS_DESCRIPTION__

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return self._set_telemetry_logging(enabled)


def __DeviceProxy__get_telemetry_logging(self) -> bool:
    """
    Get the enabled state of telemetry logging for the device.

    __GREEN_KWARGS_DESCRIPTION__

    :return: The enabled state of telemetry logging.
    :rtype: :py:obj:`bool`

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return self._get_telemetry_logging()


def __DeviceProxy__set_telemetry_logging_endpoints(self, endpoints: Sequence[TelemetryEndpoint]) -> None:
    """
    Set the telemetry logging endpoints for the device.

    Replaces all existing telemetry logging endpoints with the provided endpoints.

    :param endpoints: Telemetry logging endpoints to configure.
    :type endpoints: :py:obj:`~collections.abc.Sequence` of :obj:`~tango.telemetry.TelemetryEndpoint`

    __GREEN_KWARGS_DESCRIPTION__

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return self._set_telemetry_logging_endpoints(_telemetry_endpoints_to_wire(endpoints))


def __DeviceProxy__get_telemetry_logging_endpoints(
    self,
) -> tuple[TelemetryEndpoint, ...]:
    """
    Get the telemetry logging endpoints configured for the device.

    __GREEN_KWARGS_DESCRIPTION__

    :return: The configured telemetry logging endpoints.
    :rtype: :py:obj:`tuple` of :obj:`~tango.telemetry.TelemetryEndpoint`

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return _telemetry_endpoints_from_wire(self._get_telemetry_logging_endpoints())


def __DeviceProxy__add_telemetry_logging_endpoint(self, endpoint: TelemetryEndpoint) -> None:
    """
    Add a telemetry logging endpoint for the device.

    :param endpoint: Telemetry logging endpoint to add.
    :type endpoint: :obj:`~tango.telemetry.TelemetryEndpoint`

    __GREEN_KWARGS_DESCRIPTION__

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return self._add_telemetry_logging_endpoint(_telemetry_endpoint_to_wire(endpoint))


def __DeviceProxy__remove_telemetry_logging_endpoint(self, endpoint: TelemetryEndpoint) -> None:
    """
    Remove a telemetry logging endpoint from the device.

    :param endpoint: Telemetry logging endpoint to remove.
    :type endpoint: :obj:`~tango.telemetry.TelemetryEndpoint`

    __GREEN_KWARGS_DESCRIPTION__

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return self._remove_telemetry_logging_endpoint(_telemetry_endpoint_to_wire(endpoint))


def __DeviceProxy__set_telemetry_tracing(self, enabled: bool) -> None:
    """
    Set the enabled state of telemetry tracing for the device.

    :param enabled: True to enable telemetry tracing, False to disable it.
    :type enabled: :py:obj:`bool`

    __GREEN_KWARGS_DESCRIPTION__

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return self._set_telemetry_tracing(enabled)


def __DeviceProxy__get_telemetry_tracing(self) -> bool:
    """
    Get the enabled state of telemetry tracing for the device.

    __GREEN_KWARGS_DESCRIPTION__

    :return: The enabled state of telemetry tracing.
    :rtype: :py:obj:`bool`

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return self._get_telemetry_tracing()


def __DeviceProxy__set_telemetry_tracing_endpoints(self, endpoints: Sequence[TelemetryEndpoint]) -> None:
    """
    Set the telemetry tracing endpoints for the device.

    Replaces all existing telemetry tracing endpoints with the provided endpoints.

    :param endpoints: Telemetry tracing endpoints to configure.
    :type endpoints: :py:obj:`~collections.abc.Sequence` of :obj:`~tango.telemetry.TelemetryEndpoint`

    __GREEN_KWARGS_DESCRIPTION__

    :throws: :py:obj:`~tango.ConnectionFailed`: Raised in case of a connection failure \n
             :py:obj:`~tango.CommunicationFailed`: Raised in case of a communication failure. \n
             :py:obj:`~tango.DevFailed`: Raised in case of a device failure

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return self._set_telemetry_tracing_endpoints(_telemetry_endpoints_to_wire(endpoints))


def __DeviceProxy__get_telemetry_tracing_endpoints(
    self,
) -> tuple[TelemetryEndpoint, ...]:
    """
    Get the telemetry tracing endpoints configured for the device.

    __GREEN_KWARGS_DESCRIPTION__

    :return: The configured telemetry tracing endpoints.
    :rtype: :py:obj:`tuple` of :obj:`~tango.telemetry.TelemetryEndpoint`

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return _telemetry_endpoints_from_wire(self._get_telemetry_tracing_endpoints())


def __DeviceProxy__add_telemetry_tracing_endpoint(self, endpoint: TelemetryEndpoint) -> None:
    """
    Add a telemetry tracing endpoint for the device.

    :param endpoint: Telemetry tracing endpoint to add.
    :type endpoint: :obj:`~tango.telemetry.TelemetryEndpoint`

    __GREEN_KWARGS_DESCRIPTION__

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return self._add_telemetry_tracing_endpoint(_telemetry_endpoint_to_wire(endpoint))


def __DeviceProxy__remove_telemetry_tracing_endpoint(self, endpoint: TelemetryEndpoint) -> None:
    """
    Remove a telemetry tracing endpoint from the device.

    :param endpoint: Telemetry tracing endpoint to remove.
    :type endpoint: :obj:`~tango.telemetry.TelemetryEndpoint`

    __GREEN_KWARGS_DESCRIPTION__

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return self._remove_telemetry_tracing_endpoint(_telemetry_endpoint_to_wire(endpoint))


def __DeviceProxy__start_telemetry(self) -> None:
    """
    Start the telemetry service for the device.

    __GREEN_KWARGS_DESCRIPTION__

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return self._start_telemetry()


def __DeviceProxy__stop_telemetry(self) -> None:
    """
    Stop the telemetry service for the device.

    __GREEN_KWARGS_DESCRIPTION__

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return self._stop_telemetry()


def __DeviceProxy__is_telemetry_enabled(self) -> bool:
    """
    Get the enabled state of the telemetry service for the device.

    __GREEN_KWARGS_DESCRIPTION__

    :return: The enabled state of device telemetry.
    :rtype: :py:obj:`bool`

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return self._is_telemetry_enabled()


def __normalize_telemetry_topics(topics):
    return [str(topic).strip().lower() for topic in topics if str(topic).strip()]


def __DeviceProxy__set_telemetry_topics(self, topics: Sequence[str]) -> None:
    """
    Set the telemetry topics configured for the device.

    :param topics: Telemetry topics to configure.
    :type topics: :py:obj:`typing.Sequence`\\[:py:obj:`str`]

    __GREEN_KWARGS_DESCRIPTION__

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return self._set_telemetry_topics(__normalize_telemetry_topics(topics))


def __DeviceProxy__get_telemetry_topics(self) -> tuple[str, ...]:
    """
    Get the telemetry topics configured for the device.

    __GREEN_KWARGS_DESCRIPTION__

    :return: The configured telemetry topics.
    :rtype: :py:obj:`tuple`\\[:py:obj:`str`, ...]

    :throws: :py:obj:`tango.ConnectionFailed`, :py:obj:`tango.CommunicationFailed`,
             :py:obj:`tango.DevFailed`: from device

    __GREEN_RAISES__

    .. versionadded:: 10.3.0
    """
    return tuple(self._get_telemetry_topics())


def device_proxy_init():
    DeviceProxy.__init_orig__ = DeviceProxy.__init__
    DeviceProxy.__init__ = _trace_client(__DeviceProxy____init__)

    DeviceProxy.get_green_mode = __DeviceProxy__get_green_mode
    DeviceProxy.set_green_mode = __DeviceProxy__set_green_mode

    DeviceProxy.freeze_dynamic_interface = __DeviceProxy__freeze_dynamic_interface
    DeviceProxy.unfreeze_dynamic_interface = __DeviceProxy__unfreeze_dynamic_interface
    DeviceProxy.is_dynamic_interface_frozen = __DeviceProxy__is_dynamic_interface_frozen

    DeviceProxy.set_attribute_config_cache = __DeviceProxy__set_attribute_config_cache
    DeviceProxy.is_attribute_config_cache_enabled = __DeviceProxy__is_attribute_config_cache_enabled
    DeviceProxy.invalidate_attribute_config_cache = __DeviceProxy__invalidate_attribute_config_cache

    DeviceProxy.__get_cmd_cache = __DeviceProxy__get_cmd_cache
    DeviceProxy.__get_attr_cache = __DeviceProxy__get_attr_cache
    DeviceProxy.__refresh_cmd_cache = __DeviceProxy__refresh_cmd_cache
    DeviceProxy.__refresh_attr_cache = __DeviceProxy__refresh_attr_cache

    DeviceProxy.ping = green(_trace_client(__DeviceProxy__ping), update_signature_and_docstring=True)
    DeviceProxy.state = green(_trace_client(__DeviceProxy__state), update_signature_and_docstring=True)
    DeviceProxy.status = green(_trace_client(__DeviceProxy__status), update_signature_and_docstring=True)
    DeviceProxy.state = green(_trace_client(__DeviceProxy__state), update_signature_and_docstring=True)
    DeviceProxy.status = green(_trace_client(__DeviceProxy__status), update_signature_and_docstring=True)

    DeviceProxy.read_attribute = green(
        _trace_client(__DeviceProxy__read_attribute),
        update_signature_and_docstring=True,
    )
    DeviceProxy.read_attributes = green(
        _trace_client(__DeviceProxy__read_attributes),
        update_signature_and_docstring=True,
    )
    DeviceProxy.write_attribute = green(
        _trace_client(__DeviceProxy__write_attribute),
        update_signature_and_docstring=True,
    )
    DeviceProxy.write_attributes = green(
        _trace_client(__DeviceProxy__write_attributes),
        update_signature_and_docstring=True,
    )
    DeviceProxy.write_attributes = green(
        _trace_client(__DeviceProxy__write_attributes),
        update_signature_and_docstring=True,
    )
    DeviceProxy.write_read_attribute = green(
        _trace_client(__DeviceProxy__write_read_attribute),
        update_signature_and_docstring=True,
    )
    DeviceProxy.write_read_attributes = green(
        _trace_client(__DeviceProxy__write_read_attributes),
        update_signature_and_docstring=True,
    )

    DeviceProxy.read_attributes_asynch = green(
        _trace_client(__DeviceProxy__read_attributes_asynch),
        update_signature_and_docstring=True,
    )
    DeviceProxy.read_attribute_asynch = green(
        _trace_client(__DeviceProxy__read_attribute_asynch),
        update_signature_and_docstring=True,
    )

    DeviceProxy.read_attributes_reply = green(
        _trace_client(__DeviceProxy__read_attributes_reply),
        update_signature_and_docstring=True,
    )
    DeviceProxy.read_attribute_reply = green(
        _trace_client(__DeviceProxy__read_attribute_reply),
        update_signature_and_docstring=True,
    )

    DeviceProxy.write_attributes_asynch = green(
        _trace_client(__DeviceProxy__write_attributes_asynch),
        update_signature_and_docstring=True,
    )
    DeviceProxy.write_attribute_asynch = green(
        _trace_client(__DeviceProxy__write_attribute_asynch),
        update_signature_and_docstring=True,
    )

    DeviceProxy.write_attributes_reply = green(
        _trace_client(__DeviceProxy__write_attributes_reply),
        update_signature_and_docstring=True,
    )
    DeviceProxy.write_attribute_reply = green(
        _trace_client(__DeviceProxy__write_attribute_reply),
        update_signature_and_docstring=True,
    )

    DeviceProxy.get_property = green(_trace_client(__DeviceProxy__get_property), update_signature_and_docstring=True)
    DeviceProxy.put_property = green(_trace_client(__DeviceProxy__put_property), update_signature_and_docstring=True)
    DeviceProxy.delete_property = green(
        _trace_client(__DeviceProxy__delete_property),
        update_signature_and_docstring=True,
    )
    DeviceProxy.get_property_list = green(
        _trace_client(__DeviceProxy__get_property_list),
        update_signature_and_docstring=True,
    )
    DeviceProxy.get_attribute_config = green(
        _trace_client(__DeviceProxy__get_attribute_config),
        update_signature_and_docstring=True,
    )
    DeviceProxy.get_attribute_config_ex = green(
        _trace_client(__DeviceProxy__get_attribute_config_ex),
        update_signature_and_docstring=True,
    )
    DeviceProxy.set_attribute_config = green(
        _trace_client(__DeviceProxy__set_attribute_config),
        update_signature_and_docstring=True,
    )

    DeviceProxy.get_command_config = green(
        _trace_client(__DeviceProxy__get_command_config),
        update_signature_and_docstring=True,
    )

    DeviceProxy.set_telemetry_logging = green(
        _trace_client(__DeviceProxy__set_telemetry_logging),
        update_signature_and_docstring=True,
    )
    DeviceProxy.get_telemetry_logging = green(
        _trace_client(__DeviceProxy__get_telemetry_logging),
        update_signature_and_docstring=True,
    )
    DeviceProxy.set_telemetry_logging_endpoints = green(
        _trace_client(__DeviceProxy__set_telemetry_logging_endpoints),
        update_signature_and_docstring=True,
    )
    DeviceProxy.get_telemetry_logging_endpoints = green(
        _trace_client(__DeviceProxy__get_telemetry_logging_endpoints),
        update_signature_and_docstring=True,
    )
    DeviceProxy.add_telemetry_logging_endpoint = green(
        _trace_client(__DeviceProxy__add_telemetry_logging_endpoint),
        update_signature_and_docstring=True,
    )
    DeviceProxy.remove_telemetry_logging_endpoint = green(
        _trace_client(__DeviceProxy__remove_telemetry_logging_endpoint),
        update_signature_and_docstring=True,
    )
    DeviceProxy.set_telemetry_tracing = green(
        _trace_client(__DeviceProxy__set_telemetry_tracing),
        update_signature_and_docstring=True,
    )
    DeviceProxy.get_telemetry_tracing = green(
        _trace_client(__DeviceProxy__get_telemetry_tracing),
        update_signature_and_docstring=True,
    )
    DeviceProxy.set_telemetry_tracing_endpoints = green(
        _trace_client(__DeviceProxy__set_telemetry_tracing_endpoints),
        update_signature_and_docstring=True,
    )
    DeviceProxy.get_telemetry_tracing_endpoints = green(
        _trace_client(__DeviceProxy__get_telemetry_tracing_endpoints),
        update_signature_and_docstring=True,
    )
    DeviceProxy.add_telemetry_tracing_endpoint = green(
        _trace_client(__DeviceProxy__add_telemetry_tracing_endpoint),
        update_signature_and_docstring=True,
    )
    DeviceProxy.remove_telemetry_tracing_endpoint = green(
        _trace_client(__DeviceProxy__remove_telemetry_tracing_endpoint),
        update_signature_and_docstring=True,
    )
    DeviceProxy.start_telemetry = green(
        _trace_client(__DeviceProxy__start_telemetry),
        update_signature_and_docstring=True,
    )
    DeviceProxy.stop_telemetry = green(
        _trace_client(__DeviceProxy__stop_telemetry),
        update_signature_and_docstring=True,
    )
    DeviceProxy.is_telemetry_enabled = green(
        _trace_client(__DeviceProxy__is_telemetry_enabled),
        update_signature_and_docstring=True,
    )
    DeviceProxy.set_telemetry_topics = green(
        _trace_client(__DeviceProxy__set_telemetry_topics),
        update_signature_and_docstring=True,
    )
    DeviceProxy.get_telemetry_topics = green(
        _trace_client(__DeviceProxy__get_telemetry_topics),
        update_signature_and_docstring=True,
    )

    DeviceProxy.__get_event_map = __DeviceProxy__get_event_map
    DeviceProxy.__get_event_map_lock = __DeviceProxy__get_event_map_lock

    DeviceProxy.subscribe_event = green(
        _trace_client(__DeviceProxy__subscribe_event),
        consume_green_mode=False,
        update_signature_and_docstring=True,
    )
    DeviceProxy.unsubscribe_event = green(
        _trace_client(__DeviceProxy__unsubscribe_event),
        update_signature_and_docstring=True,
    )
    DeviceProxy.get_events = _trace_client(__DeviceProxy__get_events)
    DeviceProxy.__unsubscribe_event_all = __DeviceProxy__unsubscribe_event_all

    DeviceProxy.__str__ = __DeviceProxy__str
    DeviceProxy.__repr__ = __DeviceProxy__str
    DeviceProxy._get_info_ = __DeviceProxy___get_info_

    DeviceProxy.__getattr__ = __safe_call(__DeviceProxy__getattr)
    DeviceProxy.__setattr__ = __safe_call(__DeviceProxy__setattr)
    DeviceProxy.__getitem__ = __safe_call(__DeviceProxy__getitem)
    DeviceProxy.__setitem__ = __safe_call(__DeviceProxy__setitem)
    DeviceProxy.__contains__ = __safe_call(__DeviceProxy__contains)
    DeviceProxy.__dir__ = __safe_call(__DeviceProxy__dir)
