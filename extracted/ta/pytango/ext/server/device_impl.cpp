/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "base_types_structures/exception.h"
#include "convertors/object_casters.h"
#include "convertors/type_casters.h"
#include "server/device_impl.h"
#include "server/attr.h"
#include "server/attribute.h"
#include "server/command.h"

// cppTango since 9.4 version provides a way to stream in code location
// information wrapped in a LoggerStream::SourceLocation struct. Below
// template is used as a fallback if this struct is not defined. If it
// is and has non-zero size, the specialization defined later is used.
template <typename Stream, typename = void>
struct LogToStreamImpl {
    static void log(Stream &stream, const std::string & /*file*/, int /*line*/, const std::string &msg) {
        stream << log4tango::_begin_log << msg;
    }
};

template <typename, typename = void>
struct has_source_location : std::false_type { };

template <typename T>
struct has_source_location<T, std::void_t<typename T::SourceLocation>> : std::true_type { };

template <typename Stream>
struct LogToStreamImpl<Stream, std::enable_if_t<has_source_location<Stream>::value>> {
    static void log(Stream &stream, const std::string &file, int line, const std::string &msg) {
        typename Stream::SourceLocation location = {file.c_str(), line};
        stream << log4tango::_begin_log << location << msg;
    }
};

static void log_to_stream(log4tango::LoggerStream &stream, const std::string &file, int line, const std::string &msg) {
    LogToStreamImpl<log4tango::LoggerStream>::log(stream, file, line, msg);
}

#define TAKE_MONITOR_LOCK_AND_GET_ATTRIBUTE(dev, attr_name)                                      \
    std::string __att_name = attr_name.cast<std::string>();                                      \
    std::unique_ptr<py::gil_scoped_release> no_gil = std::make_unique<py::gil_scoped_release>(); \
    Tango::AutoTangoMonitor tango_guard(&dev);                                                   \
    Tango::Attribute &attr = dev.get_device_attr()->get_attr_by_name(__att_name.c_str());        \
    (void) attr;                                                                                 \
    no_gil.reset();

#define CONVERT_FILTERS_TO_CPP(filt_names, filt_vals)                    \
    StdStringVector cpp_filt_names = filt_names.cast<StdStringVector>(); \
    StdDoubleVector cpp_filt_vals = filt_vals.cast<StdDoubleVector>();

#define FIRE_EVENT(attr, eventType)                        \
    switch(eventType) {                                    \
    case Tango::EventType::CHANGE_EVENT:                   \
        attr.fire_change_event(nullptr);                   \
        break;                                             \
    case Tango::EventType::ARCHIVE_EVENT:                  \
        attr.fire_archive_event(nullptr);                  \
        break;                                             \
    case Tango::EventType::ALARM_EVENT:                    \
        attr.fire_alarm_event(nullptr);                    \
        break;                                             \
    default:                                               \
        throw std::invalid_argument("Unknown event type"); \
    }

namespace PyDeviceImpl {

inline py::dict get_version_info_dict(Tango::DeviceImpl &self) {
    py::dict result;
    Tango::DevInfoVersionList list = self.get_version_info();
    for(unsigned int i = 0; i < static_cast<unsigned int>(list.length()); ++i) {
        if(list[i].key != nullptr && list[i].value != nullptr) {
            // Insert into the dictionary
            result[list[i].key] = list[i].value;
        }
    }
    return result;
}

#if defined(TANGO_USE_TELEMETRY)
inline bool is_telemetry_enabled(Tango::DeviceImpl &self) {
    if(self.telemetry()) {
        return self.telemetry()->is_enabled();
    } else {
        return false;
    }
}

inline bool is_kernel_tracing_enabled(Tango::DeviceImpl &self) {
    if(self.telemetry()) {
        return self.telemetry()->are_kernel_traces_enabled();
    } else {
        return false;
    }
}
#endif

/* **********************************
 * firing event for change, alarm, archive events
 * **********************************/

inline void generic_push_event(Tango::DeviceImpl &self,
                               py::str &name,
                               Tango::EventType eventType) {
    py::str name_lower = name.attr("lower")();
    std::string name_cpp = name_lower.cast<std::string>();
    if(name_cpp != "state" && name_cpp != "status") {
        std::string err = "Cannot push event for attribute " + name_cpp + " without data. ";
        err += "Pushing event without data parameter is only allowed for State and Status attributes.";
        Tango::Except::throw_exception("PyDs_InvalidCall",
                                       err,
                                       "PyDeviceImpl::generic_push_event");
    }
    TAKE_MONITOR_LOCK_AND_GET_ATTRIBUTE(self, name_lower) // this creates attr
    attr.reset_value();
    FIRE_EVENT(attr, eventType)
}

inline void generic_push_event(Tango::DeviceImpl &self,
                               py::str &name,
                               Tango::EventType eventType,
                               py::object &data,
                               double *time = nullptr,
                               Tango::AttrQuality *quality = nullptr) {
    TAKE_MONITOR_LOCK_AND_GET_ATTRIBUTE(self, name) // this creates attr
    // Check if 'data' is an instance of Tango::DevFailed
    try {
        Tango::DevFailed except_convert = data.cast<Tango::DevFailed>();
        switch(eventType) {
        case Tango::EventType::CHANGE_EVENT:
            attr.fire_change_event(&except_convert);
            break;
        case Tango::EventType::ARCHIVE_EVENT:
            attr.fire_archive_event(&except_convert);
            break;
        case Tango::EventType::ALARM_EVENT:
            attr.fire_alarm_event(&except_convert);
            break;
        default:
            throw std::invalid_argument("Unknown event type");
        }
        return;
    } catch([[maybe_unused]] const py::cast_error &e) {
        PyAttribute::set_generic_value(attr, data, time, quality);
        FIRE_EVENT(attr, eventType)
    }
}

// Special variation for encoded data type
inline void generic_push_event(Tango::DeviceImpl &self,
                               py::str &name,
                               Tango::EventType eventType,
                               py::object &encoding,
                               py::object &data,
                               double *time = nullptr,
                               Tango::AttrQuality *quality = nullptr) {
    TAKE_MONITOR_LOCK_AND_GET_ATTRIBUTE(self, name) // this creates attr
    PyAttribute::set_encoded_value(attr, encoding, data, time, quality);
    FIRE_EVENT(attr, eventType)
}

/* **********************************
 * firing user event
 * **********************************/

inline void push_event(Tango::DeviceImpl &self,
                       py::str &name,
                       py::object &filt_names,
                       py::object &filt_vals) {
    py::str name_lower = name.attr("lower")();
    std::string name_cpp = name_lower.cast<std::string>();
    if(name_cpp != "state" && name_cpp != "status") {
        std::string err = "Cannot push event for attribute " + name_cpp + " without data. ";
        err += "Pushing event without data parameter is only allowed for State and Status attributes.";
        Tango::Except::throw_exception("PyDs_InvalidCall",
                                       err,
                                       "PyDeviceImpl::push_event");
    }
    CONVERT_FILTERS_TO_CPP(filt_names, filt_vals)         // this creates cpp_filt_names and cpp_filt_vals
    TAKE_MONITOR_LOCK_AND_GET_ATTRIBUTE(self, name_lower) // this creates attr
    attr.reset_value();
    attr.fire_event(cpp_filt_names, cpp_filt_vals);
}

inline void push_event(Tango::DeviceImpl &self,
                       py::str &name,
                       py::object &filt_names,
                       py::object &filt_vals,
                       py::object &data,
                       double *time = nullptr,
                       Tango::AttrQuality *quality = nullptr) {
    CONVERT_FILTERS_TO_CPP(filt_names, filt_vals)   // this creates cpp_filt_names and cpp_filt_vals
    TAKE_MONITOR_LOCK_AND_GET_ATTRIBUTE(self, name) // this creates attr

    // Check if 'data' is an instance of Tango::DevFailed
    try {
        Tango::DevFailed except_convert = data.cast<Tango::DevFailed>();
        attr.fire_event(cpp_filt_names, cpp_filt_vals, &except_convert);
        return;
    } catch([[maybe_unused]] const py::cast_error &e) {
        PyAttribute::set_generic_value(attr, data, time, quality);
        attr.fire_event(cpp_filt_names, cpp_filt_vals);
    }
}

// Special variation for encoded data type
inline void push_event(Tango::DeviceImpl &self,
                       py::str &name,
                       py::object &filt_names,
                       py::object &filt_vals,
                       py::object &encoding,
                       py::object &data,
                       double *time = nullptr,
                       Tango::AttrQuality *quality = nullptr) {
    CONVERT_FILTERS_TO_CPP(filt_names, filt_vals)   // this creates cpp_filt_names and cpp_filt_vals
    TAKE_MONITOR_LOCK_AND_GET_ATTRIBUTE(self, name) // this creates attr
    PyAttribute::set_encoded_value(attr, encoding, data, time, quality);
    attr.fire_event(cpp_filt_names, cpp_filt_vals);
}

/* **********************************
 * data ready event
 * **********************************/
inline void push_data_ready_event(Tango::DeviceImpl &self, const py::str &name, int ctr) {
    TAKE_MONITOR_LOCK_AND_GET_ATTRIBUTE(self, name) // this creates __att_name
    self.push_data_ready_event(__att_name, ctr);
}

void add_attribute(Tango::DeviceImpl &self,
                   const Tango::Attr &c_new_attr,
                   py::object read_meth_name,
                   py::object write_meth_name,
                   py::object is_allowed_meth_name) {
    Tango::Attr &new_attr = const_cast<Tango::Attr &>(c_new_attr);

    std::string attr_name = new_attr.get_name();
    std::string read_name_met;
    std::string write_name_met;
    std::string is_allowed_method;

    if(read_meth_name.ptr() == Py_None) {
        read_name_met = "read_" + attr_name;
    } else {
        read_name_met = read_meth_name.cast<std::string>();
    }

    if(write_meth_name.ptr() == Py_None) {
        write_name_met = "write_" + attr_name;
    } else {
        write_name_met = write_meth_name.cast<std::string>();
    }

    if(is_allowed_meth_name.ptr() == Py_None) {
        is_allowed_method = "is_" + attr_name + "_allowed";
    } else {
        is_allowed_method = is_allowed_meth_name.cast<std::string>();
    }

    Tango::AttrWriteType attr_write = new_attr.get_writable();

    //
    // Create the attribute object according to attribute format
    //

    PyScaAttr *sca_attr_ptr = nullptr;
    PySpecAttr *spec_attr_ptr = nullptr;
    PyImaAttr *ima_attr_ptr = nullptr;
    PyAttr *py_attr_ptr = nullptr;
    Tango::Attr *attr_ptr = nullptr;

    long x, y;
    std::vector<Tango::AttrProperty> &def_prop = new_attr.get_user_default_properties();
    Tango::AttrDataFormat attr_format = new_attr.get_format();
    long attr_type = new_attr.get_type();

    switch(attr_format) {
    case Tango::SCALAR:
        sca_attr_ptr = new PyScaAttr(attr_name, attr_type, attr_write, def_prop);
        py_attr_ptr = sca_attr_ptr;
        attr_ptr = sca_attr_ptr;
        break;

    case Tango::SPECTRUM:
        x = (static_cast<Tango::SpectrumAttr &>(new_attr)).get_max_x();
        spec_attr_ptr = new PySpecAttr(attr_name, attr_type, attr_write, x, def_prop);
        py_attr_ptr = spec_attr_ptr;
        attr_ptr = spec_attr_ptr;
        break;

    case Tango::IMAGE:
        x = (static_cast<Tango::ImageAttr &>(new_attr)).get_max_x();
        y = (static_cast<Tango::ImageAttr &>(new_attr)).get_max_y();
        ima_attr_ptr = new PyImaAttr(attr_name, attr_type, attr_write, x, y, def_prop);
        py_attr_ptr = ima_attr_ptr;
        attr_ptr = ima_attr_ptr;
        break;

    default:
        TangoSys_OMemStream o;
        o << "Attribute " << attr_name << " has an unexpected data format\n"
          << "Please report this bug to the PyTango development team" << std::ends;

        TangoSys_OMemStream origin;
        origin << TANGO_EXCEPTION_ORIGIN << std::ends;

        Tango::Except::throw_exception("PyDs_UnexpectedAttributeFormat", o.str(), origin.str());
        break;
    }

    py_attr_ptr->set_read_name(read_name_met);
    py_attr_ptr->set_write_name(write_name_met);
    py_attr_ptr->set_allowed_name(is_allowed_method);

    if(new_attr.get_memorized()) {
        attr_ptr->set_memorized();
    }
    attr_ptr->set_memorized_init(new_attr.get_memorized_init());

    attr_ptr->set_disp_level(new_attr.get_disp_level());
    attr_ptr->set_polling_period(new_attr.get_polling_period());
    attr_ptr->set_change_event(new_attr.is_change_event(), new_attr.is_check_change_criteria());
    attr_ptr->set_archive_event(new_attr.is_archive_event(), new_attr.is_check_archive_criteria());
    attr_ptr->set_data_ready_event(new_attr.is_data_ready_event());

    //
    // Install attribute in Tango. GIL is released during this operation
    //

    // so we have to release GIL
    py::gil_scoped_release no_gil;

    self.add_attribute(attr_ptr);
}

void add_command(Tango::DeviceImpl &self,
                 py::object cmd_name,
                 py::object cmd_data,
                 py::object is_allowed_name,
                 py::object disp_level,
                 bool device_level = false) {
    std::string name = cmd_name.cast<std::string>();

    std::string in_desc = cmd_data.attr("__getitem__")(0).attr("__getitem__")(1).cast<std::string>();
    std::string out_desc = cmd_data.attr("__getitem__")(1).attr("__getitem__")(1).cast<std::string>();

    std::string is_allowed = is_allowed_name.cast<std::string>();

    Tango::CmdArgType argtype_in = cmd_data.attr("__getitem__")(0).attr("__getitem__")(0).cast<Tango::CmdArgType>();
    Tango::CmdArgType argtype_out = cmd_data.attr("__getitem__")(1).attr("__getitem__")(0).cast<Tango::CmdArgType>();
    Tango::DispLevel display_level = disp_level.cast<Tango::DispLevel>();

    PyCmd *cmd_ptr = new PyCmd(name, argtype_in, argtype_out, in_desc, out_desc, display_level);

    if(!is_allowed.empty()) {
        cmd_ptr->set_allowed(is_allowed);
    }

    //
    // Install the command in Tango.
    //

    py::gil_scoped_release no_gil;

    self.add_command(cmd_ptr, device_level);
}

inline void debug(Tango::DeviceImpl &self, const std::string &file, int line, const std::string &msg) {
    if(self.get_logger()->is_debug_enabled()) {
        log4tango::LoggerStream stream = self.get_logger()->debug_stream();
        log_to_stream(stream, file, line, msg);
    }
}

inline void info(Tango::DeviceImpl &self, const std::string &file, int line, const std::string &msg) {
    if(self.get_logger()->is_info_enabled()) {
        log4tango::LoggerStream stream = self.get_logger()->info_stream();
        log_to_stream(stream, file, line, msg);
    }
}

inline void warn(Tango::DeviceImpl &self, const std::string &file, int line, const std::string &msg) {
    if(self.get_logger()->is_warn_enabled()) {
        log4tango::LoggerStream stream = self.get_logger()->warn_stream();
        log_to_stream(stream, file, line, msg);
    }
}

inline void error(Tango::DeviceImpl &self, const std::string &file, int line, const std::string &msg) {
    if(self.get_logger()->is_error_enabled()) {
        log4tango::LoggerStream stream = self.get_logger()->error_stream();
        log_to_stream(stream, file, line, msg);
    }
}

inline void fatal(Tango::DeviceImpl &self, const std::string &file, int line, const std::string &msg) {
    if(self.get_logger()->is_fatal_enabled()) {
        log4tango::LoggerStream stream = self.get_logger()->fatal_stream();
        log_to_stream(stream, file, line, msg);
    }
}
} // namespace PyDeviceImpl

void no_op_void_handler_method([[maybe_unused]] PyObject *self) { }

bool always_false([[maybe_unused]] PyObject *self) {
    return false;
}

void export_device_impl(py::module &m) {
    py::class_<Tango::DeviceImpl,
               LeakingSmartPtr<Tango::DeviceImpl>,
               DeviceImplTrampoline>(m,
                                     "DeviceImpl",
                                     py::dynamic_attr(),
                                     R"doc(
            Base class for all TANGO device.

            This class inherits from CORBA classes where all the network layer is implemented.)doc")
        .def(py::init<Tango::DeviceClass *, const char *, const char *, Tango::DevState, const char *>(),
             py::arg("klass"),
             py::arg("name"),
             py::arg("description") = "A Tango device",
             py::arg("state") = Tango::UNKNOWN,
             py::arg("status") = Tango::StatusNotSet)
        .def("init_device",
             &Tango::DeviceImpl::init_device,
             R"doc(
                init_device(self)

                    Initialize the device.)doc")
        .def("get_exported_flag",
             &Tango::DeviceImpl::get_exported_flag,
             R"doc(
            get_exported_flag(self) -> bool

                Returns the state of the exported flag

            :returns: the state of the exported flag
            :rtype: bool

            New in PyTango 7.1.2)doc")
        .def("set_state",
             &Tango::DeviceImpl::set_state,
             R"doc(
                set_state(self, new_state)

                Set device state.

                :param new_state: the new device state
                :type new_state: DevState)doc",
             py::arg("new_state"))
        .def("get_state",
             &Tango::DeviceImpl::get_state,
             py::return_value_policy::copy,
             R"doc(
                get_state(self) -> DevState

                    Get a COPY of the device state.

                :returns: Current device state
                :rtype: DevState)doc")
        .def("get_prev_state",
             &Tango::DeviceImpl::get_prev_state,
             py::return_value_policy::copy,
             R"doc(
                get_prev_state(self) -> DevState

                    Get a COPY of the device's previous state.

                :returns: the device's previous state
                :rtype: DevState)doc")
        .def("get_name",
             &Tango::DeviceImpl::get_name,
             py::return_value_policy::copy,
             R"doc(
                get_name(self) -> (str)

                    Get a COPY of the device name.

                :returns: the device name
                :rtype: str)doc")
        .def("get_device_attr",
             &Tango::DeviceImpl::get_device_attr,
             py::return_value_policy::reference,
             R"doc(
                get_device_attr(self) -> MultiAttribute

                    Get device multi attribute object.

                :returns: the device's MultiAttribute object
                :rtype: MultiAttribute)doc")
#if !defined WIN32
        .def("register_signal",
             py::overload_cast<long, bool>(&Tango::DeviceImpl::register_signal),
             R"doc(
                register_signal(self, signo, own_handler)

                    Register this device as device to be informed when signal signo
                    is sent to to the device server process

                :param signo: signal identifier
                :type signo: int

                :param own_handler: true if you want the device signal handler
                                    to be executed in its own handler instead of being
                                    executed by the signal thread. If this parameter
                                    is set to true, care should be taken on how the
                                    handler is written. A default false value is provided
                :type own_handler: bool)doc",
             py::arg("signo"),
             py::arg("own_handler"))
#else
        .def("register_signal",
             py::overload_cast<long>(&Tango::DeviceImpl::register_signal),
             R"doc(
                register_signal(self, signo)

                    Register a signal.

                Register this device as device to be informed when signal signo
                is sent to to the device server process

                :param signo: signal identifier
                :type signo: int)doc",
             py::arg("signo"))
#endif
        .def("unregister_signal",
             &Tango::DeviceImpl::unregister_signal,
             R"doc(
                unregister_signal(self, signo)

                    Unregister this device as device to be informed when signal signo
                    is sent to to the device server process

                :param signo: signal identifier
                :type signo: int)doc",
             py::arg("signo"))
        .def("get_status",
             &Tango::DeviceImpl::get_status,
             py::return_value_policy::copy,
             R"doc(
                get_status(self) -> str

                    Get a COPY of the device status.

                :returns: the device status
                :rtype: str)doc")
        .def("set_status",
             &Tango::DeviceImpl::set_status,
             R"doc(
                set_status(self, new_status)

                    Set device status.

                :param new_status: the new device status
                :type new_status: str)doc",
             py::arg("new_status"))
        .def("append_status",
             &Tango::DeviceImpl::append_status,
             R"doc(
                append_status(self, status, new_line=False)

                    Appends a string to the device status.

                :param status: the string to be appended to the device status
                :type status: str
                :param new_line: If true, appends a new line character before the string. Default is False
                :type new_line: bool)doc",
             py::arg("status"),
             py::arg("new_line") = false)
        .def("dev_state",
             &Tango::DeviceImpl::dev_state,
             R"doc(
                dev_state(self) -> DevState

                    Get device state.

                    Default method to get device state. The behaviour of this method depends
                    on the device state. If the device state is ON or ALARM, it reads the
                    attribute(s) with an alarm level defined, check if the read value is
                    above/below the alarm and eventually change the state to ALARM, return
                    the device state. For all th other device state, this method simply
                    returns the state This method can be redefined in sub-classes in case
                    of the default behaviour does not fullfill the needs.

                :returns: the device state
                :rtype: DevState

                :raises DevFailed: If it is necessary to read attribute(s) and a problem occurs during the reading)doc")
        .def("dev_status",
             &Tango::DeviceImpl::dev_status,
             R"doc(
                dev_status(self) -> str

                    Get device status.

                    Default method to get device status. It returns the contents of the device
                    dev_status field. If the device state is ALARM, alarm messages are added
                    to the device status. This method can be redefined in sub-classes in case
                    of the default behaviour does not fullfill the needs.

                :returns: the device status
                :rtype: str

                :raises DevFailed: If it is necessary to read attribute(s) and a problem occurs during the reading)doc")
        .def("set_attribute_config",
             &Tango::DeviceImpl::set_attribute_config,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                set_attribute_config(self, new_conf) -> None

                    Sets attribute configuration locally and in the Tango database

                :param new_conf: The new attribute(s) configuration. One AttributeConfig structure is needed for each attribute to update
                :type new_conf: list[:class:`tango.AttributeConfig`]

                :returns: None
                :rtype: None

                .. versionadded:: 10.0.0)doc",
             py::arg("new_conf"))
        .def("_get_attribute_config",
             &Tango::DeviceImpl::get_attribute_config,
             py::call_guard<py::gil_scoped_release>())
        .def("set_change_event",
             &Tango::DeviceImpl::set_change_event,
             R"doc(
                set_change_event(self, attr_name, implemented, detect=True)

                    Set an implemented flag for the attribute to indicate that the server fires
                    change events manually, without the polling to be started.

                    If the detect parameter is set to true, the criteria specified for the
                    change event (rel_change and abs_change) are verified and
                    the event is only pushed if a least one of them are fulfilled
                    (change in value compared to previous event exceeds a threshold).
                    If detect is set to false the event is fired without any value checking!

                :param attr_name: attribute name
                :type attr_name: str
                :param implemented: True when the server fires change events manually.
                :type implemented: bool
                :param detect: Triggers the verification of the change event properties
                                when set to true. Default value is true.
                :type detect: bool)doc",
             py::arg("attr_name"),
             py::arg("implemented"),
             py::arg("detect") = true)
        .def("set_alarm_event",
             &Tango::DeviceImpl::set_alarm_event,
             R"doc(
                set_alarm_event(self, attr_name, implemented, detect=True)

                    Set an implemented flag for the attribute to indicate that the server fires
                    alarm events manually, without the polling to be started.

                    If the detect parameter is set to true, the criteria specified for the
                    alarm event (rel_change and abs_change) are verified and
                    the event is only pushed if a least one of them are fulfilled
                    (change in value compared to previous event exceeds a threshold).
                    If detect is set to false the event is fired without any value checking!

                :param attr_name: attribute name
                :type attr_name: str
                :param implemented: True when the server fires alarm events manually.
                :type implemented: bool
                :param detect: Triggers the verification of the alarm event properties
                               when set to true. Default value is true.
                :type detect: bool

                .. versionadded:: 10.0.0)doc",
             py::arg("attr_name"),
             py::arg("implemented"),
             py::arg("detect") = true)
        .def("set_archive_event",
             &Tango::DeviceImpl::set_archive_event,
             R"doc(
                set_alarm_event(self, attr_name, implemented, detect)

                    Set an implemented flag for the attribute to indicate that the server fires
                    archive events manually, without the polling to be started.

                    If the detect parameter is set to true, the criteria specified for the
                    archive event (rel_change and abs_change) are verified and
                    the event is only pushed if a least one of them are fulfilled
                    (change in value compared to previous event exceeds a threshold).
                    If detect is set to false the event is fired without any value checking!

                :param attr_name: attribute name
                :type attr_name: str
                :param implemented: True when the server fires change events manually.
                :type implemented: bool
                :param detect: Triggers the verification of the change event properties
                                when set to true. Default value is true.
                :type detect: bool)doc",
             py::arg("attr_name"),
             py::arg("implemented"),
             py::arg("detect") = true)
        .def("set_data_ready_event",
             &Tango::DeviceImpl::set_data_ready_event,
             R"doc(
                set_alarm_event(self, attr_name, implemented)

                    Set an implemented flag for the attribute to indicate that the server fires
                    data ready events manually.

                :param attr_name: attribute name
                :type attr_name: str
                :param implemented: True when the server fires change events manually.
                :type implemented: bool)doc",
             py::arg("attr_name"),
             py::arg("implemented"))
        .def("_add_attribute",
             &PyDeviceImpl::add_attribute,
             py::arg("attr"),
             py::arg("read_meth_name"),
             py::arg("write_meth_name"),
             py::arg("is_allowed_meth_name"))
        .def("_remove_attribute",
             py::overload_cast<const std::string &, bool, bool>(&Tango::DeviceImpl::remove_attribute),
             py::call_guard<py::gil_scoped_release>(),
             py::arg("rem_attr_name"),
             py::arg("free_it") = false,
             py::arg("clean_db") = true)
        .def("_add_command", &PyDeviceImpl::add_command)
        .def("_remove_command",
             py::overload_cast<const std::string &, bool, bool>(&Tango::DeviceImpl::remove_command),
             py::call_guard<py::gil_scoped_release>(),
             py::arg("rem_attr_name"),
             py::arg("free_it") = false,
             py::arg("clean_db") = true)
        //@TODO .def("get_device_class")
        //@TODO .def("get_db_device")
        .def(
            "is_attribute_polled",
            [](Tango::DeviceImpl &self, const std::string &att_name) {
                return static_cast<DeviceImplTrampoline &>(self).is_attribute_polled_public(att_name);
            },
            py::call_guard<py::gil_scoped_release>(),
            R"doc(
                is_attribute_polled(self, attr_name) -> bool

                    True if the attribute is polled.

                :param attr_name: attribute name
                :type attr_name: str

                :return: True if the attribute is polled
                :rtype: bool)doc",
            py::arg("attr_name"))
        .def(
            "is_command_polled",
            [](Tango::DeviceImpl &self, const std::string &cmd_name) {
                return static_cast<DeviceImplTrampoline &>(self).is_command_polled_public(cmd_name);
            },
            py::call_guard<py::gil_scoped_release>(),
            R"doc(
                is_command_polled(self, cmd_name) -> bool

                    True if the command is polled.

                :param cmd_name: attribute name
                :type cmd_name: str

                :return: True if the command is polled
                :rtype: bool)doc",
            py::arg("cmd_name"))
        .def(
            "get_attribute_poll_period",
            [](Tango::DeviceImpl &self, const std::string &att_name) {
                return static_cast<DeviceImplTrampoline &>(self).get_attribute_poll_period_public(att_name);
            },
            R"doc(
                get_attribute_poll_period(self, attr_name) -> int

                    Returns the attribute polling period (milliseconds) or 0 if the attribute
                    is not polled.

                :param attr_name: attribute name
                :type attr_name: str

                :returns: attribute polling period (ms) or 0 if it is not polled
                :rtype: int

                New in PyTango 8.0.0)doc",
            py::arg("attr_name"))
        .def(
            "get_command_poll_period",
            [](Tango::DeviceImpl &self, const std::string &cmd_name) {
                return static_cast<DeviceImplTrampoline &>(self).get_command_poll_period_public(cmd_name);
            },
            R"doc(
                get_command_poll_period(self, cmd_name) -> int

                    Returns the command polling period (milliseconds) or 0 if the command
                    is not polled.

                :param cmd_name: command name
                :type cmd_name: str

                :returns: command polling period (ms) or 0 if it is not polled
                :rtype: int

                New in PyTango 8.0.0)doc",
            py::arg("cmd_name"))
        .def(
            "poll_attribute",
            [](Tango::DeviceImpl &self, const std::string &att_name, int period) {
                static_cast<DeviceImplTrampoline &>(self).poll_attribute_public(att_name, period);
            },
            py::call_guard<py::gil_scoped_release>(),
            R"doc(
                poll_attribute(self, attr_name, period_ms) -> None

                    Add an attribute to the list of polled attributes.

                :param attr_name: attribute name
                :type attr_name: str

                :param period_ms: polling period in milliseconds
                :type period_ms: int

                :return: None
                :rtype: None)doc",
            py::arg("attr_name"),
            py::arg("period_ms"))
        .def(
            "poll_command",
            [](Tango::DeviceImpl &self, const std::string &cmd_name, int period) {
                static_cast<DeviceImplTrampoline &>(self).poll_command_public(cmd_name, period);
            },
            py::call_guard<py::gil_scoped_release>(),
            R"doc(
                poll_command(self, cmd_name, period_ms) -> None

                    Add a command to the list of polled commands.

                :param cmd_name: command name
                :type cmd_name: str

                :param period_ms: polling period in milliseconds
                :type period_ms: int

                :return: None
                :rtype: None)doc",
            py::arg("cmd_name"),
            py::arg("period_ms"))
        .def(
            "stop_poll_attribute",
            [](Tango::DeviceImpl &self, const std::string &att_name) {
                static_cast<DeviceImplTrampoline &>(self).stop_poll_attribute_public(att_name);
            },
            py::call_guard<py::gil_scoped_release>(),
            R"doc(
                stop_poll_attribute(self, attr_name) -> None

                    Remove an attribute from the list of polled attributes.

                :param attr_name: attribute name
                :type attr_name: str

                :return: None
                :rtype: None)doc",
            py::arg("attr_name"))
        .def(
            "stop_poll_command",
            [](Tango::DeviceImpl &self, const std::string &cmd_name) {
                static_cast<DeviceImplTrampoline &>(self).stop_poll_command_public(cmd_name);
            },
            py::call_guard<py::gil_scoped_release>(),
            R"doc(
                stop_poll_command(self, cmd_name) -> None

                    Remove a command from the list of polled commands.

                :param cmd_name: cmd_name name
                :type cmd_name: str

                :return: None
                :rtype: None)doc",
            py::arg("cmd_name"))

        .def("get_poll_ring_depth",
             &Tango::DeviceImpl::get_poll_ring_depth,
             R"doc(
                get_poll_ring_depth(self) -> int

                    Returns the poll ring depth

                :returns: the poll ring depth
                :rtype: int

                New in PyTango 7.1.2)doc")
        .def("get_poll_old_factor",
             &Tango::DeviceImpl::get_poll_old_factor,
             R"doc(
                get_poll_old_factor(self) -> int

                    Returns the poll old factor

                :returns: the poll old factor
                :rtype: int

                New in PyTango 7.1.2)doc")
        .def("is_polled",
             py::overload_cast<>(&Tango::DeviceImpl::is_polled),
             R"doc(
                is_polled(self) -> bool

                    Returns if it is polled

                :returns: True if it is polled or False otherwise
                :rtype: bool

                New in PyTango 7.1.2)doc")
        .def("get_polled_cmd",
             &Tango::DeviceImpl::get_polled_cmd,
             py::return_value_policy::copy,
             R"doc(
                get_polled_cmd(self) -> Sequence[str]

                    Returns a COPY of the list of polled commands

                :returns: a COPY of the list of polled commands
                :rtype: Sequence[str]

                New in PyTango 7.1.2)doc")
        .def("get_polled_attr",
             &Tango::DeviceImpl::get_polled_attr,
             py::return_value_policy::copy,
             R"doc(
                get_polled_attr(self) -> Sequence[str]

                    Returns a COPY of the list of polled attributes

                :returns: a COPY of the list of polled attributes
                :rtype: Sequence[str]

                New in PyTango 7.1.2)doc")
        .def("get_non_auto_polled_cmd",
             &Tango::DeviceImpl::get_non_auto_polled_cmd,
             py::return_value_policy::copy,
             R"doc(
                get_non_auto_polled_cmd(self) -> Sequence[str]

                    Returns a COPY of the list of non automatic polled commands

                :returns: a COPY of the list of non automatic polled commands
                :rtype: Sequence[str]

                New in PyTango 7.1.2)doc")
        .def("get_non_auto_polled_attr",
             &Tango::DeviceImpl::get_non_auto_polled_attr,
             py::return_value_policy::copy,
             R"doc(
                get_non_auto_polled_attr(self) -> Sequence[str]

                    Returns a COPY of the list of non automatic polled attributes

                :returns: a COPY of the list of non automatic polled attributes
                :rtype: Sequence[str]

                New in PyTango 7.1.2)doc")
        //@TODO .def("get_poll_obj_list", &PyDeviceImpl::get_poll_obj_list)
        .def("stop_polling",
             py::overload_cast<>(&Tango::DeviceImpl::stop_polling),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                stop_polling(self)

                    Stop all polling for a device. if the device is polled, call this
                    method before deleting it.

                New in PyTango 7.1.2)doc")
        .def("stop_polling",
             py::overload_cast<bool>(&Tango::DeviceImpl::stop_polling),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                stop_polling(self, with_db_upd)(self)

                    Stop all polling for a device. if the device is polled, call this
                    method before deleting it.

                :param with_db_upd: Is it necessary to update db?
                :type with_db_upd: bool

                New in PyTango 7.1.2)doc",
             py::arg("with_db_upd"))
        .def("check_command_exists",
             &Tango::DeviceImpl::check_command_exists,
             R"doc(
                check_command_exists(self, cmd_name)

                    Check that a command is supported by the device and
                    does not need input value.

                    The method throws an exception if the
                    command is not defined or needs an input value.

                :param cmd_name: the command name
                :type cmd_name: str

                :raises DevFailed:
                :raises API_IncompatibleCmdArgumentType:
                :raises API_CommandNotFound:)doc",
             py::arg("cmd_name"))
        //@TODO .def("get_command", &PyDeviceImpl::get_command)
        .def("get_dev_idl_version",
             &Tango::DeviceImpl::get_dev_idl_version,
             R"doc(
                get_dev_idl_version(self) -> int

                    Returns the IDL version.

                :returns: the IDL version
                :rtype: int

                New in PyTango 7.1.2)doc")
        .def("get_cmd_poll_ring_depth",
             &Tango::DeviceImpl::get_cmd_poll_ring_depth,
             R"doc(
                get_cmd_poll_ring_depth(self, cmd_name) -> int

                    Returns the command poll ring depth.

                :param cmd_name: the command name
                :type cmd_name: str

                :returns: the command poll ring depth
                :rtype: int

                New in PyTango 7.1.2)doc",
             py::arg("cmd_name"))
        .def("get_attr_poll_ring_depth",
             &Tango::DeviceImpl::get_attr_poll_ring_depth,
             R"doc(
                get_attr_poll_ring_depth(self, attr_name) -> int

                    Returns the attribute poll ring depth.

                :param attr_name: the attribute name
                :type attr_name: str

                :returns: the attribute poll ring depth
                :rtype: int

                New in PyTango 7.1.2)doc",
             py::arg("attr_name"))
        .def("is_device_locked",
             &Tango::DeviceImpl::is_device_locked,
             R"doc(
                is_device_locked(self) -> bool

                    Returns if this device is locked by a client.

                :returns: True if it is locked or False otherwise
                :rtype: bool

                New in PyTango 7.1.2)doc")
        .def("add_version_info",
             &Tango::DeviceImpl::add_version_info,
             R"doc(
                add_version_info(self, key, value) -> dict

                    Method to add information about the module version a device is using

                :param key: Module name
                :type key: str

                :param value: Module version, or other relevant information.
                :type value: str

                .. versionadded:: 10.0.0)doc",
             py::arg("key"),
             py::arg("value"))
        .def("get_version_info",
             &PyDeviceImpl::get_version_info_dict,
             R"doc(
                get_version_info(self) -> dict

                    Returns a dict with versioning of different modules related to the
                    pytango device.

                    Example:
                        {
                            "Build.PyTango.NumPy": "1.26.4",
                            "Build.PyTango.Pybind11": "3.0.1",
                            "Build.PyTango.Python": "3.12.2",
                            "Build.PyTango.cppTango":"10.0.0",
                            "NumPy": "1.26.4",
                            "PyTango": "10.0.0.dev0",
                            "Python": "3.12.2",
                            "cppTango": "10.0.0",
                            "omniORB": "4.3.2",
                            "zmq": "4.3.5"
                        }


                :returns: modules version dict
                :rtype: dict

                .. versionadded:: 10.0.0)doc")

        .def("get_logger",
             &Tango::DeviceImpl::get_logger,
             py::return_value_policy::reference_internal,
             R"doc(
            get_logger(self) -> Logger

                Returns the Logger object for this device

            :returns: the Logger object for this device
            :rtype: Logger)doc")
        .def("__debug_stream",
             &PyDeviceImpl::debug,
             py::arg("file"),
             py::arg("lineno"),
             py::arg("msg"))
        .def("__info_stream",
             &PyDeviceImpl::info,
             py::arg("file"),
             py::arg("lineno"),
             py::arg("msg"))
        .def("__warn_stream",
             &PyDeviceImpl::warn,
             py::arg("file"),
             py::arg("lineno"),
             py::arg("msg"))
        .def("__error_stream",
             &PyDeviceImpl::error,
             py::arg("file"),
             py::arg("lineno"),
             py::arg("msg"))
        .def("__fatal_stream",
             &PyDeviceImpl::fatal,
             py::arg("file"),
             py::arg("lineno"),
             py::arg("msg"))
        .def("init_logger",
             &Tango::DeviceImpl::init_logger,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                init_logger(self) -> None

                    Setups logger for the device.  Called automatically when device starts.)doc")
        .def("start_logging",
             &Tango::DeviceImpl::start_logging,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                start_logging(self) -> None

                    Starts logging)doc")
        .def("stop_logging",
             &Tango::DeviceImpl::stop_logging,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                stop_logging(self) -> None

                    Stops logging)doc")

#if defined(TANGO_USE_TELEMETRY)
        .def("is_telemetry_enabled",
             &PyDeviceImpl::is_telemetry_enabled,
             R"doc(
                is_telemetry_enabled(self) -> bool

                    Indicates if telemetry tracing is enabled for the device.

                    Always False if telemetry support isn't compiled into cppTango.

                :returns: if device telemetry tracing is enabled
                :rtype: bool

                .. versionadded:: 10.0.0)doc")
        .def("_enable_telemetry", &Tango::DeviceImpl::enable_telemetry)
        .def("_disable_telemetry", &Tango::DeviceImpl::disable_telemetry)
        .def("_enable_kernel_traces", &Tango::DeviceImpl::enable_kernel_traces)
        .def("_disable_kernel_traces", &Tango::DeviceImpl::disable_kernel_traces)
        .def("is_kernel_tracing_enabled",
             &PyDeviceImpl::is_kernel_tracing_enabled,
             R"doc(
                is_kernel_tracing_enabled(self) -> bool

                    Indicates if telemetry tracing of the cppTango kernel API is enabled.

                    Always False if telemetry support isn't compiled into cppTango.

                :returns: if kernel tracing is enabled
                :rtype: bool

                .. versionadded:: 10.0.0)doc")
#else
        // If support for telemetry is not compiled in, we use no-op handlers, so the Python
        // code can still run without errors, but does nothing.
        .def("is_telemetry_enabled",
             &always_false,
             R"doc(
                is_telemetry_enabled(self) -> bool

                    Indicates if telemetry tracing is enabled for the device.

                    Always False if telemetry support isn't compiled into cppTango.

                :returns: if device telemetry tracing is enabled
                :rtype: bool

                .. versionadded:: 10.0.0)doc")
        .def("_enable_telemetry", &no_op_void_handler_method)
        .def("_disable_telemetry", &no_op_void_handler_method)
        .def("is_kernel_tracing_enabled",
             &always_false,
             R"doc(
                is_kernel_tracing_enabled(self) -> bool

                    Indicates if telemetry tracing of the cppTango kernel API is enabled.

                    Always False if telemetry support isn't compiled into cppTango.

                :returns: if kernel tracing is enabled
                :rtype: bool

                .. versionadded:: 10.0.0)doc")
        .def("_enable_kernel_traces", &no_op_void_handler_method)
        .def("_disable_kernel_traces", &no_op_void_handler_method)
#endif

        //.def("set_exported_flag", &Tango::DeviceImpl::set_exported_flag)
        //.def("set_poll_ring_depth", &Tango::DeviceImpl::set_poll_ring_depth)

        /* **********************************
         * firing generic event
         * **********************************/

        .def(
            "__generic_push_event",
            [](Tango::DeviceImpl &self, py::str &attr_name, Tango::EventType event_type) {
                PyDeviceImpl::generic_push_event(self, attr_name, event_type);
            },
            py::arg("attr_name"),
            py::arg("event_type"))

        .def(
            "__generic_push_event",
            [](Tango::DeviceImpl &self, py::str &attr_name, Tango::EventType event_type, py::object &data) {
                PyDeviceImpl::generic_push_event(self, attr_name, event_type, data);
            },
            py::arg("attr_name"),
            py::arg("event_type"),
            py::arg("data"))

        .def(
            "__generic_push_event",
            [](Tango::DeviceImpl &self, py::str &attr_name, Tango::EventType event_type, py::object &data, double time, Tango::AttrQuality quality) {
                PyDeviceImpl::generic_push_event(self, attr_name, event_type, data, &time, &quality);
            },
            py::arg("attr_name"),
            py::arg("event_type"),
            py::arg("data"),
            py::arg("time"),
            py::arg("quality"))

        .def(
            "__generic_push_event",
            [](Tango::DeviceImpl &self, py::str &attr_name, Tango::EventType event_type, py::object &encoding, py::object &data) {
                PyDeviceImpl::generic_push_event(self, attr_name, event_type, encoding, data);
            },
            py::arg("attr_name"),
            py::arg("event_type"),
            py::arg("encoding"),
            py::arg("data"))

        .def(
            "__generic_push_event",
            [](Tango::DeviceImpl &self, py::str &attr_name, Tango::EventType event_type, py::object &encoding, py::object &data, double time, Tango::AttrQuality quality) {
                PyDeviceImpl::generic_push_event(self, attr_name, event_type, encoding, data, &time, &quality);
            },
            py::arg("attr_name"),
            py::arg("event_type"),
            py::arg("encoding"),
            py::arg("data"),
            py::arg("time"),
            py::arg("quality"))

        /* **********************************
         * firing user event
         * **********************************/

        .def(
            "__push_event",
            [](Tango::DeviceImpl &self, py::str &attr_name, py::object &filt_names, py::object &filt_vals) {
                PyDeviceImpl::push_event(self, attr_name, filt_names, filt_vals);
            },
            py::arg("attr_name"),
            py::arg("filt_names"),
            py::arg("filt_vals"))

        .def(
            "__push_event",
            [](Tango::DeviceImpl &self, py::str &attr_name, py::object &filt_names, py::object &filt_vals, py::object &data) {
                PyDeviceImpl::push_event(self, attr_name, filt_names, filt_vals, data);
            },
            py::arg("attr_name"),
            py::arg("filt_names"),
            py::arg("filt_vals"),
            py::arg("data"))

        .def(
            "__push_event",
            [](Tango::DeviceImpl &self, py::str &attr_name, py::object &filt_names, py::object &filt_vals, py::object &encoding, py::object &data) {
                PyDeviceImpl::push_event(self, attr_name, filt_names, filt_vals, encoding, data);
            },
            py::arg("attr_name"),
            py::arg("filt_names"),
            py::arg("filt_vals"),
            py::arg("encoding"),
            py::arg("data"))

        .def(
            "__push_event",
            [](Tango::DeviceImpl &self, py::str &attr_name, py::object &filt_names, py::object &filt_vals, py::object &data, double time, Tango::AttrQuality quality) {
                PyDeviceImpl::push_event(self, attr_name, filt_names, filt_vals, data, &time, &quality);
            },
            py::arg("attr_name"),
            py::arg("filt_names"),
            py::arg("filt_vals"),
            py::arg("data"),
            py::arg("time"),
            py::arg("quality"))

        .def(
            "__push_event",
            [](Tango::DeviceImpl &self, py::str &attr_name, py::object &filt_names, py::object &filt_vals, py::object &encoding, py::object &data, double time, Tango::AttrQuality quality) {
                PyDeviceImpl::push_event(self, attr_name, filt_names, filt_vals, encoding, data, &time, &quality);
            },
            py::arg("attr_name"),
            py::arg("filt_names"),
            py::arg("filt_vals"),
            py::arg("encoding"),
            py::arg("data"),
            py::arg("time"),
            py::arg("quality"))

        /* **********************************
         * firing data ready event
         * **********************************/
        .def("push_data_ready_event",
             &PyDeviceImpl::push_data_ready_event,
             R"doc(
                push_data_ready_event(self, attr_name, counter)

                    Push a data ready event for the given attribute name.

                    The method needs the attribute name and a
                    "counter" which will be passed within the event

                :param attr_name: attribute name
                :type attr_name: str
                :param counter: the user counter
                :type counter: int

                :raises DevFailed: If the attribute name is unknown.)doc",
             py::arg("attr_name"),
             py::arg("counter"))

        .def("push_att_conf_event",
             &Tango::DeviceImpl::push_att_conf_event,
             R"doc(
                push_att_conf_event(self, attr)

                    Push an attribute configuration event.

                :param attr: the attribute for which the configuration event
                             will be sent.
                :type attr: Attribute

                New in PyTango 7.2.1)doc",
             py::arg("attr"))

        .def("get_min_poll_period",
             &Tango::DeviceImpl::get_min_poll_period,
             R"doc(
                get_min_poll_period(self) -> int

                    Returns the min poll period in milliseconds.

                :returns: the min poll period in ms
                :rtype: int

                New in PyTango 7.2.0)doc")
        .def("get_cmd_min_poll_period",
             &Tango::DeviceImpl::get_cmd_min_poll_period,
             py::return_value_policy::reference_internal,
             R"doc(
                get_cmd_min_poll_period(self) -> Sequence[str]

                    Returns the min command poll period in milliseconds.

                :returns: the min command poll period in ms
                :rtype: Sequence[str]

                New in PyTango 7.2.0)doc")
        .def("get_attr_min_poll_period",
             &Tango::DeviceImpl::get_attr_min_poll_period,
             py::return_value_policy::reference_internal,
             R"doc(
                get_attr_min_poll_period(self) -> Sequence[str]

                    Returns the min attribute poll period in milliseconds

                :returns: the min attribute poll period in ms
                :rtype: Sequence[str]

                New in PyTango 7.2.0)doc")
        .def("is_there_subscriber",
             &Tango::DeviceImpl::is_there_subscriber,
             R"doc(
                is_there_subscriber(self, attr_name, event_type) -> bool

                    Check if there is subscriber(s) listening for the event.

                    This method returns a boolean set to true if there are some
                    subscriber(s) listening on the event specified by the two method
                    arguments. Be aware that there is some delay (up to 600 sec)
                    between this method returning false and the last subscriber
                    unsubscription or crash...

                    The device interface change event is not supported by this method.

                :param attr_name: the attribute name
                :type attr_name: str
                :param event_type: the event type
                :type event_type: EventType

                :returns: True if there is at least one listener or False otherwise
                :rtype: bool)doc",
             py::arg("attr_name"),
             py::arg("event_type"))
        .def("get_client_ident",
             &Tango::DeviceImpl::get_client_ident,
             R"doc(
                get_client_ident(self) -> ClientAddr | None

                    Get client identification.

                    This method is only useful while handling a command or
                    attribute read/write. I.e., when a method has been invoked
                    by a client. It will return `None` if the method was not
                    invoked in the context of a client call.  E.g., called on startup,
                    or called internally (e.g., from the polling loop).

                    It can only be used with :obj:`tango.GreenMode.Synchronous` device
                    servers. Other device servers will not have the correct context active
                    at the time the attribute/command handler is running.  E.g., for an
                    asyncio device server, the handler is running in the asyncio event loop
                    thread.

                :returns: client identification structure
                :rtype: ClientAddr | None)doc");

    py::class_<Tango::Device_2Impl,
               LeakingSmartPtr<Tango::Device_2Impl>,
               Device_2ImplTrampoline,
               Tango::DeviceImpl>(m, "Device_2Impl", py::dynamic_attr())
        .def(py::init<Tango::DeviceClass *, const char *, const char *, Tango::DevState, const char *>(),
             py::arg("klass"),
             py::arg("name"),
             py::arg("description") = "A Tango device",
             py::arg("state") = Tango::UNKNOWN,
             py::arg("status") = Tango::StatusNotSet)
        .def("_get_attribute_config_2", &Tango::Device_2Impl::get_attribute_config_2);

    py::class_<Tango::Device_3Impl,
               LeakingSmartPtr<Tango::Device_3Impl>,
               Device_XImplTrampoline<Tango::Device_3Impl>,
               Tango::Device_2Impl>(m, "Device_3Impl", py::dynamic_attr())
        .def(py::init<Tango::DeviceClass *, const char *, const char *, Tango::DevState, const char *>(),
             py::arg("klass"),
             py::arg("name"),
             py::arg("description") = "A Tango device",
             py::arg("state") = Tango::UNKNOWN,
             py::arg("status") = Tango::StatusNotSet)
        .def("init_device", &Tango::Device_3Impl::init_device)
        .def("server_init_hook",
             &Tango::Device_3Impl::server_init_hook,
             R"doc(
                server_init_hook(self)

                    Hook method.

                    This method is called once the device server admin device is exported.
                    This allows for instance for the different devices to subscribe
                    to events at server startup on attributes from other devices
                    of the same device server with stateless parameter set to false.

                    This method can be redefined in sub-classes in case of the default
                    behaviour does not fullfill the needs

                .. versionadded:: 9.4.2)doc")
        .def("delete_device",
             &Tango::Device_3Impl::delete_device,
             R"doc(
                delete_device(self)

                    Delete the device.)doc")
        .def("always_executed_hook",
             &Tango::Device_3Impl::always_executed_hook,
             R"doc(
                always_executed_hook(self)

                    Hook method.

                    Default method to implement an action necessary on a device before
                    any command is executed. This method can be redefined in sub-classes
                    in case of the default behaviour does not fullfill the needs

                :raises DevFailed: This method does not throw exception but a redefined method can.)doc")
        .def("read_attr_hardware",
             &Tango::Device_3Impl::read_attr_hardware,
             R"doc(
                read_attr_hardware(self, attr_list)

                    Read the hardware to return attribute value(s).

                    Default method to implement an action necessary on a device to read
                    the hardware involved in a read attribute CORBA call. This method
                    must be redefined in sub-classes in order to support attribute reading

                :param attr_list: list of indices in the device object attribute vector
                                  of an attribute to be read.
                :type attr_list: Sequence[int]

                :raises DevFailed: This method does not throw exception but a redefined method can.)doc",
             py::arg("attr_list"))
        .def("write_attr_hardware",
             &Tango::Device_3Impl::write_attr_hardware,
             R"doc(
                write_attr_hardware(self, attr_list)

                    Write the hardware for attributes.

                    Default method to implement an action necessary on a device to write
                    the hardware involved in a write attribute. This method must be
                    redefined in sub-classes in order to support writable attribute

                :param attr_list: list of indices in the device object attribute vector
                                  of an attribute to be written.
                :type attr_list: Sequence[int]

                :raises DevFailed: This method does not throw exception but a redefined method can.)doc",
             py::arg("attr_list"))
        .def("dev_state",
             &Tango::Device_3Impl::dev_state,
             R"doc(
                dev_state(self) -> DevState

                    Get device state.

                    Default method to get device state. The behaviour of this method depends
                    on the device state. If the device state is ON or ALARM, it reads the
                    attribute(s) with an alarm level defined, check if the read value is
                    above/below the alarm and eventually change the state to ALARM, return
                    the device state. For all th other device state, this method simply
                    returns the state This method can be redefined in sub-classes in case
                    of the default behaviour does not fullfill the needs.

                :returns: the device state
                :rtype: DevState

                :raises DevFailed: If it is necessary to read attribute(s) and a problem occurs during the reading)doc")
        .def("dev_status",
             &Tango::Device_3Impl::dev_status,
             R"doc(
                dev_status(self) -> str

                    Get device status.

                    Default method to get device status. It returns the contents of the device
                    dev_status field. If the device state is ALARM, alarm messages are added
                    to the device status. This method can be redefined in sub-classes in case
                    of the default behaviour does not fullfill the needs.

                :returns: the device status
                :rtype: str

                :raises DevFailed: If it is necessary to read attribute(s) and a problem occurs during the reading)doc")
        .def("signal_handler",
             &Tango::Device_3Impl::signal_handler,
             R"doc(
                signal_handler(self, signo)

                    Signal handler.

                    The method executed when the signal arrived in the device server process.
                    This method is defined as virtual and then, can be redefined following
                    device needs.

                :param signo: the signal number
                :type signo: int

                :raises DevFailed: This method does not throw exception but a redefined method can.)doc",
             py::arg("signo"))
        .def("_get_attribute_config_3", &Tango::Device_3Impl::get_attribute_config_3)
        .def("set_attribute_config_3",
             &Tango::Device_3Impl::set_attribute_config_3,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                set_attribute_config_3(self, new_conf) -> None

                    Sets attribute configuration locally and in the Tango database

                :param new_conf: The new attribute(s) configuration. One AttributeConfig structure is needed for each attribute to update
                :type new_conf: list[:class:`tango.AttributeConfig_3`]

                :returns: None
                :rtype: None)doc",
             py::arg("new_conf"));

    py::class_<Tango::Device_4Impl,
               LeakingSmartPtr<Tango::Device_4Impl>,
               Device_XImplTrampoline<Tango::Device_4Impl>,
               Tango::Device_3Impl>(m, "Device_4Impl", py::dynamic_attr())
        .def(py::init<Tango::DeviceClass *, const char *, const char *, Tango::DevState, const char *>(),
             py::arg("klass"),
             py::arg("name"),
             py::arg("description") = "A Tango device",
             py::arg("state") = Tango::UNKNOWN,
             py::arg("status") = Tango::StatusNotSet)
        .def("init_device", &Tango::Device_4Impl::init_device)
        .def("server_init_hook", &Tango::Device_4Impl::server_init_hook)
        .def("delete_device", &Tango::Device_4Impl::delete_device)
        .def("always_executed_hook", &Tango::Device_4Impl::always_executed_hook)
        .def("read_attr_hardware", &Tango::Device_4Impl::read_attr_hardware)
        .def("write_attr_hardware", &Tango::Device_4Impl::write_attr_hardware)
        .def("dev_state", &Tango::Device_4Impl::dev_state)
        .def("dev_status", &Tango::Device_4Impl::dev_status);

    py::class_<Tango::Device_5Impl,
               LeakingSmartPtr<Tango::Device_5Impl>,
               Device_XImplTrampoline<Tango::Device_5Impl>,
               Tango::Device_4Impl>(m, "Device_5Impl", py::dynamic_attr())
        .def(py::init<Tango::DeviceClass *, const char *, const char *, Tango::DevState, const char *>(),
             py::arg("klass"),
             py::arg("name"),
             py::arg("description") = "A Tango device",
             py::arg("state") = Tango::UNKNOWN,
             py::arg("status") = Tango::StatusNotSet)
        .def("init_device", &Tango::Device_5Impl::init_device)
        .def("server_init_hook", &Tango::Device_5Impl::server_init_hook)
        .def("delete_device", &Tango::Device_5Impl::delete_device)
        .def("always_executed_hook", &Tango::Device_5Impl::always_executed_hook)
        .def("read_attr_hardware", &Tango::Device_5Impl::read_attr_hardware)
        .def("write_attr_hardware", &Tango::Device_5Impl::write_attr_hardware)
        .def("dev_state", &Tango::Device_5Impl::dev_state)
        .def("dev_status", &Tango::Device_5Impl::dev_status);

    py::class_<Tango::Device_6Impl,
               LeakingSmartPtr<Tango::Device_6Impl>,
               Device_XImplTrampoline<Tango::Device_6Impl>,
               Tango::Device_5Impl>(m, "Device_6Impl", py::dynamic_attr())
        .def(py::init<Tango::DeviceClass *, const char *, const char *, Tango::DevState, const char *>(),
             py::arg("klass"),
             py::arg("name"),
             py::arg("description") = "A Tango device",
             py::arg("state") = Tango::UNKNOWN,
             py::arg("status") = Tango::StatusNotSet)
        .def("init_device", &Tango::Device_6Impl::init_device)
        .def("server_init_hook", &Tango::Device_6Impl::server_init_hook)
        .def("delete_device", &Tango::Device_6Impl::delete_device)
        .def("always_executed_hook", &Tango::Device_6Impl::always_executed_hook)
        .def("read_attr_hardware", &Tango::Device_6Impl::read_attr_hardware)
        .def("write_attr_hardware", &Tango::Device_6Impl::write_attr_hardware)
        .def("dev_state", &Tango::Device_6Impl::dev_state)
        .def("dev_status", &Tango::Device_6Impl::dev_status);
}
