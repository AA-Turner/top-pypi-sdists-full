/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "common_header.h"
#include "types_structs_macros.h"
#include "convertors/attributes/extract_value.h"
#include "convertors/type_casters.h"

namespace PyDeviceAttribute {
template <int tangoTypeConst>
static inline void scalar_value_from_cpp_into_python(Tango::DeviceAttribute &self,
                                                     py::object &py_value,
                                                     [[maybe_unused]] PyTango::ExtractAs extract_as) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);

    if(self.get_written_dim_x() > 0) {
        std::vector<TangoScalarType> value;
        self.extract_read(value);
        // In the following lines, the cast is absolutely necessary because
        // vector<TangoScalarType> may not be a vector<TangoScalarType> at
        // compile time. For example, for vector<DevBoolean>, the compiler
        // may create a std::_Bit_reference type.
        py_value.attr(value_attr_name) = cpp_to_python_scalar<tangoTypeConst>::convert(value[0]);
        self.extract_set(value);
        py_value.attr(w_value_attr_name) = cpp_to_python_scalar<tangoTypeConst>::convert(value[0]);
    } else {
        TangoScalarType value;
        EXTRACT_VALUE(self, value)
        py_value.attr(value_attr_name) = cpp_to_python_scalar<tangoTypeConst>::convert(value);
        py_value.attr(w_value_attr_name) = py::none();
    }
}

template <>
inline void scalar_value_from_cpp_into_python<Tango::DEV_STRING>(Tango::DeviceAttribute &self,
                                                                 py::object &py_value,
                                                                 [[maybe_unused]] PyTango::ExtractAs extract_as) {
    if(self.get_written_dim_x() > 0) {
        std::vector<std::string> r_val, w_val;
        self.extract_read(r_val);
        py_value.attr(value_attr_name) = from_cpp_str_to_pybind11_str(r_val[0]);
        self.extract_set(w_val);
        py_value.attr(w_value_attr_name) = from_cpp_str_to_pybind11_str(w_val[0]);
    } else {
        std::string rvalue;
        EXTRACT_VALUE(self, rvalue)
        py_value.attr(value_attr_name) = from_cpp_str_to_pybind11_str(rvalue);
        py_value.attr(w_value_attr_name) = py::none();
    }
}

template <>
inline void scalar_value_from_cpp_into_python<Tango::DEV_ENCODED>(Tango::DeviceAttribute &self,
                                                                  py::object &py_value,
                                                                  PyTango::ExtractAs extract_as) {
    Tango::DevVarEncodedArray *value_ptr;
    EXTRACT_VALUE(self, value_ptr)
    std::unique_ptr<Tango::DevVarEncodedArray> guard(value_ptr);

    Tango::DevEncoded *buffer = value_ptr->get_buffer();
    Tango::DevEncoded &read_buffer = buffer[0];

    py_value.attr(value_attr_name) = cpp_to_python_scalar<Tango::DEV_ENCODED>::convert(read_buffer,
                                                                                       extract_as);

    if(self.get_written_dim_x() > 0) {
        if(value_ptr->length() < 2) {
            py_value.attr(w_value_attr_name) = cpp_to_python_scalar<Tango::DEV_ENCODED>::convert(read_buffer,
                                                                                                 extract_as);
        } else {
            Tango::DevEncoded &write_buffer = buffer[1];
            py_value.attr(w_value_attr_name) = cpp_to_python_scalar<Tango::DEV_ENCODED>::convert(write_buffer,
                                                                                                 extract_as);
        }
    } else {
        py_value.attr(w_value_attr_name) = py::none();
    }
}

template <>
inline void scalar_value_from_cpp_into_python<Tango::DEV_PIPE_BLOB>([[maybe_unused]] Tango::DeviceAttribute &self,
                                                                    [[maybe_unused]] py::object &py_value,
                                                                    [[maybe_unused]] PyTango::ExtractAs extract_as) {
    assert(false);
}
} // namespace PyDeviceAttribute

namespace PyWAttribute {
template <int tangoTypeConst>
inline void scalar_value_from_cpp_into_python(Tango::WAttribute &att,
                                              py::object &py_value) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);

    TangoScalarType value;
    att.get_write_value(value);
    py_value = cpp_to_python_scalar<tangoTypeConst>::convert(value);
}

template <>
inline void scalar_value_from_cpp_into_python<Tango::DEV_STRING>(Tango::WAttribute &att,
                                                                 py::object &py_value) {
    Tango::DevString value = nullptr;
    att.get_write_value(value);

    if(value == nullptr) {
        py_value = py::none();
    } else {
        py_value = from_cpp_str_to_pybind11_str(value);
    }
}
} // namespace PyWAttribute
