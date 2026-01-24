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
                has_failed(self) -> bool

                    Check if the record was a failure

                :returns: a boolean set to true if the record in the polling buffer was a failure
                :rtype: bool)doc")
        .def("get_date",
             &Tango::DeviceDataHistory::get_date,
             R"doc(
                get_date(self) -> TimeVal
                    Get record polling date

                :returns: the date when the device server polling thread has executed the command
                :rtype: TimeVal)doc",
             py::return_value_policy::reference_internal)
        .def("get_err_stack",
             &Tango::DeviceDataHistory::get_err_stack,
             R"doc(
                get_err_stack(self) -> DevErrorList

                    Get record error stack

                :returns: the error stack recorded by the device server polling thread in case of the command failed when it was invoked
                :rtype: DevErrorList)doc",
             py::return_value_policy::copy);
}
