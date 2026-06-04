# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""This module exposes a futures version of :class:`tango.DeviceProxy` and
:class:`tango.AttributeProxy"""

__all__ = ("AttributeProxy", "DeviceProxy")

from functools import partial

from tango import GreenMode
from tango.attribute_proxy import get_attribute_proxy
from tango.device_proxy import get_device_proxy

DeviceProxy = partial(get_device_proxy, green_mode=GreenMode.Futures)
DeviceProxy.__doc__ = """
    DeviceProxy(self, dev_name: str, wait: bool=False, timeout: float=None) -> DeviceProxy
    DeviceProxy(self, dev_name: str, need_check_acc: bool, wait: bool=False, timeout: float=None) -> DeviceProxy

    Creates a *futures* enabled :class:`~tango.DeviceProxy`.

    The DeviceProxy constructor internally makes some network calls which makes
    it *slow*. By using the futures *green mode* you are allowing other
    python code to be executed in a cooperative way.

    .. note::
        The timeout parameter has no relation with the tango device client side
        timeout (gettable by :meth:`~tango.DeviceProxy.get_timeout_millis` and
        settable through :meth:`~tango.DeviceProxy.set_timeout_millis`)

    :param dev_name: the device name or alias
    :type dev_name: str
    :param need_check_acc: (optional, default is True)
                           Determines if at creation time of DeviceProxy it
                           should check for channel access (rarely used)
    :type need_check_acc: bool
    :param wait: whether or not to wait for result of creating a DeviceProxy.
    :type wait: bool
    :param timeout: The number of seconds to wait for the result.
                    If None, then there is no limit on the wait time.
                    Ignored when wait is False.
    :type timeout: float
    :returns:
        if wait is True:
            :class:`~tango.DeviceProxy`
        else:
            :class:`concurrent.futures.Future`
    :throws: :obj:`~tango.DevFailed` if wait is True and there is an error creating the device. \n
             :obj:`concurrent.futures.TimeoutError` if wait is False, timeout is not None
                                                    and the time to create the device has expired.

    .. versionadded:: 8.1.0
"""

AttributeProxy = partial(get_attribute_proxy, green_mode=GreenMode.Futures)
AttributeProxy.__doc__ = """
    AttributeProxy(self, full_attr_name: str, wait: bool=False, timeout: float=None) -> AttributeProxy
    AttributeProxy(self, device_proxy: DeviceProxy, attr_name: str, wait: bool=False, timeout: float=None) -> AttributeProxy

    Creates a *futures* enabled :class:`~tango.AttributeProxy`.

    The AttributeProxy constructor internally makes some network calls which
    makes it *slow*. By using the *gevent mode* you are allowing other python
    code to be executed in a cooperative way.

    :param full_attr_name: the full name of the attribute
    :type full_attr_name: str
    :param device_proxy: the :class:`~tango.DeviceProxy`
    :type device_proxy: DeviceProxy
    :param attr_name: attribute name for the given device proxy
    :type attr_name: str
    :param wait: whether or not to wait for result of creating an
                 AttributeProxy.
    :type wait: bool
    :param timeout: The number of seconds to wait for the result.
                    If None, then there is no limit on the wait time.
                    Ignored when wait is False.
    :type timeout: float
    :returns:
        if wait is True:
            :class:`~tango.AttributeProxy`
        else:
            :class:`concurrent.futures.Future`
    :throws: :obj:`~tango.DevFailed` if wait is True  and there is an error creating the attribute. \n
             :obj:`concurrent.futures.TimeoutError` if wait is False, timeout is not None
                                                    and the time to create the attribute has expired.

    .. versionadded:: 8.1.0
"""

Device = DeviceProxy
Attribute = AttributeProxy

del GreenMode
del get_device_proxy
del get_attribute_proxy
