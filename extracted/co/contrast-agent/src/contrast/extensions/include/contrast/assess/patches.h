/*
 * Copyright © 2026 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
#ifndef _ASSESS_PATCHES_H_
#define _ASSESS_PATCHES_H_
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

PyObject *initialize(PyObject *, PyObject *);
PyObject *enable_c_patches(PyObject *self, PyObject *arg);
PyObject *disable_c_patches(PyObject *self, PyObject *args);
PyObject *get_tp_dict(PyTypeObject *type);
PyObject *get_tp_version_tag(PyObject *unused, PyObject *args);
PyObject *set_attr_on_type(PyObject *self, PyObject *args);
PyObject *create_unicode_hook_module(PyObject *self, PyObject *args);
PyObject *create_bytes_hook_module(PyObject *self, PyObject *args);
PyObject *create_bytearray_hook_module(PyObject *self, PyObject *args);

void apply_repeat_patch();
void apply_subscript_patch();
void apply_cast_patches();
int apply_stream_patches();
void apply_repr_patches();
int patch_stringio_methods(PyTypeObject *StreamType);
int patch_bytesio_methods(PyTypeObject *StreamType);
int patch_iobase_methods(PyTypeObject *StreamType);

void reverse_repeat_patch();
void reverse_subscript_patch();
void reverse_stream_patches();
void reverse_repr_patches();
void reverse_cast_patches();

void reverse_stringio_methods(PyTypeObject *StreamType);
void reverse_bytesio_methods(PyTypeObject *StreamType);
void reverse_iobase_methods(PyTypeObject *StreamType);

#endif /* _ASSESS_PATCHES_H_ */
