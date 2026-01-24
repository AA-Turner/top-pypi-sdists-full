/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"
#include "convertors/commands/cpp_to_python.h"
#include "convertors/commands/python_to_cpp.h"

#include "client/device_data.h"

namespace PyDeviceData {

Tango::CmdArgType get_type(Tango::DeviceData &self) {
    /// @todo This should change in Tango itself, get_type should not return int!!
    return static_cast<Tango::CmdArgType>(self.get_type());
}

void insert(Tango::DeviceData &self, long data_type, py::object py_value) {
    TANGO_DO_ON_DEVICE_DATA_TYPE_ID(data_type,
                                    (scalar_python_data_to_cpp<Tango::DeviceData, tangoTypeConst>(self, py_value));
                                    ,
                                    (array_python_data_to_cpp<Tango::DeviceData, tangoTypeConst>(self, py_value)););
}

py::object extract(py::object py_self, PyTango::ExtractAs extract_as) {
    Tango::DeviceData &self = py_self.cast<Tango::DeviceData &>();

    py::object ret;
    TANGO_DO_ON_DEVICE_DATA_TYPE_ID(self.get_type(),
                                    (scalar_cpp_data_to_python<Tango::DeviceData, tangoTypeConst>(self, ret));
                                    ,
                                    (array_cpp_data_to_python<tangoTypeConst>(self, py_self, ret, extract_as)););
    return ret;
}
} // namespace PyDeviceData

void export_device_data(py::module &m) {
    py::class_<Tango::DeviceData> DeviceData(m,
                                             "DeviceData",
                                             R"doc(
                This is the fundamental type for sending and receiving data from
                device commands. The values can be inserted and extracted using the
                insert() and extract() methods.)doc");

    DeviceData
        .def(py::init<>())
        .def(py::init<const Tango::DeviceData &>())
        .def("extract",
             &PyDeviceData::extract,
             R"doc(
                extract(self) -> any

                        Get the actual value stored in the DeviceData.

                    Parameters : None
                    Return     : Whatever is stored there, or None.)doc",
             py::arg_v("extract_as", PyTango::ExtractAsNumpy, "ExtractAs.Numpy"))
        .def("insert",
             &PyDeviceData::insert,
             R"doc(
                insert(self, data_type, value) -> None

                        Inserts a value in the DeviceData.

                    Parameters :
                            - data_type :
                            - value     : (any) The value to insert
                    Return     : Whatever is stored there, or None.)doc",
             py::arg("data_type"),
             py::arg("value"))
        .def("is_empty",
             &Tango::DeviceData::is_empty,
             R"doc(
                is_empty(self) -> bool

                        It can be used to test whether the DeviceData object has been
                        initialized or not.

                    Parameters : None
                    Return     : True or False depending on whether the DeviceData object
                                contains data or not.)doc")
        .def("get_type",
             &PyDeviceData::get_type,
             R"doc(
                get_type(self) -> CmdArgType

                        This method returns the Tango data type of the data inside the
                        DeviceData object.

                    Parameters : None
                    Return     : The content arg type.)doc");

    py::native_enum<Tango::DeviceData::except_flags>(DeviceData, "except_flags", "enum.IntEnum")
        .value("isempty_flag", Tango::DeviceData::isempty_flag)
        .value("wrongtype_flag", Tango::DeviceData::wrongtype_flag)
        .value("numFlags", Tango::DeviceData::numFlags)
        .finalize();

    py::object except_flags_class = DeviceData.attr("except_flags");
    add_names_values_to_native_enum(except_flags_class);
}
