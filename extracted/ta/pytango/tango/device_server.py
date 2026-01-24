# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.
"""

from dataclasses import dataclass

import copy
import functools
import inspect
import os
import types
import numbers

from tango._tango import (
    AttrQuality,
    AttributeConfig,
    AttributeConfig_2,
    AttributeConfig_3,
    DeviceImpl,
    Device_2Impl,
    Device_3Impl,
    Device_6Impl,
    DevFailed,
    Attribute,
    AttrWriteType,
    Attr,
    Logger,
    AttrDataFormat,
    DispLevel,
    UserDefaultAttrProp,
    StdStringVector,
    EventType,
    constants,
    CmdArgType,
    EncodedAttribute,
)
from tango.pyutil import Util
from tango.release import Release
from tango.utils import (
    get_latest_device_class,
    set_complex_value,
    is_pure_str,
    parse_type_hint,
    get_attribute_type_format,
    _force_tracing,
    _forcefully_traced_method,
    _get_non_tango_source_location,
    _exception_converter,
    _InterfaceDefinedByIDL,
)
from tango.green import get_executor
from tango.attr_data import AttrData

from tango.log4tango import TangoStream

__docformat__ = "restructuredtext"

__all__ = (
    "MultiAttrProp",
    "device_server_init",
)

# Worker access

_WORKER = get_executor()


def set_worker(worker):
    global _WORKER
    _WORKER = worker


def get_worker():
    return _WORKER


# patcher for methods
def run_in_executor(fn):
    if not hasattr(fn, "wrapped_with_executor"):

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return get_worker().execute(fn, *args, **kwargs)

        # to avoid double wrapping we add an empty field, and then use it to check, whether function is already wrapped
        wrapper.wrapped_with_executor = True
        return wrapper
    else:
        return fn


def get_source_location(source=None):
    """Helper function that provides source location for logging functions.
    :param source:
        (optional) Method or function, which will be unwrapped of decorated wrappers
        and inspected for location. If not provided - current stack will be used to deduce the location.
    :type source: Callable

    :return:
        Tuple (filename, lineno)
    :rtype :tuple:
    """
    location = _get_non_tango_source_location(source)
    filename = os.path.basename(location.filepath)
    return filename, location.lineno


# Note: the inheritance below doesn't call get_latest_device_class(),
#       because such dynamic inheritance breaks auto-completion in IDEs.
#       Instead, we manually provide the correct class here, and verify
#       that the inheritance is correct via a unit test, in test_server.py.
class LatestDeviceImpl(Device_6Impl):
    __doc__ = f"""\
    Latest implementation of the TANGO device base class (alias for {get_latest_device_class().__name__}).

    It inherits from CORBA classes where all the network layer is implemented.
    """

    def __init__(self, *args):
        super().__init__(*args)
        # Set up python related versions for DevInfo
        self.add_version_info("PyTango", Release.version_long)
        self.add_version_info("Build.PyTango.Python", constants.Compile.PY_VERSION)
        self.add_version_info("Build.PyTango.cppTango", constants.Compile.TANGO_VERSION)
        self.add_version_info("Build.PyTango.NumPy", constants.Compile.NUMPY_VERSION)
        self.add_version_info(
            "Build.PyTango.Pybind11", constants.Compile.PYBIND11_VERSION
        )
        self.add_version_info("Python", constants.Runtime.PY_VERSION)
        self.add_version_info("NumPy", constants.Runtime.NUMPY_VERSION)


@dataclass
class MultiAttrProp(_InterfaceDefinedByIDL):
    """This class represents the python interface for the Tango IDL object
    MultiAttrProp."""

    label: str = ""
    description: str = ""
    unit: str = ""
    standard_unit: str = ""
    display_unit: str = ""
    format: str = ""
    min_value: str = ""
    max_value: str = ""
    min_alarm: str = ""
    max_alarm: str = ""
    min_warning: str = ""
    max_warning: str = ""
    delta_t: str = ""
    delta_val: str = ""
    event_period: str = ""
    archive_period: str = ""
    rel_change: str = ""
    abs_change: str = ""
    archive_rel_change: str = ""
    archive_abs_change: str = ""

    def __post_init__(self):
        self._initialized = True


def __Attribute__get_properties(self, attr_cfg=None):
    """
    get_properties(self: Attribute, attr_cfg: AttributeConfig = None) -> AttributeConfig

        Get attribute properties.

        :param conf: the config object to be filled with
                     the attribute configuration. Default is None meaning the
                     method will create internally a new :obj:`tango.AttributeConfig_5`
                     and return it.
                     Can be :obj:`tango.AttributeConfig`, :obj:`tango.AttributeConfig_2`,
                     :obj:`tango.AttributeConfig_3`, :obj:`tango.AttributeConfig_5` or
                     :obj:`tango.MultiAttrProp`

        :returns: the config object filled with attribute configuration information
        :rtype: :obj:`tango.AttributeConfig`

        New in PyTango 7.1.4
    """

    if attr_cfg is None:
        attr_cfg = MultiAttrProp()
    if not isinstance(attr_cfg, MultiAttrProp):
        raise TypeError("attr_cfg must be an instance of MultiAttrProp")
    return self._get_properties_multi_attr_prop(attr_cfg)


def __Attribute__set_properties(self, attr_cfg, dev=None):
    """
    set_properties(self: Attribute, attr_cfg: AttributeConfig, dev: DeviceImpl = None)

        Set attribute properties.

        This method sets the attribute properties value with the content
        of the fields in the :obj:`tango.AttributeConfig`/ :obj:`tango.AttributeConfig_3` object

        :param conf: the config object.
        :type conf: :obj:`tango.AttributeConfig` or :obj:`tango.AttributeConfig_3`
        :param dev: the device (not used, maintained
                    for backward compatibility)
        :type dev: :obj:`tango.DeviceImpl`

        New in PyTango 7.1.4
    """

    if not isinstance(attr_cfg, MultiAttrProp):
        raise TypeError("attr_cfg must be an instance of MultiAttrProp")
    return self._set_properties_multi_attr_prop(attr_cfg)


def __Attribute__str(self):
    return f"{self.__class__.__name__}({self.get_name()})"


def __Attribute__set_value(self, *args):
    """
    .. function:: set_value(self, data)
                  set_value(self, str_data, data)
        :noindex:

    Set internal attribute value.

    This method stores the attribute read value inside the object.
    This method also stores the date when it is called and initializes the
    attribute quality factor.

    :param data: the data to be set. Data must be compatible with the attribute type and format.
                 E.g., sequence for SPECTRUM and a SEQUENCE of equal-length SEQUENCES
                 for IMAGE attributes.
                 The recommended sequence is a C continuous and aligned numpy
                 array, as it can be optimized.
    :param str_data: special variation for DevEncoded data type. In this case 'data' must
                     be a str or an object with the buffer interface.
    :type str_data: str

    .. versionchanged:: 10.1.0
        The dim_x and dim_y parameters were removed.
    """

    if not len(args):
        raise TypeError("set_value method must be called with at least one argument!")

    for arg in args:
        if arg is None:
            raise TypeError("set_value method cannot be called with None!")

    if self.get_data_type() == CmdArgType.DevEncoded and not isinstance(
        args[0], EncodedAttribute
    ):
        if len(args) > 2:
            raise TypeError(
                "Too many arguments. "
                "Note, that dim_x and dim_y arguments are no longer supported."
            )
    else:
        if len(args) > 1:
            raise TypeError(
                "Too many arguments. "
                "Note, that dim_x and dim_y arguments are no longer supported."
            )

    self._set_value(*args)


def __Attribute__set_value_date_quality(self, *args):
    """
    .. function::   set_value_date_quality(self, data, time_stamp, quality)
                    set_value_date_quality(self, str_data, data, time_stamp, quality)
        :noindex:

    Set internal attribute value, date and quality factor.

    This method stores the attribute read value, the date and the attribute quality
    factor inside the object.

    :param data: the data to be set. Data must be compatible with the attribute type and format.
                 E.g., sequence for SPECTRUM and a SEQUENCE of equal-length SEQUENCES
                 for IMAGE attributes.
                 The recommended sequence is a C continuous and aligned numpy
                 array, as it can be optimized.
    :param str_data: special variation for DevEncoded data type. In this case 'data' must
                     be a str or an object with the buffer interface.
    :type str_data: str
    :param time_stamp: the time stamp
    :type time_stamp: double
    :param quality: the attribute quality factor
    :type quality: AttrQuality

    .. versionchanged:: 10.1.0
        The dim_x and dim_y parameters were removed.
    """

    if len(args) < 3:
        raise TypeError(
            "set_value_date_quality method must be called with at least three arguments!"
        )

    for arg in args:
        if arg is None:
            raise TypeError("set_value_date_quality method cannot be called with None!")

    if self.get_data_type() == CmdArgType.DevEncoded and not isinstance(
        args[0], EncodedAttribute
    ):
        if len(args) > 4:
            raise TypeError(
                "Too many arguments. "
                "Note, that dim_x and dim_y arguments are no longer supported."
            )
        elif (
            len(args) == 4
            and not isinstance(args[-1], AttrQuality)
            and isinstance(args[-1], numbers.Number)
        ):
            raise TypeError(
                f"Last argument, {args[3]}, has the incorrect type: {type(args[3])}. "
                "It must be AttrQuality. "
                "Note, that dim_x and dim_y arguments are no longer supported."
            )
    else:
        if len(args) > 3:
            raise TypeError(
                "Too many arguments. "
                "Note, that dim_x and dim_y arguments are no longer supported."
            )
        elif (
            len(args) == 3
            and not isinstance(args[-1], AttrQuality)
            and isinstance(args[-1], numbers.Number)
        ):
            raise TypeError(
                f"Last argument, {args[2]}, has the incorrect type: {type(args[2])}. "
                "It must be AttrQuality. "
                "Note, that dim_x and dim_y arguments are no longer supported."
            )

    self._set_value_date_quality(*args)


def __init_Attribute():
    Attribute.__str__ = __Attribute__str
    Attribute.__repr__ = __Attribute__str
    Attribute.get_properties = __Attribute__get_properties
    Attribute.set_properties = __Attribute__set_properties

    Attribute.set_value = __Attribute__set_value
    Attribute.set_value_date_quality = __Attribute__set_value_date_quality


def __DeviceImpl__get_device_class(self):
    """
    get_device_class(self)

        Get device class singleton.

        :returns: the device class singleton (device_class field)
        :rtype: DeviceClass

    """
    try:
        return self._device_class_instance
    except AttributeError:
        return None


def __DeviceImpl__get_device_properties(self, ds_class=None):
    """
    get_device_properties(self, ds_class = None)

        Utility method that fetches all the device properties from the database
        and converts them into members of this DeviceImpl.

        :param ds_class: the DeviceClass object. Optional. Default value is
                         None meaning that the corresponding DeviceClass object for this
                         DeviceImpl will be used
        :type ds_class: DeviceClass

        :raises DevFailed:
    """
    if ds_class is None:
        try:
            # Call this method in a try/except in case this is called during the DS shutdown sequence
            ds_class = self.get_device_class()
        except Exception:
            return
    try:
        pu = self.prop_util = ds_class.prop_util
        self.device_property_list = copy.deepcopy(ds_class.device_property_list)
        class_prop = ds_class.class_property_list
        pu.get_device_properties(self, class_prop, self.device_property_list)
        for prop_name in class_prop:
            setattr(self, prop_name, pu.get_property_values(prop_name, class_prop))
        for prop_name in self.device_property_list:
            setattr(
                self,
                prop_name,
                self.prop_util.get_property_values(
                    prop_name, self.device_property_list
                ),
            )
    except DevFailed as df:
        print(80 * "-")
        print(df)
        raise df


def __DeviceImpl__add_attribute(
    self, attr, r_meth=None, w_meth=None, is_allo_meth=None
):
    """
    add_attribute(self, attr, r_meth=None, w_meth=None, is_allo_meth=None) -> Attr

        Add a new attribute to the device attribute list.

        Please, note that if you add
        an attribute to a device at device creation time, this attribute will be added
        to the device class attribute list. Therefore, all devices belonging to the
        same class created after this attribute addition will also have this attribute.

        If you pass a reference to unbound method for read, write or is_allowed method
        (e.g. DeviceClass.read_function or self.__class__.read_function),
        during execution the corresponding bound method (self.read_function) will be used.

        Note: Calling the synchronous add_attribute method from a coroutine function in
        an asyncio server may cause a deadlock.
        Use ``await`` :meth:`async_add_attribute` instead.
        However, if overriding the synchronous method ``initialize_dynamic_attributes``,
        then the synchronous add_attribute method must be used, even in asyncio servers.

        :param attr: the new attribute to be added to the list.
        :type attr: server.attribute or Attr or AttrData
        :param r_meth: the read method to be called on a read request
                       (if attr is of type server.attribute, then use the
                       fget field in the attr object instead)
        :type r_meth: callable
        :param w_meth: the write method to be called on a write request
                       (if attr is writable)
                       (if attr is of type server.attribute, then use the
                       fset field in the attr object instead)
        :type w_meth: callable
        :param is_allo_meth: the method that is called to check if it
                             is possible to access the attribute or not
                             (if attr is of type server.attribute, then use the
                             fisallowed field in the attr object instead)
        :type is_allo_meth: callable

        :returns: the newly created attribute.
        :rtype: Attr

        :raises DevFailed:
    """

    return __DeviceImpl__add_attribute_realization(
        self, attr, r_meth, w_meth, is_allo_meth
    )


async def __DeviceImpl__async_add_attribute(
    self, attr, r_meth=None, w_meth=None, is_allo_meth=None
):
    """
    async_add_attribute(self, attr, r_meth=None, w_meth=None, is_allo_meth=None) -> Attr

        Add a new attribute to the device attribute list.

        Please, note that if you add
        an attribute to a device at device creation time, this attribute will be added
        to the device class attribute list. Therefore, all devices belonging to the
        same class created after this attribute addition will also have this attribute.

        If you pass a reference to unbound method for read, write or is_allowed method
        (e.g. DeviceClass.read_function or self.__class__.read_function),
        during execution the corresponding bound method (self.read_function) will be used.

        :param attr: the new attribute to be added to the list.
        :type attr: server.attribute or Attr or AttrData
        :param r_meth: the read method to be called on a read request
                       (if attr is of type server.attribute, then use the
                       fget field in the attr object instead)
        :type r_meth: callable
        :param w_meth: the write method to be called on a write request
                       (if attr is writable)
                       (if attr is of type server.attribute, then use the
                       fset field in the attr object instead)
        :type w_meth: callable
        :param is_allo_meth: the method that is called to check if it
                             is possible to access the attribute or not
                             (if attr is of type server.attribute, then use the
                             fisallowed field in the attr object instead)
        :type is_allo_meth: callable

        :returns: the newly created attribute.
        :rtype: Attr

        :raises DevFailed:

        .. versionadded:: 10.0.0
    """

    return await get_worker().delegate(
        __DeviceImpl__add_attribute_realization,
        self,
        attr,
        r_meth,
        w_meth,
        is_allo_meth,
    )


def __DeviceImpl__add_attribute_realization(self, attr, r_meth, w_meth, is_allo_meth):
    attr_data = None
    type_hint = None

    if isinstance(attr, AttrData):
        attr_data = attr
        attr = attr.to_attr()

    att_name = attr.get_name()

    # get read method and its name
    r_name = f"read_{att_name}"
    if r_meth is None:
        if attr_data is not None:
            r_name = attr_data.read_method_name
        if hasattr(attr_data, "fget"):
            r_meth = attr_data.fget
        elif hasattr(self, r_name):
            r_meth = getattr(self, r_name)
    else:
        r_name = r_meth.__name__

    # patch it if attribute is readable
    if attr.get_writable() in (
        AttrWriteType.READ,
        AttrWriteType.READ_WRITE,
        AttrWriteType.READ_WITH_WRITE,
    ):
        type_hint = dict(r_meth.__annotations__).get("return", None)
        r_name = f"__wrapped_read_{att_name}_{r_name}__"
        r_meth_green_mode = getattr(attr_data, "read_green_mode", True)
        __patch_device_with_dynamic_attribute_read_method(
            self, r_name, r_meth, r_meth_green_mode
        )

    # get write method and its name
    w_name = f"write_{att_name}"
    if w_meth is None:
        if attr_data is not None:
            w_name = attr_data.write_method_name
        if hasattr(attr_data, "fset"):
            w_meth = attr_data.fset
        elif hasattr(self, w_name):
            w_meth = getattr(self, w_name)
    else:
        w_name = w_meth.__name__

    # patch it if attribute is writable
    if attr.get_writable() in (
        AttrWriteType.WRITE,
        AttrWriteType.READ_WRITE,
        AttrWriteType.READ_WITH_WRITE,
    ):
        type_hints = dict(w_meth.__annotations__)
        if type_hint is None and type_hints:
            type_hint = list(type_hints.values())[-1]

        w_name = f"__wrapped_write_{att_name}_{w_name}__"
        w_meth_green_mode = getattr(attr_data, "write_green_mode", True)
        __patch_device_with_dynamic_attribute_write_method(
            self, w_name, w_meth, w_meth_green_mode
        )

    # get is allowed method and its name
    ia_name = f"is_{att_name}_allowed"
    if is_allo_meth is None:
        if attr_data is not None:
            ia_name = attr_data.is_allowed_name
        if hasattr(attr_data, "fisallowed"):
            is_allo_meth = attr_data.fisallowed
        elif hasattr(self, ia_name):
            is_allo_meth = getattr(self, ia_name)
    else:
        ia_name = is_allo_meth.__name__

    # patch it if exists
    if is_allo_meth is not None:
        ia_name = f"__wrapped_is_allowed_{att_name}_{ia_name}__"
        ia_meth_green_mode = getattr(attr_data, "isallowed_green_mode", True)
        __patch_device_with_dynamic_attribute_is_allowed_method(
            self, ia_name, is_allo_meth, ia_meth_green_mode
        )

    if attr_data and type_hint:
        if not attr_data.has_dtype_kword:
            dtype, dformat, max_x, max_y = parse_type_hint(
                type_hint, caller="attribute"
            )
            if dformat is None:
                if attr_data.attr_format not in [
                    AttrDataFormat.IMAGE,
                    AttrDataFormat.SPECTRUM,
                ]:
                    raise RuntimeError(
                        "For numpy.ndarrays AttrDataFormat has to be specified"
                    )
                dformat = attr_data.attr_format

            dtype, dformat, enum_labels = get_attribute_type_format(
                dtype, dformat, None
            )
            attr_data.attr_type = dtype
            attr_data.attr_format = dformat
            if enum_labels:
                attr_data.set_enum_labels_to_attr_prop(enum_labels)
            if not attr_data.has_size_kword:
                if max_x:
                    attr_data.dim_x = max_x
                if max_y:
                    attr_data.dim_y = max_y

            attr = attr_data.to_attr()

    self._add_attribute(attr, r_name, w_name, ia_name)
    return attr


def __patch_device_with_dynamic_attribute_read_method(
    device, name, r_meth, r_meth_green_mode
):
    if __is_device_method(device, r_meth):
        if r_meth_green_mode:

            @functools.wraps(r_meth)
            def read_attr(device, attr):
                worker = get_worker()
                # already bound to device, so exclude device arg
                ret = worker.execute(r_meth, attr)
                if not attr.value_is_set() and ret is not None:
                    set_complex_value(attr, ret)
                return ret

        else:

            @functools.wraps(r_meth)
            def read_attr(device, attr):
                ret = r_meth(attr)
                if not attr.value_is_set() and ret is not None:
                    set_complex_value(attr, ret)
                return ret

    else:
        if r_meth_green_mode:

            @functools.wraps(r_meth)
            def read_attr(device, attr):
                worker = get_worker()
                # unbound function or not on device object, so include device arg
                ret = worker.execute(r_meth, device, attr)
                if not attr.value_is_set() and ret is not None:
                    set_complex_value(attr, ret)
                return ret

        else:

            @functools.wraps(r_meth)
            def read_attr(device, attr):
                ret = r_meth(device, attr)
                if not attr.value_is_set() and ret is not None:
                    set_complex_value(attr, ret)
                return ret

    if _force_tracing:
        read_attr = _forcefully_traced_method(read_attr)

    bound_method = types.MethodType(read_attr, device)
    setattr(device, name, bound_method)


def __patch_device_with_dynamic_attribute_write_method(
    device, name, w_meth, w_meth_green_mode
):
    if __is_device_method(device, w_meth):
        if w_meth_green_mode:

            @functools.wraps(w_meth)
            def write_attr(device, attr):
                worker = get_worker()
                # already bound to device, so exclude device arg
                return worker.execute(w_meth, attr)

        else:

            @functools.wraps(w_meth)
            def write_attr(device, attr):
                return w_meth(attr)

    else:
        if w_meth_green_mode:

            @functools.wraps(w_meth)
            def write_attr(device, attr):
                worker = get_worker()
                # unbound function or not on device object, so include device arg
                return worker.execute(w_meth, device, attr)

        else:
            write_attr = w_meth

    if _force_tracing:
        write_attr = _forcefully_traced_method(write_attr)

    bound_method = types.MethodType(write_attr, device)
    setattr(device, name, bound_method)


def __patch_device_with_dynamic_attribute_is_allowed_method(
    device, name, is_allo_meth, ia_meth_green_mode
):
    if __is_device_method(device, is_allo_meth):
        if ia_meth_green_mode:

            @functools.wraps(is_allo_meth)
            def is_allowed_attr(device, request_type):
                worker = get_worker()
                # already bound to device, so exclude device arg
                return worker.execute(is_allo_meth, request_type)

        else:

            @functools.wraps(is_allo_meth)
            def is_allowed_attr(device, request_type):
                return is_allo_meth(request_type)

    else:
        if ia_meth_green_mode:

            @functools.wraps(is_allo_meth)
            def is_allowed_attr(device, request_type):
                worker = get_worker()
                # unbound function or not on device object, so include device arg
                return worker.execute(is_allo_meth, device, request_type)

        else:
            is_allowed_attr = is_allo_meth

    if _force_tracing:
        is_allowed_attr = _forcefully_traced_method(is_allowed_attr)

    bound_method = types.MethodType(is_allowed_attr, device)
    setattr(device, name, bound_method)


def __is_device_method(device, func):
    """Return True if func is bound to device object (i.e., a method)"""
    return inspect.ismethod(func) and func.__self__ is device


def __DeviceImpl__remove_attribute(self, attr_name, free_it=False, clean_db=True):
    """
    remove_attribute(self, attr_name)

        Remove one attribute from the device attribute list.

        Note: Call of synchronous remove_attribute method from a coroutine function in
        an asyncio server may cause a deadlock.
        Use ``await`` :meth:`async_remove_attribute` instead.
        However, if overriding the synchronous method ``initialize_dynamic_attributes``,
        then the synchronous remove_attribute method must be used, even in asyncio servers.

        :param attr_name: attribute name
        :type attr_name: str

        :param free_it: free Attr object flag. Default False
        :type free_it: bool

        :param clean_db: clean attribute related info in db. Default True
        :type clean_db: bool

        :raises DevFailed:

        .. versionadded:: 9.5.0
            *free_it* parameter.
            *clean_db* parameter.

    """

    self._remove_attribute(attr_name, free_it, clean_db)


async def __DeviceImpl__async_remove_attribute(
    self, attr_name, free_it=False, clean_db=True
):
    """

    async_remove_attribute(self, attr_name, free_it=False, clean_db=True)

        Remove one attribute from the device attribute list.

        :param attr_name: attribute name
        :type attr_name: str

        :param free_it: free Attr object flag. Default False
        :type free_it: bool

        :param clean_db: clean attribute related info in db. Default True
        :type clean_db: bool

        :raises DevFailed:

        .. versionadded:: 10.0.0

    """

    await get_worker().delegate(self._remove_attribute, attr_name, free_it, clean_db)


def __DeviceImpl__add_command(self, cmd, device_level=True):
    """
    add_command(self, cmd, device_level=True) -> cmd

        Add a new command to the device command list.

        :param cmd: the new command to be added to the list
        :param device_level: Set this flag to true if the command must be added
                             for only this device

        :returns: The command to add
        :rtype: Command

        :raises DevFailed:
    """
    config = dict(cmd.__tango_command__[1][2])
    disp_level = DispLevel.OPERATOR

    cmd_name = cmd.__name__

    # default values
    fisallowed = "is_{0}_allowed".format(cmd_name)
    fisallowed_green_mode = True

    if config:
        if "Display level" in config:
            disp_level = config["Display level"]

        if "Is allowed" in config:
            fisallowed = config["Is allowed"]

        fisallowed_green_mode = config["Is allowed green_mode"]

    if is_pure_str(fisallowed):
        fisallowed = getattr(self, fisallowed, None)

    if fisallowed is not None:
        fisallowed_name = (
            f"__wrapped_{getattr(fisallowed, '__name__', f'is_{cmd_name}_allowed')}__"
        )
        __patch_device_with_dynamic_command_is_allowed_method(
            self, fisallowed_name, fisallowed, fisallowed_green_mode
        )
    else:
        fisallowed_name = ""

    setattr(self, cmd_name, cmd)

    self._add_command(
        cmd_name, cmd.__tango_command__[1], fisallowed_name, disp_level, device_level
    )
    return cmd


def __patch_device_with_dynamic_command_method(device, name, method):
    if __is_device_method(device, method):

        @functools.wraps(method)
        def wrapped_command_method(device, *args):
            worker = get_worker()
            # already bound to device, so exclude device arg
            return worker.execute(method, *args)

    else:

        @functools.wraps(method)
        def wrapped_command_method(device, *args):
            worker = get_worker()
            # unbound function or not on device object, so include device arg
            return worker.execute(method, device, *args)

    bound_method = types.MethodType(wrapped_command_method, device)
    setattr(device, name, bound_method)


def __patch_device_with_dynamic_command_is_allowed_method(
    device, name, is_allo_meth, green_mode
):
    if __is_device_method(device, is_allo_meth):
        if green_mode:

            @functools.wraps(is_allo_meth)
            def is_allowed_cmd(device):
                worker = get_worker()
                # already bound to device, so exclude device arg
                return worker.execute(is_allo_meth)

        else:
            is_allowed_cmd = is_allo_meth

    else:
        if green_mode:

            @functools.wraps(is_allo_meth)
            def is_allowed_cmd(device):
                worker = get_worker()
                # unbound function or not on device object, so include device arg
                return worker.execute(is_allo_meth, device)

        else:

            @functools.wraps(is_allo_meth)
            def is_allowed_cmd(device):
                # unbound function or not on device object, so include device arg
                return is_allo_meth(device)

    if _force_tracing:
        is_allowed_cmd = _forcefully_traced_method(is_allowed_cmd)

    bound_method = types.MethodType(is_allowed_cmd, device)
    setattr(device, name, bound_method)


def __DeviceImpl__remove_command(self, cmd_name, free_it=False, clean_db=True):
    """
    remove_command(self, cmd_name, free_it=False, clean_db=True)

        Remove one command from the device command list.

        :param cmd_name: command name to be removed from the list
        :type cmd_name: str
        :param free_it: set to true if the command object must be freed.
        :type free_it: bool
        :param clean_db: Clean command related information (included polling info
                         if the command is polled) from database.

        :raises DevFailed:
    """
    self._remove_command(cmd_name, free_it, clean_db)


def __DeviceImpl__debug_stream(self, msg, *args, source=None):
    """
    debug_stream(self, msg, *args, source=None)

        Sends the given message to the tango debug stream.

        Since PyTango 7.1.3, the same can be achieved with::

            print(msg, file=self.log_debug)

        :param msg: the message to be sent to the debug stream
        :type msg: str

        :param \\*args: Arguments to format a message string.

        :param source: Function that will be inspected for filename and lineno in the log message.
        :type source: Callable

        .. versionadded:: 9.4.2
            added *source* parameter
    """
    filename, line = get_source_location(source)
    if args:
        msg = msg % args
    self.__debug_stream(filename, line, msg)


def __DeviceImpl__info_stream(self, msg, *args, source=None):
    """
    info_stream(self, msg, *args, source=None)

        Sends the given message to the tango info stream.

        Since PyTango 7.1.3, the same can be achieved with::

            print(msg, file=self.log_info)

        :param msg: the message to be sent to the info stream
        :type msg: str

        :param \\*args: Arguments to format a message string.

        :param source: Function that will be inspected for filename and lineno in the log message.
        :type source: Callable

        .. versionadded:: 9.4.2
            added *source* parameter
    """
    filename, line = get_source_location(source)
    if args:
        msg = msg % args
    self.__info_stream(filename, line, msg)


def __DeviceImpl__warn_stream(self, msg, *args, source=None):
    """
    warn_stream(self, msg, *args, source=None)

        Sends the given message to the tango warn stream.

        Since PyTango 7.1.3, the same can be achieved with::

            print(msg, file=self.log_warn)

        :param msg: the message to be sent to the warn stream
        :type msg: str

        :param \\*args: Arguments to format a message string.

        :param source: Function that will be inspected for filename and lineno in the log message.
        :type source: Callable

        .. versionadded:: 9.4.2
            added *source* parameter
    """
    filename, line = get_source_location(source)
    if args:
        msg = msg % args
    self.__warn_stream(filename, line, msg)


def __DeviceImpl__error_stream(self, msg, *args, source=None):
    """
    error_stream(self, msg, *args, source=None)

        Sends the given message to the tango error stream.

        Since PyTango 7.1.3, the same can be achieved with::

            print(msg, file=self.log_error)

        :param msg: the message to be sent to the error stream
        :type msg: str

        :param \\*args: Arguments to format a message string.

        :param source: Function that will be inspected for filename and lineno in the log message.
        :type source: Callable

        .. versionadded:: 9.4.2
            added *source* parameter
    """
    filename, line = get_source_location(source)
    if args:
        msg = msg % args
    self.__error_stream(filename, line, msg)


def __DeviceImpl__fatal_stream(self, msg, *args, source=None):
    """
    fatal_stream(self, msg, *args, source=None)

        Sends the given message to the tango fatal stream.

        Since PyTango 7.1.3, the same can be achieved with::

            print(msg, file=self.log_fatal)

        :param msg: the message to be sent to the fatal stream
        :type msg: str

        :param \\*args: Arguments to format a message string.

        :param source: Function that will be inspected for filename and lineno in the log message.
        :type source: Callable

        .. versionadded:: 9.4.2
            added *source* parameter
    """
    filename, line = get_source_location(source)
    if args:
        msg = msg % args
    self.__fatal_stream(filename, line, msg)


@property
def __DeviceImpl__debug(self):
    if not hasattr(self, "_debug_s"):
        self._debug_s = TangoStream(self.debug_stream)
    return self._debug_s


@property
def __DeviceImpl__info(self):
    if not hasattr(self, "_info_s"):
        self._info_s = TangoStream(self.info_stream)
    return self._info_s


@property
def __DeviceImpl__warn(self):
    if not hasattr(self, "_warn_s"):
        self._warn_s = TangoStream(self.warn_stream)
    return self._warn_s


@property
def __DeviceImpl__error(self):
    if not hasattr(self, "_error_s"):
        self._error_s = TangoStream(self.error_stream)
    return self._error_s


@property
def __DeviceImpl__fatal(self):
    if not hasattr(self, "_fatal_s"):
        self._fatal_s = TangoStream(self.fatal_stream)
    return self._fatal_s


def __DeviceImpl__str(self):
    dev_name = "unknown"
    try:
        util = Util.instance(False)
        if not util.is_svr_starting() and not util.is_svr_shutting_down():
            dev_name = self.get_name()
    except DevFailed:
        pass  # Util singleton hasn't been initialised yet
    return f"{self.__class__.__name__}({dev_name})"


def __event_exception_converter(*args, **kwargs):
    args = list(args)
    exception = None

    if len(args) and isinstance(args[0], Exception):
        exception = args[0]
    elif "except" in kwargs:
        exception = kwargs.pop("except")

    if exception:
        args[0] = _exception_converter(exception)

    return args, kwargs


def __check_removed_dim_parameters(*args, **kwargs):
    if "dim_x" in kwargs or "dim_y" in kwargs:
        raise TypeError("dim_x and dim_y arguments are no longer supported")
    if len(args) < 2:
        return
    elif len(args) > 4:
        raise TypeError(
            "Too many arguments. "
            "Note, that dim_x and dim_y arguments are no longer supported."
        )
    last_arg = args[-1]
    if not isinstance(last_arg, AttrQuality) and isinstance(last_arg, numbers.Number):
        if len(args) == 2:
            msg = "For DevEncoded attribute it must one of str, bytes, bytearray. "
        else:
            msg = "It must be of type AttrQuality. "

        raise TypeError(
            f"Last argument, {last_arg}, has the incorrect type: {type(last_arg)}. "
            f"{msg}"
            "Note, that dim_x and dim_y arguments are no longer supported."
        )


def __DeviceImpl__push_change_event(self, attr_name, *args, **kwargs):
    """
    .. function:: push_change_event(self, attr_name, except)
                  push_change_event(self, attr_name, data)
                  push_change_event(self, attr_name, data, time_stamp, quality)
                  push_change_event(self, attr_name, str_data, data)
                  push_change_event(self, attr_name, str_data, data, time_stamp, quality)
        :noindex:

    Push a change event for the given attribute name.

    :param attr_name: attribute name
    :type attr_name: str
    :param data: the data to be sent as attribute event data. Data must be compatible with the
                 attribute type and format.
                 for SPECTRUM and IMAGE attributes, data can be any type of sequence of elements
                 compatible with the attribute type
    :param str_data: special variation for DevEncoded data type. In this case 'data' must
                     be a str or an object with the buffer interface.
    :type str_data: str
    :param except: Instead of data, you may want to send an exception.
    :type except: DevFailed
    :param time_stamp: the time stamp
    :type time_stamp: double
    :param quality: the attribute quality factor
    :type quality: AttrQuality

    :raises DevFailed: If the attribute data type is not coherent.

     .. versionchanged:: 10.1.0
        Removed optional 'dim_x' and 'dim_y' arguments. The dimensions are automatically
        determined from the data.
    """
    args, kwargs = __event_exception_converter(*args, **kwargs)
    __check_removed_dim_parameters(*args, **kwargs)
    self.__generic_push_event(attr_name, EventType.CHANGE_EVENT, *args, **kwargs)


def __DeviceImpl__push_alarm_event(self, attr_name, *args, **kwargs):
    """
    .. function:: push_alarm_event(self, attr_name, except)
                  push_alarm_event(self, attr_name, data)
                  push_alarm_event(self, attr_name, data, time_stamp, quality)
                  push_alarm_event(self, attr_name, str_data, data)
                  push_alarm_event(self, attr_name, str_data, data, time_stamp, quality)
        :noindex:

    Push an alarm event for the given attribute name.

    :param attr_name: attribute name
    :type attr_name: str
    :param data: the data to be sent as attribute event data. Data must be compatible with the
                 attribute type and format.
                 for SPECTRUM and IMAGE attributes, data can be any type of sequence of elements
                 compatible with the attribute type
    :param str_data: special variation for DevEncoded data type. In this case 'data' must
                     be a str or an object with the buffer interface.
    :type str_data: str
    :param except: Instead of data, you may want to send an exception.
    :type except: DevFailed
    :param time_stamp: the time stamp
    :type time_stamp: double
    :param quality: the attribute quality factor
    :type quality: AttrQuality

    :raises DevFailed: If the attribute data type is not coherent.

     .. versionchanged:: 10.1.0
        Removed optional 'dim_x' and 'dim_y' arguments. The dimensions are automatically
        determined from the data.
    """
    args, kwargs = __event_exception_converter(*args, **kwargs)
    __check_removed_dim_parameters(*args, **kwargs)
    self.__generic_push_event(attr_name, EventType.ALARM_EVENT, *args, **kwargs)


def __DeviceImpl__push_archive_event(self, attr_name, *args, **kwargs):
    """
    .. function:: push_archive_event(self, attr_name, except)
                  push_archive_event(self, attr_name, data)
                  push_archive_event(self, attr_name, data, time_stamp, quality)
                  push_archive_event(self, attr_name, str_data, data)
                  push_archive_event(self, attr_name, str_data, data, time_stamp, quality)
        :noindex:

    Push an archive event for the given attribute name.

    :param attr_name: attribute name
    :type attr_name: str
    :param data: the data to be sent as attribute event data. Data must be compatible with the
                 attribute type and format.
                 for SPECTRUM and IMAGE attributes, data can be any type of sequence of elements
                 compatible with the attribute type
    :param str_data: special variation for DevEncoded data type. In this case 'data' must
                     be a str or an object with the buffer interface.
    :type str_data: str
    :param except: Instead of data, you may want to send an exception.
    :type except: DevFailed
    :param time_stamp: the time stamp
    :type time_stamp: double
    :param quality: the attribute quality factor
    :type quality: AttrQuality

    :raises DevFailed: If the attribute data type is not coherent.

     .. versionchanged:: 10.1.0
        Removed optional 'dim_x' and 'dim_y' arguments. The dimensions are automatically
        determined from the data.
    """
    args, kwargs = __event_exception_converter(*args, **kwargs)
    __check_removed_dim_parameters(*args, **kwargs)
    self.__generic_push_event(attr_name, EventType.ARCHIVE_EVENT, *args, **kwargs)


def __DeviceImpl__push_event(self, attr_name, filt_names, filt_vals, *args, **kwargs):
    """
    .. function:: push_event(self, attr_name, filt_names, filt_vals, except)
                  push_event(self, attr_name, filt_names, filt_vals, data)
                  push_event(self, attr_name, filt_names, filt_vals, str_data, data)
                  push_event(self, attr_name, filt_names, filt_vals, data, time_stamp, quality)
                  push_event(self, attr_name, filt_names, filt_vals, str_data, data, time_stamp, quality)
        :noindex:

    Push a user event for the given attribute name.

    :param attr_name: attribute name
    :type attr_name: str
    :param filt_names: unused (kept for backwards compatibility) - pass an empty list.
    :type filt_names: Sequence[str]
    :param filt_vals: unused (kept for backwards compatibility) - pass an empty list.
    :type filt_vals: Sequence[double]
    :param data: the data to be sent as attribute event data. Data must be compatible with the
                 attribute type and format.
                 for SPECTRUM and IMAGE attributes, data can be any type of sequence of elements
                 compatible with the attribute type
    :param str_data: special variation for DevEncoded data type. In this case 'data' must
                     be a str or an object with the buffer interface.
    :type str_data: str
    :param except: Instead of data, you may want to send an exception.
    :type except: DevFailed
    :param time_stamp: the time stamp
    :type time_stamp: double
    :param quality: the attribute quality factor
    :type quality: AttrQuality

    :raises DevFailed: If the attribute data type is not coherent.

     .. versionchanged:: 10.1.0
        Removed optional 'dim_x' and 'dim_y' arguments. The dimensions are automatically
        determined from the data.
    """
    args, kwargs = __event_exception_converter(*args, **kwargs)
    __check_removed_dim_parameters(*args, **kwargs)
    self.__push_event(attr_name, filt_names, filt_vals, *args, **kwargs)


def __DeviceImpl__set_telemetry_enabled(self, enabled: bool):
    """
    set_telemetry_enabled(self, enabled) -> None

        Enable or disable the device's telemetry interface.

        This is a no-op if telemetry support isn't compiled into cppTango.

        :param enabled: True to enable telemetry tracing
        :type enabled: bool

        .. versionadded:: 10.0.0
    """
    if enabled:
        self._enable_telemetry()
    else:
        self._disable_telemetry()


def __DeviceImpl__set_kernel_tracing_enabled(self, enabled: bool):
    """
    set_kernel_tracing_enabled(self, enabled) -> None

        Enable or disable telemetry tracing of cppTango kernel methods, and
        for high-level PyTango devices, tracing of the PyTango kernel (BaseDevice)
        methods.

        This is a no-op if telemetry support isn't compiled into cppTango.

        :param enabled: True to enable kernel tracing
        :type enabled: bool

        .. versionadded:: 10.0.0
    """
    if enabled:
        self._enable_kernel_traces()
    else:
        self._disable_kernel_traces()


def __DeviceImpl__get_attribute_config(self, attr_names) -> list[AttributeConfig]:
    """
    Returns the list of :obj:`tango.AttributeConfig` for the requested names

    :param attr_names: sequence of str with attribute names, or single attribute name
    :type attr_names: list[str] | str

    :returns: :class:`tango.AttributeConfig` for each requested attribute name
    :rtype: list[:class:`tango.AttributeConfig`]

    """
    if is_pure_str(attr_names):
        attr_names = [attr_names]
    return self._get_attribute_config(attr_names)


def __DeviceImpl__fill_attr_polling_buffer(self, attribute_name, attr_history_stack):
    """
    fill_attr_polling_buffer(self, attribute_name, attr_history_stack) -> None

        Fill attribute polling buffer with your own data. E.g.:

        .. code-block:: python

            def fill_history(self):
                # note is such case quality will ATTR_VALID, and time_stamp will be time.time()
                self.fill_attr_polling_buffer(attribute_name, TimedAttrData(my_new_value))

        or:

        .. code-block:: python

            def fill_history(self):
                data = TimedAttrData(value=my_new_value,
                                     quality=AttrQuality.ATTR_WARNING,
                                     w_value=my_new_w_value,
                                     time_stamp=my_time)

                self.fill_attr_polling_buffer(attribute_name, data)

        or:

        .. code-block:: python

            def fill_history(self):
                data = [TimedAttrData(my_new_value),
                        TimedAttrData(error=RuntimeError("Cannot read value")]

                self.fill_attr_polling_buffer(attribute_name, data)

    :param attribute_name: name of the attribute to fill polling buffer
    :type attribute_name: :obj:`str`

    :param attr_history_stack: data to be inserted.
    :type attr_history_stack: :obj:`tango.TimedAttrData` or list[:obj:`tango.TimedAttrData`]

    :return: None

    :raises: :obj:`tango.DevFailed`

    .. versionadded:: 10.1.0
    """

    util = Util.instance(False)
    util.fill_attr_polling_buffer(self, attribute_name, attr_history_stack)


def __DeviceImpl__fill_cmd_polling_buffer(self, command_name, cmd_history_stack):
    """
    fill_cmd_polling_buffer(self, device, command_name, cmd_history_stack) -> None

        Fill command polling buffer with your own data. E.g.:


        .. code-block:: python

            def fill_history(self):
                # note is such case time_stamp will be set to time.time()
                self.fill_cmd_polling_buffer(command_name, TimedCmdData(my_new_value))

        or:

        .. code-block:: python

            def fill_history(self):
                data = TimedCmdData(value=my_new_value,
                                     time_stamp=my_time)

                self.fill_cmd_polling_buffer(command_name, data)

        or:

        .. code-block:: python

            def fill_history(self):
                data = [TimedCmdData(my_new_value),
                        TimedCmdData(error=RuntimeError("Cannot read value")]

                self.fill_cmd_polling_buffer(command_name, data)


    :param command_name: name of the command to fill polling buffer
    :type command_name: :obj:`str`

    :param cmd_history_stack: data to be inserted
    :type cmd_history_stack: :obj:`tango.TimedCmdData` or list[:obj:`tango.TimedCmdData`]

    :return: None

    :raises: :obj:`tango.DevFailed`

    .. versionadded:: 10.1.0
    """

    util = Util.instance(False)
    util.fill_cmd_polling_buffer(self, command_name, cmd_history_stack)


def __Device_2Impl__get_attribute_config_2(self, attr_names) -> list[AttributeConfig_2]:
    """
    Returns the list of :obj:`tango.AttributeConfig_2` for the requested names

    :param attr_names: sequence of str with attribute names, or single attribute name
    :type attr_names: list[str] | str

    :returns: :class:`tango.AttributeConfig_2` for each requested attribute name
    :rtype: list[:class:`tango.AttributeConfig_2`]
    """
    if is_pure_str(attr_names):
        attr_names = [attr_names]
    return self._get_attribute_config_2(attr_names)


def __Device_3Impl__get_attribute_config_3(self, attr_names) -> list[AttributeConfig_3]:
    """
    Returns the list of :obj:`tango.AttributeConfig_3` for the requested names

    :param attr_names: sequence of str with attribute names, or single attribute name
    :type attr_names: list[str] | str

    :returns: :class:`tango.AttributeConfig_3` for each requested attribute name
    :rtype: list[:class:`tango.AttributeConfig_3`]
    """
    if is_pure_str(attr_names):
        attr_names = [attr_names]
    return self._get_attribute_config_3(attr_names)


def __init_DeviceImpl():
    DeviceImpl._device_class_instance = None
    DeviceImpl.get_device_class = __DeviceImpl__get_device_class
    DeviceImpl.get_device_properties = __DeviceImpl__get_device_properties
    DeviceImpl.add_attribute = __DeviceImpl__add_attribute
    DeviceImpl.remove_attribute = __DeviceImpl__remove_attribute
    DeviceImpl.add_command = __DeviceImpl__add_command
    DeviceImpl.remove_command = __DeviceImpl__remove_command
    DeviceImpl.async_add_attribute = __DeviceImpl__async_add_attribute
    DeviceImpl.async_remove_attribute = __DeviceImpl__async_remove_attribute
    DeviceImpl.__str__ = __DeviceImpl__str
    DeviceImpl.__repr__ = __DeviceImpl__str
    DeviceImpl.debug_stream = __DeviceImpl__debug_stream
    DeviceImpl.info_stream = __DeviceImpl__info_stream
    DeviceImpl.warn_stream = __DeviceImpl__warn_stream
    DeviceImpl.error_stream = __DeviceImpl__error_stream
    DeviceImpl.fatal_stream = __DeviceImpl__fatal_stream
    DeviceImpl.log_debug = __DeviceImpl__debug
    DeviceImpl.log_info = __DeviceImpl__info
    DeviceImpl.log_warn = __DeviceImpl__warn
    DeviceImpl.log_error = __DeviceImpl__error
    DeviceImpl.log_fatal = __DeviceImpl__fatal
    DeviceImpl.push_change_event = __DeviceImpl__push_change_event
    DeviceImpl.push_alarm_event = __DeviceImpl__push_alarm_event
    DeviceImpl.push_archive_event = __DeviceImpl__push_archive_event
    DeviceImpl.push_event = __DeviceImpl__push_event
    DeviceImpl.set_telemetry_enabled = __DeviceImpl__set_telemetry_enabled
    DeviceImpl.set_kernel_tracing_enabled = __DeviceImpl__set_kernel_tracing_enabled
    DeviceImpl.get_attribute_config = __DeviceImpl__get_attribute_config
    DeviceImpl.fill_attr_polling_buffer = __DeviceImpl__fill_attr_polling_buffer
    DeviceImpl.fill_cmd_polling_buffer = __DeviceImpl__fill_cmd_polling_buffer


def __init_Device_2Impl():
    Device_2Impl.get_attribute_config_2 = __Device_2Impl__get_attribute_config_2


def __init_Device_3Impl():
    Device_3Impl.get_attribute_config_3 = __Device_3Impl__get_attribute_config_3


def __Logger__log(self, level, msg, *args):
    """
    log(self, level, msg, *args)

        Sends the given message to the tango the selected stream.

        :param level: Log level
        :type level: Level.LevelLevel
        :param msg: the message to be sent to the stream
        :type msg: str
        :param args: list of optional message arguments
        :type args: Sequence[str]
    """
    filename, line = get_source_location()
    if args:
        msg = msg % args
    self.__log(filename, line, level, msg)


def __Logger__log_unconditionally(self, level, msg, *args):
    """
    log_unconditionally(self, level, msg, *args)

        Sends the given message to the tango the selected stream,
        without checking the level.

        :param level: Log level
        :type level: Level.LevelLevel
        :param msg: the message to be sent to the stream
        :type msg: str
        :param args: list of optional message arguments
        :type args: Sequence[str]
    """
    filename, line = get_source_location()
    if args:
        msg = msg % args
    self.__log_unconditionally(filename, line, level, msg)


def __Logger__debug(self, msg, *args):
    """
    debug(self, msg, *args)

        Sends the given message to the tango debug stream.

        :param msg: the message to be sent to the debug stream
        :type msg: str
        :param args: list of optional message arguments
        :type args: Sequence[str]
    """
    filename, line = get_source_location()
    if args:
        msg = msg % args
    self.__debug(filename, line, msg)


def __Logger__info(self, msg, *args):
    """
    info(self, msg, *args)

        Sends the given message to the tango info stream.

        :param msg: the message to be sent to the info stream
        :type msg: str
        :param args: list of optional message arguments
        :type args: Sequence[str]
    """
    filename, line = get_source_location()
    if args:
        msg = msg % args
    self.__info(filename, line, msg)


def __Logger__warn(self, msg, *args):
    """
    warn(self, msg, *args)

        Sends the given message to the tango warn stream.

        :param msg: the message to be sent to the warn stream
        :type msg: str
        :param args: list of optional message arguments
        :type args: Sequence[str]
    """
    filename, line = get_source_location()
    if args:
        msg = msg % args
    self.__warn(filename, line, msg)


def __Logger__error(self, msg, *args):
    """
    error(self, msg, *args)

        Sends the given message to the tango error stream.

        :param msg: the message to be sent to the error stream
        :type msg: str
        :param args: list of optional message arguments
        :type args: Sequence[str]
    """
    filename, line = get_source_location()
    if args:
        msg = msg % args
    self.__error(filename, line, msg)


def __Logger__fatal(self, msg, *args):
    """
    fatal(self, msg, *args)

        Sends the given message to the tango fatal stream.

        :param msg: the message to be sent to the fatal stream
        :type msg: str
        :param args: list of optional message arguments
        :type args: Sequence[str]
    """
    filename, line = get_source_location()
    if args:
        msg = msg % args
    self.__fatal(filename, line, msg)


def __UserDefaultAttrProp_set_enum_labels(self, enum_labels):
    """
    set_enum_labels(self, enum_labels)

        Set default enumeration labels.

        :param enum_labels: list of enumeration labels
        :type enum_labels: Sequence[str]

        New in PyTango 9.2.0
    """
    elbls = StdStringVector()
    for enu in enum_labels:
        elbls.append(enu)
    return self._set_enum_labels(elbls)


def __Attr__str(self):
    return f"{self.__class__.__name__}({self.get_name()})"


def __init_Attr():
    Attr.__str__ = __Attr__str
    Attr.__repr__ = __Attr__str


def __init_UserDefaultAttrProp():
    UserDefaultAttrProp.set_enum_labels = __UserDefaultAttrProp_set_enum_labels


def __init_Logger():
    Logger.log = __Logger__log
    Logger.log_unconditionally = __Logger__log_unconditionally
    Logger.debug = __Logger__debug
    Logger.info = __Logger__info
    Logger.warning = __Logger__warn
    Logger.error = __Logger__error
    Logger.fatal = __Logger__fatal

    # kept for backward compatibility
    Logger.warn = __Logger__warn


def device_server_init(doc=True):
    __init_DeviceImpl()
    __init_Device_2Impl()
    __init_Device_3Impl()
    __init_Attribute()
    __init_Attr()
    __init_UserDefaultAttrProp()
    __init_Logger()
