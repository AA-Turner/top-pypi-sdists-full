/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

#include "server/device_class.h"
#include "server/attr.h"
#include "server/command.h"

void DeviceClassTrampoline::create_command(const std::string &cmd_name,
                                           Tango::CmdArgType param_type,
                                           Tango::CmdArgType result_type,
                                           const std::string &param_desc,
                                           const std::string &result_desc,
                                           Tango::DispLevel display_level,
                                           bool default_command,
                                           long polling_period,
                                           const std::string &is_allowed) {
    PyCmd *cmd_ptr =
        new PyCmd(cmd_name.c_str(), param_type, result_type, param_desc.c_str(), result_desc.c_str(), display_level);

    if(!is_allowed.empty()) {
        cmd_ptr->set_allowed(is_allowed);
    }

    if(polling_period > 0) {
        cmd_ptr->set_polling_period(polling_period);
    }
    if(default_command) {
        Tango::DeviceClass::set_default_command(cmd_ptr);
    } else {
        Tango::DeviceClass::command_list.push_back(cmd_ptr);
    }
}

void DeviceClassTrampoline::create_fwd_attribute(std::vector<Tango::Attr *> &att_list,
                                                 const std::string &attr_name,
                                                 Tango::UserDefaultFwdAttrProp *att_prop) {
    Tango::FwdAttr *attr_ptr = new Tango::FwdAttr(attr_name);
    attr_ptr->set_default_properties(*att_prop);
    att_list.push_back(attr_ptr);
}

void DeviceClassTrampoline::create_attribute(std::vector<Tango::Attr *> &att_list,
                                             const std::string &attr_name,
                                             Tango::CmdArgType attr_type,
                                             Tango::AttrDataFormat attr_format,
                                             Tango::AttrWriteType attr_write,
                                             long dim_x,
                                             long dim_y,
                                             Tango::DispLevel display_level,
                                             long polling_period,
                                             bool memorized,
                                             bool hw_memorized,
                                             bool alarm_event_implemented,
                                             bool alarm_event_detect,
                                             bool archive_event_implemented,
                                             bool archive_event_detect,
                                             bool change_event_implemented,
                                             bool change_event_detect,
                                             bool data_ready_event_implemented,
                                             const std::string &read_method_name,
                                             const std::string &write_method_name,
                                             const std::string &is_allowed_name,
                                             Tango::UserDefaultAttrProp *att_prop) {
    //
    // Create the attribute objet according to attribute format
    //

    PyScaAttr *sca_attr_ptr = nullptr;
    PySpecAttr *spec_attr_ptr = nullptr;
    PyImaAttr *ima_attr_ptr = nullptr;
    PyAttr *py_attr_ptr = nullptr;
    Tango::Attr *attr_ptr = nullptr;

    switch(attr_format) {
    case Tango::SCALAR:
        sca_attr_ptr = new PyScaAttr(attr_name, attr_type, attr_write);
        py_attr_ptr = sca_attr_ptr;
        attr_ptr = sca_attr_ptr;
        break;

    case Tango::SPECTRUM:
        spec_attr_ptr = new PySpecAttr(attr_name.c_str(), attr_type, attr_write, dim_x);
        py_attr_ptr = spec_attr_ptr;
        attr_ptr = spec_attr_ptr;
        break;

    case Tango::IMAGE:
        ima_attr_ptr = new PyImaAttr(attr_name.c_str(), attr_type, attr_write, dim_x, dim_y);
        py_attr_ptr = ima_attr_ptr;
        attr_ptr = ima_attr_ptr;
        break;

    default:
        std::string reason = "PyDs_UnexpectedAttributeFormat";
        std::string desc = "Attribute " + attr_name + " has an unexpected data format\nPlease report this bug to the PyTango development team";
        std::string origin = "create_attribute";

        Tango::Except::throw_exception(reason, desc, origin);
        break;
    }

    py_attr_ptr->set_read_name(read_method_name);
    py_attr_ptr->set_write_name(write_method_name);
    py_attr_ptr->set_allowed_name(is_allowed_name);

    if(att_prop != nullptr) {
        attr_ptr->set_default_properties(*att_prop);
    }

    attr_ptr->set_disp_level(display_level);
    if(memorized) {
        attr_ptr->set_memorized();
        attr_ptr->set_memorized_init(hw_memorized);
    }

    if(polling_period > 0) {
        attr_ptr->set_polling_period(polling_period);
    }

    attr_ptr->set_alarm_event(alarm_event_implemented, alarm_event_detect);
    attr_ptr->set_archive_event(archive_event_implemented, archive_event_detect);
    attr_ptr->set_change_event(change_event_implemented, change_event_detect);
    attr_ptr->set_data_ready_event(data_ready_event_implemented);

    att_list.push_back(attr_ptr);
}

namespace PyDeviceClass {
py::object get_device_list(Tango::DeviceClass &self) {
    py::list py_dev_list;
    std::vector<Tango::DeviceImpl *> dev_list = self.get_device_list();
    for(auto *dev_ptr : dev_list) {
        py_dev_list.append(py::cast(dev_ptr, py::return_value_policy::reference_internal));
    }
    return py_dev_list;
}

py::object get_command_list(Tango::DeviceClass &self) {
    py::list py_cmd_list;
    std::vector<Tango::Command *> cmd_list = self.get_command_list();
    for(auto *cmd_ptr : cmd_list) {
        py_cmd_list.append(py::cast(cmd_ptr, py::return_value_policy::reference_internal));
    }
    return py_cmd_list;
}

void register_signal(Tango::DeviceClass &self, long signo) {
    self.register_signal(signo);
}

#if !defined WIN32

void register_signal(Tango::DeviceClass &self, long signo, bool own_handler) {
    self.register_signal(signo, own_handler);
}

#endif

} // namespace PyDeviceClass

void export_device_class(py::module &m) {
    py::class_<Tango::DeviceClass,
               LeakingSmartPtr<Tango::DeviceClass>,
               DeviceClassTrampoline>(m,
                                      "DeviceClass",
                                      py::dynamic_attr(),
                                      R"doc(
                                        Base class for all TANGO device-class class.
                                        A TANGO device-class class is a class where is stored all
                                        data/method common to all devices of a TANGO device class)doc")
        .def(py::init_alias<const std::string &>())
        .def("device_factory",
             &Tango::DeviceClass::device_factory,
             py::arg("dev_list"))
        .def("device_name_factory",
             &Tango::DeviceClass::device_name_factory,
             py::arg("list"))
        .def(
            "export_device",
            [](Tango::DeviceClass &self, Tango::DeviceImpl *dev, const char *corba_dev_nam) {
                static_cast<DeviceClassTrampoline &>(self).export_device(dev, corba_dev_nam);
            },
            py::call_guard<py::gil_scoped_release>(),
            R"doc(
                export_device(self, dev, corba_dev_name = 'Unused') -> None

                        For internal usage only

                    Parameters :
                        - dev : (DeviceImpl) device object
                        - corba_dev_name : (str) CORBA device name. Default value is 'Unused'

                    Return     : None)doc",
            py::arg("dev"),
            py::arg("corba_dev_name") = "Unused")
        .def("_add_device", &Tango::DeviceClass::add_device, py::arg("device"))
        .def("register_signal",
             py::overload_cast<Tango::DeviceClass &, long>(&PyDeviceClass::register_signal),
             R"doc(
                register_signal(self, signo) -> None

                        Register a signal.
                        Register this class as class to be informed when signal signo
                        is sent to to the device server process.
                        The second version of the method is available only under Linux.

                    Throws tango.DevFailed:
                        - if the signal number is out of range
                        - if the operating system failed to register a signal for the process.

                    Parameters :
                        - signo : (int) signal identifier

                    Return     : None)doc",
             py::arg("signo"))
#if !defined WIN32
        .def("register_signal",
             py::overload_cast<Tango::DeviceClass &, long, bool>(&PyDeviceClass::register_signal),
             R"doc(
                register_signal(self, signo, own_handler) -> None

                        Register a signal.
                        Register this class as class to be informed when signal signo
                        is sent to to the device server process.
                        The second version of the method is available only under Linux.

                    Throws tango.DevFailed:
                        - if the signal number is out of range
                        - if the operating system failed to register a signal for the process.

                    Parameters :
                        - signo : (int) signal identifier
                        - own_handler : (bool) true if you want the device signal handler
                                        to be executed in its own handler instead of being
                                        executed by the signal thread. If this parameter
                                        is set to true, care should be taken on how the
                                        handler is written. A default false value is provided

                    Return     : None)doc",
             py::arg("signo"),
             py::arg("own_handler"))
#endif
        .def("unregister_signal",
             &Tango::DeviceClass::unregister_signal,
             R"doc(
                unregister_signal(self, signo) -> None

                        Unregister a signal.
                        Unregister this class as class to be informed when signal signo
                        is sent to to the device server process

                    Parameters :
                        - signo : (int) signal identifier
                    Return     : None)doc",
             py::arg("signo"))
        .def("signal_handler",
             &Tango::DeviceClass::signal_handler,
             R"doc(
                signal_handler(self, signo) -> None

                        Signal handler.

                        The method executed when the signal arrived in the device server process.
                        This method is defined as virtual and then, can be redefined following
                        device class needs.

                    Parameters :
                        - signo : (int) signal identifier
                    Return     : None)doc",
             py::arg("signo"))
        .def("get_name",
             &Tango::DeviceClass::get_name,
             py::return_value_policy::copy,
             R"doc(
                get_name(self) -> str

                    Get the TANGO device class name.

                Parameters : None
                Return     : (str) the TANGO device class name.)doc")
        .def("get_type",
             &Tango::DeviceClass::get_type,
             py::return_value_policy::copy,
             R"doc(
                get_type(self) -> str

                    Gets the TANGO device type name.

                Parameters : None
                Return     : (str) the TANGO device type name)doc")
        .def("get_doc_url",
             &Tango::DeviceClass::get_doc_url,
             py::return_value_policy::copy,
             R"doc(
                get_doc_url(self) -> str

                    Get the TANGO device class documentation URL.

                Parameters : None
                Return     : (str) the TANGO device type name)doc")
        .def("get_cvs_tag",
             &Tango::DeviceClass::get_cvs_tag,
             py::return_value_policy::copy,
             R"doc(
                get_cvs_tag(self) -> str

                    Gets the cvs tag

                Parameters : None
                Return     : (str) cvs tag)doc")
        .def("get_cvs_location",
             &Tango::DeviceClass::get_cvs_location,
             py::return_value_policy::copy,
             R"doc(
                get_cvs_location(self) -> None

                    Gets the cvs localtion

                Parameters : None
                Return     : (str) cvs location)doc")
        .def("get_device_list",
             &PyDeviceClass::get_device_list,
             R"doc(
                get_device_list(self) -> sequence<tango.DeviceImpl>

                    Gets the list of tango.DeviceImpl objects for this class

                Parameters : None
                Return     : (sequence<tango.DeviceImpl>) list of tango.DeviceImpl objects for this class)doc")
        .def("get_command_list",
             &PyDeviceClass::get_command_list,
             R"doc(
                get_command_list(self) -> sequence<tango.Command>

                    Gets the list of tango.Command objects for this class

                Parameters : None
                Return     : (sequence<tango.Command>) list of tango.Command objects for this class

                New in PyTango 8.0.0)doc")
        .def("get_cmd_by_name",
             &Tango::DeviceClass::get_cmd_by_name,
             py::return_value_policy::reference_internal,
             R"doc(
                get_cmd_by_name(self, (str)cmd_name) -> tango.Command

                    Get a reference to a command object.

                Parameters :
                    - cmd_name : (str) command name
                Return     : (tango.Command) tango.Command object

                New in PyTango 8.0.0)doc",
             py::arg("cmd_name"))
        .def("set_type",
             py::overload_cast<const char *>(&Tango::DeviceClass::set_type),
             R"doc(
                set_type(self, dev_type) -> None

                    Set the TANGO device type name.

                Parameters :
                    - dev_type : (str) the new TANGO device type name
                Return     : None)doc",
             py::arg("dev_type"))
        .def("add_wiz_dev_prop",
             py::overload_cast<const std::string &, const std::string &>(&Tango::DeviceClass::add_wiz_dev_prop),
             R"doc(
                add_wiz_dev_prop(self, name, desc) -> None

                    For internal usage only

                :param str name: device property name
                :param str desc: device property description

                :return: None)doc",
             py::arg("name"),
             py::arg("desc"))
        .def("add_wiz_dev_prop",
             py::overload_cast<const std::string &, const std::string &, const std::string &>(&Tango::DeviceClass::add_wiz_dev_prop),
             R"doc(
                add_wiz_dev_prop(self, name, desc, default) -> None

                    For internal usage only

                :param str name: device property name
                :param str desc: device property description
                :param str default: device property default value

                :return: None)doc",
             py::arg("name"),
             py::arg("desc"),
             py::arg("default"))
        .def("add_wiz_class_prop",
             py::overload_cast<const std::string &, const std::string &>(&Tango::DeviceClass::add_wiz_class_prop),
             R"doc(
                add_wiz_class_prop(self, name, desc) -> None

                    For internal usage only

                :param str name: class property name
                :param str desc: class property description

                :return: None)doc",
             py::arg("name"),
             py::arg("desc"))
        .def("add_wiz_class_prop",
             py::overload_cast<const std::string &, const std::string &, const std::string &>(&Tango::DeviceClass::add_wiz_class_prop),
             R"doc(
                add_wiz_class_prop(self, name, desc, default) -> None

                    For internal usage only

                :param str name: class property name
                :param str desc: class property description
                :param str default: class property default value

                :return: None)doc",
             py::arg("name"),
             py::arg("desc"),
             py::arg("default"))
        .def("_device_destroyer",
             py::overload_cast<const char *>(&Tango::DeviceClass::device_destroyer),
             py::call_guard<py::gil_scoped_release>())
        .def("_create_attribute",
             [](Tango::DeviceClass &self,
                VectorWrapper<Tango::Attr> &py_att_list,
                const std::string &attr_name,
                Tango::CmdArgType attr_type,
                Tango::AttrDataFormat attr_format,
                Tango::AttrWriteType attr_write,
                long dim_x,
                long dim_y,
                Tango::DispLevel display_level,
                long polling_period,
                bool memorized,
                bool hw_memorized,
                bool alarm_event_implemented,
                bool alarm_event_detect,
                bool archive_event_implemented,
                bool archive_event_detect,
                bool change_event_implemented,
                bool change_event_detect,
                bool data_ready_event_implemented,
                const std::string &read_method_name,
                const std::string &write_method_name,
                const std::string &is_allowed_name,
                Tango::UserDefaultAttrProp *att_prop) {
                 static_cast<DeviceClassTrampoline &>(self).create_attribute(*py_att_list.get_ptr(),
                                                                             attr_name,
                                                                             attr_type,
                                                                             attr_format,
                                                                             attr_write,
                                                                             dim_x,
                                                                             dim_y,
                                                                             display_level,
                                                                             polling_period,
                                                                             memorized,
                                                                             hw_memorized,
                                                                             alarm_event_implemented,
                                                                             alarm_event_detect,
                                                                             archive_event_implemented,
                                                                             archive_event_detect,
                                                                             change_event_implemented,
                                                                             change_event_detect,
                                                                             data_ready_event_implemented,
                                                                             read_method_name,
                                                                             write_method_name,
                                                                             is_allowed_name,
                                                                             att_prop);
             })
        .def("_create_fwd_attribute",
             [](Tango::DeviceClass &self,
                VectorWrapper<Tango::Attr> &py_att_list,
                const std::string &attr_name,
                Tango::UserDefaultFwdAttrProp *att_prop) {
                 static_cast<DeviceClassTrampoline &>(self).create_fwd_attribute(*py_att_list.get_ptr(),
                                                                                 attr_name,
                                                                                 att_prop);
             })
        .def("_create_command",
             [](Tango::DeviceClass &self,
                const std::string &cmd_name,
                Tango::CmdArgType param_type,
                Tango::CmdArgType result_type,
                const std::string &param_desc,
                const std::string &result_desc,
                Tango::DispLevel display_level,
                bool default_command,
                long polling_period,
                const std::string &is_allowed) {
                 static_cast<DeviceClassTrampoline &>(self).create_command(cmd_name,
                                                                           param_type,
                                                                           result_type,
                                                                           param_desc,
                                                                           result_desc,
                                                                           display_level,
                                                                           default_command,
                                                                           polling_period,
                                                                           is_allowed);
             })

        .def("get_class_attr",
             &Tango::DeviceClass::get_class_attr,
             py::return_value_policy::reference,
             R"doc(
                get_class_attr(self) -> None

                    Returns the instance of the :class:`tango.MultiClassAttribute` for the class

                :param: None

                :returns: the instance of the :class:`tango.MultiClassAttribute` for the class
                :rtype: :class:`tango.MultiClassAttribute`)doc");
}
