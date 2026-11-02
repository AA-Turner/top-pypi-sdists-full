/*
 * Copyright © 2026 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
#ifndef _ASSESS_PROPAGATE_H_
#define _ASSESS_PROPAGATE_H_
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdbool.h>

int init_propagate(void);
int init_string_tracker(void);
int init_propagation(void);
void teardown_propagate(void);
int is_tracked(PyObject *source);
void call_string_propagator(
    char *prop_method_name,
    PyObject *source,
    PyObject *newstr,
    PyObject *hook_args,
    PyObject *hook_kwargs);
PyObject *propagate_repeat(
    ssizeargfunc orig_repeat, PyObject *self, Py_ssize_t n, char *propagator);
void create_stream_source_event(PyObject *s, PyObject *args, PyObject *kwargs);

#endif /* _ASSESS_PROPAGATE_H_ */
