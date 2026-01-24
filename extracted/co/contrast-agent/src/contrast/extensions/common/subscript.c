/*
 * Copyright © 2026 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <assert.h>
#include <ctype.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>

#include <contrast/assess/patches.h>
#include <contrast/assess/propagate.h>
#include <contrast/assess/scope.h>

/*
 * Subscript:
 *
 * Returns a slice of a string
 *
 * Source: Origin/Self
 * Target: Return
 * Action: Keep
 */

#define HOOK_SUBSCRIPT(NAME)                                             \
    PyObject *NAME##_item_new(PyObject *a, PyObject *b) {                \
        PyObject *result;                                                \
                                                                         \
        enter_propagation_scope();                                       \
        result = NAME##_item_orig(a, b);                                 \
        exit_propagation_scope();                                        \
                                                                         \
        PyObject *args = PyTuple_Pack(1, b);                             \
                                                                         \
        /* Record input and result */                                    \
        if (result != NULL && !PyNumber_Check(result))                   \
            call_string_propagator(                                      \
                "propagate_" #NAME "_subscript", a, result, args, NULL); \
                                                                         \
        Py_XDECREF(args);                                                \
        return result;                                                   \
    }

binaryfunc unicode_item_orig;
binaryfunc bytes_item_orig;
binaryfunc bytearray_item_orig;
HOOK_SUBSCRIPT(unicode);
HOOK_SUBSCRIPT(bytes);
HOOK_SUBSCRIPT(bytearray);

#define APPLY_SUBSCRIPT_HOOK(TYPE, NAME)            \
    NAME##_orig = TYPE.tp_as_mapping->mp_subscript; \
    TYPE.tp_as_mapping->mp_subscript = (void *)NAME##_new;

void apply_subscript_patch() {
    APPLY_SUBSCRIPT_HOOK(PyBytes_Type, bytes_item);
    APPLY_SUBSCRIPT_HOOK(PyUnicode_Type, unicode_item);
    APPLY_SUBSCRIPT_HOOK(PyByteArray_Type, bytearray_item);
}

void reverse_subscript_patch() {
    PyBytes_Type.tp_as_mapping->mp_subscript = (void *)bytes_item_orig;
    PyUnicode_Type.tp_as_mapping->mp_subscript = (void *)unicode_item_orig;
    PyByteArray_Type.tp_as_mapping->mp_subscript = (void *)bytearray_item_orig;
}
