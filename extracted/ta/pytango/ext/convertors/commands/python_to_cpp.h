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
inline void scalar_python_data_to_cpp(T &self,
                                      py::object &py_value) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);
    TangoScalarType value;
    python_scalar_to_cpp<tangoTypeConst>::convert(py_value, value);

    // to make live of Tango developer "easier", cppTango uses different operators to insert value in different object
    // Don't let your guard down, it`s TANGO!!!
    if constexpr(std::is_same_v<T, Tango::DeviceData>) {
        self << value;
    } else {
        if constexpr(tangoTypeConst == Tango::DEV_BOOLEAN) {
            self <<= CORBA::Any::from_boolean(value);
        } else {
            self <<= value;
        }
    }

    if constexpr(tangoTypeConst == Tango::DEV_STRING) {
        delete[] value;
    }
}

template <>
inline void scalar_python_data_to_cpp<Tango::DeviceData, Tango::DEV_VOID>([[maybe_unused]] Tango::DeviceData &self,
                                                                          [[maybe_unused]] py::object &py_value) {
    raise_(PyExc_TypeError, "Trying to insert a value in a DEV_VOID DeviceData!");
}

template <>
inline void scalar_python_data_to_cpp<CORBA::Any, Tango::DEV_VOID>([[maybe_unused]] CORBA::Any &self,
                                                                   [[maybe_unused]] py::object &py_value) {
}

template <>
inline void scalar_python_data_to_cpp<Tango::DeviceData, Tango::DEV_PIPE_BLOB>([[maybe_unused]] Tango::DeviceData &self,
                                                                               [[maybe_unused]] py::object &py_value) {
    raise_(PyExc_TypeError, "DEV_PIPE_BLOB not supported!");
}

template <>
inline void scalar_python_data_to_cpp<CORBA::Any, Tango::DEV_PIPE_BLOB>([[maybe_unused]] CORBA::Any &self,
                                                                        [[maybe_unused]] py::object &py_value) {
    raise_(PyExc_TypeError, "DEV_PIPE_BLOB not supported!");
}

template <typename T, int tangoArrayTypeConst>
inline void array_python_data_to_cpp(T &self,
                                     py::object &py_value) {
    using TangoArrayType = typename TANGO_const2type(tangoArrayTypeConst);

    // Destruction will be handled by CORBA, not by Tango.
    TangoArrayType *value = fast_convert2array<tangoArrayTypeConst>(py_value);
    if constexpr(std::is_same_v<T, Tango::DeviceData>) {
        self << value;
    } else {
        self <<= value;
    }
}

template <>
inline void array_python_data_to_cpp<Tango::DeviceData, Tango::DEV_PIPE_BLOB>([[maybe_unused]] Tango::DeviceData &self,
                                                                              [[maybe_unused]] py::object &py_value) {
    raise_(PyExc_TypeError, "DEV_PIPE_BLOB not supported!");
}

template <>
inline void array_python_data_to_cpp<CORBA::Any, Tango::DEV_PIPE_BLOB>([[maybe_unused]] CORBA::Any &self,
                                                                       [[maybe_unused]] py::object &py_value) {
    raise_(PyExc_TypeError, "DEV_PIPE_BLOB not supported!");
}
