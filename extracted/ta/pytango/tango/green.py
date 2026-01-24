# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later


# Imports
import os
import inspect
import textwrap
import re

from functools import wraps

from threading import get_ident

# Tango imports
from tango._tango import GreenMode
from tango.utils import _forcefully_traced_method

__all__ = (
    "get_green_mode",
    "set_green_mode",
    "green",
    "green_callback",
    "get_executor",
    "get_object_executor",
    "switch_existing_global_executors_to_thread",
)

try:
    import gevent

    del gevent
    _gevent_available = True
except ImportError:
    _gevent_available = False

# Handle current green mode

try:
    _CURRENT_GREEN_MODE = getattr(
        GreenMode, os.environ["PYTANGO_GREEN_MODE"].capitalize()
    )
except Exception:
    _CURRENT_GREEN_MODE = GreenMode.Synchronous


def set_green_mode(green_mode=None):
    """Sets the global default PyTango green mode.

    Advice: Use only in your final application. Don't use this in a python
    library in order not to interfere with the beavior of other libraries
    and/or application where your library is being.

    :param green_mode: the new global default PyTango green mode
    :type green_mode: GreenMode
    """
    global _CURRENT_GREEN_MODE
    # Make sure the green mode is available
    get_executor(green_mode)
    # Set the green mode
    _CURRENT_GREEN_MODE = green_mode


def get_green_mode():
    """Returns the current global default PyTango green mode.

    :returns: the current global default PyTango green mode
    :rtype: GreenMode
    """
    return _CURRENT_GREEN_MODE


# Abstract executor class


class AbstractExecutor:
    asynchronous = NotImplemented
    default_wait = NotImplemented

    def __init__(self):
        self.ident = get_ident(), os.getpid()

    def get_ident(self):
        return self.ident

    def in_executor_context(self):
        return self.ident == (get_ident(), os.getpid())

    def delegate(self, fn, *args, **kwargs):
        """Delegate an operation and return an accessor."""
        if not self.asynchronous:
            raise ValueError("Not supported in synchronous mode")
        raise NotImplementedError

    def access(self, accessor, timeout=None):
        """Return a result from an accessor."""
        if not self.asynchronous:
            raise ValueError("Not supported in synchronous mode")
        raise NotImplementedError

    def submit(self, fn, *args, **kwargs):
        """Submit an operation"""
        if not self.asynchronous:
            return fn(*args, **kwargs)
        raise NotImplementedError

    def execute(self, fn, *args, **kwargs):
        """Execute an operation and return the result."""
        if not self.asynchronous:
            return fn(*args, **kwargs)
        raise NotImplementedError

    def run(self, fn, args=(), kwargs={}, wait=None, timeout=None):
        if wait is None:
            wait = self.default_wait
        # Wait and timeout are not supported in synchronous mode
        if not self.asynchronous and (not wait or timeout):
            raise ValueError("Not supported in synchronous mode")
        # Synchronous (no delegation)
        if not self.asynchronous or not self.in_executor_context():
            return fn(*args, **kwargs)
        # Asynchronous delegation
        accessor = self.delegate(fn, *args, **kwargs)
        if not wait:
            return accessor
        return self.access(accessor, timeout=timeout)


class SynchronousExecutor(AbstractExecutor):
    asynchronous = False
    default_wait = True


# Default synchronous executor


def get_synchronous_executor():
    return _SYNCHRONOUS_EXECUTOR


_SYNCHRONOUS_EXECUTOR = SynchronousExecutor()


# Getters


def get_object_green_mode(obj):
    if hasattr(obj, "get_green_mode"):
        return obj.get_green_mode()
    return get_green_mode()


def get_executor(green_mode=None):
    if green_mode is None:
        green_mode = get_green_mode()
    # Valid green modes
    if green_mode == GreenMode.Synchronous:
        return get_synchronous_executor()
    if green_mode == GreenMode.Gevent:
        from tango import gevent_executor

        return gevent_executor.get_global_executor()
    if green_mode == GreenMode.Futures:
        from tango import futures_executor

        return futures_executor.get_global_executor()
    if green_mode == GreenMode.Asyncio:
        from tango import asyncio_executor

        return asyncio_executor.get_global_executor()
    # Invalid green mode
    raise TypeError("Not a valid green mode")


def switch_existing_global_executors_to_thread():
    """
    checks which global executor existing, and if they are belong to the caller thread
    if not - creates a new executor, linked to thread, and set it as global
    """
    from tango import asyncio_executor
    from tango import futures_executor

    if _gevent_available:
        from tango import gevent_executor
    else:
        gevent_executor = None

    for executor in [asyncio_executor, futures_executor, gevent_executor]:
        if executor:
            executor._switch_global_executor_to_thread()


def get_object_executor(obj, green_mode=None):
    """Returns the proper executor for the given object.

    If the object has *_executors* and *_green_mode* members it returns
    the submit callable for the executor corresponding to the green_mode.
    Otherwise it returns the global executor for the given green_mode.

    Note: *None* is a valid object.

    :returns: submit callable"""
    # Get green mode
    if green_mode is None:
        green_mode = get_object_green_mode(obj)
    # Get executor
    executor = None
    if hasattr(obj, "_executors"):
        executor = obj._executors.get(green_mode, None)
    if executor is None:
        executor = get_executor(green_mode)
    # Get submitter
    return executor


# Green modifiers


def green(fn=None, consume_green_mode=True, update_signature_and_docstring=False):
    """Make a function green. Can be used as a decorator."""

    def decorator(fn):
        @wraps(fn)
        def greener(obj, *args, **kwargs):
            args = (obj,) + args
            wait = kwargs.pop("wait", None)
            timeout = kwargs.pop("timeout", None)
            access = kwargs.pop if consume_green_mode else kwargs.get
            green_mode = access("green_mode", None)
            executor = get_object_executor(obj, green_mode)
            return executor.run(fn, args, kwargs, wait=wait, timeout=timeout)

        sig = inspect.signature(fn)

        if update_signature_and_docstring:

            # Build green parameters
            green_mode_param = inspect.Parameter(
                "green_mode",
                kind=inspect.Parameter.KEYWORD_ONLY,
                default=None,
                annotation=None,
            )

            wait_param = inspect.Parameter(
                "wait",
                kind=inspect.Parameter.KEYWORD_ONLY,
                default=None,
                annotation=None,
            )

            timeout_param = inspect.Parameter(
                "timeout",
                kind=inspect.Parameter.KEYWORD_ONLY,
                default=None,
                annotation=None,
            )

            # Append it to the existing parameters
            old_params = list(sig.parameters.values())
            add_kwargs = False
            if old_params[-1].kind == inspect.Parameter.VAR_KEYWORD:
                old_params = old_params[:-1]
                add_kwargs = True

            if "green_mode" in [param.name for param in old_params]:
                new_params = old_params + [wait_param, timeout_param]
            else:
                new_params = old_params + [green_mode_param, wait_param, timeout_param]

            if add_kwargs:
                new_params += [
                    inspect.Parameter("kwargs", kind=inspect.Parameter.VAR_KEYWORD)
                ]

            new_sig = sig.replace(parameters=new_params)

            if greener.__doc__ is not None:
                fill_green_doc(greener)

            greener.__signature__ = new_sig

        else:
            greener.__signature__ = sig

        return greener

    if fn is None:
        return decorator
    return decorator(fn)


def green_callback(fn, obj=None, green_mode=None):
    """Return a green verion of the given callback."""
    executor = get_object_executor(obj, green_mode)

    @wraps(fn)
    def greener(*args, **kwargs):
        return executor.submit(_forcefully_traced_method(fn), *args, **kwargs)

    return greener


__GREEN_KWARGS__ = "green_mode=None, wait=True, timeout=None"
__GREEN_KWARGS_DESCRIPTION__ = """
:param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
:type green_mode: :obj:`tango.GreenMode`, optional

:param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
:type wait: bool, optional

:param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
:type timeout: float, optional
"""
__GREEN_RAISES__ = """
:throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
:throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.
"""


def fill_green_doc(method):
    """
    Replace the __GREEN_KWARGS__ __GREEN_KWARGS_DESCRIPTION__ placeholders in `doc`
    preserving the placeholder’s indentation.
    """

    dedented = textwrap.dedent(method.__doc__)
    dedented = dedented.replace("__GREEN_KWARGS__", __GREEN_KWARGS__)

    m = re.search(
        r"^(?P<indent>[ \t]*)__GREEN_KWARGS_DESCRIPTION__", dedented, flags=re.MULTILINE
    )
    if not m:
        return

    indent = m.group("indent")

    indented_desc = textwrap.indent(__GREEN_KWARGS_DESCRIPTION__.strip("\n"), indent)
    indented_raises = textwrap.indent(__GREEN_RAISES__.strip("\n"), indent)

    dedented = re.sub(
        r"^[ \t]*__GREEN_KWARGS_DESCRIPTION__",
        indented_desc,
        dedented,
        flags=re.MULTILINE,
    )

    method.__doc__ = re.sub(
        r"^[ \t]*__GREEN_RAISES__", indented_raises, dedented, flags=re.MULTILINE
    )
