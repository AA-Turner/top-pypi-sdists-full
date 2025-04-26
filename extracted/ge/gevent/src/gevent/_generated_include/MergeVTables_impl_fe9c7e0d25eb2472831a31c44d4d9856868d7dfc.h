#if !CYTHON_COMPILING_IN_LIMITED_API
static int __Pyx_MergeVtables(PyTypeObject *type) {
    int i;
    void** base_vtables;
    __Pyx_TypeName tp_base_name;
    __Pyx_TypeName base_name;
    void* unknown = (void*)-1;
    PyObject* bases = type->tp_bases;
    int base_depth = 0;
    {
        PyTypeObject* base = type->tp_base;
        while (base) {
            base_depth += 1;
            base = base->tp_base;
        }
    }
    base_vtables = (void**) malloc(sizeof(void*) * (size_t)(base_depth + 1));
    base_vtables[0] = unknown;
    for (i = 1; i < PyTuple_GET_SIZE(bases); i++) {
        void* base_vtable = __Pyx_GetVtable(((PyTypeObject*)PyTuple_GET_ITEM(bases, i)));
        if (base_vtable != NULL) {
            int j;
            PyTypeObject* base = type->tp_base;
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
                base = base->tp_base;
            }
        }
    }
    PyErr_Clear();
    free(base_vtables);
    return 0;
bad:
    tp_base_name = __Pyx_PyType_GetName(type->tp_base);
    base_name = __Pyx_PyType_GetName((PyTypeObject*)PyTuple_GET_ITEM(bases, i));
    PyErr_Format(PyExc_TypeError,
        "multiple bases have vtable conflict: '" __Pyx_FMT_TYPENAME "' and '" __Pyx_FMT_TYPENAME "'", tp_base_name, base_name);
    __Pyx_DECREF_TypeName(tp_base_name);
    __Pyx_DECREF_TypeName(base_name);
    free(base_vtables);
    return -1;
}
#endif

