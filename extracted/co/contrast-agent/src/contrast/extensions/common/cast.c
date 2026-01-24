/*
 * Copyright © 2026 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/patches.h>
#include <contrast/assess/propagate.h>
#include <contrast/assess/scope.h>

#define IS_TRACKABLE(X) \
    (PyUnicode_Check((X)) || PyBytes_Check((X)) || PyByteArray_Check((X)))

newfunc unicode_new_orig;
newfunc bytes_new_orig;
initproc bytearray_init_orig;

PyObject *bytes_new_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    PyObject *result = bytes_new_orig(type, args, kwds);

    if (result == NULL)
        return result;

    call_string_propagator("propagate_bytes_cast", NULL, result, args, kwds);

    return result;
}

int bytearray_init_new(PyObject *self, PyObject *args, PyObject *kwds) {
    int result = bytearray_init_orig(self, args, kwds);

    if (result == -1)
        return result;

    /* Here we report self_obj=None and ret=self
       to maintain the illusion of casting */
    call_string_propagator("propagate_bytearray_cast", NULL, self, args, kwds);

    return result;
}

PyObject *unicode_new_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    PyObject *result = unicode_new_orig(type, args, kwds);

    if (result == NULL)
        return result;

    call_string_propagator("propagate_unicode_cast", NULL, result, args, kwds);

    return result;
}

void apply_cast_patches() {
    PyUnicode_Type.tp_vectorcall = NULL;

    unicode_new_orig = (void *)PyUnicode_Type.tp_new;
    PyUnicode_Type.tp_new = (void *)unicode_new_new;

    bytes_new_orig = (void *)PyBytes_Type.tp_new;
    PyBytes_Type.tp_new = (void *)bytes_new_new;

    bytearray_init_orig = (void *)PyByteArray_Type.tp_init;
    PyByteArray_Type.tp_init = (void *)bytearray_init_new;
}

void reverse_cast_patches() {
    PyUnicode_Type.tp_new = (void *)unicode_new_orig;
    PyBytes_Type.tp_new = (void *)bytes_new_orig;
    PyByteArray_Type.tp_init = (void *)bytearray_init_orig;
}
