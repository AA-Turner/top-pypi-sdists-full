# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.
"""

__all__ = (
    "Util",
    "pyutil_init",
    "TimedAttrData",
    "TimedCmdData",
    "EnsureOmniThread",
    "is_omni_thread",
)

__docformat__ = "restructuredtext"

import os
import sys
import re
import copy

from argparse import ArgumentParser

from tango import AttrQuality
from tango._tango import (
    Util,
    Except,
    DevFailed,
    DbDevInfo,
    EnsureOmniThread,
    is_omni_thread,
    _telemetry,
)

from tango.utils import (
    PyTangoHelpFormatter,
    is_non_str_seq,
    _InterfaceDefinedByIDL,
    _exception_converter,
)
from tango.globals import class_list, cpp_class_list, get_constructed_classes

import collections.abc


class TimedAttrData(_InterfaceDefinedByIDL):
    """This is pure-Python class, which combines both TimedAttrData and AttributeData
    cppTango classes, for use with Util.fill_attr_polling_buffer

    :param value: value to be inserted in polling history. `Default:` :obj:`None`
    :type value: any type compatible with the Tango attribute's dtype

    :param quality: quality of value. `Default:` :obj:`tango.AttrQuality.ATTR_VALID`
    :type quality: :obj:`tango.AttrQuality`

    :param w_value: corresponding written value. Note: should be present only for writable attributes `Default:` :obj:`None`
    :type w_value: any type compatible with the Tango attribute's dtype

    :param error: if the error reading should be inserted. Note: error has a priority over value! `Default:` :obj:`None`
    :type error: :obj:`Exception` or :obj:`tango.DevFailed`

    :param time_stamp: value time stamp in seconds passed since epoch. If not provided, the current system time will be used `Default:` :obj:`None`
    :type time_stamp: :obj:`float`
    """

    def __init__(
        self,
        value=None,
        quality=AttrQuality.ATTR_VALID,
        w_value=None,
        error=None,
        time_stamp=None,
    ):
        self.value = value
        self.quality = quality
        self.w_value = w_value
        self.error = error
        self.time_stamp = time_stamp
        self._initialized = True


class TimedCmdData(_InterfaceDefinedByIDL):
    """This is pure-Python class, which mimics the TimedCmdData
    cppTango class, for use with Util.fill_cmd_polling_buffer

    :param value: value to be inserted in polling history. `Default:` :obj:`None`
    :type value: any type compatible with the Tango commands's dtype

    :param error: if the error reading should be inserted. Note: error has a priority over value! `Default:` :obj:`None`
    :type error: :obj:`Exception` or :obj:`tango.DevFailed`

    :param time_stamp: value time stamp in seconds passed since epoch. If not provided, the current system time will be used `Default:` :obj:`None`
    :type time_stamp: :obj:`float`
    """

    def __init__(
        self,
        value=None,
        error=None,
        time_stamp=None,
    ):
        self.value = value
        self.error = error
        self.time_stamp = time_stamp
        self._initialized = True


def __simplify_device_name(dev_name):
    if dev_name.startswith("tango://"):
        dev_name = dev_name[8:]
    if dev_name.count("/") > 2:
        dev_name = dev_name[dev_name.index("/") + 1 :]
    return dev_name.lower()


#
# Methods on Util
#


def __Util__get_class_list(self):
    """
    get_class_list(self) -> seq<DeviceClass>

            Returns a list of objects of inheriting from DeviceClass

        Parameters : None

        Return     : (seq<DeviceClass>) a list of objects of inheriting from DeviceClass
    """
    return get_constructed_classes()


def __Util__create_device(self, klass_name, device_name, alias=None, cb=None):
    """
    create_device(self, klass_name, device_name, alias=None, cb=None) -> None

        Creates a new device of the given class in the database, creates a new
        DeviceImpl for it and calls init_device (just like it is done for
        existing devices when the DS starts up)

        An optional parameter callback is called AFTER the device is
        registered in the database and BEFORE the init_device for the
        newly created device is called

        Throws tango.DevFailed:
            - the device name exists already or
            - the given class is not registered for this DS.
            - the cb is not a callable

    New in PyTango 7.1.2

    Parameters :
        - klass_name : (str) the device class name
        - device_name : (str) the device name
        - alias : (str) optional alias. Default value is None meaning do not create device alias
        - cb : (callable) a callback that is called AFTER the device is registered
               in the database and BEFORE the init_device for the newly created
               device is called. Typically you may want to put device and/or attribute
               properties in the database here. The callback must receive a parameter
               device_name (str). Default value is None meaning no callback

    Return     : None"""
    if cb is not None and not isinstance(cb, collections.abc.Callable):
        Except.throw_exception(
            "PyAPI_InvalidParameter",
            "The optional cb parameter must be a python callable",
            "Util.create_device",
        )

    db = self.get_database()

    device_name = __simplify_device_name(device_name)

    device_exists = True
    try:
        db.import_device(device_name)
    except DevFailed as df:
        device_exists = not df.args[0].reason == "DB_DeviceNotDefined"

    # 1 - Make sure device name doesn't exist already in the database
    if device_exists:
        Except.throw_exception(
            "PyAPI_DeviceAlreadyDefined",
            f"The device {device_name} is already defined in the database",
            "Util.create_device",
        )

    # 2 - Make sure the device class is known
    klass_list = self.get_class_list()
    klass = None
    for k in klass_list:
        name = k.get_name()
        if name == klass_name:
            klass = k
            break
    if klass is None:
        Except.throw_exception(
            "PyAPI_UnknownDeviceClass",
            f"The device class {klass_name} could not be found",
            "Util.create_device",
        )

    # 3 - Create entry in the database (with alias if necessary)
    dev_info = DbDevInfo()
    dev_info.name = device_name
    dev_info._class = klass_name
    dev_info.server = self.get_ds_name()

    db.add_device(dev_info)

    if alias is not None:
        db.put_device_alias(device_name, alias)

    # from this point on, if anything wrong happens we need to clean the database
    try:
        # 4 - run the callback which tipically is used to initialize
        #     device and/or attribute properties in the database
        if cb is not None:
            cb(device_name)

        # 5 - Initialize device object on this server
        k.device_factory([device_name])
    except Exception:
        try:
            if alias is not None:
                db.delete_device_alias(alias)
        except Exception:
            pass
        db.delete_device(device_name)


def __Util__delete_device(self, klass_name, device_name):
    """
    delete_device(self, klass_name, device_name) -> None

        Deletes an existing device from the database and from this running
        server

        Throws tango.DevFailed:
            - the device name doesn't exist in the database
            - the device name doesn't exist in this DS.

    New in PyTango 7.1.2

    Parameters :
        - klass_name : (str) the device class name
        - device_name : (str) the device name

    Return     : None"""

    db = self.get_database()
    device_name = __simplify_device_name(device_name)
    device_exists = True
    try:
        db.import_device(device_name)
    except DevFailed as df:
        device_exists = not df.args[0].reason == "DB_DeviceNotDefined"

    # 1 - Make sure device name exists in the database
    if not device_exists:
        Except.throw_exception(
            "PyAPI_DeviceNotDefined",
            f"The device {device_name} is not defined in the database",
            "Util.delete_device",
        )

    # 2 - Make sure device name is defined in this server
    class_device_name = f"{klass_name}::{device_name}"
    ds = self.get_dserver_device()
    dev_names = ds.query_device()
    device_exists = False
    for dev_name in dev_names:
        p = dev_name.index("::")
        dev_name = dev_name[:p] + dev_name[p:].lower()
        if dev_name == class_device_name:
            device_exists = True
            break
    if not device_exists:
        Except.throw_exception(
            "PyAPI_DeviceNotDefinedInServer",
            f"The device {class_device_name} is not defined in this server",
            "Util.delete_device",
        )

    db.delete_device(device_name)

    dimpl = self.get_device_by_name(device_name)

    dc = dimpl.get_device_class()
    dc.device_destroyer(device_name)


def __check_arg_for_polling_buffer(history_stack, expected_type, parameter_name):
    # if user gave us just one value - convert it to list
    if not is_non_str_seq(history_stack):
        history_stack = [history_stack]

    for v in history_stack:
        if not isinstance(v, expected_type):
            raise ValueError(
                f"{parameter_name} parameter has type {type(v)}, "
                f"while it must be {expected_type.__name__} object "
                f"or sequence of {expected_type.__name__} objects"
            )
        if isinstance(v.error, Exception):
            v.error = _exception_converter(v.error)
        if isinstance(v.error, DevFailed):
            v.error = v.error.args

    return history_stack


def __Util__fill_attr_polling_buffer(self, device, attribute_name, attr_history_stack):
    """
    fill_attr_polling_buffer(self, device, attribute_name, attr_history_stack) -> None

        Fill attribute polling buffer with your own data. E.g.:

        .. code-block:: python

            def fill_history():
                util = Util.instance(False)
                # note is such case quality will ATTR_VALID, and time_stamp will be time.time()
                util.fill_attr_polling_buffer(device, attribute_name, TimedAttrData(my_new_value))

        or:

        .. code-block:: python

            def fill_history():
                util = Util.instance(False)

                data = TimedAttrData(value=my_new_value,
                                     quality=AttrQuality.ATTR_WARNING,
                                     w_value=my_new_w_value,
                                     time_stamp=my_time)

                util.fill_attr_polling_buffer(device, attribute_name, data)

        or:

        .. code-block:: python

            def fill_history():
                util = Util.instance(False)
                data = [TimedAttrData(my_new_value),
                        TimedAttrData(error=RuntimeError("Cannot read value")]

                util.fill_attr_polling_buffer(device, attribute_name, data)

    :param device: the device to fill attribute polling buffer
    :type device: :obj:`tango.DeviceImpl`

    :param attribute_name: name of the attribute to fill polling buffer
    :type attribute_name: :obj:`str`

    :param attr_history_stack: data to be inserted.
    :type attr_history_stack: :obj:`tango.TimedAttrData` or list[:obj:`tango.TimedAttrData`]

    :return: None

    :raises: :obj:`tango.DevFailed`

    .. versionadded:: 10.1.0
    """

    attr_history_stack = __check_arg_for_polling_buffer(
        attr_history_stack, TimedAttrData, "attr_history_stack"
    )

    self._fill_attr_polling_buffer(device, attribute_name, attr_history_stack)


def __Util__fill_cmd_polling_buffer(self, device, command_name, cmd_history_stack):
    """
    fill_cmd_polling_buffer(self, device, command_name, attr_history_stack) -> None

        Fill attribute polling buffer with your own data. E.g.:


        .. code-block:: python

            def fill_history():
                util = Util.instance(False)
                # note is such time_stamp will be set to time.time()
                util.fill_cmd_polling_buffer(device, command_name, TimedCmdData(my_new_value))

        or:

        .. code-block:: python

            def fill_history():
                util = Util.instance(False)

                data = TimedCmdData(value=my_new_value,
                                     time_stamp=my_time)

                util.fill_cmd_polling_buffer(device, command_name, data)

        or:

        .. code-block:: python

            def fill_history():
                util = Util.instance(False)
                data = [TimedCmdData(my_new_value),
                        TimedCmdData(error=RuntimeError("Cannot read value")]

                util.fill_cmd_polling_buffer(device, command_name, data)


    :param device: the device to fill command polling buffer
    :type device: :obj:`tango.DeviceImpl`

    :param command_name: name of the command to fill polling buffer
    :type command_name: :obj:`str`

    :param cmd_history_stack: data to be inserted
    :type cmd_history_stack: :obj:`tango.TimedCmdData` or list[:obj:`tango.TimedCmdData`]

    :return: None

    :raises: :obj:`tango.DevFailed`

    .. versionadded:: 10.1.0
    """

    cmd_history_stack = __check_arg_for_polling_buffer(
        cmd_history_stack, TimedCmdData, "cmd_history_stack"
    )

    self._fill_cmd_polling_buffer(device, command_name, cmd_history_stack)


def parse_args(args):
    parser = ArgumentParser(
        prog=os.path.splitext(args[0])[0],
        usage="%(prog)s instance_name [-v[trace level]] "
        + "[-host] [-port] [-file=<file_name> | -nodb [-dlist]]",
        add_help=False,
        formatter_class=PyTangoHelpFormatter,
    )

    parser.add_argument("instance_name", nargs="+", help="Device server instance name")
    parser.add_argument(
        "-h", "-?", "--help", action="help", help="show this help message and exit"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="count",
        help="set the trace level. "
        + "Can be used in count way: -vv or --verbose --verbose",
    )
    # this option won't be used, since we manually pop all -vN and -v N arguments, but we have to display help about it
    parser.add_argument(
        "-vLEVEL",
        dest="vn",
        action="store",
        metavar=" ",
        help="directly set the trace level to LEVEL",
    )

    parser.add_argument(
        "-file",
        "--file",
        dest="file",
        metavar="FILE_PATH",
        help="start device server using an ASCII file instead of the Tango database",
    )

    parser.add_argument(
        "-host",
        "--host",
        dest="host",
        default="0.0.0.0",
        action="store",
        help="Force the host from which server accepts requests (alternatively use ORBendPoint option)",
    )
    parser.add_argument(
        "-port",
        "--port",
        dest="port",
        default="",
        action="store",
        help="Force the port on which the device server listens (alternatively use ORBendPoint option)",
    )

    if sys.platform.startswith("win"):
        parser.add_argument(
            "-dbg",
            "--dbg",
            dest="dbg",
            action="store_true",
            default=False,
            help="Enable debug",
        )
        parser.add_argument(
            "-i",
            dest="i",
            action="store_true",
            default=False,
            help="Install the service",
        )
        parser.add_argument(
            "-s",
            dest="s",
            action="store_true",
            default=False,
            help="Install the service and choose the automatic startup mode",
        )
        parser.add_argument(
            "-u",
            dest="u",
            action="store_true",
            default=False,
            help="Uninstall the service",
        )

    group = parser.add_argument_group("Run device server without database")
    group.add_argument(
        "-nodb",
        "--nodb",
        dest="nodb",
        action="store_true",
        help="run server without DB",
    )
    group.add_argument(
        "-dlist",
        "--dlist",
        dest="dlist",
        metavar="DEV1,DEV2,etc",
        help="The device name list. This option is supported only with the -nodb option.",
    )

    group = parser.add_argument_group(
        "ORB options (started with -ORBxxx):"
        + "options directly passed to the underlying ORB. Should be rarely used"
    )

    group.add_argument(
        "-ORBendPoint",
        "--ORBendPoint",
        dest="ORBendPoint",
        action="store",
        metavar="giop:tcp:<host>:<port>",
        help="Specifying the host from which server accept "
        "requests and port on which the device server listens.",
    )

    group.add_argument(
        "-ORB<other_option>",
        "--ORB<other_option>",
        dest="ORB_not_used",
        action="store",
        metavar="other_value",
        help="Any other ORB option, e.g., -ORBtraceLevel 5",
    )

    # workaround to add arbitrary ORB options
    for arg in args:
        match = re.match(r"(-ORB|--ORB)(?P<suffix>\w+)", arg)
        if match:
            suffix = match.group("suffix")
            if suffix != "endPoint":
                arg = arg.lstrip("-")
                group.add_argument("-" + arg, "--" + arg, action="store", dest=arg)

    # since -vvvv and -v4 options are incompatible, we have to pop all -vN options
    verbose = None
    for ind, arg in enumerate(args):
        if re.match(r"-[vV][=]?\d+", arg) is not None:
            verbose = int(re.findall(r"\d+", arg)[0])
            args.remove(arg)
            break
        if len(arg) == 2 and re.match(r"-[vV]", arg) is not None:
            if ind + 1 < len(args) and re.match(r"\d+", args[ind + 1]) is not None:
                verbose = int(args[ind + 1])
                args.pop(ind + 1)
                args.remove(arg)
                break

    parsed_args = parser.parse_args(args[1:])

    if parsed_args.port and parsed_args.ORBendPoint is None:
        parsed_args.ORBendPoint = f"giop:tcp:{parsed_args.host:s}:{parsed_args.port:s}"

    if parsed_args.nodb and parsed_args.ORBendPoint is None:
        raise SystemExit(
            "-nodb option should used with [-host] -port or -ORBendPoint options"
        )

    if parsed_args.dlist is not None and not parsed_args.nodb:
        raise SystemExit("-dlist should be used only with -nodb option")

    args = [os.path.splitext(args[0])[0]]

    args += parsed_args.instance_name

    # -v4 has priority on -vvvv
    if verbose is not None:
        args += [f"-v{verbose}"]
    elif parsed_args.verbose is not None:
        args += [f"-v{parsed_args.verbose}"]

    # we add back only exist options
    for key, value in parsed_args.__dict__.items():
        if type(value) is bool:
            if value:
                args += [f"-{key:s}"]
        elif value is not None:
            if key == "file":
                args += [f"-{key:s}={value:s}"]
            elif key not in [
                "host",
                "port",
                "verbose",
                "instance_name",
                "ORB_not_used",
            ]:
                args += [f"-{key:s}", f"{value:s}"]

    return args


def __Util__init__(self, args):
    args = parse_args(copy.copy(args))
    Util.__init_orig__(self, args)


def __Util__init(args):
    args = parse_args(list(args))
    return Util.__init_orig(args)


def __Util__add_TgClass(self, klass_device_class, klass_device, device_class_name=None):
    """Register a new python tango class. Example::

        util.add_TgClass(MotorClass, Motor)
        util.add_TgClass(MotorClass, Motor, 'Motor') # equivalent to previous line

    .. deprecated:: 7.1.2
        Use :meth:`tango.Util.add_class` instead."""
    if device_class_name is None:
        device_class_name = klass_device.__name__
    class_list.append((klass_device_class, klass_device, device_class_name))


def __Util__add_Cpp_TgClass(self, device_class_name, tango_device_class_name):
    """Register a new C++ tango class.

    If there is a shared library file called MotorClass.so which
    contains a MotorClass class and a _create_MotorClass_class method. Example::

        util.add_Cpp_TgClass('MotorClass', 'Motor')

    .. note:: the parameter 'device_class_name' must match the shared
              library name.

    .. deprecated:: 7.1.2
        Use :meth:`tango.Util.add_class` instead."""
    cpp_class_list.append((device_class_name, tango_device_class_name))


def __Util__add_class(self, *args, **kwargs):
    """
    add_class(self, class<DeviceClass>, class<DeviceImpl>, language="python") -> None

        Register a new tango class ('python' or 'c++').

        If language is 'python' then args must be the same as
        :meth:`tango.Util.add_TgClass`. Otherwise, args should be the ones
        in :meth:`tango.Util.add_Cpp_TgClass`. Example::

            util.add_class(MotorClass, Motor)
            util.add_class('CounterClass', 'Counter', language='c++')

    New in PyTango 7.1.2"""
    language = kwargs.get("language", "python")
    f = self.add_TgClass
    if language != "python":
        f = self.add_Cpp_TgClass
    return f(*args)


def __init_Util():
    Util.__init_orig__ = Util.__init__
    Util.__init__ = __Util__init__
    Util.__init_orig = staticmethod(Util.init)
    Util.init = staticmethod(__Util__init)
    Util.add_TgClass = __Util__add_TgClass
    Util.add_Cpp_TgClass = __Util__add_Cpp_TgClass
    Util.add_class = __Util__add_class
    Util.get_class_list = __Util__get_class_list
    Util.create_device = __Util__create_device
    Util.delete_device = __Util__delete_device
    Util.fill_attr_polling_buffer = __Util__fill_attr_polling_buffer
    Util.fill_cmd_polling_buffer = __Util__fill_cmd_polling_buffer


#
# EnsureOmniThread context handler
#


def __EnsureOmniThread__enter__(self):
    self._acquire()
    return self


def __EnsureOmniThread__exit__(self, exc_type, exc_value, traceback):
    self._release()
    return False


def __init_EnsureOmniThread():
    EnsureOmniThread.__enter__ = __EnsureOmniThread__enter__
    EnsureOmniThread.__exit__ = __EnsureOmniThread__exit__


#
# TraceContextScope context handler
#


def __TraceContextScope__enter__(self):
    self._acquire()
    return self


def __TraceContextScope__exit__(self, exc_type, exc_value, traceback):
    self._release()
    return False


def __init_TraceContextScope():
    _telemetry.TraceContextScope.__enter__ = __TraceContextScope__enter__
    _telemetry.TraceContextScope.__exit__ = __TraceContextScope__exit__


def pyutil_init(doc=True):
    __init_Util()
    __init_EnsureOmniThread()
    __init_TraceContextScope()
