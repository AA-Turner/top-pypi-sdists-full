/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "common_header.h"
#include "types_structs_macros.h"
#include "pyutils.h"
#include "convertors/type_casters.h"
#include "convertors/generic_to_py.h"

template <typename T, int tangoTypeConst>
inline void scalar_cpp_data_to_python(T &self,
                                      py::object &py_value) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);

    TangoScalarType data;

    // to make live of Tango developer "easier", cppTango uses different operators to extract value in different object
    // Don't let your guard down, it`s TANGO!!!
    bool res;
    if constexpr(std::is_same_v<T, Tango::DeviceData>) {
        res = self >> data;
    } else {
        res = self >>= data;
    }

    if(!res) {
        throw_bad_type(Tango::CmdArgTypeName[tangoTypeConst], TANGO_EXCEPTION_ORIGIN);
    }

    py_value = cpp_to_python_scalar<tangoTypeConst>::convert(data);
}

template <>
inline void scalar_cpp_data_to_python<CORBA::Any, Tango::DEV_STRING>(CORBA::Any &self,
                                                                     py::object &py_value) {
    Tango::ConstDevString data;

    if(!(self >>= data)) {
        throw_bad_type(Tango::CmdArgTypeName[Tango::DEV_STRING], TANGO_EXCEPTION_ORIGIN);
    }

    py_value = cpp_to_python_scalar<Tango::DEV_STRING>::convert(data);
}

template <>
inline void scalar_cpp_data_to_python<Tango::DeviceData, Tango::DEV_STRING>(Tango::DeviceData &self,
                                                                            py::object &py_value) {
    std::string data;
    if(!(self >> data)) {
        throw_bad_type(Tango::CmdArgTypeName[Tango::DEV_STRING], TANGO_EXCEPTION_ORIGIN);
    }
    py_value = from_cpp_str_to_pybind11_str(data);
}

template <>
inline void scalar_cpp_data_to_python<CORBA::Any, Tango::DEV_ENCODED>(CORBA::Any &any,
                                                                      py::object &py_value) {
    Tango::DevEncoded *data;

    if(!(any >>= data)) {
        throw_bad_type(Tango::CmdArgTypeName[Tango::DEV_ENCODED], TANGO_EXCEPTION_ORIGIN);
    }

    py_value = cpp_to_python_scalar<Tango::DEV_ENCODED>::convert(*data);
}

template <>
inline void scalar_cpp_data_to_python<CORBA::Any, Tango::DEV_VOID>([[maybe_unused]] CORBA::Any &self,
                                                                   [[maybe_unused]] py::object &py_value) {
    py_value = py::none();
}

template <>
inline void scalar_cpp_data_to_python<Tango::DeviceData, Tango::DEV_VOID>([[maybe_unused]] Tango::DeviceData &self,
                                                                          [[maybe_unused]] py::object &py_value) {
    py_value = py::none();
}

template <>
inline void scalar_cpp_data_to_python<CORBA::Any, Tango::DEV_PIPE_BLOB>([[maybe_unused]] CORBA::Any &self,
                                                                        [[maybe_unused]] py::object &py_value) {
    assert(false);
}

template <>
inline void scalar_cpp_data_to_python<Tango::DeviceData, Tango::DEV_PIPE_BLOB>([[maybe_unused]] Tango::DeviceData &self,
                                                                               [[maybe_unused]] py::object &py_value) {
    assert(false);
}

template <int tangoArrayTypeConst>
py::object cpp_to_python_buffer_no_copy(const typename TANGO_const2type(tangoArrayTypeConst) * tg_array,
                                        py::object parent) {
    using T = typename TANGO_const2scalartype(tangoArrayTypeConst);

    if(tg_array == nullptr) {
        // Return an empty array
        return py::array_t<T>({0});
    }

    // Get the data pointer and length
    const T *data_ptr = tg_array->get_buffer();
    std::size_t length = static_cast<std::size_t>(tg_array->length());

    // Create a NumPy array that wraps the existing data
    py::array array(
        pybind11::dtype::of<T>(), // Data type
        {length},                 // Shape
        {sizeof(T)},              // Strides
        data_ptr,                 // Data pointer
        parent                    // Base object to manage memory
    );

    return array;
}

template <>
inline py::object cpp_to_python_buffer_no_copy<Tango::DEVVAR_STRINGARRAY>([[maybe_unused]] const Tango::DevVarStringArray *tg_array,
                                                                          [[maybe_unused]] py::object parent) {
    return to_py_list(tg_array);
}

template <>
inline py::object cpp_to_python_buffer_no_copy<Tango::DEVVAR_STATEARRAY>([[maybe_unused]] const Tango::DevVarStateArray *tg_array,
                                                                         [[maybe_unused]] py::object parent) {
    return to_py_list(tg_array);
}

template <>
inline py::object cpp_to_python_buffer_no_copy<Tango::DEVVAR_LONGSTRINGARRAY>(const Tango::DevVarLongStringArray *tg_array,
                                                                              py::object parent) {
    py::list result;

    result.append(cpp_to_python_buffer_no_copy<Tango::DEVVAR_LONGARRAY>(&tg_array->lvalue, parent));
    result.append(cpp_to_python_buffer_no_copy<Tango::DEVVAR_STRINGARRAY>(&tg_array->svalue, parent));

    return result;
}

template <>
inline py::object cpp_to_python_buffer_no_copy<Tango::DEVVAR_DOUBLESTRINGARRAY>(const Tango::DevVarDoubleStringArray *tg_array,
                                                                                py::object parent) {
    py::list result;

    result.append(cpp_to_python_buffer_no_copy<Tango::DEVVAR_DOUBLEARRAY>(&tg_array->dvalue, parent));
    result.append(cpp_to_python_buffer_no_copy<Tango::DEVVAR_STRINGARRAY>(&tg_array->svalue, parent));

    return result;
}

template <int tangoTypeConst>
inline void array_cpp_data_to_python(CORBA::Any &self,
                                     py::object &py_result) {
    using TangoArrayType = typename TANGO_const2type(tangoTypeConst);

    TangoArrayType *data;

    if(!(self >>= data)) {
        throw_bad_type(Tango::CmdArgTypeName[tangoTypeConst], TANGO_EXCEPTION_ORIGIN);
    }

    // But I cannot manage memory inside our 'any' object, because it is
    // const and handles it's memory itself. So I need a copy before
    // creating the object.
    data = new TangoArrayType(*data);

    // For numpy we need a 'guard' object that handles the memory used
    // by the numpy object (releases it).

    py::capsule guard(data, dev_var_command_array_deleter<TangoArrayType>);

    py_result = cpp_to_python_buffer_no_copy<tangoTypeConst>(data, guard);
}

template <int tangoTypeConst>
inline void array_cpp_data_to_python(Tango::DeviceData &self,
                                     py::object &py_self,
                                     py::object &py_result,
                                     PyTango::ExtractAs extract_as) {
    using TangoArrayType = typename TANGO_const2type(tangoTypeConst);

    const TangoArrayType *data;

    if((self >> data) == false) {
        throw_bad_type(Tango::CmdArgTypeName[tangoTypeConst], TANGO_EXCEPTION_ORIGIN);
    }

    switch(extract_as) {
    default:
    case PyTango::ExtractAsNumpy:
        py_result = cpp_to_python_buffer_no_copy<tangoTypeConst>(data, py_self);
        break;
    case PyTango::ExtractAsList:
    case PyTango::ExtractAsPyTango3:
        py_result = to_py_list(data);
        break;
    case PyTango::ExtractAsTuple:
        py_result = to_py_tuple(data);
        break;
    case PyTango::ExtractAsString: /// @todo
    case PyTango::ExtractAsNothing:
        py_result = py::none();
    }
}

template <>
inline void array_cpp_data_to_python<Tango::DEV_PIPE_BLOB>([[maybe_unused]] CORBA::Any &any,
                                                           [[maybe_unused]] py::object &py_result) {
    assert(false);
}

template <>
inline void array_cpp_data_to_python<Tango::DEVVAR_STATEARRAY>([[maybe_unused]] Tango::DeviceData &self,
                                                               [[maybe_unused]] py::object &py_self,
                                                               [[maybe_unused]] py::object &py_result,
                                                               [[maybe_unused]] PyTango::ExtractAs extract_as) {
    assert(false);
}
