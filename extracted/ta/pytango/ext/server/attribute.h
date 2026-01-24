/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#ifndef _ATTRIBUTE_H_
#define _ATTRIBUTE_H_

#include "common_header.h"

namespace PyAttribute {
void set_generic_value(Tango::Attribute &attr,
                       py::object &data,
                       double *time = nullptr,
                       Tango::AttrQuality *quality = nullptr);

void set_encoded_value(Tango::Attribute &attr,
                       py::object &encoding,
                       py::object &data,
                       const double *time = nullptr,
                       const Tango::AttrQuality *quality = nullptr);

py::object get_properties(Tango::Attribute &, py::object &);

py::object get_properties_2(Tango::Attribute &, py::object &);

py::object get_properties_3(Tango::Attribute &, py::object &);

py::object get_properties_multi_attr_prop(Tango::Attribute &, py::object &);

void set_properties(Tango::Attribute &, py::object &, py::object &);

void set_properties_3(Tango::Attribute &, py::object &, py::object &);

void set_properties_multi_attr_prop(Tango::Attribute &, py::object &);
} // namespace PyAttribute

#endif // _ATTRIBUTE_H_
