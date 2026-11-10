# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.
"""

__all__ = ("DeviceClass", "device_class_init")

__docformat__ = "restructuredtext"

import collections.abc
import copy
from collections.abc import Callable
from typing import Any

from tango._tango import (
    CmdArgType,
    DevFailed,
    DeviceClass,
    DispLevel,
    Except,
    StdStringVector,
    UserDefaultAttrProp,
)
from tango.attr_data import AttrData
from tango.globals import get_class, get_class_by_class, get_constructed_class_by_class
from tango.pyutil import Util
from tango.utils import is_array, is_non_str_seq, is_pure_str, obj_2_str, seqStr_2_obj


def _seqStr_2_obj_with_context(argin, argout_type, where, prop_name):
    """Wraps seqStr_2_obj with property/owner context for clearer error messages.

    :param where: short description of where the property lives, e.g.
                  ``"device 'sys/dev/1'"`` or ``"class 'MyDeviceClass'"``;
                  ``None`` when no owner is available.
    """
    try:
        return seqStr_2_obj(argin, argout_type)
    except Exception as e:
        context = f" of {where}" if where else ""
        raise ValueError(
            f"Failed to convert property '{prop_name}'{context} (value={argin!r}) to type {argout_type}: {e}"
        ) from e


class PropUtil:
    """Internal helper for managing properties for a device class."""

    scalar_int_types = (
        CmdArgType.DevShort,
        CmdArgType.DevUShort,
        CmdArgType.DevLong,
        CmdArgType.DevULong,
    )

    scalar_long_types = (CmdArgType.DevLong64, CmdArgType.DevULong64)

    scalar_float_types = (
        CmdArgType.DevFloat,
        CmdArgType.DevDouble,
    )

    scalar_numerical_types = scalar_int_types + scalar_long_types + scalar_float_types

    scalar_str_types = (
        CmdArgType.DevString,
        CmdArgType.ConstDevString,
    )

    scalar_types = (
        scalar_numerical_types
        + scalar_str_types
        + (
            CmdArgType.DevBoolean,
            CmdArgType.DevEncoded,
            CmdArgType.DevUChar,
            CmdArgType.DevVoid,
        )
    )

    def __init__(self, dev_class: DeviceClass):
        self._dev_class = dev_class
        self._class_name = dev_class.get_name()
        self._default_class_props = copy.deepcopy(dev_class.class_property_list)
        self._default_dev_props = copy.deepcopy(dev_class.device_property_list)
        self._dev_props_from_class_props_cache = None

    @property
    def db(self):
        if not Util._UseDb:
            return None
        return Util.instance().get_database()

    def _fetch_dev_props_from_db_class_props(self) -> dict[str, list[Any]]:
        is_svr_starting = Util.instance().is_svr_starting()
        if is_svr_starting and self._dev_props_from_class_props_cache is not None:
            return self._dev_props_from_class_props_cache

        dev_props_names = list(self._default_dev_props)
        dev_props = self.db.get_class_property(self._class_name, dev_props_names)
        self._dev_props_from_class_props_cache = dev_props if is_svr_starting else None
        return dev_props

    def register_wizard_default_prop_values(self):
        """
        Register declared property defaults for use by new-device wizards.

        In Jive, this is accessed with Tools > Server Wizard.
        In Astor, this is accessed with "Create New Server".
        """
        class_props = self._default_class_props
        for name in class_props:
            tg_type = self.get_property_type(name, class_props)
            default_value = self.get_property_values(name, class_props)
            wizard_value = obj_2_str(default_value, tg_type)
            desc = self.get_property_description(name, class_props)
            self._dev_class.add_wiz_class_prop(name, desc, wizard_value)

        dev_props = self._default_dev_props
        for name in dev_props:
            tg_type = self.get_property_type(name, dev_props)
            default_value = self.get_property_values(name, dev_props)
            wizard_value = obj_2_str(default_value, tg_type)
            desc = self.get_property_description(name, dev_props)
            self._dev_class.add_wiz_dev_prop(name, desc, wizard_value)

    def fetch_class_props_from_db(self) -> dict[str, list[Any]]:
        """
        Return a copy of the declared class properties with database values.

        If no database is active, the declared property defaults are returned
        unchanged.

        :return: Class property definitions containing the resolved values.
        :rtype: dict[str, list[typing.Any]]
        """
        class_props = copy.deepcopy(self._default_class_props)
        db = self.db
        if not class_props or db is None:
            return class_props

        # call database to get properties
        db_values = db.get_class_property(self._class_name, list(class_props))
        class_where = f"class '{self._class_name}'"

        # if value defined in database, store it
        for name in class_props:
            db_value = db_values[name]
            if db_value:
                tg_type = self.get_property_type(name, class_props)
                converted_value = _seqStr_2_obj_with_context(db_value, tg_type, class_where, name)
                self.set_property_values(name, class_props, converted_value)
            else:
                print(name + " property NOT found in database")
        return class_props

    def fetch_device_props_from_db_with_class_props_fallback(self, device) -> dict[str, list[Any]]:
        """
        Return resolved device properties for a device.

        Values are resolved from the device database properties, same-named
        class database properties, same-named declared class defaults, and
        declared device defaults, in that order. If no database is active,
        values are resolved from the declared defaults.

        The device name is only read when the database is queried, so this
        may be called before ``DeviceImpl.__init__`` if the class declares
        no device properties or no database is active.

        :param device: the device the properties are resolved for
        :type device: :obj:`~tango.DeviceImpl`

        :return: Device property definitions containing the resolved values.
        :rtype: dict[str, list[typing.Any]]
        """
        dev_props = copy.deepcopy(self._default_dev_props)
        if not dev_props:
            return dev_props

        dev_props_names = list(dev_props.keys())
        db = self.db
        if db is None:
            device_db_values = dict.fromkeys(dev_props_names, ())
            class_db_values = dict.fromkeys(dev_props_names, ())
            dev_where = "device"
        else:
            dev_name = device.get_name()
            device_db_values = db.get_device_property(dev_name, dev_props_names)
            class_db_values = self._fetch_dev_props_from_db_class_props()
            dev_where = f"device '{dev_name}'"
        class_where = f"class '{self._class_name}'"

        def _set_dev_prop_from_db(name_, db_value, where):
            if not len(db_value):
                return False

            tg_type = self.get_property_type(name_, dev_props)
            converted_value = _seqStr_2_obj_with_context(db_value, tg_type, where, name_)
            if self.is_empty_seq(converted_value):
                return False

            self.set_property_values(name_, dev_props, converted_value)
            return True

        def _set_dev_prop_from_class_prop_default(name_):
            class_default = self.get_property_values(name_, self._default_class_props)
            if class_default is None or self.is_empty_seq(class_default):
                return

            if not self.is_seq(class_default):
                class_default = [class_default]
            tg_type = self.get_property_type(name_, self._default_class_props)
            converted_value = _seqStr_2_obj_with_context(class_default, tg_type, class_where, name_)
            if self.is_empty_seq(converted_value):
                return

            self.set_property_values(name_, dev_props, converted_value)

        # If value defined in database, store it.  Device properties use
        # same-named class database properties when no device value exists.
        # If no values are in the database, same-named class defaults
        # supersede device defaults, matching POGO-generated C++ servers.
        for name in dev_props:
            if _set_dev_prop_from_db(name, device_db_values[name], dev_where):
                continue
            if _set_dev_prop_from_db(name, class_db_values[name], class_where):
                continue
            _set_dev_prop_from_class_prop_default(name)
            # (if there was no class default, we already have the device default in dev_props)

        return dev_props

    def is_seq(self, v) -> bool:
        """
        Determine whether an object is a sequence.

        :param v: object to be analysed
        :type v: object

        :return: Whether the object is a sequence.
        :rtype: bool
        """
        return isinstance(v, collections.abc.Sequence)

    def is_empty_seq(self, v) -> bool:
        """
        Determine whether an object is an empty sequence.

        :param v: object to be analysed
        :type v: object

        :return: Whether the object is an empty sequence.
        :rtype: bool
        """
        return self.is_seq(v) and not len(v)

    def get_property_type(self, prop_name, properties) -> CmdArgType:
        """
        Return a property's Tango data type.

        If the property definition or its type is unavailable,
        :attr:`~tango.CmdArgType.DevVoid` is returned.

        :param prop_name: the property name
        :type prop_name: :py:obj:`str`

        :param properties: the properties
        :type properties: :py:obj:`dict`\\[:py:obj:`str`, object]

        :return: The property's Tango data type.
        :rtype: :obj:`~tango.CmdArgType`
        """
        try:
            tg_type = properties[prop_name][0]
        except (KeyError, IndexError, TypeError):
            tg_type = CmdArgType.DevVoid
        return tg_type

    def set_property_values(self, prop_name, properties, value):
        """
        Set the value field in a property definition to an independent copy.

        :param prop_name: the property name
        :type prop_name: :py:obj:`str`

        :param properties: [in,out] :py:obj:`dict`\\ which will contain the value
        :type properties: :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`]

        :param value: New scalar or sequence value.
                      Mutable values are copied before being stored.
        :type value: :py:obj:`typing.Any`
        """

        copied_value = value[:] if isinstance(value, StdStringVector) else copy.deepcopy(value)
        properties[prop_name][2] = copied_value

    def get_property_values(self, prop_name, properties) -> Any:
        """
        Return a property value converted to its declared Tango data type.

        Scalar property values are unwrapped from non-string sequences, while
        array and empty sequence values are returned as sequences.

        :param prop_name: the property name
        :type prop_name: :py:obj:`str`

        :param properties: properties
        :type properties: :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`]

        :return: the property value in the given property
        :rtype: :py:obj:`typing.Any`
        """
        tg_type = self.get_property_type(prop_name, properties)

        try:
            value = properties[prop_name][2]
        except (KeyError, IndexError, TypeError):
            value = []

        if is_pure_str(value):
            value = _seqStr_2_obj_with_context(value, tg_type, None, prop_name)

        if is_array(tg_type) or self.is_empty_seq(value):
            return value
        if is_non_str_seq(value):
            return value[0]
        return value

    def get_property_description(self, prop_name, properties):
        """
        Return the description from a property definition.

        :param prop_name: the property name
        :type prop_name: :py:obj:`str`

        :param properties: properties
        :type properties: :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`]

        :return: the description for the given property name
        :rtype: :py:obj:`str`
        """
        return properties[prop_name][1]


def __DeviceClass__init__(self, name):
    DeviceClass.__init_orig__(self, name)
    try:
        self.py_dev_list = []
        pu = self.prop_util = PropUtil(self)
        pu.register_wizard_default_prop_values()
        self.class_property_list = pu.fetch_class_props_from_db()
        for prop_name in self.class_property_list:
            if not hasattr(self, prop_name):
                setattr(
                    self,
                    prop_name,
                    pu.get_property_values(prop_name, self.class_property_list),
                )
    except DevFailed as df:
        print(f"PyDS: {name}: A Tango error occurred in the constructor:")
        Except.print_exception(df)
    except Exception as e:
        print(f"PyDS: {name}: An error occurred in the constructor:")
        print(str(e))


def __DeviceClass__str__(self):
    return f"{self.__class__.__name__}({self.get_name()})"


def __DeviceClass__repr__(self):
    return f"{self.__class__.__name__}({self.get_name()})"


def __throw_create_attribute_exception(msg):
    """
    Helper method to throw DevFailed exception when inside
    create_attribute
    """
    Except.throw_exception("PyDs_WrongAttributeDefinition", msg, "create_attribute()")


def __throw_create_command_exception(msg):
    """
    Helper method to throw DevFailed exception when inside
    create_command
    """
    Except.throw_exception("PyDs_WrongCommandDefinition", msg, "create_command()")


def __DeviceClass__create_user_default_attr_prop(self, attr_name, extra_info):
    """for internal usage only"""
    p = UserDefaultAttrProp()
    for k, v in extra_info.items():
        k_lower = k.lower()
        method_name = f"set_{k_lower.replace(' ', '_')}"
        if hasattr(p, method_name):
            method = getattr(p, method_name)
            method(str(v))
        elif k == "delta_time":
            p.set_delta_t(str(v))
        elif k_lower not in ("display level", "polling period", "memorized"):
            name = self.get_name()
            msg = (
                f"Wrong definition of attribute {attr_name} in "
                f"class {name}\nThe object extra information '{k}' "
                f"is not recognized!"
            )
            self.__throw_create_attribute_exception(msg)
    return p


def __DeviceClass__attribute_factory(self, attr_list_wrapper):
    """
    for internal usage only!!!

    Note: attempts to do anything with attr_list_wrapper here are
    not 100% save and may result either in crash or memory leak !!!
    """

    for attr_name, attr_info in self.attr_list.items():
        attr_data = attr_info if isinstance(attr_info, AttrData) else AttrData(attr_name, self.get_name(), attr_info)
        if attr_data.forward:
            self._create_fwd_attribute(attr_list_wrapper, attr_data.attr_name, attr_data.att_prop)
        else:
            self._create_attribute(
                attr_list_wrapper,
                attr_data.attr_name,
                attr_data.attr_type,
                attr_data.attr_format,
                attr_data.attr_write,
                attr_data.dim_x,
                attr_data.dim_y,
                attr_data.display_level,
                attr_data.polling_period,
                attr_data.memorized,
                attr_data.hw_memorized,
                attr_data.alarm_event_implemented,
                attr_data.alarm_event_detect,
                attr_data.archive_event_implemented,
                attr_data.archive_event_detect,
                attr_data.change_event_implemented,
                attr_data.change_event_detect,
                attr_data.data_ready_event_implemented,
                attr_data.read_method_name,
                attr_data.write_method_name,
                attr_data.is_allowed_name,
                attr_data.att_prop,
            )


def __DeviceClass__command_factory(self):
    """for internal usage only"""
    name = self.get_name()
    class_info = get_class(name)
    deviceimpl_class = class_info[1]

    if not hasattr(deviceimpl_class, "init_device"):
        msg = f"Wrong definition of class {name}\nThe init_device() method does not exist!"
        Except.throw_exception("PyDs_WrongCommandDefinition", msg, "command_factory()")

    for cmd_name, cmd_info in self.cmd_list.items():
        __create_command(self, deviceimpl_class, cmd_name, cmd_info)


def __create_command(self, deviceimpl_class, cmd_name, cmd_info):
    """for internal usage only"""
    name = self.get_name()

    # check for well defined command info

    # check parameter
    if not isinstance(cmd_info, collections.abc.Sequence):
        msg = (
            f"Wrong data type for value for describing command {cmd_name} in "
            f"class {name}\nMust be a sequence with 2 or 3 elements"
        )
        __throw_create_command_exception(msg)

    if len(cmd_info) < 2 or len(cmd_info) > 3:
        msg = (
            f"Wrong number of argument for describing command {cmd_name} in "
            f"class {name}\nMust be a sequence with 2 or 3 elements"
        )
        __throw_create_command_exception(msg)

    param_info, result_info = cmd_info[0], cmd_info[1]

    if not isinstance(param_info, collections.abc.Sequence):
        msg = (
            f"Wrong data type in command argument for command {cmd_name} in "
            f"class {name}\nCommand parameter (first element) must be a sequence"
        )
        __throw_create_command_exception(msg)

    if len(param_info) < 1 or len(param_info) > 2:
        msg = (
            f"Wrong data type in command argument for command {cmd_name} in "
            f"class {name}\nSequence describing command parameters must contain "
            f"1 or 2 elements"
        )
        __throw_create_command_exception(msg)

    param_type = CmdArgType.DevVoid
    try:
        param_type = CmdArgType(param_info[0])
    except Exception:
        msg = (
            f"Wrong data type in command argument for command {cmd_name} in "
            f"class {name}\nCommand parameter type (first element in first "
            f"sequence) must be a tango.CmdArgType"
        )
        __throw_create_command_exception(msg)

    param_desc = ""
    if len(param_info) > 1:
        param_desc = param_info[1]
        if not is_pure_str(param_desc):
            msg = (
                f"Wrong data type in command parameter for command {cmd_name} in "
                f"class {name}\nCommand parameter description (second element "
                f"in first sequence), when given, must be a string"
            )
            __throw_create_command_exception(msg)

    # Check result
    if not isinstance(result_info, collections.abc.Sequence):
        msg = (
            f"Wrong data type in command result for command {cmd_name} in "
            f"class {name}\nCommand result (second element) must be a sequence"
        )
        __throw_create_command_exception(msg)

    if len(result_info) < 1 or len(result_info) > 2:
        msg = (
            f"Wrong data type in command result for command {cmd_name} in "
            f"class {name}\nSequence describing command result must contain "
            f"1 or 2 elements"
        )
        __throw_create_command_exception(msg)

    result_type = CmdArgType.DevVoid
    try:
        result_type = CmdArgType(result_info[0])
    except Exception:
        msg = (
            f"Wrong data type in command result for command {cmd_name} in "
            f"class {name}\nCommand result type (first element in second "
            f"sequence) must be a tango.CmdArgType"
        )
        __throw_create_command_exception(msg)

    result_desc = ""
    if len(result_info) > 1:
        result_desc = result_info[1]
        if not is_pure_str(result_desc):
            msg = (
                f"Wrong data type in command result for command {cmd_name} in "
                f"class {name}\nCommand parameter description (second element "
                f"in second sequence), when given, must be a string"
            )
            __throw_create_command_exception(msg)

    # If it is defined, get addictional dictionnary used for optional parameters
    display_level, default_command, polling_period, is_allowed = (
        DispLevel.OPERATOR,
        False,
        -1,
        None,
    )

    if len(cmd_info) == 3:
        extra_info = cmd_info[2]
        if not isinstance(extra_info, collections.abc.Mapping):
            msg = (
                f"Wrong data type in command information for command {cmd_name} in "
                f"class {name}\nCommand information (third element in sequence), "
                f"when given, must be a dictionary"
            )
            __throw_create_command_exception(msg)

        if len(extra_info) > 4:
            msg = (
                f"Wrong data type in command information for command {cmd_name} in "
                f"class {name}\nThe optional dictionary can not have more than "
                f"four elements"
            )
            __throw_create_command_exception(msg)

        for info_name, info_value in extra_info.items():
            info_name_lower = info_name.lower()
            if info_name_lower == "display level":
                try:
                    display_level = DispLevel(info_value)
                except Exception:
                    msg = (
                        f"Wrong data type in command information for command {cmd_name} in "
                        f"class {name}\nCommand information for display level is not a "
                        f"tango.DispLevel"
                    )
                    __throw_create_command_exception(msg)
            elif info_name_lower == "default command":
                if not is_pure_str(info_value):
                    msg = (
                        f"Wrong data type in command information for command {cmd_name} in "
                        f"class {name}\nCommand information for default command is not a "
                        f"string"
                    )
                    __throw_create_command_exception(msg)
                v = info_value.lower()
                default_command = v == "true"
            elif info_name_lower == "polling period":
                try:
                    polling_period = int(info_value)
                except Exception:
                    msg = (
                        f"Wrong data type in command information for command {cmd_name} in "
                        f"class {name}\nCommand information for polling period is not an "
                        f"integer"
                    )
                    __throw_create_command_exception(msg)
            elif info_name_lower == "is allowed":
                is_allowed = info_value
                if not is_pure_str(is_allowed):
                    msg = (
                        f"Wrong data type in command information for command {cmd_name} in "
                        f"class {name}\nCommand information for is allowed function name"
                        f"is not an string"
                    )
                    __throw_create_command_exception(msg)
            elif info_name_lower == "is allowed green_mode":
                pass
            else:
                msg = (
                    f"Wrong data type in command information for command {cmd_name} in "
                    f"class {name}\nCommand information has unknown key "
                    f"{info_name}"
                )
                __throw_create_command_exception(msg)

    # check that the method to be executed exists
    try:
        cmd = getattr(deviceimpl_class, cmd_name)
        if not isinstance(cmd, collections.abc.Callable):
            msg = (
                f"Wrong definition of command {cmd_name} in "
                f"class {name}\nThe object exists in class but is not "
                f"a method!"
            )
            __throw_create_command_exception(msg)
    except AttributeError:
        msg = f"Wrong definition of command {cmd_name} in class {name}\nThe command method does not exist!"
        __throw_create_command_exception(msg)

    is_allowed_name = f"is_{cmd_name}_allowed" if is_allowed is None else is_allowed

    try:
        is_allowed_function = getattr(deviceimpl_class, is_allowed_name)
        if not isinstance(is_allowed_function, collections.abc.Callable):
            msg = (
                f"Wrong definition of command {cmd_name} in "
                f"class {name}\nThe object '{is_allowed_name}' exists in class but is "
                f"not a method!"
            )
            __throw_create_command_exception(msg)
    except Exception:
        is_allowed_name = ""

    self._create_command(
        cmd_name,
        param_type,
        result_type,
        param_desc,
        result_desc,
        display_level,
        default_command,
        polling_period,
        is_allowed_name,
    )


def __DeviceClass__new_device(self, klass, dev_class, dev_name):
    return klass(dev_class, dev_name)


def __DeviceClass__device_factory(self, device_list):
    """for internal usage only"""

    klass = self.__class__
    klass_name = klass.__name__
    info, klass = get_class_by_class(klass), get_constructed_class_by_class(klass)

    if info is None:
        raise RuntimeError(f"Device class '{klass_name}' is not registered")

    if klass is None:
        raise RuntimeError(f"Device class '{klass_name}' as not been constructed")

    _, deviceImplClass, _deviceImplName = info
    deviceImplClass._device_class_instance = klass

    tmp_dev_list = []
    for dev_name in device_list:
        device = self._new_device(deviceImplClass, klass, dev_name)
        self._add_device(device)
        tmp_dev_list.append(device)

    self.dyn_attr(tmp_dev_list)

    for dev in tmp_dev_list:
        if Util._UseDb and not Util._FileDb:
            self.export_device(dev)
        else:
            self.export_device(dev, dev.get_name())
    self.py_dev_list += tmp_dev_list


def __DeviceClass__create_device(self, device_name: str, alias: str | None = None, cb: Callable | None = None) -> None:
    """
    Creates a new device of the given class in the database, creates a new
    DeviceImpl for it and calls init_device (just like it is done for
    existing devices when the DS starts up)

    An optional parameter callback is called AFTER the device is
    registered in the database and BEFORE the init_device for the
    newly created device is called

    :param device_name: name of the new device
    :type device_name: :py:obj:`str`

    :param alias: optional alias. Default value is None meaning do not create device alias
    :type alias: :py:obj:`str`

    :param cb: a callback that is called AFTER the device is registered
               in the database and BEFORE the init_device for the newly created
               device is called. Typically you may want to put device and/or attribute
               properties in the database here. The callback must receive a parameter:
               device name (str). Default value is None meaning no callback
    :type cb: :py:obj:`typing.Callable`

    :throws: :obj:`~tango.DevFailed`: \n
             - the device name exists already
             - the given class is not registered for this DS
             - the cb is not a callable

    .. versionadded:: 7.1.2
    """
    util = Util.instance()
    util.create_device(self.get_name(), device_name, alias=alias, cb=cb)


def __DeviceClass__delete_device(self, device_name: str) -> None:
    """
    Deletes an existing device from the database and from this running
    server

    :param klass_name: the device class name
    :type klass_name: :py:obj:`str`

    :param device_name: name of the new device
    :type device_name: :py:obj:`str`

    :throws: :obj:`~tango.DevFailed`: \n
             - the device name doesn't exist in the database \n
             - the device name doesn't exist in this DS.

    .. versionadded:: 7.1.2
    """
    util = Util.instance()
    util.delete_device(self.get_name(), device_name)


def __DeviceClass__dyn_attr(self, device_list):
    """
    Default implementation does not do anything
    Overwrite in order to provide dynamic attributes

    :param device_list: sequence of devices of this class
    :type device_list: list[:obj:`~tango.DeviceImpl`]
    """


def __DeviceClass__device_destroyer(self, name):
    """for internal usage only"""
    name = name.lower()
    for d in self.py_dev_list:
        dname = d.get_name().lower()
        if dname == name:
            dev_cl = d.get_device_class()
            # the internal C++ device_destroyer isn't case sensitive so we
            # use the internal DeviceImpl name to make sure the DeviceClass
            # finds it
            dev_cl._device_destroyer(d.get_name())
            self.py_dev_list.remove(d)
            return
    err_mess = "Device " + name + " not in Tango class device list!"
    Except.throw_exception("PyAPI_CantDestroyDevice", err_mess, "DeviceClass.device_destroyer")


def __DeviceClass__device_name_factory(self, dev_name_list: list[str]) -> None:
    """
    Create device(s) name list (for no database device server).
    This method can be re-defined in DeviceClass sub-class for
    device server started without database. Its rule is to
    initialise class device name. The default method does nothing.

    :param dev_name_list: sequence of devices to be filled
    :type dev_name_list: list[:py:obj:`str`]
    """


def device_class_init():
    DeviceClass.class_property_list = {}
    DeviceClass.device_property_list = {}
    DeviceClass.cmd_list = {}
    DeviceClass.attr_list = {}
    DeviceClass.__init_orig__ = DeviceClass.__init__
    DeviceClass.__init__ = __DeviceClass__init__
    DeviceClass.__str__ = __DeviceClass__str__
    DeviceClass.__repr__ = __DeviceClass__repr__
    DeviceClass._create_user_default_attr_prop = __DeviceClass__create_user_default_attr_prop
    DeviceClass._attribute_factory = __DeviceClass__attribute_factory
    DeviceClass._command_factory = __DeviceClass__command_factory
    DeviceClass._new_device = __DeviceClass__new_device

    DeviceClass.device_factory = __DeviceClass__device_factory
    DeviceClass.create_device = __DeviceClass__create_device
    DeviceClass.delete_device = __DeviceClass__delete_device
    DeviceClass.dyn_attr = __DeviceClass__dyn_attr
    DeviceClass.device_destroyer = __DeviceClass__device_destroyer
    DeviceClass.device_name_factory = __DeviceClass__device_name_factory
