# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.
"""

__all__ = ("connection_init",)

__docformat__ = "restructuredtext"


import collections.abc

from tango._tango import (
    Connection,
    DeviceData,
    ExtractAs,
)
from tango.utils import _trace_client, _get_command_inout_param
from tango.utils import _get_new_CallbackAutoDie
from tango.green import green


def __CallBack__cmd_ended_aux(self, fn):
    def __new_fn(cmd_done_event):
        try:
            cmd_done_event.argout = cmd_done_event.argout_raw.extract(
                self.defaultCommandExtractAs
            )
        except Exception:
            pass
        return fn(cmd_done_event)

    return __new_fn


def __Connection__command_inout(self, name, cmd_param=None):
    """
    command_inout( self, cmd_name, cmd_param=None, __GREEN_KWARGS__) -> any

        Execute a command on a device.

    :param cmd_name: Command name
    :type value: str

    :param cmd_param: It should be a value of the type expected by the command or a DeviceData object with this value inserted.
                      It can be omitted if the command should not get any argument.
    :type cmd_param: Any

    __GREEN_KWARGS_DESCRIPTION__

    :returns: The result of the command. The type depends on the command. It may be None
    :rtype: Any

    :throws: TypeError: if cmd_param's type is not compatible with the command
    :throws: :obj:`tango.ConnectionFailed`: Raised in case of a connection failure.
    :throws: :obj:`tango.CommunicationFailed`: Raised in case of a communication failure.
    :throws: :obj:`tango.DevFailed`: Raised in case of a device failure.
    :throws: :obj:`tango.DeviceUnlocked`: Raised in case of a device failure.
    __GREEN_RAISES__

    .. versionadded:: 8.1.0
        *green_mode* parameter.
        *wait* parameter.
        *timeout* parameter.

    .. versionchanged:: 10.0.0
        TypeError's for invalid command input arguments are now more detailed.
        For commands with a DEV_STRING input argument, invalid data will now raise TypeError instead of SystemError.
    """
    r = Connection.command_inout_raw(self, name, cmd_param)
    if isinstance(r, DeviceData):
        try:
            return r.extract(self.defaultCommandExtractAs)
        except Exception:
            return None
    else:
        return r


__Connection__command_inout.__name__ = "command_inout"


def __Connection__command_inout_raw(self, cmd_name, cmd_param=None):
    """
    command_inout_raw( self, cmd_name, cmd_param=None) -> DeviceData

        Execute a command on a device. Does not convert result.

    :param cmd_name: Command name
    :type value: str

    :param cmd_param: It should be a value of the type expected by the command or a DeviceData object with this value inserted.
                      It can be omitted if the command should not get any argument.
    :type cmd_param: Any

    :returns: The result of the command. The type depends on the command. It may be None
    :rtype: Any

    :throws: TypeError: if cmd_param's type is not compatible with the command
    :throws: :obj:`tango.ConnectionFailed`: Raised in case of a connection failure.
    :throws: :obj:`tango.CommunicationFailed`: Raised in case of a communication failure.
    :throws: :obj:`tango.DevFailed`: Raised in case of a device failure.
    :throws: :obj:`tango.DeviceUnlocked`: Raised in case of a device failure.

    .. versionchanged:: 10.0.0
        TypeError's for invalid command input arguments are now more detailed.
        For commands with a DEV_STRING input argument, invalid data will now raise TypeError instead of SystemError.
    """
    param = _get_command_inout_param(self, cmd_name, cmd_param)
    return self.__command_inout(cmd_name, param)


def __Connection__command_inout_asynch(self, cmd_name, *args):
    """
    command_inout_asynch(self, cmd_name) -> id
    command_inout_asynch(self, cmd_name, cmd_param) -> id
    command_inout_asynch(self, cmd_name, cmd_param, forget) -> id

            Execute asynchronously (polling model) a command on a device

        Parameters :
                - cmd_name  : (str) Command name.
                - cmd_param : (any) It should be a value of the type expected by the
                              command or a DeviceData object with this value inserted.
                              It can be omitted if the command should not get any argument.
                              If the command should get no argument and you want
                              to set the 'forget' param, use None for cmd_param.
                - forget    : (bool) If this flag is set to true, this means that the client
                              does not care at all about the server answer and will even
                              not try to get it. Default value is False. Please,
                              note that device re-connection will not take place (in case
                              it is needed) if the fire and forget mode is used. Therefore,
                              an application using only fire and forget requests is not able
                              to automatically re-connnect to device.
        Return     : (int) This call returns an asynchronous call identifier which is
                     needed to get the command result (see command_inout_reply)

        Throws     : ConnectionFailed, TypeError, anything thrown by command_query

    command_inout_asynch( self, cmd_name, callback) -> None
    command_inout_asynch( self, cmd_name, cmd_param, callback) -> None

            Execute asynchronously (callback model) a command on a device.

        Parameters :
                - cmd_name  : (str) Command name.
                - cmd_param : (any)It should be a value of the type expected by the
                              command or a DeviceData object with this value inserted.
                              It can be omitted if the command should not get any argument.
                - callback  : Any callable object (function, lambda...) or any oject
                              with a method named "cmd_ended".
        Return     : None

        Throws     : ConnectionFailed, TypeError, anything thrown by command_query

    .. important::
        by default, TANGO is initialized with the **polling** model. If you want
        to use the **push** model (the one with the callback parameter), you
        need to change the global TANGO model to PUSH_CALLBACK.
        You can do this with the :meth:`tango.ApiUtil.set_asynch_cb_sub_model`

    .. important::
        Multiple asynchronous calls are not guaranteed to be executed by the device
        server in the same order they are invoked by the client.  E.g., a call
        to ``command_inout_asynch("A")`` followed immediately with a call to
        ``command_inout_asynch("B")`` could result in the device invoking
        command ``B`` before command ``A``.

    .. versionchanged:: 10.0.0
        TypeError's for invalid command input arguments are now more detailed.
        For commands with a DEV_STRING input argument, invalid data will now raise TypeError instead of SystemError.
    """
    if len(args) == 0:  # command_inout_asynch()
        argin = DeviceData()
        forget = False
        return self.__command_inout_asynch_id(cmd_name, argin, forget)
    elif len(args) == 1:
        if isinstance(
            args[0], collections.abc.Callable
        ):  # command_inout_asynch(lambda)
            cb = _get_new_CallbackAutoDie()
            cb.cmd_ended = args[0]
            argin = _get_command_inout_param(self, cmd_name)
            return self.__command_inout_asynch_cb(cmd_name, argin, cb)
        elif hasattr(args[0], "cmd_ended"):  # command_inout_asynch(Cbclass)
            cb = _get_new_CallbackAutoDie()
            cb.cmd_ended = args[0].cmd_ended
            argin = _get_command_inout_param(self, cmd_name)
            return self.__command_inout_asynch_cb(cmd_name, argin, cb)
        else:  # command_inout_asynch(value)
            argin = _get_command_inout_param(self, cmd_name, args[0])
            forget = False
            return self.__command_inout_asynch_id(cmd_name, argin, forget)
    elif len(args) == 2:
        if isinstance(
            args[1], collections.abc.Callable
        ):  # command_inout_asynch( value, lambda)
            cb = _get_new_CallbackAutoDie()
            cb.cmd_ended = args[1]
            argin = _get_command_inout_param(self, cmd_name, args[0])
            return self.__command_inout_asynch_cb(cmd_name, argin, cb)
        elif hasattr(args[1], "cmd_ended"):  # command_inout_asynch(value, cbClass)
            cb = _get_new_CallbackAutoDie()
            cb.cmd_ended = args[1].cmd_ended
            argin = _get_command_inout_param(self, cmd_name, args[0])
            return self.__command_inout_asynch_cb(cmd_name, argin, cb)
        else:  # command_inout_asynch(value, forget)
            argin = _get_command_inout_param(self, cmd_name, args[0])
            forget = bool(args[1])
            return self.__command_inout_asynch_id(cmd_name, argin, forget)
    else:
        raise TypeError("Wrong number of attributes!")


__Connection__command_inout_asynch.__name__ = "command_inout_asynch"


def __Connection__command_inout_reply(self, idx, timeout=None):
    """
    command_inout_reply(self, idx, timeout=None) -> DeviceData

            Check if the answer of an asynchronous command_inout is arrived
            (polling model). If the reply is arrived and if it is a valid
            reply, it is returned to the caller in a DeviceData object. If
            the reply is an exception, it is re-thrown by this call. If optional
            `timeout` parameter is not provided an exception is also thrown in case
            of the reply is not yet arrived. If `timeout` is provided, the call will
            wait (blocking the process) for the time specified
            in timeout. If after timeout milliseconds, the reply is still
            not there, an exception is thrown. If timeout is set to 0, the
            call waits until the reply arrived.

        Parameters :
            - idx      : (int) Asynchronous call identifier.
            - timeout  : (int) (optional) Milliseconds to wait for the reply.
        Return     : (DeviceData)
        Throws     : AsynCall, AsynReplyNotArrived, CommunicationFailed, DevFailed from device
    """
    if timeout is None:
        r = self.command_inout_reply_raw(idx)
    else:
        r = self.command_inout_reply_raw(idx, timeout)

    if isinstance(r, DeviceData):
        try:
            return r.extract(self.defaultCommandExtractAs)
        except Exception:
            return None
    else:
        return r


__Connection__command_inout_reply.__name__ = "command_inout_reply"


def connection_init():
    Connection.defaultCommandExtractAs = ExtractAs.Numpy
    Connection.command_inout_raw = __Connection__command_inout_raw
    Connection.command_inout = green(
        _trace_client(__Connection__command_inout), update_signature_and_docstring=True
    )
    Connection.command_inout_asynch = _trace_client(__Connection__command_inout_asynch)
    Connection.command_inout_reply = _trace_client(__Connection__command_inout_reply)
