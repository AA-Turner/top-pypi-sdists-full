/*
 * Copyright © 2026 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/propagate.h>

/*
 * Repeat (multiply):
 *
 * Repeats a string some integer number of times
 *
 * Source: Origin/Self
 * Target: Return
 * Action: SPLAT for now (TODO: PYT-1345)
 */

ssizeargfunc unicode_repeat_orig;
ssizeargfunc bytes_repeat_orig;
ssizeargfunc bytearray_repeat_orig;
ssizeargfunc bytearray_irepeat_orig;

PyObject *unicode_repeat_new(PyObject *self, Py_ssize_t n) {
    return propagate_repeat(unicode_repeat_orig, self, n, "propagate_unicode_repeat");
}

PyObject *bytes_repeat_new(PyObject *self, Py_ssize_t n) {
    return propagate_repeat(bytes_repeat_orig, self, n, "propagate_bytes_repeat");
}

PyObject *bytearray_repeat_new(PyObject *self, Py_ssize_t n) {
    return propagate_repeat(
        bytearray_repeat_orig, self, n, "propagate_bytearray_repeat");
}

/* TODO: PYT-1686 this doesn't work exactly the way we want (see ticket) */
PyObject *bytearray_irepeat_new(PyObject *self, Py_ssize_t n) {
    return propagate_repeat(
        bytearray_irepeat_orig, self, n, "propagate_unicode_repeat");
}

#define HOOK_REPEAT(TYPE, NAME)                           \
    NAME##_orig = (void *)TYPE.tp_as_sequence->sq_repeat; \
    TYPE.tp_as_sequence->sq_repeat = NAME##_new;

void apply_repeat_patch() {
    HOOK_REPEAT(PyUnicode_Type, unicode_repeat);
    HOOK_REPEAT(PyBytes_Type, bytes_repeat);
    HOOK_REPEAT(PyByteArray_Type, bytearray_repeat);

    bytearray_irepeat_orig = PyByteArray_Type.tp_as_sequence->sq_inplace_repeat;
    PyByteArray_Type.tp_as_sequence->sq_inplace_repeat = (void *)bytearray_irepeat_new;
}

void reverse_repeat_patch() {
    PyUnicode_Type.tp_as_sequence->sq_repeat = (void *)unicode_repeat_orig;
    PyBytes_Type.tp_as_sequence->sq_repeat = (void *)bytes_repeat_orig;
    PyByteArray_Type.tp_as_sequence->sq_repeat = (void *)bytearray_repeat_orig;
    PyByteArray_Type.tp_as_sequence->sq_inplace_repeat = (void *)bytearray_irepeat_orig;
}
