/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include <omnithread.h>
#include <bytesobject.h>
#include "common_header.h"
#include "types_structs_macros.h"

inline py::dict create_dict_from_lists(py::list keys, py::list values) {
    // Check that both lists have the same length
    if(keys.size() != values.size()) {
        throw std::runtime_error("Keys and values must have the same length");
    }

    py::dict dict;
    for(std::size_t i = 0; i < keys.size(); ++i) {
        dict[keys[i]] = values[i];
    }

    return dict;
}

inline py::dict create_dict_from_list(py::list values) {
    py::dict dict;
    for(std::size_t i = 0; i < values.size(); ++i) {
        dict[py::int_(values[i])] = values[i];
    }

    return dict;
}

inline void add_names_values_to_native_enum(py::object enum_class) {
    py::dict members = enum_class.attr("__members__");
    py::list keys = members.attr("keys")();
    py::list values = members.attr("values")();
    enum_class.attr("values") = create_dict_from_list(values);
    enum_class.attr("names") = create_dict_from_lists(keys, values);

    enum_class.attr("__str__") = py::cpp_function(
        [](py::object self) {
            return self.attr("name");
        },
        py::is_method(enum_class) // Tell pybind11 this will be a method
    );
}

/// This callback is run to delete Tango::DevVarXArray* objects.
/// It is called by python. The array was associated with an attribute
/// value object that is not being used anymore.
template <int tangoTypeConst>
void dev_var_attribute_array_deleter(void *ptr) {
    delete static_cast<typename TANGO_const2arraytype(tangoTypeConst) *>(ptr);
}

template <typename TangoArrayType>
void dev_var_command_array_deleter(void *ptr) {
    delete static_cast<TangoArrayType *>(ptr);
}

inline void raise_(PyObject *type, const char *message) {
    PyErr_SetString(type, message);
    throw py::error_already_set();
}

inline PyObject *EncodeAsLatin1(PyObject *in) {
    PyObject *bytes_out = PyUnicode_AsLatin1String(in);
    if(bytes_out == nullptr) {
        PyObject *bytes_replaced = PyUnicode_AsEncodedString(in, "latin-1", "replace");
        const char *string_replaced = PyBytes_AsString(bytes_replaced);
        std::string err_msg = "Can't encode ";
        if(string_replaced == nullptr) {
            err_msg += "unknown Unicode string as Latin-1";
        } else {
            err_msg += "'";
            err_msg += string_replaced;
            err_msg += "' Unicode string as Latin-1 (bad chars replaced with ?)";
        }
        Py_XDECREF(bytes_replaced);
        raise_(PyExc_UnicodeError, err_msg.c_str());
    }

    return bytes_out;
}

inline PyObject *PyObject_GetAttrString_(PyObject *o, const std::string &attr_name) {
    const char *attr = attr_name.c_str();
    return PyObject_GetAttrString(o, attr);
}

inline PyObject *PyImport_ImportModule_(const std::string &name) {
    const char *attr = name.c_str();
    return PyImport_ImportModule(attr);
}

py::object from_cpp_str_to_pybind11_str(const std::string &in,
                                        const char *encoding = nullptr, /* defaults to latin-1 */
                                        const char *errors = "strict");

py::object from_cpp_char_to_pybind11_str(const char *in,
                                         Py_ssize_t size = -1,
                                         const char *encoding = nullptr, /* defaults to latin-1 */
                                         const char *errors = "strict");

char *from_python_str_to_cpp_char(PyObject *obj_ptr,
                                  Py_ssize_t *size_out = nullptr,
                                  bool utf_encoding = false /* defaults to latin-1 */);

char *from_python_str_to_cpp_char(const py::object &in,
                                  Py_ssize_t *size_out = nullptr,
                                  bool utf_encoding = false /* defaults to latin-1 */);

void throw_bad_type(const char *type, const char *source);

void view_pybytes_as_char_array(const py::object &py_value, Tango::DevVarCharArray &out_array);

// Delete a pointer for a CppTango class with Python GIL released.
// Typically used by shared_ptr constructors as the function
// to call when the object is deleted.
struct DeleterWithoutGIL {
    template <typename T>
    void operator()(T *ptr) const {
        py::gil_scoped_release no_gil;
        delete ptr;
    }
};

/**
 * Determines if the given method name exists and is callable
 * within the python class
 *
 * @param[in] obj object to search for the method
 * @param[in] method_name the name of the method
 *
 * @return returns true is the method exists or false otherwise
 */
bool is_method_defined(py::object &obj, const std::string &method_name);

/**
 * Determines if the given method name exists and is callable
 * within the python class
 *
 * @param[in] obj object to search for the method
 * @param[in] method_name the name of the method
 * @param[out] exists set to true if the symbol exists or false otherwise
 * @param[out] is_method set to true if the symbol exists and is a method
 *             or false otherwise
 */
void is_method_defined(py::object &obj, const std::string &method_name, bool &exists, bool &is_method);

inline py::list pickle_stdstringvector(const StdStringVector &vector) {
    // Convert extensions to a Python list of strings
    py::list list;
    for(const auto &v : vector) {
        list.append(v);
    }
    return list;
}

inline StdStringVector unpickled_stdstringvector(py::list py_value) {
    // Convert the Python list back to StdStringVector
    StdStringVector vector;
    for(auto item : py_value) {
        vector.push_back(item.cast<std::string>());
    }
    return vector;
}

#define PYTANGO_MOD py::object pytango(py::module_::import("tango"));

#define CALL_METHOD(retType, self, name, ...) elf.attr(name)(__VA_ARGS__).cast<retType>();
