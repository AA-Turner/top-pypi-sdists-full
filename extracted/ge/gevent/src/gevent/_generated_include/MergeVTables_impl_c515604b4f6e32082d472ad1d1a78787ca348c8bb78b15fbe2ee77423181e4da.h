static int __Pyx_MergeVtables(PyTypeObject *type) {
    int i=0;
    Py_ssize_t size;
    void** base_vtables;
    void* unknown = (void*)-1;
    PyObject* bases = __Pyx_PyType_GetSlot(type, tp_bases, PyObject*);
    int base_depth = 0;
    {
        PyTypeObject* base = __Pyx_PyType_GetSlot(type, tp_base, PyTypeObject*);
        while (base) {
            base_depth += 1;
            base = __Pyx_PyType_TryGetSlot(base, tp_base, PyTypeObject*);
        }
    }
    base_vtables = (void**) PyMem_Malloc(sizeof(void*) * (size_t)(base_depth + 1));
    if (unlikely(!base_vtables)) {
        PyErr_NoMemory();
        return -1;
    }
    base_vtables[0] = unknown;
#if CYTHON_COMPILING_IN_LIMITED_API
    size = PyTuple_Size(bases);
    if (size < 0) goto other_failure;
#else
    size = PyTuple_GET_SIZE(bases);
#endif
    for (i = 1; i < size; i++) {
        PyObject *basei;
        void* base_vtable;
#if CYTHON_AVOID_BORROWED_REFS
        basei = PySequence_GetItem(bases, i);
        if (unlikely(!basei)) goto other_failure;
#elif !CYTHON_ASSUME_SAFE_MACROS
        basei = PyTuple_GetItem(bases, i);
        if (unlikely(!basei)) goto other_failure;
#else
        basei = PyTuple_GET_ITEM(bases, i);
#endif
        int get_vtable_result = __Pyx_GetVtable((PyTypeObject*)basei, &base_vtable);
#if CYTHON_AVOID_BORROWED_REFS
        Py_DECREF(basei);
#endif
        if (get_vtable_result != 1) {
            if (get_vtable_result == -1) {
                goto other_failure;
            }
            PyErr_Clear(); // Class doesn't have a vtable.
        } else {
            assert(base_vtable != NULL);
            int j;
            PyTypeObject* base = __Pyx_PyType_TryGetSlot(type, tp_base, PyTypeObject*);
#if CYTHON_COMPILING_IN_LIMITED_API && __PYX_LIMITED_VERSION_HEX < 0x030A0000
            if (!base) goto bad;
#endif
            for (j = 0; j < base_depth; j++) {
                if (base_vtables[j] == unknown) {
                    switch (__Pyx_GetVtable(base, &base_vtables[j])) {
                        case 1:
                            assert(base_vtables[j] == NULL);
                            break;
                        case 0:
                            goto bad;
                        case -1:
                        default:
                            goto other_failure;
                    }
                    base_vtables[j + 1] = unknown;
                }
                if (base_vtables[j] == base_vtable) {
                    break;
                }
                base = __Pyx_PyType_TryGetSlot(base, tp_base, PyTypeObject*);
#if CYTHON_COMPILING_IN_LIMITED_API && __PYX_LIMITED_VERSION_HEX < 0x030A0000
                if (!base) goto bad;
#endif
            }
        }
    }
    PyMem_Free(base_vtables);
    return 0;
bad:
    {
        PyTypeObject* tp_base = __Pyx_PyType_GetSlot(type, tp_base, PyTypeObject*);
        PyTypeObject* basei;
#if CYTHON_AVOID_BORROWED_REFS
        basei = (PyTypeObject*)PySequence_GetItem(bases, i);
        if (unlikely(!basei)) goto other_failure;
#elif !CYTHON_ASSUME_SAFE_MACROS
        basei = (PyTypeObject*)PyTuple_GetItem(bases, i);
        if (unlikely(!basei)) goto other_failure;
#else
        basei = (PyTypeObject*)PyTuple_GET_ITEM(bases, i);
#endif
    __Pyx_RaiseTypeErrorWithTypes(
        "multiple bases have vtable conflict: '" __Pyx_FMT_TYPENAME "' and '" __Pyx_FMT_TYPENAME "'", tp_base, basei);
#if CYTHON_AVOID_BORROWED_REFS
        Py_DECREF(basei);
#endif
    }
other_failure:
    PyMem_Free(base_vtables);
    return -1;
}

