#ifndef ATOMIC_DICT_METHODS_H
#define ATOMIC_DICT_METHODS_H

#include "types.h"

int atomic_array_init(AtomicArray *self, PyObject *args, PyObject *kwds);

PyObject *atomic_array_index(AtomicArray *self, PyObject * const *args, Py_ssize_t nargs);

DictIterator *atomic_array_iterator(AtomicArray *self, PyObject * const *Args, Py_ssize_t nargs);


PyObject *atomic_value_64_load(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *atomic_value_64_store(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *atomic_value_64_swap(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *atomic_value_64_add(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *atomic_value_64_sub(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *atomic_value_64_band(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *atomic_value_64_bor(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *atomic_value_64_bxor(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *atomic_value_64_cas(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs);


PyObject *atomic_value_32_load(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *atomic_value_32_store(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *atomic_value_32_swap(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *atomic_value_32_add(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *atomic_value_32_sub(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *atomic_value_32_band(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *atomic_value_32_bor(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *atomic_value_32_bxor(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *atomic_value_32_cas(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs);


PyObject *dict_iterator_key(DictIterator *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *dict_iterator_value(DictIterator *self, PyObject * const *args, Py_ssize_t nargs);

PyObject *dict_iterator_next(DictIterator *self, PyObject * const *args, Py_ssize_t nargs);


PyObject *get_pointer(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs);

#endif
