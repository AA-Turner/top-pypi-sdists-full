/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_device_data_history(py::module &m) {
    py::class_<Tango::DeviceDataHistory, Tango::DeviceData>(m, "DeviceDataHistory")
        .def(py::init<>())

        // Copy constructor
        .def(py::init<const Tango::DeviceDataHistory &>())

        // Methods
        .def("has_failed",
             &Tango::DeviceDataHistory::has_failed,
             R"doc(
                Check if the record in the polling buffer was a failure
             )doc")
        .def("get_date",
             &Tango::DeviceDataHistory::get_date,
             R"doc(
                Get date when the device server polling thread has executed the command
             )doc",
             py::return_value_policy::reference_internal)
        .def("get_err_stack",
             &Tango::DeviceDataHistory::get_err_stack,
             R"doc(
                Get record error stack recorded by the device server polling thread in case of the command failed when it was invoked
             )doc",
             py::return_value_policy::copy);
}
