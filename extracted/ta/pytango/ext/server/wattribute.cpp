/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "pyutils.h"
#include "server/attribute_utils.h"
#include "convertors/type_casters.h"

#include "convertors/attributes/scalar_python_to_cpp.h"
#include "convertors/attributes/array_python_to_cpp.h"
#include "convertors/attributes/scalar_cpp_to_python.h"
#include "convertors/attributes/array_cpp_to_python.h"

namespace PyWAttribute {

inline void set_write_value(Tango::WAttribute &att, py::object &value) {
    long type = att.get_data_type();
    Tango::AttrDataFormat format = att.get_data_format();

    const bool is_image = (format == Tango::IMAGE);

    if(format == Tango::SCALAR) {
        TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_ID(type, scalar_value_from_python_into_cpp, att, value);
    } else {
        TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_ID(type, array_value_from_python_into_cpp, att, is_image, value);
    }
}

inline py::object get_write_value(Tango::WAttribute &att, PyTango::ExtractAs extract_as) {
    long type = att.get_data_type();
    py::object value;

    Tango::AttrDataFormat fmt = att.get_data_format();

    const bool isScalar = fmt == Tango::SCALAR;

    if(isScalar) {
        TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_ID(type, scalar_value_from_cpp_into_python, att, value);
    } else {
        TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_ID(type, array_value_from_cpp_into_python, att, value, extract_as);
    }
    return value;
}

/// @}

} // namespace PyWAttribute

void export_wattribute(py::module &m) {
    py::class_<Tango::WAttribute, Tango::Attribute>(
        m, "WAttribute", py::dynamic_attr(), "This class represents a Tango writable attribute")
        .def(
            "set_min_value",
            [](Tango::WAttribute &attr, py::object &value) { set_value_limit(attr, value, TargetValue::VALUE_MIN); },
            R"doc(
                Set attribute minimum value.

                :param value: the attribute minimum value. python data type must be compatible
                              with the attribute data format and type
                :type value: :py:obj:`str`
            )doc",
            py::arg("value"))
        .def(
            "set_max_value",
            [](Tango::WAttribute &attr, py::object &value) { set_value_limit(attr, value, TargetValue::VALUE_MAX); },
            R"doc(
                Set attribute maximum value.

                :param value: the attribute maximum value. python data type must be compatible
                              with the attribute data format and type
                :type value: :py:obj:`str`
            )doc",
            py::arg("value"))
        .def(
            "get_min_value",
            [](Tango::WAttribute &attr) { return get_value_limit(attr, TargetValue::VALUE_MIN); },
            R"doc(
                Get attribute minimum value or throws an exception if the
                attribute does not have a minimum value.

                :returns: an object with the python minimum value
                :rtype: :py:obj:`typing.Any`
            )doc")
        .def(
            "get_max_value",
            [](Tango::WAttribute &attr) { return get_value_limit(attr, TargetValue::VALUE_MAX); },
            R"doc(
                Get attribute maximum value or throws an exception if the
                attribute does not have a maximum value.

                :returns: an object with the python maximum value
                :rtype: :py:obj:`typing.Any`
            )doc")
        .def("is_min_value",
             &Tango::WAttribute::is_min_value,
             R"doc(
                Check if the attribute has a minimum value.
             )doc")
        .def("is_max_value",
             &Tango::WAttribute::is_max_value,
             R"doc(
                Check if the attribute has a maximum value.
             )doc")
        .def("get_write_value_length",
             &Tango::WAttribute::get_write_value_length,
             R"doc(
                Retrieve the new value length (data number) for writable attribute.
             )doc")
        .def(
            "set_write_value",
            [](Tango::WAttribute &attr, py::object &value) { PyWAttribute::set_write_value(attr, value); },
            R"doc(
                Set the writable attribute value.

                :param value: the data to be set. Data must be compatible with the attribute type and format.
                             for SPECTRUM and IMAGE attributes, data can be any type of sequence of elements
                             compatible with the attribute type
                :type value: Any

                .. versionchanged:: 10.1.0
                    The dim_x and dim_y parameters were removed
            )doc",
            py::arg("value"))
        .def("get_write_value",
             &PyWAttribute::get_write_value,
             R"doc(
                Retrieve the new value for writable attribute.

                :param extract_as: defaults to ExtractAs.Numpy
                :type extract_as: :obj:`~tango.ExtractAs`

                :returns: the attribute write value.
                :rtype: :py:obj:`typing.Any`
             )doc",
             py::arg_v("extract_as", PyTango::ExtractAsNumpy, "ExtractAs.Numpy"));
    fix_dynamic_attr_dealloc<Tango::WAttribute>();
}
