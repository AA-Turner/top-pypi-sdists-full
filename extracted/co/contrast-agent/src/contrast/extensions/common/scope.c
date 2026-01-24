/*
 * Copyright © 2026 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdbool.h>
#include <contrast/assess/logging.h>
#include <contrast/assess/scope.h>

static PyObject *cvar_contrast_scope = NULL;
static PyObject *cvar_propagation_scope = NULL;
static PyObject *cvar_trigger_scope = NULL;

void init_contrast_scope_cvars(
    PyContextVarT *contrast_scope,
    PyContextVarT *propagation_scope,
    PyContextVarT *trigger_scope) {
    cvar_contrast_scope = contrast_scope;
    cvar_propagation_scope = propagation_scope;
    cvar_trigger_scope = trigger_scope;
}

static long get_scope_as_long(PyContextVarT *cvar) {
    PyObject *current_scope_obj = NULL;
    if (cvar == NULL) {
        return 0;
    }

    if (PyContextVar_Get(cvar, NULL, &current_scope_obj) < 0) {
        PyErr_Format(PyExc_RuntimeError, "Failed to get current scope object");
        return 0;
    }

    long scope = PyLong_AsLong(current_scope_obj);

    Py_XDECREF(current_scope_obj);

    return scope;
}

static void modify_scope(PyContextVarT *scope, long modifier) {
    /*
        Adjusts the scope count of the ContextVar scope by `modifier` (1 or -1).
    */
    long new_scope = get_scope_as_long(scope) + modifier;
    PyObject *new_scope_obj = PyLong_FromLong(new_scope);
    if (new_scope_obj == NULL) {
        PyErr_Format(PyExc_RuntimeError, "Failed to modify scope to %ld", new_scope);
        return;
    }

    PyObject *token = PyContextVar_Set(scope, new_scope_obj);
    if (token == NULL) {
        PyErr_Format(PyExc_RuntimeError, "Failed to set scope");
    } else {
        Py_DECREF(token);
    }

    Py_DECREF(new_scope_obj);
}

static inline void enter_scope(PyContextVarT *scope) {
    modify_scope(scope, 1);
}

static inline void exit_scope(PyContextVarT *scope) {
    modify_scope(scope, -1);
}

static inline bool in_scope(PyContextVarT *scope) {
    return get_scope_as_long(scope) > 0;
}

inline void enter_contrast_scope(void) {
    return enter_scope(cvar_contrast_scope);
}

inline void exit_contrast_scope(void) {
    exit_scope(cvar_contrast_scope);
}

inline void enter_propagation_scope(void) {
    return enter_scope(cvar_propagation_scope);
}

inline void exit_propagation_scope(void) {
    exit_scope(cvar_propagation_scope);
}

inline int should_propagate(void) {
    return !(
        in_scope(cvar_contrast_scope) || in_scope(cvar_propagation_scope) ||
        // TODO: PYT-2925 This behavior is not consistent with the pure Python hooks
        in_scope(cvar_trigger_scope));
}
