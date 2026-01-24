/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

#include "client/device_attribute.h"

namespace PyGroupAttrReply {
py::object get_data(Tango::GroupAttrReply &self, PyTango::ExtractAs extract_as) {
    // Usually we pass a device_proxy to "convert_to_python" in order to
    // get the data_format of the DeviceAttribute for Tango versions
    // older than 7.0. However, GroupAttrReply has no device_proxy to use!
    // So, we are using update_data_format() in:
    //       GroupElement::read_attribute_reply/read_attributes_reply
    return PyDeviceAttribute::convert_to_python(new Tango::DeviceAttribute(self.get_data()), extract_as);
}
} // namespace PyGroupAttrReply

void export_group_reply(py::module &m) {
    py::class_<Tango::GroupReply>(m,
                                  "GroupReply",
                                  py::dynamic_attr(),
                                  R"doc(
            This is the base class for the result of an operation on a
            PyTangoGroup, being it a write attribute, read attribute, or
            command inout operation.

            It has some trivial common operations:

                - has_failed(self) -> bool
                - group_element_enabled(self) ->bool
                - dev_name(self) -> str
                - obj_name(self) -> str
                - get_err_stack(self) -> DevErrorList)doc")
        .def(py::init<const Tango::GroupReply &>())
        .def("has_failed", &Tango::GroupReply::has_failed)
        .def("group_element_enabled",
             &Tango::GroupReply::group_element_enabled,
             R"doc(
                group_element_enabled(self) -> bool

                    Check if the group element corresponding to this reply is enabled.

                :return: true if corresponding element is enabled, false otherwise
                :rtype: bool)doc")
        // TODO: this method seems to be usefull, but I cannot export it due to compilation error
        //        .def("enable_exception",
        //             &Tango::GroupReply::enable_exception,
        //             R"doc(
        //                enable_exception(self, exception_mode=True) -> bool
        //
        //                    Set the group exception mode. If set to true, exception will be thrown
        //                    (when needed) by the library when the user get command  execution result.
        //                    If set to false (the default), the user has to deal with the has_failed()
        //                    exception to manage cases of wrong execution command.
        //
        //                :param exception_mode: The new exception mode. Default: True
        //                :type exception_mode: bool
        //
        //                :return: The previous exception mode
        //                :rtype: bool)doc",
        //             py::arg("exception_mode")=true)
        .def("dev_name",
             &Tango::GroupReply::dev_name,
             R"doc(
                dev_name(self) -> str

                    Returns the device name for the group element

                :return: The device name
                :rtype: str)doc",
             py::return_value_policy::copy)
        .def("obj_name",
             &Tango::GroupReply::obj_name,
             R"doc(
                obj_name(self) -> str

                    The object name

                :return: The device name
                :rtype: str)doc",
             py::return_value_policy::copy)
        .def("get_err_stack",
             &Tango::GroupReply::get_err_stack,
             R"doc(
                get_err_stack(self) -> DevErrorList

                    Get error stack

                :return: The error stack
                :rtype: DevErrorList)doc",
             py::return_value_policy::copy);

    py::class_<Tango::GroupCmdReply, Tango::GroupReply>(m, "GroupCmdReply", py::dynamic_attr())
        .def("get_data_raw",
             &Tango::GroupCmdReply::get_data,
             py::return_value_policy::reference_internal,
             R"doc(
                get_data_raw(self) -> any

                        Get the DeviceData containing the output parameter
                        of the command.

                    Parameters : None
                    Return     : (DeviceData) Whatever is stored there, or None.)doc");

    py::class_<Tango::GroupAttrReply, Tango::GroupReply>(m, "GroupAttrReply", py::dynamic_attr())
        .def("get_data",
             &PyGroupAttrReply::get_data,
             py::arg_v("extract_as", PyTango::ExtractAsNumpy, "ExtractAs.Numpy"),
             R"doc(
    Get the DeviceAttribute.

    Parameters :
        - extract_as : (ExtractAs)

    Return     : (DeviceAttribute) Whatever is stored there, or None.

        )doc");
}
