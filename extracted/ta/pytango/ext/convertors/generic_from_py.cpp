/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"

#include "convertors/generic_from_py.h"
#include "pyutils.h"

void assign_double_attr_prop(py::object &py_obj,
                             const std::string &attr_name,
                             Tango::DoubleAttrProp<Tango::DevDouble> &attr_prop) {
    py::object attr_value = py_obj.attr(attr_name.c_str());

    try {
        attr_prop = attr_value.cast<std::string>();
    } catch(const py::cast_error &) {
        try {
            if(py::isinstance<py::sequence>(attr_value)) {
                std::vector<Tango::DevDouble> vec;
                for(auto item : attr_value.cast<py::sequence>()) {
                    vec.push_back(py::cast<Tango::DevDouble>(item));
                }
                attr_prop = vec;
            } else {
                attr_prop = attr_value.cast<Tango::DevDouble>();
            }
        } catch(const py::cast_error &) {
            throw std::runtime_error("Failed to cast attribute: " + attr_name);
        }
    }
}

/// @bug Not a bug per se, but you should keep in mind: It returns a new
/// string, so if you pass it to Tango with a release flag there will be
/// no problems, but if you have to use it yourself then you must remember
/// to delete[] it!
Tango::DevString PyString_AsCorbaString(PyObject *obj_ptr) {
    return from_python_str_to_cpp_char(obj_ptr);
}

void python_seq_to_tango(const py::object &py_value, Tango::DevVarCharArray &result) {
    PyObject *py_value_ptr = py_value.ptr();
    if(PySequence_Check(py_value_ptr) == 0) {
        raise_(PyExc_TypeError, param_must_be_seq);
    }

    CORBA::ULong size = static_cast<CORBA::ULong>(py::len(py_value));
    result.length(size);

    if(PyBytes_Check(py_value_ptr)) {
        unsigned char *uch = reinterpret_cast<unsigned char *>(PyBytes_AS_STRING(py_value_ptr));
        for(CORBA::ULong i = 0; i < size; ++i) {
            result[i] = uch[i];
        }
    } else {
        for(CORBA::ULong i = 0; i < size; ++i) {
            py::object item = py_value.attr("__getitem__")(i);
            // pybind11 does not allow direct casting to char*
            py::buffer_info info = py::cast<py::buffer>(item).request();
            unsigned char *uch = static_cast<unsigned char *>(info.ptr);
            result[i] = uch[0];
        }
    }
}

void python_seq_to_tango(const py::object &py_value, StdStringVector &result) {
    result.reserve(py::len(py_value));

    for(auto item : py_value) {
        // Step 1: Ensure the item is a Python string
        py::str py_string = item.cast<py::str>();

        // Step 2: Encode the string to Latin1 bytes
        // This will raise a UnicodeEncodeError if characters are outside the Latin1 range
        py::bytes py_bytes = py_string.attr("encode")("latin1");

        // Step 3: Convert the bytes to a std::string
        std::string cpp_string = py::cast<std::string>(py_bytes);

        result.emplace_back(std::move(cpp_string));
    }
}

void python_seq_to_tango(const py::object &py_value, Tango::DevVarStringArray &result) {
    CORBA::ULong size = static_cast<CORBA::ULong>(py::len(py_value));
    result.length(size);
    for(CORBA::ULong i = 0; i < size; ++i) {
        char *c_str = from_python_str_to_cpp_char(py_value.attr("__getitem__")(i));
        result[i] = CORBA::string_dup(c_str);
        delete[] c_str;
    }
}

void python_seq_to_tango(const py::object &py_value, Tango::DevVarDoubleStringArray &result) {
    py::object py_double, py_str;

    __long_double_string_array_helper(py_value,
                                      DevVarNumericStringArray::DOUBLE_STRING,
                                      "python_seq_to_tango()",
                                      py_double,
                                      py_str);

    python_seq_to_tango(py_double, result.dvalue);
    python_seq_to_tango(py_str, result.svalue);
}

void python_seq_to_tango(const py::object &py_value, Tango::DevVarLongStringArray &result) {
    py::object py_long, py_str;

    __long_double_string_array_helper(py_value,
                                      DevVarNumericStringArray::LONG_STRING,
                                      "python_seq_to_tango()",
                                      py_long,
                                      py_str);

    python_seq_to_tango(py_long, result.lvalue);
    python_seq_to_tango(py_str, result.svalue);
}
