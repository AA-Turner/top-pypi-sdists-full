/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "common_header.h"
#include "types_structs_macros.h"
#include "pyutils.h"

template <typename ContainerType>
struct cpp_to_python_list {
    static py::object convert(const ContainerType &src) {
        py::list result;
        for(_CORBA_ULong i = 0; i < src.length(); ++i) {
            result.append(py::cast(src[i]));
        }
        return result;
    }
};

template <>
struct cpp_to_python_list<StdStringVector> {
    static py::object convert(const StdStringVector &src) {
        py::list result;
        for(size_t i = 0; i < src.size(); ++i) {
            result.append(from_cpp_str_to_pybind11_str(src[i]));
        }
        return result;
    }
};

template <>
struct cpp_to_python_list<Tango::DevVarStringArray> {
    static py::object convert(const Tango::DevVarStringArray &src) {
        py::list result;
        for(_CORBA_ULong i = 0; i < src.length(); ++i) {
            result.append(from_cpp_char_to_pybind11_str(src[i].in()));
        }
        return result;
    }
};

template <>
struct cpp_to_python_list<Tango::DevVarLongStringArray> {
    static py::object convert(const Tango::DevVarLongStringArray &src) {
        py::list lt, st, ret;

        for(_CORBA_ULong i = 0; i < src.lvalue.length(); ++i) {
            lt.append(py::cast(src.lvalue[i]));
        }

        for(_CORBA_ULong i = 0; i < src.svalue.length(); ++i) {
            st.append(from_cpp_char_to_pybind11_str(src.svalue[i].in()));
        }

        ret.append(lt);
        ret.append(st);

        return ret;
    }
};

template <>
struct cpp_to_python_list<Tango::DevVarDoubleStringArray> {
    static py::object convert(const Tango::DevVarDoubleStringArray &src) {
        py::list lt, st, ret;

        for(_CORBA_ULong i = 0; i < src.dvalue.length(); ++i) {
            lt.append(py::cast(src.dvalue[i]));
        }

        for(_CORBA_ULong i = 0; i < src.svalue.length(); ++i) {
            st.append(from_cpp_char_to_pybind11_str(src.svalue[i].in()));
        }

        ret.append(lt);
        ret.append(st);

        return ret;
    }
};

template <class T>
inline py::object to_py_list(const T *seq) {
    return cpp_to_python_list<T>::convert(*seq);
}

template <class T>
inline py::object to_py_tuple(const T *seq) {
    py::list py_list = cpp_to_python_list<T>::convert(*seq);

    std::size_t size = py::len(py_list);

    py::tuple py_tuple(size);

    for(std::size_t i = 0; i < size; ++i) {
        py_tuple[i] = py_list[i];
    }
    return py_tuple;
}

/*  Unfortunately, I did not find a way to simply do py::cast<Tango::DevString>
 *  It fails with "value is local to type caster"
 *  All my attempts to reload this caster failed.
 *  If one manage to do it - this helper structure can be removed if favour of direct py::cast
 */

template <int tangoTypeConst>
struct cpp_to_python_scalar {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);

    static py::object convert(const TangoScalarType &value) {
        return py::cast(value);
    }
};

template <>
struct cpp_to_python_scalar<Tango::DEV_STRING> {
    static py::object convert(const Tango::DevString &value) {
        return from_cpp_char_to_pybind11_str(value);
    }

    static py::object convert(const Tango::ConstDevString &value) {
        return from_cpp_char_to_pybind11_str(value);
    }
};

template <>
struct cpp_to_python_scalar<Tango::DEV_ENCODED> {
    static py::object convert(const Tango::DevEncoded &value, PyTango::ExtractAs extract_as = PyTango::ExtractAsNumpy) {
        py::object encoded_format = from_cpp_char_to_pybind11_str(value.encoded_format);
        py::object py_value;

        switch(extract_as) {
        default:
        case PyTango::ExtractAsNumpy:
        case PyTango::ExtractAsTuple:
        case PyTango::ExtractAsList:
        case PyTango::ExtractAsBytes: {
            py::bytes encoded_data(reinterpret_cast<const char *>(value.encoded_data.get_buffer()),
                                   value.encoded_data.length());
            py_value = py::make_tuple(encoded_format, encoded_data);
            break;
        }
        case PyTango::ExtractAsByteArray: {
            py::bytearray encoded_data(reinterpret_cast<const char *>(value.encoded_data.get_buffer()),
                                       value.encoded_data.length());
            py_value = py::make_tuple(encoded_format, encoded_data);
            break;
        }
        case PyTango::ExtractAsString: {
            py::str encoded_data(reinterpret_cast<const char *>(value.encoded_data.get_buffer()),
                                 value.encoded_data.length());
            py_value = py::make_tuple(encoded_format, encoded_data);
            break;
        }
        }
        return py_value;
    }
};
