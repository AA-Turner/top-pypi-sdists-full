# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Define python methods for DeviceProxy object."""

import time
import textwrap
import threading
import enum
import collections.abc
import warnings

try:
    from warnings import deprecated
except ImportError:
    from typing_extensions import deprecated

from tango.utils import PyTangoUserWarning

from tango._tango import StdStringVector, DbData, DbDatum, AttributeInfo
from tango._tango import AttributeInfoEx, AttributeInfoList, AttributeInfoListEx
from tango._tango import DeviceProxy, __CallBackAutoDie, __CallBackPushEvent
from tango._tango import EventType, DevFailed, Except, ExtractAs, GreenMode
from tango._tango import PipeInfo, PipeInfoList, constants
from tango._tango import CmdArgType, DevState

from tango.utils import TO_TANGO_TYPE, scalar_to_array_type
from tango.utils import is_pure_str, is_non_str_seq, is_integer, is_number
from tango.utils import seq_2_StdStringVector, StdStringVector_2_seq
from tango.utils import DbData_2_dict, obj_2_property
from tango.utils import document_method as __document_method
from tango.utils import dir2
from tango.utils import ensure_binary
from tango.utils import _get_device_fqtrl_if_necessary
from tango.utils import _trace_client

from tango.green import green, green_callback
from tango.green import get_green_mode

__all__ = ("device_proxy_init", "get_device_proxy")

__docformat__ = "restructuredtext"

_UNSUBSCRIBE_LIFETIME = 60


@green(consume_green_mode=False)
def get_device_proxy(*args, **kwargs):
    """get_device_proxy(self, dev_name, green_mode=None, wait=True, timeout=True) -> DeviceProxy
    get_device_proxy(self, dev_name, need_check_acc, green_mode=None, wait=True, timeout=None) -> DeviceProxy

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
    :type dev_name: str
    :param need_check_acc: in first version of the function it defaults to True.
                           Determines if at creation time of DeviceProxy it should check
                           for channel access (rarely used)
    :type need_check_acc: bool
    :param green_mode: determines the mode of execution of the device (including
                      the way it is created). Defaults to the current global
                      green_mode (check :func:`~tango.get_green_mode` and
                      :func:`~tango.set_green_mode`)
    :type green_mode: :obj:`~tango.GreenMode`
    :param wait: whether or not to wait for result. If green_mode
                 Ignored when green_mode is Synchronous (always waits).
    :type wait: bool
    :param timeout: The number of seconds to wait for the result.
                    If None, then there is no limit on the wait time.
                    Ignored when green_mode is Synchronous or wait is False.
    :type timeout: float
    :returns:
        if green_mode is Synchronous or wait is True:
            :class:`~tango.DeviceProxy`
        else if green_mode is Futures:
            :class:`concurrent.futures.Future`
        else if green_mode is Gevent:
            :class:`gevent.event.AsynchResult`
        else if green_mode is Asyncio:
            :class:`asyncio.Future`
    :throws:
        * a *DevFailed* if green_mode is Synchronous or wait is True
          and there is an error creating the device.
        * a *concurrent.futures.TimeoutError* if green_mode is Futures,
          wait is False, timeout is not None and the time to create the device
          has expired.
        * a *gevent.timeout.Timeout* if green_mode is Gevent, wait is False,
          timeout is not None and the time to create the device has expired.
        * a *asyncio.TimeoutError* if green_mode is Asyncio,
          wait is False, timeout is not None and the time to create the device
          has expired.

    New in PyTango 8.1.0
    """
    return DeviceProxy(*args, **kwargs)


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


def __check_read_pipe(dev_pipe):
    if dev_pipe.has_failed:
        raise DevFailed(*dev_pipe.get_err_stack())
    return dev_pipe


def __init_device_proxy_internals(proxy):
    if proxy.__dict__.get("_initialized", False):
        return
    executors = {key: None for key in GreenMode.names}
    proxy.__dict__["_green_mode"] = None
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


def __DeviceProxy__get_pipe_cache(self):
    try:
        ret = self.__dict__["__pipe_cache"]
    except KeyError:
        self.__dict__["__pipe_cache"] = ret = ()
    return ret


def __DeviceProxy____init__(self, *args, **kwargs):
    __init_device_proxy_internals(self)
    bypass___setattr = self.__dict__
    bypass___setattr["_green_mode"] = kwargs.pop("green_mode", None)
    bypass___setattr["_executors"][GreenMode.Futures] = kwargs.pop("executor", None)
    bypass___setattr["_executors"][GreenMode.Gevent] = kwargs.pop("threadpool", None)
    bypass___setattr["_executors"][GreenMode.Asyncio] = kwargs.pop(
        "asyncio_executor", None
    )

    # If TestContext active, short TRL is replaced with fully-qualified
    # TRL, using test server's connection details.  Otherwise, left as-is.
    device_name = args[0]
    new_device_name = _get_device_fqtrl_if_necessary(device_name)
    new_args = [new_device_name] + list(args[1:])
    try:
        return DeviceProxy.__init_orig__(self, *new_args, **kwargs)
    except DevFailed as orig_err:
        if new_device_name != device_name:
            # If device was not found, it could be an attempt to access a real device
            # with short name while running TestContext.  I.e., we need to use the
            # short name so that the real TANGO_HOST will be tried.
            try:
                return DeviceProxy.__init_orig__(self, *args, **kwargs)
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


def __DeviceProxy__get_green_mode(self):
    """Returns the green mode in use by this DeviceProxy.

    :returns: the green mode in use by this DeviceProxy.
    :rtype: GreenMode

    .. seealso::
        :func:`tango.get_green_mode`
        :func:`tango.set_green_mode`

    New in PyTango 8.1.0
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

    New in PyTango 8.1.0
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
    attr_list = self.attribute_list_query_ex()
    attr_cache = {}
    for attr in attr_list:
        name = attr.name.lower()
        enum_class = None
        if attr.data_type == CmdArgType.DevEnum and attr.enum_labels:
            labels = StdStringVector_2_seq(attr.enum_labels)
            enum_class = enum.IntEnum(attr.name, labels, start=0)
        elif attr.data_type == CmdArgType.DevState:
            enum_class = DevState
        attr_cache[name] = (
            attr.name,
            enum_class,
        )
    self.__dict__["__attr_cache"] = attr_cache


def __DeviceProxy__refresh_pipe_cache(self):
    pipe_cache = [pipe_name.lower() for pipe_name in self._get_pipe_list()]
    self.__dict__["__pipe_cache"] = pipe_cache


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


def __get_command_func(dp, cmd_info, name):
    _, doc = cmd_info

    def f(*args, **kwds):
        return dp.command_inout(name, *args, **kwds)

    f.__doc__ = doc
    return f


def __update_enum_values(attr_info, attr_value):
    _, enum_class = attr_info
    if enum_class and attr_value is not None:
        if is_non_str_seq(attr_value):
            ret = []
            for value in attr_value:
                if is_non_str_seq(value):
                    ret.append(tuple([enum_class(v) for v in value]))
                else:
                    ret.append(enum_class(value))
            return tuple(ret)

        return enum_class(attr_value)
    else:
        return attr_value


async def __async_get_attribute_value(self, attr_info, name):
    attr_value = await self.read_attribute(name)
    return __update_enum_values(attr_info, attr_value.value)


def __sync_get_attribute_value(self, attr_info, name):
    attr_value = self.read_attribute(name).value
    return __update_enum_values(attr_info, attr_value)


def __get_attribute_value(self, attr_info, name):
    if self.get_green_mode() == GreenMode.Asyncio:
        return __async_get_attribute_value(self, attr_info, name)
    else:
        return __sync_get_attribute_value(self, attr_info, name)


def __convert_str_to_enum(value, enum_class, attr_name):
    try:
        return enum_class[value]
    except KeyError:
        raise AttributeError(
            f"Invalid enum value {value} for attribute {attr_name} "
            f"Valid values: {[m for m in enum_class.__members__.keys()]}"
        )


def __set_attribute_value(self, name, value):
    attr_info = self.__get_attr_cache().get(name.lower())
    if attr_info:
        # allow writing DevEnum attributes using string values
        _, enum_class = attr_info
        if enum_class:
            if is_non_str_seq(value):
                org_value = value
                value = []
                for val in org_value:
                    if is_non_str_seq(val):
                        value.append(
                            [
                                (
                                    __convert_str_to_enum(v, enum_class, name)
                                    if is_pure_str(v)
                                    else v
                                )
                                for v in val
                            ]
                        )
                    else:
                        value.append(
                            __convert_str_to_enum(val, enum_class, name)
                            if is_pure_str(val)
                            else val
                        )
            elif is_pure_str(value):
                value = __convert_str_to_enum(value, enum_class, name)
    return self.write_attribute(name, value)


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

        attr_info = self.__get_attr_cache().get(name_l)
        if attr_info:
            return __get_attribute_value(self, attr_info, name)

        if name_l in self.__get_pipe_cache():
            return self.read_pipe(name)

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

        attr_info = self.__get_attr_cache().get(name_l)
        if attr_info:
            return __get_attribute_value(self, attr_info, name)

        try:
            self.__refresh_pipe_cache()
        except Exception as e:
            if cause is None:
                cause = e

        if name_l in self.__get_pipe_cache():
            return self.read_pipe(name)

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

        if name_l in self.__get_pipe_cache():
            return self.write_pipe(name, value)

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
            self.__refresh_pipe_cache()
        except Exception as e:
            if cause is None:
                cause = e

        if name_l in self.__get_pipe_cache():
            return self.write_pipe(name, value)

        try:
            if name in self.__dict__ or not self.is_dynamic_interface_frozen():
                return super(DeviceProxy, self).__setattr__(name, value)
            else:
                raise AttributeError(
                    f"Tried to set non-existent attr {repr(name)} to {repr(value)}.\n"
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
    try:
        extra_entries.update(self.get_command_list())
    except Exception:
        pass
    # Add attributes
    try:
        extra_entries.update(self.get_attribute_list())
    except Exception:
        pass
    # Add pipes
    try:
        extra_entries.update(self._get_pipe_list())
    except Exception:
        pass
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


def __DeviceProxy__read_attribute(self, value, extract_as=ExtractAs.Numpy):
    return __check_read_attribute(self._read_attribute(value, extract_as))


def __read_attributes_asynch__(self, attr_names, cb, extract_as):
    if cb is None:
        return self.__read_attributes_asynch(attr_names)

    cb2 = __CallBackAutoDie()
    if isinstance(cb, collections.abc.Callable):
        cb2.attr_read = cb
    else:
        cb2.attr_read = cb.attr_read
    return self.__read_attributes_asynch(attr_names, cb2, extract_as)


def __DeviceProxy__read_attributes_asynch(
    self, attr_names, cb=None, extract_as=ExtractAs.Numpy
):
    """
    read_attributes_asynch(self, attr_names, green_mode=None, wait=True, timeout=None) -> int
    read_attributes_asynch(self, attr_names, cb, extract_as=Numpy, green_mode=None, wait=True, timeout=None) -> None

        Read asynchronously an attribute list.

        New in PyTango 7.0.0

    .. important::
        by default, TANGO is initialized with the **polling** model. If you want
        to use the **push** model (the one with the callback parameter), you
        need to change the global TANGO model to PUSH_CALLBACK.
        You can do this with the :meth:`tango.ApiUtil.set_asynch_cb_sub_model`

    :param attr_names: A list of attributes to read. See read_attributes.
    :type attr_names: Sequence[str]

    :param cb: push model: as soon as attributes read, core calls cb with read results.
        This callback object should be an instance of a user class with an attr_read() method.
        It can also be any callable object.
    :type cb: Optional[Callable]

    :param extract_as: Defaults to numpy.
    :type extract_as: ExtractAs

    :param green_mode: Defaults to the current DeviceProxy GreenMode.
            (see :meth:`~tango.DeviceProxy.get_green_mode`
            and :meth:`~tango.DeviceProxy.set_green_mode`).
    :type green_mode: GreenMode

    :param wait: whether to wait for result. If green_mode
                 is *Synchronous*, this parameter is ignored as it always
                 waits for the result.
    :type wait: bool

    :param timeout: The number of seconds to wait for the result.
        If None, then there is no limit on the wait time.
        Ignored when green_mode is Synchronous or wait is False.
    :type timeout: float

    :returns: an asynchronous call identifier which is needed to get attributes value if poll model, None if push model
    :rtype: Union[int, None]

    :throws: ConnectionFailed

    .. important::
        Multiple asynchronous calls are not guaranteed to be executed by the device
        server in the same order they are invoked by the client.  E.g., a call
        to ``write_attributes_asynch([("a", 1)])`` followed immediately with a call to
        ``read_attributes_asynch(["a"])`` could result in the device reading the
        attribute ``a`` before writing to it.
    """

    return __read_attributes_asynch__(self, attr_names, cb, extract_as)


def __DeviceProxy__read_attribute_asynch(
    self, attr_name, cb=None, extract_as=ExtractAs.Numpy
):
    """
    read_attribute_asynch(self, attr_name, green_mode=None, wait=True, timeout=None) -> int
    read_attribute_asynch(self, attr_name, cb, extract_as=Numpy, green_mode=None, wait=True, timeout=None) -> None

        Read asynchronously the specified attributes.

        New in PyTango 7.0.0

    .. important::
        by default, TANGO is initialized with the **polling** model. If you want
        to use the **push** model (the one with the callback parameter), you
        need to change the global TANGO model to PUSH_CALLBACK.
        You can do this with the :meth:`tango.ApiUtil.set_asynch_cb_sub_model`

    :param attr_name: an attribute to read
    :type attr_name: str

    :param cb: push model: as soon as attributes read, core calls cb with read results.
        This callback object should be an instance of a user class with an attr_read() method.
        It can also be any callable object.
    :type cb: Optional[Callable]

    :param extract_as: Defaults to numpy.
    :type extract_as: ExtractAs

    :param green_mode: Defaults to the current DeviceProxy GreenMode.
        (see :meth:`~tango.DeviceProxy.get_green_mode`
        and :meth:`~tango.DeviceProxy.set_green_mode`).
    :type green_mode: GreenMode

    :param wait: whether to wait for result. If green_mode
         is *Synchronous*, this parameter is ignored as it always
         waits for the result.
    :type wait: bool

    :param timeout: The number of seconds to wait for the result.
        If None, then there is no limit on the wait time. Ignored when green_mode is Synchronous or wait is False.
    :type timeout: float

    :returns: an asynchronous call identifier which is needed to get attribute value if poll model, None if push model
    :rtype: Union[int, None]

    :throws: ConnectionFailed

    .. important::
        Multiple asynchronous calls are not guaranteed to be executed by the device
        server in the same order they are invoked by the client.  E.g., a call
        to the method ``write_attribute_asynch("a", 1)`` followed immediately with
        a call to ``read_attribute_asynch("a")`` could result in the device reading the
        attribute ``a`` before writing to it.
    """
    return __read_attributes_asynch__(self, [attr_name], cb, extract_as)


def __read_attributes_reply__(self, *args, **kwargs):
    if "poll_timeout" in kwargs:
        kwargs["timeout"] = kwargs.pop("poll_timeout")

    return self.__read_attributes_reply(*args, **kwargs)


def __DeviceProxy__read_attributes_reply(self, *args, **kwargs):
    """
    read_attributes_reply(self, id, extract_as=ExtractAs.Numpy, green_mode=None, wait=True) -> [DeviceAttribute]
    read_attributes_reply(self, id, poll_timeout, extract_as=ExtractAs.Numpy, green_mode=None, wait=True) -> [DeviceAttribute]

    Get the answer of an asynchronous read_attributes call, if it has arrived (polling model).

    If the reply is ready, but an attribute raised an exception while reading, it will
    still be included in the returned list.  However, the has_error field for that item
    will be set to True.

    .. versionchanged:: 7.0.0 New in PyTango
    .. versionchanged:: 10.0.0 To eliminate confusion between different timeout parameters, the core (cppTango) timeout (previously the optional second positional argument) has been renamed to "poll_timeout". Conversely, the pyTango executor timeout remains as the keyword argument "timeout". These parameters have distinct meanings and units:

        - The cppTango "poll_timeout" is measured in milliseconds and blocks the call until a reply is received. If the reply is not received within the specified poll_timeout duration, an exception is thrown. Setting poll_timeout to 0 causes the call to wait indefinitely until a reply is received.
        - The pyTango "timeout" is measured in seconds and is applicable only in asynchronous GreenModes (Asyncio, Futures, Gevent), and only when "wait" is set to True. The specific behavior when a reply is not received within the specified timeout period varies depending on the GreenMode.


    :param id: the asynchronous call identifier
    :type id: int

    :param poll_timeout: cppTango core timeout in ms.
        If the reply has not yet arrived, the call will wait for the time specified (in ms).
        If after timeout, the reply is still not there, an exception is thrown.
        If timeout set to 0, the call waits until the reply arrives.
        If the argument is not provided, then there is no timeout check, and an
        exception is raised immediately if the reply is not ready.
    :type poll_timeout: Optional[int]

    :param extract_as: Defaults to numpy.
    :type extract_as: ExtractAs

    :param green_mode: Defaults to the current DeviceProxy GreenMode.
        (see :meth:`~tango.DeviceProxy.get_green_mode`
        and :meth:`~tango.DeviceProxy.set_green_mode`).
    :type green_mode: GreenMode

    :param wait: whether to wait for result. If green_mode
         is *Synchronous*, this parameter is ignored as it always
         waits for the result.
    :type wait: bool

    :param timeout: pytango green executor timout. The number of seconds to wait for the result.
        If None, then there is no limit on the wait time. Ignored when green_mode is Synchronous or wait is False.
    :type timeout: float

    :returns: If the reply is arrived and if it is a valid reply,
        it is returned to the caller in a list of DeviceAttribute.
        If the reply is an exception, it is re-thrown by this call.
        If the reply is not yet arrived, the call will wait (blocking the process)
        for the time specified in timeout. If after timeout milliseconds, the reply is still not there, an
        exception is thrown. If timeout is set to 0, the call waits
        until the reply arrived.
    :rtype: Sequence[DeviceAttribute]

    :throws: Union[AsynCall, AsynReplyNotArrived, ConnectionFailed, CommunicationFailed, DevFailed]

    """

    return __read_attributes_reply__(self, *args, **kwargs)


def __DeviceProxy__read_attribute_reply(self, *args, **kwargs):
    """
    read_attribute_reply(self, id, extract_as=ExtractAs.Numpy, green_mode=None, wait=True) -> DeviceAttribute
    read_attribute_reply(self, id, poll_timeout, extract_as=ExtractAs.Numpy, green_mode=None, wait=True) -> DeviceAttribute

    Get the answer of an asynchronous read_attribute call, if it has arrived (polling model).

    If the reply is ready, but the attribute raised an exception while reading, an
    exception will be raised by this function (DevFailed, with reason API_AttrValueNotSet).

    .. versionchanged:: 7.0.0 New in PyTango
    .. versionchanged:: 10.0.0 To eliminate confusion between different timeout parameters, the core (cppTango) timeout (previously the optional second positional argument) has been renamed to "poll_timeout". Conversely, the pyTango executor timeout remains as the keyword argument "timeout". These parameters have distinct meanings and units:

        - The cppTango "poll_timeout" is measured in milliseconds and blocks the call until a reply is received. If the reply is not received within the specified poll_timeout duration, an exception is thrown. Setting poll_timeout to 0 causes the call to wait indefinitely until a reply is received.
        - The pyTango "timeout" is measured in seconds and is applicable only in asynchronous GreenModes (Asyncio, Futures, Gevent), and only when "wait" is set to True. The specific behavior when a reply is not received within the specified timeout period varies depending on the GreenMode.


    :param id: the asynchronous call identifier
    :type id: int

    :param poll_timeout: cppTango core timeout in ms.
        If the reply has not yet arrived, the call will wait for the time specified (in ms).
        If after timeout, the reply is still not there, an exception is thrown.
        If timeout set to 0, the call waits until the reply arrives.
        If the argument is not provided, then there is no timeout check, and an
        exception is raised immediately if the reply is not ready.
    :type poll_timeout: Optional[int]

    :param extract_as: Defaults to numpy.
    :type extract_as: ExtractAs

    :param green_mode: Defaults to the current DeviceProxy GreenMode.
        (see :meth:`~tango.DeviceProxy.get_green_mode`
        and :meth:`~tango.DeviceProxy.set_green_mode`).
    :type green_mode: GreenMode

    :param wait: whether to wait for result. If green_mode
         is *Synchronous*, this parameter is ignored as it always
         waits for the result.
    :type wait: bool

    :param timeout: pytango green executor timout. The number of seconds to wait for the result.
        If None, then there is no limit on the wait time. Ignored when green_mode is Synchronous or wait is False.
    :type timeout: float

    :returns: If the reply is arrived and if it is a valid reply,
        it is returned to the caller in a list of DeviceAttribute.
        If the reply is an exception, it is re-thrown by this call.
        If the reply is not yet arrived, the call will wait (blocking the process)
        for the time specified in timeout. If after timeout milliseconds, the reply is still not there, an
        exception is thrown. If timeout is set to 0, the call waits
        until the reply arrived.
    :rtype: DeviceAttribute

    :throws: Union[AsynCall, AsynReplyNotArrived, ConnectionFailed, CommunicationFailed, DevFailed]

    """
    attr = __read_attributes_reply__(self, *args, **kwargs)[0]
    return __check_read_attribute(attr)


def __write_attributes_asynch__(self, attr_values, cb=None):
    if cb is None:
        return self.__write_attributes_asynch(attr_values)

    cb2 = __CallBackAutoDie()
    if isinstance(cb, collections.abc.Callable):
        cb2.attr_written = cb
    else:
        cb2.attr_written = cb.attr_written
    return self.__write_attributes_asynch(attr_values, cb2)


def __DeviceProxy__write_attributes_asynch(self, attr_values, cb=None):
    """
    write_attributes_asynch(self, values, green_mode=None, wait=True, timeout=None) -> int
    write_attributes_asynch(self, values, cb, green_mode=None, wait=True, timeout=None) -> None

            Write asynchronously the specified attributes.

    .. important::
        by default, TANGO is initialized with the **polling** model. If you want
        to use the **push** model (the one with the callback parameter), you
        need to change the global TANGO model to PUSH_CALLBACK.
        You can do this with the :meth:`tango.ApiUtil.set_asynch_cb_sub_model`

    :param values: attributes to write
    :type values: Sequence[Sequence[str, Any]]

    :param cb: push model: as soon as attributes written, core calls cb with write results.
        This callback object should be an instance of a user class with an attr_written() method.
        It can also be any callable object.
    :type cb: Optional[Callable]

    :param green_mode: Defaults to the current DeviceProxy GreenMode.
        (see :meth:`~tango.DeviceProxy.get_green_mode`
        and :meth:`~tango.DeviceProxy.set_green_mode`).
    :type green_mode: GreenMode

    :param wait: whether to wait for result. If green_mode
         is *Synchronous*, this parameter is ignored as it always
         waits for the result.
    :type wait: bool

    :param timeout: The number of seconds to wait for the result.
        If None, then there is no limit on the wait time. Ignored when green_mode is Synchronous or wait is False.
    :type timeout: float

    :returns: an asynchronous call identifier which is needed to get the server reply if poll model, None if push model
    :rtype: Union[int, None]

    :throws: ConnectionFailed

    .. important::
        Multiple asynchronous calls are not guaranteed to be executed by the device
        server in the same order they are invoked by the client.  E.g., a call
        to ``write_attributes_asynch([("a", 1)])`` followed immediately with a call to
        ``read_attributes_asynch(["a"])`` could result in the device reading the
        attribute ``a`` before writing to it.
    """

    return __write_attributes_asynch__(self, attr_values, cb)


def __DeviceProxy__write_attribute_asynch(self, attr_name, value, cb=None, **kwargs):
    """
    write_attributes_asynch(self, attr_name, value, green_mode=None, wait=True, timeout=None) -> int
    write_attributes_asynch(self, attr_name, value, cb, green_mode=None, wait=True, timeout=None) -> None

        Write asynchronously the specified attribute.

    .. important::
        by default, TANGO is initialized with the **polling** model. If you want
        to use the **push** model (the one with the callback parameter), you
        need to change the global TANGO model to PUSH_CALLBACK.
        You can do this with the :meth:`tango.ApiUtil.set_asynch_cb_sub_model`

    :param attr_name: an attribute to write
    :type attr_name: str

    :param value: value to write
    :type value: Any

    :param cb: push model: as soon as attribute written, core calls cb with write results.
        This callback object should be an instance of a user class with an attr_written() method.
        It can also be any callable object.
    :type cb: Optional[Callable]

    :param green_mode: Defaults to the current DeviceProxy GreenMode.
        (see :meth:`~tango.DeviceProxy.get_green_mode`
        and :meth:`~tango.DeviceProxy.set_green_mode`).
    :type green_mode: GreenMode

    :param wait: whether to wait for result. If green_mode
         is *Synchronous*, this parameter is ignored as it always
         waits for the result.
    :type wait: bool

    :param timeout: The number of seconds to wait for the result.
        If None, then there is no limit on the wait time. Ignored when green_mode is Synchronous or wait is False.
    :type timeout: float

    :returns: an asynchronous call identifier which is needed to get the server reply if poll model, None if push model
    :rtype: Union[int, None]

    :throws: ConnectionFailed

    .. important::
        Multiple asynchronous calls are not guaranteed to be executed by the device
        server in the same order they are invoked by the client.  E.g., a call
        to the method ``write_attribute_asynch("a", 1)`` followed immediately with
        a call to ``read_attribute_asynch("a")`` could result in the device reading the
        attribute ``a`` before writing to it.
    """
    return __write_attributes_asynch__(self, [(attr_name, value)], cb)


def __write_attributes_reply__(self, *args, **kwargs):
    if "poll_timeout" in kwargs:
        kwargs["timeout"] = kwargs.pop("poll_timeout")

    return self.__write_attributes_reply(*args, **kwargs)


def __DeviceProxy__write_attributes_reply(self, *args, **kwargs):
    """

    write_attributes_reply(self, id, green_mode=None, wait=True) -> None
    write_attributes_reply(self, id, poll_timeout, green_mode=None, wait=True) -> None

        Check if the answer of an asynchronous write_attributes is arrived
        (polling model). If the reply is arrived and if it is a valid reply,
        the call returned. If the reply is an exception, it is re-thrown by
        this call. An exception is also thrown in case of the reply is not
        yet arrived.

    .. versionchanged:: 7.0.0 New in PyTango
    .. versionchanged:: 10.0.0 To eliminate confusion between different timeout parameters, the core (cppTango) timeout (previously the optional second positional argument) has been renamed to "poll_timeout". Conversely, the pyTango executor timeout remains as the keyword argument "timeout". These parameters have distinct meanings and units:

        - The cppTango "poll_timeout" is measured in milliseconds and blocks the call until a reply is received. If the reply is not received within the specified poll_timeout duration, an exception is thrown. Setting poll_timeout to 0 causes the call to wait indefinitely until a reply is received.
        - The pyTango "timeout" is measured in seconds and is applicable only in asynchronous GreenModes (Asyncio, Futures, Gevent), and only when "wait" is set to True. The specific behavior when a reply is not received within the specified timeout period varies depending on the GreenMode.

    :param id: the asynchronous call identifier
    :type id: int

    :param poll_timeout: cppTango core timeout in ms.
        If the reply has not yet arrived, the call will wait for the time specified (in ms).
        If after timeout, the reply is still not there, an exception is thrown.
        If timeout set to 0, the call waits until the reply arrives.
        If the argument is not provided, then there is no timeout check, and an
        exception is raised immediately if the reply is not ready.
    :type poll_timeout: Optional[int]

    :param extract_as: Defaults to numpy.
    :type extract_as: ExtractAs

    :param green_mode: Defaults to the current DeviceProxy GreenMode.
        (see :meth:`~tango.DeviceProxy.get_green_mode`
        and :meth:`~tango.DeviceProxy.set_green_mode`).
    :type green_mode: GreenMode

    :param wait: whether to wait for result. If green_mode
         is *Synchronous*, this parameter is ignored as it always
         waits for the result.
    :type wait: bool

    :param timeout: pytango green executor timout. The number of seconds to wait for the result.
        If None, then there is no limit on the wait time. Ignored when green_mode is Synchronous or wait is False.
    :type timeout: float

    :returns: None
    :rtype: None

    :throws: Union[AsynCall, AsynReplyNotArrived, ConnectionFailed, CommunicationFailed, DevFailed]

    """
    return __write_attributes_reply__(self, *args, **kwargs)


def __DeviceProxy__write_attribute_reply(self, *args, **kwargs):
    """
    write_attribute_reply(self, id, green_mode=None, wait=True) -> None
    write_attribute_reply(self, id, poll_timeout, green_mode=None, wait=True) -> None

        Check if the answer of an asynchronous write_attributes is arrived
        (polling model). If the reply is arrived and if it is a valid reply,
        the call returned. If the reply is an exception, it is re-thrown by
        this call. An exception is also thrown in case of the reply is not
        yet arrived.

    .. versionchanged:: 7.0.0 New in PyTango
    .. versionchanged:: 10.0.0 To eliminate confusion between different timeout parameters, the core (cppTango) timeout (previously the optional second positional argument) has been renamed to "poll_timeout". Conversely, the pyTango executor timeout remains as the keyword argument "timeout". These parameters have distinct meanings and units:

        - The cppTango "poll_timeout" is measured in milliseconds and blocks the call until a reply is received. If the reply is not received within the specified poll_timeout duration, an exception is thrown. Setting poll_timeout to 0 causes the call to wait indefinitely until a reply is received.
        - The pyTango "timeout" is measured in seconds and is applicable only in asynchronous GreenModes (Asyncio, Futures, Gevent), and only when "wait" is set to True. The specific behavior when a reply is not received within the specified timeout period varies depending on the GreenMode.

    :param id: the asynchronous call identifier
    :type id: int

    :param poll_timeout: cppTango core timeout in ms.
        If the reply has not yet arrived, the call will wait for the time specified (in ms).
        If after timeout, the reply is still not there, an exception is thrown.
        If timeout set to 0, the call waits until the reply arrives.
        If the argument is not provided, then there is no timeout check, and an
        exception is raised immediately if the reply is not ready.
    :type poll_timeout: Optional[int]

    :param extract_as: Defaults to numpy.
    :type extract_as: ExtractAs

    :param green_mode: Defaults to the current DeviceProxy GreenMode.
        (see :meth:`~tango.DeviceProxy.get_green_mode`
        and :meth:`~tango.DeviceProxy.set_green_mode`).
    :type green_mode: GreenMode

    :param wait: whether to wait for result. If green_mode
         is *Synchronous*, this parameter is ignored as it always
         waits for the result.
    :type wait: bool

    :param timeout: pytango green executor timout. The number of seconds to wait for the result.
        If None, then there is no limit on the wait time. Ignored when green_mode is Synchronous or wait is False.
    :type timeout: float

    :returns: None
    :rtype: None

    :throws: Union[AsynCall, AsynReplyNotArrived, ConnectionFailed, CommunicationFailed, DevFailed]
    """
    return __write_attributes_reply__(self, *args, **kwargs)


def __DeviceProxy__write_read_attribute(
    self, attr_name, value, extract_as=ExtractAs.Numpy
):
    result = self._write_read_attribute(attr_name, value, extract_as)
    return __check_read_attribute(result)


def __DeviceProxy__write_read_attributes(
    self, name_val, attr_read_names, extract_as=ExtractAs.Numpy
):
    return self._write_read_attributes(name_val, attr_read_names, extract_as)


def __DeviceProxy__get_property(self, propname, value=None):
    """
    get_property(self, propname, value=None, green_mode=None, wait=True, timeout=None) -> tango.DbData

        Get a (list) property(ies) for a device.

        This method accepts the following types as propname parameter:
        1. string [in] - single property data to be fetched
        2. sequence<string> [in] - several property data to be fetched
        3. tango.DbDatum [in] - single property data to be fetched
        4. tango.DbData [in,out] - several property data to be fetched.
        5. sequence<DbDatum> - several property data to be feteched

        Note: for cases 3, 4 and 5 the 'value' parameter if given, is IGNORED.

        If value is given it must be a tango.DbData that will be filled with the
        property values

    :param propname: Property(ies) name(s).
    :type propname: any
    :param value: Optional. The default is `None`, meaning that the method will create internally a `tango.DbData` and return it filled with the property values.
    :type value: DbData, optional
    :param green_mode: Defaults to the current `DeviceProxy` GreenMode. See `tango.DeviceProxy.get_green_mode` and `tango.DeviceProxy.set_green_mode`.
    :type green_mode: GreenMode
    :param wait: Whether to wait for result. If `green_mode` is *Synchronous*, this parameter is ignored as it always waits for the result. Ignored when `green_mode` is Synchronous (always waits).
    :type wait: bool
    :param timeout: The number of seconds to wait for the result. If `None`, then there is no limit on the wait time. Ignored when `green_mode` is Synchronous or `wait` is False.
    :type timeout: float, optional

    :returns: A `DbData` object containing the property(ies) value(s). If a `tango.DbData` is given as a parameter, it returns the same object; otherwise, a new `tango.DbData` is returned.
    :rtype: DbData

    :raises NonDbDevice: Raised in case of a non-database device error.
    :raises ConnectionFailed: Raised on connection failure with the database.
    :raises CommunicationFailed: Raised on communication failure with the database.
    :raises DevFailed: Raised on a device failure from the database device.`
    """

    if is_pure_str(propname) or isinstance(propname, StdStringVector):
        new_value = value
        if new_value is None:
            new_value = DbData()
        self._get_property(propname, new_value)
        return DbData_2_dict(new_value)
    elif isinstance(propname, DbDatum):
        new_value = DbData()
        new_value.append(propname)
        self._get_property(new_value)
        return DbData_2_dict(new_value)
    elif isinstance(propname, collections.abc.Sequence):
        if isinstance(propname, DbData):
            self._get_property(propname)
            return DbData_2_dict(propname)

        if is_pure_str(propname[0]):
            new_propname = StdStringVector()
            for i in propname:
                new_propname.append(i)
            new_value = value
            if new_value is None:
                new_value = DbData()
            self._get_property(new_propname, new_value)
            return DbData_2_dict(new_value)
        elif isinstance(propname[0], DbDatum):
            new_value = DbData()
            for i in propname:
                new_value.append(i)
            self._get_property(new_value)
            return DbData_2_dict(new_value)


def __DeviceProxy__put_property(self, value):
    """
    put_property(self, value, green_mode=None, wait=True, timeout=None) -> None

            Insert or update a list of properties for this device.
            This method accepts the following types as value parameter:
            1. tango.DbDatum - single property data to be inserted
            2. tango.DbData - several property data to be inserted
            3. sequence<DbDatum> - several property data to be inserted
            4. dict<str, DbDatum> - keys are property names and value has data to be inserted
            5. dict<str, seq<str>> - keys are property names and value has data to be inserted
            6. dict<str, obj> - keys are property names and str(obj) is property value

    :param value: Can be one of the following:
                    1. `tango.DbDatum` - Single property data to be inserted.
                    2. `tango.DbData` - Several property data to be inserted.
                    3. `sequence<DbDatum>` - Several property data to be inserted.
                    4. `dict<str, DbDatum>` - Keys are property names, and value has data to be inserted.
                    5. `dict<str, seq<str>>` - Keys are property names, and value has data to be inserted.
                    6. `dict<str, obj>` - Keys are property names, and `str(obj)` is property value.
    :type value: tango.DbDatum, tango.DbData, sequence<DbDatum>, dict<str, DbDatum>, dict<str, seq<str>>, dict<str, obj>
    :param green_mode: Defaults to the current `DeviceProxy` GreenMode. See `tango.DeviceProxy.get_green_mode` and `tango.DeviceProxy.set_green_mode`.
    :type green_mode: GreenMode
    :param wait: Whether or not to wait for result. If `green_mode` is *Synchronous*, this parameter is ignored as it always waits for the result. Ignored when `green_mode` is Synchronous (always waits).
    :type wait: bool
    :param timeout: The number of seconds to wait for the result. If `None`, then there is no limit on the wait time. Ignored when `green_mode` is Synchronous or `wait` is False.
    :type timeout: float, optional

    :returns: None

    :raises ConnectionFailed: Raised on connection failure.
    :raises CommunicationFailed: Raised on communication failure.
    :raises DevFailed: Raised on a device failure, specifically DB_SQLError.
    """
    value = obj_2_property(value)
    return self._put_property(value)


def __DeviceProxy__delete_property(self, value):
    """
    delete_property(self, value, green_mode=None, wait=True, timeout=None)

            Delete a the given of properties for this device.
            This method accepts the following types as value parameter:

                1. string [in] - single property to be deleted
                2. tango.DbDatum [in] - single property data to be deleted
                3. tango.DbData [in] - several property data to be deleted
                4. sequence<string> [in]- several property data to be deleted
                5. sequence<DbDatum> [in] - several property data to be deleted
                6. dict<str, obj> [in] - keys are property names to be deleted (values are ignored)
                7. dict<str, DbDatum> [in] - several DbDatum.name are property names to be deleted (keys are ignored)

    :param value: Can be one of the following:
                    1. `string` [in] - Single property data to be deleted.
                    2. `tango.DbDatum` [in] - Single property data to be deleted.
                    3. `tango.DbData` [in] - Several property data to be deleted.
                    4. `sequence<string>` [in] - Several property data to be deleted.
                    5. `sequence<DbDatum>` [in] - Several property data to be deleted.
                    6. `dict<str, obj>` [in] - Keys are property names to be deleted (values are ignored).
                    7. `dict<str, DbDatum>` [in] - Several `DbDatum.name` are property names to be deleted (keys are ignored).
    :type value: string, tango.DbDatum, tango.DbData, sequence<string>, sequence<DbDatum>, dict<str, obj>, dict<str, DbDatum>
    :param green_mode: Defaults to the current `DeviceProxy` GreenMode. Refer to `tango.DeviceProxy.get_green_mode` and `tango.DeviceProxy.set_green_mode` for more details.
    :type green_mode: GreenMode
    :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
    :type wait: bool
    :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
    :type timeout: float, optional

    :returns: None

    :raises ConnectionFailed: Raised in case of a connection failure.
    :raises CommunicationFailed: Raised in case of a communication failure.
    :raises DevFailed: Raised in case of a device failure, specifically DB_SQLError.
    :raises TypeError: Raised in case of an incorrect type of input arguments.
    """
    if (
        isinstance(value, DbData)
        or isinstance(value, StdStringVector)
        or is_pure_str(value)
    ):
        new_value = value
    elif isinstance(value, DbDatum):
        new_value = DbData()
        new_value.append(value)
    elif isinstance(value, collections.abc.Sequence):
        new_value = DbData()
        for e in value:
            if isinstance(e, DbDatum):
                new_value.append(e)
            else:
                e = ensure_binary(e, "latin-1")
                new_value.append(DbDatum(e))
    elif isinstance(value, collections.abc.Mapping):
        new_value = DbData()
        for k, v in value.items():
            if isinstance(v, DbDatum):
                new_value.append(v)
            else:
                new_value.append(DbDatum(k))
    else:
        raise TypeError(
            "Value must be a string, tango.DbDatum, "
            "tango.DbData, a sequence or a dictionary"
        )

    return self._delete_property(new_value)


def __DeviceProxy__get_property_list(self, filter, array=None):
    """
    get_property_list(self, filter, array=None, green_mode=None, wait=True, timeout=None) -> obj

            Get the list of property names for the device. The parameter
            filter allows the user to filter the returned name list. The
            wildcard character is '*'. Only one wildcard character is
            allowed in the filter parameter.

    :param filter: The filter wildcard.
    :type filter: str
    :param array: Optional. An array to be filled with the property names. If `None`, a new list will be created internally with the values. Defaults to `None`.
    :type array: sequence obj or None, optional
    :param green_mode: Defaults to the current `DeviceProxy` GreenMode. Refer to `tango.DeviceProxy.get_green_mode` and `tango.DeviceProxy.set_green_mode` for more details.
    :type green_mode: GreenMode
    :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
    :type wait: bool
    :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
    :type timeout: float, optional

    :returns: The given array filled with the property names, or a new list if `array` is `None`.
    :rtype: sequence obj

    :raises NonDbDevice: Raised in case of a non-database device error.
    :raises WrongNameSyntax: Raised in case of incorrect syntax in the name.
    :raises ConnectionFailed: Raised in case of a connection failure with the database.
    :raises CommunicationFailed: Raised in case of a communication failure with the database.
    :raises DevFailed: Raised in case of a device failure from the database device.
    :raises TypeError: Raised in case of an incorrect type of input arguments.

        New in PyTango 7.0.0
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


def __DeviceProxy__get_attribute_config(self, value):
    """
    get_attribute_config(self, name, green_mode=None, wait=True, timeout=None) -> AttributeInfoEx
    get_attribute_config(self, names, green_mode=None, wait=True, timeout=None) -> AttributeInfoList

        Return the attribute configuration for a single or a list of attribute(s). To get all the
        attributes pass a sequence containing the constant tango.constants.AllAttr

        Deprecated: use get_attribute_config_ex instead

    :param name: Attribute name.
    :type name: str
    :param names: Attribute names.
    :type names: sequence(str)
    :param green_mode: Defaults to the current `DeviceProxy` GreenMode. See `tango.DeviceProxy.get_green_mode` and `tango.DeviceProxy.set_green_mode` for more details.
    :type green_mode: GreenMode
    :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
    :type wait: bool
    :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
    :type timeout: float, optional

    :returns: An `AttributeInfoEx` or `AttributeInfoList` object containing the attribute(s) information.
    :rtype: Union[AttributeInfoEx, AttributeInfoList]

    :raises ConnectionFailed: Raised in case of a connection failure.
    :raises CommunicationFailed: Raised in case of a communication failure.
    :raises DevFailed: Raised in case of a device failure.
    :raises TypeError: Raised in case of an incorrect type of input arguments.

    """
    if isinstance(value, StdStringVector) or is_pure_str(value):
        return self._get_attribute_config(value)
    elif isinstance(value, collections.abc.Sequence):
        v = seq_2_StdStringVector(value)
        return self._get_attribute_config(v)

    raise TypeError("value must be a string or a sequence<string>")


def __DeviceProxy__get_attribute_config_ex(self, value):
    """
    get_attribute_config_ex(self, name or sequence(names), green_mode=None, wait=True, timeout=None) -> AttributeInfoListEx :

        Return the extended attribute configuration for a single attribute or for the list of
        specified attributes. To get all the attributes pass a sequence
        containing the constant tango.constants.AllAttr.

    :param name: Attribute name or attribute names. Can be a single string (for one attribute) or a sequence of strings (for multiple attributes).
    :type name: str or sequence(str)
    :param green_mode: Defaults to the current `DeviceProxy` GreenMode. Refer to `tango.DeviceProxy.get_green_mode` and `tango.DeviceProxy.set_green_mode` for more details.
    :type green_mode: GreenMode
    :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
    :type wait: bool
    :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
    :type timeout: float, optional

    :returns: An `AttributeInfoListEx` object containing the attribute information.
    :rtype: AttributeInfoListEx

    :raises ConnectionFailed: Raised in case of a connection failure.
    :raises CommunicationFailed: Raised in case of a communication failure.
    :raises DevFailed: Raised in case of a device failure.
    """
    if isinstance(value, StdStringVector):
        return self._get_attribute_config_ex(value)
    elif is_pure_str(value):
        v = StdStringVector()
        v.append(value)
        return self._get_attribute_config_ex(v)
    elif isinstance(value, collections.abc.Sequence):
        v = seq_2_StdStringVector(value)
        return self._get_attribute_config_ex(v)

    raise TypeError("value must be a string or a sequence<string>")


def __DeviceProxy__get_command_config(self, value=(constants.AllCmd,)):
    """
    get_command_config(self, green_mode=None, wait=True, timeout=None) -> CommandInfoList
    get_command_config(self, name, green_mode=None, wait=True, timeout=None) -> CommandInfo
    get_command_config(self, names) -> CommandInfoList

        Return the command configuration for single/list/all command(s).

    :param name: Command name. Used when querying information for a single command.
    :type name: str, optional
    :param names: Command names. Used when querying information for multiple commands. This parameter should not be used simultaneously with 'name'.
    :type names: sequence<str>, optional
    :param green_mode: Defaults to the current `DeviceProxy` GreenMode. Refer to `tango.DeviceProxy.get_green_mode` and `tango.DeviceProxy.set_green_mode` for more details.
    :type green_mode: GreenMode
    :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
    :type wait: bool
    :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
    :type timeout: float, optional

    :returns: A `CommandInfoList` object containing the commands information if multiple command names are provided, or a `CommandInfo` object if a single command name is provided.
    :rtype: CommandInfoList or CommandInfo

    :raises ConnectionFailed: Raised in case of a connection failure.
    :raises CommunicationFailed: Raised in case of a communication failure.
    :raises DevFailed: Raised in case of a device failure.
    :raises TypeError: Raised in case of an incorrect type of input arguments.
    """
    if isinstance(value, StdStringVector) or is_pure_str(value):
        return self._get_command_config(value)
    elif isinstance(value, collections.abc.Sequence):
        v = seq_2_StdStringVector(value)
        return self._get_command_config(v)

    raise TypeError("value must be a string or a sequence<string>")


@deprecated("get_pipe_config is deprecated - scheduled for removal in PyTango 10.1.0")
def __DeviceProxy__get_pipe_config(self, value=None):
    """
    get_pipe_config(self, green_mode=None, wait=True, timeout=None) -> PipeInfoList
    get_pipe_config(self, name, green_mode=None, wait=True, timeout=None) -> PipeInfo
    get_pipe_config(self, names) -> PipeInfoList

        Return the pipe configuration for single/list/all pipes.

    :param name: Pipe name. Used when querying information for a single pipe.
    :type name: str, optional
    :param names: Pipe names. Used when querying information for multiple pipes. This parameter should not be used simultaneously with 'name'.
    :type names: sequence<str>, optional
    :param green_mode: Defaults to the current `DeviceProxy` GreenMode. Refer to `tango.DeviceProxy.get_green_mode` and `tango.DeviceProxy.set_green_mode` for more details.
    :type green_mode: GreenMode
    :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
    :type wait: bool
    :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
    :type timeout: float, optional

    :returns: A `CommandInfoList` object containing the commands information if multiple command names are provided, or a `CommandInfo` object if a single command name is provided.
    :rtype: CommandInfoList or CommandInfo

    :raises ConnectionFailed: Raised in case of a connection failure.
    :raises CommunicationFailed: Raised in case of a communication failure.
    :raises DevFailed: Raised in case of a device failure.
    :raises TypeError: Raised in case of an incorrect type of input arguments.

    .. versionadded:: 9.2.0

    .. deprecated:: 10.0.1
        Pipes scheduled for removal from PyTango in version 10.1.0
    """
    if value is None:
        value = [constants.AllPipe]
    if isinstance(value, StdStringVector) or is_pure_str(value):
        return self._get_pipe_config(value)
    elif isinstance(value, collections.abc.Sequence):
        v = seq_2_StdStringVector(value)
        return self._get_pipe_config(v)

    raise TypeError("value must be a string or a sequence<string>")


def __DeviceProxy__set_attribute_config(self, value):
    """
    set_attribute_config(self, attr_info, green_mode=None, wait=True, timeout=None) -> None
    set_attribute_config(self, attr_info_ex, green_mode=None, wait=True, timeout=None) -> None

        Change the attribute configuration/extended attribute configuration for the specified attribute(s)

    :param attr_info: Attribute information. This parameter is used when providing basic attribute(s) information.
    :type attr_info: Union[AttributeInfo, Sequence[AttributeInfo]], optional
    :param attr_info_ex: Extended attribute information. This parameter is used when providing extended attribute information. It should not be used simultaneously with 'attr_info'.
    :type attr_info_ex: Union[AttributeInfoEx, Sequence[AttributeInfoEx]], optional
    :param green_mode: Defaults to the current `DeviceProxy` GreenMode. Refer to `tango.DeviceProxy.get_green_mode` and `tango.DeviceProxy.set_green_mode` for more details.
    :type green_mode: GreenMode
    :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
    :type wait: bool
    :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
    :type timeout: float, optional

    :returns: None

    :raises ConnectionFailed: Raised in case of a connection failure.
    :raises CommunicationFailed: Raised in case of a communication failure.
    :raises DevFailed: Raised in case of a device failure.
    :raises TypeError: Raised in case of an incorrect type of input arguments.

    """
    if isinstance(value, AttributeInfoEx):
        v = AttributeInfoListEx()
        v.append(value)
    elif isinstance(value, AttributeInfo):
        v = AttributeInfoList()
        v.append(value)
    elif isinstance(value, AttributeInfoList):
        v = value
    elif isinstance(value, AttributeInfoListEx):
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
                "Value must be a AttributeInfo, AttributeInfoEx, "
                "sequence<AttributeInfo> or sequence<AttributeInfoEx"
            )
        for i in value:
            v.append(i)
    else:
        raise TypeError(
            "Value must be a AttributeInfo, AttributeInfoEx, "
            "sequence<AttributeInfo> or sequence<AttributeInfoEx"
        )

    return self._set_attribute_config(v)


@deprecated("set_pipe_config is deprecated - scheduled for removal in PyTango 10.1.0")
def __DeviceProxy__set_pipe_config(self, value):
    """
    set_pipe_config(self, pipe_info, green_mode=None, wait=True, timeout=None) -> None
    set_pipe_config(self, pipe_info, green_mode=None, wait=True, timeout=None) -> None

            Change the pipe configuration for the specified pipe

    :param pipe_info: Pipe information for a single pipe.
    :type pipe_info: PipeInfo, optional
    :param pipes_info: Pipes information for multiple pipes.
    :type pipes_info: sequence<PipeInfo>, optional
    :param green_mode: Defaults to the current `DeviceProxy` GreenMode. Refer to `tango.DeviceProxy.get_green_mode` and `tango.DeviceProxy.set_green_mode` for more details.
    :type green_mode: GreenMode
    :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
    :type wait: bool
    :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
    :type timeout: float, optional

    :returns: None

    :raises ConnectionFailed: Raised in case of a connection failure.
    :raises CommunicationFailed: Raised in case of a communication failure.
    :raises DevFailed: Raised in case of a device failure.
    :raises TypeError: Raised in case of an incorrect type of input arguments.

    .. versionadded:: 9.2.0

    .. deprecated:: 10.0.1
        Pipes scheduled for removal from PyTango in version 10.1.0
    """
    if isinstance(value, PipeInfo):
        v = PipeInfoList()
        v.append(value)
    elif isinstance(value, PipeInfoList):
        v = value
    elif isinstance(value, collections.abc.Sequence):
        if not len(value):
            return
        if isinstance(value[0], PipeInfo):
            v = PipeInfoList()
        else:
            raise TypeError("Value must be a PipeInfo or a sequence<PipeInfo>")
        for i in value:
            v.append(i)
    else:
        raise TypeError("Value must be a PipeInfo or a sequence<PipeInfo>")

    return self._set_pipe_config(v)


def __DeviceProxy__get_event_map_lock(self):
    """
    Internal helper method"""
    if not hasattr(self, "_subscribed_events_lock"):
        # do it like this instead of self._subscribed_events = dict() to avoid
        # calling __setattr__ which requests list of tango attributes from device
        self.__dict__["_subscribed_events_lock"] = threading.Lock()
    return self._subscribed_events_lock


def __DeviceProxy__get_event_map(self):
    """
    Internal helper method"""
    if not hasattr(self, "_subscribed_events"):
        # do it like this instead of self._subscribed_events = dict() to avoid
        # calling __setattr__ which requests list of tango attributes from device
        self.__dict__["_subscribed_events"] = dict()
    return self._subscribed_events


def __DeviceProxy__subscribe_event(self, *args, **kwargs):
    """
    subscribe_event(self, event_type, cb, stateless=False, green_mode=None, wait=True, timeout=None) -> int
    subscribe_event(self, attr_name, event, cb, filters=[], stateless=False, extract_as=Numpy, green_mode=None, wait=True, timeout=None) -> int
    subscribe_event(self, attr_name, event, queuesize, filters=[], stateless=False, green_mode=None, wait=True, timeout=None) -> int

            The client call to subscribe for event reception.
            In the push model the client implements a callback method which is triggered when the
            event is received. Filtering is done based on the reason specified and
            the event type. For example when reading the state and the reason
            specified is "change" the event will be fired only when the state
            changes. Events consist of an attribute name and the event reason.
            A standard set of reasons are implemented by the system, additional
            device specific reasons can be implemented by device servers programmers.

    :param attr_name: The device attribute name which will be sent as an event, e.g., "current".
    :type attr_name: str
    :param event_type: The event reason, which must be one of the enumerated values in `EventType`. This includes:
                        * `EventType.CHANGE_EVENT`
                        * `EventType.PERIODIC_EVENT`
                        * `EventType.ARCHIVE_EVENT`
                        * `EventType.ATTR_CONF_EVENT`
                        * `EventType.DATA_READY_EVENT`
                        * `EventType.USER_EVENT`
    :type event_type: EventType
    :param cb: Any callable object or an object with a callable "push_event" method.
    :type cb: callable
    :param filters: A variable list of name, value pairs which define additional filters for events.
    :type filters: sequence<str>, optional
    :param stateless: When this flag is set to false, an exception will be thrown if the event subscription encounters a problem. With the stateless flag set to true, the event subscription will always succeed, even if the corresponding device server is not running. A keep-alive thread will attempt to subscribe for the specified event every 10 seconds, executing a callback with the corresponding exception at every retry.
    :type stateless: bool
    :param queuesize: the size of the event reception buffer. The event reception buffer is implemented as a round robin buffer. This way the client can set-up different ways to receive events:
                        * Event reception buffer size = 1 : The client is interested only in the value of the last event received. All other events that have been received since the last reading are discarded.
                        * Event reception buffer size > 1 : The client has chosen to keep an event history of a given size. When more events arrive since the last reading, older events will be discarded.
                        * Event reception buffer size = ALL_EVENTS : The client buffers all received events. The buffer size is unlimited and only restricted by the available memory for the client.
    :type queuesize: float, optional
    :param extract_as: (Description Needed)
    :type extract_as: ExtractAs
    :param green_mode: Defaults to the current `DeviceProxy` GreenMode. See `tango.DeviceProxy.get_green_mode` and `tango.DeviceProxy.set_green_mode` for more details.
    :type green_mode: GreenMode
    :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
    :type wait: bool
    :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
    :type timeout: float, optional

    :returns: An event id which has to be specified when unsubscribing from this event.
    :rtype: int

    :raises EventSystemFailed: Raised in case of a failure in the event system.
    :raises TypeError: Raised in case of an incorrect type of input arguments.

    """
    # First argument is the event type
    if args and isinstance(args[0], int):
        return __DeviceProxy__subscribe_event_global(self, *args, **kwargs)
    # First argument is the attribute name
    else:
        return __DeviceProxy__subscribe_event_attrib(self, *args, **kwargs)


def __DeviceProxy__subscribe_event_global(
    self, event_type, cb, stateless=False, green_mode=None
):
    if event_type != EventType.INTERFACE_CHANGE_EVENT:
        raise TypeError("This method is only for Interface Change Events")
    else:
        if isinstance(cb, collections.abc.Callable):
            cbfn = __CallBackPushEvent()
            cbfn.push_event = green_callback(cb, obj=self, green_mode=green_mode)
        elif hasattr(cb, "push_event") and isinstance(
            cb.push_event, collections.abc.Callable
        ):
            cbfn = __CallBackPushEvent()
            cbfn.push_event = green_callback(
                cb.push_event, obj=self, green_mode=green_mode
            )
        else:
            raise TypeError(
                "Parameter cb should be a callable object or "
                "an object with a 'push_event' method."
            )

        event_id = self.__subscribe_event(event_type, cbfn, stateless)

        with self.__get_event_map_lock():
            se = self.__get_event_map()
            evt_data = se.get(event_id)
            if evt_data is not None:
                # Raise exception
                desc = textwrap.dedent(
                    f"""\
                    Internal PyTango error:
                    {self}.subscribe_event({event_type}) already has key {event_id} assigned to ({evt_data[2]}, {evt_data[1]})
                    Please report error to PyTango"""
                )
                Except.throw_exception(
                    "Py_InternalError", desc, "DeviceProxy.subscribe_event"
                )
        se[event_id] = (cbfn, event_type, "dummy")
        return event_id


def __DeviceProxy__subscribe_event_attrib(
    self,
    attr_name,
    event_type,
    cb_or_queuesize,
    filters=[],
    stateless=False,
    extract_as=ExtractAs.Numpy,
    green_mode=None,
):
    if isinstance(cb_or_queuesize, collections.abc.Callable):
        cb = __CallBackPushEvent()
        cb.push_event = green_callback(cb_or_queuesize, obj=self, green_mode=green_mode)
    elif hasattr(cb_or_queuesize, "push_event") and isinstance(
        cb_or_queuesize.push_event, collections.abc.Callable
    ):
        cb = __CallBackPushEvent()
        cb.push_event = green_callback(
            cb_or_queuesize.push_event, obj=self, green_mode=green_mode
        )
    elif is_integer(cb_or_queuesize):
        cb = cb_or_queuesize  # queuesize
    else:
        raise TypeError(
            "Parameter cb_or_queuesize should be a number, a"
            " callable object or an object with a 'push_event' method."
        )

    event_id = self.__subscribe_event(
        attr_name, event_type, cb, filters, stateless, extract_as
    )

    with self.__get_event_map_lock():
        se = self.__get_event_map()
        evt_data = se.get(event_id)
        if evt_data is None:
            se[event_id] = (cb, event_type, attr_name)
            return event_id
        # Raise exception
        desc = textwrap.dedent(
            f"""\
            Internal PyTango error:
            {self}.subscribe_event({attr_name}, {event_type}) already has key {event_id} assigned to ({evt_data[2]}, {evt_data[1]})
            Please report error to PyTango"""
        )
        Except.throw_exception("Py_InternalError", desc, "DeviceProxy.subscribe_event")


def __DeviceProxy__unsubscribe_event(self, event_id):
    """
    unsubscribe_event(self, event_id, green_mode=None, wait=True, timeout=None) -> None

        Unsubscribes a client from receiving the event specified by event_id.

    :param event_id: The event identifier returned by `DeviceProxy::subscribe_event()`. Unlike in TangoC++, this implementation checks that the `event_id` has been subscribed to in this `DeviceProxy`.
    :type event_id: int
    :param green_mode: Defaults to the current `DeviceProxy` GreenMode. Refer to `tango.DeviceProxy.get_green_mode` and `tango.DeviceProxy.set_green_mode` for more details.
    :type green_mode: GreenMode
    :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
    :type wait: bool
    :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
    :type timeout: float, optional

    :returns: None

    :raises EventSystemFailed: Raised in case of a failure in the event system.
    :raises KeyError: Raised if the specified `event_id` is not found or not subscribed in this `DeviceProxy`.
    """
    events_del = set()
    timestamp = time.time()
    se = self.__get_event_map()

    with self.__get_event_map_lock():
        # first delete event callbacks that have expire
        for evt_id, (_, expire_time) in self._pending_unsubscribe.items():
            if expire_time <= timestamp:
                events_del.add(evt_id)
        for evt_id in events_del:
            del self._pending_unsubscribe[evt_id]

        # unsubscribe and put the callback in the pending unsubscribe callbacks
        try:
            evt_info = se[event_id]
        except KeyError:
            raise KeyError(
                "This device proxy does not own this subscription " + str(event_id)
            )
        del se[event_id]
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
    self, event_id, callback=None, extract_as=ExtractAs.Numpy
):
    """
    get_events(self, event_id, callback=None, extract_as=Numpy) -> None

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
    :type event_id: int
    :param callback: Any callable object or any object with a "push_event" method.
    :type callback: callable
    :param extract_as: (Description Needed)
    :type extract_as: ExtractAs

    :returns: None

    :raises EventSystemFailed: Raised in case of a failure in the event system.
    :raises TypeError: Raised in case of an incorrect type of input arguments.
    :raises ValueError: Raised in case of an invalid value.

    :see also: :meth:`~tango.DeviceProxy.subscribe_event`

    """
    if callback is None:
        queuesize, event_type, attr_name = self.__get_event_map().get(
            event_id, (None, None, None)
        )
        if event_type is None:
            raise ValueError(
                f"Invalid event_id. You are not subscribed to event {str(event_id)}."
            )
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
        elif event_type in (EventType.PIPE_EVENT,):
            return self.__get_pipe_events(event_id, extract_as)
        else:
            raise ValueError("Unknown event_type: " + str(event_type))
    elif isinstance(callback, collections.abc.Callable):
        cb = __CallBackPushEvent()
        cb.push_event = callback
        return self.__get_callback_events(event_id, cb, extract_as)
    elif hasattr(callback, "push_event") and isinstance(
        callback.push_event, collections.abc.Callable
    ):
        cb = __CallBackPushEvent()
        cb.push_event = callback.push_event
        return self.__get_callback_events(event_id, cb, extract_as)
    else:
        raise TypeError(
            "Parameter 'callback' should be None, a callable object or an object with a 'push_event' method."
        )


def __DeviceProxy___get_info_(self):
    """Protected method that gets device info once and stores it in cache"""
    if not hasattr(self, "_dev_info"):
        try:
            info = self.info()
            info_without_cyclic_reference = __TangoInfo.from_copy(info)
            self.__dict__["_dev_info"] = info_without_cyclic_reference
        except Exception:
            return __TangoInfo.from_defaults()
    return self._dev_info


def __DeviceProxy__str(self):
    info = self._get_info_()
    return f"{info.dev_class}({self.dev_name()})"


@deprecated("read_pipe is deprecated - scheduled for removal in PyTango 10.1.0")
def __DeviceProxy__read_pipe(self, pipe_name, extract_as=ExtractAs.Numpy):
    r = self.__read_pipe(pipe_name)
    return r.extract(extract_as)


def __get_pipe_type_simple(obj):
    if is_non_str_seq(obj):
        if (
            len(obj) == 2
            and is_pure_str(obj[0])
            and (is_non_str_seq(obj[1]) or isinstance(obj[1], dict))
        ):
            tg_type = CmdArgType.DevPipeBlob
        else:
            tg_type = __get_pipe_type(obj[0])
            tg_type = scalar_to_array_type(tg_type)
    elif is_pure_str(obj):
        tg_type = CmdArgType.DevString
    elif isinstance(obj, DevState):
        tg_type = CmdArgType.DevState
    elif isinstance(obj, bool):
        tg_type = CmdArgType.DevBoolean
    elif is_integer(obj):
        tg_type = CmdArgType.DevLong64
    elif is_number(obj):
        tg_type = CmdArgType.DevDouble
    else:
        raise ValueError("Cannot determine object tango type")
    return tg_type


def __get_tango_type(dtype):
    if is_non_str_seq(dtype):
        tg_type = dtype[0]
        if is_non_str_seq(tg_type):
            raise TypeError("Pipe doesn't support 2D data")
        tg_type = TO_TANGO_TYPE[tg_type]
        tg_type = scalar_to_array_type(tg_type)
    else:
        tg_type = TO_TANGO_TYPE[dtype]
    return tg_type


def __get_pipe_type(obj, dtype=None):
    if dtype is not None:
        return __get_tango_type(dtype)
    try:
        ndim, dtype = obj.ndim, str(obj.dtype)
    except AttributeError:
        return __get_pipe_type_simple(obj)
    if ndim > 1:
        raise TypeError(
            f"cannot translate numpy array with {obj.ndim} " f"dimensions to tango type"
        )
    tg_type = TO_TANGO_TYPE[dtype]
    if ndim > 0:
        tg_type = scalar_to_array_type(dtype)
    return tg_type


def __sanatize_pipe_element(elem):
    if isinstance(elem, dict):
        result = dict(elem)
    else:
        result = dict(name=elem[0], value=elem[1])
    result["value"] = value = result.get("value", result.pop("blob", None))
    result["dtype"] = dtype = __get_pipe_type(value, dtype=result.get("dtype"))
    if dtype == CmdArgType.DevPipeBlob:
        result["value"] = value[0], __sanatize_pipe_blob(value[1])
    return result


def __sanatize_pipe_blob(blob):
    if isinstance(blob, dict):
        return [__sanatize_pipe_element((k, v)) for k, v in blob.items()]
    else:
        return [__sanatize_pipe_element(elem) for elem in blob]


@deprecated("write_pipe is deprecated - scheduled for removal in PyTango 10.1.0")
def __DeviceProxy__write_pipe(self, *args, **kwargs):
    pipe_name, (blob_name, blob_data) = args
    sani_blob_data = __sanatize_pipe_blob(blob_data)
    self.__write_pipe(pipe_name, blob_name, sani_blob_data)


@deprecated("get_pipe_list is deprecated - scheduled for removal in PyTango 10.1.0")
def __DeviceProxy__get_pipe_list(self):
    """
    get_pipe_list(self) -> sequence<str>

    Return the names of all pipes implemented for this device.

    Parameters : None
    Return     : sequence<str>

    Throws     : ConnectionFailed, CommunicationFailed,
                 DevFailed from device

    .. versionadded:: 9.2.0

    .. deprecated:: 10.0.1
        Pipes scheduled for removal from PyTango in version 10.1.0
    """
    return self._get_pipe_list()


def __DeviceProxy__read_attributes(self, *args, **kwargs):
    return self._read_attributes(*args, **kwargs)


def __DeviceProxy__write_attribute(self, *args, **kwargs):
    return self._write_attribute(*args, **kwargs)


def __DeviceProxy__write_attributes(self, *args, **kwargs):
    return self._write_attributes(*args, **kwargs)


def __DeviceProxy__ping(self, *args, **kwargs):
    return self._ping(*args, **kwargs)


def __DeviceProxy__state(self, *args, **kwargs):
    """state(self, green_mode=None, wait=True, timeout=None) -> DevState

        A method which returns the state of the device.

    :param green_mode: Defaults to the current `DeviceProxy` GreenMode. Refer to `tango.DeviceProxy.get_green_mode` and `tango.DeviceProxy.set_green_mode` for more details.
    :type green_mode: GreenMode
    :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
    :type wait: bool
    :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
    :type timeout: float, optional

    :returns: A `DevState` constant.
    :rtype: DevState

    """
    return self._state(*args, **kwargs)


def __DeviceProxy__status(self, *args, **kwargs):
    """status(self, green_mode=None, wait=True, timeout=None) -> str

        A method which returns the status of the device as a string.

    :param green_mode: Defaults to the current `DeviceProxy` GreenMode. Refer to `tango.DeviceProxy.get_green_mode` and `tango.DeviceProxy.set_green_mode` for more details.
    :type green_mode: GreenMode
    :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
    :type wait: bool
    :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
    :type timeout: float, optional

    :returns: string describing the device status
    :rtype: str
    """
    return self._status(*args, **kwargs)


def __init_DeviceProxy():
    DeviceProxy.__init_orig__ = DeviceProxy.__init__
    DeviceProxy.__init__ = _trace_client(__DeviceProxy____init__)

    DeviceProxy.get_green_mode = __DeviceProxy__get_green_mode
    DeviceProxy.set_green_mode = __DeviceProxy__set_green_mode

    DeviceProxy.freeze_dynamic_interface = __DeviceProxy__freeze_dynamic_interface
    DeviceProxy.unfreeze_dynamic_interface = __DeviceProxy__unfreeze_dynamic_interface
    DeviceProxy.is_dynamic_interface_frozen = __DeviceProxy__is_dynamic_interface_frozen

    DeviceProxy.__getattr__ = __DeviceProxy__getattr
    DeviceProxy.__setattr__ = __DeviceProxy__setattr
    DeviceProxy.__getitem__ = __DeviceProxy__getitem
    DeviceProxy.__setitem__ = __DeviceProxy__setitem
    DeviceProxy.__contains__ = __DeviceProxy__contains
    DeviceProxy.__dir__ = __DeviceProxy__dir

    DeviceProxy.__get_cmd_cache = __DeviceProxy__get_cmd_cache
    DeviceProxy.__get_attr_cache = __DeviceProxy__get_attr_cache
    DeviceProxy.__get_pipe_cache = __DeviceProxy__get_pipe_cache
    DeviceProxy.__refresh_cmd_cache = __DeviceProxy__refresh_cmd_cache
    DeviceProxy.__refresh_attr_cache = __DeviceProxy__refresh_attr_cache
    DeviceProxy.__refresh_pipe_cache = __DeviceProxy__refresh_pipe_cache

    DeviceProxy.ping = green(_trace_client(__DeviceProxy__ping))
    DeviceProxy.state = green(_trace_client(__DeviceProxy__state))
    DeviceProxy.status = green(_trace_client(__DeviceProxy__status))

    DeviceProxy.read_attribute = green(_trace_client(__DeviceProxy__read_attribute))
    DeviceProxy.read_attributes = green(_trace_client(__DeviceProxy__read_attributes))
    DeviceProxy.write_attribute = green(_trace_client(__DeviceProxy__write_attribute))
    DeviceProxy.write_attributes = green(_trace_client(__DeviceProxy__write_attributes))
    DeviceProxy.write_read_attribute = green(
        _trace_client(__DeviceProxy__write_read_attribute)
    )
    DeviceProxy.write_read_attributes = green(
        _trace_client(__DeviceProxy__write_read_attributes)
    )

    DeviceProxy.read_attributes_asynch = green(
        _trace_client(__DeviceProxy__read_attributes_asynch)
    )
    DeviceProxy.read_attribute_asynch = green(
        _trace_client(__DeviceProxy__read_attribute_asynch)
    )

    DeviceProxy.read_attributes_reply = green(
        _trace_client(__DeviceProxy__read_attributes_reply)
    )
    DeviceProxy.read_attribute_reply = green(
        _trace_client(__DeviceProxy__read_attribute_reply)
    )

    DeviceProxy.write_attributes_asynch = green(
        _trace_client(__DeviceProxy__write_attributes_asynch)
    )
    DeviceProxy.write_attribute_asynch = green(
        _trace_client(__DeviceProxy__write_attribute_asynch)
    )

    DeviceProxy.write_attributes_reply = green(
        _trace_client(__DeviceProxy__write_attributes_reply)
    )
    DeviceProxy.write_attribute_reply = green(
        _trace_client(__DeviceProxy__write_attribute_reply)
    )

    DeviceProxy.read_pipe = green(_trace_client(__DeviceProxy__read_pipe))
    DeviceProxy.write_pipe = green(_trace_client(__DeviceProxy__write_pipe))
    DeviceProxy.get_pipe_list = __DeviceProxy__get_pipe_list

    DeviceProxy.get_property = green(_trace_client(__DeviceProxy__get_property))
    DeviceProxy.put_property = green(_trace_client(__DeviceProxy__put_property))
    DeviceProxy.delete_property = green(_trace_client(__DeviceProxy__delete_property))
    DeviceProxy.get_property_list = green(
        _trace_client(__DeviceProxy__get_property_list)
    )
    DeviceProxy.get_attribute_config = green(
        _trace_client(__DeviceProxy__get_attribute_config)
    )
    DeviceProxy.get_attribute_config_ex = green(
        _trace_client(__DeviceProxy__get_attribute_config_ex)
    )
    DeviceProxy.set_attribute_config = green(
        _trace_client(__DeviceProxy__set_attribute_config)
    )

    DeviceProxy.get_command_config = green(
        _trace_client(__DeviceProxy__get_command_config)
    )

    DeviceProxy.get_pipe_config = green(_trace_client(__DeviceProxy__get_pipe_config))
    DeviceProxy.set_pipe_config = green(_trace_client(__DeviceProxy__set_pipe_config))

    DeviceProxy.__get_event_map = __DeviceProxy__get_event_map
    DeviceProxy.__get_event_map_lock = __DeviceProxy__get_event_map_lock

    DeviceProxy.subscribe_event = green(
        _trace_client(__DeviceProxy__subscribe_event), consume_green_mode=False
    )
    DeviceProxy.unsubscribe_event = green(
        _trace_client(__DeviceProxy__unsubscribe_event)
    )
    DeviceProxy.get_events = _trace_client(__DeviceProxy__get_events)
    DeviceProxy.__unsubscribe_event_all = __DeviceProxy__unsubscribe_event_all

    DeviceProxy.__str__ = __DeviceProxy__str
    DeviceProxy.__repr__ = __DeviceProxy__str
    DeviceProxy._get_info_ = __DeviceProxy___get_info_


def __doc_DeviceProxy():
    def document_method(method_name, desc, append=True):
        return __document_method(DeviceProxy, method_name, desc, append)

    DeviceProxy.__doc__ = """\
    DeviceProxy is the high level Tango object which provides the client with
    an easy-to-use interface to TANGO devices. DeviceProxy provides interfaces
    to all TANGO Device interfaces.The DeviceProxy manages timeouts, stateless
    connections and reconnection if the device server is restarted. To create
    a DeviceProxy, a Tango Device name must be set in the object constructor.

    Example :
       dev = tango.DeviceProxy("sys/tg_test/1")

    DeviceProxy(dev_name, green_mode=None, wait=True, timeout=True) -> DeviceProxy
    DeviceProxy(self, dev_name, need_check_acc, green_mode=None, wait=True, timeout=True) -> DeviceProxy

    Creates a new :class:`~tango.DeviceProxy`.

    :param dev_name: the device name or alias
    :type dev_name: str
    :param need_check_acc: in first version of the function it defaults to True.
                           Determines if at creation time of DeviceProxy it should check
                           for channel access (rarely used)
    :type need_check_acc: bool
    :param green_mode: determines the mode of execution of the device (including.
                      the way it is created). Defaults to the current global
                      green_mode (check :func:`~tango.get_green_mode` and
                      :func:`~tango.set_green_mode`)
    :type green_mode: :obj:`~tango.GreenMode`
    :param wait: whether or not to wait for result. If green_mode
                 Ignored when green_mode is Synchronous (always waits).
    :type wait: bool
    :param timeout: The number of seconds to wait for the result.
                    If None, then there is no limit on the wait time.
                    Ignored when green_mode is Synchronous or wait is False.
    :type timeout: float
    :returns:
        if green_mode is Synchronous or wait is True:
            :class:`~tango.DeviceProxy`
        elif green_mode is Futures:
            :class:`concurrent.futures.Future`
        elif green_mode is Gevent:
            :class:`gevent.event.AsynchResult`
    :throws:
        * :class:`~tango.DevFailed` if green_mode is Synchronous or wait is True
          and there is an error creating the device.
        * :class:`concurrent.futures.TimeoutError` if green_mode is Futures,
          wait is False, timeout is not None and the time to create the device
          has expired.
        * :class:`gevent.timeout.Timeout` if green_mode is Gevent, wait is False,
          timeout is not None and the time to create the device has expired.

    .. versionadded:: 8.1.0
        *green_mode* parameter.
        *wait* parameter.
        *timeout* parameter.

    """

    # ------------------------------------
    #   General methods
    # ------------------------------------

    document_method(
        "info",
        """
    info(self) -> DeviceInfo

            A method which returns information on the device

        Parameters : None
        Return     : (DeviceInfo) object
        Example    :
                dev_info = dev.info()
                print(dev_info.dev_class)
                print(dev_info.server_id)
                print(dev_info.server_host)
                print(dev_info.server_version)
                print(dev_info.doc_url)
                print(dev_info.dev_type)
                print(dev_info.version_info)

    """,
    )

    document_method(
        "get_device_db",
        """
    get_device_db(self) -> Database

            Returns the internal database reference

        Parameters : None
        Return     : (Database) object

        New in PyTango 7.0.0
    """,
    )

    document_method(
        "adm_name",
        """
    adm_name(self) -> str

            Return the name of the corresponding administrator device. This is
            useful if you need to send an administration command to the device
            server, e.g restart it

        New in PyTango 3.0.4
    """,
    )

    document_method(
        "description",
        """
    description(self) -> str

            Get device description.

        Parameters : None
        Return     : (str) describing the device
    """,
    )

    document_method(
        "name",
        """
    name(self) -> str

            Return the device name from the device itself.
    """,
    )

    document_method(
        "alias",
        """
    alias(self) -> str

            Return the device alias if one is defined.
            Otherwise, throws exception.

        Return     : (str) device alias
    """,
    )

    document_method(
        "get_tango_lib_version",
        """
    get_tango_lib_version(self) -> int

            Returns the Tango lib version number used by the remote device
            Otherwise, throws exception.

        Return     : (int) The device Tango lib version as a 3 or 4 digits number.
                     Possible return value are: 100,200,500,520,700,800,810,...

        New in PyTango 8.1.0
    """,
    )

    document_method(
        "ping",
        """
    ping(self, green_mode=None, wait=True, timeout=True) -> int

            A method which sends a ping to the device

        Parameters :
            - green_mode : (GreenMode) Defaults to the current DeviceProxy GreenMode.
                           (see :meth:`~tango.DeviceProxy.get_green_mode` and
                           :meth:`~tango.DeviceProxy.set_green_mode`).
            - wait       : (bool) whether or not to wait for result. If green_mode
                           is *Synchronous*, this parameter is ignored as it always
                           waits for the result.
                           Ignored when green_mode is Synchronous (always waits).
            - timeout    : (float) The number of seconds to wait for the result.
                           If None, then there is no limit on the wait time.
                           Ignored when green_mode is Synchronous or wait is False.
        Return     : (int) time elapsed in microseconds
        Throws     : exception if device is not alive
    """,
    )

    document_method(
        "black_box",
        """
    black_box(self, n) -> sequence<str>

            Get the last commands executed on the device server

        Parameters :
            - n : n number of commands to get
        Return     : (sequence<str>) sequence of strings containing the date, time,
                     command and from which client computer the command
                     was executed
        Example :
                print(black_box(4))
    """,
    )

    # -------------------------------------
    #   Device methods
    # -------------------------------------

    document_method(
        "get_command_list",
        """
    get_command_list(self) -> sequence<str>

            Return the names of all commands implemented for this device.

        Parameters : None
        Return     : sequence<str>

        Throws     : ConnectionFailed, CommunicationFailed,
                     DevFailed from device
    """,
    )

    document_method(
        "command_query",
        """
    command_query(self, command) -> CommandInfo

            Query the device for information about a single command.

        Parameters :
                - command : (str) command name
        Return     : (CommandInfo) object
        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device
        Example :
                com_info = dev.command_query(""DevString"")
                print(com_info.cmd_name)
                print(com_info.cmd_tag)
                print(com_info.in_type)
                print(com_info.out_type)
                print(com_info.in_type_desc)
                print(com_info.out_type_desc)
                print(com_info.disp_level)

        See CommandInfo documentation string form more detail
    """,
    )

    document_method(
        "command_list_query",
        """
    command_list_query(self) -> sequence<CommandInfo>

            Query the device for information on all commands.

        Parameters : None
        Return     : (CommandInfoList) Sequence of CommandInfo objects
    """,
    )

    document_method(
        "import_info",
        """
    import_info(self) -> DbDevImportInfo

            Query the device for import info from the database.

        Parameters : None
        Return     : (DbDevImportInfo)
        Example :
                dev_import = dev.import_info()
                print(dev_import.name)
                print(dev_import.exported)
                print(dev_ior.ior)
                print(dev_version.version)

        All DbDevImportInfo fields are strings except for exported which
        is an integer"
    """,
    )

    # ------------------------------------
    #   Property methods
    # ------------------------------------

    # get_property -> in code
    # put_property -> in code
    # delete_property -> in code
    # get_property_list -> in code

    # ------------------------------------
    #   Attribute methods
    # ------------------------------------

    document_method(
        "get_attribute_list",
        """
    get_attribute_list(self) -> sequence<str>

            Return the names of all attributes implemented for this device.

        Parameters : None
        Return     : sequence<str>

        Throws     : ConnectionFailed, CommunicationFailed,
                     DevFailed from device
    """,
    )

    # get_attribute_config -> in code
    # get_attribute_config_ex -> in code

    document_method(
        "attribute_query",
        """
    attribute_query(self, attr_name) -> AttributeInfoEx

            Query the device for information about a single attribute.

        Parameters :
                - attr_name :(str) the attribute name
        Return     : (AttributeInfoEx) containing the attribute
                     configuration

        Throws     : ConnectionFailed, CommunicationFailed,
                     DevFailed from device
    """,
    )

    document_method(
        "attribute_list_query",
        """
    attribute_list_query(self) -> sequence<AttributeInfo>

            Query the device for info on all attributes. This method returns
            a sequence of tango.AttributeInfo.

        Parameters : None
        Return     : (sequence<AttributeInfo>) containing the
                     attributes configuration

        Throws     : ConnectionFailed, CommunicationFailed,
                     DevFailed from device
    """,
    )

    document_method(
        "attribute_list_query_ex",
        """
    attribute_list_query_ex(self) -> sequence<AttributeInfoEx>

            Query the device for info on all attributes. This method returns
            a sequence of tango.AttributeInfoEx.

        Parameters : None
        Return     : (sequence<AttributeInfoEx>) containing the
                     attributes configuration

        Throws     : ConnectionFailed, CommunicationFailed,
                     DevFailed from device
    """,
    )

    # set_attribute_config -> in code

    document_method(
        "read_attribute",
        """
    read_attribute(self, attr_name, extract_as=ExtractAs.Numpy, green_mode=None, wait=True, timeout=None) -> DeviceAttribute

            Read a single attribute.

        Parameters :
            - attr_name  : (str) The name of the attribute to read.
            - extract_as : (ExtractAs) Defaults to numpy.
            - green_mode : (GreenMode) Defaults to the current DeviceProxy GreenMode.
                           (see :meth:`~tango.DeviceProxy.get_green_mode` and
                           :meth:`~tango.DeviceProxy.set_green_mode`).
            - wait       : (bool) whether or not to wait for result. If green_mode
                           is *Synchronous*, this parameter is ignored as it always
                           waits for the result.
                           Ignored when green_mode is Synchronous (always waits).
            - timeout    : (float) The number of seconds to wait for the result.
                           If None, then there is no limit on the wait time.
                           Ignored when green_mode is Synchronous or wait is False.

        Return     : (DeviceAttribute)

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device
                     TimeoutError (green_mode == Futures) If the future didn't finish executing before the given timeout.
                     Timeout (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

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
    """,
    )

    document_method(
        "read_attributes",
        """
    read_attributes(self, attr_names, extract_as=ExtractAs.Numpy, green_mode=None, wait=True, timeout=None) -> sequence<DeviceAttribute>

            Read the list of specified attributes.

        Parameters :
                - attr_names : (sequence<str>) A list of attributes to read.
                - extract_as : (ExtractAs) Defaults to numpy.
                - green_mode : (GreenMode) Defaults to the current DeviceProxy GreenMode.
                               (see :meth:`~tango.DeviceProxy.get_green_mode` and
                               :meth:`~tango.DeviceProxy.set_green_mode`).
                - wait       : (bool) whether or not to wait for result. If green_mode
                               is *Synchronous*, this parameter is ignored as it always
                               waits for the result.
                               Ignored when green_mode is Synchronous (always waits).
                - timeout    : (float) The number of seconds to wait for the result.
                               If None, then there is no limit on the wait time.
                               Ignored when green_mode is Synchronous or wait is False.

        Return     : (sequence<DeviceAttribute>)

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device
                     TimeoutError (green_mode == Futures) If the future didn't finish executing before the given timeout.
                     Timeout (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

    .. versionadded:: 8.1.0
        *green_mode* parameter.
        *wait* parameter.
        *timeout* parameter.
    """,
    )

    document_method(
        "write_attribute",
        """
    write_attribute(self, attr_name, value, green_mode=None, wait=True, timeout=None) -> None
    write_attribute(self, attr_info, value, green_mode=None, wait=True, timeout=None) -> None

            Write a single attribute.

        Parameters :
                - attr_name : (str) The name of the attribute to write.
                - attr_info : (AttributeInfo)
                - value : The value. For non SCALAR attributes it may be any sequence of sequences.
                - green_mode : (GreenMode) Defaults to the current DeviceProxy GreenMode.
                               (see :meth:`~tango.DeviceProxy.get_green_mode` and
                               :meth:`~tango.DeviceProxy.set_green_mode`).
                - wait       : (bool) whether or not to wait for result. If green_mode
                               is *Synchronous*, this parameter is ignored as it always
                               waits for the result.
                               Ignored when green_mode is Synchronous (always waits).
                - timeout    : (float) The number of seconds to wait for the result.
                               If None, then there is no limit on the wait time.
                               Ignored when green_mode is Synchronous or wait is False.

        Throws     : ConnectionFailed, CommunicationFailed, DeviceUnlocked, DevFailed from device
                     TimeoutError (green_mode == Futures) If the future didn't finish executing before the given timeout.
                     Timeout (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

    .. versionadded:: 8.1.0
        *green_mode* parameter.
        *wait* parameter.
        *timeout* parameter.
    """,
    )

    document_method(
        "write_attributes",
        """
    write_attributes(self, name_val, green_mode=None, wait=True, timeout=None) -> None

            Write the specified attributes.

        Parameters :
                - name_val: A list of pairs (attr_name, value). See write_attribute
                - green_mode : (GreenMode) Defaults to the current DeviceProxy GreenMode.
                               (see :meth:`~tango.DeviceProxy.get_green_mode` and
                               :meth:`~tango.DeviceProxy.set_green_mode`).
                - wait       : (bool) whether or not to wait for result. If green_mode
                               is *Synchronous*, this parameter is ignored as it always
                               waits for the result.
                               Ignored when green_mode is Synchronous (always waits).
                - timeout    : (float) The number of seconds to wait for the result.
                               If None, then there is no limit on the wait time.
                               Ignored when green_mode is Synchronous or wait is False.

        Throws     : ConnectionFailed, CommunicationFailed, DeviceUnlocked,
                     DevFailed or NamedDevFailedList from device
                     TimeoutError (green_mode == Futures) If the future didn't finish executing before the given timeout.
                     Timeout (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

    .. versionadded:: 8.1.0
        *green_mode* parameter.
        *wait* parameter.
        *timeout* parameter.
    """,
    )

    document_method(
        "write_read_attribute",
        """
    write_read_attribute(self, attr_name, value, extract_as=ExtractAs.Numpy, green_mode=None, wait=True, timeout=None) -> DeviceAttribute

            Write then read a single attribute in a single network call.
            By default (serialisation by device), the execution of this call in
            the server can't be interrupted by other clients.

        Parameters : see write_attribute(attr_name, value)
        Return     : A tango.DeviceAttribute object.

        Throws     : ConnectionFailed, CommunicationFailed, DeviceUnlocked,
                     DevFailed from device, WrongData
                     TimeoutError (green_mode == Futures) If the future didn't finish executing before the given timeout.
                     Timeout (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        New in PyTango 7.0.0

    .. versionadded:: 8.1.0
        *green_mode* parameter.
        *wait* parameter.
        *timeout* parameter.
    """,
    )

    document_method(
        "write_read_attributes",
        """
    write_read_attributes(self, name_val, attr_names, extract_as=ExtractAs.Numpy, green_mode=None, wait=True, timeout=None) -> DeviceAttribute

            Write then read attribute(s) in a single network call. By
            default (serialisation by device), the execution of this
            call in the server can't be interrupted by other clients.
            On the server side, attribute(s) are first written and
            if no exception has been thrown during the write phase,
            attributes will be read.

        Parameters :
                - name_val: A list of pairs (attr_name, value). See write_attribute
                - attr_names : (sequence<str>) A list of attributes to read.
                - extract_as : (ExtractAs) Defaults to numpy.
                - green_mode : (GreenMode) Defaults to the current DeviceProxy GreenMode.
                               (see :meth:`~tango.DeviceProxy.get_green_mode` and
                               :meth:`~tango.DeviceProxy.set_green_mode`).
                - wait       : (bool) whether or not to wait for result. If green_mode
                               is *Synchronous*, this parameter is ignored as it always
                               waits for the result.
                               Ignored when green_mode is Synchronous (always waits).
                - timeout    : (float) The number of seconds to wait for the result.
                               If None, then there is no limit on the wait time.
                               Ignored when green_mode is Synchronous or wait is False.

        Return     : (sequence<DeviceAttribute>)

        Throws     : ConnectionFailed, CommunicationFailed, DeviceUnlocked,
                     DevFailed from device, WrongData
                     TimeoutError (green_mode == Futures) If the future didn't finish executing before the given timeout.
                     Timeout (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        New in PyTango 9.2.0
    """,
    )

    # -------------------------------------
    #   Pipe methods
    # -------------------------------------

    document_method(
        "read_pipe",
        """
    read_pipe(self, pipe_name, extract_as=ExtractAs.Numpy, green_mode=None, wait=True, timeout=None) -> tuple

            Read a single pipe. The result is a *blob*: a tuple with two elements: blob name (string) and blob
            data (sequence). The blob data consists of a sequence where each element is a dictionary with the
            following keys:

            - name: blob element name
            - dtype: tango data type
            - value: blob element data (str for DevString, etc)

        In case dtype is ``DevPipeBlob``, value is again a *blob*.

        Parameters :
            - pipe_name  : (str) The name of the pipe to read.
            - extract_as : (ExtractAs) Defaults to numpy.
            - green_mode : (GreenMode) Defaults to the current DeviceProxy GreenMode.
                           (see :meth:`~tango.DeviceProxy.get_green_mode` and
                           :meth:`~tango.DeviceProxy.set_green_mode`).
            - wait       : (bool) whether or not to wait for result. If green_mode
                           is *Synchronous*, this parameter is ignored as it always
                           waits for the result.
                           Ignored when green_mode is Synchronous (always waits).
            - timeout    : (float) The number of seconds to wait for the result.
                           If None, then there is no limit on the wait time.
                           Ignored when green_mode is Synchronous or wait is False.

        Return     : tuple<str, sequence>

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device
                     TimeoutError (green_mode == Futures) If the future didn't finish executing before the given timeout.
                     Timeout (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        .. versionadded:: 9.2.0

        .. deprecated:: 10.0.1
            Pipes scheduled for removal from PyTango in version 10.1.0
    """,
    )

    document_method(
        "write_pipe",
        """
    write_pipe(self, blob, green_mode=None, wait=True, timeout=None)

            Write a *blob* to a single pipe. The *blob* comprises: a tuple with two elements: blob name (string) and blob
            data (sequence). The blob data consists of a sequence where each element is a dictionary with the
            following keys:

            - name: blob element name
            - dtype: tango data type
            - value: blob element data (str for DevString, etc)

        In case dtype is ``DevPipeBlob``, value is also a *blob*.

        Parameters :
            - blob       : a tuple with two elements: blob name (string) and blob
                           data (sequence).
            - green_mode : (GreenMode) Defaults to the current DeviceProxy GreenMode.
                           (see :meth:`~tango.DeviceProxy.get_green_mode` and
                           :meth:`~tango.DeviceProxy.set_green_mode`).
            - wait       : (bool) whether or not to wait for result. If green_mode
                           is *Synchronous*, this parameter is ignored as it always
                           waits for the result.
                           Ignored when green_mode is Synchronous (always waits).
            - timeout    : (float) The number of seconds to wait for the result.
                           If None, then there is no limit on the wait time.
                           Ignored when green_mode is Synchronous or wait is False.

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device
                     TimeoutError (green_mode == Futures) If the future didn't finish executing before the given timeout.
                     Timeout (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        .. versionadded:: 9.2.1

        .. deprecated:: 10.0.1
            Pipes scheduled for removal from PyTango in version 10.1.0
    """,
    )

    # -------------------------------------
    #   History methods
    # -------------------------------------
    document_method(
        "command_history",
        """
    command_history(self, cmd_name, depth) -> sequence<DeviceDataHistory>

            Retrieve command history from the command polling buffer. See
            chapter on Advanced Feature for all details regarding polling

        Parameters :
           - cmd_name  : (str) Command name.
           - depth     : (int) The wanted history depth.
        Return     : This method returns a vector of DeviceDataHistory types.

        Throws     : NonSupportedFeature, ConnectionFailed,
                     CommunicationFailed, DevFailed from device
    """,
    )

    document_method(
        "attribute_history",
        """
    attribute_history(self, attr_name, depth, extract_as=ExtractAs.Numpy) -> sequence<DeviceAttributeHistory>

            Retrieve attribute history from the attribute polling buffer. See
            chapter on Advanced Feature for all details regarding polling

        Parameters :
           - attr_name  : (str) Attribute name.
           - depth      : (int) The wanted history depth.
           - extract_as : (ExtractAs)

        Return     : This method returns a vector of DeviceAttributeHistory types.

        Throws     : NonSupportedFeature, ConnectionFailed,
                     CommunicationFailed, DevFailed from device
    """,
    )

    # -------------------------------------
    #   Polling administration methods
    # -------------------------------------

    document_method(
        "polling_status",
        """
    polling_status(self) -> sequence<str>

            Return the device polling status.

        Parameters : None
        Return     : (sequence<str>) One string for each polled command/attribute.
                     Each string is multi-line string with:

                        - attribute/command name
                        - attribute/command polling period in milliseconds
                        - attribute/command polling ring buffer
                        - time needed for last attribute/command execution in milliseconds
                        - time since data in the ring buffer has not been updated
                        - delta time between the last records in the ring buffer
                        - exception parameters in case of the last execution failed
    """,
    )

    document_method(
        "poll_command",
        """
    poll_command(self, cmd_name, period) -> None

            Add a command to the list of polled commands.

        Parameters :
            - cmd_name : (str) command name
            - period   : (int) polling period in milliseconds
        Return     : None
    """,
    )

    document_method(
        "poll_attribute",
        """
    poll_attribute(self, attr_name, period) -> None

            Add an attribute to the list of polled attributes.

        Parameters :
            - attr_name : (str) attribute name
            - period    : (int) polling period in milliseconds
        Return     : None
    """,
    )

    document_method(
        "get_command_poll_period",
        """
    get_command_poll_period(self, cmd_name) -> int

            Return the command polling period.

        Parameters :
            - cmd_name : (str) command name
        Return     : polling period in milliseconds
    """,
    )

    document_method(
        "get_attribute_poll_period",
        """
    get_attribute_poll_period(self, attr_name) -> int

            Return the attribute polling period.

        Parameters :
            - attr_name : (str) attribute name
        Return     : polling period in milliseconds
    """,
    )

    document_method(
        "is_command_polled",
        """
    is_command_polled(self, cmd_name) -> bool

        True if the command is polled.

        :param str cmd_name: command name

        :returns: boolean value
        :rtype: bool

    """,
    )

    document_method(
        "is_attribute_polled",
        """
    is_attribute_polled(self, attr_name) -> bool

        True if the attribute is polled.

        :param str attr_name: attribute name

        :returns: boolean value
        :rtype: bool
    """,
    )

    document_method(
        "stop_poll_command",
        """
    stop_poll_command(self, cmd_name) -> None

            Remove a command from the list of polled commands.

        Parameters :
            - cmd_name : (str) command name
        Return     : None
    """,
    )

    document_method(
        "stop_poll_attribute",
        """
    stop_poll_attribute(self, attr_name) -> None

            Remove an attribute from the list of polled attributes.

        Parameters :
            - attr_name : (str) attribute name
        Return     : None
    """,
    )

    # -------------------------------------
    #   Asynchronous methods
    # -------------------------------------

    document_method(
        "pending_asynch_call",
        """
    pending_asynch_call(self) -> int

            Return number of device asynchronous pending requests"

        New in PyTango 7.0.0
    """,
    )

    # ------------------------------------
    #   Logging administration methods
    # ------------------------------------

    document_method(
        "add_logging_target",
        """
    add_logging_target(self, target_type_target_name) -> None

            Adds a new logging target to the device.

            The target_type_target_name input parameter must follow the
            format: target_type::target_name. Supported target types are:
            console, file and device. For a device target, the target_name
            part of the target_type_target_name parameter must contain the
            name of a log consumer device (as defined in A.8). For a file
            target, target_name is the full path to the file to log to. If
            omitted, the device's name is used to build the file name
            (which is something like domain_family_member.log). Finally, the
            target_name part of the target_type_target_name input parameter
            is ignored in case of a console target and can be omitted.

        Parameters :
            - target_type_target_name : (str) logging target
        Return     : None

        Throws     : DevFailed from device

        New in PyTango 7.0.0
    """,
    )

    document_method(
        "remove_logging_target",
        """
    remove_logging_target(self, target_type_target_name) -> None

            Removes a logging target from the device's target list.

            The target_type_target_name input parameter must follow the
            format: target_type::target_name. Supported target types are:
            console, file and device. For a device target, the target_name
            part of the target_type_target_name parameter must contain the
            name of a log consumer device (as defined in ). For a file
            target, target_name is the full path to the file to remove.
            If omitted, the default log file is removed. Finally, the
            target_name part of the target_type_target_name input parameter
            is ignored in case of a console target and can be omitted.
            If target_name is set to '*', all targets of the specified
            target_type are removed.

        Parameters :
            - target_type_target_name : (str) logging target
        Return     : None

        New in PyTango 7.0.0
    """,
    )

    document_method(
        "get_logging_target",
        """
    get_logging_target(self) -> sequence<str>

            Returns a sequence of string containing the current device's
            logging targets. Each vector element has the following format:
            target_type::target_name. An empty sequence is returned is the
            device has no logging targets.

        Parameters : None
        Return     : a squence<str> with the logging targets

        New in PyTango 7.0.0
    """,
    )

    document_method(
        "get_logging_level",
        """
    get_logging_level(self) -> int

            Returns the current device's logging level, where:
                - 0=OFF
                - 1=FATAL
                - 2=ERROR
                - 3=WARNING
                - 4=INFO
                - 5=DEBUG

        Parameters :None
        Return     : (int) representing the current logging level

        New in PyTango 7.0.0
    """,
    )

    document_method(
        "set_logging_level",
        """
    set_logging_level(self, (int)level) -> None

            Changes the device's logging level, where:
                - 0=OFF
                - 1=FATAL
                - 2=ERROR
                - 3=WARNING
                - 4=INFO
                - 5=DEBUG

        Parameters :
            - level : (int) logging level
        Return     : None

        New in PyTango 7.0.0
    """,
    )

    # ------------------------------------
    #   Event methods
    # ------------------------------------

    # subscribe_event -> in code
    # unsubscribe_event -> in code
    # get_events -> in code

    document_method(
        "event_queue_size",
        """
    event_queue_size(self, event_id) -> int

            Returns the number of stored events in the event reception
            buffer. After every call to DeviceProxy.get_events(), the event
            queue size is 0. During event subscription the client must have
            chosen the 'pull model' for this event. event_id is the event
            identifier returned by the DeviceProxy.subscribe_event() method.

        Parameters :
            - event_id : (int) event identifier
        Return     : an integer with the queue size

        Throws     : EventSystemFailed

        New in PyTango 7.0.0
    """,
    )

    document_method(
        "get_last_event_date",
        """
    get_last_event_date(self, event_id) -> TimeVal

            Returns the arrival time of the last event stored in the event
            reception buffer. After every call to DeviceProxy:get_events(),
            the event reception buffer is empty. In this case an exception
            will be returned. During event subscription the client must have
            chosen the 'pull model' for this event. event_id is the event
            identifier returned by the DeviceProxy.subscribe_event() method.

        Parameters :
            - event_id : (int) event identifier
        Return     : (tango.TimeVal) representing the arrival time

        Throws     : EventSystemFailed

        New in PyTango 7.0.0
    """,
    )

    document_method(
        "is_event_queue_empty",
        """
    is_event_queue_empty(self, event_id) -> bool

            Returns true when the event reception buffer is empty. During
            event subscription the client must have chosen the 'pull model'
            for this event. event_id is the event identifier returned by the
            DeviceProxy.subscribe_event() method.

            Parameters :
                - event_id : (int) event identifier
            Return     : (bool) True if queue is empty or False otherwise

            Throws     : EventSystemFailed

            New in PyTango 7.0.0
    """,
    )

    # ------------------------------------
    #   Locking methods
    # ------------------------------------
    document_method(
        "lock",
        """
    lock(self, (int)lock_validity) -> None

            Lock a device. The lock_validity is the time (in seconds) the
            lock is kept valid after the previous lock call. A default value
            of 10 seconds is provided and should be fine in most cases. In
            case it is necessary to change the lock validity, it's not
            possible to ask for a validity less than a minimum value set to
            2 seconds. The library provided an automatic system to
            periodically re lock the device until an unlock call. No code is
            needed to start/stop this automatic re-locking system. The
            locking system is re-entrant. It is then allowed to call this
            method on a device already locked by the same process. The
            locking system has the following features:

              * It is impossible to lock the database device or any device
                server process admin device
              * Destroying a locked DeviceProxy unlocks the device
              * Restarting a locked device keeps the lock
              * It is impossible to restart a device locked by someone else
              * Restarting a server breaks the lock

            A locked device is protected against the following calls when
            executed by another client:

              * command_inout call except for device state and status
                requested via command and for the set of commands defined as
                allowed following the definition of allowed command in the
                Tango control access schema.
              * write_attribute call
              * write_read_attribute call
              * set_attribute_config call

        Parameters :
            - lock_validity : (int) lock validity time in seconds
                                (optional, default value is
                                tango.constants.DEFAULT_LOCK_VALIDITY)
        Return     : None

        New in PyTango 7.0.0
    """,
    )

    document_method(
        "unlock",
        """
    unlock(self, (bool)force) -> None

            Unlock a device. If used, the method argument provides a back
            door on the locking system. If this argument is set to true,
            the device will be unlocked even if the caller is not the locker.
            This feature is provided for administration purpopse and should
            be used very carefully. If this feature is used, the locker will
            receive a DeviceUnlocked during the next call which is normally
            protected by the locking Tango system.

        Parameters :
            - force : (bool) force unlocking even if we are not the
                      locker (optional, default value is False)
        Return     : None

        New in PyTango 7.0.0
    """,
    )

    document_method(
        "locking_status",
        """
    locking_status(self) -> str

            This method returns a plain string describing the device locking
            status. This string can be:

              * 'Device <device name> is not locked' in case the device is
                not locked
              * 'Device <device name> is locked by CPP or Python client with
                PID <pid> from host <host name>' in case the device is
                locked by a CPP client
              * 'Device <device name> is locked by JAVA client class
                <main class> from host <host name>' in case the device is
                locked by a JAVA client

        Parameters : None
        Return     : a string representing the current locking status

        New in PyTango 7.0.0"
    """,
    )

    document_method(
        "is_locked",
        """
    is_locked(self) -> bool

            Returns True if the device is locked. Otherwise, returns False.

        Parameters : None
        Return     : (bool) True if the device is locked. Otherwise, False

        New in PyTango 7.0.0
    """,
    )

    document_method(
        "is_locked_by_me",
        """
    is_locked_by_me(self) -> bool

            Returns True if the device is locked by the caller. Otherwise,
            returns False (device not locked or locked by someone else)

        Parameters : None
        Return     : (bool) True if the device is locked by us.
                        Otherwise, False

        New in PyTango 7.0.0
    """,
    )

    document_method(
        "get_locker",
        """
    get_locker(self, lockinfo) -> bool

            If the device is locked, this method returns True an set some
            locker process informations in the structure passed as argument.
            If the device is not locked, the method returns False.

        Parameters :
            - lockinfo [out] : (tango.LockInfo) object that will be filled
                                with lock informantion
        Return     : (bool) True if the device is locked by us.
                     Otherwise, False

        New in PyTango 7.0.0
    """,
    )


def device_proxy_init(doc=True):
    __init_DeviceProxy()
    if doc:
        __doc_DeviceProxy()
