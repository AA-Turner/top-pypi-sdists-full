/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "common_header.h"
#include "convertors/type_casters.h"
#include "base_types_structures/exception.h"

#define CATCH_PY_EXCEPTION               \
    catch(py::error_already_set & eas) { \
        handle_python_exception(eas);    \
    }

#define GET_DEVICE                  \
    py::gil_scoped_acquire acquire; \
    py::object py_dev = py::cast(dev);

#define GET_PYTHON_METHOD(method_name) \
    py::gil_scoped_acquire gil;        \
    py::function py_method = py::get_override(this, #method_name);

#define CALL_PURE_VOID_METHOD(method_name, ...) \
    GET_PYTHON_METHOD(method_name)              \
    if(py_method) {                             \
        try {                                   \
            py_method(__VA_ARGS__);             \
        }                                       \
        CATCH_PY_EXCEPTION                      \
    };

#define CALL_PURE_RETURN_METHOD(return_type, method_name, ...) \
    GET_PYTHON_METHOD(method_name)                             \
    if(py_method) {                                            \
        try {                                                  \
            return py_method(__VA_ARGS__).cast<return_type>(); \
        }                                                      \
        CATCH_PY_EXCEPTION                                     \
    };                                                         \
    return;

#define CALL_VOID_METHOD(method_name, cpp_class, ...) \
    GET_PYTHON_METHOD(method_name)                    \
    if(py_method) {                                   \
        try {                                         \
            py_method(__VA_ARGS__);                   \
        }                                             \
        CATCH_PY_EXCEPTION                            \
    } else {                                          \
        cpp_class::method_name(__VA_ARGS__);          \
    };

#define CALL_RETURN_METHOD(return_type, method_name, cpp_class, ...) \
    GET_PYTHON_METHOD(method_name)                                   \
    if(py_method) {                                                  \
        try {                                                        \
            return py_method(__VA_ARGS__).cast<return_type>();       \
        }                                                            \
        CATCH_PY_EXCEPTION                                           \
    };                                                               \
    return cpp_class::method_name(__VA_ARGS__);
