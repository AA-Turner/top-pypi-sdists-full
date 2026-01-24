/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "common_header.h"
#include "types_structs_macros.h"
#include "convertors/type_casters.h"
#include "convertors/data_array_from_py.h"

namespace PyDeviceAttribute {
template <int tangoTypeConst>
static inline void array_value_from_python_into_cpp(Tango::DeviceAttribute &dev_attr,
                                                    bool is_image,
                                                    py::object &py_value) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);
    using TangoArrayType = typename TANGO_const2arraytype(tangoTypeConst);
    static const int tangoArrayTypeConst = TANGO_const2arrayconst(tangoTypeConst);

    TangoScalarType *data_buffer;

    py::size_t res_dim_x = 0, res_dim_y = 0;
    data_buffer = python_to_cpp_buffer<tangoArrayTypeConst>(py_value,
                                                            MemoryAllocation::ALLOC,
                                                            "Tango::DeviceAttribute::reset",
                                                            is_image,
                                                            res_dim_x,
                                                            res_dim_y);

    py::size_t nelems = res_dim_x;
    if(is_image) {
        nelems *= res_dim_y;
    }

    try {
        std::unique_ptr<TangoArrayType> value;
        value.reset(new TangoArrayType(static_cast<unsigned int>(nelems),
                                       static_cast<unsigned int>(nelems),
                                       data_buffer,
                                       true));
        dev_attr.insert(value.get(), static_cast<int>(res_dim_x), static_cast<int>(res_dim_y));
        static_cast<void>(value.release());
    } catch(...) {
        TangoArrayType::freebuf(data_buffer);
        throw;
    }
}

template <>
inline void array_value_from_python_into_cpp<Tango::DEV_ENCODED>([[maybe_unused]] Tango::DeviceAttribute &dev_attr,
                                                                 [[maybe_unused]] bool is_image,
                                                                 [[maybe_unused]] py::object &py_value) {
    Tango::Except::throw_exception("PyDs_WrongPythonDataTypeForAttribute",
                                   "DevEncoded is only supported for SCALAR attributes.",
                                   "Tango::DeviceAttribute::reset");
}
} // namespace PyDeviceAttribute

namespace PyWAttribute {
template <int tangoTypeConst>
inline void array_value_from_python_into_cpp(Tango::WAttribute &att,
                                             bool is_image,
                                             py::object &py_value) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);
    static const long tangoArrayTypeConst = TANGO_const2arrayconst(tangoTypeConst);

    TangoScalarType *data_buffer;

    py::size_t res_dim_x = 0, res_dim_y = 0;
    data_buffer = python_to_cpp_buffer<tangoArrayTypeConst>(py_value,
                                                            MemoryAllocation::NEW,
                                                            "set_write_value",
                                                            is_image,
                                                            res_dim_x,
                                                            res_dim_y);

    try {
        att.set_write_value(data_buffer, static_cast<std::size_t>(res_dim_x), static_cast<std::size_t>(res_dim_y));
        delete[] data_buffer;
    } catch(...) {
        delete[] data_buffer;
        throw;
    }
}

template <>
inline void array_value_from_python_into_cpp<Tango::DEV_ENCODED>([[maybe_unused]] Tango::WAttribute &att,
                                                                 [[maybe_unused]] bool is_image,
                                                                 [[maybe_unused]] py::object &py_value) {
    Tango::Except::throw_exception("PyDs_WrongPythonDataTypeForAttribute",
                                   "DevEncoded is only supported for SCALAR attributes.",
                                   "set_write_value()");
}
} // namespace PyWAttribute
