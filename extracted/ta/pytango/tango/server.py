# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Server helper classes for writing Tango device servers."""

import sys
import copy
import inspect
import logging
import functools
import traceback
import warnings
import types

from typing import Union, ClassVar, Any

try:
    from docstring_parser import parse as parse_docstring
except ImportError:
    parse_docstring = None

from tango import AttrDataFormat, AttrWriteType, CmdArgType, DevState
from tango import DevFailed, GreenMode, SerialModel

from tango.attr_data import AttrData
from tango.device_class import DeviceClass
from tango.device_server import (
    LatestDeviceImpl,
    get_worker,
    set_worker,
    run_in_executor,
)
from tango.utils import (
    is_seq,
    is_non_str_seq,
    is_pure_str,
    _is_coroutine_function,
    get_tango_type_format,
    get_attribute_type_format,
    set_complex_value,
    parse_type_hint,
    _create_device_telemetry_tracer,
    get_telemetry_tracer_provider_factory,
    _force_tracing,
    _forcefully_traced_method,
)
from tango.utils import scalar_to_array_type
from tango.green import get_green_mode, get_executor
from tango.pyutil import Util
from tango.asyncio_executor import AsyncioExecutor
from tango.constants import StatusNotSet

__all__ = (
    "DeviceMeta",
    "Device",
    "LatestDeviceImpl",
    "attribute",
    "command",
    "device_property",
    "class_property",
    "run",
    "server_run",
    "Server",
)

API_VERSION = 2

# Helpers


def __get_in_out_types_from_method_type_hints(method):
    # If it's a bound method (has __func__), unwrap it,
    # otherwise signature will ignore self parameter
    if isinstance(method, types.MethodType):
        func = method.__func__
    else:
        func = method

    sig = inspect.signature(func)
    params = list(sig.parameters.values())

    first_arg_type = None
    # params[0] should be self and params[1] the command argument
    if len(params) > 1 and params[1].annotation is not inspect.Parameter.empty:
        first_arg_type = params[1].annotation

    # Check return annotation
    return_type = sig.return_annotation
    if return_type is inspect.Signature.empty:
        return_type = None

    return first_arg_type, return_type


def from_typeformat_to_type(dtype, dformat):
    if dformat == AttrDataFormat.SCALAR:
        return dtype
    elif dformat == AttrDataFormat.IMAGE:
        raise TypeError("Cannot translate IMAGE to tango type")
    return scalar_to_array_type(dtype)


def __get_wrapped_read_method(attribute, read_method):
    """
    Make sure attr is updated on read, and wrap it with executor, if needed.

    :param attribute: the attribute data information
    :type attribute: AttrData
    :param read_method: read method
    :type read_method: callable
    """

    already_wrapped = hasattr(read_method, "__access_wrapped__")
    if already_wrapped:
        return read_method

    if attribute.read_green_mode:

        @functools.wraps(read_method)
        def read_attr(self, attr):
            worker = get_worker()
            ret = worker.execute(read_method, self)
            if not attr.value_is_set() and ret is not None:
                set_complex_value(attr, ret)
            return ret

    else:

        @functools.wraps(read_method)
        def read_attr(self, attr):
            ret = read_method(self)
            if not attr.value_is_set() and ret is not None:
                set_complex_value(attr, ret)
            return ret

    if _force_tracing:
        read_attr = _forcefully_traced_method(read_attr)
    read_attr.__access_wrapped__ = True
    return read_attr


def __patch_read_method(tango_device_klass, attribute):
    """
    Finds read method for attribute, wraps it with executor and adds
    wrapped method to device dict.

    :param tango_device_klass: a DeviceImpl class
    :type tango_device_klass: class
    :param attribute: the attribute data information
    :type attribute: AttrData
    """
    read_method = getattr(attribute, "fget", None)
    if not read_method:
        method_name = attribute.read_method_name
        read_method = getattr(tango_device_klass, method_name)

    read_attr = __get_wrapped_read_method(attribute, read_method)
    method_name = f"__read_{attribute.attr_name}_wrapper__"
    attribute.read_method_name = method_name

    setattr(tango_device_klass, method_name, read_attr)


def __get_wrapped_write_method(attribute, write_method):
    """
    Wraps write method with executor, if needed.
    """
    already_wrapped = hasattr(write_method, "__access_wrapped__")
    if already_wrapped:
        return write_method

    if attribute.write_green_mode:

        @functools.wraps(write_method)
        def write_attr(self, attr):
            value = attr.get_write_value()
            return get_worker().execute(write_method, self, value)

    else:

        @functools.wraps(write_method)
        def write_attr(self, attr):
            value = attr.get_write_value()
            return write_method(self, value)

    if _force_tracing:
        write_attr = _forcefully_traced_method(write_attr)
    write_attr.__access_wrapped__ = True
    return write_attr


def __patch_write_method(tango_device_klass, attribute):
    """
    Finds write method for attribute, wraps it with executor and adds
    wrapped method to device dict.

    :param tango_device_klass: a DeviceImpl class
    :type tango_device_klass: class
    :param attribute: the attribute data information
    :type attribute: AttrData
    """
    write_method = getattr(attribute, "fset", None)
    if not write_method:
        method_name = attribute.write_method_name
        write_method = getattr(tango_device_klass, method_name)

    write_attr = __get_wrapped_write_method(attribute, write_method)
    method_name = f"__write_{attribute.attr_name}_wrapper__"
    attribute.write_method_name = method_name

    setattr(tango_device_klass, method_name, write_attr)


def __get_wrapped_isallowed_method(attribute, isallowed_method):
    """
    Wraps is allowed method with executor, if needed.

    :param attribute: the attribute data information
    :type attribute: AttrData
    :param isallowed_method: is allowed method
    :type isallowed_method: callable
    """
    already_wrapped = hasattr(isallowed_method, "__access_wrapped__")
    if already_wrapped:
        return isallowed_method

    if attribute.isallowed_green_mode:

        @functools.wraps(isallowed_method)
        def isallowed_attr(self, request_type):
            worker = get_worker()
            return worker.execute(isallowed_method, self, request_type)

    else:
        isallowed_attr = isallowed_method

    if _force_tracing:
        isallowed_attr = _forcefully_traced_method(isallowed_attr)
    if isallowed_attr is not isallowed_method:
        isallowed_attr.__access_wrapped__ = True
    return isallowed_attr


def __patch_isallowed_method(tango_device_klass, attribute):
    """
    Finds isallowed method for attribute, wraps it with executor and adds
    wrapped method to device dict.

    :param tango_device_klass: a DeviceImpl class
    :type tango_device_klass: class
    :param attribute: the attribute data information
    :type attribute: AttrData
    """
    isallowed_method = getattr(attribute, "fisallowed", None)
    if not isallowed_method:
        method_name = attribute.is_allowed_name
        isallowed_method = getattr(tango_device_klass, method_name, None)

    if isallowed_method:
        isallowed_attr = __get_wrapped_isallowed_method(attribute, isallowed_method)
        method_name = f"__is_{attribute.attr_name}_allowed_wrapper__"
        attribute.is_allowed_name = method_name

        setattr(tango_device_klass, method_name, isallowed_attr)


def __patch_attr_methods(tango_device_klass, attribute):
    """
    Finds read, write and isallowed methods for attribute, and
    wraps into another method to make them work.

    Also patch methods with green executor, if requested.

    Finally, adds pathed methods to the device dict.

    :param tango_device_klass: a DeviceImpl class
    :type tango_device_klass: class
    :param attribute: the attribute data information
    :type attribute: AttrData
    """
    if attribute.attr_write in (AttrWriteType.READ, AttrWriteType.READ_WRITE):
        __patch_read_method(tango_device_klass, attribute)

    if attribute.attr_write in (AttrWriteType.WRITE, AttrWriteType.READ_WRITE):
        __patch_write_method(tango_device_klass, attribute)

    __patch_isallowed_method(tango_device_klass, attribute)


def __get_attribute_type_from_hint(attribute, type_hint=None, device_klass=None):
    if not attribute.has_dtype_kword:
        if not type_hint:
            if attribute.attr_write in (AttrWriteType.READ, AttrWriteType.READ_WRITE):
                read_method = getattr(device_klass, attribute.read_method_name)
                type_hint = dict(read_method.__annotations__).get("return", None)
            if not type_hint and attribute.attr_write in (
                AttrWriteType.WRITE,
                AttrWriteType.READ_WRITE,
            ):
                write_method = getattr(device_klass, attribute.write_method_name)
                type_hints = dict(write_method.__annotations__)
                type_hints.pop("return", None)
                if type_hints:
                    type_hint = list(type_hints.values())[-1]

        if type_hint:
            dtype, dformat, max_x, max_y = parse_type_hint(
                type_hint, caller="attribute"
            )
            if dformat is None:
                if attribute.attr_format not in [
                    AttrDataFormat.IMAGE,
                    AttrDataFormat.SPECTRUM,
                ]:
                    raise RuntimeError(
                        "For numpy.ndarrays AttrDataFormat has to be specified"
                    )
                dformat = attribute.attr_format

            dtype, dformat, enum_labels = get_attribute_type_format(
                dtype, dformat, None
            )
            attribute.attr_type = dtype
            attribute.attr_format = dformat
            if enum_labels:
                attribute.set_enum_labels_to_attr_prop(enum_labels)
            if not attribute.has_size_kword:
                if max_x:
                    attribute.dim_x = max_x
                if max_y:
                    attribute.dim_y = max_y


def __get_property_type_from_hint(property, type_hint):
    if property.dtype is None:
        dtype, _, _, _ = parse_type_hint(type_hint, caller="property")
        property.dtype = from_typeformat_to_type(*get_tango_type_format(dtype))


def __patch_is_command_allowed_method(
    tango_device_klass, is_allowed_method, cmd_name, green_mode
):
    """
    :param tango_device_klass: a DeviceImpl class
    :type tango_device_klass: class
    :param is_allowed_method: a callable to check if command is allowed
    :type is_allowed_method: callable
    :param cmd_name: command name
    :type cmd_name: str
    :param green_mode: indicates whether method should be wrapped with executor or not
    :type green_mode: bool
    """
    already_wrapped = hasattr(is_allowed_method, "__access_wrapped__")
    if already_wrapped:
        return is_allowed_method.__wrapped_method_name__

    method_name = getattr(is_allowed_method, "__name__", f"is_{cmd_name}_allowed")
    method_name = f"__wrapped_{method_name}__"

    if green_mode:
        wrapped_method = run_in_executor(is_allowed_method)
    else:
        wrapped_method = is_allowed_method
    if _force_tracing:
        wrapped_method = _forcefully_traced_method(wrapped_method)
    if wrapped_method is not is_allowed_method:
        wrapped_method.__access_wrapped__ = True
        wrapped_method.__wrapped_method_name__ = method_name
    setattr(tango_device_klass, method_name, wrapped_method)

    return method_name


def __unwrap_method(method):
    while hasattr(method, "__wrapped__"):
        method = method.__wrapped__

    return method


def __warn_if_standard_device_methods_should_be_coroutine(klass):
    worker = get_worker()
    # get base device class:
    if isinstance(worker, AsyncioExecutor):
        for parent in klass.__bases__:
            if type(parent) is DeviceMeta:
                for method in (
                    "init_device",
                    "delete_device",
                    "dev_state",
                    "dev_status",
                    "read_attr_hardware",
                    "always_executed_hook",
                ):
                    user_method = __unwrap_method(getattr(klass, method))
                    base_method = __unwrap_method(getattr(parent, method))
                    if user_method != base_method and not _is_coroutine_function(
                        user_method
                    ):
                        warnings.warn(
                            f"{method} is sync: support of "
                            f"sync functions in Asyncio Servers is "
                            f"deprecated. Use 'async def' instead of 'def'.",
                            DeprecationWarning,
                        )


async def __async_method_helper(method, *args, **kwargs):
    return await get_worker().delegate(method, *args, **kwargs)


def __patch_standard_device_methods(klass):
    # TODO allow to force non green mode

    # init_device
    init_device_orig = klass.init_device
    already_wrapped = hasattr(init_device_orig, "__access_wrapped__")
    if not already_wrapped:
        is_base_klass_init_device = init_device_orig == BaseDevice.init_device

        @functools.wraps(init_device_orig)
        def init_device(self):
            __warn_if_standard_device_methods_should_be_coroutine(klass)
            worker = get_worker()
            if isinstance(worker, AsyncioExecutor) and is_base_klass_init_device:
                # if coroutine will never be awaited, we want that RuntimeWarning will print us
                # 'init_device' instead of "__async_method_helper", so we create another intermediate
                # layer with proper  __qualname__
                method_helper = __async_method_helper
                method_helper.__qualname__ = "BaseDevice.init_device"
                return worker.execute(method_helper, init_device_orig, self)
            else:
                return worker.execute(init_device_orig, self)

        if _force_tracing:
            init_device = _forcefully_traced_method(
                init_device, is_kernel_method=is_base_klass_init_device
            )
        init_device.__access_wrapped__ = True
        setattr(klass, "init_device", init_device)

    # delete_device
    delete_device_orig = klass.delete_device
    already_wrapped = hasattr(delete_device_orig, "__access_wrapped__")
    if not already_wrapped:
        is_base_klass_delete_device = delete_device_orig == BaseDevice.delete_device

        @functools.wraps(delete_device_orig)
        def delete_device(self):
            worker = get_worker()
            if isinstance(worker, AsyncioExecutor) and is_base_klass_delete_device:
                method_helper = __async_method_helper
                method_helper.__qualname__ = "BaseDevice.delete_device"
                return worker.execute(method_helper, delete_device_orig, self)
            else:
                return worker.execute(delete_device_orig, self)

        if _force_tracing:
            delete_device = _forcefully_traced_method(
                delete_device, is_kernel_method=is_base_klass_delete_device
            )
        delete_device.__access_wrapped__ = True
        setattr(klass, "delete_device", delete_device)

    dev_state_orig = klass.dev_state
    already_wrapped = hasattr(dev_state_orig, "__access_wrapped__")
    if not already_wrapped:
        is_base_klass_dev_state = dev_state_orig == BaseDevice.dev_state

        @functools.wraps(dev_state_orig)
        def dev_state(self):
            worker = get_worker()
            if isinstance(worker, AsyncioExecutor) and is_base_klass_dev_state:
                method_helper = __async_method_helper
                method_helper.__qualname__ = "BaseDevice.dev_state"
                return worker.execute(method_helper, dev_state_orig, self)
            else:
                return worker.execute(dev_state_orig, self)

        if _force_tracing:
            dev_state = _forcefully_traced_method(
                dev_state, is_kernel_method=is_base_klass_dev_state
            )
        dev_state.__access_wrapped__ = True
        setattr(klass, "dev_state", dev_state)

    # device_status
    dev_status_orig = klass.dev_status
    already_wrapped = hasattr(dev_status_orig, "__access_wrapped__")
    if not already_wrapped:
        is_base_klass_dev_status = dev_status_orig == BaseDevice.dev_status

        @functools.wraps(dev_status_orig)
        def dev_status(self):
            worker = get_worker()
            if isinstance(worker, AsyncioExecutor) and is_base_klass_dev_status:
                method_helper = __async_method_helper
                method_helper.__qualname__ = "BaseDevice.dev_status"
                return worker.execute(method_helper, dev_status_orig, self)
            else:
                return worker.execute(dev_status_orig, self)

        if _force_tracing:
            dev_status = _forcefully_traced_method(
                dev_status, is_kernel_method=is_base_klass_dev_status
            )
        dev_status.__access_wrapped__ = True
        setattr(klass, "dev_status", dev_status)

    # read_attr_hardware
    read_attr_hardware_orig = klass.read_attr_hardware
    already_wrapped = hasattr(read_attr_hardware_orig, "__access_wrapped__")
    if not already_wrapped:
        is_base_klass_read_attr_hardware = (
            read_attr_hardware_orig == BaseDevice.read_attr_hardware
        )

        @functools.wraps(read_attr_hardware_orig)
        def read_attr_hardware(self, attr_list):
            worker = get_worker()
            if isinstance(worker, AsyncioExecutor) and is_base_klass_read_attr_hardware:
                method_helper = __async_method_helper
                method_helper.__qualname__ = "BaseDevice.read_attr_hardware"
                return worker.execute(
                    method_helper, read_attr_hardware_orig, self, attr_list
                )
            else:
                return worker.execute(read_attr_hardware_orig, self, attr_list)

        if _force_tracing:
            read_attr_hardware = _forcefully_traced_method(
                read_attr_hardware, is_kernel_method=is_base_klass_read_attr_hardware
            )
        read_attr_hardware.__access_wrapped__ = True
        setattr(klass, "read_attr_hardware", read_attr_hardware)

    # always_executed_hook
    always_executed_hook_orig = klass.always_executed_hook
    already_wrapped = hasattr(always_executed_hook_orig, "__access_wrapped__")
    if not already_wrapped:
        is_base_klass_always_executed_hook = (
            always_executed_hook_orig == BaseDevice.always_executed_hook
        )

        @functools.wraps(always_executed_hook_orig)
        def always_executed_hook(self):
            worker = get_worker()
            if (
                isinstance(worker, AsyncioExecutor)
                and is_base_klass_always_executed_hook
            ):
                method_helper = __async_method_helper
                method_helper.__qualname__ = "BaseDevice.always_executed_hook"
                return worker.execute(method_helper, always_executed_hook_orig, self)
            else:
                return worker.execute(always_executed_hook_orig, self)

        if _force_tracing:
            always_executed_hook = _forcefully_traced_method(
                always_executed_hook,
                is_kernel_method=is_base_klass_always_executed_hook,
            )
        always_executed_hook.__access_wrapped__ = True
        setattr(klass, "always_executed_hook", always_executed_hook)

    # server_init_hook
    server_init_hook_orig = klass.server_init_hook
    already_wrapped = hasattr(server_init_hook_orig, "__access_wrapped__")
    if not already_wrapped:
        is_base_klass_server_init_hook = (
            server_init_hook_orig == BaseDevice.server_init_hook
        )

        @functools.wraps(server_init_hook_orig)
        def server_init_hook(self):
            worker = get_worker()
            if isinstance(worker, AsyncioExecutor) and is_base_klass_server_init_hook:
                method_helper = __async_method_helper
                method_helper.__qualname__ = "BaseDevice.server_init_hook"
                return worker.execute(method_helper, server_init_hook_orig, self)
            else:
                return worker.execute(server_init_hook_orig, self)

        if _force_tracing:
            server_init_hook = _forcefully_traced_method(
                server_init_hook, is_kernel_method=is_base_klass_server_init_hook
            )
        server_init_hook.__access_wrapped__ = True
        setattr(klass, "server_init_hook", server_init_hook)


class _DeviceClass(DeviceClass):
    def __init__(self, name):
        DeviceClass.__init__(self, name)
        self.set_type(name)

        if _force_tracing:
            orig_dyn_attr = getattr(self, "dyn_attr")
            setattr(
                self,
                "dyn_attr",
                _forcefully_traced_method(orig_dyn_attr, is_kernel_method=True),
            )

    def dyn_attr(self, dev_list):
        """Invoked to create dynamic attributes for the given devices.
        Default implementation calls
        :meth:`TT.initialize_dynamic_attributes` for each device

        :param dev_list: list of devices
        :type dev_list: :class:`tango.DeviceImpl`"""

        for dev in dev_list:
            init_dyn_attrs = getattr(dev, "initialize_dynamic_attributes", None)
            if init_dyn_attrs and callable(init_dyn_attrs):
                try:
                    init_dyn_attrs()
                except Exception as ex:
                    dev.warn_stream("Failed to initialize dynamic attributes")
                    dev.debug_stream("Details: " + traceback.format_exc())
                    raise Exception(repr(ex))


def __create_tango_deviceclass_klass(tango_device_klass, attrs=None):
    klass_name = tango_device_klass.__name__
    if not issubclass(tango_device_klass, (BaseDevice)):
        msg = f"{klass_name} device must inherit from tango.server.Device"
        raise Exception(msg)

    if attrs is None:
        attrs = tango_device_klass.__dict__

    klass_annotations = {}
    if hasattr(tango_device_klass, "__annotations__"):
        klass_annotations = dict(tango_device_klass.__annotations__)

    attr_list = {}
    class_property_list = {}
    device_property_list = {}
    cmd_list = {}

    for attr_name, attr_obj in attrs.items():
        if isinstance(attr_obj, attribute):
            klass_attribute_name = attr_name
            if attr_obj.attr_name is None:
                attr_obj._set_name(attr_name)
            else:
                attr_name = attr_obj.attr_name
            attr_list[attr_name] = attr_obj
            if not attr_obj.forward:
                __patch_attr_methods(tango_device_klass, attr_obj)
                if klass_attribute_name in klass_annotations:
                    __get_attribute_type_from_hint(
                        attr_obj, type_hint=klass_annotations[klass_attribute_name]
                    )
                else:
                    __get_attribute_type_from_hint(
                        attr_obj, device_klass=tango_device_klass
                    )

        elif isinstance(attr_obj, device_property):
            if attr_name in klass_annotations:
                __get_property_type_from_hint(attr_obj, klass_annotations[attr_name])
            attr_obj.name = attr_name
            # if you modify the attr_obj order then you should
            # take care of the code in get_device_properties()
            device_property_list[attr_name] = [
                attr_obj.dtype,
                attr_obj.doc,
                attr_obj.default_value,
                attr_obj.mandatory,
            ]

        elif isinstance(attr_obj, class_property):
            if attr_name in klass_annotations:
                __get_property_type_from_hint(attr_obj, klass_annotations[attr_name])
            attr_obj.name = attr_name
            class_property_list[attr_name] = [
                attr_obj.dtype,
                attr_obj.doc,
                attr_obj.default_value,
            ]

        elif inspect.isroutine(attr_obj):
            if hasattr(attr_obj, "__tango_command__"):
                cmd_name, cmd_info = attr_obj.__tango_command__
                cmd_list[cmd_name] = cmd_info
                if "Is allowed" in cmd_info[2]:
                    is_allowed_method = cmd_info[2]["Is allowed"]
                else:
                    is_allowed_method = f"is_{cmd_name}_allowed"
                is_allowed_method_green_mode = cmd_info[2]["Is allowed green_mode"]

                if is_pure_str(is_allowed_method):
                    is_allowed_method = getattr(
                        tango_device_klass, is_allowed_method, None
                    )

                if is_allowed_method is not None:
                    cmd_info[2]["Is allowed"] = __patch_is_command_allowed_method(
                        tango_device_klass,
                        is_allowed_method,
                        cmd_name,
                        is_allowed_method_green_mode,
                    )

    __patch_standard_device_methods(tango_device_klass)

    devclass_name = klass_name + "Class"

    devclass_attrs = dict(
        class_property_list=class_property_list,
        device_property_list=device_property_list,
        cmd_list=cmd_list,
        attr_list=attr_list,
    )
    return type(_DeviceClass)(devclass_name, (_DeviceClass,), devclass_attrs)


def _init_tango_device_klass(tango_device_klass, attrs=None, tango_class_name=None):
    klass_name = tango_device_klass.__name__
    tango_deviceclass_klass = __create_tango_deviceclass_klass(
        tango_device_klass, attrs=attrs
    )
    if tango_class_name is None:
        if hasattr(tango_device_klass, "TangoClassName"):
            tango_class_name = tango_device_klass.TangoClassName
        else:
            tango_class_name = klass_name
    tango_device_klass.TangoClassClass = tango_deviceclass_klass
    tango_device_klass.TangoClassName = tango_class_name
    tango_device_klass._api = API_VERSION
    return tango_device_klass


def is_tango_object(arg):
    """Return tango data if the argument is a tango object,
    False otherwise.
    """
    classes = attribute, device_property, class_property
    if isinstance(arg, classes):
        return arg
    try:
        return arg.__tango_command__
    except AttributeError:
        return False


def inheritance_patch(attrs):
    """Patch tango objects before they are processed by the metaclass."""
    for key, obj in attrs.items():
        if isinstance(obj, attribute):
            if getattr(obj, "attr_write", None) == AttrWriteType.READ_WRITE:
                if not getattr(obj, "fset", None):
                    method_name = obj.write_method_name or "write_" + key
                    obj.fset = attrs.get(method_name)


class DeviceMeta(type(LatestDeviceImpl)):
    """
    The :py:data:`metaclass` callable for :class:`Device`.

    This implementation of DeviceMeta makes device inheritance possible.
    """

    def __new__(metacls, name, bases, attrs):
        # Attribute dictionary
        dct = {}
        # Filter object from bases
        bases = tuple(base for base in bases if base is not object)
        # Set tango objects as attributes
        for base in reversed(bases):
            for key, value in base.__dict__.items():
                if is_tango_object(value):
                    dct[key] = value
        # Inheritance patch
        inheritance_patch(attrs)
        # Update attribute dictionary
        dct.update(attrs)
        # Create device class
        cls = type(LatestDeviceImpl).__new__(metacls, name, bases, dct)
        # Initialize device class
        _init_tango_device_klass(cls, dct)
        cls.TangoClassName = name
        # Return device class
        return cls


class BaseDevice(LatestDeviceImpl):
    """
    Base device class for the High level API.

    It should not be used directly, since this class is not an
    instance of MetaDevice. Use tango.server.Device instead.
    """

    DEVICE_CLASS_DESCRIPTION: ClassVar[Union[str, None]] = None
    """Description of the device class (optional).

    If not specified, the class docstring is used.
    Available to clients via :meth:`tango.DeviceProxy.description`.
    Use as a class variable.

    :meta hide-value:
    """

    DEVICE_CLASS_INITIAL_STATUS: ClassVar[str] = StatusNotSet
    """Initial status string for all instances of the device (optional).

    Use as a class variable.

    :meta hide-value:
    """

    DEVICE_CLASS_INITIAL_STATE: ClassVar[DevState] = DevState.UNKNOWN
    """Initial state value for all instances of the device (optional).

    Use as a class variable.

    :meta hide-value:
    """

    def __init__(self, cl, name):
        self._tango_properties = {}
        if self.DEVICE_CLASS_DESCRIPTION is not None:
            dev_desc = self.DEVICE_CLASS_DESCRIPTION
        elif self.__doc__:
            dev_desc = self.__doc__
        else:
            dev_desc = "A TANGO device"
        dev_state = self.DEVICE_CLASS_INITIAL_STATE
        dev_status = self.DEVICE_CLASS_INITIAL_STATUS
        LatestDeviceImpl.__init__(self, cl, name, dev_desc, dev_state, dev_status)
        self._configure_device_telemetry(cl.get_name(), name)
        self.init_device()

    def init_device(self):
        """
        Code to handle device initialisation.

        This method is called automatically when the device starts,
        but before it is available to clients (i.e., before it is "exported").
        It also gets called if the device is re-initialised by a call to the
        ``Init`` command (after :meth:`~tango.server.Device.delete_device`).

        Default implementation calls :meth:`get_device_properties`

        If overwriting this method, it is important to call the super class
        method first:

        - For synchronous devices: ``super().init_device()``
        - For asyncio green mode devices: ``await super().init_device()``
        """
        self.get_device_properties()

    def delete_device(self):
        """
        Code to handle device clean-up.

        This method is called automatically when the device is shut down gracefully.
        It also gets called if the device is re-initialised by a call to the ``Init``
        command (before a new call to :meth:`~tango.server.Device.init_device`).

        If overwriting this method, it is important to call the super class
        method last:

        - For synchronous devices: ``super().delete_device()``
        - For asyncio green mode devices: ``await super().delete_device()``
        """
        pass

    def read_attr_hardware(self, attr_list):
        return LatestDeviceImpl.read_attr_hardware(self, attr_list)

    def dev_state(self):
        return LatestDeviceImpl.dev_state(self)

    def dev_status(self):
        return LatestDeviceImpl.dev_status(self)

    def get_device_properties(self, ds_class=None):
        if ds_class is None:
            try:
                # Call this method in a try/except in case this is called
                # during the DS shutdown sequence
                ds_class = self.get_device_class()
            except Exception:
                return
        try:
            pu = self.prop_util = ds_class.prop_util
            self.device_property_list = copy.deepcopy(ds_class.device_property_list)
            class_prop = ds_class.class_property_list
            pu.get_device_properties(self, class_prop, self.device_property_list)
            for prop_name in class_prop:
                value = pu.get_property_values(prop_name, class_prop)
                self._tango_properties[prop_name] = value
            for prop_name in self.device_property_list:
                value = self.prop_util.get_property_values(
                    prop_name, self.device_property_list
                )
                self._tango_properties[prop_name] = value
                properties = self.device_property_list[prop_name]
                mandatory = properties[3]
                if mandatory and value is None:
                    msg = f"Device property {prop_name} is mandatory "
                    raise Exception(msg)
        except DevFailed as df:
            print(80 * "-")
            print(df)
            raise df

    def always_executed_hook(self):
        """
        Tango always_executed_hook. Default implementation does
        nothing
        """
        pass

    def server_init_hook(self):
        """
        Tango server_init_hook.  Called once the device server admin device
        (DServer) is exported.
        Default implementation does nothing.
        """
        pass

    def initialize_dynamic_attributes(self):
        """
        Method executed at initializion phase to create dynamic
        attributes. Default implementation does nothing. Overwrite
        when necessary.

        .. note::
            This method is only called once when the device server starts,
            after init_device(), but before the device is marked as exported.
            If the Init command is executed on the device, the
            initialize_dynamic_attributes() method will not be called again.
        """
        pass

    @classmethod
    def run_server(cls, args=None, **kwargs):
        """Run the class as a device server.
        It is based on the tango.server.run method.

        The difference is that the device class
        and server name are automatically given.

        Args:
            args (iterable): args as given in the tango.server.run method
                             without the server name. If None, the sys.argv
                             list is used
            kwargs: the other keywords argument are as given
                    in the tango.server.run method.
        """
        if args is None:
            args = sys.argv[1:]
        args = [cls.__name__] + list(args)
        green_mode = getattr(cls, "green_mode", None)
        kwargs.setdefault("green_mode", green_mode)
        return run((cls,), args, **kwargs)

    def _configure_device_telemetry(self, class_name, device_name):
        device_tracer_provider = self.create_telemetry_tracer_provider(
            class_name, device_name
        )
        device_tracer = self.create_telemetry_tracer(device_tracer_provider)
        self._tango_telemetry_tracer = device_tracer

    def create_telemetry_tracer_provider(
        self, class_name, device_name
    ) -> "opentelemetry.trace.TracerProvider":  # noqa: F821
        """Factory method returning a TracerProvider for telemetry.

        The default implementation can be overridden.

        .. versionadded:: 10.0.0
        """
        tracer_provider_factory = get_telemetry_tracer_provider_factory()
        return tracer_provider_factory(class_name, device_name)

    def create_telemetry_tracer(
        self, device_tracer_provider
    ) -> "opentelemetry.trace.Tracer":  # noqa: F821
        """Factory method returning a Tracer for telemetry.

        The default implementation can be overridden.

        .. versionadded:: 10.0.0
        """
        return _create_device_telemetry_tracer(device_tracer_provider)

    def get_telemetry_tracer(self) -> "opentelemetry.trace.Tracer":  # noqa: F821
        """Returns device telemetry tracer, or None if telemetry disabled.

        .. versionadded:: 10.0.0
        """
        return self._tango_telemetry_tracer


class attribute(AttrData):
    '''
    Declares a new tango attribute in a :class:`Device`. To be used
    like the python native :obj:`property` function. For example, to
    declare a scalar, `tango.DevDouble`, read-only attribute called
    *voltage* in a *PowerSupply* :class:`Device` do::

        class PowerSupply(Device):

            voltage = attribute()

            def read_voltage(self):
                return 999.999

    The same can be achieved with::

        class PowerSupply(Device):

            @attribute
            def voltage(self):
                return 999.999


    .. note::
        avoid using *dformat* parameter. If you need a SPECTRUM
        attribute of say, boolean type, use instead ``dtype=(bool,)``.

    Example of an integer writable attribute with a customized label,
    unit and description::

        class PowerSupply(Device):

            current = attribute(label="Current", unit="mA", dtype=int,
                                access=AttrWriteType.READ_WRITE,
                                doc="the power supply current")

            def init_device(self):
                Device.init_device(self)
                self._current = -1

            def read_current(self):
                return self._current

            def write_current(self, current):
                self._current = current

    The same, but using attribute as a decorator::

        class PowerSupply(Device):

            def init_device(self):
                Device.init_device(self)
                self._current = -1

            @attribute(label="Current", unit="mA", dtype=int)
            def current(self):
                """the power supply current"""
                return 999.999

            @current.write
            def current(self, current):
                self._current = current

    In this second format, defining the `write` implicitly sets the attribute
    access to READ_WRITE.

    Receives multiple keyword arguments:

    :param name:
        attribute name. `Default:` name of decorated read method, or variable assigned to.
    :type name: str

    :param dtype:
        Data type (see :ref:`Data type equivalence <pytango-hlapi-datatypes>`).
        `Default:` :obj:`~tango.CmdArgType.DevDouble` (:obj:`float`).
    :type dtype: :obj:`~tango.CmdArgType`

    :param dformat:
        Data format: :obj:`~tango.AttrDataFormat.SCALAR` (0D),
        :obj:`~tango.AttrDataFormat.SPECTRUM` (1D) or
        :obj:`~tango.AttrDataFormat.IMAGE` (2D).
        `Default:` :obj:`~tango.AttrDataFormat.SCALAR`.
    :type dformat: :obj:`~tango.AttrDataFormat`

    :param max_dim_x:
        Maximum size for x dimension (ignored for :obj:`~tango.AttrDataFormat.SCALAR`
        format).
        `Default:` ``1``.
    :type max_dim_x: int

    :param max_dim_y:
        Maximum size for y dimension (ignored for :obj:`~tango.AttrDataFormat.SCALAR`
        and :obj:`~tango.AttrDataFormat.SPECTRUM` formats).
        `Default:` ``0``.
    :type max_dim_y: int

    :param enum_labels:
        List of enumeration label strings (for enum data type).
        `Default:` :obj:`None`.
    :type enum_labels: list | tuple | None

    :param access:
        Type of the attribute: read-only / read-write / write-only/ read-with-write.
        `Default:` :obj:`~tango.AttrWriteType.READ`.
    :type access: :obj:`~tango.AttrWriteType`

    :param fget:
        Read method name or method object. If not provided, then PyTango will
        search the method, named ``"read_<attr_name>"``.
    :type fget: :obj:`str` | :obj:`callable`

    :param fread:
        Alias for parameter ``fget``
    :type fread: :obj:`str` | :obj:`callable`

    :param fset:
        Write method name or method object. If not provided, then PyTango will
        search the method, named ``"write_<attr_name>"``.
    :type fset: :obj:`str` | :obj:`callable`

    :param fwrite:
        Alias for parameter ``fset``
    :type fwrite: :obj:`str` | :obj:`callable`

    :param fisallowed:
        Is-allowed method name or method object. If not provided, then PyTango
        will search the method, named ``"is_<attr_name>_allowed"``.
    :type fisallowed: :obj:`str` | :obj:`callable`

    :param doc:
        Attribute description.
        `Default:` ``""`` [Note_1]_
    :type doc: str

    :param description:
        Alias for parameter ``doc``.
    :type doc: str

    :param label:
        Attribute label for user interfaces.
        `Default:` ``"<attr_name>"``.
    :type label: str

    :param display_level:
        Display level on user interfaces.
        `Default:` :obj:`~tango.DispLevel.OPERATOR`.
    :type display_level: :obj:`~tango.DispLevel`

    :param unit:
        Physical units the attribute value is in.
        `Default:` ``""``.
    :type unit: str

    :param standard_unit:
        The conversion factor to transform attribute’s value into SI units.
        `Default:` ``""`` [Note_2]_
    :type standard_unit: str | int | float | None

    :param display_unit:
        The conversion factor to transform attribute’s value into value usable
        in user interfaces (hint for clients).
        `Default:` ``""`` [Note_2]_
    :type display_unit: str | int | float | None

    :param format:
        Attribute representation format for user interfaces.
        `Default:` ``"6.2f"``.
    :type format: str

    :param min_value:
        Minimum allowed value.
        `Default:` :obj:`None` [Note_2]_
    :type min_value: str | int | float | None

    :param max_value:
        Maximum allowed value.
        `Default:` :obj:`None` [Note_2]_
    :type max_value: str | int | float | None

    :param min_alarm:
        Minimum value to trigger attribute quality to be :obj:`tango.AttrQuality.ALARM`.
        `Default:` :obj:`None` [Note_2]_
    :type min_alarm: str | int | float | None

    :param max_alarm:
        Maximum value to trigger attribute quality to be :obj:`tango.AttrQuality.ALARM`.
        `Default:` :obj:`None` [Note_2]_
    :type max_alarm: str | int | float | None

    :param min_warning:
        Minimum value to trigger attribute quality to be
        :obj:`tango.AttrQuality.WARNING`.
        `Default:` :obj:`None` [Note_2]_
    :type min_warning: str | int | float | None

    :param max_warning:
        Maximum value to trigger attribute quality to be
        :obj:`tango.AttrQuality.WARNING`.
        `Default:` :obj:`None` [Note_2]_
    :type max_warning: str | int | float | None

    :param abs_change:
        Minimum absolute change of attribute value, that causes the change event.
        E.g., ``abs_change = 1`` will generate an event when:
        (current - previous) > 1.
        `Default:` :obj:`None` [Note_2]_
    :type abs_change: str | int | float | None

    :param rel_change:
        Minimum relative change (%) of attribute value, that causes change event.
        E.g., ``rel_change = 1`` will generate an event when:
        (current - previous) / previous > 1%.
        `Default:` :obj:`None` [Note_2]_
    :type rel_change: str | int | float | None

    :param alarm_event_implemented:
        indicates if alarm event for this attribute emitted by the code `Default:` False
    :type alarm_event_implemented: bool

    :param alarm_event_detect:
        enable or disable filtering for alarm event emitted by the code. `Default:` False
    :type alarm_event_detect: bool

    :param change_event_implemented:
        indicates if change event for this attribute emitted by the code `Default:` False
    :type change_event_implemented: bool

    :param change_event_detect:
        enable or disable filtering for change event emitted by the code. E.g., if user emits event,
        by the value changed less, then abs_change or rel_change - event will be filtered out  `Default:` False
    :type change_event_detect: bool

    :param period:
        Time of periodic event generation in milliseconds. This is the
        minimum time between periodic events.
        `Default:` :obj:`None` [Note_2]_
    :type period: str | int | None

    :param archive_abs_change:
        Minimum absolute change of attribute value, that causes the archive event.
        E.g., ``archive_abs_change = 1`` will generate an event when:
        (current - previous) > 1.
        `Default:` :obj:`None` [Note_2]_
    :type archive_abs_change: str | int | float | None

    :param archive_rel_change:
        Minimum relative change (%) of attribute value, that causes archive event.
        E.g., ``archive_rel_change = 1`` will generate an event when:
        (current - previous) / previous > 1%.
        `Default:` :obj:`None` [Note_2]_
    :type archive_rel_change: str | int | float | None

    :param archive_period:
        Time, after which the conditions of archive event are checked in milliseconds.
        `Default:` :obj:`None` [Note_2]_
    :type archive_period: str | int | None

    :param archive_event_implemented:
        indicates if archive event for this attribute emitted by the code `Default:` False
    :type archive_event_implemented: bool

    :param archive_event_detect:
        enable or disable filtering for archive event emitted by the code. E.g., if user emits event,
        by the value changed less, then archive_abs_change or archive_rel_change - event will be filtered out `Default:` False
    :type archive_event_detect: bool

    :param delta_val:
        RDS (Read Different Set) difference between written and read values
        that triggers the :obj:`tango.AttrQuality.ALARM` quality.
        `Default:` :obj:`None` [Note_2]_
    :type delta_val: str

    :param delta_t:
        Minimum time, after which RDS (Read Different Set) difference
        is checked in milliseconds.
        `Default:` :obj:`None` [Note_2]_
    :type delta_t: str | int | None

    :param polling_period:
        Device polling period in milliseconds.
        `Default:` ``-1`` (no polling) [Note_3]_
    :type polling_period: int

    :param memorized:
        Attribute must be memorized. If :obj:`True`, the latest written value is
        stored in the Tango database (see also ``hw_memorized``).
        `Default:` :obj:`False`.
    :type memorized: bool

    :param hw_memorized:
        If :obj:`True`, memorized value will be restored by calling the attribute
        write method at startup and after each Init command
        (only applies if ``memorized`` is :obj:`True`).
        `Default:` :obj:`False`.
    :type hw_memorized: bool

    :param data_ready_event_implemented:
        indicates if data ready event for this attribute emitted by the code `Default:` False
    :type data_ready_event_implemented: bool

    :param class_name:
        name of the device class to which the attribute belongs
        (only used for error reporting when creating the attribute).
        `Default:` :obj:`None`
    :type class_name: str

    :param green_mode:
        Default green mode for read/write/isallowed functions.
        If True, run with green mode executor, otherwise run directly.
        `Default:` :obj:`True`.
    :type green_mode: bool

    :param read_green_mode:
        Green mode for read function.
        `Default:` value of ``green_mode``.
    :type read_green_mode: bool

    :param write_green_mode:
        Green mode for write function.
        `Default:` value of ``green_mode``.
    :type write_green_mode: bool

    :param isallowed_green_mode:
        Green mode for is_allowed function.
        `Default:` value of ``green_mode``.
    :type isallowed_green_mode: bool

    :param forwarded:
        If :obj:`True`, the attribute should be forwarded.
        `Default:` :obj:`False`.
    :type forwarded: bool

    .. [Note_1]

    .. note::
        If the attribute is defined with the `@attribute` decorator,
        then the read method docstring can be used to as the attribute description.
        The `doc` kwarg has the highest priority, then `description` kwarg,
        and then docstring::

            class TestDevice(Device):

                @attribute
                def my_attr1(self) -> float:
                    """This will be used as the docstring for my_attr1"""
                    return 1.5

                my_attr2 = attribute()

                def read_my_attr2(self) -> float:
                    """This docstring WON'T be used as the description"""
                    return 2.5

                @attribute(doc="This will be used as the docstring for my_attr3)
                def my_attr3(self) -> float:
                    """This docstring WON'T be used as the description"""
                    return 1.5

    .. [Note_2]

    .. note::
        The parameters , ``min_value``, ``max_value``, ``min_alarm``, ``max_alarm``,
        ``min_warning``, ``max_warning``, ``delta_val``,
        ``abs_change``, ``archive_abs_change``,
        must be a valid numerical value, represented as either a string, int or float
        compatible with the attribute's data type.

        Parameters ``standard_unit``, ``display_unit``,
        ``rel_change`` and ``archive_rel_change`` must be a valid numerical
        value, represented as either a string, int or float.

        Parameters ``period``, ``archive_period`` and ``delta_t``, must be
        a valid integer value, represented as either a string or int.

        In all cases, the value can also be :obj:`None`, or an empty string,
        to use the default. Typically, disabled.

    .. [Note_3]

    .. warning::
        The ``polling_period`` from the code is used *ONLY* if there is no polling period value stored in the Tango DB.
        After the first run, the value from the code will be stored in the Tango DB and will used for the following runs,
        even if the value in code is changed later. And vice versa: if the value in the Tango DB was changed (e.g. in Jive),
        but the code was not, the new value from the DB will be used.
        The value from the code will only be used again if the value in DB was deleted. Think of it like a default.

    .. versionadded:: 8.1.7
        added green_mode, read_green_mode and write_green_mode options

    .. versionadded:: 10.1.0
        added alarm_event_implemented, alarm_event_detect,
        change_event_implemented, change_event_detect,
        archive_event_implemented, archive_event_detect,
        data_ready_event_implemented options
    '''

    def __init__(self, fget=None, **kwargs):
        self._kwargs = dict(kwargs)
        self.name = kwargs.pop("name", None)
        class_name = kwargs.pop("class_name", None)
        forward = kwargs.get("forwarded", False)
        if forward:
            kwarg_copy = dict(kwargs)
            for k in ["name", "label", "forwarded"]:
                if k in kwarg_copy:
                    del kwarg_copy[k]
            if len(kwarg_copy):
                raise TypeError(
                    "Forwarded attributes only support 'label' and 'name' arguments"
                )
        else:
            green_mode = kwargs.pop("green_mode", True)
            self.read_green_mode = kwargs.pop("read_green_mode", green_mode)
            self.write_green_mode = kwargs.pop("write_green_mode", green_mode)
            self.isallowed_green_mode = kwargs.pop("isallowed_green_mode", green_mode)

            if not fget:
                fget = kwargs.pop("fread", None)

            if fget:
                if inspect.isroutine(fget):
                    self.fget = fget
                    if "doc" not in kwargs and "description" not in kwargs:
                        if fget.__doc__ is not None:
                            kwargs["doc"] = fget.__doc__
                kwargs["fget"] = fget

            fset = kwargs.pop("fwrite", kwargs.pop("fset", None))
            if fset:
                if inspect.isroutine(fset):
                    self.fset = fset
                kwargs["fset"] = fset

            fisallowed = kwargs.pop("fisallowed", None)
            if fisallowed:
                if inspect.isroutine(fisallowed):
                    self.fisallowed = fisallowed
                kwargs["fisallowed"] = fisallowed

        super().__init__(self.name, class_name)
        self.__doc__ = kwargs.get("doc", kwargs.get("description", "TANGO attribute"))
        if "dtype" in kwargs:
            dtype = kwargs["dtype"]
            dformat = kwargs.get("dformat")
            dtype, dformat, enum_labels = get_attribute_type_format(
                dtype, dformat, kwargs.get("enum_labels")
            )
            kwargs["dtype"], kwargs["dformat"] = dtype, dformat
            if enum_labels:
                kwargs["enum_labels"] = enum_labels
        self.build_from_dict(kwargs)

    def get_attribute(self, obj):
        return obj.get_device_attr().get_attr_by_name(self.attr_name)

    # --------------------
    # descriptor interface
    # --------------------

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        return self.get_attribute(obj)

    def __set__(self, obj, value):
        attr = self.get_attribute(obj)
        set_complex_value(attr, value)

    def __delete__(self, obj):
        obj.remove_attribute(self.attr_name)

    def setter(self, fset):
        """
        To be used as a decorator, ``@attribute.setter``. Defines the decorated method
        as the write attribute method to be called when a client writes
        the attribute. Equivalent to ``@attribute.write``.
        """
        self.fset = fset
        if self.attr_write == AttrWriteType.READ:
            if getattr(self, "fget", None):
                self.attr_write = AttrWriteType.READ_WRITE
            else:
                self.attr_write = AttrWriteType.WRITE
        return self

    def write(self, fset):
        """
        To be used as a decorator, ``@attribute.write``. Defines the decorated method
        as the write attribute method to be called when a client writes
        the attribute. Equivalent to ``@attribute.setter``.
        """
        return self.setter(fset)

    def getter(self, fget):
        """
        To be used as a decorator, ``@attribute.getter``. Defines the decorated method
        as the read attribute method to be called when a client reads
        the attribute. Equivalent to ``@attribute.read``.
        """
        self.fget = fget
        if self.attr_write == AttrWriteType.WRITE:
            if getattr(self, "fset", None):
                self.attr_write = AttrWriteType.READ_WRITE
            else:
                self.attr_write = AttrWriteType.READ
        return self

    def read(self, fget):
        """
        To be used as a decorator, ``@attribute.read``. Defines the decorated method
        as the read attribute method to be called when a client reads
        the attribute. Equivalent to ``@attribute.getter``.
        """
        return self.getter(fget)

    def is_allowed(self, fisallowed):
        """
        To be used as a decorator, ``@attribute.is_allowed``. Defines the decorated
        method as the is allowed attribute method
        """
        self.fisallowed = fisallowed
        return self

    def __call__(self, fget):
        return type(self)(fget=fget, **self._kwargs)


def __build_command_doc_in(f, dtype_in):
    if dtype_in not in {CmdArgType.DevVoid, None}:
        sig = inspect.signature(f)
        params = list(sig.parameters.values())

        if len(params) > 1:
            param_name = params[1].name
        else:
            param_name = "arg"
        dtype_in_str = str(dtype_in)
        if not isinstance(dtype_in, str):
            try:
                dtype_in_str = dtype_in.__name__
            except Exception:
                pass
        result = (
            f":param {param_name}: (not documented)\n"
            f":type {param_name}: {dtype_in_str}"
        )
    else:
        result = "No input parameter (DevVoid)"
    return result


def __build_command_doc_out(dtype_out):
    if dtype_out not in {CmdArgType.DevVoid, None}:
        dtype_out_str = str(dtype_out)
        if not isinstance(dtype_out, str):
            try:
                dtype_out_str = dtype_out.__name__
            except Exception:
                pass
        result = f":return: (not documented)\n" f":rtype: {dtype_out_str}"
    else:
        result = "No output parameter (DevVoid)"
    return result


def __build_command_doc(name, doc_in, doc_out):
    doc = f"'{name}' TANGO command"
    if doc_in:
        doc += f"\n\n{doc_in}"
    if doc_out:
        doc += f"\n\n{doc_out}"
    return doc


class _DevVoid:
    def __repr__(self):
        return "DevVoid"

    def __str__(self):
        return "DevVoid"


def command(
    f=None,
    dtype_in: Any = _DevVoid,
    dformat_in=None,
    doc_in="",
    dtype_out: Any = _DevVoid,
    dformat_out=None,
    doc_out="",
    display_level=None,
    polling_period=None,
    green_mode=True,
    fisallowed=None,
    cmd_green_mode=None,
    isallowed_green_mode=None,
):
    """
    Declares a new tango command in a :class:`Device`.
    To be used like a decorator in the methods you want to declare as
    tango commands. The following example declares commands:

        * `void TurnOn(void)`
        * `void Ramp(DevDouble current)`
        * `DevBool Pressurize(DevDouble pressure)`

    ::

        class PowerSupply(Device):

            @command
            def TurnOn(self):
                self.info_stream('Turning on the power supply')

            @command(dtype_in=float)
            def Ramp(self, current):
                self.info_stream('Ramping on %f...' % current)

            @command(dtype_in=float, doc_in='the pressure to be set',
                     dtype_out=bool, doc_out='True if it worked, False otherwise')
            def Pressurize(self, pressure):
                self.info_stream('Pressurizing to %f...' % pressure)
                return True

    .. note::
        avoid using *dformat* parameter. If you need a SPECTRUM
        attribute of say, boolean type, use instead ``dtype=(bool,)``.

    :param dtype_in:
        a :ref:`data type <pytango-hlapi-datatypes>` describing the
        type of parameter. Default is None meaning no parameter.

    :param dformat_in: parameter data format. Default is None.
    :type dformat_in: AttrDataFormat

    :param doc_in: parameter documentation
    :type doc_in: str

    :param dtype_out:
        a :ref:`data type <pytango-hlapi-datatypes>` describing the
        type of return value. Default is None meaning no return value.

    :param dformat_out: return value data format. Default is None.
    :type dformat_out: AttrDataFormat

    :param doc_out: return value documentation
    :type doc_out: str

    :param display_level: display level for the command (optional)
    :type display_level: DispLevel

    :param polling_period: polling period in milliseconds (optional)
    :type polling_period: int

    :param green_mode: DEPRECATED: green mode for command method. If True: run with green mode executor, if False: run directly.
        See the green_mode parameter deprecation note below for more details.
    :type green_mode: bool

    :param fisallowed: is allowed method for command
    :type fisallowed: str or callable

    :param cmd_green_mode: green mode for command method. If True: run with green mode executor, if False: run directly
        See the green_mode parameter deprecation note below for more details.
    :type cmd_green_mode: bool

    :param isallowed_green_mode: green mode for isallowed method. If True: run with green mode executor, if False: run directly
        See the green_mode parameter deprecation note below for more details.
    :type isallowed_green_mode: bool

    .. versionadded:: 8.1.7
        added green_mode option

    .. versionadded:: 9.2.0
        added display_level and polling_period optional argument

    .. versionadded:: 9.4.0
        added fisallowed option

    .. versionadded:: 10.0.0
     added cmd_green_mode and isallowed_green_mode options

    .. versionchanged:: 10.0.0
        the way that the green_mode parameter is interpreted was changed to be consistent with the same parameter for attributes.
        Now it expects bool, which indicates, if methods should be run with executor (green_mode=True, default) or bypass it (green_mode=False)
        Before it was either green_mode=None - use executor or green_mode=GreenMode.Synchronous - bypass it.
        However, due python by default casts GreenMode.Synchronous (which is int value 0) to False bool,
        old code is automatically backward compatible.

    .. deprecated:: 10.0.0
         green_mode parameter is deprecated and may be removed in future.  Use cmd_green_mode and isallowed_green_mode parameters instead.
         The new parameters match how attributes and pipes are defined, offer more flexibility, and are clearer.
         If you use both old green_mode, and new isallowed_green_mode and cmd_green_mode - the new ones take priority.

    """
    if f is None:
        return functools.partial(
            command,
            dtype_in=dtype_in,
            dformat_in=dformat_in,
            doc_in=doc_in,
            dtype_out=dtype_out,
            dformat_out=dformat_out,
            doc_out=doc_out,
            display_level=display_level,
            polling_period=polling_period,
            green_mode=green_mode,
            fisallowed=fisallowed,
            cmd_green_mode=cmd_green_mode,
            isallowed_green_mode=isallowed_green_mode,
        )
    name = f.__name__

    first_arg_type, return_type = __get_in_out_types_from_method_type_hints(f)

    if dtype_out == _DevVoid:
        if return_type is not None:
            dtype_out, dformat_out, _, _ = parse_type_hint(
                return_type, caller="command"
            )
        else:
            dtype_out = None

    if dtype_in == _DevVoid:
        if first_arg_type is not None:
            dtype_in, dformat_in, _, _ = parse_type_hint(
                first_arg_type, caller="command"
            )
        else:
            dtype_in = None

    dtype_in, format_in, _ = get_attribute_type_format(dtype_in, dformat_in, None)
    dtype_out, format_out, _ = get_attribute_type_format(dtype_out, dformat_out, None)

    if parse_docstring is not None and f.__doc__ is not None:
        try:
            parsed_doc = parse_docstring(f.__doc__)
            if doc_in == "" and len(parsed_doc.params) > 0:
                doc_in = (
                    f"{parsed_doc.params[0].arg_name} ({parsed_doc.params[0].type_name}):"
                    f" {parsed_doc.params[0].description}"
                )

            if doc_out == "" and parsed_doc.returns is not None:
                doc_out = f"returns ({parsed_doc.returns.type_name}): {parsed_doc.returns.description}"
        except Exception:
            pass

    if doc_in == "":
        doc_in = __build_command_doc_in(f, dtype_in)
    if doc_out == "":
        doc_out = __build_command_doc_out(dtype_out)

    din = [from_typeformat_to_type(dtype_in, format_in), doc_in]
    dout = [from_typeformat_to_type(dtype_out, format_out), doc_out]

    config_dict = {}
    if display_level is not None:
        config_dict["Display level"] = display_level
    if polling_period is not None:
        config_dict["Polling period"] = polling_period
    if fisallowed is not None:
        config_dict["Is allowed"] = fisallowed
    config_dict["Is allowed green_mode"] = (
        isallowed_green_mode if isallowed_green_mode is not None else green_mode
    )

    cmd_green_mode = cmd_green_mode if cmd_green_mode is not None else green_mode
    command_method = __get_wrapped_command_method(f, cmd_green_mode)
    command_method.__tango_command__ = name, [din, dout, config_dict]

    # try to create a minimalistic __doc__
    if command_method.__doc__ is None:
        try:
            command_method.__doc__ = __build_command_doc(name, doc_in, doc_out)
        except Exception:
            command_method.__doc__ = "TANGO command"

    return command_method


def __get_wrapped_command_method(cmd_method, cmd_green_mode):
    already_wrapped = hasattr(cmd_method, "__access_wrapped__")
    if already_wrapped:
        return cmd_method

    if cmd_green_mode:

        @functools.wraps(cmd_method)
        def wrapped_command_method(*args, **kwargs):
            return get_worker().execute(cmd_method, *args, **kwargs)

    else:
        wrapped_command_method = cmd_method

    if _force_tracing:
        wrapped_command_method = _forcefully_traced_method(wrapped_command_method)
    if wrapped_command_method is not cmd_method:
        wrapped_command_method.__access_wrapped__ = True
    return wrapped_command_method


class _BaseProperty:
    def __init__(self, dtype=None, doc="", default_value=None, update_db=False):
        self.name = None
        if dtype:
            dtype = from_typeformat_to_type(*get_tango_type_format(dtype))
        self.dtype = dtype
        self.doc = doc
        self.default_value = default_value
        self.update_db = update_db
        self.__doc__ = doc or "TANGO property"

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        return obj._tango_properties.get(self.name)

    def __set__(self, obj, value):
        obj._tango_properties[self.name] = value
        if self.update_db:
            import tango

            db = tango.Util.instance().get_database()
            db.put_device_property(obj.get_name(), {self.name: value})

    def __delete__(self, obj):
        del obj._tango_properties[self.name]


class device_property(_BaseProperty):
    """
    Declares a new tango device property in a :class:`Device`. To be
    used like the python native :obj:`property` function. For example,
    to declare a scalar, `tango.DevString`, device property called
    *host* in a *PowerSupply* :class:`Device` do::

        from tango.server import Device, DeviceMeta
        from tango.server import device_property

        class PowerSupply(Device):

            host = device_property(dtype=str)
            port = device_property(dtype=int, mandatory=True)

    :param dtype: Data type (see :ref:`pytango-data-types`)
    :param doc: property documentation (optional)
    :param mandatory (optional: default is False)
    :param default_value: default value for the property (optional)
    :param update_db: tells if set value should write the value to database.
                     [default: False]
    :type update_db: bool

    .. versionadded:: 8.1.7
        added update_db option
    """

    def __init__(
        self, dtype=None, doc="", mandatory=False, default_value=None, update_db=False
    ):
        super().__init__(dtype, doc, default_value, update_db)
        self.mandatory = mandatory
        if mandatory and default_value is not None:
            msg = (
                "Invalid arguments: 'mandatory' is True, so 'default_value' must be None. "
                "A mandatory device property value must be defined in the Tango Database "
                "so it cannot have a default."
            )
            raise ValueError(msg)


class class_property(_BaseProperty):
    """
    Declares a new tango class property in a :class:`Device`. To be
    used like the python native :obj:`property` function. For example,
    to declare a scalar, `tango.DevString`, class property called
    *port* in a *PowerSupply* :class:`Device` do::

        from tango.server import Device, DeviceMeta
        from tango.server import class_property

        class PowerSupply(Device):

            port = class_property(dtype=int, default_value=9788)

    :param dtype: Data type (see :ref:`pytango-data-types`)
    :param doc: property documentation (optional)
    :param default_value: default value for the property (optional)
    :param update_db: tells if set value should write the value to database.
                     [default: False]
    :type update_db: bool

    .. versionadded:: 8.1.7
        added update_db option
    """

    pass


def __to_callback(callback, cb_type, green_mode):
    if callback is None:
        return lambda: None

    err_msg = (
        f"{cb_type} must be a callable or " "sequence <callable [, args, [, kwargs]]>"
    )
    if callable(callback):
        f = callback
    elif is_non_str_seq(callback):
        length = len(callback)
        if length < 1 or length > 3:
            raise TypeError(err_msg)
        cb = callback[0]
        if not callable(cb):
            raise TypeError(err_msg)
        args, kwargs = [], {}
        if length > 1:
            args = callback[1]
        if length > 2:
            kwargs = callback[2]
        f = functools.partial(cb, *args, **kwargs)
    else:
        raise TypeError(err_msg)

    if green_mode == GreenMode.Asyncio and not _is_coroutine_function(f):

        @functools.wraps(f)
        async def async_callback():
            return f()

        return async_callback
    else:
        return f


def _to_classes(classes):
    uclasses = []
    if is_seq(classes):
        for klass_info in classes:
            if is_seq(klass_info):
                if len(klass_info) == 2:
                    klass_klass, klass = klass_info
                    klass_name = klass.__name__
                else:
                    klass_klass, klass, klass_name = klass_info
            else:
                if not hasattr(klass_info, "_api") or klass_info._api < 2:
                    raise Exception(
                        "When giving a single class, it must "
                        "implement HLAPI (see tango.server)"
                    )
                klass_klass = klass_info.TangoClassClass
                klass_name = klass_info.TangoClassName
                klass = klass_info
            uclasses.append((klass_klass, klass, klass_name))
    else:
        for klass_name, klass_info in classes.items():
            if is_seq(klass_info):
                if len(klass_info) == 2:
                    klass_klass, klass = klass_info
                else:
                    klass_klass, klass, klass_name = klass_info
            else:
                if not hasattr(klass_info, "_api") or klass_info._api < 2:
                    raise Exception(
                        "When giving a single class, it must "
                        "implement HLAPI (see tango.server)"
                    )
                klass_klass = klass_info.TangoClassClass
                klass_name = klass_info.TangoClassName
                klass = klass_info
            uclasses.append((klass_klass, klass, klass_name))
    return uclasses


def _add_classes(util, classes):
    for class_info in _to_classes(classes):
        util.add_class(*class_info)


def _get_class_green_mode(classes, green_mode):
    if green_mode is not None:
        default_green_mode = green_mode
    else:
        default_green_mode = get_green_mode()

    green_modes = set()
    for _, klass, _ in _to_classes(classes):
        device_green_mode = getattr(klass, "green_mode", None)
        if device_green_mode is None:
            device_green_mode = default_green_mode
        green_modes.add(device_green_mode)
    if len(green_modes) > 1:
        raise ValueError(
            f"Devices with mixed green modes cannot be run in the same device "
            f"server process. Modes: {green_modes}. Classes: {classes}."
        )
    elif len(green_modes) == 0:
        raise ValueError(
            "No device classes specified - cannot run device server "
            "process with no classes."
        )
    unanimous_green_mode = green_modes.pop()
    return unanimous_green_mode


def __server_run(
    classes,
    args=None,
    msg_stream=sys.stdout,
    util=None,
    event_loop=None,
    pre_init_callback=None,
    post_init_callback=None,
    green_mode=None,
):
    green_mode = _get_class_green_mode(classes, green_mode)

    write = msg_stream.write if msg_stream else lambda msg: None

    if args is None:
        args = sys.argv

    pre_init_callback = __to_callback(
        pre_init_callback, "pre_init_callback", green_mode
    )
    post_init_callback = __to_callback(
        post_init_callback, "post_init_callback", green_mode
    )

    if util is None:
        util = Util.init(args)

    if green_mode in (GreenMode.Gevent, GreenMode.Asyncio):
        util.set_serial_model(SerialModel.NO_SYNC)

    worker = get_executor(green_mode)
    set_worker(worker)

    if event_loop is not None:
        event_loop = functools.partial(worker.execute, event_loop)
        util.server_set_event_loop(event_loop)

    log = logging.getLogger("tango")

    def tango_loop():
        log.debug("server loop started")
        worker.execute(pre_init_callback)
        _add_classes(util, classes)
        util.server_init()
        worker.execute(post_init_callback)
        write("Ready to accept request\n")
        util.server_run()
        log.debug("server loop exit")

    worker.run(tango_loop, wait=True)
    return util


def run(
    classes,
    args=None,
    msg_stream=sys.stdout,
    verbose=False,
    util=None,
    event_loop=None,
    pre_init_callback=None,
    post_init_callback=None,
    green_mode=None,
    raises=False,
    err_stream=sys.stderr,
):
    """
    Provides a simple way to run a tango server. It handles exceptions
    by writting a message to the msg_stream.

    :Examples:

        Example 1: registering and running a PowerSupply inheriting from
        :class:`~tango.server.Device`::

            from tango.server import Device, run

            class PowerSupply(Device):
                pass

            run((PowerSupply,))

        Example 2: registering and running a MyServer defined by tango
        classes `MyServerClass` and `MyServer`::

            from tango import Device_4Impl, DeviceClass
            from tango.server import run

            class MyServer(Device_4Impl):
                pass

            class MyServerClass(DeviceClass):
                pass

            run({'MyServer': (MyServerClass, MyServer)})

        Example 3: registering and running a MyServer defined by tango
        classes `MyServerClass` and `MyServer`::

            from tango import Device_4Impl, DeviceClass
            from tango.server import Device, run

            class PowerSupply(Device):
                pass

            class MyServer(Device_4Impl):
                pass

            class MyServerClass(DeviceClass):
                pass

            run([PowerSupply, [MyServerClass, MyServer]])
            # or: run({'MyServer': (MyServerClass, MyServer)})

    .. note::
       the order of registration of tango classes defines the order
       tango uses to initialize the corresponding devices.
       if using a dictionary as argument for classes be aware that the
       order of registration becomes arbitrary. If you need a
       predefined order use a sequence or an OrderedDict.

    :param classes:
        Defines for which Tango Device Classes the server will run.
        If :class:`~dict` is provided, it's key is the tango class name
        and value is either:

            | :class:`~tango.server.Device`
            | two element sequence: :class:`~tango.DeviceClass`, :class:`~tango.DeviceImpl`
            | three element sequence: :class:`~tango.DeviceClass`, :class:`~tango.DeviceImpl`, tango class name :class:`~str`
    :type classes: Sequence[tango.server.Device] | dict

    :param args:
        list of command line arguments [default: None, meaning use
        sys.argv]
    :type args: list

    :param msg_stream:
        stream where to put messages [default: sys.stdout]

    :param util:
        PyTango Util object [default: None meaning create a Util
        instance]
    :type util: :class:`~tango.Util`

    :param event_loop: event_loop callable
    :type event_loop: callable

    :param pre_init_callback:
        an optional callback that is executed between the calls
        Util.init and Util.server_init
        The optional `pre_init_callback` can be a callable (without
        arguments) or a tuple where the first element is the callable,
        the second is a list of arguments (optional) and the third is a
        dictionary of keyword arguments (also optional).
    :type pre_init_callback:
        callable or tuple

    :param post_init_callback:
        an optional callback that is executed between the calls
        Util.server_init and Util.server_run
        The optional `post_init_callback` can be a callable (without
        arguments) or a tuple where the first element is the callable,
        the second is a list of arguments (optional) and the third is a
        dictionary of keyword arguments (also optional).
    :type post_init_callback:
        callable or tuple

    :param raises:
        Disable error handling and propagate exceptions from the server
    :type raises: bool

    :param err_stream:
        stream where to put catched exceptions [default: sys.stderr]

    :return: The Util singleton object
    :rtype: :class:`~tango.Util`

    .. versionadded:: 8.1.2

    .. versionchanged:: 8.1.4
        when classes argument is a sequence, the items can also be
        a sequence <TangoClass, TangoClassClass>[, tango class name]

    .. versionchanged:: 9.2.2
        `raises` argument has been added

    .. versionchanged:: 9.5.0
        `pre_init_callback` argument has been added

    .. versionchanged:: 10.0.0
        `err_stream` argument has been added
    """
    server_run = functools.partial(
        __server_run,
        classes,
        args=args,
        msg_stream=msg_stream,
        util=util,
        event_loop=event_loop,
        pre_init_callback=pre_init_callback,
        post_init_callback=post_init_callback,
        green_mode=green_mode,
    )
    # Run the server without error handling
    if raises:
        return server_run()
    # Run the server with error handling
    write = err_stream.write if err_stream else lambda msg: None
    try:
        return server_run()
    except KeyboardInterrupt:
        write("Exiting: Keyboard interrupt\n")
    except DevFailed as df:
        write("Exiting: Server exited with tango.DevFailed:\n" + str(df) + "\n")
        if verbose:
            write(traceback.format_exc())
    except Exception as e:
        write("Exiting: Server exited with unforseen exception:\n" + str(e) + "\n")
        if verbose:
            write(traceback.format_exc())
    write("\nExited\n")


def server_run(
    classes,
    args=None,
    msg_stream=sys.stdout,
    verbose=False,
    util=None,
    event_loop=None,
    pre_init_callback=None,
    post_init_callback=None,
    green_mode=None,
    err_stream=sys.stderr,
):
    """
    Since PyTango 8.1.2 it is just an alias to
    :func:`~tango.server.run`. Use :func:`~tango.server.run`
    instead.

    .. versionadded:: 8.0.0

    .. versionchanged:: 8.0.3
        Added `util` keyword parameter.
        Returns util object

    .. versionchanged:: 8.1.1
        Changed default msg_stream from *stderr* to *stdout*
        Added `event_loop` keyword parameter.
        Returns util object

    .. versionchanged:: 8.1.2
        Added `post_init_callback` keyword parameter

    .. deprecated:: 8.1.2
        Use :func:`~tango.server.run` instead.

    .. versionchanged:: 9.5.0
        `pre_init_callback` argument has been added

    .. versionchanged:: 10.0.0
        `err_stream` argument has been added

    """
    return run(
        classes,
        args=args,
        msg_stream=msg_stream,
        verbose=verbose,
        util=util,
        event_loop=event_loop,
        pre_init_callback=pre_init_callback,
        post_init_callback=post_init_callback,
        green_mode=green_mode,
        err_stream=sys.stderr,
    )


class Device(BaseDevice, metaclass=DeviceMeta):
    """
    Device class for the high-level API.

    All device-specific classes should inherit from this class.
    """


# Avoid circular imports
from tango.tango_object import Server  # noqa: E402
