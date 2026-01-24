/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "pyutils.h"

py::object from_cpp_str_to_pybind11_str(const std::string &in,
                                        const char *encoding /*=NULL defaults to latin-1 */,
                                        const char *errors /*="strict" */) {
    return from_cpp_char_to_pybind11_str(in.c_str(), static_cast<Py_ssize_t>(in.size()), encoding, errors);
}

py::object from_cpp_char_to_pybind11_str(const char *in,
                                         Py_ssize_t size /* =-1 */,
                                         const char *encoding /*=NULL defaults to latin-1 */,
                                         const char *errors /*="strict" */) {
    if(size < 0) {
        size = static_cast<Py_ssize_t>(strlen(in));
    }
    if(encoding == nullptr) {
        return py::reinterpret_steal<py::object>(PyUnicode_DecodeLatin1(in, size, errors));
    } else {
        return py::reinterpret_steal<py::object>(PyUnicode_Decode(in, size, encoding, errors));
    }
}

char *__copy_bytes_to_char(PyObject *in, Py_ssize_t *size) {
    Py_buffer view;

    if(PyObject_GetBuffer(in, &view, PyBUF_FULL_RO) < 0) {
        raise_(PyExc_TypeError, "Can't translate python object to C char* - PyObject_GetBuffer failed");
    }

    Py_ssize_t view_len = view.len;

    char *out = new char[static_cast<size_t>(view_len + 1)];
    out[view_len] = '\0';
    memcpy(out, static_cast<char *>(view.buf), static_cast<size_t>(view_len));

    PyBuffer_Release(&view);

    if(size != nullptr) {
        *size = view_len;
    }

    return out;
}

// The result is a newly allocated buffer. It is the responsibility
// of the caller to manage the memory returned by this function
char *from_python_str_to_cpp_char(const py::object &in, Py_ssize_t *size_out, const bool utf_encoding) {
    return from_python_str_to_cpp_char(in.ptr(), size_out, utf_encoding);
}

// The result is a newly allocated buffer. It is the responsibility
// of the caller to manage the memory returned by this function
char *from_python_str_to_cpp_char(PyObject *in, Py_ssize_t *size_out, const bool utf_encoding) {
    char *out = nullptr;
    if(PyUnicode_Check(in)) {
        PyObject *bytes_in;
        if(utf_encoding) {
            bytes_in = PyUnicode_AsUTF8String(in);
        } else {
            bytes_in = EncodeAsLatin1(in);
        }
        out = __copy_bytes_to_char(bytes_in, size_out);
        Py_DECREF(bytes_in);
    } else if(PyBytes_Check(in) || PyByteArray_Check(in)) {
        out = __copy_bytes_to_char(in, size_out);
    } else {
        raise_(PyExc_TypeError, "can't translate python object to C char*");
    }
    return out;
}

void throw_bad_type(const char *type, const char *source) {
    TangoSys_OMemStream description;
    description << "Incompatible argument type, expected type is : Tango::" << type << std::ends;

    TangoSys_OMemStream origin;
    origin << source << std::ends;

    Tango::Except::throw_exception("API_IncompatibleCmdArgumentType", description.str(), origin.str());
}

// The out_array will be updated with a pointer to existing memory (e.g., Python's internal memory for
// a byte array). The caller gets a "view" of the memory and must not modify the memory.
void view_pybytes_as_char_array(const py::object &py_value, Tango::DevVarCharArray &out_array) {
    CORBA::ULong nb;
    PyObject *data_ptr = py_value.ptr();

    if(PyUnicode_Check(data_ptr)) {
        Py_ssize_t size;
        CORBA::Octet *encoded_data = reinterpret_cast<CORBA::Octet *>(const_cast<char *>( // NOLINT(readability-redundant-casting)
            PyUnicode_AsUTF8AndSize(data_ptr, &size)));
        nb = static_cast<CORBA::ULong>(size);
        out_array.replace(nb, nb, encoded_data, false);
    }

    else if(PyBytes_Check(data_ptr)) {
        nb = static_cast<CORBA::ULong>(py::len(py_value));
        CORBA::Octet *encoded_data = reinterpret_cast<CORBA::Octet *>(const_cast<char *>( // NOLINT(readability-redundant-casting)
            PyBytes_AsString(data_ptr)));
        out_array.replace(nb, nb, encoded_data, false);
    } else if(PyByteArray_Check(data_ptr)) {
        nb = static_cast<CORBA::ULong>(py::len(py_value));
        CORBA::Octet *encoded_data = reinterpret_cast<CORBA::Octet *>(const_cast<char *>( // NOLINT(readability-redundant-casting)
            PyByteArray_AsString(data_ptr)));
        out_array.replace(nb, nb, encoded_data, false);
    } else {
        throw_bad_type(Tango::CmdArgTypeName[Tango::DEV_ENCODED], TANGO_EXCEPTION_ORIGIN);
    }
}

bool is_method_defined(py::object &obj, const std::string &method_name) {
    bool exists, is_method;
    is_method_defined(obj, method_name, exists, is_method);
    return exists && is_method;
}

void is_method_defined(py::object &obj, const std::string &method_name, bool &exists, bool &is_method) {
    exists = py::hasattr(obj, method_name.c_str());

    if(exists) {
        py::object attr = obj.attr(method_name.c_str());
        is_method = PyCallable_Check(attr.ptr()) == 1;
    } else {
        is_method = false;
    }
}
