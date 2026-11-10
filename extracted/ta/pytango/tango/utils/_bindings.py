# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Glue between python and the C++ bindings."""

import collections.abc
import functools
import inspect
import sys
import time
import types

from tango import (
    CmdArgType,
    Database,
    DevFailed,
    DeviceData,
    DeviceDataList,
    DeviceProxy,
    ErrSeverity,
    Except,
    __auto_die_callbacks_holder,
)
from tango._tango import __CallBackAutoDie, __Group


def _is_coroutine_function(obj):
    while isinstance(obj, functools.partial):
        obj = obj.func

    return inspect.iscoroutinefunction(obj) or (callable(obj) and inspect.iscoroutinefunction(obj.__call__))


def _get_new_CallbackAutoDie():
    id = time.time_ns()
    cb = __CallBackAutoDie(id)
    __auto_die_callbacks_holder[id] = cb
    return cb


def _release_CallbackAutoDie(id):
    if id in __auto_die_callbacks_holder:
        del __auto_die_callbacks_holder[id]


def _get_command_inout_param(self, cmd_name, cmd_param=None):
    if cmd_param is None:
        return DeviceData()

    if isinstance(cmd_param, DeviceData):
        return cmd_param

    if isinstance(self, DeviceProxy):
        # This is not part of 'Connection' interface, but
        # DeviceProxy only.
        info = self.command_query(cmd_name)
        param = DeviceData()
        try:
            param.insert(info.in_type, cmd_param)
        except TypeError as err:
            raise TypeError(
                f"Invalid input argument for command {cmd_name}: "
                f"{cmd_param!r} cannot be converted to type {info.in_type}"
            ) from err
        return param
    elif isinstance(self, __Group):
        if self.get_size() == 0:
            return DeviceData()

        if isinstance(cmd_param, DeviceDataList):
            return cmd_param

        last_cause = None
        try:
            types = set()
            typ = None
            for idx in range(1, self.get_size() + 1):
                dev = self.get_device(idx)
                try:
                    typ = dev.command_query(cmd_name).in_type
                    types.add(typ)
                except DevFailed as df:
                    last_cause = df
            if not types:
                if last_cause:
                    Except.re_throw_exception(
                        last_cause,
                        "PyAPI_GroupCommandArgInTypeUnknown",
                        "Cannot fetch at least one command type in group.",
                        "Group.command_inout_asynch",
                    )
                else:
                    Except.throw_exception(
                        "PyAPI_GroupCommandArgInTypeUnknown",
                        "Cannot fetch at least one command type in group. Unknown cause.",
                        "Group.command_inout_asynch",
                    )
            elif len(types) > 1:
                raise TypeError(f"Cannot execute command with more than one type in group, types are:\n{types}")
        finally:
            del last_cause

        param = DeviceData()
        try:
            param.insert(typ, cmd_param)
        except TypeError as err:
            raise TypeError(
                f"Invalid input argument for command {cmd_name}: {cmd_param!r} cannot be converted to type {typ}"
            ) from err
        return param

    elif isinstance(self, Database):
        # I just try to guess types DevString and DevVarStringArray
        # as they are used for Database
        param = DeviceData()
        if isinstance(cmd_param, str):
            param.insert(CmdArgType.DevString, cmd_param)
            return param
        elif isinstance(cmd_param, collections.abc.Sequence) and all(isinstance(x, str) for x in cmd_param):
            param.insert(CmdArgType.DevVarStringArray, cmd_param)
            return param
        else:
            raise TypeError(
                "command_inout() parameter must be a DeviceData object or a string or a sequence of strings"
            )
    else:
        raise TypeError("command_inout() parameter must be a DeviceData object.")


def _exception_converter(exception):

    # if user managed to create DevFailed, we do not need to convert it
    if isinstance(exception, DevFailed):
        return exception
    else:
        if exception.__traceback__ is None:
            # to generate DevFailed we need traceback
            # if user does not provide one (Exception.with_traceback), we generate our
            try:
                raise Exception()
            except Exception:
                # to get to the frame, where user called push_event
                traceback = sys.exc_info()[2]
                try:
                    user_frame = traceback.tb_frame.f_back.f_back
                    exception.__traceback__ = types.TracebackType(
                        None, user_frame, user_frame.f_lasti, user_frame.f_lineno
                    )
                except Exception:
                    # if fails, use what we have
                    try:
                        Except.throw_exception(
                            reason="PyDs_PythonError",
                            description=repr(exception),
                            origin="UNKNOWN: cannot get Python's traceback",
                            severity=ErrSeverity.ERR,
                        )
                    except DevFailed as err:
                        return err
        return Except.to_dev_failed(exception.__class__, exception, exception.__traceback__)


class _InterfaceDefinedByIDL:
    _initialized = False

    def __setattr__(self, name, value):
        if name not in self.__dict__ and self._initialized:
            raise AttributeError(f"tango._tango.{self.__class__.__name__} object has no attribute '{name}'")

        return super().__setattr__(name, value)


def _check_only_allowed_kwargs(call_kwargs, allowed_keys):
    unexpected_keys = call_kwargs.keys() - allowed_keys
    if unexpected_keys:
        raise TypeError(
            f"Got unexpected keyword argument(s): {', '.join(unexpected_keys)}.\n"
            f"Allowed keys are: {', '.join(sorted(allowed_keys))}"
        )


# Helper class to replace deprecated object
class _RemovedClass:
    def __init__(self, message):
        self._message = message

    def _trigger_error(self, *args, **kwargs):
        raise AttributeError(self._message)

    __getattr__ = _trigger_error
    __call__ = _trigger_error
    __getitem__ = _trigger_error
