/*
 * Copyright © 2026 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/logging.h>
#include <contrast/assess/patches.h>
#include <contrast/assess/propagate.h>
#include <contrast/assess/scope.h>

#define DEFINE_STREAM_INIT(NAME)                                            \
    int NAME##_init_new(PyObject *self, PyObject *args, PyObject *kwargs) { \
        int retval;                                                         \
                                                                            \
        /* Call the original init function */                               \
        if ((retval = NAME##_init_orig(self, args, kwargs)) != 0)           \
            goto cleanup_and_exit;                                          \
                                                                            \
        /* Safety check for args before we proceed */                       \
        if (args == NULL || !PySequence_Check(args))                        \
            goto cleanup_and_exit;                                          \
                                                                            \
        /* Create a source event for stream.__init__ */                     \
        create_stream_source_event(self, args, kwargs);                     \
                                                                            \
    cleanup_and_exit:                                                       \
        return retval;                                                      \
    }

static int (*stringio_init_orig)(PyObject *, PyObject *, PyObject *);
static int (*bytesio_init_orig)(PyObject *, PyObject *, PyObject *);
DEFINE_STREAM_INIT(stringio);
DEFINE_STREAM_INIT(bytesio);

PyTypeObject *StringIOType;
PyTypeObject *BytesIOType;

int apply_stream_patches() {
    PyObject *io_module = NULL;
    int retcode = 0;

    StringIOType = NULL;
    BytesIOType = NULL;

    if ((io_module = PyImport_ImportModule("_io")) == NULL) {
        log_error("Failed to import io module");
        retcode = 1;
        goto cleanup_and_exit;
    }

    if ((StringIOType =
             (PyTypeObject *)PyObject_GetAttrString(io_module, "StringIO")) == NULL) {
        log_error("Failed to get StringIO type");
        retcode = 1;
        goto cleanup_and_exit;
    }

    if ((BytesIOType = (PyTypeObject *)PyObject_GetAttrString(io_module, "BytesIO")) ==
        NULL) {
        log_error("Failed to get BytesIO type");
        retcode = 1;
        goto cleanup_and_exit;
    }

    stringio_init_orig = StringIOType->tp_init;
    bytesio_init_orig = BytesIOType->tp_init;

    StringIOType->tp_init = (void *)stringio_init_new;
    BytesIOType->tp_init = (void *)bytesio_init_new;

cleanup_and_exit:
    Py_XDECREF(io_module);
    Py_XDECREF(StringIOType);
    Py_XDECREF(BytesIOType);
    return retcode;
}

void reverse_stream_patches() {
    StringIOType->tp_init = (void *)stringio_init_orig;
    BytesIOType->tp_init = (void *)bytesio_init_orig;
}
