/*
 * Copyright © 2026 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <contrast/assess/intern.h>

PyObject *is_string_interned(PyObject *self, PyObject *value) {
    if (PyUnicode_CHECK_INTERNED(value)) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}
