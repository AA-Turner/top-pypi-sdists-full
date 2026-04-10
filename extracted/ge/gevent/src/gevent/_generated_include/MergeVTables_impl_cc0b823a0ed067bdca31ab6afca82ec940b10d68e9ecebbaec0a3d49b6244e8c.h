static int __Pyx_MergeVtables(PyTypeObject *type) {
    int i=0;
    Py_ssize_t size;
    void** base_vtables;
    __Pyx_TypeName tp_base_name = NULL;
    __Pyx_TypeName base_name = NULL;
    void* unknown = (void*)-1;
    PyObject* bases = __Pyx_PyType_GetSlot(type, tp_bases, PyObject*);
    int base_depth = 0;
    {
        PyTypeObject* base = __Pyx_PyType_GetSlot(type, tp_base, PyTypeObject*);
        while (base) {
            base_depth += 1;
            base = __Pyx_PyType_GetSlot(base, tp_base, PyTypeObject*);
        }
    }
    base_vtables = (void**) PyMem_Malloc(sizeof(void*) * (size_t)(base_depth + 1));
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
        base_vtable = __Pyx_GetVtable((PyTypeObject*)basei);
#if CYTHON_AVOID_BORROWED_REFS
        Py_DECREF(basei);
#endif
        if (base_vtable != NULL) {
            int j;
            PyTypeObject* base = __Pyx_PyType_GetSlot(type, tp_base, PyTypeObject*);
            for (j = 0; j < base_depth; j++) {
                if (base_vtables[j] == unknown) {
                    base_vtables[j] = __Pyx_GetVtable(base);
                    base_vtables[j + 1] = unknown;
                }
                if (base_vtables[j] == base_vtable) {
                    break;
                } else if (base_vtables[j] == NULL) {
                    goto bad;
                }
                base = __Pyx_PyType_GetSlot(base, tp_base, PyTypeObject*);
            }
        }
    }
    PyErr_Clear();
    PyMem_Free(base_vtables);
    return 0;
bad:
    {
        PyTypeObject* basei = NULL;
        PyTypeObject* tp_base = __Pyx_PyType_GetSlot(type, tp_base, PyTypeObject*);
        tp_base_name = __Pyx_PyType_GetFullyQualifiedName(tp_base);
#if CYTHON_AVOID_BORROWED_REFS
        basei = (PyTypeObject*)PySequence_GetItem(bases, i);
        if (unlikely(!basei)) goto really_bad;
#elif !CYTHON_ASSUME_SAFE_MACROS
        basei = (PyTypeObject*)PyTuple_GetItem(bases, i);
        if (unlikely(!basei)) goto really_bad;
#else
        basei = (PyTypeObject*)PyTuple_GET_ITEM(bases, i);
#endif
        base_name = __Pyx_PyType_GetFullyQualifiedName(basei);
#if CYTHON_AVOID_BORROWED_REFS
        Py_DECREF(basei);
#endif
    }
    PyErr_Format(PyExc_TypeError,
        "multiple bases have vtable conflict: '" __Pyx_FMT_TYPENAME "' and '" __Pyx_FMT_TYPENAME "'", tp_base_name, base_name);
#if CYTHON_AVOID_BORROWED_REFS || !CYTHON_ASSUME_SAFE_MACROS
really_bad: // bad has failed!
#endif
    __Pyx_DECREF_TypeName(tp_base_name);
    __Pyx_DECREF_TypeName(base_name);
#if CYTHON_COMPILING_IN_LIMITED_API || CYTHON_AVOID_BORROWED_REFS || !CYTHON_ASSUME_SAFE_MACROS
other_failure:
#endif
    PyMem_Free(base_vtables);
    return -1;
}

