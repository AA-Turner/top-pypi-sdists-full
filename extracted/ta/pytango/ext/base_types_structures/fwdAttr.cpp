/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_user_default_fwdattr_prop(py::module &m) {
    py::class_<Tango::UserDefaultFwdAttrProp>(m, "UserDefaultFwdAttrProp")
        .def(py::init<>())
        .def("set_label",
             &Tango::UserDefaultFwdAttrProp::set_label,
             R"doc(
                Set default label property

                :param def_label: The user default label property
                :type def_label: :py:obj:`str`)doc",
             py::arg("def_label"));
}

void export_fwdattr(py::module &m) {
    py::class_<Tango::FwdAttr>(m, "FwdAttr")
        .def(py::init<const std::string &, const std::string &>())
        .def("set_default_properties",
             &Tango::FwdAttr::set_default_properties,
             R"doc(
                Set default attribute properties

                :param prop: The user default property class
                :type prop: :py:obj:`~tango.UserDefaultAttrProp`)doc",
             py::arg("prop"));
}
