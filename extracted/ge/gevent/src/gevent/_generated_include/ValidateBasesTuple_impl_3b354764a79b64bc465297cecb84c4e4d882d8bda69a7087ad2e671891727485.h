#if CYTHON_COMPILING_IN_CPYTHON || CYTHON_COMPILING_IN_LIMITED_API || CYTHON_USE_TYPE_SPECS
static int __Pyx_validate_bases_tuple(const char *type_name, int has_dictoffset, PyObject *bases) {
    Py_ssize_t i, n;
#if CYTHON_ASSUME_SAFE_SIZE
    n = PyTuple_GET_SIZE(bases);
#else
    n = PyTuple_Size(bases);
    if (unlikely(n < 0)) return -1;
#endif
    if (!has_dictoffset) {
        PyObject *b;
#if CYTHON_AVOID_BORROWED_REFS
        b = PySequence_GetItem(bases, 0);
        if (!b) return -1;
#elif CYTHON_ASSUME_SAFE_MACROS
        b = PyTuple_GET_ITEM(bases, 0);
#else
        b = PyTuple_GetItem(bases, 0);
        if (!b) return -1;
#endif
#if CYTHON_USE_TYPE_SLOTS
        has_dictoffset = ((PyTypeObject*)b)->tp_dictoffset != 0;
#else
        Py_ssize_t dictoffset = __Pyx_GetTypeDictOffset(b, 0);
        has_dictoffset = dictoffset != 0;
#endif
#if CYTHON_AVOID_BORROWED_REFS
        Py_DECREF(b);
#endif
#if !CYTHON_USE_TYPE_SLOTS
        if (dictoffset == -1 && PyErr_Occurred()) return -1;
#endif
    }
    for (i = 1; i < n; i++)
    {
        PyTypeObject *b;
#if CYTHON_AVOID_BORROWED_REFS
        PyObject *b0 = PySequence_GetItem(bases, i);
        if (!b0) return -1;
#elif CYTHON_ASSUME_SAFE_MACROS
        PyObject *b0 = PyTuple_GET_ITEM(bases, i);
#else
        PyObject *b0 = PyTuple_GetItem(bases, i);
        if (!b0) return -1;
#endif
        b = (PyTypeObject*) b0;
        if (!__Pyx_PyType_HasFeature(b, Py_TPFLAGS_HEAPTYPE))
        {
            __Pyx_RaiseErrorWithType(
                PyExc_TypeError, "base class '" __Pyx_FMT_TYPENAME "' is not a heap type", b);
#if CYTHON_AVOID_BORROWED_REFS
            Py_DECREF(b0);
#endif
            return -1;
        }
        if (!has_dictoffset)
        {
            Py_ssize_t b_dictoffset = 0;
#if CYTHON_USE_TYPE_SLOTS
            b_dictoffset = b->tp_dictoffset;
#else
            b_dictoffset = __Pyx_GetTypeDictOffset((PyObject*)b, 0);
            if (b_dictoffset == -1 && PyErr_Occurred()) goto dictoffset_return;
#endif
            if (b_dictoffset) {
                __Pyx_RaiseErrorWithType1(
                    PyExc_TypeError,
                    "extension type '%.200s' has no __dict__ slot, "
                    "but base type '" __Pyx_FMT_TYPENAME "' has: "
                    "either add 'cdef dict __dict__' to the extension type "
                    "or add '__slots__ = [...]' to the base type",
                    type_name, b);
#if !CYTHON_USE_TYPE_SLOTS
              dictoffset_return:
#endif
#if CYTHON_AVOID_BORROWED_REFS
                Py_DECREF(b0);
#endif
                return -1;
            }
        }
#if CYTHON_AVOID_BORROWED_REFS
        Py_DECREF(b0);
#endif
    }
    return 0;
}
#endif

