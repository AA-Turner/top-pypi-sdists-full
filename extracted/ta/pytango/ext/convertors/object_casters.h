/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "common_header.h"
#include "convertors/type_casters.h"

/*
 *      from cpp_tango to pytango
 */

template <typename T>
void to_py_object(Tango::MultiAttrProp<T> &multi_attr_prop, py::object &py_multi_attr_prop) {
    if(py_multi_attr_prop.ptr() == Py_None) {
        PYTANGO_MOD
        py_multi_attr_prop = pytango.attr("MultiAttrProp")();
    }

    py_multi_attr_prop.attr("label") = multi_attr_prop.label;
    py_multi_attr_prop.attr("description") = multi_attr_prop.description;
    py_multi_attr_prop.attr("unit") = multi_attr_prop.unit;
    py_multi_attr_prop.attr("standard_unit") = multi_attr_prop.standard_unit;
    py_multi_attr_prop.attr("display_unit") = multi_attr_prop.display_unit;
    py_multi_attr_prop.attr("format") = multi_attr_prop.format;
    py_multi_attr_prop.attr("min_value") = multi_attr_prop.min_value.get_str();
    py_multi_attr_prop.attr("max_value") = multi_attr_prop.max_value.get_str();
    py_multi_attr_prop.attr("min_alarm") = multi_attr_prop.min_alarm.get_str();
    py_multi_attr_prop.attr("max_alarm") = multi_attr_prop.max_alarm.get_str();
    py_multi_attr_prop.attr("min_warning") = multi_attr_prop.min_warning.get_str();
    py_multi_attr_prop.attr("max_warning") = multi_attr_prop.max_warning.get_str();
    py_multi_attr_prop.attr("delta_t") = multi_attr_prop.delta_t.get_str();
    py_multi_attr_prop.attr("delta_val") = multi_attr_prop.delta_val.get_str();
    py_multi_attr_prop.attr("event_period") = multi_attr_prop.event_period.get_str();
    py_multi_attr_prop.attr("archive_period") = multi_attr_prop.archive_period.get_str();
    py_multi_attr_prop.attr("rel_change") = multi_attr_prop.rel_change.get_str();
    py_multi_attr_prop.attr("abs_change") = multi_attr_prop.abs_change.get_str();
    py_multi_attr_prop.attr("archive_rel_change") = multi_attr_prop.archive_rel_change.get_str();
    py_multi_attr_prop.attr("archive_abs_change") = multi_attr_prop.archive_abs_change.get_str();
}

/*
 *      from pytango to cpp_tango
 */

template <typename T>
void assign_attr_prop(py::object &py_obj,
                      const std::string &attr_name,
                      Tango::AttrProp<T> &attr_prop) {
    py::object attr_value = py_obj.attr(attr_name.c_str());

    try {
        attr_prop = attr_value.cast<std::string>();
    } catch(const py::cast_error &) {
        try {
            attr_prop = attr_value.cast<T>();
        } catch(const py::cast_error &) {
            throw std::runtime_error("Failed to cast : " + attr_name);
        }
    }
}

template <>
void assign_attr_prop(py::object &py_obj,
                      const std::string &attr_name,
                      Tango::AttrProp<Tango::DevString> &attr_prop);

void assign_double_attr_prop(py::object &py_obj,
                             const std::string &attr_name,
                             Tango::DoubleAttrProp<Tango::DevDouble> &attr_prop);

template <typename T>
void from_py_object(py::object &py_obj, Tango::MultiAttrProp<T> &multi_attr_prop) {
    multi_attr_prop.label = py::str(py_obj.attr("label")).cast<std::string>();
    multi_attr_prop.description = py::str(py_obj.attr("description")).cast<std::string>();
    multi_attr_prop.unit = py::str(py_obj.attr("unit")).cast<std::string>();
    multi_attr_prop.standard_unit = py::str(py_obj.attr("standard_unit")).cast<std::string>();
    multi_attr_prop.display_unit = py::str(py_obj.attr("display_unit")).cast<std::string>();
    multi_attr_prop.format = py::str(py_obj.attr("format")).cast<std::string>();

    std::vector<std::pair<std::string, Tango::AttrProp<T> &>> attributes = {
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
void from_py_object(py::object &py_obj, Tango::MultiAttrProp<Tango::DevEncoded> &multi_attr_prop);

template <>
void from_py_object(py::object &py_obj, Tango::MultiAttrProp<Tango::DevString> &multi_attr_prop);
