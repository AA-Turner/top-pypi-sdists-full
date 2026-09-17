static PyObject *__Pyx_GetItemInt_Generic(PyObject *o, PyObject* j) {
    PyObject *r;
    if (unlikely(!j)) return NULL;
    r = PyObject_GetItem(o, j);
    Py_DECREF(j);
    return r;
}
static PyObject *__Pyx_GetItemInt_Generic_size(PyObject *o, Py_ssize_t i) {
    return __Pyx_GetItemInt_Generic(o, PyLong_FromSsize_t(i));
}
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_List_Fast(PyObject *o, Py_ssize_t i,
                                                              int wraparound, int boundscheck, int unsafe_shared) {
    CYTHON_MAYBE_UNUSED_VAR(unsafe_shared);
#if CYTHON_AVOID_BORROWED_REFS
    CYTHON_UNUSED_VAR(boundscheck);
    Py_ssize_t wrapped_i = i;
    if (wraparound & unlikely(i < 0)) {
        Py_ssize_t size = __Pyx_PyList_GET_SIZE(o);
        #if !CYTHON_ASSUME_SAFE_SIZE
        if (unlikely(size < 0)) return NULL;
        #endif
        wrapped_i += size;
    }
    return __Pyx_PyList_GetItemRef(o, wrapped_i);
#elif CYTHON_ASSUME_SAFE_SIZE && CYTHON_ASSUME_SAFE_MACROS
    Py_ssize_t wrapped_i = i;
    Py_ssize_t size = (wraparound | boundscheck) ? PyList_GET_SIZE(o) : -1;
    if (wraparound & unlikely(i < 0)) {
        wrapped_i += size;
    }
    if ((!boundscheck) || likely(__Pyx_is_valid_index(wrapped_i, size))) {
        return __Pyx_PyList_GET_ITEM_REF(o, wrapped_i, unsafe_shared);
    }
    return __Pyx_GetItemInt_Generic_size(o, i);
#else
    (void)wraparound;
    (void)boundscheck;
    return PySequence_GetItem(o, i);
#endif
}
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_Tuple_Fast(PyObject *o, Py_ssize_t i,
                                                              int wraparound, int boundscheck, int unsafe_shared) {
    CYTHON_MAYBE_UNUSED_VAR(unsafe_shared);
#if CYTHON_AVOID_BORROWED_REFS
    CYTHON_UNUSED_VAR(boundscheck);
    Py_ssize_t wrapped_i = i;
    if (wraparound & unlikely(i < 0)) {
        Py_ssize_t size = __Pyx_PyTuple_GET_SIZE(o);
        #if !CYTHON_ASSUME_SAFE_SIZE
        if (unlikely(size < 0)) return NULL;
        #endif
        wrapped_i += size;
    }
    #if CYTHON_ASSUME_SAFE_MACROS && !CYTHON_COMPILING_IN_LIMITED_API
    return PySequence_ITEM(o, wrapped_i);
    #else
    if (unlikely(wrapped_i < 0)) {
        PyErr_SetString(PyExc_IndexError, "tuple index out of range");
        return NULL;
    }
    return PySequence_GetItem(o, wrapped_i);
    #endif
#elif CYTHON_ASSUME_SAFE_SIZE && CYTHON_ASSUME_SAFE_MACROS
    Py_ssize_t wrapped_i = i;
    Py_ssize_t size = (wraparound | boundscheck) ? PyTuple_GET_SIZE(o) : -1;
    if (wraparound & unlikely(i < 0)) {
        wrapped_i += size;
    }
    if ((!boundscheck) || likely(__Pyx_is_valid_index(wrapped_i, size))) {
        return __Pyx_NewRef(__Pyx_PyTuple_GET_ITEM(o, wrapped_i));
    }
    return __Pyx_GetItemInt_Generic_size(o, i);
#else
    (void)wraparound;
    (void)boundscheck;
    return PySequence_GetItem(o, i);
#endif
}
#if CYTHON_USE_TYPE_SLOTS && !CYTHON_COMPILING_IN_PYPY
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_Fast_mapping(PyObject *o, binaryfunc getitem, Py_ssize_t i) {
    PyObject *r, *key = PyLong_FromSsize_t(i);
    if (unlikely(!key)) return NULL;
    r = getitem(o, key);
    Py_DECREF(key);
    return r;
}
#endif
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_Fast(PyObject *o, Py_ssize_t i,
                                                     int wraparound, int boundscheck, int unsafe_shared) {
    CYTHON_MAYBE_UNUSED_VAR(unsafe_shared);
#if CYTHON_ASSUME_SAFE_SIZE
    if (PyList_CheckExact(o)) {
        return __Pyx_GetItemInt_List_Fast(o, i, wraparound, boundscheck, unsafe_shared);
    } else
    #if CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
    if (PyTuple_CheckExact(o)) {
        return __Pyx_GetItemInt_Tuple_Fast(o, i, wraparound, boundscheck, unsafe_shared);
    } else
    #endif
#else
    if ((!wraparound || i >= 0) & PyList_CheckExact(o)) {
        return boundscheck ? __Pyx_PyList_GetItemRef(o, i) : __Pyx_PyList_GET_ITEM_REF(o, i, unsafe_shared);
    } else
#endif
#if CYTHON_USE_TYPE_SLOTS && !CYTHON_COMPILING_IN_PYPY
    if (PyDict_CheckExact(o)) {
        return __Pyx_GetItemInt_Fast_mapping(o, PyDict_Type.tp_as_mapping->mp_subscript, i);
    #if defined(PyFrozenDict_CheckExact)
    } else if (PyFrozenDict_CheckExact(o)) {
        return __Pyx_GetItemInt_Fast_mapping(o, PyFrozenDict_Type.tp_as_mapping->mp_subscript, i);
    #endif
    } else
    {
        PyTypeObject *obj_type = Py_TYPE(o);
        int seq_or_mapping = __Pyx_PyType_GetFlags(obj_type) & (Py_TPFLAGS_SEQUENCE|Py_TPFLAGS_MAPPING);
        if (seq_or_mapping != Py_TPFLAGS_SEQUENCE) {
            PyMappingMethods *mm = obj_type->tp_as_mapping;
            if (mm && mm->mp_subscript)
                return __Pyx_GetItemInt_Fast_mapping(o, mm->mp_subscript, i);
        }
        PySequenceMethods *sm = obj_type->tp_as_sequence;
        if (likely(sm && sm->sq_item)) {
            if (wraparound && (i < 0) && unlikely(__Pyx_GetItemInt_wraparound(o, sm, &i) == -1))
                return NULL;
            return sm->sq_item(o, i);
        }
        if (seq_or_mapping == Py_TPFLAGS_SEQUENCE) {
            PyMappingMethods *mm = obj_type->tp_as_mapping;
            if (likely(mm && mm->mp_subscript))
                return __Pyx_GetItemInt_Fast_mapping(o, mm->mp_subscript, i);
        }
    }
#else
    if (!PyMapping_Check(o)) {
        return PySequence_GetItem(o, i);
    }
#endif
    (void)wraparound;
    (void)boundscheck;
    return __Pyx_GetItemInt_Generic_size(o, i);
}

