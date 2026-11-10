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

template <typename T, int tangoTypeConst>
inline void scalar_python_data_to_cpp(T &self, py::object &py_value) {
    if constexpr(tangoTypeConst == Tango::DEV_PIPE_BLOB) {
        raise_(PyExc_TypeError, "DEV_PIPE_BLOB not supported!");
    } else if constexpr(tangoTypeConst == Tango::DEV_VOID && std::is_same_v<T, Tango::DeviceData>) {
        raise_(PyExc_TypeError, "Trying to insert a value in a DEV_VOID DeviceData!");
    } else if constexpr(tangoTypeConst == Tango::DEV_VOID) {
        // CORBA::Any: nothing to insert
    } else {
        TangoScalar<tangoTypeConst> value(py_value);

        // to make live of Tango developer "easier", cppTango uses different operators to insert value in different
        // object Don't let your guard down, it`s TANGO!!!
        if constexpr(std::is_same_v<T, Tango::DeviceData>) {
            self << value.get();
        } else {
            if constexpr(tangoTypeConst == Tango::DEV_BOOLEAN) {
                self <<= CORBA::Any::from_boolean(value.get());
            } else {
                self <<= value.get();
            }
        }
    }
}

template <typename T, int tangoArrayTypeConst>
inline void array_python_data_to_cpp(T &self, py::object &py_value) {
    if constexpr(tangoArrayTypeConst == Tango::DEV_PIPE_BLOB) {
        raise_(PyExc_TypeError, "DEV_PIPE_BLOB not supported!");
    } else {
        using TangoArrayType = typename TANGO_const2type(tangoArrayTypeConst);

        // Destruction will be handled by CORBA, not by Tango.
        TangoArrayType *value = fast_convert2array<tangoArrayTypeConst>(py_value);
        if constexpr(std::is_same_v<T, Tango::DeviceData>) {
            self << value;
        } else {
            self <<= value;
        }
    }
}
