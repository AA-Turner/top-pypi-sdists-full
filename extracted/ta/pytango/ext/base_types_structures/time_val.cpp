/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_time_val(py::module &m) {
    py::class_<Tango::TimeVal>(m,
                               "TimeVal",
                               R"doc(
    Time value structure with the following members:

        - tv_sec : seconds
        - tv_usec : microseconds
        - tv_nsec : nanoseconds
)doc")
        .def(py::init<>())
        .def_readwrite("tv_sec", &Tango::TimeVal::tv_sec)
        .def_readwrite("tv_usec", &Tango::TimeVal::tv_usec)
        .def_readwrite("tv_nsec", &Tango::TimeVal::tv_nsec);
}
