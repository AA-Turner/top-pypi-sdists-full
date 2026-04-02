#ifndef ATOMIC_DICT_TYPES_H
#define ATOMIC_DICT_TYPES_H

#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <stdatomic.h>

typedef atomic_uint_least64_t atomic_dict64_t;
typedef atomic_uint_least32_t atomic_dict32_t;

typedef union {
  atomic_dict64_t a64[8];
  atomic_dict32_t a32[16];
} AtomicCacheBlock;

typedef struct {
    PyObject_HEAD
    AtomicCacheBlock *blocks;
    int k64, k32, v64, v32, rows;
    Py_ssize_t num_blocks;
} AtomicArray;

typedef struct {
    PyObject_HEAD
    atomic_dict64_t *val;
} AtomicValue64;

typedef struct {
    PyObject_HEAD
    atomic_dict32_t *val;
} AtomicValue32;

typedef struct {
    PyObject_HEAD
    AtomicArray *array;
    Py_ssize_t offset;
} DictIterator;

#endif
