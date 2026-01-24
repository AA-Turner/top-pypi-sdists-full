/*
 * Copyright © 2026 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/propagate.h>

#define HOOK_REPR(NAME)                                                       \
    static PyObject *NAME##_new(PyObject *self) {                             \
        PyObject *result = NAME##_orig(self);                                 \
                                                                              \
        if (result == NULL)                                                   \
            return result;                                                    \
                                                                              \
        call_string_propagator("propagate_" #NAME, self, result, NULL, NULL); \
                                                                              \
        return result;                                                        \
    }

/* we need these really ugly method names for automatic hook-specific propagator
   generation to work properly */

unaryfunc bytes___repr___orig;
unaryfunc unicode___repr___orig;
unaryfunc bytearray___repr___orig;
HOOK_REPR(bytes___repr__);
HOOK_REPR(unicode___repr__);
HOOK_REPR(bytearray___repr__);

#define APPLY_REPR_HOOK(TYPE, NAME)     \
    NAME##_orig = (void *)TYPE.tp_repr; \
    TYPE.tp_repr = NAME##_new;

void apply_repr_patches() {
    APPLY_REPR_HOOK(PyBytes_Type, bytes___repr__);
    APPLY_REPR_HOOK(PyUnicode_Type, unicode___repr__);
    APPLY_REPR_HOOK(PyByteArray_Type, bytearray___repr__);
}

void reverse_repr_patches() {
    PyBytes_Type.tp_repr = (void *)bytes___repr___orig;
    PyUnicode_Type.tp_repr = (void *)unicode___repr___orig;
    PyByteArray_Type.tp_repr = (void *)bytearray___repr___orig;
}
