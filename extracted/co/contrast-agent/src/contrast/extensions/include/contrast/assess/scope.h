/*
 * Copyright © 2026 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
#ifndef _ASSESS_SCOPE_H_
#define _ASSESS_SCOPE_H_
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <patchlevel.h>

typedef PyObject PyContextVarT;

void init_contrast_scope_cvars(PyContextVarT *, PyContextVarT *, PyContextVarT *);

void enter_contrast_scope(void);
void exit_contrast_scope(void);
void enter_propagation_scope(void);
void exit_propagation_scope(void);
int should_propagate(void);

#endif /* _ASSESS_SCOPE_H_ */
