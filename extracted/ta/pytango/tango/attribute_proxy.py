# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
"""
This is an internal PyTango module. It completes the binding of
:class:`tango.AttributeProxy`.

To access these members use directly :mod:`tango` module and NOT
tango.attribute_proxy.
"""

import contextlib
import inspect

from tango._instrumentation import _trace_client
from tango._tango import (
    DbData,
    DbDatum,
    DevFailed,
    DeviceProxy,
    Except,
)
from tango._tango import __AttributeProxy as _AttributeProxy
from tango.device_proxy import __init_device_proxy_internals as init_device_proxy
from tango.green import get_green_mode, green
from tango.utils import _get_device_fqtrl_if_necessary, get_property_from_db, parameter_2_dbdata

__all__ = ("AttributeProxy", "attribute_proxy_init", "get_attribute_proxy")


@green(consume_green_mode=False)
@_trace_client
def get_attribute_proxy(*args, green_mode=None):
    """
    get_attribute_proxy(self, full_attr_name: str, green_mode: GreenMode=None, wait: bool=True, timeout: float=None) -> AttributeProxy
    get_attribute_proxy(self, device_proxy: DeviceProxy, attr_name: str, green_mode: GreenMode=None, wait: bool=True, timeout: float=None) -> AttributeProxy

    Returns a new :class:`~tango.AttributeProxy`.
    There is no difference between using this function and the direct
    :class:`~tango.AttributeProxy` constructor if you use the default kwargs.

    The added value of this function becomes evident when you choose a green_mode
    to be *Futures* or *Gevent*. The AttributeProxy constructor internally makes some
    network calls which makes it *slow*. By using one of the *green modes* as
    green_mode you are allowing other python code to be executed in a cooperative way.

    :param full_attr_name: the full name of the attribute
    :type full_attr_name: :py:obj:`str`
    :param device_proxy: the :class:`~tango.DeviceProxy`
    :type device_proxy: :py:obj:`~tango.DeviceProxy`
    :param attr_name: attribute name for the given device proxy
    :type attr_name: :py:obj:`str`
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
            :class:`~tango.AttributeProxy`
        elif green_mode is Futures:
            :class:`concurrent.futures.Future`
        elif green_mode is Gevent:
            :class:`gevent.event.AsynchResult`
        elif green_mode is Asyncio:
            :class:`asyncio.Future`
    :throws: :obj:`~tango.DevFailed` if green_mode is Synchronous or wait is True
                and there is an error creating the proxy.
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
    return AttributeProxy(*args, green_mode=green_mode)


def __AttributeProxy__get_property(
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
                    4. :py:obj:`list`\\[:py:obj:`str` | :py:obj:`bytes`] [in] - Several property data to be fetched. \n
                    5. :py:obj:`list`\\[:py:obj:`tango.DbDatum`] [in] - Several property data to be fetched. \n
                    6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] [in] - Keys are property names
                       to be fetched (values are ignored). \n
                    7. :py:obj:`dict`\\[:py:obj:`str`, :obj:`tango.DbDatum`] [in] - Several `DbDatum.name` are
                       property names to be fetched (keys are ignored). \n

    :param value: Optional. For propname overloads with :py:obj:`str` and :py:obj:`list`\\[:py:obj:`str`] will be filed
                   with the property values, if provided.
    :type value: :obj:`tango.DbData`, optional

    :returns: A :py:obj:`dict` object, which keys are the property names the value
              associated with each key being a sequence of strings being the
              property value.

    :throws:
        :py:obj:`TypeError`: Raised in case of propname has the wrong type. \n
        :py:obj:`tango.NonDbDevice`: Raised in case of a non-database device error. \n
        :py:obj:`tango.ConnectionFailed`: Raised on connection failure with the database. \n
        :py:obj:`tango.CommunicationFailed`: Raised on communication failure with the database. \n
        :py:obj:`tango.DevFailed`: Raised on a device failure from the database device.`

    .. versionadded:: 10.1.0: overloads with :obj:`dict` as propname parameter

    .. versionchanged:: 10.1.0: raises if propname has an invalid type instead of returning None
    """

    return get_property_from_db(self, propname, value)


def __AttributeProxy__put_property(
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
                    4. :py:obj:`list`\\[:py:obj:`str` | :py:obj:`bytes` | :py:obj:`~tango.DbDatum`] - Several property
                       data to be inserted. \n
                    5. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`~tango.DbDatum`] -
                       DbDatum is property to be inserted (keys are ignored). \n
                    6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`list`\\[:py:obj:`str`]] - Keys are property names,
                       and value has data to be inserted. \n
                    7. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] - Keys are property names, and `str(obj)`
                       is property value.

    :throws:
        :py:obj:`TypeError`: Raised in case of value has the wrong type. \n
        :py:obj:`tango.NonDbDevice`: Raised in case of a non-database device error. \n
        :py:obj:`tango.ConnectionFailed`: Raised on connection failure with the database. \n
        :py:obj:`tango.CommunicationFailed`: Raised on communication failure with the database. \n
        :py:obj:`tango.DevFailed`: Raised on a device failure from the database device.`
    """
    value = parameter_2_dbdata(value, "value")
    return self._put_property(value)


def __AttributeProxy__delete_property(
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
                    4. :py:obj:`list`\\[:py:obj:`str` | :py:obj:`bytes` | :py:obj:`~tango.DbDatum`] [in] -
                       Several property data to be deleted. \n
                    5. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] [in] - Keys are property names
                       to be deleted (values are ignored). \n
                    6. :py:obj:`dict`\\[:py:obj:`str`, :obj:`tango.DbDatum`] [in] - Several `DbDatum.name` are
                       property names to be deleted (keys are ignored). \n

    :throws:
        :py:obj:`TypeError`: Raised in case of value has the wrong type. \n
        :py:obj:`tango.NonDbDevice`: Raised in case of a non-database device error. \n
        :py:obj:`tango.ConnectionFailed`: Raised on connection failure with the database. \n
        :py:obj:`tango.CommunicationFailed`: Raised on communication failure with the database. \n
        :py:obj:`tango.DevFailed`: Raised on a device failure from the database device.
    """

    new_value = parameter_2_dbdata(value, "value")
    return self._delete_property(new_value)


# It is easier to reimplement AttributeProxy in python using DeviceProxy than
# wrapping C++ AttributeProxy. However I still rely in the original
# AttributeProxy for the constructor (parsing strings if necessary) and some
# other things. With the _method_* functions defined later it is really easy.
# One reason to do it this way: get_device_proxy() will always return the
# same tango.DeviceProxy with this implementation. And then we can trust
# it's automatic event unsubscription to handle events.
class AttributeProxy:
    """
    AttributeProxy is the high level Tango object which provides the
    client with an easy-to-use interface to TANGO attributes.

    To create an AttributeProxy, a complete attribute name must be set
    in the object constructor.

    Example:
        att = AttributeProxy("tango/tangotest/1/long_scalar")

    Note: PyTango implementation of AttributeProxy is in part a
    python reimplementation of the AttributeProxy found on the C++ API.
    """

    @_trace_client
    def __init__(self, *args, green_mode=None):
        self.__initialized = False
        # If TestContext active, short TRL is replaced with fully-qualified
        # TRL, using test server's connection details.  Otherwise, left as-is.
        attr_name = args[0]
        new_attr_name = _get_device_fqtrl_if_necessary(attr_name)
        new_args = [new_attr_name, *args[1:]]
        try:
            self.__attr_proxy = _AttributeProxy(*new_args)
        except DevFailed as orig_err:
            if new_attr_name != attr_name:
                # If attribute was not found, it could be an attempt to access a real
                # device with a short name while running TestContext.  I.e., we need
                # to use the short name so that the real TANGO_HOST will be tried.
                try:
                    self.__attr_proxy = _AttributeProxy(*args)
                except DevFailed as retry_exc:
                    Except.re_throw_exception(
                        retry_exc,
                        "PyAPI_AttributeProxyInitFailed",
                        f"Failed to create AttributeProxy "
                        f"(tried {new_attr_name!r} => {orig_err.args[0].reason}, and "
                        f"{attr_name!r} => {retry_exc.args[0].reason})",
                        "AttributeProxy.__init__",
                    )
            else:
                raise
        # get_device_proxy() returns a different python object each time
        # we don't want a different object, so we save the current one.
        self.__dev_proxy = dp = self.__attr_proxy.get_device_proxy()
        init_device_proxy(dp)
        dp.__dict__["_green_mode"] = green_mode if green_mode is not None else get_green_mode()
        self.__initialized = True

    def get_device_proxy(self) -> DeviceProxy:
        """
        A method which returns the device associated to the attribute
        """
        return self.__dev_proxy

    def name(self) -> str:
        """
        Returns the attribute name
        """
        return self.__attr_proxy.name() if self.__initialized else "<Unknown: object was not fully initialized>"

    def __str__(self):
        return f"AttributeProxy({self.name()})"

    def __repr__(self):
        return f"AttributeProxy({self.name()})"


def _method_dev_and_name(dp_fn_name, doc=True):
    def __new_fn(self, *args, **kwds):
        return getattr(self._AttributeProxy__dev_proxy, dp_fn_name)(self.name(), *args, **kwds)

    if doc:
        __new_fn.__doc__ = (
            f"This method is a simple way to do::\n\n"
            f"\tself.get_device_proxy().{dp_fn_name}(self.name(), ...)\n\n"
            f"For convenience, here is the documentation of "
            f":meth:`tango.DeviceProxy.{dp_fn_name}`:\n\n"
            f"{getattr(DeviceProxy, dp_fn_name).__doc__}"
        )
    __new_fn.__name__ = dp_fn_name
    __new_fn.__qualname__ = f"AttributeProxy.{dp_fn_name}"
    return __new_fn


def _method_device(dp_fn_name, doc=True):
    def __new_fn(self, *args, **kwds):
        return getattr(self._AttributeProxy__dev_proxy, dp_fn_name)(*args, **kwds)

    if doc:
        __new_fn.__doc__ = (
            f"This method is a simple way to do::\n\n"
            f"\tself.get_device_proxy().{dp_fn_name}(...)\n\n"
            f"For convenience, here is the documentation of "
            f":meth:`tango.DeviceProxy.{dp_fn_name}`:\n\n"
            f"{getattr(DeviceProxy, dp_fn_name).__doc__}"
        )
    __new_fn.__name__ = dp_fn_name
    __new_fn.__qualname__ = f"AttributeProxy.{dp_fn_name}"
    with contextlib.suppress(ValueError):
        __new_fn.__signature__ = inspect.signature(getattr(DeviceProxy, dp_fn_name))

    return __new_fn


def _method_attribute(dp_fn_name, doc=True):
    def __new_fn(self, *args, **kwds):
        return getattr(self._AttributeProxy__attr_proxy, dp_fn_name)(*args, **kwds)

    if doc:
        __new_fn.__doc__ = getattr(_AttributeProxy, dp_fn_name).__doc__
    __new_fn.__name__ = dp_fn_name
    __new_fn.__qualname__ = f"AttributeProxy.{dp_fn_name}"
    return __new_fn


def attribute_proxy_init(doc=True):
    _AttributeProxy.get_property = __AttributeProxy__get_property
    _AttributeProxy.put_property = __AttributeProxy__put_property
    _AttributeProxy.delete_property = __AttributeProxy__delete_property

    # General methods
    # AttributeProxy.name                manually defined
    AttributeProxy.status = _method_device("status", doc=doc)
    AttributeProxy.state = _method_device("state", doc=doc)
    AttributeProxy.ping = _method_device("ping", doc=doc)
    AttributeProxy.get_transparency_reconnection = _method_device("get_transparency_reconnection", doc=doc)
    AttributeProxy.set_transparency_reconnection = _method_device("set_transparency_reconnection", doc=doc)

    # Property methods
    AttributeProxy.get_property = _trace_client(_method_attribute("get_property", doc=doc))
    AttributeProxy.put_property = _trace_client(_method_attribute("put_property", doc=doc))
    AttributeProxy.delete_property = _trace_client(_method_attribute("delete_property", doc=doc))

    # Attribute methods
    AttributeProxy.get_config = _method_dev_and_name("get_attribute_config", doc=doc)
    AttributeProxy.set_config = _method_device("set_attribute_config", doc=doc)

    AttributeProxy.write = _method_dev_and_name("write_attribute", doc=doc)
    AttributeProxy.read = _method_dev_and_name("read_attribute", doc=doc)
    AttributeProxy.write_read = _method_dev_and_name("write_read_attribute", doc=doc)

    # History methods...
    AttributeProxy.history = _method_dev_and_name("attribute_history", doc=doc)

    # Polling administration methods
    AttributeProxy.poll = _method_dev_and_name("poll_attribute", doc=doc)
    AttributeProxy.get_poll_period = _method_dev_and_name("get_attribute_poll_period", doc=doc)
    AttributeProxy.is_polled = _method_dev_and_name("is_attribute_polled", doc=doc)
    AttributeProxy.stop_poll = _method_dev_and_name("stop_poll_attribute", doc=doc)

    # Asynchronous methods
    AttributeProxy.read_asynch = _method_dev_and_name("read_attribute_asynch", doc=doc)
    AttributeProxy.read_reply = _method_device("read_attribute_reply", doc=doc)
    AttributeProxy.write_asynch = _method_dev_and_name("write_attribute_asynch", doc=doc)
    AttributeProxy.write_reply = _method_device("write_attribute_reply", doc=doc)

    # Event methods
    AttributeProxy.subscribe_event = _method_dev_and_name("subscribe_event", doc=doc)
    AttributeProxy.unsubscribe_event = _method_device("unsubscribe_event", doc=doc)

    AttributeProxy.get_events = _method_device("get_events", doc=doc)
    AttributeProxy.event_queue_size = _method_device("event_queue_size", doc=doc)
    AttributeProxy.get_last_event_date = _method_device("get_last_event_date", doc=doc)
    AttributeProxy.is_event_queue_empty = _method_device("is_event_queue_empty", doc=doc)
