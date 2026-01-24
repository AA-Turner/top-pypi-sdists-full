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

#define apply_or_fail(applyfunc)                                    \
    do {                                                            \
        if ((applyfunc)() != 0) {                                   \
            /* Logging and exception is handled inside applyfunc */ \
            teardown_propagate();                                   \
            return NULL;                                            \
        }                                                           \
    } while (0);

PyObject *get_tp_dict(PyTypeObject *type) {
    /* In newer versions of python, tp_dict access must go through PyType_GetDict.
       In older versions of python, this function does not exist */
    PyObject *tp_dict = NULL;

    if (type == NULL)
        return NULL;

#if PY_MINOR_VERSION < 12
    tp_dict = type->tp_dict;
#else
    tp_dict = PyType_GetDict(type);
    /* This most closely resembles the pre-3.12 behavior of just returning type->tp_dict
       It is the caller's responsibility to XINCREF the result if necessary
    */
    Py_XDECREF(tp_dict);
#endif /* PY_MINOR_VERSION < 12 */

    return tp_dict;
}

PyObject *get_tp_version_tag(PyObject *self, PyObject *type) {
    if (!PyType_Check(type)) {
        PyErr_SetString(PyExc_TypeError, "argument must be a type");
        return NULL;
    }
    PyObject *res = PyLong_FromUnsignedLong(((PyTypeObject *)type)->tp_version_tag);
    if (res == NULL) {
        assert(PyErr_Occurred());
        return NULL;
    }
    return res;
}

PyObject *set_attr_on_type(PyObject *self, PyObject *args) {
    PyTypeObject *type = NULL;
    PyObject *name = NULL;
    PyObject *attr = NULL;
    PyObject *tp_dict = NULL;

    if (!PyArg_ParseTuple(args, "OOO", (PyObject **)&type, &name, &attr)) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse arguments");
        return NULL;
    }

    if (!PyType_Check(type)) {
        PyErr_SetString(PyExc_TypeError, "First argument must be a type");
        return NULL;
    }

    tp_dict = get_tp_dict(type);
    if (tp_dict == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to retrieve tp_dict");
        return NULL;
    }

    if (PyDict_SetItem(tp_dict, name, attr) != 0) {
        return NULL;
    }

    PyType_Modified(type);

    Py_RETURN_NONE;
}

PyObject *initialize(PyObject *unused, PyObject *unused2) {
    log_debug("BUILD DATETIME %s ", EXTENSION_BUILD_TIME);

    if (init_propagate() != 0) {
        /* Logging and exception occur inside init_propagate */
        return NULL;
    }

    log_debug("initialized propagation");

    Py_RETURN_NONE;
}

PyObject *enable_c_patches(PyObject *self, PyObject *arg) {
    apply_cast_patches();
    apply_repeat_patch();
    apply_or_fail(apply_stream_patches);
    apply_subscript_patch();
    apply_repr_patches();

    Py_RETURN_NONE;
}

PyObject *disable_c_patches(PyObject *self, PyObject *arg) {
    reverse_repr_patches();
    reverse_subscript_patch();
    reverse_stream_patches();
    reverse_repeat_patch();
    reverse_cast_patches();

    log_debug("uninstalled assess patches");

    teardown_propagate();

    log_debug("disabled propagation");

    teardown_logger();

    Py_RETURN_NONE;
}
