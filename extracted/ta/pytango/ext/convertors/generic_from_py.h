/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "common_header.h"
#include "types_structs_macros.h"
#include "auxiliary_macros.h"
#include "pyutils.h"

/// @bug Not a bug per se, but you should keep in mind: It returns a new
/// string, so if you pass it to Tango with a release flag there will be
/// no problems, but if you have to use it yourself then you must remember
/// to delete[] it!
Tango::DevString PyString_AsCorbaString(PyObject *obj_ptr);

/**
 * Translation between python object to Tango data type.
 *
 * Example:
 * Tango::DevLong tg_value;
 * try
 * {
 *     python_scalar_to_cpp<Tango::DEV_LONG>::convert(py_obj, tg_value);
 * }
 * catch(py::error_already_set &eas)
 * {
 *     handle_error(eas);
 * }
 */

// default realization for unsupported data types
template <int tangoTypeConst>
struct python_scalar_to_cpp {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);

    static void convert([[maybe_unused]] const py::object &val, [[maybe_unused]] TangoScalarType &tg) {
        Tango::Except::throw_exception(
            "PyDs_WrongPythonDataTypeForAttribute", "Unsupported attribute type translation", "python_scalar_to_cpp::convert()");
    }
};

#define DEFINE_FROM_PY_NOT_NUMERIC(tangoTypeConst, FN)                           \
    template <>                                                                  \
    struct python_scalar_to_cpp<tangoTypeConst> {                                \
        typedef TANGO_const2type(tangoTypeConst) TangoScalarType;                \
                                                                                 \
        static inline void convert(const py::object &val, TangoScalarType &tg) { \
            tg = static_cast<TangoScalarType>(FN(val.ptr()));                    \
            if(PyErr_Occurred())                                                 \
                throw py::error_already_set();                                   \
        }                                                                        \
    };

DEFINE_FROM_PY_NOT_NUMERIC(Tango::DEV_STATE, PyLong_AsLong)
DEFINE_FROM_PY_NOT_NUMERIC(Tango::DEV_STRING, PyString_AsCorbaString)
DEFINE_FROM_PY_NOT_NUMERIC(Tango::DEV_ENUM, PyLong_AsUnsignedLong)

template <>
struct python_scalar_to_cpp<Tango::DEV_ENCODED> {
    static void convert(const py::object &py_value, Tango::DevEncoded &tg) {
        if(!py::isinstance<py::sequence>(py_value) || py::len(py_value) != 2) {
            throw py::type_error("Expected a sequence of length 2 for DEV_ENCODED");
        }

        py::object encoded_format_str = py_value.attr("__getitem__")(0);
        py::object encoded_data_str = py_value.attr("__getitem__")(1);

        // Extract encoded_format
        char *encoded_format = from_python_str_to_cpp_char(encoded_format_str);
        tg.encoded_format = CORBA::string_dup(encoded_format);

        Py_ssize_t size;
        unsigned char *encoded_data = reinterpret_cast<unsigned char *>(from_python_str_to_cpp_char(encoded_data_str, &size, true));
        if(size < 0) {
            throw std::runtime_error("Size cannot be negative");
        }
        tg.encoded_data.length(static_cast<_CORBA_ULong>(size));
        memcpy(tg.encoded_data.get_buffer(), encoded_data, static_cast<size_t>(size));

        delete[] encoded_format;
        delete[] encoded_data;
    }
};

#undef max
#undef min

inline std::string type_missmatch_error(const int tangoTypeConst) {
    std::string type_str;
    if(tangoTypeConst == Tango::DEV_BOOLEAN) {
        type_str = "bool";
    } else if(tangoTypeConst == Tango::DEV_FLOAT || tangoTypeConst == Tango::DEV_DOUBLE) {
        type_str = "numeric";
    } else {
        type_str = "integer";
    };
    std::string err_msg = "Expecting a " + type_str + " type, but it is not. "
                                                      "If you use a numpy type instead of python core types,"
                                                      " then it must exactly match (ex: numpy.int32 for PyTango.DevLong)";
    return err_msg;
}

// Due to python does not provide conversion from python integers
// to all the data types accepted by tango we must check the ranges manually.
#define DEFINE_FROM_PY_NUMERIC(tangoTypeConst, cpy_type, FN)                                                        \
    template <>                                                                                                     \
    struct python_scalar_to_cpp<tangoTypeConst> {                                                                   \
        typedef TANGO_const2type(tangoTypeConst) TangoScalarType;                                                   \
        typedef std::numeric_limits<TangoScalarType> TangoScalarTypeLimits;                                         \
                                                                                                                    \
        static inline void convert(const py::object &val, TangoScalarType &tg) {                                    \
            DISABLE_WARNING("-Wold-style-cast")                                                                     \
            PyObject *py_val = val.ptr();                                                                           \
            cpy_type cpy_value = FN(py_val);                                                                        \
            if(PyErr_Occurred()) {                                                                                  \
                PyErr_Clear();                                                                                      \
                if(PyArray_CheckScalar(py_val) &&                                                                   \
                   (PyArray_DescrFromScalar(py_val) == PyArray_DescrFromType(TANGO_const2numpy(tangoTypeConst)))) { \
                    PyArray_ScalarAsCtype(py_val, reinterpret_cast<void *>(&tg));                                   \
                    return;                                                                                         \
                } else {                                                                                            \
                    PyErr_SetString(PyExc_TypeError, type_missmatch_error(tangoTypeConst).c_str());                 \
                    throw py::error_already_set();                                                                  \
                }                                                                                                   \
            }                                                                                                       \
            if(TangoScalarTypeLimits::is_integer) {                                                                 \
                if(cpy_value > static_cast<cpy_type>(TangoScalarTypeLimits::max())) {                               \
                    PyErr_SetString(PyExc_OverflowError, "Value is too large.");                                    \
                    throw py::error_already_set();                                                                  \
                }                                                                                                   \
                if(cpy_value < static_cast<cpy_type>(TangoScalarTypeLimits::min())) {                               \
                    PyErr_SetString(PyExc_OverflowError, "Value is too small.");                                    \
                    throw py::error_already_set();                                                                  \
                }                                                                                                   \
            }                                                                                                       \
            tg = static_cast<TangoScalarType>(cpy_value);                                                           \
            RESTORE_WARNING                                                                                         \
        }                                                                                                           \
    };

/* Allow for downcast */
inline unsigned PY_LONG_LONG PyLong_AsUnsignedLongLong_2(PyObject *pylong) {
    unsigned PY_LONG_LONG result = PyLong_AsUnsignedLongLong(pylong);
    if(PyErr_Occurred() != nullptr) {
        PyErr_Clear();
        result = PyLong_AsUnsignedLong(pylong);
    }
    return result;
}

DEFINE_FROM_PY_NUMERIC(Tango::DEV_BOOLEAN, long, PyLong_AsLong)
DEFINE_FROM_PY_NUMERIC(Tango::DEV_UCHAR, unsigned long, PyLong_AsUnsignedLong)
DEFINE_FROM_PY_NUMERIC(Tango::DEV_SHORT, long, PyLong_AsLong)
DEFINE_FROM_PY_NUMERIC(Tango::DEV_USHORT, unsigned long, PyLong_AsUnsignedLong)
DEFINE_FROM_PY_NUMERIC(Tango::DEV_LONG, long, PyLong_AsLong)
DEFINE_FROM_PY_NUMERIC(Tango::DEV_ULONG, unsigned long, PyLong_AsUnsignedLong)
DEFINE_FROM_PY_NUMERIC(Tango::DEV_LONG64, Tango::DevLong64, PyLong_AsLongLong)
DEFINE_FROM_PY_NUMERIC(Tango::DEV_ULONG64, Tango::DevULong64, PyLong_AsUnsignedLongLong_2)
DEFINE_FROM_PY_NUMERIC(Tango::DEV_FLOAT, double, PyFloat_AsDouble)
DEFINE_FROM_PY_NUMERIC(Tango::DEV_DOUBLE, double, PyFloat_AsDouble)

template <int tangoArrayTypeConst>
struct array_element_from_py : public python_scalar_to_cpp<TANGO_const2scalarconst(tangoArrayTypeConst)> {
};

template <>
struct array_element_from_py<Tango::DEVVAR_CHARARRAY> {
    static const int tangoArrayTypeConst = Tango::DEVVAR_CHARARRAY;

    typedef TANGO_const2scalartype(tangoArrayTypeConst) TangoScalarType;
    typedef std::numeric_limits<TangoScalarType> TangoScalarTypeLimits;

    static void convert(const py::object &val, TangoScalarType &tg) {
        DISABLE_WARNING("-Wold-style-cast")
        PyObject *py_val = val.ptr();
        long cpy_value = PyLong_AsLong(py_val);
        if(PyErr_Occurred() != nullptr) {
            PyErr_Clear();
            if(PyArray_CheckScalar(py_val) &&
               (PyArray_DescrFromScalar(py_val) == PyArray_DescrFromType(TANGO_const2scalarnumpy(tangoArrayTypeConst)))) {
                PyArray_ScalarAsCtype(py_val, reinterpret_cast<void *>(&tg));
                return;
            } else {
                std::string err_msg = "Expecting a char type but it is not. "
                                      "If you use a numpy type instead of"
                                      "python core types, then it must exactly match";
                PyErr_SetString(PyExc_TypeError, err_msg.c_str());
                throw py::error_already_set();
            }
        }
        tg = static_cast<TangoScalarType>(cpy_value);
        RESTORE_WARNING
    }
};

/**
 * Converter from python sequence to a Tango CORBA sequence
 *
 * @param[in] py_value python sequence object
 * @param[out] result CORBA sequence to be filled
 */
template <typename TangoElementType>
void python_seq_to_tango(const py::object &py_value, _CORBA_Sequence<TangoElementType> &result) {
    size_t len = py::len(py_value);
    static_assert(sizeof(Py_ssize_t) == sizeof(size_t)); // see also https://github.com/python/cpython/blob/69426fcee7fcecbe34be66d2c5b58b6d0ffe2809/Include/pyport.h#L137C51-L138C18
    if(len > std::numeric_limits<CORBA::ULong>::max() || len > static_cast<size_t>(PY_SSIZE_T_MAX)) {
        throw std::overflow_error("py::len(py_value) is too large for CORBA::ULong/Py_ssize_t");
    }

    result.length(static_cast<CORBA::ULong>(len));
    for(size_t i = 0; i < len; ++i) {
        TangoElementType ch = py::cast<TangoElementType>(py_value.attr("__getitem__")(i));
        result[static_cast<CORBA::ULong>(i)] = ch;
    }
}

void python_seq_to_tango(const py::object &py_value, StdStringVector &result);
void python_seq_to_tango(const py::object &py_value, Tango::DevVarCharArray &result);
void python_seq_to_tango(const py::object &py_value, Tango::DevVarStringArray &result);
// void python_seq_to_tango(const py::object &py_value, Tango::DevErrorList &result);
void python_seq_to_tango(const py::object &py_value, Tango::DevVarDoubleStringArray &result);
void python_seq_to_tango(const py::object &py_value, Tango::DevVarLongStringArray &result);

// helper method to extract numeric and string arrays from py::object
inline void __long_double_string_array_helper(const py::object &py_value,
                                              DevVarNumericStringArray type,
                                              std::string f_name,
                                              py::object &py_numeric,
                                              py::object &py_string) {
    std::string err_type, err_desription;
    switch(type) {
    case DevVarNumericStringArray::LONG_STRING: {
        err_type = "PyDs_WrongPythonDataTypeForLongStringArray";
        err_desription = "Converter from python object to DevVarLongStringArray "
                         "needs a python sequence<sequence<int>, sequence<str>>";
        break;
    }
    case DevVarNumericStringArray::DOUBLE_STRING: {
        err_type = "PyDs_WrongPythonDataTypeForDoubleStringArray";
        err_desription = "Converter from python object to DevVarDoubelStringArray "
                         "needs a python sequence<sequence<float>, sequence<str>>";
        break;
    }
    }

    if(py::isinstance<py::str>(py_value) || !py::isinstance<py::sequence>(py_value)) {
        Tango::Except::throw_exception(err_type, err_desription, f_name);
    }

    size_t size = py::len(py_value);

    if(size != 2) {
        Tango::Except::throw_exception(err_type, err_desription, f_name);
    }

    py_numeric = py_value.attr("__getitem__")(0);
    py_string = py_value.attr("__getitem__")(1);
}
