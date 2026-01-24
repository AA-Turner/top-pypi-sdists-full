/*
 * Copyright © 2026 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/patches.h>
#include <contrast/assess/scope.h>
#include <contrast/assess/intern.h>
#include <contrast/assess/logging.h>

static PyMethodDef methods[] = {
    {"initialize_logger", initialize_logger, METH_O, "Initialize C extension logger"},
    {"initialize",
     (PyCFunction)initialize,
     METH_NOARGS,
     "Initialize C extension patcher"},
    {"enable_c_patches",
     enable_c_patches,
     METH_NOARGS,
     "Hook relevant non-method functions"},
    {"disable_c_patches", disable_c_patches, METH_NOARGS, "Remove all hooks"},
    {"get_tp_version_tag", get_tp_version_tag, METH_O, "Get tp_version_tag for a type"},
    {"set_attr_on_type", set_attr_on_type, METH_VARARGS, "Set attribute on type"},
    {"is_string_interned", is_string_interned, METH_O, "Checks if string is interned"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef _c_ext_definition = {
    PyModuleDef_HEAD_INIT,
    "_c_ext",
    "description here",
    -1,
    methods,
    NULL,
    NULL,
    NULL,
    NULL};

PyMODINIT_FUNC PyInit__c_ext(void) {
    PyObject *module;

    Py_Initialize();

    module = PyModule_Create(&_c_ext_definition);

    if (PyModule_AddIntConstant(
            module,
            "DEBUG",
#ifdef ASSESS_DEBUG
            1
#else
            0
#endif
            ) != 0) {
        PyErr_Print();
        PyErr_SetString(PyExc_RuntimeError, "Failed to add debug constant");
    }

    PyModule_AddIntMacro(module, Py_TPFLAGS_HEAPTYPE);
#if PY_MINOR_VERSION > 9
    PyModule_AddIntMacro(module, Py_TPFLAGS_IMMUTABLETYPE);
#endif

    PyObject *py_scope = PyImport_ImportModule("contrast.agent.scope");
    if (py_scope == NULL) {
        PyErr_Print();
        PyErr_SetString(PyExc_RuntimeError, "Failed to import contrast.agent.scope");
        return NULL;
    }

    PyObject *contrast_scope = PyObject_GetAttrString(py_scope, "CONTRAST_SCOPE");
    PyObject *propagation_scope = PyObject_GetAttrString(py_scope, "PROPAGATION_SCOPE");
    PyObject *trigger_scope = PyObject_GetAttrString(py_scope, "TRIGGER_SCOPE");

    if (contrast_scope == NULL || propagation_scope == NULL || trigger_scope == NULL) {
        PyErr_Print();
        PyErr_SetString(
            PyExc_RuntimeError, "Failed to get scope vars from contrast.agent.scope");
        return NULL;
    }

    init_contrast_scope_cvars(contrast_scope, propagation_scope, trigger_scope);

    return module;
}
