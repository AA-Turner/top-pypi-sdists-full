/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_device_attribute_history(py::module &m) {
    py::class_<Tango::DeviceAttributeHistory, Tango::DeviceAttribute>(m, "DeviceAttributeHistory")
        .def(py::init<>())

        // Copy constructor
        .def(py::init<const Tango::DeviceAttributeHistory &>())

        // Methods
        .def("has_failed", &Tango::DeviceAttributeHistory::has_failed);
}
