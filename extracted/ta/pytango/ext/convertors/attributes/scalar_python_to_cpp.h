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
static inline void scalar_value_from_python_into_cpp(Tango::DeviceAttribute &dev_attr,
                                                     const py::object &py_value) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);

    TangoScalarType value;
    python_scalar_to_cpp<tangoTypeConst>::convert(py_value, value);
    dev_attr << value;
}

template <>
inline void scalar_value_from_python_into_cpp<Tango::DEV_STRING>(Tango::DeviceAttribute &dev_attr,
                                                                 const py::object &py_value) {
    Tango::DevString value = from_python_str_to_cpp_char(py_value);
    dev_attr << value;
    delete[] value;
}

template <>
inline void scalar_value_from_python_into_cpp<Tango::DEV_ENCODED>(Tango::DeviceAttribute &dev_attr,
                                                                  const py::object &py_value) {
    if(py::len(py_value) != 2) {
        raise_(PyExc_TypeError, "Expecting a tuple of strings: encoded_format, encoded_data");
    }

    py::object encoded_format_str = py_value.attr("__getitem__")(0);
    py::object encoded_data_str = py_value.attr("__getitem__")(1);

    char *encoded_format = from_python_str_to_cpp_char(encoded_format_str);

    /* todo second parameter of insert is a reference, and it does not take ownership of the pointer
     * so to be 100% sure, we have to copy data. However, in this case we have to have an option to control release
     * parameter. At the moment (cppTango 9.4.1) it is not realized, so we pass pointer to data and Python's gb destroys
     * object this is a source of bugs.
     *
     * Somehow it works, but no idea why.
     *
     * If it is done, the following code could be simplified to:
     *
     * unsigned char *encoded_data = reinterpret_cast<unsigned char *>(from_python_str_to_cpp_char(encoded_data_str, &size, true));
     * dev_attr.insert(encoded_format, encoded_data, static_cast<unsigned int>(size));
     *
     */

    unsigned int encoded_data_len = static_cast<unsigned int>(py::len(encoded_data_str));
    PyObject *encoded_data_obj = encoded_data_str.ptr();
    unsigned char *encoded_data;

    if(PyUnicode_Check(encoded_data_obj)) {
        Py_ssize_t size;
        encoded_data = reinterpret_cast<unsigned char *>(const_cast<char *>(
            PyUnicode_AsUTF8AndSize(encoded_data_obj, &size)));
        dev_attr.insert(encoded_format, encoded_data, static_cast<unsigned int>(size));
    } else if(PyBytes_Check(encoded_data_obj) || PyByteArray_Check(encoded_data_obj)) {
        Py_buffer view;

        if(PyObject_GetBuffer(encoded_data_obj, &view, PyBUF_FULL_RO) < 0) {
            raise_(PyExc_TypeError, "Cannot convert encoded data");
        }

        encoded_data = reinterpret_cast<unsigned char *>(view.buf);
        dev_attr.insert(encoded_format, encoded_data, encoded_data_len);
        PyBuffer_Release(&view);
    } else {
        raise_(PyExc_TypeError, "Encoded_data can be str, bytes or bytearray");
    }
}
} // namespace PyDeviceAttribute

namespace PyWAttribute {
template <int tangoTypeConst>
inline void scalar_value_from_python_into_cpp(Tango::WAttribute &att,
                                              py::object &value) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);

    TangoScalarType cpp_value;
    python_scalar_to_cpp<tangoTypeConst>::convert(value, cpp_value);
    att.set_write_value(cpp_value);
}

template <>
inline void scalar_value_from_python_into_cpp<Tango::DEV_ENCODED>([[maybe_unused]] Tango::WAttribute &att,
                                                                  [[maybe_unused]] py::object &value) {
    Tango::Except::throw_exception("PyDs_WrongPythonDataTypeForAttribute",
                                   "set_write_value is not supported for DEV_ENCODED attributes.",
                                   "set_write_value()");
}
} // namespace PyWAttribute
