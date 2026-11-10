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
static inline void
    array_value_from_python_into_cpp(Tango::DeviceAttribute &dev_attr, bool is_image, py::object &py_value) {
    if constexpr(tangoTypeConst == Tango::DEV_ENCODED) {
        Tango::Except::throw_exception("PyDs_WrongPythonDataTypeForAttribute",
                                       "DevEncoded is only supported for SCALAR attributes.",
                                       "Tango::DeviceAttribute::reset");
    } else {
        using TangoArrayType = typename TANGO_const2arraytype(tangoTypeConst);
        static const int tangoArrayTypeConst = TANGO_const2arrayconst(tangoTypeConst);

        py::size_t res_dim_x = 0, res_dim_y = 0;
        auto buffer = python_to_cpp_buffer<tangoArrayTypeConst, MemoryAllocation::ALLOC>(
            py_value, "Tango::DeviceAttribute::reset", is_image, res_dim_x, res_dim_y);

        std::unique_ptr<TangoArrayType> value(buffer.into_corba_sequence());
        dev_attr.insert(value.get(), static_cast<int>(res_dim_x), static_cast<int>(res_dim_y));
        static_cast<void>(value.release());
    }
}
} // namespace PyDeviceAttribute

namespace PyWAttribute {
template <int tangoTypeConst>
inline void array_value_from_python_into_cpp(Tango::WAttribute &att, bool is_image, py::object &py_value) {
    if constexpr(tangoTypeConst == Tango::DEV_ENCODED) {
        Tango::Except::throw_exception("PyDs_WrongPythonDataTypeForAttribute",
                                       "DevEncoded is only supported for SCALAR attributes.",
                                       "set_write_value()");
    } else {
        static const long tangoArrayTypeConst = TANGO_const2arrayconst(tangoTypeConst);

        py::size_t res_dim_x = 0, res_dim_y = 0;
        auto buffer = python_to_cpp_buffer<tangoArrayTypeConst, MemoryAllocation::NEW>(
            py_value, "set_write_value", is_image, res_dim_x, res_dim_y);

        // set_write_value copies the data, so the buffer stays ours.
        att.set_write_value(buffer.data(), static_cast<std::size_t>(res_dim_x), static_cast<std::size_t>(res_dim_y));
    }
}
} // namespace PyWAttribute
