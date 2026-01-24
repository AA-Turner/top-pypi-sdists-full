/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "object_casters.h"

template <>
void assign_attr_prop(py::object &py_obj,
                      const std::string &attr_name,
                      Tango::AttrProp<Tango::DevString> &attr_prop) {
    py::object attr_value = py_obj.attr(attr_name.c_str());

    try {
        attr_prop = attr_value.cast<std::string>();
    } catch(const py::cast_error &) {
        attr_prop = std::string("");
    }
}

template <>
void from_py_object(py::object &py_obj, Tango::MultiAttrProp<Tango::DevEncoded> &multi_attr_prop) {
    multi_attr_prop.label = py::str(py_obj.attr("label")).cast<std::string>();
    multi_attr_prop.description = py::str(py_obj.attr("description")).cast<std::string>();
    multi_attr_prop.unit = py::str(py_obj.attr("unit")).cast<std::string>();
    multi_attr_prop.standard_unit = py::str(py_obj.attr("standard_unit")).cast<std::string>();
    multi_attr_prop.display_unit = py::str(py_obj.attr("display_unit")).cast<std::string>();
    multi_attr_prop.format = py::str(py_obj.attr("format")).cast<std::string>();

    std::vector<std::pair<std::string, Tango::AttrProp<Tango::DevUChar> &>> attributes = {
        {"min_value", multi_attr_prop.min_value},
        {"max_value", multi_attr_prop.max_value},
        {"min_alarm", multi_attr_prop.min_alarm},
        {"max_alarm", multi_attr_prop.max_alarm},
        {"min_warning", multi_attr_prop.min_warning},
        {"max_warning", multi_attr_prop.max_warning},
        {"delta_val", multi_attr_prop.delta_val},
    };

    for(auto &[attr_name, attr_prop] : attributes) {
        assign_attr_prop(py_obj, attr_name, attr_prop);
    }

    assign_attr_prop(py_obj, "delta_t", multi_attr_prop.delta_t);
    assign_attr_prop(py_obj, "event_period", multi_attr_prop.event_period);
    assign_attr_prop(py_obj, "archive_period", multi_attr_prop.archive_period);

    assign_double_attr_prop(py_obj, "rel_change", multi_attr_prop.rel_change);
    assign_double_attr_prop(py_obj, "abs_change", multi_attr_prop.abs_change);
    assign_double_attr_prop(py_obj, "archive_rel_change", multi_attr_prop.archive_rel_change);
    assign_double_attr_prop(py_obj, "archive_abs_change", multi_attr_prop.archive_abs_change);
}

template <>
void from_py_object(py::object &py_obj, Tango::MultiAttrProp<Tango::DevString> &multi_attr_prop) {
    multi_attr_prop.label = py::str(py_obj.attr("label")).cast<std::string>();
    multi_attr_prop.description = py::str(py_obj.attr("description")).cast<std::string>();
    multi_attr_prop.unit = py::str(py_obj.attr("unit")).cast<std::string>();
    multi_attr_prop.standard_unit = py::str(py_obj.attr("standard_unit")).cast<std::string>();
    multi_attr_prop.display_unit = py::str(py_obj.attr("display_unit")).cast<std::string>();
    multi_attr_prop.format = py::str(py_obj.attr("format")).cast<std::string>();

    std::vector<std::pair<std::string, Tango::AttrProp<Tango::DevString> &>> attributes = {
        {"min_value", multi_attr_prop.min_value},
        {"max_value", multi_attr_prop.max_value},
        {"min_alarm", multi_attr_prop.min_alarm},
        {"max_alarm", multi_attr_prop.max_alarm},
        {"min_warning", multi_attr_prop.min_warning},
        {"max_warning", multi_attr_prop.max_warning},
        {"delta_val", multi_attr_prop.delta_val},
    };

    for(auto &[attr_name, attr_prop] : attributes) {
        assign_attr_prop(py_obj, attr_name, attr_prop);
    }

    assign_attr_prop(py_obj, "delta_t", multi_attr_prop.delta_t);
    assign_attr_prop(py_obj, "event_period", multi_attr_prop.event_period);
    assign_attr_prop(py_obj, "archive_period", multi_attr_prop.archive_period);

    assign_double_attr_prop(py_obj, "rel_change", multi_attr_prop.rel_change);
    assign_double_attr_prop(py_obj, "abs_change", multi_attr_prop.abs_change);
    assign_double_attr_prop(py_obj, "archive_rel_change", multi_attr_prop.archive_rel_change);
    assign_double_attr_prop(py_obj, "archive_abs_change", multi_attr_prop.archive_abs_change);
}
