#include "methods.h"

extern PyTypeObject DictIteratorType;
extern PyTypeObject AtomicValue64Type;
extern PyTypeObject AtomicValue32Type;

int atomic_array_init(AtomicArray *self, PyObject *args, PyObject *kwds) {
    PyObject *memory_view;
    Py_buffer *buffer;
    int k64, k32, v64, v32;

    if (!PyArg_ParseTuple(args, "Oiiii|", &memory_view, &k64, &k32, &v64, &v32)) {
        return -1;
    }

    if (sizeof(AtomicCacheBlock) != 64) {
       PyErr_SetString(PyExc_ValueError, "AtomicArray AtomicCacheBlock is not 64 bytes");
       return -1;
    }

    buffer = PyMemoryView_GET_BUFFER(memory_view);
    if (!buffer)
        return -1;

    if ((buffer->len & (buffer->len - 1)) != 0) {
        PyErr_SetString(PyExc_ValueError, "AtomicArray buffer must be power-of-two sized");
        return -1;
    }

    if (buffer->len < 64) {
        PyErr_SetString(PyExc_ValueError, "AtomicArray buffer must be at least one cache block");
        return -1;
    }

    if (k64 < 0 || k32 < 0 || v64 < 0 || v32 < 0) {
        PyErr_SetString(PyExc_ValueError, "AtomicArray key and value cells must be non-negative");
        return -1;
    }

    if (k64 == 0 && k32 == 0) {
        PyErr_SetString(PyExc_ValueError, "AtomicArray must have at least one key cell");
        return -1;
    }

    if (v64 + v32 > 1) {
        PyErr_SetString(PyExc_ValueError, "AtomicArray can only store one atomic value per key");
        return -1;
    }

    if ((k64 + v64) * 8 + (k32 + v32) * 4 > 64) {
        PyErr_SetString(PyExc_ValueError, "AtomicArray single entry exceeds a cache-block");
        return -1;
    }

    self->blocks = (AtomicCacheBlock *)buffer->buf;
    self->num_blocks = buffer->len / 64;
    self->k64 = k64;
    self->k32 = k32;
    self->v64 = v64;
    self->v32 = v32;
    self->rows = 64 / ((k64 + v64) * 8 + (k32 + v32) * 4);

    return 0;
}

static uint64_t key_hash(uint64_t key) {
    // Lifted from MumurHash3 fmix64
    key ^= key >> 33;
    key *= UINT64_C(0xFF51AFD7ED558CCD);
    key ^= key >> 33;
    key *= UINT64_C(0xC4CEB9FE1A85EC53);
    key ^= key >> 33;

    return key;
}

#define STR_HELPER(x) #x
#define STR(x) STR_HELPER(x)
#define CHECK_ARGN(fn, n) if (nargs != n) {                                               \
    PyErr_SetString(PyExc_TypeError, fn " expected " STR(n) " arguments"); \
    return 0;                                                                             \
}

PyObject *atomic_array_index(AtomicArray *self, PyObject * const *args, Py_ssize_t nargs) {
    AtomicCacheBlock key;
    uint64_t         kv;
    uint64_t         hash;
    int              ki;
    int              row;
    int              match = 0;
    int              first = 0;
    atomic_dict64_t  e64;
    atomic_dict32_t  e32;
    Py_ssize_t       index;
    Py_ssize_t       stride;
    Py_ssize_t       attempts;
    AtomicValue64   *v64 = 0;
    AtomicValue32   *v32 = 0;

    CHECK_ARGN("AtomicArray.index", self->k64 + self->k32);

    hash = 0;

    for (ki = 0; ki < self->k64; ++ki) {
      kv = PyLong_AsUnsignedLongLong(args[ki]);
      if (!kv) {
        PyErr_SetString(PyExc_ValueError, "AtomicArray.index requires key arguments to be non-zero");
        return 0;
      }
      key.a64[ki] = kv;
      hash = key_hash(hash ^ kv);
    }

    for (ki = 0; ki < self->k32; ++ki) {
      kv = PyLong_AsUnsignedLong(args[ki + self->k64]);
      if (!kv) {
        PyErr_SetString(PyExc_ValueError, "AtomicArray.index requires key arguments to be non-zero");
        return 0;
      }
      key.a32[ki + 2 * self->k64] = kv;
      hash = key_hash(hash ^ kv);
    }
    
    if (self->v64) {
        v64 = PyObject_New(AtomicValue64, &AtomicValue64Type);
        if (!v64) return 0;
    }

    if (self->v32) {
        v32 = PyObject_New(AtomicValue32, &AtomicValue32Type);
        if (!v32) return 0;
    }

    index = hash & (self->num_blocks - 1);
    stride = ((hash >> 32) & (self->num_blocks - 1)) | 1;

    for (attempts = 0; !match && attempts < self->num_blocks; ++attempts) {
        AtomicCacheBlock *block = self->blocks + index;
        atomic_dict64_t *a64 = &block->a64[0];
        atomic_dict32_t *a32 = &block->a32[2 * self->rows * (self->k64 + self->v64)];

        for (row = 0; !match && row < self->rows; ++row) {
            match = 1;

            for (ki = 0; match && ki < self->k64; ++ki) {
                e64 = 0;
                atomic_compare_exchange_strong(a64 + ki, &e64, key.a64[ki]);
                match = e64 == 0 || e64 == key.a64[ki];
                first = ki + 1 == self->k64 && e64 == 0 && self->k32 == 0;
            }

            for (ki = 0; match && ki < self->k32; ++ki) {
                e32 = 0;
                atomic_compare_exchange_strong(a32 + ki, &e32, key.a32[ki + 2 * self->k64]);
                match = e32 == 0 || e32 == key.a32[ki + 2 * self->k32];
                first = ki + 1 == self->k32 && e32 == 0;
            }

            if (v64) { v64->val = a64 + self->k64; }
            if (v32) { v32->val = a32 + self->k32; }

            a64 += self->k64 + self->v64;
            a32 += self->k32 + self->v32;
        }

        index = (index + stride) & (self->num_blocks - 1);
    }

    if (attempts == self->num_blocks) {
        if (v64) Py_DECREF(v64);
        if (v32) Py_DECREF(v32);
        PyErr_SetString(PyExc_ValueError, "AtomicArray capacity exceeded");
        return 0;
    }

    if (v64) return (PyObject*)v64;
    if (v32) return (PyObject*)v32;
    return PyBool_FromLong(first);
}

DictIterator *atomic_array_iterator(AtomicArray *self, PyObject * const *args, Py_ssize_t nargs) {
    DictIterator *out;

    CHECK_ARGN("AtomicArray.iterator", 0);

    out = PyObject_New(DictIterator, &DictIteratorType);
    if (out) {
        out->array = self;
        out->offset = 0;
    }

    return out;
}


PyObject *atomic_value_64_load(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue64.load", 0);
    return PyLong_FromUnsignedLongLong(atomic_load(self->val));
}

PyObject *atomic_value_64_store(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue64.store", 1);
    atomic_store(self->val, PyLong_AsUnsignedLongLong(args[0]));
    Py_RETURN_NONE;
}

PyObject *atomic_value_64_swap(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue64.swap", 1);
    return PyLong_FromUnsignedLongLong(atomic_exchange(self->val, PyLong_AsUnsignedLongLong(args[0])));
}

PyObject *atomic_value_64_add(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue64.add", 1);
    return PyLong_FromUnsignedLongLong(atomic_fetch_add(self->val, PyLong_AsUnsignedLongLong(args[0])));
}

PyObject *atomic_value_64_sub(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue64.sub", 1);
    return PyLong_FromUnsignedLongLong(atomic_fetch_sub(self->val, PyLong_AsUnsignedLongLong(args[0])));
}

PyObject *atomic_value_64_band(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue64.band", 1);
    return PyLong_FromUnsignedLongLong(atomic_fetch_and(self->val, PyLong_AsUnsignedLongLong(args[0])));
}

PyObject *atomic_value_64_bor(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue64.bor", 1);
    return PyLong_FromUnsignedLongLong(atomic_fetch_or(self->val, PyLong_AsUnsignedLongLong(args[0])));
}

PyObject *atomic_value_64_bxor(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue64.bxor", 1);
    return PyLong_FromUnsignedLongLong(atomic_fetch_xor(self->val, PyLong_AsUnsignedLongLong(args[0])));
}

PyObject *atomic_value_64_cas(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue64.cas", 2);
    atomic_dict64_t expected = PyLong_AsUnsignedLongLong(args[0]);
    atomic_dict64_t desired  = PyLong_AsUnsignedLongLong(args[1]);
    atomic_compare_exchange_strong(self->val, &expected, desired);
    return PyLong_FromUnsignedLongLong(expected);
}


PyObject *atomic_value_32_load(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue32.load", 0);
    return PyLong_FromUnsignedLong(atomic_load(self->val));
}

PyObject *atomic_value_32_store(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue32.store", 1);
    atomic_store(self->val, PyLong_AsUnsignedLong(args[0]));
    Py_RETURN_NONE;
}

PyObject *atomic_value_32_swap(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue32.swap", 1);
    return PyLong_FromUnsignedLong(atomic_exchange(self->val, PyLong_AsUnsignedLong(args[0])));
}

PyObject *atomic_value_32_add(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue32.add", 1);
    return PyLong_FromUnsignedLong(atomic_fetch_add(self->val, PyLong_AsUnsignedLong(args[0])));
}

PyObject *atomic_value_32_sub(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue32.sub", 1);
    return PyLong_FromUnsignedLong(atomic_fetch_sub(self->val, PyLong_AsUnsignedLong(args[0])));
}

PyObject *atomic_value_32_band(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue32.band", 1);
    return PyLong_FromUnsignedLong(atomic_fetch_and(self->val, PyLong_AsUnsignedLong(args[0])));
}

PyObject *atomic_value_32_bor(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue32.bor", 1);
    return PyLong_FromUnsignedLong(atomic_fetch_or(self->val, PyLong_AsUnsignedLong(args[0])));
}

PyObject *atomic_value_32_bxor(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue32.bxor", 1);
    return PyLong_FromUnsignedLong(atomic_fetch_xor(self->val, PyLong_AsUnsignedLong(args[0])));
}

PyObject *atomic_value_32_cas(AtomicValue32 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("AtomicValue32.cas", 2);
    atomic_dict32_t expected = PyLong_AsUnsignedLong(args[0]);
    atomic_dict32_t desired  = PyLong_AsUnsignedLong(args[1]);
    atomic_compare_exchange_strong(self->val, &expected, desired);
    return PyLong_FromUnsignedLong(expected);
}


PyObject *dict_iterator_key(DictIterator *self, PyObject * const *args, Py_ssize_t nargs) {
    AtomicCacheBlock *block = self->array->blocks + (self->offset / self->array->rows);
    AtomicCacheBlock *end = self->array->blocks + self->array->num_blocks;
    int n64 = self->array->k64 + self->array->v64;
    int n32 = self->array->k32 + self->array->v32;
    int o32 = self->array->rows * n64 * 2;
    int ki;

    CHECK_ARGN("DictIterator.key", 0);

    while (block != end) {
        int row = self->offset % self->array->rows;
        int set = 0;
        if (self->array->k64) {
            atomic_dict64_t key = atomic_load(&block->a64[row * n64]);
            set = key != 0;
        }
        if (self->array->k32) {
            atomic_dict32_t key = atomic_load(&block->a32[row * n32 + o32]);
            set = key != 0;
        }
        if (set) {
            PyObject *out = PyTuple_New(self->array->k64 + self->array->k32);
            if (!out) return 0;
            for (ki = 0; ki < self->array->k64; ++ki) {
                atomic_dict64_t key = atomic_load(&block->a64[ki + row * n64]);
                PyTuple_SetItem(out, ki, PyLong_FromUnsignedLongLong(key));
            }
            for (ki = 0; ki < self->array->k32; ++ki) {
                atomic_dict32_t key = atomic_load(&block->a32[ki + row * n32 + o32]);
                PyTuple_SetItem(out, ki + self->array->k64, PyLong_FromUnsignedLong(key));
            }
            return out;
        }
        ++self->offset;
        if (row == self->array->rows - 1) ++block;
    }

    Py_RETURN_NONE;
}

PyObject *dict_iterator_value(DictIterator *self, PyObject * const *args, Py_ssize_t nargs) {
    AtomicCacheBlock *block = self->array->blocks + (self->offset / self->array->rows);
    AtomicCacheBlock *end = self->array->blocks + self->array->num_blocks;
    int n64 = self->array->k64 + self->array->v64;
    int n32 = self->array->k32 + self->array->v32;
    int o32 = self->array->rows * n64 * 2;

    CHECK_ARGN("DictIterator.value", 0);

    while (block != end) {
        int row = self->offset % self->array->rows;
        int set = 0;
        if (self->array->k64) {
            atomic_dict64_t key = atomic_load(&block->a64[row * n64]);
            set = key != 0;
        }
        if (self->array->k32) {
            atomic_dict32_t key = atomic_load(&block->a32[row * n32 + o32]);
            set = key != 0;
        }
        if (set) {
            if (self->array->v64) {
                atomic_dict64_t val = atomic_load(&block->a64[self->array->k64 + row * n64]);
                return PyLong_FromUnsignedLongLong(val);
            }
            if (self->array->v32) {
                atomic_dict32_t val = atomic_load(&block->a32[self->array->k32 + row * n32 + o32]);
                return PyLong_FromUnsignedLong(val);
            }
            Py_RETURN_TRUE;
        }
        ++self->offset;
        if (row == self->array->rows - 1) ++block;
    }

    Py_RETURN_NONE;
}

PyObject *dict_iterator_next(DictIterator *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("DictIterator.next", 0);

    if (self->offset / self->array->rows < self->array->num_blocks) {
        ++self->offset;
    }

    Py_RETURN_NONE;
}

PyObject *get_pointer(AtomicValue64 *self, PyObject * const *args, Py_ssize_t nargs) {
    CHECK_ARGN("get_pointer", 1);

    const char *name = PyCapsule_GetName(args[0]);
    if (!name) return 0;

    void *pointer = PyCapsule_GetPointer(args[0], name);
    if (!pointer) return 0;

    return PyLong_FromUnsignedLongLong((uint64_t)pointer);
}
