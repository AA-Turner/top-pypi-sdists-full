# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Internal support for direct high-level attribute handler access.

A runtime :class:`~tango.Attribute` knows which device it belongs to
(:meth:`~tango.Attribute.get_att_device`), so the handlers to call can always be
resolved from the attribute itself: statically declared
:class:`tango.server.attribute` objects are found on the device class, and
dynamically added ones are recorded on the device instance when they are added.
"""

from __future__ import annotations

import inspect
import weakref
from collections.abc import Callable

from tango._tango import Attribute, WAttribute
from tango.asyncio_executor import AsyncioExecutor

# Device class -> {lower case attribute name: high-level attribute descriptor}.
_class_descriptors: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()

# Name of the device instance attribute holding the handlers of the dynamically
# added high-level attributes: {lower case attribute name: handlers}.
_DYNAMIC_HANDLERS = "_tango_direct_handlers"


def _is_high_level_attribute(value) -> bool:
    return any(base.__module__ == "tango.server" and base.__name__ == "attribute" for base in value.__class__.__mro__)


def _unbound(method: Callable | None) -> Callable | None:
    if inspect.ismethod(method) and method.__self__ is not None:
        return method.__func__
    return method


def _unsupported_error(name: str) -> NotImplementedError:
    return NotImplementedError(
        f"Direct handler access is not available for attribute '{name}'; "
        "it is supported for high-level tango.server.attribute objects only"
    )


def _no_handler_error(kind: str, name: str) -> AttributeError:
    return AttributeError(f"Attribute '{name}' has no {kind} handler")


def _class_handlers(klass) -> dict:
    """Map the high-level attribute descriptors of a device class by name."""
    try:
        return _class_descriptors[klass]
    except KeyError:
        pass
    descriptors = {}
    for base in reversed(klass.__mro__):
        for value in vars(base).values():
            if _is_high_level_attribute(value):
                descriptors[value.attr_name.lower()] = value
    _class_descriptors[klass] = descriptors
    return descriptors


def _resolve(attr):
    """Return the device, the handlers and whether the attribute is dynamic.

    :raises NotImplementedError: If the attribute is not a high-level one.
    """
    device = attr.get_att_device()
    name = attr.get_name().lower()
    dynamic = getattr(device, _DYNAMIC_HANDLERS, None)
    if dynamic is not None and name in dynamic:
        return device, dynamic[name], True
    descriptor = _class_handlers(type(device)).get(name)
    if descriptor is None:
        raise _unsupported_error(attr.get_name())
    handlers = (
        descriptor._read_user_method,
        descriptor._write_user_method,
        descriptor._isallowed_user_method,
    )
    return device, handlers, False


def _direct_read(attr):
    """Call the high-level read handler directly and return its result.

    The handler is called exactly as it was written, so Tango request processing
    and the automatic setting of the attribute value are bypassed, and the
    result is an awaitable only if the handler is a coroutine function.

    :raises AttributeError: If the attribute has no read handler.
    :raises NotImplementedError: If the attribute is not a high-level one.

    .. versionadded:: 10.3.2
    """
    device, handlers, dynamic = _resolve(attr)
    read = handlers[0]
    if read is None:
        raise _no_handler_error("read", attr.get_name())
    return read(device, attr) if dynamic else read(device)


def _direct_write(attr, value):
    """Call the high-level write handler directly with *value*.

    The handler is called exactly as it was written, so Tango request processing
    is bypassed, and the result is an awaitable only if the handler is a
    coroutine function.

    :param value: Value passed to the high-level write handler.
    :raises AttributeError: If the attribute has no write handler.
    :raises NotImplementedError: If the attribute is not a high-level one.

    .. versionadded:: 10.3.2
    """
    device, handlers, dynamic = _resolve(attr)
    write = handlers[1]
    if write is None:
        raise _no_handler_error("write", attr.get_name())
    if dynamic:
        # The handler of a dynamic attribute reads the value from the attribute.
        attr.set_write_value(value)
        return write(device, attr)
    return write(device, value)


async def _allowed() -> bool:
    return True


def _default_is_allowed():
    """Answer ``True`` the way a handler of the server's green mode would.

    There is no user handler to call, but the caller cannot know that, so in
    asyncio green mode the answer has to be awaitable like any other one.
    """
    # Imported here because tango.device_server imports this module.
    from tango.device_server import get_worker

    if isinstance(get_worker(), AsyncioExecutor):
        return _allowed()
    return True


def _direct_is_allowed(attr, request_type):
    """Call the high-level is-allowed handler directly.

    The handler is called exactly as it was written, so the result is an
    awaitable only if the handler is a coroutine function. If the attribute has
    no is-allowed handler, ``True`` is returned, as an awaitable in asyncio
    green mode.

    :param request_type: The read or write request type to check.
    :type request_type: :class:`~tango.AttReqType`
    :raises NotImplementedError: If the attribute is not a high-level one.

    .. versionadded:: 10.3.2
    """
    device, handlers, _ = _resolve(attr)
    is_allowed = handlers[2]
    if is_allowed is None:
        return _default_is_allowed()
    return is_allowed(device, request_type)


def associate_device_attributes(device):
    """Give the runtime attributes of a device their device pointer.

    Tango fills the pointer in lazily, by looking the device up by name, which
    does not work yet while the device is being created.
    """
    for attr in device.get_device_attr().get_attribute_list():
        attr._associate_device(device)


def install_attribute_access():
    """Add the direct handler methods to the runtime attribute classes."""
    Attribute.read = _direct_read
    Attribute.is_allowed = _direct_is_allowed
    WAttribute.write = _direct_write


def register_dynamic_attribute(attr, device, read, write, is_allowed):
    """Record the handlers of a dynamically added high-level attribute."""
    handlers = (_unbound(read), _unbound(write), _unbound(is_allowed))
    try:
        dynamic = getattr(device, _DYNAMIC_HANDLERS)
    except AttributeError:
        dynamic = {}
        setattr(device, _DYNAMIC_HANDLERS, dynamic)
    name = attr.get_name()
    dynamic[name.lower()] = handlers
    device.get_device_attr().get_attr_by_name(name)._associate_device(device)


def unregister_attribute(device, name):
    """Forget the handlers of a removed dynamic attribute."""
    dynamic = getattr(device, _DYNAMIC_HANDLERS, None)
    if dynamic is not None:
        dynamic.pop(name.lower(), None)


__all__ = (
    "associate_device_attributes",
    "install_attribute_access",
    "register_dynamic_attribute",
    "unregister_attribute",
)
