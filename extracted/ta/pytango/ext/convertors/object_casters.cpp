/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "object_casters.h"

template <>
void assign_attr_prop(py::object &py_obj, const std::string &attr_name, Tango::AttrProp<Tango::DevString> &attr_prop) {
    py::object attr_value = py_obj.attr(attr_name.c_str());

    // pybind11's std::string caster accepts bytes and bytearray as well as str
    if(py::isinstance<py::str>(attr_value) || py::isinstance<py::bytes>(attr_value) ||
       py::isinstance<py::bytearray>(attr_value)) {
        try {
            attr_prop = attr_value.cast<std::string>();
            return;
        } catch(const py::cast_error &) {
            // the caster also requires a str to encode to UTF-8: if it does not,
            // the value is handled below like any other non-string
        }
    }

    attr_prop = std::string("");
}
