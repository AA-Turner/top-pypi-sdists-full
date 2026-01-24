/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_attribute_dimension(py::module &m) {
    py::class_<Tango::AttributeDimension>(m,
                                          "AttributeDimension",
                                          R"doc(
    A structure containing x and y attribute data dimensions with
    the following members:

        - dim_x : (int) x dimension
        - dim_y : (int) y dimension
)doc")
        .def(py::init<>())
        .def_readonly("dim_x", &Tango::AttributeDimension::dim_x)
        .def_readonly("dim_y", &Tango::AttributeDimension::dim_y);
}
